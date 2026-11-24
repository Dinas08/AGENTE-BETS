"""Os 3 grandes na Taça de Portugal, 4.ª eliminatória (20-22 nov 2026). Recap com humor leve e rimas.

Fontes (verificadas a 24 nov 2026):
- FC Porto 1-1 Paredes (3-1 g.p., após prolongamento), Dragão, 20 nov. ESPN (401931821): Fofana 41', autogolo de
  Francisco Moura 58'. Maisfutebol: jogada iniciada por Souza, com Borja Sainz, assistência de André Silva; depois de
  uma defesa de Cláudio Ramos, Moura, sem pressão, tentou aliviar e meteu na própria baliza, saiu a chorar; Moura
  jogou a central; livre de Hwang à barra aos 111'; Cláudio Ramos "parou três tentativas" e Froholdt fechou o 3-1.
  O Jogo: marcaram Santi Giménez, Bednarek e Froholdt. Notícias ao Minuto: muito apoio dos adeptos a Moura.
  Paredes é da Liga 3; o Porto é líder da I Liga.
- Sporting 4-0 União da Serra, Alvalade, 21 nov. ESPN (401931820): Rafael Nel g.p. 58', Irankunda 61' e 73',
  Catamo 70'. Maisfutebol e ZeroZero: 0-0 ao intervalo com o guarda-redes David Santos "um gigante entre os
  postes"; União da Serra do Campeonato de Portugal (4.º escalão). ZeroZero: 61' Inácio longo, Pedro Lima de cabeça,
  Nel serve Irankunda.
- Torreense 1-3 Benfica, Jamor, 22 nov. ESPN (401931822): Durán 30', Drammeh 50', Prestianni 64', Kamiński 85'.
  Maisfutebol e ZeroZero: cruzamento de Dahl para o 2.º poste e cabeça de Durán; Sudakov perde a bola para Alfaro
  e Drammeh empata; Bah → Echeverri → Prestianni, bola no poste e golo; Torreense é o detentor da Taça (ganhou a
  final ao Sporting no Jamor). Observador: o Benfica defronta o Tondela nos oitavos.
- Agente Claudio (ramo claude/dados): previsões certas vitória do Sporting (97%), vitória do Benfica (76%); dica do
  canal "Mais de 2.5 golos" no Torreense-Benfica (72%, mensagem 296) certa. A previsão do Porto (91%) falhou (1-1
  aos 90'): não aparece.
Cores: Porto azul, Sporting verde, Benfica vermelho; os adversários a branco (cores não confirmadas).
As jogadas são ilustrações coerentes com isto.
"""
from PIL import Image, ImageDraw

from quadro_tatico import (cena_fecho, sprite, CORAL, CREME, CREME_70, CY0, CH, W, Cena, Video, fonte, suave,
                           SERIFA_N, SANS, SANS_SB)

import porto_napoli as base
import benfica_lech as bl

vai, _ov, PFP, _visto = base.vai, base._ov, base.PFP, base._visto
_fundo, _chip = bl._fundo, bl._chip
AZUL_FCP = (35, 85, 175)
VERDE_SCP = (25, 135, 75)
VERMELHO = (200, 40, 50)
BRANCO = (236, 234, 226)
CORES = {"fcp": AZUL_FCP, "scp": VERDE_SCP, "slb": VERMELHO}

