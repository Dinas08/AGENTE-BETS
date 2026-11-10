"""Meme 'Olá, olá.': telemóvel dobrável com a tabela da Champions (dados reais ESPN, 4 nov 2026).
Desenhado de raiz: sem marcas de telemóveis, sem emblemas de clubes, sem logótipos de terceiros.
Correr: .venv\\Scripts\\python.exe docs\\imagens\\memes\\meme_porto_tabela.py
"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

AQUI = Path(__file__).parent
PFP = AQUI.parent / "pfp_agente_claudio.png"
F = "C:/Windows/Fonts/"
K = 2
W, H = 1080, 1350  # 4:5 (Instagram, X, Facebook)

CREME, PRETO, CINZA = (250, 249, 245), (20, 20, 19), (110, 108, 104)
CORAL = (217, 119, 87)
ECRA, ECRA_TXT, ECRA_SUB = (24, 24, 26), (236, 236, 238), (150, 150, 156)
VERDE, VERMELHO = (88, 190, 120), (232, 84, 84)

# a tabela do meme original (pedido do Dinis), não a classificação atual
TOPO = [(1, "PSG", 4, "+12", 12, (0, 45, 98)), (2, "Aston Villa", 4, "+8", 9, (122, 38, 58)),
        (3, "Barcelona", 4, "+6", 9, (165, 0, 68)), (4, "Liverpool", 3, "+5", 9, (200, 16, 46)),
        (5, "Real Madrid", 3, "+5", 9, (230, 230, 230)), (6, "Sporting", 4, "+4", 9, (0, 128, 87)),
        (7, "Real Betis", 3, "+3", 9, (0, 150, 75)), (8, "Roma", 4, "+4", 7, (140, 20, 40))]
FUNDO_T = [(28, "Feyenoord", 4, "-5", 3, (230, 0, 30)), (29, "AEK", 3, "-5", 3, (255, 210, 0)),
           (30, "Leipzig", 3, "-5", 3, (221, 1, 63)), (31, "Fenerbahçe", 3, "-6", 2, (0, 32, 96)),
           (32, "Slavia Praha", 3, "-3", 1, (220, 30, 40)), (33, "Viking", 3, "-4", 1, (0, 100, 60)),
           (34, "Lille", 4, "-6", 1, (200, 20, 40)), (35, "Slovan", 4, "-12", 1, (60, 130, 200)),
           (36, "Porto", 3, "-4", 0, (0, 80, 160))]


def fonte(n, t):
    return ImageFont.truetype(F + n, int(t * K))


def coefs(destino, origem):
    """Coeficientes de Image.PERSPECTIVE que levam o quadrilátero 'destino' ao retângulo 'origem'."""
    A, b = [], []
    for (x, y), (u, v) in zip(destino, origem):
        A += [[x, y, 1, 0, 0, 0, -u * x, -u * y], [0, 0, 0, x, y, 1, -v * x, -v * y]]
        b += [u, v]
    return np.linalg.solve(np.array(A, float), np.array(b, float)).tolist()


def ecra(linhas, titulo, legenda, cor_barra, destaque=None, relogio=False):
    """Uma metade do ecrã, desenhada plana (vai depois em perspetiva)."""
    w, h = 520 * K, 640 * K
    im = Image.new("RGB", (w, h), ECRA)
    d = ImageDraw.Draw(im)
    s = lambda v: v * K
    if relogio:
        d.text((s(410), s(36)), "9:41", font=fonte("seguisb.ttf", 20), fill=ECRA_TXT, anchor="mm")
        d.rounded_rectangle((s(452), s(28), s(488), s(44)), radius=s(4), outline=ECRA_TXT, width=s(2))
        d.rectangle((s(456), s(32), s(480), s(40)), fill=ECRA_TXT)
    if titulo:
        d.text((s(34), s(92)), titulo, font=fonte("seguisb.ttf", 25), fill=ECRA_TXT, anchor="lm")
    y0 = 150
    d.text((s(34 if legenda else 0), s(y0)), legenda, font=fonte("segoeui.ttf", 18), fill=ECRA_SUB, anchor="lm")
    for x, t in ((330, "J"), (400, "DG"), (470, "PTS")):
        d.text((s(x), s(y0)), t, font=fonte("segoeui.ttf", 18), fill=ECRA_SUB, anchor="mm")
    passo = 50 if len(linhas) <= 8 else 46
    ini = y0 + 48
    if cor_barra:
        d.rectangle((s(18), s(ini - 22), s(22), s(ini + passo * (len(linhas) - 1) + 22)), fill=cor_barra)
    for i, (pos, nome, j, dg, pts, cor) in enumerate(linhas):
        y = ini + i * passo
        if nome == destaque:
            d.rounded_rectangle((s(26), s(y - 21), s(500), s(y + 21)), radius=s(10), fill=(58, 34, 28))
        d.text((s(46), s(y)), str(pos), font=fonte("seguisb.ttf", 20), fill=ECRA_TXT, anchor="mm")
        d.ellipse((s(74), s(y - 13), s(100), s(y + 13)), fill=cor, outline=(70, 70, 74), width=s(1))
        d.text((s(114), s(y)), nome, font=fonte("segoeui.ttf", 21), fill=ECRA_TXT, anchor="lm")
        d.text((s(330), s(y)), str(j), font=fonte("segoeui.ttf", 20), fill=ECRA_TXT, anchor="mm")
        d.text((s(400), s(y)), dg, font=fonte("segoeui.ttf", 20), fill=ECRA_TXT, anchor="mm")
        cor_pts = VERMELHO if (pts <= 1 and pos > 24) or nome == destaque else ECRA_TXT
        d.text((s(470), s(y)), str(pts), font=fonte("seguisb.ttf", 21), fill=cor_pts, anchor="mm")
    return im


def metade(tela, fora_esq: bool):
    """Uma metade do telemóvel, plana: aro de titânio, vidro preto e o ecrã; cantos redondos só do lado de fora."""
    w, h = 560 * K, 700 * K
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    r = 64 * K

    def corpo(box, raio, cor):
        x0, y0, x1, y1 = box
        d.rounded_rectangle(box, radius=raio, fill=cor)
        if fora_esq:  # lado da dobradiça (direita) com cantos retos
            d.rectangle((x1 - raio, y0, x1, y1), fill=cor)
        else:
            d.rectangle((x0, y0, x0 + raio, y1), fill=cor)

    for i in range(10):  # aro com degradê metálico
        c = 168 - i * 7
        corpo((i * K * 0.6, i * K * 0.6, w - i * K * 0.6, h - i * K * 0.6), r, (c, c, c + 6))
    corpo((7 * K, 7 * K, w - 7 * K, h - 7 * K), r - 7 * K, (10, 10, 12))  # vidro preto
    tw, th = w - 40 * K, h - 40 * K
    t = tela.resize((tw, th), Image.LANCZOS)
    m = Image.new("L", (tw, th), 0)
    dm = ImageDraw.Draw(m)
    dm.rounded_rectangle((0, 0, tw, th), radius=r - 20 * K, fill=255)
    if fora_esq:
        dm.rectangle((tw - r, 0, tw, th), fill=255)
    else:
        dm.rectangle((0, 0, r, th), fill=255)
    im.paste(t, (20 * K, 20 * K), m)
    return im


def colar_quad(base, img, quad, espessura=0):
    """Cola img (RGB ou RGBA) deformada para o quadrilátero; com espessura, desenha por baixo o bordo do aparelho."""
    w, h = img.size
    t = img.transform(base.size, Image.PERSPECTIVE, coefs(quad, [(0, 0), (w, 0), (w, h), (0, h)]), Image.BICUBIC)
    m = Image.new("L", base.size, 0)
    ImageDraw.Draw(m).polygon(quad, fill=255)
    if t.mode == "RGBA":
        from PIL import ImageChops
        m = ImageChops.multiply(m, t.getchannel("A"))
    for i in range(espessura, 0, -1):  # bordo metálico visto por baixo
        c = 70 + i * 4
        base.paste(Image.new("RGB", base.size, (c, c, c + 5)), (0, i), m)
    base.paste(t.convert("RGB"), (0, 0), m)


def main():
    im = Image.new("RGB", (W * K, H * K), CREME)
    d = ImageDraw.Draw(im)
    for i in range(200):  # leve degradê para dar profundidade
        c = tuple(int(CREME[k] - (CREME[k] - 236) * i / 200) for k in range(3))
        d.rectangle((0, (H * K) * (0.45 + 0.55 * i / 200), W * K, H * K), fill=c)
    s = lambda v: v * K

    # textos ao estilo de anúncio
    d.text((s(W / 2), s(92)), "iPhone Duo", font=fonte("seguisb.ttf", 46), fill=PRETO, anchor="mm")
    d.text((s(W / 2), s(205)), "Olá, olá.", font=fonte("segoeuib.ttf", 138), fill=PRETO, anchor="mm")
    for i, l in enumerate(["Agora podes ver o Porto na tabela da", "Champions sem teres de fazer scroll."]):
        d.text((s(W / 2), s(318 + i * 52)), l, font=fonte("seguisb.ttf", 40), fill=PRETO, anchor="mm")

    # iPhone Duo aberto: duas metades com aro metálico, vidro preto e ecrã, em perspetiva de livro aberto
    # (as bordas de fora mais perto de quem vê, a dobradiça mais funda)
    cx = W / 2
    q_esq = [(58, 452), (cx - 6, 500), (cx - 6, 1078), (58, 1128)]
    q_dir = [(cx + 6, 500), (W - 58, 452), (W - 58, 1128), (cx + 6, 1078)]
    # sombra no chão
    sh = Image.new("L", im.size, 0)
    ImageDraw.Draw(sh).ellipse((s(90), s(1110), s(W - 90), s(1175)), fill=150)
    sh = sh.filter(ImageFilter.GaussianBlur(s(22)))
    im.paste(Image.new("RGB", im.size, (120, 116, 110)), (0, 0), sh)
    d = ImageDraw.Draw(im)
    e1 = ecra(TOPO, "UEFA Champions League 26/27", "Play-off", VERDE)
    e2 = ecra(FUNDO_T, "", "", None, destaque="Porto", relogio=True)
    colar_quad(im, metade(e1, fora_esq=True), [(s(x), s(y)) for x, y in q_esq], espessura=s(9))
    colar_quad(im, metade(e2, fora_esq=False), [(s(x), s(y)) for x, y in q_dir], espessura=s(9))
    d = ImageDraw.Draw(im)
    # dobradiça
    d.polygon([(s(x), s(y)) for x, y in [(cx - 7, 498), (cx + 7, 498), (cx + 7, 1080), (cx - 7, 1080)]],
              fill=(40, 40, 44))
    d.line((s(cx), s(500), s(cx), s(1078)), fill=(150, 150, 156), width=3)
    # reflexo suave no vidro
    gl = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(gl).polygon([(s(x), s(y)) for x, y in [(70, 470), (300, 490), (150, 1100), (70, 1110)]],
                               fill=(255, 255, 255, 16))
    ImageDraw.Draw(gl).polygon([(s(x), s(y)) for x, y in [(700, 482), (860, 470), (640, 1090), (560, 1080)]],
                               fill=(255, 255, 255, 9))
    gl = gl.filter(ImageFilter.GaussianBlur(s(6)))
    im.paste(gl, (0, 0), gl)

    # o Agente Claudio a assinar em baixo
    r = 74
    pf = Image.open(PFP).convert("RGB").resize((s(2 * r), s(2 * r)), Image.LANCZOS)
    m = Image.new("L", pf.size, 0)
    ImageDraw.Draw(m).ellipse((0, 0, pf.size[0], pf.size[1]), fill=255)
    py = 1236
    im.paste(pf, (int(s(W / 2 - r - 150)), int(s(py - r))), m)
    d.text((s(W / 2 - 54), s(py - 18)), "Agente Claudio", font=fonte("seguisb.ttf", 38), fill=PRETO, anchor="lm")
    d.text((s(W / 2 - 54), s(py + 26)), "Dicas grátis no Telegram · 18+", font=fonte("segoeui.ttf", 24),
           fill=CINZA, anchor="lm")

    out = AQUI / "meme_porto_tabela.png"
    im.resize((W, H), Image.LANCZOS).save(out)
    print(out)


if __name__ == "__main__":
    main()
