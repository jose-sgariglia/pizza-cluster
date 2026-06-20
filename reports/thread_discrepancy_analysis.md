# Analisi Discrepanza Thread Detection: 50.6% → 1.7%

> Campione: 10,000 email, seed=42, `data/raw/jmail_emails.parquet`
> Data analisi: 2026-06-19

---

## 1. Tabella di confronto: tasso di esclusione del filtro promozionale

| Gruppo | Email nel campione | Rimosse dal filtro | Tasso rimozione |
|--------|-------------------|--------------------|-----------------|
| CON body-signal di thread | 1,965 | 4 | **0.2%** |
| SENZA body-signal di thread | 8,035 | 142 | **1.8%** |
| Totale campione | 10,000 | 146 | 1.5% |

Le email con segnali di thread vengono rimosse **meno** delle email senza segnali.
Il filtro non discrimina selettivamente le email conversazionali.

---

## 2. Conclusione netta: il filtro promozionale NON spiega il crollo

**Il filtro promozionale spiega 0 pp del gap.**

Riepilogo delle grandezze:

| Metrica | Valore |
|---------|--------|
| Segnali body su `content_markdown` raw (pre-filtro) | 1,965 / 10,000 = **19.6%** |
| Segnali body su `content_clean` normalizzato | 69 / 10,000 = **0.7%** |
| Segnali body persi per effetto di `normalize_text` | **1,896 / 1,965 = 96.5%** |
| Email con thread rimosse dal filtro promozionale | **4 / 1,965 = 0.2%** |
| `has_thread` atteso dopo solo il filtro (≈19.6% × 99.8%) | **~19.9%** |
| `has_thread` osservato nel notebook processed (6,335 email) | **1.7% (108 email)** |

**Il filtro promozionale spiega un calo di 0 pp** (da 19.6% a 19.9% — in realtà aumenta
leggermente perché le promo email hanno un tasso thread più basso).

**Il gap residuo non spiegato dal filtro: 19.9% − 1.7% = 18.2 pp.**

### Causa reale

`normalize_text()` in `add_text_features()` fa `" ".join(value.split())`, che converte
ogni sequenza di whitespace (compreso `\n`) in un singolo spazio. Il risultato è una
stringa su **una sola riga**. Tutti i pattern di thread detection usano `(?m)^` (ancora
inizio-riga in modalità MULTILINE): se non ci sono newline, nessun `^` matcha tranne
che alla posizione 0.

Conseguenza: su `content_clean` sopravvivono solo le email il cui marker di thread è
**già al carattere 0** del testo normalizzato — cioè email che iniziano direttamente con
un marker (es. puri forward senza preambolo). Il 96.5% dei segnali viene perso.

Verifica diretta:

```python
text = "Hi.\n\nOn Jan 1, 2020, Alice wrote:\n> yes."
normalize_text(text)
# → "Hi. On Jan 1, 2020, Alice wrote: > yes."
split_body_thread(text)     # has_thread=True, content_new="Hi."
split_body_thread(normalize_text(text))  # has_thread=False
```

---

## 3. Correzione della baseline: i numeri del censimento

Il censimento originale riportava 5,059 (50.6%) con "almeno un segnale". Quel conteggio
includeva **4,850 email con Re:/Fwd: nel subject** — segnale che il parser di thread
*non* usa (opera solo sul body). La baseline rilevante per confrontare con `has_thread`
è il **body-only signal**: 2,132 email (21.3%) secondo il censimento, 1,965 (19.6%)
nella nostra riproduzione (piccola varianza accettabile, campionamento identico).

---

## 4. Esempi concreti: email CON thread escluse dal filtro (tutti i 4 casi)

Solo 4 email su 1,965 (0.2%) con segnali di thread vengono rimosse dal filtro.
Tutti e 4 sono legittimamente promozionali o automatismi:

**Caso 1 — forward di ricevuta Uber**
- subject: `Fwd: Ride Receipt for Reservation# [REDACTED]`
- is_promotional: True
- body: `Sent from my iPhone → Begin forwarded message: → … Ride Receipt for Reservation# → Like Us on FACEBOOK * * Download Our MOBILE RESERVATION APP`
- Valutazione: vero positivo del filtro. È una notifica automatica forwardata.

**Caso 2 — forward di ricevuta salone parrucchiere**
- subject: `Fwd: Receipt From Frederic Fekkai - 5th Avenue`
- is_promotional: True
- body: `Sent from my iPhone → Begin forwarded message: → From: Frederic Fekkai - 5th Avenue → Receipt attached`
- Valutazione: vero positivo. Ricevuta commerciale forwardata, già etichettata `is_promotional=True` nel dataset raw.

**Caso 3 — forward ordine Restoration Hardware**
- subject: `Fwd: Restoration Hardware Order Confirmation - Order #: 4843085`
- is_promotional: True
- body: `more stuff for Sam's place → Begin forwarded message: → From: Restoration Hardware`
- Valutazione: unico caso borderline (commento personale "more stuff for Sam's place"), ma la sorgente è promozionale. Falso positivo marginale.

**Caso 4 — newsletter Concierge Auctions**
- sender: `inquiries@conciergeauctions.com`
- subject: `[Auction Alert®] Find Your Summer Oasis`
- body: `All No Reserve auctions in August and September. Plus five just-launched properties…`
- Valutazione: vero positivo. Newsletter pura, ha un segnale di thread per via di un link contenuto nel body che matcha accidentalmente un pattern (falso positivo del parser, non del filtro).

---

## 5. Misurazione content_new vuoto/corto (STEP 5)

