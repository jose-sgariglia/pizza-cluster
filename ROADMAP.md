# ROADMAP

## Obiettivo

Costruire una pipeline riproducibile per analizzare email e metadata degli Epstein Files tramite preprocessing, embeddings, feature engineering, clustering, validazione, API e demo.

Questo documento e' una proposta di coordinamento. Le decisioni architetturali importanti devono seguire `AGENT.md`: analisi, proposta, vantaggi/svantaggi, approvazione umana, implementazione, test e documentazione.

## Stato attuale

Completato:

- Estrazione raw JMAIL in Parquet.
- Profiling strutturale del dataset.
- Prima pipeline di cleaning e feature engineering conservativa.
- Notebook di validazione preprocessing.
- Ricerca e memo sugli embeddings.
- Pipeline embeddings con `BAAI/bge-small-en-v1.5`.
- Notebook processo embeddings.
- Test unitari di base su utility dati ed embeddings.

In sospeso:

- Chiarire e completare il task TODO sul preprocessing, gia' parzialmente coperto dalla pipeline esistente.
- Estendere feature engineering in modo misurabile.
- Progettare e validare clustering.
- Definire naming/interpretazione cluster.
- Costruire API e demo.

## Roadmap Per Fasi

### Fase 0 - Stabilizzazione Workspace

Obiettivo: rendere la base di lavoro pulita e ripetibile.

Output:

- `requirements.txt` allineato all'ambiente `uv`.
- Test eseguibili con `uv run python -m pytest`.
- Correzione di eventuali contaminazioni documentali o docstring.
- Convenzioni operative per agenti documentate.

Criterio di completamento:

- Test verdi.
- `git status` senza modifiche inattese, salvo artefatti concordati.

### Fase 1 - Preprocessing Consolidato

Obiettivo: chiudere formalmente il task di preprocessing verificando cosa e' gia' implementato e cosa manca.

Output:

- Revisione della pipeline in `src/utils/data_processing.py`.
- Documento aggiornato in `docs/knowledge/03_cleaning_feature_engineering.md`.
- Notebook di validazione aggiornato se necessario.
- TODO aggiornato solo dopo approvazione.

Decisioni da approvare:

- Se aggiungere rimozione stop words o mantenerla fuori dalla pipeline embeddings.
- Se normalizzare email, nomi, forward headers e boilerplate.
- Se separare preprocessing per embeddings da preprocessing per feature statistiche.

### Fase 2 - Feature Engineering

Obiettivo: creare feature interpretabili che aiutino analisi e clustering senza alterare il testo originale.

Candidate feature:

- Percentuale o conteggio stimato di redazioni.
- Lunghezze e densita' testuali.
- Numero destinatari e presenza CC/BCC.
- Feature temporali aggregate.
- Feature su mittenti e partecipanti.
- Indicatori di allegati.

Output:

- Modulo utility esteso o nuovo modulo dedicato, previa approvazione.
- Metadata di validazione.
- Test unitari.
- Documentazione knowledge base.

### Fase 3 - Clustering Sperimentale

Obiettivo: confrontare piu' tecniche di clustering su embeddings e feature derivate.

Candidate tecniche:

- K-Means come baseline semplice.
- DBSCAN/HDBSCAN per cluster density-based e outlier.
- PCA/UMAP per visualizzazione e diagnostica, non come unico criterio decisionale.

Output:

- Script/modulo sperimentale riproducibile.
- Metriche documentate.
- Notebook di validazione.
- Figure e JSON diagnostici.
- Memo con pro/contro e scelta raccomandata.

Decisioni da approvare:

- Algoritmi da provare.
- Metriche principali.
- Uso di riduzione dimensionale prima del clustering.
- Strategia di gestione outlier.

### Fase 4 - Interpretazione Cluster

Obiettivo: dare nomi e spiegazioni ai cluster in modo verificabile.

Candidate tecniche:

- c-TF-IDF per parole chiave per cluster.
- Frequenze termini pulite.
- Campionamento email rappresentative vicino ai centroidi o medoid.
- Analisi metadata per cluster.

Output:

- Report cluster.
- Tabelle parole chiave.
- Esempi email per cluster.
- Documentazione metodologica.

### Fase 5 - API Modello

Obiettivo: esporre cluster, email e metadata tramite API.

Output:

- API minima per lista cluster, dettaglio cluster, email per cluster e metadata.
- Documentazione OpenAPI/Swagger.
- Test API.

Decisioni da approvare:

- Framework API.
- Formato artefatti modello.
- Strategia di caricamento dati.

### Fase 6 - Demo

Obiettivo: creare una demo usabile per esplorare cluster ed email.

Output:

- Interfaccia per selezione cluster.
- Lista email e metadata.
- Vista dettaglio email.
- Istruzioni di esecuzione.

## Strategia Collaborazione Codex + Antigravity

Principio: gli agenti devono lavorare su task indipendenti, con ownership chiara dei file, evitando modifiche parallele sugli stessi moduli.

### Ruoli Proposti

Codex:

