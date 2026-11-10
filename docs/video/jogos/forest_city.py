"""Análise tática: Nottingham Forest 3–1 Manchester City (Premier League, 7 nov 2026).

Fontes (verificadas a 7 nov 2026):
- ESPN: onzes (Forest 3-4-2-1, City 4-2-3-1), golos, substituições e estatísticas: posse 22%–78%, passes
  206–753, remates 11–12, cortes 32–18. 6' Cunha; 18' Delap num contra-ataque (assist. Schlager); 52' Cherki;
  73' Delap num contra-ataque (assist. Gibbs-White). Cunha "caught City defender Josko Gvardiol in possession";
  Delap "sprint from inside his own half and between two defenders"; Cherki após cruzamento de Doku desviado.
  3.ª derrota seguida do City na liga, "the first time in two years".
- Sky Sports: Cunha "tracked Josko Gvardiol, dispossessed him and ran through"; Schlager ganha a bola a Anderson
  e lança Delap; Forest "ran six kilometres further"; Glasner: "I had to run more than Enzo Maresca".
- 101 Great Goals: Forest a pressionar "aggressively", a estragar a saída de bola do City; xG 1,02–1,55.
- Yahoo: Forest "remained compact when defending deeper".
- Agente Claudio: no canal a dica publicada foi ambas marcam — acertou.
As jogadas são ilustrações coerentes com isto.
"""
from PIL import Image, ImageDraw

from quadro_tatico import (cena_fecho, CORAL, CREME, CREME_70, CY0, CH, VERDE, AZUL, W, Cena, Video, fonte,
                           suave, SERIFA_N, SANS, SANS_SB)

import porto_napoli as base
import porto_napoli_tatico as tat
import benfica_lech as bl

vai, _ov, PFP, _visto = base.vai, base._ov, base.PFP, base._visto
_fundo, _chip, citacao = bl._fundo, bl._chip, tat.citacao

FALAS = [
    ("Setenta e oito por cento de posse. Setecentos e cinquenta passes. E o City perdeu três a um. Explico-te "
     "como.",
     "78% de posse. 750 passes. E o City perdeu 3–1. Explico-te como."),
    ("O Forest do Glasner abdicou da bola: três centrais, e um bloco compacto atrás. Mas sempre que o City saía a "
     "jogar de trás, a pressão subia, e era agressiva.",
     "O Forest do Glasner abdicou da bola: três centrais e um bloco compacto atrás. Mas sempre que o City saía a "
     "jogar de trás, a pressão subia, e era agressiva."),
    ("Minuto seis. O central Jáir Cúnha sobe na pressão, rouba a bola ao Gvárdiol, e segue sozinho até à baliza. "
     "Um a zero.",
     "6'. O central Jair Cunha sobe na pressão, rouba a bola ao Gvardiol e segue sozinho até à baliza. 1–0."),
    ("Aos dezoito, o City perde a bola no meio-campo. O Chláguer rouba, e o Délap arranca do próprio meio-campo, "
     "entre dois centrais. Dois a zero.",
     "Aos 18', o City perde a bola no meio-campo. Schlager rouba e Delap arranca do próprio meio-campo, "
     "entre dois centrais. 2–0."),
    ("O problema do City: com tanta gente à frente da bola, cada perda era um contra-ataque. E o Forest correu "
     "mais seis quilómetros.",
     "O problema do City: com tanta gente à frente da bola, cada perda era um contra-ataque. E o Forest correu "
     "mais 6 quilómetros."),
    ("O City ainda reagiu: bola longa para o Dóku, cruzamento desviado, e o Xerqui, de primeira, reduz.",
     "O City ainda reagiu: bola longa para o Doku, cruzamento desviado e Cherki, de primeira, reduz."),
    ("Mas aos setenta e três, a mesma receita. Contra-ataque, o Guíbs Uáite mete no Délap, bis, e três a um.",
     "Mas aos 73', a mesma receita. Contra-ataque, Gibbs-White mete no Delap, bis e 3–1."),
    ("O City teve a bola, e até mais golos esperados. Mas é a terceira derrota seguida na liga, algo que não "
     "acontecia há dois anos.",
     "O City teve a bola e até mais golos esperados. Mas é a terceira derrota seguida na liga, algo que não "
     "acontecia há dois anos."),
    ("E o Agente Claudio? A dica foi ambas marcam... e acertou. As dicas estão na rede vizinha, link na bio. E tu: "
     "o City do Marésca está em crise, ou é só uma fase? Diz nos comentários.",
     "E o Agente Claudio? A dica foi ambas marcam e acertou. As dicas estão na rede vizinha, link na bio. E tu: "
     "o City do Maresca está em crise ou é só uma fase? Diz nos comentários."),
]

