"""Memes estáticos do Agente Claudio (1080x1350, 4:5: Instagram, X, Facebook; também servem no TikTok como foto).

Cada guião de vídeo pode trazer uma lista MEMES; o workflow "Vídeos" desenha-os e manda-os aos admins com o vídeo.
Tudo desenhado de raiz (sem fotos de jogadores, sem emblemas nem logótipos de terceiros). O robô é o Agente Claudio.

    MEMES = [
        {"modelo": "reacao", "topo": "O líder da Liga contra a Liga 3:", "desenho": "parede",
         "baixo": "Cláudio Ramos nos penáltis", "fala": "Isto não é um guarda-redes. É obra.",
         "legenda": "texto para o post (Instagram/X)"},
        {"modelo": "expectativa", "esq": "O que o adepto esperava", "dir": "O que aconteceu",
         "desenho_esq": "placar:5–0", "desenho_dir": "placar:1–1", "baixo": "...", "legenda": "..."},
    ]

Desenhos prontos: "parede", "placar:<texto>", "trofeu", "relogio:<minuto>", "bola", "lagrima", "fogo", "zero".
Ou uma função do guião: "desenho": minha_funcao, com assinatura f(d, caixa) e caixa = (x0, y0, x1, y1).
Testar: python docs/video/memes.py   (gera exemplos em docs/video/memes_exemplo/)
"""
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw

AQUI = Path(__file__).parent
sys.path.insert(0, str(AQUI))
from quadro_tatico import fonte, SERIFA_N, SANS, SANS_SB, SANS_B  # noqa: E402

W, H = 1080, 1350
FUNDO = (20, 20, 19)
CREME, CREME_70, CORAL, CORAL_CLARO = (250, 249, 245), (190, 188, 182), (217, 119, 87), (240, 150, 112)
VERDE, AZUL, OURO = (126, 196, 132), (139, 163, 196), (226, 182, 82)
PFP = AQUI.parent / "imagens" / "pfp_agente_claudio.png"


def _quebrar(d, texto, f, larg):
    linhas, atual = [], ""
    for p in texto.split():
        t = (atual + " " + p).strip()
        if d.textlength(t, font=f) <= larg or not atual:
            atual = t
        else:
            linhas.append(atual)
            atual = p
    return linhas + ([atual] if atual else [])


def _texto(d, cx, y, texto, nome, tam, cor, larg=940, min_tam=34, max_linhas=3, anchor_top=True):
    """Texto centrado com quebra de linha; encolhe até caber em max_linhas. Devolve o y do fim."""
    t = tam
    while True:
        f = fonte(nome, t)
        ls = _quebrar(d, texto, f, larg)
        if len(ls) <= max_linhas or t <= min_tam:
            break
        t -= 4
    alt = t * 1.18
    for i, l in enumerate(ls):
        d.text((cx, y + i * alt), l, font=f, fill=cor, anchor="ma")
    return y + len(ls) * alt


# ------------------------------------------------------------------ desenhos prontos

def _parede(d, caixa):
    x0, y0, x1, y1 = caixa
    bw, bh = (x1 - x0) / 6, (y1 - y0) / 7
    for fila in range(7):
        off = 0 if fila % 2 == 0 else bw / 2
        for c in range(-1, 7):
            a, b = max(x0 + c * bw + off, x0), min(x0 + c * bw + off + bw - 8, x1)
            if b > a:
                d.rounded_rectangle((a, y0 + fila * bh, b, y0 + fila * bh + bh - 8), radius=4, fill=CORAL)
    # luvas de guarda-redes "espetadas" na parede
    for cx in (x0 + (x1 - x0) * 0.3, x0 + (x1 - x0) * 0.7):
        cy = y0 + (y1 - y0) * 0.45
        d.rounded_rectangle((cx - 55, cy - 40, cx + 55, cy + 70), radius=30, fill=CREME, outline=FUNDO, width=6)
        for k in range(4):
            fx = cx - 45 + k * 30
            d.rounded_rectangle((fx, cy - 95, fx + 24, cy - 20), radius=12, fill=CREME, outline=FUNDO, width=5)


def _placar(d, caixa, texto):
    x0, y0, x1, y1 = caixa
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    d.rounded_rectangle((x0 + 60, cy - 130, x1 - 60, cy + 130), radius=34, fill=(36, 34, 32),
                        outline=(70, 66, 60), width=4)
    d.text((cx, cy), texto, font=fonte(SERIFA_N, 190), fill=CREME, anchor="mm")


