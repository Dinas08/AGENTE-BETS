"""Canal de Telegram: publica as dicas do dia, a múltipla, os resultados (✅/❌) e o balanço semanal.

Corre no GitHub Actions (previsões → dicas e balanço; resultados → resultados). Sem TELEGRAM_BOT_TOKEN
só mostra as mensagens no ecrã (modo de ensaio). Nunca escreve dados pessoais: só jogos, probabilidades e o
link de afiliado configurado nos Secrets.
"""
import datetime as dt
import html
import json
import os
import time

import pandas as pd
import requests

from agente import config, db
from agente.model import estrela, label
from agente.recap import outcome

STATE = config.DATA_DIR / "telegram.json"
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
CHAT = os.getenv("TELEGRAM_CHAT_GRATIS", "").strip()
LINK = os.getenv("AFILIADO_LINK", "").strip()
CASA = os.getenv("AFILIADO_CASA", "").strip()

N_DICAS = 4                 # dicas por dia no canal grátis (máximo)
N_MIN, P_RESERVA = 2, 0.55   # mínimo por dia: num dia fraco completa com as melhores acima de P_RESERVA
P_MIN = 0.62                # probabilidade mínima da dica (já calibrada; no histórico: 71% de acerto vs 68% com 0.55)
ODD_MIN = 1.20              # as casas não aceitam apostas abaixo desta odd (dicas e pernas das múltiplas)
TURBO_ODD = 4.0             # múltipla turbo: junta pernas até chegar a esta odd (máx. TURBO_PERNAS)
TURBO_PERNAS, TURBO_P_MIN = 5, 0.62
P_EXTRA = 0.50              # com admin: as outras apostas (não recomendadas) também vão para aprovação, como "extra"
FLAG = {"P1": "🇵🇹", "E0": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "D1": "🇩🇪", "I1": "🇮🇹", "BRA": "🇧🇷", "ARG": "🇦🇷", "MEX": "🇲🇽", "USA": "🇺🇸", "UCL": "⭐", "UEL": "🟠", "UECL": "🟢",
        "TP": "🏆", "TL": "🏆", "FAC": "🏆", "EFL": "🏆", "DFB": "🏆", "CI": "🏆"}
DIAS = ["SEGUNDA", "TERÇA", "QUARTA", "QUINTA", "SEXTA", "SÁBADO", "DOMINGO"]
RODAPE = "🔞 +18 | Joga com responsabilidade | Análise estatística, não são garantias"
E = html.escape


# ------------------------------------------------------------------ estado e envio

def _load() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {"dicas": [], "multiplas": [], "balancos": []}


def _save(s: dict):
    if ensaio():  # no ensaio não marca nada como publicado
        return
    STATE.write_text(json.dumps(s, ensure_ascii=False, indent=1), encoding="utf-8")


def ensaio() -> bool:
    return not (TOKEN and CHAT)


def send(text: str, reply_to: int | None = None) -> int | None:
    """Envia para o canal; devolve o id da mensagem. Em ensaio imprime e devolve None."""
    if ensaio():
        print("-" * 60 + "\n" + text)
        return None
    body = {"chat_id": CHAT, "text": text, "parse_mode": "HTML", "disable_web_page_preview": True}
    if reply_to:
        body |= {"reply_parameters": {"message_id": reply_to, "allow_sending_without_reply": True}}
    r = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json=body, timeout=30)
    if not r.ok:  # mensagem clara no registo do GitHub (sem mostrar o token)
        desc = r.json().get("description", r.text[:200]) if r.headers.get("content-type", "").startswith(
            "application/json") else r.text[:200]
        dica = {"send messages to the bot": "TELEGRAM_CHAT_GRATIS tem o @ do bot; tem de ser o @ do canal",
                "chat not found": "confirma TELEGRAM_CHAT_GRATIS (ex.: @nome_do_canal) e que o canal é público",
                "Unauthorized": "o TELEGRAM_BOT_TOKEN está errado",
                "not enough rights": "o bot tem de ser administrador do canal com 'Publicar mensagens'",
                "bot is not a member": "adiciona o bot ao canal como administrador"}
        raise SystemExit(f"Telegram recusou ({r.status_code}): {desc}. "
                         + next((v for k, v in dica.items() if k.lower() in desc.lower()), ""))
    return r.json()["result"]["message_id"]


def _link() -> str:
    if not LINK:
        return ""
    return f'👉 <a href="{E(LINK, quote=True)}">Fazer a aposta{" na " + E(CASA) if CASA else ""}</a>'


# ------------------------------------------------------------------ escolha das dicas

def escolher(r, p_min: float = P_MIN, excluir=()) -> tuple[str, float] | None:
    """A dica de um jogo: a ⭐ da dashboard (a previsão mais segura). As casas não aceitam odds abaixo de
    ODD_MIN: se a ⭐ ficar abaixo, usa a previsão seguinte mais segura do mesmo jogo que pague pelo menos isso."""
    cands = sorted(((k, r["probs"].get(k, 0)) for m, k in r["picks"].items()
                    if m in ("resultado", "golos", "ambas", "cantos") and k not in excluir), key=lambda x: -x[1])
    for key, p in cands:
        if p >= p_min and odd((r["odds"] or {}).get(key), p) >= ODD_MIN:
            return key, p
    return None


BOOST_P = (0.45, 0.65)      # perna "boost" da turbo: odd um pouco maior, mas ainda a previsão mais provável
BOOST_ODD = (1.65, 2.60)    # dentro desta faixa de odds
ODD_ALTA_MIN = 1.80         # dica de odd alta: pelo menos isto


def _boost_ok(key: str) -> bool:
    """Mercados coerentes para a perna boost: resultado, golos e ambas marcam (e combinações deles)."""
    return not any(x in key for x in ("placar", "cantos", "cartoes", "marca", "sem_sofrer", "under_0.5",
                                     "over_0.5", "over_4.5", "under_4.5")) and key != "X"


def boost(r, odd_min: float = BOOST_ODD[0]) -> tuple[str, float] | None:
    """A previsão mais provável do jogo cuja odd cai na faixa [odd_min, BOOST_ODD[1]] (perna boost da turbo e
    dica de odd alta)."""
    cands = []
    for key, p in r["probs"].items():
        o = odd((r["odds"] or {}).get(key), p) if p else 0
        if _boost_ok(key) and BOOST_P[0] <= p <= BOOST_P[1] and odd_min <= o <= BOOST_ODD[1]:
            cands.append((p, key))
    return (max(cands)[1], max(cands)[0]) if cands else None


def _razoes(r, key) -> list[str]:
    e, f = r["expected"], r["form"]
    out = [f"📊 Golos esperados: {E(r['home'])} {e['golos_casa']:.1f} – {E(r['away'])} {e['golos_fora']:.1f}"]
    for lado, team in (("casa", r["home"]), ("fora", r["away"])):
        x = f.get(lado) or {}
        if x.get("jogos"):
            v = x["seq"].count("V")
            xg = f", xG {x['xg']:.1f} contra {x['xga']:.1f}" if x.get("xg") else ""  # Américas: sem xG
            out.append(f"📊 {E(team)}: {v} {'vitória' if v == 1 else 'vitórias'} nos últimos {x['jogos']} jogos{xg}")
    aus = {}
    for a in r["injuries"] or []:
        if a.get("importancia") == "titular":
            aus.setdefault(a["equipa"], []).append(a["jogador"].split()[-1])
    for team, nomes in aus.items():
        out.append(f"🚑 {E(team)} sem {E(', '.join(nomes[:4]))}")
    return out[:5]


def texto(key, home, away) -> str:
    if key == "12":
        return f"{home} ou {away} vence (sem empate)"
    return label(key, home, away)


