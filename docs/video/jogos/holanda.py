"""Holanda: do 7–0 à Grécia à final do grupo em Berlim (Liga das Nações, nov 2026). Resumo tático + antevisão.

Fontes (verificadas a 14 nov 2026):
- ESPN (Países Baixos 7–0 Grécia, 13 nov): 4-3-3 com Reijnders, De Jong e Veerman; golos 6' Summerville, 12' 18'
  33' Reijnders (assist. Veerman, Malen, Dumfries; dois do lado esquerdo da pequena área e um muito perto da
  baliza), 40' e 59' Timber, 61' Malen; remates à baliza 13–1. De Jong saiu ao intervalo.
- theScore / beIN / NOS: hat-trick na 1.ª parte, o primeiro na Holanda desde Van Basten (1990); xG 4,39–0,44;
  Holanda lidera o grupo com 11 pontos, três à frente de Alemanha e Grécia; quase garantida nos quartos.
- VI / NOS / dpa: Frenkie de Jong fica fora "uit voorzorg" para Berlim, sem substituto; Van Dijk e Brobbey
  afastados; Gravenberch, Hato, Aké e Frimpong já não estavam. Selecionador: Xavi. Alemanha: Klopp; vitória dá os
  quartos; sem Musiala, Gnabry, Havertz, Schlotterbeck, Anton (sportschau, nationalmannschaft.net).
- Modelo (agente.db, ramo claude/dados): Alemanha 53%, empate 22%, Holanda 25%; golos esperados 2,09–1,43.
  Odds 1,83 / 4,0 / 3,5. A dica do canal ainda não saiu (jogo a 16 nov).
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
    ("Sete a zero à Grécia, com um hat-trick do Réinders em meia hora. Agora, a Holanda vai a Berlim. E o Agente "
     "Claudio não dá o favoritismo a quem estás a pensar.",
     "7–0 à Grécia, com um hat-trick do Reijnders em meia hora. Agora, a Holanda vai a Berlim. E o Agente "
     "Claudio não dá o favoritismo a quem estás a pensar."),
    ("Primeiro, o sete a zero: treze remates à baliza, contra um. O Réinders fez três na primeira parte, coisa que "
     "não acontecia na Holanda desde o Van Básten, em mil novecentos e noventa.",
     "Primeiro, o 7–0: 13 remates à baliza contra 1. O Reijnders fez três na primeira parte, coisa que não "
     "acontecia na Holanda desde o Van Basten, em 1990."),
    ("E repara no padrão: passes do Veerman, do Málen e do Dumfries, e o Réinders, que é médio, aparece sempre "
     "dentro da pequena área. É a Holanda do Xávi: médios a pisar a área.",
     "E repara no padrão: passes do Veerman, do Malen e do Dumfries, e o Reijnders, que é médio, aparece sempre "
     "dentro da pequena área. É a Holanda do Xavi: médios a pisar a área."),
    ("Com o Xávi, a Holanda lidera o grupo com onze pontos, três à frente da Alemanha e da Grécia. Tem um pé nos "
     "quartos de final.",
     "Com o Xavi, a Holanda lidera o grupo com 11 pontos, três à frente da Alemanha e da Grécia. Tem um pé nos "
     "quartos de final."),
    ("Mas vai a Berlim sem o capitão Frénqui de Iong, poupado por precaução, e sem Van Dáique, Brobbey, Aké, Frimpong, "
     "Hato e Gravenberch. A Alemanha do Klopp também está desfalcada: sem Musiála, Hávertz, Gnábri e Schlotterbeck.",
     "Mas vai a Berlim sem o capitão Frenkie de Jong, poupado por precaução, e sem Van Dijk, Brobbey, Aké, Frimpong, "
     "Hato e Gravenberch. A Alemanha do Klopp também está desfalcada: sem Musiala, Havertz, Gnabry e Schlotterbeck."),
    ("Então, o que diz o Agente Claudio? Alemanha cinquenta e três por cento, empate vinte e dois, Holanda vinte e "
     "cinco. A Alemanha joga em casa e precisa de ganhar. A Holanda pode gerir. Mas cuidado: no sete a zero, ninguém "
     "deu pelas baixas.",
     "Então, o que diz o Agente Claudio? Alemanha 53%, empate 22%, Holanda 25%. A Alemanha joga em casa e precisa "
     "de ganhar. A Holanda pode gerir. Mas cuidado: no 7–0, ninguém deu pelas baixas."),
    ("E tu? Quem ganha em Berlim? A dica do jogo sai na rede vizinha, link na bio. Diz nos comentários.",
     "E tu? Quem ganha em Berlim? A dica do jogo sai na rede vizinha, link na bio. Diz nos comentários."),
]

# ------------------------------------------------------------------ jogadores (7–0: Holanda ataca para cima)
JOG = {
    "verbruggen": ("Verbruggen", "casa", (0.50, 0.95)),
    "timber": ("Timber", "casa", (0.15, 0.79)),
    "vandeven": ("Van de Ven", "casa", (0.38, 0.85)),
    "vanhecke": ("Van Hecke", "casa", (0.62, 0.85)),
    "dumfries": ("Dumfries", "casa", (0.85, 0.79)),
    "reijnders": ("Reijnders", "casa", (0.50, 0.70)),
    "dejong": ("F. de Jong", "casa", (0.36, 0.64)),
    "veerman": ("Veerman", "casa", (0.64, 0.64)),
    "gakpo": ("Gakpo", "casa", (0.17, 0.56)),
    "malen": ("Malen", "casa", (0.50, 0.54)),
    "summerville": ("Summerville", "casa", (0.83, 0.56)),
    "tzolakis": ("Tzolakis", "fora", (0.50, 0.04)),
    "rota": ("Rota", "fora", (0.16, 0.16)),
    "mavropanos": ("Mavropanos", "fora", (0.38, 0.13)),
    "retsos": ("Retsos", "fora", (0.62, 0.13)),
    "tsimikas": ("Tsimikas", "fora", (0.84, 0.16)),
    "karetsas": ("Karetsas", "fora", (0.16, 0.28)),
    "triantis": ("Triantis", "fora", (0.40, 0.28)),
    "androutsos": ("Androutsos", "fora", (0.60, 0.28)),
    "tzolis": ("Tzolis", "fora", (0.84, 0.28)),
    "pavlidis": ("Pavlidis", "fora", (0.44, 0.42)),
    "ioannidis": ("Ioannidis", "fora", (0.56, 0.42)),
}
LARANJA = (240, 122, 32)
BRANCO = (236, 234, 226)
AZUL_GR = (60, 110, 200)


def jogadores(pos, mov=None, mostrar=(), subs=None):
    out = {}
    for jid, (nome, eq, form) in JOG.items():
        x, y = pos.get(jid, form)
        out[jid] = {"nome": (subs or {}).get(jid, nome) if jid in mostrar else "", "equipa": eq,
                    "chaves": (mov or {}).get(jid, [(0, x, y)])}
    return out


# ------------------------------------------------------------------ sobreposições

def gancho(v, q, t):
    ov = _ov(q)
    d = ImageDraw.Draw(ov)
    d.rectangle((0, CY0 + CH * 0.16, W, CY0 + CH * 0.80), fill=(20, 20, 19, 228))
    esc = 1.1 - 0.1 * suave(t / 0.3)
    d.text((W / 2, CY0 + CH * 0.31), "7–0", font=fonte(SERIFA_N, 230 * esc), fill=CREME + (255,), anchor="mm")
    d.text((W / 2, CY0 + CH * 0.44), "HOLANDA  ·  GRÉCIA", font=fonte(SANS_SB, 40), fill=LARANJA + (255,),
           anchor="mm")
    k = suave((t - 2.8) / 0.35)
    if k > 0:
        d.text((W / 2, CY0 + CH * 0.57), "e agora: Berlim", font=fonte(SERIFA_N, 80), fill=CREME + (int(255 * k),),
               anchor="mm")
    k = suave((t - 4.5) / 0.3)
    if k > 0:
        _chip(d, W / 2, CY0 + CH * 0.70, "O favorito não é quem pensas", CORAL, k)
    q.im.paste(ov, (0, 0), ov)


def golos(v, q, t):
    _fundo(q, t)
    d = q.d
    k = suave((t - 0.1) / 0.35)
    if k > 0:
        d.text((W / 2, CY0 + 75), "Os 7 golos", font=fonte(SERIFA_N, 66), fill=CREME + (int(255 * k),), anchor="mm")
    lista = [("6'", "Summerville", False), ("12'", "Reijnders", True), ("18'", "Reijnders", True),
             ("33'", "Reijnders", True), ("40'", "Timber", False), ("59'", "Timber", False), ("61'", "Malen", False)]
    for i, (m, nome, hat) in enumerate(lista):
        kk = suave((t - 0.5 - i * 0.18) / 0.3)
        if kk <= 0:
            continue
        y = CY0 + 165 + i * 68
        cor = LARANJA if hat else (44, 42, 39)
        d.rounded_rectangle((210, y - 28, W - 210, y + 28), radius=14, fill=cor + (int(255 * kk),))
        txt_cor = (20, 20, 19) if hat else CREME
        d.text((250, y), m, font=fonte(SANS_SB, 32), fill=txt_cor + (int(255 * kk),), anchor="lm")
        d.text((360, y), nome, font=fonte(SANS_SB, 34), fill=txt_cor + (int(255 * kk),), anchor="lm")
    k = suave((t - 1.3) / 0.3)
    if k > 0:
        d.text((W / 2, CY0 + 680), "Remates à baliza: 13 – 1   ·   xG 4,39 – 0,44", font=fonte(SANS, 32),
               fill=CREME_70 + (int(255 * k),), anchor="mm")
    k = suave((t - 7.2) / 0.3)
    if k > 0:
        _chip(d, W / 2, CY0 + 790, "Hat-trick na 1.ª parte: 1.º desde Van Basten (1990)", LARANJA, k, tam=32)


def grupo(v, q, t):
    _fundo(q, t)
    d = q.d
    k = suave((t - 0.1) / 0.35)
    if k > 0:
        d.text((W / 2, CY0 + 90), "Liga das Nações · o grupo", font=fonte(SERIFA_N, 58), fill=CREME + (int(255 * k),),
               anchor="mm")
    linhas = [("1.º", "Holanda", 11, LARANJA, 0.9), ("2.º", "Alemanha", 8, (44, 42, 39), 3.2),
              ("3.º", "Grécia", 8, (44, 42, 39), 3.6)]
    for i, (p, nome, pts, cor, ti) in enumerate(linhas):
        kk = suave((t - ti) / 0.3)
        if kk <= 0:
            continue
        y = CY0 + 240 + i * 120
        d.rounded_rectangle((140, y - 46, W - 140, y + 46), radius=22, fill=cor + (int(255 * kk),))
        tc = (20, 20, 19) if i == 0 else CREME
        d.text((185, y), p, font=fonte(SANS_SB, 34), fill=tc + (int(255 * kk),), anchor="lm")
        d.text((290, y), nome, font=fonte(SANS_SB, 42), fill=tc + (int(255 * kk),), anchor="lm")
        d.text((W - 185, y), f"{pts} pts", font=fonte(SERIFA_N, 48), fill=tc + (int(255 * kk),), anchor="rm")
    k = suave((t - 4.2) / 0.3)
    if k > 0:
        _chip(d, W / 2, CY0 + 640, "Um pé nos quartos de final", LARANJA, k)
        d.text((W / 2, CY0 + 740), "Última jornada: Alemanha – Holanda, segunda-feira, Berlim", font=fonte(SANS, 30),
               fill=CREME_70 + (int(255 * k),), anchor="mm")


def ausencias(v, q, t):
    _fundo(q, t)
    d = q.d
    xh, xa = W / 2 - 240, W / 2 + 240
    k = suave((t - 0.2) / 0.3)
    if k > 0:
        d.text((W / 2, CY0 + 70), "Quem falta em Berlim", font=fonte(SERIFA_N, 60), fill=CREME + (int(255 * k),),
               anchor="mm")
        d.text((xh, CY0 + 160), "HOLANDA", font=fonte(SANS_SB, 36), fill=LARANJA + (int(255 * k),), anchor="mm")
        d.text((xa, CY0 + 160), "ALEMANHA", font=fonte(SANS_SB, 36), fill=CREME + (int(255 * k),), anchor="mm")
    hol = [("Frenkie de Jong", "capitão · precaução", 1.6), ("Van Dijk", "", 3.9), ("Brobbey", "", 4.5),
           ("Aké", "", 5.0), ("Frimpong", "", 5.4), ("Hato", "", 5.9), ("Gravenberch", "", 6.3)]
    ale = [("Musiala", "", 9.3), ("Havertz", "", 9.8), ("Gnabry", "", 10.3), ("Schlotterbeck", "", 10.7),
           ("Anton", "", 11.0)]
    for col, (x, lista, cor) in enumerate(((xh, hol, LARANJA), (xa, ale, CREME))):
        for i, (nome, nota, ti) in enumerate(lista):
            kk = suave((t - ti) / 0.3)
            if kk <= 0:
                continue
            y = CY0 + 250 + i * 82 + (14 if (col == 0 and i > 0) else 0)
            h = 36 if not nota else 46
            d.rounded_rectangle((x - 210, y - h, x + 210, y + h), radius=18, fill=(44, 42, 39, int(255 * kk)))
            d.text((x - 185, y - (12 if nota else 0)), nome, font=fonte(SANS_SB, 32), fill=CREME + (int(255 * kk),),
                   anchor="lm")
            if nota:
                d.text((x - 185, y + 22), nota, font=fonte(SANS, 24), fill=cor + (int(255 * kk),), anchor="lm")


def leitura(v, q, t):
    _fundo(q, t)
    d = q.d
    if PFP.exists():
        k = suave((t - 0.1) / 0.4)
        r = int(90 * (0.85 + 0.15 * k))
        im = Image.open(PFP).convert("RGB").resize((2 * r, 2 * r), Image.LANCZOS)
        m = Image.new("L", (2 * r, 2 * r), 0)
        ImageDraw.Draw(m).ellipse((0, 0, 2 * r, 2 * r), fill=int(255 * k))
        q.im.paste(im, (int(W / 2 - r), int(CY0 + 100 - r)), m)
    barras = [("Alemanha", 53, CREME, 2.1), ("Empate", 22, CREME_70, 2.9), ("Holanda", 25, LARANJA, 3.6)]
    for i, (nome, p, cor, ti) in enumerate(barras):
        kk = suave((t - ti) / 0.4)
        if kk <= 0:
            continue
        y = CY0 + 245 + i * 90
        d.text((130, y), nome, font=fonte(SANS_SB, 36), fill=CREME + (int(255 * kk),), anchor="lm")
        x0, x1 = 360, W - 250
        d.rounded_rectangle((x0, y - 18, x1, y + 18), radius=18, fill=(50, 48, 45, int(255 * kk)))
        d.rounded_rectangle((x0, y - 18, x0 + (x1 - x0) * p / 60 * kk, y + 18), radius=18, fill=cor + (int(255 * kk),))
        d.text((W - 130, y), f"{round(p * kk)}%", font=fonte(SERIFA_N, 44), fill=CREME + (int(255 * kk),), anchor="rm")
    k = suave((t - 3.9) / 0.3)
    if k > 0:
        d.text((W / 2, CY0 + 530), "golos esperados  2,1 – 1,4", font=fonte(SANS, 30), fill=CREME_70 + (int(255 * k),),
               anchor="mm")
    razoes = [("Casa e precisa de ganhar", CREME, 4.5), ("A Holanda pode gerir", LARANJA, 6.9),
              ("Mas: no 7–0 ninguém deu pelas baixas", CORAL, 8.2)]
    for i, (txt, cor, ti) in enumerate(razoes):
        kk = suave((t - ti) / 0.3)
        if kk > 0:
            _chip(d, W / 2, CY0 + 630 + i * 95, txt, cor, kk, tam=34)


def pergunta(v, q, t):
    _fundo(q, t)
    d = q.d
    k = suave((t - 0.1) / 0.35)
    if k > 0:
        d.text((W / 2, CY0 + 150), "Quem ganha em Berlim?", font=fonte(SERIFA_N, 72), fill=CREME + (int(255 * k),),
               anchor="mm")
    for i, (letra, txt, cor) in enumerate((("1", "Alemanha", (44, 42, 39)), ("X", "Empate", (44, 42, 39)),
                                           ("2", "Holanda", LARANJA))):
        kk = suave((t - 0.5 - i * 0.15) / 0.35)
        if kk <= 0:
            continue
        cx, cy = W / 2 + (i - 1) * 300, CY0 + 360
        d.rounded_rectangle((cx - 135, cy - 105, cx + 135, cy + 105), radius=28, fill=cor + (int(255 * kk),),
                            outline=(80, 76, 70, int(255 * kk)), width=2)
        tc = (20, 20, 19) if i == 2 else CREME
        d.text((cx, cy - 28), letra, font=fonte(SERIFA_N, 70), fill=tc + (int(255 * kk),), anchor="mm")
        d.text((cx, cy + 50), txt, font=fonte(SANS_SB, 34), fill=tc + (int(255 * kk),), anchor="mm")
    k = suave((t - 1.7) / 0.3)
    if k > 0:
        _chip(d, W / 2, CY0 + 580, "A dica sai na rede vizinha · link na bio", CORAL, k, tam=34)
    k = suave((t - 4.1) / 0.3)
    if k > 0:
        d.text((W / 2, CY0 + 720), "Comenta 1, X ou 2", font=fonte(SANS_SB, 48), fill=CORAL + (int(255 * k),),
               anchor="mm")


# ------------------------------------------------------------------ cenas

REF_VOZ = [7.53, 9.16, 9.90, 5.94, 12.12, 11.44, 5.26]


def construir():
    v = Video("Holanda", "Grécia", abrev=("NED", "GRE"), fonte_txt="Ilustração · dados ESPN, NOS, VI, theScore e Agente Claudio")
    v.folga, v.bpm = 0.35, 112
    v.sp["casa"] = sprite(17, LARANJA, CREME, 2.5)      # Holanda
    v.sp["fora"] = sprite(17, BRANCO, AZUL_GR, 4)       # Grécia
    VI = 0.15
    cenas = []

    def cena(dur, titulo, i, jog, **kw):
        voz, leg = FALAS[i]
        c = Cena(dur, titulo, "", jog, voz=voz, legenda=leg, voz_ini=VI, **kw)
        c.voz_ref = REF_VOZ[i]
        cenas.append(c)
        return c

    def T(x):
        return x + VI

    c = cena(8.0, "Holanda: do 7–0 a Berlim", 0, jogadores({}), placar="7–0", minuto="FIM", sobreposicao=gancho,
             nomes=False)
    c.t_capa = 6.4
    c = cena(9.6, "O 7–0", 1, jogadores({}), placar="7–0", minuto="FIM", sobreposicao=golos, nomes=False)
    c.t_capa = 8.6

    # 2. o padrão: Reijnders, médio, aparece sempre na pequena área (passes de Veerman, Malen e Dumfries)
    pos2 = {"tzolakis": (0.50, 0.03), "rota": (0.18, 0.12), "mavropanos": (0.40, 0.10), "retsos": (0.58, 0.10),
            "tsimikas": (0.80, 0.12), "karetsas": (0.20, 0.24), "triantis": (0.42, 0.22), "androutsos": (0.58, 0.22),
            "tzolis": (0.80, 0.24), "pavlidis": (0.46, 0.38), "ioannidis": (0.56, 0.40),
            "veerman": (0.70, 0.24), "malen": (0.56, 0.16), "dumfries": (0.90, 0.16), "gakpo": (0.16, 0.20),
            "summerville": (0.82, 0.30), "dejong": (0.40, 0.42), "timber": (0.12, 0.38), "vandeven": (0.36, 0.56),
            "vanhecke": (0.62, 0.56)}
    mov = {"reijnders": [(0, 0.46, 0.32), (T(3.6), 0.46, 0.31), (T(5.6), 0.43, 0.04), (99, 0.43, 0.04)]}
    setas = [{"pts": [(0.70, 0.24), (0.43, 0.05)], "t0": T(1.5), "t1": T(2.2), "tipo": "passe"},
             {"pts": [(0.56, 0.16), (0.43, 0.05)], "t0": T(2.2), "t1": T(2.8), "tipo": "passe"},
             {"pts": [(0.90, 0.16), (0.43, 0.05)], "t0": T(2.8), "t1": T(3.5), "tipo": "passe"},
             {"pts": [(0.46, 0.31), (0.43, 0.06)], "t0": T(3.6), "t1": T(5.6), "tipo": "corrida"}]
    cena(10.4, "O padrão do Reijnders", 2, jogadores(pos2, mov, mostrar={"reijnders", "veerman", "malen", "dumfries"}),
         placar="7–0", minuto="", vista="ataque", setas=setas,
         formas=[{"tipo": "rotulo", "x": 0.74, "y": 0.30, "texto": "12'", "cor": LARANJA, "t0": T(1.5), "t1": T(4.0)},
                 {"tipo": "rotulo", "x": 0.60, "y": 0.22, "texto": "18'", "cor": LARANJA, "t0": T(2.2), "t1": T(4.0)},
                 {"tipo": "rotulo", "x": 0.92, "y": 0.22, "texto": "33'", "cor": LARANJA, "t0": T(2.8), "t1": T(4.0)},
                 {"tipo": "zona", "pts": [(0.37, 0.0), (0.52, 0.0), (0.52, 0.06), (0.37, 0.06)], "cor": LARANJA,
                  "t0": T(5.4), "t1": 10.4},
                 {"tipo": "rotulo", "x": 0.30, "y": 0.13, "texto": "médio a pisar a área", "cor": LARANJA,
                  "t0": T(5.0), "t1": 10.4}],
         destaques=[("reijnders", T(3.4), 10.4)])

    c = cena(6.4, "O grupo", 3, jogadores({}), placar="", sobreposicao=grupo, nomes=False)
    c.t_capa = 5.6
    c = cena(12.6, "As baixas", 4, jogadores({}), placar="", sobreposicao=ausencias, nomes=False)
    c.t_capa = 12.0
    c = cena(11.9, "Alemanha – Holanda: o Agente", 5, jogadores({}), placar="", sobreposicao=leitura, nomes=False)
    c.t_capa = 11.0
    c = cena(5.9, "", 6, jogadores({}), placar="", sobreposicao=pergunta, nomes=False)
    c.t_capa = 5.0
    cenas.append(cena_fecho(jogadores({}), placar="", frase=7))
    return v, cenas
