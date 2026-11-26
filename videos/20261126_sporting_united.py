"""Sporting 2-2 Man United, Liga dos Campeões (5.ª jornada), Alvalade, 25 nov 2026. Gancho: 3 penalidades, 2 anulados.

Fontes (verificadas a 26 nov 2026; ESPN e os sites das crónicas estavam bloqueados na sessão, por isso só resumos de
pesquisa web — digo apenas o que as fontes concordam):
- Resultado e golos: Suárez 33' (grande penalidade) e 80'; Bruno Fernandes 48' (grande penalidade) e 50' — Diadejogo,
  JN, Sky Sports, ESPN UK, O Jogo, Record, Observador, DN, Público, ZeroZero.
- Lance do 1-0: Suárez falhou uma grande penalidade (defesa de Lammens) e pouco depois o United voltou a ser punido
  (Sky: 75 segundos; O Jogo: 3 minutos — não digo o intervalo). Segui "pouco depois".
- 1-2: Bruno Fernandes, bola a saltar num buraco do relvado (Sky / Record). 2-2: bola solta do guarda-redes do
  United na área, Suárez empata (Sky). Digo "bola solta", sem acusar ninguém.
- Golos anulados do United: um do Amad antes do intervalo e outro já no fim (VAR; JN fala em falta sobre Kaique —
  não digo qual foi qual nem o motivo).
- Expulsão: Tielemans, duas amarelas, perto do fim (Sky, Record; Observador: United com 10).
- Pontos: Sporting 10, United 7 (SportTV, Sky). Treinadores e classificação detalhada: fontes divergem/única, NÃO uso.
- Agente Claudio: o modelo dava 54% ao Sporting; o jogo acabou empatado, por isso NÃO mostro previsão (só acertos).
Cores: Sporting verde; United vermelho (ilustração).
"""
from PIL import ImageDraw

from quadro_tatico import (cena_fecho, sprite, CORAL, CREME, CREME_70, CY0, CH, W, Cena, Video, fonte, suave,
                           SERIFA_N, SANS, SANS_SB)

import porto_napoli as base
import benfica_lech as bl
import taca_grandes as tg

_ov = base._ov
_fundo, _chip = bl._fundo, bl._chip
vazio = tg.vazio
VERDE_SCP, VERMELHO = tg.VERDE_SCP, tg.VERMELHO
VI = 0.15


def T(x):
    return x + VI


FALAS = [
    ("Três grandes penalidades, dois golos anulados... e um empate que nasceu de uma bola solta. Alvalade não "
     "teve um minuto de descanso.",
     "3 grandes penalidades, 2 golos anulados… e um empate que nasceu de uma bola solta. Alvalade não teve um "
     "minuto de descanso."),
    ("Primeiro, o Suárez falha a grande penalidade e o Lammens defende. Pouco depois, outra grande penalidade, "
     "e desta vez o Suárez não perdoa. Um a zero, aos trinta e três.",
     "Primeiro, Suárez falha a grande penalidade e Lammens defende. Pouco depois, outra grande penalidade, e "
     "desta vez Suárez não perdoa. 1–0, aos 33'."),
    ("Na segunda parte, o Bruno Fernandes, que foi homenageado antes do jogo, marca duas vezes em dois minutos. "
     "Grande penalidade aos quarenta e oito, e aos cinquenta uma bola que salta num buraco do relvado. Um a dois.",
     "Na segunda parte, Bruno Fernandes, homenageado antes do jogo, marca 2 vezes em 2 minutos. Grande penalidade "
     "aos 48', e aos 50' uma bola que salta num buraco do relvado. 1–2."),
    ("E o United ainda viu dois golos anulados: um do Amad, antes do intervalo, e outro já no fim, pelo VAR. "
     "Podia ter sido muito pior para o Sporting.",
     "E o United ainda viu 2 golos anulados: um do Amad, antes do intervalo, e outro já no fim, pelo VAR. Podia "
     "ter sido muito pior para o Sporting."),
    ("Aos oitenta, uma bola solta na área e o Suárez empata. Dois a dois. Ainda houve tempo para o Tielemans ver "
     "o segundo amarelo, e o United acabou com dez.",
     "Aos 80', uma bola solta na área e Suárez empata. 2–2. Ainda houve tempo para Tielemans ver o 2.º amarelo, e "
     "o United acabou com 10."),
    ("Sporting com dez pontos, United com sete. Um jogo que o Agente Claudio leu como favorável ao Sporting... "
     "mas que acabou em empate. As previsões estão na rede vizinha, link na bio.",
     "Sporting com 10 pontos, United com 7. Um jogo que o Agente Claudio leu como favorável ao Sporting… mas que "
     "acabou em empate. As previsões estão na rede vizinha, link na bio."),
    ("Quem fez a noite: o Suárez, com dois golos, ou o Bruno Fernandes, com dois também? Comenta.",
     "Quem fez a noite: Suárez, com 2 golos, ou Bruno Fernandes, com 2 também? Comenta."),
]
FECHO = ("[laughs] Manda isto ao teu amigo que diz que o jogo está decidido... aos quarenta e oito minutos.",
         ["Manda isto ao teu amigo", "que diz «está |decidido|»", "aos |48 minutos|."])
