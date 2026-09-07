$ErrorActionPreference = "Stop"

Write-Host "== LeonardoAI setup =="

if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
    Write-Host "Installo Ollama con winget..."
    winget install --id Ollama.Ollama -e
} else {
    Write-Host "Ollama gia' presente."
}

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python non trovato. Installa Python 3.11+ e riesegui setup.ps1."
    exit 1
}

Write-Host "Scarico modelli Ollama..."
ollama pull llama3.2:3b
ollama pull nomic-embed-text

if (-not (Test-Path ".\.venv")) {
    python -m venv .venv
}

. .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt

Write-Host "Indicizzo il corpus demo..."
python .\ingest.py

Write-Host "Setup completato. Ora esegui: .\run.ps1"
