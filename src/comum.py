"""Funções compartilhadas: árvore, normalização dos votos dos modelos e leitura das rodadas em runs/.

Um "voto" normalizado é um dict com:
  fora (bool), ramo (id de nível 1 ou None), sub (id de nível 2 ou None), c_ramo, c_sub (confianças),
  multi (bool), extras (lista de ids), segunda (id), just (texto).
"""
import importlib
import json
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
arv = importlib.import_module("10_arvore")
RAIZ = Path(__file__).resolve().parents[1]

# Modelos efetivamente usados por cada rodada (apelido do claude -p resolvido em 19/10/2026) e preço de lista.
# US$ por milhão de tokens: (entrada, saída, leitura de cache).
MODELO_REAL = {"claude-opus": "claude-opus-5-5", "claude-sonnet-h": "claude-sonnet-5", "claude-sonnet-3n": "claude-sonnet-5",
               "claude-haiku-h": "claude-haiku-4-5", "claude-haiku-3n": "claude-haiku-4-5", "gpt-5.5": "gpt-5.5",
               "claude-sonnet-plano": "claude-sonnet-5", "claude-opus-h": "claude-opus-5-5", "jev-h": "jev"}
PRECO = {"claude-opus-5-5": (4.0, 20.0, 0.20), "claude-sonnet-5": (2.0, 10.0, 0.20), "claude-haiku-4-5": (1.0, 5.0, 0.10)}
# Caracteres por token medidos neste corpus (runs/calibracao_tokens.json): o tokenizador do Opus/Sonnet 5 gera ~25% mais tokens.
CHARS_POR_TOKEN = {"claude-opus-5-5": 2.36, "claude-sonnet-5": 2.36, "claude-haiku-4-5": 2.97, "gpt-5.5": 3.8}


def norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]+", " ", s)).strip()


def usavel(t):
    return t["nivel"] > 0 and t["status"] == "active" and not t["bucket"]


class Arvore:
    def __init__(self):
        self.t = arv.carregar_temas()
        self.por_titulo = {}
        for x in self.t.values():
            self.por_titulo.setdefault(norm(x["titulo"]), []).append(x)

    def redirecionar(self, tid):
        """Id usável: buckets/inativos vão para o equivalente de mesmo título (ex.: Legislação Especial) ou para o pai."""
        if tid is None or tid not in self.t:
            return None
        x = self.t[tid]
        if usavel(x):
            return tid
        for c in self.por_titulo.get(norm(x["titulo"]), []):
            if usavel(c):
                return c["tema_id"]
        pai = x["parent_id"]
        return pai if pai and self.t[pai]["nivel"] > 0 and usavel(self.t[pai]) else None

    def ramo_de(self, tid):
        if not tid or tid not in self.t:
            return None
        x = self.t[tid]
        return x["parent_id"] if x["nivel"] == 2 else (tid if x["nivel"] == 1 else None)

    def acerto(self, publicado, gabarito):
        """Régua do case: igual, pai ou filho."""
        if not publicado or not gabarito or gabarito == "FORA":
            return False
        if publicado == gabarito:
            return True
        return self.t[publicado]["parent_id"] == gabarito or self.t[gabarito]["parent_id"] == publicado

    def titulo(self, tid):
        return self.t[tid]["titulo"] if tid in self.t else str(tid)

    def rotulo(self, tid):
        """Título legível; quando o mesmo título existe em outra disciplina, acrescenta a disciplina."""
        if tid not in self.t:
            return str(tid)
        x = self.t[tid]
        iguais = [c for c in self.por_titulo.get(norm(x["titulo"]), []) if usavel(c)]
        return f"{x['titulo']} ({x['disciplina']})" if len(iguais) > 1 else x["titulo"]


