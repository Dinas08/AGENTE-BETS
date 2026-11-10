"""Análise tática: Benfica 3–1 Lech Poznań (Liga Europa, 5 nov 2026).

Fontes (verificadas a 6 nov 2026):
- ESPN: onzes (ambos 4-2-3-1), golos, substituições e estatísticas: remates 24–6, à baliza 11–5, posse 57%–43%,
  cruzamentos certos 1 em 19 (Benfica), 8 defesas de Mateusz Lis. 6' Rafa Silva na recarga a uma defesa de Lis;
  62' Prestianni, Barrenechea e Aursnes entram; 67' Prestianni, ângulo difícil na esquerda, assistência de Sudakov;
  71' Bengtsson entra e marca aos 72' (centro da área, alto); 90' Sudakov, da esquerda da área, assistência de
  Barrenechea num contra-ataque.
- RTP: Lech "mais recuado e concentrado em explorar o contra-ataque"; Rafa aproveitou "uma desatenção defensiva".
- O Jogo (vídeo do 2–1): "Trubin entrega a Barrenechea e o argentino oferece a bola ao adversário, com o
  guarda-redes fora da baliza."
- Sudakov (Sport TV, via O Jogo): "Mudei a minha posição, joguei a 8 na primeira parte."
- Agente Claudio: Benfica 88%, mais de 2,5 golos 80%, ambas marcam 57% (as três aconteceram).
As jogadas são ilustrações coerentes com isto.
"""
from PIL import Image, ImageDraw

from quadro_tatico import (FRASES_FECHO, cena_fecho, CORAL, CREME, CREME_70, CY0, CH, VERDE, AZUL, W, Cena,
                           Video, fonte, suave, SERIFA_N, SANS, SANS_SB)

import porto_napoli as base

vai, _ov, PFP, _visto = base.vai, base._ov, base.PFP, base._visto

# (voz, legenda). Voz: números por extenso e nomes escritos como se dizem.
FALAS = [
    ("Vinte e quatro remates contra seis. E mesmo assim, o Benfica só respirou ao minuto noventa. Porquê? "
     "Vê no quadro.",
     "24 remates contra 6. E mesmo assim, o Benfica só respirou ao minuto 90. Porquê? Vê no quadro."),
    ("O Lech veio recuado, à espera do contra-ataque. O Benfica teve a bola, encostou o Lech à área, e marcou "
     "cedo: o Lis defende, e o Rafa Silva faz a recarga.",
     "O Lech veio recuado, à espera do contra-ataque. O Benfica teve a bola, encostou o Lech à área e marcou "
     "cedo: Lis defende e Rafa Silva faz a recarga."),
    ("Pormenor curioso: o Sudákov jogou a oito na primeira parte, a sair de trás ao lado do Manu Silva, com o "
     "Etcheverri solto à frente. Foi ele que o contou no fim do jogo.",
     "Pormenor curioso: Sudakov jogou a 8 na primeira parte, a sair de trás ao lado do Manu Silva, com o "
     "Echeverri solto à frente. Foi ele que o contou no fim do jogo."),
    ("O problema? A finalização. Dezanove cruzamentos, e só um certo. E do outro lado, o Matéus Lis fez oito "
     "defesas.",
     "O problema? A finalização. 19 cruzamentos e só 1 certo. E do outro lado, Mateusz Lis fez 8 defesas."),
    ("Aos sessenta e dois, o Marco Silva mexeu três vezes de uma vez: Prestiâni, Barrenetchêa e Áursnes.",
     "Aos 62', Marco Silva mexeu três vezes de uma vez: Prestianni, Barrenechea e Aursnes."),
    ("Cinco minutos depois, o Sudákov encontra o Prestiâni na esquerda, e de ângulo difícil, dois a zero!",
     "5 minutos depois, Sudakov encontra Prestianni na esquerda e, de ângulo difícil, 2–0!"),
    ("Mas atenção à saída de bola. O Trubin entrega ao Barrenetchêa, que perde a bola dentro da área. O "
     "Bêngtsson, acabado de entrar, não perdoa. Dois a um.",
     "Mas atenção à saída de bola. Trubin entrega a Barrenechea, que perde a bola dentro da área. "
     "Bengtsson, acabado de entrar, não perdoa. 2–1."),
    ("E depois, a redenção: aos noventa, contra-ataque, e é o próprio Barrenetchêa a assistir o Sudákov. Três a "
     "um, e jogo fechado.",
     "E depois, a redenção: aos 90', contra-ataque, e é o próprio Barrenechea a assistir Sudakov. 3–1 e "
     "jogo fechado."),
    ("O Agente Claudio tinha vitória do Benfica, mais de dois golos e meio, e as duas a marcar. Acertou. E tu: "
     "o Barrenetchêa foi vilão, ou herói? Diz nos comentários.",
     "O Agente Claudio tinha vitória do Benfica, mais de 2,5 golos e ambas a marcar. Acertou. E tu: "
     "Barrenechea foi vilão ou herói? Diz nos comentários."),
]

