"""Viktoria Plzen 4-0 Benfica, Liga Europa (5.ª jornada), 26 nov 2026. Gancho: 69% de bola e 3 golos em 4 minutos.

Fontes (verificadas a 26 nov 2026; o ESPN e os sites das crónicas estavam bloqueados na sessão, por isso só
resumos de pesquisa web — nada além do que as fontes concordam):
- Resultado e marcadores: Hrosovsky 30', Adu 43', Kabongo 44' e 46' — RTP, Foot Africa, VAVEL, 112.ua, Sofascore,
  ZeroZero. Assistências: Kabongo -> Adu; Hrosovsky -> Kabongo (2.º golo do Kabongo). 1.º golo: o Benfica perdeu a
  bola à saída de um pontapé de baliza (resumo de pesquisa). 3–0 ao intervalo.
- Números: o Benfica com cerca de 69% de posse (uma fonte: 69,3%); 9 remates antes do intervalo, só 2 à baliza
  (resumo de pesquisa). Público (via pesquisa): domínio territorial mas muitos passes falhados.
- Contexto: 1.ª derrota do Benfica na prova, 12 pontos, 4.º lugar (RTP). As fontes divergem no estádio
  (Doosan Arena vs Stadion Mesta Plzne): não o digo. Uma fonte (RTP via pesquisa) falava em "24 jogos sem marcar" —
  as outras não confirmam, não uso.
- Declarações: Marco Silva "noite horrível para nós" e "abre-olhos" (Sport TV/A Bola); jogo quase perdido "em seis,
  sete minutos". João Palhinha: "Menosprezámos o adversário" (A Bola, título).
- Agente Claudio: o modelo dava só 16% à vitória do Plzen (falhou): não aparece cartão do Agente.
Cores: Benfica vermelho; Plzen vermelho/azul (não confirmado), desenhado a branco. Jogadas = ilustrações.
"""
from PIL import Image, ImageDraw

from quadro_tatico import (cena_fecho, sprite, CORAL, CREME, CREME_70, CY0, CH, W, Cena, Video, fonte, suave,
                           SERIFA_N, SANS, SANS_SB)

import porto_napoli as base
import benfica_lech as bl
import taca_grandes as tg

vai, _ov = base.vai, base._ov
_fundo, _chip = bl._fundo, bl._chip
jogadores = tg.jogadores


def vazio():
    return jogadores("slb", {})

VERMELHO = (200, 40, 50)
BRANCO = (236, 234, 226)

TIPO = "jogo"
TEMA = "Plzen 4-0 Benfica: 69% de bola e 3 golos em 4 minutos"
MATCH_ID = "20261126-UEL-viktoriaplzen-benfica"
HORA = "12:30"
POSTS = {
    "tiktok": "69% da bola e 3 golos sofridos em 4 minutos 😳 O Benfica em Plzen, explicado no quadro. "
              "#benfica #ligaeuropa #futebol #agenteclaudio #futeboltiktok",
    "instagram": "O Benfica teve 69% da bola em Plzen… e levou 3 golos em 4 minutos antes do intervalo. "
                 "Quem manda no jogo nem sempre manda no resultado. Previsões no link da bio. "
                 "#benfica #ligaeuropa #futebol #agenteclaudio #slb +18",
    "youtube": {"titulo": "Plzen 4-0 Benfica: 3 golos em 4 minutos #shorts",
                "descricao": "O Benfica teve 69% da bola e perdeu 4-0 em Plzen. O jogo explicado no quadro tático."
                             "\n#benfica #ligaeuropa #futebol #agenteclaudio"},
    "x": "69% de posse. 9 remates na 1.ª parte. 3 golos sofridos em 4 minutos. O Benfica em Plzen, "
         "explicado em 60 segundos. #Benfica #LigaEuropa",
}

VI = 0.15


def T(x):
    return x + VI


