#!/usr/bin/env python3
"""
Scrape specific product images using BeautifulSoup and real product pages
"""

import requests
from bs4 import BeautifulSoup
from pathlib import Path
import time

IMAGES_DIR = Path("wishlist-images")

# Product pages to scrape
PRODUCTS = {
    "07-sigma-fp.jpg": "https://www.bhphotovideo.com/c/product/1500998-REG/sigma_fp_mirrorless_digital_camera.html",
    "08-opal-tadpole.jpg": "https://opalcamera.com/tadpole-webcam",
    "11-thinkpad-x1.jpg": "https://www.lenovo.com/us/en/p/laptops/thinkpad/thinkpadx1/thinkpad-x1-carbon-gen-12-(14-inch-intel)/len101t0097",
    "15-porsche-911.jpg": "https://www.porsche.com/usa/models/911/911-turbo-models/",
    "20-ferrari-book.jpg": "https://www.taschen.com/en/books/art/05382/art-ferrari",
    "23-common-projects.jpg": "https://www.ssense.com/en-us/men/product/common-projects/white-achilles-low-sneakers/1536523",
    "24-ic-lights.jpg": "https://www.flos.com/en-us/products/ic-lights-t1-low",
    "27-sennheiser.jpg": "https://www.sennheiser.com/en-us/catalog/products/headphones/hd-660s2-black-headphones-with-detachable-cable-for-stereo-systems-09001",
    "29-yeelight.jpg": "https://www.yeelight.com/en_US/product/air96",
    "30-tool-kit.jpg": "https://www.workpro.com/products/322-piece-mechanics-tool-set",
    "33-klipsch-fives.jpg": "https://www.klipsch.com/products/the-fives-powered-speakers",
}

def scrape_image(url, filename):
    """Scrape the main product image from a page"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }

    try:
        print(f"  Fetching {url[:50]}...")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Try different image selectors
        image_url = None

        # Try og:image meta tag
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image.get('content'):
            image_url = og_image['content']

        # Try data-src attributes
        if not image_url:
            img_tag = soup.find('img', {'data-src': True})
            if img_tag:
                image_url = img_tag['data-src']

        # Try largest image by looking for high-res patterns
        if not image_url:
            imgs = soup.find_all('img', src=True)
            for img in imgs:
                src = img['src']
                if any(pattern in src.lower() for pattern in ['product', 'hero', 'main', 'large', '1500', '1200', '1000']):
                    image_url = src
                    break

        if not image_url:
            print(f"  ✗ No image found")
            return False

        # Make sure URL is absolute
        if image_url.startswith('//'):
            image_url = 'https:' + image_url
        elif image_url.startswith('/'):
            from urllib.parse import urlparse
            parsed = urlparse(url)
            image_url = f"{parsed.scheme}://{parsed.netloc}{image_url}"

        print(f"  Found: {image_url[:60]}...")

        # Download the image
        img_response = requests.get(image_url, headers=headers, timeout=15, stream=True)
        img_response.raise_for_status()

        filepath = IMAGES_DIR / filename
        with open(filepath, 'wb') as f:
            for chunk in img_response.iter_content(chunk_size=8192):
                f.write(chunk)

        # Check file size
        file_size = filepath.stat().st_size
        if file_size < 5000:
            filepath.unlink()
            print(f"  ✗ File too small ({file_size} bytes)")
            return False

        print(f"  ✓ Downloaded ({file_size // 1024}KB)")
        return True

    except Exception as e:
        print(f"  ✗ Error: {str(e)[:50]}")
        return False

def main():
    print("🔍 Scraping product images from official pages...\n")

    success_count = 0
    for filename, url in PRODUCTS.items():
        product_name = filename.replace('.jpg', '').replace('-', ' ').title()
        print(f"{product_name}:")

        if scrape_image(url, filename):
            success_count += 1

        print()
        time.sleep(1)  # Be polite

    print(f"✅ Successfully downloaded {success_count}/{len(PRODUCTS)} images")

if __name__ == '__main__':
    main()
