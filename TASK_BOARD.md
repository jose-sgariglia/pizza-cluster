# TASK BOARD

## Regole

- Ogni task deve avere uno sviluppatore owner.
- Ogni task deve dichiarare stream, branch e file ownership prima di iniziare.
- `ROADMAP.md` resta la visione degli obiettivi funzionali.
- Questo file gestisce il lavoro operativo asincrono tra sviluppatori e assistenti.
- Spostare un task in `Done` solo dopo test/verifica e handoff.

## Backlog

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



### Valutare colonne ausiliarie per feature statistiche

Owner proposto: da assegnare
Stream: feature engineering/documentazione
Branch proposta: `feature/text-stat-features`

Dipendenze:

- decisione approvata su `combined_text` embeddings;
- contratto processed aggiornato se vengono aggiunte colonne.

File scrivibili:

- `DATA_CONTRACTS.md`
- `docs/knowledge/03_cleaning_feature_engineering.md`
- eventuale modulo feature, solo dopo approvazione.

Output:

- proposta per colonne testuali ausiliarie, ad esempio testo per statistiche o keyword extraction;
- pro/contro rispetto a modificare `combined_text`;
- test previsti;
- impatto su embeddings e clustering.

### Valutare boilerplate, firme e forward headers

Owner proposto: da assegnare
Stream: feature engineering/documentazione
Branch proposta: `feature/email-boilerplate-analysis`

Dipendenze:

- sample processed disponibile;
- policy preprocessing conservativa approvata.

File scrivibili:

- `docs/knowledge/03_cleaning_feature_engineering.md`
- eventuali notebook diagnostici o report, previa approvazione.

Output:

- analisi su frequenza e impatto di boilerplate, firme e forward headers;
- regole candidate di tagging o rimozione;
- rischi informativi;
- raccomandazione prima di eventuali modifiche runtime.

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

### Proposta feature engineering fase 2

Handoff:
Owner: Filippo (Antigravity)
Stream: feature engineering
Branch: `feature/feature-engineering`
PR: N/A (local)
Task: Proposta feature engineering fase 2
File modificati:
- `DECISIONS.md`
- `docs/knowledge/03_cleaning_feature_engineering.md`
Test: Nessun file sorgente modificato, solo update documentale.
Output: Feature ausiliarie proposte, approvate e registrate.
Rischi: Durante l'implementazione andrà aggiornato DATA_CONTRACTS.md.
Prossimo passo: Sviluppo in src/utils/data_processing.py

#### 
### Consolidare task preprocessing

Owner: José (Codex)
Stream: feature engineering/documentazione
Branch: `feature/preprocessing-consolidation`

File modificati:

- `TASK_BOARD.md`
- `DECISIONS.md`
- `docs/knowledge/03_cleaning_feature_engineering.md`

File letti:

- `src/utils/data_processing.py`
- `tests/test_data_processing.py`
- `src/notebooks/data_preprocessing_validation.ipynb`
- `DATA_CONTRACTS.md`

Output:

- confermato che la pipeline preprocessing e' gia' conservativa e testata;
- approvata policy di non rimuovere stop words da `combined_text` per embeddings;
- documentata policy operativa preprocessing;
- proposti sotto-task per colonne ausiliarie e analisi boilerplate/forward headers.

Verifica:

```bash
uv run python -m pytest tests/test_data_processing.py -q
uv run python -m pytest -q
```

Esito:

- `9 passed`
- `17 passed`

Rischi residui:

- eventuali nuove colonne ausiliarie richiederanno aggiornamento di `DATA_CONTRACTS.md`;
- normalizzazioni aggressive devono essere valutate con confronto embeddings/clustering.


### Correggere docstring contaminata in data extraction

Handoff:
Owner: Filippo (Antigravity)
Stream: manutenzione
Branch: `fix/data-extraction-docstring`
PR: N/A (commit locale)
Task: Correggere docstring contaminata in data extraction
File modificati:
- `src/utils/data_extraction.py`
Test: `uv run python -m pytest tests/test_data_extraction.py -q` (Passati)
Output: Docstring corretta
Rischi: Nessuno
Prossimo passo: Commit e push

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
