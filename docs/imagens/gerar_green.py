"""Animação do Agente Claudio a festejar um GREEN (para o Telegram).

Gera docs/imagens/animacoes/green.mp4 (o melhor para o sendAnimation do Telegram: leve e nítido) e green.gif.
512x512, ~3 s, em loop. O robô é o mesmo da foto de perfil (gerar_pfps.py), desenhado por partes para poder
mexer os olhos, os braços e a antena.

Correr:  .venv\\Scripts\\python.exe docs\\imagens\\gerar_green.py
"""
import math
import random
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from gerar_pfps import CORAL, CORAL_CLARO, CORAL_ESC, CREME, CREME_ESC, PRETO, bola

AQUI = Path(__file__).parent
SAIDA = AQUI / "animacoes"
F = "C:/Windows/Fonts/"
K = 2                     # desenha a 1024 e reduz para 512 (antialiasing)
N = 512
C = N * K
FPS, DUR = 25, 3.0
FUNDO = (20, 20, 19)
VERDE = (126, 196, 132)
VERDE_CLARO = (170, 226, 172)


def suave(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def mola(t):
    """Entrada com ressalto (0 -> 1, passa um pouco e volta)."""
    t = max(0.0, min(1.0, t))
    return 1 - math.cos(t * math.pi * 2.5) * math.exp(-t * 5)


# ------------------------------------------------------------------ robô

def robo(im, cx, cy, s, feliz, braco, salto_rot=0.0):
    """Desenha o robô com o centro da cabeça em (cx, cy) e escala s (1 = tamanho do desenho original a 2048 px).
    feliz: 0 olhos redondos, 1 olhos a sorrir (^ ^). braco: 0 em baixo, 1 no ar."""
    camada = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(camada)
    P = lambda x, y: (cx + (x - 1024) * s, cy + (y - 1030) * s)
    R = lambda x0, y0, x1, y1: (*P(x0, y0), *P(x1, y1))
    w = lambda v: max(1, int(v * s))

    # braços (por trás da camisola): do ombro, rodam de baixo para cima
    for lado in (-1, 1):
        ox, oy = P(1024 + lado * 560, 1700)
        ang = math.radians(90 - lado * (20 + 135 * braco))  # 90º = para baixo; no ar fica para fora e para cima
        comp = 430 * s
        mx, my = ox + math.cos(ang) * comp, oy + math.sin(ang) * comp
        d.line((ox, oy, mx, my), fill=CREME_ESC + (255,), width=w(176))   # contorno claro (fundo escuro)
        d.line((ox, oy, mx, my), fill=PRETO + (255,), width=w(150))
        d.ellipse((mx - 95 * s, my - 95 * s, mx + 95 * s, my + 95 * s), fill=CREME + (255,))
        d.ellipse((mx - 95 * s, my - 95 * s, mx + 95 * s, my + 95 * s), outline=CREME_ESC + (255,), width=w(14))
    # camisola
    d.rectangle(R(874, 1510, 1174, 1600), fill=CREME_ESC + (255,))
    d.rounded_rectangle(R(384, 1580, 1664, 2200), radius=w(260), fill=PRETO + (255,))
    d.polygon([P(854, 1580), P(1024, 1730), P(1194, 1580)], fill=CORAL + (255,))
    d.text(P(1024, 1840), "AC", font=ImageFont.truetype(F + "georgiab.ttf", int(190 * s)), fill=CREME + (255,),
           anchor="mm")
    # antena (abana) com a bola de futebol a rodar
    ax, ay = P(1024, 560)
    topo = (ax + math.sin(salto_rot) * 40 * s, ay - 160 * s)
    d.line((ax, ay, *topo), fill=CREME_ESC + (255,), width=w(40))
    # auscultadores
    for x in (1024 - 640, 1024 + 520):
        d.rounded_rectangle(R(x, 880, x + 120, 1240), radius=w(55), fill=PRETO + (255,))
    # cabeça e visor
    d.rounded_rectangle(R(464, 540, 1584, 1520), radius=w(230), fill=CREME + (255,))
    d.rounded_rectangle(R(464, 540, 1584, 1520), radius=w(230), outline=CREME_ESC + (255,), width=w(18))
    d.rounded_rectangle(R(584, 720, 1464, 1230), radius=w(170), fill=PRETO + (255,))
    # microfone
    d.line((*P(1604, 1180), *P(1604, 1340)), fill=PRETO + (255,), width=w(34))
    d.line((*P(1604, 1340), *P(1354, 1420)), fill=PRETO + (255,), width=w(34))
    d.ellipse(R(1294, 1375, 1384, 1465), fill=PRETO + (255,))
    im.alpha_composite(camada)

    # brilho dos olhos (cor muda para verde quando está feliz)
    cor_olho = tuple(int(a + (b - a) * feliz) for a, b in zip(CORAL_CLARO, VERDE_CLARO))
    halo = Image.new("RGBA", im.size, (0, 0, 0, 0))
    hd = ImageDraw.Draw(halo)
    for ex in (1024 - 200, 1024 + 200):
        hd.ellipse(R(ex - 130, 850, ex + 130, 1110), fill=cor_olho + (150,))
    im.alpha_composite(halo.filter(ImageFilter.GaussianBlur(28 * s)))
    d = ImageDraw.Draw(im)
    for ex in (1024 - 200, 1024 + 200):
        if feliz < 0.5:   # olhos redondos
            d.ellipse(R(ex - 95, 885, ex + 95, 1075), fill=cor_olho)
            d.ellipse(R(ex - 35, 915, ex + 15, 965), fill=CREME)
        else:             # olhos a sorrir: ^ ^
            d.arc(R(ex - 100, 925, ex + 100, 1105), start=200, end=340, fill=cor_olho, width=w(46))
    # boca: sorriso que abre quando está feliz
    if feliz < 0.5:
        d.arc(R(854, 1000, 1194, 1180), start=20, end=160, fill=cor_olho, width=w(34))
    else:
        d.chord(R(864, 1040, 1184, 1200), start=0, end=180, fill=cor_olho)
    return topo


def bola_antena(im, topo, s, rot):
    """Bola de futebol pequena no topo da antena, a rodar."""
    r = int(120 * s)
    b = bola(1024, 1024, 520)  # desenha grande ao centro da tela do gerar_pfps
    b = b.crop((1024 - 560, 1024 - 560, 1024 + 560, 1024 + 560)).resize((2 * r, 2 * r), Image.LANCZOS)
    b = b.rotate(math.degrees(rot), resample=Image.BICUBIC)
    im.alpha_composite(b, (int(topo[0] - r), int(topo[1] - r)))


# ------------------------------------------------------------------ cena

def visto(d, cx, cy, r, k):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=VERDE + (int(255 * k),))
    d.line([(cx - r * 0.45, cy + r * 0.02), (cx - r * 0.12, cy + r * 0.36), (cx + r * 0.48, cy - r * 0.34)],
           fill=FUNDO + (int(255 * k),), width=int(r * 0.24), joint="curve")


