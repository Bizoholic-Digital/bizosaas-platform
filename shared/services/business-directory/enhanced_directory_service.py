#!/usr/bin/env python3
"""
Enhanced Business Directory Service
Integrates bizbook professional template with BizOSaaS platform
Provides client CRUD operations and SEO benefits
"""

from fastapi import FastAPI, HTTPException, Request, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timedelta
import asyncio
import os
import json
import uuid
from dataclasses import dataclass, asdict
from pydantic import BaseModel
from pathlib import Path

# Create FastAPI app with professional directory features
app = FastAPI(
    title="BizOSaaS Enhanced Business Directory",
    description="Professional business directory with client management, SEO optimization, and AI integration",
    version="3.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup templates and static files
templates = Jinja2Templates(directory="templates")
os.makedirs("templates", exist_ok=True)
os.makedirs("static", exist_ok=True)

# Mount static files for CSS, JS, Images
app.mount("/static", StaticFiles(directory="static"), name="static")

# Data Models
class BusinessListing(BaseModel):
    business_id: str
    client_id: str  # Links to BizOSaaS client
    name: str
    category: str
    subcategory: Optional[str] = None
    address: str
    city: str
    state: str
    zip_code: str
    country: str = "United States"
    phone: str
    email: str
    website: str
    description: str
    long_description: Optional[str] = None
    features: List[str] = []
    rating: float = 0.0
    review_count: int = 0
    verification_status: str = "pending"  # pending, verified, premium
    premium_status: str = "free"  # free, basic, premium, enterprise
    ai_enhanced: bool = False
    seo_optimized: bool = False
    social_links: Dict[str, str] = {}
    business_hours: Dict[str, str] = {}
    images: List[str] = []
    featured_image: Optional[str] = None
    tags: List[str] = []
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    published: bool = True

class DirectoryPlatform(BaseModel):
    platform_id: str
    name: str
    category: str
    priority: str  # critical, high, medium, low
    auto_submit: bool = False
    submission_cost: float = 0.0
    api_available: bool = False
    industries: List[str] = []
    location_specific: bool = False
    verification_required: bool = False
    premium_features: Dict[str, Any] = {}

class ClientDirectoryAccess(BaseModel):
    client_id: str
    access_level: str  # admin, editor, viewer
    allowed_operations: List[str] = []  # create, read, update, delete, publish
    directory_quota: int = 10  # Max listings per client
    premium_features: bool = False

# Enhanced Directory Service
class EnhancedDirectoryService:
    """Enhanced business directory service with client management and SEO optimization"""
    
    def __init__(self):
        self.directory_platforms = self._initialize_enhanced_platforms()
        self.business_categories = self._initialize_enhanced_categories()
        self.client_listings = {}  # In production, this would be a database
        self.directory_submissions = {}
        self.seo_templates = self._initialize_seo_templates()
        
    def _initialize_enhanced_platforms(self) -> List[DirectoryPlatform]:
        """Initialize comprehensive directory platforms with enhanced features"""
        return [
            # Critical SEO Directories
            DirectoryPlatform(
                platform_id="google_my_business",
                name="Google My Business",
                category="search_maps",
                priority="critical",
                auto_submit=True,
                api_available=True,
                industries=["all"],
                verification_required=True,
                premium_features={
                    "google_posts": True,
                    "messaging": True,
                    "insights": True,
                    "website_builder": True
                }
            ),
            DirectoryPlatform(
                platform_id="bing_places",
                name="Bing Places for Business",
                category="search_maps",
                priority="high",
                auto_submit=True,
                api_available=True,
                industries=["all"],
                premium_features={
                    "enhanced_listings": True,
                    "analytics": True
                }
            ),
            DirectoryPlatform(
                platform_id="apple_maps",
                name="Apple Maps Connect",
                category="search_maps",
                priority="high",
                auto_submit=True,
                industries=["all"],
                location_specific=True
            ),
            DirectoryPlatform(
                platform_id="yelp",
                name="Yelp Business",
                category="reviews",
                priority="critical",
                auto_submit=True,
                api_available=True,
                industries=["restaurants", "services", "retail", "healthcare"],
                premium_features={
                    "ads": True,
                    "enhanced_profile": True,
                    "customer_messaging": True,
                    "analytics": True
                }
            ),
            DirectoryPlatform(
                platform_id="facebook_business",
                name="Facebook Business Profile",
                category="social",
                priority="critical",
                auto_submit=True,
                api_available=True,
                industries=["all"],
                premium_features={
                    "ads": True,
                    "instagram_integration": True,
                    "messenger": True,
                    "insights": True
                }
            ),
            # Industry-Specific High-Value Directories
            DirectoryPlatform(
                platform_id="tripadvisor",
                name="TripAdvisor Business",
                category="hospitality",
                priority="critical",
                industries=["restaurants", "hotels", "travel", "attractions"],
                premium_features={
                    "ads": True,
                    "enhanced_listing": True,
                    "management_center": True
                }
            ),
            DirectoryPlatform(
                platform_id="healthgrades",
                name="Healthgrades",
                category="healthcare",
                priority="critical",
                industries=["healthcare", "medical"],
                verification_required=True,
                premium_features={
                    "patient_reviews": True,
                    "appointment_booking": True,
                    "profile_enhancement": True
                }
            ),
            # Additional 50+ platforms would be here...
        ]
    
    def _initialize_enhanced_categories(self) -> List[Dict[str, Any]]:
        """Initialize enhanced business categories with SEO data"""
        return [
            {
                "id": "restaurants",
                "name": "Restaurants & Food",
                "icon": "🍽️",
                "count": 2847,
                "seo_keywords": ["restaurant", "food", "dining", "cuisine", "delivery"],
                "subcategories": [
                    {"id": "fine_dining", "name": "Fine Dining", "count": 234},
                    {"id": "fast_food", "name": "Fast Food", "count": 892},
                    {"id": "cafes", "name": "Cafes & Coffee", "count": 445},
                    {"id": "bars_pubs", "name": "Bars & Pubs", "count": 356},
                    {"id": "catering", "name": "Catering Services", "count": 178}
                ],
                "directory_priority": ["google_my_business", "yelp", "tripadvisor", "facebook_business"],
                "seo_schema": "Restaurant"
            },
            {
                "id": "healthcare",
                "name": "Healthcare & Medical",
                "icon": "🏥",
                "count": 892,
                "seo_keywords": ["doctor", "medical", "healthcare", "clinic", "hospital"],
                "subcategories": [
                    {"id": "doctors", "name": "Doctors & Physicians", "count": 445},
                    {"id": "dentists", "name": "Dentists", "count": 178},
                    {"id": "specialists", "name": "Medical Specialists", "count": 123},
                    {"id": "clinics", "name": "Clinics & Medical Centers", "count": 89},
                    {"id": "pharmacies", "name": "Pharmacies", "count": 57}
                ],
                "directory_priority": ["google_my_business", "healthgrades", "yelp", "facebook_business"],
                "seo_schema": "MedicalOrganization"
            },
            {
                "id": "professional_services",
                "name": "Professional Services",
                "icon": "🔧",
                "count": 3156,
                "seo_keywords": ["services", "professional", "business", "consultant", "expert"],
                "subcategories": [
                    {"id": "legal", "name": "Legal Services", "count": 567},
                    {"id": "accounting", "name": "Accounting & Finance", "count": 445},
                    {"id": "consulting", "name": "Business Consulting", "count": 389},
                    {"id": "marketing", "name": "Marketing & Advertising", "count": 278},
                    {"id": "it_services", "name": "IT & Technology", "count": 445}
                ],
                "directory_priority": ["google_my_business", "yelp", "linkedin", "facebook_business"],
                "seo_schema": "ProfessionalService"
            }
        ]
    
    def _initialize_seo_templates(self) -> Dict[str, str]:
        """Initialize SEO-optimized templates for different business types"""
        return {
            "meta_title": "{business_name} - {category} in {city}, {state} | BizOSaaS Directory",
            "meta_description": "Find {business_name}, a top-rated {category} in {city}, {state}. Contact info, reviews, hours, and directions. Part of BizOSaaS Business Directory.",
            "h1_template": "{business_name} - {category} in {city}",
            "schema_template": {
                "@context": "https://schema.org",
                "@type": "LocalBusiness",
                "name": "{business_name}",
                "description": "{description}",
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": "{address}",
                    "addressLocality": "{city}",
                    "addressRegion": "{state}",
                    "postalCode": "{zip_code}",
                    "addressCountry": "{country}"
                },
                "telephone": "{phone}",
                "url": "{website}",
                "aggregateRating": {
                    "@type": "AggregateRating",
                    "ratingValue": "{rating}",
                    "reviewCount": "{review_count}"
                }
            }
        }
    
    async def create_business_listing(self, client_id: str, listing_data: Dict[str, Any]) -> BusinessListing:
        """Create a new business listing for a client"""
        business_id = str(uuid.uuid4())
        
        # Create business listing with SEO optimization
        listing = BusinessListing(
            business_id=business_id,
            client_id=client_id,
            **listing_data,
            ai_enhanced=True,  # Auto-enable AI enhancement
            seo_optimized=True,  # Auto-enable SEO optimization
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Store listing (in production, save to database)
        if client_id not in self.client_listings:
            self.client_listings[client_id] = []
        
        self.client_listings[client_id].append(listing)
        
        # Auto-generate SEO content
        await self._optimize_listing_seo(listing)
        
        # Submit to high-priority directories
        await self._auto_submit_to_directories(listing)
        
        return listing
    
    async def get_client_listings(self, client_id: str) -> List[BusinessListing]:
        """Get all business listings for a client"""
        return self.client_listings.get(client_id, [])
    
    async def update_business_listing(self, client_id: str, business_id: str, update_data: Dict[str, Any]) -> BusinessListing:
        """Update a business listing"""
        listings = self.client_listings.get(client_id, [])
        
        for i, listing in enumerate(listings):
            if listing.business_id == business_id:
                # Update listing data
                for key, value in update_data.items():
                    if hasattr(listing, key):
                        setattr(listing, key, value)
                
                listing.updated_at = datetime.utcnow()
                
                # Re-optimize SEO
                await self._optimize_listing_seo(listing)
                
                return listing
        
        raise HTTPException(status_code=404, detail="Business listing not found")
    
    async def delete_business_listing(self, client_id: str, business_id: str) -> bool:
        """Delete a business listing"""
        listings = self.client_listings.get(client_id, [])
        
        for i, listing in enumerate(listings):
            if listing.business_id == business_id:
                del self.client_listings[client_id][i]
                return True
        
        raise HTTPException(status_code=404, detail="Business listing not found")
    
    async def _optimize_listing_seo(self, listing: BusinessListing):
        """Apply SEO optimization to a business listing"""
        # Generate SEO-optimized content
        category = next((cat for cat in self.business_categories if cat["id"] == listing.category), {})
        
        if category:
            # Add SEO keywords to description if not already present
            seo_keywords = category.get("seo_keywords", [])
            for keyword in seo_keywords[:3]:  # Top 3 keywords
                if keyword.lower() not in listing.description.lower():
                    listing.description += f" {keyword.title()}"
            
            # Generate meta tags
            # Generate meta tags (would be stored in separate SEO table in production)
            seo_meta_title = self.seo_templates["meta_title"].format(
                business_name=listing.name,
                category=category["name"],
                city=listing.city,
                state=listing.state
            )
            
            seo_meta_description = self.seo_templates["meta_description"].format(
                business_name=listing.name,
                category=category["name"],
                city=listing.city,
                state=listing.state
            )
            
            # In production, these would be stored in a separate SEO optimization table
            print(f"SEO Title: {seo_meta_title}")
            print(f"SEO Description: {seo_meta_description}")
        
        listing.seo_optimized = True
        listing.updated_at = datetime.utcnow()
    
    async def _auto_submit_to_directories(self, listing: BusinessListing):
        """Auto-submit business to high-priority directories"""
        category = next((cat for cat in self.business_categories if cat["id"] == listing.category), {})
        
        if category:
            priority_directories = category.get("directory_priority", [])
            
            # Submit to top 3 priority directories
            for platform_id in priority_directories[:3]:
                platform = next((p for p in self.directory_platforms if p.platform_id == platform_id), None)
                
                if platform and platform.auto_submit:
                    # Simulate directory submission
                    submission_id = str(uuid.uuid4())
                    self.directory_submissions[submission_id] = {
                        "business_id": listing.business_id,
                        "platform_id": platform_id,
                        "status": "submitted",
                        "submitted_at": datetime.utcnow(),
                        "estimated_approval": datetime.utcnow() + timedelta(days=3)
                    }

# Initialize service
directory_service = EnhancedDirectoryService()

# API Endpoints
@app.get("/", response_class=HTMLResponse)
async def directory_homepage(request: Request):
    """Professional directory homepage with bizbook template styling"""
    
    # Get statistics
    total_listings = sum(len(listings) for listings in directory_service.client_listings.values())
    total_categories = len(directory_service.business_categories)
    total_platforms = len(directory_service.directory_platforms)
    
    # Featured businesses (mock data for demonstration)
    featured_businesses = [
        {
            "name": "Sunny Side Café",
            "category": "Restaurants & Food",
            "city": "San Francisco",
            "rating": 4.8,
            "image": "/static/images/cafe-sample.jpg",
            "verified": True
        },
        {
            "name": "TechFlow Solutions",
            "category": "Professional Services",
            "city": "Austin",
            "rating": 4.9,
            "image": "/static/images/tech-sample.jpg",
            "verified": True
        },
        {
            "name": "Wellness Center Plus",
            "category": "Healthcare & Medical",
            "city": "Denver",
            "rating": 4.7,
            "image": "/static/images/health-sample.jpg",
            "verified": True
        }
    ]
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>BizOSaaS Business Directory - Professional Directory Platform</title>
        <meta name="description" content="Find and list your business in our comprehensive directory. Professional SEO-optimized listings with AI enhancement for maximum visibility.">
        <link href="https://fonts.googleapis.com/css?family=Oswald:700|Source+Sans+Pro:300,400,600,700&display=swap" rel="stylesheet">
        <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css" rel="stylesheet">
        <style>
            :root {{
                --primary-color: #2c5aa0;
                --secondary-color: #76cef1;
                --accent-color: #f8b500;
                --text-dark: #333;
                --text-light: #666;
            }}
            
            body {{
                font-family: 'Source Sans Pro', sans-serif;
                line-height: 1.6;
                color: var(--text-dark);
            }}
            
            .hero-section {{
                background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
                color: white;
                padding: 100px 0;
                text-align: center;
            }}
            
            .hero-title {{
                font-family: 'Oswald', sans-serif;
                font-size: 3.5rem;
                font-weight: 700;
                margin-bottom: 20px;
            }}
            
            .hero-subtitle {{
                font-size: 1.3rem;
                margin-bottom: 40px;
                opacity: 0.9;
            }}
            
            .search-box {{
                background: white;
                border-radius: 50px;
                padding: 10px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.1);
                margin: 40px auto;
                max-width: 600px;
            }}
            
            .search-input {{
                border: none;
                padding: 15px 25px;
                font-size: 1.1rem;
                flex: 1;
                border-radius: 40px;
            }}
            
            .search-btn {{
                background: var(--accent-color);
                border: none;
                padding: 15px 30px;
                border-radius: 40px;
                color: white;
                font-weight: 600;
            }}
            
            .stats-section {{
                background: #f8f9fa;
                padding: 80px 0;
            }}
            
            .stat-card {{
                text-align: center;
                padding: 30px;
            }}
            
            .stat-number {{
                font-size: 3rem;
                font-weight: 700;
                color: var(--primary-color);
                display: block;
            }}
            
            .stat-label {{
                font-size: 1.1rem;
                color: var(--text-light);
                margin-top: 10px;
            }}
            
            .categories-section {{
                padding: 80px 0;
            }}
            
            .category-card {{
                background: white;
                border-radius: 15px;
                padding: 30px;
                text-align: center;
                box-shadow: 0 5px 20px rgba(0,0,0,0.08);
                transition: all 0.3s ease;
                margin-bottom: 30px;
            }}
            
            .category-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 15px 40px rgba(0,0,0,0.15);
            }}
            
            .category-icon {{
                font-size: 3rem;
                margin-bottom: 20px;
                display: block;
            }}
            
            .category-name {{
                font-size: 1.3rem;
                font-weight: 600;
                margin-bottom: 10px;
            }}
            
            .category-count {{
                color: var(--text-light);
                font-size: 1rem;
            }}
            
            .featured-section {{
                background: #f8f9fa;
                padding: 80px 0;
            }}
            
            .business-card {{
                background: white;
                border-radius: 15px;
                overflow: hidden;
                box-shadow: 0 5px 20px rgba(0,0,0,0.08);
                transition: all 0.3s ease;
            }}
            
            .business-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 15px 40px rgba(0,0,0,0.15);
            }}
            
            .business-image {{
                height: 200px;
                background: var(--secondary-color);
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 2rem;
            }}
            
            .business-info {{
                padding: 25px;
            }}
            
            .business-name {{
                font-size: 1.3rem;
                font-weight: 600;
                margin-bottom: 10px;
            }}
            
            .business-category {{
                color: var(--primary-color);
                font-size: 0.9rem;
                margin-bottom: 10px;
            }}
            
            .business-location {{
                color: var(--text-light);
                font-size: 0.9rem;
                margin-bottom: 15px;
            }}
            
            .business-rating {{
                color: var(--accent-color);
                font-weight: 600;
            }}
            
            .verified-badge {{
                background: #28a745;
                color: white;
                padding: 2px 8px;
                border-radius: 12px;
                font-size: 0.8rem;
                margin-left: 10px;
            }}
            
            .cta-section {{
                background: var(--primary-color);
                color: white;
                padding: 80px 0;
                text-align: center;
            }}
            
            .cta-title {{
                font-size: 2.5rem;
                font-weight: 700;
                margin-bottom: 20px;
            }}
            
            .cta-text {{
                font-size: 1.2rem;
                margin-bottom: 40px;
                opacity: 0.9;
            }}
            
            .cta-btn {{
                background: var(--accent-color);
                color: white;
                padding: 15px 40px;
                border: none;
                border-radius: 30px;
                font-size: 1.1rem;
                font-weight: 600;
                text-decoration: none;
                display: inline-block;
                transition: all 0.3s ease;
            }}
            
            .cta-btn:hover {{
                background: #e6a300;
                transform: translateY(-2px);
                color: white;
            }}
            
            .section-title {{
                font-size: 2.5rem;
                font-weight: 700;
                text-align: center;
                margin-bottom: 50px;
                color: var(--text-dark);
            }}
        </style>
    </head>
    <body>
        <!-- Hero Section -->
        <div class="hero-section">
            <div class="container">
                <h1 class="hero-title">Find & List Your Business</h1>
                <p class="hero-subtitle">Professional directory platform with AI-powered SEO optimization</p>
                
                <div class="search-box d-flex">
                    <input type="text" class="search-input form-control" placeholder="Search for businesses, services, or categories...">
                    <button class="search-btn">
                        <i class="material-icons">search</i> Search
                    </button>
                </div>
            </div>
        </div>
        
        <!-- Stats Section -->
        <div class="stats-section">
            <div class="container">
                <div class="row">
                    <div class="col-md-3">
                        <div class="stat-card">
                            <span class="stat-number">{total_listings:,}</span>
                            <div class="stat-label">Business Listings</div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="stat-card">
                            <span class="stat-number">{total_categories}</span>
                            <div class="stat-label">Categories</div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="stat-card">
                            <span class="stat-number">{total_platforms}</span>
                            <div class="stat-label">Directory Platforms</div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="stat-card">
                            <span class="stat-number">95%</span>
                            <div class="stat-label">SEO Success Rate</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Categories Section -->
        <div class="categories-section">
            <div class="container">
                <h2 class="section-title">Browse Categories</h2>
                <div class="row">
    """
    
    # Add category cards
    for category in directory_service.business_categories:
        html_content += f"""
                    <div class="col-md-4">
                        <div class="category-card">
                            <span class="category-icon">{category['icon']}</span>
                            <div class="category-name">{category['name']}</div>
                            <div class="category-count">{category['count']:,} businesses</div>
                        </div>
                    </div>
        """
    
    # Continue HTML
    html_content += f"""
                </div>
            </div>
        </div>
        
        <!-- Featured Businesses -->
        <div class="featured-section">
            <div class="container">
                <h2 class="section-title">Featured Businesses</h2>
                <div class="row">
    """
    
    # Add featured business cards
    for business in featured_businesses:
        verified_badge = '<span class="verified-badge">✓ Verified</span>' if business['verified'] else ''
        html_content += f"""
                    <div class="col-md-4">
                        <div class="business-card">
                            <div class="business-image">
                                🏢
                            </div>
                            <div class="business-info">
                                <div class="business-name">{business['name']}</div>
                                <div class="business-category">{business['category']}</div>
                                <div class="business-location">📍 {business['city']}</div>
                                <div class="business-rating">
                                    ⭐ {business['rating']}/5.0
                                    {verified_badge}
                                </div>
                            </div>
                        </div>
                    </div>
        """
    
    # Finish HTML
    html_content += f"""
                </div>
            </div>
        </div>
        
        <!-- CTA Section -->
        <div class="cta-section">
            <div class="container">
                <h2 class="cta-title">Ready to List Your Business?</h2>
                <p class="cta-text">Join thousands of businesses that trust our platform for SEO-optimized directory listings</p>
                <a href="/api/client/dashboard" class="cta-btn">Get Started Now</a>
            </div>
        </div>
        
        <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)

