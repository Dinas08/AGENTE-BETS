"""País de Gales 2–3 Portugal, 2.ª parte (Liga das Nações, Cardiff, 17 nov 2026). Continuação do vídeo do intervalo.

Fontes (verificadas a 17 nov 2026, depois do jogo):
- ESPN (summary 401861189): ao intervalo Cabango entra para o lugar de Rodon; 59' Neto acerta no poste esquerdo (remate
  do lado direito da área, assist. Cancelo); 59' Félix e Forbs entram para os lugares de Ramos e Trincão; 63' Johnson e
  Collins entram em Gales; 68' Costa defende cabeceamento de Cabango (cruzamento de Sorba Thomas) e remate de Wilson;
  70' golo de Forbs, pé esquerdo, do centro da área para o canto inferior esquerdo, sem assistência; 72' e 74'
  amarelos de Neto (expulso); 90' Costa defende remate de Connor Roberts "from very close range". Remates 22–11
  (2.ª parte 12–5, comparando com o resumo do intervalo), à baliza 8–6 (3–2 na 2.ª parte), cantos 6–1 (4–1),
  6 defesas de Costa. Artigo ESPN: Forbs, o novo n.º 7, marca 11 minutos depois de entrar; Portugal fica em 1.º
  do grupo e vai aos quartos de final (março).
- TVI: "corte deficiente de Ben Davies" dá espaço a Forbs na direita, que tira Davies da frente e remata colocado.
  101 Great Goals: Cabango falha o corte a um passe longo de Bruno; Forbs corta para dentro e remata rasteiro de pé
  esquerdo para o poste mais distante. Observador: Neto vê dois amarelos "no espaço de dois minutos"; Costa defende
  o cabeceamento de Cabango "em cima da linha".
- Agente Claudio (ramo claude/dados): previsão de mais de 2,5 golos (66%) certa; dica do canal "Vitória Portugal"
  (@1.38, mensagem 229) certa.
As jogadas são ilustrações coerentes com isto (quem falhou o corte do 3–2 varia entre fontes: a voz não diz).
"""
from PIL import Image, ImageDraw

from quadro_tatico import (cena_fecho, sprite, CORAL, CREME, CREME_70, CY0, CH, W, Cena, Video, fonte, suave,
                           SERIFA_N, SANS, SANS_SB)

import porto_napoli as base
import benfica_lech as bl
import gales_portugal_1p as p1

vai, _ov, PFP, _visto = base.vai, base._ov, base.PFP, base._visto
_fundo, _chip = bl._fundo, bl._chip
VERMELHO, VERDE_PT, BRANCO = p1.VERMELHO, p1.VERDE_PT, p1.BRANCO
AMARELO = (240, 200, 60)
FORA = (1.35, 0.5)   # fora do ecrã (Neto depois da expulsão)

FALAS = [
    ("Na segunda parte, o Gales rematou doze vezes. Portugal, cinco. E jogou os últimos vinte minutos com dez. "
     "Mesmo assim, ganhou três a dois.",
     "Na 2.ª parte, o Gales rematou 12 vezes. Portugal, 5. E jogou os últimos 20 minutos com 10. "
     "Mesmo assim, ganhou 3–2."),
    ("Ao intervalo, o Bélami tira o Ródon e mete o Cabango. Aos cinquenta e nove, o Pedro Neto acerta no poste, e o "
     "JJ mexe: entram o Félix e o Forbs.",
     "Ao intervalo, o Bellamy tira o Rodon e mete o Cabango. Aos 59', o Pedro Neto acerta no poste e o JJ mexe: "
     "entram o Félix e o Forbs."),
    ("Aos sessenta e oito, o Gales aperta: o Diogo Costa defende o cabeceamento do Cabango e, logo a seguir, o "
     "remate do Uílson.",
     "Aos 68', o Gales aperta: o Diogo Costa defende o cabeceamento do Cabango e, logo a seguir, o remate do Wilson."),
    ("Dois minutos depois, um corte mal feito deixa a bola ao Forbs, na direita. Puxa para dentro e, de pé esquerdo, "
     "cruza o remate. Três a dois, onze minutos depois de entrar.",
     "Dois minutos depois, um corte mal feito deixa a bola ao Forbs, na direita. Puxa para dentro e, de pé esquerdo, "
     "cruza o remate. 3–2, 11 minutos depois de entrar."),
    ("Mas aos setenta e quatro, o Pedro Neto vê o segundo amarelo em dois minutos, e Portugal fica com dez.",
     "Mas aos 74', o Pedro Neto vê o segundo amarelo em dois minutos e Portugal fica com 10."),
    ("O Gales carrega até ao fim, e aos noventa o Diogo Costa ainda tira um remate à queima-roupa ao Cónor Róberts. "
     "Seis defesas no jogo, e Portugal acaba em primeiro no grupo.",
     "O Gales carrega até ao fim e, aos 90', o Diogo Costa ainda tira um remate à queima-roupa ao Connor Roberts. "
     "6 defesas no jogo, e Portugal acaba em 1.º no grupo."),
    ("E o Agente Claudio? A previsão de mais de dois golos e meio entrou logo ao intervalo. E a dica, vitória de "
     "Portugal, também acertou. As dicas estão na rede vizinha, link na bio.",
     "E o Agente Claudio? A previsão de mais de 2,5 golos entrou logo ao intervalo. E a dica, vitória de Portugal, "
     "também acertou. As dicas estão na rede vizinha, link na bio."),
    ("E tu? O Forbs, com a sete: titular já em março, ou arma para sair do banco? Diz nos comentários.",
     "E tu? O Forbs, com a 7: titular já em março, ou arma para sair do banco? Diz nos comentários."),
]

