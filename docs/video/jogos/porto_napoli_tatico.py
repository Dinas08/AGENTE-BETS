"""Análise tática: FC Porto 4–1 Napoli (Liga dos Campeões, 4 nov 2026). Não é um resumo: explica porquê.

Fontes (verificadas a 5 nov 2026):
- ESPN: onzes, minutos, golos, substituições, estatísticas.
- Il Napolista: xG ao intervalo Porto 0,15 / Napoli 0,81; no fim 2,71 / 1,42. O 2–1 começa num pontapé longo de
  Meret e chega a Veiga em três passes. O Napoli aguenta 70 minutos e cai com o cansaço.
- Allegri (Prime Video): "Sulla prima c'è stata un'inversione ed è stato lasciato libero. Sulla seconda abbiamo
  deciso di marcare a uomo e loro sono stati bravi a cambiarsi." / "non avevo cambi".
- Farioli (O Jogo): Napoli "com quatro médios muito móveis"; Giménez e Fofana fora das posições habituais.
- Maisfutebol/TVI: Napoli em 3-5-1-1; Bednarek "tapou" Højlund; Rosario e Veiga "encheram o meio-campo".
As jogadas são ilustrações coerentes com isto.
"""
from quadro_tatico import (cena_fecho, CORAL, CREME, CREME_70, CY0, CH, VERDE, AZUL, W, Cena, Video, fonte, suave,
                           SERIFA_N, SANS, SANS_SB)
from PIL import Image, ImageDraw

import porto_napoli as base

JOG, SUBS_67, SUBS_80 = base.JOG, base.SUBS_67, base.SUBS_80
jogadores, vai, _ov, PFP, _visto = base.jogadores, base.vai, base._ov, base.PFP, base._visto

# (voz, legenda). Voz: números por extenso, nomes como se dizem, emoção só onde ajuda.
FALAS = [
    ("Ao intervalo, o Nápoles estava melhor. Então, como é que levou quatro? Três detalhes táticos explicam tudo.",
     "Ao intervalo, o Nápoles estava melhor. Então como é que levou 4? Três detalhes táticos explicam tudo."),
    ("O Nápoles veio com três centrais, e quatro médios sempre a trocar de posição. De Bruyne solto entre linhas, "
     "à procura do Højlund.",
     "O Nápoles veio com três centrais e quatro médios sempre a trocar de posição. De Bruyne solto entre linhas, "
     "à procura do Højlund."),
    ("A resposta do Porto: Bédnárek colado ao Højlund, e Rosario e Gábri Vêiga a fechar o meio. Mesmo assim, "
     "foi o Nápoles quem criou mais na primeira parte.",
     "A resposta do Porto: Bednarek colado ao Højlund, e Rosario e Gabri Veiga a fechar o meio. Mesmo assim, "
     "foi o Nápoles quem criou mais na primeira parte."),
    ("Detalhe número um: bolas paradas. No primeiro canto, o Nápoles trocou as marcações, e Bédnárek ficou "
     "sozinho na marca de grande penalidade.",
     "Detalhe nº 1: bolas paradas. No primeiro canto, o Nápoles trocou as marcações e Bednarek ficou "
     "sozinho na marca de grande penalidade."),
    ("No segundo, o Nápoles passou a marcar homem a homem. O Porto trocou posições dentro da área, os marcadores "
     "perderam-se, e Kívior cabeceou à vontade. Quem o explicou foi o próprio Allegri.",
     "No segundo, o Nápoles passou a marcar homem a homem. O Porto trocou posições dentro da área, os marcadores "
     "perderam-se e Kiwior cabeceou à vontade. Quem o explicou foi o próprio Allegri."),
    ("Detalhe número dois: o banco. O Allegri admitiu que não tinha alternativas. O Farioli mexeu cedo: Sá-mu aos "
     "cinquenta e cinco, Riménez e Zaidu aos sessenta e sete.",
     "Detalhe nº 2: o banco. O Allegri admitiu que não tinha alternativas. O Farioli mexeu cedo: Samu aos "
     "55', Giménez e Zaidu aos 67'."),
    ("Detalhe número três: com o cansaço, as linhas do Nápoles afastaram-se. Aos setenta e um, depois de um "
     "pontapé longo do Meret, bastaram três passes. Riménez mete no espaço, e Gábri Vêiga faz o dois a um.",
     "Detalhe nº 3: com o cansaço, as linhas do Nápoles afastaram-se. Aos 71', depois de um pontapé longo do "
     "Meret, bastaram três passes. Giménez mete no espaço e Gabri Veiga faz o 2–1."),
    ("Os golos esperados contam a história: ao intervalo, o Nápoles estava à frente. No fim, o Porto chegou "
     "quase aos três.",
     "Os golos esperados contam a história: ao intervalo, o Nápoles estava à frente. No fim, o Porto chegou "
     "quase aos 3."),
    ("O Agente Claudio tinha o Porto como favorito. E tu: o que pesou mais? As bolas paradas, ou o banco? "
     "Diz nos comentários.",
     "O Agente Claudio tinha o Porto como favorito. E tu: o que pesou mais? As bolas paradas ou o banco? "
     "Diz nos comentários."),
]


