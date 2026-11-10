"""Gera as fotos de perfil do bot (Agente Claudio) e do canal. Correr: .venv\\Scripts\\python.exe docs\\imagens\\gerar_pfps.py"""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

AQUI = Path(__file__).parent
S = 2048            # desenha em grande e reduz (antialiasing)
OUT = 640           # o Telegram recomenda >= 512 px, quadrado
F = "C:/Windows/Fonts/"

# paleta quente (terracota + creme + quase-preto), inspirada no estilo do Claude sem usar o logótipo
CORAL_ESC, CORAL, CORAL_CLARO = (176, 82, 52), (217, 119, 87), (240, 150, 112)
CREME, CREME_ESC = (250, 249, 245), (232, 230, 220)
BRANCO, CINZA, PRETO = CREME, CREME_ESC, (20, 20, 19)


def fundo(c1, c2) -> Image.Image:
    """Degradê radial do centro (c2) para as bordas (c1)."""
    im = Image.new("RGB", (S, S), c1)
    d = ImageDraw.Draw(im)
    for i in range(120, 0, -1):
        t = i / 120
        r = int(S * 0.75 * t)
        cor = tuple(int(c2[k] + (c1[k] - c2[k]) * t) for k in range(3))
        d.ellipse((S / 2 - r, S / 2 - r, S / 2 + r, S / 2 + r), fill=cor)
    return im


def linhas_campo(im, alpha=38, cor=(255, 255, 255)):
    ov = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    w = 14
    d.line((0, S / 2, S, S / 2), fill=cor + (alpha,), width=w)
    r = S * 0.30
    d.ellipse((S / 2 - r, S / 2 - r, S / 2 + r, S / 2 + r), outline=cor + (alpha,), width=w)
    im.paste(ov, (0, 0), ov)


def brilho(im, caixa, cor, raio=60, forca=170):
    ov = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(ov).ellipse(caixa, fill=cor + (forca,))
    ov = ov.filter(ImageFilter.GaussianBlur(raio))
    im.paste(ov, (0, 0), ov)


def pentagono(cx, cy, r, rot):
    return [(cx + r * math.cos(rot + k * 2 * math.pi / 5), cy + r * math.sin(rot + k * 2 * math.pi / 5)) for k in range(5)]


def bola(cx, cy, R) -> Image.Image:
    """Bola de futebol (gomos pretos) numa camada RGBA do tamanho da imagem."""
    lay = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=BRANCO + (255,))
    rot = -math.pi / 2
    pc = pentagono(cx, cy, R * 0.30, rot)
    seams = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ds = ImageDraw.Draw(seams)
    w = int(R * 0.035)
    fora = []  # pentágonos de fora: um em frente a cada aresta do do meio
    for k in range(5):
        b = rot + k * 2 * math.pi / 5 + math.pi / 5
        po = pentagono(cx + R * 0.80 * math.cos(b), cy + R * 0.80 * math.sin(b), R * 0.27, b)
        fora.append(po)
        ds.polygon(po, fill=PRETO + (255,))
        for v in po[1:2] + po[4:5]:  # costuras das pontas laterais para a borda
            ang = math.atan2(v[1] - cy, v[0] - cx)
            ds.line((*v, cx + R * 1.05 * math.cos(ang), cy + R * 1.05 * math.sin(ang)), fill=PRETO + (255,), width=w)
    for k in range(5):
        a = rot + k * 2 * math.pi / 5
        q = (cx + R * 0.52 * math.cos(a), cy + R * 0.52 * math.sin(a))
        ds.line((*pc[k], *q), fill=PRETO + (255,), width=w)
        for po in (fora[k], fora[k - 1]):  # do nó às pontas mais próximas dos dois pentágonos vizinhos
            v = min(po, key=lambda p: (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)
            ds.line((*q, *v), fill=PRETO + (255,), width=w)
    ds.polygon(pc, fill=PRETO + (255,))
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).ellipse((cx - R, cy - R, cx + R, cy + R), fill=255)
    lay.paste(seams, (0, 0), Image.composite(seams.getchannel("A"), Image.new("L", (S, S), 0), mask))
    # sombra interior suave para dar volume
    sh = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse((cx - R * 0.7, cy - R * 0.2, cx + R * 1.5, cy + R * 1.6), fill=(0, 0, 0, 40))
    sh = sh.filter(ImageFilter.GaussianBlur(R * 0.25))
    lay.paste(sh, (0, 0), Image.composite(sh.getchannel("A"), Image.new("L", (S, S), 0), mask))
    ImageDraw.Draw(lay).ellipse((cx - R, cy - R, cx + R, cy + R), outline=PRETO + (255,), width=int(R * 0.04))
    return lay


