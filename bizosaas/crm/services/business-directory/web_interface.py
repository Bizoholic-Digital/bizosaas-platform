"""
Web Interface for Business Directory Service
Provides HTML endpoints for browser-friendly directory viewing
"""

from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

# Import the main app and service
from directory_service import app, directory_service

# Add HTML endpoints to the existing FastAPI app
@app.get("/", response_class=HTMLResponse)
async def directory_homepage():
    """HTML homepage for directory service"""
    
    directories = directory_service.available_directories
    categories = directory_service.categories
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>BizOSaaS Business Directory Service</title>
        <style>
            body {{ 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                margin: 0; 
                padding: 20px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }}
            .container {{ 
                max-width: 1200px; 
                margin: 0 auto; 
                background: white;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                padding: 30px;
            }}
            h1 {{ 
                color: #333; 
                text-align: center; 
                margin-bottom: 10px;
                font-size: 2.5em;
            }}
            .subtitle {{
                text-align: center;
                color: #666;
                margin-bottom: 30px;
                font-size: 1.2em;
            }}
            .stats {{
                display: flex;
                justify-content: space-around;
                margin-bottom: 30px;
                flex-wrap: wrap;
            }}
            .stat-card {{
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                min-width: 200px;
                margin: 10px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }}
            .stat-number {{
                font-size: 2.5em;
                font-weight: bold;
                display: block;
            }}
            .stat-label {{
                font-size: 1.1em;
                margin-top: 5px;
            }}
            .section {{
                margin: 30px 0;
            }}
            .section h2 {{
                color: #333;
                border-bottom: 3px solid #667eea;
                padding-bottom: 10px;
                margin-bottom: 20px;
            }}
            .directory-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 15px;
                margin-top: 20px;
            }}
            .directory-item {{
                background: #f8f9ff;
                border: 1px solid #e1e5e9;
                border-radius: 8px;
                padding: 15px;
                transition: all 0.3s ease;
            }}
            .directory-item:hover {{
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                border-color: #667eea;
            }}
            .directory-name {{
                font-weight: bold;
                color: #333;
                font-size: 1.1em;
                margin-bottom: 8px;
            }}
            .directory-meta {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 10px;
            }}
            .category-tag {{
                background: #667eea;
                color: white;
                padding: 4px 8px;
                border-radius: 12px;
                font-size: 0.8em;
                text-transform: capitalize;
            }}
            .priority-badge {{
                padding: 4px 8px;
                border-radius: 12px;
                font-size: 0.8em;
                font-weight: bold;
            }}
            .priority-critical {{
                background: #ff4757;
                color: white;
            }}
            .priority-high {{
                background: #ff7675;
                color: white;
            }}
            .priority-medium {{
                background: #fdcb6e;
                color: #333;
            }}
            .priority-low {{
                background: #95a5a6;
                color: white;
            }}
            .auto-submit {{
                background: #00b894;
                color: white;
                padding: 2px 6px;
                border-radius: 10px;
                font-size: 0.7em;
                margin-left: 10px;
            }}
            .categories-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 15px;
            }}
            .category-card {{
                background: linear-gradient(135deg, #ff7675, #fd79a8);
                color: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }}
            .category-icon {{
                font-size: 2.5em;
                margin-bottom: 10px;
                display: block;
            }}
            .category-name {{
                font-size: 1.3em;
                font-weight: bold;
                margin-bottom: 5px;
            }}
            .category-count {{
                font-size: 1.1em;
                opacity: 0.9;
            }}
            .api-links {{
                background: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 20px;
                margin-top: 20px;
            }}
            .api-links h3 {{
                color: #333;
                margin-top: 0;
            }}
            .api-link {{
                display: inline-block;
                background: #007bff;
                color: white;
                padding: 8px 15px;
                text-decoration: none;
                border-radius: 5px;
                margin: 5px 10px 5px 0;
                font-size: 0.9em;
            }}
            .api-link:hover {{
                background: #0056b3;
                text-decoration: none;
                color: white;
            }}
            .filter-section {{
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 20px;
            }}
            .filter-buttons {{
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
                margin-top: 10px;
            }}
            .filter-btn {{
                padding: 8px 15px;
                border: 1px solid #667eea;
                background: white;
                color: #667eea;
                border-radius: 20px;
                cursor: pointer;
                transition: all 0.3s ease;
            }}
            .filter-btn:hover, .filter-btn.active {{
                background: #667eea;
                color: white;
            }}
        </style>
        <script>
            function filterDirectories(category) {{
                const directories = document.querySelectorAll('.directory-item');
                const buttons = document.querySelectorAll('.filter-btn');
                
                // Reset all buttons
                buttons.forEach(btn => btn.classList.remove('active'));
                
                // Activate clicked button
                event.target.classList.add('active');
                
                directories.forEach(dir => {{
                    if (category === 'all') {{
                        dir.style.display = 'block';
                    }} else {{
                        const dirCategory = dir.getAttribute('data-category');
                        dir.style.display = dirCategory === category ? 'block' : 'none';
                    }}
                }});
                
                // Update count
                const visibleDirs = document.querySelectorAll('.directory-item[style="display: block;"], .directory-item:not([style*="display: none"])');
                document.getElementById('directory-count').textContent = category === 'all' ? {len(directories)} : visibleDirs.length;
            }}
            
            function searchDirectories() {{
                const searchTerm = document.getElementById('search').value.toLowerCase();
                const directories = document.querySelectorAll('.directory-item');
                let visibleCount = 0;
                
                directories.forEach(dir => {{
                    const name = dir.querySelector('.directory-name').textContent.toLowerCase();
                    const category = dir.getAttribute('data-category').toLowerCase();
                    
                    if (name.includes(searchTerm) || category.includes(searchTerm)) {{
                        dir.style.display = 'block';
                        visibleCount++;
                    }} else {{
                        dir.style.display = 'none';
                    }}
                }});
                
                document.getElementById('directory-count').textContent = visibleCount;
            }}
        </script>
    </head>
    <body>
        <div class="container">
            <h1>🏢 BizOSaaS Business Directory Service</h1>
            <p class="subtitle">Comprehensive business directory management and client onboarding integration</p>
            
            <div class="stats">
                <div class="stat-card">
                    <span class="stat-number">{len(directories)}</span>
                    <span class="stat-label">Total Directories</span>
                </div>
                <div class="stat-card">
                    <span class="stat-number">{len(categories)}</span>
                    <span class="stat-label">Business Categories</span>
                </div>
                <div class="stat-card">
                    <span class="stat-number">{len([d for d in directories if d.get('priority') == 'critical'])}</span>
                    <span class="stat-label">Critical Priority</span>
                </div>
                <div class="stat-card">
                    <span class="stat-number">{len([d for d in directories if d.get('auto_submit', False)])}</span>
                    <span class="stat-label">Auto-Submit Ready</span>
                </div>
            </div>
            
            <div class="section">
                <h2>📊 Business Categories</h2>
                <div class="categories-grid">
                    {"".join([f'''
                    <div class="category-card">
                        <span class="category-icon">{cat["icon"]}</span>
                        <div class="category-name">{cat["name"]}</div>
                        <div class="category-count">{cat["count"]} businesses</div>
                    </div>
                    ''' for cat in categories])}
                </div>
            </div>
            
            <div class="section">
                <h2>🏪 Directory Platforms (<span id="directory-count">{len(directories)}</span>)</h2>
                
                <div class="filter-section">
                    <h3>Filter by Category:</h3>
                    <input type="text" id="search" placeholder="Search directories..." 
                           onkeyup="searchDirectories()" 
                           style="width: 300px; padding: 8px; border: 1px solid #ddd; border-radius: 5px; margin-bottom: 15px;">
                    <div class="filter-buttons">
                        <button class="filter-btn active" onclick="filterDirectories('all')">All</button>
                        {"".join([f'<button class="filter-btn" onclick="filterDirectories(\\"{cat}\\")">{cat.replace("_", " ").title()}</button>' for cat in sorted(set([d.get('category', 'other') for d in directories]))])}
                    </div>
                </div>
                
                <div class="directory-grid">
                    {"".join([f'''
                    <div class="directory-item" data-category="{d.get('category', 'other')}">
                        <div class="directory-name">{d["name"]}</div>
                        <div class="directory-meta">
                            <span class="category-tag">{d.get("category", "general").replace("_", " ")}</span>
                            <div>
                                <span class="priority-badge priority-{d.get('priority', 'medium')}">{d.get("priority", "medium").upper()}</span>
                                {f'<span class="auto-submit">AUTO-SUBMIT</span>' if d.get("auto_submit", False) else ''}
                            </div>
                        </div>
                        {f'<div style="color: #666; font-size: 0.9em; margin-top: 8px;">Industries: {", ".join(d["industries"])}</div>' if d.get("industries") else ''}
                        {f'<div style="color: #666; font-size: 0.9em; margin-top: 5px;">📍 {d["location"]}</div>' if d.get("location") else ''}
                    </div>
                    ''' for d in directories])}
                </div>
            </div>
            
            <div class="api-links">
                <h3>🔗 API Endpoints</h3>
                <a href="/directories" class="api-link" target="_blank">📄 JSON Directories</a>
                <a href="/categories" class="api-link" target="_blank">📋 JSON Categories</a>
                <a href="/health" class="api-link" target="_blank">❤️ Health Check</a>
                <a href="/docs" class="api-link" target="_blank">📚 API Documentation</a>
            </div>
        </div>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)

