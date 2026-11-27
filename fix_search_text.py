#!/usr/bin/env python3
"""
Fix searchText for works with book thumbnails
- Properly build searchText from work data
- Append 'book thumbnail added' tag
"""

import json
from pathlib import Path

# Paths
PROJECT_DIR = Path(__file__).parent
WORKS_JSON = PROJECT_DIR / "works.json"

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def build_search_text(work):
    """Build comprehensive searchText from work data"""
    search_parts = []

    # Title
    if 'title' in work:
        if 'en' in work['title']:
            search_parts.append(work['title']['en'])
        if 'is' in work['title']:
            search_parts.append(work['title']['is'])

    # Year
    if 'year' in work and work['year']:
        search_parts.append(str(work['year']))

    # Materials
    if 'materials' in work:
        if isinstance(work['materials'], dict):
            if 'en' in work['materials']:
                search_parts.extend(work['materials']['en'])
            if 'is' in work['materials']:
                search_parts.extend(work['materials']['is'])

    # Medium
    if 'medium' in work:
        if isinstance(work['medium'], dict):
            if 'en' in work['medium']:
                search_parts.extend(work['medium']['en'])
            if 'is' in work['medium']:
                search_parts.extend(work['medium']['is'])

    # Category
    if 'category' in work and isinstance(work['category'], list):
        search_parts.extend(work['category'])

    # Tags
    if 'tags' in work and isinstance(work['tags'], list):
        # Filter out the book-thumbnail-added tag - we'll add it separately
        other_tags = [t for t in work['tags'] if t != 'book-thumbnail-added']
        search_parts.extend(other_tags)

    # Description snippets
    if 'description' in work:
        if isinstance(work['description'], dict):
            if 'en' in work['description'] and work['description']['en']:
                # Add first 50 words of English description
                desc_words = work['description']['en'].split()[:50]
                search_parts.append(' '.join(desc_words))

    return ' '.join(search_parts)

def has_book_thumbnail(work):
    """Check if work has any book thumbnail images"""
    if 'images' not in work:
        return False

    for img in work['images']:
        url = img.get('url', '')
        if 'book-thumbnail' in url:
            return True
    return False

def main():
    print("Fix searchText for works with book thumbnails")
    print("="*60)

    # Load data
    works_data = load_json(WORKS_JSON)

    updated_count = 0

    for work in works_data['works']:
        if has_book_thumbnail(work):
            # Build proper searchText
            search_text = build_search_text(work)

            # Add book thumbnail tag
            if 'book thumbnail' not in search_text.lower():
                search_text = f"{search_text} book thumbnail added"

            # Update work
            work['searchText'] = search_text.strip()

            print(f"Updated: {work['id']}")
            updated_count += 1

    # Save
    if updated_count > 0:
        print(f"\n{'='*60}")
        print(f"Saving works.json with {updated_count} updated works...")
        save_json(WORKS_JSON, works_data)
        print("SUCCESS!")
    else:
        print("\nNo works to update")

    print(f"\nTotal works updated: {updated_count}")

if __name__ == '__main__':
    main()
