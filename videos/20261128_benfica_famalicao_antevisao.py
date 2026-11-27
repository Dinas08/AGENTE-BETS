"""Antevisão Benfica x Famalicão, Liga Portugal (12.ª jornada), Luz, segunda 30 nov 2026, 20h15.

Fontes (verificadas a 27 nov 2026; diadejogo.pt, ESPN e outros sites estavam bloqueados na sessão, por isso só
resumos de pesquisa web — Diário de Jogo 26 e 27/11 — e os dados do projeto):
- Benfica: Barreiro lesionado, única baixa certa; Aursnes (fase final de recuperação) e Prestianni (fadiga no
  adutor, dúvida) esperados de volta depois de ficarem fora de Plzen (Diário de Jogo). Sem outras fontes: no vídeo
  digo "esperados", nunca "regressam".
- Famalicão: só uma fonte (FotMob) para a baixa de Mattara e o treinador diverge entre resultados: NÃO os uso.
- Resultados (base de dados do projeto): Benfica 0-4 Viktoria Plzen (26/11), 3-1 Torreense na Taça, 3-1 Lech e
  1-0 Alverca na Luz; Famalicão 0-3 em Braga (1/11) e 1-0 ao Arouca (6/11).
- A manchete "16 jogos sem ganhar na Luz" (Diário de Jogo) não deu para confirmar de quem fala: NÃO a uso.
- Agente Claudio: Benfica 72%, empate 19%, Famalicão 9%; golos esperados 2,15–0,72. Antevisão: sem "acertou". Sem odds.
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
    ("Levou quatro em Plzen... e na segunda-feira volta à Luz. O Agente Claudio ainda dá setenta e dois por cento ao Benfica. Porquê?",
     "Levou 4 em Plzen… e na segunda volta à Luz. O Agente Claudio ainda dá 72% ao Benfica. Porquê?"),
    ("Primeiro, o boletim clínico: o Barreiro é a única baixa certa. E o Aursnes e o Prestianni são esperados de volta.",
     "Primeiro, o boletim clínico: Barreiro é a única baixa certa. Aursnes e Prestianni são esperados de volta."),
    ("Segundo, a Luz. Em casa, este ano, venceu o Alverca por um a zero e o Lech por três a um.",
     "Segundo, a Luz. Em casa, esta época, venceu o Alverca por 1–0 e o Lech por 3–1."),
    ("E o Famalicão? Perdeu por três a zero em Braga, e depois ganhou por um a zero ao Arouca. Altos e baixos.",
     "E o Famalicão? Perdeu 0–3 em Braga e depois ganhou 1–0 ao Arouca. Altos e baixos."),
    ("Resultado: dois golos e uns trocos para o Benfica, menos de um para o Famalicão. Setenta e dois por cento "
     "Benfica, dezanove empate, nove Famalicão. As previsões estão na rede vizinha, link na bio.",
     "Resultado: 2 golos e uns trocos para o Benfica, menos de 1 para o Famalicão. 72% Benfica, 19% empate, 9% "
     "Famalicão. As previsões estão na rede vizinha, link na bio."),
    ("Depois do quatro a zero, o Benfica responde na Luz? Ou o Famalicão surpreende? Comenta.",
     "Depois do 0–4, o Benfica responde na Luz ou o Famalicão surpreende? Comenta."),
]
FECHO = ("[laughs] Manda isto ao teu amigo que leva quatro de manhã... e à noite jura que está tudo controlado.",
         ["Manda isto ao teu amigo", "que leva |quatro| de manhã", "e à noite jura que está |controlado|."])
REF_VOZ = [7.29, 6.51, 5.2, 6.02, 11.08, 5.08]
AZUL_FCP = (200, 35, 45)   # vermelho Benfica (nome mantido do modelo)
AZUL_FAM = (40, 70, 140)


def _painel(q):
    ov = _ov(q)
    d = ImageDraw.Draw(ov)
    d.rectangle((0, CY0 + CH * 0.06, W, CY0 + CH * 0.90), fill=(20, 20, 19, 238))
    return ov, d


def gancho(v, q, t):
    ov, d = _painel(q)
    d.text((W / 2, CY0 + 120), "ANTEVISÃO · SEGUNDA NA LUZ", font=fonte(SANS_SB, 34), fill=CORAL + (255,),
           anchor="mm")
    pulso = 1 + 0.04 * max(0, 1 - t / 0.4)
    for cx, txt, cor in ((W / 2 - 280, "BENFICA", AZUL_FCP), (W / 2 + 280, "FAMALICÃO", AZUL_FAM)):
        d.rounded_rectangle((cx - 150, CY0 + 220, cx + 150, CY0 + 340), radius=26, fill=cor + (255,))
        d.text((cx, CY0 + 280), txt, font=fonte(SANS_SB, int(44 * pulso)), fill=CREME + (255,), anchor="mm")
    d.text((W / 2, CY0 + 280), "vs", font=fonte(SERIFA_N, 60), fill=CREME + (255,), anchor="mm")
    d.text((W / 2 - 280, CY0 + 410), "0–4", font=fonte(SERIFA_N, 96), fill=CORAL + (255,), anchor="mm")
    d.text((W / 2 - 280, CY0 + 490), "em Plzen", font=fonte(SANS_SB, 36), fill=CREME_70 + (255,), anchor="mm")
    k = suave((t - T(4.8)) / 0.3)
    if k > 0:
        d.text((W / 2 + 280, CY0 + 410), "9%", font=fonte(SERIFA_N, 96), fill=CREME + (int(255 * k),), anchor="mm")
        d.text((W / 2 + 280, CY0 + 490), "para o Famalicão", font=fonte(SANS_SB, 36),
               fill=CREME_70 + (int(255 * k),), anchor="mm")
    k = suave((t - T(6.0)) / 0.3)
    if k > 0:
        d.text((W / 2, CY0 + 640), "Benfica 72%. Porquê?", font=fonte(SERIFA_N, 72), fill=CREME + (int(255 * k),),
               anchor="mm")
    q.im.paste(ov, (0, 0), ov)


def baixas(v, q, t):
    ov, d = _painel(q)
    d.text((W / 2, CY0 + 130), "BENFICA · BOLETIM CLÍNICO", font=fonte(SANS_SB, 34), fill=CORAL + (255,),
           anchor="mm")
    lin = [("Barreiro", "baixa certa", T(1.8)), ("Aursnes", "esperado de volta", T(3.7)),
           ("Prestianni", "esperado de volta", T(4.2))]
    for i, (nome, mot, ti) in enumerate(lin):
        kk = suave((t - ti) / 0.25)
        if kk <= 0:
            continue
        al = int(255 * kk)
        y = CY0 + 300 + i * 130
        d.rounded_rectangle((100, y - 48, W - 100, y + 48), radius=18, fill=(36, 34, 32, al))
        d.text((150, y), nome, font=fonte(SERIFA_N, 52), fill=CREME + (al,), anchor="lm")
        d.text((W - 150, y), mot, font=fonte(SANS_SB, 30), fill=(CORAL if i == 0 else CREME_70) + (al,),
               anchor="rm")
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


luz = _duo("BENFICA · NA LUZ", [("1–0 Alverca", 3.0), ("3–1 Lech", 3.9)], AZUL_FCP, "2 vitórias em casa", 4.8)
fam = _duo("FAMALICÃO · ÚLTIMOS JOGOS", [("0–3 Braga (fora)", 1.5), ("1–0 Arouca", 3.3)], AZUL_FAM,
           "altos e baixos", 4.6)


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
    for lab, pc, cor, ti, y in (("Benfica", 72, AZUL_FCP, T(4.7), 350), ("Empate", 19, (110, 106, 100), T(5.8), 470),
                                ("Famalicão", 9, AZUL_FAM, T(6.5), 590)):
        kk = suave((t - ti) / 0.3)
        if kk <= 0:
            continue
        al = int(255 * kk)
        y += CY0
        d.text((110, y), lab, font=fonte(SANS_SB, 36), fill=CREME + (al,), anchor="lm")
        larg = (W - 560) * pc / 72 * kk
        d.rounded_rectangle((330, y - 30, 330 + max(10, larg), y + 30), radius=14, fill=cor + (al,))
        d.text((W - 90, y), f"{pc}%", font=fonte(SERIFA_N, 48), fill=CREME + (al,), anchor="rm")
    k = suave((t - T(2.0)) / 0.25)
    if k > 0:
        d.text((W / 2, CY0 + 740), "golos esperados  2,2 – 0,7", font=fonte(SANS_SB, 36),
               fill=CREME + (int(255 * k),), anchor="mm")
    k = suave((t - T(9.3)) / 0.25)
    if k > 0:
        _chip(d, W / 2, CY0 + 830, "Previsões na rede vizinha · link na bio", CORAL, k, tam=32)


def pergunta(v, q, t):
    _fundo(q, t)
    d = q.d
    d.text((W / 2, CY0 + 170), "Quem ganha a Luz?", font=fonte(SERIFA_N, 62), fill=CREME + (255,), anchor="mm")
    for i, (letra, l1, l2, ti, cor) in enumerate((("A", "Benfica", "responde ao 0–4", T(1.0), AZUL_FCP),
                                                  ("B", "Famalicão", "surpreende", T(1.6), AZUL_FAM))):
        kk = suave((t - ti) / 0.25)
        if kk <= 0:
            continue
        al = int(255 * kk)
        cx, cy = W / 2 + (-215 if i == 0 else 215), CY0 + 410
        d.rounded_rectangle((cx - 200, cy - 125, cx + 200, cy + 125), radius=28, fill=cor + (al,))
        d.text((cx, cy - 50), letra, font=fonte(SERIFA_N, 66), fill=CREME + (al,), anchor="mm")
        d.text((cx, cy + 25), l1, font=fonte(SANS_SB, 32), fill=CREME + (al,), anchor="mm")
        d.text((cx, cy + 72), l2, font=fonte(SANS, 26), fill=CREME + (al,), anchor="mm")
    k = suave((t - T(2.4)) / 0.25)
    if k > 0:
        d.text((W / 2, CY0 + 680), "Comenta A ou B", font=fonte(SANS_SB, 50), fill=CORAL + (int(255 * k),),
               anchor="mm")


def construir():
    v = Video("Benfica", "Famalicão", abrev=("SLB", "FAM"),
              fonte_txt="Ilustração · dados ESPN, fontes da imprensa e Agente Claudio")
    v.folga, v.bpm = 0.25, 120
    v.sp['fcp'] = sprite(17, AZUL_FCP, (236, 234, 226), 3)
    v.sp['adv'] = sprite(17, AZUL_FAM, (236, 234, 226), 3)
    cenas = []
    for dur, i, so, tit in ((7.5, 0, gancho, "Antevisão · Luz"), (6.8, 1, baixas, "Benfica · baixas"),
                            (5.5, 2, luz, "Benfica · na Luz"), (6.3, 3, fam, "Famalicão · forma"),
                            (11.3, 4, previsao, "Previsão do Agente"), (5.3, 5, pergunta, "")):
        voz, leg = FALAS[i]
        c = Cena(dur, tit, "", vazio(), voz=voz, legenda=leg, voz_ini=VI, sobreposicao=so, nomes=False)
        c.voz_ref = REF_VOZ[i]
        c.abrev = ("SLB", "FAM")
        c.t_capa = dur - 0.2
        cenas.append(c)
    cenas.append(cena_fecho(vazio(), placar="–", minuto="20h15", frase=FECHO))
    return v, cenas


TIPO = "antevisao"
TEMA = "Benfica x Famalicão: levou 4 em Plzen e ainda tem 72%"
MATCH_ID = "20261130-P1-benfica-famalicao"
HORA = "12:30"
POSTS = {
    "tiktok": "Levou 4 em Plzen… e o Agente Claudio ainda dá 72% ao Benfica contra o Famalicão. Porquê? 👀 "
              "#futebol #agenteclaudio #benfica #ligaportugal #futeboltiktok",
    "instagram": "Benfica x Famalicão, segunda às 20h15 na Luz: Barreiro é a única baixa certa, Aursnes e "
                 "Prestianni esperados de volta. O Agente Claudio dá 72% ao Benfica, 19% empate, 9% Famalicão. "
                 "A tua aposta: A ou B? #benfica #ligaportugal #agenteclaudio +18",
    "youtube": {"titulo": "Benfica x Famalicão: levou 4 e ainda tem 72% #shorts",
                "descricao": "Antevisão da 12.ª jornada com a previsão do Agente Claudio: 72% Benfica, 19% "
                             "empate, 9% Famalicão.\n#benfica #ligaportugal #agenteclaudio"},
    "x": "Benfica x Famalicão, segunda 20h15: depois do 0-4 em Plzen, o Agente Claudio dá 72% ao Benfica, 19% "
         "empate, 9% Famalicão. #Benfica #LigaPortugal",
}


def _interrogacao(d, c):
    x0, y0, x1, y1 = c
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    d.text((cx, cy), "0–4", font=fonte(SERIFA_N, 230), fill=CORAL + (255,), anchor="mm")
    d.line((cx - 200, cy + 150, cx + 200, cy + 150), fill=CREME + (255,), width=8)


MEMES = [
    {"modelo": "reacao", "topo": "Benfica depois do 0–4, na segunda:", "desenho": _interrogacao,
     "baixo": "O Agente Claudio, a rever os números", "fala": "72%. Eu confio nas contas. O resto é convosco.",
     "legenda": "Quatro em Plzen, 72% na Luz. Os números não têm memória curta… ou têm? 🤖⚽ #benfica "
                "#ligaportugal #agenteclaudio +18"},
    {"modelo": "expectativa", "esq": "O que o modelo calculou", "dir": "O que o adepto sente à segunda",
     "desenho_esq": "placar:2–0", "desenho_dir": "relogio:20h15", "baixo": "Depois de um 0–4, ninguém dorme.",
     "fala": "Eu só calculo. Vocês é que sofrem.",
     "legenda": "Expectativa vs realidade antes de um jogo da Luz ⏱️ #benfica #futebol #agenteclaudio +18"},
]
