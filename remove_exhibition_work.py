#!/usr/bin/env python3
"""
Remove spud-kling-og-bang-2012 from works.json (it's an exhibition, not a work)
Add exhibition tags to the actual Spud and Walking on Water works
"""

import json
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
WORKS_JSON = PROJECT_DIR / "works.json"

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    print("Remove Exhibition from Works - Cleanup")
    print("="*80)

    # Load works
    works_data = load_json(WORKS_JSON)

    # Find and remove spud-kling-og-bang-2012
    original_count = len(works_data['works'])
    works_data['works'] = [w for w in works_data['works'] if w['id'] != 'spud-kling-og-bang-2012']
    removed_count = original_count - len(works_data['works'])

    if removed_count > 0:
        print(f"Removed 'spud-kling-og-bang-2012' from works.json")
        print("This is an exhibition, not a work - already exists in solo exhibitions")
        print()

    # Add exhibition info to Spud and Walking on Water
    spud_work = next((w for w in works_data['works'] if w['id'] == 'spud-bern-mp-rg-ob-1998'), None)
    walking_work = next((w for w in works_data['works'] if w['id'] == 'walking-on-water-2012'), None)

    updated_works = []

    if spud_work:
        # Add exhibition tag
        if 'exhibitions' not in spud_work:
            spud_work['exhibitions'] = []

        exhibition_ref = "kling-og-bang-2012"
        if exhibition_ref not in spud_work['exhibitions']:
            spud_work['exhibitions'].append(exhibition_ref)
            print(f"Added Kling og Bang 2012 exhibition to Spud")
            updated_works.append('Spud')

    if walking_work:
        # Add exhibition tag
        if 'exhibitions' not in walking_work:
            walking_work['exhibitions'] = []

        exhibition_ref = "kling-og-bang-2012"
        if exhibition_ref not in walking_work['exhibitions']:
            walking_work['exhibitions'].append(exhibition_ref)
            print(f"Added Kling og Bang 2012 exhibition to Walking on Water")
            updated_works.append('Walking on Water')

    # Save
    if removed_count > 0 or updated_works:
        print()
        print("="*80)
        print("Saving works.json...")
        save_json(WORKS_JSON, works_data)
        print("SUCCESS!")
        print()

    # Summary
    print("="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Removed exhibition entries: {removed_count}")
    print(f"Updated works with exhibition tags: {len(updated_works)}")
    if updated_works:
        for work in updated_works:
            print(f"  - {work}")
    print()
    print(f"Total works now: {len(works_data['works'])}")

if __name__ == '__main__':
    main()
