"""Relatório das falhas das dicas do Telegram (dados/relatorio_falhas.md), refeito a cada ronda de resultados.

Mostra onde as dicas publicadas acertam e falham (por mercado, liga, faixa de probabilidade e tipo de dica),
se as probabilidades estão bem calibradas, o que teriam dado as extra não publicadas, e os últimos Reds.
A Rotina 2 do agente lê-o para encontrar padrões; a dashboard mostra-o na página Lições."""
import datetime as dt
import json

import pandas as pd

from agente import config, db
from agente.recap import outcome

PATH = config.DATA_DIR / "relatorio_falhas.md"
FAMILIAS = [("cantos", "Cantos"), ("cartoes", "Cartões"), ("btts", "Ambas marcam"), ("combo:", "Combinadas"),
            ("over_", "Golos +/-"), ("under_", "Golos +/-"), ("placar", "Resultado exato"), ("marca", "Equipa marca"),
            ("sem_sofrer", "Não sofre")]
TIPOS = {None: "☀️ Manhã", "odd_alta": "💎 Odd alta", "tardia": "🌙 Tardia", "madrugada": "🌎 Américas"}


def familia(key: str) -> str:
    for pre, nome in FAMILIAS:
        if key.startswith(pre) or pre in key:
            return nome
    return "Dupla hipótese" if key in ("1X", "X2", "12") else "Resultado 1X2"


def _faixa(p: float) -> str:
    return "≥ 75%" if p >= .75 else "65-75%" if p >= .65 else "55-65%" if p >= .55 else "< 55%"


def _tabela(df: pd.DataFrame, col: str, minimo: int = 1) -> list[str]:
    g = df.groupby(col).agg(n=("ok", "size"), acerto=("ok", "mean"), esperado=("prob", "mean"))
    g = g[g["n"] >= minimo].sort_values("n", ascending=False)
    if g.empty:
        return ["_Sem dados ainda._"]
    out = [f"| {col.capitalize()} | Dicas | Acerto | Esperado | Leitura |", "|---|---|---|---|---|"]
    for k, r in g.iterrows():
        d = r["acerto"] - r["esperado"]
        leitura = "⏳ poucos dados" if r["n"] < 8 else "✅ bem" if abs(d) < .08 else \
            ("⬇️ confiança a mais" if d < 0 else "⬆️ confiança a menos")
        out.append(f"| {k} | {int(r['n'])} | {r['acerto']:.0%} | {r['esperado']:.0%} | {leitura} |")
    return out


def gerar() -> str | None:
    p_state = config.DATA_DIR / "telegram.json"
    if not p_state.exists():
        return None
    s = json.loads(p_state.read_text(encoding="utf-8"))
    pub = pd.DataFrame([d for d in s.get("dicas", []) if d.get("resultado") is not None and not d.get("anulada")])
    if pub.empty:
        return None
    preds = db.load_predictions().set_index("match_id")
    pub["ok"] = pub["resultado"].astype(bool)
    pub["mercado"] = pub["key"].map(familia)
    pub["liga"] = pub["match_id"].map(lambda m: preds.loc[m, "comp_name"] if m in preds.index else "?")
    pub["faixa"] = pub["prob"].map(_faixa)
    pub["tipo"] = pub.get("tipo", pd.Series([None] * len(pub))).map(lambda t: TIPOS.get(t if isinstance(t, str) else None, t))
    hoje = dt.date.today()
    linhas = [f"# Relatório das falhas (dicas do Telegram)", "",
              f"_Atualizado automaticamente a {dt.datetime.now():%d/%m/%Y %H:%M}. Só dicas publicadas e já decididas "
              f"(jogos adiados não contam)._", ""]
    for nome, dias in (("Últimos 7 dias", 7), ("Últimos 30 dias", 30), ("Desde o início", 10_000)):
        x = pub[pub["data"] >= (hoje - dt.timedelta(days=dias)).isoformat()]
        if not x.empty:
            linhas.append(f"- **{nome}:** {int(x['ok'].sum())} Green · {int((~x['ok']).sum())} Red → "
                          f"**{x['ok'].mean():.0%}** de acerto (o modelo esperava {x['prob'].mean():.0%}).")
    mult = [m for m in s.get("multiplas", []) if m.get("resultado") is not None]
    if mult:
        linhas.append(f"- **Múltiplas:** {sum(m['resultado'] for m in mult)} Green em {len(mult)}.")

    alertas = []
    for col in ("mercado", "liga", "faixa", "tipo"):
        g = pub.groupby(col).agg(n=("ok", "size"), acerto=("ok", "mean"), esperado=("prob", "mean"))
        for k, r in g[(g["n"] >= 8) & (g["acerto"] < g["esperado"] - .08)].iterrows():
            alertas.append(f"- ⚠️ **{k}** ({col}): acerto {r['acerto']:.0%} em {int(r['n'])} dicas, o modelo esperava "
                           f"{r['esperado']:.0%}.")
    linhas += ["", "## Alertas", *(alertas or ["- Nenhum grupo com 8+ dicas abaixo do esperado. 👌"])]
    for titulo, col in (("Por mercado", "mercado"), ("Por liga", "liga"), ("Por probabilidade", "faixa"),
                        ("Por tipo de dica", "tipo")):
        linhas += ["", f"## {titulo}", *_tabela(pub, col)]

    # extras que não foram publicadas: teriam ajudado?
    ex = []
    for x in s.get("pendentes", []):
        if x.get("extra") and x["estado"] != "publicada" and x["lista"] == "dicas":
            m = x["registo"]["match_id"]
            if m in preds.index and pd.notna(preds.loc[m, "hg"]):
                ok = outcome(x["registo"]["key"], preds.loc[m])
                if ok is not None:
                    ex.append(ok)
    if ex:
        linhas += ["", "## Extras não publicadas",
                   f"Das {len(ex)} apostas extra que ficaram por publicar, {sum(ex)} teriam dado Green "
                   f"(**{sum(ex) / len(ex):.0%}**), contra {pub['ok'].mean():.0%} das publicadas."]

    reds = pub[~pub["ok"]].sort_values("data", ascending=False).head(10)
    linhas += ["", "## Últimos Reds"]
    for d in reds.itertuples():
        r = preds.loc[d.match_id] if d.match_id in preds.index else None
        placar = f"{int(r['hg'])}-{int(r['ag'])}" if r is not None and pd.notna(r["hg"]) else "?"
        xg = ""
        if r is not None and pd.notna(r.get("hxg")):
            xg = f" · xG {r['hxg']:.1f}-{r['axg']:.1f}"
        linhas.append(f"- {d.data[8:10]}/{d.data[5:7]} · {d.jogo} **{placar}**{xg} · {d.texto} ({d.prob:.0%}, {d.mercado})")
    txt = "\n".join(linhas) + "\n"
    if not PATH.exists() or PATH.read_text(encoding="utf-8").split("\n", 3)[3:] != txt.split("\n", 3)[3:]:
        PATH.write_text(txt, encoding="utf-8")  # só reescreve se mudou algo além da hora
    return txt
