#!/usr/bin/env python3
"""
Add thumbnails to works with correct matches:
- #82 Mob Shop Dummy → mob_shop_dummy_1986
- #118 Night in London → nott-i-london-2000
- #121 Horny and Farm → grad_og_bu_2002
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
    print("Add Simple Thumbnails - Correct Matches")
    print("="*80)

    # Mappings: thumb_num -> (work_id, year)
    mappings = {
        '82': ('mob_shop_dummy_1986', 1986),
        '118': ('nott-i-london-2000', 2000),
        '121': ('grad_og_bu_2002', 2002)
    }

    # Load data
    works_data = load_json(WORKS_JSON)
    new_works_data = load_json(NEW_WORKS)

    added_count = 0
    removed_from_new = []

    for thumb_num, (work_id, year) in mappings.items():
        print(f"Processing #{thumb_num} -> {work_id}")

        # Find image
        image_file = find_thumbnail_image(thumb_num)
        if not image_file:
            print(f"  ERROR: Image file not found")
            continue

        print(f"  Found: {image_file.name}")

        # Create resized images
        medium_path, thumb_path = create_resized_images(image_file, work_id)
        print(f"  Created: {medium_path.name}")

        # Find work
        work_idx = None
        for idx, w in enumerate(works_data['works']):
            if w['id'] == work_id:
                work_idx = idx
                break

        if work_idx is None:
            print(f"  ERROR: Work not found")
            continue

        # Add thumbnail
        work = works_data['works'][work_idx]
        work = add_thumbnail_to_work(work, medium_path, thumb_path, thumb_num, year)
        works_data['works'][work_idx] = work

        print(f"  Added thumbnail to: {work['title']['en']}")

        # Remove from truly_new_works if present
        before = len(new_works_data)
        new_works_data = [w for w in new_works_data if w.get('number') != thumb_num]
        if len(new_works_data) < before:
            removed_from_new.append(thumb_num)
            print(f"  Removed #{thumb_num} from truly_new_works")

        added_count += 1
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
    print(f"Thumbnails added: {added_count}")
    print(f"Removed from truly_new_works: {len(removed_from_new)}")
    for num in removed_from_new:
        print(f"  - #{num}")
    print(f"Truly new works now: {len(new_works_data)}")

if __name__ == '__main__':
    main()
