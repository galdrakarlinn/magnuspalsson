#!/usr/bin/env python3
"""
Image resizing script for Magnus Palsson website optimization.
Resizes images to maximum 800x600 while maintaining aspect ratio.
"""

import os
import sys
from PIL import Image
import argparse

def resize_image(input_path, output_path, max_width=800, max_height=600, quality=85):
    """
    Resize an image to fit within max_width x max_height while maintaining aspect ratio.
    """
    try:
        with Image.open(input_path) as img:
            # Convert to RGB if necessary (for PNG with transparency)
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')

            # Calculate new size maintaining aspect ratio
            width, height = img.size
            aspect_ratio = width / height

            if width > max_width or height > max_height:
                if aspect_ratio > max_width / max_height:
                    # Width is the limiting factor
                    new_width = max_width
                    new_height = int(max_width / aspect_ratio)
                else:
                    # Height is the limiting factor
                    new_height = max_height
                    new_width = int(max_height * aspect_ratio)

                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Save with specified quality
            img.save(output_path, 'JPEG', quality=quality, optimize=True)
            print(f"Resized {input_path} -> {output_path} ({img.size[0]}x{img.size[1]})")
            return True

    except Exception as e:
        print(f"Error processing {input_path}: {e}")
        return False

def process_directory(input_dir, output_dir, max_width=800, max_height=600):
    """
    Process all images in a directory, creating resized versions in output directory.
    """
    if not os.path.exists(input_dir):
        print(f"Input directory {input_dir} does not exist")
        return

    processed = 0
    skipped = 0
    errors = 0

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            input_path = os.path.join(input_dir, filename)

            # Skip if it's already a directory (like medium/, thumbs/)
            if os.path.isdir(input_path):
                continue

            # Create output filename
            name, ext = os.path.splitext(filename)
            output_filename = f"{name}-medium.jpg"
            output_path = os.path.join(output_dir, output_filename)

            # Skip if output already exists
            if os.path.exists(output_path):
                print(f"Skipping {filename} - medium version already exists")
                skipped += 1
                continue

            if resize_image(input_path, output_path, max_width, max_height):
                processed += 1
            else:
                errors += 1

    print(f"\nProcessing complete: {processed} processed, {skipped} skipped, {errors} errors")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resize images for Magnus Palsson website")
    parser.add_argument("input_dir", help="Input directory containing images")
    parser.add_argument("--output_dir", help="Output directory (default: input_dir/medium)")
    parser.add_argument("--width", type=int, default=800, help="Maximum width (default: 800)")
    parser.add_argument("--height", type=int, default=600, help="Maximum height (default: 600)")

    args = parser.parse_args()

    output_dir = args.output_dir or os.path.join(args.input_dir, "medium")
    process_directory(args.input_dir, output_dir, args.width, args.height)