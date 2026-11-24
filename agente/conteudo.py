"""Conteúdo para as redes (TikTok, Instagram Reels, YouTube Shorts, X).

Fluxo automático:
1. A rotina de conteúdo do agente (Claude na nuvem) corre `run.py conteudo candidatos`, escolhe 1-2 temas,
   pesquisa e escreve o guião do vídeo em dados/videos/<AAAAMMDD>_<nome>.py (ver docs/conteudo_rotina.md).
2. O workflow "Resultados" (de 10 em 10 min) vê que há guiões pendentes e dispara o workflow "Vídeos".
3. O workflow "Vídeos" renderiza cada guião pendente e manda-o em privado aos admins do Telegram, com as
   legendas de cada rede e a hora sugerida. Os admins publicam à mão. Nada vai para o canal.
4. Uma vez por semana o Dinis manda os prints das analytics e o agente atualiza
   dados/conteudo/licoes_conteudo.md, que a rotina lê antes de escolher os temas.
"""
import datetime as dt
import importlib.util
import json
import os
import sys
from pathlib import Path

import requests

from . import config, db

VIDEOS = config.DATA_DIR / "videos"            # guiões escritos pela rotina (ramo de dados)
CONTEUDO = config.DATA_DIR / "conteudo"
REGISTO = CONTEUDO / "registo.json"            # o que já foi renderizado e enviado
MOTOR = config.ROOT / "docs" / "video"

GRANDES = ("benfica", "porto", "sporting", "sp lisbon")
PESO_PROVA = {"UCL": 60, "UNL": 35, "UEL": 35, "UECL": 25, "P1": 30, "E0": 30, "SP1": 28, "I1": 24, "D1": 24,
              "F1": 18, "N1": 12, "TACA": 25, "TL": 15}
# formatos para dias sem jogo forte (a rotina deve ir inovando e juntar outros)
IDEIAS = [
    "Melhor 11 da jornada da Liga Portugal (números do ESPN)",
    "Melhor 11 de sempre de um dos 3 grandes, com uma escolha polémica para gerar comentários",
    "Duelo de números: dois jogadores da mesma posição (golos, assistências, minutos)",
    "Quem está em melhor forma: Benfica, Porto ou Sporting (últimos 5 jogos, golos marcados/sofridos)",
    "Antevisão: o jogo grande da semana com a previsão do Agente Claudio (percentagens)",
    "O golo da semana explicado no quadro tático",
    "E se a Liga acabasse hoje? Tabela e quem desce",
    "Jogador sub-21 português que está a explodir (números)",
    "O padrão tático de uma equipa em 3 lances (como marca os golos)",
]


def _grande(nome: str) -> bool:
    n = (nome or "").lower()
    return any(g in n for g in GRANDES)


def _registo() -> dict:
    try:
        return json.loads(REGISTO.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"videos": {}}


def _guardar_registo(r: dict):
    CONTEUDO.mkdir(parents=True, exist_ok=True)
    REGISTO.write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")


