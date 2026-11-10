"""Áudio dos vídeos: narração (Piper, voz pt-PT local e gratuita) e música de fundo original, gerada aqui
(sem direitos de autor de terceiros). A música baixa sozinha quando a voz fala (ducking)."""
import wave
from pathlib import Path

import numpy as np

SR = 44100
VOZ = Path(__file__).parent / "vozes" / "pt_PT-tugao-medium.onnx"
_voz = []


VOZ_NEURAL = "pt-PT-DuarteNeural"  # voz neural da Microsoft (edge-tts, precisa de internet)


def narrar_neural(texto: str, voz: str = VOZ_NEURAL, ritmo: str = "+18%", tom: str = "+0Hz") -> np.ndarray:
    """Texto -> áudio mono float32 a 44.1 kHz com a voz neural pt-PT (mais natural que a Piper)."""
    import asyncio
    import subprocess
    import tempfile

    import edge_tts
    import imageio_ffmpeg
    with tempfile.TemporaryDirectory() as tmp:
        mp3 = Path(tmp) / "voz.mp3"
        asyncio.run(edge_tts.Communicate(texto, voz, rate=ritmo, pitch=tom).save(str(mp3)))
        raw = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-loglevel", "error", "-i", str(mp3), "-f", "f32le",
                              "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    a = np.frombuffer(raw, np.float32).copy()
    # corta silêncio no início e no fim
    nz = np.flatnonzero(np.abs(a) > 0.01)
    if len(nz):
        a = a[max(0, nz[0] - int(0.03 * SR)): nz[-1] + int(0.08 * SR)]
    a = _encurtar_pausas(a)
    return a / (np.abs(a).max() + 1e-9) * 0.9


def _encurtar_pausas(a, maximo=0.2):
    """Pausas entre frases com mais de 'maximo' segundos ficam com 'maximo' (o ritmo fica mais vivo)."""
    jan = int(0.02 * SR)
    env = np.convolve(np.abs(a), np.ones(jan) / jan, mode='same')
    silencio = env < 0.008
    out, i, n, lim = [], 0, len(a), int(maximo * SR)
    while i < n:
        if silencio[i]:
            j = i
            while j < n and silencio[j]:
                j += 1
            if j - i > lim:
                meio = lim // 2
                out.append(a[i:i + meio])
                out.append(a[j - (lim - meio):j])
            else:
                out.append(a[i:j])
            i = j
        else:
            j = i
            while j < n and not silencio[j]:
                j += 1
            out.append(a[i:j])
            i = j
    return np.concatenate(out)


RAIZ = Path(__file__).resolve().parents[2]
CACHE = Path(__file__).parent / "cache_voz"  # não vai para o git; evita gastar créditos ao renderizar de novo


def _ler_env(nome):
    import os
    if os.environ.get(nome):
        return os.environ[nome]
    f = RAIZ / ".env"
    if f.exists():
        for linha in f.read_text(encoding="utf-8").splitlines():
            if linha.strip().startswith(nome + "="):
                return linha.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


def _mp3_para_array(mp3: Path, rapidez: float = 1.0) -> np.ndarray:
    import subprocess

    import imageio_ffmpeg
    filtro = ["-af", f"atempo={rapidez}"] if abs(rapidez - 1) > 1e-3 else []  # acelera sem mudar o tom
    raw = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-loglevel", "error", "-i", str(mp3)] + filtro +
                         ["-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    a = np.frombuffer(raw, np.float32).copy()
    nz = np.flatnonzero(np.abs(a) > 0.01)
    if len(nz):
        a = a[max(0, nz[0] - int(0.03 * SR)): nz[-1] + int(0.08 * SR)]
    return a


def narrar_elevenlabs(texto: str) -> np.ndarray:
    """Voz ElevenLabs (a mais natural). Precisa de ELEVENLABS_API_KEY e ELEVENLABS_VOICE_ID no .env.
    Cada frase fica guardada em cache_voz/, por isso renderizar de novo não gasta créditos."""
    import hashlib

    import requests
    chave, voz = _ler_env("ELEVENLABS_API_KEY"), _ler_env("ELEVENLABS_VOICE_ID")
    if not chave or not voz:
        raise RuntimeError("falta ELEVENLABS_API_KEY ou ELEVENLABS_VOICE_ID no .env")
    modelo = _ler_env("ELEVENLABS_MODEL") or "eleven_v3"
    if "v3" in modelo:
        # v3: o mais expressivo; aceita indicações de emoção no texto ([excited], [laughs]...)
        defin = {"stability": 0.5}
    else:
        texto = sem_etiquetas(texto)
        defin = {"stability": 0.3, "similarity_boost": 0.8, "style": 0.6, "use_speaker_boost": True}
    h = hashlib.sha1(f"{voz}|{modelo}|{defin}|{texto}".encode()).hexdigest()[:16]
    CACHE.mkdir(exist_ok=True)
    mp3 = CACHE / f"{h}.mp3"
    if not mp3.exists():
        r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{voz}?output_format=mp3_44100_128",
                          headers={"xi-api-key": chave, "Content-Type": "application/json"},
                          json={"text": texto, "model_id": modelo, "voice_settings": defin}, timeout=120)
        if r.status_code != 200:
            raise RuntimeError(f"ElevenLabs respondeu {r.status_code}: {r.text[:200]}")
        mp3.write_bytes(r.content)
    rapidez = float(_ler_env("ELEVENLABS_SPEED") or 1.18)
    a = _encurtar_pausas(_mp3_para_array(mp3, rapidez), maximo=0.3)
    return a / (np.abs(a).max() + 1e-9) * 0.9


