#!/usr/bin/env python3
"""
Business Directory Service - Port 8004
Provides comprehensive business listing and directory management APIs
"""

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
import uvicorn
import json
from datetime import datetime
import uuid

app = FastAPI(
    title="Business Directory Service",
    description="Comprehensive business listing and directory management",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample business data
SAMPLE_BUSINESSES = [
    {
        "id": "biz_001",
        "name": "Bizoholic Marketing Agency",
        "category": "Marketing",
        "subcategory": "Digital Marketing",
        "description": "Full-service digital marketing agency specializing in AI-powered marketing automation",
        "address": "123 Marketing St, Business City, BC 12345",
        "phone": "+1-555-MARKETING",
        "email": "hello@bizoholic.com",
        "website": "https://bizoholic.com",
        "rating": 4.8,
        "total_reviews": 127,
        "verified": True,
        "claimed": True,
        "business_hours": {
            "monday": "9:00 AM - 6:00 PM",
            "tuesday": "9:00 AM - 6:00 PM",
            "wednesday": "9:00 AM - 6:00 PM",
            "thursday": "9:00 AM - 6:00 PM",
            "friday": "9:00 AM - 6:00 PM",
            "saturday": "Closed",
            "sunday": "Closed"
        },
        "social_media": {
            "facebook": "https://facebook.com/bizoholic",
            "twitter": "https://twitter.com/bizoholic",
            "linkedin": "https://linkedin.com/company/bizoholic"
        },
        "images": [
            "https://bizoholic.com/images/office1.jpg",
            "https://bizoholic.com/images/team.jpg"
        ],
        "services": ["SEO", "PPC", "Social Media Marketing", "Content Marketing", "Email Marketing"],
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-09-20T14:22:00Z"
    },
    {
        "id": "biz_002",
        "name": "CorelDove E-commerce Solutions",
        "category": "E-commerce",
        "subcategory": "Platform Development",
        "description": "Custom e-commerce platform development and optimization services",
        "address": "456 Commerce Ave, Trade District, TD 67890",
        "phone": "+1-555-ECOMMERCE",
        "email": "contact@coreldove.com",
        "website": "https://coreldove.com",
        "rating": 4.9,
        "total_reviews": 89,
        "verified": True,
        "claimed": True,
        "business_hours": {
            "monday": "8:00 AM - 7:00 PM",
            "tuesday": "8:00 AM - 7:00 PM",
            "wednesday": "8:00 AM - 7:00 PM",
            "thursday": "8:00 AM - 7:00 PM",
            "friday": "8:00 AM - 7:00 PM",
            "saturday": "10:00 AM - 4:00 PM",
            "sunday": "Closed"
        },
        "social_media": {
            "facebook": "https://facebook.com/coreldove",
            "linkedin": "https://linkedin.com/company/coreldove"
        },
        "images": [
            "https://coreldove.com/images/showcase1.jpg"
        ],
        "services": ["Shopify Development", "WooCommerce", "Custom E-commerce", "Platform Migration"],
        "created_at": "2024-02-10T09:15:00Z",
        "updated_at": "2024-09-21T11:45:00Z"
    },
    {
        "id": "biz_003",
        "name": "TechStart Innovations",
        "category": "Technology",
        "subcategory": "Software Development",
        "description": "Innovative software solutions for startups and enterprises",
        "address": "789 Innovation Blvd, Tech Park, TP 13579",
        "phone": "+1-555-TECHSTART",
        "email": "info@techstart.com",
        "website": "https://techstart.com",
        "rating": 4.6,
        "total_reviews": 156,
        "verified": True,
        "claimed": False,
        "business_hours": {
            "monday": "9:00 AM - 8:00 PM",
            "tuesday": "9:00 AM - 8:00 PM",
            "wednesday": "9:00 AM - 8:00 PM",
            "thursday": "9:00 AM - 8:00 PM",
            "friday": "9:00 AM - 6:00 PM",
            "saturday": "Closed",
            "sunday": "Closed"
        },
        "social_media": {
            "linkedin": "https://linkedin.com/company/techstart",
            "twitter": "https://twitter.com/techstart"
        },
        "images": [],
        "services": ["Web Development", "Mobile Apps", "AI Integration", "Cloud Solutions"],
        "created_at": "2024-03-05T16:20:00Z",
        "updated_at": "2024-09-18T13:30:00Z"
    }
]

BUSINESS_CATEGORIES = [
    {
        "id": "cat_marketing",
        "name": "Marketing",
        "description": "Marketing and advertising services",
        "subcategories": [
            {"id": "subcat_digital", "name": "Digital Marketing"},
            {"id": "subcat_traditional", "name": "Traditional Marketing"},
            {"id": "subcat_social", "name": "Social Media Marketing"}
        ],
        "business_count": 45
    },
    {
        "id": "cat_ecommerce",
        "name": "E-commerce",
        "description": "Online retail and e-commerce services",
        "subcategories": [
            {"id": "subcat_platform", "name": "Platform Development"},
            {"id": "subcat_design", "name": "Store Design"},
            {"id": "subcat_optimization", "name": "Conversion Optimization"}
        ],
        "business_count": 32
    },
    {
        "id": "cat_technology",
        "name": "Technology",
        "description": "Technology and software services",
        "subcategories": [
            {"id": "subcat_software", "name": "Software Development"},
            {"id": "subcat_web", "name": "Web Development"},
            {"id": "subcat_mobile", "name": "Mobile Development"}
        ],
        "business_count": 78
    }
]

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "business-directory-service",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "port": 8004
    }