FALAS = [
    ("O Benfica teve quase setenta por cento da bola... e levou três golos em quatro minutos.",
     "O Benfica teve quase 70% da bola… e levou 3 golos em 4 minutos."),
    ("Tudo começa num pontapé de baliza: o Benfica perde a bola à saída, e o Hrosóvski abre o marcador. "
     "Fácil? Calma.",
     "Tudo começa num pontapé de baliza: o Benfica perde a bola à saída e o Hrosovský abre o marcador. "
     "Fácil? Calma."),
    ("Aos quarenta e três, o Cabongo serve o Adu. Aos quarenta e quatro, o Cabongo marca. Aos quarenta e seis, "
     "volta a marcar. Três golos em quatro minutos.",
     "Aos 43', o Kabongo serve o Adu. Aos 44', o Kabongo marca. Aos 46', volta a marcar. 3 golos em 4 minutos."),
    ("O Benfica teve nove remates na primeira parte, só dois à baliza, e passou o jogo a falhar passes. "
     "Muita bola, pouca ponta.",
     "O Benfica teve 9 remates na 1.ª parte, só 2 à baliza, e passou o jogo a falhar passes. "
     "Muita bola, pouca ponta."),
    ("No fim, o Marco Silva falou numa noite horrível, e o Palhinha foi direto: menosprezámos o adversário.",
     "No fim, o Marco Silva falou numa noite horrível e o Palhinha foi direto: «Menosprezámos o adversário.»"),
    ("Primeira derrota na prova, doze pontos, quarto lugar. Ainda dá para o oitavo, mas o aviso ficou dado. "
     "As previsões do Agente Claudio estão na rede vizinha, link na bio.",
     "1.ª derrota na prova, 12 pontos, 4.º lugar. Ainda dá para o top 8, mas o aviso ficou dado. "
     "As previsões do Agente Claudio estão na rede vizinha, link na bio."),
    ("O que pesou mais: menosprezar o adversário, ou os passes falhados? Comenta.",
     "O que pesou mais: menosprezar o adversário ou os passes falhados? Comenta."),
]
FECHO = ("[laughs] Manda isto ao teu amigo que domina a conversa toda... e perde sempre a discussão.",
         ["Manda isto ao teu amigo", "que domina a conversa toda", "e perde sempre a |discussão|."])

REF_VOZ = [5.08, 6.41, 8.55, 7.01, 5.85, 9.54, 4.42]


def gancho(v, q, t):
    """Frame 0 já com o contraste: 69% de bola vs 4–0."""
    ov = _ov(q)
    d = ImageDraw.Draw(ov)
    d.rectangle((0, CY0 + CH * 0.06, W, CY0 + CH * 0.90), fill=(20, 20, 19, 238))
    d.text((W / 2, CY0 + 120), "PLZEN · BENFICA", font=fonte(SANS_SB, 34), fill=CORAL + (255,), anchor="mm")
    pulso = 1 + 0.04 * max(0, 1 - t / 0.4)
    d.text((W / 2 - 230, CY0 + 290), "69%", font=fonte(SERIFA_N, int(150 * pulso)), fill=CREME + (255,),
           anchor="mm")
    d.text((W / 2 - 230, CY0 + 390), "de bola", font=fonte(SANS_SB, 38), fill=CREME_70 + (255,), anchor="mm")
    d.text((W / 2 + 230, CY0 + 290), "0–4", font=fonte(SERIFA_N, int(150 * pulso)), fill=CORAL + (255,),
           anchor="mm")
    d.text((W / 2 + 230, CY0 + 390), "no marcador", font=fonte(SANS_SB, 38), fill=CORAL + (255,), anchor="mm")
    k = suave((t - T(2.6)) / 0.25)
    if k > 0:
        d.text((W / 2, CY0 + 540), "3 golos em 4 minutos", font=fonte(SERIFA_N, 64), fill=CREME + (int(255 * k),),
               anchor="mm")
    k = suave((t - T(4.0)) / 0.25)
    if k > 0:
        d.text((W / 2, CY0 + 660), "antes do intervalo", font=fonte(SANS_SB, 40), fill=CORAL + (int(255 * k),),
               anchor="mm")
    q.im.paste(ov, (0, 0), ov)


