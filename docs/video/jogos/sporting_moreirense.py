"""Paulo Fonseca no Sporting: o que mudou em dois dias. Sporting 1–0 Moreirense (Liga, 7 nov 2026), a estreia.

Nunca escrever "Sporting Lisbon" (é o nome do ESPN/football-data): no vídeo é sempre "Sporting" (sigla SCP).

Fontes (verificadas a 7 nov 2026):
- ESPN: onzes (Sporting 4-3-3, Moreirense 4-2-3-1), estatísticas: posse 71%–29%, remates 19–9, à baliza 5–2,
  cantos 8–4. 61' Luis Suárez, pé esquerdo, do lado direito da área para o canto inferior esquerdo, assistência de
  Issa Doumbia num contra-ataque. Bola no poste de Silas Andersen (14').
- DAZN (perfil de 2 nov): 4x3x3 preferido, "construir desde trás", "laterais muito projectados", extremos a
  "derivar para o meio", "O ponta de lança pode baixar", "povoar a área contrária"; carreira: Paços (3.º), Braga
  (Taça), Shakhtar (três ligas), Roma, Lille, Milan, Lyon.
- Maisfutebol (antevisão): "Para mim, a melhor forma de defender é a ter a bola"; "Uma das minhas prioridades neste
  momento é meter o Sporting a defender bem"; "sem criticar o trabalho do Rui".
- O Jogo (pós-jogo): "muito mais agressiva sobre a linha defensiva do adversário"; "muito mais junta"; "excelente
  reação à perda de bola"; "O Moreirense não criou nenhuma ocasião de perigo"; "Com o 1-0, baixámos um bocadinho a
  nossa intensidade"; "perdemos muitas vezes a bola na segunda parte"; "dois dias que tivemos para treinar".
- Maisfutebol (pós-jogo): "cheguei ao clube que sonhava quando era criança".
- Agente Claudio: vitória do Sporting 82% — acertou (é a única que se mostra no vídeo).
As jogadas são ilustrações coerentes com isto.
"""
from PIL import Image, ImageDraw

from quadro_tatico import (cena_fecho, CORAL, CREME, CREME_70, CY0, CH, VERDE, AZUL, W, Cena, Video, fonte,
                           suave, SERIFA_N, SANS, SANS_SB)

import porto_napoli as base
import porto_napoli_tatico as tat
import benfica_lech as bl
import forest_city as fc

vai, _ov, PFP, _visto = base.vai, base._ov, base.PFP, base._visto
_fundo, _chip, _xis = bl._fundo, bl._chip, fc._xis

FALAS = [
    ("O Paulo Fonseca teve dois dias de treino. E o Sporting já parece outro. Vê o que mudou.",
     "Paulo Fonseca teve dois dias de treino. E o Sporting já parece outro. Vê o que mudou."),
    ("Quem é o Paulo Fonseca? Três campeonatos na Ucrânia com o Shakhtar, e depois Roma, Lille, Milan e Lyon. "
     "Agora voltou, para o clube que sonhava treinar desde criança.",
     "Quem é Paulo Fonseca? Três campeonatos na Ucrânia com o Shakhtar, e depois Roma, Lille, Milan e Lyon. "
     "Agora voltou, para o clube que sonhava treinar desde criança."),
    ("A ideia dele com bola: construir desde trás, laterais muito subidos, extremos a fugir para dentro, e muita "
     "gente na área. Como ele diz: a melhor forma de defender é ter a bola.",
     "A ideia dele com bola: construir desde trás, laterais muito subidos, extremos a fugir para dentro e muita "
     "gente na área. Como ele diz: a melhor forma de defender é ter a bola."),
    ("Mas a primeira prioridade é defender como ele acredita: pressão alta sobre a defesa adversária, a equipa "
     "junta, e reação imediata à perda da bola.",
     "Mas a primeira prioridade é defender como ele acredita: pressão alta sobre a defesa adversária, a equipa "
     "junta e reação imediata à perda da bola."),
    ("Contra o Moreirense, já se viu: setenta e um por cento de posse, dezanove remates, e nas palavras do "
     "Fonseca, o Moreirense não criou uma única ocasião de perigo.",
     "Contra o Moreirense, já se viu: 71% de posse, 19 remates e, nas palavras do Fonseca, o Moreirense "
     "não criou uma única ocasião de perigo."),
    ("O golo saiu de um contra-ataque: o Issa Dumbiá lança, e o Luís Suárez, de pé esquerdo, faz o um a zero.",
     "O golo saiu de um contra-ataque: Issa Doumbia lança e Luis Suárez, de pé esquerdo, faz o 1–0."),
    ("Mas nem tudo está feito. O próprio Fonseca admitiu: depois do golo, a equipa baixou a intensidade, e perdeu "
     "muitas bolas na segunda parte.",
     "Mas nem tudo está feito. O próprio Fonseca admitiu: depois do golo, a equipa baixou a intensidade e perdeu "
     "muitas bolas na segunda parte."),
    ("E o Agente Claudio? Deu vitória do Sporting, com oitenta e dois por cento... e acertou. As dicas estão na "
     "rede vizinha, link na bio. E tu: o Fonseca põe o Sporting a lutar pelo título? Diz nos comentários.",
     "E o Agente Claudio? Deu vitória do Sporting, com 82%, e acertou. As dicas estão na rede vizinha, link na "
     "bio. E tu: o Fonseca põe o Sporting a lutar pelo título? Diz nos comentários."),
]

