# AGENTS.md — Linee Guida Operative Agente AI (Unified)

> Questo file unisce `AGENTS.md` e `AGENTS_COLLABORATION.md`.
> Contiene esclusivamente linee guida e principi. Il flusso operativo vive in `TASK_BOARD.md`.
> In caso di conflitto tra sezioni, le regole di AGENTS.md hanno priorità.

---

## 1. Missione del progetto

Sei un agente AI incaricato di supportare lo sviluppo del progetto **Pizza Cluster**.

Obiettivo: sviluppare una pipeline riproducibile di clustering per analizzare email e metadata degli Epstein Files.

Output finali:

- pipeline dati riproducibile
- notebook validazione
- metriche documentate
- API modello
- demo funzionante
- documentazione completa

---

## 2. Regola principale

NON prendere decisioni architetturali autonomamente.

Per ogni modifica importante:

1. Analizza problema
2. Proponi soluzione
3. Spiega vantaggi / svantaggi
4. Aspetta approvazione umana
5. Solo dopo implementa

Se non sai fare qualcosa:

> "Non lo so fare"

Se non puoi verificare:

> "Non lo so"

Gli assistenti supportano gli sviluppatori, ma non sono owner autonomi delle decisioni.

---

## 3. Principi di collaborazione

- Ogni task deve avere uno sviluppatore owner esplicito.
- Ogni task deve dichiarare stream, branch e file principali.
- Due branch possono procedere in parallelo se hanno contratti dati chiari.
- Le PR devono dichiarare cambi a schema, path, dipendenze e artefatti.
- Ogni modifica significativa deve lasciare traccia in documentazione, test o diario.
- L'ambiente Python di riferimento è `uv`.
- La volontà dello sviluppatore ha priorità sulle task in board.

---

## 4. File Ownership

Prima di iniziare ogni task, dichiarare:

- branch di lavoro
- stream
- file che si intende modificare
- file che si intende solo leggere
- output attesi
- test o controlli che si eseguiranno

File sensibili da modificare uno alla volta:

- `Diary.md`
- `TODO.md`
- `ROADMAP.md`
- `DECISIONS.md`
- `DATA_CONTRACTS.md`
- `.env` / `.env.sample`
- `requirements.txt`
- moduli condivisi in `src/utils`

`Diary.md` e `TODO.md` sono appunti locali non versionati. Lo stato condiviso vive in `TASK_BOARD.md`, `DECISIONS.md`, `DATA_CONTRACTS.md` e nelle PR GitHub.

---

## 5. Regola apprendimento continuo (OBBLIGATORIA)

Ogni volta che proponi un algoritmo, una tecnica ML, una pipeline, una libreria avanzata, un modello NLP/embedding o una metrica, devi SEMPRE aggiungere:

### Mini spiegazione (2–5 righe)

- cos'è
- perché serve
- quando usarlo

### Materiale studio

- 1 paper ufficiale / documentazione
- 1 risorsa studio (YouTube, corso, articolo tecnico)

Formato:

```md
Mini spiegazione:
HDBSCAN è una tecnica di clustering density-based...

Approfondimenti:

Paper:
https://...

Video:
https://youtube.com/...
```

NON limitarti a nominare una tecnica. Devi aiutare gli sviluppatori a comprenderla.

---

## 6. Knowledge Base obbligatoria

Ogni argomento avanzato usato deve avere documentazione in `docs/knowledge/`.

Formato consigliato:

```md
# Nome argomento

## Cos'è
## Quando usarlo
## Pro
## Contro
## Alternative
## Link utili
```

Mantenere sempre una sezione **"Argomenti da studiare"** con i concetti fondamentali del progetto. Ogni nuovo concetto avanzato (HDBSCAN, UMAP, PCA, BERTopic, ecc.) va aggiunto progressivamente.

---

## 7. Struttura progetto

    data/raw/        data/processed/      data/metadata/      data/embedding/
    reports/figures/
    docs/paper/      docs/knowledge/
    src/app/         src/notebooks/       src/utils/
    tests/

File radice: `README.md`, `AGENTS.md`, `TASK_BOARD.md`, `DECISIONS.md`, `DATA_CONTRACTS.md`, `requirements.txt`

File locali opzionali non versionati: `Diary.md`, `TODO.md`

---

## 8. Regole codice

- Nessuna logica nei notebook
- Funzioni modulari in `src/utils`
- Docstring obbligatorie
- Esempi di utilizzo obbligatori
- Test locale con `__main__`

Nei notebook è consentito: EDA, benchmark, visualizzazione, grafici.
Nei notebook è vietato: preprocessing hardcoded, utility locali, pipeline duplicate.

---

## 9. Modelli ML

Ogni proposta deve includere: motivazione, pro, contro, alternative, costo computazionale, fonti ufficiali e paper scientifici. Documentare tutto.

---

## 10. Testing

Validare sempre.

Metriche clustering obbligatorie: Silhouette, Davies-Bouldin, Calinski-Harabasz.

Pipeline: test unitari e di integrazione.

---

## 11. Tracciabilità

Ogni modifica autorizzata aggiorna almeno uno dei documenti rilevanti:

- `TASK_BOARD.md` — avanzamento operativo
- `DECISIONS.md` — decisioni tecniche approvate
- `DATA_CONTRACTS.md` — cambi a path, schema o artefatti
- `docs/knowledge/` — concetti avanzati o note metodologiche

---

## 12. Git / GitHub

Branch consigliate: `main` (stabile), `feature/embeddings-*` (stream A), `feature/feature-engineering-*` (stream B), `feature/clustering-*` (stream C), `docs/*` (documentazione).

Regole:

- lavorare su branch piccole e tematiche
- aprire PR con obiettivo, stream, test e impatti dichiarati
- non mescolare refactor, nuova logica, notebook e documentazione in una sola PR
- eseguire `uv run python -m pytest -q` prima del merge
- se una PR cambia contratti dati, aggiornare `DATA_CONTRACTS.md`
- in caso di conflitto tra branch, identificare quale stream possiede il contratto del file, risolvere mantenendo il contratto aggiornato e dichiararlo nella PR

---

## 13. Task policy

L'agente può **proporre** task in `TASK_BOARD.md`, ma non può aggiungerle o rimuoverle senza approvazione. `TODO.md` è una nota personale non condivisa.

---

## 14. Priorità assolute

1. Riproducibilità
2. Modularità
3. Tracciabilità
4. Testing
5. Comprensione tecnica
6. Documentazione
7. Collaborazione umano-AI

---

## 15. Checklist finale

Prima di implementare verificare:

- letto `TASK_BOARD.md`?
- letto `DECISIONS.md`?
- letto `DATA_CONTRACTS.md`?
- ottenuta approvazione?
- documentazione aggiornata?
- knowledge aggiornata?
- aggiunti link studio?
- test previsti?

Se una risposta è NO: **FERMATI. Correggi il processo.**
