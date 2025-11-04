#!/usr/bin/env python3
"""
Convert works.json exhibitions from full data to ID references
by matching with exhibitions.json
"""

import json

def normalize_string(s):
    """Normalize string for comparison"""
    if not s:
        return ""
    return s.lower().strip()

def find_exhibition_id(work_ex, all_exhibitions):
    """Find matching exhibition ID from exhibitions.json"""

    # Get work exhibition data
    work_title_en = ""
    work_venue_en = ""
    work_year = str(work_ex.get('year', ''))

    if isinstance(work_ex.get('title'), dict):
        work_title_en = work_ex['title'].get('en', '')
    else:
        work_title_en = work_ex.get('title', '')

    if isinstance(work_ex.get('venue'), dict):
        work_venue_en = work_ex['venue'].get('en', '')
    else:
        work_venue_en = work_ex.get('venue', '')

    # Try to find exact match by title + year
    for ex_list in [all_exhibitions['solo'], all_exhibitions['group']]:
        for ex in ex_list:
            ex_title = ex['title'].get('en', '') if isinstance(ex['title'], dict) else ex['title']
            ex_year = str(ex.get('year', ''))

            if normalize_string(ex_title) == normalize_string(work_title_en) and ex_year == work_year:
                return ex['id']

    # Try fuzzy match (title contains or starts with)
    for ex_list in [all_exhibitions['solo'], all_exhibitions['group']]:
        for ex in ex_list:
            ex_title = ex['title'].get('en', '') if isinstance(ex['title'], dict) else ex['title']
            ex_year = str(ex.get('year', ''))

            work_norm = normalize_string(work_title_en)
            ex_norm = normalize_string(ex_title)

            if ex_year == work_year and (work_norm in ex_norm or ex_norm in work_norm):
                return ex['id']

    return None

def convert_works_exhibitions():
    """Convert all works to use exhibition ID references"""

    # Load exhibitions
    print("Loading exhibitions.json...")
    with open('exhibitions.json', 'r', encoding='utf-8') as f:
        exhibitions = json.load(f)

    # Load works
    print("Loading works.json...")
    with open('works.json', 'r', encoding='utf-8') as f:
        works = json.load(f)

    # Backup
    print("Creating backup...")
    with open('backups/works.json.pre-exhibition-ids', 'w', encoding='utf-8') as f:
        json.dump(works, f, indent=2, ensure_ascii=False)

    matched_count = 0
    unmatched_count = 0
    unmatched_list = []

    # Process each work
    print(f"\nProcessing {len(works['works'])} works...")
    for work in works['works']:
        if not work.get('exhibitions'):
            continue

        new_exhibitions = []

        for ex in work['exhibitions']:
            # Skip string format
            if isinstance(ex, str):
                print(f"  WARNING: String exhibition in {work['id']}: {ex}")
                continue

            # Try to match with exhibitions.json
            ex_id = find_exhibition_id(ex, exhibitions)

            if ex_id:
                new_exhibitions.append(ex_id)
                matched_count += 1
            else:
                # Keep original data if no match found
                unmatched_count += 1
                title = ex.get('title', {}).get('en', '') if isinstance(ex.get('title'), dict) else ex.get('title', '')
                year = ex.get('year', '')
                unmatched_list.append(f"{work['id']}: {title} ({year})")

                # Keep the full exhibition object for now
                new_exhibitions.append(ex)

        work['exhibitions'] = new_exhibitions

    # Save updated works.json
    print("\nSaving updated works.json...")
    with open('works.json', 'w', encoding='utf-8') as f:
        json.dump(works, f, indent=2, ensure_ascii=False)

    print(f"\nConversion complete!")
    print(f"  Matched: {matched_count} exhibitions converted to IDs")
    print(f"  Unmatched: {unmatched_count} exhibitions kept as full objects")

    if unmatched_list:
        print(f"\nUnmatched exhibitions (kept as objects):")
        for item in unmatched_list[:10]:
            print(f"  - {item}")
        if len(unmatched_list) > 10:
            print(f"  ... and {len(unmatched_list) - 10} more")

if __name__ == '__main__':
    convert_works_exhibitions()
