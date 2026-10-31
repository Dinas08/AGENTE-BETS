"""Canal de Telegram: publica as dicas do dia, a múltipla, os resultados (✅/❌) e o balanço semanal.

Corre no GitHub Actions (previsões → dicas e balanço; resultados → resultados). Sem TELEGRAM_BOT_TOKEN
só mostra as mensagens no ecrã (modo de ensaio). Nunca escreve dados pessoais: só jogos, probabilidades e o
link de afiliado configurado nos Secrets.
"""
import datetime as dt
import html
import json
import os

import pandas as pd
import requests

from agente import config, db
from agente.model import label
from agente.recap import outcome

STATE = config.DATA_DIR / "telegram.json"
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
CHAT = os.getenv("TELEGRAM_CHAT_GRATIS", "").strip()
LINK = os.getenv("AFILIADO_LINK", "").strip()
CASA = os.getenv("AFILIADO_CASA", "").strip()

N_DICAS = 4                 # dicas por dia no canal grátis
P_MIN, P_MAX = 0.55, 0.72   # probabilidade da dica: nem moeda ao ar, nem odd abaixo de ~1.40
MERCADOS = ("combinada", "golos", "ambas", "resultado", "dupla", "cartoes", "cantos")
FLAG = {"P1": "🇵🇹", "E0": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "D1": "🇩🇪", "I1": "🇮🇹", "UCL": "⭐", "UEL": "🟠", "UECL": "🟢",
        "TP": "🏆", "TL": "🏆", "FAC": "🏆", "EFL": "🏆", "DFB": "🏆", "CI": "🏆"}
