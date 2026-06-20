# Events Hooks Rules Context

Hook-vs-context framework + full events/hooks/permissions map → [Schema.md](Schema.md).







##


## Rules




Grade = importance. Kind = Hook (fires) or Context (just text). 3rd row = runtime weight.

### TOP

| Rule | Description |
| --- | --- |
| **BULD-01** Edit source | Edit `template.html`, never `index.html`; rebuild `python3 build_site.py` |
| <br /> | Context · verifiable |
| <br /> | ~12 always-on tokens; no runtime |
| **REPO-01** Save | commit + push to `main` after every change — owner only sees the live site; then send rebuilt `index.html` |
| <br /> | Context · verifiable |
| <br /> | ~25 always-on tokens; no runtime |
| **REPO-03** Sync first | before work, `git fetch origin main` + rebase/merge (parallel AIs edit at once) |
| <br /> | Context · verifiable |
| <br /> | ~15 always-on tokens; no runtime |
| **REPO-04** Merge conflicts | never take one `template.html` side wholesale — merge feature-by-feature (badge, SP modal, My-company, turnover/revenue, Data Explorer), keep all |
| <br /> | Context · judgment |
| <br /> | ~30 always-on tokens; no runtime |

### MED

| Rule | Description |
| --- | --- |
| **BULD-02** Version badge | `<h1>` badge every change. `vA.B.C`: bump **C**; **B** owner-only; **A** owner-only |
| <br /> | Hook [`version_reminder.py`](.claude/hooks/version_reminder.py) · verifiable |
| <br /> | ~30ms Python per Edit/Write; ~40 tokens only on template edit |
| **BULD-03** Story points | 0.5–10 per update, effort/time not LOC; logged in `VERSIONS` array, shown via "📋 SP history" modal |
| <br /> | Hook [`version_reminder.py`](.claude/hooks/version_reminder.py) · mixed |
| <br /> | shares BULD-02's hook spawn; no extra cost |
| **REPO-02** Branch | work from `main`; merge back immediately — never strand work on a side branch |
| <br /> | Context · verifiable |
| <br /> | ~15 always-on tokens; no runtime |
| **WORD-01** Terminology | `revenue` = turnover/apyvarta · `estimatedIncome` = revenue/spėjamos pajamos |
| <br /> | Context · judgment |
| <br /> | ~15 always-on tokens; no runtime |

### LOW

| Rule | Description |
| --- | --- |
| **WORD-02** Explanation length | keep explanatory blurbs 5–15 words; doesn't apply to deliberately long docstrings (e.g. the mechanistic hook headers) |
| <br /> | Context · judgment |
| <br /> | ~20 always-on tokens; no runtime |
| **CONV-01** Brevity | answer simple conversational questions in 5–15 words; no preamble |
| <br /> | Context · judgment |
| <br /> | ~15 always-on tokens; no runtime |


---

---

# Project context

## Project idea

- Self-contained HTML competitor dashboard: **113 LT** communication/marketing/consulting agencies, financials **2019–2024**.
- Built by **Adomas** working under (<g@cool.lt>) account for a company **Fabula**.
- Source: rekvizitai.vz.lt export `Komunikacija-konsultacija-konkurentai.xlsx`.
- **Fabula = Fabula ir partneriai, UAB** — formerly *Viešųjų ryšių partneriai (VRP)*, code **124099127**, founded 1997-07-03; same entity, rebranded. Its `brand` = `Fabula`.
- Fabula gets special treatment: own section at top, gold highlight in charts, pinned explorer row.

## Files & build

- `template.html` — source of all HTML/CSS/JS; placeholders `__DATA__` + `__SHEETS_DATA__`. **Edit this.**
- `data.json` — 660 records (113 brands × 2019–2024).
- `sheets_data.json` — 7 raw Excel sheets (Data Explorer source).
- `build_site.py` — injects both JSONs into template → `index.html`.
- `index.html` — generated, self-contained (Chart.js CDN). **The deliverable; never hand-edit.**
- `fabula.html` — standalone Fabula profile page (off-dashboard one-off; not linked from the app).
- Workflow: edit template → `python3 build_site.py` → `node --check` the JS → commit + push `main` → send `index.html`.

## Data dictionary (data.json record)

- Fields: `company`, `brand` (the key everywhere), `year`, `activities` (Media, Digital media, Kūryba, PR, PA, BTL, Production house, Konsultantai, Renginiai), `city`, `risk` (LT labels: Žemiausia/Žema/Vidutinė/…), `employees`, `avgSalary` (€/mo), `salaryCosts`, `revenue`, `profit` (net / grynasis pelnas), `nonSalaryCosts`, `estimatedIncome`.
- **Terminology (decided v0.1.2.0):**
  - `revenue` = **turnover / apyvarta** (incl. pass-through media ad spend).
  - `estimatedIncome` = **revenue / spėjamos pajamos** (fee income, pass-through excluded); 625/660 records have it. 2024: €362M turnover vs €100M est. income.
  - UI labels: "Turnover (apyvarta)" = `revenue`; "Revenue (spėjamos pajamos)" = `estimatedIncome`.
  - **Margins computed from `estimatedIncome`**, labelled "margin from revenue".

## Environment

- `rekvizitai.vz.lt` blocked by the sandbox (WebFetch + curl fail); company facts verified via web search.
- Repo private → no free GitHub Pages deploy; used as a local file.
- Branches: `main` (canonical) + historical `claude/`\*.

## Open / deferred

- "Key insights" texts still quote **turnover** figures (€362M etc.) — rewrite to spėjamos pajamos only if asked.
- Old `claude/`\* branches not deleted.

## Prompt & version history

- Moved to [VersionHistory.md](VersionHistory.md) to keep SessionStart context lean. Append new entries there.

