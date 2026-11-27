#!/usr/bin/env python3
"""
Add thumbnails for manual corrections identified during review
"""

import json
from pathlib import Path
from PIL import Image

# Paths
PROJECT_DIR = Path(__file__).parent
THUMBNAIL_SOURCE = Path(r"C:\Users\veiga\Downloads\Thumbnails Frances\Thumbnail images 10.10.26 updated 15.11.26")
IMAGES_DIR = PROJECT_DIR / "images"
WORKS_JSON = PROJECT_DIR / "works.json"
THUMBNAIL_DATA = PROJECT_DIR / "thumbnail_mapping_bilingual.json"

# Manual corrections: thumb_num -> work_id
MANUAL_CORRECTIONS = {
    '62': 'segdu_ekki_nei_segdu_kannski',  # Orðaveggur
    '28': 'tango-1-2-1969',  # Tangó
    '74': 'the-offs-1994',  # The Offs
}

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def find_thumbnail_image(thumb_num):
    """Find the actual image file for a thumbnail number"""
    num_padded = str(thumb_num).zfill(2) if str(thumb_num).isdigit() else str(thumb_num)

    for file in THUMBNAIL_SOURCE.iterdir():
        if (file.name.startswith(f"{thumb_num} ") or
            file.name.startswith(f"{thumb_num}.") or
            file.name.startswith(f"{num_padded} ") or
            file.name.startswith(f"{num_padded}.")):
            return file
    return None

def create_resized_images(source_path, work_id):
    """Create medium and thumbnail versions of image"""
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

    # Medium version (800px)
    medium_img = img.copy()
    medium_img.thumbnail((800, 800), Image.Resampling.LANCZOS)
    medium_img.save(medium_path, quality=90, optimize=True)

    # Thumbnail (200px)
    thumb_img = img.copy()
    thumb_img.thumbnail((200, 200), Image.Resampling.LANCZOS)
    thumb_img.save(thumb_path, quality=85, optimize=True)

    return medium_path, thumb_path

def add_image_to_work(work, medium_path, thumb_path, thumb_num):
    """Add image entry to work's images array"""
    if 'images' not in work:
        work['images'] = []

    rel_medium = str(medium_path.relative_to(PROJECT_DIR)).replace('\\', '/')
    rel_thumb = str(thumb_path.relative_to(PROJECT_DIR)).replace('\\', '/')

    image_entry = {
        "url": rel_medium,
        "caption": {
            "en": f"Book thumbnail #{thumb_num}",
            "is": f"Smamynd ur bok #{thumb_num}"
        },
        "thumbnail": rel_thumb,
        "photographer": "Book publication",
        "year": ""
    }

    work['images'].insert(0, image_entry)
    return work

def main():
    print("Add Manual Corrections - Phase 2")
    print("="*80)
    print("Processing manually identified matches")
    print()

    # Load data
    works_data = load_json(WORKS_JSON)
    thumbnail_data_list = load_json(THUMBNAIL_DATA)
    thumb_data_map = {t['number']: t for t in thumbnail_data_list}

    added_count = 0
    skipped_count = 0
    errors = []

    for thumb_num, work_id in MANUAL_CORRECTIONS.items():
        print(f"#{thumb_num} -> {work_id}")

        # Get thumbnail data
        thumb_data = thumb_data_map.get(thumb_num)
        if thumb_data:
            print(f"  Thumbnail: {thumb_data.get('title_en', '')} ({thumb_data.get('year', '')})")

        # Find work
        work_idx = None
        for idx, w in enumerate(works_data['works']):
            if w['id'] == work_id:
                work_idx = idx
                break

        if work_idx is None:
            print(f"  ERROR: Work not found")
            errors.append(f"#{thumb_num}: Work {work_id} not found")
            skipped_count += 1
            print()
            continue

        work = works_data['works'][work_idx]
        print(f"  Work: {work.get('title', {}).get('en', '')} ({work.get('year', '')})")

        # Check if already has book thumbnail
        has_book_thumb = any('book-thumbnail' in img.get('url', '') for img in work.get('images', []))
        if has_book_thumb:
            print(f"  SKIP: Already has book thumbnail")
            skipped_count += 1
            print()
            continue

        # Find image file
        image_file = find_thumbnail_image(thumb_num)
        if not image_file:
            print(f"  ERROR: Image file not found")
            errors.append(f"#{thumb_num}: Image file not found")
            skipped_count += 1
            print()
            continue

        try:
            # Create resized images
            print(f"  Processing {image_file.name}...")
            medium_path, thumb_path = create_resized_images(image_file, work_id)

            # Add to work
            work = add_image_to_work(work, medium_path, thumb_path, thumb_num)

            # Add tag
            if 'tags' not in work:
                work['tags'] = []
            if 'book-thumbnail-added' not in work['tags']:
                work['tags'].append('book-thumbnail-added')

            # Update searchText
            search_text = work.get('searchText', '')
            if 'book thumbnail' not in search_text.lower():
                if search_text:
                    work['searchText'] = f"{search_text} book thumbnail added"
                else:
                    work['searchText'] = "book thumbnail added"

            works_data['works'][work_idx] = work
            added_count += 1
            print(f"  SUCCESS - Added thumbnail")

        except Exception as e:
            print(f"  ERROR: {e}")
            errors.append(f"#{thumb_num}: {str(e)}")
            skipped_count += 1

        print()

    # Save
    if added_count > 0:
        print("="*80)
        print(f"Saving works.json with {added_count} new thumbnails...")
        save_json(WORKS_JSON, works_data)
        print("SUCCESS!")
        print()

    # Summary
    print("="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Manual corrections processed: {len(MANUAL_CORRECTIONS)}")
    print(f"Thumbnails added: {added_count}")
    print(f"Skipped: {skipped_count}")
    print()

    if errors:
        print("ERRORS:")
        for error in errors:
            print(f"  - {error}")
        print()

if __name__ == '__main__':
    main()
