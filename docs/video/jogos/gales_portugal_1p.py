"""País de Gales 2–2 Portugal, 1.ª parte (Liga das Nações, Cardiff, 17 nov 2026). Feito ao intervalo.

Fontes (verificadas a 17 nov 2026, ao intervalo):
- ESPN (summary 401861189): Gales 4-4-2 (Ward; Roberts, Rodon, Ben Davies, Da Silva; James, Sheehan, Colwill,
  Sorba Thomas; Brooks, Wilson); Portugal 4-2-3-1 (Diogo Costa; Cancelo, António Silva, Renato Veiga, Dalot;
  Vitinha, João Neves; Neto, Bruno, Trincão; Gonçalo Ramos). Golos: 11' Bruno (fora da área, assist. João Neves),
  13' Brooks (assist. Colwill, logo após defesa de Costa a Wilson), 40' Sorba Thomas (assist. Brooks), 43' Neto
  (muito perto da baliza, cruzamento de Trincão). Posse 69–31, passes 387–155, remates 6–10, à baliza 4–5.
- Observador (liveblog): 1–0 nasce de "recuperação de bola de João Neves em zona adiantada", Bruno remata "mais em
  jeito do que em força"; 2–1: "transição rápida brutal", com Portugal "ainda a recuperar de um ataque"; Neto
  desvia de primeira ao segundo poste; Portugal só precisa de um ponto para o 1.º lugar.
- DN: quatro mudanças (saem Rúben Dias, Alberto Costa, Félix e Rúben Neves; entram António Silva, Cancelo,
  Trincão e João Neves); o 2–1 "numa jogada de contra-ataque". VAVEL: Bellamy é o selecionador de Gales.
- Agente Claudio (ramo claude/dados): previsão de mais de 2,5 golos (66%, já certa ao intervalo); dica do canal
  "Vitória Portugal" (por decidir na 2.ª parte).
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
    ("Sessenta e nove por cento de posse para Portugal. E quem rematou mais? O País de Gales: dez contra seis. Ao "
     "intervalo, em Cardiff, está dois a dois.",
     "69% de posse para Portugal. E quem rematou mais? O País de Gales: 10 contra 6. Ao intervalo, em Cardiff, "
     "está 2–2."),
    ("Sem o Rúben Dias e o Palhinha, castigados, o JJ pôs o António Silva ao lado do Renato Veiga. E o Gales do "
     "Bélami fecha-se num quatro, quatro, dois, à espera do erro.",
     "Sem o Rúben Dias e o Palhinha, castigados, o JJ pôs o António Silva ao lado do Renato Veiga. E o Gales do "
     "Bellamy fecha-se num 4-4-2, à espera do erro."),
    ("Aos onze minutos, o João Neves rouba a bola lá à frente, e o Bruno, à entrada da área, coloca em jeito.",
     "Aos 11 minutos, o João Neves rouba a bola lá à frente e o Bruno, à entrada da área, coloca em jeito."),
    ("Mas dois minutos depois, o Diogo Costa defende o remate do Uílson, a recarga sobra, e o Brúks empata.",
     "Mas dois minutos depois, o Diogo Costa defende o remate do Wilson, a recarga sobra e o Brooks empata."),
    ("Aos quarenta, o lance que explica tudo: Portugal ainda está a recuperar de um ataque, o Gales sai em "
     "transição, o Brúks solta para o Sórba Tómas, e é dois a um.",
     "Aos 40', o lance que explica tudo: Portugal ainda está a recuperar de um ataque, o Gales sai em transição, o "
     "Brooks solta para o Sorba Thomas e é 2–1."),
    ("Portugal responde logo: o Trincão cruza da esquerda, e o Pedro Neto desvia de primeira, ao segundo poste.",
     "Portugal responde logo: o Trincão cruza da esquerda e o Pedro Neto desvia de primeira, ao segundo poste."),
    ("E o Agente Claudio? A previsão de mais de dois golos e meio já entrou ao intervalo. A dica foi vitória de "
     "Portugal: falta a segunda parte. As dicas estão na rede vizinha, link na bio.",
     "E o Agente Claudio? A previsão de mais de 2,5 golos já entrou ao intervalo. A dica foi vitória de Portugal: "
     "falta a segunda parte. As dicas estão na rede vizinha, link na bio."),
    ("E tu? Quem ganha a segunda parte: Portugal, com a bola, ou o Gales, no contra-ataque? Diz nos comentários.",
     "E tu? Quem ganha a segunda parte: Portugal, com a bola, ou o Gales, no contra-ataque? Diz nos comentários."),
]


# ------------------------------------------------------------------ jogadores (Portugal ataca para cima)
JOG = {
    "costa": ("Diogo Costa", "casa", (0.50, 0.95)),
    "dalot": ("Dalot", "casa", (0.15, 0.79)),
    "veiga": ("Renato Veiga", "casa", (0.38, 0.85)),
    "asilva": ("António Silva", "casa", (0.62, 0.85)),
    "cancelo": ("Cancelo", "casa", (0.85, 0.79)),
    "jneves": ("João Neves", "casa", (0.40, 0.70)),
    "vitinha": ("Vitinha", "casa", (0.60, 0.70)),
    "bruno": ("Bruno", "casa", (0.50, 0.60)),
    "trincao": ("Trincão", "casa", (0.17, 0.58)),
    "neto": ("Pedro Neto", "casa", (0.83, 0.58)),
    "ramos": ("Gonçalo Ramos", "casa", (0.50, 0.53)),
    "ward": ("Ward", "fora", (0.50, 0.04)),
    "roberts": ("Roberts", "fora", (0.15, 0.18)),
    "rodon": ("Rodon", "fora", (0.38, 0.14)),
    "davies": ("Ben Davies", "fora", (0.62, 0.14)),
    "dasilva": ("Da Silva", "fora", (0.85, 0.18)),
    "james": ("James", "fora", (0.15, 0.32)),
    "sheehan": ("Sheehan", "fora", (0.40, 0.30)),
    "colwill": ("Colwill", "fora", (0.60, 0.30)),
    "thomas": ("Sorba Thomas", "fora", (0.85, 0.32)),
    "brooks": ("Brooks", "fora", (0.42, 0.44)),
    "wilson": ("Wilson", "fora", (0.58, 0.44)),
}
VERMELHO = (200, 40, 50)
VERMELHO_GAL = (196, 30, 45)
VERDE_PT = (40, 140, 80)
BRANCO = (236, 234, 226)
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
    d.rectangle((0, CY0 + CH * 0.10, W, CY0 + CH * 0.86), fill=(20, 20, 19, 232))
    k = suave((t - 0.05) / 0.3)
    d.text((W / 2, CY0 + CH * 0.10 + 55), "INTERVALO  ·  CARDIFF", font=fonte(SANS_SB, 34), fill=CORAL + (255,),
           anchor="mm")
    linhas = [("Posse", 69, 31, T(0.1), "%"), ("Passes", 387, 155, T(0.9), ""), ("Remates", 6, 10, T(2.2), ""),
              ("À baliza", 4, 5, T(4.6), "")]
    for i, (nome, a, b, ti, suf) in enumerate(linhas):
        kk = suave((t - ti) / 0.35)
        if kk <= 0:
            continue
        y = CY0 + 260 + i * 115
        d.text((W / 2, y - 36), nome, font=fonte(SANS, 30), fill=CREME_70 + (int(255 * kk),), anchor="mm")
        x0, x1 = 270, W - 270
        tot = a + b
        xm = x0 + (x1 - x0) * a / tot
        d.rounded_rectangle((x0, y - 12, x1, y + 12), radius=12, fill=(50, 48, 45, int(255 * kk)))
        d.rounded_rectangle((x0, y - 12, x0 + (xm - x0) * kk, y + 12), radius=12, fill=VERMELHO + (int(255 * kk),))
        d.rounded_rectangle((x1 - (x1 - xm) * kk, y - 12, x1, y + 12), radius=12, fill=CREME + (int(255 * kk),))
        destaque = i >= 2
        d.text((x0 - 30, y), f"{a}{suf}", font=fonte(SERIFA_N, 50), fill=CREME + (int(255 * kk),), anchor="rm")
        d.text((x1 + 30, y), f"{b}{suf}", font=fonte(SERIFA_N, 50),
               fill=(CORAL if destaque else CREME) + (int(255 * kk),), anchor="lm")
        if i == 0:
            d.text((x0 - 30, y - 50), "POR", font=fonte(SANS_SB, 26), fill=CREME_70 + (int(255 * kk),), anchor="rm")
            d.text((x1 + 30, y - 50), "GAL", font=fonte(SANS_SB, 26), fill=CREME_70 + (int(255 * kk),), anchor="lm")
    k = suave((t - T(6.9)) / 0.3)
    if k > 0:
        esc = 1.1 - 0.1 * k
        d.text((W / 2, CY0 + CH * 0.74), "2–2", font=fonte(SERIFA_N, int(150 * esc)), fill=CREME + (int(255 * k),),
               anchor="mm")
    q.im.paste(ov, (0, 0), ov)


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
    linhas = [("A previsão · 66%", "Mais de 2,5 golos", T(1.2), T(2.8), True),
              ("A dica", "Vitória de Portugal", T(3.9), T(5.5), False)]
    for i, (cab, txt, ti, tv, certo) in enumerate(linhas):
        kk = suave((t - ti) / 0.3)
        if kk <= 0:
            continue
        y = CY0 + 300 + i * 160
        d.rounded_rectangle((80, y - 64, W - 80, y + 64), radius=24, fill=(36, 34, 32, int(255 * kk)),
                            outline=(70, 66, 60, int(255 * kk)), width=2)
        d.text((190, y - 26), cab, font=fonte(SANS, 28), fill=CREME_70 + (int(255 * kk),), anchor="lm")
        d.text((190, y + 20), txt, font=fonte(SERIFA_N, 48), fill=CREME + (int(255 * kk),), anchor="lm")
        kv = suave((t - tv) / 0.25)
        if kv > 0:
            if certo:
                _visto(d, 135, y, kv, r=28)
            else:
                f = fonte(SANS_SB, 26)
                txt2 = "2.ª parte"
                lw = d.textlength(txt2, font=f) + 36
                d.rounded_rectangle((W - 110 - lw, y - 24, W - 110, y + 24), radius=24,
                                    fill=(90, 86, 80, int(255 * kv)))
                d.text((W - 110 - lw / 2, y), txt2, font=f, fill=CREME + (int(255 * kv),), anchor="mm")
                d.ellipse((135 - 26, y - 26, 135 + 26, y + 26), outline=CREME_70 + (int(255 * kv),), width=3)
                d.text((135, y), "…", font=fonte(SANS_SB, 30), fill=CREME_70 + (int(255 * kv),), anchor="mm")
    k = suave((t - T(6.7)) / 0.3)
    if k > 0:
        _chip(d, W / 2, CY0 + 640, "Dicas na rede vizinha · link na bio", CORAL, k, tam=36)


def pergunta(v, q, t):
    _fundo(q, t)
    d = q.d
    k = suave((t - 0.1) / 0.35)
    if k > 0:
        d.text((W / 2, CY0 + 170), "Quem ganha a 2.ª parte?", font=fonte(SERIFA_N, 66), fill=CREME + (int(255 * k),),
               anchor="mm")
    for i, (letra, l1, l2, ti, cor) in enumerate((("A", "Portugal,", "com a bola", T(1.6), VERMELHO),
                                                  ("B", "o Gales, no", "contra-ataque", T(2.6), BRANCO))):
        kk = suave((t - ti) / 0.35)
        if kk <= 0:
            continue
        cx, cy = W / 2 + (-215 if i == 0 else 215), CY0 + 410
        d.rounded_rectangle((cx - 200, cy - 125, cx + 200, cy + 125), radius=28, fill=cor + (int(255 * kk),))
        tc = CREME if i == 0 else (20, 20, 19)
        d.text((cx, cy - 50), letra, font=fonte(SERIFA_N, 66), fill=tc + (int(255 * kk),), anchor="mm")
        d.text((cx, cy + 25), l1, font=fonte(SANS_SB, 34), fill=tc + (int(255 * kk),), anchor="mm")
        d.text((cx, cy + 70), l2, font=fonte(SANS_SB, 34), fill=tc + (int(255 * kk),), anchor="mm")
    k = suave((t - T(3.8)) / 0.3)
    if k > 0:
        d.text((W / 2, CY0 + 680), "Comenta A ou B", font=fonte(SANS_SB, 50), fill=CORAL + (int(255 * k),),
               anchor="mm")


# ------------------------------------------------------------------ cenas

REF_VOZ = [8.29, 8.21, 5.30, 4.55, 8.26, 4.75, 9.55, 5.03]


def construir():
    v = Video("Gales", "Portugal", abrev=("GAL", "POR"),
              fonte_txt="Ilustração · dados ESPN, Observador, DN e Agente Claudio")
    v.folga, v.bpm = 0.35, 112
    v.sp["casa"] = sprite(17, VERMELHO, VERDE_PT, 4)     # Portugal
    v.sp["fora"] = sprite(17, BRANCO, (60, 60, 60), 3)   # Gales (cor neutra para não confundir com Portugal)
    cenas = []

    def cena(dur, titulo, i, jog, **kw):
        voz, leg = FALAS[i]
        c = Cena(dur, titulo, "", jog, voz=voz, legenda=leg, voz_ini=VI, **kw)
        c.voz_ref = REF_VOZ[i]
        cenas.append(c)
        return c

    c = cena(9.0, "Gales 2–2 Portugal · intervalo", 0, jogadores({}), placar="2–2", minuto="INT",
             sobreposicao=gancho, nomes=False)
    c.t_capa = 8.4

    # 1. os planos: António Silva ao lado de Renato Veiga; Gales em 4-4-2 baixo, à espera do erro
    pos1 = {"ward": (0.5, 0.04), "roberts": (0.18, 0.22), "rodon": (0.40, 0.20), "davies": (0.60, 0.20),
            "dasilva": (0.82, 0.22), "james": (0.20, 0.34), "sheehan": (0.42, 0.33), "colwill": (0.58, 0.33),
            "thomas": (0.80, 0.34), "brooks": (0.44, 0.46), "wilson": (0.56, 0.46),
            "costa": (0.5, 0.94), "veiga": (0.40, 0.78), "asilva": (0.60, 0.78), "dalot": (0.14, 0.60),
            "cancelo": (0.86, 0.58), "jneves": (0.42, 0.60), "vitinha": (0.58, 0.62), "bruno": (0.50, 0.42),
            "trincao": (0.16, 0.36), "neto": (0.84, 0.38), "ramos": (0.50, 0.26)}
    cena(8.9, "Os planos", 1, jogadores(pos1, mostrar={"asilva", "veiga"}), placar="0–0", minuto="",
         formas=[{"tipo": "rotulo", "x": 0.5, "y": 0.86, "texto": "sem Rúben Dias", "cor": CORAL, "t0": T(0.3),
                  "t1": T(2.6)},
                 {"tipo": "linha", "ids": ["roberts", "rodon", "davies", "dasilva"], "cor": BRANCO, "t0": T(5.6),
                  "t1": 8.9},
                 {"tipo": "linha", "ids": ["james", "sheehan", "colwill", "thomas"], "cor": BRANCO, "t0": T(5.9),
                  "t1": 8.9},
                 {"tipo": "linha", "ids": ["brooks", "wilson"], "cor": BRANCO, "t0": T(6.2), "t1": 8.9},
                 {"tipo": "rotulo", "x": 0.5, "y": 0.10, "texto": "4-4-2 à espera do erro", "cor": BRANCO,
                  "t0": T(6.4), "t1": 8.9}],
         destaques=[("asilva", T(2.7), T(4.6)), ("veiga", T(3.8), T(4.6))])

    # 2. o 1–0: João Neves rouba lá à frente, Bruno à entrada da área coloca em jeito (vista do ataque)
    pos2 = {"ward": (0.5, 0.03), "roberts": (0.20, 0.13), "rodon": (0.40, 0.11), "davies": (0.60, 0.11),
            "dasilva": (0.80, 0.13), "james": (0.22, 0.26), "colwill": (0.62, 0.26), "thomas": (0.82, 0.28),
            "brooks": (0.44, 0.40), "wilson": (0.58, 0.42), "ramos": (0.50, 0.10), "trincao": (0.20, 0.20),
            "neto": (0.84, 0.20), "vitinha": (0.62, 0.38), "dalot": (0.14, 0.42), "cancelo": (0.88, 0.40),
            "veiga": (0.40, 0.62), "asilva": (0.60, 0.62), "costa": (0.5, 0.92)}
    mov = {"sheehan": vai((0.44, 0.30), (0.46, 0.31), T(1.2), T(1.6), 99),
           "jneves": vai((0.40, 0.40), (0.45, 0.31), T(0.9), T(1.6), 99),
           "bruno": vai((0.56, 0.30), (0.53, 0.19), T(1.8), T(3.2), 99),
           "ward": [(0, 0.5, 0.03), (T(4.3), 0.52, 0.03), (T(4.7), 0.47, 0.025), (99, 0.47, 0.025)]}
    bola = [(0, 0.44, 0.30), (T(1.4), 0.44, 0.30), (T(1.6), 0.45, 0.32), (T(2.0), 0.45, 0.32),
            (T(3.2), 0.53, 0.20), (T(4.1), 0.53, 0.20), (T(4.7), 0.44, 0.0)]
    cena(6.0, "O 0–1", 2, jogadores(pos2, mov, mostrar={"jneves", "bruno"}), bola=bola, placar="0–0", minuto="11'",
         vista="ataque", golo=(T(4.75), "0–1", "Bruno Fernandes"),
         formas=[{"tipo": "rotulo", "x": 0.30, "y": 0.36, "texto": "roubo lá à frente", "cor": CORAL, "t0": T(1.5),
                  "t1": T(3.0)},
                 {"tipo": "rotulo", "x": 0.70, "y": 0.18, "texto": "em jeito", "cor": CORAL, "t0": T(4.3),
                  "t1": 6.0}],
         setas=[{"pts": [(0.45, 0.32), (0.53, 0.20)], "t0": T(2.0), "t1": T(3.2), "tipo": "passe"},
                {"pts": [(0.53, 0.20), (0.44, 0.0)], "t0": T(4.1), "t1": T(4.7), "tipo": "remate"}],
         destaques=[("jneves", T(1.0), T(2.4)), ("bruno", T(2.7), 6.0)])

    # 3. o 1–1: Costa defende o remate de Wilson, a recarga sobra e Brooks empata (vista da defesa)
    pos3 = {"costa": (0.5, 0.97), "dalot": (0.20, 0.84), "veiga": (0.42, 0.87), "asilva": (0.60, 0.86),
            "cancelo": (0.82, 0.82), "jneves": (0.44, 0.74), "vitinha": (0.58, 0.72), "bruno": (0.50, 0.60),
            "trincao": (0.20, 0.62), "neto": (0.80, 0.62), "ramos": (0.50, 0.52), "james": (0.22, 0.76),
            "thomas": (0.80, 0.74), "sheehan": (0.42, 0.62), "colwill": (0.62, 0.78), "roberts": (0.16, 0.58),
            "dasilva": (0.86, 0.58), "rodon": (0.40, 0.46), "davies": (0.60, 0.46), "ward": (0.5, 0.05)}
    mov = {"wilson": vai((0.66, 0.80), (0.66, 0.84), T(1.0), T(1.8), 99),
           "brooks": vai((0.46, 0.80), (0.50, 0.87), T(2.4), T(3.4), 99),
           "costa": [(0, 0.5, 0.97), (T(2.3), 0.5, 0.97), (T(2.6), 0.56, 0.975), (T(3.6), 0.56, 0.975),
                     (T(3.9), 0.54, 0.975)]}
    bola = [(0, 0.66, 0.80), (T(1.8), 0.66, 0.84), (T(2.0), 0.66, 0.84), (T(2.5), 0.56, 0.97), (T(3.2), 0.50, 0.87),
            (T(3.6), 0.50, 0.87), (T(4.0), 0.44, 1.0)]
    cena(5.3, "O 1–1", 3, jogadores(pos3, mov, mostrar={"costa", "wilson", "brooks"}), bola=bola, placar="0–1",
         minuto="13'", vista="defesa", golo=(T(4.05), "1–1", "Brooks"),
         formas=[{"tipo": "rotulo", "x": 0.74, "y": 0.92, "texto": "defesa", "cor": BRANCO, "t0": T(2.5),
                  "t1": T(3.4)},
                 {"tipo": "rotulo", "x": 0.32, "y": 0.92, "texto": "a recarga sobra", "cor": CORAL, "t0": T(3.0),
                  "t1": 5.3}],
         setas=[{"pts": [(0.66, 0.84), (0.56, 0.97)], "t0": T(2.0), "t1": T(2.5), "tipo": "remate"},
                {"pts": [(0.50, 0.87), (0.44, 1.0)], "t0": T(3.6), "t1": T(4.0), "tipo": "remate"}],
         destaques=[("brooks", T(3.4), 5.3)])

    # 4. o 2–1: Portugal ainda a recuperar de um ataque; transição; Brooks solta para Sorba Thomas
    pos4 = {"ward": (0.5, 0.05), "roberts": (0.18, 0.40), "rodon": (0.40, 0.42), "davies": (0.60, 0.42),
            "dasilva": (0.82, 0.44), "james": (0.20, 0.52), "sheehan": (0.42, 0.50), "colwill": (0.58, 0.52),
            "trincao": (0.18, 0.40), "ramos": (0.48, 0.36), "neto": (0.80, 0.40), "bruno": (0.52, 0.44),
            "dalot": (0.12, 0.48)}
    mov = {"brooks": vai((0.46, 0.56), (0.50, 0.72), T(4.2), T(5.6), 99),
           "thomas": [(0, 0.80, 0.58), (T(4.4), 0.80, 0.58), (T(6.3), 0.76, 0.79), (T(7.1), 0.64, 0.86),
                      (99, 0.64, 0.86)],
           "wilson": vai((0.56, 0.58), (0.44, 0.82), T(4.4), T(7.0), 99),
           "cancelo": vai((0.86, 0.46), (0.82, 0.70), T(2.6), T(7.2), 99),
           "jneves": vai((0.42, 0.56), (0.46, 0.70), T(2.6), T(7.2), 99),
           "vitinha": vai((0.60, 0.56), (0.62, 0.70), T(2.6), T(7.2), 99),
           "asilva": vai((0.62, 0.68), (0.62, 0.84), T(4.6), T(7.0), 99),
           "veiga": vai((0.40, 0.68), (0.46, 0.85), T(4.6), T(7.0), 99),
           "costa": vai((0.5, 0.96), (0.56, 0.92), T(7.0), T(7.4), 99)}
    bola = [(0, 0.46, 0.56), (T(4.2), 0.46, 0.56), (T(5.6), 0.50, 0.72), (T(5.9), 0.50, 0.72), (T(6.3), 0.76, 0.79),
            (T(7.1), 0.64, 0.86), (T(7.3), 0.64, 0.86), (T(7.6), 0.45, 1.0)]
    cena(9.0, "O 2–1", 4, jogadores(pos4, mov, mostrar={"brooks", "thomas", "cancelo"}), bola=bola, placar="1–1",
         minuto="40'", vista="defesa", golo=(T(7.65), "2–1", "Sorba Thomas"),
         formas=[{"tipo": "rotulo", "x": 0.5, "y": 0.62, "texto": "Portugal ainda a recuperar", "cor": CORAL,
                  "t0": T(1.9), "t1": T(4.4)},
                 {"tipo": "rotulo", "x": 0.30, "y": 0.66, "texto": "transição", "cor": BRANCO, "t0": T(4.8),
                  "t1": T(6.6)}],
         setas=[{"pts": [(0.46, 0.56), (0.50, 0.72)], "t0": T(4.2), "t1": T(5.6), "tipo": "conducao"},
                {"pts": [(0.50, 0.72), (0.76, 0.79)], "t0": T(5.9), "t1": T(6.3), "tipo": "passe"},
                {"pts": [(0.64, 0.86), (0.45, 1.0)], "t0": T(7.3), "t1": T(7.6), "tipo": "remate"}],
         destaques=[("brooks", T(5.5), T(6.4)), ("thomas", T(6.5), 9.0)])

    # 5. o 2–2: Trincão cruza da esquerda, Neto desvia de primeira ao segundo poste (vista do ataque)
    pos5 = {"ward": (0.5, 0.03), "roberts": (0.24, 0.10), "rodon": (0.42, 0.08), "davies": (0.56, 0.08),
            "dasilva": (0.74, 0.10), "james": (0.22, 0.22), "sheehan": (0.42, 0.22), "colwill": (0.58, 0.22),
            "thomas": (0.80, 0.24), "brooks": (0.46, 0.38), "wilson": (0.56, 0.40), "ramos": (0.48, 0.09),
            "bruno": (0.50, 0.24), "jneves": (0.40, 0.36), "vitinha": (0.60, 0.36), "dalot": (0.12, 0.30),
            "cancelo": (0.86, 0.32), "veiga": (0.40, 0.60), "asilva": (0.60, 0.60), "costa": (0.5, 0.92)}
    mov = {"trincao": vai((0.14, 0.24), (0.12, 0.14), T(0.6), T(1.3), 99),
           "neto": vai((0.82, 0.20), (0.62, 0.055), T(1.5), T(2.8), 99)}
    bola = [(0, 0.15, 0.25), (T(1.3), 0.13, 0.15), (T(1.6), 0.13, 0.15), (T(2.8), 0.61, 0.06), (T(3.1), 0.50, 0.0)]
    cena(5.5, "O 2–2", 5, jogadores(pos5, mov, mostrar={"trincao", "neto"}), bola=bola, placar="2–1", minuto="43'",
         vista="ataque", golo=(T(3.15), "2–2", "Pedro Neto"),
         formas=[{"tipo": "rotulo", "x": 0.74, "y": 0.13, "texto": "2.º poste", "cor": CORAL, "t0": T(3.4),
                  "t1": 5.5}],
         setas=[{"pts": [(0.13, 0.15), (0.61, 0.06)], "t0": T(1.6), "t1": T(2.8), "tipo": "passe"},
                {"pts": [(0.82, 0.20), (0.62, 0.06)], "t0": T(1.5), "t1": T(2.8), "tipo": "corrida"},
                {"pts": [(0.61, 0.06), (0.50, 0.0)], "t0": T(2.8), "t1": T(3.1), "tipo": "remate"}],
         destaques=[("trincao", T(1.0), T(2.0)), ("neto", T(2.2), 5.5)])

    c = cena(10.1, "", 6, jogadores({}), placar="2–2", minuto="INT", sobreposicao=cartao_agente, nomes=False)
    c.t_capa = 9.6
    c = cena(5.6, "", 7, jogadores({}), placar="", sobreposicao=pergunta, nomes=False)
    c.t_capa = 5.2
    cenas.append(cena_fecho(jogadores({}), placar="2–2", minuto="INT", frase=11))
    return v, cenas