@app.get("/directories/view", response_class=HTMLResponse)
async def view_directories_html():
    """HTML view of directories with enhanced filtering"""
    
    directories = directory_service.available_directories
    
    # Group directories by category
    categories_dict = {}
    for d in directories:
        category = d.get('category', 'other')
        if category not in categories_dict:
            categories_dict[category] = []
        categories_dict[category].append(d)
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Business Directories - Detailed View</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
            .container {{ max-width: 1200px; margin: 0 auto; background: white; border-radius: 10px; padding: 30px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }}
            h1 {{ color: #333; text-align: center; }}
            .category-section {{ margin: 30px 0; }}
            .category-header {{ background: #667eea; color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px; }}
            .directory-list {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 10px; }}
            .directory-item {{ background: #f8f9ff; border-left: 4px solid #667eea; padding: 15px; margin-bottom: 10px; }}
            .directory-name {{ font-weight: bold; color: #333; margin-bottom: 5px; }}
            .directory-details {{ font-size: 0.9em; color: #666; }}
            .priority-critical {{ border-left-color: #e74c3c; }}
            .priority-high {{ border-left-color: #f39c12; }}
            .priority-medium {{ border-left-color: #3498db; }}
            .priority-low {{ border-left-color: #95a5a6; }}
            .back-link {{ display: inline-block; margin-bottom: 20px; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <a href="/" class="back-link">← Back to Dashboard</a>
            <h1>📁 Business Directories by Category</h1>
            
            {"".join([f'''
            <div class="category-section">
                <div class="category-header">
                    <h2>{category.replace("_", " ").title()} ({len(dirs)} directories)</h2>
                </div>
                <div class="directory-list">
                    {"".join([f"""
                    <div class="directory-item priority-{d.get('priority', 'medium')}">
                        <div class="directory-name">{d["name"]}</div>
                        <div class="directory-details">
                            Priority: {d.get("priority", "medium").title()}<br>
                            Category: {d.get("category", "general").replace("_", " ").title()}<br>
                            Auto Submit: {"✅ Yes" if d.get("auto_submit", False) else "❌ No"}
                            {f'<br>Industries: {", ".join(d["industries"])}' if d.get("industries") else ''}
                            {f'<br>Location: {d["location"]}' if d.get("location") else ''}
                        </div>
                    </div>
                    """ for d in dirs])}
                </div>
            </div>
            ''' for category, dirs in sorted(categories_dict.items())])}
        </div>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)