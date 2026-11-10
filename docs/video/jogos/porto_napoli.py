"""FC Porto 4–1 Napoli (Liga dos Campeões, 4 nov 2026).

Factos (ESPN, relato e estatísticas): Porto em 4-3-3, Napoli com três centrais.
11' Bednarek, cabeça, ao centro da área, canto inferior esquerdo, canto de Gabri Veiga.
43' Diogo Costa defende Politano e Højlund (assistência de De Bruyne); McTominay marca do centro da área, alto.
56' Samu entra por André Silva; 67' Giménez por Borja Sainz e Zaidu por Martim Fernandes.
71' Gabri Veiga, pé esquerdo, centro da área, passe em profundidade de Giménez num contra-ataque.
78' Hwang In-beom por Veiga, Fofana por Pepê. 80' Kiwior, cabeça, canto de Hwang.
88' Penálti: Rafa Marín derruba Samu na área, vermelho. 90' Samu marca, pé direito, canto inferior direito.
Remates 19–11, à baliza 8–6, cantos 6–5, posse 52%–48%, cartões 1–4 amarelos e 0–1 vermelho.
O Agente Claudio: vitória do Porto (52%), mais de 2.5 golos e ambas marcam (os três aconteceram).
As trajetórias são ilustrações coerentes com isto (o relato não dá a jogada inteira).
"""
from pathlib import Path

from PIL import Image, ImageDraw

from quadro_tatico import (cena_fecho, CORAL, CREME, CREME_70, CY0, CH, VERDE, W, Cena, Video, fonte, suave,
                           SERIFA_N, SANS, SANS_SB)

RAPIDEZ = 0.85
# duração (s) de cada fala na voz com que as animações foram sincronizadas
REF_VOZ = [3.44, 5.45, 6.27, 6.93, 8.88, 7.00, 6.48, 4.13, 3.83, 4.21]
# (voz, legenda): a voz tem os números por extenso, os nomes escritos como se dizem e indicações de emoção
# ([excited], [laughs]: só o modelo v3 as usa; as outras vozes ignoram-nas); a legenda é o que aparece no ecrã
FALAS = [
    ("[excited] Quatro a um ao Nápoles! E metade dos golos do Porto saiu da mesma arma secreta.",
     "4–1 ao Nápoles. E metade dos golos do Porto saiu da mesma arma secreta."),
    ("O Nápoles chegou ao Dragão com a enfermaria cheia. E o Porto, em quatro, três, três, foi para cima desde o "
     "início!",
     "O Nápoles chegou ao Dragão com a enfermaria cheia. E o Porto, em 4-3-3, foi para cima desde o início."),
    ("Minuto onze. Canto de Gábri Vêiga, bola tensa para o meio da área... [excited] Bédnárek ganha nas alturas, e "
     "cabeceia para o canto! Um a zero!",
     "11'. Canto de Gabri Veiga, bola tensa para o meio da área. Bednarek ganha nas alturas e cabeceia "
     "para o canto. 1–0!"),
    ("Mas o Nápoles reagiu. Minuto quarenta e três. Diogo Costa defende Politano! Defende Højlund! [sighs] Mas à "
     "terceira, McTominay não perdoa. Um a um.",
     "Mas o Nápoles reagiu. 43'. Diogo Costa defende Politano. Defende Højlund. Mas à terceira, "
     "McTominay não perdoa. 1–1."),
    ("Na segunda parte, o Porto mexe, e entram Sá-mu e Riménez. Aos setenta e um, o Porto sai em contra-ataque. "
     "Riménez mete nas costas da defesa, e Gábri Vêiga, de pé esquerdo, faz o dois a um!",
     "Na segunda parte, o Porto mexe: entram Samu e Giménez. Aos 71', o Porto sai em contra-ataque. Giménez mete "
     "nas costas da defesa e Gabri Veiga, de pé esquerdo, faz o 2–1."),
    ("E depois... a arma secreta, outra vez! Minuto oitenta. Canto de Huâng In-bôm, e agora é o outro central. "
     "[excited] Kívior, de cabeça! Três a um!",
     "E depois, a arma secreta outra vez. 80'. Canto de Hwang In-beom e agora é o outro central. "
     "Kiwior, de cabeça. 3–1!"),
    ("Para fechar: Sá-mu entra na área, e Rafa Marín derruba-o. Grande penalidade, e vermelho! Sá-mu bate rasteiro, "
     "para o canto. [excited] Quatro a um!",
     "Para fechar: Samu entra na área e Rafa Marín derruba-o. Grande penalidade e vermelho! Samu bate rasteiro, "
     "para o canto. 4–1."),
    ("Nos números: dezanove remates contra onze. E o Nápoles acabou com quatro amarelos, e um vermelho.",
     "Nos números: 19 remates contra 11. E o Nápoles acabou com 4 amarelos e 1 vermelho."),
    ("O Agente Claudio tinha o Porto como favorito, e golos dos dois lados. [laughs] Acertou.",
     "O Agente Claudio tinha o Porto como favorito e golos dos dois lados. Acertou."),
    ("Agora tu. Qual foi o melhor golo? Um, dois, três, ou quatro? Diz nos comentários!",
     "Agora tu: qual foi o melhor golo? 1, 2, 3 ou 4? Diz nos comentários."),
]

