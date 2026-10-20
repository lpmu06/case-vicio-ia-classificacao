"""Registra as pastas de etapas no sys.path, para que os scripts se importem pelo nome (ex.: import_module("30_classificar")).

Uso no topo de cada script:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
    import caminhos  # noqa: F401
"""
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[1]
RAIZ = SRC.parent
for pasta in ("lib", "preparo", "classificar", "analise", "entrega"):
    p = str(SRC / pasta)
    if p not in sys.path:
        sys.path.insert(0, p)