def normalizar_voto(v, A):
    base = {"multi": bool(v.get("multi_tema", False)), "segunda": v.get("segunda_opcao_id"),
            "extras": v.get("extras_ids", []) or [], "just": v.get("justificativa", "")}
    if v.get("fora"):
        return {"fora": True, "ramo": None, "sub": None, "c_ramo": float(v.get("confianca_ramo", 0) or 0), "c_sub": 0.0, **base}
    ids = [A.redirecionar(v.get("tema_n1_id") or v.get("ramo_n1_id")), A.redirecionar(v.get("subtema_n2_id"))]
    ids = [i for i in ids if i and A.t[i]["nivel"] > 0]
    ramo = sub = None
    if ids:
        no = max(ids, key=lambda i: A.t[i]["nivel"])
        if A.t[no]["nivel"] == 2:
            sub, ramo = no, A.t[no]["parent_id"]
        else:
            ramo = no
    return {"fora": False, "ramo": ramo, "sub": sub, "c_ramo": float(v.get("confianca_ramo", 0) or 0),
            "c_sub": float(v.get("confianca_subtema", 0) or 0) if sub else 0.0, **base}


def carregar_rodada(rotulo, A):
    """{id: (voto_normalizado, bruto)} de runs/<rotulo>/Q*.json"""
    out = {}
    for p in sorted((RAIZ / "runs" / rotulo).glob("Q*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        out[d["id"]] = (normalizar_voto(d, A), d)
    return out


def carregar_questoes():
    return [json.loads(l) for l in (RAIZ / "data" / "questoes_limpas.jsonl").open(encoding="utf-8")]


def carregar_origem():
    p = RAIZ / "data" / "baseline_origem.jsonl"
    return {json.loads(l)["id"]: json.loads(l) for l in p.open(encoding="utf-8")} if p.exists() else {}


# Gêmeos explícitos que o título não revela: plural, erro de grafia ou nome composto.
GEMEOS_EXPLICITOS = {"6735": "5543",   # "Provas em Espécie" -> "Provas em Espécies"
                     "6736": "5560",   # "Recursos (Parte 03) - Espécies" -> "Recursos em Espécies"
                     "6722": "4696"}   # "Estatuto do Idoso - Crimes" -> "Estaturo de Idoso - Crimes"


def gemeos_67xx(A):
    """Temas usáveis de nível 1 que têm um gêmeo "bucket" (ids 67xx, criados por importação, sem descrição nem histórico).

    Devolve {tema_usavel_id: {"gemeos": [ids], "grupo": "copia" | "parte"}}.
    - "copia": o bucket tem o mesmo título do tema usável (cópias da Legislação Especial dentro de Penal/Processo Penal,
      Lei de Execução Penal em Processo Penal, Provas em Espécie, Estatuto do Idoso). Quem rotula à mão vê dois títulos iguais.
    - "parte": o bucket é um nome de aula, "X (Parte N)", cujo X é um tema usável. Menos provável de ser escolhido à mão.
    """
    out = {}

    def liga(usavel_id, bucket, grupo):
        e = out.setdefault(usavel_id, {"gemeos": [], "grupo": grupo})
        e["gemeos"].append(bucket["tema_id"])
        if grupo == "copia":
            e["grupo"] = "copia"

    for t in A.t.values():
        if not (t["bucket"] and t["status"] == "active"):
            continue
        if t["tema_id"] in GEMEOS_EXPLICITOS:
            alvo = GEMEOS_EXPLICITOS[t["tema_id"]]
            liga(alvo, t, "parte" if "(Parte" in t["titulo"] else "copia")
            continue
        m = re.match(r"^(.*?)\s*\(Parte\s*0?\d+\)\s*$", t["titulo"], re.I)
        if m:
            base = norm(m.group(1))
            cands = [c for c in A.por_titulo.get(base, []) if usavel(c) and c["nivel"] == 1]
            mesma = [c for c in cands if c["disciplina"] == t["disciplina"]]
            for c in (mesma or cands)[:1]:
                liga(c["tema_id"], t, "parte")
        else:
            cands = [c for c in A.por_titulo.get(norm(t["titulo"]), []) if usavel(c) and c["nivel"] == 1 and c["tema_id"] != t["tema_id"]]
            for c in cands[:1]:
                liga(c["tema_id"], t, "copia")
    return out
