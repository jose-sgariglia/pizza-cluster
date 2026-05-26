# Dataset Understanding

## Snapshot

- Sorgente: JMAIL Parquet locale generato da `src/utils/data_extraction.py`.
- File raw: `data/raw/jmail_emails.parquet`.
- Righe: 1.783.792.
- Colonne: 19.
- Profilo tecnico: `data/metadata/jmail_profile.json`.

## Colonne disponibili

| Colonna | Tipo | Null ratio | Nota operativa |
|---|---:|---:|---|
| `id` | string | 0.000000 | Identificativo record. |
| `doc_id` | string | 0.000000 | Identificativo documento sorgente. |
| `message_index` | int64 | 0.000000 | Indice messaggio nel documento. |
| `sender` | string | 0.071382 | Mittente; utile per grafo e filtri. |
| `subject` | string | 0.256982 | Testo breve; utile ma spesso assente. |
| `to_recipients` | string | 0.000000 | Destinatari primari. |
| `cc_recipients` | string | 0.000001 | Destinatari in copia. |
| `bcc_recipients` | string | 0.000594 | Destinatari nascosti, quasi sempre presente. |
| `sent_at` | string | 0.002821 | Timestamp da normalizzare. |
| `content_markdown` | string | 0.000281 | Corpo email principale per NLP. |
| `content_html` | string | 0.990996 | Quasi sempre nullo; non prioritario. |
| `attachments` | int64 | 0.000000 | Conteggio allegati o indicatore simile. |
| `account_email` | string | 0.984165 | Quasi sempre nullo; bassa priorita'. |
| `email_drop_id` | string | 0.000000 | Batch/drop sorgente. |
| `folder_path` | string | 0.990219 | Quasi sempre nullo; bassa priorita'. |
| `is_promotional` | bool | 0.000004 | Filtro candidato per rimuovere rumore. |
| `release_batch` | int64 | 0.000000 | Batch di rilascio. |
| `epstein_is_sender` | bool | 0.000997 | Flag analitico utile per segmentazioni. |
| `all_participants` | string | 0.000000 | Partecipanti aggregati. |

## Colonne candidate per clustering testuale

- `content_markdown`: sorgente primaria. Ha copertura quasi completa e lunghezza media circa 619 caratteri.
- `subject`: sorgente secondaria. Utile come segnale sintetico, ma con circa 25,7% di valori nulli.
- `content_html`: per ora non prioritario perche' nullo nel 99,1% dei record e potenzialmente rumoroso.

## Colonne candidate per filtri e feature engineering

- `is_promotional`: filtro iniziale per ridurre rumore promozionale.
- `epstein_is_sender`: feature/segmentazione binaria.
- `attachments`: feature numerica grezza.
- `sent_at`: feature temporale dopo parsing in datetime.
- `sender`, `to_recipients`, `cc_recipients`, `bcc_recipients`, `all_participants`: feature relazionali o base per grafo.
- Lunghezza testo da `content_markdown` e `subject`: feature grezze per analisi preliminare.

## Rischi dati iniziali

- `sender` ha circa 7,1% nulli: serve una policy prima di costruire grafi o feature relazionali.
- `subject` ha circa 25,7% nulli: non deve essere l'unico testo per clustering.
- `content_markdown` ha valori molto lunghi: massimo osservato 360.334 caratteri. Serve clipping o normalizzazione prima di embedding.
- `content_html` ha valori estremamente lunghi quando presente: meglio escluderlo dalla prima pipeline.
- `sent_at` e' stringa: va convertito e validato prima di feature temporali.

## Decisione operativa proposta

Per la prima pipeline usare:

- ID e tracciabilita': `id`, `doc_id`, `message_index`, `email_drop_id`, `release_batch`.
- Testo: `subject`, `content_markdown`.
- Metadata email: `sender`, `to_recipients`, `cc_recipients`, `bcc_recipients`, `all_participants`, `sent_at`, `attachments`, `epstein_is_sender`, `is_promotional`.
- Escludere inizialmente: `content_html`, `account_email`, `folder_path`.

## Mini spiegazione

Il data profiling e' una fase di esplorazione strutturale: misura tipi, nulli, copertura e statistiche base prima di progettare cleaning e feature. Serve a evitare assunzioni sbagliate sulla qualita' del dataset. Si usa all'inizio di una pipeline dati e ogni volta che cambia la sorgente.

I missing values sono valori assenti o non disponibili. Servono policy esplicite per decidere se imputare, filtrare o lasciare nullo un campo. Nel clustering testuale sono importanti per evitare testi vuoti, feature distorte o segmentazioni non confrontabili.

## Approfondimenti

Documentazione:

- pandas missing data: https://pandas.pydata.org/docs/user_guide/missing_data.html
- PyArrow Parquet: https://arrow.apache.org/docs/python/parquet.html
- DuckDB Parquet: https://duckdb.org/docs/lts/data/parquet/overview.html

Risorsa studio:

- Google Machine Learning Crash Course, data preparation: https://developers.google.com/machine-learning/data-prep

