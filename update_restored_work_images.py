#!/usr/bin/env python3
"""
Update JSON references for the restored works with their actual image files.
"""

import json
import os
import glob

def update_restored_work_images():
    """Update JSON with actual image references for restored works."""

    # Read current works.json
    with open('works.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Define the restored work IDs and their image folders
    restored_works = {
        "bestu_stykkin": "bestu-stykkin",
        "augustus_my_god": "augustus-my-god-1984",
        "thyrlulending": "thyrlulending",
        "vidtol_um_daudann_2011": "vidtol-um-daudann-2011",
        "draumur_hlynsins_um_fjall_1974": "draumur-hlynsins-um-fjall-1974",
        "master_plaster_caster_2013": "master-plaster-caster-2013"
    }

    updates_made = 0

    # Process each work
    for work in data['works']:
        work_id = work.get('id')
        if work_id in restored_works:
            folder_name = restored_works[work_id]
            medium_path = f"images/{folder_name}/medium/"

            # Check if the medium folder exists
            if os.path.exists(medium_path):
                # Get all medium images
                medium_files = glob.glob(f"{medium_path}*-medium.jpg")
                medium_files.sort()  # Sort for consistent ordering

                # Create image objects for JSON
                images = []
                for img_file in medium_files:
                    # Extract filename from full path
                    filename = os.path.basename(img_file)
                    # Create relative URL
                    url = f"images/{folder_name}/medium/{filename}"

                    # Generate caption from filename
                    caption_base = filename.replace('-medium.jpg', '').replace('_', ' ').replace('-', ' ')
                    caption = caption_base.title()

                    images.append({
                        "url": url,
                        "caption": caption
                    })

                # Update the work's images
                work['images'] = images
                updates_made += 1
                print(f"Updated {work['title']} with {len(images)} images")

                # Print the image URLs for verification
                for img in images:
                    print(f"   - {img['url']}")
            else:
                print(f"Warning: Medium folder not found for {work['title']}: {medium_path}")

    # Write updated JSON
    with open('works.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\nOK: Updated {updates_made} restored works with image references")
    print("JSON file has been updated with actual image paths.")

if __name__ == "__main__":
    update_restored_work_images()