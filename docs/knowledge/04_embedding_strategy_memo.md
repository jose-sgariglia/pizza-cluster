# Embedding Strategy Memo

## Obiettivo

Preparare una pipeline embeddings per trasformare il testo processato delle email in vettori numerici utilizzabili da clustering, visualizzazione e ricerca semantica.

## Input previsto

- `data/processed/jmail_emails_processed_sample.parquet` durante la validazione.
- `data/processed/jmail_emails_processed.parquet` quando `PROCESSING_SAMPLE_SIZE=-1` e si vuole lavorare sul dataset completo.
- Colonna testuale iniziale: `combined_text`.

## Feature engineering prima degli embeddings

Prima versione consigliata:

- creare `embedding_text` da `combined_text`;
- preservare censure e marker redacted;
- non rimuovere stop words nella prima baseline;
- non eliminare nomi, email o date;
- calcolare metadata di supporto: `embedding_text_length`, `chunk_count`, `redaction_marker_count`, `redaction_ratio_estimate`.

Motivo: i Transformer usano il contesto; rimuovere stop words o token apparentemente deboli puo' peggiorare la rappresentazione semantica. Le trasformazioni aggressive vanno testate come variante, non nella baseline.

## Gestione testi lunghi

I modelli candidati hanno limiti di contesto. La pipeline dovra':

1. dividere testi lunghi in chunk;
2. calcolare embedding per chunk;
3. aggregare i chunk della stessa email, inizialmente con media vettoriale;
4. salvare `chunk_count` e parametri di chunking nei metadata.

## Modelli candidati

### `BAAI/bge-small-en-v1.5`

Vantaggi:

- leggero;
- embedding da 384 dimensioni;
- buon compromesso tra qualita' e costo;
- licenza MIT;
- adatto come prima baseline seria.

Svantaggi:

- principalmente inglese;
- va verificato sul clustering, non solo retrieval;
- richiede chunking per testi lunghi.

### `sentence-transformers/all-MiniLM-L6-v2`

Vantaggi:

- molto veloce;
- diffuso e stabile;
- embedding da 384 dimensioni;
- adatto a baseline rapida.

Svantaggi:

- meno potente dei modelli piu' recenti;
- input lungo troncato;
- puo' produrre cluster meno ricchi su testi complessi.

### `intfloat/e5-base-v2`

Vantaggi:

- piu' robusto;
- adatto a retrieval, clustering e classificazione;
- embedding da 768 dimensioni piu' espressivi.

Svantaggi:

- piu' costoso in memoria e tempo;
- richiede convenzioni di input, ad esempio prefisso `passage:`;
- clustering piu' pesante.

## Raccomandazione

Implementare prima `BAAI/bge-small-en-v1.5` su sample, mantenendo configurabile il modello in `.env`.

Poi confrontare:

1. `sentence-transformers/all-MiniLM-L6-v2` come baseline veloce;
2. `intfloat/e5-base-v2` come candidato di qualita' superiore.

## Mini spiegazione

Gli embeddings trasformano testo in vettori numerici che rappresentano similarita' semantica. Servono per applicare clustering, ricerca semantica e visualizzazioni geometriche a dati testuali. Per email lunghe serve una policy di chunking, altrimenti il modello tronca il testo e perde informazione.

## Primo run embeddings

Configurazione:

- modello: `BAAI/bge-small-en-v1.5`
- input: `data/processed/jmail_emails_processed_sample.parquet`
- testo: `combined_text`
- chunk length: 1800 caratteri
- chunk overlap: 200 caratteri
- batch size: 32
- aggregazione chunk: media vettoriale
- normalizzazione finale: L2

Output:

- `data/embeddings/email_embeddings.npy`
- `data/metadata/email_embedding_index.parquet`
- `data/metadata/email_embedding_metadata.json`
- `src/notebooks/embedding_process.ipynb` documenta il processo con grafici diagnostici.

Risultati:

- email processate: 355
- dimensioni embedding: 384
- chunk totali: 545
- righe senza chunk: 0
- norma vettoriale media: 1.0

Nota: questo run usa il processed sample, non il dataset completo.

## Approfondimenti

Paper:

- MTEB: `docs/embedding_research/papers/mteb_2210.07316.pdf`
- E5: `docs/embedding_research/papers/e5_2212.03533.pdf`

Model cards:

- `docs/embedding_research/model_cards/all-MiniLM-L6-v2_README.md`
- `docs/embedding_research/model_cards/bge-small-en-v1.5_README.md`
- `docs/embedding_research/model_cards/e5-base-v2_README.md`

Link:

- `docs/embedding_research/links/embedding_links.md`
