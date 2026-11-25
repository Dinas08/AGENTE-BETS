"""Antevisão Sporting x Man United, Liga dos Campeões (5.ª jornada), Alvalade, 25 nov 2026, 20h00.

Fontes (verificadas a 25 nov 2026; ESPN, ZeroZero e Bola na Rede estavam bloqueados na sessão, por isso só resumos
de pesquisa web e os dados do projeto — digo apenas o que as fontes concordam):
- Man United sem Cunha (castigo, vermelho contra a Roma), Ugarte, Baleba e Šeško (lesões); Rashford e Shaw em dúvida;
  vem de um 0-4 em Liverpool — Bola na Rede, ESPN Brasil, Goal, Memesita, manutd.com e ajustes do projeto.
- Sporting: Debast e Nuno Santos — fontes divergem (ZeroZero diz fora, manutd.com diz que treinaram): digo "dúvidas".
- Árbitro: Szymon Marciniak (Bola na Rede / ZeroZero via pesquisa).
- Classificação e treinadores: as fontes divergem, por isso NÃO os uso no vídeo.
- Agente Claudio: previsão do modelo vitória do Sporting 54%, empate 23%, United 23%; golos esperados 1,95–1,28.
  É antevisão: não mostro "acertou". Sem odds.
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
    ("O United chega a Alvalade com quatro baixas... e a vir de uma derrota por quatro a zero.",
     "O United chega a Alvalade com 4 baixas… e a vir de uma derrota por 4–0."),
    ("Sem o Cunha, castigado, e sem o Ugarte, o Baleba e o Chéchko, lesionados. O Rashford e o Shaw são dúvidas.",
     "Sem o Cunha, castigado, e sem Ugarte, Baleba e Šeško, lesionados. Rashford e Shaw são dúvidas."),
    ("Do outro lado, o Sporting joga em casa, com o Debast e o Nuno Santos em dúvida. Árbitro: o polaco Marciniak.",
     "Do outro lado, o Sporting joga em casa, com Debast e Nuno Santos em dúvida. Árbitro: o polaco Marciniak."),
    ("E os números do United não ajudam: em três jogos recentes, um quatro a quatro, um três a dois e um zero a "
     "quatro. Dez golos sofridos. Abre-se a porta.",
     "E os números do United não ajudam: em 3 jogos recentes, 4–4, 3–2 e 0–4. 10 golos sofridos. Abre-se a porta."),
    ("O Sporting vem da Taça com um quatro a zero em casa, e Alvalade costuma ser território verde. Mas contra o "
     "Moreirense só ganhou por um a zero: em casa, ganha, mas sem exagerar.",
     "O Sporting vem de um 4–0 em casa na Taça, e Alvalade costuma ser território verde. Mas com o Moreirense só "
     "ganhou 1–0: em casa ganha, mas sem exagerar."),
    ("O Agente Claudio dá cinquenta e quatro por cento ao Sporting, vinte e três ao empate e vinte e três ao "
     "United. Golos esperados: quase dois contra pouco mais de um. As previsões estão na rede vizinha, link na bio.",
     "O Agente Claudio dá 54% ao Sporting, 23% ao empate e 23% ao United. Golos esperados: quase 2 contra pouco "
     "mais de 1. As previsões estão na rede vizinha, link na bio."),
    ("Quem sai de Alvalade a sorrir? Sporting, ou empate e United? Comenta.",
     "Quem sai de Alvalade a sorrir? Sporting ou empate/United? Comenta."),
]
FECHO = ("[laughs] Manda isto ao teu amigo que chega sempre sem quatro titulares... e ainda quer ganhar.",
         ["Manda isto ao teu amigo", "que chega sem |4 titulares|", "e ainda quer |ganhar|."])
REF_VOZ = [5.14, 6.13, 6.24, 8.55, 9.98, 11.96, 4.09]


def gancho(v, q, t):
    ov = _ov(q)
    d = ImageDraw.Draw(ov)
    d.rectangle((0, CY0 + CH * 0.06, W, CY0 + CH * 0.90), fill=(20, 20, 19, 238))
    d.text((W / 2, CY0 + 120), "ANTEVISÃO · CHAMPIONS", font=fonte(SANS_SB, 34), fill=CORAL + (255,), anchor="mm")
    pulso = 1 + 0.04 * max(0, 1 - t / 0.4)
    for cx, txt, cor in ((W / 2 - 280, "SPORTING", VERDE_SCP), (W / 2 + 280, "UNITED", VERMELHO)):
        d.rounded_rectangle((cx - 150, CY0 + 220, cx + 150, CY0 + 340), radius=26, fill=cor + (255,))
        d.text((cx, CY0 + 280), txt, font=fonte(SANS_SB, int(46 * pulso)), fill=CREME + (255,), anchor="mm")
    d.text((W / 2, CY0 + 280), "vs", font=fonte(SERIFA_N, 60), fill=CREME + (255,), anchor="mm")
    d.text((W / 2 + 280, CY0 + 400), "4 baixas", font=fonte(SERIFA_N, 64), fill=CORAL + (255,), anchor="mm")
    k = suave((t - T(2.6)) / 0.3)
    if k > 0:
        d.text((W / 2, CY0 + 560), "e vem de um 0–4", font=fonte(SERIFA_N, 72), fill=CREME + (int(255 * k),),
               anchor="mm")
    q.im.paste(ov, (0, 0), ov)


def baixas(v, q, t):
    ov = _ov(q)
    d = ImageDraw.Draw(ov)
    d.rectangle((0, CY0 + CH * 0.06, W, CY0 + CH * 0.90), fill=(20, 20, 19, 238))
    d.text((W / 2, CY0 + 130), "UNITED · AUSENTES", font=fonte(SANS_SB, 34), fill=CORAL + (255,), anchor="mm")
    lin = [("Cunha", "castigo", T(0.9), False), ("Ugarte", "lesão", T(2.2), False),
           ("Baleba", "lesão", T(2.8), False), ("Šeško", "lesão", T(3.4), False),
           ("Rashford", "dúvida", T(4.2), True), ("Shaw", "dúvida", T(4.8), True)]
    for i, (nome, mot, ti, duv) in enumerate(lin):
        kk = suave((t - ti) / 0.25)
        if kk <= 0:
            continue
        al = int(255 * kk)
        y = CY0 + 240 + i * 100
        d.rounded_rectangle((120, y - 38, W - 120, y + 38), radius=18, fill=(36, 34, 32, al))
        d.text((170, y), nome, font=fonte(SERIFA_N, 44), fill=CREME + (al,), anchor="lm")
        d.text((W - 170, y), mot, font=fonte(SANS_SB, 32), fill=(CREME_70 if duv else CORAL) + (al,), anchor="rm")
    q.im.paste(ov, (0, 0), ov)


def casa(v, q, t):
    ov = _ov(q)
    d = ImageDraw.Draw(ov)
    d.rectangle((0, CY0 + CH * 0.06, W, CY0 + CH * 0.90), fill=(20, 20, 19, 238))
    d.text((W / 2, CY0 + 130), "SPORTING · ALVALADE", font=fonte(SANS_SB, 34), fill=CORAL + (255,), anchor="mm")
    for i, (txt, ti) in enumerate((("Debast · dúvida", T(1.8)), ("Nuno Santos · dúvida", T(2.4)))):
        kk = suave((t - ti) / 0.25)
        if kk > 0:
            _chip(d, W / 2, CY0 + 300 + i * 120, txt, VERDE_SCP, kk, tam=38)
    k = suave((t - T(4.0)) / 0.25)
    if k > 0:
        d.text((W / 2, CY0 + 590), "Árbitro: Marciniak", font=fonte(SERIFA_N, 56), fill=CREME + (int(255 * k),),
               anchor="mm")
        d.text((W / 2, CY0 + 660), "Polónia", font=fonte(SANS, 30), fill=CREME_70 + (int(255 * k),), anchor="mm")
    q.im.paste(ov, (0, 0), ov)


def numeros(v, q, t):
    ov = _ov(q)
    d = ImageDraw.Draw(ov)
    d.rectangle((0, CY0 + CH * 0.06, W, CY0 + CH * 0.90), fill=(20, 20, 19, 238))
    d.text((W / 2, CY0 + 130), "UNITED · 3 JOGOS RECENTES", font=fonte(SANS_SB, 34), fill=CORAL + (255,), anchor="mm")
    for i, (txt, ti) in enumerate((("4–4", T(1.6)), ("3–2", T(2.6)), ("0–4", T(3.6)))):
        kk = suave((t - ti) / 0.25)
        if kk > 0:
            d.text((W / 2 - 280 + i * 280, CY0 + 330), txt, font=fonte(SERIFA_N, 92),
                   fill=CREME + (int(255 * kk),), anchor="mm")
    k = suave((t - T(4.8)) / 0.3)
    if k > 0:
        d.text((W / 2, CY0 + 560), "10 golos sofridos", font=fonte(SERIFA_N, 72), fill=CORAL + (int(255 * k),),
               anchor="mm")
    q.im.paste(ov, (0, 0), ov)


def forma_scp(v, q, t):
    ov = _ov(q)
    d = ImageDraw.Draw(ov)
    d.rectangle((0, CY0 + CH * 0.06, W, CY0 + CH * 0.90), fill=(20, 20, 19, 238))
    d.text((W / 2, CY0 + 130), "SPORTING · EM CASA", font=fonte(SANS_SB, 34), fill=CORAL + (255,), anchor="mm")
    for i, (txt, ti, cor) in enumerate((("Taça: 4–0", T(1.2), VERDE_SCP), ("Moreirense: 1–0", T(4.6), VERDE_SCP))):
        kk = suave((t - ti) / 0.25)
        if kk > 0:
            _chip(d, W / 2, CY0 + 320 + i * 170, txt, cor, kk, tam=54)
    k = suave((t - T(6.0)) / 0.3)
    if k > 0:
        d.text((W / 2, CY0 + 640), "ganha, sem exagerar", font=fonte(SERIFA_N, 64), fill=CREME + (int(255 * k),),
               anchor="mm")
    q.im.paste(ov, (0, 0), ov)


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
    for i, (lab, pc, cor, ti) in enumerate((("Sporting", 54, VERDE_SCP, T(1.0)), ("Empate", 23, (110, 106, 100), T(2.6)),
                                            ("United", 23, VERMELHO, T(3.6)))):
        kk = suave((t - ti) / 0.3)
        if kk <= 0:
            continue
        al = int(255 * kk)
        y = CY0 + 350 + i * 120
        d.text((110, y), lab, font=fonte(SANS_SB, 36), fill=CREME + (al,), anchor="lm")
        larg = (W - 560) * pc / 54 * kk
        d.rounded_rectangle((330, y - 30, 330 + max(10, larg), y + 30), radius=14, fill=cor + (al,))
        d.text((W - 90, y), f"{pc}%", font=fonte(SERIFA_N, 48), fill=CREME + (al,), anchor="rm")
    k = suave((t - T(5.8)) / 0.25)
    if k > 0:
        d.text((W / 2, CY0 + 740), "golos esperados  1,9 – 1,3", font=fonte(SANS_SB, 36),
               fill=CREME + (int(255 * k),), anchor="mm")
    k = suave((t - T(8.0)) / 0.25)
    if k > 0:
        _chip(d, W / 2, CY0 + 830, "Previsões na rede vizinha · link na bio", CORAL, k, tam=32)


def pergunta(v, q, t):
    _fundo(q, t)
    d = q.d
    d.text((W / 2, CY0 + 170), "Quem sorri em Alvalade?", font=fonte(SERIFA_N, 62), fill=CREME + (255,), anchor="mm")
    for i, (letra, l1, l2, ti, cor) in enumerate((("A", "Sporting", "vitória", T(1.0), VERDE_SCP),
                                                  ("B", "Empate / United", "ponto ou mais", T(1.6),
                                                   VERMELHO))):
        kk = suave((t - ti) / 0.25)
        if kk <= 0:
            continue
        al = int(255 * kk)
        cx, cy = W / 2 + (-215 if i == 0 else 215), CY0 + 410
        d.rounded_rectangle((cx - 200, cy - 125, cx + 200, cy + 125), radius=28, fill=cor + (al,))
        d.text((cx, cy - 50), letra, font=fonte(SERIFA_N, 66), fill=CREME + (al,), anchor="mm")
        d.text((cx, cy + 25), l1, font=fonte(SANS_SB, 34), fill=CREME + (al,), anchor="mm")
        d.text((cx, cy + 72), l2, font=fonte(SANS, 28), fill=CREME + (al,), anchor="mm")
    k = suave((t - T(2.4)) / 0.25)
    if k > 0:
        d.text((W / 2, CY0 + 680), "Comenta A ou B", font=fonte(SANS_SB, 50), fill=CORAL + (int(255 * k),),
               anchor="mm")


def construir():
    v = Video("Sporting", "Man United", abrev=("SCP", "MUN"),
              fonte_txt="Ilustração · dados ESPN, fontes da imprensa e Agente Claudio")
    v.folga, v.bpm = 0.25, 120
    v.sp['fcp'] = sprite(17, VERDE_SCP, (236, 234, 226), 3)
    v.sp['adv'] = sprite(17, (236, 234, 226), (60, 60, 60), 3)
    cenas = []
    for dur, i, so, tit in ((5.8, 0, gancho, "Antevisão · Alvalade"), (6.8, 1, baixas, "Man United · baixas"),
                            (7.0, 2, casa, "Sporting · casa"), (9.0, 3, numeros, "Man United · números"),
                            (10.4, 4, forma_scp, "Sporting · forma"), (12.5, 5, previsao, "Previsão do Agente"),
                            (4.6, 6, pergunta, "")):
        voz, leg = FALAS[i]
        c = Cena(dur, tit, "", vazio(), voz=voz, legenda=leg, voz_ini=VI, sobreposicao=so, nomes=False)
        c.voz_ref = REF_VOZ[i]
        c.abrev = ("SCP", "MUN")
        c.t_capa = dur - 0.2
        cenas.append(c)
    cenas.append(cena_fecho(vazio(), placar="–", minuto="20h00", frase=FECHO))
    return v, cenas


TIPO = "antevisao"
TEMA = "Sporting x Man United: o United chega com 4 baixas e a vir de um 0-4"
MATCH_ID = "20261125-UCL-splisbon-manunited"
HORA = "17:30"
POSTS = {
    "tiktok": "O United chega a Alvalade com 4 baixas… e a vir de um 0-4 😮 Quem sorri hoje? #futebol "
              "#agenteclaudio #sporting #championsleague #futeboltiktok",
    "instagram": "Sporting x Man United, hoje às 20h: o United sem Cunha (castigo), Ugarte, Baleba e Šeško, com "
                 "Rashford e Shaw em dúvida. O Agente Claudio dá 54% ao Sporting, 23% empate, 23% United. "
                 "A tua aposta: A ou B? #sporting #championsleague #futebol #agenteclaudio +18",
    "youtube": {"titulo": "Sporting x Man United: 4 baixas e um 0-4 às costas #shorts",
                "descricao": "Antevisão de Alvalade com a previsão do Agente Claudio: 54% Sporting, 23% empate, "
                             "23% United.\n#sporting #championsleague #futebol #agenteclaudio"},
    "x": "Sporting x Man United, 20h: United com 4 baixas e a vir de um 0-4. Agente Claudio: 54% Sporting, "
         "23% empate, 23% United. #SportingCP #UCL",
}
MEMES = []
