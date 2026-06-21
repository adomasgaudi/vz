#!/usr/bin/env python3
"""Scrape 6 vijos, MB from rekvizitai.vz.lt — all company tabs. Run locally.

The company page is split across separate URLs (one per tab), not in-page
panels. We visit each and save its rendered HTML to data/raw/6_vijos_<tab>.html.
parse_6_vijos.py then reads every file and merges into data/rek.csv.

Tvarumas / Atsiliepimai link to generic site pages (not company-specific), so
they are skipped here — the four data tabs below are the company ones.
"""
import asyncio, os, sys

# Windows consoles default to cp1252 and choke on Lithuanian chars; force UTF-8.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from playwright.async_api import async_playwright

BASE = "https://rekvizitai.vz.lt/imone/6_vijos"
# tab key -> URL path under BASE ('' = the default Įmonė overview page)
TABS = {
    "imone":        "/",                      # Įmonė (overview: codes, contacts, manager)
    "finansai":     "/apyvarta/",             # Finansai (turnover / revenue)
    "darbuotojai":  "/darbuotoju-skaicius/",  # Darbuotojai (headcount over years)
    "skolos":       "/skolos/",               # Skolos (debts: Sodra etc.)
    "ataskaitos":   "/ataskaita/",            # Ataskaitos (reports)
}

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "raw")


async def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        for key, path in TABS.items():
            url = BASE + path
            print(f"Loading [{key}] {url} ...")
            try:
                await page.goto(url, wait_until="networkidle", timeout=45000)
                await asyncio.sleep(2)
            except Exception as e:
                print(f"   ! load problem ({e}); saving whatever rendered")
            html = await page.content()
            out = os.path.join(OUT_DIR, f"6_vijos_{key}.html")
            with open(out, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"   saved {len(html):>8} bytes -> {os.path.relpath(out)}")
        await browser.close()
    print("\n=== All tabs saved. Next: python3 scripts/parse_6_vijos.py ===")


asyncio.run(main())
