# DATA CONTRACTS

## Scopo

Definire i contratti dati tra le fasi della pipeline: raw, processed, embeddings, clustering, API e demo.

Questo file serve a permettere lavoro parallelo tra agenti. Un agente puo' sviluppare notebook, API o demo senza leggere l'intera pipeline se il contratto dati e' stabile e aggiornato.

## Regole

- Ogni contratto deve indicare path, formato, colonne richieste, colonne prodotte e vincoli.
- Ogni modifica a colonne, tipi o path deve essere proposta e approvata.
- API e demo devono dipendere dai contratti, non da assunzioni implicite.
- I contratti vanno aggiornati prima dei consumatori downstream.

## Raw Emails

Stato: Draft

Path:

- `data/raw/jmail_emails.parquet`
- sample: `data/raw/jmail_emails_sample.parquet`

Formato:

- Parquet

Origine:

- JMAIL endpoint configurato via `.env`.

Colonne note usate dalla pipeline:

- `id`
- `doc_id`
- `message_index`
- `sender`
- `subject`
- `to_recipients`
- `cc_recipients`
- `bcc_recipients`
- `sent_at`
- `content_markdown`
- `attachments`
- `email_drop_id`
- `is_promotional`
- `release_batch`
- `epstein_is_sender`
- `all_participants`

Vincoli:

- Raw immutato.
- Nessuna trasformazione in-place.

## Processed Emails

Stato: Draft

Path:

- full: `data/processed/jmail_emails_processed.parquet`
- sample: `data/processed/jmail_emails_processed_sample.parquet`

Formato:

- Parquet

Prodotto da:

- `src/utils/data_processing.py`

Colonne richieste in input:

- subset disponibile delle colonne raw supportate.

Colonne prodotte principali:

- colonne raw selezionate;
- `subject_clean`;
- `content_clean`;
- `combined_text`;
- `subject_length`;
- `content_length`;
- `combined_text_length`;
- `has_subject`;
- `has_redaction`;
- `sent_at_datetime`;
- `sent_year`;
- `sent_month`;
- `sent_dayofweek`;
- `has_sender`;
- `has_attachments`;
- `recipient_count_estimate`.

Vincoli:

- `combined_text` deve essere non vuoto nelle righe finali.
- Le redazioni non vengono rimosse dal testo.
- `is_promotional == True` viene escluso.

Metadata:

- full: `data/metadata/jmail_processing_metadata.json`
- sample: `data/metadata/jmail_processing_sample_metadata.json`

## Email Embeddings

Stato: Draft

Path:

- vectors: `data/embeddings/email_embeddings.npy`
- index: `data/metadata/email_embedding_index.parquet`
- metadata: `data/metadata/email_embedding_metadata.json`

Formato:

- NumPy array `.npy` per vettori.
- Parquet per index.
- JSON per metadata.

Prodotto da:

- `src/utils/embedding_pipeline.py`

Input:

- processed emails;
- colonna testo configurata, default `combined_text`.

Vincoli:

- Una riga embedding per email processata.
- Embeddings normalizzati L2 dopo aggregazione chunk.
- Index deve mantenere allineamento tra email e chunk.

## Cluster Assignments

Stato: Proposed

Path proposto:

- `data/processed/email_cluster_assignments.parquet`
- `data/metadata/clustering_metadata.json`

Formato proposto:

- Parquet per assegnazioni.
- JSON per metadata e parametri.

Colonne candidate:

- `id`
- `cluster_id`
- `cluster_label`
- `is_outlier`
- `distance_to_representative`
- `model_version`

Decisioni mancanti:

- algoritmo clustering;
- metriche;
- gestione outlier;
- strategia naming cluster.

## API/Demo Contract

Stato: Proposed

Consumatori:

- API modello;
- demo esplorativa;
- notebook di validazione cluster.

Entita' candidate:

- cluster summary;
- cluster detail;
- email summary;
- email detail;
- metadata modello.

Decisioni mancanti:

- framework API;
- formato risposta;
- paginazione;
- campi esposti per email redatte o sensibili.