def _fim() -> str:
    return (f"\n{_link()}" if LINK else "") + f"\n\n{RODAPE}"


def odd(odd_casa, p) -> float:
    """Odd a mostrar: a das casas quando há; senão a odd justa do modelo."""
    return odd_casa or 1 / p


def linha_odd(odd_casa, p) -> str:
    return f"💰 Odd: <b>{odd(odd_casa, p):.2f}</b>" + ("" if odd_casa else " (mínima com valor)")


def mensagem_dica(r, key, p) -> str:
    ko = r["kickoff"]
    odd_casa = (r["odds"] or {}).get(key)
    linhas = [
        f"{FLAG.get(r['comp'], '⚽')} <b>{E(r['comp_name'].upper())} – {DIAS[ko.weekday()]} {ko:%d/%m}</b>",
        f"{E(r['home'])} x {E(r['away'])} | {ko:%Hh%M}",
        "",
        f"✅ <b>Dica: {E(texto(key, r['home'], r['away']))}</b>",
        linha_odd(odd_casa, p),
        "",
        *_razoes(r, key),
    ]
    return "\n".join(linhas) + _fim()


def dicas(hoje: dt.date | None = None) -> int:
    """Publica as dicas dos jogos de hoje (uma vez por dia) e a múltipla do dia."""
    hoje = hoje or dt.date.today()
    s = _load()
    if any(d["data"] == hoje.isoformat() for d in s["dicas"]) or _proposto(s, hoje.isoformat(), "dicas"):
        print("Dicas de hoje já publicadas (ou à espera de aprovação).")
        return 0
    p = db.load_predictions(with_results=False)
    agora = pd.Timestamp.now()
    p = p[(p["kickoff"] > agora + pd.Timedelta(minutes=30)) & (p["kickoff"].dt.date == hoje) & ~p["limited"].astype(bool)]
    cands = sorted(((c[1], r, c[0]) for _, r in p.iterrows() if (c := escolher(r))), key=lambda x: -x[0])[:N_DICAS]
    if len(cands) < N_MIN:  # dia fraco: completa até N_MIN com as melhores acima de P_RESERVA
        ja = {r["match_id"] for _, r, _ in cands}
        extra = sorted(((c[1], r, c[0]) for _, r in p.iterrows()
                        if r["match_id"] not in ja and (c := escolher(r, P_RESERVA))), key=lambda x: -x[0])
        cands += extra[:N_MIN - len(cands)]
    if not cands:
        print("Sem dicas para hoje.")
        return 0
    novas = []
    for prob, r, key in sorted(cands, key=lambda x: x[1]["kickoff"]):
        d = _dica(r, key, prob, hoje.isoformat())
        publicar(s, "dicas", d, mensagem_dica(r, key, prob), r["kickoff"], "dicas")
        novas.append(d)
    alta = _odd_alta(s, p, {d["match_id"] for d in novas}, hoje)
    partes = []
    if len(novas) >= 2:
        partes = sorted(novas, key=lambda d: -d["prob"])[:3 if len(novas) >= 3 else 2]
        if _prod(d["prob"] for d in partes) < 0.22 and len(partes) == 3:  # 3 pernas arriscadas: só as 2 mais seguras
            partes = partes[:2]
        _multipla(s, "🎯 <b>MÚLTIPLA DO DIA</b>", partes, hoje, "segura", p)
    turbo = _turbo(p, partes + ([alta] if alta else []), hoje)
    if turbo:
        _multipla(s, "🚀 <b>MÚLTIPLA TURBO</b>", turbo, hoje, "turbo", p)
    # com admin: todos os outros jogos do dia também vão, marcados como extra (não recomendados)
    usados = {d["match_id"] for d in novas + ([alta] if alta else [])}
    for _, r in p[~p["match_id"].isin(usados)].sort_values("kickoff").iterrows():
        if rever() and (c := escolher(r, P_EXTRA)):
            publicar(s, "dicas", _dica(r, c[0], c[1], hoje.isoformat()), mensagem_dica(r, c[0], c[1]),
                     r["kickoff"], "dicas", extra=True)
    pedir_aprovacao(s, hoje.isoformat())
    _save(s)
    return len(novas)


def _turbo(p: pd.DataFrame, dia: list, hoje) -> list:
    """Múltipla turbo sem repetir nenhuma aposta da múltipla do dia (e, se der, sem os mesmos jogos):
    uma perna boost (odd ~1.65-2.60, a mais provável dessa faixa) e o resto seguras até a odd chegar a TURBO_ODD."""
    usados = {d["match_id"] for d in dia}
    apostas = {d["id"] for d in dia}
    outros = p[~p["match_id"].isin(usados)].sort_values("kickoff")
    turbo = []
    bs = [(c[1], r, c[0]) for _, r in outros.iterrows() if (c := boost(r))]
    if bs:
        prob, r, key = max(bs, key=lambda x: x[0])
        turbo.append(_perna(r, key, prob, hoje))
    jogos = {d["match_id"] for d in turbo}
    seguras = [_perna(r, *c, hoje) for _, r in outros.iterrows()
               if r["match_id"] not in jogos and (c := escolher(r, TURBO_P_MIN))]
    # se faltarem jogos: outra aposta (nunca a mesma) dos jogos da múltipla do dia
    for _, r in p[p["match_id"].isin(usados)].iterrows():
        c = escolher(r, TURBO_P_MIN, excluir={a.split("|")[1] for a in apostas if a.startswith(r["match_id"] + "|")})
        if c:
            seguras.append(_perna(r, *c, hoje) | {"reserva": True})
    om = _prod(odd(d["odd_casa"], d["prob"]) for d in turbo)
    for d in sorted(seguras, key=lambda d: (d.get("reserva", False), -d["prob"])):
        if om >= TURBO_ODD or len(turbo) >= TURBO_PERNAS:
            break
        turbo.append(d)
        om *= odd(d["odd_casa"], d["prob"])
    return turbo if len(turbo) >= 2 and om >= 2.5 else []  # sai sempre que houver 2+ pernas com odd decente


def _prod(xs) -> float:
    out = 1.0
    for x in xs:
        out *= x
    return out


def _perna(r, key, prob, hoje) -> dict:
    return {"id": f"{r['match_id']}|{key}", "match_id": r["match_id"], "key": key,
            "texto": texto(key, r["home"], r["away"]), "jogo": f"{r['home']} x {r['away']}",
            "prob": round(prob, 4), "odd_casa": (r["odds"] or {}).get(key), "data": hoje.isoformat(),
            "porque": porque(r, key)}


RESULTADO = {"1": "casa", "1X": "casa", "2": "fora", "X2": "fora"}


def porque(r, key) -> str:
    """Fundamento curto de uma aposta (sem percentagens): golos esperados e, no resultado, a forma do favorito."""
    e, f = r["expected"], r["form"] or {}
    txt = f"golos esperados {e['golos_casa']:.1f} – {e['golos_fora']:.1f}"
    lado = RESULTADO.get(key.split("&")[0].replace("combo:", ""))
    x = f.get(lado) or {} if lado else {}
    if x.get("jogos"):
        team = r["home"] if lado == "casa" else r["away"]
        txt += f" · {team} {x['seq'].count('V')}V em {x['jogos']}"
    elif "cantos" in key and e.get("cantos_casa") is not None:
        txt = f"cantos esperados {e['cantos_casa'] + e['cantos_fora']:.1f}"
    return txt


def _texto_multipla(titulo, pernas) -> str:
    om = _prod(odd(d["odd_casa"], d["prob"]) for d in pernas)
    txt = "\n".join(f"• {E(d['jogo'])}: {E(d['texto'])} (@{odd(d['odd_casa'], d['prob']):.2f})"
                    + (f"\n   <i>↳ {E(d['porque'])}</i>" if d.get("porque") else "") for d in pernas)
    return f"{titulo}\n\n{txt}\n\n💰 Odd total: <b>{om:.2f}</b>" + _fim()


