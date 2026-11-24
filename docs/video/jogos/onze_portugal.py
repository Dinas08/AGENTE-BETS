"""O melhor onze de sempre de Portugal (4-3-3) e o selecionador.

Escolhas (opinião do Agente Claudio) e factos usados. No vídeo não se fala de polémicas nem de quem fica de fora.
- Diogo Costa (GR): defendeu três penáltis no desempate com a Eslovénia (oitavos do Euro 2024).
- João Cancelo (DD), Ricardo Carvalho e Pepe (DC; Pepe campeão europeu em 2016 e jogou o Euro 2024 com 41 anos),
  Nuno Mendes (DE, campeão europeu pelo PSG em 2025).
- Mário Coluna (o "Monstro Sagrado", capitão do Benfica bicampeão europeu 1961/62), Rui Costa, Deco (nascido no
  Brasil, naturalizado em 2003; estreou-se a marcar o golo da vitória contra o Brasil).
- Luís Figo (Bola de Ouro 2000), Eusébio (Bola de Ouro 1965, melhor marcador do Mundial 1966), Cristiano Ronaldo
  (maior goleador da história das seleções).
- Selecionador: Fernando Santos (Euro 2016 e Liga das Nações 2019).
"""
from PIL import Image, ImageDraw

from quadro_tatico import (cena_fecho, sprite, CORAL, CREME, CREME_70, CY0, CH, VERDE, AZUL, W, Cena, Video, fonte, suave,
                           SERIFA_N, SANS, SANS_SB)

import porto_napoli as base
import benfica_lech as bl

vai, _ov, PFP = base.vai, base._ov, base.PFP
_fundo, _chip = bl._fundo, bl._chip

FALAS = [
    ("O melhor onze de sempre de Portugal. Sem limite de épocas, num quatro, três, três. Vê se concordas.",
     "O melhor onze de sempre de Portugal. Sem limite de épocas, num 4-3-3. Vê se concordas."),
    ("Na baliza, o Diogo Costa. Defendeu três penáltis seguidos no desempate com a Eslovénia, no Europeu de dois mil "
     "e vinte e quatro. Mais seguro não há.",
     "Na baliza, Diogo Costa. Defendeu três penáltis seguidos no desempate com a Eslovénia, no Europeu de 2024. "
     "Mais seguro não há."),
    ("Na defesa: o João Cancelo à direita, um lateral que joga por dentro. Ao centro, o Ricardo Carvalho e o Pepe: "
     "campeão da Europa, e a jogar até aos quarenta e um anos. E o Nuno Mendes à esquerda, campeão europeu pelo PSG.",
     "Na defesa: João Cancelo à direita, um lateral que joga por dentro. Ao centro, Ricardo Carvalho e Pepe: "
     "campeão da Europa e a jogar até aos 41 anos. E Nuno Mendes à esquerda, campeão europeu pelo PSG."),
    ("No meio-campo: o Mário Coluna, o Monstro Sagrado do Benfica bicampeão europeu. O Rui Costa, o maestro. E o "
     "Deco: nasceu no Brasil, escolheu Portugal, e estreou-se a marcar... ao Brasil.",
     "No meio-campo: Mário Coluna, o Monstro Sagrado do Benfica bicampeão europeu. Rui Costa, o maestro. E Deco: "
     "nasceu no Brasil, escolheu Portugal e estreou-se a marcar… ao Brasil."),
    ("Na frente, não há discussão possível. O Figo, Bola de Ouro em dois mil. O Eusébio, Bola de Ouro, e o melhor "
     "marcador do Mundial de sessenta e seis. E o Cristiano Ronaldo, o maior goleador da história das seleções.",
     "Na frente, não há discussão possível. Figo, Bola de Ouro em 2000. Eusébio, Bola de Ouro e melhor marcador do "
     "Mundial de 66. E Cristiano Ronaldo, o maior goleador da história das seleções."),
    ("E no banco? O Fernando Santos. O homem que nos deu o Europeu de dois mil e dezasseis, e a Liga das Nações. O "
     "Scolari que nos desculpe.",
     "E no banco? Fernando Santos. O homem que nos deu o Europeu de 2016 e a Liga das Nações. O Scolari que nos "
     "desculpe."),
    ("Agora tu: quem tiravas deste onze? E quem metias no lugar? Diz nos comentários.",
     "Agora tu: quem tiravas deste onze? E quem metias no lugar? Diz nos comentários."),
]

