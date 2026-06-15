# TASK BOARD

## Regole

- Ogni task deve avere uno sviluppatore owner.
- Ogni task deve dichiarare stream, branch e file ownership prima di iniziare.
- `ROADMAP.md` resta la visione degli obiettivi funzionali.
- Questo file gestisce il lavoro operativo asincrono tra sviluppatori e assistenti.
- Spostare un task in `Done` solo dopo test/verifica e handoff.

## Backlog

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

Nessun task assegnato in Ready.

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
