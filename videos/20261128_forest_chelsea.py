"""Nottingham Forest 3-2 Chelsea, Premier League, City Ground, 27 nov 2026. Gancho: 65% da bola e 3.ª derrota seguida.

Fontes (verificadas a 28 nov 2026; o ESPN e os sites das crónicas estavam bloqueados na sessão, por isso só
resumos de pesquisa web — nada além do que as fontes concordam):
- Resultado e marcadores: Igor Jesus ~5' (de primeira, cruzamento de Muñoz), Gibbs-White (2: 1.º de grande
  penalidade aos 51', falta de Fofana — Sky Sports, Playmaker Stats), Emegha (2: ~54' e 89'/90'; entrou ao
  intervalo) — Sky Sports, NBC Sports, Playmaker Stats, Yahoo, Goal. DIVERGÊNCIA: uma fonte (Journal Nigeria)
  descreve o 2.º de Gibbs-White como livre aos 72'; não digo como nem em que minuto (o 3-1 fica sem minuto) e o
  minuto do 2.º de Emegha é 89' ou 90' (mostro 89').
- Números: Chelsea com 65% de posse (Goal/crónicas), "estéril", defesa exposta nas transições. Uma só fonte
  (análise tipo theunderdog): o Forest pressionou alto nas alas — digo "segundo as crónicas".
- Contexto: 3.ª derrota seguida do Chelsea na Liga (Blueprint, Yahoo); Forest sobe ao 14.º lugar, 3 pontos acima da
  descida (Sky/Yahoo). Treinador do Forest: Glasner; do Chelsea: Xabi Alonso.
- Declaração de Alonso (Sky/NBC): «At this level, you can't concede this much and that's why we are losing games.»
- Agente Claudio: sem cartão (não há dica nem previsão certa publicada neste jogo).
Cores: Forest vermelho, Chelsea azul (ilustração, sem jogadas desenhadas).
"""
from PIL import Image, ImageDraw

from quadro_tatico import (cena_fecho, sprite, CORAL, CREME, CREME_70, CY0, CH, W, Cena, Video, fonte, suave,
                           SERIFA_N, SANS, SANS_SB)

import porto_napoli as base
import benfica_lech as bl
import taca_grandes as tg

_ov = base._ov
_fundo, _chip = bl._fundo, bl._chip
jogadores = tg.jogadores


def vazio():
    return jogadores("slb", {})


VERMELHO = (200, 40, 50)
AZUL = (40, 80, 170)
BRANCO = (236, 234, 226)

TIPO = "jogo"
TEMA = "Forest 3-2 Chelsea: 65% da bola e 3.ª derrota seguida"
MATCH_ID = "20261127-E0-nottmforest-chelsea"
HORA = "12:30"
POSTS = {
    "tiktok": "65% da bola, 2 golos marcados… e a 3.ª derrota seguida 😳 O Chelsea em Nottingham, explicado no "
              "quadro. #chelsea #premierleague #futebol #agenteclaudio #futeboltiktok",
    "instagram": "O Chelsea teve 65% da bola em Nottingham, marcou 2 e perdeu 3-2. A 3.ª derrota seguida. "
                 "Muita posse, pouca ponta, e uma defesa que se abre a cada transição. Previsões no link da bio. "
                 "#chelsea #premierleague #futebol #agenteclaudio +18",
    "youtube": {"titulo": "Forest 3-2 Chelsea: 65% da bola e 3.ª derrota #shorts",
                "descricao": "O Chelsea teve 65% da bola e perdeu 3-2 no City Ground. O jogo explicado no quadro "
                             "tático.\n#chelsea #premierleague #futebol #agenteclaudio"},
    "x": "65% de posse. 2 golos marcados. 3 derrotas seguidas. O Chelsea em Nottingham, explicado em 60 "
         "segundos. #Chelsea #PremierLeague",
}

VI = 0.15


def T(x):
    return x + VI