# ------------------------------------------------------------------ jogadores
# O Sporting (casa) ataca para cima. Formações do ESPN.
JOG = {
    "kaique": ("Kaique", "casa", (0.50, 0.95)),
    "maxi": ("Maxi Araújo", "casa", (0.15, 0.79)),
    "inacio": ("G. Inácio", "casa", (0.38, 0.85)),
    "quaresma": ("Quaresma", "casa", (0.62, 0.85)),
    "fresneda": ("Fresneda", "casa", (0.85, 0.79)),
    "altimira": ("Altimira", "casa", (0.50, 0.72)),
    "doumbia": ("Doumbia", "casa", (0.36, 0.64)),
    "andersen": ("S. Andersen", "casa", (0.64, 0.64)),
    "irankunda": ("Irankunda", "casa", (0.17, 0.56)),
    "suarez": ("Luis Suárez", "casa", (0.50, 0.54)),
    "luisg": ("Luis Guilherme", "casa", (0.83, 0.56)),
    "aferreira": ("A. Ferreira", "fora", (0.50, 0.05)),
    "dpinto": ("D. Pinto", "fora", (0.15, 0.20)),
    "gilberto": ("Gilberto", "fora", (0.38, 0.15)),
    "kevyn": ("Kevyn", "fora", (0.62, 0.15)),
    "martinez": ("Á. Martínez", "fora", (0.85, 0.20)),
    "nile": ("Nile John", "fora", (0.40, 0.30)),
    "liberato": ("Liberato", "fora", (0.60, 0.30)),
    "chipyoka": ("Chipyoka", "fora", (0.15, 0.38)),
    "mendonca": ("Mendonça", "fora", (0.50, 0.39)),
    "landerson": ("Landerson", "fora", (0.85, 0.38)),
    "vonic": ("Vonic", "fora", (0.50, 0.46)),
}
SUBS_55 = {"vonic": "Maranhão", "chipyoka": "Leandro Santos"}


def jogadores(pos, mov=None, mostrar=(), subs=None):
    out = {}
    for jid, (nome, eq, form) in JOG.items():
        x, y = pos.get(jid, form)
        out[jid] = {"nome": (subs or {}).get(jid, nome) if jid in mostrar else "", "equipa": eq,
                    "chaves": (mov or {}).get(jid, [(0, x, y)])}
    return out


MOR_BLOCO = {"aferreira": (0.50, 0.04), "dpinto": (0.15, 0.16), "gilberto": (0.38, 0.14), "kevyn": (0.62, 0.14),
             "martinez": (0.85, 0.16), "nile": (0.40, 0.28), "liberato": (0.60, 0.28), "chipyoka": (0.15, 0.32),
             "landerson": (0.85, 0.32), "mendonca": (0.50, 0.36), "vonic": (0.50, 0.47)}


