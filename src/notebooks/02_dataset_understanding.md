# Dataset Understanding

## Source: JMAIL
Il dataset analizzato è un sample locale estratto dal database JMAIL. Il sample è composto da 42 record (email) e 16 colonne. Contiene metadati relazionali e contenuti testuali, con alcune colonne che presentano valori nulli (es. `bcc_recipients`, `folder_path`).

## Available columns
*   **Identificativi:** `id`, `doc_id`, `message_index`, `email_drop_id`
*   **Partecipanti:** `sender`, `to_recipients`, `cc_recipients`, `bcc_recipients`, `account_email`, `all_participants`, `epstein_is_sender`
*   **Contenuto & Metadati:** `subject`, `content_markdown`, `attachments`
*   **Temporali & Organizzativi:** `sent_at`, `folder_path`

## Useful columns for semantic analysis
Le seguenti colonne presentano testo ricco, utile per clustering, topic modeling e NLP:
*   `subject`: Fornisce il tema principale in formato sintetico.
*   `content_markdown`: Fornisce il testo completo e formattato del corpo dell'email, essenziale per estrarre parole chiave ed entità.

## Useful columns for graph construction
Le seguenti colonne sono indispensabili per modellare i nodi e gli archi in Neo4J:
*   `id`: Identificativo univoco del nodo Email o della transazione.
*   `sender`: Nodo di partenza (sorgente).
*   `to_recipients`: Nodo/i di destinazione primaria.
*   `cc_recipients`: Nodi di destinazione secondaria (utili per ampliare il grafo relazionale).
*   *(Opzionale per filtri sui nodi:)* `epstein_is_sender` (flag booleano).

## Columns removed and motivation
In base agli obiettivi (clustering, dashboard, grafo Neo4J), le seguenti colonne non verranno utilizzate o verranno scartate nelle pipeline future:
*   `message_index` e `email_drop_id`: Metadati di ordinamento ed estrazione tecnica, inutili a livello analitico.
*   `bcc_recipients`: I valori nulli (~21% nel sample) rischiano di complicare o sbilanciare l'analisi delle reti in Neo4J.
*   `folder_path`: I valori nulli (~24% nel sample) e l'assenza di utilità relazionale lo rendono trascurabile per i nostri task principali.

## Open questions about the dataset
1.  **Formato Temporale:** La colonna `sent_at` è attualmente di tipo *string*. Dovrà essere convertita rigorosamente in *datetime* per alimentare correttamente la Dashboard.
2.  **Destinatari Multipli:** Le colonne `to_recipients` e `cc_recipients` andranno verosimilmente separate/esplose ("unpivoted") se contengono più indirizzi nella stessa stringa, per poter creare nodi distinti in Neo4J.
3.  **Pulizia Testo:** Il `content_markdown` andrà pulito da eventuali firme ripetute, forward header o boilerplate di posta elettronica per non sfalsare il clustering?