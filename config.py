from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CORPUS_DIR = BASE_DIR / "corpus"
VECTORDB_DIR = BASE_DIR / "vectordb"
COLLECTION_NAME = "leonardo_corpus"

OLLAMA_BASE_URL = "http://localhost:11434"

# Modello più leggero del precedente llama3.1:8b: molto più adatto a demo live.
# Se vuoi più qualità e accetti più lentezza, rimetti: "llama3.1:8b"
CHAT_MODEL = "llama3.2:3b"
EMBED_MODEL = "nomic-embed-text"

CHUNK_SIZE = 900
CHUNK_OVERLAP = 120
RETRIEVAL_K = 3
MAX_HISTORY_TURNS = 2
MAX_OUTPUT_TOKENS = 160
