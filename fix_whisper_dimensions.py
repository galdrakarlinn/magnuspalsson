#!/usr/bin/env python3
"""
Fix dimensions for Hvískur/Whisper 1, 2, 3 works
CSV shows: 1. 9.5 x 14.5 x 11.3 cm; 2. 9.5 x 14.5 x 55 cm; 3. 9.5 x 14.5 x 150 cm

Each work should have its own dimensions:
- Whisper 1: 9.5 x 14.5 x 11.3 cm (smallest)
- Whisper 2: 9.5 x 14.5 x 55 cm (medium)
- Whisper 3: 9.5 x 14.5 x 150 cm (largest)
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
    print("Fix Hvískur/Whisper Dimensions")
    print("="*80)

    # Load works
    works_data = load_json(WORKS_JSON)

    # Correct dimensions for each
    dimensions = {
        'hviskur_whisper_1_1975': '9.5 x 14.5 x 11.3 cm',
        'hviskur_whisper_2_1975': '9.5 x 14.5 x 55 cm',
        'hviskur_whisper_3_1975': '9.5 x 14.5 x 150 cm'
    }

    updated = 0

    for work_id, correct_dim in dimensions.items():
        for idx, work in enumerate(works_data['works']):
            if work['id'] == work_id:
                old_dim = work.get('dimensions', '')
                work['dimensions'] = correct_dim

                print(f"{work_id}:")
                print(f"  Title: {work.get('title', {}).get('en', '')}")
                print(f"  Old dimensions: {old_dim}")
                print(f"  New dimensions: {correct_dim}")
                print()

                works_data['works'][idx] = work
                updated += 1
                break

    # Save
    if updated > 0:
        print("="*80)
        print("Saving works.json...")
        save_json(WORKS_JSON, works_data)
        print("SUCCESS!")
        print()

    # Summary
    print("="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Updated dimensions for {updated} works")
    print()
    print("Correct dimensions from CSV:")
    print("  Whisper 1: 9.5 x 14.5 x 11.3 cm (smallest)")
    print("  Whisper 2: 9.5 x 14.5 x 55 cm (medium)")
    print("  Whisper 3: 9.5 x 14.5 x 150 cm (largest)")

if __name__ == '__main__':
    main()
