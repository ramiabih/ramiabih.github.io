#!/bin/bash
# Create simple SVG placeholders for products without images

cd wishlist-images

# Function to create an SVG placeholder
create_svg() {
    local filename=$1
    local text=$2

    cat > "$filename" << EOF
<svg width="400" height="400" xmlns="http://www.w3.org/2000/svg">
  <rect width="400" height="400" fill="#fafafa"/>
  <text x="50%" y="50%" font-family="system-ui, -apple-system, sans-serif" font-size="16" fill="#999" text-anchor="middle" dominant-baseline="middle">
    $text
  </text>
</svg>
EOF
}

# Create placeholders
create_svg "07-sigma-fp.svg" "Sigma fp Camera"
create_svg "08-opal-tadpole.svg" "Opal Tadpole"
create_svg "11-thinkpad-x1.svg" "ThinkPad X1 Carbon"
create_svg "15-porsche-911.svg" "Porsche 911 Turbo S"
create_svg "17-dyson-v15.svg" "Dyson V15 Detect"
create_svg "20-ferrari-book.svg" "Ferrari Art Edition"
create_svg "23-common-projects.svg" "Common Projects"
create_svg "24-ic-lights.svg" "IC Lights T1 Low"
create_svg "27-sennheiser.svg" "Sennheiser HDB 630"
create_svg "29-yeelight.svg" "Yeelight Air96 V2"
create_svg "30-tool-kit.svg" "WORKPRO Tool Kit"
create_svg "33-klipsch-fives.svg" "Klipsch The Fives"

echo "✅ Created 12 SVG placeholders"
