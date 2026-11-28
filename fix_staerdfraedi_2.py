#!/usr/bin/env python3
"""
Fix Stærðfræði 2 (Mathematics 2):
- staerdfraedi-maths-1976 on website is #48 from thumbnail mapping
- Remove #48 from truly_new_works (correct match)
- Add thumbnail #48 to existing work
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

def main():
    print("Fix Staerdfraedi 2 (Mathematics 2) - Correct Match")
    print("="*80)

    # Find image
    image_file = None
    for f in THUMBNAIL_SOURCE.iterdir():
        if f.name.startswith('48 ') or f.name.startswith('48.'):
            image_file = f
            break

    if not image_file:
        print("ERROR: Image file not found")
        return

    print(f"Found: {image_file.name}")

    # Create resized images
    work_id = "staerdfraedi-maths-1976"
    medium_path, thumb_path = create_resized_images(image_file, work_id)
    print(f"Created medium: {medium_path.name}")
    print(f"Created thumb: {thumb_path.name}")
    print()

    # Load data
    works_data = load_json(WORKS_JSON)
    new_works_data = load_json(NEW_WORKS)

    # Find work
    work_idx = None
    for idx, w in enumerate(works_data['works']):
        if w['id'] == work_id:
            work_idx = idx
            break

    if work_idx is None:
        print("ERROR: Work not found")
        return

    work = works_data['works'][work_idx]

    # Add image
    rel_medium = str(medium_path.relative_to(PROJECT_DIR)).replace('\\\\', '/')
    rel_thumb = str(thumb_path.relative_to(PROJECT_DIR)).replace('\\\\', '/')

    image_entry = {
        "url": rel_medium,
        "caption": {
            "en": "Book thumbnail #48",
            "is": "Smámynd úr bók #48"
        },
        "thumbnail": rel_thumb,
        "photographer": "Book publication",
        "year": "1976"
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
            work['searchText'] = f"{search_text} book thumbnail #48 added"
        else:
            work['searchText'] = "book thumbnail #48 added"

    works_data['works'][work_idx] = work

    # Remove #48 from truly_new_works
    original_count = len(new_works_data)
    new_works_data = [w for w in new_works_data if w.get('number') != '48']
    removed = original_count - len(new_works_data)

    # Save
    print("Saving files...")
    save_json(WORKS_JSON, works_data)
    save_json(NEW_WORKS, new_works_data)
    print("SUCCESS!")
    print()

    # Summary
    print("="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Added thumbnail #48 to staerdfraedi-maths-1976")
    print(f"Work: {work['title']['en']} / {work['title']['is']}")
    print(f"Removed #48 from truly_new_works: {removed}")
    print(f"Truly new works now: {len(new_works_data)}")

if __name__ == '__main__':
    main()
