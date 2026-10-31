"""Modo nuvem: descarrega os dados (base de dados, recaps, lições, fichas) do ramo de dados no GitHub.

Quem escreve os dados é o GitHub Actions (resultados e previsões) e as rotinas do agente na nuvem; a dashboard
só lê. Assim funciona com o PC desligado.
"""
import io
import os
import shutil
import tarfile
import tempfile
from pathlib import Path

import requests

from agente import config

API = "https://api.github.com/repos/{repo}"
SHA_FILE = config.DATA_DIR / ".sha"


def ativo() -> bool:
    return bool(config.AGENTE_REPO)


def _headers() -> dict:
    h = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    if config.GH_TOKEN:
        h["Authorization"] = f"Bearer {config.GH_TOKEN}"
    return h


def versao_remota() -> str:
    r = requests.get(f"{API.format(repo=config.AGENTE_REPO)}/commits/{config.DADOS_BRANCH}",
                     headers=_headers(), timeout=20)
    r.raise_for_status()
    return r.json()["sha"]


def sincronizar() -> bool:
    """Descarrega o ramo de dados se mudou desde a última vez. Devolve True se houve dados novos."""
    if not ativo():
        return False
    sha = versao_remota()
    if SHA_FILE.exists() and SHA_FILE.read_text().strip() == sha:
        return False
    r = requests.get(f"{API.format(repo=config.AGENTE_REPO)}/tarball/{sha}", headers=_headers(), timeout=120)
    r.raise_for_status()
    with tempfile.TemporaryDirectory() as tmp:
        with tarfile.open(fileobj=io.BytesIO(r.content), mode="r:gz") as tar:
            tar.extractall(tmp, filter="data")
        top = next(Path(tmp).iterdir())  # <dono>-<repo>-<sha>/
        for src in top.rglob("*"):
            if src.is_dir() or src.name == ".gitignore":
                continue
            dst = config.DATA_DIR / src.relative_to(top)
            dst.parent.mkdir(parents=True, exist_ok=True)
            part = dst.with_name(dst.name + ".part")
            shutil.copyfile(src, part)
            os.replace(part, dst)  # troca atómica: quem está a ler nunca vê um ficheiro a meio
    SHA_FILE.write_text(sha)
    return True
