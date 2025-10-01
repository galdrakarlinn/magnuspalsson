#!/usr/bin/env python3
"""
Fix image optimization for restored works - proper resizing and cleanup.
"""

import os
import subprocess
import glob

def optimize_restored_images():
    """Optimize images for the restored works and clean up root folders."""

    restored_folders = [
        "bestu-stykkin",
        "augustus-my-god-1984",
        "thyrlulending",
        "vidtol-um-daudann-2011",
        "draumur-hlynsins-um-fjall-1974",
        "master-plaster-caster-2013"
    ]

    for folder in restored_folders:
        folder_path = f"images/{folder}"

        if not os.path.exists(folder_path):
            print(f"Skipping {folder} - folder not found")
            continue

        print(f"\n=== Processing {folder} ===")

        # Get all image files in root (excluding directories and non-images)
        root_images = []
        for ext in ['*.jpg', '*.jpeg', '*.png', '*.tif', '*.tiff']:
            root_images.extend(glob.glob(f"{folder_path}/{ext}"))

        # Process each image in root
        for img_path in root_images:
            filename = os.path.basename(img_path)
            name_without_ext = os.path.splitext(filename)[0]

            # Skip if it's already a processed file
            if '-medium' in filename or '-thumb' in filename or '-full' in filename:
                continue

            print(f"Processing: {filename}")

            # Create full copy (original resolution but JPEG compressed)
            full_path = f"{folder_path}/full/{name_without_ext}-full.jpg"
            os.makedirs(f"{folder_path}/full", exist_ok=True)

            # Medium version (800x600 max, maintaining aspect ratio)
            medium_path = f"{folder_path}/medium/{name_without_ext}-medium.jpg"
            os.makedirs(f"{folder_path}/medium", exist_ok=True)

            # Thumbnail version (150x150, cropped square)
            thumb_path = f"{folder_path}/thumbs/{name_without_ext}-thumb.jpg"
            os.makedirs(f"{folder_path}/thumbs", exist_ok=True)

            try:
                # Create full version (original size, JPEG compressed)
                subprocess.run([
                    'ffmpeg', '-i', img_path, '-y',
                    '-q:v', '2',  # High quality
                    full_path
                ], check=True, capture_output=True)

                # Create medium version (max 800x600, maintain aspect ratio)
                subprocess.run([
                    'ffmpeg', '-i', img_path, '-y',
                    '-vf', 'scale=800:600:force_original_aspect_ratio=decrease',
                    '-q:v', '3',  # Good quality
                    medium_path
                ], check=True, capture_output=True)

                # Create thumbnail (150x150 square, cropped)
                subprocess.run([
                    'ffmpeg', '-i', img_path, '-y',
                    '-vf', 'scale=150:150:force_original_aspect_ratio=increase,crop=150:150',
                    '-q:v', '4',  # Reasonable quality for thumbs
                    thumb_path
                ], check=True, capture_output=True)

                print(f"  Created: full, medium, thumb")

                # Remove original from root
                os.remove(img_path)
                print(f"  Removed original: {filename}")

            except subprocess.CalledProcessError as e:
                print(f"  Error processing {filename}: {e}")
            except Exception as e:
                print(f"  Unexpected error with {filename}: {e}")

    print(f"\nOK: Image optimization complete for restored works")
    print("All original files removed from root directories")
    print("Medium images resized to max 800x600")
    print("Thumbnails resized to 150x150 squares")

if __name__ == "__main__":
    optimize_restored_images()