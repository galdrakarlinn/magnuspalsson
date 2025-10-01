#!/usr/bin/env python3

import json
import os
import re

def main():
    # Load the works.json file
    with open('works.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Get list of works with medium folders
    medium_works = []
    for work_dir in os.listdir('images'):
        medium_path = os.path.join('images', work_dir, 'medium')
        if os.path.isdir(medium_path):
            medium_works.append(work_dir)

    print(f"Found {len(medium_works)} works with medium/ folders")

    # Works we just optimized that need JSON updates
    newly_optimized_works = [
        'studios', 'hrognkelsaveifa-strandlegjan-1998',
        'hundar-dogs-1970', 'gibsborn-children-1971'
    ]

    # Track updates
    updates_made = 0
    works_updated = []

    # Update each work in the JSON
    for work in data['works']:
        if 'images' in work:
            work_updated = False
            work_name = None

            for image in work['images']:
                url = image['url']
                # Extract work name from URL
                match = re.match(r'images/([^/]+)/', url)
                if match:
                    work_name = match.group(1)

                    # Check if this work has medium folder and needs updating
                    if (work_name in medium_works and
                        '/medium/' not in url and
                        work_name in newly_optimized_works):

                        # Check if medium file exists with same name
                        filename = os.path.basename(url)
                        medium_file_path = f"images/{work_name}/medium/{filename}"

                        if os.path.exists(medium_file_path):
                            new_url = f"images/{work_name}/medium/{filename}"
                            print(f"Updating: {url} -> {new_url}")
                            image['url'] = new_url
                            updates_made += 1
                            work_updated = True
                        else:
                            print(f"WARNING: Medium file not found: {medium_file_path}")

            if work_updated and work_name not in works_updated:
                works_updated.append(work_name)

    print(f"\nTotal updates made: {updates_made}")
    print(f"Works updated: {len(works_updated)}")

    if updates_made > 0:
        # Create backup
        os.rename('works.json', 'works.json.backup-final')

        # Save the updated JSON
        with open('works.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print("Updated works.json saved successfully")
        print("Backup created as works.json.backup-final")
    else:
        print("No updates needed")

    # Print works that were updated
    if works_updated:
        print("\nWorks updated:")
        for work in sorted(works_updated):
            print(f"  - {work}")

if __name__ == '__main__':
    main()