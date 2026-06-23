# PROMPT: Pipeline finale "Pizza Cluster" (training completo su 1.700.000 campioni)

> Questo prompt è destinato a un agente che opera già sotto `AGENTS.md`. Tutte le regole di `AGENTS.md` restano valide e prevalgono. Questo prompt **specializza** il lavoro, non lo deroga.

---

## OBIETTIVO
Produrre il flusso end-to-end della pipeline (estrazione dati raw → creazione label) orchestrato da **un notebook in `src/notebooks/`**, da scrivere ORA in locale ed eseguire DOMANI sul server del laboratorio.

---

## VINCOLO ARCHITETTURALE DA CHIARIRE PRIMA DI TUTTO (sez. 2 + 8 di AGENTS)
`AGENTS.md` §8 vieta logica nei notebook (solo EDA/benchmark/visualizzazione/grafici); la logica va in `src/utils`. Una "pipeline tutta nel notebook" viola questa regola.
**Non decidere da solo.** Proponi e fai scegliere allo sviluppatore tra:
- **A (conforme):** logica in `src/utils` (consolidando ciò che oggi è nei notebook sperimentali, come refactor approvato e PR separata); il notebook è un **orchestratore sottile** che importa le funzioni e produce grafici/metriche.
- **B (deroga):** logica inline nel notebook, registrata come eccezione esplicita in `DECISIONS.md`.
Attendi la decisione prima di scrivere qualsiasi codice.

---

## FASE 0 — PROPOSTA E APPROVAZIONE (obbligatoria, sez. 2 + 15)
Prima di implementare, presenta una proposta e **attendi approvazione**. La proposta deve contenere:
1. **Mappatura "fonte di verità"**: per ogni fase, file/funzione canonica da riusare + elenco esplicito dei notebook sperimentali **da IGNORARE**.
2. **Scelte tecniche di scala** (vedi sotto) come proposte con pro/contro: dimensioni sottocampioni, obiettivo e budget di Optuna, strategia GPU/CPU.
3. **Cambi di contratto** da autorizzare e registrare in `DATA_CONTRACTS.md`: nuova colonna etichette, nuovo path `data/validation/`, artefatto embeddings, nuove figure.
4. **Decomposizione in PR** (sez. 12): refactor `src/utils`, notebook orchestratore, knowledge docs e documentazione **in PR separate**.
5. **Dichiarazione di ownership** (sez. 4): branch, stream, file da modificare / da sola lettura, output attesi, test previsti.

### Fonte di verità (da compilare con lo sviluppatore)
| Fase | File/funzione canonica in `src/utils` (o da consolidare)                   | Sperimentali da IGNORARE                                        |
|------|----------------------------------------------------------------------------|-----------------------------------------------------------------|
| Preprocessing | pipeline_processing.ipynb                                                  | feature_engineering.ipynb                                       |
| Embedding | embedding_pipeline.py, final_embedding_validation.ipynb                    | Tutti i file contenenti altri informazioni riguardo agli embedding |
| Clustering | clustering_optuna_tuning.ipynb, clustering_umap_hdbscan_thread_aware.ipynd | Tutti i file contenenti altri informazioni riguardo i cluter    |
| Labelling | llm_cluster_naming_experiment.ipynb                                        |                                                   |

---

