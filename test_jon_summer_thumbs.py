#!/usr/bin/env python3
"""
Test script to verify Jon Summer thumbnail paths and file existence.
"""

import os
import json

def test_jon_summer_thumbs():
    """Test Jon Summer thumbnail generation and file existence."""

    # Read works.json
    with open('works.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Find Jon Summer work
    jon_summer_work = None
    for work in data['works']:
        if work.get('id') == 'jon_summer_2008_2022':
            jon_summer_work = work
            break

    if not jon_summer_work:
        print("ERROR: Jon Summer work not found in works.json")
        return

    print(f"OK: Found work: {jon_summer_work['title']}")
    print(f"Work ID: {jon_summer_work['id']}")

    # Check each image and its expected thumbnail
    for i, image in enumerate(jon_summer_work.get('images', [])):
        medium_url = image['url']
        print(f"\nImage {i+1}: {medium_url}")

        # Simulate the JavaScript getThumbPath logic
        if '/medium/' in medium_url:
            parts = medium_url.split('/')
            filename = parts[-1]

            # Extract base name (remove -medium suffix)
            if '-medium.' in filename:
                file_base = filename.replace('-medium.', '.').split('.')[0]
            else:
                file_base = filename.split('.')[0]

            # Create thumbnail path
            path_parts = parts[:-1]  # Remove filename
            for j, part in enumerate(path_parts):
                if part == 'medium':
                    path_parts[j] = 'thumbs'
                    break

            thumb_path = '/'.join(path_parts) + '/' + file_base + '-thumb.jpg'
            print(f"Expected thumbnail: {thumb_path}")

            # Check if thumbnail file exists
            if os.path.exists(thumb_path):
                print(f"OK: Thumbnail exists: {thumb_path}")
            else:
                print(f"ERROR: Thumbnail missing: {thumb_path}")

        # Check if medium file exists
        if os.path.exists(medium_url):
            print(f"OK: Medium file exists: {medium_url}")
        else:
            print(f"ERROR: Medium file missing: {medium_url}")

if __name__ == "__main__":
    test_jon_summer_thumbs()