#!/usr/bin/env python3
"""
Extract missing data from works.json to fill thumbnail_mapping_bilingual.json
"""

import json
from pathlib import Path

# Paths
PROJECT_DIR = Path(__file__).parent
WORKS_JSON = PROJECT_DIR / "works.json"
THUMBNAIL_DATA = PROJECT_DIR / "thumbnail_mapping_bilingual.json"
MATCH_REPORT = PROJECT_DIR / "thumbnail_match_report.csv"

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    print("Extract Missing Data from works.json")
    print("="*80)

    # Load data
    works_data = load_json(WORKS_JSON)
    thumbnail_data_list = load_json(THUMBNAIL_DATA)

    # Create lookups
    thumb_data_map = {t['number']: t for t in thumbnail_data_list}
    works_map = {w['id']: w for w in works_data['works']}

    # Load matches
    matches = {}
    with open(MATCH_REPORT, 'r', encoding='utf-8') as f:
        lines = f.readlines()[1:]
        for line in lines:
            parts = line.strip().split(',')
            if len(parts) >= 5 and parts[0].upper() == 'EXACT':
                thumb_num = parts[1]
                work_id = parts[4]
                matches[thumb_num] = work_id

    # Thumbnails with missing data (from previous report)
    missing_thumbs = [
        "10", "13", "22", "30", "33", "34", "36", "37", "45", "50",
        "52", "53", "54", "61", "68", "69", "72", "75", "77", "81",
        "82", "88", "121", "124", "127", "129", "132", "138"
    ]

    print("Checking what data exists in works.json:\n")

    suggestions = []

    for thumb_num in missing_thumbs:
        thumb = thumb_data_map.get(thumb_num)
        work_id = matches.get(thumb_num)

        if not thumb or not work_id:
            continue

        work = works_map.get(work_id)
        if not work:
            continue

        print(f"#{thumb_num} - {thumb.get('title_en', 'N/A')}")
        print(f"  Work ID: {work_id}")

        # Check what's missing and what exists in works.json
        found_data = {}

        # Check materials_is
        if not thumb.get('materials_is') or len(thumb.get('materials_is', [])) == 0:
            work_materials_is = work.get('materials', {}).get('is', [])
            if work_materials_is:
                found_data['materials_is'] = work_materials_is
                print(f"  Found materials_is in work: {work_materials_is}")

        # Check materials_en
        if not thumb.get('materials') or len(thumb.get('materials', [])) == 0:
            work_materials_en = work.get('materials', {}).get('en', [])
            if work_materials_en:
                found_data['materials_en'] = work_materials_en
                print(f"  OK:Found materials_en in work: {work_materials_en}")

        # Check title_is
        if not thumb.get('title_is'):
            work_title_is = work.get('title', {}).get('is', '')
            if work_title_is:
                found_data['title_is'] = work_title_is
                print(f"  OK:Found title_is in work: {work_title_is}")

        # Check dimensions
        if not thumb.get('dimensions') or not thumb.get('dimensions').strip():
            work_dims = work.get('dimensions', '')
            if work_dims:
                found_data['dimensions'] = work_dims
                print(f"  OK:Found dimensions in work: {work_dims}")

        # Check location_is
        if not thumb.get('location_is') or not thumb.get('location_is').strip():
            work_owner_is = work.get('ownership', {}).get('owner_is', '')
            if work_owner_is:
                found_data['location_is'] = work_owner_is
                print(f"  OK:Found location_is in work: {work_owner_is}")

        # Check location_en
        if not thumb.get('location') or not thumb.get('location').strip():
            work_owner_en = work.get('ownership', {}).get('owner_en', '')
            if work_owner_en:
                found_data['location_en'] = work_owner_en
                print(f"  OK:Found location_en in work: {work_owner_en}")

        if found_data:
            suggestions.append({
                'thumb_num': thumb_num,
                'work_id': work_id,
                'data': found_data
            })
        else:
            print(f"  NO:No useful data found in works.json")

        print()

    # Print summary
    print("="*80)
    print(f"Found data in works.json for {len(suggestions)} thumbnails")
    print("="*80)

    # Save suggestions
    output_file = PROJECT_DIR / "data_suggestions.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(suggestions, f, indent=2, ensure_ascii=False)

    print(f"\nSuggestions saved to: data_suggestions.json")

if __name__ == '__main__':
    main()
