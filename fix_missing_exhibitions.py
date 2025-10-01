#!/usr/bin/env python3
"""
Fix missing exhibitions property for restored works that are causing JavaScript errors.
"""

import json

def fix_missing_exhibitions():
    """Add missing exhibitions arrays to works that don't have them."""

    # Read current works.json
    with open('works.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    fixed_count = 0

    # Process each work
    for work in data['works']:
        # Check if exhibitions property is missing
        if 'exhibitions' not in work:
            work['exhibitions'] = []
            fixed_count += 1
            print(f"Added empty exhibitions array to: {work.get('title', 'Unknown')} ({work.get('id', 'no-id')})")

        # Also ensure materials property exists (JavaScript might expect this too)
        if 'materials' not in work:
            work['materials'] = []
            print(f"Added empty materials array to: {work.get('title', 'Unknown')} ({work.get('id', 'no-id')})")

    # Write updated JSON
    with open('works.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\nOK: Fixed {fixed_count} works missing exhibitions property")
    print("All works now have exhibitions and materials arrays (empty if no data)")

if __name__ == "__main__":
    fix_missing_exhibitions()