# ------------------------------------------------------------------ jogadores
# id: (nome, equipa, posição na formação). O Porto ataca para cima.
JOG = {
    "costa": ("D. Costa", "casa", (0.50, 0.95)),
    "martim": ("M. Fernandes", "casa", (0.15, 0.79)),
    "kiwior": ("Kiwior", "casa", (0.38, 0.85)),
    "bednarek": ("Bednarek", "casa", (0.62, 0.85)),
    "acosta": ("A. Costa", "casa", (0.85, 0.79)),
    "rosario": ("Rosario", "casa", (0.50, 0.72)),
    "veiga": ("G. Veiga", "casa", (0.33, 0.64)),
    "froholdt": ("Froholdt", "casa", (0.67, 0.64)),
    "sainz": ("B. Sainz", "casa", (0.17, 0.56)),
    "silva": ("A. Silva", "casa", (0.50, 0.55)),
    "pepe": ("Pepê", "casa", (0.83, 0.56)),
    "meret": ("Meret", "fora", (0.50, 0.05)),
    "beukema": ("Beukema", "fora", (0.33, 0.16)),
    "rrahmani": ("Rrahmani", "fora", (0.50, 0.15)),
    "marin": ("R. Marín", "fora", (0.67, 0.16)),
    "politano": ("Politano", "fora", (0.12, 0.29)),
    "anguissa": ("Anguissa", "fora", (0.38, 0.31)),
    "gilmour": ("Gilmour", "fora", (0.50, 0.25)),
    "mctominay": ("McTominay", "fora", (0.62, 0.31)),
    "vergara": ("Vergara", "fora", (0.88, 0.29)),
    "debruyne": ("De Bruyne", "fora", (0.50, 0.39)),
    "hojlund": ("Højlund", "fora", (0.50, 0.46)),
}
SUBS_67 = {"silva": "Samu", "sainz": "Giménez", "martim": "Zaidu"}
SUBS_80 = dict(SUBS_67, veiga="Hwang", pepe="Fofana", anguissa="N. Lang", vergara="Giovane")
SUBS_88 = dict(SUBS_80, politano="Lucca")


def jogadores(pos, mov=None, mostrar=(), subs=None):
    """pos = {id: (x, y)} posições fixas da cena (as que faltam ficam na formação);
    mov = {id: [(t, x, y), ...]} trajetórias; mostrar = ids com nome visível."""
    out = {}
    for jid, (nome, eq, form) in JOG.items():
        x, y = pos.get(jid, form)
        out[jid] = {"nome": (subs or {}).get(jid, nome) if jid in mostrar else "", "equipa": eq,
                    "chaves": (mov or {}).get(jid, [(0, x, y)])}
    return out


def vai(a, b, t0, t1, fim=12):
    """Trajetória simples de a para b entre t0 e t1."""
    return [(0, *a), (t0, *a), (t1, *b), (fim, *b)]


# ------------------------------------------------------------------ sobreposições

def _ov(q):
    return Image.new("RGBA", q.im.size, (0, 0, 0, 0))


