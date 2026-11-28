#!/usr/bin/env python3
"""
Split contours_of_a_baby_1987 into two separate works:
1. Madame President (1986) - madame-president-1986
2. Contours of a Baby (1987) - contours-of-a-baby-1987

Also add thumbnail #84 to eyetalk_augntal_1986_1998
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

def main():
    print("Split Madame President / Contours of a Baby + Fix Eyetalk")
    print("="*80)

    # Load data
    works_data = load_json(WORKS_JSON)
    new_works_data = load_json(NEW_WORKS)

    # Find the combined work
    combined_idx = None
    for idx, w in enumerate(works_data['works']):
        if w['id'] == 'contours_of_a_baby_1987':
            combined_idx = idx
            break

    if combined_idx is None:
        print("ERROR: contours_of_a_baby_1987 not found")
        return

    combined_work = works_data['works'][combined_idx]

    # Create Madame President (1986)
    print("Creating Madame President (1986)...")
    madame_work = {
        "id": "madame-president-1986",
        "title": {
            "en": "Madame President",
            "is": "Madame President"
        },
        "year": 1986,
        "dimensions": None,
        "description": {
            "en": "Audio cassette for four loudspeakers. First performed at Henie-Onstad Kunstsenter in Oslo 1986 with the artist's own participation, a video monitor and four loudspeakers. Recorded at Studio VEC Maastricht and Studio Stef Kópavogur. Published as Hong Kong Press nr. 7.",
            "is": "Hljóðsnælda fyrir fjóra hátalara. Fyrst flutt á Henie-Onstad Kunstsenter í Ósló 1986 með þátttöku listamannsins sjálfs, sjónvarpsskjá og fjórum háttölurum. Hljóðritað í Studio VEC Maastricht og Studio Stef Kópavogi. Gefið út sem Hong Kong Press nr. 7."
        },
        "images": [],
        "tags": ["sound", "performance", "book-thumbnail-added"],
        "materials": {
            "en": ["audio cassette"],
            "is": ["hljóðsnælda"]
        },
        "category": ["sound-art", "performance"],
        "ownership": {
            "owner": "various museums and collections and the artist",
            "owner_en": "various museums and collections and the artist",
            "owner_is": "ýmis söfn og söfn og listamaðurinn"
        },
        "searchText": "madame president 1986 audio cassette hong kong press book thumbnail #83 added"
    }

    # Add thumbnail #83 to Madame President
    image_83 = find_thumbnail_image('83')
    if image_83:
        print(f"  Found thumbnail: {image_83.name}")
        medium_path, thumb_path = create_resized_images(image_83, 'madame-president-1986')

        rel_medium = str(medium_path.relative_to(PROJECT_DIR)).replace('\\\\', '/')
        rel_thumb = str(thumb_path.relative_to(PROJECT_DIR)).replace('\\\\', '/')

        madame_work['images'].append({
            "url": rel_medium,
            "caption": {
                "en": "Book thumbnail #83",
                "is": "Smámynd úr bók #83"
            },
            "thumbnail": rel_thumb,
            "photographer": "Book publication",
            "year": "1986"
        })

    # Add Madame President images from combined work
    for img in combined_work.get('images', []):
        if 'madame' in img.get('url', '').lower() or 'madame' in img.get('caption', {}).get('en', '').lower():
            madame_work['images'].append(img)

    print(f"  Created with {len(madame_work['images'])} images")

    # Update Contours of a Baby (keep only Contours images)
    print("\nUpdating Contours of a Baby (1987)...")
    contours_images = []

    # Add thumbnail #85
    image_85 = find_thumbnail_image('85')
    if image_85:
        print(f"  Found thumbnail: {image_85.name}")
        medium_path, thumb_path = create_resized_images(image_85, 'contours-of-a-baby-1987')

        rel_medium = str(medium_path.relative_to(PROJECT_DIR)).replace('\\\\', '/')
        rel_thumb = str(thumb_path.relative_to(PROJECT_DIR)).replace('\\\\', '/')

        contours_images.append({
            "url": rel_medium,
            "caption": {
                "en": "Book thumbnail #85",
                "is": "Smámynd úr bók #85"
            },
            "thumbnail": rel_thumb,
            "photographer": "Book publication",
            "year": "1987"
        })

    # Keep only Contours images from combined work
    for img in combined_work.get('images', []):
        if 'madame' not in img.get('url', '').lower() and 'madame' not in img.get('caption', {}).get('en', '').lower():
            contours_images.append(img)

    combined_work['title'] = {
        "en": "Contours of a Baby",
        "is": "Contours of a Baby"
    }
    combined_work['description'] = {
        "en": "Audio cassette for four loudspeakers. Performed at Kunstcentret Brandts Klædefabrik in Odense 1987 with four loudspeakers. Recorded at Studio VEC Maastricht and Studio Stef Kópavogur. Published as Hong Kong Press nr. 7.",
        "is": "Hljóðsnælda fyrir fjóra hátalara. Flutt á Kunstcentret Brandts Klædefabrik í Odense 1987 með fjórum háttölurum. Hljóðritað í Studio VEC Maastricht og Studio Stef Kópavogi. Gefið út sem Hong Kong Press nr. 7."
    }
    combined_work['images'] = contours_images
    combined_work['searchText'] = "contours of a baby 1987 audio cassette hong kong press book thumbnail #85 added"

    print(f"  Updated with {len(contours_images)} images")

    # Insert Madame President before Contours
    works_data['works'].insert(combined_idx, madame_work)
    # Update the Contours work (now at combined_idx + 1)
    works_data['works'][combined_idx + 1] = combined_work

    # Remove #83 from truly_new_works
    before = len(new_works_data)
    new_works_data = [w for w in new_works_data if w.get('number') != '83']
    if len(new_works_data) < before:
        print(f"\nRemoved #83 from truly_new_works")

    # Add thumbnail #84 to Eyetalk preceding Eyetalk
    print("\n" + "="*80)
    print("Adding thumbnail #84 to Eyetalk preceding Eyetalk...")

    for idx, w in enumerate(works_data['works']):
        if w['id'] == 'eyetalk_augntal_1986_1998':
            image_84 = find_thumbnail_image('84')
            if image_84:
                print(f"  Found: {image_84.name}")
                medium_path, thumb_path = create_resized_images(image_84, 'eyetalk_augntal_1986_1998')

                rel_medium = str(medium_path.relative_to(PROJECT_DIR)).replace('\\\\', '/')
                rel_thumb = str(thumb_path.relative_to(PROJECT_DIR)).replace('\\\\', '/')

                if 'images' not in w:
                    w['images'] = []

                w['images'].insert(0, {
                    "url": rel_medium,
                    "caption": {
                        "en": "Book thumbnail #84",
                        "is": "Smámynd úr bók #84"
                    },
                    "thumbnail": rel_thumb,
                    "photographer": "Book publication",
                    "year": "1986"
                })

                if 'tags' not in w:
                    w['tags'] = []
                if 'book-thumbnail-added' not in w['tags']:
                    w['tags'].append('book-thumbnail-added')

                works_data['works'][idx] = w
                print(f"  Added thumbnail to: {w['title']['en']}")
            break

    # Save
    print("\n" + "="*80)
    print("Saving files...")
    save_json(WORKS_JSON, works_data)
    save_json(NEW_WORKS, new_works_data)
    print("SUCCESS!")
    print()

    # Summary
    print("="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Split contours_of_a_baby_1987 into 2 works:")
    print(f"  1. madame-president-1986 (1986) with thumbnail #83")
    print(f"  2. contours-of-a-baby-1987 (1987) with thumbnail #85")
    print()
    print(f"Added thumbnail #84 to eyetalk_augntal_1986_1998")
    print()
    print(f"Removed #83 from truly_new_works")
    print(f"Truly new works now: {len(new_works_data)}")
    print(f"Total works now: {len(works_data['works'])}")

if __name__ == '__main__':
    main()
