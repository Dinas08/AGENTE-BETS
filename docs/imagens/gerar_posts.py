"""Imagens para posts (X, Reddit, Instagram...) a partir dos resultados REAIS do canal.

Usa o estado do bot (telegram.json) e a base de dados (agente.db) do ramo claude/dados:
    git show origin/claude/dados:telegram.json > tg.json
    git show origin/claude/dados:agente.db > agente.db
    .venv\\Scripts\\python.exe docs\\imagens\\gerar_posts.py tg.json agente.db [AAAA-MM-DD início] [AAAA-MM-DD fim]

Gera em docs/imagens/posts/: um cartão por Green, um por múltipla Green e o balanço do período.
A simulação em € só entra no balanço se o acumulado do período for positivo (nunca se escolhe a janela a dedo:
o período é o que se passa na linha de comandos, por omissão desde o início).
"""
import datetime as dt
import json
import sqlite3
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from agente.telegram import STAKE, _lucro, _prod, odd  # noqa: E402

AQUI = Path(__file__).parent / "posts"
F = "C:/Windows/Fonts/"
K = 2                      # desenha a 2x e reduz (bordas suaves)
W = H = 1080               # quadrado: serve no X, Reddit, Instagram e Telegram

FUNDO, FUNDO2 = (20, 20, 19), (38, 35, 32)
CREME, CREME_70, CREME_45 = (250, 249, 245), (190, 188, 182), (130, 128, 122)
CORAL, CORAL_CLARO = (217, 119, 87), (240, 150, 112)
VERDE, VERMELHO = (126, 196, 132), (224, 92, 82)
MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]


def fonte(nome, tam):
    return ImageFont.truetype(F + nome, int(tam * K))


SERIFA, SERIFA_N = "pala.ttf", "palab.ttf"
SANS, SANS_SB, SANS_B = "segoeui.ttf", "seguisb.ttf", "segoeuib.ttf"


