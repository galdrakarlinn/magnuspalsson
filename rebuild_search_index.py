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

def load_exhibitions():
    """Load exhibitions from exhibitions.json"""
    try:
        with open('exhibitions.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return {'solo': [], 'group': []}

def lookup_exhibition(exhibition_id, exhibitions_data):
    """Look up exhibition by ID"""
    all_exhibitions = exhibitions_data.get('solo', []) + exhibitions_data.get('group', [])
    for ex in all_exhibitions:
        if ex.get('id') == exhibition_id:
            return ex
    return None

def get_localized_value(field, lang='en'):
    """Extract value from bilingual field or return string if legacy format"""
    if not field:
        return ''
    if isinstance(field, dict) and (lang in field):
        return field[lang]
    if isinstance(field, dict):
        # Fallback to any available language
        return field.get('en', field.get('is', ''))
    return str(field)  # Legacy string format

def get_materials_string(materials, lang='en'):
    """Convert materials to searchable string, handling various formats"""
    if not materials:
        return ''

    # If it's a bilingual object with language keys
    if isinstance(materials, dict) and (lang in materials or 'en' in materials or 'is' in materials):
        mat = materials.get(lang, materials.get('en', materials.get('is', [])))
        if isinstance(mat, list):
            return ' '.join(mat)
        return str(mat)

    # If it's a simple list
    if isinstance(materials, list):
        return ' '.join(materials)

    # If it's a string
    return str(materials)

def create_work_search_entry(work, exhibitions_data):
    """Create a search entry for a work with bilingual content"""
    work_id = work.get('id', '')

    # Extract bilingual fields
    title_en = get_localized_value(work.get('title'), 'en')
    title_is = get_localized_value(work.get('title'), 'is')
    desc_en = get_localized_value(work.get('description'), 'en')
    desc_is = get_localized_value(work.get('description'), 'is')

    # Handle materials in both languages
    materials_en = get_materials_string(work.get('materials'), 'en')
    materials_is = get_materials_string(work.get('materials'), 'is')

    # Build searchable content (include both languages)
    content_parts = [
        title_en,
        title_is,
        desc_en,
        desc_is,
        str(work.get('year', '')),
        ' '.join(work.get('tags', [])),
        materials_en,
        materials_is,
    ]

    # Add exhibition info (handle ID references and bilingual objects)
    for ex in work.get('exhibitions', []):
        if isinstance(ex, str):
            # Exhibition ID reference - look up from exhibitions.json
            exhibition = lookup_exhibition(ex, exhibitions_data)
            if exhibition:
                ex_title_en = get_localized_value(exhibition.get('title'), 'en')
                ex_title_is = get_localized_value(exhibition.get('title'), 'is')
                ex_venue_en = get_localized_value(exhibition.get('venue'), 'en')
                ex_venue_is = get_localized_value(exhibition.get('venue'), 'is')
                location = exhibition.get('location', '')
                content_parts.extend([ex_title_en, ex_title_is, ex_venue_en, ex_venue_is, location])
            else:
                # Legacy string exhibition (just add as-is)
                content_parts.append(ex)
        elif isinstance(ex, dict):
            # Unmatched exhibition with full bilingual data
            ex_title_en = get_localized_value(ex.get('title'), 'en')
            ex_title_is = get_localized_value(ex.get('title'), 'is')
            ex_venue_en = get_localized_value(ex.get('venue'), 'en')
            ex_venue_is = get_localized_value(ex.get('venue'), 'is')
            location = ex.get('location', ex.get('city', ''))
            content_parts.extend([ex_title_en, ex_title_is, ex_venue_en, ex_venue_is, location])

    # Add image captions
    for img in work.get('images', []):
        caption_en = get_localized_value(img.get('caption'), 'en')
        caption_is = get_localized_value(img.get('caption'), 'is')
        if caption_en:
            content_parts.append(caption_en)
        if caption_is:
            content_parts.append(caption_is)

    content = ' '.join(filter(None, content_parts))

    # Create snippet from description (prefer English)
    snippet = desc_en if desc_en else desc_is
    if len(snippet) > 150:
        snippet = snippet[:147] + '...'
    elif not snippet and work.get('tags'):
        snippet = ', '.join(work.get('tags', [])[:5])

    # Store both titles for bilingual display
    return {
        "type": "work",
        "title": {
            "en": title_en if title_en else title_is if title_is else 'Untitled',
            "is": title_is if title_is else title_en if title_en else 'Untitled'
        },
        "snippet": snippet,
        "content": content,
        "url": f"works.html?work={work.get('id', '')}",
        "year": work.get('year', ''),
        "page": "works"
    }

def rebuild_search_index():
    """Rebuild the complete search index with bilingual support"""

    print("Rebuilding search index from bilingual works.json and exhibitions.json...")

    searchable_content = []

    # Load exhibitions data
    print("Loading exhibitions...")
    exhibitions_data = load_exhibitions()
    print(f"Loaded {len(exhibitions_data.get('solo', []))} solo + {len(exhibitions_data.get('group', []))} group exhibitions")

    # Add all works
    works = load_works()
    print(f"Processing {len(works)} works...")

    for work in works:
        try:
            entry = create_work_search_entry(work, exhibitions_data)
            searchable_content.append(entry)
        except Exception as e:
            print(f"Error processing work {work.get('id', 'unknown')}: {e}")
            import traceback
            traceback.print_exc()

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
