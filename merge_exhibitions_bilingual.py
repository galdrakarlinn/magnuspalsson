#!/usr/bin/env python3
"""
Merge exhibitions-en.json and exhibitions-is.json into single bilingual exhibitions.json
with unique IDs for each exhibition.
"""

import json
import re

def generate_exhibition_id(title, year):
    """Generate a unique ID from title and year"""
    # Take English title, lowercase, remove special chars, replace spaces with hyphens
    id_base = re.sub(r'[^\w\s-]', '', title.lower())
    id_base = re.sub(r'\s+', '-', id_base.strip())
    # Remove multiple hyphens
    id_base = re.sub(r'-+', '-', id_base)
    # Limit length and add year
    id_base = id_base[:50].strip('-')
    return f"{id_base}-{year}"

def merge_exhibitions():
    """Merge EN and IS exhibition files into bilingual format with IDs"""

    # Load both files
    with open('translations/exhibitions-en.json', 'r', encoding='utf-8') as f:
        en = json.load(f)

    with open('translations/exhibitions-is.json', 'r', encoding='utf-8') as f:
        is_ex = json.load(f)

    # Create bilingual exhibitions
    bilingual = {
        "ui": {
            "en": en.get("ui", {}),
            "is": is_ex.get("ui", {})
        },
        "solo": [],
        "group": []
    }

    # Process solo exhibitions
    print("Processing solo exhibitions...")
    for en_item, is_item in zip(en.get("solo", []), is_ex.get("solo", [])):
        # Verify they match by year
        if en_item.get("year") != is_item.get("year"):
            print(f"  WARNING: Year mismatch - EN:{en_item.get('year')} IS:{is_item.get('year')}")

        # Generate ID
        exhibition_id = generate_exhibition_id(en_item.get("title", ""), en_item.get("year", ""))

        exhibition = {
            "id": exhibition_id,
            "year": str(en_item.get("year", "")),
            "title": {
                "en": en_item.get("title", ""),
                "is": is_item.get("title", "")
            },
            "venue": {
                "en": en_item.get("venue", ""),
                "is": is_item.get("venue", "")
            },
            "location": en_item.get("location", "")
        }

        # Add notes if present (bilingual)
        if en_item.get("notes") or is_item.get("notes"):
            exhibition["notes"] = {
                "en": en_item.get("notes", ""),
                "is": is_item.get("notes", "")
            }

        bilingual["solo"].append(exhibition)

    # Process group exhibitions
    print("Processing group exhibitions...")
    for en_item, is_item in zip(en.get("group", []), is_ex.get("group", [])):
        # Verify they match by year
        if en_item.get("year") != is_item.get("year"):
            print(f"  WARNING: Year mismatch - EN:{en_item.get('year')} IS:{is_item.get('year')}")

        # Generate ID
        exhibition_id = generate_exhibition_id(en_item.get("title", ""), en_item.get("year", ""))

        exhibition = {
            "id": exhibition_id,
            "year": str(en_item.get("year", "")),
            "title": {
                "en": en_item.get("title", ""),
                "is": is_item.get("title", "")
            },
            "venue": {
                "en": en_item.get("venue", ""),
                "is": is_item.get("venue", "")
            },
            "location": en_item.get("location", "")
        }

        # Add notes if present (bilingual)
        if en_item.get("notes") or is_item.get("notes"):
            exhibition["notes"] = {
                "en": en_item.get("notes", ""),
                "is": is_item.get("notes", "")
            }

        bilingual["group"].append(exhibition)

    # Save bilingual exhibitions.json
    with open('exhibitions.json', 'w', encoding='utf-8') as f:
        json.dump(bilingual, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Created exhibitions.json")
    print(f"  Solo: {len(bilingual['solo'])} exhibitions")
    print(f"  Group: {len(bilingual['group'])} exhibitions")

    # Show some sample IDs
    print(f"\nSample IDs:")
    for ex in bilingual['solo'][:3]:
        print(f"  {ex['id']} - {ex['title']['en']}")

if __name__ == '__main__':
    merge_exhibitions()
