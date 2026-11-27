#!/usr/bin/env python3
"""
Update all works with book thumbnails from thumbnail_mapping_bilingual.json
- Update titles (EN and IS)
- Update dimensions
- Update materials
- Update ownership/location
This is the source of truth from the book publication.
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

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def parse_materials(materials_list):
    """Convert materials list to proper format"""
    if not materials_list:
        return []
    # Clean up materials
    result = []
    for mat in materials_list:
        if mat and mat.strip():
            result.append(mat.strip())
    return result

def update_work_from_thumbnail(work, thumb_data):
    """Update work with data from thumbnail mapping"""
    updated_fields = []

    # Update title
    if thumb_data.get('title_en') or thumb_data.get('title_is'):
        work['title'] = {
            'en': thumb_data.get('title_en', ''),
            'is': thumb_data.get('title_is', '')
        }
        updated_fields.append('title')

    # Update year (only if provided in thumbnail data)
    if thumb_data.get('year'):
        work['year'] = thumb_data['year']
        updated_fields.append('year')

    # Update dimensions
    if thumb_data.get('dimensions'):
        work['dimensions'] = thumb_data['dimensions']
        updated_fields.append('dimensions')

    # Update materials
    materials_en = parse_materials(thumb_data.get('materials', []))
    materials_is = parse_materials(thumb_data.get('materials_is', []))

    if materials_en or materials_is:
        work['materials'] = {}
        if materials_en:
            work['materials']['en'] = materials_en
        if materials_is:
            work['materials']['is'] = materials_is
        updated_fields.append('materials')

    # Update ownership/location
    location_en = thumb_data.get('location', '').strip()
    location_is = thumb_data.get('location_is', '').strip()

    if location_en or location_is:
        if 'ownership' not in work:
            work['ownership'] = {}

        if location_en:
            work['ownership']['owner'] = location_en
            work['ownership']['owner_en'] = location_en
        if location_is:
            work['ownership']['owner_is'] = location_is

        updated_fields.append('ownership')

    return work, updated_fields

def main():
    print("Update Works from Book Publication Data")
    print("="*80)
    print("Source of truth: thumbnail_mapping_bilingual.json")
    print("="*80)

    # Load data
    works_data = load_json(WORKS_JSON)
    thumbnail_data_list = load_json(THUMBNAIL_DATA)

    # Create thumbnail lookup
    thumb_data_map = {t['number']: t for t in thumbnail_data_list}

    # Load match report to get the mappings
    # Format: Match Type,Thumb#,Thumb Title EN,Thumb Year,Work ID,Work Title EN,Work Year,Score,Action Needed
    matches = []
    with open(MATCH_REPORT, 'r', encoding='utf-8') as f:
        lines = f.readlines()[1:]  # Skip header
        for line in lines:
            parts = line.strip().split(',')
            if len(parts) >= 5 and parts[0].upper() == 'EXACT':
                thumb_num = parts[1]
                work_id = parts[4]
                matches.append((thumb_num, work_id))

    print(f"Found {len(matches)} exact matches to update\n")

    # Update works
    updated_count = 0
    all_updates = {}

    for thumb_num, work_id in matches:
        thumb_data = thumb_data_map.get(thumb_num)
        if not thumb_data:
            print(f"WARNING: No thumbnail data for #{thumb_num}")
            continue

        # Find work
        work_idx = None
        for i, w in enumerate(works_data['works']):
            if w['id'] == work_id:
                work_idx = i
                break

        if work_idx is None:
            print(f"WARNING: Work {work_id} not found")
            continue

        # Update work
        work = works_data['works'][work_idx]
        updated_work, updated_fields = update_work_from_thumbnail(work, thumb_data)
        works_data['works'][work_idx] = updated_work

        if updated_fields:
            updated_count += 1
            all_updates[work_id] = updated_fields
            print(f"#{thumb_num} - {work_id}")
            print(f"  Title: {updated_work['title']['en']} / {updated_work['title']['is']}")
            print(f"  Updated: {', '.join(updated_fields)}")
            print()

    # Save
    if updated_count > 0:
        print("="*80)
        print(f"Saving works.json with {updated_count} updated works...")
        save_json(WORKS_JSON, works_data)
        print("SUCCESS!")

        # Print summary
        print("\nUpdated fields summary:")
        field_counts = {}
        for fields in all_updates.values():
            for field in fields:
                field_counts[field] = field_counts.get(field, 0) + 1

        for field, count in sorted(field_counts.items()):
            print(f"  {field}: {count} works")
    else:
        print("No works to update")

    print(f"\nTotal works updated: {updated_count}")

if __name__ == '__main__':
    main()