# ------------------------------------------------------------------ jogadores
# id: (nome, equipa, posição na formação). O Benfica ataca para cima. Ambos em 4-2-3-1 (ESPN).
JOG = {
    "trubin": ("Trubin", "casa", (0.50, 0.95)),
    "elkarouani": ("El Karouani", "casa", (0.15, 0.79)),
    "araujo": ("T. Araújo", "casa", (0.38, 0.85)),
    "circati": ("Circati", "casa", (0.62, 0.85)),
    "banjaqui": ("Banjaqui", "casa", (0.85, 0.79)),
    "manu": ("Manu Silva", "casa", (0.40, 0.70)),
    "sudakov": ("Sudakov", "casa", (0.60, 0.70)),
    "echeverri": ("Echeverri", "casa", (0.50, 0.60)),
    "schjelderup": ("Schjelderup", "casa", (0.17, 0.58)),
    "rafa": ("Rafa Silva", "casa", (0.83, 0.58)),
    "duran": ("J. Durán", "casa", (0.50, 0.53)),
    "lis": ("Lis", "fora", (0.50, 0.05)),
    "pereira": ("J. Pereira", "fora", (0.15, 0.20)),
    "skrz": ("Skrzypczak", "fora", (0.38, 0.15)),
    "yegbe": ("Yegbe", "fora", (0.62, 0.15)),
    "gurgul": ("Gurgul", "fora", (0.85, 0.20)),
    "murawski": ("Murawski", "fora", (0.40, 0.30)),
    "kozubal": ("Kozubal", "fora", (0.60, 0.30)),
    "walemark": ("Wålemark", "fora", (0.15, 0.38)),
    "rodriguez": ("P. Rodríguez", "fora", (0.50, 0.39)),
    "hakans": ("Håkans", "fora", (0.85, 0.38)),
    "agnero": ("Agnero", "fora", (0.50, 0.46)),
}
SUBS_62 = {"rafa": "Prestianni", "manu": "Barrenechea", "echeverri": "Aursnes", "hakans": "Palma"}
SUBS_72 = dict(SUBS_62, araujo="Palhinha", rodriguez="Jagiełło", walemark="Bengtsson", kozubal="Berggren")
SUBS_90 = dict(SUBS_72, schjelderup="Lukébakio", pereira="Gumny")


def jogadores(pos, mov=None, mostrar=(), subs=None):
    out = {}
    for jid, (nome, eq, form) in JOG.items():
        x, y = pos.get(jid, form)
        out[jid] = {"nome": (subs or {}).get(jid, nome) if jid in mostrar else "", "equipa": eq,
                    "chaves": (mov or {}).get(jid, [(0, x, y)])}
    return out


# ------------------------------------------------------------------ sobreposições

def _fundo(q, t, alfa=238):
    ov = _ov(q)
    ImageDraw.Draw(ov).rectangle((0, CY0 - 10, W, CY0 + CH + 10), fill=(20, 20, 19, int(alfa * suave(t / 0.3))))
    q.im.paste(ov, (0, 0), ov)