# ------------------------------------------------------------------ o onze (4-3-3, a atacar para cima)
POS = {"costa": (0.50, 0.92), "cancelo": (0.85, 0.74), "carvalho": (0.38, 0.80), "pepe": (0.62, 0.80),
       "mendes": (0.15, 0.74), "coluna": (0.50, 0.62), "ruicosta": (0.66, 0.50), "deco": (0.34, 0.50),
       "figo": (0.82, 0.30), "eusebio": (0.50, 0.22), "ronaldo": (0.18, 0.30)}
NOMES = {"costa": "Diogo Costa", "cancelo": "Cancelo", "carvalho": "R. Carvalho", "pepe": "Pepe",
         "mendes": "Nuno Mendes", "coluna": "Coluna", "ruicosta": "Rui Costa", "deco": "Deco", "figo": "Figo",
         "eusebio": "Eusébio", "ronaldo": "Ronaldo"}
ORDEM = [["costa"], ["cancelo", "carvalho", "pepe", "mendes"], ["coluna", "ruicosta", "deco"],
         ["figo", "eusebio", "ronaldo"]]


def onze(cena_i, entradas):
    """Jogadores das cenas anteriores já em campo; os da cena atual entram (de baixo) no tempo indicado."""
    ja = {j for bloco in ORDEM[:cena_i] for j in bloco}
    out = {}
    for jid, (x, y) in POS.items():
        if jid in ja:
            chaves = [(0, x, y)]
        elif jid in entradas:
            t0 = entradas[jid]
            chaves = [(0, x, 1.3), (t0, x, 1.25), (t0 + 0.7, x, y), (99, x, y)]
        else:
            chaves = [(0, x, 1.3)]
        out[jid] = {"nome": NOMES[jid], "equipa": "casa", "chaves": chaves}
    return out


# ------------------------------------------------------------------ sobreposições

def gancho(v, q, t):
    ov = _ov(q)
    d = ImageDraw.Draw(ov)
    d.rectangle((0, CY0 + CH * 0.16, W, CY0 + CH * 0.80), fill=(20, 20, 19, 228))
    esc = 1.08 - 0.08 * suave(t / 0.3)
    d.text((W / 2, CY0 + CH * 0.27), "O MELHOR ONZE", font=fonte(SERIFA_N, 96 * esc), fill=CREME + (255,), anchor="mm")
    d.text((W / 2, CY0 + CH * 0.37), "DE SEMPRE", font=fonte(SERIFA_N, 96 * esc), fill=CREME + (255,), anchor="mm")
    d.text((W / 2, CY0 + CH * 0.47), "PORTUGAL", font=fonte(SANS_SB, 46), fill=CORAL + (255,), anchor="mm")
    k = suave((t - 3.4) / 0.3)
    if k > 0:
        _chip(d, W / 2, CY0 + CH * 0.60, "4-3-3", CORAL, k, tam=44)
    q.im.paste(ov, (0, 0), ov)


def banco(v, q, t):
    _fundo(q, t)
    d = q.d
    k = suave((t - 0.2) / 0.35)
    if k > 0:
        d.text((W / 2, CY0 + 200), "No banco", font=fonte(SANS, 40), fill=CREME_70 + (int(255 * k),), anchor="mm")
    k = suave((t - 1.0) / 0.35)
    if k > 0:
        esc = 1.1 - 0.1 * k
        d.text((W / 2, CY0 + 320), "Fernando Santos", font=fonte(SERIFA_N, int(96 * esc)),
               fill=CREME + (int(255 * k),), anchor="mm")
    k = suave((t - 3.2) / 0.3)
    if k > 0:
        _chip(d, W / 2, CY0 + 460, "Euro 2016 · Liga das Nações 2019", CORAL, k, tam=38)
    k = suave((t - 5.4) / 0.3)
    if k > 0:
        d.text((W / 2, CY0 + 600), "(desculpa, Scolari)", font=fonte(SANS, 36), fill=CREME_70 + (int(255 * k),),
               anchor="mm")


def pergunta(v, q, t):
    k = suave((t - 0.1) / 0.3)
    if k <= 0:
        return
    ov = _ov(q)
    d = ImageDraw.Draw(ov)
    y0 = CY0 + 380
    d.rounded_rectangle((80, y0, W - 80, y0 + 230), radius=30, fill=(24, 23, 22, int(240 * k)),
                        outline=CORAL + (int(255 * k),), width=3)
    d.text((W / 2, y0 + 70), "Quem tiravas?", font=fonte(SERIFA_N, 66), fill=CREME + (int(255 * k),), anchor="mm")
    d.text((W / 2, y0 + 150), "E quem metias no lugar?", font=fonte(SANS_SB, 42), fill=CORAL + (int(255 * k),),
           anchor="mm")
    q.im.paste(ov, (0, 0), ov)