SUBS = {"ramos": "Félix", "trincao": "Forbs", "rodon": "Cabango", "james": "Johnson", "brooks": "Collins"}


def jogadores(pos, mov=None, mostrar=()):
    return p1.jogadores(pos, mov, mostrar, subs=SUBS)


VI = 0.15


def T(x):
    return x + VI


# ------------------------------------------------------------------ sobreposições

def gancho(v, q, t):
    ov = _ov(q)
    d = ImageDraw.Draw(ov)
    d.rectangle((0, CY0 + CH * 0.10, W, CY0 + CH * 0.86), fill=(20, 20, 19, 232))
    d.text((W / 2, CY0 + CH * 0.10 + 55), "2.ª PARTE  ·  CARDIFF", font=fonte(SANS_SB, 34), fill=CORAL + (255,),
           anchor="mm")
    linhas = [("Remates", 5, 12, T(0.9)), ("À baliza", 2, 3, T(2.0)), ("Cantos", 1, 4, T(2.5))]
    for i, (nome, a, b, ti) in enumerate(linhas):
        kk = suave((t - ti) / 0.35)
        if kk <= 0:
            continue
        al = int(255 * kk)
        y = CY0 + 260 + i * 115
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
            d.text((x0 - 30, y - 50), "POR", font=fonte(SANS_SB, 26), fill=CREME_70 + (al,), anchor="rm")
            d.text((x1 + 30, y - 50), "GAL", font=fonte(SANS_SB, 26), fill=CREME_70 + (al,), anchor="lm")
    k = suave((t - T(3.4)) / 0.3)
    if k > 0:
        y = CY0 + 260 + 3 * 115 - 10
        al = int(255 * k)
        d.rounded_rectangle((W / 2 - 230, y - 32, W / 2 - 190, y + 26), radius=6, fill=(210, 40, 45, al))
        d.text((W / 2 - 165, y - 3), "10 contra 11 desde os 74'", font=fonte(SANS_SB, 34), fill=CREME + (al,),
               anchor="lm")
    k = suave((t - T(5.8)) / 0.3)
    if k > 0:
        esc = 1.1 - 0.1 * k
        d.text((W / 2, CY0 + CH * 0.77), "2–3", font=fonte(SERIFA_N, int(150 * esc)), fill=CREME + (int(255 * k),),
               anchor="mm")
    q.im.paste(ov, (0, 0), ov)


