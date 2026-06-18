# TASK BOARD

## Regole

- Ogni task deve avere uno sviluppatore owner.
- Ogni task deve dichiarare stream, branch e file ownership prima di iniziare.
- `ROADMAP.md` resta la visione degli obiettivi funzionali.
- Questo file gestisce il lavoro operativo asincrono tra sviluppatori e assistenti.
- Spostare un task in `Done` solo dopo test/verifica e handoff.

## Backlog

### Gestione Thread Email

Owner proposto: da assegnare
Stream: Preprocessing
Branch proposta: `feature/email-thread-detection`

Scopo:
Alcune email sono risposte o forward di conversazioni precedenti. Il corpo può contenere messaggi concatenati separati da header del tipo `-----Original Message-----`. Senza gestione, il `combined_text` ingloba tutto il thread come se fosse un unico documento, introducendo contenuto ridondante e fuorviante per embeddings e clustering.

Dipendenze:
- boilerplate detection completato (merged);
- `DATA_CONTRACTS.md` aggiornato prima di modificare `content_clean`.

File scrivibili:
- `src/utils/data_processing.py`
- `src/utils/constants/preprocessing.py`
- `DATA_CONTRACTS.md`
- `docs/knowledge/03_cleaning_feature_engineering.md`
- `tests/test_data_processing.py`

Output attesi:
- funzione `split_thread_body(text) -> tuple[str, str | None]` che isola il body del messaggio corrente dal thread citato;
- nuova colonna `has_thread` (bool): `True` se è stato rilevato almeno un forward/reply header nel corpo;
- `content_clean` aggiornato a contenere solo il corpo del messaggio corrente;
- documentazione e test unitari;
- valutazione dell'impatto su clustering vs baseline.

Rischi:
- alcune email hanno come contenuto principale proprio il messaggio inoltrato; uno strip aggressivo del thread eliminerebbe il contenuto reale;
- le catene di risposta sono strutturalmente eterogenee: il forward header non è standardizzato;
- approccio consigliato: safe by default, come per il disclaimer.

---

### Arricchimento Contestuale via LLM

Owner proposto: da assegnare
Stream: Feature Engineering / NLP
Branch proposta: `feature/llm-contextual-enrichment`

Scopo:
Alcune email assumono un contesto implicito (riferimenti a eventi, persone o accordi non menzionati esplicitamente). Questo riduce la qualità semantica degli embeddings e produce cluster poco interpretabili. L'obiettivo è usare un LLM locale (Ollama) per aggiungere una colonna di contesto sintetico che arricchisca il testo prima dell'embedding.

Dipendenze:
- pipeline di processing stabile (merged);
- Ollama disponibile in locale con un modello adatto (es. `llama3`);
- `DATA_CONTRACTS.md` aggiornato prima di aggiungere nuove colonne al processed.

File scrivibili:
- `src/utils/data_processing.py` o nuovo modulo `src/utils/contextual_enrichment.py`
- `DATA_CONTRACTS.md`
- `docs/knowledge/` (nuovo documento dedicato)
- `tests/`

Output attesi:
- funzione `enrich_with_context(text, model) -> str` che genera una breve stringa di contesto (es. 1-2 frasi) a partire dal testo dell'email;
- nuova colonna `context_summary` (string, nullable): contesto sintetico generato dall'LLM;
- valutazione dell'impatto: confronto embeddings con e senza `context_summary` concatenato a `combined_text`;
- stima del costo computazionale (latenza per row, batch size ottimale).

Rischi:
- latenza LLM: con 355 email nel sample il costo è gestibile; su dataset full (~40k+) richiede batching e caching;
- allucinazioni LLM: il contesto generato potrebbe introdurre bias semantico; validazione qualitativa obbligatoria prima del merge;
- dipendenza da Ollama locale: la pipeline non è riproducibile su macchine senza Ollama; valutare flag `--skip-enrichment` per ambienti senza GPU.

### Valutare colonne ausiliarie per feature statistiche

Owner proposto: da assegnare
Stream: feature engineering/documentazione
Branch proposta: `feature/text-stat-features`

