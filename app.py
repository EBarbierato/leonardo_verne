import gradio as gr

from rag import LeonardoRAG

rag = LeonardoRAG()

def ask_leonardo(message, history):
    return rag.answer(message, history)

demo = gr.ChatInterface(
    fn=ask_leonardo,
    title="Leonardo da Vinci virtuale per bambini",
    description=(
        "Prototipo locale RAG. Inserisci testi, PDF o HTML nella cartella corpus, "
        "riesegui ingest.py, poi fai domande a Leonardo virtuale."
    ),
    examples=[
        "Leonardo era piu' pittore o inventore?",
        "Perche' Leonardo studiava il volo degli uccelli?",
        "Cos'e' l'Uomo Vitruviano spiegato a un bambino?",
        "Leonardo ha davvero inventato l'elicottero?",
    ],
)

if __name__ == "__main__":
    demo.launch()