# ------------------------------------------------------------------ sobreposições

def _fundo(q, t, alfa=238):
    ov = _ov(q)
    ImageDraw.Draw(ov).rectangle((0, CY0 - 10, W, CY0 + CH + 10), fill=(20, 20, 19, int(alfa * suave(t / 0.3))))
    q.im.paste(ov, (0, 0), ov)


def gancho(v, q, t):
    """Primeiro frame já cheio (capa): o 4–1 e o paradoxo do xG ao intervalo."""
    ov = _ov(q)
    d = ImageDraw.Draw(ov)
    d.rectangle((0, CY0 + CH * 0.16, W, CY0 + CH * 0.80), fill=(20, 20, 19, 228))
    esc = 1.1 - 0.1 * suave(t / 0.3)
    d.text((W / 2, CY0 + CH * 0.31), "4–1", font=fonte(SERIFA_N, 230 * esc), fill=CREME + (255,), anchor="mm")
    d.text((W / 2, CY0 + CH * 0.44), "PORTO  ·  NÁPOLES", font=fonte(SANS_SB, 40), fill=CORAL + (255,), anchor="mm")
    k = suave((t - 0.5) / 0.35)
    if k > 0:
        d.text((W / 2, CY0 + CH * 0.54), "golos esperados ao intervalo", font=fonte(SANS, 34),
               fill=CREME_70 + (int(255 * k),), anchor="mm")
        d.text((W / 2 - 150, CY0 + CH * 0.62), "0,15", font=fonte(SERIFA_N, 84), fill=CORAL + (int(255 * k),),
               anchor="mm")
        d.text((W / 2, CY0 + CH * 0.62), "vs", font=fonte(SANS, 34), fill=CREME_70 + (int(255 * k),), anchor="mm")
        d.text((W / 2 + 150, CY0 + CH * 0.62), "0,81", font=fonte(SERIFA_N, 84), fill=AZUL + (int(255 * k),),
               anchor="mm")
    k = suave((t - 3.6) / 0.3)
    if k > 0:
        txt = "3 detalhes táticos"
        f = fonte(SANS_SB, 40)
        lw = d.textlength(txt, font=f) + 64
        y = CY0 + CH * 0.73
        d.rounded_rectangle((W / 2 - lw / 2, y - 34, W / 2 + lw / 2, y + 34), radius=34, fill=CORAL + (int(255 * k),))
        d.text((W / 2, y), txt, font=f, fill=(20, 20, 19, int(255 * k)), anchor="mm")
    q.im.paste(ov, (0, 0), ov)


def citacao(t0, texto, autor):
    """Cartão com uma citação, em baixo no campo."""
    def sob(v, q, t):
        k = suave((t - t0) / 0.35)
        if k <= 0:
            return
        ov = _ov(q)
        d = ImageDraw.Draw(ov)
        x0, x1, y0 = 70, W - 70, CY0 + 640 + 20 * (1 - k)
        f = fonte(SERIFA_N, 42)
        linhas, atual = [], ""
        for pal in texto.split():
            tt = (atual + " " + pal).strip()
            if d.textlength(tt, font=f) > x1 - x0 - 90 and atual:
                linhas.append(atual)
                atual = pal
            else:
                atual = tt
        linhas.append(atual)
        alt = 58 * len(linhas) + 100
        d.rounded_rectangle((x0, y0, x1, y0 + alt), radius=26, fill=(24, 23, 22, int(245 * k)),
                            outline=(70, 66, 60, int(255 * k)), width=2)
        d.rounded_rectangle((x0, y0, x0 + 12, y0 + alt), radius=6, fill=AZUL + (int(255 * k),))
        for i, l in enumerate(linhas):
            d.text((x0 + 48, y0 + 50 + i * 58), l, font=f, fill=CREME + (int(255 * k),), anchor="lm")
        d.text((x0 + 48, y0 + alt - 38), autor, font=fonte(SANS_SB, 30), fill=AZUL + (int(255 * k),), anchor="lm")
        q.im.paste(ov, (0, 0), ov)
    return sob


