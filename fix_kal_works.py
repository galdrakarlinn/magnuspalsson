#!/usr/bin/env python3
"""
Fix Kál works:
1. Remove kal-1-1963 (titled "Kál 1-4")
2. Rename kal_series_1963_66 to just "Kál" / "Cabbage"
3. Add series tag
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
    print("Fix Kál Works - Cleanup")
    print("="*80)

    # Load works
    works_data = load_json(WORKS_JSON)

    # Remove kal-1-1963 (titled "Kál 1-4")
    original_count = len(works_data['works'])
    works_data['works'] = [w for w in works_data['works'] if w['id'] != 'kal-1-1963']
    removed_count = original_count - len(works_data['works'])

    if removed_count > 0:
        print(f"Removed 'kal-1-1963' (Kál 1-4) from works.json")
        print()

    # Update kal_series_1963_66
    for work in works_data['works']:
        if work['id'] == 'kal_series_1963_66':
            # Update title
            work['title'] = {
                'en': 'Cabbage',
                'is': 'Kál'
            }

            # Add series tag
            if 'tags' not in work:
                work['tags'] = []
            if 'series' not in work['tags']:
                work['tags'].append('series')

            print(f"Updated kal_series_1963_66:")
            print(f"  Title EN: {work['title']['en']}")
            print(f"  Title IS: {work['title']['is']}")
            print(f"  Added tag: series")
            print()
            break

    # Save
    print("="*80)
    print("Saving works.json...")
    save_json(WORKS_JSON, works_data)
    print("SUCCESS!")
    print()

    # Summary
    print("="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Removed works: {removed_count}")
    print(f"Renamed Kál series work: 1")
    print(f"Total works now: {len(works_data['works'])}")

if __name__ == '__main__':
    main()