- Coordinamento roadmap e vincoli di progetto.
- Moduli core in `src/utils`.
- Test e validazione locale.
- Aggiornamento `Diary.md`, `TODO.md` e knowledge base.

Antigravity:

- Notebook, report e visualizzazioni.
- Analisi esplorative su output gia' prodotti.
- Proposte di feature o metriche documentate.
- Demo/API quando il contratto dati e' stabile.

Questa divisione puo' cambiare, ma ogni cambio deve essere annotato nel diario o in un file di coordinamento.

### Regole Di Parallelizzazione

Task parallelizzabili:

- Un agente lavora su modulo utility, l'altro su notebook che consuma output gia' stabile.
- Un agente prepara documentazione knowledge base, l'altro implementa test su una funzione gia' definita.
- Un agente esplora metriche, l'altro sistema packaging/test environment.
- Un agente lavora su API, l'altro su demo, solo dopo contratto dati approvato.

Task non parallelizzabili senza coordinamento:

- Due agenti sullo stesso file Python.
- Due agenti su `TODO.md` o `Diary.md`.
- Modifiche contemporanee a schema dati, nomi colonne o path `.env`.
- Refactor che spostano moduli o cambiano contratti pubblici.

### Protocollo Prima Di Ogni Task

Ogni task dovrebbe dichiarare:

- Obiettivo.
- File ownership.
- Input attesi.
- Output attesi.
- Test da eseguire.
- Documentazione da aggiornare.
- Dipendenze da altri task.

Esempio:

```md
Task: aggiungere feature redaction_ratio
Owner: Codex
File ownership: src/utils/data_processing.py, tests/test_data_processing.py, docs/knowledge/03_cleaning_feature_engineering.md
Input: processed/raw dataframe esistente
Output: nuova colonna redaction_ratio e metadata aggiornati
Test: uv run python -m pytest tests/test_data_processing.py -q
Dipendenze: nessuna
```

### Protocollo Di Handoff

Quando un agente termina:

- Riassume modifiche.
- Elenca file toccati.
- Riporta comandi di test eseguiti.
- Dichiara rischi o parti non verificate.
- Aggiorna il diario se la modifica e' significativa.

## File Markdown Consigliati

Consiglio di aggiungere questi file, ma non li creo finche' non vengono approvati.

### `AGENTS_COLLABORATION.md`

Scopo: regole condivise tra Codex e Antigravity.

Contenuto:

- Ruoli.
- Regole di ownership file.
- Protocollo di handoff.
- Convenzioni per test e documentazione.
- Come gestire conflitti.

Pro:

- Riduce conflitti tra agenti.
- Evita decisioni implicite.
- Rende piu' chiaro chi fa cosa.

Contro:

- Un file in piu' da mantenere aggiornato.

### `TASK_BOARD.md`

Scopo: task board leggera in Markdown.

Contenuto:

- Backlog.
- Ready.
- In progress.
- Blocked.
- Done.
- Owner e file ownership per task.

Pro:

- Migliora parallelizzazione.
- Evita che due agenti lavorino sullo stesso file.

Contro:

- Duplica parzialmente `TODO.md` se non definiamo bene la differenza.

Proposta di separazione:

- `TODO.md`: obiettivi funzionali di progetto.
- `TASK_BOARD.md`: pianificazione operativa giornaliera per agenti.

### `DECISIONS.md`

Scopo: registro decisioni tecniche approvate.

Contenuto:

- Data.
- Decisione.
- Alternative considerate.
- Pro.
- Contro.
- Motivazione.
- Impatto sui file o pipeline.

Pro:

- Evita di ridiscutere scelte gia' approvate.
- Utile per clustering, API, metriche e modelli.

Contro:

- Richiede disciplina: ogni decisione importante va registrata.

### `DATA_CONTRACTS.md`

Scopo: definire contratti dati tra fasi pipeline.

Contenuto:

- Path input/output.
- Colonne richieste.
- Colonne prodotte.
- Tipi dati.
- Regole su valori nulli.
- Versione artefatti.

Pro:

- Permette lavoro parallelo tra API, demo, clustering e notebook.
- Riduce rotture quando cambia una colonna.

Contro:

- Va aggiornato a ogni cambio schema.

## Procedura Raccomandata

1. Mantenere `ROADMAP.md` come visione di medio periodo.
2. Creare `AGENTS_COLLABORATION.md` per le regole tra agenti.
3. Creare `TASK_BOARD.md` per il lavoro operativo giornaliero.
4. Creare `DECISIONS.md` appena iniziano scelte su clustering, feature o API.
5. Creare `DATA_CONTRACTS.md` prima che API/demo consumino output di clustering.
6. Prima di iniziare una task, assegnare owner e file ownership.
7. Alla fine di ogni task, aggiornare test, documentazione e handoff.

## Prossime Azioni Proposte

1. Correggere la docstring contaminata in `src/utils/data_extraction.py`.
2. Creare `AGENTS_COLLABORATION.md`.
3. Creare `TASK_BOARD.md` con i task immediati.
4. Decidere se chiudere il TODO sul preprocessing o trasformarlo in sotto-task piu' specifici.
