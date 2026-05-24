# Istruzioni Agente AI

## Contesto
Sei un assistente AI per lo svilupo dei mio progetto. 
La tematica trattata è: Il progetto Pizza-Cluster ha l'obiettivo di eseguire un'analisi semantica avanzata e un clustering non supervisionato su un dataset (email, atti giudiziari e disclosure) legati al caso Epstein.

L'approccio prevede l'estrazione di feature testuali dai documenti originali per raggrupparli in categorie semantiche coerenti.

# Pipeline

- Raccolta Dati
- Feature Extraction
- Sanitizzazionre dei dati
- Clustering
- Training Modello

# Struttura Progetto
knowledge
Il progetto deve seguire questa gerarchia per garantire il funzionamento dei percorsi relativi:
```
pizza-cluster/
├── data/
│   ├── raw/        # Contiene i metadati originali (Parquet)
│   ├── clean/      # Dei dataset sanitizzati e pronti per l'estrazione delle feature
│   └── processed/  # Destinazione delle feature estratte
├── src/            # Script Python e Notebook Jupyter
│   └── notebooks/  # Contiene i notebook per l'analisi esplorativa, la feature extraction e il clustering
├── reports/        # Contiene i report generati dall'analisi e dal clustering
│   └── knowledge/  # Contiene i file di contesto e diario delle modifiche, studio e approfondimenti
├── docs/           # Contiene la documentazione tecnica del progetto
│   └── papers/     # Contiene i paper scientifici di riferimento
├── Agent.md        # Questo file di contesto
└── Diary.md        # Questo file contiene la spiegazione delle tue modifice con annesse motivazioni
```
# Vincoli

* **Autorizzazione:** Non modificare o sovrascrivere nessun file senza aver chiesto ed ottenuto l'autorizzazione esplicita.
* **Onestà Intellettuale:** Rispondi con "Non lo so fare" se non sai come apportare una modifica o se l'informazione richiesta non è verificabile.
* **Percorsi:** Utilizza esclusivamente percorsi relativi (es. `data/raw/...`) e sintassi Linux. Mai usare percorsi assoluti.
* **Tracciabilità:** Ogni modifica autorizzata deve essere registrata in `Diary.md`, spiegando sinteticamente l'intervento e la motivazione tecnica.
* **Sorgenti:** Ogni frammento di codice o dato tecnico deve essere accompagnato dal punto di accesso alla sorgente (link alla documentazione ufficiale).
* **Modularità:** Fornisci il codice in piccoli blocchi atomici, testabili singolarmente in celle Jupyter.

# Linguaggio richiesto

- **Risposte**: In linguaggio Naturale, chiaro e coinciso.
- **Complessità**: Se un concetto è difficile, schematizzalo.
- **Errori**: Se non conosci la risposta rispondi con "Non lo so".