FALAS = [
    ("O líder da Liga quase caiu contra uma equipa da Liga Três... e quem o salvou foi uma parede.",
     "O líder da Liga quase caiu contra uma equipa da Liga 3… e quem o salvou foi uma parede."),
    ("No Dragão, o André Silva serve, e o Fofana marca. Fácil? Calma.",
     "No Dragão, o André Silva serve e o Fofana marca. Fácil? Calma."),
    ("O Cláudio Ramos defende, a bola sobra para o Francisco Moura, sozinho... e ele mete-a na própria baliza. "
     "Saiu a chorar, e o Dragão aplaudiu-o.",
     "O Cláudio Ramos defende, a bola sobra para o Francisco Moura, sozinho… e ele mete-a na própria baliza. "
     "Saiu a chorar, e o Dragão aplaudiu-o."),
    ("Prolongamento, grandes penalidades, e o Cláudio Ramos defende três. Contra o Paredes... uma parede.",
     "Prolongamento, grandes penalidades, e o Cláudio Ramos defende três. Contra o Paredes… uma parede."),
    ("Em Alvalade, uma hora a bater à porta do União da Serra... e depois, quatro golos em quinze minutos: o Nél, "
     "o Catamo, e o Irankunda a bisar.",
     "Em Alvalade, uma hora a bater à porta do União da Serra… e depois, 4 golos em 15 minutos: o Nel, o Catamo e "
     "o Irankunda a bisar."),
    ("No Jamor, contra o dono da Taça: o Durán marca de cabeça, o Dramé empata, mas o Prestiáni e o Kamínski "
     "resolvem. O dono da Taça ficou sem ela... e o Benfica vai defrontar o Tondela.",
     "No Jamor, contra o dono da Taça: o Durán marca de cabeça, o Drammeh empata, mas o Prestianni e o Kamiński "
     "resolvem. O dono da Taça ficou sem ela… e o Benfica vai defrontar o Tondela."),
    ("O Agente Claudio acertou na vitória do Sporting, na do Benfica, e nos golos do Jamor. As previsões estão na "
     "rede vizinha, link na bio.",
     "O Agente Claudio acertou na vitória do Sporting, na do Benfica e nos golos do Jamor. As previsões estão na "
     "rede vizinha, link na bio."),
    ("Herói da eliminatória: o Irankunda, ou o Cláudio Ramos? Comenta.",
     "Herói da eliminatória: o Irankunda ou o Cláudio Ramos? Comenta."),
]
FECHO = ("[laughs] Manda isto ao teu amigo que acha a Taça sem graça... e roeu as unhas até ao fim.",
         ["Manda isto ao teu amigo", "que acha a Taça sem graça", "e roeu as unhas até ao |fim|."])

# ------------------------------------------------------------------ jogadores genéricos
# o grande ataca sempre para cima ("g_"); o adversário defende a baliza de cima ("a_")
G = {"gr": (0.50, 0.95), "d1": (0.15, 0.80), "d2": (0.38, 0.85), "d3": (0.62, 0.85), "d4": (0.85, 0.80),
     "m1": (0.35, 0.66), "m2": (0.50, 0.70), "m3": (0.65, 0.66), "a1": (0.18, 0.50), "a2": (0.50, 0.48),
     "a3": (0.82, 0.50)}
A = {"gr": (0.50, 0.04), "d1": (0.15, 0.18), "d2": (0.38, 0.14), "d3": (0.62, 0.14), "d4": (0.85, 0.18),
     "m1": (0.15, 0.32), "m2": (0.40, 0.30), "m3": (0.60, 0.30), "m4": (0.85, 0.32), "a1": (0.42, 0.44),
     "a2": (0.58, 0.44)}


def jogadores(grande, pos, mov=None, nomes=None):
    """grande: 'fcp'/'scp'/'slb'. pos/mov/nomes com chaves 'g_xx' (grande) e 'a_xx' (adversário)."""
    out = {}
    for pre, base_pos, eq in (("g_", G, grande), ("a_", A, "adv")):
        for k, xy in base_pos.items():
            jid = pre + k
            x, y = (pos or {}).get(jid, xy)
            out[jid] = {"nome": (nomes or {}).get(jid, ""), "equipa": eq, "chaves": (mov or {}).get(jid, [(0, x, y)])}
    return out


def vazio():
    return jogadores("fcp", {})


VI = 0.15


def T(x):
    return x + VI


def _linha_res(d, y, cor, casa, plac, fora, extra, k, destaque=False):
    al = int(255 * k)
    d.rounded_rectangle((70, y - 52, W - 70, y + 52), radius=22,
                        fill=((70, 40, 36) if destaque else (36, 34, 32)) + (al,), outline=(70, 66, 60, al), width=2)
    d.rounded_rectangle((70, y - 52, 84, y + 52), radius=7, fill=cor + (al,))
    d.text((W / 2 - 95, y), casa, font=fonte(SERIFA_N, 44), fill=CREME + (al,), anchor="rm")
    d.text((W / 2, y), plac, font=fonte(SERIFA_N, 54), fill=(CORAL if destaque else CREME) + (al,), anchor="mm")
    d.text((W / 2 + 95, y), fora, font=fonte(SERIFA_N, 44), fill=CREME + (al,), anchor="lm")
    if extra:
        d.text((W / 2, y + 40), extra, font=fonte(SANS_SB, 24), fill=CORAL + (al,), anchor="mm")