### 5.1 Sul campione pre-filtro (10k seed=42, `content_markdown` raw)

| Metrica | Count | % su email con has_thread |
|---------|-------|--------------------------|
| Email con `has_thread=True` | 1,965 | 19.6% del campione |
| `content_new_is_short=True` (<20 chars) | 502 | **25.5%** |
| `content_new` esattamente vuoto (0 chars) | 81 | **4.1%** |
| `content_new` corto ma non vuoto (1–19 chars) | 421 | **21.4%** |

Interpretazione: 1 email su 4 con thread ha una risposta brevissima (<20 chars). Il
fenomeno è reale ma non patologico: le risposte di 1–2 parole ("ok", "+1", "grazie")
sono frequenti in email conversazionali brevi. I puri forward senza commento (content_new
vuoto, 4.1%) sono la minoranza.

### 5.2 Confronto pre-filtro vs post-filtro vs post-normalizzazione

| Fase | n email | has_thread % | is_short % (di quelle con thread) | empty % (di quelle con thread) |
|------|---------|-------------|----------------------------------|-------------------------------|
| Pre-filtro, raw markdown, 10k seed=42 | 10,000 | 19.6% | 25.5% | 4.1% |
| Post-filtro promozionale, raw markdown | 9,854 | 19.9% | 25.5% | 4.1% |
| Post-normalizzazione (parquet processed, content_clean) | 6,335 | **1.7%** | **100%** | **100%** |

**Conclusione STEP 5:** la proporzione di `content_new_is_short` e `content_new` vuoto
è **stabile** tra pre-filtro e post-filtro promozionale (25.5% → 25.5%, 4.1% → 4.1%).
Dopo la normalizzazione del testo (`content_clean`), invece, il 100% delle 108 email
rilevate ha `content_new` vuoto — perché le uniche che sopravvivono alla normalizzazione
sono quelle dove il marker cade già al carattere 0, producendo `content_new = ""`.
Questo rende il flag `content_new_is_short` del parquet processed **non diagnostico**:
segnala al 100% non perché le risposte siano brevi, ma perché il parser lavora su testo
senza newline.

### 5.3 Campione di casi content_new vuoto (raw, pre-filtro)

15 esempi su 81 (campione random seed=42):

| sender | subject | content_quoted [:120] |
|--------|---------|----------------------|
| Jeffrey Epstein | Re: 6,,, | On Thu, Mar 31, 2011 at 11:07 AM, wrote: Ok, and what time are you leaving tomorrow? |
| Lesley Groff | FW: VH1 SmartLipo The Cougars Short 2min version | From: RhodesVictor@aol.com … Subject: VH1 SmartLipo |
| jeevacation@gmail.com | Re: | On Thu, Jun 9, 2011 at 4:34 PM, < > wrote: do you have 30 seconds? |
| Richard Kahn | PBI Carpet installation update | Begin forwarded message: … Sender: Blacked out |
| Fran | Fwd: Seasons Greetings | -------- Forwarded message -------- From: Hardeep Singh Puri |
| nan | Fwd: LSJ Meeting | Begin forwarded message: From: Warwick Wicksman … Darren Indyke |
| Jeffrey Epstein | Re: can you come ? | On Wed, Sep 15, 2010 at 7:20 AM, < wrote: EFTA_R1_00485483 |
| Jeffrey Epstein | excuses | On Thu, Oct 22, 2009 at 7:58 PM, <blackened out> wrote: Ok. I will not be able to take … |
| nan | Fwd: sponsorship | ------- Forwarded message ------- From: Ben Taplin |
| Jeffrey Epstein | Re: any time you want,, but alone. | On Wed, Jun 16, 2010 at 2:50 PM, <1 wrote: I like that u in NY :) |
| Lesley Groff | FW: UBS Business Jet Update | From: Sean J. Lancaster … 'Alan Goldman'; 'Alex Hsu'; … |
| unknown | Fwd: | Begin forwarded message: From: "Feierstein, Kimberly" |
| jeffrey E. | Re: | On Wed, Oct 21, 2015 at 2:49 PM, Farkas, Andrew L. wrote: No. Not really. I live now at the Essex |
| Lesley Groff | Fwd: WEF | Begin forwarded message: * From: Maree Glass |
| nan | Fwd: | Begin forwarded message: From: … Date: March 12, 2012 3:27:32 PM EDT |

Tutti i 15 casi sono **forward puri** (Begin forwarded message / FW:) oppure **reply
senza testo aggiunto** (Re: con body che inizia direttamente col blocco citato).
Nessun falso positivo del parser: sono email in cui chi risponde non ha scritto nulla
di proprio prima del thread citato. Il flag `content_new_is_short` funziona correttamente
come QA flag per questi casi.

---

## 6. Sintesi e prossimi passi suggeriti (non implementare in questo step)

| Ipotesi | Verdetto | Evidenza |
|---------|----------|----------|
| Filtro promozionale esclude selettivamente email con thread | **Falsificata** | 0.2% esclusione vs 1.8% senza thread |
| Normalizzazione testo (`normalize_text`) distrugge i marker `^` | **Confermata** | 96.5% dei segnali persi, 100% empty nel processed |
| Parser di marker è corretto su raw markdown | **Confermato** | 19.6% segnali su content_markdown ≈ 21.3% del censimento |

**Azione richiesta (fuori scope di questa analisi):** decidere se `split_body_thread`
debba operare su `content_markdown` (raw, pre-normalizzazione) invece di `content_clean`,
oppure se `normalize_text` debba preservare i newline prima dello step di thread-splitting.
