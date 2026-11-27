#!/usr/bin/env python3
"""
Update all works that have book thumbnails with metadata from thumbnail_mapping_bilingual.json
Phase 4: Sync dimensions, materials, ownership from book data (source of truth)
"""

import json
from pathlib import Path

# Paths
PROJECT_DIR = Path(__file__).parent
WORKS_JSON = PROJECT_DIR / "works.json"
THUMBNAIL_DATA = PROJECT_DIR / "thumbnail_mapping_bilingual.json"

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def find_thumbnail_for_work(work, thumbnail_data_list):
    """Find the thumbnail number that matches this work"""
    if 'images' not in work:
        return None

    for img in work.get('images', []):
        url = img.get('url', '')
        if 'book-thumbnail' in url:
            # This work has a book thumbnail, now find which one
            # Look through thumbnail_data to find matches by title/year
            work_title_en = work.get('title', {}).get('en', '').lower()
            work_title_is = work.get('title', {}).get('is', '').lower()
            work_year = str(work.get('year', ''))

            for thumb in thumbnail_data_list:
                thumb_title_en = thumb.get('title_en', '').lower()
                thumb_title_is = thumb.get('title_is', '').lower()
                thumb_year = str(thumb.get('year', ''))

                # Check if titles match
                title_match = (
                    (work_title_en and thumb_title_en and work_title_en in thumb_title_en) or
                    (work_title_en and thumb_title_en and thumb_title_en in work_title_en) or
                    (work_title_is and thumb_title_is and work_title_is in thumb_title_is) or
                    (work_title_is and thumb_title_is and thumb_title_is in work_title_is)
                )

                # Check if years match or overlap
                year_match = work_year in thumb_year or thumb_year in work_year

                if title_match and year_match:
                    return thumb['number']

            return None

    return None

def update_work_from_thumbnail(work, thumb_data):
    """Update work with data from thumbnail mapping (source of truth)"""
    updated_fields = []

    # Update title if more complete in book
    if thumb_data.get('title_en') and thumb_data.get('title_is'):
        old_title_en = work.get('title', {}).get('en', '')
        old_title_is = work.get('title', {}).get('is', '')
        new_title_en = thumb_data.get('title_en', '')
        new_title_is = thumb_data.get('title_is', '')

        if new_title_en != old_title_en or new_title_is != old_title_is:
            work['title'] = {
                'en': new_title_en,
                'is': new_title_is
            }
            updated_fields.append('title')

    # Update year if exists
    if thumb_data.get('year'):
        thumb_year = str(thumb_data.get('year'))
        work_year = str(work.get('year', ''))
        if thumb_year != work_year:
            work['year'] = thumb_year
            updated_fields.append('year')

    # Update dimensions if exists and more complete
    if thumb_data.get('dimensions'):
        thumb_dims = thumb_data.get('dimensions', '').strip()
        work_dims = work.get('dimensions', '')
        if thumb_dims and (not work_dims or len(thumb_dims) > len(str(work_dims))):
            work['dimensions'] = thumb_dims
            updated_fields.append('dimensions')

    # Update materials (EN and IS)
    if thumb_data.get('materials') or thumb_data.get('materials_is'):
        materials_en = thumb_data.get('materials', [])
        materials_is = thumb_data.get('materials_is', [])

        if materials_en or materials_is:
            if 'materials' not in work:
                work['materials'] = {}

            if materials_en:
                work['materials']['en'] = materials_en
                updated_fields.append('materials_en')

            if materials_is:
                work['materials']['is'] = materials_is
                updated_fields.append('materials_is')

    # Update ownership/location
    if thumb_data.get('location') or thumb_data.get('location_is'):
        location_en = thumb_data.get('location', '').strip()
        location_is = thumb_data.get('location_is', '').strip()

        if location_en or location_is:
            if 'ownership' not in work:
                work['ownership'] = {}

            if location_en:
                work['ownership']['owner_en'] = location_en
                updated_fields.append('ownership_en')

            if location_is:
                work['ownership']['owner_is'] = location_is
                updated_fields.append('ownership_is')

    return work, updated_fields

def main():
    print("Update All Book Thumbnail Works - Phase 4")
    print("="*80)
    print("Syncing metadata from thumbnail_mapping_bilingual.json (source of truth)")
    print()

    # Load data
    works_data = load_json(WORKS_JSON)
    thumbnail_data_list = load_json(THUMBNAIL_DATA)

    # Create thumbnail lookup by number
    thumb_data_map = {t['number']: t for t in thumbnail_data_list}

    updated_count = 0
    all_updates = {}

    for i, work in enumerate(works_data['works']):
        # Check if work has book thumbnail
        has_book_thumb = any('book-thumbnail' in img.get('url', '') for img in work.get('images', []))

        if not has_book_thumb:
            continue

        # Find which thumbnail this is
        thumb_num = find_thumbnail_for_work(work, thumbnail_data_list)

        if not thumb_num:
            continue

        thumb_data = thumb_data_map.get(thumb_num)
        if not thumb_data:
            continue

        # Update work with thumbnail data
        work, updated_fields = update_work_from_thumbnail(work, thumb_data)

        if updated_fields:
            works_data['works'][i] = work
            updated_count += 1

            work_id = work.get('id', 'unknown')
            all_updates[work_id] = updated_fields

            print(f"#{thumb_num} -> {work_id}")
            print(f"  Updated: {', '.join(updated_fields)}")
            print()

    # Save
    if updated_count > 0:
        print("="*80)
        print(f"Saving works.json with {updated_count} updated works...")
        save_json(WORKS_JSON, works_data)
        print("SUCCESS!")
        print()

    # Summary
    print("="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Works with book thumbnails updated: {updated_count}")

    # Count field updates
    field_counts = {}
    for fields in all_updates.values():
        for field in fields:
            field_counts[field] = field_counts.get(field, 0) + 1

    if field_counts:
        print()
        print("Fields updated:")
        for field, count in sorted(field_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {field}: {count} works")

if __name__ == '__main__':
    main()
