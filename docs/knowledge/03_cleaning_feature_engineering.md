# Cleaning and Feature Engineering (Phase 1)

## Obiettivo

Trasformare il dataset raw JMAIL in un dataset `processed` ottimizzato per gli embeddings e il clustering. In questa fase abbiamo dato priorità alla modularità, alla pulizia delle feature ridondanti e alla strutturazione del testo per i modelli linguistici.

## Input e output

Input:
- `data/raw/jmail_emails.parquet`

Output:
- `data/processed/jmail_emails_processed.parquet`
- `data/metadata/jmail_processing_metadata.json`

## Pipeline Aggiornata (Phase 1)

La pipeline è stata refactorizzata per essere più modulare e configurabile:

1.  **Caricamento & Blacklist:** Utilizzo di costanti centralizzate in `src/utils/constants/preprocessing.py` e filtraggio basato su domini (Task 1).
2.  **Pulizia Testo:** Normalizzazione whitespace e rimozione email promozionali.
3.  **Feature Engineering "Potato" (Pruning):** Rimozione di feature statistiche granulari a favore di indicatori generici e potenti (Task 2).
4.  **Template Strutturato:** Creazione della colonna `combined_text` tramite un template che include metadati (Task 3).
5.  **Validazione:** Controllo integrità e rimozione righe senza testo.

## Feature Engineering: Cosa abbiamo tenuto e aggiunto

Abbiamo applicato una strategia di **Feature Pruning** per ridurre il rumore e migliorare la condivisibilità del dataset:

### Feature Mantenute (Generic & Core)
- `id`, `sender`, `subject`, `to_recipients`, `sent_at_datetime`: Metadati essenziali.
- `attachment_count`: Conteggio allegati (senza flag booleani ridondanti).
- `has_redaction`, `redaction_count`: Presenza e numero di censure.

### Feature Aggiunte (High Value)
- **`redaction_ratio`**: Rapporto tra marker di censura e lunghezza del testo. È un segnale critico: documenti con alto ratio tendono a raggrupparsi in cluster di "documenti sensibili/riservati".
- **`sender_domain`**: Dominio estratto dal mittente per analisi di network.

### Feature Rimosse (Redundant)
Abbiamo rimosso `sent_hour`, `sent_year`, `is_weekend`, `subject_length`, ecc. poiché sono derivabili dal timestamp e appesantiscono l'analisi senza aggiungere segnale semantico diretto agli embeddings.

## Il Template Strutturato (Task 3)

Per migliorare la comprensione del modello di embedding, non inviamo più solo il corpo della mail, ma un testo formattato:

```text
DATE: {date}
FROM: {sender}
TO: {recipients}
SUBJECT: {subject}

BODY:
{body}
```

**Perché è importante?** I modelli di Sentence Embedding moderni (come BGE o BERT) sono sensibili alla struttura. Includere i metadati direttamente nel testo permette al modello di "vedere" le relazioni temporali e di network durante il calcolo della similarità semantica.

## Modularità: `preprocessing.py` e `.env`

Abbiamo rimosso tutte le costanti "hardcodate" da `data_processing.py`.
- **Regex e Blacklist:** Gestite in `src/utils/constants/preprocessing.py`.
- **Configurabilità:** Il template è salvato nel `.env`. Questo permette di sperimentare diverse strutture di testo senza modificare il codice sorgente.

## Mini spiegazione dei concetti

- **Feature Pruning:** L'arte di rimuovere variabili che non aggiungono informazioni uniche. In ML, meno feature spesso significano modelli più robusti e meno overfitting.
- **Redaction Ratio:** Una metrica di densità. Non ci dice solo *se* c'è una censura, ma quanto il documento è "coperto", riflettendo il livello di segretezza o sensibilità.
- **Structured Prompting for Embeddings:** Tecnica che consiste nel dare una struttura fissa al testo (tipo JSON o template testuale) per aiutare il modello a distinguere tra metadati e contenuto.

## Approfondimenti e Risorse di Studio

