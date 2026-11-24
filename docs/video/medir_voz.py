"""Gera (ou lê da cache) a voz de cada fala de um vídeo e mostra a duração e o tempo estimado de cada palavra.

Usar antes de montar as cenas, para sincronizar as jogadas com as palavras (tempo na cena = tempo da palavra + 0.15).
    .venv\\Scripts\\python.exe docs\\video\\medir_voz.py <nome_do_ficheiro_em_jogos>
"""
import importlib
import sys
from pathlib import Path

AQUI = Path(__file__).parent
sys.path.insert(0, str(AQUI))
sys.path.insert(0, str(AQUI / "jogos"))

import audio  # noqa: E402
from quadro_tatico import Cena, tempos_legenda  # noqa: E402

alvo = sys.argv[1] if len(sys.argv) > 1 else "porto_napoli"
if alvo.endswith(".py"):  # caminho de um ficheiro (ex.: dados/videos/x.py)
    sys.path.insert(0, str(Path(alvo).resolve().parent))
    alvo = Path(alvo).stem
mod = importlib.import_module(alvo)
# --estimar: sem voz (ex.: rotina na nuvem sem chave da ElevenLabs). Duração estimada pelo tamanho do texto
# (~0,055 s por carácter à velocidade 1,18); no render a sério as animações esticam para a voz real (REF_VOZ).
estimar = "--estimar" in sys.argv
for i, (voz, leg) in enumerate(mod.FALAS):
    if estimar:
        d = 0.3 + 0.055 * len(audio.sem_etiquetas(voz))
    else:
        a = audio.narrar(voz)
        d = len(a) / audio.SR
    c = Cena(1, voz=voz, legenda=leg, voz_ini=0)
    tempos_legenda(c, d)
    print(f"[{i}] {d:.2f}s  " + "  ".join(f"{p}@{t0:.1f}" for p, t0, _ in c.palavras))
