"""Alemanha 5–0 Países Baixos (Liga das Nações, Berlim, 16 nov 2026). O Klopp disse "cinco" e fez cinco.

Fontes (verificadas a 17 nov 2026):
- ESPN (summary 401861185): onzes (4-2-3-1 os dois); golos 41' Scherhant (assist. Kimmich), 60' Wirtz (fora da
  área, pé esquerdo), 65' Schlotterbeck (cabeça, livre, assist. Gruda), 71' Wirtz (lado direito da pequena área,
  assist. Gruda), 77' Gruda; remates 18–9, à baliza 10–1, posse 56–44; 71 765 espectadores.
- Sky / Eurosport: Klopp quis travar os contra-ataques ("den Stock in die Speichen"); Schlotterbeck e Brown
  entram no onze; 19' Summerville escorrega na relva molhada num contra-ataque, 25' Malen falha; Gruda bate o livre
  do 3–0 (NOS diz Wirtz: seguimos Sky, Eurosport e ESPN) e assiste o 4–0; Scherhant, berlinense, cresceu a cinco
  minutos do estádio; 50.º jogo de Wirtz pela seleção; maior vitória com Klopp.
- Sportschau / Frühes-Tor: Klopp antes do jogo, "Im besten Fall machen wir fünf" (há a variante "Im Idealfall").
- NOS: Xavi "Dit was beschamend", pede desculpa aos adeptos, "99 procent door de values"; Dumfries: "Te slap in de
  duels", "ruimtes die te groot zijn"; maior derrota da Holanda desde 1959.
- ESPN (classificação): Alemanha, Holanda e Grécia com 11 pontos; Alemanha 1.ª, Holanda 2.ª, Grécia 3.ª.
- Agente Claudio (ramo claude/dados): previsão Alemanha 54% (acertou); dicas do canal: "Mais de 2.5 golos" neste
  jogo (message_id 213, Green) e "Vitória Alemanha" em Sérvia 1–3 Alemanha (message_id 160, Green).
As jogadas são ilustrações coerentes com isto.
"""
from PIL import Image, ImageDraw

from quadro_tatico import (cena_fecho, sprite, CORAL, CREME, CREME_70, CY0, CH, VERDE, AZUL, W, Cena, Video, fonte,
                           suave, SERIFA_N, SANS, SANS_SB)

import porto_napoli as base
import porto_napoli_tatico as tat
import benfica_lech as bl

vai, _ov, PFP, _visto = base.vai, base._ov, base.PFP, base._visto
_fundo, _chip = bl._fundo, bl._chip

