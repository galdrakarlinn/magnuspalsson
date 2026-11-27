#!/usr/bin/env python3
"""
Apply data suggestions from works.json to thumbnail_mapping_bilingual.json
"""

import json
from pathlib import Path

# Paths
PROJECT_DIR = Path(__file__).parent
THUMBNAIL_DATA = PROJECT_DIR / "thumbnail_mapping_bilingual.json"
SUGGESTIONS = PROJECT_DIR / "data_suggestions.json"

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    print("Apply Data Suggestions to Thumbnail Mapping")
    print("="*80)

    # Load data
    thumbnail_data_list = load_json(THUMBNAIL_DATA)
    suggestions = load_json(SUGGESTIONS)

    # Create thumbnail lookup
    thumb_data_map = {t['number']: i for i, t in enumerate(thumbnail_data_list)}

    updated_count = 0

    for suggestion in suggestions:
        thumb_num = suggestion['thumb_num']
        data = suggestion['data']

        thumb_idx = thumb_data_map.get(thumb_num)
        if thumb_idx is None:
            print(f"WARNING: Thumbnail #{thumb_num} not found")
            continue

        thumb = thumbnail_data_list[thumb_idx]

        print(f"#{thumb_num} - {thumb.get('title_en', 'N/A')}")

        # Apply materials_en
        if 'materials_en' in data:
            if not thumb.get('materials') or len(thumb.get('materials', [])) == 0:
                thumb['materials'] = data['materials_en']
                print(f"  + materials_en: {data['materials_en']}")

        # Apply materials_is
        if 'materials_is' in data:
            if not thumb.get('materials_is') or len(thumb.get('materials_is', [])) == 0:
                thumb['materials_is'] = data['materials_is']
                print(f"  + materials_is: {data['materials_is']}")

        # Apply location_en
        if 'location_en' in data:
            if not thumb.get('location') or not thumb.get('location').strip():
                thumb['location'] = data['location_en']
                print(f"  + location_en: {data['location_en']}")

        # Apply location_is
        if 'location_is' in data:
            if not thumb.get('location_is') or not thumb.get('location_is').strip():
                thumb['location_is'] = data['location_is']
                print(f"  + location_is: {data['location_is']}")

        # Apply dimensions
        if 'dimensions' in data:
            if not thumb.get('dimensions') or not thumb.get('dimensions').strip():
                thumb['dimensions'] = data['dimensions']
                thumb['dimensions_is'] = data['dimensions']  # Same for both languages
                print(f"  + dimensions: {data['dimensions']}")

        # Apply title_is (if any)
        if 'title_is' in data:
            if not thumb.get('title_is'):
                thumb['title_is'] = data['title_is']
                print(f"  + title_is: {data['title_is']}")

        thumbnail_data_list[thumb_idx] = thumb
        updated_count += 1
        print()

    # Save
    print("="*80)
    print(f"Saving thumbnail_mapping_bilingual.json with {updated_count} updates...")
    save_json(THUMBNAIL_DATA, thumbnail_data_list)
    print("SUCCESS!")

if __name__ == '__main__':
    main()
