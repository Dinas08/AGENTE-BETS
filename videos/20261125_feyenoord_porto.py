"""Feyenoord 0-1 Porto, Liga dos Campeões (5.ª jornada), De Kuip, 24 nov 2026. Gancho: o golo aos 2 minutos.

Fontes (verificadas a 25 nov 2026; o ESPN e os sites das crónicas estavam bloqueados na sessão, por isso só
resumos de pesquisa web — nada além do que as fontes concordam):
- Resultado: autogolo de Targhalline (2'; algumas fontes dizem 3') — UEFA/O Jogo/Observador/DN/Sofascore/Goal.
  Lance (Observador via pesquisa): cruzamento de Pietuszewski pela esquerda, Froholdt desvia à boca da baliza, a bola
  ainda toca em Targhalline. Uma fonte (Bola na Rede) titula "Froholdt abre as contas": segui a maioria (autogolo).
- Onze do Farioli: 9 novidades (Diogo Costa, Alberto Costa, Bednarek, Kiwior, Zaidu, Pablo Rosário, Froholdt,
  Pietuszewski, Gimenez) — Observador. Pietuszewski o desequilibrador da 1.ª parte; Rosário (8 desarmes, 10 cortes —
  Sofascore) e Diogo Costa em destaque no fim.
- 2.ª parte: o Feyenoord carregou; o árbitro Irfan Peljto chegou a dar golo à equipa da casa mas não valeu (VAR /
  tecnologia: as fontes divergem no pormenor e no minuto, por isso não digo o minuto nem o motivo).
  Estatísticas de remates divergem entre fontes: não as uso.
- Classificação: Porto 6 pontos, 20.º lugar (zona de play-off); Feyenoord 3 pontos, sem vencer há 7 jogos (Sofascore).
  Próximo jogo europeu do Porto: 9 dez vs Liverpool (O Jogo/Golo FM).
- Agente Claudio: previsão do modelo vitória do Porto 58% (certa); dica do canal certa (msg 317, "Vitória Porto").
Cores: Porto azul; Feyenoord vermelho/branco (cores não confirmadas). Jogadas são ilustrações coerentes com isto.
"""
from PIL import Image, ImageDraw

from quadro_tatico import (cena_fecho, sprite, CORAL, CREME, CREME_70, CY0, CH, W, Cena, Video, fonte, suave,
                           SERIFA_N, SANS, SANS_SB)

import porto_napoli as base
import benfica_lech as bl
import taca_grandes as tg

vai, _ov, PFP, _visto = base.vai, base._ov, base.PFP, base._visto
_fundo, _chip = bl._fundo, bl._chip
jogadores, vazio = tg.jogadores, tg.vazio
AZUL_FCP = (35, 85, 175)
VERMELHO = (200, 40, 50)
BRANCO = (236, 234, 226)

VI = 0.15


def T(x):
    return x + VI


FALAS = [
    ("O Porto marcou aos dois minutos... e passou o resto do jogo a sofrer.",
     "O Porto marcou aos 2 minutos… e passou o resto do jogo a sofrer."),
    ("Cruzamento do Pietuchévski pela esquerda, o Fróholt desvia, bate no Targalín... e entra. Autogolo, e o Porto "
     "vai à frente em Roterdão.",
     "Cruzamento do Pietuszewski pela esquerda, o Froholdt desvia, bate no Targhalline… e entra. Autogolo, e o "
     "Porto vai à frente em Roterdão."),
    ("O Farioli mexeu muito: nove novidades no onze. Atrás, o Pablo Rosário a cortar tudo. Descansado? Nem pensar.",
     "O Farioli mexeu muito: 9 novidades no onze. Atrás, o Pablo Rosário a cortar tudo. Descansado? Nem pensar."),
    ("Na segunda parte, o Feyenoord carregou. O árbitro chegou a dar golo à equipa da casa, mas não valeu... "
     "e o Diogo Costa segurou o resto.",
     "Na segunda parte, o Feyenoord carregou. O árbitro chegou a dar golo à equipa da casa, mas não valeu… e o "
     "Diogo Costa segurou o resto."),
    ("Seis pontos, vigésimo lugar, e o Liverpool a seguir, a nove de dezembro.",
     "6 pontos, 20.º lugar, e o Liverpool a seguir, a 9 de dezembro."),
    ("O Agente Claudio deu cinquenta e oito por cento à vitória do Porto, e acertou. As previsões estão na rede "
     "vizinha, link na bio.",
     "O Agente Claudio deu 58% à vitória do Porto, e acertou. As previsões estão na rede vizinha, link na bio."),
    ("Quem mandou mais: o Pietuchévski, que abriu o caminho, ou o Diogo Costa, que fechou a porta? Comenta.",
     "Quem mandou mais: o Pietuszewski, que abriu o caminho, ou o Diogo Costa, que fechou a porta? Comenta."),
]
FECHO = ("[laughs] Manda isto ao teu amigo que chega sempre atrasado... e perdeu o golo logo aos dois minutos.",
         ["Manda isto ao teu amigo", "que chega sempre atrasado", "e perdeu o golo aos |2 minutos|."])