# Business listing endpoints
@app.get("/api/brain/business-directory/businesses")
async def get_businesses(
    query: Optional[str] = None,
    category: Optional[str] = None,
    location: Optional[str] = None,
    verified: Optional[bool] = None,
    page: int = 1,
    size: int = 20
):
    """Get business listings with optional filtering"""
    try:
        filtered_businesses = SAMPLE_BUSINESSES.copy()
        
        # Apply filters
        if query:
            filtered_businesses = [
                b for b in filtered_businesses 
                if query.lower() in b["name"].lower() or query.lower() in b["description"].lower()
            ]
        
        if category:
            filtered_businesses = [
                b for b in filtered_businesses 
                if b["category"].lower() == category.lower()
            ]
        
        if verified is not None:
            filtered_businesses = [
                b for b in filtered_businesses 
                if b["verified"] == verified
            ]
        
        # Pagination
        start_idx = (page - 1) * size
        end_idx = start_idx + size
        paginated_businesses = filtered_businesses[start_idx:end_idx]
        
        return {
            "businesses": paginated_businesses,
            "total": len(filtered_businesses),
            "page": page,
            "size": size,
            "total_pages": (len(filtered_businesses) + size - 1) // size
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch businesses: {str(e)}")

@app.post("/api/brain/business-directory/businesses")
async def create_business(business_data: dict):
    """Create a new business listing"""
    try:
        new_business = {
            "id": f"biz_{uuid.uuid4().hex[:8]}",
            "name": business_data.get("name", ""),
            "category": business_data.get("category", ""),
            "subcategory": business_data.get("subcategory", ""),
            "description": business_data.get("description", ""),
            "address": business_data.get("address", ""),
            "phone": business_data.get("phone", ""),
            "email": business_data.get("email", ""),
            "website": business_data.get("website", ""),
            "rating": 0.0,
            "total_reviews": 0,
            "verified": False,
            "claimed": False,
            "business_hours": business_data.get("business_hours", {}),
            "social_media": business_data.get("social_media", {}),
            "images": business_data.get("images", []),
            "services": business_data.get("services", []),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # In a real implementation, save to database
        SAMPLE_BUSINESSES.append(new_business)
        
        return {
            "message": "Business created successfully",
            "business_id": new_business["id"],
            "business": new_business
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create business: {str(e)}")

@app.get("/api/brain/business-directory/businesses/{business_id}")
async def get_business_details(business_id: str):
    """Get detailed information about a specific business"""
    try:
        business = next((b for b in SAMPLE_BUSINESSES if b["id"] == business_id), None)
        if not business:
            raise HTTPException(status_code=404, detail="Business not found")
        
        return {
            "business": business,
            "similar_businesses": [
                b for b in SAMPLE_BUSINESSES 
                if b["category"] == business["category"] and b["id"] != business_id
            ][:3]
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch business details: {str(e)}")

@app.put("/api/brain/business-directory/businesses/{business_id}")
async def update_business(business_id: str, business_data: dict):
    """Update business information"""
    try:
        business_idx = next((i for i, b in enumerate(SAMPLE_BUSINESSES) if b["id"] == business_id), None)
        if business_idx is None:
            raise HTTPException(status_code=404, detail="Business not found")
        
        # Update business data
        for key, value in business_data.items():
            if key in SAMPLE_BUSINESSES[business_idx]:
                SAMPLE_BUSINESSES[business_idx][key] = value
        
        SAMPLE_BUSINESSES[business_idx]["updated_at"] = datetime.now().isoformat()
        
        return {
            "message": "Business updated successfully",
            "business": SAMPLE_BUSINESSES[business_idx]
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update business: {str(e)}")

# Category endpoints
@app.get("/api/brain/business-directory/categories")
async def get_business_categories(parent_id: Optional[str] = None):
    """Get business categories"""
    try:
        return {
            "categories": BUSINESS_CATEGORIES,
            "total": len(BUSINESS_CATEGORIES)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch categories: {str(e)}")

# Search suggestions
@app.get("/api/brain/business-directory/businesses/suggestions/autocomplete")
async def get_search_suggestions(query: str, limit: int = 5):
    """Get search suggestions for autocomplete"""
    try:
        suggestions = []
        query_lower = query.lower()
        
        # Business name suggestions
        for business in SAMPLE_BUSINESSES:
            if query_lower in business["name"].lower():
                suggestions.append({
                    "type": "business",
                    "text": business["name"],
                    "category": business["category"]
                })
        
        # Category suggestions
        for category in BUSINESS_CATEGORIES:
            if query_lower in category["name"].lower():
                suggestions.append({
                    "type": "category",
                    "text": category["name"],
                    "business_count": category["business_count"]
                })
        
        return {
            "suggestions": suggestions[:limit],
            "query": query
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch suggestions: {str(e)}")

# Analytics endpoint
@app.get("/api/brain/business-directory/businesses/{business_id}/analytics")
async def get_business_analytics(business_id: str, period: str = "30d"):
    """Get analytics for a specific business"""
    try:
        business = next((b for b in SAMPLE_BUSINESSES if b["id"] == business_id), None)
        if not business:
            raise HTTPException(status_code=404, detail="Business not found")
        
        # Mock analytics data
        return {
            "business_id": business_id,
            "period": period,
            "views": {
                "total": 1250,
                "unique": 890,
                "growth": 15.2
            },
            "contact_actions": {
                "phone_calls": 45,
                "website_clicks": 123,
                "email_contacts": 28,
                "direction_requests": 67
            },
            "review_stats": {
                "new_reviews": 8,
                "average_rating": business["rating"],
                "review_trend": "positive"
            },
            "search_keywords": [
                {"keyword": "digital marketing", "impressions": 340},
                {"keyword": "marketing agency", "impressions": 280},
                {"keyword": "bizoholic", "impressions": 190}
            ]
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch analytics: {str(e)}")

# Main entry point
if __name__ == "__main__":
    print("🚀 Starting Business Directory Service on port 8004...")
    print("📊 Service provides comprehensive business directory management")
    print("🔗 Integrates with FastAPI Brain Gateway on port 8001")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8004,
        log_level="info"
    )