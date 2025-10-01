#!/usr/bin/env python3
"""
Process the remaining K, L, M works that were missed in the initial batch processing.
These include PDF-only works, single files, and collections with non-image files.
"""

import os
import json
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

def process_single_tif_as_work(file_path, work_name):
    """Process a single TIF file as a complete work."""

    work_id = clean_work_id(work_name)
    print(f"\nProcessing single TIF work: {work_name} -> {work_id}")

    # Create folder structure
    work_folder = f"images/{work_id}"
    os.makedirs(f"{work_folder}/medium", exist_ok=True)
    os.makedirs(f"{work_folder}/thumbs", exist_ok=True)

    try:
        # Process medium image
        medium_path = f"{work_folder}/medium/{work_id}-01-medium.jpg"
        subprocess.run([
            'ffmpeg', '-i', file_path, '-y',
            '-vf', 'scale=800:600:force_original_aspect_ratio=decrease',
            '-q:v', '3',
            medium_path
        ], check=True, capture_output=True)

        # Process thumbnail
        thumb_path = f"{work_folder}/thumbs/{work_id}-01-thumb.jpg"
        subprocess.run([
            'ffmpeg', '-i', file_path, '-y',
            '-vf', 'scale=150:150:force_original_aspect_ratio=increase,crop=150:150',
            '-q:v', '4',
            thumb_path
        ], check=True, capture_output=True)

        # Extract year
        year = "Unknown"
        for word in work_name.split():
            if word.isdigit() and len(word) == 4 and word.startswith(('19', '20')):
                year = int(word)
                break

        # Create JSON entry
        work_entry = {
            "id": work_id,
            "title": work_name.replace('.tif', '').replace('.TIF', ''),
            "year": year,
            "description": f"A work by Magnús Pálsson from {year}. This piece represents his artistic exploration during this period.",
            "images": [
                {
                    "url": f"images/{work_id}/medium/{work_id}-01-medium.jpg",
                    "caption": f"{work_name.split()[0]} - main view"
                }
            ],
            "tags": ["artwork", str(year) if year != "Unknown" else "undated"],
            "exhibitions": [],
            "materials": [],
            "searchText": f"{work_name.lower()} {year} magnús pálsson"
        }

        print(f"  Successfully processed: {work_name}")
        return work_entry

    except subprocess.CalledProcessError as e:
        print(f"  Error processing {work_name}: {e}")
        return None

def process_pdf_work(folder_path, work_name):
    """Process a work that consists mainly of PDFs."""

    work_id = clean_work_id(work_name)
    print(f"\nProcessing PDF work: {work_name} -> {work_id}")

    # Create folder structure
    work_folder = f"images/{work_id}"
    os.makedirs(work_folder, exist_ok=True)

    # Copy PDF files to the work folder
    pdf_files = []
    for file in os.listdir(folder_path):
        if file.lower().endswith('.pdf'):
            src = os.path.join(folder_path, file)
            dst = os.path.join(work_folder, file)
            shutil.copy2(src, dst)
            pdf_files.append(file)

    if not pdf_files:
        print(f"  No PDF files found in {work_name}")
        return None

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
        "description": f"A documentation or text-based work by Magnús Pálsson from {year}. This work includes written materials and documentation that form part of his artistic practice.",
        "images": [],  # No images for PDF-only works
        "tags": ["documentation", "text", str(year) if year != "Unknown" else "undated"],
        "exhibitions": [],
        "materials": ["text", "documentation"],
        "searchText": f"{work_name.lower()} {year} magnús pálsson documentation text"
    }

    print(f"  Successfully processed: {work_name} with {len(pdf_files)} PDF files")
    return work_entry

def process_documentation_work(folder_path, work_name):
    """Process a work with documentation files (videos, texts, etc.)."""

    work_id = clean_work_id(work_name)
    print(f"\nProcessing documentation work: {work_name} -> {work_id}")

    # Create folder structure
    work_folder = f"images/{work_id}"
    os.makedirs(work_folder, exist_ok=True)

    # Copy relevant files
    doc_files = []
    for file in os.listdir(folder_path):
        if file.lower().endswith(('.pdf', '.doc', '.txt')):
            src = os.path.join(folder_path, file)
            dst = os.path.join(work_folder, file)
            shutil.copy2(src, dst)
            doc_files.append(file)

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
        "description": f"A performance and documentation work by Magnús Pálsson from {year}. This work includes scripts, documentation, and materials from the performance or exhibition.",
        "images": [],  # No images for documentation-only works
        "tags": ["performance", "documentation", "text", str(year) if year != "Unknown" else "undated"],
        "exhibitions": [],
        "materials": ["performance", "documentation", "text"],
        "searchText": f"{work_name.lower()} {year} magnús pálsson performance documentation"
    }

    print(f"  Successfully processed: {work_name} with {len(doc_files)} documentation files")
    return work_entry

def process_remaining_klm_works():
    """Process the remaining K, L, M works that were missed."""

    base_path = r"C:\Users\VeigaMagnusdottir\projects\magnusPalsson\images-not-used"

    # Read current works.json
    with open('works.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    new_entries = []

    # 1. Process single TIF files
    single_tifs = [
        ("Magnús Pálsson Hvískur  2 1975 JAS-1 3.tif", "Hvískur 2 1975"),
        ("MP 04.tif", "MP 04"),
        ("MP 08.tif", "MP 08"),
        ("MP 10.tif", "MP 10")
    ]

    for filename, work_name in single_tifs:
        file_path = os.path.join(base_path, filename)
        if os.path.exists(file_path):
            work_entry = process_single_tif_as_work(file_path, work_name)
            if work_entry:
                new_entries.append(work_entry)

    # 2. Process PDF-only work
    pdf_work = "Kennaraskóli Íslands model with DR"
    pdf_path = os.path.join(base_path, pdf_work)
    if os.path.exists(pdf_path):
        work_entry = process_pdf_work(pdf_path, pdf_work)
        if work_entry:
            new_entries.append(work_entry)

    # 3. Process documentation work
    doc_work = "Mutations Stökkbreytingar Dada TATE Hackney empire 2005"
    doc_path = os.path.join(base_path, doc_work)
    if os.path.exists(doc_path):
        work_entry = process_documentation_work(doc_path, doc_work)
        if work_entry:
            new_entries.append(work_entry)

    # Add new entries to JSON
    data['works'] = new_entries + data['works']

    # Write updated JSON
    with open('works.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n=== REMAINING K, L, M PROCESSING COMPLETE ===")
    print(f"Successfully processed: {len(new_entries)} additional works")
    print(f"Total works now: {len(data['works'])}")

    return len(new_entries)

if __name__ == "__main__":
    count = process_remaining_klm_works()