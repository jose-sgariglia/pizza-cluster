import re

# Regex per identificare i marker di censura e redazione nel testo delle email.
# Queste vengono usate per popolare la feature 'has_redaction' e 'redaction_count'.
REDACTION_PATTERNS = (
    re.compile(r"\bredacted\b", re.IGNORECASE),             # Parola 'redacted' isolata
    re.compile(r"\bwithheld\b", re.IGNORECASE),             # Parola 'withheld' (trattenuto)
    re.compile(r"\bsealed\b", re.IGNORECASE),               # Parola 'sealed' (sotto sigillo)
    re.compile(r"\[\s*redacted\s*\]", re.IGNORECASE),       # Formato classico [redacted]
    re.compile(r"\[+\s*(?:redacted|withheld|sealed)\s*\]+", re.IGNORECASE), # Varianti con più parentesi [[...]]
    re.compile(r"\bX{4,}\b", re.IGNORECASE),                # Stringhe di X (es. XXXX) usate come censura
    re.compile(r"[█■]{2,}"),                                # Caratteri grafici di blocco (Unicode)
)

# Pattern combinato per il conteggio veloce dei marker.
# Utile per estrarre statistiche sulla "densità" di censura in un documento.
COMBINED_REDACTION_PATTERN = re.compile(
    r"\[+\s*(?:redacted|withheld|sealed)\s*\]+|\bredacted\b|\bwithheld\b|\bsealed\b|\bX{4,}\b|[█■]{2,}",
    re.IGNORECASE
)

# Colonne del dataset RAW che decidiamo di mantenere durante il primo caricamento.
# Queste rappresentano il set di dati minimo necessario per le analisi successive.
KEEP_COLUMNS = [
    "id",
    "doc_id",
    "message_index",
    "sender",
    "subject",
    "to_recipients",
    "cc_recipients",
    "bcc_recipients",
    "sent_at",
    "content_markdown",
    "attachments",
    "email_drop_id",
    "is_promotional",
    "release_batch",
    "epstein_is_sender",
    "all_participants",
]

# Blacklist di domini o termini che potrebbero indicare email da escludere 
# o trattare con cautela (Task 1).
BLACKLIST_DOMAINS = [
    "newsletter.com",
    "marketing.it",
    "notifications@",
]

# Template per la formattazione del testo destinato agli embedding (Task 3).
# Utilizza placeholder che verranno sostituiti dai valori delle colonne.
EMBEDDING_TEXT_TEMPLATE = """DATE: {date}
FROM: {sender}
TO: {recipients}
SUBJECT: {subject}

BODY:
{body}"""

# Structural delimiter: a line composed entirely of 2+ repeated -, _, =, or * characters.
# Used as the first signal in disclaimer splitting (requires keyword confirmation).
DISCLAIMER_DELIMITER_RE = re.compile(r"^[\-_=*]{2,}$")

# Phrase-level anchors that reliably open a legal disclaimer block.
# Patterns are intentionally specific to minimize false positives on email body content.
# Single-word patterns (e.g. "disclaimer") are only accepted when followed by a colon.
DISCLAIMER_KEYWORD_ANCHORS = (
    re.compile(r"this (?:e-?mail|message|communication) is (?:intended|confidential|privileged)", re.IGNORECASE),
    re.compile(r"privileged\s+and\s+confidential", re.IGNORECASE),
    re.compile(r"if you (?:have received|received) this (?:e-?mail|message) in error", re.IGNORECASE),
    re.compile(r"the information contained in this (?:e-?mail|message|communication)", re.IGNORECASE),
    re.compile(r"this communication is for informational purposes only", re.IGNORECASE),
    re.compile(r"confidentiality notice\s*:", re.IGNORECASE),
    re.compile(r"disclaimer\s*:", re.IGNORECASE),
    re.compile(r"legal notice\s*:", re.IGNORECASE),
    re.compile(r"this e-?mail (?:and any|may contain|contains)", re.IGNORECASE),
    re.compile(r"intended solely for the (?:use|recipient)", re.IGNORECASE),
    re.compile(r"delete (?:it|this) from your (?:system|computer)", re.IGNORECASE),
)