# ------------------------------------------------------------------ cenas

REF_VOZ = [4.97, 6.75, 11.60, 11.57, 9.18, 7.18, 4.04]


def construir():
    v = Video("Portugal", "", abrev=("POR", ""), fonte_txt="O onze do Agente Claudio · opinião, para discutir")
    v.folga, v.bpm = 0.35, 112
    v.f["nome"] = fonte(SANS_SB, 28)
    v.sp["casa"] = sprite(23, CORAL, CREME, 3)
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

    c = cena(5.5, "O melhor onze de sempre", 0, onze(0, {}), placar="", sobreposicao=gancho, nomes=False)
    c.t_capa = 4.6

    cena(7.3, "Na baliza", 1, onze(0, {"costa": T(0.6)}), placar="",
         formas=[{"tipo": "rotulo", "x": 0.5, "y": 0.84, "texto": "3 penáltis defendidos · Euro 2024", "cor": CORAL,
                  "t0": T(1.4), "t1": 7.3}],
         destaques=[("costa", T(0.6), 7.3)])

    cena(12.1, "A defesa", 2,
         onze(1, {"cancelo": T(0.7), "carvalho": T(4.3), "pepe": T(5.2), "mendes": T(8.2)}), placar="",
         formas=[{"tipo": "rotulo", "x": 0.80, "y": 0.66, "texto": "joga por dentro", "cor": CREME, "t0": T(2.0),
                  "t1": T(3.7)},
                 {"tipo": "rotulo", "x": 0.5, "y": 0.62, "texto": "Pepe: Euro 2016 · jogou até aos 41", "cor": CORAL,
                  "t0": T(5.7), "t1": T(8.2)},
                 {"tipo": "rotulo", "x": 0.20, "y": 0.66, "texto": "campeão europeu · PSG", "cor": CREME,
                  "t0": T(9.5), "t1": 12.1},
                 {"tipo": "linha", "ids": ["mendes", "carvalho", "pepe", "cancelo"], "cor": CORAL, "t0": T(9.0),
                  "t1": 12.1}],
         destaques=[("cancelo", T(0.7), T(3.7)), ("carvalho", T(4.3), T(5.2)), ("pepe", T(5.2), T(8.2)),
                    ("mendes", T(8.2), 12.1)])

    cena(12.1, "O meio-campo", 3, onze(2, {"coluna": T(1.0), "ruicosta": T(4.6), "deco": T(6.3)}), placar="",
         formas=[{"tipo": "rotulo", "x": 0.5, "y": 0.69, "texto": "Monstro Sagrado", "cor": CREME, "t0": T(2.0),
                  "t1": T(4.5)},
                 {"tipo": "rotulo", "x": 0.70, "y": 0.43, "texto": "o maestro", "cor": CREME, "t0": T(5.4),
                  "t1": T(6.6)},
                 {"tipo": "rotulo", "x": 0.34, "y": 0.43, "texto": "estreia: golo ao Brasil", "cor": CORAL,
                  "t0": T(9.0), "t1": 12.1}],
         destaques=[("coluna", T(1.0), T(4.6)), ("ruicosta", T(4.6), T(6.3)), ("deco", T(6.3), 12.1)])

    cena(9.7, "O ataque", 4, onze(3, {"figo": T(1.7), "eusebio": T(3.2), "ronaldo": T(5.9)}), placar="",
         formas=[{"tipo": "rotulo", "x": 0.80, "y": 0.38, "texto": "Bola de Ouro 2000", "cor": CREME, "t0": T(2.2),
                  "t1": 9.7},
                 {"tipo": "rotulo", "x": 0.5, "y": 0.14, "texto": "Bola de Ouro · Mundial 66", "cor": CREME,
                  "t0": T(3.7), "t1": 9.7},
                 {"tipo": "rotulo", "x": 0.24, "y": 0.38, "texto": "maior goleador das seleções", "cor": CORAL,
                  "t0": T(6.9), "t1": 9.7}],
         destaques=[("figo", T(1.7), T(3.2)), ("eusebio", T(3.2), T(5.9)), ("ronaldo", T(5.9), 9.7)])

    c = cena(7.7, "O selecionador", 5, onze(4, {}), placar="", sobreposicao=banco, nomes=False)
    c.t_capa = 6.8
    c = cena(4.6, "O onze", 6, onze(4, {}), placar="", sobreposicao=pergunta)
    c.t_capa = 3.6
    cenas.append(cena_fecho(onze(4, {}), placar="", frase=9))
    return v, cenas