# ------------------------------------------------------------------ sobreposições

def _parede(d, cx, y0, k, bw=96, bh=40, n=5):
    """Parede de tijolos a cair de cima (k 0→1)."""
    al = int(255 * min(1, k * 1.5))
    queda = (1 - suave(k)) * 120
    x0 = cx - n * bw / 2
    for fila in range(3):
        off = 0 if fila % 2 == 0 else bw / 2
        for c in range(-1, n + 1):
            xa, xb = max(x0 + c * bw + off, x0), min(x0 + c * bw + off + bw - 6, x0 + n * bw - 6)
            if xb > xa:
                y = y0 + fila * bh - queda * (3 - fila) / 3
                d.rectangle((xa, y, xb, y + bh - 6), fill=CORAL + (al,))


def gancho(v, q, t):
    """Primeiro frame já com tudo o que prende: o líder, o 1–1 e a Liga 3. Sem entrada em fade."""
    ov = _ov(q)
    d = ImageDraw.Draw(ov)
    d.rectangle((0, CY0 + CH * 0.06, W, CY0 + CH * 0.90), fill=(20, 20, 19, 238))
    d.text((W / 2, CY0 + 120), "OS 3 GRANDES NA TAÇA", font=fonte(SANS_SB, 34), fill=CORAL + (255,), anchor="mm")
    # o líder vs a Liga 3 (já visível no frame 0)
    pulso = 1 + 0.04 * max(0, 1 - t / 0.4)
    for cx, txt, cor, sub in ((W / 2 - 280, "LÍDER", AZUL_FCP, "da Liga"), (W / 2 + 280, "LIGA 3", (90, 86, 80),
                                                                            "Paredes")):
        d.rounded_rectangle((cx - 140, CY0 + 220, cx + 140, CY0 + 360), radius=26, fill=cor + (255,))
        d.text((cx, CY0 + 275), txt, font=fonte(SANS_SB, int(52 * pulso)), fill=CREME + (255,), anchor="mm")
        d.text((cx, CY0 + 330), sub, font=fonte(SANS, 28), fill=CREME + (220,), anchor="mm")
    d.text((W / 2, CY0 + 290), "1–1", font=fonte(SERIFA_N, int(96 * pulso)), fill=CREME + (255,), anchor="mm")
    k = suave((t - T(1.0)) / 0.25)  # "quase caiu"
    if k > 0:
        d.text((W / 2, CY0 + 430), "quase caiu…", font=fonte(SERIFA_N, 58), fill=CREME_70 + (int(255 * k),),
               anchor="mm")
    k = (t - T(3.3)) / 0.5  # "quem o salvou foi uma parede"
    if k > 0:
        _parede(d, W / 2, CY0 + 520, min(1, k))
        kk = suave((t - T(4.1)) / 0.2)
        if kk > 0:
            d.text((W / 2, CY0 + 690), "uma parede?", font=fonte(SERIFA_N, 66), fill=CREME + (int(255 * kk),),
                   anchor="mm")
    q.im.paste(ov, (0, 0), ov)


