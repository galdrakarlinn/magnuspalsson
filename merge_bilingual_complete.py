#!/usr/bin/env python3
"""
Merge bilingual works (titles, descriptions) with bilingual exhibitions
"""

import json

def load_json(filepath):
    """Load JSON file with UTF-8 encoding"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath, data):
    """Save JSON file with UTF-8 encoding"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    print("Merging bilingual titles with bilingual exhibitions...")

    # Load both files
    bilingual_works = load_json('works-bilingual.json')  # Has bilingual titles/descriptions
    current_works = load_json('works.json')  # Has bilingual exhibitions

    # Build a map of exhibitions by work ID from current works
    exhibitions_map = {}
    for work in current_works['works']:
        exhibitions_map[work['id']] = work.get('exhibitions', [])

    # Update bilingual works with bilingual exhibitions
    for work in bilingual_works['works']:
        work_id = work['id']
        if work_id in exhibitions_map:
            work['exhibitions'] = exhibitions_map[work_id]

    # Save result
    print("Saving merged works.json...")
    save_json('works.json', bilingual_works)

    print("\nMerge complete!")
    print(f"Total works: {len(bilingual_works['works'])}")

    # Verify a sample
    sample = next((w for w in bilingual_works['works'] if w['id'] == 'walking-on-water-2012'), None)
    if sample:
        print("\nSample verification (Walking on Water):")
        print(f"  Title type: {type(sample['title'])}")
        if isinstance(sample['title'], dict):
            print(f"  Title EN: {sample['title'].get('en', 'N/A')}")
            print(f"  Title IS: {sample['title'].get('is', 'N/A')}")
        if sample.get('exhibitions') and len(sample['exhibitions']) > 0:
            ex = sample['exhibitions'][0]
            if isinstance(ex, dict):
                print(f"  First exhibition title type: {type(ex.get('title', ''))}")
                if isinstance(ex.get('title'), dict):
                    print(f"  Exhibition EN: {ex['title'].get('en', 'N/A')}")
                    print(f"  Exhibition IS: {ex['title'].get('is', 'N/A')}")

if __name__ == '__main__':
    main()
