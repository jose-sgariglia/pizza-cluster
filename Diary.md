# Diary

## Storico compresso - 2026-05-26

Sessione avviata con reset del workspace e ripartenza da repository pulita. Sono state create o riallineate le directory base (`data/`, `docs/`, `reports/`, `src/`, `tests/`) con placeholder dove necessario.

Attivita' completate prima degli ultimi checkpoint:

- estrazione dati JMAIL da endpoint Parquet in `data/raw/jmail_emails.parquet`;
- generazione sample raw e metadata di estrazione;
- profiling strutturale del dataset raw con `src/utils/data_profiling.py`;
- documentazione dataset in `docs/knowledge/02_dataset_understanding.md`;
- prima pipeline cleaning/feature engineering in `src/utils/data_processing.py`;
- validazione pipeline su sample configurabile;
- notebook preprocessing `src/notebooks/data_preprocessing_validation.ipynb`;
- salvataggio figure preprocessing in `reports/figures/data_preprocessing_validation/` con JSON affiancati;
- configurazione `PROCESSING_SAMPLE_SIZE`, dove `-1` indica dataset completo;
- raccolta documentazione embeddings in `docs/embedding_research/`;
- memo embeddings in `docs/knowledge/04_embedding_strategy_memo.md`;
- primo sviluppo della pipeline embeddings in `src/utils/embedding_pipeline.py`.

Risultati consolidati:

- raw JMAIL: 1.783.792 righe, 19 colonne;
- processed sample: 355 righe da input sample di 1000;
- modello embeddings scelto per primo run: `BAAI/bge-small-en-v1.5`;
- test suite mantenuta verde durante la sessione.

## 2026-05-26 - Pipeline Python embeddings

### Checkpoint

Implementata pipeline Python per generazione embeddings.

### Intervento

- Esteso `src/utils/embedding_pipeline.py` con caricamento modello, costruzione chunk, encoding, aggregazione mean-pooling, salvataggio `.npy`, index Parquet e metadata JSON.
- Aggiunto `EMBEDDING_BATCH_SIZE` a `.env` e `.env.sample`.
- Aggiunti test unitari in `tests/test_embedding_pipeline.py`.

### Motivazione tecnica

La pipeline resta modulare e verificabile: funzioni pure e configurazione sono testate senza scaricare o caricare modelli reali.

## 2026-05-26 - Embeddings sample generati

### Checkpoint

Generati embeddings sul processed sample.

### Intervento

- Eseguita `src.utils.embedding_pipeline` con modello `BAAI/bge-small-en-v1.5`.
- Salvato array embeddings inizialmente in `models/embeddings/email_embeddings.npy`.
- Salvato index email/chunk in `data/metadata/email_embedding_index.parquet`.
- Salvati metadata in `data/metadata/email_embedding_metadata.json`.
- Aggiornata memo embeddings con risultati del primo run.
- Aggiornato `TODO.md` marcando completata la task embeddings.

### Risultati

- email processate: 355
- dimensioni embedding: 384
- chunk totali: 545
- righe senza chunk: 0
- norme vettoriali min/media/max: 1.0 / 1.0 / 1.0

### Motivazione tecnica

Il sample conferma che la pipeline produce vettori normalizzati coerenti e allineati alle email processate prima di passare a esperimenti di clustering.

## 2026-05-26 - Path embeddings in data

### Checkpoint

Output embeddings spostato sotto `data/embeddings`.

### Intervento

- Aggiunta cartella `data/embeddings/`.
- Aggiornati `.env`, `.env.sample`, `.gitignore` e `src/utils/embedding_pipeline.py`.
- Aggiornati test e memo embeddings per usare `data/embeddings/email_embeddings.npy`.
- Spostato l'array embeddings sample dalla vecchia path `models/embeddings/` alla nuova path `data/embeddings/`.

### Motivazione tecnica

Gli embeddings sono dati derivati dal dataset, non pesi o checkpoint di modello. Tenerli sotto `data/embeddings` separa meglio artefatti dati e artefatti modello.

## 2026-05-26 - Notebook processo embeddings

### Checkpoint

Notebook embeddings creato ed eseguito.

### Intervento

- Creato `src/notebooks/embedding_process.ipynb`.
- Documentate le fasi: pulizia input, feature engineering pre-embedding, chunking, generazione embeddings e controlli.
- Salvati grafici diagnostici in `reports/figures/embedding_process/` con JSON affiancati.
- Rieseguita la pipeline embeddings con output in `data/embeddings/email_embeddings.npy`.
- Rieseguito il notebook con `nbconvert`.

### Motivazione tecnica

Il notebook rende verificabile e comunicabile il processo embeddings senza spostare logica applicativa fuori dai moduli `src/utils`.

## 2026-05-26 - Chiusura sessione

### Checkpoint

Sessione giornaliera chiusa con diario compresso.

### Intervento

- Mantenuti estesi solo gli ultimi 5 checkpoint operativi.
- Compresso lo storico precedente in un riepilogo sintetico.
- Preservati i dettagli essenziali su dati, pipeline, notebook, documentazione e risultati principali.

### Motivazione tecnica

Il diario resta leggibile senza perdere il contesto necessario per riprendere il lavoro nella prossima sessione.
