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
- Normalizzare subito email, nomi, forward headers e boilerplate email dentro `combined_text`.
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

## 2026-06-01 - Gestione recipient sconosciuti e marker [redacted]

Stato: Approved

Contesto:

Durante la validazione di `recipient_count_estimate`, il notebook di preprocessing ha mostrato valori nulli nella feature e destinatari raw presenti in formati JSON-like. L'utente ha inoltre rilevato che in email come `EFTA00552880` alcune redazioni compaiono come `[redacted]`.

Decisione:

- Correggere il calcolo di `recipient_count_estimate` per preservare l'indice dopo i filtri e non produrre null artificiali.
- Se una riga non contiene nessun destinatario utilizzabile in `to_recipients`, `cc_recipients` o `bcc_recipients`, impostare `to_recipients` a `Unknown`.
- Aggiungere `person_unknown` per tracciare le righe in cui il destinatario e' sconosciuto/censurato.
- Rilevare esplicitamente `[redacted]` come marker di redazione.
- Chiarire che `person_unknown` non identifica recipient potenzialmente censurati dentro campi recipient gia' valorizzati; per quel caso servirebbe una feature distinta.

Alternative considerate:

- Lasciare `recipient_count_estimate` nullable e documentare solo il limite.
- Sostituire ogni campo recipient vuoto con `Unknown`, incluso CC/BCC.
- Non aggiungere una feature dedicata per recipient sconosciuti.

Pro:

- Rende `recipient_count_estimate` utilizzabile senza null artificiali.
- Mantiene separata l'informazione di persona sconosciuta tramite `person_unknown`.
- Evita di trasformare CC/BCC vuoti in falsi unknown.
- Migliora la copertura del rilevamento redazioni.

Contro:

- `recipient_count_estimate` resta una stima euristica, non un conteggio anagrafico certificato.
- `Unknown` rappresenta informazione assente/censurata, non una persona identificabile.
- Nel sample corrente `person_unknown` puo' risultare tutto `False` se ogni riga ha almeno un recipient utilizzabile.

Impatto:

- Cambia schema processed aggiungendo `person_unknown`.
- Aggiorna la garanzia di `recipient_count_estimate`: non nullo nelle righe finali.
- Richiede rigenerazione degli artefatti processed.
- Aggiorna test, notebook preprocessing e `DATA_CONTRACTS.md`.

File o artefatti coinvolti:

- `src/utils/data_processing.py`
- `tests/test_data_processing.py`
- `src/notebooks/data_preprocessing_validation.ipynb`
- `DATA_CONTRACTS.md`
- `docs/knowledge/03_cleaning_feature_engineering.md`

Approvazione:

- Approvata dall'utente il 2026-06-01 dopo revisione del notebook diagnostico.

## 2026-06-03 - Grafici robusti nei notebook diagnostici

Stato: Approved

Contesto:
Durante la generazione di embeddings multi-modello, l'istogramma delle norme L2 nel notebook `embedding_process.ipynb` ha generato un `ValueError` in quanto le norme erano tutte identiche (1.0) a causa della normalizzazione L2, rendendo impossibile la creazione di 30 bin finiti.

Decisione:
Implementare una logica di plotting robusta che verifichi se il range dei dati è nullo prima di definire il numero di bin. In caso di dati costanti, usare 1 solo bin.

Alternative considerate:
- Rimuovere il grafico delle norme.
- Disabilitare la normalizzazione (scartata per coerenza pipeline).

Pro:
- Evita crash del notebook.
- Gestisce correttamente embeddings normalizzati.

Contro:
- Aggiunge logica condizionale nel notebook.

Impatto:
- Modifica a `src/notebooks/embedding_process.ipynb`.

File o artefatti coinvolti:
- `src/notebooks/embedding_process.ipynb`

Approvazione:
- Approvata dall'utente il 2026-06-03.

## 2026-06-04 - Selezione di bge-small-en-v1.5 come modello di embedding ufficiale

Stato: Approved

Contesto:

Durante la fase di confronto multi-modello in `embedding_model_comparison.ipynb`, sono stati valutati `all-MiniLM-L6-v2` (384d), `BAAI/bge-small-en-v1.5` (384d) e `intfloat/e5-base-v2` (768d) sull'intero dataset di ~42.000 email tramite K-Means.

Decisione:

Selezionare `BAAI/bge-small-en-v1.5` come modello principale di embedding per il progetto.

Alternative considerate:

