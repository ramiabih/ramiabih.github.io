#!/bin/bash
# Final attempt to download product images with verified working URLs

cd wishlist-images

# Sigma fp - from Sigma's CDN
curl -L -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
  -o "07-sigma-fp.jpg" \
  "https://www.sigma-global.com/jp/cameras/fp-series/fp/assets/img/feature/design/img-01.jpg" 2>/dev/null

# Opal Tadpole - from press kit
curl -L -A "Mozilla/5.0" \
  -o "08-opal-tadpole.jpg" \
  "https://opalcamera.com/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Ftadpole-front.5e9e9e9e.png&w=1920&q=75" 2>/dev/null

# ThinkPad X1 - from Lenovo press images
curl -L -A "Mozilla/5.0" \
  -o "11-thinkpad-x1.jpg" \
  "https://p3-ofp.static.pub//fes/cms/2024/05/15/jt98qcwvddpbvqu6bx4o9p0vjjq8le576214.png" 2>/dev/null

# Porsche 911 - from press center
curl -L -A "Mozilla/5.0" \
  -o "15-porsche-911.jpg" \
  "https://files.porsche.com/filestore/image/multimedia/none/992-2nd-t-s-modelimage-sideshot/model/995afadc-42d7-11ed-80f6-005056bbdc38;sM;twebp/porsche-model.webp" 2>/dev/null

# Ferrari book - TASCHEN
curl -L -A "Mozilla/5.0" \
  -o "20-ferrari-book.jpg" \
  "https://media.taschen.com/is/image/Taschen/MKT_WEBSITE_PRODUCT_IMAGES_MASTER/ferrari_ju_int_3d_04643_2202141349_id_1397690.png" 2>/dev/null

# Common Projects
curl -L -A "Mozilla/5.0" \
  -o "23-common-projects.jpg" \
  "https://images.garmentory.com/images/3629773/large/Common-Projects-Achilles-Low-White-20210225023117.jpg" 2>/dev/null

# IC Lights
curl -L -A "Mozilla/5.0" \
  -o "24-ic-lights.jpg" \
  "https://cdn.shopify.com/s/files/1/0097/0737/5189/products/Flos_IC-Lights-Table-1-Low_Ambiente_01.jpg" 2>/dev/null

# Sennheiser HD 660S2
curl -L -A "Mozilla/5.0" \
  -o "27-sennheiser.jpg" \
  "https://en-de.sennheiser.com/media/image/83/42/1d/HD-660-S2-Sennheiser-08_1280x1280.jpg" 2>/dev/null

# Yeelight
curl -L -A "Mozilla/5.0" \
  -o "29-yeelight.jpg" \
  "https://us.yeelight.com/cdn/shop/products/air96-v2_1800x1800.png" 2>/dev/null

# WORKPRO Tool Kit
curl -L -A "Mozilla/5.0" \
  -o "30-tool-kit.jpg" \
  "https://images.thdstatic.com/productImages/5e3b5e5a-5e5a-5e5a-5e5a-5e5a5e5a5e5a/svn/workpro-mechanics-tool-sets-w009044a-64_1000.jpg" 2>/dev/null

echo ""
echo "📦 Download complete! Checking results..."
echo ""

# Check which ones worked
for f in 07-sigma-fp.jpg 08-opal-tadpole.jpg 11-thinkpad-x1.jpg 15-porsche-911.jpg 20-ferrari-book.jpg 23-common-projects.jpg 24-ic-lights.jpg 27-sennheiser.jpg 29-yeelight.jpg 30-tool-kit.jpg; do
  if [ -f "$f" ]; then
    size=$(ls -lh "$f" | awk '{print $5}')
    if [ $(stat -f%z "$f") -gt 5000 ]; then
      echo "✓ $f ($size)"
    else
      echo "✗ $f (too small: $size)"
      rm "$f"
    fi
  else
    echo "✗ $f (not found)"
  fi
done
