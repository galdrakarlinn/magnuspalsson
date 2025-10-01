#!/usr/bin/env python3
"""
Fix broken image references in works.json by removing entries that point to missing files.
"""

import json
import os
import sys

def file_exists(file_path):
    """Check if a file exists."""
    return os.path.isfile(file_path)

def fix_works_json():
    """Remove broken image references from works.json."""

    # Read the current works.json
    with open('works.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Track statistics
    total_images = 0
    removed_images = 0
    works_processed = 0
    works_removed = 0

    # Process each work
    works_to_keep = []

    for work in data['works']:
        works_processed += 1

        # Filter images to keep only those that exist
        if 'images' in work:
            valid_images = []

            for image in work['images']:
                total_images += 1
                url = image.get('url', '')

                # Check if the file exists
                if file_exists(url):
                    valid_images.append(image)
                else:
                    removed_images += 1
                    print(f"Removing broken reference: {url}")

            # Update the work's images
            work['images'] = valid_images

        # Only keep works that have at least one valid image or have no images field
        if 'images' not in work or len(work['images']) > 0:
            works_to_keep.append(work)
        else:
            works_removed += 1
            print(f"Removing work with no valid images: {work.get('title', 'Unknown')}")

    # Update the data
    data['works'] = works_to_keep

    # Write the fixed JSON back
    with open('works.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Print summary
    print(f"\nSummary:")
    print(f"Works processed: {works_processed}")
    print(f"Works removed: {works_removed}")
    print(f"Total image references: {total_images}")
    print(f"Broken references removed: {removed_images}")
    print(f"Valid references remaining: {total_images - removed_images}")

    return removed_images > 0

if __name__ == "__main__":
    if fix_works_json():
        print("\nworks.json has been updated to remove broken references.")
    else:
        print("\nNo broken references found.")