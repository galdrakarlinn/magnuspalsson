#!/usr/bin/env python3
"""
Batch process N, P, R quick win works (1-5 images) from images-not-used folder.
"""

import os
import json
import glob
import subprocess
import shutil
import re
from pathlib import Path

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

def process_single_work(work_name, source_path, max_images=5):
    """Process a single work: images + JSON entry."""

    print(f"\n=== Processing: {work_name} ===")

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

    # Select best images (max specified)
    selected_images = image_files[:max_images]
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

        # Clean filename for output
        clean_base = re.sub(r'[^a-zA-Z0-9]', '-', base_name).lower()
        clean_base = re.sub(r'-+', '-', clean_base).strip('-')

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
        elif '-' in word:
            parts = word.split('-')
            for part in parts:
                if part.isdigit() and len(part) == 4:
                    year = int(part)
                    break

    # Determine materials based on work content
    materials = []
    if any('audio' in f.lower() or f.endswith(('.mp3', '.wav')) for f in other_files):
        materials.append("audio")
    if any('video' in f.lower() or f.endswith(('.mp4', '.mov')) for f in other_files):
        materials.append("video")
    if any(f.endswith('.pdf') for f in other_files):
        materials.append("documentation")

    # Create JSON entry
    work_entry = {
        "id": work_id,
        "title": work_name.split('(')[0].strip() if '(' in work_name else work_name,
        "year": year,
        "description": f"A work by Magnús Pálsson from {year}. This piece demonstrates his artistic exploration and creative practice during this period.",
        "images": image_entries,
        "tags": ["artwork", str(year) if year != "Unknown" else "undated"],
        "exhibitions": [],
        "materials": materials if materials else [],
        "searchText": f"{work_name.lower()} {year} magnús pálsson"
    }

    print(f"  Created JSON entry with {len(image_entries)} images")
    if other_files:
        print(f"  Included {len(other_files)} additional files")
    return work_entry

def batch_process_npr_quick_wins():
    """Process N, P, R works with 1-5 images."""

    base_path = r"C:\Users\VeigaMagnusdottir\projects\magnusPalsson\images-not-used"

    # Get all N, P, R folders
    all_items = os.listdir(base_path)
    npr_works = [item for item in all_items if item[0].upper() in ['N', 'P', 'R']]

    # Filter for quick wins (1-5 images)
    quick_wins = []
    for work_name in npr_works:
        work_path = os.path.join(base_path, work_name)
        if os.path.isdir(work_path):
            image_files = []
            for ext in ['*.jpg', '*.jpeg', '*.png', '*.tif', '*.tiff']:
                image_files.extend(glob.glob(os.path.join(work_path, ext)))

            if 1 <= len(image_files) <= 5:
                quick_wins.append((work_name, work_path))

    print(f"Found {len(quick_wins)} N, P, R quick win works to process")

    # Read current works.json
    with open('works.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    processed_count = 0
    new_entries = []

    for work_name, work_path in quick_wins:
        work_entry = process_single_work(work_name, work_path)
        if work_entry:
            new_entries.append(work_entry)
            processed_count += 1

    # Add new entries to JSON (at the beginning for chronological order)
    data['works'] = new_entries + data['works']

    # Write updated JSON
    with open('works.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n=== BATCH PROCESSING COMPLETE ===")
    print(f"Successfully processed: {processed_count} N, P, R quick win works")
    print(f"Total works now: {len(data['works'])}")
    print(f"New entries added to beginning of works.json")

    return processed_count

if __name__ == "__main__":
    count = batch_process_npr_quick_wins()