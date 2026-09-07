import glob
import hashlib
import os
from pathlib import Path

import chromadb
from bs4 import BeautifulSoup
from pypdf import PdfReader

from config import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    COLLECTION_NAME,
    CORPUS_DIR,
    VECTORDB_DIR,
)
from ollama_client import check_ollama, embed

SUPPORTED_EXTENSIONS = [".txt", ".md", ".pdf", ".html", ".htm"]

def read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")

def read_pdf(path: Path) -> str:
    reader = PdfReader(str(path))
    pages = []
    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if text.strip():
            pages.append(f"[Pagina {page_number}]\n{text}")
    return "\n".join(pages)

def read_html(path: Path) -> str:
    soup = BeautifulSoup(path.read_text(encoding="utf-8", errors="ignore"), "lxml")
    return soup.get_text("\n")

def read_document(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in [".txt", ".md"]:
        return read_text_file(path)
    if ext == ".pdf":
        return read_pdf(path)
    if ext in [".html", ".htm"]:
        return read_html(path)
    return ""

def normalize(text: str) -> str:
    return " ".join(text.split())

def chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    text = normalize(text)
    chunks = []
    start = 0
    while start < len(text):
        chunk = text[start:start + size]
        if chunk.strip():
            chunks.append(chunk)
        start += size - overlap
    return chunks

def list_corpus_files() -> list[Path]:
    files = []
    for ext in SUPPORTED_EXTENSIONS:
        files.extend(Path(p) for p in glob.glob(str(CORPUS_DIR / f"**/*{ext}"), recursive=True))
    return sorted(files)

def main() -> None:
    check_ollama()
    CORPUS_DIR.mkdir(exist_ok=True)
    VECTORDB_DIR.mkdir(exist_ok=True)

    files = list_corpus_files()
    if not files:
        raise RuntimeError(f"Nessun file supportato trovato in {CORPUS_DIR}")

    client = chromadb.PersistentClient(path=str(VECTORDB_DIR))
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    collection = client.get_or_create_collection(COLLECTION_NAME)

    ids, documents, embeddings, metadatas = [], [], [], []

    for path in files:
        print(f"Leggo: {path.name}")
        text = read_document(path)
        chunks = chunk_text(text)
        for chunk_index, chunk in enumerate(chunks):
            stable_id = hashlib.sha256(f"{path}-{chunk_index}-{chunk}".encode("utf-8")).hexdigest()
            ids.append(stable_id)
            documents.append(chunk)
            embeddings.append(embed(chunk))
            metadatas.append({
                "source": path.name,
                "relative_path": str(path.relative_to(CORPUS_DIR)),
                "chunk": chunk_index,
            })

    if not ids:
        raise RuntimeError("I file nel corpus non contengono testo estraibile.")

    collection.add(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas)
    print(f"Indicizzazione completata: {len(documents)} frammenti da {len(files)} file.")

if __name__ == "__main__":
    main()