PERNA = ("id", "match_id", "key", "prob", "odd_casa", "jogo", "texto", "porque")


def _odd_alta(s, p: pd.DataFrame, usados: set, hoje) -> dict | None:
    """Uma dica por dia de odd mais alta (1.80-2.60): a mais provável dessa faixa, de preferência com valor
    (a odd da casa paga mais do que a probabilidade calibrada sugere). Fora dos jogos das outras dicas."""
    cands = []
    for _, r in p[~p["match_id"].isin(usados)].iterrows():
        if c := boost(r, ODD_ALTA_MIN):
            oc = (r["odds"] or {}).get(c[0])
            cands.append((bool(oc and c[1] * oc > 1.03), c[1], r, c[0]))
    if not cands:
        return None
    valor, prob, r, key = max(cands, key=lambda x: (x[0], x[1]))
    d = _dica(r, key, prob, hoje.isoformat(), "odd_alta")
    msg = mensagem_dica(r, key, prob)
    if valor:
        msg = msg.replace("\n\n📊", "\n💡 A odd paga mais do que o risco real deste jogo\n\n📊", 1)
    publicar(s, "dicas", d, "💎 <b>DICA DE ODD ALTA</b>\n\n" + msg, r["kickoff"], "dicas")
    return d


def _multipla(s, titulo, partes, hoje, tipo, p):
    pernas = [{k: d[k] for k in PERNA if k in d} for d in partes]
    m = {"data": hoje.isoformat(), "tipo": tipo, "titulo": titulo, "partes": [d["id"] for d in partes],
         "pernas": pernas, "prob": round(_prod(d["prob"] for d in partes), 4), "resultado": None}
    inicio = p[p["match_id"].isin([d["match_id"] for d in partes])]["kickoff"].min()
    publicar(s, "multiplas", m, _texto_multipla(titulo, pernas), inicio, "dicas")


N_TARDIAS = 2      # dicas extra por dia para os jogos da noite, ~45 min antes do início, com os onzes já conhecidos
N_MADRUGADA = 2    # dicas às 22h para os jogos entre as 00h e as 3h (Américas)
ROTACAO = 5        # alterações no onze em relação ao jogo anterior a partir das quais não damos dica


def _dica(r, key, prob, dia, tipo=None) -> dict:
    d = {"id": f"{r['match_id']}|{key}", "match_id": r["match_id"], "key": key,
         "texto": texto(key, r["home"], r["away"]), "jogo": f"{r['home']} x {r['away']}",
         "prob": round(prob, 4), "odd_casa": (r["odds"] or {}).get(key), "data": dia, "resultado": None}
    return d | ({"tipo": tipo} if tipo else {})


def onzes(r) -> dict | None:
    """Onzes confirmados (API-Football) e alterações de cada equipa face ao jogo anterior.
    None se ainda não saíram ou não há API."""
    from agente.sources import api_football as apif
    if not (apif.enabled() and pd.notna(r.get("apif_id"))):
        return None
    try:
        lu = apif.lineups(int(r["apif_id"]))
        if len(lu) < 2:
            return None
        out = {}
        for team in lu:
            xi = {p["player"]["id"] for p in team.get("startXI", [])}
            prev = apif.last_fixture(team["team"]["id"])
            antes = set()
            if prev:
                for t in apif.lineups(prev[0]["fixture"]["id"]):
                    if t["team"]["id"] == team["team"]["id"]:
                        antes = {p["player"]["id"] for p in t.get("startXI", [])}
            out[team["team"]["name"]] = len(xi - antes) if antes else None
        return out
    except Exception as e:  # quota, rede... publica sem onzes
        print(f"  [onzes] {e}")
        return None


def tardias(hoje: dt.date | None = None) -> int:
    """Corre de 10 em 10 min: para jogos de hoje a partir das 17h que começam daqui a 20-75 min e ainda não
    tiveram dica, espera pelos onzes (até ~35 min antes) e publica, exceto se uma equipa rodar o onze.
    Faz N_TARDIAS por noite: se os jogos que ainda faltam não chegarem com ≥ P_MIN, completa com ≥ P_RESERVA."""
    agora = pd.Timestamp.now()
    hoje = hoje or agora.date()
    s = _load()
    feitas = max(len([x for x in _proposto(s, hoje.isoformat(), "tardia") if not x.get("extra")]), sum(
        1 for d in s["dicas"] if d["data"] == hoje.isoformat() and (d.get("tipo") == "tardia" or d.get("tardia"))))
    if feitas >= N_TARDIAS and not rever():
        return 0
    ignorados = s.setdefault("ignorados", [])
    ja = {d["match_id"] for d in s["dicas"]} | set(ignorados) | _jogos_propostos(s, ("tardia", "madrugada"))
    p = db.load_predictions(with_results=False)
    p = p[(p["kickoff"].dt.date == hoje) & (p["kickoff"].dt.hour >= 17) & ~p["limited"].astype(bool)
          & ~p["match_id"].isin(ja)]
    janela = (p["kickoff"] > agora + pd.Timedelta(minutes=20)) & (p["kickoff"] < agora + pd.Timedelta(minutes=75))
    # jogos mais tarde esta noite que ainda podem dar uma dica forte: guardar-lhes a vaga
    depois = sum(1 for _, r in p[p["kickoff"] >= agora + pd.Timedelta(minutes=75)].iterrows() if escolher(r))
    vagas = max(0, N_TARDIAS - feitas)
    reserva = max(0, vagas - depois)
    fortes, fracas, resto = [], [], []
    for _, r in p[janela].iterrows():
        if c := escolher(r):
            fortes.append((c[1], r, c[0]))
        elif c := escolher(r, P_RESERVA):
            fracas.append((c[1], r, c[0]))
        elif c := escolher(r, P_EXTRA):
            resto.append((c[1], r, c[0]))
    fortes.sort(key=lambda x: -x[0])
    fracas.sort(key=lambda x: -x[0])
    cands = fortes + fracas[:reserva]
    extras = sorted(fracas[reserva:] + resto, key=lambda x: -x[0]) if rever() else []
    recomendaveis = {c[1]["match_id"] for c in cands}
    n = 0
    for prob, r, key in cands + extras:
        extra = n >= vagas or r["match_id"] not in recomendaveis
        on = onzes(r)
        falta = (r["kickoff"] - agora).total_seconds() / 60
        if on is None and falta > 35:
            continue  # os onzes ainda não saíram: tenta na próxima execução
        if on and any(v is not None and v >= ROTACAO for v in on.values()):
            print(f"  {r['home']} x {r['away']}: onze muito rodado {on}, sem dica")
            ignorados.append(r["match_id"])
            continue
        info = ""
        if on:
            mud = [f"{E(t)} {v} {'alteração' if v == 1 else 'alterações'}" for t, v in on.items() if v]
            info = "📋 Onzes confirmados" + (f" ({'; '.join(mud)})" if mud else " (sem alterações)") + "\n"
        msg = mensagem_dica(r, key, prob).replace("\n\n📊", f"\n\n{info}📊", 1)
        publicar(s, "dicas", _dica(r, key, prob, hoje.isoformat(), "tardia"), "🌙 <b>DICA TARDIA</b>\n\n" + msg,
                 r["kickoff"], "tardia", extra=extra)
        n += not extra
    _save(s)
    return n