def sem_etiquetas(texto: str) -> str:
    """Tira as indicações de emoção [excited] para as vozes que as leriam em voz alta."""
    import re
    return re.sub(r"\s*\[[^\]]+\]\s*", " ", texto).strip()


def narrar(texto: str, rapidez: float = 0.9) -> np.ndarray:
    """Texto -> áudio mono float32 a 44.1 kHz. Ordem: ElevenLabs (se houver chave), voz neural da Microsoft,
    e por fim a Piper (local, sem internet)."""
    if _ler_env("ELEVENLABS_API_KEY"):
        try:
            return narrar_elevenlabs(texto)
        except Exception as e:
            print(f"ElevenLabs indisponível ({e}); a usar a voz da Microsoft")
    texto = sem_etiquetas(texto)
    try:
        return narrar_neural(texto)
    except Exception as e:  # sem rede ou serviço em baixo
        print(f"voz neural indisponível ({e}); a usar a Piper")
    from piper import PiperVoice, SynthesisConfig
    if not _voz:
        _voz.append(PiperVoice.load(str(VOZ)))
    v = _voz[0]
    partes = [c.audio_float_array for c in v.synthesize(texto, syn_config=SynthesisConfig(length_scale=rapidez))]
    a = np.concatenate(partes).astype(np.float32)
    sr = v.config.sample_rate
    t_novo = np.arange(int(len(a) * SR / sr)) / SR
    a = np.interp(t_novo, np.arange(len(a)) / sr, a).astype(np.float32)
    return a / (np.abs(a).max() + 1e-9) * 0.9


# ------------------------------------------------------------------ música

def _nota(m):  # MIDI -> Hz
    return 440.0 * 2 ** ((m - 69) / 12)


def _env(n, a=0.01, r=0.3):
    t = np.arange(n) / SR
    e = np.minimum(1, t / a) * np.exp(-t / r)
    return e


def musica(dur: float, bpm: float = 96) -> np.ndarray:
    """Base calma e moderna: pad de acordes (Am–F–C–G), arpejo suave, bombo e chimbal leves. Estéreo."""
    n = int(dur * SR)
    L = np.zeros(n, np.float32)
    R = np.zeros(n, np.float32)
    batida = 60 / bpm
    compasso = 4 * batida
    acordes = [(57, 60, 64), (53, 57, 60), (48, 52, 55), (55, 59, 62)]  # Am F C G
    rng = np.random.default_rng(7)
    t_all = np.arange(n) / SR
    k = 0
    while k * compasso < dur:
        ac = acordes[k % 4]
        i0, i1 = int(k * compasso * SR), min(n, int((k + 1) * compasso * SR))
        t = t_all[i0:i1] - k * compasso
        env = np.minimum(1, t / 0.6) * np.minimum(1, (compasso - t) / 0.4)
        pad = sum(np.sin(2 * np.pi * _nota(m) * t + 0.3 * np.sin(2 * np.pi * 0.25 * t)) +
                  0.25 * np.sin(2 * np.pi * 2 * _nota(m) * t) for m in ac)
        pad *= 0.045 * env
        L[i0:i1] += pad
        R[i0:i1] += pad * 0.92
        baixo = 0.09 * np.sin(2 * np.pi * _nota(ac[0] - 12) * t) * env
        L[i0:i1] += baixo
        R[i0:i1] += baixo
        # arpejo em colcheias
        for j in range(8):
            ts = k * compasso + j * batida / 2
            s0 = int(ts * SR)
            m = ac[[0, 1, 2, 1][j % 4]] + 12 + (12 if j == 6 else 0)
            ln = min(int(0.45 * SR), n - s0)
            if ln <= 0:
                continue
            tt = np.arange(ln) / SR
            nota = np.sin(2 * np.pi * _nota(m) * tt) * _env(ln, 0.005, 0.18) * 0.035
            pan = 0.35 if j % 2 else -0.35
            L[s0:s0 + ln] += nota * (1 - pan)
            R[s0:s0 + ln] += nota * (1 + pan)
        # bombo (1 e 3) e chimbal (contratempos)
        for j in range(4):
            s0 = int((k * compasso + j * batida) * SR)
            if j in (0, 2) or bpm >= 110:
                ln = min(int(0.35 * SR), n - s0)
                if ln > 0:
                    tt = np.arange(ln) / SR
                    f = 110 * np.exp(-tt * 18) + 45
                    kick = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 9) * 0.22
                    L[s0:s0 + ln] += kick
                    R[s0:s0 + ln] += kick
            if bpm >= 110 and j in (1, 3):  # palmas
                ln = min(int(0.15 * SR), n - s0)
                if ln > 0:
                    pal = rng.standard_normal(ln) * np.exp(-np.arange(ln) / SR * 28) * 0.07
                    pal = np.diff(np.concatenate([[0], pal]))
                    L[s0:s0 + ln] += pal
                    R[s0:s0 + ln] += pal
            s1 = int((k * compasso + (j + 0.5) * batida) * SR)
            ln = min(int(0.06 * SR), n - s1)
            if ln > 0:
                hat = rng.standard_normal(ln) * np.exp(-np.arange(ln) / SR * 70) * 0.025
                hat = np.diff(np.concatenate([[0], hat]))  # tira graves
                L[s1:s1 + ln] += hat * 0.8
                R[s1:s1 + ln] += hat
        k += 1
    # entrada e saída suaves
    fade = np.minimum(1, np.minimum(t_all / 1.5, (dur - t_all) / 2.0)).clip(0, 1)
    return np.stack([L * fade, R * fade], 1)


