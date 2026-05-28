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