def madrugada(hoje: dt.date | None = None) -> int:
    """Às 22h: dicas para os jogos entre as 00h e as 3h (Brasileirão, MLS, Liga MX, Argentina)."""
    agora = pd.Timestamp.now()
    hoje = hoje or agora.date()
    if hoje == agora.date() and agora.hour < 21:
        return 0
    s = _load()
    if (any(d["data"] == hoje.isoformat() and d.get("tipo") == "madrugada" for d in s["dicas"])
            or _proposto(s, hoje.isoformat(), "madrugada")):
        return 0
    ja = {d["match_id"] for d in s["dicas"]} | _jogos_propostos(s, ("tardia", "madrugada"))
    p = db.load_predictions(with_results=False)
    p = p[(p["kickoff"].dt.date == hoje + dt.timedelta(days=1)) & (p["kickoff"].dt.time <= dt.time(3, 0))
          & (p["kickoff"] > agora) & ~p["limited"].astype(bool) & ~p["match_id"].isin(ja)]
    cands = sorted(((c[1], r, c[0]) for _, r in p.iterrows() if (c := escolher(r))), key=lambda x: -x[0])
    for prob, r, key in sorted(cands[:N_MADRUGADA], key=lambda x: x[1]["kickoff"]):
        publicar(s, "dicas", _dica(r, key, prob, hoje.isoformat(), "madrugada"),
                 "🌙 <b>MADRUGADA</b>\n\n" + mensagem_dica(r, key, prob), r["kickoff"], "madrugada")
    if rever():  # as outras também, como extra
        rec = {r["match_id"] for _, r, _ in cands[:N_MADRUGADA]}
        for _, r in p[~p["match_id"].isin(rec)].sort_values("kickoff").iterrows():
            if c := escolher(r, P_EXTRA):
                publicar(s, "dicas", _dica(r, c[0], c[1], hoje.isoformat(), "madrugada"),
                         "🌙 <b>MADRUGADA</b>\n\n" + mensagem_dica(r, c[0], c[1]), r["kickoff"], "madrugada",
                         extra=True)
    _save(s)
    return len(cands[:N_MADRUGADA])


# ------------------------------------------------------------------ resultados e balanço

def resultados() -> int:
    """Responde a cada dica (e múltipla) já decidida com ✅/❌ e o resultado final."""
    s = _load()
    pend = [d for d in s["dicas"] if d["resultado"] is None]
    if pend or any(m["resultado"] is None for m in s["multiplas"]):
        p = db.load_predictions().set_index("match_id")
    n = 0
    for d in pend:
        if d["match_id"] not in p.index:
            continue
        r = p.loc[d["match_id"]]
        ok = outcome(d["key"], r)
        if ok is None:
            continue
        d["resultado"] = ok
        send(f"{'✅ <b>GREEN</b>' if ok else '❌ RED'}: {E(d['texto'])}\n{E(r['home'])} {int(r['hg'])}-{int(r['ag'])} "
             f"{E(r['away'])}", reply_to=d["message_id"])
        n += 1
    by_id = {d["id"]: d for d in s["dicas"]}
    for m in s["multiplas"]:
        if m["resultado"] is None:
            res = []
            for pe in m.get("pernas") or [{"id": i} for i in m["partes"]]:
                if pe["id"] in by_id:  # perna que também foi dica do dia
                    res.append(by_id[pe["id"]]["resultado"])
                elif pe.get("match_id") in p.index:  # perna só da múltipla (turbo)
                    res.append(outcome(pe["key"], p.loc[pe["match_id"]]))
                else:
                    res.append(None)
            if False in res or (res and None not in res):
                m["resultado"] = False not in res
                nome = "MÚLTIPLA TURBO" if m.get("tipo") == "turbo" else "MÚLTIPLA"
                send(f"✅ <b>GREEN NA {nome}!</b> 💰" if m["resultado"] else
                     f"❌ RED na {nome.lower()} ({sum(x is True for x in res)}/{len(res)} pernas certas até agora)",
                     reply_to=m["message_id"])
    resumo_dia(s)
    _save(s)
    return n


STAKE = 100  # simulação: 100 € em cada dica (e na múltipla), à odd publicada


def _lucro(dicas: list, mult: list, by_id: dict) -> tuple[float, int]:
    """Lucro simulado (€) e nº de apostas: green paga (odd - 1) × STAKE, red perde STAKE."""
    total = sum((odd(d["odd_casa"], d["prob"]) - 1) * STAKE if d["resultado"] else -STAKE for d in dicas)
    for m in mult:
        pernas = m.get("pernas") or [by_id[i] for i in m["partes"] if i in by_id]
        om = _prod(odd(pe["odd_casa"], pe["prob"]) for pe in pernas)
        total += (om - 1) * STAKE if m["resultado"] else -STAKE
    return total, len(dicas) + len(mult)


def _linha_lucro(total: float, n: int) -> list:
    """Só aparece quando houve lucro (nos dias maus não se mostra)."""
    return [f"💶 Lucro: <b>{total:+.0f} €</b>"] if round(total) > 0 else []  # com STAKE € em cada aposta (n apostas)


def resumo_dia(s: dict) -> bool:
    """Quando todas as dicas de um dia estão decididas: resumo curto (Greens e Reds; destaque se ≥ 80%)."""
    feitos = s.setdefault("resumos", [])
    agora = dt.datetime.now()
    for dia in sorted({d["data"] for d in s["dicas"]} - set(feitos)):
        if dia >= agora.date().isoformat():  # o dia só fecha depois das dicas tardias e de madrugada
            continue
        do_dia = [d for d in s["dicas"] if d["data"] == dia]
        mult = [m for m in s["multiplas"] if m["data"] == dia]
        if any(x["resultado"] is None for x in do_dia + mult):
            continue
        g = sum(d["resultado"] for d in do_dia)
        linhas = [f"📊 <b>RESUMO DE {dt.date.fromisoformat(dia):%d/%m}</b>", ""]
        if g / len(do_dia) >= 0.8:
            linhas.append(f"🔥 <b>DIA DE {g / len(do_dia):.0%} DE ACERTO!</b>")
        linhas.append(f"🟢 {g} Green" + (f" · 🔴 {len(do_dia) - g} Red" if g < len(do_dia) else ""))
        for m in mult:
            if m["resultado"]:
                linhas.append(("🚀 Múltipla turbo" if m.get("tipo") == "turbo" else "🎯 Múltipla") + ": GREEN 💰")
        linhas += _linha_lucro(*_lucro(do_dia, mult, {d["id"]: d for d in s["dicas"]}))
        if mid := send("\n".join(linhas) + _fim()):
            s["ultimo_resumo"] = mid  # o botão "Últimos resultados" das boas-vindas aponta para aqui
        feitos.append(dia)
        return True  # um por execução
    return False


def balanco(forcar: bool = False) -> bool:
    """À segunda-feira: balanço dos últimos 7 dias (acertos, falhas e o esperado pelo modelo)."""
    hoje = dt.date.today()
    s = _load()
    if not forcar and (hoje.weekday() != 0 or hoje.isoformat() in s["balancos"]):
        return False
    ini = (hoje - dt.timedelta(days=7)).isoformat()
    sem = [d for d in s["dicas"] if ini <= d["data"] < hoje.isoformat() and d["resultado"] is not None]
    if not sem:
        return False
    certas = sum(d["resultado"] for d in sem)
    mult = [m for m in s["multiplas"] if ini <= m["data"] < hoje.isoformat() and m["resultado"] is not None]
    linhas = [f"📋 <b>BALANÇO DA SEMANA</b> ({(hoje - dt.timedelta(days=7)):%d/%m} – {(hoje - dt.timedelta(days=1)):%d/%m})",
              "", f"🟢 {certas} Green · 🔴 {len(sem) - certas} Red"]
    if certas / len(sem) >= 0.8:
        linhas.append(f"🔥 {certas / len(sem):.0%} de acerto na semana!")
    if mult:
        linhas.append(f"🎯 Múltiplas: {sum(m['resultado'] for m in mult)} Green em {len(mult)}")
    linhas += _linha_lucro(*_lucro(sem, mult, {d["id"]: d for d in s["dicas"]}))
    linhas += ["", RODAPE]
    if mid := send("\n".join(linhas)):
        s["ultimo_resumo"] = mid
    s["balancos"].append(hoje.isoformat())
    _save(s)
    return True


