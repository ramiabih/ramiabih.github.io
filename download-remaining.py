#!/usr/bin/env python3
"""
Download remaining product images with working URLs
"""

import requests
from pathlib import Path

IMAGES_DIR = Path("wishlist-images")

# Working image URLs for remaining products
REMAINING_IMAGES = {
    "07-sigma-fp.jpg": "https://images.squarespace-cdn.com/content/v1/53d5a45ae4b08fb6de130fca/1565024318583-QQ3YIWI3JMSCABTAKBR5/ke17ZwdGBToddI8pDm48kLkXF2pIyv_F2eUT9F60jBl7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z4YTzHvnKhyp6Da-NYroOW3ZGjoBKy3azqku80C789l0iyqMbMesKd95J-X4EagrgU9L3Sa3U8cogeb0tjXbfawd0urKshkc5MgdBeJmALQKw/FP-L_side1.jpg",
    "08-opal-tadpole.png": "https://images.ctfassets.net/xxo14k7ywmtv/3p8uMjADW35pVo6SyJBmxS/d1f4d0eb5b0c52f9b0c7a6b4e6c5a8e2/tadpole-hero.png",
    "11-thinkpad-x1.jpg": "https://p2-ofp.static.pub/fes/cms/2024/05/15/jt98qcwvddpbvqu6bx4o9p0vjjq8le576214.png",
    "15-porsche-911.png": "https://files.porsche.com/filestore/image/multimedia/none/992-2nd-t-s-c4s-modelimage-sideshot/model/e02d7c8f-42d7-11ed-80f6-005056bbdc38/porsche-model.png",
    "17-dyson-v15.jpg": "https://m.media-amazon.com/images/I/61vGc3gNBbL._AC_SL1500_.jpg",
    "20-ferrari-book.jpg": "https://m.media-amazon.com/images/I/81J7-1KcwEL._SL1500_.jpg",
    "23-common-projects.jpg": "https://m.media-amazon.com/images/I/71Y4xrHVi9L._AC_SY695_.jpg",
    "24-ic-lights.jpg": "https://m.media-amazon.com/images/I/61-o8oHJY0L._AC_SL1500_.jpg",
    "27-sennheiser.jpg": "https://m.media-amazon.com/images/I/61UpkW+rZzL._AC_SL1500_.jpg",
    "29-yeelight.jpg": "https://m.media-amazon.com/images/I/61Oc9E9sJOL._AC_SL1500_.jpg",
    "30-tool-kit.jpg": "https://m.media-amazon.com/images/I/81Gr4G1gz5L._AC_SL1500_.jpg",
    "33-klipsch-fives.jpg": "https://m.media-amazon.com/images/I/61EWPFL+M0L._AC_SL1000_.jpg",
}

def download_image(url, filename):
    """Download a single image"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=15, stream=True)
        response.raise_for_status()

        filepath = IMAGES_DIR / filename
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return True
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        return False

def main():
    print("📥 Downloading remaining images...\n")

    success_count = 0
    for filename, url in REMAINING_IMAGES.items():
        product_name = filename.replace('.jpg', '').replace('.png', '').replace('-', ' ').title()
        print(f"Downloading: {product_name}")

        if download_image(url, filename):
            print(f"  ✓ Saved: {filename}\n")
            success_count += 1
        else:
            print()

    print(f"✅ Successfully downloaded {success_count}/{len(REMAINING_IMAGES)} images")

if __name__ == '__main__':
    main()
