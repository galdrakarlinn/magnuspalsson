#!/usr/bin/env python3

import json
import os

# Load the works.json file
with open('works.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Define the mappings for files that need to be updated
updates = [
    {
        'old': 'images/hundljod-1990/hundljod-documentation.jpg',
        'new': 'images/hundljod-1990/medium/hundljod-documentation-medium.jpg'
    },
    {
        'old': 'images/draumur-hlynsins-um-fjall-1974/Hanging mountain.png',
        'new': 'images/draumur-hlynsins-um-fjall-1974/medium/Hanging mountain-medium.jpg'
    },
    {
        'old': 'images/galleri-gangur-1982/Cockerel.jpg',
        'new': 'images/galleri-gangur-1982/medium/Cockerel-medium.jpg'
    },
    {
        'old': 'images/gapassipi-1995/Gapassipi 1.JPG',
        'new': 'images/gapassipi-1995/medium/Gapassipi 1-medium.JPG'
    },
    {
        'old': 'images/g-ljod-2009/G-ljóð1 front page 2009.jpg',
        'new': 'images/g-ljod-2009/medium/G-ljóð1 front page 2009-medium.jpg'
    },
    {
        'old': 'images/gibsborn-children-1971/Children Lund.jpg',
        'new': 'images/gibsborn-children-1971/medium/Children Lund-medium.jpg'
    },
    {
        'old': 'images/hattar-1969-71/IMG_0199.jpg',
        'new': 'images/hattar-1969-71/medium/IMG_0199-medium.jpg'
    },
    {
        'old': 'images/hrognkelsaveifa-strandlegjan-1998/Beach sculpture 1.jpg',
        'new': 'images/hrognkelsaveifa-strandlegjan-1998/medium/Beach sculpture 1-medium.jpg'
    },
    {
        'old': 'images/jonsmessunott-bank-piece-1982/Whole piece.JPG',
        'new': 'images/jonsmessunott-bank-piece-1982/medium/Whole piece-medium.JPG'
    },
    {
        'old': 'images/jorgen-bruun-hansen-2013/Jörgen BH pencil sketch MP.jpg',
        'new': 'images/jorgen-bruun-hansen-2013/medium/Jörgen BH pencil sketch MP-medium.jpg'
    }
]

# Create backup
with open('works.json.backup-before-medium-fix', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# Apply updates
updated_count = 0
for work in data['works']:
    for image in work.get('images', []):
        for update in updates:
            if image['url'] == update['old']:
                print(f"Updating: {update['old']} -> {update['new']}")
                image['url'] = update['new']
                updated_count += 1

print(f"\nTotal updates made: {updated_count}")

# Save the updated works.json
with open('works.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("JSON references updated successfully!")