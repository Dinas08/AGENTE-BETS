"""Antevisão FC Porto x Sporting, Liga Portugal (12.ª jornada), Dragão, domingo 29 nov 2026, 20h30.

Fontes (verificadas a 27 nov 2026; diadejogo.pt, flashscore.pt e ZeroZero estavam bloqueados na sessão, por isso só
resumos de pesquisa web — Sapo 25/11, Diário de Jogo 26/11, Notícias ao Minuto, Flashscore — e os dados do projeto):
- Porto: Smalling e Vasco Sousa a recuperar de lesões, três baixas no boletim clínico (Sapo, Flashscore). O terceiro
  nome diverge entre fontes: NÃO o digo, só "mais uma baixa".
- Sporting: treina com todos os jogadores disponíveis (Diário de Jogo, Notícias ao Minuto).
- Treinadores, classificação e árbitro: fontes divergem ou só uma fonte, por isso NÃO os uso no vídeo.
- Resultados recentes (base de dados do projeto): Porto 4-1 Napoli, 2-1 Guimarães (fora), 1-0 Feyenoord (fora);
  Sporting 1-0 Moreirense, 2-2 Man United.
- Agente Claudio: Porto 46%, empate 30%, Sporting 24%; golos esperados 1,35–0,95. É antevisão: sem "acertou". Sem odds.
"""
from PIL import ImageDraw

from quadro_tatico import (cena_fecho, sprite, CORAL, CREME, CREME_70, CY0, CH, W, Cena, Video, fonte, suave,
                           SERIFA_N, SANS, SANS_SB)

import porto_napoli as base
import benfica_lech as bl
import taca_grandes as tg

_ov, PFP = base._ov, base.PFP
_fundo, _chip = bl._fundo, bl._chip
vazio = tg.vazio
VERDE_SCP, VERMELHO = tg.VERDE_SCP, tg.VERMELHO
VI = 0.15


def T(x):
    return x + VI



FALAS = [
    ("Domingo, no Dragão: o Porto tem três baixas... e o Sporting não tem nenhuma. Mesmo assim, só um é favorito.",
     "Domingo, no Dragão: o Porto tem 3 baixas… e o Sporting não tem nenhuma. Mesmo assim, só um é favorito."),
    ("No Porto, o Smalling e o Vasco Sousa ainda estão a recuperar de lesão, e há mais uma baixa no boletim clínico.",
     "No Porto, Smalling e Vasco Sousa ainda recuperam de lesão, e há mais 1 baixa no boletim clínico."),
    ("Já o Sporting treina com todos os jogadores disponíveis. Plantel inteiro, e um clássico pela frente.",
     "Já o Sporting treina com todos os jogadores disponíveis. Plantel inteiro e um clássico pela frente."),
    ("Mas o Porto vem forte: em casa, marcou oito golos em dois jogos. Quatro a zero ao Estoril e quatro a um ao "
     "Napoli. O Dragão tem sido festa.",
     "Mas o Porto vem forte: em casa, marcou 8 golos em 2 jogos. 4–0 ao Estoril e 4–1 ao Napoli. O Dragão tem "
     "sido festa."),
    ("E o Sporting fora? Não sofreu: dois a zero em Casa Pia e um a zero ao Shakhtar. Mas empatou a dois com o "
     "United em Alvalade.",
     "E o Sporting fora? Não sofreu: 2–0 em Casa Pia e 1–0 ao Shakhtar. Mas empatou 2–2 com o United em Alvalade."),
    ("O Agente Claudio dá quarenta e seis por cento ao Porto, trinta ao empate e vinte e quatro ao Sporting. Golos "
     "esperados: pouco mais de um, contra menos de um. As previsões estão na rede vizinha, link na bio.",
     "O Agente Claudio dá 46% ao Porto, 30% ao empate e 24% ao Sporting. Golos esperados: pouco mais de 1 contra "
     "menos de 1. As previsões estão na rede vizinha, link na bio."),
    ("Quem sorri no Dragão? Porto, ou empate e Sporting? Comenta.",
     "Quem sorri no Dragão? Porto ou empate/Sporting? Comenta."),
]
FECHO = ("[laughs] Manda isto ao teu amigo que tem o plantel todo disponível... e ainda arranja desculpa.",
         ["Manda isto ao teu amigo", "que tem o |plantel todo|", "e ainda arranja |desculpa|."])
