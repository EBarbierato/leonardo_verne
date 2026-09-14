# LeonardoAI

**LeonardoAI** è un prototipo locale basato su **Retrieval-Augmented
Generation (RAG)** che permette di conversare con un Leonardo da Vinci
virtuale pensato per bambini.

Il sistema viene eseguito interamente sul computer locale e utilizza
**Ollama**, **Llama 3.2 3B**, **nomic-embed-text**, **ChromaDB**,
**Python**, **Gradio**, **PyPDF** e **BeautifulSoup**.

Il modello non viene addestrato direttamente sui documenti di Leonardo:
il corpus viene indicizzato e recuperato dinamicamente quando viene
formulata una domanda.

------------------------------------------------------------------------

# 1. Requisiti

Il prototipo è progettato per **Windows 10/11 a 64 bit**.

Sono necessari:

-   connessione Internet durante l'installazione iniziale;
-   almeno 8 GB di RAM, preferibilmente 16 GB;
-   alcuni GB di spazio libero su disco;
-   PowerShell;
-   Python 3.11 o successivo;
-   Ollama.

Una GPU dedicata non è obbligatoria, ma può ridurre sensibilmente i
tempi di risposta.

# 2. Scaricare ed estrarre il progetto

Scaricare `LeonardoAI.zip` e decomprimerlo in una cartella a propria
scelta, per esempio:

``` text
C:\LeonardoAI
```

oppure:

``` text
E:\ricerca\LeonardoAI
```

La directory del progetto contiene gli script Python, gli script
PowerShell, il file `requirements.txt`, la cartella `corpus` e il
database vettoriale.

# 3. Aprire PowerShell

Aprire PowerShell e spostarsi nella cartella del progetto:

``` powershell
cd "E:\ricerca\LeonardoAI"
```

Verificare la directory:

``` powershell
Get-Location
dir
```

Tra i file deve essere presente `setup.ps1`.

# 4. Abilitare temporaneamente gli script PowerShell

Eseguire:

``` powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

La modifica vale soltanto per la finestra PowerShell corrente.

# 5. Prima installazione

Dalla directory di LeonardoAI eseguire:

``` powershell
.\setup.ps1
```

Lo script prepara l'ambiente necessario al progetto: verifica o installa
Ollama, scarica i modelli, crea l'ambiente virtuale Python, installa le
dipendenze e indicizza il corpus iniziale.

Il primo setup può richiedere diversi minuti perché i modelli devono
essere scaricati.

# 6. Modelli utilizzati

Il modello linguistico è:

``` text
llama3.2:3b
```

È il modello che genera le risposte di Leonardo. Il modello 3B è stato
scelto per contenere la latenza su computer senza hardware AI
particolarmente potente.

Il modello per gli embedding è:

``` text
nomic-embed-text
```

Serve a trasformare documenti e domande in rappresentazioni vettoriali
utilizzate dal sistema RAG.

# 7. Verificare Ollama

Controllare che Ollama funzioni:

``` powershell
ollama --version
```

Controllare i modelli installati:

``` powershell
ollama list
```

Dovrebbero comparire almeno:

``` text
llama3.2:3b
nomic-embed-text
```

Se `ollama` non viene riconosciuto subito dopo l'installazione, chiudere
PowerShell, aprire una nuova finestra e riprovare. Può essere necessario
avviare Ollama almeno una volta dal menu Start di Windows.

# 8. Avviare LeonardoAI

Dopo il setup:

``` powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\run.ps1
```

Il programma avvia il server locale. Dopo alcuni secondi dovrebbe
apparire un indirizzo simile a:

``` text
http://127.0.0.1:7860
```

Aprirlo con Chrome, Edge o Firefox.

# 9. Prima prova

Provare domande come:

``` text
Dove sei nato?
```

``` text
Perché studiavi il volo degli uccelli?
```

``` text
Che cos'è l'Uomo Vitruviano?
```

Il flusso è:

``` text
Domanda
   |
   v
Embedding della domanda
   |
   v
Ricerca in ChromaDB
   |
   v
Frammenti pertinenti del corpus
   |
   v
Llama 3.2
   |
   v
Risposta di Leonardo
```

# 10. Il corpus

La cartella:

``` text
corpus\
```

contiene i documenti utilizzati come base documentale.

Sono supportati file:

``` text
.txt
.md
.pdf
.html
.htm
```

Per esempio:

``` text
corpus\
├── biografia_leonardo.txt
├── codice_volo.pdf
├── appunti_anatomia.txt
└── trattato_pittura.pdf
```

Per risultati storicamente affidabili è essenziale utilizzare fonti
autorevoli e curate.

# 11. Aggiungere nuovi documenti

Copiare i nuovi documenti nella cartella `corpus`.

Poi ricostruire l'indice:

``` powershell
.\reindex.ps1
```

e riavviare:

``` powershell
.\run.ps1
```

# 12. Indicizzazione e RAG

Durante l'indicizzazione:

``` text
Documento
   |
   v
Estrazione del testo
   |
   v
Suddivisione in chunk
   |
   v
nomic-embed-text
   |
   v
Embedding
   |
   v
ChromaDB
```

Quando viene posta una domanda, vengono recuperati soltanto i frammenti
più pertinenti. Questa architettura prende il nome di
**Retrieval-Augmented Generation (RAG)**.

# 13. Il modello non viene addestrato su Leonardo

LeonardoAI non modifica i parametri di Llama 3.2. Il corpus viene
fornito dinamicamente tramite retrieval:

``` text
Llama 3.2
       +
documenti recuperati dal corpus
       +
prompt del personaggio
       =