FALAS = [
    ("O Chelsea teve quase dois terços da bola... marcou duas vezes... e perdeu pela terceira vez seguida.",
     "O Chelsea teve quase 2/3 da bola… marcou 2 vezes… e perdeu pela 3.ª vez seguida."),
    ("Aos cinco minutos, o Igor Jesus fecha um cruzamento do Munhoz de primeira e abre o marcador. "
     "Depois do intervalo, grande penalidade, e o Guibs-Uáit faz o segundo. Fácil? Calma.",
     "Aos 5', o Igor Jesus fecha um cruzamento do Muñoz de primeira e abre o marcador. "
     "Depois do intervalo, grande penalidade, e o Gibbs-White faz o 2-0. Fácil? Calma."),
    ("O Emega entra ao intervalo e, três minutos depois, faz o dois-um. O Guibs-Uáit volta a marcar, o Emega "
     "ainda reduz já no fim... mas só deu para o três-dois.",
     "O Emegha entra ao intervalo e, 3 minutos depois, faz o 2-1. O Gibbs-White volta a marcar, o Emegha "
     "ainda reduz já no fim… mas só deu para o 3-2."),
    ("Sessenta e cinco por cento da bola, mas uma posse sem ponta, e uma defesa que se abria em cada "
     "transição. Segundo as crónicas, o Forest apertou lá em cima, nas alas.",
     "65% da bola, mas uma posse sem ponta e uma defesa que se abria em cada transição. "
     "Segundo as crónicas, o Forest apertou lá em cima, nas alas."),
    ("No fim, o Xabi Alonso foi direto: a este nível, não se pode sofrer tantos golos, e é por isso que "
     "estão a perder jogos.",
     "No fim, o Xabi Alonso foi direto: «A este nível, não se pode sofrer tantos golos, e é por isso que "
     "estamos a perder jogos.»"),
    ("O Forest sobe ao décimo quarto lugar, a três pontos da descida. O Chelsea soma a terceira derrota seguida. "
     "As previsões do Agente Claudio estão na rede vizinha, link na bio.",
     "O Forest sobe ao 14.º lugar, a 3 pontos da descida. O Chelsea soma a 3.ª derrota seguida. "
     "As previsões do Agente Claudio estão na rede vizinha, link na bio."),
    ("O problema do Chelsea é a defesa, ou a falta de ponta? Comenta.",
     "O problema do Chelsea é a defesa ou a falta de ponta? Comenta."),
]
FECHO = ("[laughs] Manda isto ao teu amigo que tem sempre a bola toda... e perde sempre a conversa por três a dois.",
         ["Manda isto ao teu amigo", "que tem sempre a bola toda", "e perde a conversa por |3–2|."])

REF_VOZ = [5.80, 9.98, 8.88, 9.38, 6.84, 9.82, 3.76]


def _painel(q, titulo):
    ov = _ov(q)
    d = ImageDraw.Draw(ov)
    d.rectangle((0, CY0 + CH * 0.06, W, CY0 + CH * 0.90), fill=(20, 20, 19, 238))
    d.text((W / 2, CY0 + 120), titulo, font=fonte(SANS_SB, 34), fill=CORAL + (255,), anchor="mm")
    return ov, d


def gancho(v, q, t):
    """Frame 0 já com o contraste: 65% de bola vs 2–3."""
    ov, d = _painel(q, "FOREST · CHELSEA")
    pulso = 1 + 0.04 * max(0, 1 - t / 0.4)
    d.text((W / 2 - 230, CY0 + 290), "65%", font=fonte(SERIFA_N, int(150 * pulso)), fill=CREME + (255,),
           anchor="mm")
    d.text((W / 2 - 230, CY0 + 390), "de bola", font=fonte(SANS_SB, 38), fill=CREME_70 + (255,), anchor="mm")
    d.text((W / 2 + 230, CY0 + 290), "2–3", font=fonte(SERIFA_N, int(150 * pulso)), fill=CORAL + (255,),
           anchor="mm")
    d.text((W / 2 + 230, CY0 + 390), "no marcador", font=fonte(SANS_SB, 38), fill=CORAL + (255,), anchor="mm")
    k = suave((t - T(2.6)) / 0.25)
    if k > 0:
        d.text((W / 2, CY0 + 540), "3.ª derrota seguida", font=fonte(SERIFA_N, 64), fill=CREME + (int(255 * k),),
               anchor="mm")
    k = suave((t - T(4.0)) / 0.25)
    if k > 0:
        d.text((W / 2, CY0 + 660), "Premier League", font=fonte(SANS_SB, 40), fill=CORAL + (int(255 * k),),
               anchor="mm")
    q.im.paste(ov, (0, 0), ov)


def golos_a(v, q, t):
    ov, d = _painel(q, "FOREST 2–0 CHELSEA")
    linhas = [("5'", "Igor Jesus", "de primeira · cruz. Muñoz", T(0.8)),
              ("51'", "Gibbs-White", "grande penalidade", T(5.7))]
    for i, (m, nome, ex, ti) in enumerate(linhas):
        kk = suave((t - ti) / 0.25)
        if kk <= 0:
            continue
        al = int(255 * kk)
        y = CY0 + 330 + i * 180
        d.rounded_rectangle((90, y - 70, W - 90, y + 70), radius=22, fill=(36, 34, 32, al),
                            outline=(70, 66, 60, al), width=2)
        d.text((150, y), m, font=fonte(SANS_SB, 50), fill=CORAL + (al,), anchor="lm")
        d.text((300, y - 16), nome, font=fonte(SERIFA_N, 56), fill=CREME + (al,), anchor="lm")
        d.text((300, y + 36), ex, font=fonte(SANS, 28), fill=CREME_70 + (al,), anchor="lm")
    k = suave((t - T(8.3)) / 0.25)
    if k > 0:
        d.text((W / 2, CY0 + 760), "Fácil? Calma.", font=fonte(SERIFA_N, 70), fill=CREME + (int(255 * k),),
               anchor="mm")
    q.im.paste(ov, (0, 0), ov)


