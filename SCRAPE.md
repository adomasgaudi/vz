# Scraping rekvizitai.vz.lt

## Task for local Claude (VS Code)

Run the scraper for `6 vijos, MB`, parse the output, build a structured CSV, and commit it.

## Steps

### 1. Install dependencies
```bash
pip install playwright beautifulsoup4
playwright install chromium
```

### 2. Run the scraper
```bash
python3 scrape_6_vijos.py
```
This saves `6_vijos_raw.html` in the repo root.

### 3. Parse the HTML and build a CSV

Write a new script `parse_6_vijos.py` that:
- Reads `6_vijos_raw.html`
- Extracts every field visible on the page (financials, contacts, employees, addresses, risk, activities, etc.)
- Saves the result as `rek.csv` in the repo root
- Prints a summary of what was extracted

The HTML structure of rekvizitai.vz.lt company pages uses standard `<table>` elements and labeled `<dt>`/`<dd>` pairs. Parse all of them — don't cherry-pick.

### 4. Commit and push
```bash
git add rek.csv parse_6_vijos.py
git commit -m "v++ REPO-01 | scrape 6_vijos from rekvizitai.vz.lt into rek.csv"
git push origin main
```

## Goal
Once `rek.csv` exists and looks good, the web Claude session will add a "Rek" tab to the Data Explorer in `template.html` that renders it.