FALAS = [
    ("Há três dias, a Holanda deu sete à Grécia. Ontem, em Berlim, levou cinco. E o Klopp tinha avisado: no melhor "
     "cenário, fazemos cinco.",
     "Há três dias, a Holanda deu 7 à Grécia. Ontem, em Berlim, levou 5. E o Klopp tinha avisado: no melhor "
     "cenário, fazemos cinco."),
    ("O plano do Klopp: travar os contra-ataques da Holanda, com o Schlotterbeck e o Brown a entrar no onze. Mesmo "
     "assim, a Holanda ainda assustou: o Summerville escorregou na relva molhada, e o Málen cabeceou por cima.",
     "O plano do Klopp: travar os contra-ataques da Holanda, com o Schlotterbeck e o Brown a entrar no onze. Mesmo "
     "assim, a Holanda ainda assustou: o Summerville escorregou na relva molhada e o Malen cabeceou por cima."),
    ("Depois, a Alemanha acordou. Abriu o Chérhant, um miúdo de Berlim que cresceu a cinco minutos do estádio. O "
     "Virtz, no jogo cinquenta pela seleção, bisou. E o Schlotterbeck marcou de cabeça.",
     "Depois, a Alemanha acordou. Abriu o Scherhant, um miúdo de Berlim que cresceu a cinco minutos do estádio. O "
     "Wirtz, no jogo 50 pela seleção, bisou. E o Schlotterbeck marcou de cabeça."),
    ("Mas o homem do jogo foi o Grúda, pela direita. Bateu o livre para o Schlotterbeck, serviu o Virtz no quatro "
     "a zero, e ainda fez o quinto.",
     "Mas o homem do jogo foi o Gruda, pela direita. Bateu o livre para o Schlotterbeck, serviu o Wirtz no 4–0 e "
     "ainda fez o quinto."),
    ("Do lado da Holanda, o Dumfries admitiu: moles nos duelos, espaços grandes demais. E o Xávi foi duro: isto foi "
     "vergonhoso. Pediu desculpa aos adeptos. É a maior derrota da Holanda desde mil novecentos e cinquenta e nove.",
     "Do lado da Holanda, o Dumfries admitiu: moles nos duelos, espaços grandes demais. E o Xavi foi duro: isto foi "
     "vergonhoso. Pediu desculpa aos adeptos. É a maior derrota da Holanda desde 1959."),
    ("E repara na tabela: Alemanha, Holanda e Grécia acabam todas com onze pontos. A Alemanha fica em primeiro, a "
     "Holanda passa em segundo, e a Grécia fica de fora.",
     "E repara na tabela: Alemanha, Holanda e Grécia acabam todas com 11 pontos. A Alemanha fica em primeiro, a "
     "Holanda passa em segundo e a Grécia fica de fora."),
    ("E o Agente Claudio? Deu a Alemanha a ganhar, com cinquenta e quatro por cento. A dica foi mais de dois golos e "
     "meio, e entrou. E na Sérvia, a dica foi vitória alemã: também entrou. As dicas estão na rede vizinha, link na "
     "bio.",
     "E o Agente Claudio? Deu a Alemanha a ganhar, com 54%. A dica foi mais de 2,5 golos e entrou. E na Sérvia, a "
     "dica foi vitória alemã: também entrou. As dicas estão na rede vizinha, link na bio."),
    ("E tu? A Alemanha é candidata a ganhar a Liga das Nações, ou foi a Holanda que não apareceu? Diz nos "
     "comentários.",
     "E tu? A Alemanha é candidata a ganhar a Liga das Nações, ou foi a Holanda que não apareceu? Diz nos "
     "comentários."),
]


# ------------------------------------------------------------------ jogadores (Alemanha ataca para cima)
JOG = {
    "terstegen": ("ter Stegen", "casa", (0.50, 0.95)),
    "brown": ("Brown", "casa", (0.15, 0.79)),
    "schlotterbeck": ("Schlotterbeck", "casa", (0.38, 0.85)),
    "tah": ("Tah", "casa", (0.62, 0.85)),
    "treu": ("Treu", "casa", (0.85, 0.79)),
    "kimmich": ("Kimmich", "casa", (0.40, 0.70)),
    "pavlovic": ("Pavlović", "casa", (0.60, 0.70)),
    "wirtz": ("Wirtz", "casa", (0.50, 0.60)),
    "scherhant": ("Scherhant", "casa", (0.17, 0.58)),
    "gruda": ("Gruda", "casa", (0.83, 0.58)),
    "havertz": ("Havertz", "casa", (0.50, 0.53)),
    "verbruggen": ("Verbruggen", "fora", (0.50, 0.04)),
    "dumfries": ("Dumfries", "fora", (0.15, 0.20)),
    "vanhecke": ("Van Hecke", "fora", (0.38, 0.15)),
    "vandeven": ("Van de Ven", "fora", (0.62, 0.15)),
    "jtimber": ("J. Timber", "fora", (0.85, 0.20)),
    "qtimber": ("Q. Timber", "fora", (0.40, 0.30)),
    "veerman": ("Veerman", "fora", (0.60, 0.30)),
    "reijnders": ("Reijnders", "fora", (0.50, 0.39)),
    "summerville": ("Summerville", "fora", (0.15, 0.38)),
    "gakpo": ("Gakpo", "fora", (0.85, 0.38)),
    "malen": ("Malen", "fora", (0.50, 0.46)),
}
LARANJA = (240, 122, 32)
BRANCO = (236, 234, 226)
PRETO = (25, 25, 25)
CINZA = (44, 42, 39)


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
    d.rectangle((0, CY0 + CH * 0.14, W, CY0 + CH * 0.84), fill=(20, 20, 19, 228))
    esc = 1.1 - 0.1 * suave(t / 0.3)
    d.text((W / 2, CY0 + CH * 0.28), "5–0", font=fonte(SERIFA_N, 230 * esc), fill=CREME + (255,), anchor="mm")
    d.text((W / 2, CY0 + CH * 0.41), "ALEMANHA  ·  HOLANDA", font=fonte(SANS_SB, 40), fill=LARANJA + (255,),
           anchor="mm")
    k = suave((t - T(2.0)) / 0.35)
    if k > 0:
        d.text((W / 2, CY0 + CH * 0.50), "3 dias depois do 7–0 à Grécia", font=fonte(SERIFA_N, 56),
               fill=CREME + (int(255 * k),), anchor="mm")
    k = suave((t - T(4.6)) / 0.35)
    if k > 0:
        y0 = CY0 + CH * 0.58 + 20 * (1 - k)
        d.rounded_rectangle((80, y0, W - 80, y0 + 190), radius=26, fill=(36, 34, 32, int(250 * k)),
                            outline=(70, 66, 60, int(255 * k)), width=2)
        d.rounded_rectangle((80, y0, 92, y0 + 190), radius=6, fill=CORAL + (int(255 * k),))
        d.text((125, y0 + 70), "“No melhor cenário, fazemos cinco.”", font=fonte(SERIFA_N, 50),
               fill=CREME + (int(255 * k),), anchor="lm")
        d.text((125, y0 + 140), "— Klopp, antes do jogo", font=fonte(SANS_SB, 32), fill=CORAL + (int(255 * k),),
               anchor="lm")
    q.im.paste(ov, (0, 0), ov)