def golos_b(v, q, t):
    ov, d = _painel(q, "A REAÇÃO DO CHELSEA")
    linhas = [("54'", "Emegha", "2–1 · entrou ao intervalo", T(2.9), CORAL),
              ("", "Gibbs-White", "3–1 · bis", T(3.8), CREME),
              ("89'", "Emegha", "3–2 · já no fim", T(5.8), CORAL)]
    for i, (m, nome, ex, ti, cor) in enumerate(linhas):
        kk = suave((t - ti) / 0.25)
        if kk <= 0:
            continue
        al = int(255 * kk)
        y = CY0 + 290 + i * 160
        d.rounded_rectangle((90, y - 62, W - 90, y + 62), radius=22, fill=(36, 34, 32, al),
                            outline=(70, 66, 60, al), width=2)
        if m:
            d.text((150, y), m, font=fonte(SANS_SB, 46), fill=cor + (al,), anchor="lm")
        d.text((300, y - 14), nome, font=fonte(SERIFA_N, 52), fill=CREME + (al,), anchor="lm")
        d.text((300, y + 36), ex, font=fonte(SANS, 28), fill=CREME_70 + (al,), anchor="lm")
    k = suave((t - T(7.9)) / 0.25)
    if k > 0:
        d.text((W / 2, CY0 + 790), "3–2 final", font=fonte(SERIFA_N, 76), fill=CREME + (int(255 * k),),
               anchor="mm")
    q.im.paste(ov, (0, 0), ov)


