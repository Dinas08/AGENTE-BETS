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
from agente.model import estrela, label
from agente.recap import outcome

STATE = config.DATA_DIR / "telegram.json"
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
CHAT = os.getenv("TELEGRAM_CHAT_GRATIS", "").strip()
LINK = os.getenv("AFILIADO_LINK", "").strip()
CASA = os.getenv("AFILIADO_CASA", "").strip()

N_DICAS = 4                 # dicas por dia no canal grátis
P_MIN = 0.55                # probabilidade mínima da dica (abaixo disto é quase moeda ao ar)
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

def escolher(r) -> tuple[str, float] | None:
    """A dica de um jogo: a mesma da ⭐ da dashboard (a previsão mais segura), se tiver pelo menos P_MIN."""
    key = estrela(r["probs"], r["picks"])
    p = r["probs"].get(key) if key else None
    return (key, p) if p and p >= P_MIN else None


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
        om = 1.0
        for d in partes:
            om *= odd(d["odd_casa"], d["prob"])
        txt = "\n".join(f"• {E(d['jogo'])}: {E(d['texto'])} (@{odd(d['odd_casa'], d['prob']):.2f})" for d in partes)
        msg = f"🎯 <b>MÚLTIPLA DO DIA</b>\n\n{txt}\n\n💰 Odd total: <b>{om:.2f}</b>" + _fim()
        s["multiplas"].append({"data": hoje.isoformat(), "partes": [d["id"] for d in partes], "prob": round(pm, 4),
                               "message_id": send(msg), "resultado": None})
    _save(s)
    return len(novas)


N_TARDIAS = 2      # dicas extra por dia para os jogos da noite, ~45 min antes do início, com os onzes já conhecidos
N_MADRUGADA = 2    # dicas às 22h para os jogos entre as 00h e as 4h (Américas)
ROTACAO = 5        # alterações no onze em relação ao jogo anterior a partir das quais não damos dica


def _registar(s, r, key, prob, mid, dia, tipo) -> None:
    s["dicas"].append({"id": f"{r['match_id']}|{key}", "match_id": r["match_id"], "key": key,
                       "texto": texto(key, r["home"], r["away"]), "jogo": f"{r['home']} x {r['away']}",
                       "prob": round(prob, 4), "odd_casa": (r["odds"] or {}).get(key), "data": dia,
                       "message_id": mid, "resultado": None, "tipo": tipo})


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
    """Corre de 30 em 30 min: para jogos de hoje a partir das 18h que começam daqui a 20-75 min e ainda não
    tiveram dica, espera pelos onzes (até ~35 min antes) e publica, exceto se uma equipa rodar o onze."""
    agora = pd.Timestamp.now()
    hoje = hoje or agora.date()
    s = _load()
    feitas = sum(1 for d in s["dicas"] if d["data"] == hoje.isoformat() and (d.get("tipo") == "tardia" or d.get("tardia")))
    if feitas >= N_TARDIAS:
        return 0
    ignorados = s.setdefault("ignorados", [])
    ja = {d["match_id"] for d in s["dicas"]} | set(ignorados)
    p = db.load_predictions(with_results=False)
    p = p[(p["kickoff"] > agora + pd.Timedelta(minutes=20)) & (p["kickoff"] < agora + pd.Timedelta(minutes=75))
          & (p["kickoff"].dt.date == hoje) & (p["kickoff"].dt.hour >= 18) & ~p["limited"].astype(bool)
          & ~p["match_id"].isin(ja)]
    cands = sorted(((c[1], r, c[0]) for _, r in p.iterrows() if (c := escolher(r))), key=lambda x: -x[0])
    n = 0
    for prob, r, key in cands[:N_TARDIAS - feitas]:
        on = onzes(r)
        falta = (r["kickoff"] - agora).total_seconds() / 60
        if on is None and falta > 35:
            continue  # os onzes ainda não saíram: tenta na próxima execução
        if on and any(v is not None and v >= ROTACAO for v in on.values()):
            print(f"  {r['home']} x {r['away']}: onze muito rodado {on}, sem dica")
            ignorados.append(r["match_id"])
            continue
        extra = ""
        if on:
            mud = [f"{E(t)} {v} {'alteração' if v == 1 else 'alterações'}" for t, v in on.items() if v]
            extra = "📋 Onzes confirmados" + (f" ({'; '.join(mud)})" if mud else " (sem alterações)") + "\n"
        msg = mensagem_dica(r, key, prob).replace("\n\n📊", f"\n\n{extra}📊", 1)
        _registar(s, r, key, prob, send("🌙 <b>DICA TARDIA</b>\n\n" + msg), hoje.isoformat(), "tardia")
        n += 1
    _save(s)
    return n


