# Scraping rekvizitai.vz.lt

> **Status: done (v53).** Scraper + parser live in `scripts/`, output in `data/rek.csv`
> + the `Rek` sheet of `data/sheets_data.json`. Kept as a reference for re-running
> or scraping another company.

## What it covers

A company on rekvizitai.vz.lt is split across separate tab URLs, not in-page
panels. The pipeline scrapes the four data tabs (Ataskaitos is a paywall, skipped):

| Tab | URL suffix | Yields |
| --- | --- | --- |
| Įmonė | `/` | codes, contacts, manager, address, LinkedIn, risk, export, Sodra debt |
| Finansai | `/apyvarta/` | 2021–2025 statement: sales, profit, margins, equity, assets, liabilities |
| Darbuotojai | `/darbuotoju-skaicius/` | headcount + annual average |
| Skolos | `/skolos/` | registered-debt status, debt-change records, credit check |

## Steps

### 1. Install dependencies
```bash
pip install playwright beautifulsoup4
playwright install chromium
```

### 2. Scrape all tabs
```bash
python3 scripts/scrape_6_vijos.py
```
Saves one HTML file per tab to `data/raw/6_vijos_<tab>.html` (gitignored — multi-MB intermediates).

### 3. Parse → CSV + Data Explorer sheet
```bash
python3 scripts/parse_6_vijos.py
```
`scripts/parse_6_vijos.py`:
- Reads every `data/raw/6_vijos_<tab>.html`
- Runs the right extractor per tab — label/value `<table>` rows, the Finansai
  metric×year grid, and targeted prose facts (headcount / debt)
- Writes `data/rek.csv` with columns **`tab, field, value`** (SSOT)
- Mirrors the same rows into the `Rek` sheet of `data/sheets_data.json` so the
  Data Explorer renders them

### 4. Rebuild, commit, push
```bash
python3 src/build_site.py
git add data/rek.csv data/sheets_data.json scripts/ index.html src/template.html
git commit -m "vN REPO-01 | scrape all 6_vijos tabs into rek.csv | N sp"
git push origin main
```

## Goal
The "Rek" tab in the Data Explorer (`src/template.html`) renders the `Rek` sheet —
re-run the pipeline to refresh it. To scrape another company, change `BASE`/`TABS`
in `scrape_6_vijos.py` and the file keys in `parse_6_vijos.py`.
