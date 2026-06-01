# DECISIONS

## Scopo

Registro delle decisioni tecniche approvate per Pizza Cluster.

Questo file evita di ridiscutere scelte gia' valutate e rende espliciti compromessi, alternative e impatti. Le nuove decisioni devono rispettare il workflow di `AGENT.md`: analisi, proposta, vantaggi/svantaggi, approvazione umana, implementazione.

## Template

```md
## YYYY-MM-DD - Titolo decisione

Stato: Proposed | Approved | Rejected | Superseded

Contesto:

Decisione:

Alternative considerate:

Pro:

Contro:

Impatto:

File o artefatti coinvolti:

Approvazione:
```

## 2026-05-27 - Usare uv come ambiente Python operativo

Stato: Approved

Contesto:

Il progetto usa un ambiente locale gestito tramite `uv`. I test devono essere eseguiti nello stesso ambiente usato per installare dipendenze.

Decisione:

Usare `uv` per installare dipendenze ed eseguire comandi Python.

Alternative considerate:

- Python di sistema.
- `.venv/bin/python` invocato direttamente.

Pro:

- Ambiente coerente.
- Dipendenze installate con un solo strumento.
- Comandi riproducibili tra agenti.

Contro:

- Richiede che ogni agente usi esplicitamente `uv`.

Impatto:

- Installazioni tramite `uv pip install`.
- Test tramite `uv run python -m pytest -q`.

File o artefatti coinvolti:

- `requirements.txt`
- `AGENTS_COLLABORATION.md`

Approvazione:

- Richiesta esplicita dell'utente del 2026-05-27.

## 2026-05-28 - Non rimuovere stop words da combined_text embeddings

Stato: Approved

Contesto:

`combined_text` e' l'input della pipeline embeddings baseline. Il TODO storico citava rimozione stop words e normalizzazione testuale, ma la pipeline attuale usa un cleaning conservativo: normalizzazione whitespace, preservazione delle redazioni e nessuna rimozione di token informativi.

Decisione:

Non rimuovere stop words da `combined_text` usato per sentence embeddings. Eventuali trasformazioni piu' aggressive saranno valutate come colonne ausiliarie per feature statistiche o analisi interpretabili, non come sostituzione implicita dell'input embeddings.

Alternative considerate:

- Rimuovere stop words direttamente da `combined_text`.
- Normalizzare subito email, nomi, forward headers e boilerplate dentro `combined_text`.
- Creare un secondo campo testuale per feature statistiche.
- Mantenere solo la pipeline corrente senza decisione esplicita.

Pro:

- Preserva contesto sintattico e semantico utile ai sentence embeddings.
- Mantiene confrontabile la baseline embeddings gia' prodotta.
- Evita rigenerazioni non controllate degli embeddings.
- Permette feature interpretabili separate in task successivi.

Contro:

- Non riduce rumore lessicale nel campo embeddings.
- Lascia ancora da valutare firme, forward headers e boilerplate email.
- Richiede task successivi se servono feature statistiche piu' pulite.

Impatto:

- Nessun cambio schema immediato.
- Nessun cambio agli embeddings gia' generati.
- `src/utils/data_processing.py` resta invariato.
- La policy preprocessing viene documentata in knowledge base.
- Nuove colonne ausiliarie future richiederanno proposta e aggiornamento di `DATA_CONTRACTS.md`.

File o artefatti coinvolti:

- `src/utils/data_processing.py`
- `docs/knowledge/03_cleaning_feature_engineering.md`
- `DATA_CONTRACTS.md`
- `data/embeddings/email_embeddings.npy`

Approvazione:

- Approvata dall'utente il 2026-05-28 dopo proposta di medio termine su branch `feature/preprocessing-consolidation`.

## 2026-05-28 - Approvazione Feature Engineering Fase 2

Stato: Approved

Contesto:

Per migliorare l'interpretabilita' dei cluster e fornire meta-dati utili all'analisi senza inquinare il campo semantico usato per gli embeddings (`combined_text`), e' necessario aggiungere feature numeriche, temporali e di network.

Decisione:

Implementare le seguenti feature ausiliarie: `redaction_count`, `word_count`, `uppercase_ratio`, `sent_hour`, `is_weekend`, `sender_domain`, `is_epstein_involved`, `attachment_count`. Queste andranno ad arricchire il dataset elaborato.

Alternative considerate:

- Mantenere solo le feature attuali.
- Aggiungere il testo di queste feature nel body dell'email (scartato per non alterare la semantica).

Pro:

- Aggiunge metriche quantitative potenti (ore di invio, domini, conteggio esatto file/redazioni) per la profilazione dei cluster.
- Nessun impatto distruttivo su `combined_text`.

Contro:

- Aumenta il numero di colonne del dataset elaborato.
- Richiede funzioni di parsing dedicate.

Impatto:

- Saranno introdotte nuove funzioni in `src/utils/data_processing.py`.
- `DATA_CONTRACTS.md` dovra' essere aggiornato durante l'implementazione.

File o artefatti coinvolti:

- `docs/knowledge/03_cleaning_feature_engineering.md`
- `DECISIONS.md`

Approvazione:

- Approvata dall'utente il 2026-05-28.
