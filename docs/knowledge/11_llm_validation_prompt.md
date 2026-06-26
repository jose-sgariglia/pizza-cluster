# Prompt — Agente di Validazione Cluster (Fase 8)

Due versioni disponibili:
- **Prompt A** — agente autonomo con accesso al filesystem (Antigravity): processa tutti i cluster in un colpo solo.
- **Prompt B** — chat senza accesso a file: un cluster alla volta, cambia solo `CLUSTER_ID = X`.

---

## Prompt A — Agente autonomo (filesystem access)

```
## YOUR TASK

You are a cluster label validation agent. You must process ALL cluster folders,
validate each one, and produce a final summary report.
Do not stop until every cluster folder has been processed.

---

## FILE STRUCTURE

All files are under: /home/suga/Workspace/Projects/pizza-cluster/data/validation/

- all_label.md                    → full list of existing cluster labels (read this first)
- cluster_0/ .. cluster_288/      → one folder per cluster, each contains:
    cluster_info.md               → cluster name, n_emails, probability stats
    exemplar_1_*.md               → most representative email (highest HDBSCAN prob)
    exemplar_2_*.md
    exemplar_3_*.md
    boundary_1_*.md               → most ambiguous email (lowest prob > 0)
    boundary_2_*.md
    results.md                    → OUTPUT: write this file for each cluster

Final output:
- data/validation/summary_results.md   → aggregate report (write at the end)

---

## STEP 1 — Read the label list

Read data/validation/all_label.md.
Extract the full table of cluster IDs and names. This is your ONLY valid label source.

---

## STEP 2 — Process each cluster (repeat for ALL cluster_* folders)

For each folder in data/validation/cluster_*/:

  a) SKIP if results.md already exists in that folder (idempotent — safe to resume).

  b) Read:
     - cluster_info.md         → get cluster_id, assigned_name, n_emails
     - all exemplar_*.md files → most representative emails
     - all boundary_*.md files → most ambiguous emails

  c) Reason about the emails WITHOUT looking at assigned_name first.
     Identify the common theme from the email content.

  d) From the label list read in Step 1, select:
     - best_existing_label: the ONE label that best fits the emails
     - best_existing_label_id: its numeric ID
     - alternative_existing_labels: up to 2 other close matches (optional)

  e) If no existing label fits well, set suggested_new_label to a short new label (2-4 words).
     Otherwise set it to null.

  f) Compare best_existing_label with assigned_name and choose a verdict:
     OK         → assigned label is the best match from the existing list
     REASSIGN   → a different existing label fits better
     NEW_LABEL  → no existing label fits; a new one is needed
     SPLIT      → emails cover 2+ distinct topics

  g) Write the following JSON to cluster_{id}/results.md:

{
  "cluster_id": <integer>,
  "assigned_name": "<from cluster_info.md>",
  "n_emails": <integer>,
  "best_existing_label": "<label from the list>",
  "best_existing_label_id": <integer>,
  "alternative_existing_labels": ["<optional>", "<optional>"],
  "suggested_new_label": null,
  "verdict": "<OK|REASSIGN|NEW_LABEL|SPLIT>",
  "confidence": "<alta|media|bassa>",
  "note": "<one sentence, max 20 words>"
}

---

## STEP 3 — Write the final summary

After ALL cluster folders have been processed, read every results.md and write
data/validation/summary_results.md with this structure:

# Validation Summary

Generated: <datetime>
Total clusters processed: <N>

## Verdict distribution

| Verdict    | Count | % |
|------------|-------|---|
| OK         | ...   |   |
| REASSIGN   | ...   |   |
| NEW_LABEL  | ...   |   |
| SPLIT      | ...   |   |
| ERROR      | ...   |   |

## Confidence distribution

| Confidence | Count |
|------------|-------|
| alta       | ...   |
| media      | ...   |
| bassa      | ...   |

## Clusters to REASSIGN

| Cluster ID | Assigned Name | Suggested Label | Suggested ID | Confidence |
|------------|---------------|-----------------|--------------|------------|
| ...        | ...           | ...             | ...          | ...        |

## Clusters needing NEW LABEL

| Cluster ID | Assigned Name | Suggested New Label | Confidence |
|------------|---------------|---------------------|------------|
| ...        | ...           | ...                 | ...        |

## Clusters to SPLIT

| Cluster ID | Assigned Name | Note | Confidence |
|------------|---------------|------|------------|
| ...        | ...           | ...  | ...        |

## Low confidence results (bassa)

| Cluster ID | Assigned Name | Verdict | Note |
|------------|---------------|---------|------|
| ...        | ...           | ...     | ...  |
```

