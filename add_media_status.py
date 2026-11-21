import json

# Read the works file
with open('works.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Add mediaStatus field to all works
for work in data['works']:
    work['mediaStatus'] = 'images draft'

# Write back to file with proper formatting
with open('works.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Added 'mediaStatus' field to {len(data['works'])} works")
print(f"All works set to: 'images draft'")
