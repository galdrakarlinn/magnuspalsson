#!/usr/bin/env python3
"""
Convert remaining TIF thumbnails to JPEG format
"""

import json
from pathlib import Path
from PIL import Image

PROJECT_DIR = Path(__file__).parent
WORKS_JSON = PROJECT_DIR / "works.json"

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def convert_tif_to_jpg(tif_path):
    """Convert TIF to JPEG and create thumbnail"""
    if not tif_path.exists():
        return None, None

    # Create JPEG paths
    jpg_medium = Path(str(tif_path).replace('.tif', '.jpg'))
    jpg_thumb = tif_path.parent.parent / 'thumbs' / Path(str(tif_path.name).replace('.tif', '.jpg'))

    # Ensure thumbs directory exists
    jpg_thumb.parent.mkdir(exist_ok=True)

    # Convert
    img = Image.open(tif_path)

    # Medium JPEG
    medium_img = img.copy()
    if medium_img.mode == 'RGBA':
        medium_img = medium_img.convert('RGB')
    medium_img.save(jpg_medium, 'JPEG', quality=90, optimize=True)

    # Thumbnail JPEG
    thumb_img = img.copy()
    thumb_img.thumbnail((200, 200), Image.Resampling.LANCZOS)
    if thumb_img.mode == 'RGBA':
        thumb_img = thumb_img.convert('RGB')
    thumb_img.save(jpg_thumb, 'JPEG', quality=85, optimize=True)

    return jpg_medium, jpg_thumb

def main():
    print("Convert TIF Thumbnails to JPEG")
    print("="*80)

    # Load works
    works_data = load_json(WORKS_JSON)

    tif_works = [
        'hviskur_whisper_1_1975',
        'hundljod_1970'
    ]

    converted = 0

    for work_id in tif_works:
        print(f"\nProcessing {work_id}...")

        for idx, work in enumerate(works_data['works']):
            if work['id'] == work_id:
                for img in work.get('images', []):
                    url = img.get('url', '')
                    if url.endswith('.tif'):
                        tif_path = PROJECT_DIR / url
                        print(f"  Found TIF: {tif_path.name}")

                        # Convert
                        jpg_medium, jpg_thumb = convert_tif_to_jpg(tif_path)

                        if jpg_medium:
                            # Update URL
                            img['url'] = str(jpg_medium.relative_to(PROJECT_DIR)).replace('\\\\', '/')
                            print(f"  Created: {jpg_medium.name}")

                            # Add/update thumbnail
                            if jpg_thumb:
                                img['thumbnail'] = str(jpg_thumb.relative_to(PROJECT_DIR)).replace('\\\\', '/')
                                print(f"  Created: {jpg_thumb.name}")

                            converted += 1

                works_data['works'][idx] = work
                break

    # Save
    if converted > 0:
        print("\n" + "="*80)
        print("Saving works.json...")
        save_json(WORKS_JSON, works_data)
        print("SUCCESS!")
        print()

    # Summary
    print("="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Converted {converted} TIF images to JPEG")

if __name__ == '__main__':
    main()