REF_VOZ = [4.09, 7.67, 6.24, 7.72, 4.26, 7.29, 5.85]


def gancho(v, q, t):
    """Frame 0 já com o contraste: 2 minutos, 1–0... e o resto do jogo."""
    ov = _ov(q)
    d = ImageDraw.Draw(ov)
    d.rectangle((0, CY0 + CH * 0.06, W, CY0 + CH * 0.90), fill=(20, 20, 19, 238))
    d.text((W / 2, CY0 + 120), "FEYENOORD · PORTO", font=fonte(SANS_SB, 34), fill=CORAL + (255,), anchor="mm")
    pulso = 1 + 0.04 * max(0, 1 - t / 0.4)
    d.text((W / 2, CY0 + 290), "2'", font=fonte(SERIFA_N, int(170 * pulso)), fill=CREME + (255,), anchor="mm")
    d.text((W / 2, CY0 + 420), "Autogolo · 0–1", font=fonte(SANS_SB, 44), fill=CORAL + (255,), anchor="mm")
    k = suave((t - T(1.8)) / 0.25)  # "o resto do jogo"
    if k > 0:
        al = int(255 * k)
        d.text((W / 2, CY0 + 540), "e depois… 88 minutos", font=fonte(SERIFA_N, 56), fill=CREME + (al,),
               anchor="mm")
    k = suave((t - T(3.4)) / 0.25)  # "a sofrer"
    if k > 0:
        d.text((W / 2, CY0 + 650), "a sofrer", font=fonte(SERIFA_N, 76), fill=CORAL + (int(255 * k),), anchor="mm")
    q.im.paste(ov, (0, 0), ov)


def onze(v, q, t):
    ov = _ov(q)
    d = ImageDraw.Draw(ov)
    d.rectangle((0, CY0 + CH * 0.06, W, CY0 + CH * 0.90), fill=(20, 20, 19, 232))
    k = suave((t - T(0.2)) / 0.25)
    d.text((W / 2, CY0 + 140), "O onze do Farioli", font=fonte(SANS_SB, 36), fill=CORAL + (int(255 * k),),
           anchor="mm")
    d.text((W / 2, CY0 + 260), "9 novidades", font=fonte(SERIFA_N, 96), fill=CREME + (int(255 * k),), anchor="mm")
    nomes = ["Diogo Costa · Alberto Costa · Bednarek", "Kiwior · Zaidu · Pablo Rosário", "Froholdt · Pietuszewski · Gimenez"]
    for i, n in enumerate(nomes):
        kk = suave((t - T(1.0) - i * 0.25) / 0.25)
        if kk > 0:
            al = int(255 * kk)
            y = CY0 + 400 + i * 80
            d.rounded_rectangle((90, y - 32, W - 90, y + 32), radius=16, fill=(36, 34, 32, al))
            d.text((W / 2, y), n, font=fonte(SANS_SB, 34), fill=CREME + (al,), anchor="mm")
    kk = suave((t - T(4.6)) / 0.25)
    if kk > 0:
        d.text((W / 2, CY0 + 690), "Rosário · 8 desarmes · 10 cortes", font=fonte(SERIFA_N, 44),
               fill=CORAL + (int(255 * kk),), anchor="mm")
    q.im.paste(ov, (0, 0), ov)