# ------------------------------------------------------------------ mensagens privadas ao bot

def link_canal() -> str | None:
    """Link público do canal grátis (pelo @ do canal ou pelo link de convite)."""
    r = requests.get(f"https://api.telegram.org/bot{TOKEN}/getChat", params={"chat_id": CHAT}, timeout=30).json()
    c = r.get("result") or {}
    return f"https://t.me/{c['username']}" if c.get("username") else c.get("invite_link")


def privados() -> int:
    """Mensagens privadas e botões de aprovação, sem esperar (corre de 10 em 10 min nos resultados)."""
    return painel(0)


# ------------------------------------------------------------------ aprovação pelo admin (rascunhos)
#
# Com TELEGRAM_ADMIN (o id do Telegram do dono, só nos Secrets) as dicas, múltiplas, tardias e madrugada
# vão primeiro em privado para o admin como rascunho, com botões ✅ Publicar / ❌ Descartar. Para editar,
# o admin responde ao rascunho com o texto novo. Os Green/Red, resumos e balanços continuam automáticos.

ADMIN = os.getenv("TELEGRAM_ADMIN", "").strip()
# Bot só para os rascunhos (opcional). Com ele, o bot público passa a responder às pessoas na hora pelo
# Cloudflare Worker (bot/worker.js, webhook) e o GitHub Actions só lê a fila deste bot de admin.
ADMIN_TOKEN = os.getenv("TELEGRAM_ADMIN_BOT_TOKEN", "").strip()
PUBLICO = config.DATA_DIR / "bot_publico.json"  # textos e botões que o Worker usa para responder
MARCA = "———"  # separa o cabeçalho do rascunho do texto que vai para o canal
ESTADOS = {"publicada": "✅ <b>PUBLICADA</b>", "descartada": "❌ <b>DESCARTADA</b>",
           "expirada": "⌛ <b>EXPIROU</b> (o jogo já começou)",
           "substituida": "🔁 <b>SUBSTITUÍDA</b> (há uma proposta mais recente para este jogo)"}


def rever() -> bool:
    return bool(ADMIN) and not ensaio()


def _bot(metodo: str, _token: str | None = None, **body) -> dict:
    """Pedido ao bot de admin (rascunhos e botões); _token=TOKEN para responder em nome do bot público."""
    r = requests.post(f"https://api.telegram.org/bot{_token or ADMIN_TOKEN or TOKEN}/{metodo}", json=body, timeout=70)
    return r.json() if r.headers.get("content-type", "").startswith("application/json") else {}


def _proposto(s: dict, dia: str, origem: str) -> list:
    return [x for x in s.get("pendentes", []) if x["data"] == dia and x["origem"] == origem]


def _jogos_propostos(s: dict, extras_de=()) -> set:
    """Jogos já propostos como dica (os extra não contam, exceto os das origens em extras_de)."""
    return {x["registo"]["match_id"] for x in s.get("pendentes", [])
            if x["lista"] == "dicas" and (not x.get("extra") or x["origem"] in extras_de)}


def _cabecalho(x: dict) -> str:
    tipo = "📎 <b>EXTRA</b> (não ia meter)" if x.get("extra") else "📝 <b>RASCUNHO</b> ⭐ <b>recomendada</b>"
    return (f"{tipo} · expira às {pd.Timestamp(x['expira']):%Hh%M}\n"
            f"<i>Responde a esta mensagem com o texto novo para editar.</i>\n{MARCA}\n")


def _botoes(x: dict) -> dict:
    """Publicar/Descartar e 🔄 Trocar (pede a aposta por escrito); nas múltiplas, Trocar e ❌ Tirar em cada perna."""
    linhas = []
    if x["lista"] == "multiplas":
        for i, pe in enumerate(x["registo"]["pernas"]):
            linhas.append([{"text": f"🔄 {i + 1}. {pe.get('jogo', pe['match_id'])[:24]}", "callback_data": f"tr:{x['pid']}:{i}"},
                           {"text": f"❌ Tirar {i + 1}", "callback_data": f"rm:{x['pid']}:{i}"}])
    else:
        linhas.append([{"text": "🔄 Trocar aposta", "callback_data": f"tr:{x['pid']}:-1"}])
    linhas.append([{"text": "✅ Publicar", "callback_data": f"pub:{x['pid']}"},
                   {"text": "❌ Descartar", "callback_data": f"desc:{x['pid']}"}])
    return {"inline_keyboard": linhas}


def _mexer_perna(s: dict, x: dict, acao: str, i: int) -> str:
    m = x["registo"]
    if i >= len(m["pernas"]):
        return "Essa perna já não existe."
    if len(m["pernas"]) <= 2:  # ❌ Tirar (o 🔄 Trocar pede a aposta por escrito: _pedir_troca)
        return "Uma múltipla precisa de pelo menos 2 pernas."
    aviso = f"Tirei: {m['pernas'].pop(i)['jogo']}"
    m["partes"] = [pe["id"] for pe in m["pernas"]]
    m["prob"] = round(_prod(pe["prob"] for pe in m["pernas"]), 4)
    x["texto"] = _texto_multipla(m.get("titulo", "🎯 <b>MÚLTIPLA</b>"), m["pernas"])
    _bot("editMessageText", chat_id=ADMIN, message_id=x["admin_msg"], text=_cabecalho(x) + x["texto"],
         parse_mode="HTML", disable_web_page_preview=True, reply_markup=_botoes(x))
    return aviso


def _jogo(match_id: str):
    p = db.load_predictions(with_results=False)
    p = p[p["match_id"] == match_id]
    return None if p.empty else p.iloc[0]


def _alvo(x: dict, i: int) -> dict:
    """A aposta a trocar: a perna i da múltipla, ou a própria dica (i = -1)."""
    return x["registo"]["pernas"][i] if i >= 0 else x["registo"]


def _sugestoes(r, atual: str, n: int = 6) -> list[str]:
    cands = sorted(((k, pr) for k, pr in r["probs"].items() if k != atual and pr >= 0.45
                    and not k.startswith("placar_") and odd((r["odds"] or {}).get(k), pr) >= ODD_MIN),
                   key=lambda c: -c[1])[:n]
    return [f"{texto(k, r['home'], r['away'])} (@{odd((r['odds'] or {}).get(k), pr):.2f})" for k, pr in cands]


def _pedir_troca(s: dict, x: dict, i: int) -> str:
    """🔄 Trocar: pede ao admin que escreva a aposta que quer (em resposta à mensagem que o bot manda)."""
    if i >= 0 and i >= len(x["registo"].get("pernas", [])):
        return "Essa perna já não existe."
    alvo = _alvo(x, i)
    r = _jogo(alvo["match_id"])
    sug = "\n".join(f"• {E(t)}" for t in _sugestoes(r, alvo["key"])) if r is not None else ""
    casa = E(r["home"]) if r is not None else "casa"
    msg = (f"✍️ <b>Que aposta queres para {E(alvo['jogo'])}?</b>\nAgora: {E(alvo['texto'])}\n\n"
           f"Escreve-a em resposta a esta mensagem, por exemplo: <i>mais de 2.5 golos</i>, <i>ambas marcam</i>, "
           f"<i>vitória {casa}</i>, <i>1X</i>, <i>menos de 9.5 cantos</i>, <i>2-1</i>."
           + (f"\n\nSugestões:\n{sug}" if sug else ""))
    res = _bot("sendMessage", chat_id=ADMIN, text=msg, parse_mode="HTML",
               reply_parameters={"message_id": x["admin_msg"]},
               reply_markup={"force_reply": True, "input_field_placeholder": "ex.: mais de 2.5 golos"})
    if res.get("ok"):
        s["troca"] = {"pid": x["pid"], "i": i, "msg": res["result"]["message_id"]}
    return "Escreve a aposta que queres ✍️"


