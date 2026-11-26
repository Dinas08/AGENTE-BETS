"""Memes do Sporting 2-2 Man United (Champions, Alvalade, 25 nov 2026). Só memes: o vídeo já foi feito
(20261126_sporting_united).

Fontes: ESPN (summary 401915373 e crónica "Lammens errors cost Man United win despite bizarre Fernandes goal"):
- 30': Lammens defende a grande penalidade de Luis Suárez; 31': derruba Maxi Araújo e faz outra; 33': Suárez marca.
- 50': o segundo golo de Bruno Fernandes (antigo jogador do Sporting) bate num torrão/irregularidade do relvado
  ("hit a divot") e passa por cima de Kaique.
"""
import math

TIPO = "memes"
TEMA = "Memes do Sporting 2-2 Man United: Lammens herói e vilão, o torrão do Bruno"
MATCH_ID = "20261125-UCL-splisbon-manunited"

CREME, FUNDO, CORAL, VERDE = (250, 249, 245), (20, 20, 19), (217, 119, 87), (126, 196, 132)
RELVA, TERRA = (40, 110, 60), (120, 82, 50)


def luva(d, caixa):
    """Luva de guarda-redes a agarrar a bola."""
    x0, y0, x1, y1 = caixa
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + 30
    d.ellipse((cx - 95, cy - 210, cx + 95, cy - 20), fill=CREME, outline=FUNDO, width=8)  # bola
    for i in range(5):
        a = i * 2 * math.pi / 5
        px, py = cx + math.sin(a) * 40, cy - 115 - math.cos(a) * 40
        d.line((cx, cy - 115, px, py), fill=FUNDO, width=6)
    d.rounded_rectangle((cx - 130, cy - 40, cx + 130, cy + 170), radius=60, fill=CORAL, outline=FUNDO, width=8)
    for k in range(4):
        fx = cx - 120 + k * 62
        d.rounded_rectangle((fx, cy - 140, fx + 52, cy + 10), radius=26, fill=CORAL, outline=FUNDO, width=7)
    d.rounded_rectangle((cx - 110, cy + 120, cx + 110, cy + 170), radius=14, fill=FUNDO)


def dupla_marca(d, caixa):
    """Duas marcas de grande penalidade, a segunda a coral: 'outra vez?'"""
    x0, y0, x1, y1 = caixa
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    d.rounded_rectangle((x0 + 10, y0 + 40, x1 - 10, y1 - 40), radius=24, fill=RELVA)
    for dx, cor in ((-80, CREME), (80, CORAL)):
        d.ellipse((cx + dx - 34, cy - 34, cx + dx + 34, cy + 34), fill=cor)
    d.text((cx, cy + 120), "×2", fill=CREME, font=__import__("quadro_tatico").fonte("palab.ttf", 90), anchor="mm")


def torrao(d, caixa):
    """Bola a saltar num torrão de relva por cima de um guarda-redes deitado."""
    x0, y0, x1, y1 = caixa
    chao = y1 - 90
    d.rectangle((x0, chao, x1, y1), fill=RELVA)
    tx = x0 + (x1 - x0) * 0.35
    d.pieslice((tx - 70, chao - 60, tx + 70, chao + 60), 180, 360, fill=TERRA)  # o torrão
    d.polygon([(tx - 60, chao - 10), (tx - 40, chao - 50), (tx - 25, chao - 12)], fill=RELVA)
    d.polygon([(tx + 10, chao - 12), (tx + 30, chao - 58), (tx + 45, chao - 10)], fill=RELVA)
    # trajetória da bola: rasteira até ao torrão, depois por cima
    pts = [(x0 + 20, chao - 25)] + [(tx + t * (x1 - 60 - tx), chao - 40 - math.sin(t * math.pi) * 330)
                                     for t in [i / 20 for i in range(21)]]
    for i in range(0, len(pts) - 1, 2):
        d.line((*pts[i], *pts[i + 1]), fill=CREME, width=7)
    bx, by = pts[11]
    d.ellipse((bx - 38, by - 38, bx + 38, by + 38), fill=CREME, outline=FUNDO, width=6)
    # guarda-redes deitado (estilizado) por baixo da bola
    gx = x0 + (x1 - x0) * 0.7
    d.rounded_rectangle((gx - 110, chao - 55, gx + 90, chao - 15), radius=20, fill=(90, 140, 200))
    d.ellipse((gx + 80, chao - 70, gx + 130, chao - 20), fill=(230, 200, 170))
    d.text((tx, chao + 50), "torrão", fill=CREME, font=__import__("quadro_tatico").fonte("seguisb.ttf", 36),
           anchor="mm")


MEMES = [
    {"modelo": "expectativa", "esq": "Lammens aos 30'", "dir": "Lammens aos 31'",
     "desenho_esq": luva, "desenho_dir": dupla_marca,
     "baixo": "Herói e vilão em 60 segundos.",
     "fala": "A adrenalina é bonita. Até deixar de ser.",
     "legenda": "Defende a grande penalidade… e faz outra logo a seguir 🧤➡️⚽ Sporting 2-2 Man United "
                "#sporting #manutd #championsleague #futebol #agenteclaudio +18"},
    {"modelo": "reacao", "topo": "O Bruno Fernandes de volta a Alvalade:", "desenho": torrao,
     "baixo": "Até o relvado quis ajudar o antigo capitão",
     "fala": "Não foi sorte. Foi um torrão com memória.",
     "legenda": "O golo do Bruno em Alvalade teve ajuda… do relvado 😅 #sporting #manutd #brunofernandes "
                "#championsleague #futebol +18"},
]
