# How to Run This Site Locally

This is a static HTML website that can be run locally in several ways. Here are the most common and easiest methods:

## Method 1: Using Python (Recommended)

### Python 3 (Most Common)
```bash
# Navigate to the project directory
cd /Users/rami/Documents/GitHub/ramiabih.github.io

# Start a simple HTTP server
python3 -m http.server 8000
```

### Python 2 (if Python 3 is not available)
```bash
python -m SimpleHTTPServer 8000
```

Then open your browser and go to: `http://localhost:8000`

## Method 2: Using Node.js

If you have Node.js installed:

```bash
# Install a simple HTTP server globally
npm install -g http-server

# Navigate to the project directory
cd /Users/rami/Documents/GitHub/ramiabih.github.io

# Start the server
http-server -p 8000
```

Then open your browser and go to: `http://localhost:8000`

## Method 3: Using PHP

If you have PHP installed:

```bash
# Navigate to the project directory
cd /Users/rami/Documents/GitHub/ramiabih.github.io

# Start PHP's built-in server
php -S localhost:8000
```

Then open your browser and go to: `http://localhost:8000`

## Method 4: Using Live Server (VS Code Extension)

If you're using VS Code:

1. Install the "Live Server" extension
2. Right-click on `index.html`
3. Select "Open with Live Server"
4. The site will open in your browser with live reload

## Method 5: Using npx (No Installation Required)

```bash
# Navigate to the project directory
cd /Users/rami/Documents/GitHub/ramiabih.github.io

# Run a simple server using npx (no installation needed)
npx http-server -p 8000
```

## Troubleshooting

### Port Already in Use
If port 8000 is already in use, try a different port:
- Python: `python3 -m http.server 8080`
- Node.js: `http-server -p 8080`
- PHP: `php -S localhost:8080`

### File Permissions
If you get permission errors, make sure you have read access to all files in the directory.

### CORS Issues
If you encounter CORS issues when loading resources, make sure you're accessing the site through `http://localhost:8000` and not opening the HTML file directly in the browser.

## Why Use a Local Server?

Opening HTML files directly in the browser (file:// protocol) can cause issues with:
- Loading external resources
- CORS (Cross-Origin Resource Sharing) restrictions
- Relative path resolution
- JavaScript modules

Using a local HTTP server ensures the site behaves exactly as it would when deployed to GitHub Pages.

## Quick Start (Recommended)

The easiest way to get started:

```bash
# Navigate to your project
cd /Users/rami/Documents/GitHub/ramiabih.github.io

# Start Python server (works on most systems)
python3 -m http.server 8000

# Open browser to http://localhost:8000
```

That's it! Your site should now be running locally and accessible in your browser.
