# Tecniche di Topic Labeling

Questo documento descrive le principali tecniche utilizzate per estrarre parole chiave ed etichette (topic labels) dai cluster testuali.

## 1. YAKE (Yet Another Keyword Extractor)

### Cos'è
Un estrattore di keyword non supervisionato basato su feature statistiche del testo. Calcola il punteggio delle parole basandosi su fattori come la frequenza, la posizione nel testo (es. le parole all'inizio pesano di più), il contesto e le maiuscole, senza dipendere da dizionari esterni o addestramento preventivo.

### Quando usarlo
Ottimo per un'estrazione rapida, leggera e multilingua da singoli documenti o cluster di documenti in contesti in cui non si dispone di grandi capacità computazionali.

### Pro
- Estremamente veloce.
- Nessuna dipendenza da modelli pre-addestrati o pesanti.
- Supporto multilingua nativo.

### Contro
- Basandosi solo sulle statistiche, non comprende la semantica profonda del testo.
- Può estrarre keyword rumorose se il testo non è ben pulito.

### Alternative
- TF-IDF standard.
- TextRank.

### Link utili
- Paper: https://arxiv.org/abs/1801.04470
- GitHub: https://github.com/LIAAD/yake
- Video / Talk: https://www.youtube.com/watch?v=0k-b8BvB-C0

---

## 2. TextRank

### Cos'è
Un algoritmo basato su grafi, ispirato al PageRank di Google. Rappresenta il testo come una rete dove i nodi sono le parole o frasi (es. *noun phrases*) e gli archi sono le loro co-occorrenze. L'algoritmo identifica i nodi più "centrali" e importanti nella rete.

### Quando usarlo
Ideale quando si vogliono estrarre frasi intere di senso compiuto (es. *noun chunks*) catturando la struttura e le relazioni grammaticali all'interno di un testo, piuttosto che parole isolate.

### Pro
- Estrae frasi chiave di alta qualità (es. nomi propri o entità complesse).
- Considera le relazioni grammaticali locali.

### Contro
- Lento su testi molto lunghi.
- Dipende fortemente dalla qualità del parser NLP sottostante (es. Spacy).

### Alternative
- RAKE (Rapid Automatic Keyword Extraction).

### Link utili
- Paper: https://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf
- Documentazione: https://spacy.io/universe/project/spacy-pytextrank

---

## 3. c-TF-IDF (Class-based TF-IDF)

### Cos'è
Una variante del TF-IDF in cui tutti i documenti di uno stesso gruppo (la "classe" o "cluster") vengono concatenati in un unico enorme "macro-documento". La frequenza termica (TF) viene quindi calcolata per ogni classe, bilanciandola con la frequenza inversa nei documenti (IDF) ricalcolata sulle varie classi.

### Quando usarlo
È lo standard d'eccellenza per estrarre topic words distintive per cluster. Usato come motore principale in framework come BERTopic.

### Pro
- Penalizza parole molto comuni presenti trasversalmente in tutti i cluster.
- Fa emergere parole localmente iper-specifiche.
- Facile e veloce da calcolare usando le matrici sparse standard.

### Contro
- Necessita di tutti i documenti pre-processati.
- Soffre se un cluster è dominato da testo "spazzatura" estremamente ricorrente.

### Alternative
- BM25.
- Informational Gain.

### Link utili
- Articolo BERTopic: https://maartengr.github.io/BERTopic/algorithm/algorithm.html#c-tf-idf
- Documentazione Scikit-learn (per la variante classica TF-IDF): https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html

---

## 4. KeyBERT

### Cos'è
Tecnica che sfrutta i *language models* (come BERT o modelli *Sentence Transformer*) per estrarre parole chiave calcolando la similarità semantica (es. *cosine similarity*) tra l'embedding dell'intero documento/cluster e gli embedding delle singole parole candidate estratte.

### Quando usarlo
Quando si vuole avere la certezza matematica che le parole chiave estratte siano semanticamente collegate al concetto generale del testo, a prescindere dalla loro pura frequenza statistica.

### Pro
- Comprensione semantica profonda grazie ai Transformer.
- Altissima coerenza tematica.
- Ignora statistiche fuorvianti se le parole non contribuiscono al vero significato.

### Contro
- Computazionalmente costoso (richiede la generazione di *embeddings* per tutte le parole/n-grammi candidati).
- Rallenta notevolmente se non si usa una GPU.

### Alternative
- EmbedRank.
- Topic modeling basato su LLM generativi (GPT, Claude).

### Link utili
- GitHub e Documentazione: https://github.com/MaartenGr/KeyBERT

---

# Argomenti da studiare / approfondire per la comprensione

- Embedding NLP e Sentence Transformers
- Misure di similarità spaziale (Cosine Similarity)
- Costruzione di grafi per l'estrazione testuale (PageRank)
- Frequenze termiche e penalizzazione (TF-IDF vs c-TF-IDF)
- Estrazione di Noun Chunks con Spacy