def _chip(d, x, y, txt, cor, k, tam=40):
    f = fonte(SANS_SB, tam)
    lw = d.textlength(txt, font=f) + 64
    d.rounded_rectangle((x - lw / 2, y - tam * 0.85, x + lw / 2, y + tam * 0.85), radius=int(tam * 0.85),
                        fill=cor + (int(255 * k),))
    d.text((x, y), txt, font=f, fill=(20, 20, 19, int(255 * k)), anchor="mm")


def gancho(v, q, t):
    """Primeiro frame já cheio (capa): o 3–1 e o paradoxo dos 24 remates."""
    ov = _ov(q)
    d = ImageDraw.Draw(ov)
    d.rectangle((0, CY0 + CH * 0.16, W, CY0 + CH * 0.80), fill=(20, 20, 19, 228))
    esc = 1.1 - 0.1 * suave(t / 0.3)
    d.text((W / 2, CY0 + CH * 0.31), "3–1", font=fonte(SERIFA_N, 230 * esc), fill=CREME + (255,), anchor="mm")
    d.text((W / 2, CY0 + CH * 0.44), "BENFICA  ·  LECH", font=fonte(SANS_SB, 40), fill=CORAL + (255,), anchor="mm")
    k = suave((t - 0.2) / 0.35)
    if k > 0:
        d.text((W / 2, CY0 + CH * 0.54), "remates", font=fonte(SANS, 34), fill=CREME_70 + (int(255 * k),),
               anchor="mm")
        d.text((W / 2 - 140, CY0 + CH * 0.62), "24", font=fonte(SERIFA_N, 92), fill=CORAL + (int(255 * k),),
               anchor="mm")
        d.text((W / 2, CY0 + CH * 0.62), "vs", font=fonte(SANS, 34), fill=CREME_70 + (int(255 * k),), anchor="mm")
        d.text((W / 2 + 140, CY0 + CH * 0.62), "6", font=fonte(SERIFA_N, 92), fill=AZUL + (int(255 * k),),
               anchor="mm")
    k = suave((t - 5.1) / 0.3)
    if k > 0:
        _chip(d, W / 2, CY0 + CH * 0.73, "Só respirou ao 90'. Porquê?", CORAL, k)
    q.im.paste(ov, (0, 0), ov)


def contador(t_cruz, t_lis):
    """Cartão em baixo no campo: cruzamentos certos a contar até 1/19 e as defesas do Lis."""
    def sob(v, q, t):
        k = suave((t - t_cruz) / 0.3)
        if k <= 0:
            return
        ov = _ov(q)
        d = ImageDraw.Draw(ov)
        y0 = CY0 + 650
        d.rounded_rectangle((70, y0, W - 70, y0 + 200), radius=26, fill=(24, 23, 22, int(245 * k)),
                            outline=(70, 66, 60, int(255 * k)), width=2)
        n = min(19, int(19 * suave((t - t_cruz) / 1.4)) + 0)
        d.text((W / 4 + 20, y0 + 60), "CRUZAMENTOS CERTOS", font=fonte(SANS_SB, 26), fill=CREME_70 + (int(255 * k),),
               anchor="mm")
        d.text((W / 4 + 20, y0 + 130), f"1 / {max(1, n)}", font=fonte(SERIFA_N, 76), fill=CORAL + (int(255 * k),),
               anchor="mm")
        k2 = suave((t - t_lis) / 0.3)
        if k2 > 0:
            d.text((3 * W / 4 - 20, y0 + 60), "DEFESAS DO LIS", font=fonte(SANS_SB, 26),
                   fill=CREME_70 + (int(255 * k2),), anchor="mm")
            d.text((3 * W / 4 - 20, y0 + 130), "8", font=fonte(SERIFA_N, 76), fill=AZUL + (int(255 * k2),),
                   anchor="mm")
        q.im.paste(ov, (0, 0), ov)
    return sob


