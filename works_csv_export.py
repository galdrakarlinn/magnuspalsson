#!/usr/bin/env python3
"""
Export works.json to CSV for Excel editing, and import back.
"""

import json
import csv
from pathlib import Path

def get_localized_value(field, lang):
    """Extract value from bilingual field"""
    if not field:
        return ''
    if isinstance(field, dict):
        return field.get(lang, '')
    return str(field)

def get_materials_string(materials, lang):
    """Convert materials to comma-separated string"""
    if not materials:
        return ''
    if isinstance(materials, dict) and (lang in materials or 'en' in materials or 'is' in materials):
        mat = materials.get(lang, materials.get('en', materials.get('is', [])))
        if isinstance(mat, list):
            return ', '.join(mat)
        return str(mat)
    if isinstance(materials, list):
        return ', '.join(materials)
    return str(materials)

def export_to_csv():
    """Export works.json to CSV"""
    with open('works.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    works = data['works']

    # CSV columns
    fieldnames = [
        'id',
        'title_en',
        'title_is',
        'year',
        'dimensions',
        'materials_en',
        'materials_is',
        'contentStatus',
        'mediaStatus'
    ]

    with open('works_export.csv', 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()

        for work in works:
            if isinstance(work, str):
                continue

            row = {
                'id': work.get('id', ''),
                'title_en': get_localized_value(work.get('title'), 'en'),
                'title_is': get_localized_value(work.get('title'), 'is'),
                'year': work.get('year', ''),
                'dimensions': work.get('dimensions') or '',
                'materials_en': get_materials_string(work.get('materials'), 'en'),
                'materials_is': get_materials_string(work.get('materials'), 'is'),
                'contentStatus': work.get('contentStatus', ''),
                'mediaStatus': work.get('mediaStatus', '')
            }
            writer.writerow(row)

    print(f"Exported {len(works)} works to works_export.csv")
    print("Note: CSV uses semicolon (;) delimiter for Excel compatibility")

def import_from_csv():
    """Import CSV back to works.json, updating only the editable fields"""
    # Load existing works.json
    with open('works.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    works = data['works']
    works_by_id = {w.get('id'): w for w in works if isinstance(w, dict)}

    # Read CSV
    updated_count = 0
    with open('works_export.csv', 'r', encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f, delimiter=';')

        for row in reader:
            work_id = row.get('id', '').strip()
            if not work_id or work_id not in works_by_id:
                print(f"Skipping unknown work: {work_id}")
                continue

            work = works_by_id[work_id]

            # Update title
            title_en = row.get('title_en', '').strip()
            title_is = row.get('title_is', '').strip()
            if title_en or title_is:
                if not isinstance(work.get('title'), dict):
                    work['title'] = {}
                if title_en:
                    work['title']['en'] = title_en
                if title_is:
                    work['title']['is'] = title_is

            # Update year
            year = row.get('year', '').strip()
            if year:
                try:
                    work['year'] = int(year)
                except ValueError:
                    work['year'] = year

            # Update dimensions
            dimensions = row.get('dimensions', '').strip()
            work['dimensions'] = dimensions if dimensions else None

            # Update materials
            materials_en = row.get('materials_en', '').strip()
            materials_is = row.get('materials_is', '').strip()
            if materials_en or materials_is:
                if not isinstance(work.get('materials'), dict):
                    work['materials'] = {'en': [], 'is': []}
                if materials_en:
                    work['materials']['en'] = [m.strip() for m in materials_en.split(',')]
                if materials_is:
                    work['materials']['is'] = [m.strip() for m in materials_is.split(',')]

            # Update status fields
            content_status = row.get('contentStatus', '').strip()
            if content_status:
                work['contentStatus'] = content_status

            media_status = row.get('mediaStatus', '').strip()
            if media_status:
                work['mediaStatus'] = media_status

            updated_count += 1

    # Save updated works.json
    with open('works.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Updated {updated_count} works in works.json")

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python works_csv_export.py export  - Export to CSV")
        print("  python works_csv_export.py import  - Import from CSV")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == 'export':
        export_to_csv()
    elif command == 'import':
        import_from_csv()
    else:
        print(f"Unknown command: {command}")
        print("Use 'export' or 'import'")