- `all-MiniLM-L6-v2`: Scartato per alta instabilità dei cluster (Silhouette picco a K=3 con estrema varianza ARI/NMI in bootstrap).
- `intfloat/e5-base-v2`: Scartato nonostante l'alta stabilità perché, a parità di risoluzione ottimale (K=15), ha ottenuto un Silhouette Score leggermente inferiore rispetto a BGE e richiede il doppio delle dimensioni (768 vs 384), incrementando notevolmente i costi computazionali.

Pro:

- Ottima stabilità dei cluster (bassa deviazione standard per ARI e NMI in bootstrap).
- Miglior Silhouette Score a parità di risoluzione K=15.
- Efficienza computazionale (384 dimensioni), che ottimizza tempi di elaborazione e storage su disco.

Contro:

- Rischio teorico di perdere marginalmente sfumature semantiche in task di Information Retrieval estremamente complessi rispetto a modelli "base".

Impatto:

- `BAAI/bge-small-en-v1.5` verrà utilizzato come standard per le prossime fasi della pipeline.
- Nuova documentazione aggiunta al progetto in docs/knowledge.

File o artefatti coinvolti:

- `src/notebooks/embedding_model_comparison.ipynb`
- `TASK_BOARD.md`
- `docs/knowledge/06_embedding_resolution_and_k_selection.md`

Approvazione:

- Approvata dall'utente il 2026-06-04.

## 2026-06-05 - Pipeline UMAP + HDBSCAN e Grid Search

Stato: Approved

Contesto:

L'applicazione diretta di HDBSCAN su 42.000 embeddings a 384 dimensioni richiedeva tempi di esecuzione inaccettabili (oltre 10 minuti per run), rendendo impraticabile il tuning dei parametri e l'esplorazione del modello.

Decisione:

1. Reintegrare UMAP per ridurre la dimensionalità a 15 (utilizzando metrica `cosine` per preservare la topologia originale).
2. Eseguire una Grid Search sistematica per ottimizzare i parametri di HDBSCAN sui vettori ridotti.
3. Parametri finali scelti tramite Grid Search (Scelta 9): `min_cluster_size` = 200, `min_samples` = 10.
   Questa configurazione bilancia i macro-cluster (40 identificati) con un tasso di rumore accettabile per l'information retrieval (41.11%).

Alternative considerate:

- HDBSCAN diretto (euclidean): Scartato per i colli di bottiglia computazionali eccessivi.

Impatto:

- Pipeline ottimizzata che gira in pochi secondi.
- `src/utils/clustering_hdbscan.py` aggiornato per includere la logica UMAP.
- Nuovo notebook `src/notebooks/clustering_hdbscan_experiment.ipynb` creato per la Grid Search automatizzata.

File o artefatti coinvolti:

- `src/notebooks/clustering_hdbscan_experiment.ipynb`
- `src/notebooks/clustering_umap_hdbscan.ipynb`
- `src/utils/clustering_hdbscan.py`

Approvazione:

- Approvata dall'utente il 2026-06-05.

## 2026-06-17 - Esportazione Dataset Etichettato (Clustered Emails)

Stato: Approved

Contesto:

L'utente ha richiesto la creazione di un file `.parquet` alla fine della pipeline che contenga tutti i dati etichettati con il cluster di appartenenza e il nome del cluster generato dall'LLM.

Decisione:

Standardizzare l'output finale della pipeline di orchestrazione nel file `data/processed/jmail_emails_clustered.parquet`. Questo file includerà tutte le colonne del dataset processato più le label del clustering e i nomi descrittivi.

Alternative considerate:

- Salvare solo una mappatura ID -> Cluster (scartato per scomodità d'uso downstream).
- Usare CSV (scartato per perdita di tipi e inefficienza).

Pro:

- Dataset "chiavi in mano" per visualizzazioni e API.
- Preservazione dei nomi generati dall'LLM direttamente nel dato.
- Facile integrazione con strumenti di BI o altri notebook.

Contro:

- Duplicazione parziale dei dati (il file clustered è una copia del processed con colonne extra).

Impatto:

- Aggiornamento di `src/notebooks/full_pipeline_orchestration.ipynb`.
- Aggiornamento di `DATA_CONTRACTS.md`.

File o artefatti coinvolti:

- `src/notebooks/full_pipeline_orchestration.ipynb`
- `data/processed/jmail_emails_clustered.parquet`

Approvazione:

- Approvata dall'utente il 2026-06-17.
