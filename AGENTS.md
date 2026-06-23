# AGENT.md --- Istruzioni Operative Agente AI

## 1. Missione del progetto

Sei un agente AI incaricato di supportare lo sviluppo del progetto
**Pizza Cluster**.

Obiettivo: sviluppare una pipeline riproducibile di clustering per
analizzare email e metadata degli Epstein Files.

Output finali:

-   pipeline dati riproducibile
-   notebook validazione
-   metriche documentate
-   API modello
-   demo funzionante
-   documentazione completa

------------------------------------------------------------------------

## 2. Regola principale

NON prendere decisioni architetturali autonomamente.

Per ogni modifica importante:

1.  Analizza problema
2.  Proponi soluzione
3.  Spiega vantaggi / svantaggi
4.  Aspetta approvazione umana
5.  Solo dopo implementa

Se non sai fare qualcosa:

> "Non lo so fare"

Se non puoi verificare:

> "Non lo so"

------------------------------------------------------------------------

## 3. Workflow obbligatorio

1. Leggere `TASK_BOARD.md`
2. Leggere `DECISIONS.md`
3. Leggere `DATA_CONTRACTS.md`
4. Leggere eventuale diario locale se presente
5. Proporre le task aperte all'utente ed attendere la sua scelta
6. Progettare pipeline 
7. Aspettare approvazione 
8. Implementare codice Python per la business logic
9. Testare 
10. Creare Notebook per eseguire il codice python mostrando tabelle, grafici e risultati
11. ocumentare 
12. Aggiornare task board, decisioni o contratti quando necessario

------------------------------------------------------------------------

## 4. Regola apprendimento continuo (OBBLIGATORIA)

Ogni volta che proponi:

-   un algoritmo
-   una tecnica ML
-   una pipeline nuova
-   una libreria avanzata
-   un modello NLP / embedding
-   una metrica

Devi SEMPRE aggiungere:

### Mini spiegazione (2--5 righe)

Spiega rapidamente:

-   cos'è
-   perché serve
-   quando usarlo

### Materiale studio

Inserire SEMPRE almeno:

-   1 paper ufficiale / documentazione
-   1 risorsa studio (YouTube, corso, articolo tecnico)

Formato:

``` md
Mini spiegazione:
HDBSCAN è una tecnica di clustering density-based...

Approfondimenti:

Paper:
https://...

Video:
https://youtube.com/...
```

NON limitarti a nominare una tecnica.

Devi aiutare gli sviluppatori a comprenderla.

------------------------------------------------------------------------

## 5. Knowledge Base obbligatoria

Dentro:

    docs/knowledge/

Ogni argomento avanzato usato deve avere documentazione.

Formato consigliato:

``` md
# Nome argomento

## Cos'è

...

## Quando usarlo

...

## Pro

...

## Contro

...

## Alternative

...

## Link utili

Paper:
...

Video:
...

Documentazione:
...
```

Inoltre mantenere SEMPRE una sezione:

``` md
# Argomenti da studiare / approfondire per la comprensione

- Clustering gerarchico
- K-Means
- DBSCAN
- Embedding NLP
- Sentence Transformer
```

Regola:

Se durante sviluppo emergono concetti avanzati:

AGGIUNGERLI.

Esempi:

-   HDBSCAN
-   UMAP
-   PCA
-   BERTopic
-   Contrastive Learning
-   Transformer Embedding

Obiettivo:

Creare una knowledge base progressiva per sviluppatori umani.

------------------------------------------------------------------------

## 6. Struttura progetto

    PizzaCluster/

    data/
    data/raw/
    data/processed/
    data/metadata/
    data/embedding/

    models/
    mtrained/
    checkpoints/

    reports/
    figures/

    docs/
    paper/
    knowledge/

    src/
    app/
    notebooks/
    utils/

    tests/

    README.md
    AGENT.md
    ROADMAP.md
    TASK_BOARD.md
    DECISIONS.md
    DATA_CONTRACTS.md
    requirements.txt

File locali opzionali non versionati:

    Diary.md
    TODO.md

------------------------------------------------------------------------

## 7. Regole codice

-   Nessuna logica nei notebook
-   Funzioni modulari
-   Ogni funzione in `src/utils`
-   Docstring obbligatorie
-   Esempi utilizzo obbligatori
-   Test locale con `__main__`

Notebook:

Consentito:

-   EDA
-   benchmark
-   visualizzazione

Vietato:

-   preprocessing hardcoded
-   utility locali
-   pipeline duplicate

------------------------------------------------------------------------

## 8. Modelli ML

Ogni proposta deve includere:

-   motivazione
-   pro
-   contro
-   alternative
-   costo computazionale
-   fonti ufficiali
-   paper scientifici

Documentare tutto.

------------------------------------------------------------------------

## 9. Testing

Validare sempre.

Metriche clustering:

-   Silhouette
-   Davies-Bouldin
-   Calinski-Harabasz

Pipeline:

-   test unitari
-   integrazione

------------------------------------------------------------------------

## 10. Tracciabilità

Ogni modifica autorizzata aggiorna almeno uno dei documenti condivisi rilevanti:

- `TASK_BOARD.md` per avanzamento operativo e handoff
- `DECISIONS.md` per decisioni tecniche approvate
- `DATA_CONTRACTS.md` per cambi a path, schema o artefatti dati
- `docs/knowledge/` per concetti avanzati o note metodologiche

`Diary.md` e `TODO.md` sono file locali opzionali, non versionati. Possono essere usati come appunti personali dello sviluppatore o dell'assistente, ma non devono essere fonte primaria di coordinamento Git/GitHub.

Formato handoff consigliato:

``` md
YYYY-MM-DD

Checkpoint

Intervento

Motivazione tecnica

Test eseguiti

Rischi residui
```

------------------------------------------------------------------------

## 11. Task policy

L'agente può proporre task in `TASK_BOARD.md`.

NON può:

-   aggiungerli
-   rimuoverli

senza approvazione.

`TODO.md`, se presente localmente, e' una nota personale non condivisa.

------------------------------------------------------------------------

## 12. Priorità assolute

1.  Riproducibilità
2.  Modularità
3.  Tracciabilità
4.  Testing
5.  Comprensione tecnica
6.  Documentazione
7.  Collaborazione umano-AI

------------------------------------------------------------------------

## 13. Checklist finale

Prima di implementare:

-   letto ROADMAP?
-   letto TASK_BOARD?
-   letto DECISIONS?
-   letto DATA_CONTRACTS?
-   ottenuta approvazione?
-   documentazione aggiornata?
-   knowledge aggiornata?
-   aggiunti link studio?
-   test previsti?

Se una risposta è NO:

FERMATI.

Correggi il processo.
