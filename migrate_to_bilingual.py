#!/usr/bin/env python3
"""
Migrate works.json to include bilingual content from translation files.
This merges en.json and is.json into works.json so we have a single source of truth.
"""

import json
import sys

def load_json(filepath):
    """Load and parse a JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath, data):
    """Save data to a JSON file with pretty formatting."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def migrate_works():
    """Merge translation files into works.json."""
    print("Loading files...")
    works_data = load_json('works.json')
    en_data = load_json('translations/en.json')
    is_data = load_json('translations/is.json')

    print(f"Loaded {len(works_data['works'])} works")
    print(f"Loaded {len(en_data['works'])} English translations")
    print(f"Loaded {len(is_data['works'])} Icelandic translations")

    # Create lookup dictionaries for translations
    en_works = en_data['works']
    is_works = is_data['works']

    migrated_count = 0
    missing_translations = []

    # Process each work
    for work in works_data['works']:
        work_id = work['id']

        # Get translations for this work
        en_trans = en_works.get(work_id)
        is_trans = is_works.get(work_id)

        if not en_trans or not is_trans:
            missing_translations.append(work_id)
            print(f"  Warning: Missing translations for {work_id}")
            continue

        # Migrate title
        work['title'] = {
            'en': en_trans.get('title', work.get('title', '')),
            'is': is_trans.get('title', work.get('title', ''))
        }

        # Migrate description
        work['description'] = {
            'en': en_trans.get('description', work.get('description', '')),
            'is': is_trans.get('description', work.get('description', ''))
        }

        # Migrate materials (if they exist in translations)
        if 'materials' in en_trans or 'materials' in is_trans:
            work['materials'] = {
                'en': en_trans.get('materials', work.get('materials', [])),
                'is': is_trans.get('materials', work.get('materials', []))
            }

        # Migrate image captions
        if 'images' in work and work['images']:
            en_images = en_trans.get('images', [])
            is_images = is_trans.get('images', [])

            for i, img in enumerate(work['images']):
                if i < len(en_images) and i < len(is_images):
                    # Store captions as bilingual object
                    img['caption'] = {
                        'en': en_images[i].get('caption', img.get('caption', '')),
                        'is': is_images[i].get('caption', img.get('caption', ''))
                    }

        migrated_count += 1

    print(f"\nMigration complete!")
    print(f"  Migrated: {migrated_count} works")
    print(f"  Missing translations: {len(missing_translations)}")

    if missing_translations:
        print(f"  Works without complete translations: {', '.join(missing_translations[:5])}")
        if len(missing_translations) > 5:
            print(f"  ... and {len(missing_translations) - 5} more")

    # Save migrated data
    output_file = 'works-bilingual.json'
    print(f"\nSaving to {output_file}...")
    save_json(output_file, works_data)
    print(f"Saved successfully!")

    # Calculate file size
    import os
    size_kb = os.path.getsize(output_file) / 1024
    print(f"New file size: {size_kb:.1f} KB")

    return works_data

if __name__ == '__main__':
    try:
        migrate_works()
        print("\n✓ Migration completed successfully!")
        print("  Review works-bilingual.json before replacing works.json")
    except Exception as e:
        print(f"\n✗ Error during migration: {e}", file=sys.stderr)
        sys.exit(1)
