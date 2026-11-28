#!/usr/bin/env python3
"""
Add missing thumbnails:
- #9 Vending I and II: 09 Twisting Vending I and II.JPG
- #112 Small Object: 112b as thumbnail, 112a as additional work image
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

def create_resized_images(source_path, work_id, suffix=''):
    """Create medium and thumbnail versions"""
    work_dir = IMAGES_DIR / work_id
    medium_dir = work_dir / "medium"
    thumb_dir = work_dir / "thumbs"

    medium_dir.mkdir(parents=True, exist_ok=True)
    thumb_dir.mkdir(parents=True, exist_ok=True)

    ext = source_path.suffix
    base_name = f"{work_id}-book-thumbnail{suffix}"
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
    print("Add Missing Thumbnails - #9 and #112")
    print("="*80)

    # Load data
    works_data = load_json(WORKS_JSON)

    # Add #9 Vending I and II
    print("\nProcessing #9 Vending I and II...")
    image_9 = THUMBNAIL_SOURCE / "09 Twisting Vending I and II.JPG"

    if image_9.exists():
        print(f"  Found: {image_9.name}")

        # Create resized images
        medium_path, thumb_path = create_resized_images(image_9, "vending-i-and-ii-1965")
        print(f"  Created: {medium_path.name}")

        # Find work and add image
        for idx, work in enumerate(works_data['works']):
            if work['id'] == 'vending-i-and-ii-1965':
                rel_medium = str(medium_path.relative_to(PROJECT_DIR)).replace('\\\\', '/')
                rel_thumb = str(thumb_path.relative_to(PROJECT_DIR)).replace('\\\\', '/')

                if 'images' not in work:
                    work['images'] = []

                work['images'].insert(0, {
                    "url": rel_medium,
                    "caption": {
                        "en": "Book thumbnail #9",
                        "is": "Smámynd úr bók #9"
                    },
                    "thumbnail": rel_thumb,
                    "photographer": "Book publication",
                    "year": "1965"
                })

                works_data['works'][idx] = work
                print(f"  Added thumbnail to work")
                break
    else:
        print(f"  ERROR: Image not found")

    # Add #112 Small Object
    print("\nProcessing #112 Small Object...")
    image_112b = THUMBNAIL_SOURCE / "112b Smáhlutir.jpg"
    image_112a = THUMBNAIL_SOURCE / "112a Smáhlutir (Small Objects).jpg"

    if image_112b.exists():
        print(f"  Found 112b: {image_112b.name}")

        # Create resized images for 112b (main thumbnail)
        medium_path_b, thumb_path_b = create_resized_images(image_112b, "small-object-1998", "-b")
        print(f"  Created: {medium_path_b.name}")

        # Find work and add images
        for idx, work in enumerate(works_data['works']):
            if work['id'] == 'small-object-1998':
                rel_medium_b = str(medium_path_b.relative_to(PROJECT_DIR)).replace('\\\\', '/')
                rel_thumb_b = str(thumb_path_b.relative_to(PROJECT_DIR)).replace('\\\\', '/')

                if 'images' not in work:
                    work['images'] = []

                # Add 112b as main thumbnail
                work['images'].insert(0, {
                    "url": rel_medium_b,
                    "caption": {
                        "en": "Book thumbnail #112b",
                        "is": "Smámynd úr bók #112b"
                    },
                    "thumbnail": rel_thumb_b,
                    "photographer": "Book publication",
                    "year": "1998"
                })

                print(f"  Added 112b as main thumbnail")

                # Add 112a if exists
                if image_112a.exists():
                    print(f"  Found 112a: {image_112a.name}")
                    medium_path_a, thumb_path_a = create_resized_images(image_112a, "small-object-1998", "-a")
                    print(f"  Created: {medium_path_a.name}")

                    rel_medium_a = str(medium_path_a.relative_to(PROJECT_DIR)).replace('\\\\', '/')
                    rel_thumb_a = str(thumb_path_a.relative_to(PROJECT_DIR)).replace('\\\\', '/')

                    work['images'].append({
                        "url": rel_medium_a,
                        "caption": {
                            "en": "Small Objects - Additional view #112a",
                            "is": "Smáhlutir - Viðbótarmynd #112a"
                        },
                        "thumbnail": rel_thumb_a,
                        "photographer": "Book publication",
                        "year": "1998"
                    })

                    print(f"  Added 112a as additional image")

                works_data['works'][idx] = work
                break
    else:
        print(f"  ERROR: Image 112b not found")

    # Save
    print("\n" + "="*80)
    print("Saving works.json...")
    save_json(WORKS_JSON, works_data)
    print("SUCCESS!")
    print()

    # Summary
    print("="*80)
    print("SUMMARY")
    print("="*80)
    print("Added thumbnails:")
    print("  #9 Vending I and II - 1 image")
    print("  #112 Small Object - 2 images (112b as thumbnail, 112a additional)")

if __name__ == '__main__':
    main()