def _trofeu(d, caixa):
    x0, y0, x1, y1 = caixa
    cx, h = (x0 + x1) / 2, y1 - y0
    top = y0 + h * 0.1
    d.pieslice((cx - 150, top - 120, cx + 150, top + 260), 0, 180, fill=OURO)
    d.rectangle((cx - 150, top - 10, cx + 150, top + 70), fill=OURO)
    for s in (-1, 1):
        d.arc((cx + s * 150 - 70, top, cx + s * 150 + 70, top + 150), 270 if s > 0 else 90,
              90 if s > 0 else 270, fill=OURO, width=22)
    d.rectangle((cx - 28, top + 260, cx + 28, top + 360), fill=OURO)
    d.rounded_rectangle((cx - 130, top + 360, cx + 130, top + 420), radius=14, fill=OURO)


def _relogio(d, caixa, minuto):
    x0, y0, x1, y1 = caixa
    cx, cy, r = (x0 + x1) / 2, (y0 + y1) / 2, min(x1 - x0, y1 - y0) * 0.42
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=CREME, outline=CORAL, width=18)
    for i in range(12):
        a = i * math.pi / 6
        d.line((cx + math.sin(a) * r * 0.82, cy - math.cos(a) * r * 0.82, cx + math.sin(a) * r * 0.92,
                cy - math.cos(a) * r * 0.92), fill=FUNDO, width=8)
    d.line((cx, cy, cx + r * 0.55, cy - r * 0.2), fill=FUNDO, width=14)
    d.line((cx, cy, cx - r * 0.1, cy - r * 0.75), fill=CORAL, width=10)
    d.text((cx, cy + r * 0.42), minuto, font=fonte(SANS_B, int(r * 0.32)), fill=CORAL, anchor="mm")


def _bola(d, caixa):
    x0, y0, x1, y1 = caixa
    cx, cy, r = (x0 + x1) / 2, (y0 + y1) / 2, min(x1 - x0, y1 - y0) * 0.38
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=CREME, outline=FUNDO, width=8)
    pts = [(cx + math.sin(a) * r * 0.38, cy - math.cos(a) * r * 0.38) for a in [i * 2 * math.pi / 5 for i in range(5)]]
    d.polygon(pts, fill=FUNDO)
    for (px, py) in pts:
        d.line((px, py, cx + (px - cx) * 2.4, cy + (py - cy) * 2.4), fill=FUNDO, width=8)


def _lagrima(d, caixa):
    x0, y0, x1, y1 = caixa
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    for i, s in enumerate((-1, 1)):
        x = cx + s * 120
        d.polygon([(x, cy - 160), (x - 70, cy + 20), (x + 70, cy + 20)], fill=AZUL)
        d.ellipse((x - 70, cy - 50, x + 70, cy + 90), fill=AZUL)


def _fogo(d, caixa):
    x0, y0, x1, y1 = caixa
    cx, base = (x0 + x1) / 2, y1 - 20
    for cor, esc in ((CORAL, 1.0), (OURO, 0.66), (CREME, 0.33)):
        w, h = 300 * esc, 460 * esc
        d.polygon([(cx - w / 2, base), (cx - w / 2.2, base - h * 0.5), (cx - w / 6, base - h * 0.62),
                   (cx, base - h), (cx + w / 6, base - h * 0.55), (cx + w / 2.2, base - h * 0.62),
                   (cx + w / 2, base)], fill=cor)


def _zero(d, caixa):
    x0, y0, x1, y1 = caixa
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    d.text((cx, cy), "0", font=fonte(SERIFA_N, 420), fill=CORAL, anchor="mm")


PRONTOS = {"parede": _parede, "trofeu": _trofeu, "bola": _bola, "lagrima": _lagrima, "fogo": _fogo, "zero": _zero}


def desenhar(d, caixa, desenho):
    if callable(desenho):
        return desenho(d, caixa)
    if not desenho:
        return
    nome, _, arg = str(desenho).partition(":")
    if nome == "placar":
        return _placar(d, caixa, arg)
    if nome == "relogio":
        return _relogio(d, caixa, arg)
    if nome in PRONTOS:
        return PRONTOS[nome](d, caixa)
    raise ValueError(f"desenho desconhecido: {desenho}")


# ------------------------------------------------------------------ o robô e a moldura