def _e_troca(s: dict, m: dict) -> bool:
    t = s.get("troca")
    return bool(t) and (m.get("reply_to_message") or {}).get("message_id") == t["msg"]


def _norm(t: str) -> str:
    import unicodedata
    t = unicodedata.normalize("NFKD", t.lower()).encode("ascii", "ignore").decode()
    return " ".join(t.replace(",", ".").split())


def interpretar(txt: str, r) -> str | None:
    """Texto escrito pelo admin -> chave do mercado (só mercados que o modelo calcula, para dar Green/Red)."""
    import difflib
    import re
    t = _norm(txt)
    probs = r["probs"]
    partes = [x for x in re.split(r"\s*\+\s*|\s+e\s+", t) if x]
    if len(partes) == 2:
        ks = [interpretar(x, r) for x in partes]
        if all(ks):
            for a, b in ((ks[0], ks[1]), (ks[1], ks[0])):
                if f"combo:{a}&{b}" in probs:
                    return f"combo:{a}&{b}"
        return None

    def lado() -> str | None:
        for nome, l in ((r["home"], "casa"), (r["away"], "fora")):
            pal = [w for w in _norm(nome).split() if len(w) >= 3 and w not in ("club", "sporting", "real", "united")]
            if _norm(nome) in t or any(re.search(rf"\b{re.escape(w)}", t) for w in pal):
                return l
        return "casa" if re.search(r"\bcasa\b", t) else "fora" if re.search(r"\bfora\b", t) else None

    k = None
    if m := re.fullmatch(r"(?:resultado exato |placar )?(\d+)\s*[-x:]\s*(\d+)", t):
        k = f"placar_{m[1]}-{m[2]}"
    elif m := re.search(r"(\d+\.5)", t):
        sob = re.search(r"\b(menos|under|u)\b|(^|\s)-\s*\d", t)
        tipo = "cantos_" if "canto" in t or "corner" in t else "cartoes_" if "cart" in t else ""
        k = f"{tipo}{'under' if sob else 'over'}_{m[1]}"
    elif "ambas" in t or "btts" in t or t in ("gg", "ng"):
        k = "btts_nao" if re.search(r"\b(nao|no|ng)\b", t) else "btts_sim"
    elif "mais cantos" in t and (l := lado()):
        k = f"cantos_mais_{l}"
    elif re.search(r"sem sofrer|nao sofre|clean", t) and (l := lado()):
        k = f"{l}_sem_sofrer"
    elif re.search(r"\bmarca\b", t) and (l := lado()):
        k = f"{l}_marca"
    elif t in ("1x", "x2", "12", "1", "2", "x"):
        k = t.upper()
    elif "sem empate" in t or "nao ha empate" in t:
        k = "12"
    elif "ou empate" in t or "dupla" in t:
        k = {"casa": "1X", "fora": "X2"}.get(lado())
    elif "empate" in t:
        k = "X"
    elif l := lado():
        k = "1" if l == "casa" else "2"
    if k in probs:
        return k
    nomes = {_norm(texto(c, r["home"], r["away"])): c for c in probs}
    perto = difflib.get_close_matches(t, list(nomes), n=1, cutoff=0.8)
    return nomes[perto[0]] if perto else None


def _trocar(s: dict, m: dict) -> None:
    t = s.pop("troca")
    x = next((x for x in s.get("pendentes", []) if x["pid"] == t["pid"] and x["estado"] == "pendente"), None)
    if x is None:
        _bot("sendMessage", chat_id=ADMIN, text="Esse rascunho já não está pendente.")
        return
    alvo = _alvo(x, t["i"])
    r = _jogo(alvo["match_id"])
    key = interpretar(m.get("text") or "", r) if r is not None else None
    if key is None:
        s["troca"] = t  # continua à espera
        sug = "\n".join(f"• {E(q)}" for q in _sugestoes(r, alvo["key"])) if r is not None else ""
        _bot("sendMessage", chat_id=ADMIN, parse_mode="HTML", reply_parameters={"message_id": t["msg"]},
             text="🤔 Não percebi essa aposta (ou o modelo não a calcula, e assim não dava para dar o Green/Red). "
                  "Responde outra vez à mensagem de cima." + (f"\n\nExemplos:\n{sug}" if sug else ""))
        return
    prob = r["probs"][key]
    if t["i"] >= 0:  # perna da múltipla
        mm = x["registo"]
        nova = _perna(r, key, prob, dt.date.fromisoformat(x["data"]))
        mm["pernas"][t["i"]] = {k: nova[k] for k in PERNA if k in nova}
        mm["partes"] = [pe["id"] for pe in mm["pernas"]]
        mm["prob"] = round(_prod(pe["prob"] for pe in mm["pernas"]), 4)
        x["texto"] = _texto_multipla(mm.get("titulo", "🎯 <b>MÚLTIPLA</b>"), mm["pernas"])
    else:  # dica simples: troca a linha da dica e a odd, mantém o resto da mensagem
        x["registo"] = x["registo"] | {k: v for k, v in _dica(r, key, prob, x["data"]).items() if k != "tipo"}
        linhas = []
        for ln in x["texto"].split("\n"):
            if ln.startswith("✅ <b>Dica:"):
                ln = f"✅ <b>Dica: {E(texto(key, r['home'], r['away']))}</b>"
            elif ln.startswith("💰 Odd:"):
                ln = linha_odd((r["odds"] or {}).get(key), prob)
            elif ln.startswith("💡 A odd paga mais"):
                continue
            linhas.append(ln)
        x["texto"] = "\n".join(linhas)
    _bot("editMessageText", chat_id=ADMIN, message_id=x["admin_msg"], text=_cabecalho(x) + x["texto"],
         parse_mode="HTML", disable_web_page_preview=True, reply_markup=_botoes(x))
    _bot("sendMessage", chat_id=ADMIN, reply_parameters={"message_id": x["admin_msg"]},
         text=f"🔄 Agora: {texto(key, r['home'], r['away'])} (@{odd((r['odds'] or {}).get(key), prob):.2f}, "
              f"{prob:.0%} pelo modelo). Carrega em ✅ Publicar quando estiver pronto.")


def publicar(s, lista, registo, msg, inicio, origem, extra: bool = False) -> None:
    """Sem admin publica já no canal; com admin manda o rascunho e só publica quando for aprovado.
    extra=True: aposta não recomendada, só vai para aprovação (sem admin não sai)."""
    if extra and not rever():
        return
    if rever():
        for y in s.get("pendentes", []):  # proposta nova para um jogo que tinha um extra à espera: substitui-o
            if (y["estado"] == "pendente" and y.get("extra") and y["lista"] == "dicas" == lista
                    and y["registo"]["match_id"] == registo.get("match_id")):
                _fechar(y, "substituida")
        x = {"pid": f"{dt.datetime.now():%d%H%M%S}{len(s.setdefault('pendentes', []))}", "origem": origem,
             "data": registo["data"], "lista": lista, "registo": registo | ({"extra": True} if extra else {}),
             "texto": msg, "expira": pd.Timestamp(inicio).isoformat(), "estado": "pendente"}
        if extra:
            x["extra"] = True
        r = _bot("sendMessage", chat_id=ADMIN, text=_cabecalho(x) + msg, parse_mode="HTML",
                 disable_web_page_preview=True, reply_markup=_botoes(x))
        if r.get("ok"):
            x["admin_msg"] = r["result"]["message_id"]
            s["pendentes"].append(x)
            return
        if extra:
            return
        print(f"  [admin] não consegui mandar o rascunho ({r.get('description')}); publico direto")
    s[lista].append(registo | {"message_id": send(msg)})