---

## Prompt B — Chat (un cluster alla volta)

```
CLUSTER_ID = X

---

You are validating cluster X from an email clustering pipeline.

I have attached the files for this cluster:
- cluster_info.md    → cluster name, size, probability stats
- exemplar_1..3      → the 3 most representative emails (highest HDBSCAN probability)
- boundary_1..2      → the 2 most ambiguous emails (lowest probability still assigned)

Your task:
1. Read all attached emails.
2. Pick the BEST matching label from the list below (you must choose one).
3. Optionally list 1-2 close alternatives from the same list.
4. If no existing label fits, suggest a new one in "suggested_new_label".
5. Read the assigned label from cluster_info.md and compare.
6. Output ONLY the JSON below, nothing else.

---

EXISTING CLUSTER LABELS:

| ID  | Label                   |
|-----|-------------------------|
| 0   | Package Delivery        |
| 1   | Financial Report        |
| 2   | Flight Alerts           |
| 3   | Calendar Events         |
| 4   | Alerts                  |
| 5   | Birthday                |
| 6   | OutOfOffice             |
| 7   | Delivery Failure        |
| 8   | Sex Scandal             |
| 9   | Gotham Chairs           |
| 10  | Passport                |
| 11  | Negotiations            |
| 12  | Travel                  |
| 13  | Calendar Reminders      |
| 14  | Reminders               |
| 15  | HastyPudding            |
| 16  | Rothschild Meeting      |
| 17  | Salary Bonus            |
| 18  | IMAX                    |
| 19  | Leon Meetings           |
| 20  | Epstein Case            |
| 21  | LinkedIn Invites        |
| 22  | Meetings                |
| 23  | Summers                 |
| 24  | Interior Design         |
| 25  | Personal Calls          |
| 26  | Tuscan Cooking          |
| 27  | Apple Watches           |
| 28  | Paris Trip              |
| 29  | Private                 |
| 30  | Friendship              |
| 31  | Fitness Equipment       |
| 32  | Skype Meetings          |
| 33  | JeffreyEpstein          |
| 34  | Leon Meetings           |
| 35  | Personal Meetings       |
| 36  | SEC Scandals            |
| 37  | Epstein Interview       |
| 38  | Skype Calls             |
| 39  | Business Trip           |
| 40  | Personal Advice         |
| 41  | Trump                   |
| 42  | Bannon                  |
| 43  | Epstein Case            |
| 44  | Dr. Bard Meeting        |
| 45  | Meditation Research     |
| 46  | Personal Meetings       |
| 47  | Dubin Benefit           |
| 48  | Lawyer Confidential     |
| 49  | Business Meetings       |
| 50  | Goodbyes                |
| 51  | Harvard Trip            |
| 52  | BBB                     |
| 53  | Wire Delay              |
| 54  | Faith Kates             |
| 55  | Barak Meetings          |
| 56  | JEFFREY EMAILS          |
| 57  | JesStaley               |
| 58  | Epstein Meeting         |
| 59  | No                      |
| 60  | Summers                 |
| 61  | Personal Meetings       |
| 62  | Personal                |
| 63  | Musk Meetings           |
| 64  | Printer Issues          |
| 65  | Trip Planning           |
| 66  | Meeting                 |
| 67  | Sony                    |
| 68  | Sony                    |
| 69  | Krauss Epstein          |
| 70  | Personal Updates        |
| 71  | Bread Pudding           |
| 72  | BlackBerry Deal         |
| 73  | Game Hunting            |
| 74  | BlackBerry              |
| 75  | BlackBerry              |
| 76  | BlackBerry              |
| 77  | Personal Messages       |
| 78  | Call Schedule           |
| 79  | Jeffrey Epstein         |
| 80  | Car Reservation         |
| 81  | Peter Meetings          |
| 82  | Rothschild Stock        |
| 83  | Haircuts                |
| 84  | MRI Results             |
| 85  | Dentist Appointment     |
| 86  | Home Photos             |
| 87  | Photos                  |
| 88  | Appointments            |
| 89  | Reminder Notes          |
| 90  | Meetup Plans            |
| 91  | Lawyer Contact          |
| 92  | Office Work             |
| 93  | Mandelson Contacts      |
| 94  | Leon Black              |
| 95  | Photos                  |
| 96  | Confirmations           |
| 97  | Personal Matters        |
| 98  | Leon Arrival            |
| 99  | Amex Charges            |
| 100 | EFTA Clearance          |
| 101 | Epstein Affair          |
| 102 | SEO                     |
| 103 | Passport Issue          |
| 104 | Carnegie Hall           |
| 105 | Sulayem Meeting         |
| 106 | Japan Trip              |
| 107 | Package Delivery        |
| 108 | FedEx Tracking          |
| 109 | Estate Settlement       |
| 110 | Phone Calls             |
| 111 | Marrakech Property      |
| 112 | ChristiesAuction        |
| 113 | Brad Notes              |
| 114 | Epstein                 |
| 115 | Israel Affairs          |
| 116 | GenomicsResearch        |
| 117 | Linguistic Theory       |
| 118 | Apt Arrangements        |
| 119 | Flight Bookings         |
| 120 | Transfer Requests       |
| 121 | JoiIto                  |
| 122 | RealEstate              |
| 123 | Address Update          |
| 124 | Pedophile               |
| 125 | Pedophile               |
| 126 | Financial Matters       |
| 127 | Epstein Meetings        |
| 128 | Epstein Meetings        |
| 129 | Stock Trades            |
| 130 | Customs Clearance       |
| 131 | Skin Consult            |
| 132 | Home Theater            |
| 133 | Epstein Affairs         |
| 134 | Chomsky Meetings        |
| 135 | Private Matters         |
| 136 | Miami Trip              |
| 137 | Chomsky Meetings        |
| 138 | Wire Transfer           |
| 139 | Personal Messages       |
| 140 | Epstein                 |
| 141 | Personal Messages       |
| 142 | Bitcoin                 |
| 143 | Family Matters          |
| 144 | Zorro Ranch             |
| 145 | Marital Trust           |
| 146 | Epstein                 |
| 147 | Nathan Meeting          |
| 148 | Personal Struggles      |
| 149 | Watergate               |
| 150 | Financial Report        |
| 151 | Exterminator Schedule   |
| 152 | Alarm Disarm            |
| 153 | Cirque du Soleil        |
| 154 | Sweatshirts             |
| 155 | Marrakech Trip          |
| 156 | Loan Money              |
| 157 | WIRE REQUESTS           |
| 158 | Vacation Photos         |
| 159 | Personal Notes          |
| 160 | New Year Wishes         |
| 161 | Ranch Plans             |
| 162 | Epstein Hotels          |
| 163 | LSJ Construction        |
| 164 | Paris Trip              |
| 165 | Jeffrey Visit           |
| 166 | Tax Returns             |
| 167 | Woody Allen             |
| 168 | AML Review              |
| 169 | Social Scheduling       |
| 170 | Private Equity          |
| 171 | Art Loans               |
| 172 | InvestmentOpportunities |
| 173 | Financial Trades        |
| 174 | Epstein                 |
| 175 | Personal Notes          |
| 176 | Law Firm                |
| 177 | Epstein Files           |
| 178 | Currency Exchange       |
| 179 | JeffreyEpstein          |
| 180 | Investment Notes        |
| 181 | Bank Wires              |
| 182 | Jeffrey Meeting         |
| 183 | Wealth Management       |
| 184 | Financial Markets       |
| 185 | Finance Deals           |
| 186 | Epstein Confidential    |
| 187 | Southern Financial      |
| 188 | Garden Design           |
| 189 | Family                  |
| 190 | Food Options            |
| 191 | Deutsche Bank           |
| 192 | KYC Cases               |
| 193 | Banking Accounts        |
| 194 | Financial Meetings      |
| 195 | Bank Wire Transfer      |
| 196 | Trip Planning           |
| 197 | Photos                  |
| 198 | Pool Design             |
| 199 | Travel                  |
| 200 | Palm Beach              |
| 201 | Birthday Wishes         |
| 202 | Epstein Contacts        |
| 203 | Epstein                 |
| 204 | Epstein Affair          |
| 205 | Epstein                 |
| 206 | Doctor Visit            |
| 207 | iPhone Notes            |
| 208 | Mandelson Meeting       |
| 209 | Paris                   |
| 210 | Phone Calls             |
| 211 | iPad Notes              |
| 212 | iPad                    |
| 213 | Jeffrey Emails          |
| 214 | Travel Invoices         |
| 215 | Personal Messages       |
| 216 | iPhone Files            |
| 217 | Island Visit            |
| 218 | Flight Plans            |
| 219 | Social Calendar         |
| 220 | Person Contacts         |
| 221 | Travel                  |
| 222 | Travel                  |
| 223 | New York                |
| 224 | NYC Trip                |
| 225 | Travel Arrangements     |
| 226 | Flight Reservations     |
| 227 | FollowUp                |
| 228 | Airline Tickets         |
| 229 | Epstein                 |
| 230 | Friendship              |
| 231 | Jojo Help               |
| 232 | Welcome Letters         |
| 233 | Personal Conversations  |
| 234 | Private Life            |
| 235 | Luxury Cars             |
| 236 | Fun                     |
| 237 | Island Getaway          |
| 238 | Private Flights         |
| 239 | Travel Plans            |
| 240 | Paris Trip              |
| 241 | Epstein Photos          |
| 242 | Photos                  |
| 243 | New York                |
| 244 | Medical Records         |
| 245 | GSJ Cable               |
| 246 | Please                  |
| 247 | Pool Maintenance        |
| 248 | Beach Maintenance       |
| 249 | Jeffrey Calls           |
| 250 | Airport Info            |
| 251 | Furniture               |
| 252 | Apartment Cleaning      |
| 253 | Boat                    |
| 254 | Personal Calls          |
| 255 | Private Flight          |
| 256 | Private Jets            |
| 257 | AircraftSales           |
| 258 | Airline Tickets         |
| 259 | Computer Issues         |
| 260 | Palm Trees              |
| 261 | Pool Design             |
| 262 | Jeffrey Meetings        |
| 263 | Thank                   |
| 264 | Flight Issues           |
| 265 | Travel Arrangements     |
| 266 | Personal Issues         |
| 267 | Chinchilla              |
| 268 | Personal Issues         |
| 269 | Mysterious Meetings     |
| 270 | Agreement               |
| 271 | Epstein                 |
| 272 | Harvard Meetings        |
| 273 | Epstein                 |
| 274 | iPad Notes              |
| 275 | EFTA_R1                 |
| 276 | Epstein                 |
| 277 | Epstein                 |
| 278 | Reminders               |
| 279 | Dinner Plans            |
| 280 | Epstein                 |
| 281 | Epstein Correspondence  |
| 282 | Epstein Calls           |
| 283 | Epstein Meetings        |
| 284 | Cell Phone              |
| 285 | Epstein                 |
| 286 | iPhone Notes            |
| 287 | Epstein                 |
| 288 | Epstein Case            |

---

OUTPUT (return only this JSON, nothing else):

{
  "cluster_id": X,
  "assigned_name": "<from cluster_info.md>",
  "n_emails": <from cluster_info.md>,
  "best_existing_label": "<chosen from the table above>",
  "best_existing_label_id": <integer>,
  "alternative_existing_labels": ["<optional>", "<optional>"],
  "suggested_new_label": null,
  "verdict": "<OK|REASSIGN|NEW_LABEL|SPLIT>",
  "confidence": "<alta|media|bassa>",
  "note": "<one sentence, max 20 words>"
}
```