def guardar(im, nome):
    im = im.resize((OUT, OUT), Image.LANCZOS)
    im.save(AQUI / f"{nome}.png")
    # pré-visualização como o Telegram mostra (círculo)
    m = Image.new("L", (OUT, OUT), 0)
    ImageDraw.Draw(m).ellipse((0, 0, OUT, OUT), fill=255)
    prev = Image.new("RGBA", (OUT, OUT), (255, 255, 255, 0))
    prev.paste(im, (0, 0), m)
    prev.save(AQUI / f"{nome}_circulo.png")


# ------------------------------------------------------------------ Agente Claudio (bot de boas-vindas)

def agente():
    im = fundo(CORAL_ESC, CORAL)
    linhas_campo(im, alpha=40, cor=CREME)
    d = ImageDraw.Draw(im)
    cx = S / 2
    # antena com bola na ponta
    d.line((cx, 560, cx, 400), fill=CREME_ESC, width=40)
    b = bola(cx, 330, 120)
    im.paste(b, (0, 0), b)
    d = ImageDraw.Draw(im)
    # orelhas / auscultadores (agente de apoio)
    for x in (cx - 640, cx + 520):
        d.rounded_rectangle((x, 880, x + 120, 1240), radius=55, fill=PRETO)
    # cabeça
    d.rounded_rectangle((cx - 560, 540, cx + 560, 1520), radius=230, fill=CREME)
    d.rounded_rectangle((cx - 560, 540, cx + 560, 1520), radius=230, outline=CREME_ESC, width=18)
    # visor
    d.rounded_rectangle((cx - 440, 720, cx + 440, 1230), radius=170, fill=PRETO)
    # olhos a brilhar
    for ex in (cx - 200, cx + 200):
        brilho(im, (ex - 150, 830, ex + 150, 1130), CORAL_CLARO, raio=55, forca=150)
    d = ImageDraw.Draw(im)
    for ex in (cx - 200, cx + 200):
        d.ellipse((ex - 95, 885, ex + 95, 1075), fill=CORAL_CLARO)
        d.ellipse((ex - 35, 915, ex + 15, 965), fill=CREME)
    # sorriso
    d.arc((cx - 170, 1000, cx + 170, 1180), start=20, end=160, fill=CORAL_CLARO, width=34)
    # microfone do auscultador
    d.line((cx + 580, 1180, cx + 580, 1340), fill=PRETO, width=34)
    d.line((cx + 580, 1340, cx + 330, 1420), fill=PRETO, width=34)
    d.ellipse((cx + 270, 1375, cx + 360, 1465), fill=PRETO)
    # pescoço + camisola de futebol
    d.rectangle((cx - 150, 1510, cx + 150, 1600), fill=CREME_ESC)
    d.rounded_rectangle((cx - 640, 1580, cx + 640, 2200), radius=260, fill=PRETO)
    d.polygon([(cx - 170, 1580), (cx, 1730), (cx + 170, 1580)], fill=CORAL)
    d.text((cx, 1840), "AC", font=ImageFont.truetype(F + "georgiab.ttf", 190), fill=CREME, anchor="mm")
    guardar(im, "pfp_agente_claudio")


# ------------------------------------------------------------------ canal

def espacado(d, cx, y, txt, fonte, cor, esp):
    """Texto centrado com letras espaçadas (look de marca premium)."""
    larg = sum(d.textlength(c, font=fonte) + esp for c in txt) - esp
    x = cx - larg / 2
    for c in txt:
        d.text((x, y), c, font=fonte, fill=cor, anchor="lm")
        x += d.textlength(c, font=fonte) + esp


def canal():
    """Monograma: um 'C' serifado (Palatino) com a marca do centro do campo em terracota no meio e a linha do
    meio-campo, discreta, por trás. Paleta inversa da do agente (quase-preto, creme, terracota)."""
    im = fundo((20, 20, 19), (34, 33, 31))  # quase-preto liso, só um respiro de luz ao centro
    cx, cy = S / 2, 870
    ov = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(ov).line((0, cy, S, cy), fill=CREME + (46,), width=10)
    im.paste(ov, (0, 0), ov)
    d = ImageDraw.Draw(im)
    # o C, centrado pela caixa do desenho (não pela da fonte)
    fc = ImageFont.truetype(F + "palab.ttf", 1180)
    x0, y0, x1, y1 = d.textbbox((0, 0), "C", font=fc, anchor="lt")
    d.text((cx - (x0 + x1) / 2, cy - (y0 + y1) / 2), "C", font=fc, fill=CREME, anchor="lt")
    # marca do centro, no meio do "olho" do C
    r, px = 66, cx + (x1 - x0) * 0.10
    d.ellipse((px - r, cy - r, px + r, cy + r), fill=CORAL)
    # nome
    espacado(d, cx, 1585, "CLAUDIO", ImageFont.truetype(F + "palab.ttf", 150), CREME, 40)
    espacado(d, cx, 1745, "BET TIPS", ImageFont.truetype(F + "segoeui.ttf", 86), CORAL, 34)
    guardar(im, "pfp_canal")


if __name__ == "__main__":
    agente()
    canal()
    print("feito:", *sorted(p.name for p in AQUI.glob("pfp_*.png")))
