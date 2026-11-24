"""Dinamarca 2–3 Noruega (Liga das Nações, Copenhaga, 17 nov 2026).

Fontes (verificadas a 17 nov 2026, depois do jogo):
- ESPN (summary 401861194): Dinamarca 4-2-3-1 (Hermansen; Kristensen, Andersen, Provstgaard, Mæhle; Hjulmand,
  Højbjerg; Isaksen, Damsgaard, Daramy; Højlund); Noruega 4-2-3-1 (Nyland; Ryerson, Ajer, Østigård, Heggem; Berge,
  Berg; Sørloth, Ødegaard, Nusa; Haaland). 11' Højlund (muito perto); 14' Højbjerg (cabeça, lado esquerdo da pequena
  área, cruzamento de Isaksen); 31' golo de Haaland anulado pelo VAR por mão; 37' Haaland (muito perto, assist.
  Ødegaard); 74' Ajer no poste direito; 83' Schjelderup no poste direito e golo de Ødegaard; 90+4' mão de Joachim
  Andersen, VAR dá penálti; 90+6' Haaland marca (pé esquerdo, canto inferior direito); 90+7' amarelo a Haaland por
  festejo excessivo. Remates 7–22, à baliza 4–7, cantos 1–7. Classificação: Portugal 15, Noruega 9, Dinamarca 9,
  Gales 3.
- ESPN (artigo): 2–0 "inside of 15 minutes"; Noruega fica em 2.º e vai aos quartos de final (março); Haaland
  "tore off his shirt", "sent Mads Hermansen the wrong way", 68 golos internacionais. ESPN (artigo do Gales–Portugal):
  a Dinamarca ganhou 4–1 em Portugal no sábado.
- Flashscore: atraso "misdirected" de Heggem para Nyland no 1–0; Isaksen com "time and space" na direita no 2–0;
  Schjelderup no poste e Ødegaard na recarga no 2–2; a Dinamarca vai ao play-off da Liga A/B.
- Agente Claudio (ramo claude/dados): dica do canal "Mais de 2.5 golos" (@1.49, mensagem 230) certa; previsão do
  modelo para o resultado: vitória da Noruega (39%), certa.
Cores dos equipamentos: a Dinamarca de vermelho, a Noruega a branco (para não confundir; não confirmado).
As jogadas são ilustrações coerentes com isto.
"""
from PIL import Image, ImageDraw

from quadro_tatico import (cena_fecho, sprite, CORAL, CREME, CREME_70, CY0, CH, W, Cena, Video, fonte, suave,
                           SERIFA_N, SANS, SANS_SB)

import porto_napoli as base
import benfica_lech as bl

vai, _ov, PFP, _visto = base.vai, base._ov, base.PFP, base._visto
_fundo, _chip = bl._fundo, bl._chip
VERMELHO = (200, 40, 50)
BRANCO = (236, 234, 226)
AZUL_NOR = (30, 40, 90)
AMARELO = (240, 200, 60)

