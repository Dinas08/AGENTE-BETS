"""Quadro tático animado para TikTok/Reels/Shorts (vertical 1080x1920, 30 fps, sem som).

O motor é genérico (campo, jogadores, bola, setas, legendas); cada jogo é um ficheiro de dados em
docs/video/jogos/<nome>.py com as cenas. As jogadas são ILUSTRAÇÕES baseadas no relato do jogo
(minuto, marcador, assistência, zona e pé do remate, vindos do ESPN) — o vídeo diz isso no ecrã.

Correr:  .venv\\Scripts\\python.exe docs\\video\\quadro_tatico.py barcelona_astonvilla
Precisa do ffmpeg do pacote imageio-ffmpeg (pip install imageio-ffmpeg).
"""
import importlib.util
import math
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

AQUI = Path(__file__).parent
W, H, FPS = 1080, 1920, 30
F = "C:/Windows/Fonts/"

FUNDO = (20, 20, 19)
RELVA, RELVA2 = (27, 38, 31), (31, 43, 35)
LINHA = (214, 210, 196)
CREME, CREME_70, CREME_45 = (250, 249, 245), (190, 188, 182), (130, 128, 122)
CORAL, CORAL_CLARO = (217, 119, 87), (240, 150, 112)
AZUL = (139, 163, 196)
VERDE = (126, 196, 132)

# campo vertical (a equipa da casa ataca para cima). Duas "câmaras": o campo inteiro e o meio-campo ofensivo
# aproximado (mesma escala em x e y: 68 m de largura, 105 m de comprimento)
CX0, CY0, CW, CH = 210, 500, 660, 980
_HZ = round(1000 * 0.56 * 105 / 68)
# nome: (retângulo no ecrã, y inicial do campo, fração do comprimento visível)
VISTAS = {"inteiro": ((CX0, CY0, CW, CH), 0.0, 1.0),
          "ataque": ((40, 500, 1000, _HZ), 0.0, 0.56),
          "defesa": ((40, 500, 1000, _HZ), 0.44, 0.56)}
_vista = ["inteiro"]


def usar_vista(nome):
    _vista[0] = nome


def retangulo():
    return VISTAS[_vista[0]][0]


def fonte(nome, tam):
    return ImageFont.truetype(F + nome, int(tam))


SERIFA_N, SANS, SANS_SB, SANS_B = "palab.ttf", "segoeui.ttf", "seguisb.ttf", "segoeuib.ttf"


def P(x, y):
    """Coordenadas do campo (0-1; y=0 é a baliza de cima) -> píxeis, na câmara atual."""
    (x0, y0, w, h), yi, alcance = VISTAS[_vista[0]]
    return x0 + x * w, y0 + (y - yi) / alcance * h


