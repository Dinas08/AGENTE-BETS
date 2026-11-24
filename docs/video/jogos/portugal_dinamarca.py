"""Portugal 1–4 Dinamarca (Liga das Nações, Braga, 14 nov 2026). Ronaldo, JJ, a polémica do penálti e os piores.

Fontes (verificadas a 15 nov 2026):
- ESPN: onzes (4-2-3-1 os dois), golos: 43' Højbjerg (penálti por mão de Rúben Dias, após VAR), 49' e 57' Højlund,
  75' J. Andersen de cabeça (bola parada), 90+3' Bernardo Silva (confirmado pelo VAR). 64': Trincão, Palhinha e
  Forbs entram. Amarelo a Rúben Dias (46').
- 24Notícias: 1.º jogo depois da despedida de Ronaldo (anunciada a 5 nov); jogadores entram com camisolas 7;
  Jesus: "Faz falta para fazer companhia, mas já não joga"; "a derrota caseira mais pesada" em jogos oficiais.
- TVI: adeptos a chamar por Ronaldo; pressão homem a homem deixou "Rúben Neves e Vitinha contra o mundo";
  Félix "muito desinspirado"; as entradas "não ajudaram".
- Observador: Bruno "encostado à esquerda" e Félix no mesmo corredor, o que "esvaziava" o impacto nas costas de
  Gonçalo Ramos; Højlund livre ao segundo poste; GoalPoint: Rúben Dias com nota 4.0 aos 55'; Dias falha Cardiff.
- Zerozero (SAPO): Renato Veiga "Uma barata tonta", "driblado com facilidade no terceiro golo"; Dias deixou Højlund
  sozinho; Neves, Vitinha e Veiga "acumularam passes falhados".
- A Bola (Pedro Henriques): penálti bem assinalado, braço "fora do plano do corpo"; golo dinamarquês anulado aos
  38' por fora de jogo; golo de Bernardo validado pelo VAR. Árbitro: Rade Obrenovic.
- DN: Portugal 1.º com 12 pontos, já nos quartos; precisa de um ponto em Cardiff (17 nov) para ficar em 1.º.
- Dica do canal: mais de 2,5 golos — acertou.
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
    ("O primeiro jogo depois do Ronaldo. Homenagem, camisolas sete... e um a quatro, em casa. A derrota caseira mais "
     "pesada de sempre, em jogos oficiais.",
     "O primeiro jogo depois do Ronaldo. Homenagem, camisolas 7… e 1–4, em casa. A derrota caseira mais pesada de "
     "sempre em jogos oficiais."),
    ("Em Braga, os adeptos chamaram pelo Ronaldo. E o Jorge Jesus respondeu assim: faz falta para fazer companhia, "
     "mas já não joga.",
     "Em Braga, os adeptos chamaram pelo Ronaldo. E Jorge Jesus respondeu assim: faz falta para fazer companhia, "
     "mas já não joga."),
    ("O plano do JJ: pressão homem a homem. Resultado? O Rúben Neves e o Vitinha contra o mundo. E com o Bruno e o "
     "Félix no mesmo corredor, o Gonçalo Ramos ficou sozinho lá na frente.",
     "O plano do JJ: pressão homem a homem. Resultado? Rúben Neves e Vitinha contra o mundo. E com o Bruno e o "
     "Félix no mesmo corredor, o Gonçalo Ramos ficou sozinho lá na frente."),
    ("Agora, a polémica. Aos quarenta, a bola bate no braço do Rúben Dias. O árbitro não viu, mas o VAR chamou-o: "
     "penálti. Exagero? O Pedro Henriques diz que não: o braço estava fora do plano do corpo.",
     "Agora, a polémica. Aos 40', a bola bate no braço do Rúben Dias. O árbitro não viu, mas o VAR chamou-o: "
     "penálti. Exagero? O Pedro Henriques diz que não: o braço estava fora do plano do corpo."),
    ("E na segunda parte, desabou. O Højlund aparece sozinho nas costas do Rúben Dias. Depois bisa, a ganhar a "
     "posição ao Renato Veiga. E no quarto, o Andersen cabeceia sozinho num livre.",
     "E na segunda parte, desabou. O Højlund aparece sozinho nas costas do Rúben Dias. Depois bisa, a ganhar a "
     "posição ao Renato Veiga. E no quarto, o Andersen cabeceia sozinho num livre."),
    ("Os piores em campo? O Rúben Dias: penálti, amarelo, e o Højlund à solta. O Renato Veiga, driblado com "
     "facilidade no terceiro golo. O Rúben Neves e o Vitinha, com passes falhados atrás de passes falhados. E até o "
     "Félix andou desinspirado.",
     "Os piores em campo? Rúben Dias: penálti, amarelo e o Højlund à solta. Renato Veiga, driblado com facilidade "
     "no terceiro golo. Rúben Neves e Vitinha, com passes falhados atrás de passes falhados. E até o Félix andou "
     "desinspirado."),
    ("O JJ mexeu aos sessenta e quatro, mas o ataque continuou sem produzir. O Bernardo ainda marcou, confirmado pelo "
     "VAR. Portugal continua em primeiro, já está nos quartos, mas vai a Cardiff sem o Rúben Dias.",
     "O JJ mexeu aos 64', mas o ataque continuou sem produzir. O Bernardo ainda marcou, confirmado pelo VAR. "
     "Portugal continua em primeiro, já está nos quartos, mas vai a Cardiff sem o Rúben Dias."),
    ("E o Agente Claudio? A dica foi mais de dois golos e meio... e entrou. As dicas estão na rede vizinha, link na "
     "bio. E tu: a culpa é do JJ, ou dos jogadores? Diz nos comentários.",
     "E o Agente Claudio? A dica foi mais de 2,5 golos e entrou. As dicas estão na rede vizinha, link na bio. "
     "E tu: a culpa é do JJ ou dos jogadores? Diz nos comentários."),
]

# ------------------------------------------------------------------ jogadores (Portugal ataca para cima)
JOG = {
    "costa": ("Diogo Costa", "casa", (0.50, 0.95)),
    "dalot": ("Dalot", "casa", (0.15, 0.79)),
    "veiga": ("Renato Veiga", "casa", (0.38, 0.85)),
    "dias": ("Rúben Dias", "casa", (0.62, 0.85)),
    "acosta": ("Alberto Costa", "casa", (0.85, 0.79)),
    "vitinha": ("Vitinha", "casa", (0.40, 0.70)),
    "neves": ("Rúben Neves", "casa", (0.60, 0.70)),
    "felix": ("João Félix", "casa", (0.50, 0.60)),
    "bruno": ("Bruno", "casa", (0.17, 0.58)),
    "neto": ("Pedro Neto", "casa", (0.83, 0.58)),
    "ramos": ("Gonçalo Ramos", "casa", (0.50, 0.53)),
    "hermansen": ("Hermansen", "fora", (0.50, 0.04)),
    "bah": ("Bah", "fora", (0.15, 0.20)),
    "andersen": ("J. Andersen", "fora", (0.38, 0.15)),
    "provstgaard": ("Provstgaard", "fora", (0.62, 0.15)),
    "maehle": ("Mæhle", "fora", (0.85, 0.20)),
    "hjulmand": ("Hjulmand", "fora", (0.40, 0.30)),
    "hojbjerg": ("Højbjerg", "fora", (0.60, 0.30)),
    "isaksen": ("Isaksen", "fora", (0.15, 0.38)),
    "damsgaard": ("Damsgaard", "fora", (0.50, 0.39)),
    "daramy": ("Daramy", "fora", (0.85, 0.38)),
    "hojlund": ("Højlund", "fora", (0.50, 0.46)),
}
BRANCO = (236, 234, 226)
VERMELHO = (200, 40, 50)
VERDE_PT = (40, 140, 80)


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
    d.text((W / 2, CY0 + CH * 0.31), "1–4", font=fonte(SERIFA_N, 230 * esc), fill=CREME + (255,), anchor="mm")
    d.text((W / 2, CY0 + CH * 0.44), "PORTUGAL  ·  DINAMARCA", font=fonte(SANS_SB, 40), fill=CORAL + (255,),
           anchor="mm")
    k = suave((t - 0.2) / 0.35)
    if k > 0:
        d.text((W / 2, CY0 + CH * 0.57), "o 1.º jogo sem Ronaldo", font=fonte(SERIFA_N, 70),
               fill=CREME + (int(255 * k),), anchor="mm")
    k = suave((t - 4.7) / 0.3)
    if k > 0:
        _chip(d, W / 2, CY0 + CH * 0.70, "A derrota caseira mais pesada em jogos oficiais", CORAL, k, tam=34)
    q.im.paste(ov, (0, 0), ov)


def jj(v, q, t):
    _fundo(q, t)
    d = q.d
    k = suave((t - 0.1) / 0.4)
    if k > 0:
        d.text((W / 2, CY0 + 230), "7", font=fonte(SERIFA_N, 420), fill=(60, 57, 53, int(255 * k)), anchor="mm")
        d.text((W / 2, CY0 + 470), "Braga a chamar pelo Ronaldo", font=fonte(SANS, 36), fill=CREME_70 + (int(255 * k),),
               anchor="mm")
    k = suave((t - 3.8) / 0.35)
    if k > 0:
        esc = 1.08 - 0.08 * k
        d.text((W / 2, CY0 + 610), "“Faz falta para fazer companhia,", font=fonte(SERIFA_N, int(54 * esc)),
               fill=CREME + (int(255 * k),), anchor="mm")
        d.text((W / 2, CY0 + 690), "mas já não joga.”", font=fonte(SERIFA_N, int(54 * esc)),
               fill=CREME + (int(255 * k),), anchor="mm")
        d.text((W / 2, CY0 + 780), "— Jorge Jesus", font=fonte(SANS_SB, 36), fill=CORAL + (int(255 * k),),
               anchor="mm")


def penalti_sob(v, q, t):
    """VAR a chamar o árbitro e a citação de Pedro Henriques."""
    k = suave((t - 4.7) / 0.25) * suave((6.4 - t) / 0.25)
    if k > 0:
        ov = _ov(q)
        d = ImageDraw.Draw(ov)
        d.rounded_rectangle((W / 2 - 230, CY0 + 300, W / 2 + 230, CY0 + 420), radius=26, fill=(24, 23, 22, int(245 * k)),
                            outline=CREME + (int(255 * k),), width=3)
        d.text((W / 2, CY0 + 340), "VAR", font=fonte(SANS_SB, 40), fill=CREME + (int(255 * k),), anchor="mm")
        d.text((W / 2, CY0 + 390), "penálti", font=fonte(SERIFA_N, 40), fill=CORAL + (int(255 * k),), anchor="mm")
        q.im.paste(ov, (0, 0), ov)
    tat.citacao(6.8, "“VAR bem ao considerar infração para castigo máximo.”", "Pedro Henriques, A Bola")(v, q, t)


def piores(v, q, t):
    _fundo(q, t)
    d = q.d
    k = suave((t - 0.1) / 0.35)
    if k > 0:
        d.text((W / 2, CY0 + 75), "Os piores em campo", font=fonte(SERIFA_N, 64), fill=CREME + (int(255 * k),),
               anchor="mm")
    lista = [("Rúben Dias", "penálti · amarelo · Højlund à solta", "nota 4.0 aos 55' (GoalPoint)", 1.2),
             ("Renato Veiga", "driblado com facilidade no 3.º golo", "“Uma barata tonta” — Zerozero", 3.9),
             ("Rúben Neves e Vitinha", "passes falhados atrás de passes falhados", "Zerozero", 6.6),
             ("João Félix", "“muito desinspirado”", "TVI", 10.1)]
    for i, (nome, sub, fonte_txt, ti) in enumerate(lista):
        kk = suave((t - ti) / 0.3)
        if kk <= 0:
            continue
        y = CY0 + 210 + i * 165
        d.rounded_rectangle((70, y - 68, W - 70, y + 68), radius=24, fill=(36, 34, 32, int(255 * kk)),
                            outline=(70, 66, 60, int(255 * kk)), width=2)
        d.rounded_rectangle((70, y - 68, 82, y + 68), radius=6, fill=(224, 92, 82, int(255 * kk)))
        d.text((112, y - 30), nome, font=fonte(SANS_SB, 40), fill=CREME + (int(255 * kk),), anchor="lm")
        d.text((112, y + 12), sub, font=fonte(SANS, 30), fill=CREME_70 + (int(255 * kk),), anchor="lm")
        d.text((112, y + 46), fonte_txt, font=fonte(SANS, 24), fill=CORAL + (int(230 * kk),), anchor="lm")


def depois(v, q, t):
    _fundo(q, t)
    d = q.d
    for i, (m, txt, sub, ti) in enumerate((("64'", "Palhinha · Forbs · Trincão", "o ataque continuou sem produzir", 0.7),
                                           ("90+3'", "Bernardo marca", "o VAR confirma", 3.3))):
        kk = suave((t - ti) / 0.3)
        if kk <= 0:
            continue
        y = CY0 + 110 + i * 130
        d.rounded_rectangle((80, y - 52, W - 80, y + 52), radius=22, fill=(36, 34, 32, int(255 * kk)))
        d.text((120, y), m, font=fonte(SERIFA_N, 44), fill=CORAL + (int(255 * kk),), anchor="lm")
        d.text((280, y - 14), txt, font=fonte(SANS_SB, 36), fill=CREME + (int(255 * kk),), anchor="lm")
        d.text((280, y + 24), sub, font=fonte(SANS, 26), fill=CREME_70 + (int(255 * kk),), anchor="lm")
    tabela = [("Portugal", 12), ("Dinamarca", 9), ("Noruega", 6), ("País de Gales", 3)]
    for i, (nome, pts) in enumerate(tabela):
        kk = suave((t - 5.7 - i * 0.12) / 0.3)
        if kk <= 0:
            continue
        y = CY0 + 400 + i * 74
        cor = CORAL if i == 0 else (44, 42, 39)
        d.rounded_rectangle((200, y - 30, W - 200, y + 30), radius=15, fill=cor + (int(255 * kk),))
        tc = (20, 20, 19) if i == 0 else CREME
        d.text((235, y), f"{i + 1}.º  {nome}", font=fonte(SANS_SB, 32), fill=tc + (int(255 * kk),), anchor="lm")
        d.text((W - 235, y), f"{pts} pts", font=fonte(SANS_SB, 32), fill=tc + (int(255 * kk),), anchor="rm")
    k = suave((t - 7.9) / 0.3)
    if k > 0:
        d.text((W / 2, CY0 + 720), "já nos quartos de final", font=fonte(SANS, 30), fill=CREME_70 + (int(255 * k),),
               anchor="mm")
    k = suave((t - 8.6) / 0.3)
    if k > 0:
        _chip(d, W / 2, CY0 + 820, "Cardiff, terça: sem Rúben Dias", CORAL, k, tam=36)


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
    k = suave((t - 1.3) / 0.3)
    if k > 0:
        d.text((W / 2, CY0 + 265), "A dica do canal", font=fonte(SANS, 36), fill=CREME_70 + (int(255 * k),),
               anchor="mm")
        d.text((W / 2 + 30, CY0 + 335), "Mais de 2,5 golos", font=fonte(SERIFA_N, 60), fill=CREME + (int(255 * k),),
               anchor="mm")
    k = suave((t - 2.85) / 0.25)
    if k > 0:
        _visto(d, W / 2 - 280, CY0 + 337, k, r=28)
    k = suave((t - 3.45) / 0.3)
    if k > 0:
        _chip(d, W / 2, CY0 + 455, "Dicas na rede vizinha · link na bio", CORAL, k, tam=34)
    k = suave((t - 5.85) / 0.3)
    if k > 0:
        d.text((W / 2, CY0 + 570), "A culpa é…", font=fonte(SERIFA_N, 70), fill=CREME + (int(255 * k),), anchor="mm")
    for i, (letra, txt) in enumerate((("A", "do JJ"), ("B", "dos jogadores"))):
        kk = suave((t - 6.2 - i * 0.15) / 0.35)
        if kk <= 0:
            continue
        cx, cy = W / 2 + (-215 if i == 0 else 215), CY0 + 740
        d.rounded_rectangle((cx - 195, cy - 85, cx + 195, cy + 85), radius=28, fill=(44, 42, 39, int(255 * kk)),
                            outline=(80, 76, 70, int(255 * kk)), width=2)
        d.text((cx, cy - 22), letra, font=fonte(SERIFA_N, 58), fill=CREME + (int(255 * kk),), anchor="mm")
        d.text((cx, cy + 40), txt, font=fonte(SANS_SB, 36), fill=CREME + (int(255 * kk),), anchor="mm")
    k = suave((t - 8.1) / 0.3)
    if k > 0:
        d.text((W / 2, CY0 + 900), "Comenta A ou B", font=fonte(SANS_SB, 46), fill=CORAL + (int(255 * k),),
               anchor="mm")


# ------------------------------------------------------------------ cenas

REF_VOZ = [8.29, 6.54, 10.57, 10.53, 9.87, 12.22, 10.88, 9.65]


def construir():
    v = Video("Portugal", "Dinamarca", abrev=("POR", "DIN"),
              fonte_txt="Ilustração · dados ESPN, Observador, TVI, Zerozero, A Bola e 24Notícias")
    v.folga, v.bpm = 0.35, 112
    v.sp["fora"] = sprite(17, BRANCO, VERMELHO, 4)   # Dinamarca
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

    c = cena(8.8, "Portugal 1–4 Dinamarca", 0, jogadores({}), placar="1–4", minuto="FIM", sobreposicao=gancho,
             nomes=False)
    c.t_capa = 6.0
    c = cena(7.0, "Ronaldo e o JJ", 1, jogadores({}), placar="", sobreposicao=jj, nomes=False)
    c.t_capa = 6.4

    # 2. o plano do JJ: pressão homem a homem; Neves e Vitinha contra o mundo; Bruno e Félix no mesmo corredor
    DIN = {"hermansen": (0.5, 0.04), "andersen": (0.36, 0.12), "provstgaard": (0.64, 0.12), "bah": (0.12, 0.26),
           "maehle": (0.88, 0.26), "hjulmand": (0.42, 0.30), "hojbjerg": (0.58, 0.30), "damsgaard": (0.50, 0.44),
           "hojlund": (0.50, 0.58)}
    POR = {"costa": (0.5, 0.93), "ramos": (0.40, 0.16), "neto": (0.66, 0.17), "bruno": (0.16, 0.31),
           "acosta": (0.84, 0.36), "vitinha": (0.58, 0.37), "neves": (0.50, 0.50), "dias": (0.55, 0.66),
           "veiga": (0.38, 0.68), "dalot": (0.20, 0.58), "felix": (0.44, 0.35)}
    mov = {"isaksen": vai((0.18, 0.46), (0.40, 0.46), T(2.6), T(4.0), 99),
           "daramy": vai((0.82, 0.46), (0.60, 0.46), T(2.6), T(4.0), 99),
           "damsgaard": vai((0.50, 0.44), (0.50, 0.48), T(2.6), T(4.0), 99),
           "felix": vai((0.44, 0.35), (0.24, 0.34), T(5.3), T(6.6), 99)}
    bola = [(0, 0.36, 0.13), (T(2.4), 0.36, 0.13), (T(3.2), 0.50, 0.475)]
    pares = [("ramos", "andersen"), ("neto", "provstgaard"), ("bruno", "bah"), ("acosta", "maehle"),
             ("felix", "hjulmand"), ("vitinha", "hojbjerg"), ("neves", "damsgaard"), ("dias", "hojlund")]
    cena(11.0, "O plano do JJ", 2, jogadores(dict(DIN, **POR), mov, mostrar={"neves", "vitinha", "bruno", "felix",
                                                                           "ramos"}),
         bola=bola, placar="0–0", minuto="",
         formas=[{"tipo": "liga", "a": a, "b": b, "cor": CORAL, "t0": T(1.0), "t1": T(4.4)} for a, b in pares] + [
             {"tipo": "rotulo", "x": 0.5, "y": 0.24, "texto": "homem a homem", "cor": CORAL, "t0": T(1.2),
              "t1": T(2.6)},
             {"tipo": "rotulo", "x": 0.5, "y": 0.60, "texto": "Neves e Vitinha contra o mundo", "cor": BRANCO,
              "t0": T(3.1), "t1": T(5.2)},
             {"tipo": "rotulo", "x": 0.26, "y": 0.42, "texto": "mesmo corredor", "cor": CORAL, "t0": T(6.0),
              "t1": T(7.8)},
             {"tipo": "rotulo", "x": 0.40, "y": 0.06, "texto": "Ramos sozinho", "cor": CORAL, "t0": T(7.9),
              "t1": 11.0}],
         destaques=[("neves", T(3.1), T(5.2)), ("vitinha", T(3.1), T(5.2)), ("ramos", T(7.9), 11.0)])

    # 3. a polémica: mão de Rúben Dias, VAR, penálti (vista da defesa de Portugal)
    pos3 = {"costa": (0.5, 0.975), "dalot": (0.20, 0.86), "veiga": (0.42, 0.89), "acosta": (0.82, 0.86),
            "vitinha": (0.40, 0.76), "neves": (0.60, 0.76), "felix": (0.50, 0.62), "bruno": (0.20, 0.66),
            "neto": (0.80, 0.66), "ramos": (0.50, 0.55), "damsgaard": (0.44, 0.80), "daramy": (0.80, 0.80),
            "hojbjerg": (0.58, 0.70), "hjulmand": (0.42, 0.66), "bah": (0.16, 0.66), "maehle": (0.86, 0.66),
            "andersen": (0.40, 0.50), "provstgaard": (0.60, 0.50), "hermansen": (0.5, 0.05)}
    mov = {"isaksen": [(0, 0.16, 0.74), (T(1.0), 0.17, 0.76), (T(1.6), 0.18, 0.78), (99, 0.18, 0.78)],
           "hojlund": vai((0.50, 0.82), (0.50, 0.885), T(1.2), T(2.3), 99),
           "dias": vai((0.58, 0.88), (0.535, 0.905), T(1.4), T(2.4), 99)}
    bola = [(0, 0.17, 0.75), (T(1.6), 0.18, 0.78), (T(2.3), 0.50, 0.88), (T(2.5), 0.53, 0.905), (T(2.9), 0.50, 0.97)]
    cena(11.3, "A polémica", 3, jogadores(pos3, mov, mostrar={"dias", "hojlund", "isaksen"}),
         bola=bola, placar="0–0", minuto="40'", vista="defesa",
         formas=[{"tipo": "rotulo", "x": 0.76, "y": 0.95, "texto": "braço de Rúben Dias", "cor": CORAL,
                  "t0": T(2.5), "t1": T(4.5)}],
         sobreposicao=penalti_sob,
         setas=[{"pts": [(0.18, 0.78), (0.50, 0.88)], "t0": T(1.6), "t1": T(2.3), "tipo": "passe"},
                {"pts": [(0.50, 0.88), (0.53, 0.905)], "t0": T(2.3), "t1": T(2.5), "tipo": "remate"}],
         destaques=[("dias", T(2.3), T(6.0))])

    # 4. a 2.ª parte desaba: Højlund sozinho nas costas de Rúben Dias (0–2); depois o 0–3 e o 0–4
    pos4 = {"costa": (0.5, 0.975), "dalot": (0.20, 0.86), "veiga": (0.40, 0.88), "acosta": (0.80, 0.86),
            "vitinha": (0.40, 0.74), "neves": (0.58, 0.74), "felix": (0.50, 0.60), "bruno": (0.22, 0.64),
            "neto": (0.80, 0.64), "ramos": (0.50, 0.54), "hjulmand": (0.40, 0.66), "hojbjerg": (0.56, 0.68),
            "isaksen": (0.34, 0.84), "daramy": (0.80, 0.78), "bah": (0.14, 0.64), "maehle": (0.86, 0.64),
            "andersen": (0.40, 0.50), "provstgaard": (0.60, 0.50), "hermansen": (0.5, 0.05)}
    mov = {"damsgaard": [(0, 0.22, 0.76), (T(1.6), 0.21, 0.78), (99, 0.21, 0.78)],
           "hojlund": vai((0.60, 0.80), (0.66, 0.895), T(1.4), T(2.6), 99),
           "dias": vai((0.56, 0.86), (0.52, 0.89), T(1.6), T(2.6), 99),
           "costa": [(0, 0.5, 0.975), (T(2.8), 0.53, 0.975), (T(3.1), 0.56, 0.975)]}
    bola = [(0, 0.21, 0.78), (T(1.9), 0.21, 0.78), (T(2.6), 0.655, 0.895), (T(2.8), 0.655, 0.895), (T(3.1), 0.50, 1.0)]
    cena(10.4, "A 2.ª parte desaba", 4, jogadores(pos4, mov, mostrar={"damsgaard", "hojlund", "dias"}),
         bola=bola, placar="0–1", minuto="49'", vista="defesa", golo=(T(3.15), "0–2", "Højlund"),
         formas=[{"tipo": "rotulo", "x": 0.82, "y": 0.95, "texto": "sozinho", "cor": CORAL, "t0": T(2.4),
                  "t1": T(4.2)},
                 {"tipo": "rotulo", "x": 0.5, "y": 0.62, "texto": "57' · Højlund ganha a Renato Veiga", "cor": CORAL,
                  "t0": T(4.3), "t1": T(6.6)},
                 {"tipo": "rotulo", "x": 0.5, "y": 0.62, "texto": "75' · Andersen sozinho num livre", "cor": CORAL,
                  "t0": T(6.8), "t1": 10.4}],
         setas=[{"pts": [(0.21, 0.78), (0.655, 0.895)], "t0": T(1.9), "t1": T(2.6), "tipo": "passe"},
                {"pts": [(0.60, 0.80), (0.66, 0.89)], "t0": T(1.4), "t1": T(2.6), "tipo": "corrida_fora"},
                {"pts": [(0.655, 0.895), (0.50, 0.995)], "t0": T(2.8), "t1": T(3.1), "tipo": "remate"}],
         destaques=[("hojlund", T(1.4), T(4.0))])

    c = cena(12.8, "Os piores", 5, jogadores({}), placar="", sobreposicao=piores, nomes=False)
    c.t_capa = 12.0
    c = cena(11.4, "E agora?", 6, jogadores({}), placar="", sobreposicao=depois, nomes=False)
    c.t_capa = 10.6
    c = cena(10.2, "", 7, jogadores({}), placar="1–4", minuto="FIM", sobreposicao=cartao_agente, nomes=False)
    c.t_capa = 8.8
    cenas.append(cena_fecho(jogadores({}), placar="1–4", frase=8))
    return v, cenas
