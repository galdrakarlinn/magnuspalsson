#!/usr/bin/env python3
"""
Process the remaining N, P, R works: complex (20+ images) and documentation-only works.
"""

import os
import json
import glob
import subprocess
import shutil
import re

def clean_work_id(work_name):
    """Convert work name to clean ID format."""
    # Extract year
    year = "unknown"
    for word in work_name.split():
        if word.isdigit() and len(word) == 4 and word.startswith(('19', '20')):
            year = word
            break
        elif '-' in word and any(part.isdigit() and len(part) == 4 for part in word.split('-')):
            parts = word.split('-')
            for part in parts:
                if part.isdigit() and len(part) == 4:
                    year = part
                    break

    # Clean the name
    clean_name = work_name.lower()
    clean_name = re.sub(r'[áàäâ]', 'a', clean_name)
    clean_name = re.sub(r'[éèëê]', 'e', clean_name)
    clean_name = re.sub(r'[íìïî]', 'i', clean_name)
    clean_name = re.sub(r'[óòöô]', 'o', clean_name)
    clean_name = re.sub(r'[úùüû]', 'u', clean_name)
    clean_name = re.sub(r'[ýÿ]', 'y', clean_name)
    clean_name = re.sub(r'[þ]', 'th', clean_name)
    clean_name = re.sub(r'[ð]', 'd', clean_name)
    clean_name = re.sub(r'[æ]', 'ae', clean_name)
    clean_name = re.sub(r'[ø]', 'o', clean_name)

    # Remove special characters and replace with hyphens
    clean_name = re.sub(r'[^a-z0-9\s]', '', clean_name)
    clean_name = re.sub(r'\s+', '-', clean_name)
    clean_name = clean_name.strip('-')

    # Add year if we found one
    if year != "unknown":
        return f"{clean_name}-{year}"
    else:
        return clean_name

def select_best_images(image_files, max_images=10):
    """Select the best images from a large collection."""

    # Sort by file size (often higher quality) and name
    file_info = []
    for img in image_files:
        try:
            size = os.path.getsize(img)
            name = os.path.basename(img).lower()

            # Quality scoring
            score = size

            # Bonus for high-quality indicators
            if any(qual in name for qual in ['high', 'hq', 'main', 'master', '01', 'cover']):
                score += 1000000

            # Penalty for low-quality indicators
            if any(bad in name for bad in ['thumb', 'small', 'icon', 'preview', 'test']):
                score -= 5000000

            file_info.append((img, score))
        except:
            file_info.append((img, 0))

    # Sort by score descending
    file_info.sort(key=lambda x: -x[1])

    # Select best ones
    selected = []
    for img_path, score in file_info:
        if score > -1000000:  # Skip obviously bad ones
            selected.append(img_path)
            if len(selected) >= max_images:
                break

    return selected

def process_complex_work(work_name, source_path, max_images=10):
    """Process a complex work with many images."""

    print(f"\n=== Processing Complex Work: {work_name} ===")

    # Generate work ID
    work_id = clean_work_id(work_name)
    print(f"Work ID: {work_id}")

    # Get image files
    image_files = []
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.tif', '*.tiff']:
        image_files.extend(glob.glob(os.path.join(source_path, ext)))

    if not image_files:
        print(f"No images found in {work_name}")
        return None

    # Select best images
    selected_images = select_best_images(image_files, max_images)
    print(f"Selected {len(selected_images)} images from {len(image_files)} available")

    # Create folder structure
    work_folder = f"images/{work_id}"
    os.makedirs(f"{work_folder}/medium", exist_ok=True)
    os.makedirs(f"{work_folder}/thumbs", exist_ok=True)

    # Copy other files if they exist
    other_files = []
    for ext in ['*.mp3', '*.wav', '*.mp4', '*.mov', '*.pdf', '*.doc']:
        other_files.extend(glob.glob(os.path.join(source_path, ext)))

    for other_file in other_files:
        filename = os.path.basename(other_file)
        dst = os.path.join(work_folder, filename)
        shutil.copy2(other_file, dst)
        print(f"  Copied: {filename}")

    # Process images
    image_entries = []
    for i, img_path in enumerate(selected_images, 1):
        img_name = os.path.basename(img_path)
        base_name = os.path.splitext(img_name)[0]

        output_base = f"{work_id.split('-')[0]}-{i:02d}"

        try:
            # Process medium image
            medium_path = f"{work_folder}/medium/{output_base}-medium.jpg"
            subprocess.run([
                'ffmpeg', '-i', img_path, '-y',
                '-vf', 'scale=800:600:force_original_aspect_ratio=decrease',
                '-q:v', '3',
                medium_path
            ], check=True, capture_output=True)

            # Process thumbnail
            thumb_path = f"{work_folder}/thumbs/{output_base}-thumb.jpg"
            subprocess.run([
                'ffmpeg', '-i', img_path, '-y',
                '-vf', 'scale=150:150:force_original_aspect_ratio=increase,crop=150:150',
                '-q:v', '4',
                thumb_path
            ], check=True, capture_output=True)

            # Add to image entries
            image_entries.append({
                "url": f"images/{work_id}/medium/{output_base}-medium.jpg",
                "caption": f"{work_name.split()[0]} - view {i}"
            })

            print(f"  Processed: {img_name} -> {output_base}")

        except subprocess.CalledProcessError as e:
            print(f"  Error processing {img_name}: {e}")
            continue

    if not image_entries:
        print(f"No images successfully processed for {work_name}")
        return None

    # Extract year for JSON
    year = "Unknown"
    for word in work_name.split():
        if word.isdigit() and len(word) == 4 and word.startswith(('19', '20')):
            year = int(word)
            break

    # Create JSON entry
    work_entry = {
        "id": work_id,
        "title": work_name,
        "year": year,
        "description": f"A comprehensive work by Magnús Pálsson from {year}. This extensive piece demonstrates his artistic development and exploration during this significant period.",
        "images": image_entries,
        "tags": ["artwork", str(year) if year != "Unknown" else "undated"],
        "exhibitions": [],
        "materials": [],
        "searchText": f"{work_name.lower()} {year} magnús pálsson"
    }

    print(f"  Created JSON entry with {len(image_entries)} images")
    return work_entry

