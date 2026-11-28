#!/usr/bin/env python3
"""
Fix year mismatches and add thumbnails:
- #106 Litlar myndir: small-sketches-with-veiga-and-palli (1976 → 1996)
- #141 Mótun lands: motun-lands-askja-2010-2010 (2009 → 2010)
"""

import json
from pathlib import Path
from PIL import Image

PROJECT_DIR = Path(__file__).parent
THUMBNAIL_SOURCE = Path(r"C:\Users\veiga\Downloads\Thumbnails Frances\Thumbnail images 10.10.26 updated 15.11.26")
IMAGES_DIR = PROJECT_DIR / "images"
WORKS_JSON = PROJECT_DIR / "works.json"
NEW_WORKS = PROJECT_DIR / "truly_new_works_corrected.json"

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def find_thumbnail_image(thumb_num):
    """Find the actual image file for a thumbnail number"""
    for file in THUMBNAIL_SOURCE.iterdir():
        if (file.name.startswith(f"{thumb_num} ") or
            file.name.startswith(f"{thumb_num}.")):
            return file
    return None

def create_resized_images(source_path, work_id):
    """Create medium and thumbnail versions"""
    work_dir = IMAGES_DIR / work_id
    medium_dir = work_dir / "medium"
    thumb_dir = work_dir / "thumbs"

    medium_dir.mkdir(parents=True, exist_ok=True)
    thumb_dir.mkdir(parents=True, exist_ok=True)

    ext = source_path.suffix
    base_name = f"{work_id}-book-thumbnail"
    medium_path = medium_dir / f"{base_name}-medium{ext}"
    thumb_path = thumb_dir / f"{base_name}-thumb{ext}"

    img = Image.open(source_path)

    # Medium (800px)
    medium_img = img.copy()
    medium_img.thumbnail((800, 800), Image.Resampling.LANCZOS)
    medium_img.save(medium_path, quality=90, optimize=True)

    # Thumbnail (200px)
    thumb_img = img.copy()
    thumb_img.thumbnail((200, 200), Image.Resampling.LANCZOS)
    thumb_img.save(thumb_path, quality=85, optimize=True)

    return medium_path, thumb_path

def add_thumbnail_to_work(work, medium_path, thumb_path, thumb_num, year):
    """Add thumbnail image to work"""
    rel_medium = str(medium_path.relative_to(PROJECT_DIR)).replace('\\\\', '/')
    rel_thumb = str(thumb_path.relative_to(PROJECT_DIR)).replace('\\\\', '/')

    image_entry = {
        "url": rel_medium,
        "caption": {
            "en": f"Book thumbnail #{thumb_num}",
            "is": f"Smámynd úr bók #{thumb_num}"
        },
        "thumbnail": rel_thumb,
        "photographer": "Book publication",
        "year": str(year)
    }

    if 'images' not in work:
        work['images'] = []

    work['images'].insert(0, image_entry)

    # Add tag
    if 'tags' not in work:
        work['tags'] = []
    if 'book-thumbnail-added' not in work['tags']:
        work['tags'].append('book-thumbnail-added')

    # Update searchText
    search_text = work.get('searchText', '')
    if 'book thumbnail' not in search_text.lower():
        if search_text:
            work['searchText'] = f"{search_text} book thumbnail #{thumb_num} added"
        else:
            work['searchText'] = f"book thumbnail #{thumb_num} added"

    return work

def main():
    print("Fix Year Mismatches and Add Thumbnails")
    print("="*80)

    # Load data
    works_data = load_json(WORKS_JSON)
    new_works_data = load_json(NEW_WORKS)

    # #106 Litlar myndir
    print("Processing #106 Litlar myndir (Small drawings)")
    work_idx = None
    for idx, w in enumerate(works_data['works']):
        if w['id'] == 'small-sketches-with-veiga-and-palli':
            work_idx = idx
            break

    if work_idx is not None:
        work = works_data['works'][work_idx]
        old_year = work.get('year')
        work['year'] = 1996
        print(f"  Updated year: {old_year} -> 1996")

        # Add thumbnail
        image_file = find_thumbnail_image('106')
        if image_file:
            print(f"  Found: {image_file.name}")
            medium_path, thumb_path = create_resized_images(image_file, 'small-sketches-with-veiga-and-palli')
            work = add_thumbnail_to_work(work, medium_path, thumb_path, '106', 1996)
            print(f"  Added thumbnail")

        works_data['works'][work_idx] = work

        # Remove from truly_new_works
        before = len(new_works_data)
        new_works_data = [w for w in new_works_data if w.get('number') != '106']
        if len(new_works_data) < before:
            print(f"  Removed #106 from truly_new_works")
    print()

    # #141 Mótun lands
    print("Processing #141 Mótun lands (Creation of Land)")
    work_idx = None
    for idx, w in enumerate(works_data['works']):
        if w['id'] == 'motun-lands-askja-2010-2010':
            work_idx = idx
            break

    if work_idx is not None:
        work = works_data['works'][work_idx]
        old_year = work.get('year')
        work['year'] = 2010
        print(f"  Updated year: {old_year} -> 2010")

        # Add thumbnail
        image_file = find_thumbnail_image('141')
        if image_file:
            print(f"  Found: {image_file.name}")
            medium_path, thumb_path = create_resized_images(image_file, 'motun-lands-askja-2010-2010')
            work = add_thumbnail_to_work(work, medium_path, thumb_path, '141', 2010)
            print(f"  Added thumbnail")

        works_data['works'][work_idx] = work

        # Remove from truly_new_works
        before = len(new_works_data)
        new_works_data = [w for w in new_works_data if w.get('number') != '141']
        if len(new_works_data) < before:
            print(f"  Removed #141 from truly_new_works")
    print()

    # Save
    print("="*80)
    print("Saving files...")
    save_json(WORKS_JSON, works_data)
    save_json(NEW_WORKS, new_works_data)
    print("SUCCESS!")
    print()

    # Summary
    print("="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Fixed year mismatches: 2")
    print(f"  #106: 1976 -> 1996")
    print(f"  #141: 2009 -> 2010")
    print(f"Thumbnails added: 2")
    print(f"Truly new works now: {len(new_works_data)}")

if __name__ == '__main__':
    main()
