#!/bin/bash

# Function to create a modern, minimalist product SVG
create_product_svg() {
    local filename=$1
    local product_name=$2
    local icon=$3

    cat > "$filename" << EOF
<svg width="800" height="800" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg-$filename" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#fafafa;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#f5f5f5;stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="800" height="800" fill="url(#bg-$filename)"/>
  <g transform="translate(400, 350)">
    $icon
  </g>
  <text x="50%" y="620" font-family="system-ui, -apple-system, sans-serif" font-size="28" font-weight="300" fill="#999" text-anchor="middle" letter-spacing="0.5">
    $product_name
  </text>
</svg>
EOF
}

# Icons
camera='<rect x="-80" y="-50" width="160" height="100" rx="12" fill="none" stroke="#ccc" stroke-width="3"/><circle cx="30" cy="0" r="35" fill="none" stroke="#ccc" stroke-width="3"/><circle cx="30" cy="0" r="25" fill="none" stroke="#ccc" stroke-width="2"/><rect x="-65" y="-30" width="30" height="15" rx="3" fill="#e8e8e8"/>'

webcam='<circle cx="0" cy="0" r="50" fill="none" stroke="#ccc" stroke-width="3"/><circle cx="0" cy="0" r="30" fill="none" stroke="#ccc" stroke-width="3"/><circle cx="0" cy="0" r="15" fill="#e8e8e8"/><rect x="-8" y="50" width="16" height="30" rx="8" fill="#e8e8e8"/>'

laptop='<rect x="-100" y="-50" width="200" height="120" rx="8" fill="none" stroke="#ccc" stroke-width="3"/><rect x="-100" y="-50" width="200" height="90" rx="8" fill="#f0f0f0"/><line x1="-120" y1="70" x2="120" y2="70" stroke="#ccc" stroke-width="3"/><rect x="-20" y="70" width="40" height="4" fill="#e8e8e8"/>'

book='<rect x="-70" y="-90" width="140" height="180" rx="4" fill="none" stroke="#ccc" stroke-width="3"/><rect x="-60" y="-80" width="120" height="160" rx="2" fill="#f0f0f0"/><text x="0" y="10" font-family="serif" font-size="48" font-weight="bold" fill="#999" text-anchor="middle">F</text>'

sneaker='<ellipse cx="0" cy="20" rx="90" ry="25" fill="#f0f0f0"/><path d="M -80 -10 Q -60 -40, 0 -45 Q 60 -40, 80 -10 L 85 20 L -85 20 Z" fill="none" stroke="#ccc" stroke-width="3"/>'

lamp='<circle cx="0" cy="-60" r="40" fill="none" stroke="#ccc" stroke-width="3"/><circle cx="0" cy="-60" r="30" fill="#f0f0f0" opacity="0.5"/><line x1="0" y1="-20" x2="0" y2="80" stroke="#ccc" stroke-width="3"/><ellipse cx="0" cy="80" rx="30" ry="8" fill="#e8e8e8"/>'

desk_lamp='<path d="M -40 -80 L 0 40 L 40 -80 Z" fill="none" stroke="#ccc" stroke-width="3"/><ellipse cx="0" cy="-80" rx="50" ry="15" fill="#f0f0f0"/><rect x="-5" y="40" width="10" height="50" fill="#e8e8e8"/><ellipse cx="0" cy="90" rx="35" ry="10" fill="#e8e8e8"/>'

toolbox='<rect x="-80" y="-30" width="160" height="80" rx="6" fill="none" stroke="#ccc" stroke-width="3"/><rect x="-80" y="-30" width="160" height="25" fill="#f0f0f0"/><path d="M -25 -30 L -25 -50 L 25 -50 L 25 -30" fill="none" stroke="#ccc" stroke-width="3"/>'

# Create SVGs
create_product_svg "07-sigma-fp.svg" "Sigma fp" "$camera"
create_product_svg "08-opal-tadpole.svg" "Opal Tadpole" "$webcam"
create_product_svg "11-thinkpad-x1.svg" "ThinkPad X1 Carbon" "$laptop"
create_product_svg "20-ferrari-book.svg" "Ferrari" "$book"
create_product_svg "23-common-projects.svg" "Common Projects" "$sneaker"
create_product_svg "24-ic-lights.svg" "IC Lights" "$lamp"
create_product_svg "29-yeelight.svg" "Yeelight" "$desk_lamp"
create_product_svg "30-tool-kit.svg" "WORKPRO" "$toolbox"

echo "✅ Created modern SVG placeholders"
