"""Camada única de chamada a modelos com saída JSON validada por esquema.

Provedores:
- "anthropic": API da Anthropic (SDK oficial), com cache do system prompt.
- "openai":    API Responses da OpenAI, com saída estruturada estrita.
- "claude_cli": Claude Code em modo headless (`claude -p`), usando uma assinatura Max.
               Cada chamada carrega o contexto do próprio Claude Code; o custo informado vem
               do campo total_cost_usd (preço de lista), mas não é cobrado na assinatura.

Uso: dados, uso = chamar_json(provedor, modelo, sistema, pedido, esquema, effort)
     uso = {"in", "out", "cache_w", "cache_r", "custo_usd"}
"""
import json, shutil, subprocess, tempfile, os
from pathlib import Path

from config import carregar_chaves
carregar_chaves()

# US$ por milhão de tokens: entrada, saída, leitura de cache. Fonte: tabela de preços de 06/2026 (Anthropic);
# OpenAI: preencher em runs/precos.json se quiser custo em dólares (os tokens ficam registrados de qualquer forma).
PRECOS = {
    "claude-opus-5": (5.0, 25.0, 0.5), "claude-opus-5-5": (4.0, 20.0, 0.2), "claude-sonnet-5": (2.0, 10.0, 0.2),
    "claude-haiku-4-5": (1.0, 5.0, 0.1),
}
_precos_extra = Path(__file__).resolve().parents[2] / "runs" / "precos.json"
if _precos_extra.exists():
    PRECOS.update({k: tuple(v) for k, v in json.loads(_precos_extra.read_text(encoding="utf-8")).items()})

def custo(modelo, uso):
    p = PRECOS.get(modelo)
    if not p:
        return None
    return round((uso["in"] * p[0] + uso["out"] * p[1] + uso["cache_r"] * p[2] + uso["cache_w"] * p[0] * 1.25) / 1e6, 5)

def _anthropic(modelo, sistema, pedido, esquema, effort, max_tokens):
    import anthropic
    client = anthropic.Anthropic()
    r = client.messages.create(
        model=modelo, max_tokens=max_tokens,
        system=[{"type": "text", "text": sistema, "cache_control": {"type": "ephemeral"}}],
        output_config={"effort": effort, "format": {"type": "json_schema", "schema": esquema}},
        messages=[{"role": "user", "content": pedido}],
    )
    texto = next(b.text for b in r.content if b.type == "text")
    u = r.usage
    uso = {"in": u.input_tokens, "out": u.output_tokens,
           "cache_w": u.cache_creation_input_tokens or 0, "cache_r": u.cache_read_input_tokens or 0}
    uso["custo_usd"] = custo(modelo, uso)
    return json.loads(texto), uso

def _openai(modelo, sistema, pedido, esquema, effort, max_tokens):
    import openai
    client = openai.OpenAI()
    r = client.responses.create(
        model=modelo, reasoning={"effort": effort},
        input=[{"role": "system", "content": sistema}, {"role": "user", "content": pedido}],
        text={"format": {"type": "json_schema", "name": "resposta", "schema": esquema, "strict": True}},
    )
    u = r.usage
    cached = getattr(getattr(u, "input_tokens_details", None), "cached_tokens", 0) or 0
    uso = {"in": u.input_tokens - cached, "out": u.output_tokens, "cache_w": 0, "cache_r": cached}
    uso["custo_usd"] = custo(modelo, uso)
    return json.loads(r.output_text), uso

def _claude_cli(modelo, sistema, pedido, esquema, effort, max_tokens):
    exe = shutil.which("claude")
    if not exe:
        raise RuntimeError("claude CLI não encontrado no PATH")
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(sistema)
        caminho = f.name
    try:
        cmd = [exe, "-p", "--model", modelo, "--system-prompt-file", caminho, "--json-schema", json.dumps(esquema),
               "--output-format", "json", "--no-session-persistence", "--max-turns", "1", "--tools", ""]
        if effort:
            cmd += ["--effort", effort]
        env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}  # força a assinatura, não a chave
        out = subprocess.run(cmd, input=pedido, capture_output=True, text=True, encoding="utf-8", timeout=900, env=env)
        if out.returncode != 0:
            raise RuntimeError(f"claude -p falhou ({out.returncode}): {out.stderr[:500]} {out.stdout[:500]}")
        j = json.loads(out.stdout)
    finally:
        Path(caminho).unlink(missing_ok=True)
    dados = j.get("structured_output")
    if dados is None:
        dados = json.loads(j["result"])
    u = j.get("usage", {})
    uso = {"in": u.get("input_tokens", 0), "out": u.get("output_tokens", 0),
           "cache_w": u.get("cache_creation_input_tokens", 0), "cache_r": u.get("cache_read_input_tokens", 0),
           "custo_usd": j.get("total_cost_usd")}
    return dados, uso

def chamar_json(provedor, modelo, sistema, pedido, esquema, effort="medium", max_tokens=4000, tentativas=3):
    """Chama o provedor com até `tentativas` repetições em caso de erro transitório (backoff simples)."""
    import time
    fn = {"anthropic": _anthropic, "openai": _openai, "claude_cli": _claude_cli}[provedor]
    ultimo = None
    for i in range(tentativas):
        try:
            return fn(modelo, sistema, pedido, esquema, effort, max_tokens)
        except Exception as e:  # noqa: BLE001 - registramos e tentamos de novo
            ultimo = e
            time.sleep(5 * (i + 1))
    raise ultimo
