#!/usr/bin/env python3
"""
Analyze the new K, L, M works to understand what we need to process.
"""

import os
import glob

def analyze_new_works():
    """Analyze the available works and their contents."""

    base_path = r"C:\Users\VeigaMagnusdottir\projects\magnusPalsson\images-not-used"

    # Get all K, L, M folders
    all_items = os.listdir(base_path)
    klm_works = [item for item in all_items if item[0].lower() in ['k', 'l', 'm'] and item != "Kúlan 1962"]

    print(f"Found {len(klm_works)} K, L, M works to process:")
    print("=" * 80)

    work_data = []

    for work_name in sorted(klm_works):
        work_path = os.path.join(base_path, work_name)

        if os.path.isdir(work_path):
            # Count image files
            image_files = []
            for ext in ['*.jpg', '*.jpeg', '*.png', '*.tif', '*.tiff']:
                image_files.extend(glob.glob(os.path.join(work_path, ext)))

            # Count other files
            other_files = []
            for ext in ['*.pdf', '*.mp3', '*.mp4', '*.mov', '*.txt']:
                other_files.extend(glob.glob(os.path.join(work_path, ext)))

            # Extract potential year from folder name
            year = "Unknown"
            for word in work_name.split():
                if word.isdigit() and len(word) == 4 and word.startswith(('19', '20')):
                    year = word
                    break
                elif '-' in word and any(part.isdigit() and len(part) == 4 for part in word.split('-')):
                    # Handle ranges like 1963-66
                    parts = word.split('-')
                    for part in parts:
                        if part.isdigit() and len(part) == 4:
                            year = part
                            break

            work_info = {
                'name': work_name,
                'path': work_path,
                'images': len(image_files),
                'other_files': len(other_files),
                'year': year,
                'image_list': [os.path.basename(f) for f in image_files[:5]]  # First 5 for preview
            }

            work_data.append(work_info)

            print(f"{work_name}")
            print(f"  Year: {year}")
            print(f"  Images: {len(image_files)} | Other files: {len(other_files)}")
            if image_files:
                print(f"  Sample images: {', '.join(work_info['image_list'])}")
            print()
        else:
            print(f"{work_name} - SKIP (not a directory)")
            print()

    print("=" * 80)
    print(f"SUMMARY:")
    print(f"Total works to process: {len(work_data)}")
    print(f"Works with images: {len([w for w in work_data if w['images'] > 0])}")
    print(f"Works with no images: {len([w for w in work_data if w['images'] == 0])}")

    # Suggest processing order
    print(f"\nSUGGESTED PROCESSING ORDER:")
    print(f"1. Works with 1-5 images (quick wins): {len([w for w in work_data if 1 <= w['images'] <= 5])}")
    print(f"2. Works with 6-15 images (medium): {len([w for w in work_data if 6 <= w['images'] <= 15])}")
    print(f"3. Works with 15+ images (complex): {len([w for w in work_data if w['images'] > 15])}")

    return work_data

if __name__ == "__main__":
    works = analyze_new_works()