- **Feature Engineering & Selection:** [Google ML Crash Course - Feature Engineering](https://developers.google.com/machine-learning/data-prep/transform/feature-engineering)
- **Sentence Embeddings Context:** [SBERT Contextual Information](https://www.sbert.net/examples/applications/semantic-search/README.html)
- **Redaction in NLP:** [Handling Sensitive Data in NLP](https://arxiv.org/abs/2010.06053) (Paper sulla de-identificazione).
- **Pythonic Constants:** [Best Practices for Constants in Python](https://realpython.com/python-constants/)

---

## Boilerplate Detection: Separazione del Disclaimer Legale

### Cos'è il problema

Le email corporate contengono frequentemente, in coda al corpo, un blocco di disclaimer legale standardizzato:

> *"This e-mail is intended only for the use of the individual to whom it is addressed and may contain information that is privileged, confidential..."*

Questo testo:
- È **semanticamente identico** in migliaia di email → introduce rumore massivo per gli embeddings
- Crea un **cluster artificiale** che raggruppa email per presenza di disclaimer piuttosto che per contenuto
- Aggiunge token ripetitivi che abbassano la qualità della rappresentazione vettoriale

### Approccio: euristica posizionale a due strategie

Non è necessario un modello ML. Le email di JMAIL sono email corporate (periodo 1999–2002) con disclaimer standardizzati e struttura prevedibile. Vengono applicate due strategie in cascata con postura **safe by default**: in caso di incertezza il testo originale viene restituito invariato.

**Strategia 1 — Delimitatore strutturale + conferma keyword**

Si cerca una riga separatore composta esclusivamente da caratteri ripetuti (`---`, `___`, `===`, ...). Se trovata, si verifica che nei primi 500 caratteri del testo successivo sia presente almeno una keyword di disclaimer. La conferma è obbligatoria: un `---` senza keyword (firma personale, separatore Markdown) viene ignorato.

**Strategia 2 — Keyword anchor posizionale**

Se nessun delimitatore strutturale è trovato, si cerca una keyword di disclaimer nell'**ultimo 30% delle righe**. Il vincolo posizionale è il principale presidio contro i falsi positivi: un'email che discute di clausole di riservatezza le avrà nel corpo centrale, non in coda.

In entrambe le strategie: se il corpo residuo risulterebbe vuoto, il testo viene restituito invariato.

### Keyword anchors censiti

Tutti i pattern sono phrase-level per ridurre i falsi positivi. I termini ambigui come `disclaimer` o `legal notice` sono accettati solo se seguiti da `:`.

| Pattern | Esempio tipico |
|---|---|
| `this e-mail is intended/confidential/privileged` | "This e-mail is intended only for..." |
| `privileged and confidential` | "PRIVILEGED AND CONFIDENTIAL" |
| `if you received this e-mail in error` | "If you have received this message in error..." |
| `the information contained in this e-mail` | "The information contained in this communication..." |
| `disclaimer:` | "Disclaimer: This email and any files..." |
| `confidentiality notice:` | "Confidentiality Notice: ..." |
| `delete it/this from your system/computer` | "...please delete it from your system." |

### Impatto sul dataset processed

| Feature | Tipo | Descrizione |
|---|---|---|
| `content_clean` | `string` | Corpo dell'email senza disclaimer |
| `has_disclaimer` | `bool` | `True` se un disclaimer è stato rilevato e separato |

`combined_text` e il template di embedding beneficiano automaticamente della pulizia di `content_clean`, in quanto `combined_text` viene costruito da `content_clean`.

### Limiti noti

- **Forward headers** (`----- Original Message -----`, catene di risposta): fuori scope, gestiti in una task separata del backlog.
- **Falsi negativi**: disclaimer senza delimitatori strutturali e senza le keyword censite non vengono rilevati. Preferibile a un falso positivo che strippa contenuto reale.
- **Calibrazione posizionale**: la soglia del 30% è un valore di partenza ragionevole; può essere abbassata se i test su dati reali mostrano falsi negativi sistematici.

### Dove si trova nel codice

- **Costanti**: `src/utils/constants/preprocessing.py` → `DISCLAIMER_DELIMITER_RE`, `DISCLAIMER_KEYWORD_ANCHORS`
- **Funzione**: `src/utils/data_processing.py` → `split_body_disclaimer(text) -> tuple[str, str | None]`
- **Integrazione**: chiamata dentro `add_text_features()`, prima della normalizzazione del testo

### Mini spiegazione: perché non ML?

Un classificatore ML per la segmentazione email (es. CRF, BERT fine-tuned) richiederebbe dati annotati, dipendenze pesanti e pipeline di inferenza. Per questo dataset le regole heuristiche sono preferibili perché:
1. Il dominio è ristretto (email corporate US, anni 1999–2002)
2. I disclaimer sono strutturalmente uniformi
3. Il costo di un falso positivo (testo utile rimosso) è alto → meglio sbagliare in direzione conservativa
4. Le regole sono ispezionabili e modificabili senza retraining

### Approfondimenti

Paper:
Carvalho, V. R., & Cohen, W. W. (2004). *Learning to Extract Signature and Reply Lines from Email*. CEAS 2004.
[Citato in Mailgun Talon](https://github.com/mailgun/talon) — libreria open source che formalizza questo problema con approccio ML ibrido.

Documentazione:
RFC 2822 — *Internet Message Format* (struttura formale delle email, include la convenzione `-- ` come separatore firma):
https://www.ietf.org/rfc/rfc2822.txt

Risorsa studio:
[Real Python — Regex in Python](https://realpython.com/regex-python/) — guida pratica all'uso di `re` per text processing strutturato.

---

## Prossimi Passi: Phase 2 - Embedding Strategy

Nella Phase 2 ci occuperemo di trasformare il testo strutturato in vettori matematici:
1.  **Scelta del Modello:** Validazione del modello `BAAI/bge-small-en-v1.5` (ottimo rapporto prestazioni/velocità).
2.  **Chunking Strategy:** Gestione delle email molto lunghe che superano il limite di token del modello (512 token).
3.  **Vettorizzazione:** Generazione degli embeddings e salvataggio in formato NumPy per alte prestazioni.
4.  **Validazione Semantica:** Test di similarità per assicurarci che email simili finiscano "vicine" nello spazio vettoriale.