REF_VOZ = [7.50, 9.49, 12.02, 8.28, 8.66, 10.15, 5.30]


def _base(q, titulo, y=130):
    ov = _ov(q)
    d = ImageDraw.Draw(ov)
    d.rectangle((0, CY0 + CH * 0.06, W, CY0 + CH * 0.90), fill=(20, 20, 19, 238))
    d.text((W / 2, CY0 + y), titulo, font=fonte(SANS_SB, 34), fill=CORAL + (255,), anchor="mm")
    return ov, d


def gancho(v, q, t):
    ov, d = _base(q, "SPORTING · UNITED", 120)
    pulso = 1 + 0.04 * max(0, 1 - t / 0.4)
    d.text((W / 2, CY0 + 290), "2–2", font=fonte(SERIFA_N, int(190 * pulso)), fill=CREME + (255,), anchor="mm")
    d.text((W / 2, CY0 + 430), "3 grandes penalidades", font=fonte(SANS_SB, 46), fill=CORAL + (255,), anchor="mm")
    k = suave((t - T(1.3)) / 0.25)
    if k > 0:
        d.text((W / 2, CY0 + 530), "2 golos anulados", font=fonte(SERIFA_N, 58), fill=CREME + (int(255 * k),),
               anchor="mm")
    k = suave((t - T(3.5)) / 0.25)
    if k > 0:
        d.text((W / 2, CY0 + 640), "e uma bola solta", font=fonte(SERIFA_N, 70), fill=CORAL + (int(255 * k),),
               anchor="mm")
    q.im.paste(ov, (0, 0), ov)


def cron(titulo, linhas, final=None):
    """Cena com uma lista de lances (texto, cor, tempo) e uma linha final."""
    def f(v, q, t):
        ov, d = _base(q, titulo)
        for i, (minuto, txt, cor, ti) in enumerate(linhas):
            kk = suave((t - T(ti)) / 0.25)
            if kk <= 0:
                continue
            al = int(255 * kk)
            y = CY0 + 250 + i * 130
            d.rounded_rectangle((90, y - 50, W - 90, y + 50), radius=20, fill=(36, 34, 32, al),
                                outline=cor + (al,), width=3)
            d.text((150, y), minuto, font=fonte(SERIFA_N, 50), fill=cor + (al,), anchor="lm")
            d.text((290, y), txt, font=fonte(SANS_SB, 34), fill=CREME + (al,), anchor="lm")
        if final:
            txt, ti = final
            k = suave((t - T(ti)) / 0.3)
            if k > 0:
                d.text((W / 2, CY0 + 250 + len(linhas) * 130 + 60), txt, font=fonte(SERIFA_N, 72),
                       fill=CORAL + (int(255 * k),), anchor="mm")
        q.im.paste(ov, (0, 0), ov)
    return f




def parte1(v, q, t):
    ov, d = _base(q, "1.ª PARTE · ALVALADE")
    k = suave((t - T(0.6)) / 0.25)
    if k > 0:
        al = int(255 * k)
        d.rounded_rectangle((90, CY0 + 200, W - 90, CY0 + 320), radius=22, fill=(36, 34, 32, al),
                            outline=VERMELHO + (al,), width=3)
        d.text((W / 2, CY0 + 260), "Grande penalidade falhada", font=fonte(SANS_SB, 42), fill=CREME + (al,),
               anchor="mm")
    k = suave((t - T(5.2)) / 0.25)
    if k > 0:
        al = int(255 * k)
        d.rounded_rectangle((90, CY0 + 370, W - 90, CY0 + 490), radius=22, fill=(36, 34, 32, al),
                            outline=VERDE_SCP + (al,), width=3)
        d.text((W / 2, CY0 + 430), "33' · Suárez marca", font=fonte(SANS_SB, 42), fill=CREME + (al,), anchor="mm")
    k = suave((t - T(7.8)) / 0.3)
    if k > 0:
        d.text((W / 2, CY0 + 660), "1–0", font=fonte(SERIFA_N, 150), fill=CORAL + (int(255 * k),), anchor="mm")
    q.im.paste(ov, (0, 0), ov)