def numeros(v, q, t):
    ov, d = _painel(q, "CHELSEA · NOTTINGHAM")
    for i, (num, txt, ti) in enumerate((("65%", "posse de bola", T(0.1)), ("2", "golos marcados", T(1.2)),
                                        ("3", "golos sofridos", T(3.0)), ("3", "derrotas seguidas", T(5.8)))):
        kk = suave((t - ti) / 0.25)
        if kk <= 0:
            continue
        al = int(255 * kk)
        cx = W / 2 + (-210 if i % 2 == 0 else 210)
        cy = CY0 + 330 + (i // 2) * 270
        d.rounded_rectangle((cx - 190, cy - 110, cx + 190, cy + 110), radius=26, fill=(36, 34, 32, al),
                            outline=(CORAL if i >= 2 else (70, 66, 60)) + (al,), width=3)
        d.text((cx, cy - 25), num, font=fonte(SERIFA_N, 100), fill=(CORAL if i >= 2 else CREME) + (al,),
               anchor="mm")
        d.text((cx, cy + 62), txt, font=fonte(SANS_SB, 32), fill=CREME_70 + (al,), anchor="mm")
    k = suave((t - T(7.4)) / 0.25)
    if k > 0:
        d.text((W / 2, CY0 + 800), "muita bola, pouca ponta", font=fonte(SERIFA_N, 54),
               fill=CREME + (int(255 * k),), anchor="mm")
    q.im.paste(ov, (0, 0), ov)


def palavras(v, q, t):
    ov, d = _painel(q, "DEPOIS DO JOGO")
    kk = suave((t - T(0.6)) / 0.25)
    if kk > 0:
        al = int(255 * kk)
        y = CY0 + 400
        d.rounded_rectangle((70, y - 190, W - 70, y + 190), radius=26, fill=(36, 34, 32, al),
                            outline=(70, 66, 60, al), width=2)
        d.text((W / 2, y - 130), "Xabi Alonso", font=fonte(SANS_SB, 36), fill=CORAL + (al,), anchor="mm")
        for j, l in enumerate(("«A este nível,", "não se pode sofrer", "tantos golos»")):
            d.text((W / 2, y - 50 + j * 78), l, font=fonte(SERIFA_N, 56), fill=CREME + (al,), anchor="mm")
    k = suave((t - T(4.4)) / 0.25)
    if k > 0:
        d.text((W / 2, CY0 + 760), "«é por isso que perdemos jogos»", font=fonte(SERIFA_N, 42),
               fill=CREME_70 + (int(255 * k),), anchor="mm")
    q.im.paste(ov, (0, 0), ov)


def tabela(v, q, t):
    ov, d = _painel(q, "PREMIER LEAGUE")
    k = suave((t - T(1.0)) / 0.25)
    if k > 0:
        d.text((W / 2, CY0 + 300), "14.º", font=fonte(SERIFA_N, 190), fill=CREME + (int(255 * k),), anchor="mm")
        d.text((W / 2, CY0 + 440), "Forest · a 3 pontos da descida", font=fonte(SANS_SB, 38),
               fill=CORAL + (int(255 * k),), anchor="mm")
    k = suave((t - T(3.3)) / 0.25)
    if k > 0:
        d.text((W / 2, CY0 + 580), "Chelsea: 3.ª derrota seguida", font=fonte(SERIFA_N, 54),
               fill=CREME + (int(255 * k),), anchor="mm")
    k = suave((t - T(6.5)) / 0.25)
    if k > 0:
        _chip(d, W / 2, CY0 + 730, "Previsões na rede vizinha · link na bio", CORAL, k, tam=34)
    q.im.paste(ov, (0, 0), ov)


def pergunta(v, q, t):
    _fundo(q, t)
    d = q.d
    d.text((W / 2, CY0 + 170), "O problema do Chelsea?", font=fonte(SERIFA_N, 62), fill=CREME + (255,),
           anchor="mm")
    for i, (letra, l1, l2, ti, cor) in enumerate((("A", "A defesa", "3 golos sofridos", T(0.9), AZUL),
                                                  ("B", "A falta de ponta", "muita bola, pouca ponta", T(1.6),
                                                   (90, 86, 80)))):
        kk = suave((t - ti) / 0.25)
        if kk <= 0:
            continue
        al = int(255 * kk)
        cx, cy = W / 2 + (-215 if i == 0 else 215), CY0 + 410
        d.rounded_rectangle((cx - 200, cy - 125, cx + 200, cy + 125), radius=28, fill=cor + (al,))
        d.text((cx, cy - 50), letra, font=fonte(SERIFA_N, 66), fill=CREME + (al,), anchor="mm")
        d.text((cx, cy + 25), l1, font=fonte(SANS_SB, 34), fill=CREME + (al,), anchor="mm")
        d.text((cx, cy + 72), l2, font=fonte(SANS, 24), fill=CREME + (al,), anchor="mm")
    k = suave((t - T(2.4)) / 0.25)
    if k > 0:
        d.text((W / 2, CY0 + 680), "Comenta A ou B", font=fonte(SANS_SB, 50), fill=CORAL + (int(255 * k),),
               anchor="mm")


def construir():
    v = Video("Nottingham Forest", "Chelsea", abrev=("NFO", "CHE"),
              fonte_txt="Ilustração · dados ESPN, Sky Sports, NBC Sports e Yahoo")
    v.folga, v.bpm = 0.25, 120
    v.sp["slb"] = sprite(17, VERMELHO, BRANCO, 3)
    v.sp["adv"] = sprite(17, AZUL, BRANCO, 3)
    cenas = []

    def cena(dur, titulo, i, sobre):
        voz, leg = FALAS[i]
        c = Cena(dur, titulo, "", vazio(), voz=voz, legenda=leg, voz_ini=VI, sobreposicao=sobre, nomes=False)
        c.voz_ref = REF_VOZ[i]
        c.abrev = ("NFO", "CHE")
        c.t_capa = dur - 0.2
        cenas.append(c)
        return c

    cena(6.2, "Premier League · City Ground", 0, gancho)
    cena(10.6, "Forest 2–0 Chelsea", 1, golos_a)
    cena(9.4, "Forest 3–2 Chelsea", 2, golos_b)
    cena(9.8, "Chelsea · números", 3, numeros)
    cena(7.4, "Depois do jogo", 4, palavras)
    cena(10.2, "Premier League", 5, tabela)
    cena(4.4, "", 6, pergunta)
    cenas.append(cena_fecho(vazio(), frase=FECHO))
    return v, cenas


MEMES = [
    {"modelo": "reacao", "topo": "O Chelsea com 65% da bola em Nottingham:", "desenho": "bola",
     "baixo": "2 golos marcados, 3 sofridos", "fala": "A bola era deles. Os pontos, do Forest.",
     "legenda": "Muita bola, pouca ponta ⚽ #chelsea #premierleague #futebol #agenteclaudio +18"},
    {"modelo": "expectativa", "esq": "O que a posse de bola prometia", "dir": "O que o marcador mostrou",
     "desenho_esq": "bola", "desenho_dir": "placar:3–2", "baixo": "Posse de bola: 65%. Pontos: 0.",
     "fala": "Eu só medi a posse. Os pontos eram com o Forest.",
     "legenda": "Expectativa vs realidade no City Ground 📉 #chelsea #premierleague #futebol #agenteclaudio +18"},
]