REF_VOZ = [6.18, 6.35, 5.8, 7.95, 7.12, 11.63, 3.54]
AZUL_FCP = (40, 90, 170)


def _painel(q):
    ov = _ov(q)
    d = ImageDraw.Draw(ov)
    d.rectangle((0, CY0 + CH * 0.06, W, CY0 + CH * 0.90), fill=(20, 20, 19, 238))
    return ov, d


def gancho(v, q, t):
    ov, d = _painel(q)
    d.text((W / 2, CY0 + 120), "ANTEVISÃO · O CLÁSSICO", font=fonte(SANS_SB, 34), fill=CORAL + (255,), anchor="mm")
    pulso = 1 + 0.04 * max(0, 1 - t / 0.4)
    for cx, txt, cor in ((W / 2 - 280, "PORTO", AZUL_FCP), (W / 2 + 280, "SPORTING", VERDE_SCP)):
        d.rounded_rectangle((cx - 150, CY0 + 220, cx + 150, CY0 + 340), radius=26, fill=cor + (255,))
        d.text((cx, CY0 + 280), txt, font=fonte(SANS_SB, int(46 * pulso)), fill=CREME + (255,), anchor="mm")
    d.text((W / 2, CY0 + 280), "vs", font=fonte(SERIFA_N, 60), fill=CREME + (255,), anchor="mm")
    d.text((W / 2 - 280, CY0 + 410), "3 baixas", font=fonte(SERIFA_N, 64), fill=CORAL + (255,), anchor="mm")
    d.text((W / 2 + 280, CY0 + 410), "0 baixas", font=fonte(SERIFA_N, 64), fill=CREME + (255,), anchor="mm")
    k = suave((t - T(4.7)) / 0.3)
    if k > 0:
        d.text((W / 2, CY0 + 590), "e só um é favorito", font=fonte(SERIFA_N, 72), fill=CREME + (int(255 * k),),
               anchor="mm")
    q.im.paste(ov, (0, 0), ov)


def baixas(v, q, t):
    ov, d = _painel(q)
    d.text((W / 2, CY0 + 130), "PORTO · BOLETIM CLÍNICO", font=fonte(SANS_SB, 34), fill=CORAL + (255,),
           anchor="mm")
    lin = [("Smalling", "lesão", T(0.7)), ("Vasco Sousa", "lesão", T(1.4)), ("+ 1 baixa", "boletim clínico", T(4.2))]
    for i, (nome, mot, ti) in enumerate(lin):
        kk = suave((t - ti) / 0.25)
        if kk <= 0:
            continue
        al = int(255 * kk)
        y = CY0 + 300 + i * 130
        d.rounded_rectangle((120, y - 48, W - 120, y + 48), radius=18, fill=(36, 34, 32, al))
        d.text((170, y), nome, font=fonte(SERIFA_N, 52), fill=CREME + (al,), anchor="lm")
        d.text((W - 170, y), mot, font=fonte(SANS_SB, 32), fill=CORAL + (al,), anchor="rm")
    q.im.paste(ov, (0, 0), ov)


def casa(v, q, t):
    ov, d = _painel(q)
    d.text((W / 2, CY0 + 130), "SPORTING · BOLETIM CLÍNICO", font=fonte(SANS_SB, 34), fill=CORAL + (255,),
           anchor="mm")
    k = suave((t - T(0.8)) / 0.3)
    if k > 0:
        d.text((W / 2, CY0 + 360), "0", font=fonte(SERIFA_N, 260), fill=VERDE_SCP + (int(255 * k),), anchor="mm")
        d.text((W / 2, CY0 + 560), "baixas", font=fonte(SERIFA_N, 80), fill=CREME + (int(255 * k),), anchor="mm")
    k = suave((t - T(3.0)) / 0.3)
    if k > 0:
        d.text((W / 2, CY0 + 680), "plantel todo disponível", font=fonte(SANS_SB, 42),
               fill=CREME_70 + (int(255 * k),), anchor="mm")
    q.im.paste(ov, (0, 0), ov)


