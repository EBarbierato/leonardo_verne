# LeonardoAI

Prototipo locale RAG per un **Leonardo da Vinci virtuale per bambini**.

## Avvio rapido

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\setup.ps1
.\run.ps1
```

Poi apri l'URL mostrato da Gradio, di solito:

```text
http://127.0.0.1:7860
```

## Aggiornamento 0.2

Questa versione corregge l'errore Gradio:

```text
ValueError: too many values to unpack (expected 2)
```

e riduce la latenza usando:

- modello chat `llama3.2:3b` invece di `llama3.1:8b`;
- `RETRIEVAL_K = 3`;
- limite di output più breve;
- `keep_alive` per tenere i modelli caricati in Ollama.

## Aggiungere corpus

Metti file `.txt`, `.md`, `.pdf`, `.html` in:

```text
corpus/
```

Poi riesegui:

```powershell
.\reindex.ps1
.\run.ps1
```

## Nota prestazionale

La prima domanda può essere lenta perché Ollama carica il modello in memoria. Le domande successive dovrebbero essere più rapide. Su macchine senza GPU dedicata, un modello 8B può facilmente impiegare 10-20 secondi; per demo live conviene usare 3B.
