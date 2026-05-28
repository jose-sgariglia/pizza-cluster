# TASK BOARD

## Regole

- Ogni task deve avere un owner.
- Ogni task deve dichiarare file ownership prima di iniziare.
- `TODO.md` resta la lista degli obiettivi funzionali.
- Questo file gestisce il lavoro operativo giornaliero tra agenti.
- Spostare un task in `Done` solo dopo test/verifica e handoff.

## Backlog

### Correggere docstring contaminata in data extraction

Owner: da assegnare

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

Owner: da assegnare

File scrivibili:

- `TODO.md`
- `Diary.md`
- `docs/knowledge/03_cleaning_feature_engineering.md`

File da leggere:

- `src/utils/data_processing.py`
- `tests/test_data_processing.py`
- `src/notebooks/data_preprocessing_validation.ipynb`

Output:

- proposta su cosa manca realmente per chiudere il TODO preprocessing;
- eventuale lista sotto-task.

### Preparare contratto dati processed

Owner: da assegnare

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

Owner: da assegnare

File scrivibili:

- `DECISIONS.md`
- `docs/knowledge/03_cleaning_feature_engineering.md`

Output:

- proposta con pro/contro;
- feature candidate;
- test previsti;
- impatto su clustering.

## Ready

Nessun task assegnato.

## In Progress

Nessun task in corso.

## Blocked

Nessun task bloccato.

## Done

### Creare documenti di coordinamento agenti

Owner: Codex

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