def golos3(v, q, t):
    ov = _ov(q)
    d = ImageDraw.Draw(ov)
    d.rectangle((0, CY0 + CH * 0.06, W, CY0 + CH * 0.90), fill=(20, 20, 19, 234))
    d.text((W / 2, CY0 + 130), "3 GOLOS EM 4 MINUTOS", font=fonte(SANS_SB, 36), fill=CORAL + (255,), anchor="mm")
    linhas = [("43'", "Adu", "assist. Kabongo", T(0.3)), ("44'", "Kabongo", "", T(2.7)),
              ("46'", "Kabongo", "assist. Hrosovsky", T(4.7))]
    for i, (m, nome, ex, ti) in enumerate(linhas):
        kk = suave((t - ti) / 0.25)
        if kk <= 0:
            continue
        al = int(255 * kk)
        y = CY0 + 290 + i * 150
        d.rounded_rectangle((90, y - 58, W - 90, y + 58), radius=22, fill=(36, 34, 32, al),
                            outline=(70, 66, 60, al), width=2)
        d.text((150, y), m, font=fonte(SANS_SB, 46), fill=CORAL + (al,), anchor="lm")
        d.text((300, y - (12 if ex else 0)), nome, font=fonte(SERIFA_N, 54), fill=CREME + (al,), anchor="lm")
        if ex:
            d.text((300, y + 34), ex, font=fonte(SANS, 28), fill=CREME_70 + (al,), anchor="lm")
    k = suave((t - T(6.4)) / 0.25)
    if k > 0:
        d.text((W / 2, CY0 + 790), "0–3 ao intervalo", font=fonte(SERIFA_N, 66), fill=CREME + (int(255 * k),),
               anchor="mm")
    q.im.paste(ov, (0, 0), ov)


