#!/usr/bin/env python3

import os
import shutil
import sys

# Files to move to archive (these are the specific files we just processed)
files_to_archive = [
    'images/draumur-hlynsins-um-fjall-1974/Hanging mountain.png',
    'images/galleri-gangur-1982/Cockerel.jpg',
    'images/gapassipi-1995/Gapassipi 1.JPG',
    'images/g-ljod-2009/G-ljóð1 front page 2009.jpg',
    'images/gibsborn-children-1971/Children Lund.jpg',
    'images/hattar-1969-71/IMG_0199.jpg',
    'images/hrognkelsaveifa-strandlegjan-1998/Beach sculpture 1.jpg',
    'images/jonsmessunott-bank-piece-1982/Whole piece.JPG',
    'images/jorgen-bruun-hansen-2013/Jörgen BH pencil sketch MP.jpg'
]

archive_base = '../images-not-used'

print("Moving original large files to archive...")

for file_path in files_to_archive:
    if os.path.exists(file_path):
        # Extract directory structure
        dir_name = os.path.dirname(file_path).replace('images/', '')
        filename = os.path.basename(file_path)

        # Create archive directory structure
        archive_dir = os.path.join(archive_base, dir_name)
        os.makedirs(archive_dir, exist_ok=True)

        # Move file
        dest_path = os.path.join(archive_dir, filename)
        print(f"Moving: {file_path} -> {dest_path}")

        # If destination exists, add a timestamp
        if os.path.exists(dest_path):
            import time
            timestamp = int(time.time())
            name, ext = os.path.splitext(filename)
            dest_path = os.path.join(archive_dir, f"{name}_{timestamp}{ext}")
            print(f"  Destination exists, using: {dest_path}")

        shutil.move(file_path, dest_path)
    else:
        print(f"File not found (may already be archived): {file_path}")

print("Archive process completed!")