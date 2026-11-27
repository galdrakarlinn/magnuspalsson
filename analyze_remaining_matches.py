#!/usr/bin/env python3
"""
Analyze remaining partial matches and categorize them
"""

import json
from pathlib import Path
import csv

# Paths
PROJECT_DIR = Path(__file__).parent
WORKS_JSON = PROJECT_DIR / "works.json"
THUMBNAIL_DATA = PROJECT_DIR / "thumbnail_mapping_bilingual.json"
MATCH_REPORT = PROJECT_DIR / "thumbnail_match_report.csv"

# Already processed thumbnails
PROCESSED = {
    # HIGH scores
    '119', '126', '151', '148', '85', '96', '136', '86', '97', '143', '102',
    '89', '113', '128', '150', '107', '139', '100', '123', '147',
    # MEDIUM likely
    '80', '104', '140', '115', '3', '130', '133',
    # Manual corrections
    '62', '28', '74',
}

# Known new works
NEW_WORKS = {
    '17', '19', '20', '111'
}

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    print("Analyze Remaining Partial Matches - Phase 2")
    print("="*80)

    # Load data
    works_data = load_json(WORKS_JSON)
    thumbnail_data_list = load_json(THUMBNAIL_DATA)
    thumb_data_map = {t['number']: t for t in thumbnail_data_list}
    works_map = {w['id']: w for w in works_data['works']}

    # Load all partial matches
    all_matches = []
    with open(MATCH_REPORT, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            if len(row) >= 8 and row[0].upper() == 'PARTIAL':
                try:
                    score = float(row[7])
                except (ValueError, IndexError):
                    score = 0
                all_matches.append({
                    'thumb_num': row[1],
                    'thumb_title': row[2],
                    'thumb_year': row[3],
                    'work_id': row[4],
                    'work_title': row[5],
                    'work_year': row[6],
                    'score': score
                })

    # Filter to unprocessed
    remaining = [m for m in all_matches if m['thumb_num'] not in PROCESSED and m['thumb_num'] not in NEW_WORKS]
    remaining.sort(key=lambda x: x['score'], reverse=True)

    print(f"Total partial matches: {len(all_matches)}")
    print(f"Already processed: {len(PROCESSED)}")
    print(f"Known new works: {len(NEW_WORKS)}")
    print(f"Remaining to review: {len(remaining)}")
    print()

    # Categorize remaining
    likely_matches = []
    uncertain = []

    for match in remaining:
        thumb_num = match['thumb_num']
        work_id = match['work_id']

        thumb_data = thumb_data_map.get(thumb_num)
        work = works_map.get(work_id)

        if not thumb_data or not work:
            uncertain.append(match)
            continue

        thumb_year = str(thumb_data.get('year', ''))
        work_year = str(work.get('year', ''))

        # Check if years match
        years_match = thumb_year in work_year or work_year in thumb_year

        # Check if titles are very similar
        thumb_title = match['thumb_title'].lower()
        work_title = match['work_title'].lower()

        # Remove common words for comparison
        for word in ['(', ')', 'the', 'a', 'an']:
            thumb_title = thumb_title.replace(word, '')
            work_title = work_title.replace(word, '')

        # If years match and titles have significant overlap
        if years_match and (thumb_title in work_title or work_title in thumb_title or match['score'] > 0.60):
            likely_matches.append(match)
        else:
            uncertain.append(match)

    # Print results
    print("="*80)
    print(f"LIKELY MATCHES ({len(likely_matches)}):")
    print("="*80)
    for match in likely_matches:
        thumb_data = thumb_data_map.get(match['thumb_num'])
        work = works_map.get(match['work_id'])

        print(f"#{match['thumb_num']}: {match['thumb_title']} ({match['thumb_year']}) [score: {match['score']}]")
        print(f"  -> {match['work_id']}: {match['work_title']} ({match['work_year']})")

        if thumb_data and work:
            thumb_year = thumb_data.get('year', 'N/A')
            work_year = work.get('year', 'N/A')
            if str(thumb_year) != str(work_year):
                print(f"  NOTE: Year difference - thumb: {thumb_year}, work: {work_year}")
        print()

    print("="*80)
    print(f"UNCERTAIN / LIKELY NEW WORKS ({len(uncertain)}):")
    print("="*80)
    for match in uncertain:
        thumb_data = thumb_data_map.get(match['thumb_num'])
        work = works_map.get(match['work_id'])

        print(f"#{match['thumb_num']}: {match['thumb_title']} ({match['thumb_year']}) [score: {match['score']}]")
        print(f"  -> {match['work_id']}: {match['work_title']} ({match['work_year']})")

        if thumb_data and work:
            thumb_year = thumb_data.get('year', 'N/A')
            work_year = work.get('year', 'N/A')
            if str(thumb_year) != str(work_year):
                print(f"  Year mismatch: {thumb_year} vs {work_year}")
        print()

    # Summary
    print("="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Processed so far: {len(PROCESSED)} matches")
    print(f"Known new works: {len(NEW_WORKS)} thumbnails")
    print(f"Likely matches remaining: {len(likely_matches)}")
    print(f"Uncertain/probably new: {len(uncertain)}")
    print()
    print(f"Total Phase 2: {len(PROCESSED)} / {len(all_matches)} matches processed")
    print(f"Remaining work: {len(remaining)} matches to review")

if __name__ == '__main__':
    main()