# ------------------------------------------------------------------ efeitos

def _passa_baixo(x, corte):
    """Filtro passa-baixo de 1 polo; corte pode ser um valor ou um array (Hz)."""
    corte = np.broadcast_to(np.asarray(corte, np.float64), x.shape)
    a = 1 - np.exp(-2 * np.pi * corte / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc += a[i] * (x[i] - acc)
        y[i] = acc
    return y


def whoosh(dur=0.35):
    n = int(dur * SR)
    t = np.arange(n) / n
    ruido = np.random.default_rng(3).standard_normal(n)
    corte = 300 + 4500 * np.sin(np.pi * t) ** 2
    env = np.sin(np.pi * t) ** 1.5
    return (_passa_baixo(ruido, corte) * env * 0.5).astype(np.float32)


def impacto():
    n = int(0.7 * SR)
    t = np.arange(n) / SR
    f = 38 + 90 * np.exp(-t * 14)
    bum = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 5)
    clique = np.random.default_rng(5).standard_normal(n) * np.exp(-t * 60) * 0.3
    return ((bum + clique) * 0.75).astype(np.float32)


def bancada(dur=2.4):
    """Rugido de estádio: ruído filtrado que sobe depressa e desce devagar."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    r = np.random.default_rng(9).standard_normal(n)
    banda = _passa_baixo(r, 1800) - _passa_baixo(r, 250)
    mod = 1 + 0.25 * np.sin(2 * np.pi * 3.1 * t) * np.sin(2 * np.pi * 0.7 * t)
    env = np.minimum(1, t / 0.12) * np.exp(-np.maximum(0, t - 0.4) / 0.9)
    return (banda * mod * env * 0.9).astype(np.float32)


_EFEITOS = {}


def efeito(nome):
    if nome not in _EFEITOS:
        if nome == "whoosh":
            _EFEITOS[nome] = whoosh()
        elif nome == "golo":
            imp, ban = impacto(), bancada()
            m = np.zeros(max(len(imp), len(ban)), np.float32)
            m[:len(imp)] += imp
            m[:len(ban)] += ban
            _EFEITOS[nome] = m
    return _EFEITOS[nome]


def misturar(dur: float, falas: list[tuple[float, np.ndarray]], vol_musica: float = 0.55, efeitos=(),
             bpm: float = 96) -> np.ndarray:
    """falas = [(início em s, áudio mono)], efeitos = [(início, "whoosh"/"golo")].
    Devolve estéreo int16 com a música a baixar sob a voz."""
    n = int(dur * SR)
    voz = np.zeros(n, np.float32)
    for ini, a in falas:
        s0 = int(ini * SR)
        a = a[: max(0, n - s0)]
        voz[s0:s0 + len(a)] += a
    m = musica(dur, bpm)
    # ducking: envolvente da voz suavizada
    env = np.abs(voz)
    jan = int(0.25 * SR)
    env = np.convolve(env, np.ones(jan) / jan, mode="same")
    duck = 1 - 0.6 * np.clip(env / 0.08, 0, 1)
    fx = np.zeros(n, np.float32)
    for ini, nome in efeitos:
        a = efeito(nome)
        s0 = max(0, int(ini * SR))
        a = a[: max(0, n - s0)]
        fx[s0:s0 + len(a)] += a * (0.35 if nome == "whoosh" else 0.5)
    mix = m * (vol_musica * duck)[:, None] + voz[:, None] * 0.95 + fx[:, None]
    mix /= max(1.0, np.abs(mix).max() / 0.97)
    return (mix * 32767).astype(np.int16)


def guardar_wav(caminho, estereo_int16):
    with wave.open(str(caminho), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(estereo_int16.tobytes())
