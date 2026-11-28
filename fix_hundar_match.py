#!/usr/bin/env python3
"""
Fix Hundar (Dogs) work:
- hundur_adrir_1971 on website is actually #32 Hundar from thumbnail mapping
- Update title from "Dogs other / Hundur aðrir" to "Dogs / Hundar"
- Update year from 1968 to 1970
- Add thumbnail #32 to this existing work
- Remove #32 from truly_new_works (it's a correct match)
"""

import json
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
WORKS_JSON = PROJECT_DIR / "works.json"
NEW_WORKS = PROJECT_DIR / "truly_new_works_corrected.json"

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    print("Fix Hundar (Dogs) Match")
    print("="*80)

    # Load data
    works_data = load_json(WORKS_JSON)
    new_works_data = load_json(NEW_WORKS)

    # Find hundur_adrir_1971
    work_idx = None
    for idx, w in enumerate(works_data['works']):
        if w['id'] == 'hundur_adrir_1971':
            work_idx = idx
            break

    if work_idx is None:
        print("ERROR: hundur_adrir_1971 not found")
        return

    work = works_data['works'][work_idx]

    print(f"Found work: {work['id']}")
    print(f"  Current title: {work['title']['en']} / {work['title']['is']}")
    print(f"  Current year: {work['year']}")
    print()

    # Update title
    work['title'] = {
        'en': 'Dogs',
        'is': 'Hundar'
    }

    # Update year
    work['year'] = 1970

    print(f"Updated to match #32 from thumbnail mapping:")
    print(f"  New title: {work['title']['en']} / {work['title']['is']}")
    print(f"  New year: {work['year']}")
    print()

    works_data['works'][work_idx] = work

    # Remove #32 from truly_new_works
    original_count = len(new_works_data)
    new_works_data = [w for w in new_works_data if w.get('number') != '32']
    removed = original_count - len(new_works_data)

    if removed > 0:
        print(f"Removed #32 Hundar from truly_new_works (correct match found)")
        print()

    # Save
    print("="*80)
    print("Saving files...")
    save_json(WORKS_JSON, works_data)
    save_json(NEW_WORKS, new_works_data)
    print("SUCCESS!")
    print()

    # Summary
    print("="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Updated hundur_adrir_1971:")
    print(f"  Title: 'Dogs other' → 'Dogs' / 'Hundur aðrir' → 'Hundar'")
    print(f"  Year: 1968 → 1970")
    print()
    print(f"Removed #32 from truly_new_works: {removed}")
    print(f"Truly new works now: {len(new_works_data)}")
    print()
    print("Note: This is a correct match - hundur_adrir_1971 is #32 Hundar")

if __name__ == '__main__':
    main()