Dipendenze:

- decisione approvata su `combined_text` embeddings;
- contratto processed aggiornato se vengono aggiunte colonne.

File scrivibili:

- `DATA_CONTRACTS.md`
- `docs/knowledge/03_cleaning_feature_engineering.md`
- eventuale modulo feature, solo dopo approvazione.

Output:

- proposta per colonne testuali ausiliarie, ad esempio testo per statistiche o keyword extraction;
- pro/contro rispetto a modificare `combined_text`;
- test previsti;
- impatto su embeddings e clustering.

### Valutare boilerplate, firme e forward headers

Owner proposto: da assegnare
Stream: feature engineering/documentazione
Branch proposta: `feature/email-boilerplate-analysis`

Dipendenze:

- sample processed disponibile;
- policy preprocessing conservativa approvata.

File scrivibili:

- `docs/knowledge/03_cleaning_feature_engineering.md`
- eventuali notebook diagnostici o report, previa approvazione.

Output:

- analisi su frequenza e impatto di boilerplate, firme e forward headers;
- regole candidate di tagging o rimozione;
- rischi informativi;
- raccomandazione prima di eventuali modifiche runtime.

### Implementazione Entity Normalization

Owner proposto: da assegnare
Stream: feature engineering / NLP
Branch proposta: `feature/entity-normalization`

Scopo:
Sviluppare una utility per normalizzare i nomi di persone e organizzazioni (es. "Barack Obama" vs "President Obama") per migliorare la densità semantica del clustering e del labeling.

Output:
- Modulo di Entity Resolution.
- Lookup table o logica basata su NER.

### Implementazione Pulizia Boilerplate e POS Filtering

Owner proposto: da assegnare
Stream: Preprocessing
Branch proposta: `feature/advanced-cleaning`

Scopo:
Rimuovere il rumore dalle email (header, firme) e implementare filtri grammaticali (solo Sostantivi) per l'estrazione delle keyword, migliorando l'interpretabilità dei cluster.

Output:
- Funzioni di pulizia regex.
- Pipeline di filtraggio POS via Spacy.

### Ricongiungere embeddings e feature engineering

Owner: da assegnare dopo merge stream A e B
Stream: integrazione
Branch proposta: `integration/embeddings-features`

Dipendenze:

- stream embeddings baseline completato;
- stream feature engineering completato;
- `DATA_CONTRACTS.md` aggiornato.

Output:

- embeddings rigenerati sul dataset arricchito;
- confronto baseline vs arricchito;
- decisione sul dataset da usare per clustering.

## Ready

### Ottimizzazione Iperparametri UMAP e HDBSCAN (Dataset 1.75M)

Owner proposto: Filippo (Antigravity) / Utente
Stream: clustering
Branch proposta: `feature/clustering-optimization`
Stato: Ready

Scopo:
Rivisitare le configurazioni di UMAP e HDBSCAN alla luce della rigenerazione completa degli embedding su 1.75 milioni di email. Gli errori di configurazione precedenti (es. `n_neighbors` troppo basso, `min_cluster_size` non proporzionato) andranno corretti per evitare che il rumore si mescoli ai macro-cluster. Eseguire eventualmente su un campione se UMAP impiega troppo tempo.

Dipendenze:
- Run di `embedding_pipeline.py` completato con successo (file `email_embeddings.npy` disponibile).
- Validazione geometrica eseguita tramite `final_embeddings_validation.ipynb`.

File scrivibili:
- `src/utils/clustering_hdbscan.py`
- `src/notebooks/clustering_umap_hdbscan.ipynb`
- `DECISIONS.md`

Output:
- Nuovi iperparametri validati per scalare sui 1.75M di vettori `bge-small` ottimizzati.
- Parametri candidati UMAP: `n_neighbors=30/50`, `min_dist=0.0`.
- Parametri candidati HDBSCAN: `min_cluster_size` proporzionale al dataset (es. valutare min_cluster_size molto più alti visto il volume).

## In Progress

### Sperimentazione e Implementazione Topic Labeling