# ------------------------------------------------------------------ sobreposições

def gancho(v, q, t):
    ov = _ov(q)
    d = ImageDraw.Draw(ov)
    d.rectangle((0, CY0 + CH * 0.16, W, CY0 + CH * 0.80), fill=(20, 20, 19, 228))
    esc = 1.1 - 0.1 * suave(t / 0.3)
    d.text((W / 2, CY0 + CH * 0.31), "1–0", font=fonte(SERIFA_N, 230 * esc), fill=CREME + (255,), anchor="mm")
    d.text((W / 2, CY0 + CH * 0.44), "SPORTING  ·  MOREIRENSE", font=fonte(SANS_SB, 40), fill=CORAL + (255,),
           anchor="mm")
    k = suave((t - 0.15) / 0.35)
    if k > 0:
        d.text((W / 2, CY0 + CH * 0.55), "A estreia de", font=fonte(SANS, 36), fill=CREME_70 + (int(255 * k),),
               anchor="mm")
        d.text((W / 2, CY0 + CH * 0.62), "Paulo Fonseca", font=fonte(SERIFA_N, 84), fill=CREME + (int(255 * k),),
               anchor="mm")
    k = suave((t - 1.0) / 0.3)
    if k > 0:
        _chip(d, W / 2, CY0 + CH * 0.73, "2 dias de treino", CORAL, k)
    q.im.paste(ov, (0, 0), ov)


def percurso(v, q, t):
    _fundo(q, t)
    d = q.d
    clubes = [("Paços de Ferreira", "3.º lugar histórico", 0.6), ("Braga", "Taça de Portugal", 0.9),
              ("Shakhtar", "3 campeonatos", 2.85), ("Roma", "meias da Liga Europa", 3.85), ("Lille", "", 4.15),
              ("Milan", "", 4.65), ("Lyon", "", 4.95)]
    for i, (nome, det, ti) in enumerate(clubes):
        k = suave((t - ti) / 0.3)
        if k <= 0:
            continue
        y = CY0 + 70 + i * 92
        d.rounded_rectangle((150, y - 38, W - 150, y + 38), radius=20, fill=(44, 42, 39, int(255 * k)))
        d.text((190, y), nome, font=fonte(SANS_SB, 38), fill=CREME + (int(255 * k),), anchor="lm")
        if det:
            d.text((W - 190, y), det, font=fonte(SANS, 30), fill=CREME_70 + (int(255 * k),), anchor="rm")
    k = suave((t - 5.5) / 0.35)
    if k > 0:
        y = CY0 + 70 + 7 * 92 + 40
        esc = 1.15 - 0.15 * k
        d.rounded_rectangle((120, y - 50, W - 120, y + 50), radius=26, fill=CORAL + (int(255 * k),))
        d.text((W / 2, y), "Sporting", font=fonte(SERIFA_N, 64 * esc), fill=(20, 20, 19, int(255 * k)), anchor="mm")
        k2 = suave((t - 7.0) / 0.3)
        if k2 > 0:
            d.text((W / 2, y + 95), "“o clube que sonhava quando era criança”", font=fonte(SANS, 32),
                   fill=CREME_70 + (int(255 * k2),), anchor="mm")