def confetes(seed=4, n=70):
    rnd = random.Random(seed)
    cores = [CORAL, CORAL_CLARO, CREME, VERDE, VERDE_CLARO]
    out = []
    for _ in range(n):
        ang = rnd.uniform(-math.pi * 0.95, -math.pi * 0.05)   # para cima, em leque
        vel = rnd.uniform(380, 900) * K
        out.append({"vx": math.cos(ang) * vel, "vy": math.sin(ang) * vel, "cor": rnd.choice(cores),
                    "w": rnd.uniform(9, 16) * K, "h": rnd.uniform(5, 9) * K, "rot": rnd.uniform(0, 6.3),
                    "vr": rnd.uniform(-9, 9), "atraso": rnd.uniform(0, 0.12)})
    return out


CONF = confetes()
T_GREEN = 0.75   # momento em que o GREEN carimba


def quadro(t):
    im = Image.new("RGBA", (C, C), FUNDO + (255,))
    # halo verde atrás do robô depois do GREEN (a pulsar)
    kg = suave((t - T_GREEN) / 0.3)
    if kg > 0:
        pulso = 0.85 + 0.15 * math.sin((t - T_GREEN) * 6)
        halo = Image.new("RGBA", (C, C), (0, 0, 0, 0))
        r = 330 * K * pulso
        ImageDraw.Draw(halo).ellipse((C / 2 - r, C * 0.62 - r, C / 2 + r, C * 0.62 + r),
                                     fill=VERDE + (int(70 * kg),))
        im.alpha_composite(halo.filter(ImageFilter.GaussianBlur(70 * K)))
    # disco coral por trás do robô (o mesmo da foto de perfil)
    disco = Image.new("RGBA", (C, C), (0, 0, 0, 0))
    dd = ImageDraw.Draw(disco)
    rc, ccy = 0.37 * C, 0.60 * C
    for i in range(40):  # degradê radial simples: escuro fora, claro dentro
        r = rc * (1 - i / 40)
        cor = tuple(int(a + (b - a) * i / 39) for a, b in zip(CORAL_ESC, CORAL))
        dd.ellipse((C / 2 - r, ccy - r, C / 2 + r, ccy + r), fill=cor + (255,))
    esc_d = mola(t / 0.5)
    if esc_d < 1:
        disco = disco.resize((max(1, int(C * esc_d)),) * 2, Image.LANCZOS)
        tmp = Image.new("RGBA", (C, C), (0, 0, 0, 0))
        tmp.alpha_composite(disco, (int(C / 2 - disco.size[0] / 2), int(ccy - ccy * esc_d)))
        disco = tmp
    im.alpha_composite(disco)
    # robô: entra de baixo com ressalto, salta no GREEN e fica a abanar
    entrada = mola(t / 0.7)
    cy = C * 0.66 + (1 - entrada) * C * 0.6
    if t > T_GREEN:
        u = t - T_GREEN
        cy -= abs(math.sin(u * 7)) * 36 * K * math.exp(-u * 0.6)   # saltinhos
    feliz = 1.0 if t > T_GREEN - 0.05 else 0.0
    braco = suave((t - (T_GREEN - 0.15)) / 0.25)
    if t > T_GREEN + 0.3:
        braco = 0.85 + 0.15 * math.sin((t - T_GREEN) * 8)          # braços a acenar
    s = 0.19 * K  # escala do robô (desenho original a 2048 px) na tela de 1024
    topo = robo(im, C / 2, cy, s, feliz, braco, salto_rot=math.sin(t * 6) * 0.6)
    bola_antena(im, topo, s, t * 4)
    # confetes
    d = ImageDraw.Draw(im)
    if t > T_GREEN:
        u = t - T_GREEN
        ox, oy = C / 2, C * 0.42
        for p in CONF:
            tt = u - p["atraso"]
            if tt <= 0:
                continue
            x = ox + p["vx"] * tt
            y = oy + p["vy"] * tt + 0.5 * 1500 * K * tt * tt
            if y > C + 40:
                continue
            rot = p["rot"] + p["vr"] * tt
            cw, ch = p["w"] / 2, p["h"] / 2 * abs(math.cos(rot * 1.7))
            pts = [(-cw, -ch), (cw, -ch), (cw, ch), (-cw, ch)]
            pts = [(x + a * math.cos(rot) - b * math.sin(rot), y + a * math.sin(rot) + b * math.cos(rot)) for a, b in pts]
            d.polygon(pts, fill=p["cor"] + (255,))
    # GREEN a carimbar (escala grande -> normal) com o visto
    if t > T_GREEN - 0.02:
        u = t - T_GREEN
        esc = 1.0 + 0.6 * math.exp(-u * 14) * (1 if u > 0 else 0)
        k = suave(u / 0.12)
        f = ImageFont.truetype(F + "palab.ttf", int(80 * K * esc))
        txt = "GREEN"
        larg = d.textlength(txt, font=f)
        rv = 31 * K * esc
        total = rv * 2 + 16 * K + larg
        x0 = C / 2 - total / 2
        y = C * 0.12
        sombra = Image.new("RGBA", (C, C), (0, 0, 0, 0))
        sd = ImageDraw.Draw(sombra)
        sd.text((x0 + 2 * rv + 16 * K + 5 * K, y + 6 * K), txt, font=f, fill=(0, 0, 0, int(140 * k)), anchor="lm")
        im.alpha_composite(sombra.filter(ImageFilter.GaussianBlur(6 * K)))
        d = ImageDraw.Draw(im)
        visto(d, x0 + rv, y, rv, k)
        d.text((x0 + 2 * rv + 16 * K, y), txt, font=f, fill=VERDE + (int(255 * k),), anchor="lm")
    return im.convert("RGB").resize((N, N), Image.LANCZOS)


def main():
    import imageio_ffmpeg
    SAIDA.mkdir(exist_ok=True)
    n = int(FPS * DUR)
    frames = [quadro(i / FPS) for i in range(n)]
    mp4 = SAIDA / "green.mp4"
    cmd = [imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{N}x{N}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "20",
           "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an", str(mp4)]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for fr in frames:
        pr.stdin.write(fr.tobytes())
    pr.stdin.close()
    pr.wait()
    gif = SAIDA / "green.gif"
    pal = [f.resize((384, 384), Image.LANCZOS).quantize(colors=128, method=Image.Quantize.MEDIANCUT) for f in frames]
    pal[0].save(gif, save_all=True, append_images=pal[1:], duration=int(1000 / FPS), loop=0, optimize=True,
                disposal=2)
    for i, tt in enumerate((0.3, 0.8, 1.0, 1.6, 2.6)):
        frames[int(tt * FPS)].save(SAIDA / f"green_frame{i + 1}.png")
    print(mp4.name, f"{mp4.stat().st_size // 1024} KB;", gif.name, f"{gif.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