def cartoes(v, q, t):
    ov = _ov(q)
    d = ImageDraw.Draw(ov)
    for i, (cor, txt, ti) in enumerate(((AMARELO, "72'", T(1.6)), (AMARELO, "74'", T(1.9)),
                                       ((210, 40, 45), "", T(2.4)))):
        k = suave((t - ti) / 0.25)
        if k <= 0:
            continue
        al = int(255 * k)
        cx = W / 2 - 150 + i * 150
        cy = CY0 + 150 - 20 * (1 - k)
        if i == 2:
            d.text((cx - 75, cy), "=", font=fonte(SANS_SB, 60), fill=CREME + (al,), anchor="mm")
        d.rounded_rectangle((cx - 38, cy - 52, cx + 38, cy + 52), radius=8, fill=cor + (al,))
        if txt:
            d.text((cx, cy + 82), txt, font=fonte(SANS_SB, 30), fill=CREME + (al,), anchor="mm")
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
    linhas = [("A previsão · 66%", "Mais de 2,5 golos", T(1.3), T(3.7)),
              ("A dica · odd 1,38", "Vitória de Portugal", T(4.5), T(6.5))]
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
    k = suave((t - T(7.2)) / 0.3)
    if k > 0:
        _chip(d, W / 2, CY0 + 640, "Dicas na rede vizinha · link na bio", CORAL, k, tam=36)


def pergunta(v, q, t):
    _fundo(q, t)
    d = q.d
    k = suave((t - 0.1) / 0.35)
    if k > 0:
        d.text((W / 2, CY0 + 170), "O Forbs, com a 7?", font=fonte(SERIFA_N, 66), fill=CREME + (int(255 * k),),
               anchor="mm")
    for i, (letra, l1, l2, ti, cor) in enumerate((("A", "titular", "já em março", T(1.5), VERMELHO),
                                                  ("B", "arma para", "sair do banco", T(2.7), BRANCO))):
        kk = suave((t - ti) / 0.35)
        if kk <= 0:
            continue
        al = int(255 * kk)
        cx, cy = W / 2 + (-215 if i == 0 else 215), CY0 + 410
        d.rounded_rectangle((cx - 200, cy - 125, cx + 200, cy + 125), radius=28, fill=cor + (al,))
        tc = CREME if i == 0 else (20, 20, 19)
        d.text((cx, cy - 50), letra, font=fonte(SERIFA_N, 66), fill=tc + (al,), anchor="mm")
        d.text((cx, cy + 25), l1, font=fonte(SANS_SB, 34), fill=tc + (al,), anchor="mm")
        d.text((cx, cy + 70), l2, font=fonte(SANS_SB, 34), fill=tc + (al,), anchor="mm")
    k = suave((t - T(3.9)) / 0.3)
    if k > 0:
        d.text((W / 2, CY0 + 680), "Comenta A ou B", font=fonte(SANS_SB, 50), fill=CORAL + (int(255 * k),),
               anchor="mm")


# ------------------------------------------------------------------ cenas

REF_VOZ = [6.75, 8.06, 6.02, 8.73, 4.99, 8.24, 10.34, 5.18]