FALAS = [
    ("Aos catorze minutos, a Noruega perdia dois a zero em Copenhaga. Aos noventa e seis, ganhava três a dois. E "
     "rematou vinte e duas vezes, contra sete.",
     "Aos 14 minutos, a Noruega perdia 2–0 em Copenhaga. Aos 96, ganhava 3–2. E rematou 22 vezes, contra 7."),
    ("Começa mal: aos onze, um atraso mal medido do Héguem para o guarda-redes, e o Róilund só tem de encostar.",
     "Começa mal: aos 11', um atraso mal medido do Heggem para o guarda-redes, e o Højlund só tem de encostar."),
    ("Três minutos depois, o Íssaksen tem tempo na direita, cruza, e o Róibierg cabeceia. Dois a zero.",
     "Três minutos depois, o Isaksen tem tempo na direita, cruza, e o Højbjerg cabeceia. 2–0."),
    ("O Hólan ainda vê um golo anulado pelo VAR, por mão. Mas aos trinta e sete, o Ódegor serve, e ele encosta. "
     "Dois a um.",
     "O Haaland ainda vê um golo anulado pelo VAR, por mão. Mas aos 37', o Ødegaard serve e ele encosta. 2–1."),
    ("Na segunda parte é só Noruega. O Ajer acerta no poste. Aos oitenta e três, é o Chélderup no poste, e o "
     "Ódegor, na recarga, empata.",
     "Na 2.ª parte é só Noruega. O Ajer acerta no poste. Aos 83', é o Schjelderup no poste e o Ødegaard, na "
     "recarga, empata."),
    ("Já nos descontos, o VAR apanha mão do Joachim Andersen na área. Grande penalidade: o Hólan engana o "
     "guarda-redes, tira a camisola, e vê amarelo.",
     "Já nos descontos, o VAR apanha mão do Joachim Andersen na área. Grande penalidade: o Haaland engana o "
     "guarda-redes, tira a camisola e vê amarelo."),
    ("Sessenta e oito golos em sessenta e um jogos. A Noruega vai aos quartos de final. E a Dinamarca, que no "
     "sábado tinha goleado Portugal, vai ao play-off.",
     "68 golos em 61 jogos. A Noruega vai aos quartos de final. E a Dinamarca, que no sábado tinha goleado "
     "Portugal, vai ao play-off."),
    ("E o Agente Claudio? A dica foi mais de dois golos e meio: entrou. E o modelo dava vitória da Noruega, mesmo "
     "a jogar fora. As dicas estão na rede vizinha, link na bio.",
     "E o Agente Claudio? A dica foi mais de 2,5 golos: entrou. E o modelo dava vitória da Noruega, mesmo a jogar "
     "fora. As dicas estão na rede vizinha, link na bio."),
    ("E tu? Quem decidiu este jogo: o Hólan, ou o Ódegor? Diz nos comentários.",
     "E tu? Quem decidiu este jogo: o Haaland ou o Ødegaard? Diz nos comentários."),
]

# ------------------------------------------------------------------ jogadores (Dinamarca ataca para cima)
JOG = {
    "hermansen": ("Hermansen", "casa", (0.50, 0.95)),
    "maehle": ("Mæhle", "casa", (0.15, 0.80)),
    "provst": ("Provstgaard", "casa", (0.38, 0.85)),
    "andersen": ("Andersen", "casa", (0.62, 0.85)),
    "kristensen": ("Kristensen", "casa", (0.85, 0.80)),
    "hojbjerg": ("Højbjerg", "casa", (0.40, 0.70)),
    "hjulmand": ("Hjulmand", "casa", (0.60, 0.70)),
    "daramy": ("Daramy", "casa", (0.17, 0.58)),
    "damsgaard": ("Damsgaard", "casa", (0.50, 0.60)),
    "isaksen": ("Isaksen", "casa", (0.83, 0.58)),
    "hojlund": ("Højlund", "casa", (0.50, 0.52)),
    "nyland": ("Nyland", "fora", (0.50, 0.04)),
    "ryerson": ("Ryerson", "fora", (0.15, 0.18)),
    "ajer": ("Ajer", "fora", (0.38, 0.14)),
    "ostigard": ("Østigård", "fora", (0.62, 0.14)),
    "heggem": ("Heggem", "fora", (0.85, 0.18)),
    "berge": ("Berge", "fora", (0.40, 0.30)),
    "berg": ("Berg", "fora", (0.60, 0.30)),
    "sorloth": ("Sørloth", "fora", (0.17, 0.42)),
    "odegaard": ("Ødegaard", "fora", (0.50, 0.40)),
    "nusa": ("Nusa", "fora", (0.83, 0.42)),
    "haaland": ("Haaland", "fora", (0.50, 0.50)),
}
SUBS_2P = {"heggem": "Møller Wolfe", "sorloth": "Schjelderup", "berg": "Bobb", "damsgaard": "Froholdt",
           "hojlund": "Osula", "kristensen": "Bah"}


def jogadores(pos, mov=None, mostrar=(), subs=None):
    out = {}
    for jid, (nome, eq, form) in JOG.items():
        x, y = pos.get(jid, form)
        out[jid] = {"nome": (subs or {}).get(jid, nome) if jid in mostrar else "", "equipa": eq,
                    "chaves": (mov or {}).get(jid, [(0, x, y)])}
    return out


VI = 0.15


def T(x):
    return x + VI