def tripla(v, q, t):
    _fundo(q, t)
    d = q.d
    k = suave((t - 0.1) / 0.35)
    d.text((W / 2, CY0 + 110), "62'", font=fonte(SERIFA_N, 130), fill=CREME + (int(255 * k),), anchor="mm")
    d.text((W / 2, CY0 + 220), "TRIPLA SUBSTITUIÇÃO", font=fonte(SANS_SB, 38), fill=CORAL + (int(255 * k),),
           anchor="mm")
    trocas = [("Rafa Silva", "Prestianni", 3.4), ("Manu Silva", "Barrenechea", 4.1), ("Echeverri", "Aursnes", 4.9)]
    for i, (sai, entra, ti) in enumerate(trocas):
        kk = suave((t - ti) / 0.3)
        if kk <= 0:
            continue
        y = CY0 + 360 + i * 130
        d.rounded_rectangle((110, y - 50, W - 110, y + 50), radius=24, fill=(44, 42, 39, int(255 * kk)))
        d.text((150, y), sai, font=fonte(SANS, 36), fill=CREME_70 + (int(255 * kk),), anchor="lm")
        d.text((W / 2 + 10, y), "→", font=fonte(SANS_SB, 40), fill=CORAL + (int(255 * kk),), anchor="mm")
        d.text((W - 150, y), entra, font=fonte(SANS_SB, 40), fill=CREME + (int(255 * kk),), anchor="rm")


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
    itens = [("Vitória do Benfica", 1.35), ("Mais de 2,5 golos", 2.45), ("Ambas marcam", 3.45)]
    for i, (txt, ti) in enumerate(itens):
        k = suave((t - ti) / 0.3)
        if k <= 0:
            continue
        y = CY0 + 270 + i * 82
        _visto(d, 330, y, k, r=24)
        d.text((372, y), txt, font=fonte(SANS_SB, 42), fill=CREME + (int(255 * k),), anchor="lm")
    k = suave((t - 5.1) / 0.3)
    d.text((W / 2, CY0 + 570), "Barrenechea foi…", font=fonte(SERIFA_N, 70), fill=CREME + (int(255 * k),),
           anchor="mm")
    for i, (letra, txt, ti) in enumerate((("A", "Vilão", 6.25), ("B", "Herói", 6.75))):
        kk = suave((t - 5.4 - i * 0.15) / 0.35)
        if kk <= 0:
            continue
        cx, cy = W / 2 + (-215 if i == 0 else 215), CY0 + 740
        ativo = ti <= t < ti + 0.6
        cor = CORAL if ativo else (44, 42, 39)
        d.rounded_rectangle((cx - 195, cy - 85, cx + 195, cy + 85), radius=28, fill=cor + (int(255 * kk),),
                            outline=(80, 76, 70, int(255 * kk)), width=2)
        d.text((cx, cy - 22), letra, font=fonte(SERIFA_N, 58), fill=CREME + (int(255 * kk),), anchor="mm")
        d.text((cx, cy + 40), txt, font=fonte(SANS_SB, 40), fill=CREME + (int(255 * kk),), anchor="mm")
    k = suave((t - 7.3) / 0.3)
    d.text((W / 2, CY0 + 900), "Comenta A ou B", font=fonte(SANS_SB, 46), fill=CORAL + (int(255 * k),), anchor="mm")


# ------------------------------------------------------------------ cenas

REF_VOZ = [7.13, 8.16, 8.27, 7.94, 5.85, 5.13, 7.59, 6.86, 8.79]