# ------------------------------------------------------------------ jogadores
# O Forest (casa) ataca para cima; o City ataca para baixo. Formações do ESPN.
JOG = {
    "sels": ("Sels", "casa", (0.50, 0.95)),
    "murillo": ("Murillo", "casa", (0.33, 0.85)),
    "milenkovic": ("Milenković", "casa", (0.50, 0.86)),
    "cunha": ("Jair Cunha", "casa", (0.67, 0.85)),
    "williams": ("N. Williams", "casa", (0.10, 0.72)),
    "yates": ("Yates", "casa", (0.40, 0.72)),
    "schlager": ("Schlager", "casa", (0.60, 0.72)),
    "munoz": ("Muñoz", "casa", (0.90, 0.72)),
    "gibbswhite": ("Gibbs-White", "casa", (0.36, 0.60)),
    "mcatee": ("McAtee", "casa", (0.64, 0.60)),
    "delap": ("Delap", "casa", (0.50, 0.54)),
    "donnarumma": ("Donnarumma", "fora", (0.50, 0.05)),
    "khusanov": ("Khusanov", "fora", (0.15, 0.20)),
    "dias": ("Rúben Dias", "fora", (0.38, 0.15)),
    "guehi": ("Guéhi", "fora", (0.62, 0.15)),
    "gvardiol": ("Gvardiol", "fora", (0.85, 0.20)),
    "enzo": ("Enzo", "fora", (0.40, 0.30)),
    "anderson": ("Anderson", "fora", (0.60, 0.30)),
    "ndiaye": ("Ndiaye", "fora", (0.15, 0.38)),
    "cherki": ("Cherki", "fora", (0.50, 0.39)),
    "doku": ("Doku", "fora", (0.85, 0.38)),
    "haaland": ("Haaland", "fora", (0.50, 0.46)),
}
SUBS_46 = {"gvardiol": "O'Reilly", "guehi": "M. Nunes"}
SUBS_73 = dict(SUBS_46, mcatee="Ndoye", munoz="Netz")


def jogadores(pos, mov=None, mostrar=(), subs=None):
    out = {}
    for jid, (nome, eq, form) in JOG.items():
        x, y = pos.get(jid, form)
        out[jid] = {"nome": (subs or {}).get(jid, nome) if jid in mostrar else "", "equipa": eq,
                    "chaves": (mov or {}).get(jid, [(0, x, y)])}
    return out


# o City com a bola no meio-campo do Forest; o Forest fechado em 5-4-1
CITY_ATQ = {"donnarumma": (0.50, 0.20), "dias": (0.40, 0.42), "guehi": (0.60, 0.42), "khusanov": (0.12, 0.56),
            "gvardiol": (0.88, 0.56), "enzo": (0.42, 0.56), "anderson": (0.58, 0.55), "cherki": (0.50, 0.66),
            "ndiaye": (0.20, 0.70), "doku": (0.80, 0.70), "haaland": (0.50, 0.78)}
FOR_BLOCO = {"sels": (0.50, 0.95), "williams": (0.10, 0.84), "murillo": (0.32, 0.87), "milenkovic": (0.50, 0.88),
             "cunha": (0.68, 0.87), "munoz": (0.90, 0.84), "yates": (0.40, 0.75), "schlager": (0.60, 0.75),
             "gibbswhite": (0.28, 0.73), "mcatee": (0.72, 0.73), "delap": (0.50, 0.62)}
# o City a sair de trás; o Forest a pressionar alto
CITY_SAIDA = {"donnarumma": (0.50, 0.05), "dias": (0.36, 0.13), "guehi": (0.64, 0.13), "khusanov": (0.10, 0.25),
              "gvardiol": (0.90, 0.25), "enzo": (0.42, 0.28), "anderson": (0.56, 0.27), "cherki": (0.50, 0.40),
              "ndiaye": (0.18, 0.42), "doku": (0.82, 0.42), "haaland": (0.50, 0.52)}
