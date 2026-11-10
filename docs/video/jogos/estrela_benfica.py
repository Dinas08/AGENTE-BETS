"""Análise: Estrela da Amadora 2–3 Benfica (Liga, 8 nov 2026). O jogo, o frango de Samuel Soares e as "polémicas".

Fontes (verificadas a 9 nov 2026):
- ESPN: onzes (ambos 4-2-3-1 no papel), golos e estatísticas: Estrela 2 remates à baliza e 2 golos; Samuel Soares
  sem defesas. 26' Prestianni (assist. Echeverri); 48' Zvonarek (assist. Rafa Soares, contra-ataque); 68'
  autogolo de Schappo; 76' Antonetti de cabeça (livre, cruzamento de Joan Jordán); 90+4' Pavlidis (assist.
  Schjelderup).
- Maisfutebol (crónica): Estrela num 5-4-1 de Pepa; o Benfica "circulava por fora do bloco"; o 1–0 "sem que o
  Benfica entrasse dentro da área"; na 2.ª parte "menos pressionante e mais distante entre setores"; Soares
  "Saiu fora de tempo a um livre indireto"; trivela de Schjelderup; Pavlidis "de primeira"; "o quinto jogo
  consecutivo do avançado a marcar".
- A Bola: "abordagem desastrada" de Samuel Soares; Schappo "desviou de carrinho"; Marco Silva: «Os adeptos gostam
  de ver, mas eu não gostei nada» (título). O Jogo: Soares "praticamente imóvel na baliza".
- Polémicas: Observador (Sem Falta, Pedro Henriques): António Nobre nota 6, "noite sem casos", golos todos legais,
  penálti sobre Pavlidis (15') não, no 2–2 "quem provoca até o contacto é o Samuel Soares", faltas por assinalar
  (braço de Lukébakio ~92' devia ser amarelo). O Jogo (Tribunal, paywall) analisou um contacto de Tomás Araújo
  sobre Antonetti na área (sem penálti assinalado).
- Dica do canal: vitória do Benfica (75%) — acertou.
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
    ("Dois remates à baliza do Estrela, dois golos. E um frango pelo meio. Vê como o Benfica ganhou ao minuto "
     "noventa e quatro.",
     "Dois remates à baliza do Estrela, dois golos. E um frango pelo meio. Vê como o Benfica ganhou ao minuto 94."),
    ("O Estrela fechou-se num cinco, quatro, um. O Benfica circulava por fora do bloco, e o golo chegou de fora da "
     "área: o Prestiáni, ao ângulo, depois de um passe rápido do Etcheverri.",
     "O Estrela fechou-se num 5-4-1. O Benfica circulava por fora do bloco e o golo chegou de fora da área: "
     "Prestianni, ao ângulo, depois de um passe rápido do Echeverri."),
    ("Na segunda parte, o Benfica voltou menos pressionante, e com as linhas afastadas. O Estrela aproveitou logo: "
     "transição pela esquerda, cruzamento do Rafa Soares, e o Zvó-narek empata.",
     "Na segunda parte, o Benfica voltou menos pressionante e com as linhas afastadas. O Estrela aproveitou logo: "
     "transição pela esquerda, cruzamento do Rafa Soares e Zvonarek empata."),
    ("O Marco Silva mexeu, e aos sessenta e oito, o Rafa Silva cruza rasteiro, e o Scápo, de carrinho, mete na "
     "própria baliza.",
     "Marco Silva mexeu e, aos 68', Rafa Silva cruza rasteiro e Schappo, de carrinho, mete na própria baliza."),
    ("E depois... o frango. Livre do Estrela, o Samuel Soares sai fora de tempo, fica a meio caminho, e o Antonéti "
     "cabeceia para a baliza. Dois a dois.",
     "E depois, o frango. Livre do Estrela, Samuel Soares sai fora de tempo, fica a meio caminho e Antonetti "
     "cabeceia para a baliza. 2–2."),
    ("Lances polémicos? Houve dois na área: um pedido de penálti sobre o Pavlidis, e um contacto do Tomás Araújo "
     "com o Antonéti. O árbitro mandou seguir nos dois. E no frango, o Samuel Soares ainda choca com o Antonéti, mas o "
     "golo é legal. A grande polémica desta noite... chama-se Samuel Soares.",
     "Lances polémicos? Houve dois na área: um pedido de penálti sobre o Pavlidis e um contacto do Tomás Araújo "
     "com o Antonetti. O árbitro mandou seguir nos dois. E no frango, Samuel Soares ainda choca com o Antonetti, mas o "
     "golo é legal. A grande polémica desta noite chama-se Samuel Soares."),
    ("Até que, ao minuto noventa e quatro, o Chélderup inventa um cruzamento de trivela, e o Pavlidis, de primeira, "
     "faz o dois a três. Quinto jogo seguido a marcar.",
     "Até que, ao minuto 94, Schjelderup inventa um cruzamento de trivela e Pavlidis, de primeira, faz o 2–3. "
     "Quinto jogo seguido a marcar."),
    ("E o Agente Claudio? Deu vitória do Benfica... e acertou. As dicas estão na rede vizinha, link na bio. E tu: "
     "o Samuel Soares deve continuar na baliza? Diz nos comentários.",
     "E o Agente Claudio? Deu vitória do Benfica e acertou. As dicas estão na rede vizinha, link na bio. E tu: "
     "Samuel Soares deve continuar na baliza? Diz nos comentários."),
]

# ------------------------------------------------------------------ jogadores
# O Benfica (casa no motor) ataca para cima; o Estrela (bolas brancas) ataca para baixo. Marcador EST–BEN.
JOG = {
    "soares": ("Samuel Soares", "casa", (0.50, 0.95)),
    "dahl": ("Dahl", "casa", (0.15, 0.79)),
    "lenglet": ("Lenglet", "casa", (0.38, 0.85)),
    "araujo": ("T. Araújo", "casa", (0.62, 0.85)),
    "bah": ("Bah", "casa", (0.85, 0.79)),
    "palhinha": ("Palhinha", "casa", (0.40, 0.70)),
    "sudakov": ("Sudakov", "casa", (0.60, 0.70)),
    "echeverri": ("Echeverri", "casa", (0.50, 0.60)),
    "prestianni": ("Prestianni", "casa", (0.17, 0.58)),
    "rafa": ("Rafa Silva", "casa", (0.83, 0.58)),
    "pavlidis": ("Pavlidis", "casa", (0.50, 0.53)),
    "linck": ("Léo Linck", "fora", (0.50, 0.04)),
    "scholze": ("Scholze", "fora", (0.10, 0.17)),
    "luan": ("Luan Patrick", "fora", (0.32, 0.13)),
    "jansson": ("Höög Jansson", "fora", (0.50, 0.12)),
    "schappo": ("Schappo", "fora", (0.68, 0.13)),
    "rsoares": ("Rafa Soares", "fora", (0.90, 0.17)),
    "marcus": ("A. Marcus", "fora", (0.18, 0.28)),
    "serra": ("S. Serra", "fora", (0.40, 0.27)),
    "zvonarek": ("Zvonarek", "fora", (0.60, 0.27)),
    "stoica": ("Stoica", "fora", (0.82, 0.28)),
    "antonetti": ("Antonetti", "fora", (0.50, 0.42)),
}
SUBS_68 = {"araujo": "Circati", "echeverri": "Lukébakio", "stoica": "Alisson", "serra": "Joan Jordán"}
SUBS_90 = dict(SUBS_68, rafa="Schjelderup", bah="Durán", dahl="Banjaqui", jansson="Moustier", schappo="Chernev",
               antonetti="Encada")
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
    d.text((W / 2, CY0 + CH * 0.31), "2–3", font=fonte(SERIFA_N, 230 * esc), fill=CREME + (255,), anchor="mm")
    d.text((W / 2, CY0 + CH * 0.44), "ESTRELA  ·  BENFICA", font=fonte(SANS_SB, 40), fill=CORAL + (255,),
           anchor="mm")
    k = suave((t - 0.15) / 0.35)
    if k > 0:
        d.text((W / 2, CY0 + CH * 0.55), "remates à baliza do Estrela", font=fonte(SANS, 34),
               fill=CREME_70 + (int(255 * k),), anchor="mm")
        d.text((W / 2, CY0 + CH * 0.62), "2  =  2 golos", font=fonte(SERIFA_N, 76), fill=CREME + (int(255 * k),),
               anchor="mm")
    k = suave((t - 2.9) / 0.3)
    if k > 0:
        _chip(d, W / 2, CY0 + CH * 0.73, "E um frango pelo meio", CORAL, k)
    q.im.paste(ov, (0, 0), ov)


def polemicas(v, q, t):
    _fundo(q, t)
    d = q.d
    k = suave((t - 0.1) / 0.35)
    if k > 0:
        d.text((W / 2, CY0 + 80), "Lances polémicos", font=fonte(SERIFA_N, 66), fill=CREME + (int(255 * k),),
               anchor="mm")
    lances = [("15'", "Penálti sobre Pavlidis?", "o árbitro mandou seguir", 2.2, 6.2),
              ("–", "Tomás Araújo sobre Antonetti?", "o árbitro mandou seguir", 4.0, 6.4),
              ("76'", "Soares choca com Antonetti", "golo legal", 8.1, 11.1)]
    for i, (m, txt, sub, ti, ts) in enumerate(lances):
        kk = suave((t - ti) / 0.3)
        if kk <= 0:
            continue
        y = CY0 + 210 + i * 125
        d.rounded_rectangle((80, y - 52, W - 80, y + 52), radius=22, fill=(36, 34, 32, int(255 * kk)),
                            outline=(70, 66, 60, int(255 * kk)), width=2)
        d.text((125, y), m, font=fonte(SERIFA_N, 44), fill=CORAL + (int(255 * kk),), anchor="lm")
        d.text((225, y - 14), txt, font=fonte(SANS_SB, 36), fill=CREME + (int(255 * kk),), anchor="lm")
        ks = suave((t - ts) / 0.3)
        if ks > 0:
            d.text((225, y + 26), sub, font=fonte(SANS, 28), fill=CREME_70 + (int(255 * ks),), anchor="lm")
    k = suave((t - 11.8) / 0.3)
    if k > 0:
        esc = 1.12 - 0.12 * k
        y = CY0 + 680
        d.rounded_rectangle((80, y - 105, W - 80, y + 105), radius=30, fill=CORAL + (int(255 * k),))
        d.text((W / 2, y - 45), "A polémica da noite", font=fonte(SANS_SB, 36), fill=(20, 20, 19, int(255 * k)),
               anchor="mm")
        d.text((W / 2, y + 25), "Samuel Soares, 76'", font=fonte(SERIFA_N, int(70 * esc)),
               fill=(20, 20, 19, int(255 * k)), anchor="mm")
        d.text((W / 2, y + 80), "saída fora de tempo no 2–2", font=fonte(SANS, 30), fill=(20, 20, 19, int(220 * k)),
               anchor="mm")
    k = suave((t - 1.0) / 0.3)
    if k > 0:
        d.text((W / 2, CY0 + 905), "Árbitro: António Nobre · nota 6 no Observador", font=fonte(SANS, 26),
               fill=CREME_70 + (int(200 * k),), anchor="mm")


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
        d.text((W / 2 + 30, CY0 + 335), "Vitória do Benfica · 75%", font=fonte(SERIFA_N, 56),
               fill=CREME + (int(255 * k),), anchor="mm")
    k = suave((t - 2.35) / 0.25)
    if k > 0:
        _visto(d, W / 2 - 340, CY0 + 337, k, r=28)
    k = suave((t - 2.95) / 0.3)
    if k > 0:
        _chip(d, W / 2, CY0 + 455, "Dicas na rede vizinha · link na bio", CORAL, k, tam=34)
    k = suave((t - 5.3) / 0.3)
    if k > 0:
        d.text((W / 2, CY0 + 570), "Samuel Soares na baliza?", font=fonte(SERIFA_N, 64),
               fill=CREME + (int(255 * k),), anchor="mm")
    for i, (letra, txt) in enumerate((("A", "Continua"), ("B", "Muda"))):
        kk = suave((t - 5.6 - i * 0.15) / 0.35)
        if kk <= 0:
            continue
        cx, cy = W / 2 + (-215 if i == 0 else 215), CY0 + 740
        d.rounded_rectangle((cx - 195, cy - 85, cx + 195, cy + 85), radius=28, fill=(44, 42, 39, int(255 * kk)),
                            outline=(80, 76, 70, int(255 * kk)), width=2)
        d.text((cx, cy - 22), letra, font=fonte(SERIFA_N, 58), fill=CREME + (int(255 * kk),), anchor="mm")
        d.text((cx, cy + 40), txt, font=fonte(SANS_SB, 38), fill=CREME + (int(255 * kk),), anchor="mm")
    k = suave((t - 7.6) / 0.3)
    if k > 0:
        d.text((W / 2, CY0 + 900), "Comenta A ou B", font=fonte(SANS_SB, 46), fill=CORAL + (int(255 * k),),
               anchor="mm")


# ------------------------------------------------------------------ cenas

REF_VOZ = [6.22, 8.40, 9.26, 6.50, 7.79, 15.13, 8.91, 8.92]


def construir():
    v = Video("Estrela", "Benfica", abrev=("EST", "BEN"), fonte_txt="Ilustração · dados ESPN, Maisfutebol, A Bola e O Jogo")
    v.folga, v.bpm = 0.35, 112
    v.sp["fora"] = sprite(17, BRANCO, (20, 20, 19), 3)   # Estrela: branco
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
    c = cena(6.7, "Estrela 2–3 Benfica", 0, jogadores({}), placar="2–3", minuto="FIM", sobreposicao=gancho,
             nomes=False)
    c.t_capa = 4.4

    # 1. o 5-4-1 do Estrela; o Benfica circula por fora e marca de fora da área (26')
    pos1 = {"dahl": (0.10, 0.40), "bah": (0.90, 0.40), "lenglet": (0.36, 0.56), "araujo": (0.64, 0.56),
            "palhinha": (0.42, 0.45), "sudakov": (0.62, 0.44), "echeverri": (0.50, 0.34), "rafa": (0.80, 0.30),
            "pavlidis": (0.50, 0.20)}
    mov = {"prestianni": vai((0.20, 0.30), (0.36, 0.22), T(4.0), T(4.7), 99),
           "linck": [(0, 0.5, 0.03), (T(5.2), 0.48, 0.03), (T(5.6), 0.53, 0.02)]}
    bola = [(0, 0.42, 0.45), (T(1.7), 0.42, 0.45), (T(2.3), 0.11, 0.40), (T(2.4), 0.11, 0.40), (T(2.9), 0.42, 0.45),
            (T(3.0), 0.42, 0.45), (T(3.4), 0.62, 0.44), (T(3.5), 0.62, 0.44), (T(4.0), 0.89, 0.40),
            (T(4.1), 0.89, 0.40), (T(4.6), 0.50, 0.34), (T(4.7), 0.50, 0.34), (T(5.0), 0.36, 0.225),
            (T(5.2), 0.36, 0.225), (T(5.6), 0.545, 0.0)]
    cena(8.9, "O 5-4-1 do Estrela", 1, jogadores(pos1, mov, mostrar={"prestianni", "echeverri"}),
         bola=bola, placar="0–0", minuto="26'", vista="ataque", golo=(T(5.65), "0–1", "Prestianni"),
         formas=[{"tipo": "zona", "pts": [(0.03, 0.07), (0.97, 0.07), (0.97, 0.32), (0.03, 0.32)], "cor": BRANCO,
                  "rotulo": "bloco 5-4-1", "t0": T(0.5), "t1": T(2.0)},
                 {"tipo": "rotulo", "x": 0.5, "y": 0.52, "texto": "por fora do bloco", "cor": CORAL, "t0": T(2.0),
                  "t1": T(4.4)}],
         setas=[{"pts": [(0.42, 0.45), (0.11, 0.40)], "t0": T(1.7), "t1": T(2.3), "tipo": "passe"},
                {"pts": [(0.62, 0.44), (0.89, 0.40)], "t0": T(3.5), "t1": T(4.0), "tipo": "passe"},
                {"pts": [(0.50, 0.34), (0.36, 0.225)], "t0": T(4.7), "t1": T(5.0), "tipo": "passe"},
                {"pts": [(0.36, 0.225), (0.545, 0.005)], "t0": T(5.2), "t1": T(5.6), "tipo": "remate"}],
         destaques=[("echeverri", T(4.1), T(4.9)), ("prestianni", T(4.9), 8.9)])

    # 2. 48': linhas afastadas e a transição do Estrela (vista da defesa do Benfica)
    pos2 = {"soares": (0.5, 0.975), "dahl": (0.16, 0.80), "lenglet": (0.38, 0.86), "araujo": (0.62, 0.86),
            "bah": (0.84, 0.80), "palhinha": (0.40, 0.58), "sudakov": (0.60, 0.56), "echeverri": (0.50, 0.48),
            "prestianni": (0.20, 0.50), "rafa": (0.80, 0.50), "pavlidis": (0.50, 0.44),
            "antonetti": (0.46, 0.80), "marcus": (0.22, 0.70), "serra": (0.42, 0.62), "linck": (0.5, 0.05)}
    mov = {"stoica": [(0, 0.76, 0.58), (T(5.2), 0.77, 0.58), (T(6.2), 0.84, 0.74), (99, 0.84, 0.74)],
           "rsoares": [(0, 0.90, 0.60), (T(5.4), 0.90, 0.62), (T(6.4), 0.88, 0.82), (99, 0.88, 0.82)],
           "zvonarek": [(0, 0.56, 0.70), (T(6.0), 0.56, 0.72), (T(7.0), 0.53, 0.885), (99, 0.53, 0.885)],
           "araujo": vai((0.62, 0.86), (0.70, 0.86), T(6.0), T(7.0), 99),
           "soares": [(0, 0.5, 0.975), (T(7.5), 0.52, 0.975), (T(7.9), 0.47, 0.975)]}
    bola = [(0, 0.76, 0.59), (T(5.2), 0.77, 0.59), (T(6.2), 0.84, 0.75), (T(6.25), 0.84, 0.75), (T(6.5), 0.875, 0.815),
            (T(6.6), 0.875, 0.815), (T(7.1), 0.53, 0.88), (T(7.6), 0.53, 0.88), (T(7.9), 0.455, 1.0)]
    cena(9.8, "2.ª parte · as linhas", 2, jogadores(pos2, mov, mostrar={"stoica", "rsoares", "zvonarek"}),
         bola=bola, placar="0–1", minuto="48'", vista="defesa", golo=(T(7.95), "1–1", "Zvonarek"),
         formas=[{"tipo": "entre", "de": ["palhinha", "sudakov"], "ate": ["lenglet", "araujo"], "cor": CORAL,
                  "rotulo": "linhas afastadas", "t0": T(2.8), "t1": T(5.0)}],
         setas=[{"pts": [(0.77, 0.59), (0.84, 0.75)], "t0": T(5.2), "t1": T(6.2), "tipo": "conducao"},
                {"pts": [(0.90, 0.62), (0.88, 0.82)], "t0": T(5.4), "t1": T(6.4), "tipo": "corrida_fora"},
                {"pts": [(0.875, 0.815), (0.53, 0.88)], "t0": T(6.6), "t1": T(7.1), "tipo": "passe"},
                {"pts": [(0.53, 0.88), (0.455, 0.995)], "t0": T(7.6), "t1": T(7.9), "tipo": "remate"}],
         destaques=[("stoica", T(5.0), T(6.4)), ("zvonarek", T(6.6), 9.8)])

    # 3. 68': cruzamento rasteiro de Rafa Silva, autogolo de Schappo
    pos3 = {"linck": (0.5, 0.03), "scholze": (0.12, 0.14), "luan": (0.36, 0.10), "jansson": (0.46, 0.13),
            "rsoares": (0.84, 0.14), "marcus": (0.22, 0.26), "serra": (0.42, 0.25), "zvonarek": (0.60, 0.24),
            "stoica": (0.80, 0.27), "antonetti": (0.50, 0.40), "pavlidis": (0.52, 0.10), "echeverri": (0.50, 0.28),
            "sudakov": (0.62, 0.36), "palhinha": (0.44, 0.44), "dahl": (0.10, 0.36), "bah": (0.90, 0.36)}
    mov = {"prestianni": [(0, 0.28, 0.26)],
           "rafa": vai((0.80, 0.24), (0.74, 0.13), T(0.8), T(2.2), 99),
           "schappo": [(0, 0.60, 0.12), (T(2.8), 0.59, 0.11), (T(3.4), 0.51, 0.065), (99, 0.51, 0.065)],
           "linck": [(0, 0.5, 0.03), (T(3.0), 0.55, 0.03), (T(3.7), 0.53, 0.025)]}
    bola = [(0, 0.28, 0.26), (T(1.6), 0.28, 0.26), (T(2.2), 0.735, 0.135), (T(2.6), 0.735, 0.135), (T(3.35), 0.52, 0.07),
            (T(3.7), 0.47, 0.0)]
    cena(7.0, "68' · o autogolo", 3, jogadores(pos3, mov, mostrar={"prestianni", "rafa", "schappo"}, subs=SUBS_68),
         bola=bola, placar="1–1", minuto="68'", vista="ataque", golo=(T(3.75), "1–2", "Schappo (p.b.)"),
         setas=[{"pts": [(0.28, 0.26), (0.735, 0.135)], "t0": T(1.6), "t1": T(2.2), "tipo": "passe"},
                {"pts": [(0.735, 0.135), (0.52, 0.07)], "t0": T(2.6), "t1": T(3.35), "tipo": "passe"}],
         destaques=[("rafa", T(1.8), T(3.0)), ("schappo", T(3.0), 7.0)])

    # 4. 76': o frango. Livre de Joan Jordán, Samuel Soares sai fora de tempo, Antonetti de cabeça
    pos4 = {"dahl": (0.20, 0.88), "lenglet": (0.40, 0.90), "araujo": (0.58, 0.89), "bah": (0.68, 0.86),
            "palhinha": (0.48, 0.86), "sudakov": (0.36, 0.84), "echeverri": (0.62, 0.80), "prestianni": (0.30, 0.74),
            "rafa": (0.80, 0.74), "pavlidis": (0.50, 0.66), "luan": (0.42, 0.86), "schappo": (0.54, 0.84),
            "zvonarek": (0.60, 0.86), "marcus": (0.30, 0.82), "stoica": (0.46, 0.66), "rsoares": (0.70, 0.62),
            "scholze": (0.20, 0.62), "jansson": (0.50, 0.56), "linck": (0.5, 0.05)}
    mov = {"serra": [(0, 0.84, 0.72)],
           "soares": [(0, 0.50, 0.975), (T(3.4), 0.50, 0.975), (T(4.6), 0.565, 0.905), (99, 0.565, 0.905)],
           "antonetti": [(0, 0.46, 0.84), (T(3.6), 0.46, 0.84), (T(5.2), 0.47, 0.935), (99, 0.47, 0.935)]}
    bola = [(0, 0.835, 0.72), (T(3.6), 0.835, 0.72), (T(4.1), 0.72, 0.80), (T(4.65), 0.60, 0.88), (T(5.2), 0.475, 0.93),
            (T(5.3), 0.475, 0.93), (T(5.7), 0.545, 1.0)]
    cena(8.4, "76' · o frango", 4, jogadores(pos4, mov, mostrar={"serra", "soares", "antonetti"}, subs=SUBS_68),
         bola=bola, placar="1–2", minuto="76'", vista="defesa", golo=(T(5.75), "2–2", "Antonetti"),
         formas=[{"tipo": "rotulo", "x": 0.78, "y": 0.95, "texto": "fora de tempo", "cor": CORAL, "t0": T(4.3),
                  "t1": 8.4}],
         setas=[{"pts": [(0.835, 0.72), (0.72, 0.80), (0.60, 0.88), (0.475, 0.93)], "t0": T(3.6), "t1": T(5.2),
                 "tipo": "passe"},
                {"pts": [(0.50, 0.975), (0.565, 0.905)], "t0": T(3.4), "t1": T(4.6), "tipo": "corrida"},
                {"pts": [(0.475, 0.93), (0.545, 0.995)], "t0": T(5.3), "t1": T(5.7), "tipo": "remate"}],
         destaques=[("serra", T(1.2), T(3.6)), ("soares", T(2.4), 8.4)])

    # 5. lances polémicos (não houve)
    c = cena(15.6, "Os lances polémicos", 5, jogadores({}), placar="2–2", minuto="", sobreposicao=polemicas,
             nomes=False)
    c.t_capa = 14.0

    # 6. 90+4': trivela de Schjelderup, Pavlidis de primeira
    pos6 = {"linck": (0.5, 0.03), "scholze": (0.14, 0.13), "luan": (0.38, 0.10), "jansson": (0.56, 0.11),
            "schappo": (0.46, 0.13), "rsoares": (0.82, 0.14), "marcus": (0.26, 0.24), "serra": (0.44, 0.24),
            "zvonarek": (0.62, 0.22), "stoica": (0.78, 0.30), "antonetti": (0.52, 0.36), "echeverri": (0.64, 0.20),
            "bah": (0.42, 0.18), "prestianni": (0.78, 0.26), "sudakov": (0.38, 0.34), "palhinha": (0.48, 0.40),
            "dahl": (0.12, 0.40)}
    mov = {"rafa": vai((0.16, 0.30), (0.20, 0.22), T(0.6), T(1.6), 99),
           "pavlidis": [(0, 0.53, 0.17), (T(3.6), 0.53, 0.16), (T(4.8), 0.50, 0.075), (99, 0.50, 0.075)],
           "linck": [(0, 0.5, 0.03), (T(4.5), 0.53, 0.03), (T(5.0), 0.49, 0.03)]}
    bola = [(0, 0.38, 0.34), (T(1.0), 0.38, 0.34), (T(1.6), 0.20, 0.225), (T(3.8), 0.20, 0.225), (T(4.3), 0.33, 0.12),
            (T(4.8), 0.495, 0.075), (T(4.9), 0.505, 0.075), (T(5.2), 0.50, 0.0)]
    cena(10.9, "90+4' · a trivela", 6, jogadores(pos6, mov, mostrar={"rafa", "pavlidis"}, subs=SUBS_90),
         bola=bola, placar="2–2", minuto="90+4'", vista="ataque", golo=(T(5.25), "2–3", "Pavlidis"),
         sobreposicao=tat.citacao(T(6.9), "“Os adeptos gostam de ver, mas eu não gostei nada.”", "Marco Silva"),
         setas=[{"pts": [(0.38, 0.34), (0.20, 0.225)], "t0": T(1.0), "t1": T(1.6), "tipo": "passe"},
                {"pts": [(0.20, 0.225), (0.33, 0.12), (0.495, 0.075)], "t0": T(3.8), "t1": T(4.8), "tipo": "passe"},
                {"pts": [(0.53, 0.16), (0.50, 0.08)], "t0": T(3.6), "t1": T(4.8), "tipo": "corrida"},
                {"pts": [(0.495, 0.075), (0.50, 0.005)], "t0": T(4.9), "t1": T(5.2), "tipo": "remate"}],
         destaques=[("rafa", T(1.4), T(4.0)), ("pavlidis", T(4.0), 6.8)])

    # 7. Agente Claudio + pergunta
    c = cena(9.5, "", 7, jogadores({}), placar="2–3", minuto="FIM", sobreposicao=cartao_agente, nomes=False)
    c.t_capa = 8.2
    # 8. fecho com humor
    cenas.append(cena_fecho(jogadores({}), placar="2–3", frase=5))
    return v, cenas