def golos(v, q, t):
    _fundo(q, t)
    d = q.d
    k = suave((t - 0.1) / 0.35)
    if k > 0:
        d.text((W / 2, CY0 + 80), "Os 5 golos", font=fonte(SERIFA_N, 66), fill=CREME + (int(255 * k),), anchor="mm")
    lista = [("41'", "Scherhant", "berlinense · a 5 min do estádio", T(1.4)),
             ("60'", "Wirtz", "o 50.º jogo pela seleção", T(4.7)),
             ("65'", "Schlotterbeck", "de cabeça, num livre", T(6.8)),
             ("71'", "Wirtz", "bis", T(5.9)),
             ("77'", "Gruda", "…", T(7.9))]
    for i, (m, nome, nota, ti) in enumerate(lista):
        kk = suave((t - ti) / 0.3)
        if kk <= 0:
            continue
        y = CY0 + 200 + i * 112
        d.rounded_rectangle((90, y - 46, W - 90, y + 46), radius=20, fill=(BRANCO if i == 0 else CINZA) + (int(255 * kk),))
        tc = (20, 20, 19) if i == 0 else CREME
        d.text((130, y), m, font=fonte(SERIFA_N, 40), fill=(CORAL if i else (20, 20, 19)) + (int(255 * kk),),
               anchor="lm")
        d.text((250, y), nome, font=fonte(SANS_SB, 40), fill=tc + (int(255 * kk),), anchor="lm")
        d.text((W - 130, y), nota, font=fonte(SANS, 28), fill=(tc if i == 0 else CREME_70) + (int(255 * kk),),
               anchor="rm")
    k = suave((t - T(7.4)) / 0.3)
    if k > 0:
        d.text((W / 2, CY0 + 790), "Remates à baliza: 10 – 1", font=fonte(SANS, 32), fill=CREME_70 + (int(255 * k),),
               anchor="mm")


