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

Stato: Draft verificato su sample

Path:

- full: `data/processed/jmail_emails_processed.parquet`
- sample: `data/processed/jmail_emails_processed_sample.parquet`

Formato:

- Parquet

Prodotto da:

- `src/utils/data_processing.py`

Colonne richieste in input:

- subset disponibile delle colonne raw supportate da `KEEP_COLUMNS`;
- colonne usate per feature se presenti:
  - `subject`
  - `content_markdown`
  - `sent_at`
  - `sender`
  - `attachments`
  - `to_recipients`
  - `cc_recipients`
  - `bcc_recipients`
  - `is_promotional`

Regole di trasformazione:

- seleziona solo le colonne raw supportate disponibili;
- esclude righe con `is_promotional == True`;
- conserva righe con `is_promotional` nullo o non vero;
- normalizza whitespace in `subject_clean` e `content_clean`;
- costruisce `combined_text` concatenando `subject_clean` e `content_clean`;
- rimuove righe con `combined_text` vuoto;
- conserva redazioni e marker sensibili nel testo;
- segnala redazioni tramite `has_redaction`;
- non rimuove stop words da `combined_text`;
- non normalizza ancora email, nomi, firme, boilerplate o forward headers.

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

Schema colonne processed:

| Colonna | Tipo atteso | Null | Origine | Note |
| --- | --- | --- | --- | --- |
| `id` | string | dipende dal raw | raw | Identificativo email. |
| `doc_id` | string | dipende dal raw | raw | Identificativo documento. |
| `message_index` | integer | dipende dal raw | raw | Indice messaggio nel documento/drop. |
| `sender` | string | ammesso | raw | Mittente raw, non normalizzato. |
| `subject` | string | ammesso | raw | Oggetto raw. |
| `to_recipients` | string | ammesso | raw | Destinatari raw, non normalizzati. |
| `cc_recipients` | string | ammesso | raw | Destinatari CC raw, non normalizzati. |
| `bcc_recipients` | string | ammesso | raw | Destinatari BCC raw, non normalizzati. |
| `sent_at` | string | ammesso | raw | Timestamp raw. |
| `content_markdown` | string | ammesso | raw | Corpo markdown raw. |
| `attachments` | integer | ammesso | raw | Conteggio allegati raw quando disponibile. |
| `email_drop_id` | string | dipende dal raw | raw | Identificativo drop. |
| `is_promotional` | boolean | ammesso | raw | Le righe con valore `True` sono escluse. |
| `release_batch` | integer | dipende dal raw | raw | Batch di rilascio. |
| `epstein_is_sender` | boolean | ammesso | raw | Flag raw. |
| `all_participants` | string | ammesso | raw | Partecipanti raw, non normalizzati. |
| `subject_clean` | string | no | pipeline | Whitespace normalizzato; stringa vuota se input non testuale. |
| `content_clean` | string | no | pipeline | Whitespace normalizzato; redazioni preservate. |
| `combined_text` | string | no | pipeline | Campo testuale primario per embeddings; deve essere non vuoto. |
| `subject_length` | integer | no | pipeline | Lunghezza di `subject_clean`. |
| `content_length` | integer | no | pipeline | Lunghezza di `content_clean`. |
| `combined_text_length` | integer | no | pipeline | Lunghezza di `combined_text`. |
| `has_subject` | boolean | no | pipeline | `True` se `subject_clean` non e' vuoto. |
| `has_redaction` | boolean | no | pipeline | Flag euristico; non modifica il testo. |
| `sent_at_datetime` | datetime UTC | ammesso | pipeline | Parsing di `sent_at` con errori convertiti a null. |
| `sent_year` | nullable integer | ammesso | pipeline | Anno derivato da `sent_at_datetime`. |
| `sent_month` | nullable integer | ammesso | pipeline | Mese derivato da `sent_at_datetime`. |
| `sent_dayofweek` | nullable integer | ammesso | pipeline | Giorno settimana derivato da `sent_at_datetime`. |
| `has_sender` | boolean | no | pipeline | `True` se `sender` contiene testo non vuoto. |
| `has_attachments` | boolean | no | pipeline | `True` se `attachments > 0`; null trattato come 0. |
| `recipient_count_estimate` | nullable integer | ammesso | pipeline | Stima grezza da destinatari; da non trattare come feature obbligatoria finche' non viene validata. |

Vincoli:

- `combined_text` deve essere non vuoto nelle righe finali.
- `combined_text` e' il campo testuale default per `Email Embeddings`.
- `combined_text` mantiene stop words, redazioni, nomi, indirizzi email, boilerplate e forward headers.
- Le redazioni non vengono rimosse dal testo.
- `is_promotional == True` viene escluso.
- Le colonne raw mantenute non sono normalizzate.
- Le nuove colonne ausiliarie per feature statistiche richiedono aggiornamento di questo contratto.
- `recipient_count_estimate` e' una stima euristica e puo' essere nullo negli artefatti correnti; prima di usarlo per clustering o feature obbligatorie va verificato o corretto.

Metadata:

- full: `data/metadata/jmail_processing_metadata.json`
- sample: `data/metadata/jmail_processing_sample_metadata.json`

Campi metadata attesi:

- `processed_at_utc`
- `input_rows`
- `selected_rows`
- `after_promotional_filter_rows`
- `output_rows`
- `removed_promotional_rows`
- `removed_empty_text_rows`
- `output_columns`
- `redaction_policy`
- `execution_mode`
- `input_limit`

Verifica sample corrente:

- metadata: `data/metadata/jmail_processing_sample_metadata.json`
- input rows: 1000
- output rows: 355
- output columns: 31
- record promozionali rimossi: 645
- righe senza testo rimosse: 0
- `combined_text` vuoto: 0 righe nel sample letto
- `is_promotional == True`: 0 righe nel sample letto
- nota: `recipient_count_estimate` ha valori null nel sample corrente e va trattato come campo nullable.

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