def _duo(titulo, itens, cor, final=None, tf=0):
    def f(v, q, t):
        ov, d = _painel(q)
        d.text((W / 2, CY0 + 130), titulo, font=fonte(SANS_SB, 34), fill=CORAL + (255,), anchor="mm")
        for i, (txt, ti) in enumerate(itens):
            kk = suave((t - T(ti)) / 0.25)
            if kk > 0:
                _chip(d, W / 2, CY0 + 300 + i * 150, txt, cor, kk, tam=54)
        if final:
            k = suave((t - T(tf)) / 0.3)
            if k > 0:
                d.text((W / 2, CY0 + 300 + len(itens) * 150 + 40), final, font=fonte(SERIFA_N, 64),
                       fill=CREME + (int(255 * k),), anchor="mm")
        q.im.paste(ov, (0, 0), ov)
    return f


numeros = _duo("PORTO · EM CASA", [("4–0 Estoril", 3.8), ("4–1 Napoli", 4.7)], AZUL_FCP, "8 golos em 2 jogos", 2.4)
fora = _duo("SPORTING · FORA", [("2–0 Casa Pia", 2.0), ("1–0 Shakhtar", 3.0)], VERDE_SCP, "2 jogos sem sofrer", 1.5)


def previsao(v, q, t):
    _fundo(q, t)
    d = q.d
    if PFP.exists():
        from PIL import Image
        k = suave((t - 0.05) / 0.3)
        r = int(90 * (0.85 + 0.15 * k))
        im = Image.open(PFP).convert("RGB").resize((2 * r, 2 * r), Image.LANCZOS)
        m = Image.new("L", (2 * r, 2 * r), 0)
        ImageDraw.Draw(m).ellipse((0, 0, 2 * r, 2 * r), fill=int(255 * k))
        q.im.paste(im, (int(W / 2 - r), int(CY0 + 100 - r)), m)
    d.text((W / 2, CY0 + 240), "PREVISÃO DO AGENTE", font=fonte(SANS_SB, 32), fill=CORAL + (255,), anchor="mm")
    for i, (lab, pc, cor, ti) in enumerate((("Porto", 46, AZUL_FCP, T(1.0)), ("Empate", 30, (110, 106, 100), T(2.3)),
                                            ("Sporting", 24, VERDE_SCP, T(3.6)))):
        kk = suave((t - ti) / 0.3)
        if kk <= 0:
            continue
        al = int(255 * kk)
        y = CY0 + 350 + i * 120
        d.text((110, y), lab, font=fonte(SANS_SB, 36), fill=CREME + (al,), anchor="lm")
        larg = (W - 560) * pc / 46 * kk
        d.rounded_rectangle((330, y - 30, 330 + max(10, larg), y + 30), radius=14, fill=cor + (al,))
        d.text((W - 90, y), f"{pc}%", font=fonte(SERIFA_N, 48), fill=CREME + (al,), anchor="rm")
    k = suave((t - T(4.3)) / 0.25)
    if k > 0:
        d.text((W / 2, CY0 + 740), "golos esperados  1,4 – 0,9", font=fonte(SANS_SB, 36),
               fill=CREME + (int(255 * k),), anchor="mm")
    k = suave((t - T(7.8)) / 0.25)
    if k > 0:
        _chip(d, W / 2, CY0 + 830, "Previsões na rede vizinha · link na bio", CORAL, k, tam=32)


def pergunta(v, q, t):
    _fundo(q, t)
    d = q.d
    d.text((W / 2, CY0 + 170), "Quem sorri no Dragão?", font=fonte(SERIFA_N, 62), fill=CREME + (255,), anchor="mm")
    for i, (letra, l1, l2, ti, cor) in enumerate((("A", "Porto", "vitória", T(1.0), AZUL_FCP),
                                                  ("B", "Empate / Sporting", "ponto ou mais", T(1.6), VERDE_SCP))):
        kk = suave((t - ti) / 0.25)
        if kk <= 0:
            continue
        al = int(255 * kk)
        cx, cy = W / 2 + (-215 if i == 0 else 215), CY0 + 410
        d.rounded_rectangle((cx - 200, cy - 125, cx + 200, cy + 125), radius=28, fill=cor + (al,))
        d.text((cx, cy - 50), letra, font=fonte(SERIFA_N, 66), fill=CREME + (al,), anchor="mm")
        d.text((cx, cy + 25), l1, font=fonte(SANS_SB, 32), fill=CREME + (al,), anchor="mm")
        d.text((cx, cy + 72), l2, font=fonte(SANS, 28), fill=CREME + (al,), anchor="mm")
    k = suave((t - T(2.4)) / 0.25)
    if k > 0:
        d.text((W / 2, CY0 + 680), "Comenta A ou B", font=fonte(SANS_SB, 50), fill=CORAL + (int(255 * k),),
               anchor="mm")