# ------------------------------------------------------------------ sobreposições

def gancho(v, q, t):
    ov = _ov(q)
    d = ImageDraw.Draw(ov)
    d.rectangle((0, CY0 + CH * 0.10, W, CY0 + CH * 0.86), fill=(20, 20, 19, 232))
    d.text((W / 2, CY0 + CH * 0.10 + 55), "COPENHAGA", font=fonte(SANS_SB, 34), fill=CORAL + (255,), anchor="mm")
    for i, (mins, plac, ti, cor) in enumerate((("14'", "2–0", T(0.3), CREME), ("96'", "2–3", T(4.2), CORAL))):
        k = suave((t - ti) / 0.35)
        if k <= 0:
            continue
        al = int(255 * k)
        y = CY0 + 250 + i * 150
        d.text((W / 2 - 60, y), mins, font=fonte(SANS_SB, 44), fill=CREME_70 + (al,), anchor="rm")
        d.text((W / 2 - 20, y), plac, font=fonte(SERIFA_N, int(110 * (1.08 - 0.08 * k))), fill=cor + (al,),
               anchor="lm")
    for i, (nome, a, b, ti) in enumerate((("Remates", 7, 22, T(6.0)), ("À baliza", 4, 7, T(7.2)))):
        kk = suave((t - ti) / 0.35)
        if kk <= 0:
            continue
        al = int(255 * kk)
        y = CY0 + 610 + i * 110
        d.text((W / 2, y - 36), nome, font=fonte(SANS, 30), fill=CREME_70 + (al,), anchor="mm")
        x0, x1 = 270, W - 270
        xm = x0 + (x1 - x0) * a / (a + b)
        d.rounded_rectangle((x0, y - 12, x1, y + 12), radius=12, fill=(50, 48, 45, al))
        d.rounded_rectangle((x0, y - 12, x0 + (xm - x0) * kk, y + 12), radius=12, fill=VERMELHO + (al,))
        d.rounded_rectangle((x1 - (x1 - xm) * kk, y - 12, x1, y + 12), radius=12, fill=CREME + (al,))
        d.text((x0 - 30, y), str(a), font=fonte(SERIFA_N, 50), fill=CREME + (al,), anchor="rm")
        d.text((x1 + 30, y), str(b), font=fonte(SERIFA_N, 50), fill=(CORAL if i == 0 else CREME) + (al,),
               anchor="lm")
        if i == 0:
            d.text((x0 - 30, y - 50), "DIN", font=fonte(SANS_SB, 26), fill=CREME_70 + (al,), anchor="rm")
            d.text((x1 + 30, y - 50), "NOR", font=fonte(SANS_SB, 26), fill=CREME_70 + (al,), anchor="lm")
    q.im.paste(ov, (0, 0), ov)


def amarelo(v, q, t):
    k = suave((t - T(7.0)) / 0.25)
    if k <= 0:
        return
    ov = _ov(q)
    d = ImageDraw.Draw(ov)
    cx, cy = W - 170, CY0 + 140 - 20 * (1 - k)
    d.rounded_rectangle((cx - 38, cy - 52, cx + 38, cy + 52), radius=8, fill=AMARELO + (int(255 * k),))
    d.text((cx, cy + 82), "festejo", font=fonte(SANS_SB, 28), fill=CREME + (int(255 * k),), anchor="mm")
    q.im.paste(ov, (0, 0), ov)


