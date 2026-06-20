# Censimento Pattern Thread/Quote — JMAIL Dataset

> Generato da `_tmp_census.py` · campione 10,000 email · seed=42

---

## 1. Schema Dataset

- **Path:** `data/raw/jmail_emails.parquet`
- **Formato:** Parquet
- **Righe totali:** 1,783,792
- **Colonne:** 19

### Colonne disponibili

| Colonna | Tipo | Null % |
|---------|------|--------|
| `id` | str | 0.0% |
| `doc_id` | str | 0.0% |
| `message_index` | int64 | 0.0% |
| `sender` | str | 7.1% |
| `subject` | str | 25.7% |
| `to_recipients` | str | 0.0% |
| `cc_recipients` | str | 0.0% |
| `bcc_recipients` | str | 0.1% |
| `sent_at` | str | 0.3% |
| `content_markdown` | str | 0.0% |
| `content_html` | str | 99.1% |
| `attachments` | int64 | 0.0% |
| `account_email` | str | 98.4% |
| `email_drop_id` | str | 0.0% |
| `folder_path` | str | 99.0% |
| `is_promotional` | object | 0.0% |
| `release_batch` | int64 | 0.0% |
| `epstein_is_sender` | object | 0.1% |
| `all_participants` | str | 0.0% |

**Colonne rilevanti per thread detection:**
- `content_markdown` — corpo email (testo markdown)
- `subject` — oggetto (rileva Re:/Fwd:)
- Assenti: `Message-ID`, `In-Reply-To`, `References` come colonne dedicate nel raw

---

## 2. Statistiche Generali

- Campione analizzato: **10,000** email (random, seed=42)
- Email con almeno 1 segnale generico nel body: **2,132** (21.3%)
- Email con subject Re:/Fwd:/FW:: **4,850** (48.5%)
- Email con almeno 1 segnale (body o subject): **5,059** (50.6%)

### Distribuzione livelli di annidamento (su email con segnali)

| Livelli quote | N email | % |
|---------------|---------|---|
| 0 | 102 | 4.8% |
| 1 | 1,134 | 53.2% |
| 2 | 451 | 21.2% |
| 3 | 180 | 8.4% |
| 4+ | 265 | 12.4% |

---

## 3. Pattern-Tipo per Frequenza

Frequenza = numero di *email* (non occorrenze) in cui il pattern è stato trovato.

### `ON_DATE_WROTE` — 1,755 email (82.3% delle email con segnali)

**Esempi verbatim:**

1. `On Jan`

2. `on Mon`

3. `On May`

### `OUTLOOK_HEADER_BLOCK` — 465 email (21.8% delle email con segnali)

**Esempi verbatim:**

1. `From: Bebe Avdiu < ↵ Date: Thu, Nov 2, 2017 at 11:15 AM ↵ Subject: Phone call from Kevin - ↵ To:`

2. `From: Jermaine Ruan ↵ Date: Mon, Aug 13, 2018 at 2:16 PM ↵ Subject: Re: LSJ Pool Wall ↵ To:`

3. `From: Jeffrey Epstein <jeevacation@gmail.com> ↵ Date: Tue, 5 Mar 2013 09:41:06 -0400 ↵ To:`

### `CHEVRON_QUOTE` — 405 email (19.0% delle email con segnali)

**Esempi verbatim:**

1. `> On Jan 12, 2019, at 10:11 AM, Nili Priell < > wrote:`

2. `> •`

3. `> Hi Lesley,`

### `BEGIN_FORWARDED` — 283 email (13.3% delle email con segnali)

**Esempi verbatim:**

1. `Begin forwarded message:`

2. `Begin forwarded message`

### `ORIGINAL_MSG_DASHES` — 108 email (5.1% delle email con segnali)

**Esempi verbatim:**

1. `-----Original Message-----`

2. `-------Original Message------`

3. `---Original Message-----`

### `FORWARDED_DASHES` — 26 email (1.2% delle email con segnali)

**Esempi verbatim:**

1. `------- Forwarded message -------`

2. `---------- Forwarded message ----------`

3. `--------- Forwarded message -------------`

### `FWD_BY_LINE` — 24 email (1.1% delle email con segnali)

**Esempi verbatim:**

1. `----- Forwarded by Ami Sheth/New York/Kirkland-Ellis on 08/21/2008 11:27 AM -----`

2. `------- Forwarded message -------`

3. `---------- Forwarded message ----------`


---

## 4. Pattern Corrotti da OCR

Occorrenze totali sul campione completo (10k email).

| Pattern OCR | Occorrenze totali | Esempi |
|-------------|-------------------|--------|
| `BROKEN_SEP` | 27 | ---Original Message / --- Original Message |

**Nessun blocco Outlook con entrambi i marker corrotti nello stesso campione.**

**Email con almeno un pattern OCR:** 26 (0.3% del campione)

---

## 5. Casi Anomali / Outlier

- **Email molto lunghe con segnali di quote** (>95° percentile body length): 316
- **Email con body quasi vuoto ma subject Re:/Fwd:**: 203
- **Email con >5 marker 'Original Message'** (thread molto profondo): 0
- **Email con >20 righe con '>'** (stile mbox/citazione pesante): 78

---

## Note Metodologiche

- Il rilevamento OCR è *euristico*: cattura varianti comuni ma non è esaustivo.
- I livelli di annidamento sono stimati tramite occorrenze multiple degli stessi marker strutturali o profondità `>` max.
- Questo censimento NON modifica il dataset né la pipeline. È input per la strategia di `split_thread_body`.
- Prima di implementare qualsiasi logica di stripping, proporre strategia + pro/contro per approvazione (AGENTS.md §2).