#!/usr/bin/env python3
"""
Review MEDIUM score matches and categorize them
Separate likely matches from uncertain ones
"""

import json
from pathlib import Path
import csv

# Paths
PROJECT_DIR = Path(__file__).parent
WORKS_JSON = PROJECT_DIR / "works.json"
THUMBNAIL_DATA = PROJECT_DIR / "thumbnail_mapping_bilingual.json"
MATCH_REPORT = PROJECT_DIR / "thumbnail_match_report.csv"

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    print("Review MEDIUM Score Matches (0.60-0.70)")
    print("="*80)

    # Load data
    works_data = load_json(WORKS_JSON)
    thumbnail_data_list = load_json(THUMBNAIL_DATA)
    thumb_data_map = {t['number']: t for t in thumbnail_data_list}
    works_map = {w['id']: w for w in works_data['works']}

    # Load MEDIUM score matches (0.60-0.70)
    medium_matches = []
    with open(MATCH_REPORT, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            if len(row) >= 8 and row[0].upper() == 'PARTIAL':
                try:
                    score = float(row[7])
                    if 0.60 < score <= 0.70:
                        medium_matches.append({
                            'thumb_num': row[1],
                            'thumb_title': row[2],
                            'thumb_year': row[3],
                            'work_id': row[4],
                            'work_title': row[5],
                            'work_year': row[6],
                            'score': score
                        })
                except (ValueError, IndexError):
                    continue

    # Sort by score (highest first)
    medium_matches.sort(key=lambda x: x['score'], reverse=True)

    print(f"Found {len(medium_matches)} MEDIUM score matches")
    print()

    # Categorize matches
    likely_correct = []
    year_mismatch = []
    uncertain = []

    for match in medium_matches:
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

        # Check if titles are very similar (normalized)
        thumb_title = match['thumb_title'].lower().replace('(', '').replace(')', '')
        work_title = match['work_title'].lower().replace('(', '').replace(')', '')

        if years_match and (thumb_title in work_title or work_title in thumb_title):
            likely_correct.append(match)
        elif not years_match:
            year_mismatch.append(match)
        else:
            uncertain.append(match)

    # Print categorization
    print("="*80)
    print("LIKELY CORRECT MATCHES (same title + same year):")
    print("="*80)
    for match in likely_correct:
        print(f"#{match['thumb_num']}: {match['thumb_title']} ({match['thumb_year']})")
        print(f"  -> {match['work_id']}: {match['work_title']} ({match['work_year']})")
        print(f"  Score: {match['score']}")
        print()

    print("="*80)
    print("YEAR MISMATCH (need manual review):")
    print("="*80)
    for match in year_mismatch:
        thumb_data = thumb_data_map.get(match['thumb_num'])
        work = works_map.get(match['work_id'])
        thumb_year = thumb_data.get('year', 'N/A') if thumb_data else 'N/A'
        work_year = work.get('year', 'N/A') if work else 'N/A'

        print(f"#{match['thumb_num']}: {match['thumb_title']} ({thumb_year})")
        print(f"  -> {match['work_id']}: {match['work_title']} ({work_year})")
        print(f"  Score: {match['score']}")
        print()

    print("="*80)
    print("UNCERTAIN (need manual review):")
    print("="*80)
    for match in uncertain:
        print(f"#{match['thumb_num']}: {match['thumb_title']} ({match['thumb_year']})")
        print(f"  -> {match['work_id']}: {match['work_title']} ({match['work_year']})")
        print(f"  Score: {match['score']}")
        print()

    # Summary
    print("="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total MEDIUM matches: {len(medium_matches)}")
    print(f"Likely correct (can auto-process): {len(likely_correct)}")
    print(f"Year mismatch (manual review): {len(year_mismatch)}")
    print(f"Uncertain (manual review): {len(uncertain)}")
    print()

    # Save likely correct to JSON for auto-processing
    if likely_correct:
        output = {
            'likely_correct': [m['thumb_num'] for m in likely_correct],
            'matches': likely_correct
        }
        output_path = PROJECT_DIR / "medium_matches_likely_correct.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"Saved likely correct matches to: medium_matches_likely_correct.json")

if __name__ == '__main__':
    main()
