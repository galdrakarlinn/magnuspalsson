#!/usr/bin/env python3
"""
Clean up duplicate restored works and add missing master-plaster-caster work.
"""

import json

def clean_and_complete_restored_works():
    """Remove duplicates and add missing works."""

    # Read current works.json
    with open('works.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Track seen IDs to remove duplicates
    seen_ids = set()
    cleaned_works = []

    # First pass: remove duplicates, keeping the one with images
    for work in data['works']:
        work_id = work.get('id')
        if work_id not in seen_ids:
            seen_ids.add(work_id)
            cleaned_works.append(work)
        else:
            # If we've seen this ID before, check if this version has images
            existing_work = next(w for w in cleaned_works if w.get('id') == work_id)
            if not existing_work.get('images') and work.get('images'):
                # Replace the existing work with this one that has images
                for i, w in enumerate(cleaned_works):
                    if w.get('id') == work_id:
                        cleaned_works[i] = work
                        break
            print(f"Removed duplicate: {work.get('title', 'Unknown')} ({work_id})")

    # Add master-plaster-caster work if not present
    if 'master_plaster_caster_2013' not in seen_ids:
        master_work = {
            "id": "master_plaster_caster_2013",
            "title": "Master Plaster Caster",
            "year": 2013,
            "description": "An installation work exploring themes of casting, reproduction, and material transformation. Created as part of Pálsson's ongoing investigation into the relationship between original and copy, presence and absence.",
            "images": [
                {
                    "url": "images/master-plaster-caster-2013/medium/master-plaster-caster-installation-medium.jpg",
                    "caption": "Master Plaster Caster Installation"
                }
            ],
            "tags": [
                "installation",
                "sculpture",
                "plaster",
                "casting",
                "reproduction",
                "2010s"
            ],
            "searchText": "master plaster caster installation sculpture casting reproduction material transformation 2013"
        }
        # Add at the beginning with other restored works
        cleaned_works.insert(5, master_work)  # After the other restored works
        print(f"Added missing work: Master Plaster Caster (2013)")

    # Update data
    data['works'] = cleaned_works

    # Write updated JSON
    with open('works.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\nOK: Cleaned works list")
    print(f"Total works now: {len(cleaned_works)}")

    # Verify restored works are present
    restored_ids = ["bestu_stykkin", "augustus_my_god", "thyrlulending", "vidtol_um_daudann_2011",
                   "draumur_hlynsins_um_fjall_1974", "master_plaster_caster_2013"]

    print("\nRestored works verification:")
    for work_id in restored_ids:
        work = next((w for w in cleaned_works if w.get('id') == work_id), None)
        if work:
            img_count = len(work.get('images', []))
            print(f"✓ {work['title']} ({work['year']}) - {img_count} images")
        else:
            print(f"✗ Missing: {work_id}")

if __name__ == "__main__":
    clean_and_complete_restored_works()