#!/usr/bin/env python3
"""
Fix studios.html to reference the correct filenames with -medium suffix.
"""

import re
import os

def fix_studios_html():
    """Update studios.html to use correct -medium filename references."""

    # Read the current studios.html
    with open('studios.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all image src references to studios
    pattern = r'src="images/studios/medium/([^"]+\.jpg)"'

    def replace_src(match):
        filename = match.group(1)

        # If filename doesn't end with -medium.jpg, add it
        if not filename.endswith('-medium.jpg'):
            base_name = filename.replace('.jpg', '')
            new_filename = f"{base_name}-medium.jpg"

            # Check if the file with -medium suffix actually exists
            file_path = f"images/studios/medium/{new_filename}"
            if os.path.exists(file_path):
                print(f"Updating reference: {filename} -> {new_filename}")
                return f'src="images/studios/medium/{new_filename}"'
            else:
                # Check if file exists without suffix
                file_path_no_suffix = f"images/studios/medium/{filename}"
                if os.path.exists(file_path_no_suffix):
                    print(f"Keeping existing reference (file exists): {filename}")
                    return match.group(0)
                else:
                    print(f"Warning: Neither {filename} nor {new_filename} exists")
                    return match.group(0)
        else:
            # Already has -medium suffix
            return match.group(0)

    # Apply the replacements
    updated_content = re.sub(pattern, replace_src, content)

    # Write the updated HTML back
    with open('studios.html', 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print("\nstudios.html has been updated to use correct filename references.")

if __name__ == "__main__":
    fix_studios_html()