def pedir_aprovacao(s: dict, dia: str) -> None:
    """Depois das dicas da manhã: uma mensagem com 'Publicar todos' / 'Descartar todos'."""
    pend = [x for x in s.get("pendentes", []) if x["data"] == dia and x["estado"] == "pendente"]
    rec = sum(1 for x in pend if not x.get("extra"))
    if rever() and len(pend) >= 2:
        _bot("sendMessage", chat_id=ADMIN, text=f"📝 Hoje: {rec} recomendadas (⭐) e {len(pend) - rec} extra (📎) "
             "à espera da tua aprovação. Os extra só saem se carregares em ✅ Publicar neles.",
             reply_markup={"inline_keyboard": [[{"text": "✅ Publicar recomendadas", "callback_data": "pub:*"},
                                                {"text": "❌ Descartar tudo", "callback_data": "desc:*"}]]})


def _fechar(x: dict, estado: str) -> None:
    x["estado"] = estado
    if x.get("admin_msg"):
        _bot("editMessageText", chat_id=ADMIN, message_id=x["admin_msg"], parse_mode="HTML",
             disable_web_page_preview=True, text=f"{ESTADOS[estado]}\n{MARCA}\n{x['texto']}")


def _aprovar(s: dict, x: dict) -> None:
    s[x["lista"]].append(x["registo"] | {"message_id": send(x["texto"])})
    _fechar(x, "publicada")