def parte2(v, q, t):
    ov, d = _base(q, "2.ª PARTE · BRUNO FERNANDES")
    for i, (m, txt, ti) in enumerate((("48'", "grande penalidade", 6.7), ("50'", "bola salta no relvado", 7.8))):
        kk = suave((t - T(ti)) / 0.25)
        if kk <= 0:
            continue
        al = int(255 * kk)
        y = CY0 + 280 + i * 150
        d.rounded_rectangle((90, y - 55, W - 90, y + 55), radius=22, fill=(36, 34, 32, al),
                            outline=VERMELHO + (al,), width=3)
        d.text((150, y), m, font=fonte(SERIFA_N, 56), fill=CORAL + (al,), anchor="lm")
        d.text((300, y), txt, font=fonte(SANS_SB, 36), fill=CREME + (al,), anchor="lm")
    k = suave((t - T(10.8)) / 0.3)
    if k > 0:
        d.text((W / 2, CY0 + 640), "1–2", font=fonte(SERIFA_N, 150), fill=CREME + (int(255 * k),), anchor="mm")
        d.text((W / 2, CY0 + 760), "2 golos em 2 minutos", font=fonte(SANS_SB, 36), fill=CORAL + (int(255 * k),),
               anchor="mm")
    q.im.paste(ov, (0, 0), ov)


def anulados(v, q, t):
    ov, d = _base(q, "UNITED · GOLOS ANULADOS")
    for i, (txt, sub, ti) in enumerate((("Amad", "antes do intervalo", 2.2), ("Já no fim", "VAR", 4.5))):
        kk = suave((t - T(ti)) / 0.25)
        if kk <= 0:
            continue
        al = int(255 * kk)
        y = CY0 + 330 + i * 190
        d.rounded_rectangle((110, y - 70, W - 110, y + 70), radius=24, fill=(36, 34, 32, al),
                            outline=CORAL + (al,), width=3)
        d.text((W / 2, y - 18), txt, font=fonte(SERIFA_N, 56), fill=CREME + (al,), anchor="mm")
        d.text((W / 2, y + 36), sub, font=fonte(SANS, 30), fill=CREME_70 + (al,), anchor="mm")
        d.line((130, y + 62, W - 130, y - 62), fill=VERMELHO + (al,), width=6)
    q.im.paste(ov, (0, 0), ov)


def empate(v, q, t):
    ov, d = _base(q, "80' · ALVALADE")
    k = suave((t - T(0.7)) / 0.25)
    if k > 0:
        d.text((W / 2, CY0 + 270), "bola solta na área", font=fonte(SERIFA_N, 60), fill=CREME + (int(255 * k),),
               anchor="mm")
    k = suave((t - T(3.1)) / 0.3)
    if k > 0:
        d.text((W / 2, CY0 + 470), "2–2", font=fonte(SERIFA_N, 190), fill=CORAL + (int(255 * k),), anchor="mm")
        d.text((W / 2, CY0 + 610), "Suárez empata", font=fonte(SANS_SB, 40), fill=CREME + (int(255 * k),),
               anchor="mm")
    k = suave((t - T(4.8)) / 0.25)
    if k > 0:
        _chip(d, W / 2, CY0 + 740, "Tielemans · 2.º amarelo · United com 10", VERMELHO, k, tam=32)
    q.im.paste(ov, (0, 0), ov)


