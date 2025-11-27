#!/usr/bin/env python3
"""
Update wishlist images - replaces image URLs with local paths
"""

import json
import re

# Load mapping
with open('image-mapping.json', 'r') as f:
    mapping = json.load(f)

# Read HTML
with open('wishlist.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update each image
updated_count = 0
for item in mapping:
    old_url = item['old_img']
    new_path = item['new_img']

    # Use regex to replace the src attribute
    pattern = rf'src="{re.escape(old_url)}"'
    replacement = f'src="{new_path}"'

    if pattern in html:
        html = html.replace(f'src="{old_url}"', f'src="{new_path}"')
        updated_count += 1
        print(f"✓ Updated: {item['name']}")

# Write back
with open('wishlist.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n✅ Updated {updated_count} images")
