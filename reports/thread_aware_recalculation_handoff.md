# Report: Ricalcolo Globale Pipeline e Thread Management
**Data:** 22 Giugno 2026
**Contesto:** Integrazione della Pull Request `feature/processing-refinement` per l'estrazione semantica dei thread.

## Analisi del Problema
L'analisi `thread_discrepancy_analysis.md` ha evidenziato un bug nel vecchio preprocessing: la funzione `normalize_text` rimuoveva i newline, invalidando le regex di estrazione e portando alla **perdita del 96.5% dei thread** nel calcolo del flag `has_thread` (rilevati solo 1.7% contro un atteso ~19.9%).

La recente PR del team ha risolto questo problema spostando la ricerca su `content_markdown` e introducendo la logica "Thread-Aware" per gli embedding (che ora separa il `content_new` dal testo storico relegato sotto `THREAD:`).

## Decisione Operativa
Essendo l'obiettivo finale il **re-clustering globale** sull'intero dataset (1.75 milioni di record), non è sufficiente operare su un campione temporaneo. I dati attualmente memorizzati in `jmail_emails_processed.parquet` ed `email_embeddings.npy` contengono l'errore originario e una struttura testuale promiscua.

È stato quindi deciso di procedere col ricalcolo integrale della pipeline.

## Azioni Implementate
È stato creato il notebook orchestratore `src/notebooks/experiment/full_thread_aware_recalculation.ipynb` progettato per eseguire i seguenti task in sequenza:

1. **Ricalcolo Preprocessing:**
   Esecuzione di `run_processing()` sull'intero dataset per recuperare la percentuale corretta di `has_thread` (~19.9%) e generare il campo testo formattato correttamente. Per evitare conflitti, l'output verrà salvato nel nuovo file isolato: `jmail_emails_processed_thread_aware.parquet`.
   
2. **Generazione Embeddings Massiva:**
   Esecuzione di `run_embedding_pipeline()` per ricreare i vettori a 384 dimensioni. Viene mantenuta rigorosamente la configurazione precedente, ma il risultato verrà esportato nel nuovo file: `email_embeddings_thread_aware.npy`.
   *Tempo stimato di esecuzione:* ~14 ore.

## Next Steps
1. Lanciare il notebook `full_thread_aware_recalculation.ipynb` e attenderne il completamento.
2. Eseguire uno snapshot comparativo sui risultati finali generati, visualizzando grafi a dispersione per validare matematicamente l'impatto sui vettori prima della clusterizzazione.
3. Procedere con UMAP e HDBSCAN (tramite Optuna) sul nuovo `.npy` ripulito.