def classificacao(v, q, t):
    _fundo(q, t)
    d = q.d
    k = suave((t - 0.05) / 0.3)
    if k > 0:
        d.text((W / 2, CY0 + 110), "Haaland pela Noruega", font=fonte(SANS, 32), fill=CREME_70 + (int(255 * k),),
               anchor="mm")
        d.text((W / 2, CY0 + 185), "68 golos · 61 jogos", font=fonte(SERIFA_N, 70), fill=CREME + (int(255 * k),),
               anchor="mm")
    linhas = [("Portugal", 15, "quartos", T(1.4), None), ("Noruega", 9, "quartos", T(1.4), T(2.3)),
              ("Dinamarca", 9, "play-off", T(1.4), T(5.9)), ("Gales", 3, "", T(1.4), None)]
    kk = suave((t - T(1.4)) / 0.35)
    if kk > 0:
        al = int(255 * kk)
        d.text((W / 2, CY0 + 300), "GRUPO · LIGA DAS NAÇÕES", font=fonte(SANS_SB, 28), fill=CORAL + (al,),
               anchor="mm")
    for i, (eq, pts, fim, ti, tdest) in enumerate(linhas):
        if kk <= 0:
            break
        al = int(255 * kk)
        y = CY0 + 380 + i * 90
        dest = tdest is not None and t >= tdest
        d.rounded_rectangle((120, y - 36, W - 120, y + 36), radius=18,
                            fill=((70, 40, 36) if dest else (36, 34, 32)) + (al,))
        d.text((160, y), f"{i + 1}.", font=fonte(SANS_SB, 32), fill=CREME_70 + (al,), anchor="lm")
        d.text((220, y), eq, font=fonte(SERIFA_N, 42), fill=CREME + (al,), anchor="lm")
        d.text((W / 2 + 120, y), f"{pts} pts", font=fonte(SANS_SB, 32), fill=CREME + (al,), anchor="mm")
        if tdest is not None:
            kd = suave((t - tdest) / 0.3)
            if kd > 0:
                d.text((W - 160, y), fim, font=fonte(SANS_SB, 32), fill=CORAL + (int(255 * kd),), anchor="rm")
        elif fim:
            d.text((W - 160, y), fim, font=fonte(SANS_SB, 32), fill=CREME_70 + (al,), anchor="rm")


def cartao_agente(v, q, t):
    _fundo(q, t)
    d = q.d
    if PFP.exists():
        k = suave((t - 0.1) / 0.4)
        r = int(95 * (0.85 + 0.15 * k))
        im = Image.open(PFP).convert("RGB").resize((2 * r, 2 * r), Image.LANCZOS)
        m = Image.new("L", (2 * r, 2 * r), 0)
        ImageDraw.Draw(m).ellipse((0, 0, 2 * r, 2 * r), fill=int(255 * k))
        q.im.paste(im, (int(W / 2 - r), int(CY0 + 110 - r)), m)
    linhas = [("A dica · odd 1,49", "Mais de 2,5 golos", T(1.1), T(2.6)),
              ("A previsão do modelo · 39%", "Vitória da Noruega", T(3.2), T(4.7))]
    for i, (cab, txt, ti, tv) in enumerate(linhas):
        kk = suave((t - ti) / 0.3)
        if kk <= 0:
            continue
        al = int(255 * kk)
        y = CY0 + 300 + i * 160
        d.rounded_rectangle((80, y - 64, W - 80, y + 64), radius=24, fill=(36, 34, 32, al),
                            outline=(70, 66, 60, al), width=2)
        d.text((190, y - 26), cab, font=fonte(SANS, 28), fill=CREME_70 + (al,), anchor="lm")
        d.text((190, y + 20), txt, font=fonte(SERIFA_N, 48), fill=CREME + (al,), anchor="lm")
        kv = suave((t - tv) / 0.25)
        if kv > 0:
            _visto(d, 135, y, kv, r=28)
    k = suave((t - T(5.9)) / 0.3)
    if k > 0:
        _chip(d, W / 2, CY0 + 640, "Dicas na rede vizinha · link na bio", CORAL, k, tam=36)


def pergunta(v, q, t):
    _fundo(q, t)
    d = q.d
    k = suave((t - 0.1) / 0.35)
    if k > 0:
        d.text((W / 2, CY0 + 170), "Quem decidiu o jogo?", font=fonte(SERIFA_N, 66), fill=CREME + (int(255 * k),),
               anchor="mm")
    for i, (letra, l1, l2, ti, cor) in enumerate((("A", "Haaland", "2 golos", T(1.8), BRANCO),
                                                  ("B", "Ødegaard", "golo + assistência", T(2.4), AZUL_NOR))):
        kk = suave((t - ti) / 0.35)
        if kk <= 0:
            continue
        al = int(255 * kk)
        cx, cy = W / 2 + (-215 if i == 0 else 215), CY0 + 410
        d.rounded_rectangle((cx - 200, cy - 125, cx + 200, cy + 125), radius=28, fill=cor + (al,))
        tc = (20, 20, 19) if i == 0 else CREME
        d.text((cx, cy - 50), letra, font=fonte(SERIFA_N, 66), fill=tc + (al,), anchor="mm")
        d.text((cx, cy + 25), l1, font=fonte(SANS_SB, 38), fill=tc + (al,), anchor="mm")
        d.text((cx, cy + 72), l2, font=fonte(SANS, 28), fill=tc + (al,), anchor="mm")
    k = suave((t - T(3.0)) / 0.3)
    if k > 0:
        d.text((W / 2, CY0 + 680), "Comenta A ou B", font=fonte(SANS_SB, 50), fill=CORAL + (int(255 * k),),
               anchor="mm")