def construir():
    v = Video("Gales", "Portugal", abrev=("GAL", "POR"),
              fonte_txt="Ilustração · dados ESPN, Observador, TVI e Agente Claudio")
    v.folga, v.bpm = 0.35, 112
    v.sp["casa"] = sprite(17, VERMELHO, VERDE_PT, 4)     # Portugal
    v.sp["fora"] = sprite(17, BRANCO, (60, 60, 60), 3)   # Gales
    cenas = []

    def cena(dur, titulo, i, jog, **kw):
        voz, leg = FALAS[i]
        c = Cena(dur, titulo, "", jog, voz=voz, legenda=leg, voz_ini=VI, **kw)
        c.voz_ref = REF_VOZ[i]
        cenas.append(c)
        return c

    c = cena(7.4, "Gales 2–3 Portugal · 2.ª parte", 0, jogadores({}), placar="2–3", minuto="FIM",
             sobreposicao=gancho, nomes=False)
    c.t_capa = 7.0

    # 1. mexidas: Cabango por Rodon; Neto acerta no poste esquerdo; entram Félix e Forbs
    pos1 = {"ward": (0.5, 0.03), "roberts": (0.20, 0.13), "rodon": (0.34, 0.10), "davies": (0.58, 0.11),
            "dasilva": (0.80, 0.14), "james": (0.22, 0.26), "sheehan": (0.42, 0.26), "colwill": (0.58, 0.26),
            "thomas": (0.80, 0.28), "brooks": (0.44, 0.42), "wilson": (0.58, 0.42), "ramos": (0.50, 0.19),
            "trincao": (0.18, 0.22), "bruno": (0.50, 0.28), "jneves": (0.40, 0.44), "vitinha": (0.62, 0.42),
            "dalot": (0.12, 0.40), "veiga": (0.40, 0.64), "asilva": (0.60, 0.64), "costa": (0.5, 0.93)}
    mov = {"cancelo": vai((0.88, 0.36), (0.88, 0.24), T(3.4), T(4.0), 99),
           "neto": vai((0.80, 0.24), (0.70, 0.13), T(3.6), T(4.5), 99),
           "ward": [(0, 0.5, 0.03), (T(4.5), 0.5, 0.03), (T(4.8), 0.46, 0.03), (99, 0.46, 0.03)]}
    bola = [(0, 0.88, 0.36), (T(3.4), 0.88, 0.36), (T(4.0), 0.88, 0.24), (T(4.2), 0.80, 0.21), (T(4.5), 0.70, 0.13),
            (T(4.9), 0.445, 0.005), (T(5.3), 0.36, 0.06), (99, 0.36, 0.06)]
    cena(8.6, "As mexidas", 1, jogadores(pos1, mov, mostrar={"rodon", "neto", "ramos", "trincao"}), bola=bola,
         placar="2–2", minuto="59'",
         formas=[{"tipo": "rotulo", "x": 0.5, "y": 0.20, "texto": "sai Rodon, entra Cabango", "cor": BRANCO,
                  "t0": T(1.5), "t1": T(3.1)},
                 {"tipo": "rotulo", "x": 0.30, "y": 0.08, "texto": "poste!", "cor": CORAL, "t0": T(4.9),
                  "t1": T(6.0)},
                 {"tipo": "rotulo", "x": 0.30, "y": 0.34, "texto": "entram Félix e Forbs", "cor": CORAL,
                  "t0": T(6.1), "t1": 8.6}],
         setas=[{"pts": [(0.70, 0.13), (0.445, 0.005)], "t0": T(4.5), "t1": T(4.9), "tipo": "remate"}],
         destaques=[("rodon", T(1.5), T(3.0)), ("neto", T(3.8), T(5.4)), ("ramos", T(6.3), 8.6),
                    ("trincao", T(6.9), 8.6)])

    # 2. 68': Costa defende o cabeceamento de Cabango e o remate de Wilson (vista da defesa)
    pos2 = {"dalot": (0.20, 0.84), "veiga": (0.42, 0.88), "asilva": (0.58, 0.87), "cancelo": (0.80, 0.83),
            "jneves": (0.44, 0.76), "vitinha": (0.60, 0.74), "bruno": (0.50, 0.62), "trincao": (0.22, 0.62),
            "neto": (0.80, 0.62), "ramos": (0.50, 0.50), "james": (0.24, 0.80), "colwill": (0.66, 0.90),
            "sheehan": (0.44, 0.66), "brooks": (0.36, 0.84), "roberts": (0.16, 0.60), "dasilva": (0.84, 0.62),
            "davies": (0.60, 0.48), "ward": (0.5, 0.05), "thomas": (0.86, 0.78)}
    mov = {"rodon": vai((0.46, 0.80), (0.40, 0.91), T(1.6), T(3.0), 99),
           "wilson": vai((0.56, 0.74), (0.54, 0.83), T(3.2), T(4.4), 99),
           "costa": [(0, 0.5, 0.97), (T(3.0), 0.5, 0.97), (T(3.3), 0.44, 0.98), (T(4.2), 0.48, 0.97),
                     (T(4.9), 0.50, 0.97), (T(5.3), 0.57, 0.98), (99, 0.57, 0.98)]}
    bola = [(0, 0.86, 0.78), (T(1.9), 0.86, 0.78), (T(3.0), 0.40, 0.91), (T(3.3), 0.44, 0.985), (T(3.6), 0.38, 1.0),
            (T(4.0), 0.54, 0.84), (T(4.9), 0.54, 0.84), (T(5.3), 0.57, 0.985), (T(5.7), 0.66, 1.0)]
    cena(6.5, "O Costa segura", 2, jogadores(pos2, mov, mostrar={"costa", "rodon", "wilson"}), bola=bola,
         placar="2–2", minuto="68'", vista="defesa",
         formas=[{"tipo": "rotulo", "x": 0.28, "y": 0.96, "texto": "defesa", "cor": CORAL, "t0": T(3.3),
                  "t1": T(4.4)},
                 {"tipo": "rotulo", "x": 0.76, "y": 0.96, "texto": "outra", "cor": CORAL, "t0": T(5.3), "t1": 6.5}],
         setas=[{"pts": [(0.86, 0.78), (0.40, 0.91)], "t0": T(1.9), "t1": T(3.0), "tipo": "passe"},
                {"pts": [(0.40, 0.91), (0.44, 0.985)], "t0": T(3.0), "t1": T(3.3), "tipo": "remate"},
                {"pts": [(0.54, 0.84), (0.57, 0.985)], "t0": T(4.9), "t1": T(5.3), "tipo": "remate"}],
         destaques=[("costa", T(1.4), T(2.4)), ("rodon", T(2.9), T(3.6)), ("wilson", T(4.6), 6.5)])

    # 3. 70': corte mal feito, Forbs na direita puxa para dentro e remata cruzado de pé esquerdo (vista do ataque)
    pos3 = {"ward": (0.5, 0.03), "roberts": (0.24, 0.12), "rodon": (0.44, 0.10), "dasilva": (0.26, 0.20),
            "james": (0.22, 0.30), "sheehan": (0.42, 0.28), "colwill": (0.58, 0.30), "thomas": (0.76, 0.36),
            "brooks": (0.46, 0.44), "wilson": (0.60, 0.46), "ramos": (0.46, 0.14), "neto": (0.24, 0.24),
            "bruno": (0.52, 0.32), "jneves": (0.40, 0.48), "vitinha": (0.62, 0.50), "dalot": (0.12, 0.44),
            "cancelo": (0.88, 0.46), "veiga": (0.40, 0.66), "asilva": (0.60, 0.66), "costa": (0.5, 0.93)}
    mov = {"davies": [(0, 0.62, 0.12), (T(1.0), 0.62, 0.12), (T(1.4), 0.66, 0.15), (T(3.8), 0.70, 0.18),
                      (T(4.4), 0.64, 0.15), (99, 0.64, 0.15)],
           "trincao": [(0, 0.82, 0.30), (T(1.6), 0.82, 0.30), (T(2.6), 0.80, 0.22), (T(3.8), 0.74, 0.18),
                       (T(5.2), 0.60, 0.14), (99, 0.58, 0.13)],
           "ward": [(0, 0.5, 0.03), (T(5.4), 0.52, 0.03), (T(5.9), 0.47, 0.03), (99, 0.47, 0.03)]}
    bola = [(0, 0.40, 0.30), (T(0.6), 0.40, 0.30), (T(1.2), 0.62, 0.13), (T(1.4), 0.63, 0.14), (T(2.6), 0.80, 0.22),
            (T(3.8), 0.74, 0.185), (T(5.2), 0.60, 0.145), (T(5.6), 0.60, 0.145), (T(6.0), 0.445, 0.005)]
    cena(9.2, "O 2–3", 3, jogadores(pos3, mov, mostrar={"trincao", "davies"}), bola=bola, placar="2–2",
         minuto="70'", vista="ataque", golo=(T(6.05), "2–3", "Carlos Forbs"),
         formas=[{"tipo": "rotulo", "x": 0.50, "y": 0.20, "texto": "corte mal feito", "cor": BRANCO, "t0": T(1.3),
                  "t1": T(3.0)},
                 {"tipo": "rotulo", "x": 0.80, "y": 0.10, "texto": "pé esquerdo", "cor": CORAL, "t0": T(5.1),
                  "t1": T(6.6)},
                 {"tipo": "rotulo", "x": 0.70, "y": 0.30, "texto": "11' depois de entrar", "cor": CORAL,
                  "t0": T(6.8), "t1": 9.2}],
         setas=[{"pts": [(0.40, 0.30), (0.62, 0.13)], "t0": T(0.6), "t1": T(1.2), "tipo": "passe"},
                {"pts": [(0.63, 0.14), (0.80, 0.22)], "t0": T(1.4), "t1": T(2.6), "tipo": "corrida_fora"},
                {"pts": [(0.74, 0.185), (0.60, 0.145)], "t0": T(3.8), "t1": T(5.2), "tipo": "conducao"},
                {"pts": [(0.60, 0.145), (0.445, 0.005)], "t0": T(5.6), "t1": T(6.0), "tipo": "remate"}],
         destaques=[("davies", T(1.1), T(2.4)), ("trincao", T(2.6), 9.2)])

    # 4. 74': Neto, segundo amarelo em dois minutos; Portugal com dez
    pos4 = {"neto": (0.80, 0.56), "trincao": (0.84, 0.40)}
    mov = {"neto": [(0, 0.80, 0.56), (T(3.2), 0.80, 0.56), (T(5.4), 1.02, 0.60), (5.6, FORA[0], FORA[1])],
           "james": vai((0.80, 0.50), (0.78, 0.52), T(1.0), T(1.6), 99)}
    cena(5.6, "Expulsão", 4, jogadores(pos4, mov, mostrar={"neto"}), placar="2–3", minuto="74'",
         sobreposicao=cartoes,
         formas=[{"tipo": "rotulo", "x": 0.5, "y": 0.72, "texto": "10 contra 11", "cor": CORAL, "t0": T(3.6),
                  "t1": 5.6}],
         destaques=[("neto", T(0.9), T(3.2))])

    # 5. pressão final; 90': Costa tira o remate à queima-roupa de Connor Roberts (vista da defesa)
    pos5 = {"neto": FORA, "dalot": (0.22, 0.86), "veiga": (0.42, 0.90), "asilva": (0.58, 0.90),
            "cancelo": (0.78, 0.86), "jneves": (0.40, 0.80), "vitinha": (0.60, 0.80), "bruno": (0.50, 0.70),
            "trincao": (0.24, 0.70), "ramos": (0.70, 0.66), "james": (0.20, 0.78), "brooks": (0.36, 0.82),
            "wilson": (0.66, 0.76), "colwill": (0.56, 0.84), "thomas": (0.84, 0.80), "sheehan": (0.46, 0.68),
            "dasilva": (0.86, 0.62), "davies": (0.54, 0.56), "ward": (0.5, 0.05)}
    mov = {"roberts": vai((0.40, 0.84), (0.47, 0.93), T(2.2), T(3.3), 99),
           "rodon": vai((0.62, 0.92), (0.58, 0.91), T(2.4), T(2.9), 99),
           "costa": [(0, 0.5, 0.97), (T(3.4), 0.5, 0.97), (T(3.7), 0.45, 0.985), (99, 0.45, 0.985)]}
    bola = [(0, 0.84, 0.80), (T(1.8), 0.84, 0.80), (T(2.5), 0.60, 0.92), (T(2.9), 0.58, 0.91), (T(3.4), 0.47, 0.93),
            (T(3.7), 0.45, 0.99), (T(4.1), 0.38, 1.0)]
    cena(8.6, "Aguentar", 5, jogadores(pos5, mov, mostrar={"costa", "roberts"}), bola=bola, placar="2–3",
         minuto="90'", vista="defesa",
         formas=[{"tipo": "rotulo", "x": 0.72, "y": 0.96, "texto": "queima-roupa", "cor": CORAL, "t0": T(3.7),
                  "t1": T(5.0)},
                 {"tipo": "rotulo", "x": 0.5, "y": 0.60, "texto": "6 defesas no jogo", "cor": CORAL, "t0": T(5.2),
                  "t1": T(7.0)},
                 {"tipo": "rotulo", "x": 0.5, "y": 0.60, "texto": "1.º do grupo", "cor": CORAL, "t0": T(7.0),
                  "t1": 8.6}],
         setas=[{"pts": [(0.84, 0.80), (0.60, 0.92)], "t0": T(1.8), "t1": T(2.5), "tipo": "passe"},
                {"pts": [(0.58, 0.91), (0.47, 0.93)], "t0": T(2.9), "t1": T(3.4), "tipo": "passe"},
                {"pts": [(0.47, 0.93), (0.45, 0.99)], "t0": T(3.4), "t1": T(3.7), "tipo": "remate"}],
         destaques=[("roberts", T(3.0), T(3.8)), ("costa", T(3.8), 8.6)])

    c = cena(10.9, "", 6, jogadores({}), placar="2–3", minuto="FIM", sobreposicao=cartao_agente, nomes=False)
    c.t_capa = 10.4
    c = cena(5.8, "", 7, jogadores({}), placar="", sobreposicao=pergunta, nomes=False)
    c.t_capa = 5.4
    cenas.append(cena_fecho(jogadores({}), placar="2–3", minuto="FIM", frase=12))
    return v, cenas