def construir():
    v = Video("Benfica", "Lech", abrev=("BEN", "LEC"), fonte_txt="Ilustração · dados ESPN, RTP e O Jogo")
    v.folga, v.bpm = 0.35, 112
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
    c = cena(7.6, "Benfica 3–1 Lech: a tática", 0, jogadores({}), placar="3–1", minuto="FIM",
             sobreposicao=gancho, nomes=False)
    c.t_capa = 5.8

    # 1. o Lech fecha-se, o Benfica encosta-o à área e marca cedo (vista de ataque)
    BLOCO = {"lis": (0.50, 0.03), "pereira": (0.16, 0.15), "skrz": (0.39, 0.13), "yegbe": (0.61, 0.13),
             "gurgul": (0.84, 0.15), "walemark": (0.16, 0.28), "murawski": (0.40, 0.27), "kozubal": (0.60, 0.27),
             "hakans": (0.84, 0.28), "rodriguez": (0.50, 0.35), "agnero": (0.50, 0.44)}
    ATQ = {"trubin": (0.50, 0.80), "araujo": (0.38, 0.58), "circati": (0.62, 0.58), "elkarouani": (0.08, 0.34),
           "banjaqui": (0.92, 0.34), "manu": (0.42, 0.48), "sudakov": (0.60, 0.46), "echeverri": (0.50, 0.33),
           "schjelderup": (0.24, 0.22), "rafa": (0.76, 0.22), "duran": (0.50, 0.19)}
    mov = {jid: vai(JOG[jid][2], p, T(0.3), T(2.3)) for jid, p in BLOCO.items()}
    mov.update({jid: vai(JOG[jid][2], p, T(2.6), T(4.6)) for jid, p in ATQ.items()})
    mov["rafa"] = [(0, *JOG["rafa"][2]), (T(2.6), *JOG["rafa"][2]), (T(4.6), 0.76, 0.22), (T(5.4), 0.60, 0.10),
                   (T(6.2), 0.57, 0.07), (99, 0.57, 0.07)]
    mov["lis"] = [(0, 0.5, 0.05), (T(2.3), 0.5, 0.03), (T(5.7), 0.51, 0.03), (T(6.6), 0.46, 0.025)]
    bola = [(0, 0.5, 0.50), (T(4.6), 0.50, 0.335), (T(4.9), 0.50, 0.335), (T(5.4), 0.60, 0.105),
            (T(5.8), 0.51, 0.03), (T(6.2), 0.57, 0.075), (T(6.6), 0.545, 0.0)]
    defesa, meio = ["pereira", "skrz", "yegbe", "gurgul"], ["walemark", "murawski", "kozubal", "hakans"]
    cena(8.6, "O plano do Lech", 1, jogadores({}, mov, mostrar={"rafa", "lis", "echeverri"}),
         bola=bola, placar="0–0", minuto="6'", vista="ataque", golo=(T(6.65), "1–0", "Rafa Silva"),
         formas=[{"tipo": "zona", "pts": [(0.03, 0.07), (0.97, 0.07), (0.97, 0.32), (0.03, 0.32)], "cor": AZUL,
                  "rotulo": "bloco recuado", "t0": T(0.5), "t1": T(2.6)},
                 {"tipo": "linha", "ids": defesa, "cor": AZUL, "t0": T(0.5), "t1": T(5.6)},
                 {"tipo": "linha", "ids": meio, "cor": AZUL, "t0": T(0.5), "t1": T(5.6)}],
         setas=[{"pts": [(0.50, 0.335), (0.60, 0.105)], "t0": T(4.9), "t1": T(5.4), "tipo": "passe"},
                {"pts": [(0.60, 0.105), (0.51, 0.035)], "t0": T(5.4), "t1": T(5.8), "tipo": "remate"},
                {"pts": [(0.57, 0.075), (0.545, 0.005)], "t0": T(6.2), "t1": T(6.6), "tipo": "remate"}],
         destaques=[("lis", T(5.6), T(6.1)), ("rafa", T(6.1), 8.6)])

    # 2. Sudakov a 8 ao lado do Manu Silva; Echeverri solto entre linhas
    LECH2 = {"lis": (0.5, 0.04), "pereira": (0.18, 0.24), "skrz": (0.38, 0.22), "yegbe": (0.62, 0.22),
             "gurgul": (0.82, 0.24), "walemark": (0.20, 0.42), "murawski": (0.40, 0.43), "kozubal": (0.60, 0.43),
             "hakans": (0.80, 0.42), "rodriguez": (0.50, 0.50), "agnero": (0.50, 0.58)}
    BEN2 = {"trubin": (0.5, 0.93), "araujo": (0.36, 0.73), "circati": (0.64, 0.73), "manu": (0.44, 0.62),
            "elkarouani": (0.12, 0.52), "banjaqui": (0.88, 0.52), "schjelderup": (0.18, 0.31),
            "rafa": (0.82, 0.31), "duran": (0.50, 0.26), "echeverri": (0.50, 0.40), "sudakov": (0.64, 0.50)}
    pos2 = dict(LECH2, **BEN2)
    mov = {"sudakov": vai((0.64, 0.50), (0.57, 0.63), T(1.0), T(2.6)),
           "echeverri": vai((0.50, 0.40), (0.52, 0.33), T(4.4), T(5.4))}
    bola = [(0, 0.36, 0.72), (T(2.7), 0.36, 0.72), (T(3.2), 0.565, 0.625), (T(4.8), 0.565, 0.625),
            (T(5.5), 0.52, 0.34)]
    cena(8.8, "Sudakov a 8", 2, jogadores(pos2, mov, mostrar={"sudakov", "manu", "echeverri", "araujo"}),
         bola=bola, placar="1–0", minuto="", formas=[
             {"tipo": "rotulo", "x": 0.70, "y": 0.70, "texto": "Sudakov a 8", "cor": CORAL, "t0": T(1.2),
              "t1": T(4.4)},
             {"tipo": "linha", "ids": ["pereira", "skrz", "yegbe", "gurgul"], "cor": AZUL, "t0": T(4.3), "t1": 8.8},
             {"tipo": "linha", "ids": ["walemark", "murawski", "kozubal", "hakans"], "cor": AZUL, "t0": T(4.3),
              "t1": 8.8},
             {"tipo": "entre", "de": ["pereira", "skrz", "yegbe", "gurgul"],
              "ate": ["walemark", "murawski", "kozubal", "hakans"], "cor": CORAL, "rotulo": "Echeverri solto",
              "t0": T(4.6), "t1": 8.8}],
         setas=[{"pts": [(0.64, 0.50), (0.57, 0.63)], "t0": T(1.0), "t1": T(2.6), "tipo": "corrida"},
                {"pts": [(0.36, 0.72), (0.565, 0.625)], "t0": T(2.7), "t1": T(3.2), "tipo": "passe"},
                {"pts": [(0.565, 0.625), (0.52, 0.34)], "t0": T(4.8), "t1": T(5.5), "tipo": "passe"}],
         destaques=[("sudakov", T(0.8), T(4.4)), ("echeverri", T(4.6), 8.8)])

    # 3. o problema: 1 cruzamento certo em 19, e 8 defesas do Lis
    pos3 = dict(BLOCO, **ATQ)
    alvos = [(0.45, 0.12), (0.58, 0.11), (0.40, 0.13), (0.55, 0.09), (0.62, 0.13), (0.47, 0.10)]
    setas = []
    for i, alvo in enumerate(alvos):
        ori = (0.08, 0.20) if i % 2 == 0 else (0.92, 0.20)
        t0 = T(2.0) + i * 0.32
        setas.append({"pts": [ori, alvo], "t0": t0, "t1": t0 + 0.4, "tipo": "passe"})
    cena(8.4, "O problema", 3, jogadores(pos3, {}, mostrar={"lis"}), placar="1–0", minuto="",
         vista="ataque", setas=setas, sobreposicao=contador(T(2.1), T(5.5)),
         destaques=[("lis", T(5.4), 8.4)])

    # 4. tripla substituição (62')
    cena(6.3, "O banco", 4, jogadores({}), placar="1–0", minuto="62'", sobreposicao=tripla, nomes=False)

    # 5. 67' Prestianni, de ângulo difícil na esquerda, assistência de Sudakov
    pos5 = dict(BLOCO, **ATQ)
    pos5.update({"sudakov": (0.40, 0.24), "rafa": (0.18, 0.21), "echeverri": (0.55, 0.30)})
    mov = {"rafa": [(0, 0.18, 0.21), (T(1.4), 0.18, 0.20), (T(2.5), 0.20, 0.09), (T(3.3), 0.24, 0.055),
                    (99, 0.24, 0.055)],
           "pereira": vai((0.16, 0.15), (0.21, 0.08), T(2.0), T(3.3)),
           "lis": [(0, 0.50, 0.03), (T(3.2), 0.42, 0.03), (T(3.9), 0.47, 0.02)]}
    bola = [(0, 0.40, 0.235), (T(1.9), 0.40, 0.235), (T(2.5), 0.205, 0.095), (T(3.3), 0.245, 0.06),
            (T(3.5), 0.245, 0.06), (T(3.9), 0.50, 0.0)]
    cena(5.8, "67' · ângulo difícil", 5,
         jogadores(pos5, mov, mostrar={"rafa", "sudakov", "lis"}, subs=SUBS_62),
         bola=bola, placar="1–0", minuto="67'", vista="ataque", golo=(T(3.95), "2–0", "Prestianni"),
         setas=[{"pts": [(0.40, 0.235), (0.205, 0.095)], "t0": T(1.9), "t1": T(2.5), "tipo": "passe"},
                {"pts": [(0.205, 0.095), (0.245, 0.06)], "t0": T(2.5), "t1": T(3.3), "tipo": "conducao"},
                {"pts": [(0.245, 0.06), (0.50, 0.005)], "t0": T(3.5), "t1": T(3.9), "tipo": "remate"}],
         destaques=[("sudakov", T(1.0), T(2.0)), ("rafa", T(2.0), 5.8)])

    # 6. 72': a saída de bola. Trubin entrega a Barrenechea, que perde a bola na área; Bengtsson marca
    pos6 = {"circati": (0.64, 0.91), "araujo": (0.30, 0.90), "elkarouani": (0.12, 0.78), "banjaqui": (0.88, 0.78),
            "sudakov": (0.62, 0.72), "echeverri": (0.42, 0.70), "schjelderup": (0.20, 0.62), "rafa": (0.80, 0.62),
            "duran": (0.50, 0.55), "agnero": (0.66, 0.83), "rodriguez": (0.40, 0.76), "hakans": (0.80, 0.70),
            "kozubal": (0.55, 0.64), "murawski": (0.30, 0.62), "gurgul": (0.85, 0.55), "pereira": (0.15, 0.55),
            "yegbe": (0.60, 0.48), "skrz": (0.40, 0.48), "lis": (0.5, 0.05)}
    mov = {"trubin": [(0, 0.50, 0.975), (T(1.4), 0.50, 0.965), (T(2.2), 0.44, 0.94), (T(4.6), 0.43, 0.94),
                      (T(5.0), 0.47, 0.96)],
           "manu": [(0, 0.38, 0.88), (T(2.2), 0.37, 0.885), (T(3.4), 0.39, 0.88), (99, 0.39, 0.88)],
           "walemark": [(0, 0.52, 0.80), (T(2.2), 0.50, 0.82), (T(3.4), 0.42, 0.875), (T(4.6), 0.47, 0.875),
                        (99, 0.47, 0.875)]}
    bola = [(0, 0.50, 0.97), (T(1.6), 0.50, 0.965), (T(2.3), 0.375, 0.89), (T(3.1), 0.38, 0.89),
            (T(3.5), 0.42, 0.875), (T(4.5), 0.465, 0.875), (T(4.65), 0.465, 0.875), (T(5.0), 0.50, 1.0)]
    cena(8.3, "72' · a saída de bola", 6,
         jogadores(pos6, mov, mostrar={"trubin", "manu", "walemark"}, subs=SUBS_72),
         bola=bola, placar="2–0", minuto="72'", vista="defesa", golo=(T(5.05), "2–1", "Bengtsson"),
         formas=[{"tipo": "rotulo", "x": 0.5, "y": 0.66, "texto": "saída arriscada", "cor": CORAL, "t0": T(0.4),
                  "t1": T(2.6)},
                 {"tipo": "rotulo", "x": 0.30, "y": 0.80, "texto": "bola perdida", "cor": AZUL, "t0": T(3.3),
                  "t1": T(4.6)}],
         setas=[{"pts": [(0.50, 0.965), (0.375, 0.89)], "t0": T(1.6), "t1": T(2.3), "tipo": "passe"},
                {"pts": [(0.52, 0.80), (0.42, 0.875)], "t0": T(2.2), "t1": T(3.4), "tipo": "corrida_fora"},
                {"pts": [(0.465, 0.875), (0.50, 0.995)], "t0": T(4.65), "t1": T(5.0), "tipo": "remate"}],
         destaques=[("trubin", T(1.3), T(2.2)), ("manu", T(2.2), T(3.4)), ("walemark", T(3.4), 8.3)])

    # 7. 90': a redenção. Contra-ataque, Barrenechea assiste Sudakov
    pos7 = {"trubin": (0.5, 0.95), "circati": (0.62, 0.84), "araujo": (0.38, 0.84), "elkarouani": (0.15, 0.76),
            "banjaqui": (0.85, 0.76), "echeverri": (0.58, 0.68), "schjelderup": (0.20, 0.56), "duran": (0.52, 0.50),
            "agnero": (0.50, 0.80), "rodriguez": (0.40, 0.74), "hakans": (0.80, 0.70), "kozubal": (0.60, 0.70),
            "murawski": (0.30, 0.68), "walemark": (0.66, 0.78), "gurgul": (0.85, 0.52), "skrz": (0.38, 0.40),
            "lis": (0.5, 0.04)}
    mov = {"manu": [(0, 0.46, 0.72), (T(1.6), 0.47, 0.72), (T(3.4), 0.46, 0.46), (99, 0.46, 0.46)],
           "sudakov": [(0, 0.34, 0.62), (T(1.8), 0.33, 0.60), (T(4.2), 0.30, 0.15), (99, 0.30, 0.15)],
           "rafa": vai((0.70, 0.60), (0.64, 0.20), T(1.8), T(4.4), 99),
           "yegbe": vai((0.58, 0.40), (0.45, 0.17), T(1.8), T(4.4), 99),
           "pereira": vai((0.25, 0.42), (0.34, 0.20), T(1.8), T(4.4), 99),
           "lis": [(0, 0.5, 0.04), (T(4.3), 0.47, 0.04), (T(4.85), 0.53, 0.025)]}
    bola = [(0, 0.48, 0.74), (T(1.6), 0.47, 0.735), (T(3.4), 0.46, 0.47), (T(3.5), 0.46, 0.47),
            (T(4.2), 0.305, 0.16), (T(4.4), 0.305, 0.16), (T(4.8), 0.545, 0.0)]
    cena(7.4, "90' · a redenção", 7,
         jogadores(pos7, mov, mostrar={"manu", "sudakov"}, subs=SUBS_90),
         bola=bola, placar="2–1", minuto="90'", golo=(T(4.85), "3–1", "Sudakov"),
         setas=[{"pts": [(0.47, 0.735), (0.46, 0.47)], "t0": T(1.6), "t1": T(3.4), "tipo": "conducao"},
                {"pts": [(0.33, 0.60), (0.30, 0.15)], "t0": T(1.8), "t1": T(4.2), "tipo": "corrida"},
                {"pts": [(0.46, 0.47), (0.305, 0.16)], "t0": T(3.5), "t1": T(4.2), "tipo": "passe"},
                {"pts": [(0.305, 0.16), (0.545, 0.005)], "t0": T(4.4), "t1": T(4.8), "tipo": "remate"}],
         destaques=[("manu", T(1.4), T(4.0)), ("sudakov", T(4.0), 7.4)])

    # 8. Agente Claudio + pergunta
    c = cena(9.3, "", 8, jogadores({}), placar="3–1", minuto="FIM", sobreposicao=cartao_agente, nomes=False)
    c.t_capa = 7.6
    # 9. fecho com humor
    cenas.append(cena_fecho(jogadores({}), placar="3–1", frase=1))
    return v, cenas