def banco(v, q, t):
    _fundo(q, t)
    d = q.d
    k = suave((t - 0.2) / 0.4)
    d.text((W / 2, CY0 + 70), "Primeira substituição", font=fonte(SANS, 40), fill=CREME_70 + (int(255 * k),),
           anchor="mm")
    xp, xn = W / 2 - 230, W / 2 + 230
    for x, eq, cor in ((xp, "PORTO", CORAL), (xn, "NÁPOLES", AZUL)):
        d.text((x, CY0 + 160), eq, font=fonte(SANS_SB, 36), fill=cor + (int(255 * k),), anchor="mm")
    k = suave((t - 4.3) / 0.3)
    d.text((xp, CY0 + 270), "55'", font=fonte(SERIFA_N, 120), fill=CREME + (int(255 * k),), anchor="mm")
    k = suave((t - 1.9) / 0.3)
    d.text((xn, CY0 + 270), "78'", font=fonte(SERIFA_N, 120), fill=CREME + (int(255 * k),), anchor="mm")
    d.text((xn, CY0 + 370), "“Não tinha alternativas”", font=fonte(SANS, 30), fill=CREME_70 + (int(255 * k),),
           anchor="mm")
    d.text((xn, CY0 + 410), "Allegri", font=fonte(SANS_SB, 28), fill=AZUL + (int(255 * k),), anchor="mm")
    trocas = [("55'", "Samu", 5.3), ("67'", "Giménez", 6.1), ("67'", "Zaidu", 6.7), ("78'", "Hwang · Fofana", 7.2)]
    for i, (m, nome, ti) in enumerate(trocas):
        k = suave((t - ti) / 0.3)
        if k <= 0:
            continue
        y = CY0 + 500 + i * 92
        d.rounded_rectangle((xp - 200, y - 36, xp + 200, y + 36), radius=18, fill=(44, 42, 39, int(255 * k)))
        d.text((xp - 170, y), m, font=fonte(SANS_SB, 32), fill=CORAL + (int(255 * k),), anchor="lm")
        d.text((xp - 80, y), nome, font=fonte(SANS_SB, 34), fill=CREME + (int(255 * k),), anchor="lm")
    k = suave((t - 7.2) / 0.3)
    if k > 0:
        y = CY0 + 500
        d.rounded_rectangle((xn - 200, y - 36, xn + 200, y + 36), radius=18, fill=(44, 42, 39, int(255 * k)))
        d.text((xn - 170, y), "78'", font=fonte(SANS_SB, 32), fill=AZUL + (int(255 * k),), anchor="lm")
        d.text((xn - 80, y), "Lang · Giovane", font=fonte(SANS_SB, 34), fill=CREME + (int(255 * k),), anchor="lm")


def xg(v, q, t):
    _fundo(q, t)
    d = q.d
    k = suave((t - 0.2) / 0.4)
    d.text((W / 2, CY0 + 70), "Golos esperados (xG)", font=fonte(SERIFA_N, 60), fill=CREME + (int(255 * k),),
           anchor="mm")
    d.text((W / 2, CY0 + 140), "PORTO                    NÁPOLES", font=fonte(SANS_SB, 30),
           fill=CREME_70 + (int(255 * k),), anchor="mm")
    blocos = [("AO INTERVALO", 0.15, 0.81, 2.1), ("NO FIM", 2.71, 1.42, 4.4)]
    for i, (nome, a, b, ti) in enumerate(blocos):
        k = suave((t - ti) / 0.5)
        if k <= 0:
            continue
        y = CY0 + 300 + i * 300
        d.text((W / 2, y - 70), nome, font=fonte(SANS_SB, 34), fill=CREME_70 + (int(255 * k),), anchor="mm")
        fv = fonte(SERIFA_N, 76)
        d.text((150, y + 10), f"{a * k:.2f}".replace(".", ","), font=fv, fill=CREME + (int(255 * k),), anchor="lm")
        d.text((W - 150, y + 10), f"{b * k:.2f}".replace(".", ","), font=fv, fill=CREME + (int(255 * k),),
               anchor="rm")
        meio, esc = W / 2, 330 / 3.0
        d.rounded_rectangle((meio - 4 - a * esc * k, y + 70, meio - 4, y + 100), radius=12,
                            fill=CORAL + (int(255 * k),))
        d.rounded_rectangle((meio + 4, y + 70, meio + 4 + b * esc * k, y + 100), radius=12,
                            fill=AZUL + (int(255 * k),))
    k = suave((t - 5.5) / 0.4)
    d.text((W / 2, CY0 + 900), "xG: Il Napolista", font=fonte(SANS, 26), fill=CREME_70 + (int(200 * k),), anchor="mm")