def holanda(v, q, t):
    _fundo(q, t)
    d = q.d
    k = suave((t - 0.1) / 0.35)
    if k > 0:
        d.text((W / 2, CY0 + 75), "E a Holanda?", font=fonte(SERIFA_N, 66), fill=CREME + (int(255 * k),), anchor="mm")
    # Dumfries
    k = suave((t - T(1.3)) / 0.3)
    if k > 0:
        y0 = CY0 + 150
        d.rounded_rectangle((70, y0, W - 70, y0 + 220), radius=24, fill=(36, 34, 32, int(255 * k)),
                            outline=(70, 66, 60, int(255 * k)), width=2)
        d.rounded_rectangle((70, y0, 82, y0 + 220), radius=6, fill=LARANJA + (int(255 * k),))
        d.text((112, y0 + 45), "Dumfries", font=fonte(SANS_SB, 36), fill=LARANJA + (int(255 * k),), anchor="lm")
        d.text((112, y0 + 110), "“Moles nos duelos.”", font=fonte(SERIFA_N, 46), fill=CREME + (int(255 * k),),
               anchor="lm")
        kk = suave((t - T(3.3)) / 0.3)
        if kk > 0:
            d.text((112, y0 + 175), "“Espaços grandes demais.”", font=fonte(SERIFA_N, 46),
                   fill=CREME + (int(255 * kk),), anchor="lm")
    # Xavi
    k = suave((t - T(4.9)) / 0.3)
    if k > 0:
        y0 = CY0 + 410
        d.rounded_rectangle((70, y0, W - 70, y0 + 230), radius=24, fill=(36, 34, 32, int(255 * k)),
                            outline=(70, 66, 60, int(255 * k)), width=2)
        d.rounded_rectangle((70, y0, 82, y0 + 230), radius=6, fill=CORAL + (int(255 * k),))
        d.text((112, y0 + 45), "Xavi", font=fonte(SANS_SB, 36), fill=CORAL + (int(255 * k),), anchor="lm")
        kk = suave((t - T(5.9)) / 0.3)
        if kk > 0:
            esc = 1.08 - 0.08 * kk
            d.text((112, y0 + 120), "“Isto foi vergonhoso.”", font=fonte(SERIFA_N, int(60 * esc)),
                   fill=CREME + (int(255 * kk),), anchor="lm")
        kk = suave((t - T(7.2)) / 0.3)
        if kk > 0:
            d.text((112, y0 + 190), "e pediu desculpa aos adeptos", font=fonte(SANS, 32),
                   fill=CREME_70 + (int(255 * kk),), anchor="lm")
    k = suave((t - T(8.9)) / 0.3)
    if k > 0:
        _chip(d, W / 2, CY0 + 750, "A maior derrota da Holanda desde 1959", LARANJA, k, tam=36)
    k = suave((t - T(9.5)) / 0.3)
    if k > 0:
        d.text((W / 2, CY0 + 830), "fonte: NOS", font=fonte(SANS, 24), fill=CREME_70 + (int(200 * k),), anchor="mm")


