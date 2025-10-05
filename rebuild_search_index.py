#!/usr/bin/env python3
"""
Rebuild search index from all content sources with bilingual support.
"""

import json
import os
from pathlib import Path

def load_works():
    """Load all works from works.json"""
    with open('works.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['works']

def load_translations(lang='en'):
    """Load translations for works"""
    try:
        with open(f'translations/{lang}.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Handle both nested "works" structure and flat structure
            return data.get('works', data)
    except FileNotFoundError:
        return {}

def create_work_search_entry(work, translations_en=None, translations_is=None):
    """Create a search entry for a work with bilingual content"""
    work_id = work.get('id', '')

    # Get translations if available
    trans_en = translations_en.get(work_id, {}) if translations_en else {}
    trans_is = translations_is.get(work_id, {}) if translations_is else {}

    # Build searchable content (include both languages)
    # Handle materials - can be list or string
    work_materials = work.get('materials', [])
    if isinstance(work_materials, list):
        work_materials_str = ' '.join(work_materials)
    else:
        work_materials_str = str(work_materials)

    trans_en_materials = trans_en.get('materials', '')
    if isinstance(trans_en_materials, list):
        trans_en_materials = ' '.join(trans_en_materials)

    trans_is_materials = trans_is.get('materials', '')
    if isinstance(trans_is_materials, list):
        trans_is_materials = ' '.join(trans_is_materials)

    content_parts = [
        work.get('title', ''),
        trans_en.get('title', ''),
        trans_is.get('title', ''),
        work.get('description', ''),
        trans_en.get('description', ''),
        trans_is.get('description', ''),
        str(work.get('year', '')),
        ' '.join(work.get('tags', [])),
        work_materials_str,
        trans_en_materials,
        trans_is_materials,
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

    # Create snippet from description or tags (prefer English)
    snippet = trans_en.get('description', work.get('description', ''))
    if len(snippet) > 150:
        snippet = snippet[:147] + '...'
    elif not snippet and work.get('tags'):
        snippet = ', '.join(work.get('tags', [])[:5])

    # Use translated title if available, otherwise original
    title = trans_en.get('title', work.get('title', 'Untitled'))

    return {
        "type": "work",
        "title": title,
        "snippet": snippet,
        "content": content,
        "url": f"works.html?work={work.get('id', '')}",
        "year": work.get('year', ''),
        "page": "works"
    }

def rebuild_search_index():
    """Rebuild the complete search index with bilingual support"""

    print("Rebuilding search index with bilingual content...")

    searchable_content = []

    # Load translations
    print("Loading translations...")
    translations_en = load_translations('en')
    translations_is = load_translations('is')
    print(f"Loaded {len(translations_en)} English translations and {len(translations_is)} Icelandic translations")

    # Add all works
    works = load_works()
    print(f"Adding {len(works)} works to search index...")

    for work in works:
        try:
            entry = create_work_search_entry(work, translations_en, translations_is)
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
