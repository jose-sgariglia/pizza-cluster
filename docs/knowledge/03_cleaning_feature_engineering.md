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

## Colonne escluse nella prima pipeline

- `content_html`: quasi sempre nullo e potenzialmente molto rumoroso quando presente.
- `account_email`: quasi sempre nullo.
- `folder_path`: quasi sempre nullo.

## Limiti noti

- `recipient_count_estimate` e' una stima basata su split testuale semplice.
- `has_redaction` e' euristico e va raffinato dopo revisione mirata.
- La pipeline non rimuove ancora firme, forward header o boilerplate email.
- La pipeline non normalizza ancora entita', nomi o indirizzi email.

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

## Approfondimenti

Documentazione:

- pandas text data: https://pandas.pydata.org/docs/user_guide/text.html
- pandas time series: https://pandas.pydata.org/docs/user_guide/timeseries.html
- scikit-learn feature extraction: https://scikit-learn.org/stable/modules/feature_extraction.html

Risorsa studio:ò

- Google Machine Learning Crash Course, data preparation: https://developers.google.com/machine-learning/data-prep