class Cartao:
    def __init__(self):
        self.im = Image.new("RGB", (W * K, H * K), FUNDO)
        d = ImageDraw.Draw(self.im)
        for i in range(90, 0, -1):  # respiro de luz quente ao centro
            t = i / 90
            r = W * K * 0.78 * t
            cor = tuple(int(FUNDO2[k] + (FUNDO[k] - FUNDO2[k]) * t) for k in range(3))
            d.ellipse((W * K / 2 - r, H * K * 0.42 - r, W * K / 2 + r, H * K * 0.42 + r), fill=cor)
        self.d = ImageDraw.Draw(self.im)

    # utilitários em coordenadas de 1080
    def texto(self, xy, s, f, cor, anchor="la", esp=0):
        x, y = xy
        if not esp:
            self.d.text((x * K, y * K), s, font=f, fill=cor, anchor=anchor)
            return
        larg = sum(self.d.textlength(c, font=f) + esp * K for c in s) - esp * K
        x0 = x * K - (larg / 2 if anchor[0] == "m" else larg if anchor[0] == "r" else 0)
        for c in s:
            self.d.text((x0, y * K), c, font=f, fill=cor, anchor="l" + anchor[1])
            x0 += self.d.textlength(c, font=f) + esp * K

    def largura(self, s, f):
        return self.d.textlength(s, font=f) / K

    def caber(self, s, nome, tam, maxw):
        while tam > 18 and self.largura(s, fonte(nome, tam)) > maxw:
            tam -= 2
        return fonte(nome, tam)

    def ret(self, box, cor, raio=0, contorno=None, w=0):
        b = tuple(v * K for v in box)
        self.d.rounded_rectangle(b, radius=raio * K, fill=cor, outline=contorno, width=w * K)

    def linha(self, a, b, cor, w=1):
        self.d.line((a[0] * K, a[1] * K, b[0] * K, b[1] * K), fill=cor, width=int(w * K))

    def circulo(self, c, r, cor=None, contorno=None, w=0):
        self.d.ellipse(((c[0] - r) * K, (c[1] - r) * K, (c[0] + r) * K, (c[1] + r) * K), fill=cor,
                       outline=contorno, width=int(w * K))

    def visto(self, c, tam, cor, w=6):
        x, y = c
        pts = [(x - tam * 0.45, y + tam * 0.02), (x - tam * 0.12, y + tam * 0.33), (x + tam * 0.48, y - tam * 0.32)]
        self.d.line([(px * K, py * K) for px, py in pts], fill=cor, width=int(w * K), joint="curve")

    def cruz(self, c, tam, cor, w=6):
        x, y, t = c[0], c[1], tam * 0.32
        self.linha((x - t, y - t), (x + t, y + t), cor, w)
        self.linha((x - t, y + t), (x + t, y - t), cor, w)

    # blocos da marca
    def cabecalho(self, direita: str):
        f = fonte(SERIFA_N, 50)
        self.texto((72, 86), "C", f, CREME, "lm")
        x0, y0, x1, y1 = self.d.textbbox((72 * K, 86 * K), "C", font=f, anchor="lm")
        # no "olho" do C, como na foto do canal
        self.circulo((x0 / K + (x1 - x0) / K * 0.60, (y0 + y1) / 2 / K), 5, CORAL)
        self.texto((122, 88), "CLAUDIO", fonte(SERIFA_N, 25), CREME, "lm", esp=7)
        self.texto((W - 72, 88), direita.upper(), fonte(SANS_SB, 20), CREME_70, "rm", esp=3)
        self.linha((72, 140), (W - 72, 140), (60, 57, 53), 1.5)

    def rodape(self, nota: str = ""):
        self.linha((72, 960), (W - 72, 960), (60, 57, 53), 1.5)
        self.texto((72, 1006), "Dicas grátis todos os dias no Telegram", fonte(SANS_SB, 23), CREME, "lm")
        if nota:
            self.texto((72, 1040), nota, fonte(SANS, 17), CREME_45, "lm")
        f = fonte(SANS, 19)
        x = W - 72 - self.largura("Joga com responsabilidade", f)
        self.texto((W - 72, 1006), "Joga com responsabilidade", f, CREME_70, "rm")
        self.circulo((x - 34, 1006), 22, None, CORAL, 2.5)
        self.texto((x - 34, 1007), "18+", fonte(SANS_B, 16), CORAL, "mm")

    def selo(self, c, txt, cor, ok=True):
        f = fonte(SANS_B, 30)
        lw = self.largura(txt, f) + 4 * (len(txt) - 1) + 120
        x, y = c
        self.ret((x - lw / 2, y - 36, x + lw / 2, y + 36), None, 36, cor, 3)
        ic = (x - lw / 2 + 46, y)
        self.circulo(ic, 21, cor)
        (self.visto if ok else self.cruz)(ic, 26, FUNDO, 5)
        self.texto((x - lw / 2 + 82, y + 1), txt, f, cor, "lm", esp=4)

    def guardar(self, nome):
        AQUI.mkdir(parents=True, exist_ok=True)
        self.im.resize((W, H), Image.LANCZOS).save(AQUI / f"{nome}.png")
        return AQUI / f"{nome}.png"


# ------------------------------------------------------------------ dados

def carregar(tg, db):
    s = json.load(open(tg, encoding="utf-8"))
    c = sqlite3.connect(db)
    jogos = {}
    for mid, comp, home, away, ko, hg, ag in c.execute(
            "SELECT p.match_id, p.comp_name, p.home, p.away, p.kickoff, r.hg, r.ag FROM predictions p "
            "LEFT JOIN results r USING(match_id)"):
        jogos[mid] = {"comp": comp, "home": home, "away": away, "ko": dt.datetime.fromisoformat(ko), "hg": hg, "ag": ag}
    return s, jogos


def data_pt(d: dt.date) -> str:
    return f"{d.day:02d} {MESES[d.month - 1]}"


