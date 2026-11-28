#!/usr/bin/env python3
"""
Add thumbnail #32 to hundur_adrir_1971 (Hundar/Dogs)
"""

import json
from pathlib import Path
from PIL import Image

PROJECT_DIR = Path(__file__).parent
THUMBNAIL_SOURCE = Path(r"C:\Users\veiga\Downloads\Thumbnails Frances\Thumbnail images 10.10.26 updated 15.11.26")
IMAGES_DIR = PROJECT_DIR / "images"
WORKS_JSON = PROJECT_DIR / "works.json"

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
    print("Add Thumbnail #32 to Hundar (Dogs)")
    print("="*80)

    # Find image
    image_file = None
    for f in THUMBNAIL_SOURCE.iterdir():
        if f.name.startswith('32 ') or f.name.startswith('32.'):
            image_file = f
            break

    if not image_file:
        print("ERROR: Image file not found")
        return

    print(f"Found: {image_file.name}")

    # Create resized images
    work_id = "hundur_adrir_1971"
    medium_path, thumb_path = create_resized_images(image_file, work_id)
    print(f"Created medium: {medium_path.name}")
    print(f"Created thumb: {thumb_path.name}")
    print()

    # Load works
    works_data = load_json(WORKS_JSON)

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

    # Add image to beginning
    rel_medium = str(medium_path.relative_to(PROJECT_DIR)).replace('\\\\', '/')
    rel_thumb = str(thumb_path.relative_to(PROJECT_DIR)).replace('\\\\', '/')

    image_entry = {
        "url": rel_medium,
        "caption": {
            "en": "Book thumbnail #32",
            "is": "Smámynd úr bók #32"
        },
        "thumbnail": rel_thumb,
        "photographer": "Book publication",
        "year": "1970"
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
            work['searchText'] = f"{search_text} book thumbnail #32 added"
        else:
            work['searchText'] = "book thumbnail #32 added"

    works_data['works'][work_idx] = work

    # Save
    print("Saving works.json...")
    save_json(WORKS_JSON, works_data)
    print("SUCCESS!")
    print()

    print("="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Added thumbnail #32 to {work_id}")
    print(f"Work: {work['title']['en']} / {work['title']['is']}")
    print(f"Year: {work['year']}")

if __name__ == '__main__':
    main()
