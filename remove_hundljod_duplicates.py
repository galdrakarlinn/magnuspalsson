#!/usr/bin/env python3
"""
Remove duplicate hundljóð entries from works.json, keeping only the hundar-dogs-1970 work.
"""

import json

def remove_hundljod_duplicates():
    """Remove standalone hundljóð entries from works.json."""

    # Read the current works.json
    with open('works.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Track what we're removing
    original_count = len(data['works'])
    removed_works = []

    # Filter out standalone hundljóð works
    filtered_works = []

    for work in data['works']:
        work_id = work.get('id', '')
        work_title = work.get('title', '')

        # Remove standalone hundljóð entries (but keep hundar-dogs-1970)
        if work_id in ['hundljod', 'hundljod_1990']:
            removed_works.append(f"{work_title} ({work.get('year', 'Unknown year')})")
            print(f"Removing duplicate: {work_title} (ID: {work_id})")
        else:
            filtered_works.append(work)

    # Update the data
    data['works'] = filtered_works

    # Write the updated JSON back
    with open('works.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Print summary
    print(f"\nSummary:")
    print(f"Original works count: {original_count}")
    print(f"Works removed: {len(removed_works)}")
    print(f"Final works count: {len(filtered_works)}")
    print(f"Removed works: {', '.join(removed_works)}")

    print(f"\nKeeping: hundar-dogs-1970 work which includes hundljóð references")

    return len(removed_works) > 0

if __name__ == "__main__":
    if remove_hundljod_duplicates():
        print("\nworks.json has been updated to remove duplicate hundljóð entries.")
    else:
        print("\nNo duplicate hundljóð entries found.")