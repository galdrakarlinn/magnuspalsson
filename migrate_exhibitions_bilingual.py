#!/usr/bin/env python3
"""
Migrate exhibitions in works.json to bilingual format by matching with exhibitions translation files.
"""

import json
from pathlib import Path

def load_json(filepath):
    """Load JSON file with UTF-8 encoding"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath, data):
    """Save JSON file with UTF-8 encoding"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def normalize_title(title):
    """Normalize title for matching - remove bilingual parts in parentheses and extra whitespace"""
    # Remove content in parentheses that looks like translations
    import re
    # Remove patterns like (EITTHVAÐ úr ENGU – ...)
    title = re.sub(r'\s*\([^)]*\)\s*', ' ', title)
    # Normalize whitespace
    title = ' '.join(title.split())
    return title.strip()

def build_exhibition_mapping():
    """Build mapping from English exhibitions to Icelandic translations"""
    ex_en = load_json('translations/exhibitions-en.json')
    ex_is = load_json('translations/exhibitions-is.json')

    mapping = {}
    normalized_mapping = {}  # For fuzzy matching

    # Process solo exhibitions
    for ex_en_item, ex_is_item in zip(ex_en.get('solo', []), ex_is.get('solo', [])):
        if ex_en_item.get('year') == ex_is_item.get('year'):
            year = str(ex_en_item.get('year', ''))
            title_en_full = ex_en_item.get('title', '').strip()
            title_en_normalized = normalize_title(title_en_full)

            trans = {
                'title_en': title_en_full,
                'title_is': ex_is_item.get('title', '').strip(),
                'venue_is': ex_is_item.get('venue', '').strip(),
                'location': ex_is_item.get('location', ex_en_item.get('location', '')).strip()
            }

            # Exact match key
            key = (title_en_full, year)
            mapping[key] = trans

            # Normalized match key
            norm_key = (title_en_normalized.lower(), year)
            normalized_mapping[norm_key] = trans

    # Process group exhibitions
    for ex_en_item, ex_is_item in zip(ex_en.get('group', []), ex_is.get('group', [])):
        if ex_en_item.get('year') == ex_is_item.get('year'):
            year = str(ex_en_item.get('year', ''))
            title_en_full = ex_en_item.get('title', '').strip()
            title_en_normalized = normalize_title(title_en_full)

            trans = {
                'title_en': title_en_full,
                'title_is': ex_is_item.get('title', '').strip(),
                'venue_is': ex_is_item.get('venue', '').strip(),
                'location': ex_is_item.get('location', ex_en_item.get('location', '')).strip()
            }

            key = (title_en_full, year)
            mapping[key] = trans

            norm_key = (title_en_normalized.lower(), year)
            normalized_mapping[norm_key] = trans

    return mapping, normalized_mapping

def migrate_work_exhibitions(works_data, exact_mapping, normalized_mapping):
    """Migrate exhibitions in works to bilingual format"""

    matched_count = 0
    unmatched_count = 0
    unmatched_exhibitions = []

    for work in works_data['works']:
        exhibitions = work.get('exhibitions', [])
        if not exhibitions:
            continue

        new_exhibitions = []

        for ex in exhibitions:
            # Skip string format exhibitions
            if isinstance(ex, str):
                new_exhibitions.append(ex)
                continue

            # Get current values - check if already bilingual
            if isinstance(ex.get('title'), dict):
                # Already migrated, skip
                new_exhibitions.append(ex)
                continue

            title_en = ex.get('title', '').strip()
            venue_en = ex.get('venue', '').strip()
            year = ex.get('year', '')
            location = ex.get('location', ex.get('city', '')).strip()

            # Try exact match first
            key = (title_en, str(year))
            trans = exact_mapping.get(key)

            # Try normalized match if exact failed
            if not trans:
                norm_key = (normalize_title(title_en).lower(), str(year))
                trans = normalized_mapping.get(norm_key)

            if trans:
                # Found translation!
                new_ex = {
                    'title': {
                        'en': title_en,
                        'is': trans['title_is']
                    },
                    'venue': {
                        'en': venue_en,
                        'is': trans['venue_is']
                    },
                    'location': trans['location'] if trans['location'] else location,
                    'year': year
                }
                matched_count += 1
            else:
                # No translation found - keep English only for now
                new_ex = {
                    'title': {
                        'en': title_en,
                        'is': title_en  # Fallback to English
                    },
                    'venue': {
                        'en': venue_en,
                        'is': venue_en  # Fallback to English
                    },
                    'location': location,
                    'year': year
                }
                unmatched_count += 1
                unmatched_exhibitions.append(f"{title_en} ({year}) at {venue_en}")

            new_exhibitions.append(new_ex)

        work['exhibitions'] = new_exhibitions

    return works_data, matched_count, unmatched_count, unmatched_exhibitions

def main():
    print("Migrating exhibitions in works.json to bilingual format...")

    # Build translation mapping
    print("\nBuilding exhibition translation mapping...")
    exact_mapping, normalized_mapping = build_exhibition_mapping()
    print(f"Found translations for {len(exact_mapping)} exhibitions (exact) and {len(normalized_mapping)} (normalized)")

    # Load works.json
    print("\nLoading works.json...")
    works_data = load_json('works.json')
    print(f"Loaded {len(works_data['works'])} works")

    # Backup original
    print("\nCreating backup...")
    save_json('backups/works.json.pre-bilingual-exhibitions', works_data)

    # Migrate
    print("\nMigrating exhibitions...")
    works_data, matched, unmatched, unmatched_list = migrate_work_exhibitions(works_data, exact_mapping, normalized_mapping)

    # Save result
    print("\nSaving updated works.json...")
    save_json('works.json', works_data)

    print(f"\nMigration complete!")
    print(f"  Matched exhibitions: {matched}")
    print(f"  Unmatched exhibitions: {unmatched}")

    if unmatched_list:
        print(f"\nUnmatched exhibitions (using English as fallback):")
        for ex in unmatched_list[:10]:
            print(f"  - {ex}")
        if len(unmatched_list) > 10:
            print(f"  ... and {len(unmatched_list) - 10} more")

if __name__ == '__main__':
    main()
