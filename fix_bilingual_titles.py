#!/usr/bin/env python3
"""
Fix bilingual titles in thumbnail_mapping_bilingual.json
Extract Icelandic titles from English title field when they're in parentheses
Sync with works.json titles where possible
"""

import json
import re
from pathlib import Path

# Paths
PROJECT_DIR = Path(__file__).parent
THUMBNAIL_DATA = PROJECT_DIR / "thumbnail_mapping_bilingual.json"
WORKS_JSON = PROJECT_DIR / "works.json"
MATCH_REPORT = PROJECT_DIR / "thumbnail_match_report.csv"

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def extract_titles_from_parentheses(title_en):
    """
    Extract Icelandic and English titles from format like:
    "Sólúr (Sundial)" -> ("Sundial", "Sólúr")
    "Hundljóð (Dog Poem)" -> ("Dog Poem", "Hundljóð")
    """
    # Pattern: "Icelandic (English)" or "English (Icelandic)"
    match = re.match(r'^(.+?)\s*\((.+?)\)$', title_en)
    if match:
        part1 = match.group(1).strip()
        part2 = match.group(2).strip()

        # Check which part is likely Icelandic (contains ð, þ, æ, ö, á, etc.)
        icelandic_chars = set('áðéíóúýþæö')
        part1_is_icelandic = any(c.lower() in icelandic_chars for c in part1)
        part2_is_icelandic = any(c.lower() in icelandic_chars for c in part2)

        if part1_is_icelandic and not part2_is_icelandic:
            return (part2, part1)  # (English, Icelandic)
        elif part2_is_icelandic and not part1_is_icelandic:
            return (part1, part2)  # (English, Icelandic)
        else:
            # Both or neither have Icelandic chars, assume first is Icelandic
            return (part2, part1)

    return None

def main():
    print("Fix Bilingual Titles in Thumbnail Mapping")
    print("="*80)

    # Load data
    thumbnail_data_list = load_json(THUMBNAIL_DATA)
    works_data = load_json(WORKS_JSON)
    works_map = {w['id']: w for w in works_data['works']}

    # Load matches to sync with works.json
    import csv
    thumb_to_work = {}
    with open(MATCH_REPORT, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if len(row) >= 5 and row[0].upper() in ['EXACT', 'PARTIAL']:
                thumb_to_work[row[1]] = row[4]

    fixed_count = 0
    synced_count = 0

    for i, thumb in enumerate(thumbnail_data_list):
        thumb_num = thumb.get('number', '')
        title_en = thumb.get('title_en', '')
        title_is = thumb.get('title_is', '')

        print(f"\n#{thumb_num} - {title_en}")

        # First, try to sync with works.json if there's a match
        work_id = thumb_to_work.get(thumb_num)
        if work_id and work_id in works_map:
            work = works_map[work_id]
            work_title_en = work.get('title', {}).get('en', '')
            work_title_is = work.get('title', {}).get('is', '')

            if work_title_en and work_title_is:
                # Use titles from works.json
                thumb['title_en'] = work_title_en
                thumb['title_is'] = work_title_is
                print(f"  SYNCED with work {work_id}")
                print(f"    EN: {work_title_en}")
                print(f"    IS: {work_title_is}")
                synced_count += 1
                thumbnail_data_list[i] = thumb
                continue

        # If not synced, try to extract from parentheses
        if not title_is or not title_is.strip():
            extracted = extract_titles_from_parentheses(title_en)
            if extracted:
                new_en, new_is = extracted
                thumb['title_en'] = new_en
                thumb['title_is'] = new_is
                print(f"  EXTRACTED from parentheses")
                print(f"    EN: {new_en}")
                print(f"    IS: {new_is}")
                fixed_count += 1
                thumbnail_data_list[i] = thumb

    # Save
    print(f"\n{'='*80}")
    print(f"Saving thumbnail_mapping_bilingual.json...")
    save_json(THUMBNAIL_DATA, thumbnail_data_list)
    print("SUCCESS!")

    print(f"\nSynced with works.json: {synced_count}")
    print(f"Extracted from parentheses: {fixed_count}")
    print(f"Total updated: {synced_count + fixed_count}")

if __name__ == '__main__':
    main()
