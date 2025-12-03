#!/usr/bin/env python3
"""
Fetch real product images using multiple strategies
"""

import requests
import time
from pathlib import Path

IMAGES_DIR = Path("wishlist-images")

# Product URLs and manual image sources
PRODUCTS = {
    "07-sigma-fp.jpg": {
        "direct_urls": [
            "https://www.sigma-global.com/en/lenses/others/fp/",
            "https://images.squarespace-cdn.com/content/v1/5a1c92131f318d91c2e93a66/1565215556586-P2N8U6J2K9K9MZPO5HF5/sigma-fp-front.jpg",
            "https://www.dpreview.com/files/p/articles/9451020783/Images/sigma-fp-front.jpeg"
        ]
    },
    "08-opal-tadpole.jpg": {
        "direct_urls": [
            "https://assets-global.website-files.com/60b8cd7e07f2e47e87b8d77e/64b0e4b5a5c5e5f8d5e5e5e5_tadpole-hero.png",
            "https://opalcamera.com/static/tadpole-hero.png"
        ]
    },
    "11-thinkpad-x1.jpg": {
        "direct_urls": [
            "https://p1-ofp.static.pub/medias/24200082US_LenovoPRO_SP_01.png",
            "https://p3-ofp.static.pub/fes/cms/2024/05/15/r9xp2dvi5ib78u3n07jnjk7rlhgqdk713092.png"
        ]
    },
    "15-porsche-911.jpg": {
        "direct_urls": [
            "https://files.porsche.com/filestore/image/multimedia/none/992-2nd-t-s-modelimage-sideshot/model/995afadc-42d7-11ed-80f6-005056bbdc38/porsche-model.png",
            "https://www.porsche.com/germany/_germany_/media/Images/models/911/turbo-models/Turbo/porsche_model/porsche-turbo-models-turbo-s-992-product-image.jpg"
        ]
    },
    "17-dyson-v15.jpg": {
        "direct_urls": [
            "https://dyson-h.assetsadobe2.com/is/image/content/dam/dyson/images/products/primary/369227-01.png",
            "https://www.dyson.com/medialibrary/Products/Vacuum-Cleaners/Cordless/V15-Detect-Absolute/ProductCarousel/V15-Detect-Absolute-Product-Carousel-01.png"
        ]
    },
    "20-ferrari-book.jpg": {
        "direct_urls": [
            "https://www.taschen.com/media/images/960/art_ferrari_ju_3d_05382_2104061057_id_1382857.png",
            "https://cdn.shopify.com/s/files/1/0438/4405/products/ferrari-art-edition-book.jpg"
        ]
    },
    "23-common-projects.jpg": {
        "direct_urls": [
            "https://cdn.shopify.com/s/files/1/0094/2252/products/Common-Projects-Achilles-Low-White-1.jpg",
            "https://commonprojects.com/media/catalog/product/1/5/1528-0506-product.jpg"
        ]
    },
    "24-ic-lights.jpg": {
        "direct_urls": [
            "https://www.flos.com/on/demandware.static/-/Sites-flos-master-catalog/default/dw9d5f5b5e/products/F3154057_product.jpg",
            "https://assets.flos.com/media/catalog/product/f/3/f3154057_product_1.jpg"
        ]
    },
    "27-sennheiser.jpg": {
        "direct_urls": [
            "https://www.sennheiser-hearing.com/globalassets/digizuite/113736-hdb-630.jpg",
            "https://assets.sennheiser.com/img/7564/hd-660s2-01.png"
        ]
    },
    "29-yeelight.jpg": {
        "direct_urls": [
            "https://www.yeelight.com/en_US/images/product/air96-v2.png",
            "https://cdn.shopify.com/s/files/1/0572/3224/products/yeelight-air96.jpg"
        ]
    },
    "30-tool-kit.jpg": {
        "direct_urls": [
            "https://images-na.ssl-images-amazon.com/images/I/71zJ5JvKDaL.jpg",
            "https://m.media-amazon.com/images/I/81Qz5mF5AFL._AC_SL1500_.jpg"
        ]
    },
    "33-klipsch-fives.jpg": {
        "direct_urls": [
            "https://images.klipsch.com/The-Fives-Black_635162950775460000_Hero-Standard.png",
            "https://cdn.shopify.com/s/files/1/0256/3761/products/klipsch-the-fives.jpg"
        ]
    }
}

def download_image(url, filepath):
    """Try to download an image with various headers"""
    headers_list = [
        {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'},
        {'User-Agent': 'curl/7.68.0'},
    ]

    for headers in headers_list:
        try:
            response = requests.get(url, headers=headers, timeout=10, allow_redirects=True, stream=True)
            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                return True
        except:
            continue

    return False

def main():
    print("🔍 Attempting to download real product images...\n")

    success_count = 0

    for filename, data in PRODUCTS.items():
        product_name = filename.replace('.jpg', '').replace('-', ' ').title()
        print(f"Trying: {product_name}")

        filepath = IMAGES_DIR / filename

        for url in data['direct_urls']:
            print(f"  → {url[:60]}...")
            if download_image(url, filepath):
                file_size = filepath.stat().st_size
                if file_size > 5000:  # At least 5KB
                    print(f"  ✓ Success! ({file_size // 1024}KB)")
                    success_count += 1
                    break
                else:
                    filepath.unlink()
                    print(f"  ✗ File too small, trying next...")
            else:
                print(f"  ✗ Failed, trying next...")

        if not filepath.exists():
            print(f"  ⚠️  Could not download, keeping SVG placeholder")

        print()
        time.sleep(0.5)

    print(f"\n✅ Successfully downloaded {success_count}/{len(PRODUCTS)} real images")

if __name__ == '__main__':
    main()