def _robo(im, cx, cy, r, inclinar=0):
    if not PFP.exists():
        return
    p = Image.open(PFP).convert("RGBA").resize((2 * r, 2 * r), Image.LANCZOS)
    m = Image.new("L", (2 * r, 2 * r), 0)
    ImageDraw.Draw(m).ellipse((0, 0, 2 * r, 2 * r), fill=255)
    p.putalpha(m)
    if inclinar:
        p = p.rotate(inclinar, resample=Image.BICUBIC)
    im.paste(p, (int(cx - r), int(cy - r)), p)


def _fala(d, x, y, texto, larg=520, direita=True):
    """Balão de fala do robô; (x, y) é a ponta do balão."""
    f = fonte(SANS_SB, 38)
    ls = _quebrar(d, texto, f, larg - 60)[:4]
    alt = 46 * len(ls) + 40
    bx1 = x - 20 if direita else x + larg + 20
    bx0 = bx1 - larg
    by1 = y - 30
    by0 = by1 - alt
    d.rounded_rectangle((bx0, by0, bx1, by1), radius=28, fill=CREME)
    d.polygon([(x, y), (x - 60 if direita else x + 30, by1 - 2), (x - 20 if direita else x + 70, by1 - 2)],
              fill=CREME)
    for i, l in enumerate(ls):
        d.text(((bx0 + bx1) / 2, by0 + 20 + i * 46), l, font=f, fill=FUNDO, anchor="ma")


def _moldura():
    im = Image.new("RGB", (W, H), FUNDO)
    d = ImageDraw.Draw(im)
    d.text((70, 70), "C L A U D I O", font=fonte(SERIFA_N, 30), fill=CORAL, anchor="lm")
    d.text((W - 70, H - 50), "Agente Claudio · +18", font=fonte(SANS, 26), fill=CREME_70, anchor="rm")
    return im, d


def meme(cfg: dict, saida: Path) -> Path:
    im, d = _moldura()
    modelo = cfg.get("modelo", "reacao")
    if modelo == "reacao":
        y = _texto(d, W / 2, 130, cfg.get("topo", ""), SERIFA_N, 66, CREME)
        caixa = (140, max(y + 30, 330), W - 140, 870)
        desenhar(d, caixa, cfg.get("desenho"))
        if cfg.get("baixo"):
            d.rounded_rectangle((90, 895, W - 90, 1000), radius=26, fill=CORAL)
            _texto(d, W / 2, 915, cfg["baixo"], SANS_B, 52, FUNDO, larg=860, max_linhas=1, min_tam=30)
        _robo(im, 190, 1215, 95, inclinar=8)
        if cfg.get("fala"):
            _fala(d, 300, 1195, cfg["fala"], larg=640, direita=False)
    elif modelo == "expectativa":
        for i, (tit, des) in enumerate(((cfg.get("esq", "Expectativa"), cfg.get("desenho_esq")),
                                        (cfg.get("dir", "Realidade"), cfg.get("desenho_dir")))):
            x0 = 60 + i * 490
            d.rounded_rectangle((x0, 140, x0 + 470, 850), radius=30, fill=(32, 31, 29),
                                outline=(CORAL if i else (70, 66, 60)), width=4)
            _texto(d, x0 + 235, 170, tit, SANS_SB, 40, CORAL if i else CREME_70, larg=420, max_linhas=2)
            desenhar(d, (x0 + 20, 290, x0 + 450, 830), des)
        if cfg.get("baixo"):
            _texto(d, W / 2, 875, cfg["baixo"], SERIFA_N, 56, CREME, max_linhas=2)
        _robo(im, 190, 1215, 95, inclinar=-8)
        if cfg.get("fala"):
            _fala(d, 300, 1195, cfg["fala"], larg=640, direita=False)
    else:
        raise ValueError(f"modelo de meme desconhecido: {modelo}")
    saida.parent.mkdir(parents=True, exist_ok=True)
    im.save(saida)
    return saida


if __name__ == "__main__":
    pasta = AQUI / "memes_exemplo"
    meme({"modelo": "reacao", "topo": "O líder da Liga contra uma equipa da Liga 3:", "desenho": "parede",
          "baixo": "Cláudio Ramos nas grandes penalidades", "fala": "Isto não é um guarda-redes. É obra."},
         pasta / "exemplo_reacao.png")
    meme({"modelo": "expectativa", "esq": "O que o adepto do Porto esperava", "dir": "O que teve",
          "desenho_esq": "placar:5–0", "desenho_dir": "relogio:120'", "baixo": "Taça de Portugal, essa simpática.",
          "fala": "Eu só queria ir dormir antes da meia-noite."}, pasta / "exemplo_expectativa.png")
    print("exemplos em", pasta)
