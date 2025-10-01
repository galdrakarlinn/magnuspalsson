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

    # Track works that need updating
    works_to_update = []
    already_updated = []

    # Check each work in the JSON
    for work in data['works']:
        if 'images' in work:
            work_needs_update = False
            work_name = None

            # Check if any image URL references a work with medium/ folder
            for image in work['images']:
                url = image['url']
                # Extract work name from URL pattern: images/work-name/file.jpg
                match = re.match(r'images/([^/]+)/', url)
                if match:
                    work_name = match.group(1)
                    if work_name in medium_works:
                        # Check if it's already using medium/
                        if '/medium/' not in url:
                            work_needs_update = True
                        break

            if work_name:
                if work_needs_update:
                    works_to_update.append(work_name)
                elif work_name in medium_works:
                    already_updated.append(work_name)

    print(f"Works that need updating: {len(works_to_update)}")
    print(f"Works already updated: {len(already_updated)}")

    # Print the works that need updating
    print("\nWorks needing update:")
    for work in sorted(works_to_update):
        print(f"  - {work}")

    print("\nWorks already updated:")
    for work in sorted(already_updated):
        print(f"  - {work}")

if __name__ == '__main__':
    main()