def abertura(v, q, t):
    """Primeiro frame já cheio (é a capa do TikTok)."""
    ov = _ov(q)
    d = ImageDraw.Draw(ov)
    d.rectangle((0, CY0 + CH * 0.22, W, CY0 + CH * 0.74), fill=(20, 20, 19, 225))
    esc = 1.12 - 0.12 * suave(t / 0.35)
    d.text((W / 2, CY0 + CH * 0.42), "4–1", font=fonte(SERIFA_N, 260 * esc), fill=CREME + (255,), anchor="mm")
    d.text((W / 2, CY0 + CH * 0.57), "PORTO  ·  NÁPOLES", font=fonte(SANS_SB, 44), fill=CORAL + (255,), anchor="mm")
    k = suave((t - 1.4) / 0.4)
    if k > 0:
        txt = "1 arma secreta. 2 golos."
        f = fonte(SANS_SB, 40)
        larg = d.textlength(txt, font=f) + 60
        y = CY0 + CH * 0.66
        d.rounded_rectangle((W / 2 - larg / 2, y - 34, W / 2 + larg / 2, y + 34), radius=34,
                            fill=CORAL + (int(255 * k),))
        d.text((W / 2, y), txt, font=f, fill=(20, 20, 19, int(255 * k)), anchor="mm")
    q.im.paste(ov, (0, 0), ov)


def cartao_vermelho(t0, t1, nome):
    def sob(v, q, t):
        if not t0 <= t <= t1:
            return
        k = suave((t - t0) / 0.25) * suave((t1 - t) / 0.25)
        esc = 1.3 - 0.3 * suave((t - t0) / 0.25)
        cw, ch = int(170 * esc), int(240 * esc)
        c = Image.new("RGBA", (cw + 40, ch + 40), (0, 0, 0, 0))
        dc = ImageDraw.Draw(c)
        dc.rounded_rectangle((20, 20, 20 + cw, 20 + ch), radius=16, fill=(214, 48, 49, int(255 * k)),
                             outline=(250, 249, 245, int(200 * k)), width=4)
        c = c.rotate(-9, resample=Image.BICUBIC, expand=True)
        cx, cy = W / 2, CY0 + 330
        q.im.paste(c, (int(cx - c.size[0] / 2), int(cy - c.size[1] / 2)), c)
        q.d.text((cx, cy + 200), nome, font=fonte(SANS_SB, 46), fill=CREME + (int(255 * k),), anchor="mm",
                 stroke_width=5, stroke_fill=(20, 20, 19, int(230 * k)))
    return sob


def numeros(v, q, t):
    ov = _ov(q)
    d = ImageDraw.Draw(ov)
    d.rectangle((0, CY0 - 10, W, CY0 + CH + 10), fill=(20, 20, 19, int(228 * suave(t / 0.3))))
    linhas = [("Remates", 19, 11), ("Remates à baliza", 8, 6), ("Cantos", 6, 5), ("Cartões", 1, 5)]
    fn, fv = fonte(SANS_SB, 34), fonte(SERIFA_N, 70)
    d.text((W / 2, CY0 + 70), "PORTO              NÁPOLES", font=fonte(SANS_SB, 30), fill=CREME_70 + (255,),
           anchor="mm")
    for i, (nome, a, b) in enumerate(linhas):
        k = suave((t - 0.2 - i * 0.3) / 0.45)
        if k <= 0:
            continue
        y = CY0 + 210 + i * 215
        d.text((W / 2, y - 60), nome.upper(), font=fn, fill=CREME_70 + (int(255 * k),), anchor="mm")
        d.text((150, y + 10), str(a), font=fv, fill=CREME + (int(255 * k),), anchor="lm")
        d.text((W - 150, y + 10), str(b), font=fv, fill=CREME + (int(255 * k),), anchor="rm")
        x0, x1 = 300, W - 300
        meio = x0 + (x1 - x0) * a / (a + b)
        d.rounded_rectangle((x0, y, x1, y + 22), radius=11, fill=(60, 57, 53, int(255 * k)))
        d.rounded_rectangle((x0, y, x0 + (meio - x0) * k, y + 22), radius=11, fill=CORAL + (int(255 * k),))
    q.im.paste(ov, (0, 0), ov)


PFP = Path(__file__).resolve().parents[2] / "imagens" / "pfp_agente_claudio.png"


def _visto(d, cx, cy, k, r=28):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=VERDE + (int(255 * k),))
    d.line([(cx - r * 0.45, cy + 1), (cx - r * 0.12, cy + r * 0.38), (cx + r * 0.48, cy - r * 0.35)],
           fill=(20, 20, 19, int(255 * k)), width=7)


