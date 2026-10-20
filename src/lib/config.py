"""Carrega chaves de API de keys.txt (ignorado pelo git) ou das variáveis de ambiente."""
import os
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]

def carregar_chaves() -> dict:
    chaves = {}
    arq = RAIZ / "keys.txt"
    if arq.exists():
        for linha in arq.read_text(encoding="utf-8").splitlines():
            if "=" in linha:
                k, v = linha.split("=", 1)
                chaves[k.strip().lower()] = v.strip()
    os.environ.setdefault("OPENAI_API_KEY", chaves.get("openai", os.environ.get("OPENAI_API_KEY", "")))
    os.environ.setdefault("ANTHROPIC_API_KEY", chaves.get("claude", os.environ.get("ANTHROPIC_API_KEY", "")))
    return chaves
