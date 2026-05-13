# Dataset Notes - JMAIL

## Analisi delle Colonne

| Colonna           | Descrizione                             | Tipo   |   Valori Nulli | La teniamo?   | Motivo                                           |
|:------------------|:----------------------------------------|:-------|---------------:|:--------------|:-------------------------------------------------|
| id                | Identificatore univoco del record       | str    |              0 | Sì            | Chiave primaria per database e ID nodo in Neo4J. |
| doc_id            | Identificatore del documento originale  | str    |              0 | Forse         | Da valutare se serve per risalire alla fonte.    |
| message_index     | Indice sequenziale del messaggio        | int64  |              0 | No            | Ordinamento interno inutile per i nostri scopi.  |
| sender            | Indirizzo email del mittente            | str    |              0 | Sì            | Nodi e archi in Neo4J.                           |
| subject           | Oggetto dell'email                      | str    |              0 | Sì            | Testo chiave per clustering e NLP.               |
| to_recipients     | Indirizzi email dei destinatari primari | str    |              0 | Sì            | Archi verso i destinatari in Neo4J.              |
| cc_recipients     | Indirizzi email in copia (CC)           | str    |              0 | Sì            | Connessioni secondarie nel grafo.                |
| bcc_recipients    | Indirizzi email in copia nascosta (BCC) | str    |              9 | No            | Valori nulli, complica l'analisi relazionale.    |
| sent_at           | Timestamp di invio                      | str    |              0 | Sì            | Dashboard (serie storiche).                      |
| content_markdown  | Corpo del messaggio                     | str    |              0 | Sì            | Testo primario per clustering.                   |
| attachments       | Contatore allegati                      | int64  |              0 | Forse         | Statistiche per la Dashboard.                    |
| account_email     | Account proprietario mailbox            | str    |              0 | Forse         | Ridondante se account singolo.                   |
| email_drop_id     | Batch di estrazione                     | str    |              0 | No            | Metadato tecnico inutile.                        |
| folder_path       | Percorso cartella                       | str    |             10 | No            | Poco valore semantico.                           |
| epstein_is_sender | Flag mittente Epstein                   | bool   |              0 | Sì            | Filtro rapido.                                   |
| all_participants  | Tutti i partecipanti                    | str    |              0 | Forse         | Possibile scorciatoia, ma ridondante.            |