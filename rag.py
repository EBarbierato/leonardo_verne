import chromadb

from config import COLLECTION_NAME, MAX_HISTORY_TURNS, RETRIEVAL_K, VECTORDB_DIR
from ollama_client import check_ollama, embed, generate
from prompts import SYSTEM_PROMPT

class LeonardoRAG:
    def __init__(self) -> None:
        check_ollama()
        self.client = chromadb.PersistentClient(path=str(VECTORDB_DIR))
        self.collection = self.client.get_or_create_collection(COLLECTION_NAME)

    def retrieve(self, question: str, k: int = RETRIEVAL_K) -> tuple[str, list[str]]:
        query_embedding = embed(question)
        results = self.collection.query(query_embeddings=[query_embedding], n_results=k)

        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]

        context_parts = []
        sources = []
        for doc, meta in zip(docs, metas):
            source = meta.get("source", "sconosciuto")
            chunk = meta.get("chunk", "?")
            context_parts.append(f"[Fonte: {source}, frammento {chunk}]\n{doc}")
            sources.append(f"{source}#{chunk}")

        return "\n\n".join(context_parts), sorted(set(sources))

    def _history_to_text(self, history: list | None) -> str:
        """Accetta sia history Gradio in formato tuple/list sia formato messages."""
        if not history:
            return ""

        lines = []
        recent = history[-MAX_HISTORY_TURNS:]

        for item in recent:
            if isinstance(item, dict):
                role = item.get("role", "")
                content = item.get("content", "")
                if role == "user" and content:
                    lines.append(f"Bambino: {content}")
                elif role == "assistant" and content:
                    lines.append(f"Leonardo virtuale: {content}")
                continue

            if isinstance(item, (list, tuple)) and len(item) >= 2:
                user_msg = item[0]
                assistant_msg = item[1]
                if user_msg:
                    lines.append(f"Bambino: {user_msg}")
                if assistant_msg:
                    lines.append(f"Leonardo virtuale: {assistant_msg}")

        return "\n".join(lines)

    def answer(self, question: str, history: list | None = None) -> str:
        question = (question or "").strip()
        if not question:
            return "Scrivi una domanda su Leonardo."

        context, sources = self.retrieve(question)
        if not context.strip():
            return "Non ho ancora abbastanza testi nel corpus per rispondere. Aggiungi documenti nella cartella corpus e riesegui ingest.py."

        history_text = self._history_to_text(history)

        prompt = f"""
{SYSTEM_PROMPT}

CONVERSAZIONE RECENTE:
{history_text}

CONTESTO RECUPERATO DAL CORPUS:
{context}

DOMANDA:
{question}

Rispondi in massimo 8 frasi. Se il contesto non basta, dichiaralo esplicitamente.
""".strip()

        answer = generate(prompt)
        if sources:
            answer += "\n\nFonti locali recuperate: " + ", ".join(sources)
        return answer