def agente(v, q, t):
    ov = _ov(q)
    ImageDraw.Draw(ov).rectangle((0, CY0 - 10, W, CY0 + CH + 10), fill=(20, 20, 19, int(238 * suave(t / 0.3))))
    q.im.paste(ov, (0, 0), ov)
    if PFP.exists():
        k = suave((t - 0.1) / 0.4)
        r = int(150 * (0.8 + 0.2 * k))
        im = Image.open(PFP).convert("RGB").resize((2 * r, 2 * r), Image.LANCZOS)
        m = Image.new("L", (2 * r, 2 * r), 0)
        ImageDraw.Draw(m).ellipse((0, 0, 2 * r, 2 * r), fill=int(255 * k))
        q.im.paste(im, (int(W / 2 - r), int(CY0 + 170 - r)), m)
    d = q.d
    k = suave((t - 0.3) / 0.4)
    d.text((W / 2, CY0 + 370), "O Agente Claudio previa", font=fonte(SANS, 44), fill=CREME_70 + (int(255 * k),),
           anchor="mm")
    itens = [("Vitória do Porto", 1.3), ("Mais de 2,5 golos", 2.2), ("Ambas marcam", 2.6)]
    for i, (txt, ti) in enumerate(itens):
        k = suave((t - ti) / 0.3)
        if k <= 0:
            continue
        y = CY0 + 480 + i * 105
        _visto(d, 300, y, k)
        d.text((350, y), txt, font=fonte(SANS_SB, 50), fill=CREME + (int(255 * k),), anchor="lm")
    k = suave((t - 3.25) / 0.25)
    if k > 0:
        esc = 1.4 - 0.4 * k
        d.text((W / 2, CY0 + 860), "ACERTOU", font=fonte(SERIFA_N, 110 * esc), fill=VERDE + (int(255 * k),),
               anchor="mm")


