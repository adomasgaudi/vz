#!/usr/bin/env python3
"""Build data.html with embedded sheet data from sheets_data.json."""
import json

with open('sheets_data.json', encoding='utf-8') as f:
    data = json.load(f)

html = open('data_template.html', encoding='utf-8').read()
html = html.replace('__SHEETS_DATA__', json.dumps(data, ensure_ascii=False))

with open('data.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("data.html built,", len(html), "bytes")