def construir():
    v = Video("Porto", "Sporting", abrev=("FCP", "SCP"),
              fonte_txt="Ilustração · dados ESPN, fontes da imprensa e Agente Claudio")
    v.folga, v.bpm = 0.25, 120
    v.sp['fcp'] = sprite(17, AZUL_FCP, (236, 234, 226), 3)
    v.sp['adv'] = sprite(17, VERDE_SCP, (236, 234, 226), 3)
    cenas = []
    for dur, i, so, tit in ((6.4, 0, gancho, "Antevisão · Dragão"), (6.8, 1, baixas, "Porto · baixas"),
                            (6.3, 2, casa, "Sporting · plantel"), (8.4, 3, numeros, "Porto · em casa"),
                            (7.6, 4, fora, "Sporting · fora"), (12.2, 5, previsao, "Previsão do Agente"),
                            (4.2, 6, pergunta, "")):
        voz, leg = FALAS[i]
        c = Cena(dur, tit, "", vazio(), voz=voz, legenda=leg, voz_ini=VI, sobreposicao=so, nomes=False)
        c.voz_ref = REF_VOZ[i]
        c.abrev = ("FCP", "SCP")
        c.t_capa = dur - 0.2
        cenas.append(c)
    cenas.append(cena_fecho(vazio(), placar="–", minuto="20h30", frase=FECHO))
    return v, cenas


TIPO = "antevisao"
TEMA = "Porto x Sporting: o Dragão com 3 baixas de um lado e 0 do outro"
MATCH_ID = "20261129-P1-porto-splisbon"
HORA = "17:30"
POSTS = {
    "tiktok": "Clássico no Dragão: Porto com 3 baixas, Sporting com 0… e só um é favorito 👀 Quem sorri? "
              "#futebol #agenteclaudio #fcporto #sporting #futeboltiktok",
    "instagram": "Porto x Sporting, domingo às 20h30: o Porto sem Smalling e Vasco Sousa (+1 baixa), o Sporting com "
                 "o plantel todo. O Agente Claudio dá 46% ao Porto, 30% empate, 24% Sporting. A tua aposta: A ou B? "
                 "#fcporto #sporting #ligaportugal #agenteclaudio +18",
    "youtube": {"titulo": "Porto x Sporting: 3 baixas contra 0 e só um favorito #shorts",
                "descricao": "Antevisão do clássico no Dragão com a previsão do Agente Claudio: 46% Porto, 30% "
                             "empate, 24% Sporting.\n#fcporto #sporting #ligaportugal #agenteclaudio"},
    "x": "Porto x Sporting, domingo 20h30: Porto com 3 baixas, Sporting sem nenhuma. Agente Claudio: 46% Porto, "
         "30% empate, 24% Sporting. #FCPorto #SportingCP",
}
MEMES = [
    {"modelo": "reacao", "topo": "Porto com 3 baixas, Sporting com 0:", "desenho": "bola",
     "baixo": "O Agente Claudio, a fazer contas ao clássico", "fala": "46%, 30% e 24%. Já só falta jogar.",
     "legenda": "O clássico está calculado… falta só jogá-lo 🤖⚽ #fcporto #sporting #ligaportugal "
                "#agenteclaudio +18"},
    {"modelo": "expectativa", "esq": "O que o modelo calculou", "dir": "O que o coração sente aos 85'",
     "desenho_esq": "placar:1–0", "desenho_dir": "relogio:85'", "baixo": "Clássicos não se preveem. Sofrem-se.",
     "fala": "Eu só calculo. Vocês é que sofrem.",
     "legenda": "Expectativa vs realidade nos clássicos ⏱️ #fcporto #sporting #futebol #agenteclaudio +18"},
]