def _dicas_certas() -> dict:
    """match_id -> textos das dicas publicadas no canal que acertaram (para o cartão do Agente)."""
    try:
        s = json.loads((config.DATA_DIR / "telegram.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    out = {}
    for d in s.get("dicas", []):
        if d.get("resultado") is True and d.get("message_id"):
            out.setdefault(d["match_id"], []).append(f"{d['texto']} (msg {d['message_id']})")
    return out


def candidatos(horas: int = 36, limite: int = 12) -> list[dict]:
    """Jogos acabados nas últimas `horas`, ordenados pelo potencial de views."""
    p = db.load_predictions()
    if p.empty:
        return []
    agora = dt.datetime.now()
    p = p[(p["kickoff"] >= agora - dt.timedelta(hours=horas)) & (p["kickoff"] <= agora) & p["hg"].notna()]
    certas = _dicas_certas()
    feitos = {v.get("match_id") for v in _registo()["videos"].values()}
    out = []
    for _, r in p.iterrows():
        hg, ag = int(r["hg"]), int(r["ag"])
        pr = r["probs"] or {}
        motivos, pts = [], PESO_PROVA.get(r["comp"], 5)
        if r["comp"] in config.AMERICAS:
            pts = 2
        if _grande(r["home"]) or _grande(r["away"]):
            pts += 100
            motivos.append("um dos 3 grandes")
        elif "Portugal" in (r["home"], r["away"]):
            pts += 90
            motivos.append("seleção de Portugal")
        if hg + ag >= 4:
            pts += 15
            motivos.append(f"{hg + ag} golos")
        ht = (r.get("hthg"), r.get("htag"))
        if all(x is not None and x == x for x in ht):
            hh, ha = int(ht[0]), int(ht[1])
            if (hh - ha) * (hg - ag) < 0:
                pts += 30
                motivos.append(f"reviravolta (intervalo {hh}-{ha})")
            elif hh != ha and hg == ag:
                pts += 12
                motivos.append(f"empate depois de {hh}-{ha} ao intervalo")
        vencedor = "1" if hg > ag else "2" if ag > hg else "X"
        pv = pr.get(vencedor)
        if pv is not None and vencedor != "X" and pv < 0.30:
            pts += 20
            motivos.append(f"surpresa (o modelo dava {pv:.0%})")
        elif pv is not None and pv >= 0.5:
            motivos.append(f"previsão do modelo certa ({pv:.0%})")
        if r["match_id"] in certas:
            pts += 15
            motivos.append("dica do canal certa: " + "; ".join(certas[r["match_id"]]))
        if r["match_id"] in feitos:
            continue
        out.append({"match_id": r["match_id"], "jogo": f"{r['home']} {hg}-{ag} {r['away']}",
                    "prova": r["comp_name"], "pontos": pts, "motivos": motivos,
                    "espn": r.get("espn_ref") or "", "kickoff": f"{r['kickoff']:%d/%m %H:%M}"})
    return sorted(out, key=lambda x: -x["pontos"])[:limite]


def proximos_grandes(dias: int = 3) -> list[str]:
    p = db.load_predictions(with_results=False)
    if p.empty:
        return []
    agora = dt.datetime.now()
    p = p[(p["kickoff"] >= agora) & (p["kickoff"] <= agora + dt.timedelta(days=dias))].sort_values("kickoff")
    out = []
    for _, r in p.iterrows():
        if _grande(r["home"]) or _grande(r["away"]) or r["comp"] in ("UCL",):
            pr = r["probs"] or {}
            out.append(f"[{r['match_id']}] {r['kickoff']:%d/%m %H:%M} {r['comp_name']}: {r['home']} vs {r['away']}"
                       f" (1 {pr.get('1', 0):.0%} X {pr.get('X', 0):.0%} 2 {pr.get('2', 0):.0%})")
    return out


def relatorio() -> str:
    """Texto para a rotina: candidatos de hoje, jogos grandes a seguir, últimos vídeos e ideias."""
    reg = _registo()["videos"]
    ult = sorted(reg.items(), key=lambda kv: kv[1].get("enviado_em", ""), reverse=True)[:10]
    linhas = ["# Candidatos a vídeo", ""]
    for c in candidatos():
        linhas.append(f"- **{c['jogo']}** · {c['prova']} · {c['kickoff']} · {c['pontos']} pts · "
                      f"{', '.join(c['motivos']) or '—'} · ESPN {c['espn']} · id {c['match_id']}")
    linhas += ["", "# Jogos dos 3 grandes e da Champions nos próximos 3 dias", ""]
    linhas += [f"- {x}" for x in proximos_grandes()] or ["- (nenhum)"]
    linhas += ["", "# Últimos vídeos (não repetir tema nem frase de fecho)", ""]
    linhas += [f"- {k}: {v.get('tipo', '')} · {v.get('tema', '')} · {v.get('enviado_em', '')}" for k, v in ult] or ["- (nenhum)"]
    linhas += ["", "# Ideias para dias sem jogo forte (inventa outras)", ""] + [f"- {i}" for i in IDEIAS]
    return "\n".join(linhas)


# ------------------------------------------------------------------ guiões pendentes, render e envio

def pendentes() -> list[Path]:
    feitos = _registo()["videos"]
    return sorted(p for p in VIDEOS.glob("*.py") if p.stem not in feitos and not p.name.startswith("_"))


def _carregar(guiao: Path):
    sys.path[:0] = [str(MOTOR), str(MOTOR / "jogos"), str(guiao.parent)]
    import quadro_tatico  # noqa: F401  (os guiões fazem "from quadro_tatico import ...")
    spec = importlib.util.spec_from_file_location(guiao.stem, guiao)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _tg(metodo: str, files=None, **dados) -> dict:
    from . import telegram
    token = telegram.ADMIN_TOKEN or telegram.TOKEN
    r = requests.post(f"https://api.telegram.org/bot{token}/{metodo}", data=dados, files=files, timeout=300)
    return r.json() if r.headers.get("content-type", "").startswith("application/json") else {"ok": False}


def _texto_posts(nome: str, posts: dict, hora: str) -> list[str]:
    """Uma mensagem por rede; o texto vai em <code> para copiar com um toque."""
    from html import escape as e
    yt = posts.get("youtube") or {}
    return [f"🎬 <b>{e(nome)}</b> · publicar às <b>{e(hora or '?')}</b> (sugestão)",
            f"<b>TikTok</b>\n<code>{e(posts.get('tiktok', ''))}</code>",
            f"<b>Instagram</b>\n<code>{e(posts.get('instagram', ''))}</code>",
            f"<b>YouTube Shorts</b>\nTítulo: <code>{e(yt.get('titulo', ''))}</code>\n"
            f"Descrição: <code>{e(yt.get('descricao', ''))}</code>",
            f"<b>X</b>\n<code>{e(posts.get('x', ''))}</code>"]


def enviar(guiao: Path, mp4: Path, capa: Path | None = None, voz: str = "") -> bool:
    """Manda o vídeo e as legendas de cada rede aos admins (em privado). Não publica em lado nenhum."""
    from . import telegram
    mod = _carregar(guiao)
    posts, hora = getattr(mod, "POSTS", {}), getattr(mod, "HORA", "")
    if not telegram.ADMINS:
        print(f"[ensaio] {guiao.stem}: sem TELEGRAM_ADMIN; não enviado")
        return False
    ok = True
    for chat in telegram.ADMINS:
        with open(mp4, "rb") as f:
            r = _tg("sendVideo", files={"video": (mp4.name, f, "video/mp4")}, chat_id=chat,
                    caption=f"🎬 {guiao.stem} · rascunho para as redes" + (f" · voz {voz}" if voz else ""), supports_streaming="true",
                    width="1080", height="1920")
        ok &= bool(r.get("ok"))
        if not r.get("ok"):
            print(f"Telegram recusou o vídeo: {r.get('description')}")
        if capa and capa.exists():
            with open(capa, "rb") as f:
                _tg("sendDocument", files={"document": (capa.name, f, "image/png")}, chat_id=chat,
                    caption="Capa (para o YouTube/Instagram)")
        for bloco in _texto_posts(guiao.stem, posts, hora):
            _tg("sendMessage", chat_id=chat, text=bloco, parse_mode="HTML")
    return ok


def marcar(guiao: Path, estado: str, dur: float | None = None, erro: str = "", voz: str = ""):
    mod = None
    try:
        mod = _carregar(guiao)
    except Exception as e:  # um guião partido também fica registado, para não tentar sem fim
        erro = erro or f"{type(e).__name__}: {e}"
    r = _registo()
    r["videos"][guiao.stem] = {"estado": estado, "enviado_em": dt.datetime.now().isoformat(timespec="minutes"),
                               "tipo": getattr(mod, "TIPO", ""), "tema": getattr(mod, "TEMA", ""),
                               "match_id": getattr(mod, "MATCH_ID", ""), "duracao": dur, "voz": voz, "erro": erro[:300]}
    _guardar_registo(r)


def processar() -> int:
    """Renderiza e envia todos os guiões pendentes (corre no workflow Vídeos)."""
    import subprocess
    n = 0
    saida = config.DATA_DIR.parent / "saida_videos"
    for g in pendentes():
        print(f"== {g.stem}")
        cmd = [sys.executable, str(MOTOR / "quadro_tatico.py"), str(g), "--saida", str(saida)]
        res = subprocess.run(cmd, capture_output=True, text=True, env={**os.environ, "PYTHONIOENCODING": "utf-8"})
        print(res.stdout[-2000:], res.stderr[-3000:])
        mp4 = saida / f"{g.stem}.mp4"
        if res.returncode != 0 or not mp4.exists():
            marcar(g, "erro", erro=res.stderr[-300:])
            from . import telegram
            for chat in telegram.ADMINS:
                _tg("sendMessage", chat_id=chat, text=f"⚠️ O vídeo {g.stem} falhou no render: {res.stderr[-300:]}")
            continue
        dur = None
        for linha in res.stdout.splitlines():
            if linha.startswith(f"{g.stem}.mp4:"):
                dur = float(linha.split(":")[1].strip().split()[0])
        log = res.stdout + res.stderr
        voz = ("Piper" if "a usar a Piper" in log else "Microsoft" if "a usar a voz da Microsoft" in log
               else "ElevenLabs" if os.environ.get("ELEVENLABS_API_KEY") else "Microsoft")
        enviado = enviar(g, mp4, saida / f"{g.stem}_capa.png", voz)
        marcar(g, "enviado" if enviado else "renderizado", dur, voz=voz)
        n += 1
    return n
