#!/usr/bin/env python3
"""
Correct Icelandic matches - remove wrong ones
#106 Litlar myndir is NOT Watercolours
#111 is Göngur (Round Ups), not Spud
"""

import json
from pathlib import Path

PROJECT_DIR = Path(__file__).parent

# Load data
with open(PROJECT_DIR / "icelandic_rematches.json", 'r', encoding='utf-8') as f:
    matches = json.load(f)

with open(PROJECT_DIR / "truly_new_works.json", 'r', encoding='utf-8') as f:
    new_works = json.load(f)

with open(PROJECT_DIR / "thumbnail_mapping_bilingual.json", 'r', encoding='utf-8') as f:
    all_thumbs = json.load(f)

# Remove #106 and #111 from matches
corrected_matches = [m for m in matches if m['thumb_num'] not in ['106', '111']]

print(f"Removed 2 incorrect matches")
print(f"Corrected matches: {len(corrected_matches)}")

# Add #106 and #111 back to new works
thumb_106 = next((t for t in all_thumbs if t['number'] == '106'), None)
thumb_111 = next((t for t in all_thumbs if t['number'] == '111'), None)

if thumb_106:
    new_works.append(thumb_106)
    print(f"Added #106 back to new works: {thumb_106.get('title_en')}")

if thumb_111:
    # Update title for #111 to be Göngur
    thumb_111['title_en'] = 'Göngur (Round Ups)'
    thumb_111['title_is'] = 'Göngur'
    new_works.append(thumb_111)
    print(f"Added #111 back to new works as Göngur: {thumb_111.get('title_en')}")

# Sort new works by number
new_works.sort(key=lambda x: int(x['number']) if x['number'].isdigit() else 0)

# Save corrected versions
with open(PROJECT_DIR / "icelandic_rematches_corrected.json", 'w', encoding='utf-8') as f:
    json.dump(corrected_matches, f, indent=2, ensure_ascii=False)

with open(PROJECT_DIR / "truly_new_works_corrected.json", 'w', encoding='utf-8') as f:
    json.dump(new_works, f, indent=2, ensure_ascii=False)

print(f"\nFinal count:")
print(f"  Corrected matches: {len(corrected_matches)}")
print(f"  Truly new works: {len(new_works)}")
print(f"\nSaved to:")
print(f"  - icelandic_rematches_corrected.json")
print(f"  - truly_new_works_corrected.json")
