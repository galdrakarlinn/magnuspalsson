#!/usr/bin/env python3
"""
Fix thumbnail data errors discovered in truly_new_works_corrected.json
Based on CSV source data:
- #17: "Miami Beach" NOT "Flæðarmál (Beach)"
- #19: "Untitled plaster sculpture" NOT "Untitled (Gerður)"
- #20: "Untitled plaster sculpture" NOT "Untitled (Gerður)"
"""

import json
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
THUMB_BILINGUAL = PROJECT_DIR / "thumbnail_mapping_bilingual.json"
NEW_WORKS = PROJECT_DIR / "truly_new_works_corrected.json"

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    print("Fix Thumbnail Data Errors")
    print("="*80)
    print("Correcting #17, #19, #20 based on CSV source data")
    print()

    # Load data
    thumb_data = load_json(THUMB_BILINGUAL)
    new_works_data = load_json(NEW_WORKS)

    corrections = {
        '17': {
            'title_en': 'Miami Beach',
            'title_is': 'Miami Beach',
            'materials': ['cuboid of acrylic glass, mixed media'],
            'materials_is': ['kassalaga akrýlgler, blönduð tækni']
        },
        '19': {
            'title_en': 'Untitled plaster sculpture',
            'title_is': 'Án titils, gifsskúlptúrar',
            'materials': ['plaster'],
            'materials_is': ['gibs']
        },
        '20': {
            'title_en': 'Untitled plaster sculpture',
            'title_is': 'Án titils, gifsskúlptúrar',
            'materials': ['plaster'],
            'materials_is': ['gibs']
        }
    }

    # Fix thumbnail_mapping_bilingual.json
    print("Fixing thumbnail_mapping_bilingual.json...")
    print()
    for thumb in thumb_data:
        num = thumb.get('number', '')
        if num in corrections:
            old_title_en = thumb.get('title_en', '')
            old_title_is = thumb.get('title_is', '')

            thumb['title_en'] = corrections[num]['title_en']
            thumb['title_is'] = corrections[num]['title_is']
            thumb['materials'] = corrections[num]['materials']
            thumb['materials_is'] = corrections[num]['materials_is']

            print(f"#{num}:")
            print(f"  OLD: {old_title_en} / {old_title_is}")
            print(f"  NEW: {thumb['title_en']} / {thumb['title_is']}")
            print()

    # Fix truly_new_works_corrected.json
    print("Fixing truly_new_works_corrected.json...")
    print()
    for work in new_works_data:
        num = work.get('number', '')
        if num in corrections:
            old_title_en = work.get('title_en', '')
            old_title_is = work.get('title_is', '')

            work['title_en'] = corrections[num]['title_en']
            work['title_is'] = corrections[num]['title_is']
            work['materials'] = corrections[num]['materials']
            work['materials_is'] = corrections[num]['materials_is']

            print(f"#{num}:")
            print(f"  OLD: {old_title_en} / {old_title_is}")
            print(f"  NEW: {work['title_en']} / {work['title_is']}")
            print()

    # Save both files
    print("="*80)
    print("Saving corrected files...")
    save_json(THUMB_BILINGUAL, thumb_data)
    save_json(NEW_WORKS, new_works_data)
    print("SUCCESS!")
    print()

    # Summary
    print("="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Fixed 3 thumbnail entries:")
    print(f"  #17: Miami Beach (was Flæðarmál)")
    print(f"  #19: Untitled plaster sculpture (was Untitled Gerður)")
    print(f"  #20: Untitled plaster sculpture (was Untitled Gerður)")
    print()
    print("Note: Flæðarmál is a different work (#49) already on the website")
    print("Note: Gerði has nothing to do with #19 and #20")

if __name__ == '__main__':
    main()