def balanco(v, q, t):
    ov, d = _base(q, "LIGA DOS CAMPEÕES · 5.ª JORNADA")
    k = suave((t - T(0.4)) / 0.25)
    if k > 0:
        al = int(255 * k)
        for cx, nome, pts, cor in ((W / 2 - 230, "SPORTING", "10", VERDE_SCP), (W / 2 + 230, "UNITED", "7", VERMELHO)):
            d.rounded_rectangle((cx - 190, CY0 + 220, cx + 190, CY0 + 520), radius=28, fill=cor + (al,))
            d.text((cx, CY0 + 290), nome, font=fonte(SANS_SB, 38), fill=CREME + (al,), anchor="mm")
            d.text((cx, CY0 + 410), pts, font=fonte(SERIFA_N, 150), fill=CREME + (al,), anchor="mm")
            d.text((cx, CY0 + 490), "pontos", font=fonte(SANS, 28), fill=CREME + (al,), anchor="mm")
    k = suave((t - T(3.4)) / 0.3)
    if k > 0:
        d.text((W / 2, CY0 + 640), "o modelo dava vantagem ao Sporting", font=fonte(SANS_SB, 34),
               fill=CREME + (int(255 * k),), anchor="mm")
        d.text((W / 2, CY0 + 700), "…e saiu empate", font=fonte(SERIFA_N, 56), fill=CORAL + (int(255 * k),),
               anchor="mm")
    k = suave((t - T(8.2)) / 0.25)
    if k > 0:
        _chip(d, W / 2, CY0 + 810, "Previsões na rede vizinha · link na bio", CORAL, k, tam=32)
    q.im.paste(ov, (0, 0), ov)


def pergunta(v, q, t):
    _fundo(q, t)
    d = q.d
    d.text((W / 2, CY0 + 170), "Quem fez a noite?", font=fonte(SERIFA_N, 62), fill=CREME + (255,), anchor="mm")
    for i, (letra, l1, l2, ti, cor) in enumerate((("A", "Suárez", "2 golos", T(1.0), VERDE_SCP),
                                                  ("B", "Bruno Fernandes", "2 golos", T(2.6), VERMELHO))):
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


DURS = [8.0, 10.0, 12.5, 8.8, 9.2, 10.7, 5.8]
SOBRE = [gancho, parte1, parte2, anulados, empate, balanco, pergunta]
TITS = ["Liga dos Campeões · Alvalade"] * 5 + ["Liga dos Campeões · 5.ª jornada", ""]
PLAC = [("2–2", "FIM"), ("1–0", "33'"), ("1–2", "50'"), ("1–2", "2.ª parte"), ("2–2", "80'"), ("2–2", "FIM"),
        ("2–2", "FIM")]


def construir():
    v = Video("Sporting", "Man United", abrev=("SCP", "MUN"),
              fonte_txt="Ilustração · dados ESPN, fontes da imprensa e Agente Claudio")
    v.folga, v.bpm = 0.25, 120
    v.sp['fcp'] = sprite(17, VERDE_SCP, (236, 234, 226), 3)
    v.sp['adv'] = sprite(17, (236, 234, 226), (60, 60, 60), 3)
    cenas = []
    for i in range(7):
        voz, leg = FALAS[i]
        c = Cena(DURS[i], TITS[i], "", vazio(), voz=voz, legenda=leg, voz_ini=VI, sobreposicao=SOBRE[i],
                 nomes=False, placar=PLAC[i][0], minuto=PLAC[i][1])
        c.voz_ref = REF_VOZ[i]
        c.abrev = ("SCP", "MUN")
        c.t_capa = DURS[i] - 0.2
        cenas.append(c)
    cenas.append(cena_fecho(vazio(), placar="2–2", minuto="FIM", frase=FECHO))
    return v, cenas


TIPO = "jogo"
TEMA = "Sporting 2-2 Man United: 3 penalidades, 2 golos anulados e uma bola solta"
MATCH_ID = "20261125-UCL-splisbon-manunited"
HORA = "12:30"
POSTS = {
    "tiktok": "3 grandes penalidades, 2 golos anulados… e um empate que nasceu de uma bola solta 🤯 Alvalade não "
              "descansou. #futebol #agenteclaudio #sporting #championsleague #futeboltiktok",
    "instagram": "Sporting 2-2 Man United em Alvalade: Suárez falhou uma grande penalidade e marcou outra, Bruno "
                 "Fernandes fez 2 em 2 minutos, o United viu 2 golos anulados e acabou com 10. Quem fez a noite? "
                 "A ou B? #sporting #championsleague #futebol #agenteclaudio +18",
    "youtube": {"titulo": "Sporting 2-2 United: 3 penalidades e 2 golos anulados #shorts",
                "descricao": "Suárez e Bruno Fernandes com dois golos cada, o VAR em campo e o United com 10. "
                             "A noite louca de Alvalade explicada.\n"
                             "#sporting #championsleague #futebol #agenteclaudio"},
    "x": "Sporting 2-2 Man United: 3 grandes penalidades, 2 golos anulados, Tielemans expulso e 2 golos de "
         "Suárez e de Bruno Fernandes. Que noite em Alvalade. #SportingCP #UCL",
}
MEMES = []
