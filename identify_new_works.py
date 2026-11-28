#!/usr/bin/env python3
"""
Identify which thumbnails need new works created
These are thumbnails that weren't matched or had wrong matches
"""

import json
from pathlib import Path
import csv

# Paths
PROJECT_DIR = Path(__file__).parent
WORKS_JSON = PROJECT_DIR / "works.json"
THUMBNAIL_DATA = PROJECT_DIR / "thumbnail_mapping_bilingual.json"
MATCH_REPORT = PROJECT_DIR / "thumbnail_match_report.csv"

# Thumbnails that have been successfully added to existing works
PROCESSED = {
    # Phase 1 exact matches (73)
    '1', '2', '3', '4', '5', '6', '7', '8', '10', '11', '13', '14', '21', '22', '23', '24',
    '25', '26', '27', '30', '31', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42',
    '43', '44', '45', '46', '47', '49', '50', '51', '52', '53', '54', '55', '57', '58', '59',
    '60', '61', '63', '65', '66', '67', '68', '69', '70', '71', '72', '73', '75', '76', '77',
    '81', '88', '124', '127', '129', '132', '138', '59', '62', '28', '74',
    # Phase 2 HIGH scores (20)
    '119', '126', '151', '148', '85', '96', '136', '86', '97', '143', '102',
    '89', '113', '128', '150', '107', '139', '100', '123', '147',
    # Phase 2 MEDIUM (7)
    '80', '104', '140', '115', '130', '133',
}

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    print("Identify Thumbnails Needing New Works - Phase 3")
    print("="*80)

    # Load data
    thumbnail_data_list = load_json(THUMBNAIL_DATA)
    works_data = load_json(WORKS_JSON)

    # Get all thumbnail numbers
    all_thumbs = {t['number'] for t in thumbnail_data_list}

    # Find unprocessed
    unprocessed = sorted(all_thumbs - PROCESSED, key=lambda x: int(x) if x.isdigit() else 0)

    print(f"Total thumbnails in book: {len(all_thumbs)}")
    print(f"Already added to website: {len(PROCESSED)}")
    print(f"Need new works: {len(unprocessed)}")
    print()

    # Print details for each
    print("="*80)
    print("THUMBNAILS NEEDING NEW WORKS:")
    print("="*80)

    new_works_list = []

    for thumb_num in unprocessed:
        thumb_data = next((t for t in thumbnail_data_list if t['number'] == thumb_num), None)
        if not thumb_data:
            continue

        title_en = thumb_data.get('title_en', 'N/A')
        title_is = thumb_data.get('title_is', 'N/A')
        year = thumb_data.get('year', 'N/A')
        materials = thumb_data.get('materials', [])
        dimensions = thumb_data.get('dimensions', 'N/A')

        print(f"#{thumb_num}: {title_en}")
        if title_is and title_is != 'N/A':
            print(f"  IS: {title_is}")
        print(f"  Year: {year}")
        if materials:
            print(f"  Materials: {', '.join(materials)}")
        if dimensions and dimensions != 'N/A':
            print(f"  Dimensions: {dimensions}")
        print()

        new_works_list.append({
            'thumb_num': thumb_num,
            'title_en': title_en,
            'title_is': title_is,
            'year': year,
            'materials': materials,
            'dimensions': dimensions
        })

    # Save to JSON for processing
    output_path = PROJECT_DIR / "new_works_to_create.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(new_works_list, f, indent=2, ensure_ascii=False)

    print("="*80)
    print(f"Saved list to: new_works_to_create.json")
    print(f"Total new works to create: {len(new_works_list)}")

if __name__ == '__main__':
    main()