def penaltis(v, q, t):
    ov = _ov(q)
    d = ImageDraw.Draw(ov)
    d.rectangle((0, CY0 + CH * 0.08, W, CY0 + CH * 0.88), fill=(20, 20, 19, 230))
    k = suave((t - T(0.6)) / 0.25)
    if k > 0:
        d.text((W / 2, CY0 + 160), "GRANDES PENALIDADES", font=fonte(SANS_SB, 34), fill=CORAL + (int(255 * k),),
               anchor="mm")
        d.text((W / 2, CY0 + 250), "POR 3–1 PAR", font=fonte(SERIFA_N, 90), fill=CREME + (int(255 * k),),
               anchor="mm")
    for i in range(3):  # as três defesas
        kk = suave((t - T(2.6) - i * 0.2) / 0.2)
        if kk <= 0:
            continue
        al = int(255 * kk)
        cx, cy = W / 2 - 180 + i * 180, CY0 + 420
        d.ellipse((cx - 62, cy - 62, cx + 62, cy + 62), fill=AZUL_FCP + (al,), outline=CREME + (al,), width=4)
        d.text((cx, cy - 4), "DEF", font=fonte(SANS_SB, 40), fill=CREME + (al,), anchor="mm")
    k = suave((t - T(3.0)) / 0.25)
    if k > 0:
        d.text((W / 2, CY0 + 530), "Cláudio Ramos · 3 defesas", font=fonte(SANS_SB, 36),
               fill=CREME + (int(255 * k),), anchor="mm")
    k = (t - T(4.4)) / 0.4
    if k > 0:
        _parede(d, W / 2, CY0 + 600, min(1, k))
        kk = suave((t - T(4.7)) / 0.2)
        if kk > 0:
            d.text((W / 2, CY0 + 760), "uma parede", font=fonte(SERIFA_N, 58), fill=CREME + (int(255 * kk),),
                   anchor="mm")
    q.im.paste(ov, (0, 0), ov)


def golos_scp(v, q, t):
    ov = _ov(q)
    d = ImageDraw.Draw(ov)
    d.rectangle((0, CY0 + CH * 0.06, W, CY0 + CH * 0.90), fill=(20, 20, 19, 230))
    for txt, ti, y, cor in (("1 hora: 0 golos", T(1.0), CY0 + 140, (90, 86, 80)),
                            ("15 minutos: 4 golos", T(4.0), CY0 + 230, CORAL)):
        kk = suave((t - ti) / 0.25)
        if kk > 0:
            _chip(d, W / 2, y, txt, cor, kk, tam=40)
    golos = [("58'", "Rafael Nel", "grande penalidade", T(5.5)), ("61'", "Irankunda", "", T(6.7)),
             ("70'", "Catamo", "", T(6.0)), ("73'", "Irankunda", "bis", T(6.9))]
    for i, (m, nome, ex, ti) in enumerate(golos):
        kk = suave((t - ti) / 0.25)
        if kk <= 0:
            continue
        al = int(255 * kk)
        y = CY0 + 640 + i * 74
        d.rounded_rectangle((150, y - 32, W - 150, y + 32), radius=16, fill=(36, 34, 32, al))
        d.text((190, y), m, font=fonte(SANS_SB, 32), fill=CORAL + (al,), anchor="lm")
        d.text((300, y), nome, font=fonte(SERIFA_N, 40), fill=CREME + (al,), anchor="lm")
        if ex:
            d.text((W - 180, y), ex, font=fonte(SANS, 26), fill=CREME_70 + (al,), anchor="rm")
    q.im.paste(ov, (0, 0), ov)


def cartao_agente(v, q, t):
    _fundo(q, t)
    d = q.d
    if PFP.exists():
        k = suave((t - 0.05) / 0.3)
        r = int(90 * (0.85 + 0.15 * k))
        im = Image.open(PFP).convert("RGB").resize((2 * r, 2 * r), Image.LANCZOS)
        m = Image.new("L", (2 * r, 2 * r), 0)
        ImageDraw.Draw(m).ellipse((0, 0, 2 * r, 2 * r), fill=int(255 * k))
        q.im.paste(im, (int(W / 2 - r), int(CY0 + 100 - r)), m)
    linhas = [("Previsão · 97%", "Vitória do Sporting", T(1.0), T(1.6)),
              ("Previsão · 76%", "Vitória do Benfica", T(2.3), T(2.8)),
              ("Previsão · 72%", "Mais de 2,5 golos no Jamor", T(3.0), T(3.6))]
    for i, (cab, txt, ti, tv) in enumerate(linhas):
        kk = suave((t - ti) / 0.25)
        if kk <= 0:
            continue
        al = int(255 * kk)
        y = CY0 + 270 + i * 135
        d.rounded_rectangle((80, y - 56, W - 80, y + 56), radius=22, fill=(36, 34, 32, al),
                            outline=(70, 66, 60, al), width=2)
        d.text((190, y - 22), cab, font=fonte(SANS, 26), fill=CREME_70 + (al,), anchor="lm")
        d.text((190, y + 18), txt, font=fonte(SERIFA_N, 42), fill=CREME + (al,), anchor="lm")
        kv = suave((t - tv) / 0.2)
        if kv > 0:
            _visto(d, 135, y, kv, r=26)
    k = suave((t - T(4.2)) / 0.25)
    if k > 0:
        _chip(d, W / 2, CY0 + 690, "Previsões na rede vizinha · link na bio", CORAL, k, tam=34)


