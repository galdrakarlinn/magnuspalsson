#!/usr/bin/env python3
"""
Script to add ownership information to works.json for works that are missing it.
This moves hardcoded ownership data from works.js into the JSON file.
"""

import json

# Read works.json
with open('works.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Ownership information from works.js getOwnershipInfo()
ownership_additions = {
    'bestu_stykkin': {
        'owner': 'The Living Art Museum (Nýlistasafnið)',
        'url': 'https://sarpur.is/Adfang.aspx?AdfangID=1396243',
        'catalogNumber': 'N-277'
    },
    'vidtol_um_daudann_2011': {
        'owner': 'National Gallery of Iceland (Listasafn Íslands)',
        'url': 'https://www.listasafn.is/list/safneign/li-8249/',
        'catalogNumber': 'LÍ-8249'
    }
}

# Add ownership to works that don't have it
for work in data['works']:
    if work['id'] in ownership_additions and 'ownership' not in work:
        work['ownership'] = ownership_additions[work['id']]
        print(f"Added ownership info to: {work['id']}")

# Write back to works.json
with open('works.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Ownership information added successfully!")
