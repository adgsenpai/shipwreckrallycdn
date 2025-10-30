import os
from pathlib import Path

# Configuration
DOMAIN = "https://cdn.shipwreckrally.co.za"
GALLERY_DIR = "static/gallery"
OUTPUT_TXT = "compile.txt"
OUTPUT_HTML = "index.html"

def get_media_files(directory):
    """Get all image and video files from the directory"""
    media_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.mp4', '.webm', '.mov'}
    media_files = []
    
    gallery_path = Path(directory)
    if not gallery_path.exists():
        print(f"Directory {directory} does not exist!")
        return []
    
    for file in sorted(gallery_path.iterdir()):
        if file.is_file() and file.suffix.lower() in media_extensions:
            media_files.append(file.name)
    
    return media_files

def generate_compile_txt(media_files):
    """Generate compile.txt with CDN URLs"""
    with open(OUTPUT_TXT, 'w', encoding='utf-8') as f:
        f.write("Shipwreck Rally CDN - Media Files\n")
        f.write("=" * 60 + "\n\n")
        
        for filename in media_files:
            url = f"{DOMAIN}/{GALLERY_DIR}/{filename}"
            f.write(f"{url}\n")
        
        f.write("\n" + "=" * 60 + "\n")
        f.write(f"Total files: {len(media_files)}\n")
    
    print(f"✓ Generated {OUTPUT_TXT} with {len(media_files)} files")