DIAS = ["SEGUNDA", "TERÇA", "QUARTA", "QUINTA", "SEXTA", "SÁBADO", "DOMINGO"]
RODAPE = "🔞 +18 | Joga com responsabilidade | Probabilidades do modelo, não são garantias"
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
        dica = {"chat not found": "confirma TELEGRAM_CHAT_GRATIS (ex.: @nome_do_canal) e que o canal é público",
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

def escolher(r) -> tuple[str, float] | None:
    """A dica de um jogo: o palpite principal mais provável dentro de [P_MIN, P_MAX]."""
    best = None
    for m in MERCADOS:
        key = r["picks"].get(m)
        p = r["probs"].get(key) if key else None
        if p and P_MIN <= p <= P_MAX and (best is None or p > best[1]):
            best = (key, p)
    return best


def _razoes(r, key) -> list[str]:
    e, f = r["expected"], r["form"]
    out = [f"📊 Golos esperados: {E(r['home'])} {e['golos_casa']:.1f} – {E(r['away'])} {e['golos_fora']:.1f}"]
    for lado, team in (("casa", r["home"]), ("fora", r["away"])):
        x = f.get(lado) or {}
        if x.get("jogos"):
            v = x["seq"].count("V")
            xg = f", xG {x['xg']:.1f} contra {x['xga']:.1f}" if x.get("xg") is not None else ""
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


def mensagem_dica(r, key, p) -> str:
    ko = r["kickoff"]
    odd_casa = (r["odds"] or {}).get(key)
    linhas = [
        f"{FLAG.get(r['comp'], '⚽')} <b>{E(r['comp_name'].upper())} – {DIAS[ko.weekday()]} {ko:%d/%m}</b>",
        f"{E(r['home'])} x {E(r['away'])} | {ko:%Hh%M}",
        "",
        f"✅ <b>Dica: {E(texto(key, r['home'], r['away']))}</b>",
        f"📈 Probabilidade do agente: {p:.0%} (odd justa {1 / p:.2f}"
        + (f"; casas ≈ {odd_casa:.2f}" if odd_casa else "") + ")",
        "",
        *_razoes(r, key),
    ]
    return "\n".join(linhas) + _fim()


def dicas(hoje: dt.date | None = None) -> int:
    """Publica as dicas dos jogos de hoje (uma vez por dia) e a múltipla do dia."""
    hoje = hoje or dt.date.today()
    s = _load()
    if any(d["data"] == hoje.isoformat() for d in s["dicas"]):
        print("Dicas de hoje já publicadas.")
        return 0
    p = db.load_predictions(with_results=False)
    agora = pd.Timestamp.now()
    p = p[(p["kickoff"] > agora + pd.Timedelta(minutes=30)) & (p["kickoff"].dt.date == hoje) & ~p["limited"].astype(bool)]
    cands = []
    for _, r in p.iterrows():
        c = escolher(r)
        if c:
            cands.append((c[1], r, c[0]))
    cands = sorted(cands, key=lambda x: -x[0])[:N_DICAS]
    if not cands:
        print("Sem dicas para hoje.")
        return 0
    novas = []
    for prob, r, key in sorted(cands, key=lambda x: x[1]["kickoff"]):
        mid = send(mensagem_dica(r, key, prob))
        novas.append({"id": f"{r['match_id']}|{key}", "match_id": r["match_id"], "key": key,
                      "texto": texto(key, r["home"], r["away"]), "jogo": f"{r['home']} x {r['away']}",
                      "prob": round(prob, 4), "odd_casa": (r["odds"] or {}).get(key), "data": hoje.isoformat(),
                      "message_id": mid, "resultado": None})
    s["dicas"] += novas
    if len(novas) >= 2:
        partes = sorted(novas, key=lambda d: -d["prob"])[:3 if len(novas) >= 3 else 2]
        pm = 1.0
        for d in partes:
            pm *= d["prob"]
        if pm < 0.22 and len(partes) == 3:  # 3 pernas demasiado arriscadas: fica com as 2 mais seguras
            partes = partes[:2]
            pm = partes[0]["prob"] * partes[1]["prob"]
        txt = "\n".join(f"• {E(d['jogo'])}: {E(d['texto'])} ({d['prob']:.0%})" for d in partes)
        msg = (f"🎯 <b>MÚLTIPLA DO DIA</b>\n\n{txt}\n\n📈 Probabilidade do agente: {pm:.0%} "
               f"(odd justa {1 / pm:.2f})" + _fim())
        s["multiplas"].append({"data": hoje.isoformat(), "partes": [d["id"] for d in partes], "prob": round(pm, 4),
                               "message_id": send(msg), "resultado": None})
    _save(s)
    return len(novas)


# ------------------------------------------------------------------ resultados e balanço

def resultados() -> int:
    """Responde a cada dica (e múltipla) já decidida com ✅/❌ e o resultado final."""
    s = _load()
    pend = [d for d in s["dicas"] if d["resultado"] is None]
    if not pend:
        return 0
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
        send(f"{'✅ Certo' if ok else '❌ Falhou'}: {E(d['texto'])}\n{E(r['home'])} {int(r['hg'])}-{int(r['ag'])} "
             f"{E(r['away'])}", reply_to=d["message_id"])
        n += 1
    by_id = {d["id"]: d for d in s["dicas"]}
    for m in s["multiplas"]:
        if m["resultado"] is None:
            res = [by_id[i]["resultado"] for i in m["partes"] if i in by_id]
            if False in res or (res and None not in res):
                m["resultado"] = False not in res
                send(f"{'✅ Múltipla certa!' if m['resultado'] else '❌ Múltipla falhada'} "
                     f"({sum(x is True for x in res)}/{len(res)} pernas certas)", reply_to=m["message_id"])
    _save(s)
    return n


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
    esperado = sum(d["prob"] for d in sem)
    mult = [m for m in s["multiplas"] if ini <= m["data"] < hoje.isoformat() and m["resultado"] is not None]
    linhas = [f"📋 <b>BALANÇO DA SEMANA</b> ({(hoje - dt.timedelta(days=7)):%d/%m} – {(hoje - dt.timedelta(days=1)):%d/%m})",
              "", f"✅ {certas} certas | ❌ {len(sem) - certas} falhadas ({certas / len(sem):.0%})",
              f"📈 O modelo esperava {esperado:.1f} certas em {len(sem)}"]
    if mult:
        linhas.append(f"🎯 Múltiplas: {sum(m['resultado'] for m in mult)}/{len(mult)} certas")
    com_odd = [d for d in sem if d.get("odd_casa")]
    if com_odd:
        lucro = sum((d["odd_casa"] - 1) if d["resultado"] else -1 for d in com_odd)
        linhas.append(f"💶 Dicas com odd das casas: {lucro:+.1f} unidades em {len(com_odd)} apostas de 1 unidade")
    linhas += ["", "Publicamos todas as dicas, certas e erradas.", "", RODAPE]
    send("\n".join(linhas))
    s["balancos"].append(hoje.isoformat())
    _save(s)
    return True