Owner: Gemini (AI Agent)
Stream: Topic Modeling
Branch: `feature/topic-labeling`
Stato: In Progress

Scopo:
Interpretazione semantica dei cluster tramite Topic Labeling, confrontando diversi approcci (YAKE, TextRank, c-TF-IDF, KeyBERT, LLM) per estrarre keyword e nomi di cluster significativi.

File scrivibili:
- `src/utils/topic_labeling.py`
- `src/notebooks/cluster_labeling_experiment.ipynb`
- `DECISIONS.md`
- `docs/knowledge/08_topic_labeling.md`

Output attesi:
- Utility script con algoritmi di keyword extraction.
- Notebook di confronto qualitativo.
- Documentazione tecnica e decisione finale.

## Blocked

Nessun task bloccato.

## Done

### Ottimizzazione Token-Aware Chunking e Decay Pooling

Owner: Filippo (Antigravity)
Stream: embeddings
Branch: `feature/embedding-optimizations`
Stato: Done

Scopo:
Migliorare la qualità semantica e la densità geometrica degli embedding per evitare falsi raggruppamenti causati da firme o boilerplate, e scalare la pipeline per gestire senza crash enormi dataset.

Handoff:
Owner: Filippo (Antigravity)
Stream: embeddings
Branch: `feature/embedding-optimizations`
Task: Ottimizzazione Token-Aware Chunking e Decay Pooling
File modificati:
- `src/utils/embedding_pipeline.py`
- `.env`
- `DECISIONS.md`
- `docs/knowledge/07_embedding_pipeline_optimizations.md`
- `src/notebooks/final_embeddings_validation.ipynb` (creato)
Test:
- Eseguito sweep K-Means su campione 3.1k: registrato un incremento del Silhouette Score del +38% e una "perdita" calcolata di falsa stabilità (-0.1 ARI).
- Generato nuovo notebook `final_embeddings_validation.ipynb`.
- Risolto bug OOM su batch colossali (1 Miliardo di caratteri) con tecnica di *Slicing Sequenziale*.
Output:
- Pipeline robusta e attiva in background su 1.75 milioni di record.
Rischi:
- Esecuzione massiva completata (14 ore).
Prossimo passo:
- Passare a `Ottimizzazione Iperparametri UMAP e HDBSCAN (Dataset 1.75M)`.

### Esportazione Dataset Etichettato (Clustered Emails)

Owner: Gemini (AI Agent)
Stream: Integrazione
Branch: `feature/labeled-dataset-export`
Stato: Done

Scopo:
Garantire che la pipeline di orchestrazione produca un file Parquet finale con tutti i dati etichettati (cluster ID, probabilità e nomi descrittivi LLM).

Handoff:
Owner: Gemini (AI Agent)
Stream: Integrazione
Branch: `feature/labeled-dataset-export`
Task: Esportazione Dataset Etichettato (Clustered Emails)
File modificati:
- `src/notebooks/full_pipeline_orchestration.ipynb`
- `DATA_CONTRACTS.md`
- `DECISIONS.md`
Test:
- Validata logica di mappatura via script Python.
- Verifica coerenza con DATA_CONTRACTS.md.
Output:
- Notebook aggiornato con export in `data/processed/jmail_emails_clustered.parquet`.
Rischi:
- I nomi dei cluster potrebbero essere "Outlier" se l'LLM naming viene limitato a un subset (come nel notebook corrente).

### Creazione Notebook Orchestratore Pipeline Completa

Owner: Filippo (Antigravity)
Stream: Integrazione
Branch: `feature/full-pipeline-notebook`
Stato: Done

Scopo:
Creare un notebook centralizzato (`full_pipeline_orchestration.ipynb`) che orchestri l'intera pipeline di lavoro, dall'estrazione del dataset fino al preprocessing, embeddings, clustering UMAP+HDBSCAN e assegnazione dei nomi tramite LLM, riutilizzando esclusivamente i moduli validati presenti in `src/utils/`.

