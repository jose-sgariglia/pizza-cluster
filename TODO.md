# TODO

# Breve Termine
- [x] Crea degli embeddings per ogni email, utilizzando un modello di embedding pre-addestrato (come BERT o simili). Documenta la scelta del modello e i parametri utilizzati.
- [ ] Preprocessa i dati delle email (rimuovendo stop words, normalizzando il testo, ecc.) e documenta le tecniche di preprocessing utilizzate e le scelte fatte.
- [ ] Fase di Feature Engineering: esplora e documenta eventuali tecniche di feature engineering che potrebbero migliorare la qualità degli embeddings o del clustering, come l'aggiunta di metadata (ad esempio, mittente, destinatario, data) o l'uso di tecniche di riduzione della dimensionalità (come PCA o t-SNE) per visualizzare gli embeddings. Anche aggiunta di features basate su tecniche di NLP, come la frequenza di parole chiave o l'analisi del sentiment, potrebbe essere utile. Oppure analisi statistiche sui dati (se un file è redacted, quanta percentuale è il redacting, ecc). Documenta le tecniche utilizzate e i risultati ottenuti.
 
# Medio Termine
- [ ] Sperimenta con diverse tecniche di clustering (come K-means, DBSCAN, HDBSCAN, ecc.) sui dati processed e sugli embeddings. Documenta i risultati, le metriche di valutazione e le scelte fatte.
- [ ] Per dare un nome ai cluster, potresti utilizzare tecniche di estrazione di parole chiave (usanto inizialmente un modello naive come c-TF-IDF) o topic modeling (come LDA) per identificare i temi principali di ogni cluster. Documenta la metodologia e i risultati ottenuti.

# Lungo Termine
- [ ] Sviluppa un'API per esporre il modello di clustering, permettendo agli utenti di vedere i cluster, selezionarne uno e vedere le email che ne fanno parte, con i relativi metadata. Documenta l'API e fornisci esempi di utilizzo.
- [ ] Ricreare i cluster con un modello di embedding più avanzato, come un modello fine-tuned specifico per il dominio delle email, e confrontare i risultati con quelli ottenuti con il modello pre-addestrato. Documenta le differenze e i miglioramenti ottenuti.
- [ ] Documentare le API con swagger o simili, fornendo una documentazione chiara e dettagliata per gli sviluppatori che vogliono utilizzare il modello di clustering.
- [ ] Sviluppare una demo funzionante che mostri l'utilizzo dell'API e i risultati del clustering, permettendo agli utenti di interagire con i dati e vedere i cluster in azione. Documenta la demo e fornisci istruzioni per l'uso.


