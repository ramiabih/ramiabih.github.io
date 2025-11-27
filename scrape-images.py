#!/usr/bin/env python3
"""
Wishlist Image Scraper
Scrapes product images from the wishlist HTML and downloads them locally.
"""

import os
import re
import json
import time
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from pathlib import Path

# Create images directory
IMAGES_DIR = Path("wishlist-images")
IMAGES_DIR.mkdir(exist_ok=True)

def extract_products_from_html(html_file):
    """Extract product information from wishlist HTML"""
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    products = []
    for card in soup.find_all('div', class_='product-card'):
        link = card.find('a')
        img = card.find('img')
        name = card.find('h3', class_='product-name')

        if link and img and name:
            product = {
                'name': name.text.strip(),
                'url': link['href'],
                'current_img': img['src'],
                'alt': img.get('alt', '')
            }
            products.append(product)

    return products

def get_best_image_from_url(product_url, timeout=10):
    """Fetch the product page and find the best image"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(product_url, headers=headers, timeout=timeout, allow_redirects=True)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Try various common product image selectors
        image_selectors = [
            'meta[property="og:image"]',
            'meta[name="twitter:image"]',
            'img[class*="product"]',
            'img[class*="hero"]',
            'img[class*="main"]',
            'img[itemprop="image"]',
            'picture source',
            'img[data-src]',
        ]

        for selector in image_selectors:
            element = soup.select_one(selector)
            if element:
                if element.name == 'meta':
                    img_url = element.get('content', '')
                elif element.name == 'source':
                    img_url = element.get('srcset', '').split(',')[0].split()[0]
                else:
                    img_url = element.get('data-src') or element.get('src', '')

                if img_url:
                    # Make absolute URL
                    if img_url.startswith('//'):
                        img_url = 'https:' + img_url
                    elif not img_url.startswith('http'):
                        img_url = urljoin(product_url, img_url)

                    # Filter out tiny images and icons
                    if 'logo' not in img_url.lower() and 'icon' not in img_url.lower():
                        return img_url

        return None

    except Exception as e:
        print(f"  ❌ Error fetching {product_url}: {e}")
        return None

def download_image(img_url, product_name, index):
    """Download image and save locally"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }

    try:
        # Clean filename
        safe_name = re.sub(r'[^a-zA-Z0-9\-]', '-', product_name.lower())
        safe_name = re.sub(r'-+', '-', safe_name).strip('-')

        response = requests.get(img_url, headers=headers, timeout=15, stream=True)
        response.raise_for_status()

        # Determine file extension
        content_type = response.headers.get('content-type', '')
        if 'png' in content_type:
            ext = 'png'
        elif 'webp' in content_type:
            ext = 'webp'
        elif 'svg' in content_type:
            ext = 'svg'
        else:
            ext = 'jpg'

        filename = f"{index:02d}-{safe_name}.{ext}"
        filepath = IMAGES_DIR / filename

        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"  ✓ Saved: {filename}")
        return f"wishlist-images/{filename}"

    except Exception as e:
        print(f"  ❌ Failed to download: {e}")
        return None

def main():
    print("🔍 Scraping wishlist images...\n")

    # Extract products from HTML
    products = extract_products_from_html('wishlist.html')
    print(f"Found {len(products)} products\n")

    results = []

    for i, product in enumerate(products, 1):
        print(f"[{i}/{len(products)}] {product['name']}")

        # Try to get better image from product page
        new_img_url = get_best_image_from_url(product['url'])

        if new_img_url:
            print(f"  Found image: {new_img_url[:80]}...")
            local_path = download_image(new_img_url, product['name'], i)

            if local_path:
                results.append({
                    'name': product['name'],
                    'old_img': product['current_img'],
                    'new_img': local_path,
                    'source_url': new_img_url
                })
        else:
            print(f"  ⚠️  Could not find image, trying current URL...")
            local_path = download_image(product['current_img'], product['name'], i)
            if local_path:
                results.append({
                    'name': product['name'],
                    'old_img': product['current_img'],
                    'new_img': local_path,
                    'source_url': product['current_img']
                })

        time.sleep(1)  # Be respectful to servers
        print()

    # Save mapping
    with open('image-mapping.json', 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n✅ Done! Downloaded {len(results)} images")
    print(f"📁 Images saved in: {IMAGES_DIR}/")
    print(f"📝 Mapping saved in: image-mapping.json")

if __name__ == '__main__':
    main()
