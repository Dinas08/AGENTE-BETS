"""Análise tática: Vitória SC 1–2 FC Porto (Liga, 8 nov 2026). Como o Porto recuperou depois de sofrer o empate.

Fontes (verificadas a 8 nov 2026):
- ESPN: onzes (Vitória 4-2-3-1, Porto 4-3-3), golos, substituições, estatísticas (Porto 7 foras de jogo, remates
  16–12 para o Vitória). 38' Borja Sainz, cruzamento de Alberto Costa; 58' André Silva, Alan Varela e Martim
  Fernandes entram (saem Samu, Rosario, Sainz); 66' Nehuén Pérez por Bednarek (lesão) e Hwang por Veiga;
  77' Alan, pé esquerdo, do lado esquerdo da área para o canto inferior direito (assist. Gustavo Silva);
  86' Martim Fernandes, do lado direito da área, assist. Pepê num contra-ataque.
- A Bola (ao minuto): 26' golo de Samu anulado "por posição irregular de Alberto, já confirmada pelo VAR";
  57' Sidibé à trave; 52' "Vitória pede penálti por mão de Zaidu na área, mas o juiz manda jogar"; 56' Gonçalo
  Nogueira queixa-se de "eventual puxão"; 77' "Kiwior, com um mau passe, deu origem à jogada"; árbitro David Silva.
- Maisfutebol: o Porto com bolas em profundidade, muitas vezes "em posição de fora de jogo"; Farioli "musculando o
  meio campo com Hwang e Alan Varela"; Farioli: "A equipa do Vitória é muito física"; "Há momentos em que temos de
  sofrer e ganhar assim" (título). O Jogo: "Sofremos um golo, mas a nossa reação foi excelente"; "O Martim consegue
  jogar nas alas e como lateral".
- Futebol Divertido: possível mão de André Silva na origem do 2–1 discutida nas redes; "não esteja confirmada".
- Observador: 11.ª vitória em 11 jornadas. Dica do canal: vitória do Porto (64%) — acertou.
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
    ("Onze jogos, onze vitórias. Mas em Guimarães, o Porto esteve perto de tropeçar. Vê como é que recuperou.",
     "11 jogos, 11 vitórias. Mas em Guimarães, o Porto esteve perto de tropeçar. Vê como é que recuperou."),
    ("Na primeira parte, o Porto mandou: bolas nas costas de uma defesa do Vitória que subia muito. Tanto que caiu "
     "sete vezes em fora de jogo, e até viu um golo anulado pelo VAR.",
     "Na primeira parte, o Porto mandou: bolas nas costas de uma defesa do Vitória que subia muito. Tanto que caiu "
     "7 vezes em fora de jogo e até viu um golo anulado pelo VAR."),
    ("Aos trinta e oito, o Alberto Costa sobe pela direita, cruza ao milímetro, e o Borja Sainz, de primeira, faz "
     "o zero a um.",
     "Aos 38', Alberto Costa sobe pela direita, cruza ao milímetro e Borja Sainz, de primeira, faz o 0–1."),
    ("Na segunda parte, o Vitória soltou-se: muito físico, a atacar o espaço, e o Sidibé ainda acertou na trave. "
     "O Diogo Costa segurou o que pôde.",
     "Na segunda parte, o Vitória soltou-se: muito físico, a atacar o espaço, e Sidibé ainda acertou na trave. "
     "Diogo Costa segurou o que pôde."),
    ("Aos cinquenta e oito, o Farioli mexeu três vezes de uma vez: André Silva, Alan Varela para dar músculo ao "
     "meio-campo, e o Martim Fernandes, que tanto joga a lateral como na ala.",
     "Aos 58', Farioli mexeu três vezes de uma vez: André Silva, Alan Varela para dar músculo ao meio-campo, "
     "e Martim Fernandes, que tanto joga a lateral como na ala."),
    ("Mas aos setenta e sete, um mau passe do Kívior, e o Alan, acabado de entrar, empata.",
     "Mas aos 77', um mau passe de Kiwior e Alan, acabado de entrar, empata."),
    ("A reação: ataque rápido, o Pepê serve, e o Martim Fernandes, da tripla substituição, faz o um a dois. Nas "
     "palavras do Farioli: há momentos em que temos de sofrer, e ganhar assim.",
     "A reação: ataque rápido, Pepê serve e Martim Fernandes, da tripla substituição, faz o 1–2. Nas palavras do "
     "Farioli: há momentos em que temos de sofrer e ganhar assim."),
    ("E os lances polémicos? O Vitória pediu penálti por mão do Zaidu, e por um puxão ao Gonçalo Nogueira, mas o "
     "árbitro mandou jogar. E nas redes, discute-se uma possível mão do André Silva na origem do segundo golo. "
     "Sem confirmação.",
     "E os lances polémicos? O Vitória pediu penálti por mão do Zaidu e por um puxão ao Gonçalo Nogueira, mas o "
     "árbitro mandou jogar. E nas redes, discute-se uma possível mão do André Silva na origem do segundo golo. "
     "Sem confirmação."),
    ("E o Agente Claudio? Deu vitória do Porto... e acertou. As dicas estão na rede vizinha, link na bio. E tu: "
     "onze em onze, este Porto já é candidato a campeão? Diz nos comentários.",
     "E o Agente Claudio? Deu vitória do Porto e acertou. As dicas estão na rede vizinha, link na bio. E tu: "
     "11 em 11, este Porto já é candidato a campeão? Diz nos comentários."),
]

# ------------------------------------------------------------------ jogadores
# Aqui o Porto é a equipa "casa" do motor (ataca para cima, bolas azuis); o Vitória ataca para baixo (bolas brancas).
# O marcador continua VIT–POR (o Vitória jogou em casa).
JOG = {
    "costa": ("D. Costa", "casa", (0.50, 0.95)),
    "zaidu": ("Zaidu", "casa", (0.15, 0.79)),
    "kiwior": ("Kiwior", "casa", (0.38, 0.85)),
    "bednarek": ("Bednarek", "casa", (0.62, 0.85)),
    "acosta": ("Alberto Costa", "casa", (0.85, 0.79)),
    "rosario": ("Rosario", "casa", (0.50, 0.72)),
    "veiga": ("G. Veiga", "casa", (0.36, 0.64)),
    "froholdt": ("Froholdt", "casa", (0.64, 0.64)),
    "sainz": ("Borja Sainz", "casa", (0.17, 0.56)),
    "samu": ("Samu", "casa", (0.50, 0.54)),
    "pepe": ("Pepê", "casa", (0.83, 0.56)),
    "furtado": ("L. Furtado", "fora", (0.50, 0.05)),
    "strata": ("Strata", "fora", (0.15, 0.20)),
    "borevkovic": ("Borevković", "fora", (0.38, 0.15)),
    "sidibe": ("Sidibé", "fora", (0.62, 0.15)),
    "mendes": ("J. Mendes", "fora", (0.85, 0.20)),
    "gnogueira": ("G. Nogueira", "fora", (0.40, 0.30)),
    "mukendi": ("Mukendi", "fora", (0.60, 0.30)),
    "camara": ("Camara", "fora", (0.15, 0.38)),
    "samuv": ("Samu", "fora", (0.50, 0.39)),
    "gustavo": ("Gustavo Silva", "fora", (0.85, 0.38)),
    "jakupovic": ("Jakupović", "fora", (0.50, 0.46)),
}
SUBS_58 = {"samu": "André Silva", "rosario": "Alan Varela", "sainz": "Martim F."}
SUBS_77 = dict(SUBS_58, bednarek="Nehuén Pérez", veiga="Hwang", samuv="Alan", jakupovic="Ndoye")
SUBS_86 = dict(SUBS_77, acosta="Giménez", gustavo="M. Nogueira", sidibe="Balieiro")
BRANCO = (236, 234, 226)


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
    d.text((W / 2, CY0 + CH * 0.44), "VITÓRIA  ·  PORTO", font=fonte(SANS_SB, 40), fill=AZUL + (255,), anchor="mm")
    k = suave((t - 0.15) / 0.35)
    if k > 0:
        d.text((W / 2, CY0 + CH * 0.57), "11 jogos · 11 vitórias", font=fonte(SERIFA_N, 70),
               fill=CREME + (int(255 * k),), anchor="mm")
    k = suave((t - 3.8) / 0.3)
    if k > 0:
        _chip(d, W / 2, CY0 + CH * 0.70, "Mas esteve perto de tropeçar", CORAL, k)
    q.im.paste(ov, (0, 0), ov)


def tripla(v, q, t):
    _fundo(q, t)
    d = q.d
    k = suave((t - 0.1) / 0.35)
    if k > 0:
        d.text((W / 2, CY0 + 100), "58'", font=fonte(SERIFA_N, 120), fill=CREME + (int(255 * k),), anchor="mm")
        d.text((W / 2, CY0 + 200), "A TRIPLA DO FARIOLI", font=fonte(SANS_SB, 38), fill=AZUL + (int(255 * k),),
               anchor="mm")
    trocas = [("Samu", "André Silva", "", 2.4), ("Rosario", "Alan Varela", "músculo no meio", 3.1),
              ("Borja Sainz", "Martim Fernandes", "lateral ou ala", 5.2)]
    for i, (sai, entra, nota, ti) in enumerate(trocas):
        kk = suave((t - ti) / 0.3)
        if kk <= 0:
            continue
        y = CY0 + 320 + i * 120
        d.rounded_rectangle((90, y - 48, W - 90, y + 48), radius=24, fill=(44, 42, 39, int(255 * kk)))
        d.text((125, y), sai, font=fonte(SANS, 34), fill=CREME_70 + (int(255 * kk),), anchor="lm")
        d.text((W / 2 - 60, y), "→", font=fonte(SANS_SB, 38), fill=AZUL + (int(255 * kk),), anchor="mm")
        d.text((W / 2 - 20, y - (12 if nota else 0)), entra, font=fonte(SANS_SB, 38), fill=CREME + (int(255 * kk),),
               anchor="lm")
        if nota:
            d.text((W / 2 - 20, y + 26), nota, font=fonte(SANS, 24), fill=AZUL + (int(255 * kk),), anchor="lm")
    k = suave((t - 6.6) / 0.3)
    if k > 0:
        d.text((W / 2, CY0 + 700), "66'  Bednarek (concussão) → Nehuén Pérez", font=fonte(SANS, 32),
               fill=CREME_70 + (int(255 * k),), anchor="mm")
        d.text((W / 2, CY0 + 760), "66'  Gabri Veiga → Hwang", font=fonte(SANS, 32),
               fill=CREME_70 + (int(255 * k),), anchor="mm")


def polemicas(v, q, t):
    _fundo(q, t)
    d = q.d
    k = suave((t - 0.1) / 0.35)
    if k > 0:
        d.text((W / 2, CY0 + 80), "Lances polémicos", font=fonte(SERIFA_N, 70), fill=CREME + (int(255 * k),),
               anchor="mm")
    lances = [("26'", "Golo do Porto anulado", "VAR: fora de jogo", 0.6, AZUL),
              ("52'", "Mão de Zaidu na área?", "o árbitro mandou jogar", 2.1, BRANCO),
              ("56'", "Puxão a Gonçalo Nogueira?", "o árbitro mandou jogar", 3.6, BRANCO),
              ("86'", "Mão de André Silva no 1–2?", "sem confirmação", 6.7, CORAL)]
    for i, (m, txt, sub, ti, cor) in enumerate(lances):
        kk = suave((t - ti) / 0.3)
        if kk <= 0:
            continue
        y = CY0 + 230 + i * 160
        d.rounded_rectangle((80, y - 62, W - 80, y + 62), radius=24, fill=(36, 34, 32, int(255 * kk)),
                            outline=(70, 66, 60, int(255 * kk)), width=2)
        d.rounded_rectangle((80, y - 62, 92, y + 62), radius=6, fill=cor + (int(255 * kk),))
        d.text((130, y), m, font=fonte(SERIFA_N, 50), fill=cor + (int(255 * kk),), anchor="lm")
        d.text((250, y - 18), txt, font=fonte(SANS_SB, 38), fill=CREME + (int(255 * kk),), anchor="lm")
        d.text((250, y + 28), sub, font=fonte(SANS, 30), fill=CREME_70 + (int(255 * kk),), anchor="lm")
    k = suave((t - 1.0) / 0.3)
    if k > 0:
        d.text((W / 2, CY0 + 900), "Árbitro: David Silva", font=fonte(SANS, 28), fill=CREME_70 + (int(200 * k),),
               anchor="mm")


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
        d.text((W / 2 + 30, CY0 + 335), "Vitória do Porto · 64%", font=fonte(SERIFA_N, 58),
               fill=CREME + (int(255 * k),), anchor="mm")
    k = suave((t - 2.35) / 0.25)
    if k > 0:
        _visto(d, W / 2 - 330, CY0 + 337, k, r=28)
    k = suave((t - 2.85) / 0.3)
    if k > 0:
        _chip(d, W / 2, CY0 + 455, "Dicas na rede vizinha · link na bio", CORAL, k, tam=34)
    k = suave((t - 5.15) / 0.3)
    if k > 0:
        d.text((W / 2, CY0 + 570), "11 em 11: candidato?", font=fonte(SERIFA_N, 66), fill=CREME + (int(255 * k),),
               anchor="mm")
    for i, (letra, txt) in enumerate((("A", "Já é"), ("B", "Ainda é cedo"))):
        kk = suave((t - 5.5 - i * 0.15) / 0.35)
        if kk <= 0:
            continue
        cx, cy = W / 2 + (-215 if i == 0 else 215), CY0 + 740
        d.rounded_rectangle((cx - 195, cy - 85, cx + 195, cy + 85), radius=28, fill=(44, 42, 39, int(255 * kk)),
                            outline=(80, 76, 70, int(255 * kk)), width=2)
        d.text((cx, cy - 22), letra, font=fonte(SERIFA_N, 58), fill=CREME + (int(255 * kk),), anchor="mm")
        d.text((cx, cy + 40), txt, font=fonte(SANS_SB, 38), fill=CREME + (int(255 * kk),), anchor="mm")
    k = suave((t - 8.0) / 0.3)
    if k > 0:
        d.text((W / 2, CY0 + 900), "Comenta A ou B", font=fonte(SANS_SB, 46), fill=CORAL + (int(255 * k),),
               anchor="mm")


# ------------------------------------------------------------------ cenas

REF_VOZ = [5.21, 7.29, 6.08, 6.51, 8.33, 4.53, 10.06, 10.85, 9.45]


def construir():
    v = Video("Vitória", "Porto", abrev=("VIT", "POR"), fonte_txt="Ilustração · dados ESPN, A Bola, Maisfutebol e O Jogo")
    v.folga, v.bpm = 0.35, 112
    v.sp["casa"] = sprite(17, (48, 98, 180), CREME, 2.5)   # Porto: azul
    v.sp["fora"] = sprite(17, BRANCO, (20, 20, 19), 3)    # Vitória: branco
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
    c = cena(5.7, "Vitória 1–2 Porto: a tática", 0, jogadores({}), placar="1–2", minuto="FIM",
             sobreposicao=gancho, nomes=False)
    c.t_capa = 4.6

    # 1. 1.ª parte: o Porto ataca a profundidade contra uma linha alta (7 foras de jogo, golo anulado)
    pos1 = {"furtado": (0.5, 0.04), "strata": (0.15, 0.30), "borevkovic": (0.38, 0.28), "sidibe": (0.62, 0.28),
            "mendes": (0.85, 0.30), "gnogueira": (0.40, 0.42), "mukendi": (0.60, 0.42), "camara": (0.18, 0.50),
            "gustavo": (0.82, 0.50), "samuv": (0.50, 0.52), "jakupovic": (0.50, 0.60),
            "sainz": (0.17, 0.36), "pepe": (0.83, 0.36), "veiga": (0.36, 0.50), "froholdt": (0.64, 0.48),
            "acosta": (0.88, 0.50), "zaidu": (0.12, 0.54), "rosario": (0.5, 0.62)}
    mov = {"samu": [(0, 0.48, 0.33), (T(1.5), 0.48, 0.33), (T(2.6), 0.50, 0.12), (T(4.0), 0.50, 0.12),
                    (T(5.2), 0.47, 0.33), (T(5.9), 0.52, 0.12), (99, 0.52, 0.12)],
           "acosta": [(0, 0.88, 0.50), (T(5.0), 0.86, 0.46), (T(5.9), 0.76, 0.20), (99, 0.76, 0.20)]}
    bola = [(0, 0.36, 0.50), (T(1.6), 0.36, 0.50), (T(2.5), 0.50, 0.13), (T(3.6), 0.50, 0.13), (T(4.2), 0.36, 0.50),
            (T(5.2), 0.36, 0.50), (T(5.8), 0.75, 0.21), (T(6.1), 0.52, 0.13), (T(6.3), 0.50, 0.0)]
    defesa = ["strata", "borevkovic", "sidibe", "mendes"]
    cena(7.8, "1.ª parte · a profundidade", 1, jogadores(pos1, mov, mostrar={"samu", "acosta"}),
         bola=bola, placar="0–0", minuto="", vista="ataque",
         formas=[{"tipo": "linha", "ids": defesa, "cor": BRANCO, "t0": T(1.8), "t1": T(4.4)},
                 {"tipo": "rotulo", "x": 0.5, "y": 0.22, "texto": "linha alta", "cor": BRANCO, "t0": T(2.6),
                  "t1": T(3.9)},
                 {"tipo": "rotulo", "x": 0.5, "y": 0.22, "texto": "7 foras de jogo", "cor": AZUL, "t0": T(4.0),
                  "t1": T(5.5)},
                 {"tipo": "rotulo", "x": 0.5, "y": 0.22, "texto": "golo anulado pelo VAR", "cor": CORAL,
                  "t0": T(6.4), "t1": 7.8}],
         setas=[{"pts": [(0.36, 0.50), (0.50, 0.13)], "t0": T(1.6), "t1": T(2.5), "tipo": "passe"},
                {"pts": [(0.48, 0.33), (0.50, 0.12)], "t0": T(1.5), "t1": T(2.6), "tipo": "corrida"}],
         destaques=[("samu", T(1.4), T(3.0)), ("acosta", T(5.6), T(6.6))])

    # 2. 38': Alberto Costa cruza, Borja Sainz de primeira
    pos2 = {"furtado": (0.5, 0.03), "strata": (0.16, 0.16), "borevkovic": (0.40, 0.12), "sidibe": (0.58, 0.12),
            "mendes": (0.84, 0.17), "gnogueira": (0.42, 0.26), "mukendi": (0.58, 0.26), "camara": (0.20, 0.32),
            "gustavo": (0.80, 0.32), "samuv": (0.50, 0.38), "jakupovic": (0.50, 0.50),
            "samu": (0.52, 0.12), "pepe": (0.66, 0.20), "veiga": (0.40, 0.34), "froholdt": (0.64, 0.38),
            "rosario": (0.5, 0.46), "zaidu": (0.12, 0.44)}
    mov = {"acosta": [(0, 0.85, 0.42), (T(1.2), 0.85, 0.40), (T(2.4), 0.88, 0.15), (99, 0.88, 0.15)],
           "sainz": [(0, 0.24, 0.24), (T(2.8), 0.26, 0.22), (T(4.1), 0.43, 0.075), (99, 0.43, 0.075)],
           "mendes": vai((0.84, 0.17), (0.86, 0.12), T(1.6), T(2.6), 99),
           "furtado": [(0, 0.5, 0.03), (T(4.1), 0.46, 0.03), (T(4.6), 0.52, 0.02)]}
    bola = [(0, 0.64, 0.385), (T(1.0), 0.64, 0.385), (T(1.7), 0.865, 0.30), (T(2.4), 0.875, 0.16),
            (T(3.2), 0.875, 0.16), (T(4.1), 0.43, 0.08), (T(4.3), 0.43, 0.08), (T(4.6), 0.455, 0.0)]
    cena(6.6, "38' · o cruzamento", 2, jogadores(pos2, mov, mostrar={"acosta", "sainz"}),
         bola=bola, placar="0–0", minuto="38'", vista="ataque", golo=(T(4.65), "0–1", "Borja Sainz"),
         setas=[{"pts": [(0.64, 0.385), (0.865, 0.30)], "t0": T(1.0), "t1": T(1.7), "tipo": "passe"},
                {"pts": [(0.85, 0.40), (0.88, 0.15)], "t0": T(1.2), "t1": T(2.4), "tipo": "corrida"},
                {"pts": [(0.875, 0.16), (0.43, 0.08)], "t0": T(3.2), "t1": T(4.1), "tipo": "passe"},
                {"pts": [(0.43, 0.08), (0.455, 0.005)], "t0": T(4.3), "t1": T(4.6), "tipo": "remate"}],
         destaques=[("acosta", T(1.0), T(3.3)), ("sainz", T(3.3), 6.6)])

    # 3. 2.ª parte: o Vitória solta-se (físico, ataca o espaço, Sidibé à trave). Vista da defesa do Porto
    pos3 = {"costa": (0.5, 0.975), "zaidu": (0.18, 0.86), "kiwior": (0.40, 0.88), "bednarek": (0.60, 0.88),
            "acosta": (0.82, 0.86), "rosario": (0.50, 0.78), "veiga": (0.38, 0.74), "froholdt": (0.62, 0.74),
            "sainz": (0.20, 0.64), "pepe": (0.80, 0.64), "samu": (0.50, 0.60),
            "gustavo": (0.80, 0.74), "camara": (0.20, 0.74), "samuv": (0.47, 0.70), "mukendi": (0.58, 0.64),
            "gnogueira": (0.40, 0.62), "borevkovic": (0.40, 0.52), "strata": (0.12, 0.62), "mendes": (0.88, 0.62),
            "furtado": (0.5, 0.05)}
    mov = {"jakupovic": [(0, 0.50, 0.72), (T(1.8), 0.50, 0.73), (T(2.6), 0.52, 0.82), (99, 0.52, 0.82)],
           "camara": vai((0.20, 0.74), (0.26, 0.86), T(2.4), T(3.3), 99),
           "sidibe": [(0, 0.60, 0.52), (T(2.6), 0.60, 0.54), (T(3.5), 0.58, 0.69), (99, 0.58, 0.69)],
           "costa": [(0, 0.5, 0.975), (T(3.6), 0.5, 0.975), (T(4.0), 0.47, 0.978)]}
    bola = [(0, 0.40, 0.53), (T(1.8), 0.40, 0.53), (T(2.6), 0.52, 0.81), (T(2.9), 0.52, 0.81), (T(3.5), 0.58, 0.68),
            (T(3.6), 0.58, 0.68), (T(4.0), 0.50, 0.995), (T(4.5), 0.53, 0.89)]
    cena(7.0, "2.ª parte · o Vitória solta-se", 3,
         jogadores(pos3, mov, mostrar={"jakupovic", "sidibe", "costa"}),
         bola=bola, placar="0–1", minuto="", vista="defesa",
         formas=[{"tipo": "rotulo", "x": 0.5, "y": 0.62, "texto": "muito físico", "cor": BRANCO, "t0": T(1.8),
                  "t1": T(3.2)},
                 {"tipo": "rotulo", "x": 0.26, "y": 0.93, "texto": "trave!", "cor": CORAL, "t0": T(4.0),
                  "t1": T(5.6)}],
         setas=[{"pts": [(0.40, 0.53), (0.52, 0.81)], "t0": T(1.8), "t1": T(2.6), "tipo": "passe"},
                {"pts": [(0.20, 0.74), (0.26, 0.86)], "t0": T(2.4), "t1": T(3.3), "tipo": "corrida_fora"},
                {"pts": [(0.58, 0.68), (0.50, 0.995)], "t0": T(3.6), "t1": T(4.0), "tipo": "remate"}],
         destaques=[("jakupovic", T(1.8), T(3.0)), ("sidibe", T(3.0), T(4.6)), ("costa", T(4.6), 7.0)])

    # 4. a tripla do Farioli (58')
    cena(8.8, "A resposta do Farioli", 4, jogadores({}), placar="0–1", minuto="58'", sobreposicao=tripla,
         nomes=False)

    # 5. 77': mau passe de Kiwior, Gustavo Silva serve, Alan empata (vista da defesa do Porto)
    pos5 = {"costa": (0.5, 0.975), "zaidu": (0.18, 0.86), "bednarek": (0.62, 0.88), "acosta": (0.84, 0.84),
            "rosario": (0.46, 0.74), "veiga": (0.62, 0.70), "froholdt": (0.70, 0.66), "sainz": (0.82, 0.60),
            "samu": (0.50, 0.58), "pepe": (0.25, 0.60), "camara": (0.22, 0.72), "jakupovic": (0.50, 0.84),
            "mukendi": (0.58, 0.60), "gnogueira": (0.40, 0.60), "borevkovic": (0.40, 0.48), "sidibe": (0.60, 0.48),
            "strata": (0.12, 0.60), "mendes": (0.88, 0.62), "furtado": (0.5, 0.05)}
    mov = {"kiwior": [(0, 0.40, 0.84)],
           "gustavo": [(0, 0.60, 0.70), (T(1.0), 0.60, 0.71), (T(1.6), 0.55, 0.765), (99, 0.55, 0.765)],
           "samuv": [(0, 0.74, 0.76), (T(1.6), 0.74, 0.77), (T(2.5), 0.71, 0.86), (99, 0.71, 0.86)],
           "costa": [(0, 0.5, 0.975), (T(3.0), 0.53, 0.975), (T(3.4), 0.47, 0.978)]}
    bola = [(0, 0.40, 0.835), (T(1.0), 0.40, 0.835), (T(1.6), 0.55, 0.76), (T(1.9), 0.55, 0.76), (T(2.5), 0.705, 0.855),
            (T(3.0), 0.705, 0.855), (T(3.4), 0.455, 1.0)]
    cena(5.0, "77' · o erro", 5, jogadores(pos5, mov, mostrar={"kiwior", "gustavo", "samuv"}, subs=SUBS_77),
         bola=bola, placar="0–1", minuto="77'", vista="defesa", golo=(T(3.45), "1–1", "Alan"),
         formas=[{"tipo": "rotulo", "x": 0.30, "y": 0.78, "texto": "mau passe", "cor": CORAL, "t0": T(1.0),
                  "t1": T(2.4)}],
         setas=[{"pts": [(0.40, 0.835), (0.55, 0.76)], "t0": T(1.0), "t1": T(1.6), "tipo": "passe"},
                {"pts": [(0.55, 0.76), (0.705, 0.855)], "t0": T(1.9), "t1": T(2.5), "tipo": "passe"},
                {"pts": [(0.705, 0.855), (0.455, 0.995)], "t0": T(3.0), "t1": T(3.4), "tipo": "remate"}],
         destaques=[("kiwior", T(0.8), T(1.8)), ("samuv", T(2.0), 5.0)])

    # 6. 86': a reação. Contra-ataque, Pepê serve, Martim Fernandes marca
    pos6 = {"costa": (0.5, 0.95), "zaidu": (0.18, 0.80), "kiwior": (0.40, 0.84), "bednarek": (0.60, 0.84),
            "rosario": (0.46, 0.70), "veiga": (0.56, 0.68), "froholdt": (0.68, 0.66), "acosta": (0.40, 0.56),
            "samu": (0.30, 0.52), "furtado": (0.5, 0.04), "samuv": (0.52, 0.72), "jakupovic": (0.46, 0.78),
            "camara": (0.22, 0.70), "mukendi": (0.56, 0.58), "gnogueira": (0.40, 0.60), "strata": (0.15, 0.55),
            "mendes": (0.86, 0.60)}
    mov = {"pepe": [(0, 0.62, 0.62), (T(0.7), 0.62, 0.61), (T(1.6), 0.58, 0.40), (99, 0.58, 0.40)],
           "sainz": [(0, 0.80, 0.56), (T(0.8), 0.80, 0.55), (T(2.6), 0.74, 0.15), (99, 0.74, 0.15)],
           "gustavo": vai((0.75, 0.60), (0.72, 0.30), T(0.8), T(2.8), 99),
           "borevkovic": vai((0.40, 0.42), (0.50, 0.16), T(0.8), T(2.8), 99),
           "sidibe": vai((0.60, 0.42), (0.62, 0.18), T(0.8), T(2.8), 99),
           "furtado": [(0, 0.5, 0.04), (T(4.0), 0.48, 0.04), (T(4.6), 0.44, 0.03)]}
    bola = [(0, 0.62, 0.62), (T(0.7), 0.62, 0.61), (T(1.6), 0.58, 0.41), (T(1.7), 0.58, 0.41), (T(2.5), 0.735, 0.16),
            (T(2.7), 0.74, 0.15), (T(4.3), 0.74, 0.15), (T(4.6), 0.545, 0.0)]
    cena(10.6, "86' · a reação", 6, jogadores(pos6, mov, mostrar={"pepe", "sainz"}, subs=SUBS_86),
         bola=bola, placar="1–1", minuto="86'", golo=(T(4.65), "1–2", "Martim Fernandes"),
         sobreposicao=tat.citacao(T(5.5), "“Há momentos em que temos de sofrer e ganhar assim.”",
                                  "Francesco Farioli"),
         setas=[{"pts": [(0.62, 0.61), (0.58, 0.41)], "t0": T(0.7), "t1": T(1.6), "tipo": "conducao"},
                {"pts": [(0.80, 0.55), (0.74, 0.15)], "t0": T(0.8), "t1": T(2.6), "tipo": "corrida"},
                {"pts": [(0.58, 0.41), (0.735, 0.16)], "t0": T(1.7), "t1": T(2.5), "tipo": "passe"},
                {"pts": [(0.74, 0.15), (0.545, 0.005)], "t0": T(4.3), "t1": T(4.6), "tipo": "remate"}],
         destaques=[("pepe", T(0.7), T(2.2)), ("sainz", T(2.2), 6.0)])

    # 7. lances polémicos
    cena(11.4, "Os lances polémicos", 7, jogadores({}), placar="1–2", minuto="FIM", sobreposicao=polemicas,
         nomes=False)
    # 8. Agente Claudio + pergunta
    c = cena(10.0, "", 8, jogadores({}), placar="1–2", minuto="FIM", sobreposicao=cartao_agente, nomes=False)
    c.t_capa = 8.6
    # 9. fecho com humor
    cenas.append(cena_fecho(jogadores({}), placar="1–2", frase=4))
    return v, cenas