def final(v, q, t):
    ov = _ov(q)
    d = ImageDraw.Draw(ov)
    d.rectangle((0, CY0 + CH * 0.08, W, CY0 + CH * 0.88), fill=(20, 20, 19, 232))
    d.text((W / 2, CY0 + 150), "2.ª PARTE", font=fonte(SANS_SB, 34), fill=CORAL + (255,), anchor="mm")
    k = suave((t - T(0.8)) / 0.25)
    if k > 0:
        d.text((W / 2, CY0 + 270), "O Feyenoord carrega", font=fonte(SERIFA_N, 62), fill=CREME + (int(255 * k),),
               anchor="mm")
    k = suave((t - T(3.2)) / 0.25)
    if k > 0:
        al = int(255 * k)
        d.rounded_rectangle((120, CY0 + 380, W - 120, CY0 + 500), radius=24, fill=(36, 34, 32, al),
                            outline=VERMELHO + (al,), width=3)
        d.text((W / 2, CY0 + 440), "Golo da casa? NÃO VALEU", font=fonte(SANS_SB, 44), fill=CREME + (al,),
               anchor="mm")
    k = suave((t - T(5.8)) / 0.25)
    if k > 0:
        al = int(255 * k)
        d.ellipse((W / 2 - 80, CY0 + 590, W / 2 + 80, CY0 + 750), fill=AZUL_FCP + (al,), outline=CREME + (al,),
                  width=4)
        d.text((W / 2, CY0 + 665), "DC", font=fonte(SANS_SB, 56), fill=CREME + (al,), anchor="mm")
        d.text((W / 2, CY0 + 790), "Diogo Costa segura o 0–1", font=fonte(SANS_SB, 34), fill=CREME + (al,),
               anchor="mm")
    q.im.paste(ov, (0, 0), ov)


def tabela(v, q, t):
    ov = _ov(q)
    d = ImageDraw.Draw(ov)
    d.rectangle((0, CY0 + CH * 0.08, W, CY0 + CH * 0.88), fill=(20, 20, 19, 232))
    d.text((W / 2, CY0 + 160), "LIGA DOS CAMPEÕES", font=fonte(SANS_SB, 34), fill=CORAL + (255,), anchor="mm")
    k = suave((t - T(0.3)) / 0.25)
    if k > 0:
        d.text((W / 2, CY0 + 300), "20.º", font=fonte(SERIFA_N, 170), fill=CREME + (int(255 * k),), anchor="mm")
        d.text((W / 2, CY0 + 430), "6 pontos · zona de play-off", font=fonte(SANS_SB, 38),
               fill=CORAL + (int(255 * k),), anchor="mm")
    k = suave((t - T(2.8)) / 0.25)
    if k > 0:
        _chip(d, W / 2, CY0 + 600, "9 dez · Liverpool", AZUL_FCP, k, tam=44)
    q.im.paste(ov, (0, 0), ov)


def cartao_agente(v, q, t):
    _fundo(q, t)
    d = q.d
    if PFP.exists():
        k = suave((t - 0.05) / 0.3)
        r = int(90 * (0.85 + 0.15 * k))
        im = Image.open(PFP).convert("RGB").resize((2 * r, 2 * r), Image.LANCZOS)
        m = Image.new("L", (2 * r, 2 * r), 0)
        ImageDraw.Draw(m).ellipse((0, 0, 2 * r, 2 * r), fill=int(255 * k))
        q.im.paste(im, (int(W / 2 - r), int(CY0 + 100 - r)), m)
    kk = suave((t - T(1.0)) / 0.25)
    if kk > 0:
        al = int(255 * kk)
        y = CY0 + 330
        d.rounded_rectangle((80, y - 70, W - 80, y + 70), radius=22, fill=(36, 34, 32, al),
                            outline=(70, 66, 60, al), width=2)
        d.text((190, y - 24), "Previsão · 58%", font=fonte(SANS, 28), fill=CREME_70 + (al,), anchor="lm")
        d.text((190, y + 22), "Vitória do Porto", font=fonte(SERIFA_N, 46), fill=CREME + (al,), anchor="lm")
        kv = suave((t - T(2.6)) / 0.2)
        if kv > 0:
            _visto(d, 135, y, kv, r=28)
    k = suave((t - T(4.0)) / 0.25)
    if k > 0:
        _chip(d, W / 2, CY0 + 600, "Previsões na rede vizinha · link na bio", CORAL, k, tam=34)


