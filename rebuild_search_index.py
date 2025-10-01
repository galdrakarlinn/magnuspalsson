#!/usr/bin/env python3
"""
Rebuild search index from all content sources.
"""

import json
import os
from pathlib import Path

def load_works():
    """Load all works from works.json"""
    with open('works.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['works']

def create_work_search_entry(work):
    """Create a search entry for a work"""
    # Build searchable content
    content_parts = [
        work.get('title', ''),
        work.get('description', ''),
        str(work.get('year', '')),
        ' '.join(work.get('tags', [])),
        ' '.join(work.get('materials', []))
    ]

    # Add exhibition info
    for ex in work.get('exhibitions', []):
        if isinstance(ex, dict):
            content_parts.append(ex.get('title', ''))
            content_parts.append(ex.get('venue', ''))
            content_parts.append(ex.get('city', ''))
        elif isinstance(ex, str):
            content_parts.append(ex)

    content = ' '.join(filter(None, content_parts))

    # Create snippet from description or tags
    snippet = work.get('description', '')
    if len(snippet) > 150:
        snippet = snippet[:147] + '...'
    elif not snippet and work.get('tags'):
        snippet = ', '.join(work.get('tags', [])[:5])

    return {
        "type": "work",
        "title": work.get('title', 'Untitled'),
        "snippet": snippet,
        "content": content,
        "url": f"works.html?work={work.get('id', '')}",
        "year": work.get('year', ''),
        "page": "works"
    }

def rebuild_search_index():
    """Rebuild the complete search index"""

    print("Rebuilding search index...")

    searchable_content = []

    # Add all works
    works = load_works()
    print(f"Adding {len(works)} works to search index...")

    for work in works:
        try:
            entry = create_work_search_entry(work)
            searchable_content.append(entry)
        except Exception as e:
            print(f"Error processing work {work.get('id', 'unknown')}: {e}")

    # Read existing search index to preserve non-work entries
    existing_entries = []
    if os.path.exists('search-index.json'):
        with open('search-index.json', 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
            existing_entries = [e for e in existing_data.get('searchableContent', []) if e.get('type') != 'work']

    print(f"Preserving {len(existing_entries)} non-work entries from existing index...")

    # Combine new works with existing non-work entries
    searchable_content.extend(existing_entries)

    # Create search index structure
    search_index = {
        "searchableContent": searchable_content
    }

    # Write to file
    with open('search-index.json', 'w', encoding='utf-8') as f:
        json.dump(search_index, f, indent=2, ensure_ascii=False)

    print(f"\nSearch index rebuilt successfully!")
    print(f"Total entries: {len(searchable_content)}")
    print(f"  - Works: {len([e for e in searchable_content if e['type'] == 'work'])}")
    print(f"  - Other: {len(existing_entries)}")

if __name__ == '__main__':
    rebuild_search_index()
