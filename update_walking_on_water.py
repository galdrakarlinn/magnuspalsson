#!/usr/bin/env python3
"""
Update Walking on Water entry in works.json
"""

import json

# The updated work data
updated_work = {
  "id": "walking-on-water-2012",
  "title": {
    "en": "Walking on Water",
    "is": "Gengið á vatni"
  },
  "year": 2012,
  "description": {
    "en": "Installation at Kling og Bang gallery in March 2012.",
    "is": "Innsetning í Gallerý Kling og Bang í mars 2012."
  },
  "images": [
    {
      "url": "images/walking-on-water-2012/medium/walking-on-water-2012-01-medium.jpg",
      "caption": {
        "en": "Walking on Water installation 1",
        "is": ""
      },
      "thumbnail": "images/walking-on-water-2012/thumbs/walking-on-water-2012-01-thumb.jpg"
    },
    {
      "url": "images/walking-on-water-2012/medium/walking-on-water-2012-02-medium.jpg",
      "caption": {
        "en": "Walking on Water installation 2",
        "is": ""
      },
      "thumbnail": "images/walking-on-water-2012/thumbs/walking-on-water-2012-02-thumb.jpg"
    },
    {
      "url": "images/walking-on-water-2012/medium/walking-on-water-2012-03-medium.jpg",
      "caption": {
        "en": "Walking on Water installation 3",
        "is": ""
      },
      "thumbnail": "images/walking-on-water-2012/thumbs/walking-on-water-2012-03-thumb.jpg"
    },
    {
      "url": "images/walking-on-water-2012/medium/walking-on-water-2012-04-medium.jpg",
      "caption": {
        "en": "Walking on Water installation 4",
        "is": ""
      },
      "thumbnail": "images/walking-on-water-2012/thumbs/walking-on-water-2012-04-thumb.jpg"
    },
    {
      "url": "images/walking-on-water-2012/medium/walking-on-water-2012-05-medium.jpg",
      "caption": {
        "en": "Walking on Water installation 5",
        "is": ""
      },
      "thumbnail": "images/walking-on-water-2012/thumbs/walking-on-water-2012-05-thumb.jpg"
    }
  ],
  "tags": [
    "sculpture",
    "installation"
  ],
  "exhibitions": [
    {
      "title": {
        "en": "Red Snow - Ice in Motion",
        "is": "Rauður snjór - Ís í hreyfingu"
      },
      "venue": {
        "en": "Nordic House (Nordes Hus)",
        "is": "Norðurlandahúsið (Nordes Hus)"
      },
      "location": "Tórshavn, Færeyjar",
      "year": 2016
    },
    {
      "title": {
        "en": "Red Snow - Ice in Motion",
        "is": "Rauður snjór - Ís í hreyfingu"
      },
      "venue": {
        "en": "The Nordic House",
        "is": "Nordatlantens Brygge"
      },
      "location": "Kaupmannahöfn, Danmörk",
      "year": 2015
    },
    {
      "title": {
        "en": "Red Snow - Ice in Motion",
        "is": "Rauður snjór - Ís í hreyfingu"
      },
      "venue": {
        "en": "Nordatlantens Brygge",
        "is": "Nordatlantens Brygge"
      },
      "location": "Kaupmannahöfn, Danmörk",
      "year": 2015
    },
    {
      "title": {
        "en": "Red Snow - Ice in Motion",
        "is": "Rauður snjór - Ís í hreyfingu"
      },
      "venue": {
        "en": "Katuaq",
        "is": "Katuaq (Menningarhús Grænlands)"
      },
      "location": "Nuuk, Grænland",
      "year": 2014
    },
    {
      "title": {
        "en": "Walking on water",
        "is": "Walking on water"
      },
      "venue": {
        "en": "Gallerí Kling og Bang",
        "is": "Gallerí Kling og Bang"
      },
      "location": "Reykjavík, Iceland",
      "year": 2012
    },
    {
      "title": {
        "en": "SOMETHING from NOTHING – The Visual Realm of Magnús Pálsson",
        "is": "Retrospective – Myndheimur: Eitthvað úr engu (The Visual Realm of Magnús Pálsson. Something from Nothing)"
      },
      "venue": {
        "en": "Reykjavík Art Museum – Hafnarhús",
        "is": "Reykjavík Art Museum – Hafnarhús"
      },
      "location": "Reykjavík, Iceland",
      "year": 2019
    }
  ],
  "searchText": "walking on water gengið á vatnið 2012 kling og bang installation magnús pálsson",
  "materials": {
    "en": [
      "mixed media",
      "sculpture"
    ],
    "is": [
      "blandað efni",
      "höggmynd"
    ]
  },
  "status": "incomplete",
  "ownership": {
    "owner": "Magnús Pálsson"
  }
}

# Load works.json
with open('works.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Find and replace Walking on Water
for i, work in enumerate(data['works']):
    if work['id'] == 'walking-on-water-2012':
        data['works'][i] = updated_work
        print(f'Updated Walking on Water at index {i}')
        break

# Save back to works.json
with open('works.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print('Works.json updated successfully!')
