#!/usr/bin/env python3
"""
Restore important works that were removed during cleanup, but without broken image references.
"""

import json

def restore_missing_works():
    """Add back important works without broken image references."""

    # Read current works.json
    with open('works.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Works to restore (without broken image references)
    restored_works = [
        {
            "id": "bestu_stykkin",
            "title": "Bestu stykkin",
            "year": 1965,
            "description": "Three surviving sculptures from a larger anti-art series of cloth figures called Frúöld, created in 1965 and exhibited at Magnús Pálsson's debut solo exhibition at Ásmundarsalur in 1967. Made by stuffing old cloths with paper, stiffening with glue and paint until hard, then removing the paper so the cloth figures could stand like empty skins. Created in the artist's Hvarf garage studio during 1965-1967, a converted rural space that was documented in October 1967 before being destroyed by fire. The ironic titles (allegedly suggested by Dieter Roth) were inversely related to their visual appeal - the most miserable-looking was called 'The best piece,' with titles descending in flattery as the works became more visually interesting. The Frúöld were not well received; the public called them ugly and idiotic, questioning Pálsson's sanity. In response, he gathered the remaining pieces, piled them under the stairway to SÚM exhibition space on Vatnsstígur, poured concrete over them, and let them decompose. Only three survive in the Living Art Museum collection. The work exemplifies Pálsson's anti-art philosophy - childishly simple in concept, executed without traditional artistry, and deliberately unaesthetic, challenging Icelandic art's boundaries alongside contemporaneous provocations like the rye bread pile on Skólavörðuholt and SÚM's infamous hay bale. (Source: Kjarvalstaðir catalogue, 1994)",
            "images": [],
            "tags": [
                "sculpture",
                "anti-art",
                "cloth figures",
                "conceptual",
                "frúöld",
                "dieter roth",
                "controversial",
                "1960s",
                "debut exhibition"
            ],
            "exhibitions": [
                {
                    "title": "Bestu stykkin",
                    "venue": "Ásmundarsalur",
                    "year": 1967,
                    "city": "Reykjavík"
                }
            ],
            "materials": [
                "cloth",
                "paper",
                "glue",
                "paint"
            ],
            "searchText": "bestu stykkin best pieces cloth figures frúöld anti-art ásmundarsalur 1967 debut exhibition dieter roth controversial ugly idiotic magnús pálsson hvarf garage studio"
        },
        {
            "id": "augustus_my_god",
            "title": "Augustus My God I Have It",
            "year": 1984,
            "description": "A groundbreaking sound poetry work that crosses boundaries between audio art, book, and performance. Created as both a recorded piece and live performance, exploring themes of discovery, revelation, and the power of language.",
            "images": [],
            "tags": [
                "sound poetry",
                "audio art",
                "book",
                "performance",
                "language",
                "revelation",
                "1980s"
            ],
            "searchText": "augustus my god have it sound poetry audio art book performance language revelation nordic sound art festival reykjavik"
        },
        {
            "id": "thyrlulending",
            "title": "Þyrlulending (Helicopter Landing)",
            "year": 1976,
            "description": "Conceptual work measuring anticipation and mechanical intervention, titled 'Sekúndurnar þar til Sikorskýþyrlan snertir' (The Seconds Before the Sikorsky Helicopter Touches Down). This time-based sculpture captures the moment before the Coast Guard's helicopter lands, materializing the immaterial through three plaster forms arranged in a triangle on the floor. The forms are casts of the negative space between the helicopter's wheels and the ground, with different heights indicating temporal progression - the tail wheel, which lands last, is the highest. Time is here transformed into solid matter, exploring themes of anticipation, mechanical intervention, and the transformation of temporal experience into physical form. Exhibited at the Venice Biennale in 1980 where Pálsson represented Iceland. (Source: Reykjavík Art Museum collection description and Kjarvalstaðir catalog)",
            "images": [],
            "tags": [
                "sculpture",
                "conceptual",
                "time",
                "anticipation",
                "plaster",
                "helicopter",
                "venice biennale",
                "negative space",
                "1970s"
            ],
            "exhibitions": [
                {
                    "title": "Venice Biennale",
                    "venue": "Venice Biennale",
                    "year": 1980,
                    "city": "Venice"
                }
            ],
            "searchText": "þyrlulending helicopter landing sikorsky coast guard anticipation mechanical intervention plaster venice biennale 1980 iceland representation time sculpture"
        },
        {
            "id": "vidtol_um_daudann_2011",
            "title": "Viðtöl um dauðann",
            "year": 2011,
            "description": "A profound exploration of death and mortality through conversations and interviews. This work examines how we speak about death, confront mortality, and find meaning in the face of the inevitable. The project includes documentation, texts, and collaborative elements exploring the universal human experience of confronting death.",
            "images": [],
            "tags": [
                "death",
                "mortality",
                "conversations",
                "interviews",
                "existential",
                "collaboration",
                "2010s"
            ],
            "searchText": "viðtöl um dauðann conversations about death mortality existential meaning inevitable human experience"
        },
        {
            "id": "draumur_hlynsins_um_fjall_1974",
            "title": "Draumur hlynsins um fjall",
            "year": 1974,
            "description": "A poetic work exploring dreams, sound, and landscape. Created in collaboration with Edda Jónsdóttir in 1974, this work examines the relationship between sound, memory, and the mountain landscape through performance and documentation.",
            "images": [],
            "tags": [
                "poetry",
                "dreams",
                "sound",
                "landscape",
                "mountain",
                "collaboration",
                "edda jónsdóttir",
                "1970s"
            ],
            "searchText": "draumur hlynsins um fjall dreams sound landscape mountain collaboration edda jónsdóttir 1974 poetry magnús pálsson"
        }
    ]

    # Add restored works to the beginning of the works array
    data['works'] = restored_works + data['works']

    # Write updated JSON
    with open('works.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"OK: Restored {len(restored_works)} important works:")
    for work in restored_works:
        print(f"   - {work['title']} ({work['year']})")

    print(f"\nTotal works now: {len(data['works'])}")
    print("Note: These works are restored without images but with full descriptions and metadata.")

if __name__ == "__main__":
    restore_missing_works()