def madrugada(hoje: dt.date | None = None) -> int:
    """Às 22h: dicas para os jogos entre as 00h e as 4h (Brasileirão, MLS, Liga MX, Argentina)."""
    agora = pd.Timestamp.now()
    hoje = hoje or agora.date()
    if hoje == agora.date() and agora.hour < 21:
        return 0
    s = _load()
    if any(d["data"] == hoje.isoformat() and d.get("tipo") == "madrugada" for d in s["dicas"]):
        return 0
    ja = {d["match_id"] for d in s["dicas"]}
    p = db.load_predictions(with_results=False)
    p = p[(p["kickoff"].dt.date == hoje + dt.timedelta(days=1)) & (p["kickoff"].dt.hour < 4)
          & (p["kickoff"] > agora) & ~p["limited"].astype(bool) & ~p["match_id"].isin(ja)]
    cands = sorted(((c[1], r, c[0]) for _, r in p.iterrows() if (c := escolher(r))), key=lambda x: -x[0])
    for prob, r, key in sorted(cands[:N_MADRUGADA], key=lambda x: x[1]["kickoff"]):
        _registar(s, r, key, prob, send("🌙 <b>MADRUGADA</b>\n\n" + mensagem_dica(r, key, prob)),
                  hoje.isoformat(), "madrugada")
    _save(s)
    return len(cands[:N_MADRUGADA])


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
        send(f"{'✅ <b>GREEN</b>' if ok else '❌ RED'}: {E(d['texto'])}\n{E(r['home'])} {int(r['hg'])}-{int(r['ag'])} "
             f"{E(r['away'])}", reply_to=d["message_id"])
        n += 1
    by_id = {d["id"]: d for d in s["dicas"]}
    for m in s["multiplas"]:
        if m["resultado"] is None:
            res = [by_id[i]["resultado"] for i in m["partes"] if i in by_id]
            if False in res or (res and None not in res):
                m["resultado"] = False not in res
                send("✅ <b>GREEN NA MÚLTIPLA!</b> 💰" if m["resultado"] else
                     f"❌ RED na múltipla ({sum(x is True for x in res)}/{len(res)} pernas)", reply_to=m["message_id"])
    resumo_dia(s)
    _save(s)
    return n


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
        if mult and mult[0]["resultado"]:
            linhas.append("🎯 Múltipla: GREEN 💰")
        send("\n".join(linhas) + _fim())
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
    com_odd = [d for d in sem if d.get("odd_casa")]
    if com_odd:
        lucro = sum((d["odd_casa"] - 1) if d["resultado"] else -1 for d in com_odd)
        linhas.append(f"💶 Dicas com odd das casas: {lucro:+.1f} unidades em {len(com_odd)} apostas de 1 unidade")
    linhas += ["", RODAPE]
    send("\n".join(linhas))
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
    """Responde a quem escreve ao bot em privado com o link do canal grátis. Só guarda a posição da fila
    (update_id), nunca nomes nem ids de pessoas."""
    if ensaio():
        return 0
    s = _load()
    r = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates",
                     params={"offset": s.get("offset", 0), "timeout": 0,
                             "allowed_updates": json.dumps(["message"])}, timeout=30).json()
    ups = r.get("result", [])
    if not ups:
        return 0
    link = link_canal()
    n = 0
    for u in ups:
        m = u.get("message") or {}
        if (m.get("chat") or {}).get("type") == "private" and link:
            txt = ("👋 Bem-vindo!\n\nAs dicas grátis do dia, a múltipla e os Greens saem todos os dias no canal:\n"
                   f"👉 {link}\n\n{RODAPE}")
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                          json={"chat_id": m["chat"]["id"], "text": txt, "disable_web_page_preview": True}, timeout=30)
            n += 1
    s["offset"] = ups[-1]["update_id"] + 1
    _save(s)
    return n