Handoff:
Owner: Filippo (Antigravity)
Stream: Integrazione
Branch: `feature/full-pipeline-notebook`
Task: Creazione Notebook Orchestratore Pipeline Completa
File creati/modificati:
- `src/notebooks/full_pipeline_orchestration.ipynb`
- `TASK_BOARD.md`
Test:
- Validato sintatticamente l'IPYNB generato tramite esecuzione di Python nbformat.
Output:
- Nuovo notebook `full_pipeline_orchestration.ipynb` disponibile.
Rischi:
- Nessuno, il notebook prevede la possibilità di lavorare su limit_rows per il preprocessing per evitare sovraccarichi hardware.

### LLM-Naming per riassumere i cluster

Owner: Filippo (Antigravity)
Stream: Labelling Topic
Branch: `feature/llm-naming`
Stato: Done

Scopo:
Sviluppare un'utility per l'assegnazione automatica di un nome (1-3 parole massime) ai cluster partendo dalle keyword estratte, interfacciandosi con un modello LLM locale tramite Ollama.

Handoff:
Owner: Filippo (Antigravity)
Stream: Labelling Topic
Branch: `feature/llm-naming`
Task: LLM-Naming per riassumere i cluster
File modificati:
- `src/utils/llm_naming.py`
- `TASK_BOARD.md`
Test:
- Esecuzione `uv run python src/utils/llm_naming.py` andata a buon fine.
- Risolto blocco di Ollama (generation loop) causato dall'uso dell'endpoint `/api/generate` passando a `/api/chat` e implementando un **Few-Shot Prompt** con temperatura 0.0 per garantire risposte formattate esattamente come richiesto.
Output:
- Modulo `get_llm_cluster_name` funzionante e validato in locale con modello `llama3`.
Rischi:
- La latenza dell'LLM può rallentare l'elaborazione per i 40 cluster, ma l'impostazione Few-Shot minimizza i tempi di inferenza.
Prossimo passo:
- Eseguire il processo massivamente nel notebook `cluster_labeling_experiment.ipynb` su tutti i cluster individuati.

### Sperimentante clustering UMAP + HDBSCAN e Grid Search

Owner: Filippo (Antigravity)
Stream: clustering
Branch: `feature/clustering-hdbscan`
Stato: Done

Scopo:
Risolvere il blocco computazionale dell'approccio diretto sviluppando una pipeline UMAP (15D, cosine) + HDBSCAN (euclidean) e trovare i parametri ottimali tramite Grid Search.

Handoff:
Owner: Filippo (Antigravity)
Stream: clustering
Branch: `feature/clustering-hdbscan`
Task: Sperimentare clustering UMAP + HDBSCAN e Grid Search
File modificati:
- `src/utils/clustering_hdbscan.py`
- `src/notebooks/clustering_umap_hdbscan.ipynb`
- `src/notebooks/clustering_hdbscan_experiment.ipynb`
- `DECISIONS.md`
- `TASK_BOARD.md`
Test:
- Esecuzione notebook pipeline completata con successo in pochi secondi.
- Grid Search completata.
Output:
- Utility per pipeline UMAP + HDBSCAN creata.
- Notebook di grid search configurato.
- Parametri finali scelti (Configurazione 9): `min_cluster_size=200`, `min_samples=10`.
Rischi:
- Nessuno, la pipeline ridotta è performante.
Prossimo passo:
- Analisi qualitativa ed estrazione semantica dei cluster individuati.

### Consolidare embeddings baseline

Owner: José (Codex)
Stream: embeddings/studio/analisi
Branch: `feature/embeddings-baseline`
Stato: Done

Scopo:
Generare embeddings per tre modelli diversi (`bge-small-en-v1.5`, `all-MiniLM-L6-v2`, `e5-base-v2`) e validare il processo tramite notebook diagnostico.

Handoff:
Owner: José (Codex)
Stream: embeddings/studio/analisi
Branch: `feature/embeddings-baseline`
Task: Consolidare embeddings baseline
File modificati:
- `src/notebooks/embedding_process.ipynb`
Test:
- Esecuzione notebook (verifica visiva dei grafici diagnostici).
- Verifica artefatti in `data/embeddings/` e `data/metadata/`.
Output:
- Artefatti embedding per i 3 modelli generati e salvati.
- Notebook diagnostico corretto per gestire norme L2 costanti (1.0).
Rischi:
- Nessuno rilevato; la normalizzazione è garantita dalla pipeline.
Prossimo passo:
- Avviare analisi comparativa embeddings o procedere al clustering.