FOR_PRESSAO = {"sels": (0.50, 0.93), "delap": (0.42, 0.16), "gibbswhite": (0.62, 0.18), "mcatee": (0.30, 0.22),
               "cunha": (0.80, 0.34), "williams": (0.14, 0.36), "munoz": (0.86, 0.46), "yates": (0.44, 0.36),
               "schlager": (0.58, 0.35), "murillo": (0.34, 0.60), "milenkovic": (0.52, 0.62)}


# ------------------------------------------------------------------ sobreposições

def gancho(v, q, t):
    ov = _ov(q)
    d = ImageDraw.Draw(ov)
    d.rectangle((0, CY0 + CH * 0.16, W, CY0 + CH * 0.80), fill=(20, 20, 19, 228))
    esc = 1.1 - 0.1 * suave(t / 0.3)
    d.text((W / 2, CY0 + CH * 0.31), "3–1", font=fonte(SERIFA_N, 230 * esc), fill=CREME + (255,), anchor="mm")
    d.text((W / 2, CY0 + CH * 0.44), "FOREST  ·  CITY", font=fonte(SANS_SB, 40), fill=CORAL + (255,), anchor="mm")
    k = suave((t - 0.15) / 0.35)
    if k > 0:
        d.text((W / 2, CY0 + CH * 0.54), "posse de bola", font=fonte(SANS, 34), fill=CREME_70 + (int(255 * k),),
               anchor="mm")
        d.text((W / 2 - 150, CY0 + CH * 0.62), "22%", font=fonte(SERIFA_N, 88), fill=CORAL + (int(255 * k),),
               anchor="mm")
        d.text((W / 2, CY0 + CH * 0.62), "vs", font=fonte(SANS, 34), fill=CREME_70 + (int(255 * k),), anchor="mm")
        d.text((W / 2 + 150, CY0 + CH * 0.62), "78%", font=fonte(SERIFA_N, 88), fill=AZUL + (int(255 * k),),
               anchor="mm")
    k = suave((t - 4.0) / 0.3)
    if k > 0:
        _chip(d, W / 2, CY0 + CH * 0.73, "Quem tem a bola perdeu", CORAL, k)
    q.im.paste(ov, (0, 0), ov)


def km(t0):
    def sob(v, q, t):
        k = suave((t - t0) / 0.3)
        if k > 0:
            _chip(q.d, W / 2, CY0 + 470, "Forest: +6 km a correr", CORAL, k, tam=44)
    return sob


def numeros(v, q, t):
    _fundo(q, t)
    d = q.d
    k0 = suave((t - 0.1) / 0.3)
    if k0 > 0:
        d.text((W / 2, CY0 + 70), "FOREST              CITY", font=fonte(SANS_SB, 30),
               fill=CREME_70 + (int(255 * k0),), anchor="mm")
    linhas = [("Posse (%)", 22, 78, 0.3), ("Passes", 206, 753, 0.6), ("Golos esperados", 1.02, 1.55, 1.4),
              ("Golos", 3, 1, 2.2)]
    for i, (nome, a, b, ti) in enumerate(linhas):
        k = suave((t - ti) / 0.4)
        if k <= 0:
            continue
        y = CY0 + 210 + i * 190
        fv = fonte(SERIFA_N, 66)
        fmt = (lambda x: f"{x:.2f}".replace(".", ",")) if isinstance(a, float) else str
        d.text((W / 2, y - 55), nome.upper(), font=fonte(SANS_SB, 32), fill=CREME_70 + (int(255 * k),), anchor="mm")
        d.text((150, y + 10), fmt(a), font=fv, fill=CREME + (int(255 * k),), anchor="lm")
        d.text((W - 150, y + 10), fmt(b), font=fv, fill=CREME + (int(255 * k),), anchor="rm")
        x0, x1 = 320, W - 320
        meio = x0 + (x1 - x0) * a / (a + b)
        d.rounded_rectangle((x0, y, x1, y + 22), radius=11, fill=AZUL + (int(255 * k),))
        d.rounded_rectangle((x0, y, x0 + (meio - x0) * k, y + 22), radius=11, fill=CORAL + (int(255 * k),))
    k = suave((t - 2.6) / 0.3)
    if k > 0:
        _chip(d, W / 2, CY0 + 900, "3.ª derrota seguida na liga", AZUL, k, tam=38)


