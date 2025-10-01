#!/usr/bin/env python3
"""
Add Kúlan 1962 work to works.json as a test of the workflow.
"""

import json

def add_kulan_work():
    """Add Kúlan 1962 work entry."""

    # Read current works.json
    with open('works.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Create new work entry
    kulan_work = {
        "id": "kulan_1962",
        "title": "Kúlan",
        "year": 1962,
        "description": "An early sculptural work from 1962 demonstrating Magnús Pálsson's exploration of geometric forms and spatial relationships. This piece represents his early artistic development and interest in abstraction during his formative years as an artist. The work shows his experimentation with materials and form that would later develop into his more conceptual practice.",
        "images": [
            {
                "url": "images/kulan-1962/medium/kulan-01-medium.jpg",
                "caption": "Kúlan - main view"
            },
            {
                "url": "images/kulan-1962/medium/kulan-02-medium.jpg",
                "caption": "Kúlan - detail view"
            },
            {
                "url": "images/kulan-1962/medium/kulan-03-medium.jpg",
                "caption": "Kúlan - installation context"
            },
            {
                "url": "images/kulan-1962/medium/kulan-04-medium.jpg",
                "caption": "Kúlan - with people for scale"
            }
        ],
        "tags": [
            "sculpture",
            "geometric",
            "early work",
            "1960s",
            "abstract"
        ],
        "exhibitions": [],
        "materials": [
            "wood",
            "paint"
        ],
        "searchText": "kúlan geometric sculpture early work 1962 abstract form spatial magnús pálsson"
    }

    # Add to the beginning of the works array (chronologically early work)
    data['works'].insert(0, kulan_work)

    # Write updated JSON
    with open('works.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("OK: Added Kúlan 1962 to works.json")
    print(f"Total works now: {len(data['works'])}")
    print("Work added at beginning (chronologically early)")

if __name__ == "__main__":
    add_kulan_work()