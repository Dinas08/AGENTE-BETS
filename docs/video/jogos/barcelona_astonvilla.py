"""Barcelona 3–0 Aston Villa (Liga dos Campeões, 3 nov 2026).

Factos (ESPN, relato e estatísticas do jogo): ambos em 4-2-3-1; 7' Lamine Yamal, pé esquerdo, do centro da área,
canto inferior esquerdo; 52' Raphinha, pé esquerdo, do centro da área, canto inferior direito, assistência de
Fermín López; 64' Raphinha, pé esquerdo, à boca da baliza, canto inferior esquerdo, assistência de João Cancelo.
Remates 16–9, à baliza 8–1, posse 65%–35%. O Agente Claudio deu 83% a mais de 2.5 golos.
As trajetórias são ilustrações coerentes com isto (o relato não dá a jogada inteira).
"""
from pathlib import Path

from PIL import Image, ImageDraw

from quadro_tatico import (CORAL, CREME, CREME_70, CY0, CH, VERDE, W, Cena, Video, fonte, P, suave,
                           SERIFA_N, SANS, SANS_SB)

# id: (nome, equipa, formação inicial, posição em ataque organizado)
JOG = {
    "garcia": ("J. García", "casa", (0.50, 0.95), (0.50, 0.90)),
    "farinas": ("Fariñas", "casa", (0.85, 0.80), (0.86, 0.50)),
    "cubarsi": ("Cubarsí", "casa", (0.62, 0.84), (0.62, 0.62)),
    "martin": ("G. Martín", "casa", (0.38, 0.84), (0.38, 0.62)),
    "cancelo": ("Cancelo", "casa", (0.15, 0.80), (0.14, 0.48)),
    "rodri": ("Rodri", "casa", (0.60, 0.70), (0.60, 0.50)),
    "pedri": ("Pedri", "casa", (0.40, 0.70), (0.38, 0.47)),
    "yamal": ("Yamal", "casa", (0.85, 0.60), (0.84, 0.34)),
    "fermin": ("Fermín", "casa", (0.50, 0.62), (0.46, 0.40)),
    "gordon": ("Gordon", "casa", (0.15, 0.60), (0.17, 0.30)),
    "raphinha": ("Raphinha", "casa", (0.50, 0.54), (0.50, 0.25)),
    "suzuki": ("Suzuki", "fora", (0.50, 0.05), (0.50, 0.025)),
    "cash": ("Cash", "fora", (0.15, 0.20), (0.17, 0.19)),
    "lindelof": ("Lindelöf", "fora", (0.38, 0.16), (0.40, 0.165)),
    "torres": ("P. Torres", "fora", (0.62, 0.16), (0.60, 0.165)),
    "maatsen": ("Maatsen", "fora", (0.85, 0.20), (0.83, 0.19)),
    "gomes": ("J. Gomes", "fora", (0.40, 0.30), (0.42, 0.29)),
    "kamara": ("Kamara", "fora", (0.60, 0.30), (0.60, 0.29)),
    "mcginn": ("McGinn", "fora", (0.15, 0.40), (0.22, 0.35)),
    "manzambi": ("Manzambi", "fora", (0.50, 0.38), (0.57, 0.41)),
    "buendia": ("Buendía", "fora", (0.85, 0.40), (0.78, 0.35)),
    "jackson": ("N. Jackson", "fora", (0.50, 0.46), (0.47, 0.53)),
}
# depois dos 62': Mbaye, Goretzka e Barkley entram por Buendía, Manzambi e João Gomes
SUBS_62 = {"buendia": "Mbaye", "manzambi": "Goretzka", "gomes": "Barkley"}


def jogadores(mov=None, mostrar=None, subs=None, fase="ataque"):
    """Todos em posição; mov = {id: [(t, x, y), ...]} sobrepõe trajetórias. mostrar = ids com nome visível."""
    out = {}
    for jid, (nome, eq, form, atq) in JOG.items():
        x, y = form if fase == "formacao" else atq
        nome = (subs or {}).get(jid, nome)
        out[jid] = {"nome": nome if (mostrar is None or jid in mostrar) else "", "equipa": eq,
                    "chaves": (mov or {}).get(jid, [(0, x, y)])}
    return out


def pos(jid):
    return JOG[jid][3]


# ------------------------------------------------------------------ sobreposições

