#!/usr/bin/env python3
"""
Update wishlist HTML with downloaded images
"""

import json
from bs4 import BeautifulSoup

def update_wishlist_html():
    # Load mapping
    with open('image-mapping.json', 'r') as f:
        mapping = json.load(f)

    # Load HTML
    with open('wishlist.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

    # Create a lookup dict by product name
    image_map = {item['name']: item['new_img'] for item in mapping}

    updated_count = 0
    for card in soup.find_all('div', class_='product-card'):
        name_elem = card.find('h3', class_='product-name')
        img_elem = card.find('img')

        if name_elem and img_elem:
            product_name = name_elem.text.strip()

            if product_name in image_map:
                old_src = img_elem['src']
                new_src = image_map[product_name]
                img_elem['src'] = new_src
                updated_count += 1
                print(f"✓ Updated: {product_name}")

    # Save updated HTML
    with open('wishlist.html', 'w', encoding='utf-8') as f:
        f.write(str(soup.prettify()))

    print(f"\n✅ Updated {updated_count} images in wishlist.html")

if __name__ == '__main__':
    update_wishlist_html()
