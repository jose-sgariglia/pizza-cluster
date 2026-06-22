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
    "@e.newyorktimesinfo.com",
    "facebook.com",
    "notifier@",
    "forgot@nytimes.com",
    "newyorktimes.com"

]

# Template per la formattazione del testo destinato agli embedding (Task 3).
# Utilizza placeholder che verranno sostituiti dai valori delle colonne.
EMBEDDING_TEXT_TEMPLATE = """DATE: {date}
FROM: {sender}
TO: {recipients}
SUBJECT: {subject}

BODY:
{body}{thread_section}"""

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

# ── Thread / quote split patterns ─────────────────────────────────────────────
# Used by split_body_thread() in data_processing.py.
# Earliest match position across all patterns determines the cut point.
# Ordering reflects census frequency (thread_pattern_census.md); the parser
# uses position-based priority, not list order.

# 1. "On [Day/Month …], [Name] wrote:" — Gmail, Apple Mail, Yahoo.
#    Requires a day/month name after "On" to avoid false positives.
#    Handles single-line and two-line (name wraps before "wrote:") variants.
THREAD_ON_DATE_WROTE_RE = re.compile(
    r"(?m)^[ \t]*On[ \t]+"
    r"(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*"
    r"[^\n]{0,200}(?:\n[^\n]{0,150})?wrote[ \t]*:",
    re.IGNORECASE,
)

# 2. Outlook-style header block: From: / Sent|Date: / To: anchored to line start.
#    Never appears inside chevron-quoted lines in this dataset
#    (confirmed thread_validation.md STEP 1: 0 % nested in 10 k-email sample).
THREAD_OUTLOOK_HEADER_RE = re.compile(
    r"(?m)^From[ \t]*:[^\n]*\n(?:[^\n]*\n){0,3}(?:Sent|Date)[ \t]*:[^\n]*\n(?:[^\n]*\n){0,3}To[ \t]*:",
    re.IGNORECASE,
)

# 3. Chevron-quoted block: any line starting with ">" (leading whitespace allowed).
THREAD_CHEVRON_RE = re.compile(r"(?m)^[ \t]*>")

# 4. "Begin forwarded message" — Apple Mail and some webmail clients.
THREAD_BEGIN_FORWARDED_RE = re.compile(
    r"(?m)^[ \t]*-*[ \t]*Begin[ \t]+forwarded[ \t]+message[ \t]*:?",
    re.IGNORECASE,
)

# 5. "-----Original Message-----" and OCR-tolerant variants (≥ 2 dashes each side).
THREAD_ORIGINAL_MSG_RE = re.compile(
    r"(?m)^[ \t]*-{2,}[ \t]*Original[ \t]+Message[ \t]*-{2,}",
    re.IGNORECASE,
)

# 6. "------- Forwarded message -------" and variants (≥ 2 dashes each side).
THREAD_FORWARDED_DASHES_RE = re.compile(
    r"(?m)^[ \t]*-{2,}[ \t]*Forwarded[ \t]+message[ \t]*-{2,}",
    re.IGNORECASE,
)

# 7. "----- Forwarded by [Name] on [date] -----" and variants (≥ 2 dashes each side).
THREAD_FWD_BY_RE = re.compile(
    r"(?m)^[ \t]*-{2,}[ \t]*Forwarded[ \t]+by[ \t]+.{1,80}?-{2,}",
    re.IGNORECASE,
)

# Ordered tuple consumed by split_body_thread(); earliest position across all
# patterns determines the cut — list order does not affect priority.
THREAD_MARKER_PATTERNS: tuple[re.Pattern, ...] = (
    THREAD_ON_DATE_WROTE_RE,
    THREAD_OUTLOOK_HEADER_RE,
    THREAD_CHEVRON_RE,
    THREAD_BEGIN_FORWARDED_RE,
    THREAD_ORIGINAL_MSG_RE,
    THREAD_FORWARDED_DASHES_RE,
    THREAD_FWD_BY_RE,
)