def generate_index_html(media_files):
    """Generate index.html with gallery display"""
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Shipwreck Rally CDN</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }}
        
        header {{
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 30px;
            border-bottom: 3px solid #667eea;
        }}
        
        h1 {{
            color: #667eea;
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        }}
        
        .subtitle {{
            color: #666;
            font-size: 1.2em;
            margin-bottom: 20px;
        }}
        
        .stats {{
            display: flex;
            justify-content: center;
            gap: 30px;
            flex-wrap: wrap;
            margin: 20px 0;
        }}
        
        .stat-box {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 30px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }}
        
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
        }}
        
        .stat-label {{
            font-size: 0.9em;
            opacity: 0.9;
        }}
        
        .gallery {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }}
        
        .gallery-item {{
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            position: relative;
        }}
        
        .gallery-item:hover {{
            transform: translateY(-10px);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
        }}
        
        .gallery-item img,
        .gallery-item video {{
            width: 100%;
            height: 250px;
            object-fit: cover;
            display: block;
        }}
        
        .gallery-item-info {{
            padding: 15px;
            background: #f8f9fa;
        }}
        
        .filename {{
            font-size: 0.85em;
            color: #666;
            word-break: break-word;
            margin-bottom: 10px;
        }}
        
        .copy-btn {{
            background: #667eea;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 0.9em;
            width: 100%;
            transition: background 0.3s ease;
        }}
        
        .copy-btn:hover {{
            background: #764ba2;
        }}
        
        .copy-btn:active {{
            background: #5a67d8;
        }}
        
        .copied {{
            background: #48bb78 !important;
        }}
        
        footer {{
            text-align: center;
            margin-top: 50px;
            padding-top: 30px;
            border-top: 2px solid #e2e8f0;
            color: #666;
        }}
        
        .search-box {{
            margin: 30px 0;
            text-align: center;
        }}
        
        #searchInput {{
            width: 100%;
            max-width: 600px;
            padding: 15px 20px;
            font-size: 1em;
            border: 2px solid #667eea;
            border-radius: 10px;
            outline: none;
            transition: border-color 0.3s ease;
        }}
        
        #searchInput:focus {{
            border-color: #764ba2;
        }}
        
        .video-indicator {{
            position: absolute;
            top: 10px;
            right: 10px;
            background: rgba(0, 0, 0, 0.7);
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 0.8em;
        }}
        
        @media (max-width: 768px) {{
            .container {{
                padding: 20px;
            }}
            
            h1 {{
                font-size: 2em;
            }}
            
            .gallery {{
                grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
                gap: 15px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🚢 Shipwreck Rally CDN</h1>
            <p class="subtitle">Media Content Delivery Network</p>
            
            <div class="stats">
                <div class="stat-box">
                    <div class="stat-number" id="totalFiles">{len(media_files)}</div>
                    <div class="stat-label">Total Files</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number" id="imageCount">{sum(1 for f in media_files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')))}</div>
                    <div class="stat-label">Images</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number" id="videoCount">{sum(1 for f in media_files if f.lower().endswith(('.mp4', '.webm', '.mov')))}</div>
                    <div class="stat-label">Videos</div>
                </div>
            </div>
        </header>
        
        <div class="search-box">
            <input type="text" id="searchInput" placeholder="🔍 Search files...">
        </div>
        
        <div class="gallery" id="gallery">
"""
    
    # Add gallery items
    for filename in media_files:
        url = f"{DOMAIN}/{GALLERY_DIR}/{filename}"
        is_video = filename.lower().endswith(('.mp4', '.webm', '.mov'))
        
        if is_video:
            media_tag = f'<video src="{url}" controls muted></video>\n                    <div class="video-indicator">▶️ VIDEO</div>'
        else:
            media_tag = f'<img src="{url}" alt="{filename}" loading="lazy">'
        
        html_content += f"""            <div class="gallery-item" data-filename="{filename.lower()}">
                <div style="position: relative;">
                    {media_tag}
                </div>
                <div class="gallery-item-info">
                    <div class="filename" title="{filename}">{filename}</div>
                    <button class="copy-btn" onclick="copyToClipboard('{url}', this)">
                        📋 Copy URL
                    </button>
                </div>
            </div>
"""
    
    html_content += f"""        </div>
        
        <footer>
            <p>🌊 Shipwreck Rally CDN • Generated on {Path(OUTPUT_HTML).stat().st_mtime if Path(OUTPUT_HTML).exists() else 'now'}</p>
            <p style="margin-top: 10px; font-size: 0.9em;">
                <a href="{OUTPUT_TXT}" style="color: #667eea; text-decoration: none;">📄 View compile.txt</a>
            </p>
        </footer>
    </div>
    
    <script>
        function copyToClipboard(url, button) {{
            navigator.clipboard.writeText(url).then(() => {{
                const originalText = button.textContent;
                button.textContent = '✓ Copied!';
                button.classList.add('copied');
                
                setTimeout(() => {{
                    button.textContent = originalText;
                    button.classList.remove('copied');
                }}, 2000);
            }}).catch(err => {{
                console.error('Failed to copy:', err);
                alert('Failed to copy URL');
            }});
        }}
        
        // Search functionality
        const searchInput = document.getElementById('searchInput');
        const galleryItems = document.querySelectorAll('.gallery-item');
        
        searchInput.addEventListener('input', (e) => {{
            const searchTerm = e.target.value.toLowerCase();
            
            galleryItems.forEach(item => {{
                const filename = item.getAttribute('data-filename');
                if (filename.includes(searchTerm)) {{
                    item.style.display = 'block';
                }} else {{
                    item.style.display = 'none';
                }}
            }});
        }});
        
        // Lazy loading enhancement
        if ('loading' in HTMLImageElement.prototype) {{
            console.log('Browser supports native lazy loading');
        }} else {{
            console.log('Browser does not support native lazy loading');
        }}
    </script>
</body>
</html>"""
    
    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ Generated {OUTPUT_HTML} with gallery display")

def main():
    """Main function to run the compilation"""
    print("=" * 60)
    print("Shipwreck Rally CDN - Compiler")
    print("=" * 60)
    print()
    
    # Get all media files
    print(f"Scanning directory: {GALLERY_DIR}")
    media_files = get_media_files(GALLERY_DIR)
    
    if not media_files:
        print("⚠ No media files found!")
        return
    
    print(f"Found {len(media_files)} media files")
    print()
    
    # Generate outputs
    generate_compile_txt(media_files)
    generate_index_html(media_files)
    
    print()
    print("=" * 60)
    print("✓ Compilation complete!")
    print(f"  - {OUTPUT_TXT}: List of all CDN URLs")
    print(f"  - {OUTPUT_HTML}: Interactive gallery page")
    print("=" * 60)

if __name__ == "__main__":
    main()
