"""Recap pós-jornada: o que o modelo acertou, o que falhou e porquê (explicações automáticas a partir do xG,
expulsões e probabilidades). O agente acrescenta depois a sua análise qualitativa ao ficheiro."""
import datetime as dt

import numpy as np
import pandas as pd

from agente import config, db
from agente.model import label

PICK_NAMES = {"resultado": "Resultado (1X2)", "dupla": "Dupla hipótese", "golos": "Golos +/-2.5",
              "ambas": "Ambas marcam", "cantos": "Cantos +/-9.5", "cartoes": "Cartões +/-4.5",
              "combinada": "Combinada"}


def outcome(key: str, r) -> bool | None:
    """True/False se o mercado `key` aconteceu no jogo `r`; None se faltam dados."""
    if key.startswith("combo:"):
        parts = [outcome(k, r) for k in key[6:].split("&")]
        return None if None in parts else all(parts)
    hg, ag = r["hg"], r["ag"]
    if pd.isna(hg):
        return None
    t = hg + ag
    simple = {"1": hg > ag, "X": hg == ag, "2": hg < ag, "1X": hg >= ag, "X2": hg <= ag, "12": hg != ag,
              "btts_sim": hg > 0 and ag > 0, "btts_nao": hg == 0 or ag == 0, "casa_marca": hg > 0,
              "fora_marca": ag > 0, "casa_sem_sofrer": ag == 0, "fora_sem_sofrer": hg == 0}
    if key in simple:
        return bool(simple[key])
    if key.startswith("placar_"):
        return key[7:] == f"{int(hg)}-{int(ag)}"
    if key in ("cantos_mais_casa", "cantos_mais_fora"):
        if pd.isna(r.get("hc")):
            return None
        return bool(r["hc"] > r["ac"]) if key.endswith("casa") else bool(r["hc"] < r["ac"])
    parts = key.split("_")
    if parts[0] in ("over", "under"):
        side, line, total = parts[0], float(parts[1]), t
    else:
        cols = ("hc", "ac") if parts[0] == "cantos" else ("hy", "ay")
        if pd.isna(r.get(cols[0])) or pd.isna(r.get(cols[1])):
            return None
        side, line, total = parts[1], float(parts[2]), r[cols[0]] + r[cols[1]]
    return bool(total > line) if side == "over" else bool(total < line)


def explain(r) -> list[str]:
    """Razões prováveis para o resultado divergir do previsto."""
    p, picks, home, away = r["probs"], r["picks"], r["home"], r["away"]
    why = []
    res = "1" if r["hg"] > r["ag"] else "X" if r["hg"] == r["ag"] else "2"
    if picks["resultado"] != res:
        pr = p.get(res, 0)
        if pr < 0.25:
            why.append(f"Surpresa: o modelo dava só {pr:.0%} a este desfecho.")
        if pd.notna(r.get("hxg")) and pd.notna(r.get("axg")):
            xh, xa = r["hxg"], r["axg"]
            xres = "1" if xh - xa > 0.4 else "2" if xa - xh > 0.4 else "X"
            if xres == picks["resultado"]:
                why.append(f"O xG ({xh:.1f}-{xa:.1f}) dava razão ao modelo: o resultado foi decidido por "
                           f"eficácia/sorte na finalização, não pelo domínio do jogo.")
            elif xres == res:
                why.append(f"O xG ({xh:.1f}-{xa:.1f}) confirma o resultado: o modelo sobrestimou "
                           f"{home if picks['resultado'] == '1' else away if picks['resultado'] == '2' else 'o equilíbrio'}.")
        e = r["expected"]
        why.append(f"Golos esperados pelo modelo: {e.get('golos_casa', 0):.1f}-{e.get('golos_fora', 0):.1f}.")
    for side, team in (("hr", home), ("ar", away)):
        if pd.notna(r.get(side)) and r[side] > 0:
            why.append(f"Cartão vermelho para {team} ({int(r[side])}) mudou o jogo.")
    if r.get("limited"):
        why.append("Previsão com dados limitados (equipa fora das ligas com histórico).")
    adj = r.get("adjustments") or {}
    if adj.get("notas"):
        why.append("Ajustes do agente aplicados: " + "; ".join(adj["notas"]))
    return why