def odd_txt(x) -> str:
    return f"{odd(x.get('odd_casa'), x['prob']):.2f}"


# ------------------------------------------------------------------ cartões

def cartao_green(d, j):
    c = Cartao()
    c.cabecalho(f"{j['comp']} · {data_pt(j['ko'].date())}")
    c.selo((W / 2, 245), "GREEN", VERDE)
    # jogo e resultado
    fs = fonte(SERIFA_N, 150)
    placar = f"{j['hg']}–{j['ag']}"
    c.texto((W / 2, 455), placar, fs, CREME, "mm")
    meio = c.largura(placar, fs) / 2 + 40
    for nome, x, anc in ((j["home"], W / 2 - meio, "rm"), (j["away"], W / 2 + meio, "lm")):
        c.texto((x, 455), nome, c.caber(nome, SERIFA, 50, W / 2 - meio - 80), CREME, anc)
    c.texto((W / 2, 560), "RESULTADO FINAL", fonte(SANS_SB, 17), CREME_45, "mm", esp=5)
    # a previsão
    c.ret((140, 630, W - 140, 860), (30, 29, 27), 28, (66, 62, 57), 2)
    c.texto((W / 2, 680), "A PREVISÃO DO AGENTE CLAUDIO", fonte(SANS_SB, 18), CORAL, "mm", esp=5)
    c.texto((W / 2, 748), d["texto"], c.caber(d["texto"], SANS_SB, 50, W - 360), CREME, "mm")
    c.texto((W / 2, 815), f"Probabilidade {d['prob']:.0%}     ·     Odd {odd_txt(d)}", fonte(SANS, 25), CREME_70, "mm")
    c.rodape("Publicada no canal antes do jogo." + ("" if d.get("odd_casa") else " Odd justa do modelo."))
    return c.guardar(f"green_{d['data']}_{d['match_id'].split('-', 2)[-1]}")


def cartao_multipla(m, pernas, jogos):
    c = Cartao()
    dia = dt.date.fromisoformat(m["data"])
    c.cabecalho(f"Múltipla · {data_pt(dia)}")
    c.selo((W / 2, 230), "MÚLTIPLA GREEN", VERDE)
    om = _prod(odd(p.get("odd_casa"), p["prob"]) for p in pernas)
    c.texto((W / 2, 365), f"{om:.2f}", fonte(SERIFA_N, 130), CREME, "mm")
    c.texto((W / 2, 450), "ODD TOTAL", fonte(SANS_SB, 17), CREME_45, "mm", esp=5)
    y = 520
    alt = min(120, 400 / max(1, len(pernas)))
    for p in pernas:
        j = jogos.get(p["match_id"], {})
        c.ret((120, y, W - 120, y + alt - 16), (30, 29, 27), 22, (66, 62, 57), 2)
        mid = y + (alt - 16) / 2
        c.circulo((170, mid), 20, VERDE)
        c.visto((170, mid), 24, FUNDO, 4.5)
        jogo = f"{j.get('home', '')} {j.get('hg', '')}–{j.get('ag', '')} {j.get('away', '')}"
        c.texto((214, mid - 17), jogo, c.caber(jogo, SERIFA_N, 30, 560), CREME, "lm")
        c.texto((214, mid + 21), p["texto"], fonte(SANS, 21), CREME_70, "lm")
        c.texto((W - 150, mid), odd_txt(p), fonte(SANS_SB, 26), CREME, "rm")
        y += alt
    c.rodape("Publicada no canal antes dos jogos. Odds justas do modelo quando não havia odd da casa.")
    return c.guardar(f"multipla_green_{m['data']}")