def abertura(v, q, t):
    a = suave(t / 0.5)
    ov = Image.new("RGBA", (W, q.im.size[1]), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    d.rectangle((0, CY0 + CH * 0.30, W, CY0 + CH * 0.70), fill=(20, 20, 19, int(215 * a)))
    f1, f2 = fonte(SERIFA_N, 200), fonte(SANS_SB, 40)
    d.text((W / 2, CY0 + CH * 0.47), "3–0", font=f1, fill=CREME + (int(255 * a),), anchor="mm")
    d.text((W / 2, CY0 + CH * 0.60), "BARCELONA  ·  ASTON VILLA", font=f2, fill=CORAL + (int(255 * a),), anchor="mm")
    q.im.paste(ov, (0, 0), ov)


def numeros(v, q, t):
    ov = Image.new("RGBA", (W, q.im.size[1]), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    d.rectangle((0, CY0 - 10, W, CY0 + CH + 10), fill=(20, 20, 19, int(225 * suave(t / 0.4))))
    linhas = [("Remates", 16, 9), ("Remates à baliza", 8, 1), ("Posse de bola (%)", 65, 35), ("Cantos", 4, 8)]
    fn, fv = fonte(SANS_SB, 34), fonte(SERIFA_N, 64)
    d.text((W / 2, CY0 + 70), "BARCELONA        ASTON VILLA", font=fonte(SANS_SB, 28), fill=CREME_70 + (255,), anchor="mm")
    for i, (nome, a, b) in enumerate(linhas):
        k = suave((t - 0.3 - i * 0.35) / 0.6)
        if k <= 0:
            continue
        y = CY0 + 210 + i * 215
        d.text((W / 2, y - 60), nome.upper(), font=fn, fill=CREME_70 + (int(255 * k),), anchor="mm")
        d.text((150, y + 10), str(a), font=fv, fill=CREME + (int(255 * k),), anchor="lm")
        d.text((W - 150, y + 10), str(b), font=fv, fill=CREME + (int(255 * k),), anchor="rm")
        x0, x1 = 300, W - 300
        meio = x0 + (x1 - x0) * a / (a + b)
        d.rounded_rectangle((x0, y, x1, y + 22), radius=11, fill=(60, 57, 53, int(255 * k)))
        d.rounded_rectangle((x0, y, x0 + (meio - x0) * k, y + 22), radius=11, fill=CORAL + (int(255 * k),))
    q.im.paste(ov, (0, 0), ov)


PFP = Path(__file__).resolve().parents[2] / "imagens" / "pfp_agente_claudio.png"


def agente(v, q, t):
    ov = Image.new("RGBA", (W, q.im.size[1]), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    d.rectangle((0, CY0 - 10, W, CY0 + CH + 10), fill=(20, 20, 19, int(235 * suave(t / 0.4))))
    q.im.paste(ov, (0, 0), ov)
    if PFP.exists():
        k = suave((t - 0.2) / 0.5)
        r = int(170 * (0.8 + 0.2 * k))
        im = Image.open(PFP).convert("RGB").resize((2 * r, 2 * r), Image.LANCZOS)
        m = Image.new("L", (2 * r, 2 * r), 0)
        ImageDraw.Draw(m).ellipse((0, 0, 2 * r, 2 * r), fill=int(255 * k))
        q.im.paste(im, (int(W / 2 - r), int(CY0 + 200 - r)), m)
    d = q.d
    k = suave((t - 0.7) / 0.5)
    d.text((W / 2, CY0 + 430), "O Agente Claudio previa", font=fonte(SANS, 44), fill=CREME_70 + (int(255 * k),), anchor="mm")
    d.text((W / 2, CY0 + 515), "um jogo com 3+ golos", font=fonte(SERIFA_N, 72), fill=CREME + (int(255 * k),), anchor="mm")
    d.text((W / 2, CY0 + 600), "83% de probabilidade", font=fonte(SANS_SB, 40), fill=CORAL + (int(255 * k),), anchor="mm")
    k2 = suave((t - 1.6) / 0.4)
    if k2 > 0:
        cx, cy = W / 2 - 120, CY0 + 730
        d.ellipse((cx - 30, cy - 30, cx + 30, cy + 30), fill=VERDE + (int(255 * k2),))
        d.line([(cx - 13, cy + 1), (cx - 4, cy + 11), (cx + 14, cy - 10)], fill=(20, 20, 19, int(255 * k2)), width=7)
        d.text((cx + 50, cy), "Acertou: 3–0", font=fonte(SANS_SB, 46), fill=VERDE + (int(255 * k2),), anchor="lm")
    k3 = suave((t - 2.6) / 0.4)
    d.text((W / 2, CY0 + 880), "Segue para a próxima análise", font=fonte(SANS, 38),
           fill=CREME_70 + (int(255 * k3),), anchor="mm")


# ------------------------------------------------------------------ cenas

def construir():
    v = Video("Barcelona", "Aston Villa", abrev=("BAR", "AVL"),
              fonte_txt="Ilustração baseada no relato do jogo · dados ESPN")
    cenas = []
    # narração (números por extenso e nomes escritos como se dizem, para a voz ler bem)
    V = [
        "Barcelona três, Aston Vila zero. Vê como o Barça desmontou o Vila em três jogadas.",
        "Os dois em quatro, dois, três, um. Mas o Barça ficou com sessenta e cinco por cento da bola, "
        "e empurrou o Vila lá para trás.",
        "Minuto sete. Lamine Iamal pega na bola na direita, puxa para dentro, e remata de pé esquerdo, rasteiro, "
        "ao canto. Um a zero!",
        "Minuto cinquenta e dois. Fermín López vê a desmarcação de Rafinha nas costas dos centrais. "
        "Pé esquerdo, canto inferior direito. Dois a zero!",
        "Minuto sessenta e quatro. Cancelo sobe pela esquerda e serve Rafinha à boca da baliza. "
        "Bis do brasileiro, e jogo fechado.",
        "Nos números, domínio total. Dezasseis remates contra nove. Oito à baliza, contra apenas um.",
        "O Agente Claudio previa um jogo com três ou mais golos. E acertou. Segue, para a próxima análise.",
    ]

    # 1. gancho
    cenas.append(Cena(3.2, "Como o Barça desmontou o Villa", "3 golos, 3 ideias. Vê no quadro.",
                      jogadores(fase="formacao", mostrar=set()), placar="3–0", minuto="FIM", sobreposicao=abertura, voz=V[0], voz_ini=0.2,
                      nomes=False))

    # 2. os onzes: da formação para o ataque organizado
    mov = {jid: [(0.6, *JOG[jid][2]), (3.4, *JOG[jid][3])] for jid in JOG}
    cenas.append(Cena(5.5, "4-2-3-1 contra 4-2-3-1",
                      "O Barça ficou com 65% da bola e empurrou o Villa para um bloco baixo.",
                      jogadores(mov), placar="0–0", minuto="", destaques=[("raphinha", 3.4, 5.5)], voz=V[1]))

    # 3. golo 1 — 7' Yamal
    y0 = pos("yamal")
    mov = {
        "yamal": [(0, *y0), (0.4, *y0), (2.6, 0.70, 0.25), (3.3, 0.60, 0.205), (8, 0.60, 0.205)],
        "maatsen": [(0, *pos("maatsen")), (0.8, *pos("maatsen")), (3.2, 0.67, 0.215)],
        "torres": [(0, *pos("torres")), (2.4, *pos("torres")), (3.4, 0.57, 0.18)],
        "suzuki": [(0, *pos("suzuki")), (3.0, 0.50, 0.025), (3.8, 0.47, 0.02)],
        "buendia": [(0, *pos("buendia")), (3.4, 0.74, 0.30)],
        "raphinha": [(0, *pos("raphinha")), (3.0, 0.46, 0.20)],
    }
    bola = [(0, 0.82, 0.335), (0.4, 0.82, 0.335), (2.6, 0.685, 0.24), (3.3, 0.585, 0.195), (3.95, 0.455, 0.0)]
    cenas.append(Cena(7.5, "7' · Lamine Yamal",
                      "Pega na bola na direita, puxa para dentro e remata de pé esquerdo, rasteiro, ao canto.",
                      jogadores(mov, mostrar={"yamal", "maatsen"}),
                      bola=bola, placar="0–0", minuto="7'", vista="ataque", voz=V[2], voz_ini=0.1, golo=(4.0, "1–0"),
                      setas=[{"pts": [(0.82, 0.335), (0.70, 0.25), (0.60, 0.205)], "t0": 0.4, "t1": 3.2,
                              "tipo": "conducao"},
                             {"pts": [(0.585, 0.195), (0.455, 0.005)], "t0": 3.3, "t1": 3.9, "tipo": "remate"}],
                      destaques=[("yamal", 0, 4.2)]))

    # 4. golo 2 — 52' Raphinha, assistência de Fermín López
    mov = {
        "fermin": [(0, *pos("fermin")), (1.2, 0.48, 0.37)],
        "raphinha": [(0, 0.38, 0.27), (0.8, 0.38, 0.27), (2.5, 0.465, 0.14), (3.2, 0.47, 0.13)],
        "lindelof": [(0, *pos("lindelof")), (1.6, *pos("lindelof")), (2.8, 0.43, 0.15)],
        "torres": [(0, *pos("torres")), (2.0, 0.56, 0.16)],
        "kamara": [(0, *pos("kamara")), (2.0, 0.53, 0.33)],
        "suzuki": [(0, *pos("suzuki")), (2.6, 0.48, 0.03), (3.4, 0.52, 0.02)],
    }
    bola = [(0, 0.47, 0.375), (1.3, 0.47, 0.375), (2.4, 0.46, 0.15), (2.75, 0.462, 0.135), (3.35, 0.545, 0.0)]
    cenas.append(Cena(7.5, "52' · Raphinha",
                      "Fermín López vê a desmarcação nas costas dos centrais. Pé esquerdo, canto inferior direito.",
                      jogadores(mov, mostrar={"fermin", "raphinha"}),
                      bola=bola, placar="1–0", minuto="52'", vista="ataque", voz=V[3], voz_ini=0.1, golo=(3.45, "2–0"),
                      setas=[{"pts": [(0.38, 0.27), (0.465, 0.14)], "t0": 0.6, "t1": 2.4, "tipo": "corrida"},
                             {"pts": [(0.47, 0.375), (0.46, 0.155)], "t0": 1.3, "t1": 2.4, "tipo": "passe"},
                             {"pts": [(0.462, 0.135), (0.545, 0.005)], "t0": 2.75, "t1": 3.3, "tipo": "remate"}],
                      destaques=[("fermin", 0, 1.6), ("raphinha", 1.6, 3.8)]))

    # 5. golo 3 — 64' Raphinha, assistência de João Cancelo
    mov = {
        "pedri": [(0, *pos("pedri")), (1.0, 0.36, 0.44)],
        "cancelo": [(0, 0.14, 0.40), (0.5, 0.14, 0.40), (1.2, 0.13, 0.31), (2.6, 0.15, 0.13), (4, 0.16, 0.12)],
        "raphinha": [(0, *pos("raphinha")), (1.4, *pos("raphinha")), (3.3, 0.47, 0.065), (4, 0.47, 0.06)],
        "cash": [(0, *pos("cash")), (1.6, *pos("cash")), (2.8, 0.19, 0.12)],
        "lindelof": [(0, *pos("lindelof")), (2.6, 0.42, 0.10)],
        "suzuki": [(0, *pos("suzuki")), (2.7, 0.44, 0.025), (3.6, 0.50, 0.03)],
        "gordon": [(0, *pos("gordon")), (2.4, 0.30, 0.20)],
    }
    bola = [(0, 0.385, 0.455), (0.5, 0.385, 0.455), (1.2, 0.14, 0.32), (2.6, 0.16, 0.14), (3.3, 0.465, 0.07),
            (3.75, 0.455, 0.0)]
    cenas.append(Cena(7.5, "64' · Raphinha bis",
                      "Cancelo sobe pela esquerda e serve Raphinha à boca da baliza. Jogo fechado.",
                      jogadores(mov, mostrar={"cancelo", "raphinha", "pedri"}, subs=SUBS_62),
                      bola=bola, placar="2–0", minuto="64'", vista="ataque", voz=V[4], voz_ini=0.1, golo=(3.85, "3–0"),
                      setas=[{"pts": [(0.385, 0.455), (0.14, 0.32)], "t0": 0.5, "t1": 1.2, "tipo": "passe"},
                             {"pts": [(0.14, 0.32), (0.16, 0.14)], "t0": 1.2, "t1": 2.6, "tipo": "conducao"},
                             {"pts": [(0.50, 0.25), (0.47, 0.07)], "t0": 1.4, "t1": 3.3, "tipo": "corrida"},
                             {"pts": [(0.16, 0.14), (0.465, 0.07)], "t0": 2.6, "t1": 3.3, "tipo": "passe"},
                             {"pts": [(0.465, 0.07), (0.455, 0.005)], "t0": 3.3, "t1": 3.75, "tipo": "remate"}],
                      destaques=[("cancelo", 0.5, 2.8), ("raphinha", 2.8, 4.2)]))

    # 6. números
    cenas.append(Cena(5.5, "Os números", "Domínio do Barça do princípio ao fim.", jogadores(), placar="3–0",
                      minuto="FIM", sobreposicao=numeros, voz=V[5], nomes=False))

    # 7. Agente Claudio
    cenas.append(Cena(4.8, "", "", jogadores(), placar="3–0", minuto="FIM", sobreposicao=agente, voz=V[6], nomes=False))
    return v, cenas