def pergunta(v, q, t):
    _fundo(q, t)
    d = q.d
    if PFP.exists():
        k = suave((t - 0.1) / 0.4)
        r = int(110 * (0.85 + 0.15 * k))
        im = Image.open(PFP).convert("RGB").resize((2 * r, 2 * r), Image.LANCZOS)
        m = Image.new("L", (2 * r, 2 * r), 0)
        ImageDraw.Draw(m).ellipse((0, 0, 2 * r, 2 * r), fill=int(255 * k))
        q.im.paste(im, (int(W / 2 - r), int(CY0 + 130 - r)), m)
    k = suave((t - 1.3) / 0.3)
    if k > 0:
        _visto(d, W / 2 - 250, CY0 + 300, k)
        d.text((W / 2 - 205, CY0 + 300), "Porto favorito: acertou", font=fonte(SANS_SB, 44),
               fill=CREME + (int(255 * k),), anchor="lm")
    k = suave((t - 2.2) / 0.3)
    d.text((W / 2, CY0 + 440), "O que pesou mais?", font=fonte(SERIFA_N, 76), fill=CREME + (int(255 * k),),
           anchor="mm")
    for i, (txt, ti) in enumerate((("Bolas paradas", 3.85), ("O banco", 4.6))):
        kk = suave((t - 2.6 - i * 0.15) / 0.35)
        if kk <= 0:
            continue
        cx, cy = W / 2 + (-215 if i == 0 else 215), CY0 + 620
        ativo = ti <= t < ti + 0.6
        cor = CORAL if ativo else (44, 42, 39)
        d.rounded_rectangle((cx - 195, cy - 90, cx + 195, cy + 90), radius=28, fill=cor + (int(255 * kk),),
                            outline=(80, 76, 70, int(255 * kk)), width=2)
        d.text((cx, cy - 22), "AB"[i], font=fonte(SERIFA_N, 60), fill=CREME + (int(255 * kk),), anchor="mm")
        d.text((cx, cy + 42), txt, font=fonte(SANS_SB, 38), fill=CREME + (int(255 * kk),), anchor="mm")
    k = suave((t - 5.2) / 0.3)
    d.text((W / 2, CY0 + 800), "Comenta A ou B", font=fonte(SANS_SB, 48), fill=CORAL + (int(255 * k),), anchor="mm")


# ------------------------------------------------------------------ cenas

REF_VOZ = [5.38, 7.43, 7.38, 6.86, 8.94, 7.94, 10.63, 6.85, 6.56]  # durações com que as cenas foram acertadas
CORAL_E = CORAL


