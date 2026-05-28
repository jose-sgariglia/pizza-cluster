# TASK BOARD

## Regole

- Ogni task deve avere uno sviluppatore owner.
- Ogni task deve dichiarare stream, branch e file ownership prima di iniziare.
- `ROADMAP.md` resta la visione degli obiettivi funzionali.
- Questo file gestisce il lavoro operativo asincrono tra sviluppatori e assistenti.
- Spostare un task in `Done` solo dopo test/verifica e handoff.

## Backlog

### Correggere docstring contaminata in data extraction

Owner: Filippo (Antigravity)
Stream: manutenzione
Branch proposta: `fix/data-extraction-docstring`

File scrivibili:

- `src/utils/data_extraction.py`

Test:

```bash
uv run python -m pytest tests/test_data_extraction.py -q
```

Note:

- La contaminazione e' nella docstring di `extract_sample_from_local_parquet`.
- Non dovrebbe cambiare comportamento runtime.

### Consolidare task preprocessing

Owner: José (Codex)
Stream: feature engineering/documentazione
Branch proposta: `feature/preprocessing-consolidation`

File scrivibili:

- `TASK_BOARD.md`
- `DECISIONS.md`
- `docs/knowledge/03_cleaning_feature_engineering.md`

File da leggere:

- `src/utils/data_processing.py`
- `tests/test_data_processing.py`
- `src/notebooks/data_preprocessing_validation.ipynb`

Output:

- proposta su cosa manca realmente per chiudere il TODO preprocessing;
- eventuale lista sotto-task.

### Preparare contratto dati processed

Owner: José (Codex)
Stream: feature engineering/documentazione
Branch proposta: `feature/processed-contracts`

File scrivibili:

- `DATA_CONTRACTS.md`

File da leggere:

- `src/utils/data_processing.py`
- `data/metadata/jmail_processing_sample_metadata.json`
- `docs/knowledge/03_cleaning_feature_engineering.md`

Output:

- schema colonne processed;
- path input/output;
- regole su null e tipi.

### Proposta feature engineering fase 2

Owner proposto: Filippo (Antigravity)
Stream: feature engineering
Branch proposta: `feature/feature-engineering`

File scrivibili:

- `DECISIONS.md`
- `docs/knowledge/03_cleaning_feature_engineering.md`

Output:

- proposta con pro/contro;
- feature candidate;
- test previsti;
- impatto su clustering.

### Consolidare embeddings baseline

Owner proposto: José (Codex)
Stream: embeddings/studio/analisi
Branch proposta: `feature/embeddings-baseline`

File scrivibili:

- `src/utils/embedding_pipeline.py`
- `tests/test_embedding_pipeline.py`
- `docs/knowledge/04_embedding_strategy_memo.md`
- `docs/embedding_research/`

Output:

- baseline embeddings riproducibile;
- parametri documentati;
- test verdi;
- note su come rigenerare embeddings dopo feature engineering.

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

Nessun task assegnato.

## In Progress

Nessun task in corso.

## Blocked

Nessun task bloccato.

## Done

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