def evaluate(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, r in df.iterrows():
        if pd.isna(r["hg"]):
            continue
        for kind, key in r["picks"].items():
            hit = outcome(key, r)
            if hit is None:
                continue
            rows.append({"match_id": r["match_id"], "tipo": kind, "mercado": key, "prob": r["probs"].get(key),
                         "acertou": hit, "odd": r["odds"].get(key)})
    return pd.DataFrame(rows)


def value_pnl(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, r in df.iterrows():
        if pd.isna(r["hg"]):
            continue
        for vb in r["value_bets"] or []:
            hit = outcome(vb["mercado"], r)
            if hit is None:
                continue
            rows.append({"match_id": r["match_id"], "kickoff": r["kickoff"], "mercado": vb["mercado"],
                         "odd": vb["odd_casa"], "prob": vb["prob"], "acertou": hit,
                         "lucro": vb["odd_casa"] - 1 if hit else -1.0})
    return pd.DataFrame(rows)


def brier_1x2(df: pd.DataFrame) -> float | None:
    d = df.dropna(subset=["hg"])
    if d.empty:
        return None
    s = []
    for _, r in d.iterrows():
        res = "1" if r["hg"] > r["ag"] else "X" if r["hg"] == r["ag"] else "2"
        s.append(sum((r["probs"][k] - (k == res)) ** 2 for k in ("1", "X", "2")))
    return float(np.mean(s))


def week_bounds(day: dt.date):
    start = day - dt.timedelta(days=day.weekday())
    return start, start + dt.timedelta(days=6)


def build_recap(day: dt.date | None = None) -> tuple[str, str] | None:
    """Gera o recap da semana (seg-dom) que contém `day` (por omissão, a semana passada)."""
    day = day or dt.date.today() - dt.timedelta(days=7)
    start, end = week_bounds(day)
    preds = db.load_predictions()
    if preds.empty:
        return None
    wk = preds[(preds["kickoff"].dt.date >= start) & (preds["kickoff"].dt.date <= end)].copy()
    done = wk.dropna(subset=["hg"])
    if done.empty:
        return None
    iso = start.isocalendar()
    name = f"{iso.year}-S{iso.week:02d}"
    ev = evaluate(done)
    pnl = value_pnl(done)

    L = [f"# Recap semana {iso.week} ({start:%d/%m} a {end:%d/%m/%Y})", "",
         f"Jogos avaliados: **{len(done)}** de {len(wk)} previstos.", ""]
    L.append("## Resumo por mercado\n")
    L.append("| Mercado | Acertos | Taxa | Prob. média prevista |")
    L.append("|---|---|---|---|")
    for kind, g in ev.groupby("tipo", sort=False):
        L.append(f"| {PICK_NAMES.get(kind, kind)} | {int(g['acertou'].sum())}/{len(g)} | "
                 f"{g['acertou'].mean():.0%} | {g['prob'].mean():.0%} |")
    b = brier_1x2(done)
    if b is not None:
        L.append(f"\nBrier score 1X2: **{b:.3f}** (0.667 = palpite aleatório; abaixo de 0.60 é bom).")
    if not pnl.empty:
        L.append(f"\nApostas de valor simuladas (1 unidade cada): {len(pnl)} apostas, "
                 f"{int(pnl['acertou'].sum())} ganhas, lucro **{pnl['lucro'].sum():+.2f} u** "
                 f"(ROI {pnl['lucro'].sum() / len(pnl):+.1%}).")

    L.append("\n## Jogo a jogo\n")
    for comp, g in done.sort_values("kickoff").groupby("comp_name", sort=False):
        L.append(f"### {comp}\n")
        for _, r in g.iterrows():
            e = ev[ev["match_id"] == r["match_id"]]
            hits = [f"{'✅' if x.acertou else '❌'} {label(x.mercado, r['home'], r['away'])} ({x.prob:.0%})"
                    for x in e.itertuples()]
            extra = []
            if pd.notna(r.get("hc")):
                extra.append(f"cantos {int(r['hc'])}-{int(r['ac'])}")
            if pd.notna(r.get("hxg")):
                extra.append(f"xG {r['hxg']:.1f}-{r['axg']:.1f}")
            L.append(f"**{r['home']} {int(r['hg'])}-{int(r['ag'])} {r['away']}**"
                     + (f" ({', '.join(extra)})" if extra else ""))
            L.append("- " + " · ".join(hits))
            for w in explain(r):
                L.append(f"  - {w}")
            L.append("")

    L.append("## Análise do agente\n")
    L.append("<!-- AGENTE: substituir esta linha pela análise qualitativa (o que correu bem, o que falhou e porquê, "
             "padrões a corrigir nos ajustes da próxima jornada). -->")
    text = "\n".join(L)
    path = config.RECAP_DIR / f"{name}.md"
    if path.exists():  # preservar análise já escrita pelo agente
        old = path.read_text(encoding="utf-8")
        if "## Análise do agente" in old and "<!-- AGENTE:" not in old:
            text = text.split("## Análise do agente")[0] + "## Análise do agente" + old.split("## Análise do agente", 1)[1]
    path.write_text(text, encoding="utf-8")
    return name, str(path)