def pergunta(v, q, t):
    ov = _ov(q)
    ImageDraw.Draw(ov).rectangle((0, CY0 - 10, W, CY0 + CH + 10), fill=(20, 20, 19, int(238 * suave(t / 0.3))))
    q.im.paste(ov, (0, 0), ov)
    d = q.d
    k = suave((t - 0.1) / 0.4)
    d.text((W / 2, CY0 + 120), "Qual foi o melhor golo?", font=fonte(SERIFA_N, 78), fill=CREME + (int(255 * k),),
           anchor="mm")
    golos = [("1", "Bednarek", "11' · cabeça"), ("2", "G. Veiga", "71' · contra-ataque"),
             ("3", "Kiwior", "80' · cabeça"), ("4", "Samu", "90' · penálti")]
    tempos = [2.0, 2.3, 2.6, 2.8]
    for i, (n, nome, det) in enumerate(golos):
        kk = suave((t - 0.4 - i * 0.15) / 0.35)
        if kk <= 0:
            continue
        cx = W / 2 + (-215 if i % 2 == 0 else 215)
        cy = CY0 + 330 + (i // 2) * 290
        ativo = tempos[i] <= t < tempos[i] + 0.35
        cor = CORAL if ativo else (44, 42, 39)
        d.rounded_rectangle((cx - 195, cy - 120, cx + 195, cy + 120), radius=28, fill=cor + (int(255 * kk),),
                            outline=(80, 76, 70, int(255 * kk)), width=2)
        d.text((cx, cy - 45), n, font=fonte(SERIFA_N, 96), fill=CREME + (int(255 * kk),), anchor="mm")
        d.text((cx, cy + 35), nome, font=fonte(SANS_SB, 40), fill=CREME + (int(255 * kk),), anchor="mm")
        d.text((cx, cy + 82), det, font=fonte(SANS, 28), fill=CREME_70 + (int(255 * kk),), anchor="mm")
    k = suave((t - 3.2) / 0.3)
    d.text((W / 2, CY0 + 930), "Comenta o número", font=fonte(SANS_SB, 48), fill=CORAL + (int(255 * k),),
           anchor="mm")


# ------------------------------------------------------------------ cenas

def construir():
    v = Video("Porto", "Nápoles", abrev=("POR", "NAP"),
              fonte_txt="Ilustração baseada no relato do jogo · dados ESPN")
    v.rapidez, v.folga, v.bpm = RAPIDEZ, 0.3, 118
    VI = 0.15  # início da voz em cada cena
    cenas = []

    def cena(dur, titulo, i, jog, **kw):
        voz, leg = FALAS[i]
        c = Cena(dur, titulo, "", jog, voz=voz, legenda=leg, voz_ini=VI, **kw)
        c.voz_ref = REF_VOZ[i]  # as jogadas foram acertadas para estas durações; uma voz mais lenta estica-as
        cenas.append(c)
        return c

    # 0. gancho: o resultado e a promessa
    c = cena(3.8, "A arma secreta do Porto", 0, jogadores({}), placar="4–1", minuto="FIM",
             sobreposicao=abertura, nomes=False)
    c.t_capa = 2.2

    # 1. o plano: o Porto sobe as linhas, o Nápoles recua
    mov = {}
    for jid, (_, eq, (x, y)) in JOG.items():
        if jid in ("costa", "meret"):
            continue
        alvo = (x, y - 0.09) if eq == "casa" else (x, y + 0.03)
        alvo = {"hojlund": (0.57, 0.40), "debruyne": (0.42, 0.36)}.get(jid, alvo)  # recuam para não chocar
        mov[jid] = vai((x, y), alvo, 2.6, 4.6)
    cena(5.6, "O plano", 1, jogadores({}, mov, mostrar=set(JOG)), placar="0–0", minuto="",
         destaques=[("bednarek", 4.0, 5.6), ("kiwior", 4.0, 5.6)])

    # 2. 11' Bednarek de cabeça, canto de Gabri Veiga (canto da direita)
    pos = {"veiga": (0.985, 0.012), "froholdt": (0.50, 0.25), "rosario": (0.55, 0.38), "martim": (0.25, 0.46),
           "acosta": (0.78, 0.42), "anguissa": (0.36, 0.14), "gilmour": (0.54, 0.20), "politano": (0.30, 0.25),
           "debruyne": (0.50, 0.30), "vergara": (0.70, 0.045), "hojlund": (0.58, 0.42), "costa": (0.5, 0.95)}
    mov = {"bednarek": vai((0.60, 0.18), (0.52, 0.108), 3.0, 4.2),
           "kiwior": vai((0.40, 0.17), (0.42, 0.08), 3.0, 4.0),
           "silva": vai((0.56, 0.13), (0.61, 0.05), 3.0, 3.9),
           "pepe": vai((0.46, 0.19), (0.47, 0.13), 3.0, 4.0),
           "sainz": vai((0.30, 0.21), (0.33, 0.17), 3.0, 4.0),
           "meret": [(0, 0.50, 0.02), (3.6, 0.49, 0.02), (4.4, 0.45, 0.018)],
           "rrahmani": vai((0.57, 0.14), (0.545, 0.12), 3.2, 4.3),
           "beukema": vai((0.42, 0.12), (0.43, 0.09), 3.0, 4.0),
           "marin": vai((0.60, 0.07), (0.62, 0.06), 3.0, 4.0),
           "mctominay": vai((0.47, 0.16), (0.46, 0.13), 3.0, 4.0)}
    bola = [(0, 0.985, 0.012), (2.9, 0.985, 0.012), (3.35, 0.83, 0.045), (3.8, 0.67, 0.085), (4.25, 0.525, 0.108),
            (4.65, 0.462, 0.0)]
    cena(6.6, "11' · Bednarek", 2, jogadores(pos, mov, mostrar={"veiga", "bednarek"}),
         bola=bola, placar="0–0", minuto="11'", vista="ataque", golo=(4.7, "1–0"),
         setas=[{"pts": [(0.985, 0.012), (0.83, 0.045), (0.67, 0.085), (0.525, 0.108)], "t0": 2.9, "t1": 4.25,
                 "tipo": "passe"},
                {"pts": [(0.60, 0.18), (0.52, 0.11)], "t0": 3.0, "t1": 4.2, "tipo": "corrida"},
                {"pts": [(0.525, 0.108), (0.462, 0.005)], "t0": 4.25, "t1": 4.65, "tipo": "remate"}],
         destaques=[("veiga", 0.6, 2.9), ("bednarek", 2.9, 5.4)])

    # 3. 43' McTominay à terceira (o Nápoles ataca para baixo; câmara na defesa do Porto)
    pos = {"costa": (0.50, 0.975), "martim": (0.20, 0.86), "acosta": (0.80, 0.86), "rosario": (0.50, 0.80),
           "veiga": (0.35, 0.76), "froholdt": (0.62, 0.77), "sainz": (0.18, 0.68), "silva": (0.50, 0.60),
           "pepe": (0.80, 0.68), "anguissa": (0.40, 0.74), "politano": (0.24, 0.855), "hojlund": (0.48, 0.875),
           "debruyne": (0.42, 0.79), "vergara": (0.82, 0.80), "gilmour": (0.50, 0.66), "beukema": (0.32, 0.52),
           "rrahmani": (0.50, 0.50), "marin": (0.68, 0.52), "meret": (0.5, 0.05)}
    mov = {"costa": [(0, 0.50, 0.975), (2.5, 0.50, 0.975), (2.9, 0.555, 0.975), (3.3, 0.51, 0.975),
                     (3.8, 0.50, 0.978), (5.5, 0.50, 0.978), (5.75, 0.47, 0.975)],
           "kiwior": vai((0.42, 0.89), (0.47, 0.93), 2.6, 4.0),
           "bednarek": vai((0.58, 0.89), (0.52, 0.935), 2.6, 4.0),
           "mctominay": vai((0.62, 0.80), (0.545, 0.885), 3.9, 5.1)}
    bola = [(0, 0.40, 0.735), (1.7, 0.40, 0.735), (2.3, 0.24, 0.85), (2.45, 0.24, 0.85), (2.85, 0.555, 0.982),
            (3.1, 0.42, 0.80), (3.4, 0.48, 0.87), (3.75, 0.50, 0.982), (4.4, 0.545, 0.89), (5.15, 0.545, 0.89),
            (5.55, 0.50, 1.0)]
    cena(7.3, "43' · McTominay", 3,
         jogadores(pos, mov, mostrar={"politano", "hojlund", "mctominay", "costa", "debruyne"}),
         bola=bola, placar="1–0", minuto="43'", vista="defesa", golo=(5.6, "1–1"),
         setas=[{"pts": [(0.24, 0.85), (0.555, 0.98)], "t0": 2.45, "t1": 2.85, "tipo": "remate"},
                {"pts": [(0.48, 0.87), (0.50, 0.98)], "t0": 3.4, "t1": 3.75, "tipo": "remate"},
                {"pts": [(0.545, 0.89), (0.50, 0.995)], "t0": 5.15, "t1": 5.55, "tipo": "remate"}],
         destaques=[("costa", 2.4, 4.0), ("mctominay", 4.0, 6.2)])

    # 4. 71' contra-ataque: Rosario rouba, Giménez mete nas costas, Gabri Veiga marca
    pos = {"costa": (0.50, 0.95), "kiwior": (0.42, 0.84), "bednarek": (0.58, 0.84), "martim": (0.20, 0.78),
           "acosta": (0.80, 0.78), "froholdt": (0.64, 0.64), "politano": (0.18, 0.68), "vergara": (0.84, 0.66),
           "hojlund": (0.52, 0.78), "debruyne": (0.58, 0.70), "gilmour": (0.52, 0.52), "mctominay": (0.62, 0.60)}
    mov = {"anguissa": [(0, 0.40, 0.60), (1.4, 0.44, 0.62), (3.0, 0.46, 0.65), (12, 0.46, 0.65)],
           "rosario": [(0, 0.50, 0.70), (2.8, 0.49, 0.69), (3.3, 0.47, 0.665), (12, 0.47, 0.665)],
           "sainz": [(0, 0.30, 0.52), (3.4, 0.30, 0.52), (3.95, 0.36, 0.50), (4.9, 0.40, 0.34), (12, 0.40, 0.34)],
           "veiga": [(0, 0.40, 0.62), (3.4, 0.42, 0.61), (5.75, 0.50, 0.20), (6.8, 0.50, 0.14), (12, 0.50, 0.14)],
           "silva": vai((0.58, 0.50), (0.63, 0.16), 3.5, 6.5),
           "pepe": vai((0.82, 0.52), (0.76, 0.28), 3.5, 6.0),
           "beukema": vai((0.30, 0.42), (0.42, 0.21), 3.6, 6.5),
           "rrahmani": vai((0.50, 0.44), (0.53, 0.17), 3.6, 6.8),
           "marin": vai((0.68, 0.42), (0.59, 0.20), 3.6, 6.5),
           "meret": [(0, 0.50, 0.04), (6.6, 0.50, 0.05), (7.3, 0.45, 0.025)]}
    bola = [(0, 0.62, 0.59), (0.9, 0.62, 0.59), (1.4, 0.44, 0.61), (3.0, 0.46, 0.64), (3.3, 0.47, 0.655),
            (3.45, 0.47, 0.655), (3.95, 0.36, 0.49), (4.9, 0.40, 0.33), (5.0, 0.40, 0.33), (5.75, 0.50, 0.19),
            (6.8, 0.50, 0.13), (6.9, 0.50, 0.13), (7.3, 0.47, 0.0)]
    cena(9.3, "71' · Gabri Veiga", 4,
         jogadores(pos, mov, mostrar={"silva", "sainz", "veiga", "rosario"}, subs=SUBS_67),
         bola=bola, placar="1–1", minuto="71'", golo=(7.35, "2–1"),
         setas=[{"pts": [(0.47, 0.655), (0.36, 0.49)], "t0": 3.45, "t1": 3.95, "tipo": "passe"},
                {"pts": [(0.36, 0.49), (0.40, 0.33)], "t0": 3.95, "t1": 4.9, "tipo": "conducao"},
                {"pts": [(0.42, 0.61), (0.50, 0.20)], "t0": 3.4, "t1": 5.75, "tipo": "corrida"},
                {"pts": [(0.40, 0.33), (0.50, 0.19)], "t0": 5.0, "t1": 5.75, "tipo": "passe"},
                {"pts": [(0.50, 0.13), (0.47, 0.005)], "t0": 6.9, "t1": 7.3, "tipo": "remate"}],
         destaques=[("silva", 1.9, 2.6), ("sainz", 2.3, 3.0), ("rosario", 3.0, 3.6), ("sainz", 3.6, 5.2),
                    ("veiga", 5.2, 8.0)])

    # 5. 80' Kiwior de cabeça, canto de Hwang (canto da esquerda): a arma secreta outra vez
    pos = {"veiga": (0.015, 0.012), "pepe": (0.62, 0.22), "froholdt": (0.50, 0.26), "rosario": (0.50, 0.38),
           "martim": (0.22, 0.42), "acosta": (0.75, 0.44), "costa": (0.5, 0.95), "anguissa": (0.42, 0.15),
           "gilmour": (0.56, 0.21), "vergara": (0.30, 0.045), "politano": (0.70, 0.25), "debruyne": (0.48, 0.29),
           "hojlund": (0.40, 0.42), "meret": (0.50, 0.02)}
    mov = {"kiwior": vai((0.40, 0.19), (0.49, 0.105), 4.0, 5.2),
           "bednarek": vai((0.58, 0.17), (0.60, 0.08), 3.9, 4.9),
           "silva": vai((0.52, 0.13), (0.38, 0.065), 3.9, 4.8),
           "sainz": vai((0.45, 0.18), (0.55, 0.12), 3.9, 4.9),
           "rrahmani": vai((0.47, 0.15), (0.505, 0.125), 4.2, 5.3),
           "beukema": vai((0.58, 0.12), (0.57, 0.10), 4.0, 5.0),
           "marin": vai((0.40, 0.07), (0.39, 0.06), 4.0, 5.0),
           "mctominay": vai((0.54, 0.15), (0.53, 0.13), 4.0, 5.0),
           "meret": [(0, 0.50, 0.02), (5.1, 0.51, 0.02), (5.7, 0.455, 0.018)]}
    bola = [(0, 0.015, 0.012), (3.9, 0.015, 0.012), (4.35, 0.17, 0.045), (4.8, 0.33, 0.085), (5.2, 0.49, 0.103),
            (5.6, 0.462, 0.0)]
    c = cena(7.0, "80' · Kiwior", 5, jogadores(pos, mov, mostrar={"veiga", "kiwior"}, subs=SUBS_80),
             bola=bola, placar="2–1", minuto="80'", vista="ataque", golo=(5.65, "3–1"),
             setas=[{"pts": [(0.015, 0.012), (0.17, 0.045), (0.33, 0.085), (0.49, 0.103)], "t0": 3.9, "t1": 5.2,
                     "tipo": "passe"},
                    {"pts": [(0.40, 0.19), (0.49, 0.11)], "t0": 4.0, "t1": 5.2, "tipo": "corrida"},
                    {"pts": [(0.49, 0.103), (0.462, 0.005)], "t0": 5.2, "t1": 5.6, "tipo": "remate"}],
             destaques=[("veiga", 2.6, 3.9), ("kiwior", 3.9, 6.4)])
    c.t_capa = 4.9

    # 6. 88'-90' Samu: derrubado por Rafa Marín, penálti, vermelho e golo
    pos = {"costa": (0.5, 0.95), "rosario": (0.50, 0.42), "martim": (0.22, 0.45), "acosta": (0.78, 0.45),
           "kiwior": (0.40, 0.55), "bednarek": (0.60, 0.55), "debruyne": (0.45, 0.32), "politano": (0.25, 0.30),
           "vergara": (0.75, 0.33), "hojlund": (0.50, 0.45), "anguissa": (0.38, 0.25)}
    mov = {"pepe": [(0, 0.55, 0.40), (12, 0.55, 0.40)],
           "silva": [(0, 0.64, 0.31), (1.0, 0.64, 0.30), (2.3, 0.585, 0.16), (2.6, 0.575, 0.15), (3.5, 0.575, 0.15),
                     (4.0, 0.51, 0.135), (12, 0.51, 0.135)],
           "marin": [(0, 0.72, 0.30), (0.9, 0.72, 0.29), (2.35, 0.60, 0.17), (3.4, 0.60, 0.17), (4.2, 0.97, 0.30)],
           "sainz": vai((0.40, 0.28), (0.36, 0.18), 1.0, 2.6),
           "veiga": vai((0.30, 0.36), (0.32, 0.20), 3.4, 4.0),
           "froholdt": vai((0.62, 0.40), (0.66, 0.19), 3.4, 4.0),
           "rrahmani": vai((0.50, 0.16), (0.42, 0.18), 3.4, 4.0),
           "beukema": vai((0.40, 0.16), (0.36, 0.19), 3.4, 4.0),
           "mctominay": vai((0.56, 0.22), (0.62, 0.19), 3.4, 4.0),
           "gilmour": vai((0.52, 0.26), (0.55, 0.19), 3.4, 4.0),
           "meret": [(0, 0.50, 0.03), (3.6, 0.50, 0.02), (4.45, 0.50, 0.02), (4.85, 0.45, 0.02)]}
    bola = [(0, 0.55, 0.39), (0.6, 0.55, 0.39), (1.0, 0.63, 0.31), (2.3, 0.575, 0.155), (2.6, 0.57, 0.14),
            (3.5, 0.57, 0.14), (3.9, 0.50, 0.105), (4.45, 0.50, 0.105), (4.85, 0.545, 0.0)]
    cena(6.8, "90' · Samu", 6, jogadores(pos, mov, mostrar={"silva", "marin", "pepe"}, subs=SUBS_88),
         bola=bola, placar="3–1", minuto="90'", vista="ataque", golo=(4.9, "4–1"),
         sobreposicao=cartao_vermelho(3.3, 4.4, "Rafa Marín"),
         setas=[{"pts": [(0.55, 0.39), (0.63, 0.31)], "t0": 0.6, "t1": 1.0, "tipo": "passe"},
                {"pts": [(0.64, 0.30), (0.585, 0.16)], "t0": 1.0, "t1": 2.3, "tipo": "conducao"},
                {"pts": [(0.50, 0.105), (0.545, 0.005)], "t0": 4.45, "t1": 4.85, "tipo": "remate"}],
         destaques=[("silva", 0.8, 2.6), ("marin", 2.0, 3.3), ("silva", 4.0, 5.6)])

    # 7. números
    cena(4.5, "Os números", 7, jogadores({}), placar="4–1", minuto="FIM", sobreposicao=numeros, nomes=False)
    # 8. Agente Claudio
    c = cena(4.4, "", 8, jogadores({}), placar="4–1", minuto="FIM", sobreposicao=agente, nomes=False)
    c.t_capa = 3.8
    # 9. pergunta para os comentários
    c = cena(5.0, "", 9, jogadores({}), placar="4–1", minuto="FIM", sobreposicao=pergunta, nomes=False)
    c.t_capa = 3.6
    # 10. fecho com humor
    cenas.append(cena_fecho(jogadores({}), placar="4–1"))
    return v, cenas
