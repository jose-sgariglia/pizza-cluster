# Cleaning and Rough Feature Engineering

## Obiettivo

Creare il primo dataset `processed` partendo dal raw JMAIL, mantenendo il raw immutato e aggiungendo feature semplici per esplorazione, clustering e controlli successivi.

## Input e output

Input:

- `data/raw/jmail_emails.parquet`

Output:

- `data/processed/jmail_emails_processed.parquet`
- `data/metadata/jmail_processing_metadata.json`

Output sample per test veloce:

- `data/processed/jmail_emails_processed_sample.parquet`
- `data/metadata/jmail_processing_sample_metadata.json`

## Pipeline implementata

1. Selezione colonne utili per la prima pipeline.
2. Rimozione record esplicitamente promozionali con `is_promotional == True`.
3. Normalizzazione whitespace su `subject` e `content_markdown`.
4. Creazione `combined_text` da subject e corpo markdown.
5. Parsing temporale di `sent_at`.
6. Feature grezze:
   - `subject_length`
   - `content_length`
   - `combined_text_length`
   - `has_subject`
   - `has_sender`
   - `has_attachments`
   - `has_redaction`
   - `recipient_count_estimate`
   - `sent_year`
   - `sent_month`
   - `sent_dayofweek`
7. Rimozione righe senza testo utilizzabile in `combined_text`.

## Policy sulle censure

Le parti censurate non vengono modificate, rimosse o riscritte.

La pipeline crea solo `has_redaction`, un flag euristico che segnala marker come `redacted`, `withheld`, `sealed`, blocchi `XXXX` o caratteri oscuranti. Il testo rimane preservato in `content_clean` e `combined_text`, salvo normalizzazione degli spazi.

## Policy operativa preprocessing

La pipeline corrente usa cleaning conservativo per preservare il contenuto utile agli embeddings. `combined_text` normalizza whitespace, combina subject e corpo markdown, conserva redazioni e non rimuove stop words.

La rimozione stop words non e' applicata all'input embeddings per evitare perdita di contesto sintattico e semantico nei sentence embeddings. Eventuali trasformazioni piu' aggressive vanno introdotte come colonne ausiliarie per feature statistiche o analisi interpretabili, non come sostituzione implicita di `combined_text`.

Questa policy mantiene confrontabile la baseline embeddings gia' prodotta. Se in futuro si introduce una colonna testuale alternativa, il cambio dovra' essere trattato come modifica di contratto dati e validato con test e confronto embeddings/clustering.

Decisioni ancora aperte:

- normalizzazione email e nomi;
- rimozione o tagging di forward headers;
- gestione boilerplate e firme;
- eventuale colonna dedicata per feature statistiche.

## Colonne escluse nella prima pipeline

- `content_html`: quasi sempre nullo e potenzialmente molto rumoroso quando presente.
- `account_email`: quasi sempre nullo.
- `folder_path`: quasi sempre nullo.

## Limiti noti

- `recipient_count_estimate` e' una stima basata su split testuale semplice.
- `has_redaction` e' euristico e va raffinato dopo revisione mirata.
- La pipeline non rimuove ancora firme, forward header o boilerplate email.
- La pipeline non normalizza ancora entita', nomi o indirizzi email.
- La pipeline non rimuove stop words da `combined_text` per scelta metodologica approvata.

## Validazione su sample

Per evitare tempi lunghi nella fase di test, la pipeline puo' essere eseguita sul numero di sample specificato nella variabile `PROCESSING_SAMPLE_SIZE`.

```bash
python -m src.utils.data_processing --limit <PROCESSING_SAMPLE_SIZE>
```

Se `PROCESSING_SAMPLE_SIZE=-1`, la pipeline deve essere eseguita sul dataset completo:

```bash
python -m src.utils.data_processing --limit -1
```

Risultati della validazione corrente con `PROCESSING_SAMPLE_SIZE=1000`:

- input: 1000 righe
- output: 355 righe
- record promozionali rimossi: 645
- righe senza testo rimosse: 0
- colonne output: 31
- righe con `has_redaction == True`: 6

Questa validazione non sostituisce l'esecuzione completa sul dataset intero.

## Mini spiegazione

Il cleaning rende il dataset coerente senza alterare il raw originale. Serve a rimuovere rumore evidente, uniformare formati e preparare colonne stabili per le fasi successive. In questa pipeline il cleaning e' conservativo per non perdere informazione sensibile o contestuale.

Il feature engineering crea variabili derivate dai dati originali. Serve a rendere osservabili caratteristiche utili, come lunghezza testo, presenza allegati, temporalita' o redazioni. In questa fase usiamo feature grezze e interpretabili per guidare analisi e modelli futuri.

Le stop words sono parole molto frequenti, come articoli, preposizioni e ausiliari. In modelli bag-of-words o TF-IDF possono essere filtrate per ridurre rumore e dimensionalita'. Con sentence embeddings moderni vanno trattate con cautela perche' il modello usa anche contesto, ordine e funzione grammaticale.

I sentence embeddings sono vettori densi che rappresentano il significato di frasi o documenti. Servono per similarita', clustering e retrieval semantico. In questo progetto sono sensibili al testo di input, quindi modifiche aggressive a `combined_text` devono essere misurate e non introdotte implicitamente.

TF-IDF e bag-of-words trasformano testi in vettori sparsi basati su frequenze di token. Servono per feature interpretabili, keyword extraction e baseline semplici. Sono piu' adatti a colonne ausiliarie o analisi cluster che al testo semantico usato per embeddings.

## Approfondimenti

Documentazione:

- pandas text data: https://pandas.pydata.org/docs/user_guide/text.html
- pandas time series: https://pandas.pydata.org/docs/user_guide/timeseries.html
- scikit-learn feature extraction: https://scikit-learn.org/stable/modules/feature_extraction.html
- Sentence Transformers documentation: https://sbert.net/
- BGE small EN v1.5 model card: https://huggingface.co/BAAI/bge-small-en-v1.5

Paper:

- Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks: https://arxiv.org/abs/1908.10084

Risorsa studio:

- Google Machine Learning Crash Course, data preparation: https://developers.google.com/machine-learning/data-prep
- Google Machine Learning Crash Course: https://developers.google.com/machine-learning/crash-course

## Argomenti da studiare / approfondire per la comprensione

- Cleaning conservativo vs cleaning aggressivo
- Stop words
- Sentence embeddings
- TF-IDF
- Bag-of-words
- Feature engineering testuale
- Boilerplate email
- Forward headers