## MODALITÀ DI LAVORO (authoring locale → esecuzione in lab, transfer solo via GitHub)
- Scrittura ora in locale; esecuzione domani sul server del lab; trasferimento **solo via GitHub**.
- In locale **non è eseguibile** la pipeline completa sui 1.7M campioni. Il notebook deve quindi essere robusto "alla cieca":
  - **Auto-detect hardware A RUNTIME**: cella iniziale che rileva GPU/VRAM/RAM/core sul server e sceglie da sola il percorso, dimensionando i sottocampioni sulla RAM rilevata.
  - **GPU opportunistica, mai obbligatoria**: `try import cuml/RAPIDS` → fallback CPU (`umap-learn`, `hdbscan`) con sottocampione. Nessuna dipendenza hard da cuML.
  - **`DEV_MODE` (smoke test = integration test, sez. 10)**: flag che esegue l'INTERA pipeline su un campione minuscolo (es. 1.000 mail). Da lanciare ora in locale e come prima cosa in lab. Solo se passa, si flippa a `FULL`.
  - **Transfer via GitHub**: `.gitignore` per `data/`, `reports/figures/`, cache e pesi (embeddings ~2.6GB e 1.7M campioni NON in git: scaricati/generati sul server). Install via **`uv`** (sez. 3); test con `uv run python -m pytest -q`.
- **Validazione pre-lab obbligatoria**: dopo la generazione, eseguire il notebook in `DEV_MODE` su un piccolo campione locale per intercettare errori di import/glue prima del commit.

---

## VINCOLI GLOBALI
**Scala (1.7M):** ogni operazione O(n²) o che renderizza tutti i punti **deve** usare un sottocampione con seed fisso:
- Silhouette/metriche pesanti → campione (es. 20–50k).
- Scatter 2D/3D → `datashader` o sottocampione (es. 50–100k).
- UMAP/HDBSCAN → cuML su GPU se presente, altrimenti sottocampione.

**Checkpointing (obbligatorio):** ogni fase salva i propri artefatti e li riusa se presenti (skip ricalcolo). `parquet` per i dataframe, `.npy`/FAISS per gli embedding (in `data/embedding/`), `joblib` per i modelli.

