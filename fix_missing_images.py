#!/usr/bin/env python3
"""
1. Add images to Lítill, Trítill, Karlsson og fuglarnir (#79a, #79b)
2. Clean up Stærðfræði 2 duplicate images
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
    print("Fix Missing Images")
    print("="*80)

    # Load works
    works_data = load_json(WORKS_JSON)

    # 1. Add images to Lítill, Trítill
    print("\n1. Adding images to Lítill, Trítill, Karlsson og fuglarnir...")

    image_79a = THUMBNAIL_SOURCE / "79a Lítill, Trítill, Karlsson og fuglarnir.JPG"
    image_79b = THUMBNAIL_SOURCE / "79b Lítill, Trítill, Karlsson og fuglarnir.JPG"

    for idx, work in enumerate(works_data['works']):
        if work['id'] == 'litill-tritill-karlsson-og-fuglarnir-1985':
            print(f"  Found work: {work.get('title', {}).get('en', '')}")

            if 'images' not in work:
                work['images'] = []

            # Add 79a
            if image_79a.exists():
                print(f"  Processing 79a...")
                medium_a, thumb_a = create_resized_images(image_79a, work['id'], '-a')

                rel_medium_a = str(medium_a.relative_to(PROJECT_DIR)).replace('\\\\', '/')
                rel_thumb_a = str(thumb_a.relative_to(PROJECT_DIR)).replace('\\\\', '/')

                work['images'].append({
                    "url": rel_medium_a,
                    "caption": {
                        "en": "Book thumbnail #79a",
                        "is": "Smámynd úr bók #79a"
                    },
                    "thumbnail": rel_thumb_a,
                    "photographer": "Book publication",
                    "year": "1985"
                })
                print(f"    Added: {medium_a.name}")

            # Add 79b
            if image_79b.exists():
                print(f"  Processing 79b...")
                medium_b, thumb_b = create_resized_images(image_79b, work['id'], '-b')

                rel_medium_b = str(medium_b.relative_to(PROJECT_DIR)).replace('\\\\', '/')
                rel_thumb_b = str(thumb_b.relative_to(PROJECT_DIR)).replace('\\\\', '/')

                work['images'].append({
                    "url": rel_medium_b,
                    "caption": {
                        "en": "Book thumbnail #79b",
                        "is": "Smámynd úr bók #79b"
                    },
                    "thumbnail": rel_thumb_b,
                    "photographer": "Book publication",
                    "year": "1985"
                })
                print(f"    Added: {medium_b.name}")

            # Add book-thumbnail-added tag
            if 'tags' not in work:
                work['tags'] = []
            if 'book-thumbnail-added' not in work['tags']:
                work['tags'].append('book-thumbnail-added')

            works_data['works'][idx] = work
            break

    # 2. Clean up Stærðfræði 2 duplicates
    print("\n2. Cleaning up Stærðfræði 2 duplicate images...")

    for idx, work in enumerate(works_data['works']):
        if work['id'] == 'staerdfraedi-maths-1976':
            original_count = len(work.get('images', []))
            print(f"  Found work with {original_count} images")

            # Remove duplicates - keep only unique URLs
            seen_urls = set()
            unique_images = []

            for img in work.get('images', []):
                url = img.get('url', '')
                # Normalize path separators
                url_normalized = url.replace('\\\\', '/').lower()

                if url_normalized not in seen_urls:
                    seen_urls.add(url_normalized)
                    # Keep the forward-slash version
                    img['url'] = url.replace('\\\\', '/')
                    unique_images.append(img)
                else:
                    print(f"  Removing duplicate: {url}")

            work['images'] = unique_images
            works_data['works'][idx] = work

            print(f"  Reduced from {original_count} to {len(unique_images)} images")
            break

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
    print("1. Added 2 images to Lítill, Trítill, Karlsson (#79a, #79b)")
    print("2. Cleaned up Stærðfræði 2 duplicate images")

if __name__ == '__main__':
    main()