def numeros(v, q, t):
    ov = _ov(q)
    d = ImageDraw.Draw(ov)
    d.rectangle((0, CY0 + CH * 0.06, W, CY0 + CH * 0.90), fill=(20, 20, 19, 234))
    d.text((W / 2, CY0 + 130), "BENFICA · 1.ª PARTE", font=fonte(SANS_SB, 36), fill=CORAL + (255,), anchor="mm")
    for i, (num, txt, ti) in enumerate((("69%", "posse de bola", T(0.1)), ("9", "remates", T(0.8)),
                                        ("2", "à baliza", T(2.4)), ("0", "golos", T(4.2)))):
        kk = suave((t - ti) / 0.25)
        if kk <= 0:
            continue
        al = int(255 * kk)
        cx = W / 2 + (-210 if i % 2 == 0 else 210)
        cy = CY0 + 330 + (i // 2) * 270
        d.rounded_rectangle((cx - 190, cy - 110, cx + 190, cy + 110), radius=26, fill=(36, 34, 32, al),
                            outline=(CORAL if i == 3 else (70, 66, 60)) + (al,), width=3)
        d.text((cx, cy - 25), num, font=fonte(SERIFA_N, 100), fill=(CORAL if i == 3 else CREME) + (al,),
               anchor="mm")
        d.text((cx, cy + 62), txt, font=fonte(SANS_SB, 32), fill=CREME_70 + (al,), anchor="mm")
    k = suave((t - T(5.1)) / 0.25)
    if k > 0:
        d.text((W / 2, CY0 + 800), "muita bola, pouca ponta", font=fonte(SERIFA_N, 54),
               fill=CREME + (int(255 * k),), anchor="mm")
    q.im.paste(ov, (0, 0), ov)


def palavras(v, q, t):
    ov = _ov(q)
    d = ImageDraw.Draw(ov)
    d.rectangle((0, CY0 + CH * 0.06, W, CY0 + CH * 0.90), fill=(20, 20, 19, 234))
    d.text((W / 2, CY0 + 130), "DEPOIS DO JOGO", font=fonte(SANS_SB, 36), fill=CORAL + (255,), anchor="mm")
    for i, (quem, frase, ti) in enumerate((("Marco Silva", "«Uma noite horrível»", T(0.6)),
                                           ("João Palhinha", "«Menosprezámos o adversário»", T(2.9)))):
        kk = suave((t - ti) / 0.25)
        if kk <= 0:
            continue
        al = int(255 * kk)
        y = CY0 + 350 + i * 270
        d.rounded_rectangle((70, y - 100, W - 70, y + 100), radius=26, fill=(36, 34, 32, al),
                            outline=(70, 66, 60, al), width=2)
        d.text((W / 2, y - 50), quem, font=fonte(SANS_SB, 34), fill=CORAL + (al,), anchor="mm")
        d.text((W / 2, y + 25), frase, font=fonte(SERIFA_N, 46), fill=CREME + (al,), anchor="mm")
    q.im.paste(ov, (0, 0), ov)


def tabela(v, q, t):
    ov = _ov(q)
    d = ImageDraw.Draw(ov)
    d.rectangle((0, CY0 + CH * 0.06, W, CY0 + CH * 0.90), fill=(20, 20, 19, 234))
    d.text((W / 2, CY0 + 130), "LIGA EUROPA · 5 JORNADAS", font=fonte(SANS_SB, 34), fill=CORAL + (255,),
           anchor="mm")
    k = suave((t - T(1.9)) / 0.25)
    if k > 0:
        d.text((W / 2, CY0 + 300), "4.º", font=fonte(SERIFA_N, 190), fill=CREME + (int(255 * k),), anchor="mm")
        d.text((W / 2, CY0 + 440), "12 pontos · 1.ª derrota", font=fonte(SANS_SB, 40),
               fill=CORAL + (int(255 * k),), anchor="mm")
    k = suave((t - T(3.4)) / 0.25)
    if k > 0:
        d.text((W / 2, CY0 + 580), "ainda dentro do top 8", font=fonte(SERIFA_N, 54),
               fill=CREME + (int(255 * k),), anchor="mm")
    k = suave((t - T(5.4)) / 0.25)
    if k > 0:
        _chip(d, W / 2, CY0 + 730, "Previsões na rede vizinha · link na bio", CORAL, k, tam=34)
    q.im.paste(ov, (0, 0), ov)


def pergunta(v, q, t):
    _fundo(q, t)
    d = q.d
    d.text((W / 2, CY0 + 170), "O que pesou mais?", font=fonte(SERIFA_N, 62), fill=CREME + (255,), anchor="mm")
    for i, (letra, l1, l2, ti, cor) in enumerate((("A", "Menosprezar", "o adversário", T(0.9), VERMELHO),
                                                  ("B", "Passes falhados", "muita bola, pouca ponta", T(1.6),
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
    v = Video("Viktoria Plzen", "Benfica", abrev=("PLZ", "SLB"),
              fonte_txt="Ilustração · dados ESPN, RTP, Sofascore, A Bola e Público")
    v.folga, v.bpm = 0.25, 120
    v.sp["slb"] = sprite(17, VERMELHO, BRANCO, 3)
    v.sp["adv"] = sprite(17, BRANCO, (60, 60, 60), 3)
    cenas = []

    def cena(dur, titulo, i, jog, **kw):
        voz, leg = FALAS[i]
        c = Cena(dur, titulo, "", jog, voz=voz, legenda=leg, voz_ini=VI, **kw)
        c.voz_ref = REF_VOZ[i]
        c.abrev = ("PLZ", "SLB")
        cenas.append(c)
        return c

    c = cena(5.6, "Liga Europa · 5.ª jornada", 0, vazio(), sobreposicao=gancho, nomes=False)
    c.t_capa = 5.4

    # 30': o Benfica (g_, baliza em baixo) perde a bola à saída do pontapé de baliza; Hrosovsky marca
    pos = {"g_d1": (0.22, 0.86), "g_d3": (0.60, 0.88), "g_d4": (0.80, 0.85), "g_m1": (0.38, 0.78),
           "g_m2": (0.52, 0.74), "g_m3": (0.66, 0.76), "a_m1": (0.24, 0.78), "a_m4": (0.76, 0.80),
           "a_a2": (0.60, 0.84), "a_a1": (0.46, 0.86)}
    mov = {"a_m3": [(0, 0.56, 0.60), (T(1.6), 0.56, 0.60), (T(2.3), 0.50, 0.80), (99, 0.50, 0.80)],
           "g_d2": vai((0.40, 0.88), (0.34, 0.90), T(2.0), T(3.0), 99)}
    bola = [(0, 0.50, 0.97), (T(0.8), 0.50, 0.97), (T(1.4), 0.56, 0.62), (T(2.3), 0.50, 0.80),
            (T(3.4), 0.47, 1.0)]
    cena(7.0, "Plzen 0–0 Benfica · 30'", 1, jogadores("slb", pos, mov, {"a_m3": "Hrosovsky"}),
         placar="0–0", minuto="30'", vista="defesa", golo=(T(3.5), "1–0", "Hrosovsky"), bola=bola,
         formas=[{"tipo": "rotulo", "x": 0.74, "y": 0.96, "texto": "pontapé de baliza", "cor": CORAL, "t0": T(0.3),
                  "t1": T(1.8)},
                 {"tipo": "rotulo", "x": 0.5, "y": 0.50, "texto": "bola perdida", "cor": BRANCO, "t0": T(1.5),
                  "t1": T(2.8)}],
         setas=[{"pts": [(0.50, 0.97), (0.56, 0.62)], "t0": T(0.8), "t1": T(1.4), "tipo": "passe"},
                {"pts": [(0.50, 0.80), (0.47, 1.0)], "t0": T(3.0), "t1": T(3.4), "tipo": "remate"}],
         destaques=[("a_m3", T(1.6), T(4.2))])

    c = cena(9.0, "Plzen 3–0 Benfica", 2, vazio(), placar="0–1", minuto="43'", sobreposicao=golos3, nomes=False)
    c.t_capa = 8.8

    c = cena(7.6, "Benfica · 1.ª parte", 3, vazio(), sobreposicao=numeros, nomes=False)
    c.t_capa = 7.4

    c = cena(6.4, "Depois do jogo", 4, vazio(), sobreposicao=palavras, nomes=False)
    c.t_capa = 6.2

    c = cena(10.0, "Liga Europa", 5, vazio(), sobreposicao=tabela, nomes=False)
    c.t_capa = 9.8

    c = cena(4.6, "", 6, vazio(), sobreposicao=pergunta, nomes=False)
    c.t_capa = 4.4
    cenas.append(cena_fecho(vazio(), frase=FECHO))
    return v, cenas


MEMES = [
    {"modelo": "reacao", "topo": "O Benfica com 69% da bola em Plzen:", "desenho": "bola",
     "baixo": "3 golos em 4 minutos antes do intervalo", "fala": "A bola era nossa. O resultado, nem por isso.",
     "legenda": "Muita bola, pouca ponta ⚽ #benfica #ligaeuropa #futebol #agenteclaudio +18"},
    {"modelo": "expectativa", "esq": "O que a posse de bola prometia", "dir": "O que o marcador mostrou",
     "desenho_esq": "bola", "desenho_dir": "placar:0–4", "baixo": "Posse de bola: 69%. Golos: 0.",
     "fala": "Eu só calculei a bola. Os golos eram com eles.",
     "legenda": "Expectativa vs realidade em Plzen 📉 #benfica #ligaeuropa #futebol #agenteclaudio +18"},
]
