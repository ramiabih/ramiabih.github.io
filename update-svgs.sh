#!/bin/bash
cd wishlist-images

# Function to create a product SVG
create_product_svg() {
    local filename=$1
    local text=$2

    cat > "$filename" << EOF
<svg width="400" height="400" xmlns="http://www.w3.org/2000/svg">
  <rect width="400" height="400" fill="#f5f5f5"/>
  <rect x="100" y="120" width="200" height="140" rx="8" fill="#e8e8e8"/>
  <text x="50%" y="300" font-family="system-ui, -apple-system, sans-serif" font-size="16" font-weight="500" fill="#666" text-anchor="middle">
    $text
  </text>
  <text x="50%" y="330" font-family="system-ui, -apple-system, sans-serif" font-size="12" fill="#999" text-anchor="middle">
    Product image
  </text>
</svg>
EOF
}

# Create all SVG placeholders
create_product_svg "07-sigma-fp.svg" "Sigma fp Camera"
create_product_svg "08-opal-tadpole.svg" "Opal Tadpole"
create_product_svg "11-thinkpad-x1.svg" "ThinkPad X1 Carbon"
create_product_svg "15-porsche-911.svg" "Porsche 911 Turbo S"
create_product_svg "17-dyson-v15.svg" "Dyson V15 Detect"
create_product_svg "20-ferrari-book.svg" "Ferrari Art Edition"
create_product_svg "23-common-projects.svg" "Common Projects"
create_product_svg "24-ic-lights.svg" "IC Lights T1 Low"
create_product_svg "27-sennheiser.svg" "Sennheiser HDB 630"
create_product_svg "29-yeelight.svg" "Yeelight Air96 V2"
create_product_svg "30-tool-kit.svg" "WORKPRO Tool Kit"
create_product_svg "33-klipsch-fives.svg" "Klipsch The Fives"

echo "✅ Updated 12 SVG placeholders"