def pergunta(v, q, t):
    _fundo(q, t)
    d = q.d
    d.text((W / 2, CY0 + 170), "Quem mandou mais?", font=fonte(SERIFA_N, 62), fill=CREME + (255,), anchor="mm")
    for i, (letra, l1, l2, ti) in enumerate((("A", "Pietuszewski", "o cruzamento", T(1.0)),
                                             ("B", "Diogo Costa", "a porta fechada", T(1.8)))):
        kk = suave((t - ti) / 0.25)
        if kk <= 0:
            continue
        al = int(255 * kk)
        cx, cy = W / 2 + (-215 if i == 0 else 215), CY0 + 410
        d.rounded_rectangle((cx - 200, cy - 125, cx + 200, cy + 125), radius=28, fill=AZUL_FCP + (al,))
        d.text((cx, cy - 50), letra, font=fonte(SERIFA_N, 66), fill=CREME + (al,), anchor="mm")
        d.text((cx, cy + 25), l1, font=fonte(SANS_SB, 34), fill=CREME + (al,), anchor="mm")
        d.text((cx, cy + 72), l2, font=fonte(SANS, 28), fill=CREME + (al,), anchor="mm")
    k = suave((t - T(2.8)) / 0.25)
    if k > 0:
        d.text((W / 2, CY0 + 680), "Comenta A ou B", font=fonte(SANS_SB, 50), fill=CORAL + (int(255 * k),),
               anchor="mm")