def process_documentation_work(work_name, source_path):
    """Process a documentation-only work (videos, etc.)."""

    print(f"\n=== Processing Documentation Work: {work_name} ===")

    # Generate work ID
    work_id = clean_work_id(work_name)
    print(f"Work ID: {work_id}")

    # Create folder structure
    work_folder = f"images/{work_id}"
    os.makedirs(work_folder, exist_ok=True)

    # Copy all files
    doc_files = []
    for file in os.listdir(source_path):
        src = os.path.join(source_path, file)
        if os.path.isfile(src):
            dst = os.path.join(work_folder, file)
            shutil.copy2(src, dst)
            doc_files.append(file)
            print(f"  Copied: {file}")

    # Extract year
    year = "Unknown"
    for word in work_name.split():
        if word.isdigit() and len(word) == 4 and word.startswith(('19', '20')):
            year = int(word)
            break

    # Create JSON entry
    work_entry = {
        "id": work_id,
        "title": work_name,
        "year": year,
        "description": f"A performance documentation work by Magnús Pálsson from {year}. This work includes video documentation and materials from the performance.",
        "images": [],  # No images for video-only works
        "tags": ["performance", "video", "documentation", str(year) if year != "Unknown" else "undated"],
        "exhibitions": [],
        "materials": ["video", "performance", "documentation"],
        "searchText": f"{work_name.lower()} {year} magnús pálsson performance video documentation"
    }

    print(f"  Created JSON entry with {len(doc_files)} documentation files")
    return work_entry

def process_remaining_npr_works():
    """Process the remaining N, P, R works."""

    base_path = r"C:\Users\VeigaMagnusdottir\projects\magnusPalsson\images-not-used"

    # Read current works.json
    with open('works.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    new_entries = []

    # 1. Process complex work: Rúmbjarni Suðurgata 7 1976
    complex_work = "Rúmbjarni Suðurgata 7 1976"
    complex_path = os.path.join(base_path, complex_work)
    if os.path.exists(complex_path):
        work_entry = process_complex_work(complex_work, complex_path, max_images=10)
        if work_entry:
            new_entries.append(work_entry)

    # 2. Process documentation work: Pendúll student performance 1.2.1999
    doc_work = "Pendúll student performance 1.2.1999"
    doc_path = os.path.join(base_path, doc_work)
    if os.path.exists(doc_path):
        work_entry = process_documentation_work(doc_work, doc_path)
        if work_entry:
            new_entries.append(work_entry)

    # Add new entries to JSON
    data['works'] = new_entries + data['works']

    # Write updated JSON
    with open('works.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n=== REMAINING N, P, R PROCESSING COMPLETE ===")
    print(f"Successfully processed: {len(new_entries)} additional works")
    print(f"Total works now: {len(data['works'])}")

    return len(new_entries)

if __name__ == "__main__":
    count = process_remaining_npr_works()