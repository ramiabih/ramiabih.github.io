#!/usr/bin/env python3
"""
Download missing product images with fallback URLs
"""

import requests
from pathlib import Path

IMAGES_DIR = Path("wishlist-images")

# Manual fallback URLs for products that failed
FALLBACK_IMAGES = {
    "fp": ("https://www.bhphotovideo.com/images/images500x500/sigma_fp_l_mirrorless_digital_1634654956_1672645.jpg", "07-fp.jpg"),
    "Tadpole": ("https://framerusercontent.com/images/JhB2IkrStyaIslm6QqTW9KBzK0.png", "08-tadpole.png"),
    "ThinkPad X1 Carbon Gen 13": ("https://p3-ofp.static.pub/fes/cms/2024/06/13/b5wowj4g6j93ej3q2v9p4gq2s28a7h165267.png", "11-thinkpad-x1-carbon.png"),
    "911 Turbo S": ("https://files.porsche.com/filestore/image/multimedia/none/992-2nd-t-s-modelimage-sideshot/model/0bc11259-5c5f-11ed-80fb-005056bbdc38/porsche-model.png", "15-911-turbo-s.png"),
    "V15 Detect Absolute": ("https://dyson-h.assetsadobe2.com/is/image/content/dam/dyson/images/products/primary/394882-01.png", "17-v15-detect.png"),
    "Ferrari Art Edition": ("https://www.taschen.com/media/images/960/art_ferrari_gift_fo_int_3d_04677_2005221713_id_1423866.png", "20-ferrari-art.png"),
    "Original Achilles Low": ("https://cdn-images.farfetch-contents.com/14/22/75/47/14227547_22054104_1000.jpg", "23-achilles-low.jpg"),
    "IC Lights T1 Low": ("https://www.flos.com/media/catalog/product/cache/6/small_image/415x340/17f82f742ffe127f42dca9de82fb58b1/F/3/F3157057_product.jpg", "24-ic-lights.jpg"),
    "HDB 630": ("https://cdn.shopify.com/s/files/1/0016/3437/7835/files/Sennheiser-HD-660S2-Headphones-1.png", "27-hdb-630.png"),
    "Air96 V2": ("https://m.media-amazon.com/images/I/61h5fR7JGBL._AC_SL1500_.jpg", "29-air96.jpg"),
    "322-Piece Tool Kit": ("https://m.media-amazon.com/images/I/81vWqPTqpEL._AC_SL1500_.jpg", "30-tool-kit.jpg"),
    "The Fives Heritage Powered Speakers": ("https://m.media-amazon.com/images/I/61Xoyt7NHTL._AC_SL1000_.jpg", "33-the-fives.jpg"),
}

def download_fallback_images():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }

    print("📥 Downloading fallback images...\n")

    for product_name, (url, filename) in FALLBACK_IMAGES.items():
        try:
            print(f"Downloading: {product_name}")
            response = requests.get(url, headers=headers, timeout=15, stream=True)
            response.raise_for_status()

            filepath = IMAGES_DIR / filename

            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"  ✓ Saved: {filename}\n")

        except Exception as e:
            print(f"  ❌ Failed: {e}\n")

    print("✅ Done downloading fallback images!")

if __name__ == '__main__':
    download_fallback_images()
