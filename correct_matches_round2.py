#!/usr/bin/env python3
"""
Correct matches round 2:
1. Remove #29, #32, #63 from truly_new_works (they are correct matches)
2. Add #32 Hundar (Dogs) to new works (different from #31 Hundljóð)
3. Remove edda_text_works_ancestry_malmo_1978 from works (it's an exhibition)
"""

import json
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
NEW_WORKS = PROJECT_DIR / "truly_new_works_corrected.json"
WORKS_JSON = PROJECT_DIR / "works.json"

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    print("Correct Matches - Round 2")
    print("="*80)

    # Load data
    new_works_data = load_json(NEW_WORKS)
    works_data = load_json(WORKS_JSON)

    # Remove correct matches from new works (#29, #32 Hundljóð, #63)
    correct_matches = ['29', '32', '63']
    original_count = len(new_works_data)

    removed_works = []
    for num in correct_matches:
        work = next((w for w in new_works_data if w.get('number') == num), None)
        if work:
            removed_works.append(f"#{num} {work.get('title_en', '')}")
            new_works_data = [w for w in new_works_data if w.get('number') != num]

    print(f"Removed {len(removed_works)} correct matches from truly_new_works:")
    for w in removed_works:
        print(f"  - {w}")
    print()

    # Add #32 Hundar (Dogs) to new works
    hundar_work = {
        "number": "32",
        "title_en": "Hundar (Dogs)",
        "year": "1970",
        "materials": [
            "plaster, plastic, paper, clothes"
        ],
        "dimensions": "42 x 31 x 21 cm",
        "location": "private collections and the artist",
        "details": [],
        "title_is": "Hundar",
        "materials_is": [
            "gifs, plast, pappír, föt"
        ],
        "dimensions_is": "42 x 31 x 21 cm",
        "location_is": "einkasöfn og listamaðurinn",
        "details_is": []
    }

    new_works_data.append(hundar_work)
    print(f"Added #32 Hundar (Dogs) to new works")
    print(f"  Note: #31 Hundljóð (Dog Poem) is the existing work")
    print(f"  Note: #32 Hundar (Dogs) is a new, different work")
    print()

    # Sort by number
    new_works_data.sort(key=lambda x: int(x['number']) if x['number'].isdigit() else 0)

    # Remove Edda 1978 from works
    original_works_count = len(works_data['works'])
    edda_work = next((w for w in works_data['works'] if w['id'] == 'edda_text_works_ancestry_malmo_1978'), None)

    if edda_work:
        works_data['works'] = [w for w in works_data['works'] if w['id'] != 'edda_text_works_ancestry_malmo_1978']
        print(f"Removed 'Edda 1978' (edda_text_works_ancestry_malmo_1978) from works")
        print(f"  Reason: This is a group exhibition, not a work")
        print(f"  Note: Should be added to group exhibitions list instead")
        print()

    # Save
    print("="*80)
    print("Saving corrected files...")
    save_json(NEW_WORKS, new_works_data)
    save_json(WORKS_JSON, works_data)
    print("SUCCESS!")
    print()

    # Summary
    print("="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Removed correct matches: {len(removed_works)}")
    for w in removed_works:
        print(f"  - {w}")
    print()
    print(f"Added new work: #32 Hundar (Dogs)")
    print()
    print(f"Removed Edda 1978 exhibition from works: {1 if edda_work else 0}")
    print()
    print(f"Truly new works now: {len(new_works_data)}")
    print(f"Total works now: {len(works_data['works'])}")

if __name__ == '__main__':
    main()