def cartao_balanco(dicas, mult, by_id, ini, fim):
    c = Cartao()
    c.cabecalho(f"{data_pt(ini)} – {data_pt(fim)}")
    dias = (fim - ini).days + 1
    c.texto((W / 2, 230), f"Os primeiros {dias} dias" if not ini_antes(dicas, ini) else "Balanço do período",
            fonte(SERIFA_N, 66), CREME, "mm")
    g, n = sum(d["resultado"] for d in dicas), len(dicas)
    # números grandes
    c.texto((330, 395), str(g), fonte(SERIFA_N, 170), VERDE, "mm")
    c.texto((330, 505), f"GREENS EM {n} DICAS", fonte(SANS_SB, 19), CREME_70, "mm", esp=4)
    c.linha((W / 2, 330), (W / 2, 520), (66, 62, 57), 2)
    c.texto((750, 395), f"{g / n:.0%}", fonte(SERIFA_N, 170), CREME, "mm")
    c.texto((750, 505), "DE ACERTO", fonte(SANS_SB, 19), CREME_70, "mm", esp=4)
    # bolinhas, por ordem
    por_linha, r, gap = 10, 24, 66
    for i, d in enumerate(dicas):
        lin, col = divmod(i, por_linha)
        k = min(por_linha, n - lin * por_linha)
        x = W / 2 - (k - 1) * gap / 2 + col * gap
        y = 640 + lin * 72
        cor = VERDE if d["resultado"] else VERMELHO
        c.circulo((x, y), r, cor)
        (c.visto if d["resultado"] else c.cruz)((x, y), 28, FUNDO, 4.5)
    # linha de factos
    y = 640 + ((n - 1) // por_linha + 1) * 72 + 70
    factos = []
    if mult:
        factos.append(f"Múltiplas: {sum(m['resultado'] for m in mult)} Green em {len(mult)}")
    melhor = max(sorted({d["data"] for d in dicas}), key=lambda x: (sum(d["resultado"] for d in dicas if d["data"] == x),
                                                          -sum(not d["resultado"] for d in dicas if d["data"] == x)))
    md = [d for d in dicas if d["data"] == melhor]
    factos.append(f"Melhor dia: {data_pt(dt.date.fromisoformat(melhor))} ({sum(x['resultado'] for x in md)}/{len(md)})")
    lucro, napostas = _lucro(dicas, mult, by_id)
    if lucro > 0:  # só se o período inteiro for positivo
        factos.append(f"Simulação {STAKE} €/aposta: +{lucro:.0f} €")
    c.texto((W / 2, y), "     ·     ".join(factos), fonte(SANS, 25), CREME_70, "mm")
    c.rodape("Todas as dicas do período, Greens e Reds, por ordem de publicação.")
    return c.guardar(f"balanco_{ini}_{fim}")


def ini_antes(dicas, ini):
    return False


# ------------------------------------------------------------------ principal

def main():
    tg, db = sys.argv[1], sys.argv[2]
    s, jogos = carregar(tg, db)
    dec = [d for d in s["dicas"] if d["resultado"] is not None]
    ini = dt.date.fromisoformat(sys.argv[3]) if len(sys.argv) > 3 else min(dt.date.fromisoformat(d["data"]) for d in dec)
    fim = dt.date.fromisoformat(sys.argv[4]) if len(sys.argv) > 4 else max(dt.date.fromisoformat(d["data"]) for d in dec)
    no = [d for d in dec if ini.isoformat() <= d["data"] <= fim.isoformat()]
    by_id = {d["id"]: d for d in s["dicas"]}
    mult = [m for m in s["multiplas"] if m["resultado"] is not None and ini.isoformat() <= m["data"] <= fim.isoformat()]
    feitos = []
    for d in no:
        if d["resultado"] and d["match_id"] in jogos and jogos[d["match_id"]]["hg"] is not None:
            feitos.append(cartao_green(d, jogos[d["match_id"]]))
    for m in mult:
        if m["resultado"]:
            pernas = m.get("pernas") or [by_id[i] for i in m["partes"] if i in by_id]
            feitos.append(cartao_multipla(m, pernas, jogos))
    feitos.append(cartao_balanco(no, mult, by_id, ini, fim))
    print(*[p.name for p in feitos], sep="\n")


if __name__ == "__main__":
    main()