risposta
```

Questo consente di aggiornare facilmente il corpus, mantenere traccia
delle fonti, evitare un costoso fine-tuning e aggiungere in seguito
altri personaggi con corpus indipendenti.

# 14. Prestazioni

La prima domanda dopo l'avvio può essere più lenta perché Ollama deve
caricare il modello in memoria.

Il prototipo utilizza `llama3.2:3b` invece di un modello 8B per ridurre
la latenza e usa `keep_alive` per mantenere il modello caricato tra
richieste successive.

Le prestazioni dipendono da CPU, RAM e GPU.

# 15. Arrestare LeonardoAI

Nella finestra PowerShell in cui è in esecuzione il server premere:

``` text
CTRL+C
```

# 16. Avvii successivi

`setup.ps1` serve principalmente per la prima installazione. Negli
utilizzi successivi è normalmente sufficiente:

``` powershell
cd "E:\ricerca\LeonardoAI"
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\run.ps1
```

Sostituire il percorso con quello effettivo del proprio computer.

# 17. Dopo una modifica del corpus

Se sono stati aggiunti, eliminati o modificati documenti:

``` powershell
cd "E:\ricerca\LeonardoAI"
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\reindex.ps1
.\run.ps1
```

# 18. Risoluzione dei problemi

## `setup.ps1 cannot be loaded`

Eseguire:

``` powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\setup.ps1
```

## `ollama is not recognized`

Chiudere e riaprire PowerShell, quindi:

``` powershell
ollama --version
```

Se necessario, avviare Ollama dal menu Start. Per localizzare
l'eseguibile:

``` powershell
where.exe ollama
```

## Modelli mancanti

Verificare:

``` powershell
ollama list
```

Se necessario:

``` powershell
ollama pull llama3.2:3b
ollama pull nomic-embed-text
```

## Python non viene riconosciuto

Verificare:

``` powershell
python --version
```

oppure:

``` powershell
py --version
```

È consigliato Python 3.11 o successivo.

## Il virtual environment non esiste

Crearlo:

``` powershell
python -m venv .venv
```

Attivarlo:

``` powershell
.\.venv\Scripts\Activate.ps1
```

## Le risposte sono lente

La prima risposta è normalmente la più lenta. Verificare che il modello
configurato sia `llama3.2:3b` e non `llama3.1:8b`.

## Il browser non si apre automaticamente

Aprire manualmente:

``` text
http://127.0.0.1:7860
```

oppure utilizzare la porta indicata da Gradio.

# 19. Privacy

LeonardoAI è progettato per funzionare localmente:

-   il modello viene eseguito tramite Ollama sul computer locale;
-   ChromaDB risiede localmente;
-   il corpus rimane sul computer;
-   Gradio viene eseguito su `127.0.0.1`.

Il download iniziale dei modelli richiede Internet.

Prima di utilizzare il sistema con minori in un contesto reale è
necessaria una valutazione specifica di privacy, logging, sicurezza,
contenuti e trattamento dei dati.

# 20. Limiti del prototipo

LeonardoAI è un **proof of concept**. Una risposta generata da un LLM
non deve essere considerata automaticamente storicamente corretta.

Il RAG riduce il rischio di allucinazioni, ma non lo elimina.

Per un impiego didattico reale sarà necessario:

-   costruire un corpus storico curato;
-   associare metadati precisi alle fonti;
-   migliorare le citazioni;
-   valutare sistematicamente le risposte;
-   implementare controlli appropriati per l'interazione con bambini;
-   distinguere fatti documentati, interpretazioni e ricostruzioni
    narrative.

# 21. Evoluzione prevista: Leonardo e Jules Verne

L'architettura è pensata per essere estesa a più personaggi:

``` text
                 Domanda del bambino
                         |
              +----------+----------+
              |                     |
              v                     v
       Corpus Leonardo         Corpus Verne
              |                     |
              v                     v
      Agente Leonardo         Agente Verne
              |                     |
              +----------+----------+
                         |
                         v
                 Dialogo con il bambino
```

Leonardo potrà rappresentare osservazione, arte, ingegneria, anatomia,
sperimentazione e scienza rinascimentale.

Jules Verne potrà rappresentare immaginazione scientifica, esplorazione,
tecnologia, narrativa e rapporto tra invenzione e possibilità
scientifica.

Una stessa domanda potrà ricevere due risposte complementari.

Una versione successiva potrà integrare **Text-to-Speech (TTS)**,
assegnando una voce distinta ai due personaggi.

# 22. Architettura software

``` text
                         +----------------+
                         |    Bambino     |
                         +-------+--------+
                                 |
                                 v
                         +----------------+
                         |     Gradio     |
                         +-------+--------+
                                 |
                                 v
                         +----------------+
                         |   Python/RAG   |
                         +-------+--------+
                                 |
                   +-------------+-------------+
                   |                           |
                   v                           v
          +----------------+          +----------------+
          |   ChromaDB     |          |     Ollama     |
          | Vector Store   |          |                |
          +-------+--------+          +-------+--------+
                  |                           |
                  v                           v
          +----------------+          +----------------+
          | nomic-embed-   |          | Llama 3.2 3B  |
          | text           |          |                |
          +----------------+          +----------------+
                  ^
                  |
          +----------------+
          | Corpus storico |
          +----------------+
```

# 23. Stato del progetto

Versione corrente:

``` text
LeonardoAI 0.2
```

La versione 0.2:

-   utilizza `llama3.2:3b`;
-   utilizza `nomic-embed-text`;
-   utilizza ChromaDB per il retrieval;
-   mantiene il modello attivo mediante `keep_alive`;
-   limita il numero di chunk recuperati per ridurre la latenza;
-   corregge la gestione della cronologia nelle versioni recenti di
    Gradio.

Il progetto è destinato alla **prototipazione e sperimentazione**, non
all'impiego in produzione.