def numeros(v, q, t):
    _fundo(q, t)
    d = q.d
    k0 = suave((t - 0.1) / 0.3)
    if k0 > 0:
        d.text((W / 2, CY0 + 70), "SPORTING          MOREIRENSE", font=fonte(SANS_SB, 30),
               fill=CREME_70 + (int(255 * k0),), anchor="mm")
    linhas = [("Posse (%)", 71, 29, 1.9), ("Remates", 19, 9, 2.8), ("Remates à baliza", 5, 2, 3.3)]
    for i, (nome, a, b, ti) in enumerate(linhas):
        k = suave((t - ti) / 0.4)
        if k <= 0:
            continue
        y = CY0 + 210 + i * 190
        fv = fonte(SERIFA_N, 66)
        d.text((W / 2, y - 55), nome.upper(), font=fonte(SANS_SB, 32), fill=CREME_70 + (int(255 * k),), anchor="mm")
        d.text((150, y + 10), str(a), font=fv, fill=CREME + (int(255 * k),), anchor="lm")
        d.text((W - 150, y + 10), str(b), font=fv, fill=CREME + (int(255 * k),), anchor="rm")
        x0, x1 = 320, W - 320
        meio = x0 + (x1 - x0) * a / (a + b)
        d.rounded_rectangle((x0, y, x1, y + 22), radius=11, fill=AZUL + (int(255 * k),))
        d.rounded_rectangle((x0, y, x0 + (meio - x0) * k, y + 22), radius=11, fill=CORAL + (int(255 * k),))
    k = suave((t - 4.4) / 0.35)
    if k > 0:
        y0 = CY0 + 760
        d.rounded_rectangle((70, y0, W - 70, y0 + 170), radius=26, fill=(24, 23, 22, int(245 * k)),
                            outline=(70, 66, 60, int(255 * k)), width=2)
        d.rounded_rectangle((70, y0, 82, y0 + 170), radius=6, fill=CORAL + (int(255 * k),))
        d.text((118, y0 + 62), "“O Moreirense não criou nenhuma", font=fonte(SERIFA_N, 37),
               fill=CREME + (int(255 * k),), anchor="lm")
        d.text((118, y0 + 110), "ocasião de perigo.”  — Paulo Fonseca", font=fonte(SERIFA_N, 37),
               fill=CREME + (int(255 * k),), anchor="lm")


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
    k = suave((t - 1.35) / 0.3)
    if k > 0:
        d.text((W / 2, CY0 + 265), "O Agente Claudio deu", font=fonte(SANS, 36), fill=CREME_70 + (int(255 * k),),
               anchor="mm")
        d.text((W / 2 + 30, CY0 + 335), "Vitória do Sporting · 82%", font=fonte(SERIFA_N, 56),
               fill=CREME + (int(255 * k),), anchor="mm")
    k = suave((t - 3.25) / 0.25)
    if k > 0:
        _visto(d, W / 2 - 345, CY0 + 337, k, r=28)
    k = suave((t - 4.6) / 0.3)
    if k > 0:
        _chip(d, W / 2, CY0 + 455, "Dicas na rede vizinha · link na bio", CORAL, k, tam=34)
    k = suave((t - 6.1) / 0.3)
    if k > 0:
        d.text((W / 2, CY0 + 570), "Sporting de Fonseca: título?", font=fonte(SERIFA_N, 62),
               fill=CREME + (int(255 * k),), anchor="mm")
    for i, (letra, txt) in enumerate((("A", "Vai lutar"), ("B", "Ainda não"))):
        kk = suave((t - 6.5 - i * 0.15) / 0.35)
        if kk <= 0:
            continue
        cx, cy = W / 2 + (-215 if i == 0 else 215), CY0 + 740
        d.rounded_rectangle((cx - 195, cy - 85, cx + 195, cy + 85), radius=28, fill=(44, 42, 39, int(255 * kk)),
                            outline=(80, 76, 70, int(255 * kk)), width=2)
        d.text((cx, cy - 22), letra, font=fonte(SERIFA_N, 58), fill=CREME + (int(255 * kk),), anchor="mm")
        d.text((cx, cy + 40), txt, font=fonte(SANS_SB, 38), fill=CREME + (int(255 * kk),), anchor="mm")
    k = suave((t - 9.0) / 0.3)
    if k > 0:
        d.text((W / 2, CY0 + 900), "Comenta A ou B", font=fonte(SANS_SB, 46), fill=CORAL + (int(255 * k),),
               anchor="mm")


# ------------------------------------------------------------------ cenas

REF_VOZ = [4.73, 8.78, 8.26, 7.15, 7.92, 4.57, 6.82, 10.49]