# ------------------------------------------------------------------ cenas

REF_VOZ = [8.88, 5.14, 5.33, 6.44, 7.68, 8.17, 7.59, 8.46, 4.22]


def construir():
    v = Video("Dinamarca", "Noruega", abrev=("DIN", "NOR"),
              fonte_txt="Ilustração · dados ESPN, Flashscore e Agente Claudio")
    v.folga, v.bpm = 0.35, 112
    v.sp["casa"] = sprite(17, VERMELHO, BRANCO, 4)    # Dinamarca
    v.sp["fora"] = sprite(17, BRANCO, AZUL_NOR, 3)    # Noruega (cor neutra para não confundir)
    cenas = []

    def cena(dur, titulo, i, jog, **kw):
        voz, leg = FALAS[i]
        c = Cena(dur, titulo, "", jog, voz=voz, legenda=leg, voz_ini=VI, **kw)
        c.voz_ref = REF_VOZ[i]
        cenas.append(c)
        return c

    c = cena(9.3, "Dinamarca 2–3 Noruega", 0, jogadores({}), placar="2–3", minuto="FIM", sobreposicao=gancho,
             nomes=False)
    c.t_capa = 8.8

    # 1. 11': atraso mal medido de Heggem para Nyland, Højlund encosta (vista do ataque dinamarquês)
    pos1 = {"ryerson": (0.20, 0.14), "ajer": (0.40, 0.12), "ostigard": (0.62, 0.13), "berge": (0.42, 0.28),
            "berg": (0.62, 0.30), "sorloth": (0.22, 0.38), "odegaard": (0.50, 0.40), "nusa": (0.80, 0.40),
            "haaland": (0.52, 0.50), "daramy": (0.20, 0.26), "damsgaard": (0.44, 0.30), "isaksen": (0.86, 0.30),
            "hojbjerg": (0.40, 0.48), "hjulmand": (0.62, 0.50), "maehle": (0.12, 0.44), "kristensen": (0.90, 0.46),
            "provst": (0.40, 0.66), "andersen": (0.60, 0.66), "hermansen": (0.5, 0.92)}
    mov = {"heggem": vai((0.82, 0.22), (0.80, 0.20), T(0.8), T(1.2), 99),
           "hojlund": [(0, 0.54, 0.22), (T(1.6), 0.54, 0.22), (T(2.6), 0.56, 0.08), (99, 0.55, 0.07)],
           "nyland": [(0, 0.5, 0.03), (T(2.0), 0.50, 0.03), (T(2.8), 0.48, 0.05), (99, 0.48, 0.05)]}
    bola = [(0, 0.80, 0.21), (T(1.3), 0.80, 0.21), (T(2.5), 0.56, 0.08), (T(3.9), 0.56, 0.075), (T(4.3), 0.50, 0.0)]
    cena(5.6, "O 1–0", 1, jogadores(pos1, mov, mostrar={"heggem", "hojlund"}), bola=bola, placar="0–0",
         minuto="11'", vista="ataque", golo=(T(4.35), "1–0", "Højlund"),
         formas=[{"tipo": "rotulo", "x": 0.74, "y": 0.10, "texto": "atraso mal medido", "cor": CORAL,
                  "t0": T(1.5), "t1": T(3.4)}],
         setas=[{"pts": [(0.80, 0.21), (0.56, 0.08)], "t0": T(1.3), "t1": T(2.5), "tipo": "passe"},
                {"pts": [(0.56, 0.075), (0.50, 0.0)], "t0": T(3.9), "t1": T(4.3), "tipo": "remate"}],
         destaques=[("heggem", T(1.8), T(2.6)), ("hojlund", T(3.4), 5.6)])

    # 2. 14': Isaksen com tempo na direita, cruza, Højbjerg cabeceia (vista do ataque)
    pos2 = {"nyland": (0.5, 0.03), "ryerson": (0.22, 0.12), "ajer": (0.40, 0.09), "ostigard": (0.58, 0.09),
            "berge": (0.44, 0.24), "berg": (0.62, 0.24), "sorloth": (0.24, 0.32), "odegaard": (0.52, 0.36),
            "nusa": (0.76, 0.34), "haaland": (0.54, 0.48), "hojlund": (0.52, 0.07), "daramy": (0.26, 0.12),
            "damsgaard": (0.50, 0.22), "hjulmand": (0.60, 0.42), "maehle": (0.14, 0.40), "kristensen": (0.86, 0.40),
            "provst": (0.40, 0.62), "andersen": (0.60, 0.62), "hermansen": (0.5, 0.92)}
    mov = {"isaksen": vai((0.84, 0.26), (0.86, 0.15), T(1.3), T(2.4), 99),
           "heggem": vai((0.76, 0.14), (0.78, 0.17), T(1.6), T(2.6), 99),
           "hojbjerg": vai((0.40, 0.22), (0.41, 0.065), T(2.6), T(3.5), 99),
           "nyland": [(0, 0.5, 0.03), (T(3.6), 0.5, 0.03), (T(3.9), 0.47, 0.03), (99, 0.47, 0.03)]}
    bola = [(0, 0.84, 0.26), (T(1.3), 0.84, 0.26), (T(2.4), 0.86, 0.15), (T(2.8), 0.86, 0.15), (T(3.5), 0.41, 0.065),
            (T(3.9), 0.55, 0.0)]
    cena(5.8, "O 2–0", 2, jogadores(pos2, mov, mostrar={"isaksen", "hojbjerg"}), bola=bola, placar="1–0",
         minuto="14'", vista="ataque", golo=(T(3.95), "2–0", "Højbjerg"),
         formas=[{"tipo": "rotulo", "x": 0.70, "y": 0.30, "texto": "tempo e espaço", "cor": CORAL, "t0": T(1.4),
                  "t1": T(2.9)}],
         setas=[{"pts": [(0.84, 0.26), (0.86, 0.15)], "t0": T(1.3), "t1": T(2.4), "tipo": "conducao"},
                {"pts": [(0.86, 0.15), (0.41, 0.065)], "t0": T(2.8), "t1": T(3.5), "tipo": "passe"},
                {"pts": [(0.41, 0.065), (0.55, 0.0)], "t0": T(3.5), "t1": T(3.9), "tipo": "remate"}],
         destaques=[("isaksen", T(1.2), T(2.9)), ("hojbjerg", T(3.3), 5.8)])

    # 3. 31' golo anulado (mão); 37' Ødegaard serve, Haaland encosta (vista da defesa dinamarquesa)
    pos3 = {"hermansen": (0.5, 0.97), "maehle": (0.20, 0.86), "provst": (0.40, 0.89), "andersen": (0.60, 0.89),
            "kristensen": (0.80, 0.86), "hojbjerg": (0.44, 0.78), "hjulmand": (0.60, 0.76), "daramy": (0.22, 0.70),
            "damsgaard": (0.52, 0.66), "isaksen": (0.82, 0.70), "hojlund": (0.50, 0.54), "ryerson": (0.18, 0.74),
            "nusa": (0.78, 0.82), "sorloth": (0.30, 0.82), "berge": (0.40, 0.64), "berg": (0.62, 0.62),
            "ajer": (0.40, 0.48), "ostigard": (0.60, 0.48), "heggem": (0.86, 0.62), "nyland": (0.5, 0.05)}
    mov = {"odegaard": vai((0.60, 0.74), (0.62, 0.82), T(2.8), T(3.9), 99),
           "haaland": vai((0.46, 0.80), (0.50, 0.92), T(3.9), T(4.8), 99),
           "hermansen": [(0, 0.5, 0.97), (T(4.4), 0.5, 0.97), (T(4.8), 0.55, 0.96), (99, 0.55, 0.96)]}
    bola = [(0, 0.60, 0.74), (T(2.8), 0.60, 0.74), (T(3.9), 0.62, 0.82), (T(4.1), 0.62, 0.82), (T(4.8), 0.50, 0.92),
            (T(5.0), 0.50, 0.92), (T(5.3), 0.48, 1.0)]
    cena(6.9, "O 2–1", 3, jogadores(pos3, mov, mostrar={"haaland", "odegaard"}), bola=bola, placar="2–0",
         minuto="37'", vista="defesa", golo=(T(5.35), "2–1", "Haaland"),
         formas=[{"tipo": "rotulo", "x": 0.5, "y": 0.60, "texto": "31' · anulado pelo VAR (mão)", "cor": BRANCO,
                  "t0": T(0.4), "t1": T(3.1)}],
         setas=[{"pts": [(0.62, 0.82), (0.50, 0.92)], "t0": T(4.1), "t1": T(4.8), "tipo": "passe"},
                {"pts": [(0.50, 0.92), (0.48, 1.0)], "t0": T(5.0), "t1": T(5.3), "tipo": "remate"}],
         destaques=[("haaland", T(0.3), T(2.8)), ("odegaard", T(3.9), T(4.8)), ("haaland", T(4.9), 6.9)])

    # 4. 2.ª parte: Ajer no poste; 83' Schjelderup no poste, Ødegaard na recarga (vista da defesa)
    pos4 = {"maehle": (0.24, 0.88), "provst": (0.40, 0.91), "andersen": (0.56, 0.91), "kristensen": (0.74, 0.88),
            "hojbjerg": (0.44, 0.82), "hjulmand": (0.62, 0.80), "daramy": (0.24, 0.74), "damsgaard": (0.52, 0.72),
            "isaksen": (0.80, 0.74), "hojlund": (0.50, 0.60), "ryerson": (0.16, 0.80), "nusa": (0.82, 0.84),
            "berge": (0.42, 0.70), "berg": (0.60, 0.68), "haaland": (0.46, 0.92), "ostigard": (0.58, 0.54),
            "heggem": (0.86, 0.66), "nyland": (0.5, 0.05)}
    mov = {"ajer": [(0, 0.24, 0.86), (T(1.6), 0.24, 0.86), (T(2.1), 0.22, 0.90), (T(3.0), 0.30, 0.80),
                    (99, 0.30, 0.80)],
           "sorloth": vai((0.66, 0.86), (0.58, 0.935), T(3.4), T(4.4), 99),
           "odegaard": vai((0.56, 0.76), (0.50, 0.87), T(4.6), T(5.6), 99),
           "hermansen": [(0, 0.5, 0.97), (T(4.5), 0.5, 0.97), (T(4.9), 0.47, 0.975), (T(6.6), 0.47, 0.975),
                         (T(6.9), 0.55, 0.97), (99, 0.55, 0.97)]}
    bola = [(0, 0.22, 0.90), (T(2.1), 0.22, 0.90), (T(2.6), 0.445, 0.995), (T(3.0), 0.36, 1.02), (T(3.6), 0.66, 0.86),
            (T(4.4), 0.58, 0.935), (T(4.8), 0.445, 0.995), (T(5.6), 0.50, 0.87), (T(6.6), 0.50, 0.87),
            (T(6.95), 0.52, 1.0)]
    cena(8.2, "O 2–2", 4, jogadores(pos4, mov, mostrar={"ajer", "sorloth", "odegaard"}, subs=SUBS_2P), bola=bola,
         placar="2–1", minuto="83'", vista="defesa", golo=(T(7.0), "2–2", "Ødegaard"),
         formas=[{"tipo": "rotulo", "x": 0.22, "y": 0.97, "texto": "poste", "cor": CORAL, "t0": T(2.6),
                  "t1": T(3.6)},
                 {"tipo": "rotulo", "x": 0.26, "y": 0.84, "texto": "outra vez o poste", "cor": CORAL, "t0": T(4.8),
                  "t1": T(6.4)},
                 {"tipo": "rotulo", "x": 0.70, "y": 0.80, "texto": "recarga", "cor": CORAL, "t0": T(6.1),
                  "t1": 8.2}],
         setas=[{"pts": [(0.22, 0.90), (0.445, 0.995)], "t0": T(2.1), "t1": T(2.6), "tipo": "remate"},
                {"pts": [(0.58, 0.935), (0.445, 0.995)], "t0": T(4.4), "t1": T(4.8), "tipo": "remate"},
                {"pts": [(0.50, 0.87), (0.52, 1.0)], "t0": T(6.6), "t1": T(6.95), "tipo": "remate"}],
         destaques=[("ajer", T(1.7), T(3.0)), ("sorloth", T(3.9), T(5.0)), ("odegaard", T(5.2), 8.2)])

    # 5. 90+4': mão de Andersen, VAR; 90+6' Haaland engana o guarda-redes (vista da defesa)
    pos5 = {"maehle": (0.22, 0.80), "provst": (0.38, 0.80), "kristensen": (0.70, 0.80), "hojbjerg": (0.46, 0.79),
            "hjulmand": (0.58, 0.80), "daramy": (0.30, 0.78), "damsgaard": (0.64, 0.78), "isaksen": (0.80, 0.78),
            "hojlund": (0.50, 0.62), "ryerson": (0.18, 0.76), "nusa": (0.84, 0.80), "berge": (0.42, 0.78),
            "berg": (0.54, 0.78), "sorloth": (0.34, 0.80), "odegaard": (0.62, 0.79), "ajer": (0.40, 0.60),
            "ostigard": (0.60, 0.58), "heggem": (0.76, 0.70), "nyland": (0.5, 0.05)}
    mov = {"andersen": [(0, 0.52, 0.88), (T(3.3), 0.52, 0.88), (T(3.9), 0.48, 0.80), (99, 0.48, 0.80)],
           "haaland": [(0, 0.40, 0.88), (T(3.3), 0.40, 0.88), (T(4.0), 0.50, 0.86), (T(4.6), 0.50, 0.875),
                       (T(5.4), 0.50, 0.88), (T(6.6), 0.70, 0.74), (99, 0.70, 0.74)],
           "hermansen": [(0, 0.5, 0.97), (T(4.6), 0.5, 0.97), (T(5.0), 0.57, 0.975), (99, 0.57, 0.975)]}
    bola = [(0, 0.52, 0.875), (T(3.3), 0.52, 0.875), (T(3.9), 0.50, 0.895), (T(4.7), 0.50, 0.895),
            (T(5.0), 0.455, 0.995), (99, 0.455, 0.995)]
    cena(8.7, "A grande penalidade", 5, jogadores(pos5, mov, mostrar={"andersen", "haaland"}, subs=SUBS_2P),
         bola=bola, placar="2–2", minuto="90+6'", vista="defesa", golo=(T(5.05), "2–3", "Haaland"),
         sobreposicao=amarelo,
         formas=[{"tipo": "rotulo", "x": 0.74, "y": 0.92, "texto": "VAR: mão", "cor": CORAL, "t0": T(1.7),
                  "t1": T(3.6)},
                 {"tipo": "rotulo", "x": 0.70, "y": 0.96, "texto": "engana o guarda-redes", "cor": CORAL,
                  "t0": T(5.2), "t1": T(6.4)}],
         setas=[{"pts": [(0.50, 0.895), (0.455, 0.995)], "t0": T(4.7), "t1": T(5.0), "tipo": "remate"}],
         destaques=[("andersen", T(1.8), T(3.4)), ("haaland", T(4.3), 8.7)])

    c = cena(8.0, "", 6, jogadores({}), placar="2–3", minuto="FIM", sobreposicao=classificacao, nomes=False)
    c.t_capa = 7.6
    c = cena(9.0, "", 7, jogadores({}), placar="2–3", minuto="FIM", sobreposicao=cartao_agente, nomes=False)
    c.t_capa = 8.6
    c = cena(4.8, "", 8, jogadores({}), placar="", sobreposicao=pergunta, nomes=False)
    c.t_capa = 4.4
    cenas.append(cena_fecho(jogadores({}), placar="2–3", minuto="FIM", frase=13))
    return v, cenas