def grupo(v, q, t):
    _fundo(q, t)
    d = q.d
    k = suave((t - 0.1) / 0.35)
    if k > 0:
        d.text((W / 2, CY0 + 90), "Liga das Nações · o grupo", font=fonte(SERIFA_N, 58), fill=CREME + (int(255 * k),),
               anchor="mm")
    linhas = [("1.º", "Alemanha", 11, T(0.9), "quartos", T(3.0), BRANCO),
              ("2.º", "Holanda", 11, T(1.3), "quartos", T(4.1), LARANJA),
              ("3.º", "Grécia", 11, T(1.6), "fora", T(5.1), (224, 92, 82)),
              ("4.º", "Sérvia", 0, T(1.6), "", 99, CINZA)]
    for i, (p, nome, pts, ti, est, te, cor) in enumerate(linhas):
        kk = suave((t - ti) / 0.3)
        if kk <= 0:
            continue
        y = CY0 + 230 + i * 115
        d.rounded_rectangle((90, y - 46, W - 90, y + 46), radius=22, fill=CINZA + (int(255 * kk),))
        d.text((130, y), p, font=fonte(SANS_SB, 34), fill=CREME_70 + (int(255 * kk),), anchor="lm")
        d.text((230, y), nome, font=fonte(SANS_SB, 42), fill=CREME + (int(255 * kk),), anchor="lm")
        d.text((620, y), f"{pts} pts", font=fonte(SERIFA_N, 46), fill=CREME + (int(255 * kk),), anchor="rm")
        ke = suave((t - te) / 0.3)
        if ke > 0 and est:
            f = fonte(SANS_SB, 30)
            lw = d.textlength(est, font=f) + 44
            d.rounded_rectangle((W - 120 - lw, y - 28, W - 120, y + 28), radius=28, fill=cor + (int(255 * ke),))
            d.text((W - 120 - lw / 2, y), est, font=f, fill=(20, 20, 19, int(255 * ke)), anchor="mm")
    k = suave((t - T(2.4)) / 0.3)
    if k > 0:
        _chip(d, W / 2, CY0 + 720, "Três equipas com 11 pontos", CORAL, k, tam=36)


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
    linhas = [("A previsão · Alemanha–Holanda", "Vitória Alemanha · 54%", T(1.2), T(2.8)),
              ("A dica · Alemanha–Holanda", "Mais de 2,5 golos", T(3.2), T(4.8)),
              ("A dica · Sérvia 1–3 Alemanha", "Vitória Alemanha", T(5.4), T(7.9))]
    for i, (cab, txt, ti, tv) in enumerate(linhas):
        kk = suave((t - ti) / 0.3)
        if kk <= 0:
            continue
        y = CY0 + 290 + i * 150
        d.rounded_rectangle((80, y - 62, W - 80, y + 62), radius=24, fill=(36, 34, 32, int(255 * kk)),
                            outline=(70, 66, 60, int(255 * kk)), width=2)
        d.text((190, y - 26), cab, font=fonte(SANS, 28), fill=CREME_70 + (int(255 * kk),), anchor="lm")
        d.text((190, y + 20), txt, font=fonte(SERIFA_N, 48), fill=CREME + (int(255 * kk),), anchor="lm")
        kv = suave((t - tv) / 0.25)
        if kv > 0:
            _visto(d, 135, y, kv, r=28)
    k = suave((t - T(8.5)) / 0.3)
    if k > 0:
        _chip(d, W / 2, CY0 + 760, "Dicas na rede vizinha · link na bio", CORAL, k, tam=36)


def pergunta(v, q, t):
    _fundo(q, t)
    d = q.d
    k = suave((t - 0.1) / 0.35)
    if k > 0:
        d.text((W / 2, CY0 + 170), "A Alemanha…", font=fonte(SERIFA_N, 76), fill=CREME + (int(255 * k),), anchor="mm")
    for i, (letra, l1, l2, ti) in enumerate((("A", "é candidata", "ao título", T(0.5)),
                                             ("B", "ou a Holanda", "não apareceu?", T(2.7)))):
        kk = suave((t - ti) / 0.35)
        if kk <= 0:
            continue
        cx, cy = W / 2 + (-215 if i == 0 else 215), CY0 + 410
        d.rounded_rectangle((cx - 200, cy - 125, cx + 200, cy + 125), radius=28,
                            fill=(BRANCO if i == 0 else LARANJA) + (int(255 * kk),))
        d.text((cx, cy - 50), letra, font=fonte(SERIFA_N, 66), fill=(20, 20, 19, int(255 * kk)), anchor="mm")
        d.text((cx, cy + 25), l1, font=fonte(SANS_SB, 34), fill=(20, 20, 19, int(255 * kk)), anchor="mm")
        d.text((cx, cy + 70), l2, font=fonte(SANS_SB, 34), fill=(20, 20, 19, int(255 * kk)), anchor="mm")
    k = suave((t - T(4.3)) / 0.3)
    if k > 0:
        d.text((W / 2, CY0 + 680), "Comenta A ou B", font=fonte(SANS_SB, 50), fill=CORAL + (int(255 * k),),
               anchor="mm")


# ------------------------------------------------------------------ cenas

REF_VOZ = [6.72, 10.72, 8.80, 7.18, 11.99, 6.45, 11.64, 5.67]


