import json

with open('works.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("CONTENT STATUS SUMMARY")
print("="*60)
print(f"Content 'needs review': {sum(1 for w in data['works'] if w.get('contentStatus') == 'needs review')}")
print(f"Content 'draft': {sum(1 for w in data['works'] if w.get('contentStatus') == 'draft')}")
print()
print("MEDIA STATUS SUMMARY")
print("="*60)
print(f"Media 'images done': {sum(1 for w in data['works'] if w.get('mediaStatus') == 'images done')}")
print(f"Media 'images review': {sum(1 for w in data['works'] if w.get('mediaStatus') == 'images review')}")
print(f"Media 'images draft': {sum(1 for w in data['works'] if w.get('mediaStatus') == 'images draft')}")
print()
print("="*60)
print(f"Total works: {len(data['works'])}")
print()

# Show works by status combination
print("\nWORKS NEEDING ATTENTION")
print("="*60)

print("\nContent needs review (ready for content approval):")
for work in data['works']:
    if work.get('contentStatus') == 'needs review':
        title_en = work['title'].get('en', '')
        year = work.get('year', 'N/A')
        media_status = work.get('mediaStatus', 'unknown')
        print(f"  - {title_en} ({year}) | media: {media_status}")

print("\nImages ready for review:")
for work in data['works']:
    if work.get('mediaStatus') == 'images review':
        title_en = work['title'].get('en', '')
        year = work.get('year', 'N/A')
        content_status = work.get('contentStatus', 'unknown')
        print(f"  - {title_en} ({year}) | content: {content_status}")