# Client API Endpoints
@app.post("/api/client/{client_id}/listings")
async def create_listing(client_id: str, listing_data: Dict[str, Any]):
    """Create a new business listing for a client"""
    try:
        listing = await directory_service.create_business_listing(client_id, listing_data)
        return {"status": "success", "business_id": listing.business_id, "message": "Business listing created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/client/{client_id}/listings")
async def get_client_listings(client_id: str):
    """Get all business listings for a client"""
    listings = await directory_service.get_client_listings(client_id)
    return {"listings": [listing.dict() for listing in listings]}

@app.put("/api/client/{client_id}/listings/{business_id}")
async def update_listing(client_id: str, business_id: str, update_data: Dict[str, Any]):
    """Update a business listing"""
    try:
        listing = await directory_service.update_business_listing(client_id, business_id, update_data)
        return {"status": "success", "message": "Business listing updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/client/{client_id}/listings/{business_id}")
async def delete_listing(client_id: str, business_id: str):
    """Delete a business listing"""
    try:
        success = await directory_service.delete_business_listing(client_id, business_id)
        return {"status": "success", "message": "Business listing deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Directory Platform Management
@app.get("/api/platforms")
async def get_directory_platforms():
    """Get all directory platforms"""
    return {"platforms": [platform.dict() for platform in directory_service.directory_platforms]}

@app.get("/api/categories")
async def get_business_categories():
    """Get all business categories"""
    return {"categories": directory_service.business_categories}

# SEO and Analytics Endpoints
@app.get("/api/client/{client_id}/seo-analysis")
async def get_seo_analysis(client_id: str):
    """Get SEO analysis for client's listings"""
    listings = await directory_service.get_client_listings(client_id)
    
    seo_stats = {
        "total_listings": len(listings),
        "seo_optimized": sum(1 for listing in listings if listing.seo_optimized),
        "avg_rating": sum(listing.rating for listing in listings) / len(listings) if listings else 0,
        "total_reviews": sum(listing.review_count for listing in listings),
        "verified_listings": sum(1 for listing in listings if listing.verification_status == "verified")
    }
    
    return {"seo_analysis": seo_stats}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "service": "Enhanced Business Directory Service",
        "version": "3.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    print("🏢 Starting Enhanced Business Directory Service...")
    print("📊 Professional directory with client management")
    print("🔍 SEO optimization and AI enhancement")
    print("🚀 Server starting on http://localhost:8008")
    uvicorn.run(app, host="0.0.0.0", port=8008)