def construir():
    v = Video("Sporting", "Moreirense", abrev=("SCP", "MOR"), fonte_txt="Ilustração · dados ESPN, DAZN, O Jogo e Maisfutebol")
    v.folga, v.bpm = 0.35, 112
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
    c = cena(5.2, "Fonseca: o que mudou em 2 dias", 0, jogadores({}), placar="1–0", minuto="FIM",
             sobreposicao=gancho, nomes=False)
    c.t_capa = 3.6

    # 1. quem é Paulo Fonseca
    c = cena(9.3, "Quem é Paulo Fonseca", 1, jogadores({}), placar="", sobreposicao=percurso, nomes=False)
    c.t_capa = 8.6

    # 2. a ideia com bola: construir de trás, laterais subidos, extremos por dentro, área cheia
    pos = dict(MOR_BLOCO)
    mov = {"kaique": [(0, 0.50, 0.94)],
           "inacio": [(0, 0.33, 0.84)], "quaresma": [(0, 0.67, 0.84)],
           "altimira": [(0, 0.50, 0.74)],
           "maxi": vai((0.12, 0.70), (0.07, 0.40), T(1.9), T(3.0)),
           "fresneda": vai((0.88, 0.70), (0.93, 0.40), T(1.9), T(3.0)),
           "irankunda": [(0, 0.10, 0.46), (T(2.9), 0.10, 0.46), (T(3.9), 0.30, 0.32), (T(5.0), 0.32, 0.12),
                         (99, 0.32, 0.12)],
           "luisg": [(0, 0.90, 0.46), (T(2.9), 0.90, 0.46), (T(3.9), 0.70, 0.32), (T(5.0), 0.68, 0.12),
                     (99, 0.68, 0.12)],
           "doumbia": vai((0.38, 0.58), (0.42, 0.20), T(4.1), T(5.1), 99),
           "andersen": vai((0.62, 0.58), (0.58, 0.19), T(4.1), T(5.1), 99),
           "suarez": vai((0.50, 0.42), (0.50, 0.11), T(4.1), T(5.1), 99)}
    bola = [(0, 0.50, 0.93), (T(1.0), 0.50, 0.93), (T(1.5), 0.665, 0.835), (T(1.9), 0.665, 0.835),
            (T(2.4), 0.50, 0.735), (T(3.0), 0.50, 0.735), (T(3.6), 0.92, 0.41)]
    cena(8.8, "A ideia com bola", 2,
         jogadores(pos, mov, mostrar={"maxi", "fresneda", "irankunda", "luisg", "suarez"}),
         bola=bola, placar="", minuto="",
         formas=[{"tipo": "zona", "pts": [(0.2, 0.0), (0.8, 0.0), (0.8, 0.157), (0.2, 0.157)], "cor": CORAL,
                  "rotulo": "área cheia", "t0": T(4.6), "t1": T(5.6)}],
         sobreposicao=tat.citacao(T(5.8), "“Para mim, a melhor forma de defender é ter a bola.”",
                                  "Paulo Fonseca"),
         setas=[{"pts": [(0.50, 0.93), (0.665, 0.835)], "t0": T(1.0), "t1": T(1.5), "tipo": "passe"},
                {"pts": [(0.665, 0.835), (0.50, 0.735)], "t0": T(1.9), "t1": T(2.4), "tipo": "passe"},
                {"pts": [(0.12, 0.70), (0.07, 0.40)], "t0": T(1.9), "t1": T(3.0), "tipo": "corrida"},
                {"pts": [(0.88, 0.70), (0.93, 0.40)], "t0": T(1.9), "t1": T(3.0), "tipo": "corrida"},
                {"pts": [(0.10, 0.46), (0.30, 0.32)], "t0": T(2.9), "t1": T(3.9), "tipo": "corrida"},
                {"pts": [(0.90, 0.46), (0.70, 0.32)], "t0": T(2.9), "t1": T(3.9), "tipo": "corrida"}],
         destaques=[("maxi", T(1.9), T(3.0)), ("fresneda", T(1.9), T(3.0)), ("irankunda", T(2.9), T(4.0)),
                    ("luisg", T(2.9), T(4.0))])

    # 3. a prioridade: pressão alta, equipa junta, reação à perda
    MOR_SAIDA = {"aferreira": (0.50, 0.05), "gilberto": (0.34, 0.13), "kevyn": (0.66, 0.13), "dpinto": (0.10, 0.24),
                 "martinez": (0.90, 0.24), "nile": (0.42, 0.28), "liberato": (0.58, 0.28), "chipyoka": (0.16, 0.40),
                 "landerson": (0.84, 0.40), "mendonca": (0.50, 0.40), "vonic": (0.50, 0.52)}
    SCP_MEIO = {"kaique": (0.5, 0.94), "inacio": (0.38, 0.78), "quaresma": (0.62, 0.78), "maxi": (0.15, 0.72),
                "fresneda": (0.85, 0.72), "altimira": (0.50, 0.64), "doumbia": (0.38, 0.56), "andersen": (0.62, 0.56),
                "irankunda": (0.18, 0.48), "suarez": (0.50, 0.46), "luisg": (0.82, 0.48)}
    SCP_PRESSAO = {"kaique": (0.5, 0.90), "inacio": (0.38, 0.58), "quaresma": (0.62, 0.58), "maxi": (0.16, 0.48),
                   "fresneda": (0.84, 0.48), "altimira": (0.50, 0.42), "doumbia": (0.42, 0.33),
                   "andersen": (0.60, 0.32), "irankunda": (0.16, 0.26), "suarez": (0.40, 0.17), "luisg": (0.63, 0.18)}
    mov = {j: vai(SCP_MEIO[j], SCP_PRESSAO[j], T(2.5), T(3.8), 99) for j in SCP_MEIO}
    mov["doumbia"] = [(0, *SCP_MEIO["doumbia"]), (T(2.5), *SCP_MEIO["doumbia"]), (T(3.8), 0.42, 0.33),
                      (T(5.6), 0.42, 0.33), (T(6.0), 0.43, 0.29), (99, 0.43, 0.29)]
    bola = [(0, 0.50, 0.06), (T(1.0), 0.50, 0.06), (T(1.5), 0.345, 0.135), (T(5.0), 0.345, 0.135),
            (T(5.5), 0.42, 0.275), (T(5.9), 0.43, 0.285), (T(6.6), 0.47, 0.25)]
    pares = [("suarez", "gilberto"), ("luisg", "kevyn"), ("irankunda", "dpinto")]
    cena(7.7, "A prioridade: defender", 3, jogadores(MOR_SAIDA, mov, mostrar={"suarez", "doumbia"}),
         bola=bola, placar="", minuto="",
         formas=[{"tipo": "liga", "a": a, "b": b, "cor": CORAL, "t0": T(3.0), "t1": T(4.6)} for a, b in pares] + [
             {"tipo": "rotulo", "x": 0.5, "y": 0.08, "texto": "pressão alta", "cor": CORAL, "t0": T(2.8),
              "t1": T(4.4)},
             {"tipo": "entre", "de": ["irankunda", "suarez", "luisg"], "ate": ["maxi", "inacio", "quaresma", "fresneda"],
              "cor": CORAL, "rotulo": "equipa junta", "t0": T(4.4), "t1": T(5.6)},
             {"tipo": "rotulo", "x": 0.74, "y": 0.40, "texto": "reação à perda", "cor": CORAL, "t0": T(5.4),
              "t1": 7.7}],
         setas=[{"pts": [SCP_MEIO[j], SCP_PRESSAO[j]], "t0": T(2.5), "t1": T(3.8), "tipo": "corrida"}
                for j in ("suarez", "luisg", "irankunda")],
         destaques=[("doumbia", T(5.4), 7.7)])

    # 4. os números da estreia
    cena(8.4, "A estreia em números", 4, jogadores({}), placar="1–0", minuto="FIM", sobreposicao=numeros, nomes=False)

    # 5. 61': o golo em contra-ataque (Doumbia lança, Suárez de pé esquerdo)
    pos5 = {"kaique": (0.5, 0.94), "inacio": (0.38, 0.80), "quaresma": (0.62, 0.80), "maxi": (0.15, 0.72),
            "fresneda": (0.85, 0.70), "altimira": (0.50, 0.66), "irankunda": (0.22, 0.48), "luisg": (0.80, 0.50),
            "vonic": (0.52, 0.74), "mendonca": (0.44, 0.66), "landerson": (0.80, 0.66), "chipyoka": (0.20, 0.66),
            "nile": (0.40, 0.56), "liberato": (0.60, 0.58), "dpinto": (0.15, 0.44), "martinez": (0.85, 0.44),
            "aferreira": (0.5, 0.05)}
    mov = {"doumbia": [(0, 0.40, 0.62), (T(0.8), 0.41, 0.60), (T(1.6), 0.45, 0.50), (99, 0.45, 0.50)],
           "suarez": [(0, 0.56, 0.50), (T(1.1), 0.57, 0.48), (T(2.6), 0.68, 0.14), (99, 0.68, 0.14)],
           "andersen": vai((0.62, 0.58), (0.56, 0.24), T(1.0), T(3.0), 99),
           "gilberto": vai((0.40, 0.38), (0.50, 0.15), T(1.2), T(3.0), 99),
           "kevyn": vai((0.60, 0.38), (0.63, 0.17), T(1.2), T(3.0), 99),
           "aferreira": [(0, 0.5, 0.05), (T(2.8), 0.53, 0.04), (T(3.6), 0.47, 0.025)]}
    bola = [(0, 0.40, 0.63), (T(0.8), 0.41, 0.61), (T(1.6), 0.45, 0.51), (T(1.7), 0.45, 0.51), (T(2.4), 0.665, 0.17),
            (T(2.7), 0.68, 0.145), (T(3.2), 0.68, 0.145), (T(3.6), 0.455, 0.0)]
    cena(5.6, "61' · contra-ataque", 5,
         jogadores(pos5, mov, mostrar={"doumbia", "suarez"}, subs=SUBS_55),
         bola=bola, placar="0–0", minuto="61'", golo=(T(3.65), "1–0", "Luis Suárez"),
         setas=[{"pts": [(0.41, 0.61), (0.45, 0.51)], "t0": T(0.8), "t1": T(1.6), "tipo": "conducao"},
                {"pts": [(0.57, 0.48), (0.68, 0.14)], "t0": T(1.1), "t1": T(2.6), "tipo": "corrida"},
                {"pts": [(0.45, 0.51), (0.665, 0.17)], "t0": T(1.7), "t1": T(2.4), "tipo": "passe"},
                {"pts": [(0.68, 0.145), (0.455, 0.005)], "t0": T(3.2), "t1": T(3.6), "tipo": "remate"}],
         destaques=[("doumbia", T(0.8), T(2.0)), ("suarez", T(2.0), 5.6)])

    # 6. o que falta: a intensidade baixou depois do golo e perderam-se muitas bolas
    mov = {j: vai(SCP_PRESSAO[j], SCP_MEIO[j], T(3.6), T(4.7), 99) for j in SCP_PRESSAO}
    bola = [(0, 0.50, 0.42), (T(4.8), 0.50, 0.64), (T(5.3), 0.62, 0.56), (T(5.4), 0.61, 0.55), (T(6.0), 0.58, 0.45)]
    pos6 = dict(MOR_BLOCO)
    pos6.update({"liberato": (0.60, 0.52), "mendonca": (0.50, 0.44), "vonic": (0.52, 0.58)})
    cena(7.4, "O que ainda falta", 6, jogadores(pos6, mov, mostrar={"altimira"}, subs=SUBS_55),
         bola=bola, placar="1–0", minuto="",
         formas=[{"tipo": "rotulo", "x": 0.5, "y": 0.30, "texto": "intensidade a baixar", "cor": CORAL,
                  "t0": T(3.6), "t1": T(4.8)},
                 {"tipo": "rotulo", "x": 0.75, "y": 0.47, "texto": "bola perdida", "cor": AZUL, "t0": T(5.0),
                  "t1": 7.4}],
         setas=[{"pts": [SCP_PRESSAO[j], SCP_MEIO[j]], "t0": T(3.6), "t1": T(4.7), "tipo": "corrida"}
                for j in ("suarez", "luisg", "irankunda")])

    # 7. Agente Claudio (a dica falhou) + pergunta
    c = cena(11.0, "", 7, jogadores({}), placar="1–0", minuto="FIM", sobreposicao=cartao_agente, nomes=False)
    c.t_capa = 9.6
    # 8. fecho com humor
    cenas.append(cena_fecho(jogadores({}), placar="1–0", frase=3))
    return v, cenas