def construir():
    v = Video("Alemanha", "Holanda", abrev=("ALE", "HOL"),
              fonte_txt="Ilustração · dados ESPN, Sky, Eurosport, Sportschau, NOS e Agente Claudio")
    v.folga, v.bpm = 0.35, 112
    v.sp["casa"] = sprite(17, BRANCO, PRETO, 4)        # Alemanha
    v.sp["fora"] = sprite(17, LARANJA, CREME, 2.5)     # Holanda
    cenas = []

    def cena(dur, titulo, i, jog, **kw):
        voz, leg = FALAS[i]
        c = Cena(dur, titulo, "", jog, voz=voz, legenda=leg, voz_ini=VI, **kw)
        c.voz_ref = REF_VOZ[i]
        cenas.append(c)
        return c

    c = cena(7.4, "Alemanha 5–0 Holanda", 0, jogadores({}), placar="5–0", minuto="FIM", sobreposicao=gancho,
             nomes=False)
    c.t_capa = 6.5

    # 1. o plano: travar os contra-ataques; mesmo assim, 19' Summerville escorrega e 25' Malen cabeceia por cima
    pos1 = {"terstegen": (0.5, 0.96), "brown": (0.20, 0.70), "schlotterbeck": (0.40, 0.80), "tah": (0.60, 0.80),
            "treu": (0.82, 0.68), "kimmich": (0.42, 0.62), "pavlovic": (0.58, 0.60), "wirtz": (0.50, 0.46),
            "scherhant": (0.20, 0.44), "gruda": (0.80, 0.44), "havertz": (0.50, 0.38), "reijnders": (0.50, 0.55),
            "qtimber": (0.38, 0.48), "veerman": (0.62, 0.48)}
    mov = {"summerville": [(0, 0.20, 0.62), (T(6.9), 0.20, 0.62), (T(7.8), 0.30, 0.81), (99, 0.30, 0.81)],
           "brown": [(0, 0.20, 0.70), (T(6.9), 0.20, 0.70), (T(8.2), 0.18, 0.88), (99, 0.18, 0.88)],
           "gakpo": vai((0.80, 0.64), (0.84, 0.79), T(7.4), T(8.4), 99),
           "malen": vai((0.50, 0.64), (0.50, 0.855), T(8.3), T(8.95), 99),
           "tah": vai((0.60, 0.80), (0.56, 0.86), T(8.3), T(8.95), 99)}
    bola = [(0, 0.21, 0.63), (T(6.9), 0.21, 0.63), (T(7.8), 0.31, 0.80), (T(8.2), 0.19, 0.875),
            (T(8.4), 0.84, 0.785), (T(8.95), 0.50, 0.85), (T(9.3), 0.56, 1.02)]
    cena(11.3, "O plano do Klopp", 1,
         jogadores(pos1, mov, mostrar={"schlotterbeck", "brown", "summerville", "malen", "gakpo"}),
         bola=bola, placar="0–0", minuto="", vista="defesa",
         formas=[{"tipo": "rotulo", "x": 0.5, "y": 0.70, "texto": "travar o contra-ataque", "cor": CORAL,
                  "t0": T(0.9), "t1": T(2.8)},
                 {"tipo": "rotulo", "x": 0.30, "y": 0.90, "texto": "entram no onze", "cor": BRANCO,
                  "t0": T(3.0), "t1": T(5.0)},
                 {"tipo": "rotulo", "x": 0.42, "y": 0.73, "texto": "19' · escorrega na relva", "cor": LARANJA,
                  "t0": T(7.6), "t1": T(8.6)},
                 {"tipo": "rotulo", "x": 0.68, "y": 0.92, "texto": "25' · Malen, por cima", "cor": LARANJA,
                  "t0": T(9.2), "t1": 11.3}],
         setas=[{"pts": [(0.20, 0.62), (0.30, 0.81)], "t0": T(6.9), "t1": T(7.8), "tipo": "corrida_fora"},
                {"pts": [(0.84, 0.785), (0.50, 0.85)], "t0": T(8.4), "t1": T(8.95), "tipo": "passe"},
                {"pts": [(0.50, 0.85), (0.56, 1.0)], "t0": T(8.95), "t1": T(9.3), "tipo": "remate"}],
         destaques=[("schlotterbeck", T(2.9), T(5.0)), ("brown", T(3.6), T(5.0)), ("summerville", T(6.9), T(8.5)),
                    ("malen", T(8.9), 11.3)])

    c = cena(9.4, "Os golos", 2, jogadores({}), placar="5–0", minuto="FIM", sobreposicao=golos, nomes=False)
    c.t_capa = 9.0

    # 3. o homem do jogo: Gruda pela direita (o 4–0, servido a Wirtz na pequena área)
    pos3 = {"verbruggen": (0.5, 0.03), "dumfries": (0.18, 0.14), "vanhecke": (0.40, 0.10), "vandeven": (0.58, 0.10),
            "qtimber": (0.40, 0.24), "veerman": (0.60, 0.24), "reijnders": (0.50, 0.32), "summerville": (0.20, 0.30),
            "gakpo": (0.80, 0.30), "malen": (0.5, 0.42), "havertz": (0.46, 0.12), "scherhant": (0.22, 0.18),
            "kimmich": (0.42, 0.36), "pavlovic": (0.58, 0.40), "treu": (0.90, 0.42), "brown": (0.12, 0.40),
            "schlotterbeck": (0.40, 0.62), "tah": (0.60, 0.62), "terstegen": (0.5, 0.92)}
    mov = {"gruda": vai((0.84, 0.33), (0.88, 0.125), T(2.0), T(4.3), 99),
           "jtimber": vai((0.80, 0.16), (0.85, 0.125), T(2.6), T(4.3), 99),
           "wirtz": vai((0.62, 0.26), (0.585, 0.065), T(3.6), T(4.9), 99),
           "verbruggen": [(0, 0.5, 0.03), (T(5.0), 0.53, 0.03), (T(5.3), 0.47, 0.035), (99, 0.47, 0.035)]}
    bola = [(0, 0.845, 0.34), (T(2.0), 0.845, 0.34), (T(4.3), 0.885, 0.135), (T(4.5), 0.885, 0.135),
            (T(4.95), 0.59, 0.07), (T(5.3), 0.50, 0.0)]
    cena(7.7, "O homem do jogo", 3, jogadores(pos3, mov, mostrar={"gruda", "wirtz"}),
         bola=bola, placar="3–0", minuto="71'", vista="ataque", golo=(T(5.35), "4–0", "Wirtz"),
         formas=[{"tipo": "rotulo", "x": 0.5, "y": 0.50, "texto": "65' · livre do Gruda → Schlotterbeck",
                  "cor": BRANCO, "t0": T(2.6), "t1": T(4.3)},
                 {"tipo": "rotulo", "x": 0.66, "y": 0.22, "texto": "77' · o 5–0 é dele", "cor": CORAL,
                  "t0": T(5.9), "t1": 7.7}],
         setas=[{"pts": [(0.84, 0.33), (0.88, 0.13)], "t0": T(2.0), "t1": T(4.3), "tipo": "conducao"},
                {"pts": [(0.62, 0.26), (0.585, 0.07)], "t0": T(3.6), "t1": T(4.9), "tipo": "corrida"},
                {"pts": [(0.885, 0.135), (0.59, 0.07)], "t0": T(4.5), "t1": T(4.95), "tipo": "passe"},
                {"pts": [(0.59, 0.07), (0.50, 0.0)], "t0": T(4.95), "t1": T(5.3), "tipo": "remate"}],
         destaques=[("gruda", T(1.3), 7.7)])

    c = cena(12.5, "E a Holanda?", 4, jogadores({}), placar="", sobreposicao=holanda, nomes=False)
    c.t_capa = 12.0
    c = cena(6.9, "O grupo", 5, jogadores({}), placar="", sobreposicao=grupo, nomes=False)
    c.t_capa = 6.5
    c = cena(12.1, "", 6, jogadores({}), placar="5–0", minuto="FIM", sobreposicao=cartao_agente, nomes=False)
    c.t_capa = 11.6
    c = cena(6.2, "", 7, jogadores({}), placar="", sobreposicao=pergunta, nomes=False)
    c.t_capa = 5.8
    cenas.append(cena_fecho(jogadores({}), placar="5–0", frase=10))
    return v, cenas