def construir():
    v = Video("Porto", "Nápoles", abrev=("POR", "NAP"), fonte_txt="Ilustração · dados ESPN · xG Il Napolista")
    v.folga, v.bpm = 0.35, 112
    VI = 0.15
    cenas = []

    def cena(dur, titulo, i, jog, **kw):
        voz, leg = FALAS[i]
        c = Cena(dur, titulo, "", jog, voz=voz, legenda=leg, voz_ini=VI, **kw)
        c.voz_ref = REF_VOZ[i]
        cenas.append(c)
        return c

    def T(x):  # tempo da palavra na fala + início da voz
        return x + VI

    # 0. gancho
    c = cena(5.8, "Porto 4–1 Nápoles: a tática", 0, jogadores({}), placar="4–1", minuto="FIM",
             sobreposicao=gancho, nomes=False)
    c.t_capa = 4.2

    # posições de ataque organizado do Nápoles (ataca para baixo) contra o bloco do Porto
    NAP = {"meret": (0.5, 0.04), "beukema": (0.30, 0.28), "rrahmani": (0.50, 0.26), "marin": (0.70, 0.28),
           "politano": (0.10, 0.56), "vergara": (0.90, 0.56), "gilmour": (0.50, 0.42), "anguissa": (0.36, 0.52),
           "mctominay": (0.64, 0.52), "debruyne": (0.58, 0.62), "hojlund": (0.47, 0.83)}
    POR = {"costa": (0.5, 0.96), "martim": (0.18, 0.84), "kiwior": (0.40, 0.86), "bednarek": (0.58, 0.86),
           "acosta": (0.82, 0.84), "rosario": (0.50, 0.70), "veiga": (0.35, 0.68), "froholdt": (0.65, 0.68),
           "sainz": (0.20, 0.57), "silva": (0.44, 0.55), "pepe": (0.80, 0.57)}
    pos = dict(NAP, **POR)
    mid_porto, def_porto = ["rosario", "veiga", "froholdt"], ["martim", "kiwior", "bednarek", "acosta"]

    # 1. o plano do Nápoles: três centrais, quatro médios móveis, De Bruyne entre linhas
    mov = {"anguissa": vai(NAP["anguissa"], (0.62, 0.50), T(3.0), T(3.9)),
           "mctominay": vai(NAP["mctominay"], (0.38, 0.54), T(3.0), T(3.9)),
           "gilmour": vai(NAP["gilmour"], (0.50, 0.36), T(3.0), T(3.9)),
           "debruyne": vai(NAP["debruyne"], (0.56, 0.765), T(4.2), T(5.3))}
    bola = [(0, 0.50, 0.43), (T(4.6), 0.50, 0.43), (T(5.3), 0.555, 0.755), (T(5.9), 0.555, 0.755),
            (T(6.5), 0.47, 0.82)]
    cena(7.9, "O plano do Nápoles", 1, jogadores(pos, mov, mostrar={"debruyne", "hojlund", "anguissa", "mctominay",
                                                                   "gilmour", "beukema", "rrahmani", "marin"}),
         bola=bola, placar="0–0", minuto="",
         formas=[{"tipo": "linha", "ids": ["beukema", "rrahmani", "marin"], "cor": AZUL, "t0": T(0.9), "t1": T(3.0)},
                 {"tipo": "rotulo", "x": 0.5, "y": 0.20, "texto": "3 centrais", "cor": AZUL, "t0": T(0.9),
                  "t1": T(3.0)},
                 {"tipo": "rotulo", "x": 0.5, "y": 0.47, "texto": "4 médios móveis", "cor": AZUL, "t0": T(2.0),
                  "t1": T(4.2)},
                 {"tipo": "entre", "de": mid_porto, "ate": def_porto, "cor": AZUL, "rotulo": "entre linhas",
                  "t0": T(4.3), "t1": 7.9}],
         setas=[{"pts": [NAP["anguissa"], (0.62, 0.50)], "t0": T(3.0), "t1": T(3.9), "tipo": "corrida_fora"},
                {"pts": [NAP["mctominay"], (0.38, 0.54)], "t0": T(3.0), "t1": T(3.9), "tipo": "corrida_fora"},
                {"pts": [(0.50, 0.43), (0.555, 0.755)], "t0": T(4.6), "t1": T(5.3), "tipo": "passe"},
                {"pts": [(0.555, 0.755), (0.47, 0.82)], "t0": T(5.9), "t1": T(6.5), "tipo": "passe"}],
         destaques=[("debruyne", T(4.2), T(6.0)), ("hojlund", T(6.0), 7.9)])

    # 2. a resposta do Porto: Bednarek colado a Højlund, meio fechado; o Nápoles cria pelas alas
    pos2 = dict(pos, anguissa=(0.62, 0.50), mctominay=(0.38, 0.54), gilmour=(0.50, 0.36), debruyne=(0.56, 0.765))
    mov = {"bednarek": vai(POR["bednarek"], (0.53, 0.865), T(0.9), T(1.8)),
           "rosario": vai(POR["rosario"], (0.53, 0.735), T(2.3), T(3.6)),
           "veiga": vai(POR["veiga"], (0.45, 0.715), T(2.3), T(3.6)),
           "debruyne": vai((0.56, 0.765), (0.62, 0.66), T(3.0), T(4.0)),
           "politano": vai(NAP["politano"], (0.12, 0.78), T(4.9), T(6.0))}
    bola = [(0, 0.50, 0.37), (T(4.3), 0.50, 0.37), (T(4.9), 0.11, 0.57), (T(6.0), 0.13, 0.775),
            (T(6.6), 0.48, 0.86)]
    cena(7.8, "A resposta do Porto", 2,
         jogadores(pos2, mov, mostrar={"bednarek", "hojlund", "rosario", "veiga", "politano"}),
         bola=bola, placar="0–0", minuto="",
         formas=[{"tipo": "liga", "a": "bednarek", "b": "hojlund", "cor": CORAL, "t0": T(1.0), "t1": 7.8},
                 {"tipo": "zona", "pts": [(0.36, 0.64), (0.66, 0.64), (0.62, 0.80), (0.40, 0.80)], "cor": CORAL,
                  "rotulo": "meio fechado", "t0": T(2.6), "t1": T(4.6)},
                 {"tipo": "rotulo", "x": 0.5, "y": 0.15, "texto": "xG 1.ª parte: 0,15 – 0,81", "cor": AZUL,
                  "t0": T(4.6), "t1": 7.8}],
         setas=[{"pts": [(0.50, 0.37), (0.11, 0.57)], "t0": T(4.3), "t1": T(4.9), "tipo": "passe"},
                {"pts": [(0.11, 0.57), (0.13, 0.775)], "t0": T(4.9), "t1": T(6.0), "tipo": "conducao"},
                {"pts": [(0.13, 0.775), (0.48, 0.86)], "t0": T(6.0), "t1": T(6.6), "tipo": "passe"}],
         destaques=[("bednarek", T(0.9), T(2.2)), ("rosario", T(2.3), T(3.8)), ("veiga", T(2.3), T(3.8))])

    # 3. detalhe 1: o primeiro canto (11'): troca na marcação, Bednarek sozinho
    pos3 = {"veiga": (0.985, 0.012), "froholdt": (0.50, 0.25), "rosario": (0.55, 0.38), "martim": (0.25, 0.46),
            "acosta": (0.78, 0.42), "anguissa": (0.36, 0.14), "gilmour": (0.54, 0.21), "politano": (0.30, 0.25),
            "debruyne": (0.50, 0.30), "hojlund": (0.58, 0.42), "costa": (0.5, 0.95), "kiwior": (0.40, 0.17),
            "silva": (0.62, 0.06), "pepe": (0.46, 0.20), "sainz": (0.30, 0.21), "beukema": (0.43, 0.09),
            "marin": (0.66, 0.07), "rrahmani": (0.40, 0.12), "meret": (0.5, 0.02)}
    mov = {"vergara": vai((0.47, 0.11), (0.62, 0.15), T(3.0), T(3.9)),
           "mctominay": vai((0.60, 0.15), (0.45, 0.10), T(3.0), T(3.9)),
           "bednarek": vai((0.60, 0.20), (0.505, 0.108), T(3.9), T(5.1)),
           "meret": [(0, 0.5, 0.02), (T(5.8), 0.49, 0.02), (T(6.3), 0.45, 0.018)]}
    bola = [(0, 0.985, 0.012), (T(4.7), 0.985, 0.012), (T(5.1), 0.83, 0.045), (T(5.45), 0.67, 0.085),
            (T(5.8), 0.51, 0.108), (T(6.15), 0.462, 0.0)]
    cena(8.4, "Detalhe 1 · bolas paradas", 3,
         jogadores(pos3, mov, mostrar={"veiga", "bednarek", "vergara", "mctominay"}),
         bola=bola, placar="0–0", minuto="11'", vista="ataque", golo=(T(6.2), "1–0", "Bednarek"),
         formas=[{"tipo": "rotulo", "x": 0.53, "y": 0.27, "texto": "troca na marcação", "cor": AZUL, "t0": T(2.9),
                  "t1": T(4.4)},
                 {"tipo": "zona", "pts": [(0.44, 0.08), (0.57, 0.08), (0.57, 0.14), (0.44, 0.14)], "cor": CORAL,
                  "rotulo": "sozinho", "t0": T(4.3), "t1": T(6.2)}],
         setas=[{"pts": [(0.47, 0.11), (0.62, 0.15)], "t0": T(3.0), "t1": T(3.9), "tipo": "corrida_fora"},
                {"pts": [(0.60, 0.15), (0.45, 0.10)], "t0": T(3.0), "t1": T(3.9), "tipo": "corrida_fora"},
                {"pts": [(0.60, 0.20), (0.51, 0.11)], "t0": T(3.9), "t1": T(5.1), "tipo": "corrida"},
                {"pts": [(0.985, 0.012), (0.83, 0.045), (0.67, 0.085), (0.51, 0.108)], "t0": T(4.7),
                 "t1": T(5.8), "tipo": "passe"},
                {"pts": [(0.51, 0.108), (0.462, 0.005)], "t0": T(5.8), "t1": T(6.15), "tipo": "remate"}],
         destaques=[("vergara", T(2.9), T(4.0)), ("mctominay", T(2.9), T(4.0)), ("bednarek", T(4.0), T(7.0))])

    # 4. o segundo canto (80'): homem a homem, o Porto troca posições, Kiwior livre
    pos4 = {"veiga": (0.015, 0.012), "pepe": (0.62, 0.24), "froholdt": (0.50, 0.27), "rosario": (0.50, 0.38),
            "martim": (0.22, 0.42), "acosta": (0.75, 0.44), "costa": (0.5, 0.95), "anguissa": (0.40, 0.22),
            "gilmour": (0.58, 0.22), "vergara": (0.30, 0.045), "politano": (0.70, 0.30), "debruyne": (0.48, 0.32),
            "hojlund": (0.40, 0.44), "meret": (0.50, 0.02)}
    mov = {"kiwior": vai((0.60, 0.19), (0.48, 0.105), T(3.0), T(4.4)),
           "bednarek": vai((0.42, 0.17), (0.62, 0.09), T(3.0), T(4.2)),
           "silva": vai((0.53, 0.13), (0.40, 0.065), T(3.0), T(4.0)),
           "sainz": vai((0.45, 0.20), (0.55, 0.125), T(3.0), T(4.0)),
           "rrahmani": vai((0.63, 0.165), (0.57, 0.15), T(3.2), T(4.6)),
           "beukema": vai((0.44, 0.15), (0.61, 0.10), T(3.2), T(4.4)),
           "marin": vai((0.55, 0.11), (0.42, 0.075), T(3.2), T(4.2)),
           "mctominay": vai((0.47, 0.19), (0.54, 0.14), T(3.2), T(4.2)),
           "meret": [(0, 0.50, 0.02), (T(5.4), 0.51, 0.02), (T(5.9), 0.455, 0.018)]}
    bola = [(0, 0.015, 0.012), (T(4.5), 0.015, 0.012), (T(4.85), 0.17, 0.045), (T(5.2), 0.33, 0.085),
            (T(5.5), 0.48, 0.103), (T(5.85), 0.462, 0.0)]
    homem = [("rrahmani", "kiwior", T(4.4)), ("beukema", "bednarek", None), ("marin", "silva", None),
             ("mctominay", "sainz", None)]
    formas = [{"tipo": "liga", "a": a, "b": b, "cor": AZUL, "t0": T(1.4), "t1": T(6.3),
               **({"quebra": q} if q else {})} for a, b, q in homem]
    formas += [{"tipo": "rotulo", "x": 0.5, "y": 0.29, "texto": "homem a homem", "cor": AZUL, "t0": T(1.4),
                "t1": T(2.9)},
               {"tipo": "rotulo", "x": 0.5, "y": 0.29, "texto": "trocas de posição", "cor": CORAL, "t0": T(2.9),
                "t1": T(4.6)}]
    cena(10.6, "Bolas paradas · 2.º canto", 4,
         jogadores(pos4, mov, mostrar={"veiga", "kiwior", "rrahmani", "bednarek"}, subs=SUBS_80),
         bola=bola, placar="2–1", minuto="80'", vista="ataque", golo=(T(5.9), "3–1", "Kiwior"), formas=formas,
         sobreposicao=citacao(T(6.6), "“Marcámos homem a homem e eles foram bons a trocar-se.”",
                              "Allegri, treinador do Nápoles"),
         setas=[{"pts": [(0.60, 0.19), (0.48, 0.105)], "t0": T(3.0), "t1": T(4.4), "tipo": "corrida"},
                {"pts": [(0.42, 0.17), (0.62, 0.09)], "t0": T(3.0), "t1": T(4.2), "tipo": "corrida"},
                {"pts": [(0.015, 0.012), (0.17, 0.045), (0.33, 0.085), (0.48, 0.103)], "t0": T(4.5),
                 "t1": T(5.5), "tipo": "passe"},
                {"pts": [(0.48, 0.103), (0.462, 0.005)], "t0": T(5.5), "t1": T(5.85), "tipo": "remate"}],
         destaques=[("kiwior", T(2.9), T(6.6))])

    # 5. detalhe 2: o banco
    cena(8.4, "Detalhe 2 · o banco", 5, jogadores({}), placar="1–1", minuto="", sobreposicao=banco, nomes=False)

    # 6. detalhe 3: linhas afastadas e o contra-ataque do 2–1 (71')
    pos6 = {"politano": (0.12, 0.60), "vergara": (0.88, 0.60), "hojlund": (0.46, 0.64), "debruyne": (0.62, 0.66),
            "costa": (0.5, 0.95), "kiwior": (0.42, 0.78), "bednarek": (0.58, 0.78), "martim": (0.20, 0.72),
            "acosta": (0.80, 0.72), "rosario": (0.50, 0.67), "froholdt": (0.68, 0.62), "meret": (0.5, 0.04)}
    mov = {"gilmour": vai((0.50, 0.42), (0.50, 0.56), T(1.8), T(3.2)),
           "anguissa": vai((0.36, 0.44), (0.36, 0.57), T(1.8), T(3.2)),
           "mctominay": vai((0.64, 0.44), (0.64, 0.57), T(1.8), T(3.2)),
           "beukema": [(0, 0.32, 0.29), (T(7.4), 0.32, 0.29), (T(8.6), 0.40, 0.21)],
           "rrahmani": [(0, 0.50, 0.28), (T(7.4), 0.50, 0.28), (T(8.6), 0.50, 0.19)],
           "marin": [(0, 0.68, 0.29), (T(7.4), 0.68, 0.29), (T(8.6), 0.58, 0.21)],
           "silva": [(0, 0.56, 0.48), (T(6.5), 0.56, 0.47), (T(8.4), 0.63, 0.20), (99, 0.63, 0.20)],
           "sainz": [(0, 0.34, 0.47), (T(6.7), 0.38, 0.40), (T(7.4), 0.40, 0.38), (99, 0.40, 0.38)],
           "veiga": [(0, 0.56, 0.60), (T(6.6), 0.56, 0.58), (T(8.4), 0.52, 0.19), (T(9.0), 0.50, 0.135),
                     (99, 0.50, 0.135)],
           "pepe": vai((0.82, 0.50), (0.78, 0.28), T(6.6), T(8.6), 99)}
    bola = [(0, 0.5, 0.05), (T(5.0), 0.5, 0.05), (T(5.8), 0.48, 0.655), (T(6.0), 0.50, 0.66), (T(6.6), 0.555, 0.485),
            (T(6.75), 0.555, 0.485), (T(7.3), 0.395, 0.385), (T(7.6), 0.395, 0.385), (T(8.4), 0.52, 0.18),
            (T(9.0), 0.50, 0.13), (T(9.1), 0.50, 0.13), (T(9.45), 0.47, 0.0)]
    defesa, meio = ["beukema", "rrahmani", "marin"], ["anguissa", "gilmour", "mctominay"]
    cena(11.2, "Detalhe 3 · linhas partidas", 6,
         jogadores(pos6, mov, mostrar={"meret", "rosario", "silva", "sainz", "veiga"}, subs=SUBS_67),
         bola=bola, placar="1–1", minuto="71'", golo=(T(9.5), "2–1", "Gabri Veiga"),
         formas=[{"tipo": "linha", "ids": defesa, "cor": AZUL, "t0": T(1.5), "t1": T(7.4)},
                 {"tipo": "linha", "ids": meio, "cor": AZUL, "t0": T(1.5), "t1": T(7.4)},
                 {"tipo": "entre", "de": defesa, "ate": meio, "cor": CORAL, "rotulo": "espaço", "t0": T(2.0),
                  "t1": T(7.8)}],
         setas=[{"pts": [(0.5, 0.05), (0.48, 0.655)], "t0": T(5.0), "t1": T(5.8), "tipo": "passe"},
                {"pts": [(0.50, 0.66), (0.555, 0.485)], "t0": T(6.0), "t1": T(6.6), "tipo": "passe"},
                {"pts": [(0.555, 0.485), (0.395, 0.385)], "t0": T(6.75), "t1": T(7.3), "tipo": "passe"},
                {"pts": [(0.56, 0.58), (0.52, 0.19)], "t0": T(6.6), "t1": T(8.4), "tipo": "corrida"},
                {"pts": [(0.395, 0.385), (0.52, 0.18)], "t0": T(7.6), "t1": T(8.4), "tipo": "passe"},
                {"pts": [(0.50, 0.13), (0.47, 0.005)], "t0": T(9.1), "t1": T(9.45), "tipo": "remate"}],
         destaques=[("meret", T(4.8), T(5.8)), ("sainz", T(7.3), T(8.6)), ("veiga", T(8.6), 11.2)])

    # 7. xG
    cena(7.3, "Os números", 7, jogadores({}), placar="4–1", minuto="FIM", sobreposicao=xg, nomes=False)
    # 8. Agente Claudio + pergunta
    c = cena(7.0, "", 8, jogadores({}), placar="4–1", minuto="FIM", sobreposicao=pergunta, nomes=False)
    c.t_capa = 5.6
    # 9. fecho com humor
    cenas.append(cena_fecho(jogadores({}), placar="4–1"))
    return v, cenas