def _xis(d, cx, cy, k, r=24):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(224, 92, 82, int(255 * k)))
    s = r * 0.42
    d.line([(cx - s, cy - s), (cx + s, cy + s)], fill=(20, 20, 19, int(255 * k)), width=6)
    d.line([(cx - s, cy + s), (cx + s, cy - s)], fill=(20, 20, 19, int(255 * k)), width=6)


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
    # só a dica que foi publicada no canal: ambas marcam
    k = suave((t - 1.9) / 0.3)
    if k > 0:
        d.text((W / 2, CY0 + 265), "A dica do canal", font=fonte(SANS, 36), fill=CREME_70 + (int(255 * k),),
               anchor="mm")
        d.text((W / 2 + 30, CY0 + 335), "Ambas marcam", font=fonte(SERIFA_N, 62), fill=CREME + (int(255 * k),),
               anchor="mm")
    k = suave((t - 2.75) / 0.25)
    if k > 0:
        _visto(d, W / 2 - 250, CY0 + 337, k, r=28)
    k = suave((t - 3.35) / 0.3)
    if k > 0:
        _chip(d, W / 2, CY0 + 445, "Dicas na rede vizinha · link na bio", CORAL, k, tam=34)
    k = suave((t - 5.85) / 0.3)
    if k > 0:
        d.text((W / 2, CY0 + 570), "O City do Maresca…", font=fonte(SERIFA_N, 66), fill=CREME + (int(255 * k),),
               anchor="mm")
    for i, (letra, txt, ti) in enumerate((("A", "Está em crise", 7.65), ("B", "É só uma fase", 8.3))):
        kk = suave((t - 6.1 - i * 0.15) / 0.35)
        if kk <= 0:
            continue
        cx, cy = W / 2 + (-215 if i == 0 else 215), CY0 + 740
        ativo = ti <= t < ti + 0.6
        cor = CORAL if ativo else (44, 42, 39)
        d.rounded_rectangle((cx - 195, cy - 85, cx + 195, cy + 85), radius=28, fill=cor + (int(255 * kk),),
                            outline=(80, 76, 70, int(255 * kk)), width=2)
        d.text((cx, cy - 22), letra, font=fonte(SERIFA_N, 58), fill=CREME + (int(255 * kk),), anchor="mm")
        d.text((cx, cy + 40), txt, font=fonte(SANS_SB, 36), fill=CREME + (int(255 * kk),), anchor="mm")
    k = suave((t - 9.0) / 0.3)
    if k > 0:
        d.text((W / 2, CY0 + 900), "Comenta A ou B", font=fonte(SANS_SB, 46), fill=CORAL + (int(255 * k),),
               anchor="mm")


# ------------------------------------------------------------------ cenas

REF_VOZ = [5.40, 8.85, 6.34, 6.87, 7.39, 4.88, 5.97, 6.44, 10.71]