def pergunta(v, q, t):
    _fundo(q, t)
    d = q.d
    d.text((W / 2, CY0 + 170), "O herói da eliminatória?", font=fonte(SERIFA_N, 62), fill=CREME + (255,),
           anchor="mm")
    for i, (letra, l1, l2, ti, cor) in enumerate((("A", "Irankunda", "2 golos", T(1.2), VERDE_SCP),
                                                  ("B", "Cláudio Ramos", "3 defesas", T(1.9), AZUL_FCP))):
        kk = suave((t - ti) / 0.25)
        if kk <= 0:
            continue
        al = int(255 * kk)
        cx, cy = W / 2 + (-215 if i == 0 else 215), CY0 + 410
        d.rounded_rectangle((cx - 200, cy - 125, cx + 200, cy + 125), radius=28, fill=cor + (al,))
        d.text((cx, cy - 50), letra, font=fonte(SERIFA_N, 66), fill=CREME + (al,), anchor="mm")
        d.text((cx, cy + 25), l1, font=fonte(SANS_SB, 36), fill=CREME + (al,), anchor="mm")
        d.text((cx, cy + 72), l2, font=fonte(SANS, 28), fill=CREME + (al,), anchor="mm")
    k = suave((t - T(2.8)) / 0.25)
    if k > 0:
        d.text((W / 2, CY0 + 680), "Comenta A ou B", font=fonte(SANS_SB, 50), fill=CORAL + (int(255 * k),),
               anchor="mm")


# ------------------------------------------------------------------ cenas

REF_VOZ = [5.06, 3.92, 7.56, 5.57, 8.46, 9.99, 6.92, 3.58]