def construir():
    v = Video("Feyenoord", "Porto", abrev=("FEY", "POR"),
              fonte_txt="Ilustração · dados ESPN, O Jogo, Observador, Sofascore e Agente Claudio")
    v.folga, v.bpm = 0.25, 120
    v.sp["fcp"] = sprite(17, AZUL_FCP, BRANCO, 3)
    v.sp["adv"] = sprite(17, VERMELHO, BRANCO, 3)
    cenas = []

    def cena(dur, titulo, i, jog, **kw):
        voz, leg = FALAS[i]
        c = Cena(dur, titulo, "", jog, voz=voz, legenda=leg, voz_ini=VI, **kw)
        c.voz_ref = REF_VOZ[i]
        c.abrev = ("FEY", "POR")
        cenas.append(c)
        return c

    c = cena(5.0, "Liga dos Campeões · De Kuip", 0, vazio(), sobreposicao=gancho, nomes=False)
    c.t_capa = 4.8

    # autogolo: Pietuszewski cruza da esquerda, Froholdt desvia, a bola toca no Targhalline e entra
    pos = {"a_d2": (0.40, 0.11), "a_d3": (0.58, 0.10), "a_d1": (0.22, 0.13), "a_d4": (0.78, 0.13),
           "a_m2": (0.42, 0.26), "a_m3": (0.60, 0.26), "g_a1": (0.12, 0.30), "g_a3": (0.80, 0.30),
           "g_m1": (0.36, 0.42), "g_m3": (0.66, 0.42), "g_d1": (0.12, 0.45), "g_d4": (0.88, 0.45)}
    mov = {"g_m2": vai((0.50, 0.40), (0.50, 0.14), T(1.2), T(2.8), 99),
           "a_m1": vai((0.15, 0.32), (0.20, 0.30), T(0.3), T(0.9), 99)}
    bola = [(0, 0.12, 0.30), (T(0.2), 0.12, 0.30), (T(0.9), 0.12, 0.30), (T(2.8), 0.50, 0.14), (T(3.4), 0.50, 0.14),
            (T(3.9), 0.50, 0.0)]
    cena(9.0, "Liga dos Campeões · De Kuip", 1,
         jogadores("fcp", pos, mov, {"g_a1": "Pietuszewski", "g_m2": "Froholdt", "a_d3": "Targhalline"}),
         placar="0–0", minuto="2'", vista="ataque", golo=(T(4.0), "0–1", "Autogolo"), bola=bola,
         setas=[{"pts": [(0.12, 0.30), (0.50, 0.14)], "t0": T(1.5), "t1": T(2.8), "tipo": "passe"},
                {"pts": [(0.50, 0.14), (0.50, 0.0)], "t0": T(3.4), "t1": T(3.9), "tipo": "remate"}],
         formas=[{"tipo": "rotulo", "x": 0.2, "y": 0.22, "texto": "cruzamento", "cor": CORAL, "t0": T(1.5),
                  "t1": T(3.0)},
                 {"tipo": "rotulo", "x": 0.5, "y": 0.55, "texto": "bate no Targhalline · autogolo", "cor": CORAL,
                  "t0": T(4.2), "t1": 9.0}],
         destaques=[("g_a1", T(0.2), T(1.8)), ("g_m2", T(2.2), T(4.0))])

    c = cena(7.8, "Liga dos Campeões · De Kuip", 2, vazio(), placar="0–1", minuto="HT", sobreposicao=onze,
             nomes=False)
    c.t_capa = 7.5
    c = cena(8.5, "Liga dos Campeões · De Kuip", 3, vazio(), placar="0–1", minuto="2.ª parte", sobreposicao=final,
             nomes=False)
    c.t_capa = 8.2
    c = cena(5.6, "Liga dos Campeões · De Kuip", 4, vazio(), placar="0–1", minuto="FIM", sobreposicao=tabela,
             nomes=False)
    c.t_capa = 5.3
    c = cena(7.8, "", 5, vazio(), sobreposicao=cartao_agente, nomes=False)
    c.t_capa = 7.5
    c = cena(6.8, "", 6, vazio(), sobreposicao=pergunta, nomes=False)
    c.t_capa = 6.5
    cenas.append(cena_fecho(vazio(), placar="0–1", minuto="FIM", frase=FECHO))
    return v, cenas


TIPO = "jogo"
TEMA = "Feyenoord 0-1 Porto: marcou aos 2 minutos e passou o resto a sofrer"
MATCH_ID = "20261124-UCL-feyenoord-porto"
HORA = "12:30"
POSTS = {
    "tiktok": "O Porto marcou aos 2 minutos… e passou o resto do jogo a sofrer 😅 #futebol #agenteclaudio "
              "#fcporto #championsleague #futeboltiktok",
    "instagram": "Aos 2 minutos já ganhava em Roterdão… e depois foi segurar. O Porto vence o Feyenoord (0-1) e "
                 "sobe ao 20.º lugar da Champions. O Agente Claudio deu 58% à vitória: dica certa ✅ "
                 "#fcporto #championsleague #futebol #agenteclaudio +18",
    "youtube": {"titulo": "Feyenoord 0-1 Porto: golo aos 2 minutos e 88 a sofrer #shorts",
                "descricao": "O autogolo madrugador, o Diogo Costa a segurar e o Porto no 20.º lugar da Champions. "
                             "Previsão do Agente Claudio: 58% de vitória do Porto.\n"
                             "#fcporto #championsleague #futebol #agenteclaudio"},
    "x": "Feyenoord 0-1 Porto: golo aos 2 minutos e 88 a sofrer. 6 pontos, 20.º lugar. "
         "Agente Claudio: 58% Porto ✅ #FCPorto #UCL",
}

MEMES = [
    {"modelo": "expectativa", "esq": "O que o adepto do Porto esperava", "dir": "O que teve",
     "desenho_esq": "placar:0–1", "desenho_dir": "relogio:88'", "baixo": "Marcar aos 2 minutos tem destas coisas.",
     "fala": "Vantagem cedo, unhas curtas.",
     "legenda": "Marcar cedo e sofrer o resto ⏰ #fcporto #championsleague #futebol +18"},
]
