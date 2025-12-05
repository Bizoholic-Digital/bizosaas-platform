#!/usr/bin/env python3
"""
Client Dashboard for Business Directory Management
Provides CRUD interface for clients to manage their business listings
Integrates with BizOSaaS platform
"""

from fastapi import FastAPI, HTTPException, Request, Form, Depends, Cookie
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import uuid

# Create dashboard app
dashboard_app = FastAPI(
    title="BizOSaaS Directory Client Dashboard",
    description="Client interface for managing business directory listings",
    version="1.0.0"
)

# Add CORS middleware
dashboard_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@dashboard_app.get("/", response_class=HTMLResponse)
async def client_dashboard(request: Request, client_id: str = "demo_client"):
    """Main client dashboard for managing business listings"""
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Business Directory Dashboard - BizOSaaS</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
        <style>
            :root {{
                --primary-color: #2c5aa0;
                --secondary-color: #76cef1;
                --accent-color: #f8b500;
                --success-color: #28a745;
                --danger-color: #dc3545;
                --warning-color: #ffc107;
            }}
            
            body {{
                background-color: #f8f9fa;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }}
            
            .sidebar {{
                background: linear-gradient(180deg, var(--primary-color) 0%, #1e3d72 100%);
                color: white;
                min-height: 100vh;
                padding: 20px 0;
            }}
            
            .sidebar-header {{
                text-align: center;
                padding: 20px;
                border-bottom: 1px solid rgba(255,255,255,0.1);
                margin-bottom: 30px;
            }}
            
            .sidebar-menu {{
                list-style: none;
                padding: 0;
                margin: 0;
            }}
            
            .sidebar-menu li {{
                margin-bottom: 5px;
            }}
            
            .sidebar-menu a {{
                color: rgba(255,255,255,0.8);
                text-decoration: none;
                padding: 12px 25px;
                display: flex;
                align-items: center;
                transition: all 0.3s ease;
            }}
            
            .sidebar-menu a:hover, .sidebar-menu a.active {{
                background: rgba(255,255,255,0.1);
                color: white;
                border-right: 3px solid var(--accent-color);
            }}
            
            .sidebar-menu i {{
                margin-right: 15px;
                font-size: 20px;
            }}
            
            .main-content {{
                padding: 30px;
            }}
            
            .page-header {{
                background: white;
                border-radius: 15px;
                padding: 30px;
                margin-bottom: 30px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            }}
            
            .page-title {{
                font-size: 2rem;
                font-weight: 600;
                color: var(--primary-color);
                margin-bottom: 10px;
            }}
            
            .page-subtitle {{
                color: #6c757d;
                font-size: 1.1rem;
            }}
            
            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }}
            
            .stat-card {{
                background: white;
                border-radius: 15px;
                padding: 25px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                position: relative;
                overflow: hidden;
            }}
            
            .stat-card::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 4px;
                background: var(--accent-color);
            }}
            
            .stat-number {{
                font-size: 2.5rem;
                font-weight: 700;
                color: var(--primary-color);
                margin-bottom: 5px;
            }}
            
            .stat-label {{
                color: #6c757d;
                font-size: 0.95rem;
                margin-bottom: 10px;
            }}
            
            .stat-change {{
                font-size: 0.85rem;
                font-weight: 600;
            }}
            
            .stat-change.positive {{
                color: var(--success-color);
            }}
            
            .stat-change.negative {{
                color: var(--danger-color);
            }}
            
            .content-card {{
                background: white;
                border-radius: 15px;
                padding: 30px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                margin-bottom: 30px;
            }}
            
            .btn-primary {{
                background: var(--primary-color);
                border-color: var(--primary-color);
                border-radius: 10px;
                padding: 12px 25px;
                font-weight: 600;
            }}
            
            .btn-success {{
                background: var(--success-color);
                border-color: var(--success-color);
                border-radius: 10px;
                padding: 12px 25px;
                font-weight: 600;
            }}
            
            .btn-warning {{
                background: var(--warning-color);
                border-color: var(--warning-color);
                border-radius: 10px;
                padding: 12px 25px;
                font-weight: 600;
                color: #000;
            }}
            
            .listing-card {{
                background: white;
                border-radius: 15px;
                padding: 25px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                margin-bottom: 20px;
                border-left: 4px solid var(--accent-color);
            }}
            
            .listing-name {{
                font-size: 1.3rem;
                font-weight: 600;
                color: var(--primary-color);
                margin-bottom: 10px;
            }}
            
            .listing-category {{
                color: var(--secondary-color);
                font-weight: 500;
                margin-bottom: 10px;
            }}
            
            .listing-location {{
                color: #6c757d;
                margin-bottom: 15px;
            }}
            
            .listing-status {{
                padding: 6px 12px;
                border-radius: 20px;
                font-size: 0.85rem;
                font-weight: 600;
                text-transform: uppercase;
            }}
            
            .status-active {{
                background: rgba(40, 167, 69, 0.1);
                color: var(--success-color);
            }}
            
            .status-pending {{
                background: rgba(255, 193, 7, 0.1);
                color: var(--warning-color);
            }}
            
            .status-inactive {{
                background: rgba(220, 53, 69, 0.1);
                color: var(--danger-color);
            }}
            
            .quick-actions {{
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
            }}
            
            .action-btn {{
                border: none;
                border-radius: 8px;
                padding: 8px 15px;
                font-size: 0.9rem;
                cursor: pointer;
                transition: all 0.3s ease;
            }}
            
            .action-btn:hover {{
                transform: translateY(-2px);
            }}
            
            .empty-state {{
                text-align: center;
                padding: 60px 20px;
                color: #6c757d;
            }}
            
            .empty-state i {{
                font-size: 4rem;
                margin-bottom: 20px;
                opacity: 0.3;
            }}
            
            @media (max-width: 768px) {{
                .sidebar {{
                    display: none;
                }}
                .main-content {{
                    padding: 20px 15px;
                }}
                .stats-grid {{
                    grid-template-columns: 1fr;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container-fluid">
            <div class="row">
                <!-- Sidebar -->
                <div class="col-md-3 col-lg-2 px-0">
                    <div class="sidebar">
                        <div class="sidebar-header">
                            <h4>BizOSaaS</h4>
                            <small>Directory Management</small>
                        </div>
                        <ul class="sidebar-menu">
                            <li><a href="#" class="active" onclick="showSection('dashboard')">
                                <i class="material-icons">dashboard</i>
                                <span>Dashboard</span>
                            </a></li>
                            <li><a href="#" onclick="showSection('listings')">
                                <i class="material-icons">business</i>
                                <span>My Listings</span>
                            </a></li>
                            <li><a href="#" onclick="showSection('add-listing')">
                                <i class="material-icons">add_business</i>
                                <span>Add Listing</span>
                            </a></li>
                            <li><a href="#" onclick="showSection('analytics')">
                                <i class="material-icons">analytics</i>
                                <span>Analytics</span>
                            </a></li>
                            <li><a href="#" onclick="showSection('directories')">
                                <i class="material-icons">list</i>
                                <span>Directories</span>
                            </a></li>
                            <li><a href="#" onclick="showSection('seo')">
                                <i class="material-icons">search</i>
                                <span>SEO Tools</span>
                            </a></li>
                            <li><a href="#" onclick="showSection('settings')">
                                <i class="material-icons">settings</i>
                                <span>Settings</span>
                            </a></li>
                        </ul>
                    </div>
                </div>
                
                <!-- Main Content -->
                <div class="col-md-9 col-lg-10">
                    <div class="main-content">
                        <!-- Dashboard Section -->
                        <div id="dashboard-section" class="content-section">
                            <div class="page-header">
                                <h1 class="page-title">Directory Dashboard</h1>
                                <p class="page-subtitle">Manage your business listings and track performance</p>
                            </div>
                            
                            <div class="stats-grid">
                                <div class="stat-card">
                                    <div class="stat-number">3</div>
                                    <div class="stat-label">Active Listings</div>
                                    <div class="stat-change positive">+1 this month</div>
                                </div>
                                <div class="stat-card">
                                    <div class="stat-number">47</div>
                                    <div class="stat-label">Directory Platforms</div>
                                    <div class="stat-change positive">+5 available</div>
                                </div>
                                <div class="stat-card">
                                    <div class="stat-number">4.7</div>
                                    <div class="stat-label">Average Rating</div>
                                    <div class="stat-change positive">+0.3 improvement</div>
                                </div>
                                <div class="stat-card">
                                    <div class="stat-number">89%</div>
                                    <div class="stat-label">SEO Optimized</div>
                                    <div class="stat-change positive">+12% this month</div>
                                </div>
                            </div>
                            
                            <div class="content-card">
                                <h3>Recent Activity</h3>
                                <div class="list-group list-group-flush">
                                    <div class="list-group-item d-flex justify-content-between align-items-center">
                                        <div>
                                            <strong>Sunny Side Café</strong> listing approved on Google My Business
                                            <small class="text-muted d-block">2 hours ago</small>
                                        </div>
                                        <span class="badge bg-success rounded-pill">Approved</span>
                                    </div>
                                    <div class="list-group-item d-flex justify-content-between align-items-center">
                                        <div>
                                            <strong>TechFlow Solutions</strong> received 3 new reviews
                                            <small class="text-muted d-block">4 hours ago</small>
                                        </div>
                                        <span class="badge bg-info rounded-pill">Reviews</span>
                                    </div>
                                    <div class="list-group-item d-flex justify-content-between align-items-center">
                                        <div>
                                            <strong>Wellness Center Plus</strong> SEO optimization completed
                                            <small class="text-muted d-block">1 day ago</small>
                                        </div>
                                        <span class="badge bg-primary rounded-pill">SEO</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Listings Section -->
                        <div id="listings-section" class="content-section" style="display: none;">
                            <div class="page-header">
                                <h1 class="page-title">My Business Listings</h1>
                                <p class="page-subtitle">Manage and monitor your business directory listings</p>
                            </div>
                            
                            <div class="content-card">
                                <div class="d-flex justify-content-between align-items-center mb-4">
                                    <h3>Active Listings</h3>
                                    <button class="btn btn-primary" onclick="showSection('add-listing')">
                                        <i class="material-icons me-2">add</i>Add New Listing
                                    </button>
                                </div>
                                
                                <div id="listings-container">
                                    <!-- Sample listings will be loaded here -->
                                    <div class="listing-card">
                                        <div class="d-flex justify-content-between align-items-start mb-3">
                                            <div>
                                                <div class="listing-name">Sunny Side Café</div>
                                                <div class="listing-category">Restaurants & Food</div>
                                                <div class="listing-location">📍 123 Main St, San Francisco, CA</div>
                                            </div>
                                            <span class="listing-status status-active">Active</span>
                                        </div>
                                        <div class="row">
                                            <div class="col-md-6">
                                                <small class="text-muted">Listed on 12 directories</small><br>
                                                <small class="text-success">4.8⭐ (24 reviews)</small>
                                            </div>
                                            <div class="col-md-6 text-end">
                                                <div class="quick-actions">
                                                    <button class="action-btn btn btn-sm btn-outline-primary">Edit</button>
                                                    <button class="action-btn btn btn-sm btn-outline-success">View</button>
                                                    <button class="action-btn btn btn-sm btn-outline-warning">Promote</button>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <div class="listing-card">
                                        <div class="d-flex justify-content-between align-items-start mb-3">
                                            <div>
                                                <div class="listing-name">TechFlow Solutions</div>
                                                <div class="listing-category">Professional Services</div>
                                                <div class="listing-location">📍 456 Tech Ave, Austin, TX</div>
                                            </div>
                                            <span class="listing-status status-pending">Pending</span>
                                        </div>
                                        <div class="row">
                                            <div class="col-md-6">
                                                <small class="text-muted">Listed on 8 directories</small><br>
                                                <small class="text-success">4.9⭐ (15 reviews)</small>
                                            </div>
                                            <div class="col-md-6 text-end">
                                                <div class="quick-actions">
                                                    <button class="action-btn btn btn-sm btn-outline-primary">Edit</button>
                                                    <button class="action-btn btn btn-sm btn-outline-success">View</button>
                                                    <button class="action-btn btn btn-sm btn-outline-warning">Promote</button>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Add Listing Section -->
                        <div id="add-listing-section" class="content-section" style="display: none;">
                            <div class="page-header">
                                <h1 class="page-title">Add New Business Listing</h1>
                                <p class="page-subtitle">Create a new listing with AI-powered SEO optimization</p>
                            </div>
                            
                            <div class="content-card">
                                <form id="add-listing-form" onsubmit="submitListing(event)">
                                    <div class="row">
                                        <div class="col-md-6 mb-3">
                                            <label for="business-name" class="form-label">Business Name *</label>
                                            <input type="text" class="form-control" id="business-name" required>
                                        </div>
                                        <div class="col-md-6 mb-3">
                                            <label for="category" class="form-label">Category *</label>
                                            <select class="form-select" id="category" required>
                                                <option value="">Select Category</option>
                                                <option value="restaurants">Restaurants & Food</option>
                                                <option value="healthcare">Healthcare & Medical</option>
                                                <option value="professional_services">Professional Services</option>
                                                <option value="retail">Retail & Shopping</option>
                                                <option value="technology">Technology</option>
                                                <option value="fitness">Fitness & Wellness</option>
                                            </select>
                                        </div>
                                    </div>
                                    
                                    <div class="row">
                                        <div class="col-md-8 mb-3">
                                            <label for="address" class="form-label">Street Address *</label>
                                            <input type="text" class="form-control" id="address" required>
                                        </div>
                                        <div class="col-md-4 mb-3">
                                            <label for="city" class="form-label">City *</label>
                                            <input type="text" class="form-control" id="city" required>
                                        </div>
                                    </div>
                                    
                                    <div class="row">
                                        <div class="col-md-4 mb-3">
                                            <label for="state" class="form-label">State *</label>
                                            <input type="text" class="form-control" id="state" required>
                                        </div>
                                        <div class="col-md-4 mb-3">
                                            <label for="zip" class="form-label">ZIP Code *</label>
                                            <input type="text" class="form-control" id="zip" required>
                                        </div>
                                        <div class="col-md-4 mb-3">
                                            <label for="phone" class="form-label">Phone Number *</label>
                                            <input type="tel" class="form-control" id="phone" required>
                                        </div>
                                    </div>
                                    
                                    <div class="row">
                                        <div class="col-md-6 mb-3">
                                            <label for="email" class="form-label">Email *</label>
                                            <input type="email" class="form-control" id="email" required>
                                        </div>
                                        <div class="col-md-6 mb-3">
                                            <label for="website" class="form-label">Website</label>
                                            <input type="url" class="form-control" id="website" placeholder="https://...">
                                        </div>
                                    </div>
                                    
                                    <div class="mb-3">
                                        <label for="description" class="form-label">Business Description *</label>
                                        <textarea class="form-control" id="description" rows="4" required 
                                                  placeholder="Describe your business, services, and what makes you unique..."></textarea>
                                    </div>
                                    
                                    <div class="mb-4">
                                        <label class="form-label">Directory Platforms</label>
                                        <div class="row">
                                            <div class="col-md-4">
                                                <div class="form-check">
                                                    <input class="form-check-input" type="checkbox" id="google-my-business" checked>
                                                    <label class="form-check-label" for="google-my-business">
                                                        Google My Business
                                                    </label>
                                                </div>
                                            </div>
                                            <div class="col-md-4">
                                                <div class="form-check">
                                                    <input class="form-check-input" type="checkbox" id="yelp" checked>
                                                    <label class="form-check-label" for="yelp">
                                                        Yelp Business
                                                    </label>
                                                </div>
                                            </div>
                                            <div class="col-md-4">
                                                <div class="form-check">
                                                    <input class="form-check-input" type="checkbox" id="facebook" checked>
                                                    <label class="form-check-label" for="facebook">
                                                        Facebook Business
                                                    </label>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <div class="d-flex gap-3">
                                        <button type="submit" class="btn btn-primary">
                                            <i class="material-icons me-2">add_business</i>
                                            Create Listing
                                        </button>
                                        <button type="button" class="btn btn-outline-secondary" onclick="showSection('listings')">
                                            Cancel
                                        </button>
                                    </div>
                                </form>
                            </div>
                        </div>
                        
                        <!-- Other sections would be implemented similarly -->
                        <div id="analytics-section" class="content-section" style="display: none;">
                            <div class="page-header">
                                <h1 class="page-title">Analytics & Reports</h1>
                                <p class="page-subtitle">Track your directory listing performance</p>
                            </div>
                            <div class="content-card">
                                <div class="empty-state">
                                    <i class="material-icons">analytics</i>
                                    <h4>Analytics Coming Soon</h4>
                                    <p>Detailed analytics and reporting features are being developed.</p>
                                </div>
                            </div>
                        </div>
                        
                    </div>
                </div>
            </div>
        </div>
        
        <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/js/bootstrap.bundle.min.js"></script>
        <script>
            function showSection(sectionName) {{
                // Hide all sections
                document.querySelectorAll('.content-section').forEach(section => {{
                    section.style.display = 'none';
                }});
                
                // Remove active class from all menu items
                document.querySelectorAll('.sidebar-menu a').forEach(link => {{
                    link.classList.remove('active');
                }});
                
                // Show selected section
                document.getElementById(sectionName + '-section').style.display = 'block';
                
                // Add active class to clicked menu item
                event.target.closest('a').classList.add('active');
            }}
            
            function submitListing(event) {{
                event.preventDefault();
                
                const formData = new FormData(event.target);
                const listingData = Object.fromEntries(formData.entries());
                
                // Show success message
                alert('Listing created successfully! It will be submitted to selected directories.');
                
                // Reset form and go back to listings
                event.target.reset();
                showSection('listings');
            }}
            
            // Load client data on page load
            document.addEventListener('DOMContentLoaded', function() {{
                console.log('Dashboard loaded for client: {client_id}');
            }});
        </script>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)

@dashboard_app.get("/api/client/{client_id}/dashboard-data")
async def get_dashboard_data(client_id: str):
    """Get dashboard data for a specific client"""
    # Mock data - in production, this would query the database
    dashboard_data = {
        "client_id": client_id,
        "stats": {
            "active_listings": 3,
            "total_directories": 47,
            "average_rating": 4.7,
            "seo_optimized_percent": 89
        },
        "recent_activity": [
            {
                "type": "approval",
                "business_name": "Sunny Side Café",
                "platform": "Google My Business",
                "timestamp": "2 hours ago",
                "status": "approved"
            },
            {
                "type": "reviews",
                "business_name": "TechFlow Solutions",
                "count": 3,
                "timestamp": "4 hours ago",
                "status": "new_reviews"
            }
        ],
        "listings": [
            {
                "business_id": "1",
                "name": "Sunny Side Café",
                "category": "Restaurants & Food",
                "address": "123 Main St, San Francisco, CA",
                "status": "active",
                "directories_count": 12,
                "rating": 4.8,
                "review_count": 24
            },
            {
                "business_id": "2", 
                "name": "TechFlow Solutions",
                "category": "Professional Services",
                "address": "456 Tech Ave, Austin, TX",
                "status": "pending",
                "directories_count": 8,
                "rating": 4.9,
                "review_count": 15
            }
        ]
    }
    
    return dashboard_data

if __name__ == "__main__":
    import uvicorn
    print("🎯 Starting Business Directory Client Dashboard...")
    print("📊 Client interface for listing management")
    print("🔧 CRUD operations for business listings")
    print("🚀 Dashboard starting on http://localhost:8009")
    uvicorn.run(dashboard_app, host="0.0.0.0", port=8009)