def construir():
    v = Video("Porto", "Paredes", abrev=("POR", "PAR"),
              fonte_txt="Ilustração · dados ESPN, Maisfutebol, ZeroZero, O Jogo e Agente Claudio")
    v.folga, v.bpm = 0.25, 120
    v.sp["fcp"] = sprite(17, AZUL_FCP, BRANCO, 3)
    v.sp["scp"] = sprite(17, VERDE_SCP, BRANCO, 3)
    v.sp["slb"] = sprite(17, VERMELHO, BRANCO, 3)
    v.sp["adv"] = sprite(17, BRANCO, (60, 60, 60), 3)
    cenas = []

    def cena(dur, titulo, i, jog, abrev=None, golos=None, **kw):
        voz, leg = FALAS[i]
        c = Cena(dur, titulo, "", jog, voz=voz, legenda=leg, voz_ini=VI, **kw)
        c.voz_ref = REF_VOZ[i]
        c.abrev = abrev
        if golos:
            c.golos = golos
            c.golo = golos[0]
        cenas.append(c)
        return c

    # 0. gancho: já visível no frame 0
    c = cena(5.5, "1/3 · Porto · Dragão", 0, vazio(), sobreposicao=gancho, nomes=False)
    c.t_capa = 5.3

    # 1. Porto 1–0: Sainz → André Silva → Fofana (vista do ataque)
    pos = {"a_d2": (0.40, 0.11), "a_d3": (0.58, 0.10), "a_d1": (0.22, 0.13), "a_d4": (0.78, 0.13),
           "a_m2": (0.42, 0.26), "a_m3": (0.60, 0.26), "g_a2": (0.55, 0.15), "g_a3": (0.80, 0.22),
           "g_m1": (0.36, 0.38), "g_m2": (0.50, 0.44), "g_d1": (0.12, 0.40), "g_d4": (0.88, 0.42),
           "g_a1": (0.22, 0.24)}
    mov = {"g_m3": vai((0.56, 0.32), (0.47, 0.22), T(0.4), T(1.4), 99),
           "a_gr": [(0, 0.5, 0.03), (T(1.9), 0.52, 0.03), (T(2.2), 0.46, 0.03), (99, 0.46, 0.03)]}
    bola = [(0, 0.22, 0.24), (T(0.2), 0.22, 0.24), (T(0.7), 0.55, 0.15), (T(0.9), 0.55, 0.15), (T(1.4), 0.47, 0.22),
            (T(1.7), 0.47, 0.22), (T(2.1), 0.45, 0.0)]
    cena(4.2, "1/3 · Porto · Dragão", 1, jogadores("fcp", pos, mov, {"g_a2": "André Silva", "g_m3": "Fofana"}),
         abrev=("POR", "PAR"), placar="0–0", minuto="41'", vista="ataque", golo=(T(2.15), "1–0", "Fofana"),
         bola=bola,
         formas=[{"tipo": "rotulo", "x": 0.74, "y": 0.34, "texto": "Fácil? Calma.", "cor": CORAL, "t0": T(2.7),
                  "t1": 4.2}],
         setas=[{"pts": [(0.22, 0.24), (0.55, 0.15)], "t0": T(0.2), "t1": T(0.7), "tipo": "passe"},
                {"pts": [(0.55, 0.15), (0.47, 0.22)], "t0": T(0.9), "t1": T(1.4), "tipo": "passe"},
                {"pts": [(0.47, 0.22), (0.45, 0.0)], "t0": T(1.7), "t1": T(2.1), "tipo": "remate"}],
         destaques=[("g_a2", T(0.6), T(1.4)), ("g_m3", T(1.5), 4.2)])

    # 2. 58': Cláudio Ramos defende, a bola sobra para Moura, autogolo (vista da defesa)
    pos = {"g_d1": (0.22, 0.86), "g_d3": (0.60, 0.88), "g_d4": (0.80, 0.85), "g_m1": (0.38, 0.78),
           "g_m2": (0.52, 0.74), "g_m3": (0.66, 0.76), "a_m1": (0.24, 0.78), "a_m4": (0.76, 0.80),
           "a_a2": (0.60, 0.84), "a_m3": (0.56, 0.68), "a_a1": (0.46, 0.86)}
    mov = {"g_gr": [(0, 0.5, 0.97), (T(0.4), 0.5, 0.97), (T(0.7), 0.53, 0.975), (99, 0.53, 0.975)],
           "g_d2": vai((0.40, 0.88), (0.47, 0.925), T(1.2), T(2.1), 99)}
    bola = [(0, 0.46, 0.86), (T(0.2), 0.46, 0.86), (T(0.7), 0.53, 0.975), (T(1.9), 0.47, 0.925), (T(3.8), 0.47, 0.925),
            (T(4.2), 0.505, 1.0)]
    cena(7.9, "1/3 · Porto · Dragão", 2, jogadores("fcp", pos, mov, {"g_gr": "Cláudio Ramos", "g_d2": "F. Moura"}),
         abrev=("POR", "PAR"), placar="1–0", minuto="58'", vista="defesa", golo=(T(4.25), "1–1", "Autogolo"),
         bola=bola,
         formas=[{"tipo": "rotulo", "x": 0.74, "y": 0.96, "texto": "defesa", "cor": CORAL, "t0": T(0.7),
                  "t1": T(1.9)},
                 {"tipo": "rotulo", "x": 0.26, "y": 0.95, "texto": "sozinho", "cor": BRANCO, "t0": T(2.9),
                  "t1": T(3.9)},
                 {"tipo": "rotulo", "x": 0.5, "y": 0.62, "texto": "saiu a chorar · o Dragão aplaudiu", "cor": CORAL,
                  "t0": T(5.2), "t1": 7.9}],
         setas=[{"pts": [(0.46, 0.86), (0.53, 0.975)], "t0": T(0.2), "t1": T(0.7), "tipo": "remate"},
                {"pts": [(0.47, 0.925), (0.505, 1.0)], "t0": T(3.8), "t1": T(4.2), "tipo": "remate"}],
         destaques=[("g_gr", T(0.1), T(1.2)), ("g_d2", T(2.2), T(4.8))])

    # 3. grandes penalidades: 3 defesas e a parede (paga o gancho)
    c = cena(5.9, "1/3 · Porto · Dragão", 3, vazio(), abrev=("POR", "PAR"), placar="1–1", minuto="120'",
             sobreposicao=penaltis, nomes=False)
    c.t_capa = 5.7

    # 4. Sporting: 1 hora sem golos, depois 4 em 15 minutos
    c = cena(8.8, "2/3 · Sporting · Alvalade", 4, vazio(), abrev=("SCP", "UDS"), placar="0–0", minuto="73'",
             golos=[(T(5.6), "1–0", "Rafael Nel"), (T(6.9), "4–0", "Irankunda")],
             sobreposicao=golos_scp, nomes=False)
    c.t_capa = 8.5

    # 5. Benfica: Durán, Drammeh, Prestianni, Kamiński (campo inteiro)
    pos = {"g_d4": (0.82, 0.66), "g_m1": (0.36, 0.56), "g_m3": (0.66, 0.54), "a_d1": (0.24, 0.12),
           "a_d4": (0.78, 0.16), "a_m1": (0.20, 0.40), "a_m4": (0.80, 0.42), "a_m2": (0.42, 0.50)}
    mov = {"g_d1": [(0, 0.14, 0.24), (T(1.3), 0.12, 0.20), (T(3.0), 0.18, 0.62), (99, 0.18, 0.66)],
           "g_a2": [(0, 0.52, 0.16), (T(2.0), 0.61, 0.07), (T(3.4), 0.50, 0.30), (99, 0.50, 0.30)],
           "g_m2": vai((0.46, 0.78), (0.48, 0.76), T(2.9), T(3.2), 99),
           "a_a1": vai((0.52, 0.72), (0.48, 0.77), T(2.9), T(3.2), 99),
           "a_a2": vai((0.60, 0.80), (0.56, 0.86), T(3.0), T(3.5), 99),
           "g_gr": [(0, 0.5, 0.95), (T(3.5), 0.5, 0.95), (T(3.8), 0.45, 0.955), (99, 0.45, 0.955)],
           "g_d2": vai((0.40, 0.84), (0.44, 0.86), T(3.0), T(3.5), 99),
           "g_d3": vai((0.60, 0.84), (0.62, 0.86), T(3.0), T(3.5), 99),
           "g_a3": vai((0.70, 0.30), (0.64, 0.20), T(3.6), T(4.2), 99),
           "g_a1": vai((0.30, 0.28), (0.40, 0.14), T(3.8), T(4.5), 99),
           "a_d2": vai((0.40, 0.10), (0.42, 0.12), T(3.8), T(4.4), 99),
           "a_d3": vai((0.58, 0.10), (0.62, 0.17), T(3.6), T(4.2), 99),
           "a_m3": vai((0.60, 0.30), (0.56, 0.20), T(4.9), T(5.3), 99),
           "a_gr": [(0, 0.5, 0.04), (T(2.4), 0.5, 0.04), (T(2.7), 0.46, 0.035), (T(4.7), 0.48, 0.035),
                    (T(4.95), 0.47, 0.035), (T(5.4), 0.47, 0.035), (T(5.65), 0.55, 0.04), (99, 0.55, 0.04)]}
    bola = [(0, 0.14, 0.22), (T(1.6), 0.12, 0.20), (T(2.3), 0.61, 0.07), (T(2.4), 0.61, 0.07), (T(2.7), 0.47, 0.0),
            (T(3.0), 0.50, 0.78), (T(3.2), 0.50, 0.78), (T(3.5), 0.56, 0.86), (T(3.6), 0.56, 0.86),
            (T(3.85), 0.47, 1.0), (T(4.2), 0.64, 0.20), (T(4.5), 0.40, 0.14), (T(4.7), 0.40, 0.14),
            (T(4.95), 0.445, 0.003), (T(5.1), 0.47, 0.0), (T(5.3), 0.57, 0.15), (T(5.65), 0.53, 0.0)]
    cena(10.5, "3/3 · Benfica · Jamor", 5,
         jogadores("slb", pos, mov, {"g_a2": "Durán", "a_a2": "Drammeh", "g_a1": "Prestianni"}),
         abrev=("TOR", "SLB"), placar="0–0", minuto="85'",
         golos=[(T(2.75), "0–1", "Jhon Durán", (0.47, 0.0)), (T(3.9), "1–1", "Drammeh", (0.47, 1.0)),
                (T(5.15), "1–2", "Prestianni", (0.47, 0.0)), (T(5.7), "1–3", "Kamiński", (0.53, 0.0))],
         bola=bola,
         formas=[{"tipo": "rotulo", "x": 0.5, "y": 0.42, "texto": "o dono da Taça", "cor": BRANCO, "t0": T(0.6),
                  "t1": T(1.8)},
                 {"tipo": "rotulo", "x": 0.26, "y": 0.06, "texto": "poste e golo", "cor": CORAL, "t0": T(5.0),
                  "t1": T(6.0)},
                 {"tipo": "rotulo", "x": 0.5, "y": 0.52, "texto": "próximo: Tondela", "cor": CORAL,
                  "t0": T(7.6), "t1": 10.5}],
         setas=[{"pts": [(0.12, 0.20), (0.61, 0.07)], "t0": T(1.6), "t1": T(2.3), "tipo": "passe"},
                {"pts": [(0.61, 0.07), (0.47, 0.0)], "t0": T(2.4), "t1": T(2.7), "tipo": "remate"},
                {"pts": [(0.56, 0.86), (0.47, 1.0)], "t0": T(3.6), "t1": T(3.85), "tipo": "remate"},
                {"pts": [(0.64, 0.20), (0.40, 0.14)], "t0": T(4.2), "t1": T(4.5), "tipo": "passe"},
                {"pts": [(0.40, 0.14), (0.445, 0.003)], "t0": T(4.7), "t1": T(4.95), "tipo": "remate"},
                {"pts": [(0.57, 0.15), (0.53, 0.0)], "t0": T(5.3), "t1": T(5.65), "tipo": "remate"}],
         destaques=[("g_a2", T(1.8), T(2.9)), ("a_a2", T(3.1), T(4.0)), ("g_a1", T(4.3), T(5.3))])

    c = cena(7.3, "", 6, vazio(), sobreposicao=cartao_agente, nomes=False)
    c.t_capa = 7.0
    c = cena(4.0, "", 7, vazio(), sobreposicao=pergunta, nomes=False)
    c.t_capa = 3.8
    cenas.append(cena_fecho(vazio(), frase=FECHO))
    return v, cenas


TIPO = "recap"
TEMA = "Os 3 grandes na Taça de Portugal (4.ª eliminatória): Porto nos penáltis, Sporting 4-0, Benfica no Jamor"
MATCH_ID = "20261120-TP-porto-paredes"
HORA = "19:30"
POSTS = {
    "tiktok": "O líder quase caiu contra a Liga 3... e quem o salvou foi uma parede 🧱 #futebol #fcporto #sporting #benfica #agenteclaudio",
    "instagram": "Porto nos penáltis, Sporting em 15 minutos, Benfica no Jamor. Os 3 grandes na Taça em 60 segundos 🧱⚽ #futebol #tacadeportugal #fcporto #sporting #benfica +18",
    "youtube": {"titulo": "Os 3 grandes na Taça: o Porto salvo por uma parede #shorts",
                "descricao": "Porto 1-1 Paredes (3-1 g.p.), Sporting 4-0 União da Serra, Torreense 1-3 Benfica. #tacadeportugal #futebol"},
    "x": "O líder da Liga quase caiu contra a Liga 3. Quem o salvou? Uma parede: Cláudio Ramos, 3 penáltis defendidos 🧱 #TaçaDePortugal",
}