def _html(texto: str, entidades) -> str:
    """Texto de uma mensagem do Telegram (com negrito, itálico, links) -> HTML para voltar a enviar."""
    b = texto.encode("utf-16-le")
    tags = {"bold": "b", "italic": "i", "underline": "u", "strikethrough": "s", "code": "code"}
    abre, fecha = {}, {}
    for e in entidades or []:
        if e["type"] == "text_link":
            a, f = f'<a href="{E(e["url"], quote=True)}">', "</a>"
        elif e["type"] in tags:
            a, f = f"<{tags[e['type']]}>", f"</{tags[e['type']]}>"
        else:
            continue
        abre.setdefault(e["offset"], []).append(a)
        fecha.setdefault(e["offset"] + e["length"], []).insert(0, f)
    cortes = sorted({0, len(b) // 2, *abre, *fecha})
    out = []
    for i, j in zip(cortes, cortes[1:] + [None]):
        out += fecha.get(i, []) + abre.get(i, [])
        if j is not None:
            out.append(E(b[2 * i:2 * j].decode("utf-16-le", errors="replace")))
    return "".join(out)


def _editar(s: dict, m: dict) -> None:
    alvo = (m.get("reply_to_message") or {}).get("message_id")
    x = next((x for x in s.get("pendentes", []) if alvo and x.get("admin_msg") == alvo), None)
    if x is None:
        n = sum(1 for x in s.get("pendentes", []) if x["estado"] == "pendente")
        _bot("sendMessage", chat_id=ADMIN, text=f"📝 {n} rascunho(s) à espera. Para editar, responde ao rascunho.")
        return
    if x["estado"] != "pendente":
        _bot("sendMessage", chat_id=ADMIN, text="Esse rascunho já não está pendente.")
        return
    novo = _html(m.get("text") or "", m.get("entities"))
    if MARCA in novo:  # copiou o rascunho inteiro, com o cabeçalho
        novo = novo.split(MARCA, 1)[1]
    novo = novo.strip() + ("" if RODAPE in novo else _fim())
    r = _bot("editMessageText", chat_id=ADMIN, message_id=x["admin_msg"], text=_cabecalho(x) + novo,
             parse_mode="HTML", disable_web_page_preview=True, reply_markup=_botoes(x))
    if r.get("ok"):
        x["texto"] = novo
        aviso = "✏️ Rascunho atualizado. Carrega em ✅ Publicar quando estiver pronto."
    else:
        aviso = f"Não consegui usar esse texto ({r.get('description', 'erro')})."
    _bot("sendMessage", chat_id=ADMIN, text=aviso, reply_parameters={"message_id": x["admin_msg"]})


# ------------------------------------------------------------------ boas-vindas e comandos públicos
#
# O bot só corre quando o GitHub Actions o acorda (10-60 min), por isso os botões das boas-vindas são todos
# links (abrem logo, sem esperar pelo bot): entrar no canal confirmando os 18+ e o último resumo/balanço do canal.
# Nada é guardado sobre as pessoas. Os botões "pb:" antigos (mensagens já enviadas) continuam a ser tratados.

OLA = ("👋 Olá! Bem-vindo ao <b>CLAUDIO BET TIPS FREE</b> ⚽🤖\n\n"
       "Todos os dias, dicas de futebol grátis escolhidas pelo <b>Agente Claudio</b>, que cruza estatística, "
       "odds e notícias (lesões, onzes) antes de cada jogo.\n\n")
IDADE = "🔞 <b>Só para maiores de 18.</b> Ao entrares no canal confirmas que tens 18 anos ou mais."
AGENDA = ("☀️ <b>10h30</b> — dicas do dia, 💎 odd alta e 🚀 múltipla turbo\n"
          "🌆 <b>À noite</b> — dicas com os onzes confirmados\n"
          "🌙 <b>22h</b> — madrugada (Brasil, Argentina, México, MLS)\n"
          "✅ Resultado de cada dica assim que o jogo acaba\n"
          "📋 <b>Segunda</b> — balanço da semana")
MENOR = "Este canal é só para maiores de 18. Volta quando chegar a hora — o futebol não foge! ⚽"
COMO = ("🤖 <b>COMO O AGENTE CLAUDIO ESCOLHE AS DICAS</b>\n\n"
        "1️⃣ <b>Números</b>: ataque e defesa de cada equipa, forma recente e golos esperados.\n"
        "2️⃣ <b>Mercado</b>: cruza tudo com as odds das casas.\n"
        "3️⃣ <b>Notícias</b>: lê lesões, castigos e onzes antes do jogo, e ajusta.\n"
        "4️⃣ <b>Aprende</b>: depois de cada jornada vê o que falhou e corrige.\n\n"
        "Liga Portugal 🇵🇹 · Premier 🏴󠁧󠁢󠁥󠁮󠁧󠁿 · Bundesliga 🇩🇪 · Serie A 🇮🇹 · Europa ⭐ · Taças 🏆 · Américas 🌙")
COMANDOS = {"/start": "ola", "/resultados": "res", "/comofunciona": "como"}


def _link_resultados(s: dict, link: str | None) -> str | None:
    """Link para o último resumo/balanço no canal (só dá com canal público, t.me/<nome>)."""
    msg = s.get("ultimo_resumo")
    if not (link and msg) or "/+" in link or "joinchat" in link:
        return None
    return f"{link.rstrip('/')}/{msg}"


def _menu(s: dict, link: str | None, entrar: str = "📢 Entrar no canal") -> dict | None:
    """Só botões de link: abrem logo, sem esperar que o bot volte a correr."""
    linhas = [[{"text": entrar, "url": link}]] if link else []
    if res := _link_resultados(s, link):
        linhas.append([{"text": "📊 Últimos resultados", "url": res}])
    return {"inline_keyboard": linhas} if linhas else None


def texto_entrada(link: str | None) -> str:
    entra = (f'👉 <a href="{E(link, quote=True)}">Entra aqui no canal</a>\n' if link else "")
    return (f"Bora! 🔥\n\n{AGENDA}\n\n{entra}Ativa as notificações 🔔 para não perderes nada.\n\n"
            "🔞 +18 | Joga com responsabilidade")


def texto_resultados(s: dict, dias: int = 7) -> str:
    """Greens e Reds das dicas fechadas nos últimos dias (os mesmos números do balanço de segunda)."""
    hoje = dt.date.today()
    ini = (hoje - dt.timedelta(days=dias)).isoformat()
    sem = [d for d in s["dicas"] if d["data"] >= ini and d["resultado"] is not None]
    if not sem:
        return "📊 Ainda não há dicas fechadas nos últimos 7 dias. Amanhã às 10h30 há mais! ⚽"
    mult = [m for m in s["multiplas"] if m["data"] >= ini and m["resultado"] is not None]
    g = sum(d["resultado"] for d in sem)
    linhas = [f"📊 <b>ÚLTIMOS {dias} DIAS NO CANAL</b>", "", f"🟢 {g} Green · 🔴 {len(sem) - g} Red"]
    if mult:
        linhas.append(f"🎯 Múltiplas: {sum(m['resultado'] for m in mult)} Green em {len(mult)}")
    linhas += _linha_lucro(*_lucro(sem, mult, {d["id"]: d for d in s["dicas"]})) + ["", RODAPE]
    return "\n".join(linhas)


def texto_publico(s: dict, acao: str, link: str | None) -> dict:
    """Texto e botões de uma resposta a uma pessoa: boas-vindas, entrada no canal, resultados ou como funciona."""
    if acao == "ola":
        msg = OLA + AGENDA + "\n\n" + IDADE
        botoes = _menu(s, link, "✅ Tenho 18+ · Entrar no canal")
    elif acao == "18":
        msg, botoes = texto_entrada(link), _menu(s, link)
    elif acao == "menor":
        msg, botoes = MENOR, None
    elif acao == "res":
        msg, botoes = texto_resultados(s), _menu(s, link)
    else:
        msg, botoes = COMO + "\n\n🔞 +18 | Joga com responsabilidade", _menu(s, link)
    return {"text": msg} | ({"reply_markup": botoes} if botoes else {})


def guardar_publico(s: dict, link: str | None) -> None:
    """Escreve bot_publico.json (lido pelo Worker do Cloudflare). Sem data/hora: só muda quando o texto muda."""
    d = {"textos": {a: texto_publico(s, a, link) for a in ("ola", "18", "menor", "res", "como")}}
    novo = json.dumps(d, ensure_ascii=False, indent=1)
    if not PUBLICO.exists() or PUBLICO.read_text(encoding="utf-8") != novo:
        PUBLICO.write_text(novo, encoding="utf-8")


def _publico(s: dict, chat: int, acao: str, link: str | None, editar: int | None = None) -> None:
    """Resposta a uma pessoa pelo GitHub Actions (só sem bot de admin; com ele responde o Worker)."""
    corpo = {"chat_id": chat, "parse_mode": "HTML", "disable_web_page_preview": True} | texto_publico(s, acao, link)
    if editar and acao in ("18", "menor"):  # substitui a pergunta da idade (tira os botões)
        r = _bot("editMessageText", TOKEN, message_id=editar, **corpo)
        if r.get("ok"):
            return
    _bot("sendMessage", TOKEN, **corpo)


def _botao(s: dict, cb: dict, link: str | None = None) -> int:
    acao, _, pid = (cb.get("data") or "").partition(":")
    if acao == "pb":  # botões públicos (boas-vindas)
        _bot("answerCallbackQuery", TOKEN, callback_query_id=cb["id"])
        m = cb.get("message") or {}
        _publico(s, (m.get("chat") or {}).get("id", cb["from"]["id"]), pid, link, m.get("message_id"))
        return 1
    if str(cb["from"]["id"]) != ADMIN:
        _bot("answerCallbackQuery", callback_query_id=cb["id"], text="Sem permissão.")
        return 0
    if acao in ("tr", "rm"):  # trocar / tirar uma perna da múltipla
        pid, _, i = pid.partition(":")
        x = next((x for x in s.get("pendentes", []) if x["pid"] == pid and x["estado"] == "pendente"), None)
        if x and acao == "tr":
            aviso = _pedir_troca(s, x, int(i))
        else:
            aviso = _mexer_perna(s, x, acao, int(i)) if x else "Já não está pendente."
        _bot("answerCallbackQuery", callback_query_id=cb["id"], text=aviso[:190])
        return 1 if x else 0
    alvos = [x for x in s.get("pendentes", []) if x["estado"] == "pendente"
             and (pid == x["pid"] or (pid == "*" and not (acao == "pub" and x.get("extra"))))]
    for x in alvos:
        _aprovar(s, x) if acao == "pub" else _fechar(x, "descartada")
    feito = "publicado" if acao == "pub" else "descartado"
    _bot("answerCallbackQuery", callback_query_id=cb["id"],
         text=f"{len(alvos)} {feito}(s)" if alvos else "Já não está pendente.")
    return len(alvos)


def _expirar(s: dict) -> None:
    agora = pd.Timestamp.now()
    for x in s.get("pendentes", []):
        if x["estado"] == "pendente" and pd.Timestamp(x["expira"]) <= agora:
            _fechar(x, "expirada")


def painel(minutos: float = 0) -> int:
    """Lê as mensagens privadas e os botões do bot. Com minutos > 0 e rascunhos pendentes, fica à escuta
    (long polling) para o admin aprovar em tempo real. Só guarda a posição da fila, nunca dados de pessoas
    (o id do admin vem dos Secrets)."""
    if ensaio():
        return 0
    s = _load()
    lim = (dt.date.today() - dt.timedelta(days=3)).isoformat()
    s["pendentes"] = [x for x in s.get("pendentes", []) if x["data"] >= lim]
    fim, n = time.time() + minutos * 60, 0
    try:
        link = link_canal()
    except Exception:  # sem rede: fica sem botão de link desta vez
        link = None
    guardar_publico(s, link)
    fila = "offset_admin" if ADMIN_TOKEN else "offset"  # cada bot tem a sua fila de mensagens
    while True:
        _expirar(s)
        pend = any(x["estado"] == "pendente" for x in s["pendentes"])
        espera = max(0, int(min(50, fim - time.time()))) if pend else 0
        ups = _bot("getUpdates", offset=s.get(fila, 0), timeout=espera,
                   allowed_updates=["message", "callback_query"]).get("result", [])
        for u in ups:
            cb = u.get("callback_query")
            if cb:
                n += _botao(s, cb, link)
                continue
            m = u.get("message") or {}
            chat = (m.get("chat") or {})
            if chat.get("type") != "private":
                continue
            cmd = (m.get("text") or "").strip().split()[0].split("@")[0].lower() if (m.get("text") or "").strip() else ""
            if cmd == "/id":
                _bot("sendMessage", chat_id=chat["id"], text=f"O teu id do Telegram: {chat['id']}")
            elif ADMIN and str(chat["id"]) == ADMIN and _e_troca(s, m):
                _trocar(s, m)
            elif ADMIN and str(chat["id"]) == ADMIN and (ADMIN_TOKEN or cmd not in COMANDOS):
                _editar(s, m)
            elif ADMIN_TOKEN:  # o bot de admin não é para o público
                continue
            else:
                _publico(s, chat["id"], COMANDOS.get(cmd, "ola"), link)
            n += 1
        if ups:
            s[fila] = ups[-1]["update_id"] + 1
        _save(s)
        if not (espera and time.time() < fim):
            return n