### Validare recipient_count_estimate

Owner: José (Codex)
Stream: feature engineering/documentazione
Branch proposta: `fix/recipient-count-estimate`
Stato: Done

Scopo:

Verificare se `recipient_count_estimate` e' nullable per limiti reali dei dati raw o per un problema nella logica di parsing dei destinatari.

Dipendenze:

- contratto processed aggiornato;
- sample processed disponibile.

File scrivibili:

- `src/utils/data_processing.py`
- `tests/test_data_processing.py`
- `DATA_CONTRACTS.md`
- `src/notebooks/data_preprocessing_validation.ipynb`
- `Diary.md`
- `TODO.md`
- `TASK_BOARD.md`

File da leggere:

- `data/processed/jmail_emails_processed_sample.parquet`
- `data/raw/jmail_emails_sample.parquet`
- `data/metadata/jmail_processing_sample_metadata.json`

Piano:

- confrontare colonne recipient raw e processed sul sample;
- individuare formati concreti di `to_recipients`, `cc_recipients`, `bcc_recipients`;
- leggere la funzione che produce `recipient_count_estimate`;
- decidere se correggere il parsing o mantenere il campo nullable;
- aggiungere test mirati se cambia logica runtime;
- aggiornare `DATA_CONTRACTS.md` se cambia la garanzia del campo.

Notebook diagnostico:

- accorpato in `src/notebooks/data_preprocessing_validation.ipynb`;
- sezione dedicata: `Diagnostica recipient_count_estimate`;
- output generati in `reports/figures/data_preprocessing_validation/`, ignorati da Git.

Output attesi:

- diagnosi del motivo per cui `recipient_count_estimate` e' nullo in molte righe del sample;
- correzione o decisione documentata se il campo deve restare nullable;
- test unitario sui formati recipient raw supportati, se necessario;
- contratto processed aggiornato se cambia la garanzia del campo.

Handoff:
Owner: José (Codex)
Stream: feature engineering/documentazione
Branch: `fix/recipient-count-estimate` proposta, lavoro attuale su branch locale corrente
PR: da aprire
Task: Validare recipient_count_estimate
File modificati:
- `src/utils/data_processing.py`
- `tests/test_data_processing.py`
- `DATA_CONTRACTS.md`
- `DECISIONS.md`
- `docs/knowledge/03_cleaning_feature_engineering.md`
- `src/notebooks/data_preprocessing_validation.ipynb`
- `TASK_BOARD.md`
- `Diary.md`
- `TODO.md`
Test:
- `uv run python -m pytest tests/test_data_processing.py -q` (`13 passed`)
- `uv run python -m pytest -q` (`21 passed`)
Output: Corretto `recipient_count_estimate` eliminando null artificiali da disallineamento indice, aggiunto `person_unknown`, gestito `Unknown` per righe senza recipient utilizzabili e rilevato `[redacted]`.
Rischi: `recipient_count_estimate` resta una stima euristica basata sui campi recipient raw; `Unknown` indica persona non identificata/censurata, non una identita' risolta. Nel sample rigenerato `person_unknown` e' tutto `False` perche' ogni riga finale ha almeno un recipient utilizzabile; non copre recipient potenzialmente censurati dentro campi valorizzati.
Prossimo passo: discutere se rigenerare anche il dataset full oltre al sample e se aprire PR separata per questa correzione runtime.

### Preparare contratto dati processed

