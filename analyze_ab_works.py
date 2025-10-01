#!/usr/bin/env python3
"""
Analyze the A and B works to understand what we need to process next.
"""

import os
import glob

def analyze_ab_works():
    """Analyze the available A and B works and their contents."""

    base_path = r"C:\Users\VeigaMagnusdottir\projects\magnusPalsson\images-not-used"

    # Get all A and B folders (and files that might be individual works)
    all_items = os.listdir(base_path)
    ab_items = [item for item in all_items if item[0].upper() in ['A', 'B']]

    print(f"Found {len(ab_items)} A & B items to analyze:")
    print("=" * 80)

    work_data = []

    for item_name in sorted(ab_items):
        item_path = os.path.join(base_path, item_name)

        if os.path.isdir(item_path):
            # Count image files
            image_files = []
            for ext in ['*.jpg', '*.jpeg', '*.png', '*.tif', '*.tiff']:
                image_files.extend(glob.glob(os.path.join(item_path, ext)))

            # Count other files
            other_files = []
            for ext in ['*.pdf', '*.mp3', '*.mp4', '*.mov', '*.txt', '*.wav']:
                other_files.extend(glob.glob(os.path.join(item_path, ext)))

            # Extract potential year from folder name
            year = "Unknown"
            for word in item_name.split():
                if word.isdigit() and len(word) == 4 and word.startswith(('19', '20')):
                    year = word
                    break
                elif '-' in word and any(part.isdigit() and len(part) == 4 for part in word.split('-')):
                    # Handle ranges like 1970-74
                    parts = word.split('-')
                    for part in parts:
                        if part.isdigit() and len(part) == 4:
                            year = part
                            break

            work_info = {
                'name': item_name,
                'path': item_path,
                'images': len(image_files),
                'other_files': len(other_files),
                'year': year,
                'image_list': [os.path.basename(f) for f in image_files[:5]]  # First 5 for preview
            }

            work_data.append(work_info)

            print(f"{item_name}")
            print(f"  Year: {year}")
            print(f"  Images: {len(image_files)} | Other files: {len(other_files)}")
            if image_files:
                print(f"  Sample images: {', '.join(work_info['image_list'])}")
            print()
        else:
            # Single file - might be orphaned
            print(f"{item_name} - SINGLE FILE")
            print()

    print("=" * 80)
    print(f"SUMMARY:")
    print(f"Total works to process: {len(work_data)}")
    print(f"Works with images: {len([w for w in work_data if w['images'] > 0])}")
    print(f"Works with no images: {len([w for w in work_data if w['images'] == 0])}")

    # Suggest processing order
    print(f"\nSUGGESTED PROCESSING ORDER:")
    quick = [w for w in work_data if 1 <= w['images'] <= 5]
    medium = [w for w in work_data if 6 <= w['images'] <= 15]
    complex = [w for w in work_data if w['images'] > 15]

    print(f"1. Quick wins (1-5 images): {len(quick)}")
    if quick:
        for w in quick:
            print(f"   - {w['name']} ({w['year']}) - {w['images']} images")

    print(f"2. Medium works (6-15 images): {len(medium)}")
    if medium:
        for w in medium:
            print(f"   - {w['name']} ({w['year']}) - {w['images']} images")

    print(f"3. Complex works (15+ images): {len(complex)}")
    if complex:
        for w in complex:
            print(f"   - {w['name']} ({w['year']}) - {w['images']} images")

    return work_data

if __name__ == "__main__":
    works = analyze_ab_works()