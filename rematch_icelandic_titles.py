#!/usr/bin/env python3
"""
Re-match thumbnails using Icelandic titles
Many works exist on website with Icelandic names
"""

import json
from pathlib import Path
from difflib import SequenceMatcher

# Paths
PROJECT_DIR = Path(__file__).parent
WORKS_JSON = PROJECT_DIR / "works.json"
THUMBNAIL_DATA = PROJECT_DIR / "thumbnail_mapping_bilingual.json"
NEW_WORKS_LIST = PROJECT_DIR / "new_works_to_create.json"

# Already processed thumbnails
PROCESSED = {
    '1', '2', '3', '4', '5', '6', '7', '8', '10', '11', '13', '14', '21', '22', '23', '24',
    '25', '26', '27', '30', '31', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42',
    '43', '44', '45', '46', '47', '49', '50', '51', '52', '53', '54', '55', '57', '58', '59',
    '60', '61', '63', '65', '66', '67', '68', '69', '70', '71', '72', '73', '75', '76', '77',
    '81', '88', '124', '127', '129', '132', '138', '62', '28', '74',
    '119', '126', '151', '148', '85', '96', '136', '86', '97', '143', '102',
    '89', '113', '128', '150', '107', '139', '100', '123', '147',
    '80', '104', '140', '115', '130', '133',
}

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def normalize_title(title):
    """Normalize title for comparison"""
    if not title:
        return ""
    # Remove common words, parentheses, punctuation
    title = title.lower()
    for word in ['(', ')', ',', '.', ':', '-', '/', '\\']:
        title = title.replace(word, ' ')
    # Remove extra spaces
    title = ' '.join(title.split())
    return title

def title_similarity(title1, title2):
    """Calculate similarity between two titles"""
    t1 = normalize_title(title1)
    t2 = normalize_title(title2)
    return SequenceMatcher(None, t1, t2).ratio()

def find_work_by_icelandic_title(thumb_data, works_list):
    """Find work using Icelandic title"""
    thumb_title_is = thumb_data.get('title_is', '')
    thumb_title_en = thumb_data.get('title_en', '')
    thumb_year = str(thumb_data.get('year', ''))

    if not thumb_title_is and not thumb_title_en:
        return None

    best_match = None
    best_score = 0.0

    for work in works_list:
        work_title_is = work.get('title', {}).get('is', '')
        work_title_en = work.get('title', {}).get('en', '')
        work_year = str(work.get('year', ''))

        # Check if already has book thumbnail
        has_book_thumb = any('book-thumbnail' in img.get('url', '') for img in work.get('images', []))
        if has_book_thumb:
            continue

        # Try Icelandic title match
        score_is = 0
        if thumb_title_is and work_title_is:
            score_is = title_similarity(thumb_title_is, work_title_is)

        # Try English title match
        score_en = 0
        if thumb_title_en and work_title_en:
            score_en = title_similarity(thumb_title_en, work_title_en)

        # Use best score
        score = max(score_is, score_en)

        # Bonus for year match
        if thumb_year and work_year:
            if thumb_year in work_year or work_year in thumb_year:
                score += 0.2

        if score > best_score and score > 0.65:  # Lower threshold for better matches
            best_match = {
                'work': work,
                'score': score,
                'match_type': 'IS' if score_is > score_en else 'EN'
            }
            best_score = score

    return best_match

def main():
    print("Re-match Thumbnails Using Icelandic Titles")
    print("="*80)

    # Load data
    works_data = load_json(WORKS_JSON)
    thumbnail_data_list = load_json(THUMBNAIL_DATA)
    new_works_list = load_json(NEW_WORKS_LIST)

    # Get unprocessed thumbnail numbers
    unprocessed_nums = {item['thumb_num'] for item in new_works_list}

    print(f"Re-checking {len(unprocessed_nums)} thumbnails")
    print()

    found_matches = []
    still_unmatched = []

    for thumb_data in thumbnail_data_list:
        thumb_num = thumb_data.get('number')

        if thumb_num not in unprocessed_nums:
            continue

        # Try to find match
        match = find_work_by_icelandic_title(thumb_data, works_data['works'])

        if match:
            work = match['work']
            print(f"MATCH FOUND: #{thumb_num}")
            print(f"  Thumbnail: {thumb_data.get('title_en')} / {thumb_data.get('title_is')} ({thumb_data.get('year')})")
            print(f"  Work: {work.get('title', {}).get('en')} / {work.get('title', {}).get('is')} ({work.get('year')})")
            print(f"  Score: {match['score']:.2f} ({match['match_type']} match)")
            print()

            found_matches.append({
                'thumb_num': thumb_num,
                'work_id': work['id'],
                'score': match['score'],
                'thumb_title_en': thumb_data.get('title_en'),
                'thumb_title_is': thumb_data.get('title_is'),
                'work_title_en': work.get('title', {}).get('en'),
                'work_title_is': work.get('title', {}).get('is'),
            })
        else:
            still_unmatched.append(thumb_data)

    # Save results
    if found_matches:
        output_path = PROJECT_DIR / "icelandic_rematches.json"
        save_json(output_path, found_matches)
        print(f"Saved {len(found_matches)} new matches to: icelandic_rematches.json")

    if still_unmatched:
        output_path = PROJECT_DIR / "truly_new_works.json"
        save_json(output_path, still_unmatched)
        print(f"Saved {len(still_unmatched)} truly new works to: truly_new_works.json")

    # Summary
    print()
    print("="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Thumbnails re-checked: {len(unprocessed_nums)}")
    print(f"New matches found: {len(found_matches)}")
    print(f"Truly new works: {len(still_unmatched)}")

if __name__ == '__main__':
    main()