Handoff:
Owner: José (Codex)
Stream: feature engineering/documentazione
Branch: `feature/processed-contracts`
PR: da aprire
Task: Preparare contratto dati processed
File modificati:
- `DATA_CONTRACTS.md`
- `Diary.md`
- `TODO.md`
- `TASK_BOARD.md`
Test:
- `uv run python -m pytest tests/test_data_processing.py -q` (`9 passed`)
- `uv run python -m pytest -q` (`17 passed`)
Output: Contratto processed aggiornato con path, formato, input richiesti, regole di trasformazione, schema colonne, nullabilita', vincoli, metadata e verifica sample.
Rischi: `recipient_count_estimate` risulta nullable nel sample corrente; prima di usarlo come feature obbligatoria va validato o corretto.
Prossimo passo: Avviare `Validare recipient_count_estimate` oppure chiudere PR documentale se il team vuole separare fix runtime e contratto.

### Proposta feature engineering fase 2

Handoff:
Owner: Filippo (Antigravity)
Stream: feature engineering
Branch: `feature/feature-engineering`
PR: N/A (local)
Task: Proposta feature engineering fase 2
File modificati:
- `DECISIONS.md`
- `docs/knowledge/03_cleaning_feature_engineering.md`
Test: Nessun file sorgente modificato, solo update documentale.
Output: Feature ausiliarie proposte, approvate e registrate.
Rischi: Durante l'implementazione andrà aggiornato DATA_CONTRACTS.md.
Prossimo passo: Sviluppo in src/utils/data_processing.py

### Consolidare task preprocessing

Owner: José (Codex)
Stream: feature engineering/documentazione
Branch: `feature/preprocessing-consolidation`

File modificati:

- `TASK_BOARD.md`
- `DECISIONS.md`
- `docs/knowledge/03_cleaning_feature_engineering.md`

File letti:

- `src/utils/data_processing.py`
- `tests/test_data_processing.py`
- `src/notebooks/data_preprocessing_validation.ipynb`
- `DATA_CONTRACTS.md`

Output:

- confermato che la pipeline preprocessing e' gia' conservativa e testata;
- approvata policy di non rimuovere stop words da `combined_text` per embeddings;
- documentata policy operativa preprocessing;
- proposti sotto-task per colonne ausiliarie e analisi boilerplate/forward headers.

Verifica:

```bash
uv run python -m pytest tests/test_data_processing.py -q
uv run python -m pytest -q
```

Esito:

- `9 passed`
- `17 passed`

Rischi residui:

- eventuali nuove colonne ausiliarie richiederanno aggiornamento di `DATA_CONTRACTS.md`;
- normalizzazioni aggressive devono essere valutate con confronto embeddings/clustering.


### Correggere docstring contaminata in data extraction

Handoff:
Owner: Filippo (Antigravity)
Stream: manutenzione
Branch: `fix/data-extraction-docstring`
PR: N/A (commit locale)
Task: Correggere docstring contaminata in data extraction
File modificati:
- `src/utils/data_extraction.py`
Test: `uv run python -m pytest tests/test_data_extraction.py -q` (Passati)
Output: Docstring corretta
Rischi: Nessuno
Prossimo passo: Commit e push

### Creare documenti di coordinamento agenti

Owner: Codex
Stream: coordinamento
Branch: workspace locale

File modificati:

- `AGENTS_COLLABORATION.md`
- `TASK_BOARD.md`
- `DECISIONS.md`
- `DATA_CONTRACTS.md`
- `docs/knowledge/agent_workflow.md`
- `docs/knowledge/00_index.md`

Verifica:

- controllo sintattico manuale Markdown;
- nessun codice modificato.

### Raffinamento Preprocessing e Pulizia Rumore

Owner: Gemini (AI Agent)
Stream: Preprocessing
Branch: `feature/refined-preprocessing`
Stato: In Progress

Scopo:
Migliorare la qualità del dataset in input agli embeddings raffinando i filtri (es. Salesforce), rimuovendo feature inutilizzate e integrando analisi contestuali/LLM per ridurre il rumore semantico.

File scrivibili:
- `src/utils/data_processing.py`
- `DATA_CONTRACTS.md`
- `DECISIONS.md`
- `docs/knowledge/03_cleaning_feature_engineering.md`

Output attesi:
- Filtri migliorati per email promozionali/automatiche.
- Dataset snellito (rimozione feature superflue).
