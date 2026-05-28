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

## Strategia Collaborazione Sviluppatori + Assistenti

Scenario reale: due sviluppatori lavorano in modo asincrono sullo stesso progetto Git/GitHub. Uno usa Codex, l'altro usa Antigravity. Gli assistenti non sono owner autonomi del progetto: aiutano i rispettivi sviluppatori a portare avanti stream di lavoro separati, che devono poi ricongiungersi tramite branch, pull request, review e merge.

Principio: dividere il lavoro per stream funzionali indipendenti, non per singola sessione locale. Ogni stream deve avere branch dedicata, output chiari e un punto di integrazione concordato.

### Stream Proposti

Stream A - Embeddings, studio e analisi

Owner proposto: sviluppatore con Codex.

Responsabilita':

- Ricerca modelli embedding.
- Pipeline embeddings.
- Confronto tra embeddings baseline e embeddings generati dopo feature engineering/preprocessing piu' raffinato.
- Analisi metriche sugli embeddings.
- Documentazione metodologica su modelli, parametri e tradeoff.

File probabili:

- `src/utils/embedding_pipeline.py`
- `tests/test_embedding_pipeline.py`
- `docs/embedding_research/`
- `docs/knowledge/04_embedding_strategy_memo.md`
- notebook/report legati agli embeddings.

Stream B - Feature engineering, estrazione feature e documentazione

Owner proposto: sviluppatore con Antigravity.

Responsabilita':

- Feature engineering testuale e metadata.
- Miglioramento preprocessing conservativo.
- Estrazione feature statistiche e interpretabili.
- Miglioramento documentazione contenutistica.
- Aggiornamento contratti dati processed/features.

File probabili:

- `src/utils/data_processing.py`
- eventuale nuovo modulo feature, se approvato.
- `tests/test_data_processing.py`
- `docs/knowledge/03_cleaning_feature_engineering.md`
- `DATA_CONTRACTS.md`

Stream C - Integrazione clustering

Owner: da assegnare dopo merge degli stream A e B.

Responsabilita':

- Usare embeddings e feature stabili.
- Confrontare clustering su dati baseline e dati arricchiti.
- Valutare metriche e interpretabilita'.
- Proporre il modello candidato.

### Punto Di Ricongiungimento A/B

Gli stream A e B possono procedere in parallelo fino a quando:

- lo stream embeddings produce una baseline riproducibile;
- lo stream feature engineering produce un dataset processed/features stabile;
- `DATA_CONTRACTS.md` descrive chiaramente colonne e path;
- entrambi gli stream hanno test verdi.

Dopo il ricongiungimento:

1. mergiare feature engineering su branch di integrazione;
2. rigenerare embeddings sul dataset arricchito;
3. confrontare embeddings baseline vs embeddings post-feature/preprocessing;
4. documentare differenze e impatto;
5. solo dopo avviare clustering sperimentale.

### Strategia Git/GitHub

Branch consigliate:

- `main`: stato stabile.
- `develop` o `integration`: branch di integrazione, se il progetto vuole separare lavoro stabile da lavoro in corso.
- `feature/embeddings-*`: lavoro stream A.
- `feature/feature-engineering-*`: lavoro stream B.
- `feature/clustering-*`: lavoro dopo ricongiungimento.
- `docs/*`: documentazione trasversale, quando non legata a una feature.

Regole pratiche:

- Ogni stream lavora su branch propria.
- Prima di iniziare: `git fetch` e branch aggiornata dalla base concordata.
- Prima di aprire PR: rebase o merge dalla base concordata, test con `uv run python -m pytest -q`.
- Ogni PR deve dichiarare quali contratti dati cambia.
- Evitare PR grandi che mescolano pipeline, notebook, documentazione e refactor non necessari.
- Le modifiche a `DATA_CONTRACTS.md`, `.env.sample`, `requirements.txt`, `TODO.md` e `Diary.md` vanno trattate come punti di coordinamento.

### Pull Request E Review

Ogni PR dovrebbe includere:

- obiettivo;
- branch base;
- stream di appartenenza;
- file principali toccati;
- test eseguiti;
- artefatti prodotti;
- cambi a schema dati o path;
- note per lo sviluppatore dell'altro stream.

Una PR dello stream A non deve richiedere dettagli interni dello stream B, ma deve indicare quali input si aspetta. Una PR dello stream B non deve rigenerare embeddings, ma deve rendere chiaro quando gli embeddings vanno rigenerati.

### Task Parallelizzabili

Parallelizzabili:

- embeddings baseline mentre feature engineering evolve;
- documentazione feature mentre embeddings vengono testati;
- ricerca modelli embedding mentre si definiscono feature metadata;
- notebook diagnostici su sample gia' prodotti;
- definizione contratti dati mentre si completano test dei moduli.

Da serializzare o integrare con attenzione:

- cambio schema `processed`;
- cambio colonna usata come input embedding;
- introduzione di nuove dipendenze pesanti;
- refactor di path `.env`;
- clustering finale;
- API/demo che dipendono dagli output del clustering.

## File Markdown Di Coordinamento

Questi file servono a coordinare il lavoro asincrono tra sviluppatori e assistenti.

### `AGENTS_COLLABORATION.md`

Scopo: regole condivise tra gli sviluppatori che usano Codex e Antigravity.

Contenuto:

- Stream di lavoro.
- Regole Git/GitHub.
- Regole di ownership per branch e file.
- Protocollo di handoff.
- Convenzioni per test e documentazione.
- Come gestire conflitti.

Pro:

- Riduce conflitti tra branch.
- Evita decisioni implicite.
- Rende piu' chiaro chi fa cosa e quando integrare.

Contro:

- Un file in piu' da mantenere aggiornato.

### `TASK_BOARD.md`

Scopo: task board leggera in Markdown per coordinare lavoro asincrono.

Contenuto:

- Backlog.
- Ready.
- In progress.
- Blocked.
- Done.
- Owner, branch, stream e file ownership per task.

Pro:

- Migliora parallelizzazione.
- Evita che due sviluppatori aprano PR incompatibili.

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
2. Usare `AGENTS_COLLABORATION.md` per regole tra sviluppatori, assistenti e branch.
3. Usare `TASK_BOARD.md` per task operativi, stream, branch e owner.
4. Usare `DECISIONS.md` per scelte tecniche approvate.
5. Usare `DATA_CONTRACTS.md` per stabilizzare input/output tra stream.
6. Prima di iniziare una task, dichiarare stream, branch, owner e file ownership.
7. Alla fine di ogni PR, aggiornare test, documentazione e handoff.

## Prossime Azioni Proposte

1. Correggere la docstring contaminata in `src/utils/data_extraction.py`.
2. Allineare `AGENTS_COLLABORATION.md` e `TASK_BOARD.md` allo scenario Git/GitHub asincrono.
3. Definire branch base di lavoro: `main` diretto o branch `develop/integration`.
4. Assegnare formalmente stream A embeddings e stream B feature engineering.
5. Decidere se chiudere il TODO sul preprocessing o trasformarlo in sotto-task piu' specifici.
