import requests
from config import OLLAMA_BASE_URL, CHAT_MODEL, EMBED_MODEL, MAX_OUTPUT_TOKENS

class OllamaError(RuntimeError):
    pass

def check_ollama() -> None:
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=10)
        response.raise_for_status()
    except Exception as exc:
        raise OllamaError(
            "Ollama non sembra attivo. Avvia Ollama e verifica che risponda su http://localhost:11434."
        ) from exc

def embed(text: str) -> list[float]:
    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/embeddings",
        json={"model": EMBED_MODEL, "prompt": text, "keep_alive": "30m"},
        timeout=120,
    )
    response.raise_for_status()
    return response.json()["embedding"]

def generate(prompt: str) -> str:
    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json={
            "model": CHAT_MODEL,
            "prompt": prompt,
            "stream": False,
            "keep_alive": "30m",
            "options": {
                "temperature": 0.25,
                "top_p": 0.85,
                "num_predict": MAX_OUTPUT_TOKENS,
                "num_ctx": 2048,
            },
        },
        timeout=240,
    )
    response.raise_for_status()
    return response.json().get("response", "").strip()
