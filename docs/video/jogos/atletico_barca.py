"""Análise tática: Atlético Madrid 1–2 Barcelona (LaLiga, 8 nov 2026). A defesa do Barça e a troca do intervalo.

Fontes (verificadas a 10 nov 2026):
- ESPN: onzes (Atlético 4-4-2, Barça 4-1-4-1), golos, substituições e estatísticas (posse 37–63, remates 9–19).
  10' Giuliano Simeone, muito perto da baliza, assist. Julián Álvarez; 45' Fermín, pé esquerdo; 46' De Jong por
  Fariñas; 60' Christensen por Cancelo; 66' Fermín, assist. Lamine Yamal em passe de rutura. Pubill e Pedri à barra.
- Coaches' Voice (9 nov): Barça "especialmente vulnerable por la altura de su última línea"; "separación vertical
  entre las líneas"; Bernal demasiado perto da 1.ª linha e Pedri a correr demais; De Jong "ocuparía el lateral
  derecho" com comportamento de organizador; Christensen e Gerard Martín à esquerda, "distribución defensiva más
  natural"; depois do 1–2 o Atlético só fez um remate. Flick: "La idea era que jugase 15 minutos de lateral derecho
  y luego cambiar cuando Bernal estuviese cansado".
- JMftbl: o 1–0 nasce de uma mudança de jogo para Lee; "Cancelo steps but is beaten by the pass"; De Jong
  "becoming part of the back three when Barca had the ball"; passes picados de Oblak para as costas do meio-campo.
- Goal: bolas nas costas da linha alta; o 1–2 de uma sobrecarga à direita.
- Sem lances polémicos de arbitragem nas análises.
- Agente Claudio: vitória do Barça (50%) — acertou (não houve dica no canal para este jogo).
A "melhoria" proposta no fim é leitura nossa, apoiada no que mudou na 2.ª parte.
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
    ("O Barça esteve a perder, levou uma bola na trave, e passou a primeira parte a sofrer. E mesmo assim, ganhou no "
     "Metropolitano. A explicação está numa troca ao intervalo.",
     "O Barça esteve a perder, levou uma bola na trave e passou a primeira parte a sofrer. E mesmo assim ganhou no "
     "Metropolitano. A explicação está numa troca ao intervalo."),
    ("O problema da primeira parte: a linha defensiva muito alta, e uma grande distância entre linhas. O Atlético "
     "puxava o Barça para um lado, mudava o jogo, e o Cancelo saía, mas era batido pelo passe.",
     "O problema da primeira parte: a linha defensiva muito alta e uma grande distância entre linhas. O Atlético "
     "puxava o Barça para um lado, mudava o jogo, e o Cancelo saía, mas era batido pelo passe."),
    ("Foi assim o primeiro golo: mudança de jogo, o Julián Álvarez aparece por dentro, e serve o Djuliano Simeóne à "
     "boca da baliza. Um a zero.",
     "Foi assim o primeiro golo: mudança de jogo, Julián Álvarez aparece por dentro e serve Giuliano Simeone à boca "
     "da baliza. 1–0."),
    ("E havia outro buraco: o Bernal, sozinho no meio, ficava colado aos centrais. O Pedri tinha de correr demais para "
     "pressionar, e o Óblak metia bolas picadas nas costas do meio-campo.",
     "E havia outro buraco: o Bernal, sozinho no meio, ficava colado aos centrais. Pedri tinha de correr demais para "
     "pressionar e Oblak metia bolas picadas nas costas do meio-campo."),
    ("Mesmo assim, antes do intervalo, o Pedri conduz por dentro, a bola sobra, e o Fermín empata, de pé esquerdo.",
     "Mesmo assim, antes do intervalo, Pedri conduz por dentro, a bola sobra e Fermín empata, de pé esquerdo."),
    ("Ao intervalo, o Flick mexeu: o Frénqui de Iong entra para lateral direito. Mas com bola, fecha por dentro, e "
     "forma uma linha de três. O Bernal sobe para junto do Pedri, e a pressão ganha coordenação. Aos sessenta, entra o "
     "Cristensen, e o Gerard Martín volta à esquerda.",
     "Ao intervalo, Flick mexeu: Frenkie de Jong entra para lateral direito. Mas com bola fecha por dentro e "
     "forma uma linha de três. Bernal sobe para junto do Pedri e a pressão ganha coordenação. Aos 60', entra "
     "Christensen e Gerard Martín volta à esquerda."),
    ("O resultado? Aos sessenta e seis, o Lamine Iamal recebe na direita, mete nas costas da defesa, e o Fermín bisa. "
     "Um a dois. E depois disso, o Atlético só fez um remate.",
     "O resultado? Aos 66', Lamine Yamal recebe na direita, mete nas costas da defesa e Fermín bisa. 1–2. E depois "
     "disso, o Atlético só fez um remate."),
    ("A melhoria que nós víamos: começar o jogo como ele acabou. Um lateral que fecha por dentro, três atrás com bola, "
     "e o médio defensivo mais perto do meio-campo. Assim, a linha alta tem cobertura, e as bolas nas costas deixam "
     "de doer.",
     "A melhoria que nós víamos: começar o jogo como ele acabou. Um lateral que fecha por dentro, três atrás com bola "
     "e o médio defensivo mais perto do meio-campo. Assim, a linha alta tem cobertura e as bolas nas costas deixam "
     "de doer."),
    ("E o Agente Claudio? Deu vitória do Barça... e acertou. As dicas estão na rede vizinha, link na bio. E tu: o "
     "Frénqui de Iong deve ficar a lateral? Diz nos comentários.",
     "E o Agente Claudio? Deu vitória do Barça e acertou. As dicas estão na rede vizinha, link na bio. E tu: "
     "Frenkie de Jong deve ficar a lateral? Diz nos comentários."),
]

# ------------------------------------------------------------------ jogadores
# O Barça (casa no motor, azul) ataca para cima; o Atlético (branco com contorno vermelho) ataca para baixo.
JOG = {
    "garcia": ("Joan García", "casa", (0.50, 0.95)),
    "cancelo": ("Cancelo", "casa", (0.15, 0.79)),
    "martin": ("Gerard Martín", "casa", (0.38, 0.85)),
    "cubarsi": ("Cubarsí", "casa", (0.62, 0.85)),
    "farinas": ("Fariñas", "casa", (0.85, 0.79)),
    "bernal": ("Bernal", "casa", (0.50, 0.72)),
    "pedri": ("Pedri", "casa", (0.38, 0.62)),
    "fermin": ("Fermín", "casa", (0.62, 0.62)),
    "gordon": ("Gordon", "casa", (0.15, 0.56)),
    "yamal": ("Yamal", "casa", (0.85, 0.56)),
    "raphinha": ("Raphinha", "casa", (0.50, 0.52)),
    "oblak": ("Oblak", "fora", (0.50, 0.04)),
    "llorente": ("Llorente", "fora", (0.16, 0.16)),
    "pubill": ("Pubill", "fora", (0.38, 0.13)),
    "hancko": ("Hancko", "fora", (0.62, 0.13)),
    "grimaldo": ("Grimaldo", "fora", (0.84, 0.16)),
    "giuliano": ("Giuliano", "fora", (0.16, 0.28)),
    "koke": ("Koke", "fora", (0.40, 0.28)),
    "barrios": ("Barrios", "fora", (0.60, 0.28)),
    "baena": ("Baena", "fora", (0.84, 0.28)),
    "alvarez": ("Julián Álvarez", "fora", (0.56, 0.42)),
    "lee": ("Lee Kang-in", "fora", (0.44, 0.42)),
}
SUBS_46 = {"farinas": "De Jong"}
SUBS_66 = dict(SUBS_46, cancelo="Christensen", lee="Sørloth")
AZUL_BARCA = (40, 78, 168)
BRANCO = (236, 234, 226)
VERMELHO = (205, 48, 56)


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
    d.text((W / 2, CY0 + CH * 0.31), "1–2", font=fonte(SERIFA_N, 230 * esc), fill=CREME + (255,), anchor="mm")
    d.text((W / 2, CY0 + CH * 0.44), "ATLÉTICO  ·  BARÇA", font=fonte(SANS_SB, 40), fill=AZUL + (255,), anchor="mm")
    k = suave((t - 0.3) / 0.35)
    if k > 0:
        d.text((W / 2, CY0 + CH * 0.55), "a perder aos 10'  ·  trave aos 6'", font=fonte(SANS, 36),
               fill=CREME_70 + (int(255 * k),), anchor="mm")
        d.text((W / 2, CY0 + CH * 0.62), "e ganhou", font=fonte(SERIFA_N, 80), fill=CREME + (int(255 * k),),
               anchor="mm")
    k = suave((t - 6.0) / 0.3)
    if k > 0:
        _chip(d, W / 2, CY0 + CH * 0.73, "A chave: uma troca ao intervalo", CORAL, k)
    q.im.paste(ov, (0, 0), ov)


def cartao_agente(v, q, t):
    _fundo(q, t)
    d = q.d
    if PFP.exists():
        k = suave((t - 0.1) / 0.4)
        r = int(100 * (0.85 + 0.15 * k))
        im = Image.open(PFP).convert("RGB").resize((2 * r, 2 * r), Image.LANCZOS)
        m = Image.new("L", (2 * r, 2 * r), 0)
        ImageDraw.Draw(m).ellipse((0, 0, 2 * r, 2 * r), fill=int(255 * k))
        q.im.paste(im, (int(W / 2 - r), int(CY0 + 115 - r)), m)
    k = suave((t - 1.25) / 0.3)
    if k > 0:
        d.text((W / 2, CY0 + 265), "O Agente Claudio deu", font=fonte(SANS, 36), fill=CREME_70 + (int(255 * k),),
               anchor="mm")
        d.text((W / 2 + 30, CY0 + 335), "Vitória do Barça · 50%", font=fonte(SERIFA_N, 58),
               fill=CREME + (int(255 * k),), anchor="mm")
    k = suave((t - 2.35) / 0.25)
    if k > 0:
        _visto(d, W / 2 - 320, CY0 + 337, k, r=28)
    k = suave((t - 2.95) / 0.3)
    if k > 0:
        _chip(d, W / 2, CY0 + 455, "Dicas na rede vizinha · link na bio", CORAL, k, tam=34)
    k = suave((t - 5.4) / 0.3)
    if k > 0:
        d.text((W / 2, CY0 + 570), "De Jong a lateral?", font=fonte(SERIFA_N, 66), fill=CREME + (int(255 * k),),
               anchor="mm")
    for i, (letra, txt) in enumerate((("A", "Sim, fica"), ("B", "Não, ao meio"))):
        kk = suave((t - 5.7 - i * 0.15) / 0.35)
        if kk <= 0:
            continue
        cx, cy = W / 2 + (-215 if i == 0 else 215), CY0 + 740
        d.rounded_rectangle((cx - 195, cy - 85, cx + 195, cy + 85), radius=28, fill=(44, 42, 39, int(255 * kk)),
                            outline=(80, 76, 70, int(255 * kk)), width=2)
        d.text((cx, cy - 22), letra, font=fonte(SERIFA_N, 58), fill=CREME + (int(255 * kk),), anchor="mm")
        d.text((cx, cy + 40), txt, font=fonte(SANS_SB, 36), fill=CREME + (int(255 * kk),), anchor="mm")
    k = suave((t - 7.6) / 0.3)
    if k > 0:
        d.text((W / 2, CY0 + 900), "Comenta A ou B", font=fonte(SANS_SB, 46), fill=CORAL + (int(255 * k),),
               anchor="mm")


# ------------------------------------------------------------------ cenas

REF_VOZ = [8.33, 9.41, 7.01, 8.08, 5.45, 12.91, 9.34, 10.68, 9.16]


def construir():
    v = Video("Atlético", "Barça", abrev=("ATM", "BAR"), fonte_txt="Ilustração · dados ESPN, Coaches' Voice, JMftbl e Goal")
    v.folga, v.bpm = 0.35, 112
    v.sp["casa"] = sprite(17, AZUL_BARCA, CREME, 2.5)      # Barça
    v.sp["fora"] = sprite(17, BRANCO, VERMELHO, 4)         # Atlético
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

    # 0. gancho
    c = cena(8.8, "Atlético 1–2 Barça: a tática", 0, jogadores({}), placar="1–2", minuto="FIM", sobreposicao=gancho,
             nomes=False)
    c.t_capa = 6.8

    defesa = ["cancelo", "martin", "cubarsi", "farinas"]
    # 1. 1.ª parte: linha alta, distância entre linhas; mudança de jogo e Cancelo batido (vista da defesa do Barça)
    pos1 = {"garcia": (0.5, 0.97), "martin": (0.40, 0.66), "cubarsi": (0.60, 0.66), "farinas": (0.82, 0.64),
            "bernal": (0.52, 0.60), "pedri": (0.42, 0.48), "fermin": (0.64, 0.48),
            "baena": (0.85, 0.58), "grimaldo": (0.90, 0.50), "barrios": (0.62, 0.53), "koke": (0.44, 0.52),
            "alvarez": (0.52, 0.72), "llorente": (0.12, 0.50), "hancko": (0.62, 0.44), "pubill": (0.40, 0.44)}
    mov = {"cancelo": [(0, 0.18, 0.64), (T(6.6), 0.18, 0.64), (T(7.4), 0.23, 0.69), (99, 0.23, 0.69)],
           "lee": [(0, 0.26, 0.70), (T(6.0), 0.25, 0.71), (99, 0.25, 0.71)],
           "giuliano": [(0, 0.10, 0.60), (T(7.4), 0.10, 0.62), (T(8.5), 0.15, 0.84), (99, 0.15, 0.84)]}
    bola = [(0, 0.84, 0.58), (T(5.9), 0.84, 0.58), (T(6.7), 0.255, 0.705), (T(7.6), 0.255, 0.705),
            (T(8.4), 0.155, 0.83)]
    cena(9.9, "1.ª parte · o problema", 1,
         jogadores(pos1, mov, mostrar={"cancelo", "lee", "baena", "bernal"}),
         bola=bola, placar="1–0", minuto="", vista="defesa",
         formas=[{"tipo": "linha", "ids": defesa, "cor": AZUL, "t0": T(1.3), "t1": T(4.2)},
                 {"tipo": "rotulo", "x": 0.5, "y": 0.75, "texto": "linha alta", "cor": AZUL, "t0": T(1.5),
                  "t1": T(3.0)},
                 {"tipo": "entre", "de": ["pedri", "fermin"], "ate": ["martin", "cubarsi"], "cor": CORAL,
                  "rotulo": "distância entre linhas", "t0": T(3.0), "t1": T(4.8)},
                 {"tipo": "rotulo", "x": 0.30, "y": 0.92, "texto": "Cancelo batido", "cor": CORAL, "t0": T(7.8),
                  "t1": 9.9}],
         setas=[{"pts": [(0.84, 0.58), (0.255, 0.705)], "t0": T(5.9), "t1": T(6.7), "tipo": "passe"},
                {"pts": [(0.18, 0.64), (0.23, 0.69)], "t0": T(6.6), "t1": T(7.4), "tipo": "corrida"},
                {"pts": [(0.255, 0.705), (0.155, 0.83)], "t0": T(7.6), "t1": T(8.4), "tipo": "passe"}],
         destaques=[("cancelo", T(6.6), T(8.2)), ("lee", T(6.0), T(7.6))])

    # 2. 10': o 1–0. Mudança de jogo, Álvarez por dentro, Giuliano à boca da baliza
    pos2 = {"garcia": (0.5, 0.97), "farinas": (0.80, 0.72), "bernal": (0.52, 0.66), "pedri": (0.42, 0.56),
            "fermin": (0.64, 0.56), "baena": (0.80, 0.62), "grimaldo": (0.88, 0.56), "barrios": (0.62, 0.60),
            "koke": (0.44, 0.58), "llorente": (0.14, 0.56)}
    mov = {"lee": [(0, 0.24, 0.72), (T(2.4), 0.25, 0.73), (99, 0.25, 0.73)],
           "cancelo": vai((0.22, 0.68), (0.26, 0.74), T(2.0), T(3.0), 99),
           "alvarez": [(0, 0.50, 0.70), (T(2.4), 0.48, 0.72), (T(3.1), 0.41, 0.80), (99, 0.41, 0.80)],
           "giuliano": [(0, 0.20, 0.80), (T(3.3), 0.24, 0.84), (T(4.6), 0.52, 0.935), (99, 0.52, 0.935)],
           "martin": vai((0.40, 0.70), (0.42, 0.86), T(2.6), T(4.4), 99),
           "cubarsi": vai((0.60, 0.70), (0.56, 0.86), T(2.6), T(4.4), 99),
           "garcia": [(0, 0.5, 0.975), (T(4.7), 0.5, 0.975), (T(5.1), 0.53, 0.975)]}
    bola = [(0, 0.25, 0.73), (T(2.4), 0.25, 0.73), (T(3.1), 0.41, 0.80), (T(4.1), 0.41, 0.80), (T(4.6), 0.52, 0.93),
            (T(4.8), 0.52, 0.93), (T(5.1), 0.50, 1.0)]
    cena(7.6, "10' · o primeiro golo", 2,
         jogadores(pos2, mov, mostrar={"lee", "alvarez", "giuliano"}),
         bola=bola, placar="0–0", minuto="10'", vista="defesa", golo=(T(5.15), "1–0", "Giuliano Simeone"),
         setas=[{"pts": [(0.25, 0.73), (0.41, 0.80)], "t0": T(2.4), "t1": T(3.1), "tipo": "passe"},
                {"pts": [(0.41, 0.80), (0.52, 0.93)], "t0": T(4.1), "t1": T(4.6), "tipo": "passe"},
                {"pts": [(0.24, 0.84), (0.52, 0.935)], "t0": T(3.3), "t1": T(4.6), "tipo": "corrida_fora"}],
         destaques=[("alvarez", T(2.4), T(4.6)), ("giuliano", T(4.6), 7.6)])

    # 3. o buraco do meio: Bernal colado aos centrais, Pedri a correr demais, bolas picadas de Oblak
    pos3 = {"garcia": (0.5, 0.94), "cancelo": (0.15, 0.62), "martin": (0.38, 0.72), "cubarsi": (0.62, 0.72),
            "farinas": (0.85, 0.62), "bernal": (0.50, 0.70), "fermin": (0.62, 0.30), "gordon": (0.70, 0.14),
            "yamal": (0.85, 0.30), "raphinha": (0.50, 0.12), "oblak": (0.5, 0.05), "pubill": (0.36, 0.10),
            "hancko": (0.64, 0.10), "llorente": (0.12, 0.24), "grimaldo": (0.88, 0.24), "koke": (0.42, 0.30),
            "barrios": (0.58, 0.32), "giuliano": (0.16, 0.40), "baena": (0.84, 0.42), "lee": (0.42, 0.50)}
    mov = {"pedri": vai((0.38, 0.52), (0.42, 0.33), T(3.4), T(5.0), 99),
           "alvarez": vai((0.60, 0.46), (0.56, 0.58), T(5.6), T(6.6), 99)}
    bola = [(0, 0.5, 0.05), (T(5.4), 0.5, 0.05), (T(6.6), 0.56, 0.58)]
    cena(8.6, "O buraco do meio", 3,
         jogadores(pos3, mov, mostrar={"bernal", "pedri", "oblak", "alvarez"}),
         bola=bola, placar="1–0", minuto="",
         formas=[{"tipo": "rotulo", "x": 0.50, "y": 0.80, "texto": "colado aos centrais", "cor": AZUL, "t0": T(1.0),
                  "t1": T(3.4)},
                 {"tipo": "entre", "de": ["pedri", "fermin"], "ate": ["bernal"], "cor": CORAL, "rotulo": "espaço",
                  "t0": T(5.2), "t1": 8.6}],
         setas=[{"pts": [(0.38, 0.52), (0.42, 0.33)], "t0": T(3.4), "t1": T(5.0), "tipo": "corrida"},
                {"pts": [(0.5, 0.05), (0.56, 0.58)], "t0": T(5.4), "t1": T(6.6), "tipo": "passe"}],
         destaques=[("bernal", T(1.0), T(3.4)), ("pedri", T(3.4), T(5.2)), ("alvarez", T(6.2), 8.6)])

    # 4. 45': Pedri conduz por dentro, a bola sobra, Fermín empata
    pos4 = {"oblak": (0.5, 0.03), "raphinha": (0.50, 0.12), "gordon": (0.20, 0.18), "yamal": (0.84, 0.22),
            "bernal": (0.50, 0.50), "cancelo": (0.14, 0.40), "farinas": (0.86, 0.42), "martin": (0.38, 0.60),
            "cubarsi": (0.62, 0.60)}
    mov = {"pedri": [(0, 0.42, 0.40), (T(1.8), 0.42, 0.40), (T(2.8), 0.46, 0.25), (99, 0.46, 0.25)],
           "fermin": vai((0.60, 0.27), (0.53, 0.165), T(2.6), T(3.4), 99),
           "koke": vai((0.40, 0.28), (0.45, 0.24), T(2.4), T(2.9), 99),
           "oblak": [(0, 0.5, 0.03), (T(3.6), 0.48, 0.03), (T(3.95), 0.45, 0.02)]}
    bola = [(0, 0.42, 0.39), (T(1.8), 0.42, 0.39), (T(2.8), 0.46, 0.245), (T(2.9), 0.46, 0.245), (T(3.3), 0.53, 0.165),
            (T(3.6), 0.53, 0.165), (T(3.95), 0.545, 0.0)]
    cena(6.0, "45' · o empate", 4, jogadores(pos4, mov, mostrar={"pedri", "fermin"}),
         bola=bola, placar="1–0", minuto="45'", vista="ataque", golo=(T(4.0), "1–1", "Fermín"),
         setas=[{"pts": [(0.42, 0.39), (0.46, 0.245)], "t0": T(1.8), "t1": T(2.8), "tipo": "conducao"},
                {"pts": [(0.53, 0.165), (0.545, 0.005)], "t0": T(3.6), "t1": T(3.95), "tipo": "remate"}],
         destaques=[("pedri", T(1.6), T(3.0)), ("fermin", T(3.0), 6.0)])

    # 5. a troca do intervalo: De Jong a lateral que fecha por dentro (linha de 3), Bernal sobe; 60' Christensen
    pos5 = {"garcia": (0.5, 0.93), "gordon": (0.15, 0.40), "yamal": (0.85, 0.40), "raphinha": (0.50, 0.34),
            "fermin": (0.62, 0.50), "oblak": (0.5, 0.05), "pubill": (0.38, 0.14), "hancko": (0.62, 0.14),
            "llorente": (0.16, 0.20), "grimaldo": (0.84, 0.20), "koke": (0.42, 0.32), "barrios": (0.58, 0.32),
            "giuliano": (0.20, 0.30), "baena": (0.80, 0.30), "alvarez": (0.56, 0.44), "lee": (0.44, 0.44)}
    mov = {"farinas": vai((0.85, 0.70), (0.70, 0.78), T(4.0), T(5.6), 99),
           "cubarsi": vai((0.62, 0.80), (0.50, 0.81), T(4.0), T(5.6), 99),
           "martin": [(0, 0.38, 0.80), (T(4.0), 0.38, 0.80), (T(5.6), 0.30, 0.79), (T(10.4), 0.30, 0.79),
                      (T(11.6), 0.15, 0.72), (99, 0.15, 0.72)],
           "cancelo": [(0, 0.15, 0.70), (T(4.0), 0.15, 0.70), (T(5.6), 0.12, 0.54), (T(9.8), 0.12, 0.54),
                       (T(10.4), 0.30, 0.80), (99, 0.30, 0.80)],
           "bernal": vai((0.50, 0.74), (0.52, 0.60), T(6.3), T(7.5), 99),
           "pedri": [(0, 0.40, 0.58)]}
    bola = [(0, 0.50, 0.80), (T(5.6), 0.50, 0.80), (T(6.6), 0.52, 0.61), (T(8.0), 0.52, 0.61), (T(8.6), 0.40, 0.58)]
    cena(15.6, "A troca do intervalo", 5,
         jogadores(pos5, mov, mostrar={"farinas", "bernal", "pedri", "martin"}, subs=SUBS_46),
         bola=bola, placar="1–1", minuto="46'",
         formas=[{"tipo": "linha", "ids": ["martin", "cubarsi", "farinas"], "cor": AZUL, "t0": T(5.0), "t1": T(9.6)},
                 {"tipo": "rotulo", "x": 0.5, "y": 0.90, "texto": "3 atrás com bola", "cor": AZUL, "t0": T(5.4),
                  "t1": T(7.0)},
                 {"tipo": "rotulo", "x": 0.72, "y": 0.62, "texto": "Bernal sobe", "cor": AZUL, "t0": T(6.6),
                  "t1": T(8.2)},
                 {"tipo": "rotulo", "x": 0.30, "y": 0.90, "texto": "60' Christensen entra", "cor": AZUL,
                  "t0": T(9.9), "t1": T(12.2)},
                 {"tipo": "rotulo", "x": 0.20, "y": 0.64, "texto": "Martín à esquerda", "cor": AZUL, "t0": T(11.3),
                  "t1": T(12.6)}],
         sobreposicao=tat.citacao(T(12.6), "“A ideia era 15 minutos de lateral direito e trocar quando o Bernal "
                                           "estivesse cansado.”", "Hansi Flick"),
         setas=[{"pts": [(0.85, 0.70), (0.70, 0.78)], "t0": T(4.0), "t1": T(5.6), "tipo": "corrida"},
                {"pts": [(0.50, 0.74), (0.52, 0.60)], "t0": T(6.3), "t1": T(7.5), "tipo": "corrida"}],
         destaques=[("farinas", T(1.4), T(6.0)), ("bernal", T(6.2), T(8.6)), ("martin", T(10.4), T(12.4))])

    # 6. 66': Yamal mete nas costas, Fermín bisa; depois disso o Atlético só remata uma vez
    pos6 = {"oblak": (0.5, 0.03), "llorente": (0.18, 0.15), "pubill": (0.40, 0.12), "koke": (0.42, 0.26),
            "barrios": (0.58, 0.26), "giuliano": (0.20, 0.28), "baena": (0.78, 0.30), "alvarez": (0.55, 0.42),
            "lee": (0.45, 0.42), "raphinha": (0.50, 0.15), "pedri": (0.45, 0.34), "gordon": (0.18, 0.22),
            "farinas": (0.66, 0.50), "bernal": (0.52, 0.46), "cancelo": (0.38, 0.60), "martin": (0.20, 0.52)}
    mov = {"yamal": vai((0.88, 0.36), (0.85, 0.27), T(1.2), T(2.0), 99),
           "grimaldo": vai((0.84, 0.16), (0.83, 0.22), T(1.6), T(2.4), 99),
           "fermin": [(0, 0.63, 0.33), (T(2.6), 0.63, 0.32), (T(4.0), 0.61, 0.12), (99, 0.61, 0.12)],
           "hancko": vai((0.62, 0.13), (0.58, 0.12), T(3.0), T(4.0), 99),
           "oblak": [(0, 0.5, 0.03), (T(4.6), 0.53, 0.03), (T(5.2), 0.47, 0.025)]}
    bola = [(0, 0.66, 0.50), (T(1.2), 0.66, 0.50), (T(1.9), 0.85, 0.28), (T(3.3), 0.85, 0.28), (T(4.0), 0.61, 0.125),
            (T(4.9), 0.61, 0.125), (T(5.2), 0.50, 0.0)]
    cena(9.9, "66' · o bis", 6, jogadores(pos6, mov, mostrar={"yamal", "fermin", "hancko"}, subs=SUBS_66),
         bola=bola, placar="1–1", minuto="66'", vista="ataque", golo=(T(5.25), "1–2", "Fermín"),
         formas=[{"tipo": "rotulo", "x": 0.5, "y": 0.52, "texto": "depois: 1 remate do Atlético", "cor": AZUL,
                  "t0": T(6.2), "t1": 9.9}],
         setas=[{"pts": [(0.66, 0.50), (0.85, 0.28)], "t0": T(1.2), "t1": T(1.9), "tipo": "passe"},
                {"pts": [(0.63, 0.32), (0.61, 0.12)], "t0": T(2.6), "t1": T(4.0), "tipo": "corrida"},
                {"pts": [(0.85, 0.28), (0.61, 0.125)], "t0": T(3.3), "t1": T(4.0), "tipo": "passe"},
                {"pts": [(0.61, 0.125), (0.50, 0.005)], "t0": T(4.9), "t1": T(5.2), "tipo": "remate"}],
         destaques=[("yamal", T(1.2), T(4.0)), ("fermin", T(4.0), 7.0)])

    # 7. a melhoria (leitura nossa): começar como acabou — lateral por dentro, 3 atrás com bola, médio mais à frente
    A = {"martin": (0.38, 0.62), "cubarsi": (0.62, 0.62), "farinas": (0.88, 0.42), "bernal": (0.50, 0.66)}
    B = {"martin": (0.30, 0.62), "cubarsi": (0.50, 0.64), "farinas": (0.70, 0.60), "bernal": (0.50, 0.48)}
    pos7 = {"garcia": (0.5, 0.92), "cancelo": (0.12, 0.40), "pedri": (0.40, 0.36), "fermin": (0.62, 0.34),
            "gordon": (0.15, 0.24), "yamal": (0.85, 0.24), "raphinha": (0.50, 0.20), "oblak": (0.5, 0.03),
            "llorente": (0.16, 0.13), "pubill": (0.38, 0.12), "hancko": (0.62, 0.12), "grimaldo": (0.84, 0.13),
            "giuliano": (0.18, 0.24), "koke": (0.40, 0.25), "barrios": (0.60, 0.25), "baena": (0.82, 0.25),
            "lee": (0.40, 0.52)}
    mov = {j: vai(A[j], B[j], T(2.6), T(6.2), 99) for j in A}
    mov["alvarez"] = vai((0.58, 0.50), (0.62, 0.55), T(7.0), T(7.8), 99)
    bola = [(0, 0.40, 0.36), (T(7.0), 0.40, 0.36), (T(7.0), 0.45, 0.32), (T(7.6), 0.62, 0.56), (T(8.2), 0.68, 0.59)]
    cena(11.2, "A melhoria (a nossa leitura)", 7,
         jogadores(pos7, mov, mostrar={"farinas", "bernal", "alvarez"}, subs={"farinas": "Lateral"}),
         bola=bola, placar="", minuto="",
         formas=[{"tipo": "rotulo", "x": 0.5, "y": 0.78, "texto": "como começou", "cor": CORAL, "t0": T(0.2),
                  "t1": T(2.5)},
                 {"tipo": "entre", "de": ["pedri", "fermin"], "ate": ["martin", "cubarsi"], "cor": CORAL,
                  "rotulo": "buraco", "t0": T(0.3), "t1": T(3.0)},
                 {"tipo": "rotulo", "x": 0.5, "y": 0.78, "texto": "como acabou", "cor": AZUL, "t0": T(2.7),
                  "t1": T(6.8)},
                 {"tipo": "linha", "ids": ["martin", "cubarsi", "farinas"], "cor": AZUL, "t0": T(4.0), "t1": 11.2},
                 {"tipo": "liga", "a": "bernal", "b": "lee", "cor": AZUL, "t0": T(6.2), "t1": 11.2},
                 {"tipo": "liga", "a": "farinas", "b": "alvarez", "cor": AZUL, "t0": T(7.6), "t1": 11.2},
                 {"tipo": "rotulo", "x": 0.5, "y": 0.78, "texto": "linha alta com cobertura", "cor": AZUL,
                  "t0": T(7.2), "t1": 11.2}],
         setas=[{"pts": [A[j], B[j]], "t0": T(2.6), "t1": T(6.2), "tipo": "corrida"} for j in ("farinas", "bernal")] +
               [{"pts": [(0.45, 0.32), (0.62, 0.56)], "t0": T(7.0), "t1": T(7.6), "tipo": "passe"}],
         destaques=[("farinas", T(2.6), T(4.4)), ("bernal", T(4.4), T(6.6))])

    # 8. Agente Claudio + pergunta
    c = cena(9.7, "", 8, jogadores({}), placar="1–2", minuto="FIM", sobreposicao=cartao_agente, nomes=False)
    c.t_capa = 8.4
    # 9. fecho com humor
    cenas.append(cena_fecho(jogadores({}), placar="1–2", frase=6))
    return v, cenas