def suave(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def interp(chaves, t, linear=False):
    """chaves: [(t, x, y), ...] -> (x, y) em t, com easing entre chaves (linear para a bola)."""
    if t <= chaves[0][0]:
        return chaves[0][1:]
    for (t0, x0, y0), (t1, x1, y1) in zip(chaves, chaves[1:]):
        if t <= t1:
            k = ((t - t0) / (t1 - t0) if linear else suave((t - t0) / (t1 - t0))) if t1 > t0 else 1
            return x0 + (x1 - x0) * k, y0 + (y1 - y0) * k
    return chaves[-1][1:]


# ------------------------------------------------------------------ desenho base

def campo(vista="inteiro") -> Image.Image:
    usar_vista(vista)
    k = 2
    im = Image.new("RGB", (W * k, H * k), FUNDO)
    d = ImageDraw.Draw(im)
    for i in range(12):  # faixas da relva (12 em todo o comprimento)
        (xa, ya), (xb, yb) = P(0, i / 12), P(1, (i + 1) / 12)
        d.rectangle((xa * k, ya * k, xb * k, yb * k), fill=RELVA if i % 2 else RELVA2)
    lw = 3 * k
    L = lambda *pts: d.line([(P(x, y)[0] * k, P(x, y)[1] * k) for x, y in pts], fill=LINHA, width=lw)
    L((0, 0), (1, 0), (1, 1), (0, 1), (0, 0))
    L((0, 0.5), (1, 0.5))
    rx = ry = 0.135 * VISTAS[vista][0][2]
    cx, cy = P(0.5, 0.5)
    d.ellipse(((cx - rx) * k, (cy - ry) * k, (cx + rx) * k, (cy + ry) * k), outline=LINHA, width=lw)
    for y0, s in ((0, 1), (1, -1)):
        L((0.2, y0), (0.2, y0 + s * 0.157), (0.8, y0 + s * 0.157), (0.8, y0))       # grande área
        L((0.37, y0), (0.37, y0 + s * 0.052), (0.63, y0 + s * 0.052), (0.63, y0))    # pequena área
        px, py = P(0.5, y0 + s * 0.105)
        d.ellipse(((px - 4) * k, (py - 4) * k, (px + 4) * k, (py + 4) * k), fill=LINHA)
        gx0, gy = P(0.44, y0)
        gx1, _ = P(0.56, y0)
        d.rectangle((gx0 * k, (gy - (14 if s == 1 else 0)) * k, gx1 * k, (gy + (0 if s == 1 else 14)) * k),
                    outline=LINHA, width=lw)
    im = im.resize((W, H), Image.LANCZOS)
    # recorta à câmara; na aproximada, o fundo do campo esbate-se para o preto
    (x0, y0, w, h), yi, alcance = VISTAS[vista]
    fundo = Image.new("RGB", (W, H), FUNDO)
    m = Image.new("L", (W, H), 0)
    dm = ImageDraw.Draw(m)
    dm.rectangle((x0 - 10, y0 - (22 if yi == 0 else 0), x0 + w + 10, y0 + h + (22 if yi + alcance >= 1 else 0)),
                 fill=255)
    if yi + alcance < 1:  # esbate em baixo
        for i in range(160):
            dm.line((x0 - 10, y0 + h - i, x0 + w + 10, y0 + h - i), fill=int(255 * i / 160))
    if yi > 0:  # esbate em cima
        for i in range(160):
            dm.line((x0 - 10, y0 + i, x0 + w + 10, y0 + i), fill=int(255 * i / 160))
    fundo.paste(im, (0, 0), m)
    return fundo


def sprite(r, cor, contorno=None, w=0, oco=False):
    k = 4
    im = Image.new("RGBA", (int(2 * r * k + 8 * k), int(2 * r * k + 8 * k)), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = im.size[0] / 2
    if not oco:
        d.ellipse((c - r * k, c - r * k, c + r * k, c + r * k), fill=cor + (255,))
    if contorno:
        d.ellipse((c - r * k, c - r * k, c + r * k, c + r * k), outline=contorno + (255,), width=int(w * k))
    return im.resize((im.size[0] // k, im.size[1] // k), Image.LANCZOS)


class _Desenho(ImageDraw.ImageDraw):
    """No Pillow, texto com alfa 0 sobre uma imagem RGB aparece opaco; aqui fica invisível, como deve."""

    def text(self, xy, text, fill=None, *args, **kwargs):
        if isinstance(fill, tuple) and len(fill) == 4 and fill[3] <= 0:
            return
        return super().text(xy, text, fill, *args, **kwargs)


class Quadro:
    """Uma imagem do vídeo, com utilitários de desenho."""

    def __init__(self, base):
        self.im = base.copy()
        self.d = _Desenho(self.im, "RGBA")

    def colar(self, sp, x, y):
        self.im.paste(sp, (int(x - sp.size[0] / 2), int(y - sp.size[1] / 2)), sp)

    def texto(self, xy, s, f, cor, anchor="la", alpha=255):
        self.d.text(xy, s, font=f, fill=cor + (int(alpha),), anchor=anchor)

    def bloco(self, x, y, s, f, cor, maxw, alpha=255, anchor="la", entre=1.25):
        """Texto com quebra de linha; devolve o y final."""
        linhas, atual = [], ""
        for pal in s.split():
            t = (atual + " " + pal).strip()
            if self.d.textlength(t, font=f) > maxw and atual:
                linhas.append(atual)
                atual = pal
            else:
                atual = t
        linhas.append(atual)
        alt = f.size * entre
        for i, l in enumerate(linhas):
            self.texto((x, y + i * alt), l, f, cor, anchor, alpha)
        return y + len(linhas) * alt

    def seta(self, pts, prog, cor, w=6, tracejado=False, cabeca=True, alpha=255):
        """Desenha a seta até à fração prog do comprimento total."""
        if prog <= 0 or len(pts) < 2:
            return
        segs = list(zip(pts, pts[1:]))
        total = sum(math.dist(a, b) for a, b in segs)
        alvo, feito, ultimo = total * min(prog, 1), 0, None
        caminho = [pts[0]]
        for a, b in segs:
            s = math.dist(a, b)
            if feito + s >= alvo:
                k = (alvo - feito) / s if s else 0
                caminho.append((a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k))
                ultimo = (a, caminho[-1])
                break
            caminho.append(b)
            feito += s
            ultimo = (a, b)
        c = cor + (int(alpha),)
        if tracejado:
            for a, b in zip(caminho, caminho[1:]):
                s = math.dist(a, b)
                n = max(1, int(s / 22))
                for i in range(n):
                    if i % 2 == 0:
                        p0 = (a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n)
                        p1 = (a[0] + (b[0] - a[0]) * (i + 1) / n, a[1] + (b[1] - a[1]) * (i + 1) / n)
                        self.d.line((p0, p1), fill=c, width=w)
        else:
            self.d.line(caminho, fill=c, width=w, joint="curve")
        if cabeca and ultimo:
            (ax, ay), (bx, by) = ultimo
            ang = math.atan2(by - ay, bx - ax)
            tam = w * 3.4
            p1 = (bx - tam * math.cos(ang - 0.45), by - tam * math.sin(ang - 0.45))
            p2 = (bx - tam * math.cos(ang + 0.45), by - tam * math.sin(ang + 0.45))
            self.d.polygon([(bx + w * 0.8 * math.cos(ang), by + w * 0.8 * math.sin(ang)), p1, p2], fill=c)


# ------------------------------------------------------------------ cena genérica

class Cena:
    """Uma cena: duração, legenda, jogadores com trajetórias, bola, setas e destaques.

    jogadores: {id: {"nome", "equipa": "casa"/"fora", "chaves": [(t, x, y), ...]}}
    bola: [(t, x, y), ...] ou None
    setas: [{"pts": [(x, y), ...], "t0", "t1", "tipo": "passe"/"corrida"/"remate"}]
    destaques: [(id, t0, t1)]   golo: (t, "1–0", "7'") -> flash "GOLO"
    """

    def __init__(self, dur, titulo="", texto="", jogadores=None, bola=None, setas=(), destaques=(),
                 golo=None, placar=None, minuto="", sobreposicao=None, nomes=True, vista="inteiro",
                 voz="", voz_ini=0.3, legenda="", formas=()):
        self.dur, self.titulo, self.texto = dur, titulo, texto
        self.jogadores, self.bola, self.setas = jogadores or {}, bola, list(setas)
        self.destaques, self.golo, self.placar, self.minuto = list(destaques), golo, placar, minuto
        self.sobreposicao, self.nomes, self.vista = sobreposicao, nomes, vista
        self.voz, self.voz_ini, self.legenda = voz, voz_ini, legenda
        self.formas = list(formas)  # elementos táticos: zonas, marcações, linhas, espaço entre linhas, rótulos
        self.palavras = []  # [(palavra, t0, t1)] calculado com a duração da voz


def tempos_legenda(cena, dur_voz):
    """Distribui as palavras da legenda pela duração da voz (peso = letras + pausa na pontuação)."""
    pal = cena.legenda.split()
    if not pal:
        return
    pesos = [len(p) + 2 + (5 if p[-1] in ".!?" else 3 if p[-1] in ",:;" else 0) for p in pal]
    tot, t = sum(pesos), cena.voz_ini + 0.05
    util = dur_voz * 0.94
    cena.palavras = []
    for p, w in zip(pal, pesos):
        d = util * w / tot
        cena.palavras.append((p, t, t + d))
        t += d


def blocos_legenda(palavras, medir, maxw=900, maxn=3):
    """Agrupa as palavras em blocos curtos (máx. 3 palavras, corta na pontuação)."""
    blocos, atual = [], []
    for p in palavras:
        if atual and (len(atual) >= maxn or medir(" ".join(x[0] for x in atual + [p])) > maxw
                      or atual[-1][0][-1] in ".!?,:;"):
            blocos.append(atual)
            atual = []
        atual.append(p)
    if atual:
        blocos.append(atual)
    return blocos


class Video:
    def __init__(self, casa, fora, cor_casa=CORAL, cor_fora=AZUL, abrev=("CAS", "FOR"), fonte_txt=""):
        self.casa, self.fora, self.abrev, self.fonte_txt = casa, fora, abrev, fonte_txt
        self.rapidez, self.folga, self.bpm = 0.9, 0.45, 96
        self.bases = {v: campo(v) for v in VISTAS}
        self.sp = {"casa": sprite(17, cor_casa, CREME, 2.5), "fora": sprite(17, FUNDO, cor_fora, 4),
                   "bola": sprite(9, CREME, FUNDO, 2), "anel": sprite(30, CREME, CREME, 3, oco=True)}
        self.cor = {"casa": cor_casa, "fora": cor_fora}
        self.f = {"tit": fonte(SERIFA_N, 58), "txt": fonte(SANS, 36), "nome": fonte(SANS_SB, 20),
                  "plac": fonte(SANS_B, 34), "min": fonte(SANS_SB, 26), "golo": fonte(SERIFA_N, 190),
                  "marca": fonte(SERIFA_N, 28), "peq": fonte(SANS, 22),
                  "leg": fonte("seguibl.ttf", 66)}

    def desenhar(self, cena: Cena, t_real: float, tg: float) -> Image.Image:
        # a animação estica quando a voz é mais lenta do que a de referência; legendas e zoom usam o tempo real
        t = t_real / getattr(cena, "esc", 1.0)
        usar_vista(cena.vista)
        (rx0, ry0, rw, rh), yi, alcance = VISTAS[cena.vista]
        q = Quadro(self.bases[cena.vista])
        d = q.d
        # marca no topo
        q.texto((80, 165), "C L A U D I O", self.f["marca"], CORAL, "lm")
        # placar
        if cena.placar:
            placar = cena.golo[1] if cena.golo and t >= cena.golo[0] else cena.placar
            txt = f"{self.abrev[0]}  {placar}  {self.abrev[1]}"
            larg = d.textlength(txt, font=self.f["plac"]) + 60
            d.rounded_rectangle((W / 2 - larg / 2, CY0 - 78, W / 2 + larg / 2, CY0 - 22), radius=28,
                                fill=(30, 29, 27, 235), outline=(70, 66, 60, 255), width=2)
            q.texto((W / 2, CY0 - 50), txt, self.f["plac"], CREME, "mm")
            if cena.minuto:
                q.texto((W / 2 + larg / 2 + 18, CY0 - 50), cena.minuto, self.f["min"], CORAL, "lm")
        # elementos táticos (por baixo das setas e dos jogadores)
        if cena.formas:
            self.desenhar_formas(q, cena, t)
        # setas
        for s in cena.setas:
            prog = (t - s["t0"]) / max(0.01, s["t1"] - s["t0"])
            pts = [P(x, y) for x, y in s["pts"]]
            cor, tr, w = {"passe": (CREME, False, 6), "corrida": (CORAL_CLARO, True, 6),
                          "remate": (VERDE, False, 8), "corrida_fora": (AZUL, True, 6), "conducao": (CORAL_CLARO, False, 5)}[s["tipo"]]
            q.seta(pts, prog, cor, w, tr, alpha=230)
        # jogadores
        for jid, j in cena.jogadores.items():
            jx, jy = interp(j["chaves"], t)
            if jy > yi + alcance * 0.97 or (yi > 0 and jy < yi + 0.03):  # fora da câmara
                continue
            x, y = P(jx, jy)
            for hid, t0, t1 in cena.destaques:
                if hid == jid and t0 <= t <= t1:
                    pulso = 1 + 0.12 * math.sin((t - t0) * 7)
                    an = self.sp["anel"].resize((int(self.sp["anel"].size[0] * pulso),) * 2, Image.LANCZOS)
                    q.colar(an, x, y)
            q.colar(self.sp[j["equipa"]], x, y)
            if cena.nomes and j.get("nome"):
                q.texto((x, y + 31), j["nome"], self.f["nome"], CREME if j["equipa"] == "casa" else CREME_70, "mm",
                        alpha=235)
        # bola
        if cena.bola:
            bx, by = P(*interp(cena.bola, t, linear=True))
            q.colar(self.sp["bola"], bx, by)
        # sobreposição (cartões de estatísticas, abertura, fecho)
        if cena.sobreposicao:
            cena.sobreposicao(self, q, t)
        # legenda (topo, área segura do TikTok)
        a = 255 * suave(t / 0.35) * suave((cena.dur - t) / 0.25)
        if cena.titulo:
            q.texto((80, 262), cena.titulo, self.f["tit"], CREME, "ls", a)
        if cena.palavras:
            self.legenda(q, cena, t_real)
        elif cena.texto:
            q.bloco(80, 292, cena.texto, self.f["txt"], CREME_70, W - 180, a, entre=1.2)
        # golo: ondas na rede onde a bola entra + faixa com o marcador
        if cena.golo and cena.golo[0] <= t <= cena.golo[0] + 2.0:
            self.anim_golo(q, cena, t - cena.golo[0])
        # rodapé: fonte dos dados
        q.texto((W / 2, ry0 + rh + 40), self.fonte_txt, self.f["peq"], CREME_45, "mm")
        # barra de progresso
        d.rectangle((0, H - 6, W * tg, H), fill=CORAL + (255,))
        im = q.im
        # impacto do golo: zoom leve (sem clarão)
        if cena.golo and cena.golo[0] <= t <= cena.golo[0] + 0.35:
            z = 1.0 + 0.025 * (1 - suave((t - cena.golo[0]) / 0.35))
            cw, ch = int(W / z), int(H / z)
            im = im.crop(((W - cw) // 2, (H - ch) // 2, (W - cw) // 2 + cw, (H - ch) // 2 + ch)).resize((W, H))
        # entrada de cena: pequeno zoom
        if t_real < 0.22:
            z = 1.06 - 0.06 * suave(t / 0.22)
            cw, ch = int(W / z), int(H / z)
            im = im.crop(((W - cw) // 2, (H - ch) // 2, (W - cw) // 2 + cw, (H - ch) // 2 + ch)).resize((W, H))
        return im

    def desenhar_formas(self, q, cena, t):
        """Formas (cada uma com t0, t1; aparece e desaparece suavemente):
        {"tipo": "zona", "pts": [(x, y), ...], "cor", "rotulo"}         área sombreada fixa
        {"tipo": "entre", "de": [ids], "ate": [ids], "cor", "rotulo"}    faixa entre duas linhas de jogadores (segue-os)
        {"tipo": "linha", "ids": [ids], "cor"}                           linha que une jogadores (ordenados em x)
        {"tipo": "liga", "a": id, "b": id, "cor", "quebra": t}           marcação (tracejado); parte-se em 'quebra'
        {"tipo": "rotulo", "x", "y", "texto", "cor"}                     etiqueta no campo
        """
        pos = {jid: P(*interp(j["chaves"], t)) for jid, j in cena.jogadores.items()}
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(ov)
        rotulos = []
        for f in cena.formas:
            t0, t1 = f.get("t0", 0), f.get("t1", 99)
            if not t0 <= t <= t1:
                continue
            a = suave((t - t0) / 0.35) * suave((t1 - t) / 0.35)
            cor = f.get("cor", CORAL)
            tipo = f["tipo"]
            if tipo in ("zona", "entre"):
                if tipo == "zona":
                    pts = [P(x, y) for x, y in f["pts"]]
                else:
                    ya = sum(pos[i][1] for i in f["de"]) / len(f["de"])
                    yb = sum(pos[i][1] for i in f["ate"]) / len(f["ate"])
                    x0, _ = P(0.04, 0)
                    x1, _ = P(0.96, 0)
                    pts = [(x0, ya), (x1, ya), (x1, yb), (x0, yb)]
                od.polygon(pts, fill=cor + (int(70 * a),))
                od.line(pts + [pts[0]], fill=cor + (int(190 * a),), width=3)
                if f.get("rotulo"):
                    cx = sum(x for x, _ in pts) / len(pts)
                    if tipo == "entre":  # rótulo encostado à esquerda, para não tapar jogadores
                        cx = pts[0][0] + 120
                    cy = sum(y for _, y in pts) / len(pts)
                    rotulos.append((cx, cy, f["rotulo"], cor, a))
            elif tipo == "linha":
                pts = sorted(pos[i] for i in f["ids"])
                od.line(pts, fill=cor + (int(200 * a),), width=5, joint="curve")
            elif tipo == "liga":
                (ax, ay), (bx, by) = pos[f["a"]], pos[f["b"]]
                if "quebra" in f and t > f["quebra"]:  # a marcação perde-se: o traço some
                    a *= 1 - suave((t - f["quebra"]) / 0.3)
                n = max(2, int(((bx - ax) ** 2 + (by - ay) ** 2) ** 0.5 / 14))
                for i in range(0, n, 2):
                    p0 = (ax + (bx - ax) * i / n, ay + (by - ay) * i / n)
                    p1 = (ax + (bx - ax) * (i + 1) / n, ay + (by - ay) * (i + 1) / n)
                    od.line((p0, p1), fill=cor + (int(230 * a),), width=4)
            elif tipo == "rotulo":
                x, y = P(f["x"], f["y"])
                rotulos.append((x, y, f["texto"], cor, a))
        q.im.paste(ov, (0, 0), ov)
        fr = fonte(SANS_SB, 30)
        for x, y, txt, cor, a in rotulos:
            lw = q.d.textlength(txt, font=fr) + 36
            q.d.rounded_rectangle((x - lw / 2, y - 25, x + lw / 2, y + 25), radius=25, fill=cor + (int(240 * a),))
            q.d.text((x, y), txt, font=fr, fill=(20, 20, 19, int(255 * a)), anchor="mm")

    def anim_golo(self, q, cena, dt):
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(ov)
        # ondas a partir do ponto onde a bola entra
        if cena.bola:
            gx, gy = P(*cena.bola[-1][1:])
            for i in range(3):
                k = (dt - i * 0.12) / 0.8
                if 0 < k < 1:
                    r = 18 + 110 * suave(k)
                    od.ellipse((gx - r, gy - r, gx + r, gy + r), outline=CORAL_CLARO + (int(220 * (1 - k)),),
                               width=max(2, int(7 * (1 - k))))
        # faixa: entra da esquerda, fica, sai para a direita
        ent, sai = suave((dt - 0.15) / 0.3), suave((dt - 1.65) / 0.3)
        if ent > 0 and sai < 1:
            a = ent * (1 - sai)
            cw, chh = 780, 168
            x0 = W / 2 - cw / 2 + (1 - ent) * -140 + sai * 140
            y0 = CY0 + 420
            od.rounded_rectangle((x0, y0, x0 + cw, y0 + chh), radius=26, fill=(24, 23, 22, int(240 * a)),
                                 outline=(70, 66, 60, int(255 * a)), width=2)
            od.rounded_rectangle((x0, y0, x0 + 14, y0 + chh), radius=7, fill=CORAL + (int(255 * a),))
            fg = fonte(SANS_SB, 28)
            xx = x0 + 52
            for ch_ in "GOLO":
                od.text((xx, y0 + 46), ch_, font=fg, fill=CORAL + (int(255 * a),), anchor="lm")
                xx += od.textlength(ch_, font=fg) + 9
            nome = cena.golo[2] if len(cena.golo) > 2 else (
                cena.titulo.split("·")[-1].strip() if "·" in cena.titulo else "")
            od.text((x0 + 50, y0 + 112), nome, font=fonte(SERIFA_N, 62), fill=CREME + (int(255 * a),), anchor="lm")
            od.text((x0 + cw - 44, y0 + chh / 2 + 4), cena.golo[1], font=fonte(SERIFA_N, 84),
                    fill=CREME + (int(255 * a),), anchor="rm")
        q.im.paste(ov, (0, 0), ov)

    def legenda(self, q, cena, t):
        """Legendas grandes, palavra a palavra (a palavra dita fica a coral)."""
        f = self.f["leg"]
        blocos = blocos_legenda(cena.palavras, lambda s: q.d.textlength(s, font=f))
        atual = None
        for b in blocos:
            if b[0][1] <= t:
                atual = b
        if not atual or t > atual[-1][2] + 0.6:
            return
        txt = " ".join(p[0] for p in atual)
        larg = q.d.textlength(txt, font=f)
        x, y = W / 2 - larg / 2, 372
        entrada = suave((t - atual[0][1]) / 0.12)
        dy = 14 * (1 - entrada)
        for p, t0, t1 in atual:
            cor = CORAL_CLARO if t0 <= t < t1 + 0.05 else CREME
            # contorno escuro para ler sobre qualquer fundo
            q.d.text((x, y + dy), p, font=f, fill=cor + (int(255 * entrada),), anchor="lm",
                     stroke_width=6, stroke_fill=(20, 20, 19, int(230 * entrada)))
            x += q.d.textlength(p + " ", font=f)

    def render(self, cenas, saida: Path, som=True, com_voz=True):
        """com_voz=False: a voz só serve para dar o ritmo às cenas e às legendas; no áudio fica só a música."""
        import imageio_ffmpeg
        falas, efeitos = [], []
        if som and any(c.voz for c in cenas):
            import audio
            ini = 0.0
            for c in cenas:
                if c.voz:
                    a = audio.narrar(c.voz, self.rapidez)
                    dv = len(a) / audio.SR
                    ref = getattr(c, "voz_ref", None)
                    c.esc = max(1.0, dv / ref) if ref else 1.0
                    c.dur = max(c.dur * c.esc, c.voz_ini + dv + self.folga)  # a cena espera pela voz
                    tempos_legenda(c, len(a) / audio.SR)
                    falas.append((ini + c.voz_ini, a))
                if ini > 0:
                    efeitos.append((ini - 0.12, "whoosh"))
                ini += c.dur
        total = sum(c.dur for c in cenas)
        wav = None
        if falas:
            wav = saida.with_suffix(".wav")
            audio.guardar_wav(wav, audio.misturar(total, falas if com_voz else [], efeitos=efeitos, bpm=self.bpm,
                                                  vol_musica=0.55 if com_voz else 0.8))
        n = int(total * FPS)
        cmd = [imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
               "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-"] + (["-i", str(wav)] if wav else []) + [
               "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p"] + (
               ["-c:a", "aac", "-b:a", "192k", "-shortest"] if wav else []) + ["-movflags", "+faststart", str(saida)]
        pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        ini, idx = 0.0, 0
        for c in cenas:
            nf = int(round(c.dur * FPS))
            for i in range(nf):
                t = i / FPS
                pr.stdin.write(self.desenhar(c, t, (ini + t) / total).tobytes())
                idx += 1
            ini += c.dur
        pr.stdin.close()
        pr.wait()
        if wav:
            wav.unlink(missing_ok=True)
        return saida, total

    def capa(self, cena, t, saida: Path):
        if cena.legenda and not cena.palavras:  # sem voz: estima 15 letras por segundo
            tempos_legenda(cena, len(cena.legenda) / 15)
        self.desenhar(cena, t, 0).save(saida)


# ------------------------------------------------------------------ fecho com humor (igual em todos os vídeos)

PFP = AQUI.parent / "imagens" / "pfp_agente_claudio.png"
FRASES_FECHO = [
    ("[laughs] Manda isto ao teu amigo que é alérgico a acertar uma bet.",
     ["Manda isto ao teu amigo", "que é |alérgico|", "a acertar uma bet."]),
    ("[laughs] Manda isto ao teu amigo que cruza como o Benfica: um em dezanove.",
     ["Manda isto ao teu amigo", "que |cruza| como o Benfica:", "1 em 19."]),
    ("[laughs] Manda isto ao teu amigo que tem setenta e oito por cento de posse... e mesmo assim perde.",
     ["Manda isto ao teu amigo", "que tem |78%| de posse", "e mesmo assim perde."]),
    ("[laughs] Manda isto ao teu amigo que em dois dias nem consegue arrumar o quarto.",
     ["Manda isto ao teu amigo", "que em |2 dias|", "nem arruma o quarto."]),
    ("[laughs] Manda isto ao teu amigo que, como o Porto, só ganha a sofrer.",
     ["Manda isto ao teu amigo", "que, como o Porto,", "só ganha a |sofrer|."]),
    ("[laughs] Manda isto ao teu amigo que sai aos cruzamentos como o Samuel Soares.",
     ["Manda isto ao teu amigo", "que sai aos cruzamentos", "como o |Samuel Soares|."]),
]


def fecho(linhas):
    """Sobreposição final: robô, a piada em 3 linhas (|palavra| fica a coral), seguir e +18."""
    def sob(v, q, t):
        ov = Image.new("RGBA", q.im.size, (0, 0, 0, 0))
        ImageDraw.Draw(ov).rectangle((0, CY0 - 10, W, CY0 + CH + 10), fill=(20, 20, 19, int(242 * suave(t / 0.3))))
        q.im.paste(ov, (0, 0), ov)
        d = q.d
        if PFP.exists():
            k = suave((t - 0.05) / 0.35)
            balanco = math.sin(t * 5) * 6 * k  # o robô abana a cabeça, a rir
            r = int(130 * (0.85 + 0.15 * k))
            im = Image.open(PFP).convert("RGBA").resize((2 * r, 2 * r), Image.LANCZOS)
            m = Image.new("L", (2 * r, 2 * r), 0)
            ImageDraw.Draw(m).ellipse((0, 0, 2 * r, 2 * r), fill=int(255 * k))
            im.putalpha(m)
            im = im.rotate(balanco, resample=Image.BICUBIC)
            q.im.paste(im, (int(W / 2 - r), int(CY0 + 150 - r)), im)
        f = fonte(SERIFA_N, 74)
        for i, linha in enumerate(linhas):
            k = suave((t - 0.25 - i * 0.45) / 0.3)
            if k <= 0:
                continue
            partes = linha.split("|")
            larg = sum(d.textlength(p, font=f) for p in partes)
            x, y = W / 2 - larg / 2, CY0 + 400 + i * 100 + 12 * (1 - k)
            for j, p in enumerate(partes):
                cor = CORAL_CLARO if j % 2 else CREME
                d.text((x, y), p, font=f, fill=cor + (int(255 * k),), anchor="lm")
                x += d.textlength(p, font=f)
        k = suave((t - 1.9) / 0.4)
        if k > 0:
            txt = "Segue o Agente Claudio"
            fs = fonte(SANS_SB, 42)
            lw = d.textlength(txt, font=fs) + 70
            y = CY0 + 760
            d.rounded_rectangle((W / 2 - lw / 2, y - 38, W / 2 + lw / 2, y + 38), radius=38, fill=CORAL + (int(255 * k),))
            d.text((W / 2, y), txt, font=fs, fill=(20, 20, 19, int(255 * k)), anchor="mm")
            d.text((W / 2, CY0 + 880), "+18 · Joga com responsabilidade", font=fonte(SANS, 30),
                   fill=CREME_45 + (int(255 * k),), anchor="mm")
    return sob


def cena_fecho(jog, placar="", minuto="FIM", frase=0):
    voz, linhas = FRASES_FECHO[frase]
    c = Cena(3.6, "", "", jog, placar=placar, minuto=minuto, sobreposicao=fecho(linhas), nomes=False,
             voz=voz, voz_ini=0.25)
    c.t_capa = 3.0
    return c


def main():
    nome = sys.argv[1] if len(sys.argv) > 1 else "barcelona_astonvilla"
    spec = importlib.util.spec_from_file_location(nome, AQUI / "jogos" / f"{nome}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["quadro_tatico"] = sys.modules[__name__]
    sys.path.insert(0, str(AQUI))
    sys.path.insert(0, str(AQUI / "jogos"))
    spec.loader.exec_module(mod)
    v, cenas = mod.construir()
    saida = AQUI / f"{nome}.mp4"
    if "--capas" in sys.argv:  # só imagens de algumas cenas, para rever
        for i, c in enumerate(cenas):
            v.capa(c, getattr(c, "t_capa", c.dur * 0.75), AQUI / f"{nome}_cena{i + 1}.png")
        return
    com_voz = "--sem-voz" not in sys.argv
    if not com_voz:
        saida = saida.with_name(saida.stem + "_legendas.mp4")
    _, total = v.render(cenas, saida, som="--sem-som" not in sys.argv, com_voz=com_voz)
    v.capa(cenas[0], cenas[0].dur * 0.8, AQUI / f"{nome}_capa.png")
    print(f"{saida.name}: {total:.1f} s")


if __name__ == "__main__":
    main()
