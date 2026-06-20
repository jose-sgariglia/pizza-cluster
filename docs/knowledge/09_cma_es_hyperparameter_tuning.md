# CMA-ES per l'Ottimizzazione Iperparametrica

## Cos'è
CMA-ES (Covariance Matrix Adaptation Evolution Strategy) è un algoritmo di ottimizzazione stocastico derivato dalle strategie evolutive, particolarmente efficace per problemi di ottimizzazione continua non convessa. Optuna lo utilizza come campionatore avanzato (`CmaEsSampler`). Funziona mantenendo e adattando una "matrice delle covarianze" che descrive la forma della distribuzione delle soluzioni migliori, permettendogli di muoversi nello spazio di ricerca in modo molto più intelligente e rapido rispetto alla pura Grid Search o Random Search.

## Perché serve
Nel contesto del clustering complesso (come UMAP + HDBSCAN su vettori NLP), gli iperparametri interagiscono in modo non lineare. Ad esempio, aumentare `n_neighbors` in UMAP cambia drasticamente la topologia su cui HDBSCAN dovrà operare con `min_cluster_size`. Una Grid Search tradizionale proverebbe tutte le combinazioni alla cieca, richiedendo tempi infiniti. CMA-ES impara dalle interazioni passate, indirizzando la ricerca verso le "valli" matematiche dove il Silhouette Score è più alto e il rumore è minore.

## Quando usarlo
CMA-ES è ideale quando:
- Lo spazio di ricerca (i parametri da testare) ha dimensioni continue o ampi range discreti.
- La funzione obiettivo (es. calcolare un cluster e valutarne il Silhouette) è costosa in termini di tempo.
- Si sospetta che ci sia una forte correlazione tra i parametri (es. `n_neighbors` e `min_samples`).

## Pro
- Converge verso l'ottimo globale molto più velocemente di Grid/Random Search.
- Tiene conto delle dipendenze complesse tra i vari iperparametri.
- Riduce significativamente il numero di Trial (esecuzioni) necessarie per trovare una configurazione vincente.

## Contro
- È progettato matematicamente per spazi continui. Per usarlo con interi o categorici (es. in Optuna), richiede una mappatura che a volte ne riduce l'efficienza teorica pura.
- Se l'algoritmo non riesce a generare la matrice delle covarianze (es. a causa di parametri statici non ben definiti o vincoli dinamici errati), Optuna esegue un fallback al campionamento casuale, perdendo tutti i vantaggi evolutivi.

## Alternative
- **Grid Search**: Esplora esaustivamente una griglia fissa. Lenta e prigioniera della definizione iniziale della griglia.
- **Random Search**: Veloce, ma cieca. Non impara dai Trial precedenti.
- **TPE (Tree-structured Parzen Estimator)**: Il campionatore predefinito di Optuna. Ottimo per molti task, ma meno performante di CMA-ES in spazi fortemente correlati o topologie complesse come quelle generate da UMAP.

## Approfondimenti

- **Paper ufficiale originale di Nikolaus Hansen**:
  Hansen, N., Ostermeier, A. (2001). Completely Derandomized Self-Adaptation in Evolution Strategies. *Evolutionary Computation*, 9(2), 159-195.
  [Link PDF (MIT Press)](https://direct.mit.edu/evco/article/9/2/159/1105)

- **Documentazione Optuna (CmaEsSampler)**:
  [Optuna Documentation](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.CmaEsSampler.html)

- **Video Esplicativo Consigliato (YouTube)**:
  *Covariance Matrix Adaptation Evolution Strategy (CMA-ES) in a nutshell*
  [Guarda su YouTube](https://www.youtube.com/watch?v=1i8muvzZkPw)