def construir():
    v = Video("Forest", "City", abrev=("FOR", "MCI"), fonte_txt="Ilustração · dados ESPN, Sky Sports e 101 Great Goals")
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
    c = cena(5.9, "Forest 3–1 City: a tática", 0, jogadores({}), placar="3–1", minuto="FIM",
             sobreposicao=gancho, nomes=False)
    c.t_capa = 4.6

    # 1. o plano do Glasner: bloco baixo de 5 e pressão alta quando o City sai de trás
    mov = {}
    for jid in JOG:
        if jid in CITY_ATQ:
            mov[jid] = [(0, *CITY_ATQ[jid]), (T(4.0), *CITY_ATQ[jid]), (T(5.4), *CITY_SAIDA[jid]), (99, *CITY_SAIDA[jid])]
        else:
            mov[jid] = [(0, *FOR_BLOCO[jid]), (T(6.0), *FOR_BLOCO[jid]), (T(7.4), *FOR_PRESSAO[jid]),
                        (99, *FOR_PRESSAO[jid])]
    bola = [(0, 0.42, 0.57), (T(4.0), 0.42, 0.57), (T(4.6), 0.40, 0.43), (T(5.4), 0.50, 0.06), (T(6.2), 0.50, 0.06),
            (T(6.8), 0.36, 0.13)]
    centrais = ["murillo", "milenkovic", "cunha"]
    cena(9.3, "O plano do Glasner", 1,
         jogadores({}, mov, mostrar={"murillo", "milenkovic", "cunha", "delap", "gibbswhite", "gvardiol"}),
         bola=bola, placar="0–0", minuto="",
         formas=[{"tipo": "linha", "ids": centrais, "cor": CORAL, "t0": T(1.8), "t1": T(4.0)},
                 {"tipo": "rotulo", "x": 0.5, "y": 0.95, "texto": "3 centrais", "cor": CORAL, "t0": T(1.8),
                  "t1": T(3.0)},
                 {"tipo": "zona", "pts": [(0.04, 0.68), (0.96, 0.68), (0.96, 0.91), (0.04, 0.91)], "cor": CORAL,
                  "rotulo": "bloco compacto", "t0": T(2.8), "t1": T(4.4)},
                 {"tipo": "rotulo", "x": 0.24, "y": 0.50, "texto": "pressão alta", "cor": CORAL, "t0": T(6.4),
                  "t1": 9.3}],
         setas=[{"pts": [FOR_BLOCO[j], FOR_PRESSAO[j]], "t0": T(6.0), "t1": T(7.4), "tipo": "corrida"}
                for j in ("delap", "gibbswhite", "mcatee", "cunha")],
         destaques=[("cunha", T(6.4), 9.3)])

    # 2. 6': Cunha sobe, rouba a Gvardiol e marca (vista de ataque do Forest)
    pos2 = dict(CITY_SAIDA, **FOR_PRESSAO)
    pos2.update({"gvardiol": (0.88, 0.24), "cunha": (0.74, 0.42)})
    mov = {"cunha": [(0, 0.74, 0.42), (T(1.5), 0.74, 0.40), (T(2.6), 0.86, 0.27), (T(3.0), 0.84, 0.25),
                     (T(4.6), 0.60, 0.12), (99, 0.60, 0.12)],
           "gvardiol": [(0, 0.88, 0.24), (T(2.9), 0.88, 0.24), (T(3.6), 0.84, 0.21)],
           "dias": vai((0.36, 0.13), (0.50, 0.12), T(3.0), T(4.6)),
           "guehi": vai((0.64, 0.13), (0.62, 0.10), T(3.0), T(4.4)),
           "donnarumma": [(0, 0.50, 0.04), (T(4.6), 0.52, 0.04), (T(5.2), 0.56, 0.03)]}
    bola = [(0, 0.36, 0.13), (T(1.0), 0.36, 0.13), (T(1.6), 0.875, 0.245), (T(2.6), 0.87, 0.25),
            (T(3.0), 0.845, 0.255), (T(4.6), 0.61, 0.125), (T(4.8), 0.61, 0.125), (T(5.2), 0.455, 0.0)]
    cena(7.2, "6' · o central a pressionar", 2, jogadores(pos2, mov, mostrar={"cunha", "gvardiol", "donnarumma"}),
         bola=bola, placar="0–0", minuto="6'", vista="ataque", golo=(T(5.25), "1–0", "Jair Cunha"),
         formas=[{"tipo": "rotulo", "x": 0.62, "y": 0.36, "texto": "central sobe", "cor": CORAL, "t0": T(1.4),
                  "t1": T(2.9)}],
         setas=[{"pts": [(0.36, 0.13), (0.875, 0.245)], "t0": T(1.0), "t1": T(1.6), "tipo": "passe"},
                {"pts": [(0.74, 0.40), (0.86, 0.27)], "t0": T(1.5), "t1": T(2.6), "tipo": "corrida"},
                {"pts": [(0.845, 0.255), (0.61, 0.125)], "t0": T(3.0), "t1": T(4.6), "tipo": "conducao"},
                {"pts": [(0.61, 0.125), (0.455, 0.005)], "t0": T(4.8), "t1": T(5.2), "tipo": "remate"}],
         destaques=[("cunha", T(1.4), 7.2)])

    # 3. 18': perda no meio-campo, Schlager rouba, Delap arranca entre dois centrais
    pos3 = dict(FOR_BLOCO, **CITY_ATQ)
    pos3.update({"anderson": (0.56, 0.55), "ndiaye": (0.46, 0.58), "schlager": (0.60, 0.66),
                 "delap": (0.50, 0.60), "donnarumma": (0.5, 0.12)})
    mov = {"schlager": vai((0.60, 0.66), (0.57, 0.565), T(2.2), T(2.8)),
           "delap": [(0, 0.50, 0.60), (T(3.1), 0.50, 0.59), (T(5.6), 0.50, 0.14), (99, 0.50, 0.14)],
           "dias": vai((0.40, 0.42), (0.45, 0.17), T(3.4), T(5.6)),
           "guehi": vai((0.60, 0.42), (0.55, 0.17), T(3.4), T(5.6)),
           "gibbswhite": vai((0.28, 0.73), (0.30, 0.40), T(3.2), T(5.6)),
           "donnarumma": [(0, 0.5, 0.12), (T(5.0), 0.5, 0.07), (T(6.0), 0.53, 0.04)]}
    bola = [(0, 0.555, 0.545), (T(2.6), 0.555, 0.545), (T(2.9), 0.57, 0.56), (T(3.1), 0.57, 0.56),
            (T(3.5), 0.50, 0.58), (T(5.6), 0.50, 0.13), (T(5.7), 0.50, 0.13), (T(6.0), 0.47, 0.0)]
    cena(7.6, "18' · a perda de bola", 3,
         jogadores(pos3, mov, mostrar={"anderson", "schlager", "delap"}),
         bola=bola, placar="1–0", minuto="18'", golo=(T(6.05), "2–0", "Delap"),
         formas=[{"tipo": "rotulo", "x": 0.5, "y": 0.47, "texto": "perda no meio-campo", "cor": AZUL,
                  "t0": T(0.9), "t1": T(2.4)}],
         setas=[{"pts": [(0.57, 0.56), (0.50, 0.58)], "t0": T(3.1), "t1": T(3.5), "tipo": "passe"},
                {"pts": [(0.50, 0.58), (0.50, 0.14)], "t0": T(3.5), "t1": T(5.6), "tipo": "conducao"},
                {"pts": [(0.50, 0.13), (0.47, 0.005)], "t0": T(5.7), "t1": T(6.0), "tipo": "remate"}],
         destaques=[("schlager", T(2.2), T(3.3)), ("delap", T(3.3), 7.6)])

    # 4. o problema do City: muita gente à frente da bola, espaço enorme atrás
    pos4 = dict(FOR_BLOCO, **CITY_ATQ)
    cena(8.0, "O problema do City", 4, jogadores(pos4, {}, mostrar={"dias", "guehi"}),
         bola=[(0, 0.42, 0.57)], placar="2–0", minuto="",
         formas=[{"tipo": "rotulo", "x": 0.5, "y": 0.63, "texto": "8 à frente da bola", "cor": AZUL, "t0": T(1.1),
                  "t1": T(3.0)},
                 {"tipo": "rotulo", "x": 0.5, "y": 0.47, "texto": "só 2 atrás", "cor": AZUL, "t0": T(2.0),
                  "t1": T(4.8)},
                 {"tipo": "zona", "pts": [(0.04, 0.08), (0.96, 0.08), (0.96, 0.38), (0.04, 0.38)], "cor": CORAL,
                  "rotulo": "espaço para o contra-ataque", "t0": T(3.0), "t1": 8.0}],
         sobreposicao=km(T(4.9)), destaques=[("dias", T(2.0), T(4.8)), ("guehi", T(2.0), T(4.8))])

    # 5. 52': bola longa para Doku, cruzamento desviado, Cherki de primeira (vista da defesa do Forest)
    pos5 = {"sels": (0.50, 0.975), "williams": (0.14, 0.86), "murillo": (0.36, 0.89), "milenkovic": (0.52, 0.90),
            "cunha": (0.70, 0.88), "munoz": (0.86, 0.84), "yates": (0.42, 0.78), "schlager": (0.60, 0.78),
            "gibbswhite": (0.30, 0.70), "mcatee": (0.72, 0.70), "delap": (0.50, 0.60),
            "guehi": (0.60, 0.50), "dias": (0.40, 0.50), "khusanov": (0.14, 0.62), "enzo": (0.44, 0.64),
            "anderson": (0.58, 0.66), "ndiaye": (0.24, 0.78), "haaland": (0.52, 0.86), "donnarumma": (0.5, 0.1)}
    mov = {"doku": vai((0.84, 0.66), (0.86, 0.80), T(0.9), T(1.8)),
           "cherki": vai((0.50, 0.72), (0.50, 0.81), T(1.6), T(3.0)),
           "gvardiol": vai((0.88, 0.58), (0.84, 0.68), T(0.9), T(2.0))}
    bola = [(0, 0.60, 0.50), (T(1.0), 0.60, 0.50), (T(1.8), 0.855, 0.80), (T(2.2), 0.855, 0.80), (T(2.55), 0.70, 0.87),
            (T(3.1), 0.505, 0.815), (T(3.2), 0.505, 0.815), (T(3.6), 0.545, 1.0)]
    cena(5.6, "52' · o City reage", 5,
         jogadores(pos5, mov, mostrar={"doku", "cherki", "guehi"}, subs=SUBS_46),
         bola=bola, placar="2–0", minuto="52'", vista="defesa", golo=(T(3.65), "2–1", "Cherki"),
         setas=[{"pts": [(0.60, 0.50), (0.855, 0.80)], "t0": T(1.0), "t1": T(1.8), "tipo": "passe"},
                {"pts": [(0.855, 0.80), (0.70, 0.87), (0.505, 0.815)], "t0": T(2.2), "t1": T(3.1), "tipo": "passe"},
                {"pts": [(0.505, 0.815), (0.545, 0.995)], "t0": T(3.2), "t1": T(3.6), "tipo": "remate"}],
         destaques=[("doku", T(1.0), T(2.4)), ("cherki", T(2.6), 5.6)])

    # 6. 73': a mesma receita. Contra-ataque, Gibbs-White mete em Delap; Glasner e o festejo
    pos6 = dict(FOR_BLOCO, **CITY_ATQ)
    pos6.update({"gibbswhite": (0.40, 0.62), "donnarumma": (0.5, 0.14)})
    mov = {"gibbswhite": [(0, 0.40, 0.66), (T(2.0), 0.40, 0.64), (T(3.1), 0.42, 0.50), (99, 0.42, 0.50)],
           "delap": [(0, 0.54, 0.58), (T(2.2), 0.54, 0.56), (T(3.9), 0.42, 0.22), (T(4.3), 0.38, 0.15),
                     (99, 0.38, 0.15)],
           "dias": vai((0.40, 0.42), (0.43, 0.20), T(2.6), T(4.4)),
           "guehi": vai((0.60, 0.42), (0.50, 0.19), T(2.6), T(4.4)),
           "donnarumma": [(0, 0.5, 0.14), (T(3.6), 0.48, 0.07), (T(4.8), 0.44, 0.04)]}
    bola = [(0, 0.40, 0.67), (T(2.0), 0.40, 0.65), (T(3.1), 0.42, 0.51), (T(3.9), 0.425, 0.23), (T(4.3), 0.385, 0.155),
            (T(4.4), 0.385, 0.155), (T(4.8), 0.545, 0.0)]
    cena(10.2, "73' · a mesma receita", 6,
         jogadores(pos6, mov, mostrar={"gibbswhite", "delap"}, subs=SUBS_73),
         bola=bola, placar="2–1", minuto="73'", golo=(T(4.85), "3–1", "Delap"),
         sobreposicao=tat.citacao(T(6.9), "“Tive de correr mais do que o Enzo Maresca.”",
                                  "Oliver Glasner, sobre o sprint no festejo do 3–1"),
         setas=[{"pts": [(0.40, 0.65), (0.42, 0.51)], "t0": T(2.0), "t1": T(3.1), "tipo": "conducao"},
                {"pts": [(0.54, 0.56), (0.38, 0.15)], "t0": T(2.2), "t1": T(4.3), "tipo": "corrida"},
                {"pts": [(0.42, 0.51), (0.425, 0.23)], "t0": T(3.1), "t1": T(3.9), "tipo": "passe"},
                {"pts": [(0.385, 0.155), (0.545, 0.005)], "t0": T(4.4), "t1": T(4.8), "tipo": "remate"}],
         destaques=[("gibbswhite", T(2.0), T(3.6)), ("delap", T(3.6), 7.0)])

    # 7. números
    cena(6.9, "Os números", 7, jogadores({}), placar="3–1", minuto="FIM", sobreposicao=numeros, nomes=False)
    # 8. Agente Claudio (com o erro) + pergunta
    c = cena(11.3, "", 8, jogadores({}), placar="3–1", minuto="FIM", sobreposicao=cartao_agente, nomes=False)
    c.t_capa = 9.4
    # 9. fecho com humor
    cenas.append(cena_fecho(jogadores({}), placar="3–1", frase=2))
    return v, cenas
