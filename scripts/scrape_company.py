#!/usr/bin/env python3
"""Scrape any rekvizitai.vz.lt company — all data tabs. Run locally.

    python3 scripts/scrape_company.py <slug>
    e.g. python3 scripts/scrape_company.py adell_reklama

<slug> is the path segment in https://rekvizitai.vz.lt/imone/<slug>/. Each
company page is split across separate tab URLs (not in-page panels); we visit
each and save its rendered HTML to data/raw/<slug>_<tab>.html. Then run
parse_company.py <slug> to extract it into data/rek_tabs.json.

Tvarumas / Atsiliepimai link to generic site pages (not company-specific) and
the Ataskaitos tab is a paywall, so the four data tabs below are the useful ones.
"""
import asyncio, os, sys

# Windows consoles default to cp1252 and choke on Lithuanian chars; force UTF-8.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from playwright.async_api import async_playwright

# tab key -> URL path under the company base ('/' = the default Įmonė overview)
TABS = {
    "imone":        "/",                      # Įmonė (overview: codes, contacts, manager)
    "finansai":     "/apyvarta/",             # Finansai (turnover / revenue / statement)
    "darbuotojai":  "/darbuotoju-skaicius/",  # Darbuotojai (headcount over time)
    "skolos":       "/skolos/",               # Skolos (VMI / Sodra debt history)
    "ataskaitos":   "/ataskaita/",            # Ataskaitos (paywall report — kept for completeness)
}

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "raw")


async def scrape(slug):
    base = f"https://rekvizitai.vz.lt/imone/{slug}"
    os.makedirs(OUT_DIR, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        for key, path in TABS.items():
            url = base + path
            print(f"Loading [{key}] {url} ...")
            try:
                await page.goto(url, wait_until="networkidle", timeout=45000)
                await asyncio.sleep(2)
            except Exception as e:
                print(f"   ! load problem ({e}); saving whatever rendered")
            html = await page.content()
            out = os.path.join(OUT_DIR, f"{slug}_{key}.html")
            with open(out, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"   saved {len(html):>8} bytes -> {os.path.relpath(out)}")
        await browser.close()
    print(f"\n=== Tabs saved. Next: python3 scripts/parse_company.py {slug} ===")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: python3 scripts/scrape_company.py <slug>  (e.g. adell_reklama)")
    asyncio.run(scrape(sys.argv[1]))
