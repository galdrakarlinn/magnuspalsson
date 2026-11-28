#!/usr/bin/env python3
"""
Create all 16 new works from truly_new_works_corrected.json
"""

import json
import re
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

def create_work_id(title_en, year):
    """Create work ID from title and year"""
    # Clean title
    title = re.sub(r'\([^)]*\)', '', title_en)  # Remove parentheses
    title = re.sub(r'[^\w\s-]', '', title)  # Remove special chars
    title = title.strip().lower()
    title = re.sub(r'\s+', '-', title)  # Replace spaces with hyphens
    title = re.sub(r'-+', '-', title)  # Remove multiple hyphens

    return f"{title}-{year}"

def categorize_work(title_en, materials):
    """Determine category based on title and materials"""
    title_lower = title_en.lower()

    if any(mat in str(materials).lower() for mat in ['acrylic glass', 'glass', 'plaster', 'ceramic', 'gibs', 'akrýl']):
        return ['sculpture']
    elif any(mat in str(materials).lower() for mat in ['paper', 'ink', 'pencil', 'waterc', 'touch', 'pen']):
        return ['drawing']
    elif 'video' in str(materials).lower() or 'eyetalk' in title_lower or 'augntal' in title_lower:
        return ['video']
    elif 'audio' in str(materials).lower() or 'sound' in str(materials).lower() or any(word in title_lower for word in ['night in london', 'horny and farm', 'grað']):
        return ['sound-art']
    elif 'book' in str(materials).lower() or 'magazine' in str(materials).lower():
        return ['book']
    elif 'outdoor' in str(materials).lower() or 'log' in str(materials).lower():
        return ['sculpture', 'outdoor']
    else:
        return ['mixed-media']

def create_work_from_data(work_data):
    """Create a work object from truly_new_works data"""
    thumb_num = work_data.get('number', '')
    title_en = work_data.get('title_en', '')
    title_is = work_data.get('title_is', '')
    year = work_data.get('year', '')
    materials_en = work_data.get('materials', [])
    materials_is = work_data.get('materials_is', [])
    dimensions = work_data.get('dimensions', '')
    dimensions_is = work_data.get('dimensions_is', '')
    location = work_data.get('location', '')
    location_is = work_data.get('location_is', '')
    details = work_data.get('details', [])
    details_is = work_data.get('details_is', [])

    # Create work ID
    work_id = create_work_id(title_en, year)

    # Create description from details
    description_en = '. '.join(details) if details else ''
    description_is = '. '.join(details_is) if details_is else ''

    # Determine category
    category = categorize_work(title_en, materials_en)

    # Create work object
    work = {
        "id": work_id,
        "title": {
            "en": title_en,
            "is": title_is if title_is else title_en
        },
        "year": int(year) if isinstance(year, str) and year.isdigit() else year,
        "dimensions": dimensions if dimensions else None,
        "description": {
            "en": description_en,
            "is": description_is
        },
        "images": [],
        "tags": ["book-thumbnail-added"],
        "category": category,
        "searchText": f"{title_en.lower()} {title_is.lower() if title_is else ''} {year} book thumbnail #{thumb_num} added"
    }

    # Add materials
    if materials_en or materials_is:
        work["materials"] = {
            "en": materials_en if materials_en else [],
            "is": materials_is if materials_is else materials_en
        }
        work["medium"] = {
            "en": materials_en if materials_en else [],
            "is": materials_is if materials_is else materials_en
        }

    # Add ownership
    if location or location_is:
        work["ownership"] = {
            "owner": location if location else "owned by the artist",
            "owner_en": location if location else "owned by the artist",
            "owner_is": location_is if location_is else "eign listamannsins"
        }

    # Add dimensions to description if present
    if dimensions and dimensions not in description_en:
        if description_en:
            work["description"]["en"] = f"{description_en}. Dimensions: {dimensions}"

    if dimensions_is and dimensions_is not in description_is:
        if description_is:
            work["description"]["is"] = f"{description_is}. Mál: {dimensions_is}"

    return work, work_id

def main():
    print("Create New Works from truly_new_works_corrected.json")
    print("="*80)

    # Load data
    works_data = load_json(WORKS_JSON)
    new_works_data = load_json(NEW_WORKS)

    created_count = 0
    errors = []

    for new_work_data in new_works_data:
        thumb_num = new_work_data.get('number', '')
        title_en = new_work_data.get('title_en', '')

        print(f"\n[{created_count + 1}/{len(new_works_data)}] Creating #{thumb_num}: {title_en}")

        try:
            # Create work object
            work, work_id = create_work_from_data(new_work_data)
            print(f"  Work ID: {work_id}")

            # Find and process thumbnail image
            image_file = find_thumbnail_image(thumb_num)
            if not image_file:
                print(f"  WARNING: Thumbnail image not found")
                errors.append(f"#{thumb_num}: Image not found")
            else:
                print(f"  Found: {image_file.name}")

                # Create resized images
                medium_path, thumb_path = create_resized_images(image_file, work_id)

                # Add image to work
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
                    "year": str(work['year'])
                }

                work['images'].append(image_entry)
                print(f"  Added thumbnail image")

            # Add work to works array
            works_data['works'].append(work)
            created_count += 1
            print(f"  SUCCESS - Created work")

        except Exception as e:
            print(f"  ERROR: {e}")
            errors.append(f"#{thumb_num}: {str(e)}")

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
    print(f"Works created: {created_count}/{len(new_works_data)}")
    print(f"Total works now: {len(works_data['works'])}")
    print()

    if errors:
        print("ERRORS:")
        for error in errors:
            print(f"  - {error}")
        print()

    print("Next step: Clear truly_new_works_corrected.json (all works created)")

if __name__ == '__main__':
    main()
