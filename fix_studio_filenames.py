#!/usr/bin/env python3
"""
Fix studio image filenames to match what studios.html expects.
Remove -medium suffix from filenames in the medium folder.
"""

import os
import re

def fix_studio_filenames():
    """Rename studio files to remove -medium suffix."""

    studio_dir = "images/studios/medium/"

    if not os.path.exists(studio_dir):
        print(f"Directory {studio_dir} not found")
        return False

    # Get all files in the medium directory
    files = os.listdir(studio_dir)
    renamed_count = 0

    for filename in files:
        if filename.endswith('-medium.jpg'):
            # Remove the -medium suffix
            new_filename = filename.replace('-medium.jpg', '.jpg')

            old_path = os.path.join(studio_dir, filename)
            new_path = os.path.join(studio_dir, new_filename)

            # Check if target file already exists
            if os.path.exists(new_path):
                print(f"Warning: {new_filename} already exists, skipping {filename}")
                continue

            # Rename the file
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} → {new_filename}")
            renamed_count += 1

    print(f"\nRenamed {renamed_count} files in {studio_dir}")

    # Also check thumbs directory for consistency
    thumbs_dir = "images/studios/thumbs/"
    if os.path.exists(thumbs_dir):
        thumbs_files = os.listdir(thumbs_dir)
        thumbs_renamed = 0

        for filename in thumbs_files:
            if filename.endswith('-thumb.jpg'):
                # Rename to remove -thumb suffix for consistency
                new_filename = filename.replace('-thumb.jpg', '.jpg')

                old_path = os.path.join(thumbs_dir, filename)
                new_path = os.path.join(thumbs_dir, new_filename)

                # Check if target file already exists
                if os.path.exists(new_path):
                    print(f"Warning: {new_filename} already exists in thumbs, skipping {filename}")
                    continue

                # Rename the file
                os.rename(old_path, new_path)
                print(f"Thumbs renamed: {filename} → {new_filename}")
                thumbs_renamed += 1

        print(f"Renamed {thumbs_renamed} files in {thumbs_dir}")

    return renamed_count > 0

if __name__ == "__main__":
    if fix_studio_filenames():
        print("\nStudio filenames have been fixed to match HTML references.")
    else:
        print("\nNo files needed renaming.")