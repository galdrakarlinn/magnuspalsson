#!/usr/bin/env python3

import json
import os
import re

def update_image_url(url, work_name):
    """Convert URL from main directory to medium/ directory"""
    # Pattern: images/work-name/file.jpg -> images/work-name/medium/file-medium.jpg
    if f'images/{work_name}/' in url and '/medium/' not in url:
        # Extract the filename
        filename = os.path.basename(url)
        name, ext = os.path.splitext(filename)

        # Create medium filename
        medium_filename = f"{name}-medium{ext}"

        # Create new URL
        new_url = f"images/{work_name}/medium/{medium_filename}"
        return new_url
    return url

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
                    if work_name in medium_works and '/medium/' not in url:
                        # Check if medium file exists
                        filename = os.path.basename(url)
                        name, ext = os.path.splitext(filename)
                        medium_filename = f"{name}-medium{ext}"
                        medium_file_path = f"images/{work_name}/medium/{medium_filename}"

                        if os.path.exists(medium_file_path):
                            new_url = update_image_url(url, work_name)
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

    # Save the updated JSON
    with open('works.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Updated works.json saved successfully")

    # Print works that were updated
    print("\nWorks updated:")
    for work in sorted(works_updated):
        print(f"  - {work}")

if __name__ == '__main__':
    main()