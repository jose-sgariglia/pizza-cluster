# Data Extraction

## Obiettivo

Estrarre il dataset raw da JMAIL e salvarlo in `data/raw/`, mantenendo metadata tecnici in `data/metadata/`.

## Sorgente

- API configurata tramite `JMAIL_API` nel file `.env`.
- Endpoint usato: `v1/emails.parquet`.
- Il valore completo dell'URL non viene documentato per evitare di copiare configurazioni operative nei report.

## Output

- `data/raw/jmail_emails.parquet`
- opzionale: `data/raw/jmail_emails_sample.parquet`
- `data/metadata/jmail_extraction_metadata.json`

I file dati generati sono esclusi da git tramite `.gitignore`; i placeholder `.gitkeep` mantengono invece la struttura del repository.

## Comando

```bash
python -m src.utils.data_extraction
```

Per creare anche un sample locale:

```bash
python -m src.utils.data_extraction --sample-limit 100
```

## Mini spiegazione

DuckDB e' un motore SQL embedded che puo' leggere direttamente file Parquet remoti senza scaricare manualmente tutto il dataset. Serve per ispezionare schema, contare righe ed estrarre sample in modo riproducibile. Si usa quando i dati sono tabellari e conviene lavorare con query SQL leggere prima di materializzare file locali.

Parquet e' un formato colonnare pensato per dati analitici. Serve per salvare dataset tabellari in modo compatto ed efficiente. Si usa quando si devono leggere colonne specifiche, lavorare con dataset medi/grandi o mantenere compatibilita' con tool data science.

## Approfondimenti

Documentazione:

- DuckDB Python API: https://duckdb.org/docs/stable/clients/python/overview
- DuckDB Parquet: https://duckdb.org/docs/lts/data/parquet/overview.html
- Apache Parquet format: https://parquet.apache.org/docs/file-format/

Risorsa studio:

- DuckDB guides: https://duckdb.org/docs/stable/guides/overview