**Riproducibilità (priorità #1 AGENTS):** `SEED` globale unico usato ovunque (incluse le 100 mail della validazione).

**Apprendimento continuo (sez. 5-6, OBBLIGATORIO):** per OGNI tecnica/algoritmo/libreria/metrica introdotta (UMAP, HDBSCAN, Optuna+CMA-ES, DBCV, MiniBatchKMeans, c-TF-IDF, YAKE, TextRank, KeyBERT, datashader, cuML, soft-clustering, BGE, FAISS…) aggiungere mini-spiegazione (cos'è/perché/quando) + 1 paper + 1 risorsa video/corso, e una scheda in `docs/knowledge/{argomento}.md` (Cos'è/Quando usarlo/Pro/Contro/Alternative/Link). Non limitarsi a nominarla.

**Tracciabilità (sez. 11):** aggiornare `TASK_BOARD.md` (avanzamento; solo proporre task, non aggiungere senza ok), `DECISIONS.md` (scelte approvate), `DATA_CONTRACTS.md` (path/schema/artefatti).

**Output grafici:** salvare in `reports/figures/{nome_figure}/` un `.png` + un `.json` con i metadati (parametri, dimensione campione, seed, tempi).

**Cosa NON fare:** non reimplementare logica canonica; niente librerie/algoritmi nuovi non richiesti; niente esperimenti extra; non eseguire UMAP/HDBSCAN/Optuna sul full dataset senza la strategia di sottocampionamento.

---

## 1. SETUP
- Dipendenze via `uv` (ramo CPU + note per install GPU/RAPIDS opzionale).
- Cella di **config centralizzata**: modello embedding (default `bge-small`), LLM locale per il labelling, `SEED`, path I/O (struttura AGENTS §7), `DEV_MODE`/`SAMPLE_SIZE`, `USE_GPU`, budget Optuna.
- Cella di auto-detect hardware a runtime con scelta GPU/CPU.

## 2. PREPROCESSING
- Scaricare tutti i dati raw in `data/raw/`; preprocessing (funzioni canoniche) → `data/processed/` (cache `parquet`).
- Analisi: grafico raw vs processato (dimensione dataset, distribuzione lunghezza messaggi, n. redacted, n. email con thread); tabella shape dei due dataset con `null_ratio` e `data_type`; 10 email (5 con thread, 5 senza) raw vs dopo template.

## 3. EMBEDDING
- Embedding in batch col modello configurato (default `bge-small`), con **mapping indice → file originale**; salvataggio in `data/embedding/` (cache). Gestire email lunghe (troncamento/chunking).
- UMAP per i grafici (GPU se disponibile, altrimenti sottocampione).
- `MiniBatchKMeans` con k = [3, 5, 10, 15, 20].
- Analisi: scatter 2D e 3D (sottocampione/datashader); metriche obbligatorie Silhouette/Davies-Bouldin/Calinski-Harabasz (su campione). **ARI/NMI**: chiarire se confrontano KMeans vs HDBSCAN o vs ground truth — «esiste ground truth? quale?». **Recall@K/MRR**: definire il protocollo di retrieval (query + rilevanti) — «DA DEFINIRE».

## 4. CLUSTERING
- Embedding della fase 3.
- **Optuna + CMA-ES** su UMAP+HDBSCAN. **Strategia di scala obbligatoria:** ottimizzare su sottocampione (es. 100–200k), poi **rifittare i best params sul full dataset**. Specificare metrica obiettivo (es. DBCV), search space, `n_trials`, timeout.
- Analisi Optuna (history, importanza iperparametri, slice). Modello finale coi best params (rifittato).
- Grafici: cluster 2D (sottocampione); condensed tree (albero di densità).
- **Overlapping** (soft-clustering); attenzione alla memoria di `all_points_membership_vectors`. **Network graph a livello di CLUSTER** (nodi = cluster, archi = overlap), non per singolo punto.

## 5. LABELLING
- 4 algoritmi: c-TF-IDF, YAKE, TextRank, KeyBERT; tabella primi 20 risultati per algoritmo.
- Per ogni cluster: passare a un **LLM locale** («DA COMPILARE: modello, serving (ollama/vLLM/transformers), context window») i 20 keyword × 4 algoritmi + i 50 punti più vicini al centro (per HDBSCAN usare **medoide/exemplars**) per ottenere l'etichetta. Indicare il prompt template e gestire il caso di molti cluster (batching, stima tempi/token). Mostrare i risultati.

## 6. DATASET FINALE CON ETICHETTE
- Aggiungere al dataset processato la colonna etichetta (join via mapping della fase 3). **Cambio di schema → `DATA_CONTRACTS.md` + approvazione.** Salvataggio in cache.

## 7. VALIDAZIONE MANUALE
- Salvare tutte le etichette in `data/validation/all_label.md` (**nuovo path → `DATA_CONTRACTS.md` + approvazione**).
- 100 mail random dai cluster **con `SEED` fisso**. Per ogni mail, in `data/validation/_{id}/`: `mail.md` (solo contenuto) e `label.md` (etichette del modello).

---

## CHECKLIST PRE-LAB (da verificare con lo sviluppatore)
- [ ] **Internet sul server del lab?** (download dati raw + pesi embedding/LLM, altrimenti pre-staging) → «DA VERIFICARE»
- [ ] **Origine dei dati raw sul server** (i 1.7M non passano da GitHub) → «DA COMPILARE»
- [ ] **GPU presente?** (auto-detect la gestisce, serve per stima tempi) → «DA VERIFICARE»
- [ ] **LLM locale eseguibile sull'hardware del lab** + serving → «DA COMPILARE»
- [ ] **Conflitto §8 risolto** (Opzione A o B) e registrato in `DECISIONS.md`
- [ ] **Cambi di contratto approvati** in `DATA_CONTRACTS.md` (etichette, validation, embedding)

## CHECKLIST FINALE AGENTS (sez. 15) — prima di implementare
letto TASK_BOARD/DECISIONS/DATA_CONTRACTS? approvazione ottenuta? docs e knowledge aggiornate? link studio aggiunti? test previsti (`uv run python -m pytest -q`)? — se un NO: **FERMATI**.
