"""
Image Integration Service for BizOSaaS Platform
Integrates with multiple image APIs for content creation and product descriptions
"""

import os
import asyncio
import httpx
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from datetime import datetime

app = FastAPI(
    title="BizOSaaS Image Integration Service",
    description="Centralized image management for product descriptions and blog content",
    version="1.0.0"
)

# Image API Configuration
IMAGE_APIS = {
    "pexels": {
        "base_url": "https://api.pexels.com/v1",
        "api_key": os.getenv("PEXELS_API_KEY", ""),
        "rate_limit": 200,  # per hour
        "search_endpoint": "/search"
    },
    "unsplash": {
        "base_url": "https://api.unsplash.com",
        "api_key": os.getenv("UNSPLASH_ACCESS_KEY", ""),
        "rate_limit": 50,  # per hour
        "search_endpoint": "/search/photos"
    },
    "pixabay": {
        "base_url": "https://pixabay.com/api",
        "api_key": os.getenv("PIXABAY_API_KEY", ""),
        "rate_limit": 100,  # per minute
        "search_endpoint": "/"
    },
    "amazon_sp_api": {
        "base_url": "https://sellingpartnerapi-na.amazon.com",
        "access_key": os.getenv("AMAZON_SP_ACCESS_KEY", ""),
        "secret_key": os.getenv("AMAZON_SP_SECRET_KEY", ""),
        "role_arn": os.getenv("AMAZON_SP_ROLE_ARN", "")
    }
}

class ImageRequest(BaseModel):
    query: str
    category: str = "general"
    count: int = 10
    min_width: int = 800
    min_height: int = 600
    orientation: str = "landscape"  # landscape, portrait, square
    source: str = "auto"  # auto, pexels, unsplash, pixabay

class ImageResult(BaseModel):
    id: str
    url: str
    thumbnail_url: str
    width: int
    height: int
    source: str
    alt_text: str
    tags: List[str]
    license: str
    attribution: Optional[str]

# ========================================================================================
# PEXELS INTEGRATION
# ========================================================================================

async def search_pexels_images(query: str, count: int = 10) -> List[ImageResult]:
    """Search Pexels for images"""
    if not IMAGE_APIS["pexels"]["api_key"]:
        return []
    
    try:
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": IMAGE_APIS["pexels"]["api_key"]}
            params = {
                "query": query,
                "per_page": min(count, 50),
                "orientation": "landscape"
            }
            
            response = await client.get(
                f"{IMAGE_APIS['pexels']['base_url']}/search",
                headers=headers,
                params=params,
                timeout=10.0
            )
            
            if response.status_code == 200:
                data = response.json()
                return [
                    ImageResult(
                        id=f"pexels_{photo['id']}",
                        url=photo['src']['large'],
                        thumbnail_url=photo['src']['medium'],
                        width=photo['width'],
                        height=photo['height'],
                        source="pexels",
                        alt_text=photo.get('alt', query),
                        tags=[query],
                        license="Pexels License",
                        attribution=f"Photo by {photo['photographer']} on Pexels"
                    )
                    for photo in data.get('photos', [])
                ]
    except Exception as e:
        print(f"Pexels API error: {e}")
        return []

# ========================================================================================
# UNSPLASH INTEGRATION
# ========================================================================================

async def search_unsplash_images(query: str, count: int = 10) -> List[ImageResult]:
    """Search Unsplash for images"""
    if not IMAGE_APIS["unsplash"]["api_key"]:
        return []
    
    try:
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Client-ID {IMAGE_APIS['unsplash']['api_key']}"}
            params = {
                "query": query,
                "per_page": min(count, 30),
                "orientation": "landscape"
            }
            
            response = await client.get(
                f"{IMAGE_APIS['unsplash']['base_url']}/search/photos",
                headers=headers,
                params=params,
                timeout=10.0
            )
            
            if response.status_code == 200:
                data = response.json()
                return [
                    ImageResult(
                        id=f"unsplash_{photo['id']}",
                        url=photo['urls']['regular'],
                        thumbnail_url=photo['urls']['small'],
                        width=photo['width'],
                        height=photo['height'],
                        source="unsplash",
                        alt_text=photo.get('alt_description', query),
                        tags=photo.get('tags', []),
                        license="Unsplash License",
                        attribution=f"Photo by {photo['user']['name']} on Unsplash"
                    )
                    for photo in data.get('results', [])
                ]
    except Exception as e:
        print(f"Unsplash API error: {e}")
        return []

# ========================================================================================
# PIXABAY INTEGRATION
# ========================================================================================

async def search_pixabay_images(query: str, count: int = 10) -> List[ImageResult]:
    """Search Pixabay for images"""
    if not IMAGE_APIS["pixabay"]["api_key"]:
        return []
    
    try:
        async with httpx.AsyncClient() as client:
            params = {
                "key": IMAGE_APIS["pixabay"]["api_key"],
                "q": query,
                "image_type": "photo",
                "orientation": "horizontal",
                "min_width": 800,
                "per_page": min(count, 50)
            }
            
            response = await client.get(
                IMAGE_APIS["pixabay"]["base_url"],
                params=params,
                timeout=10.0
            )
            
            if response.status_code == 200:
                data = response.json()
                return [
                    ImageResult(
                        id=f"pixabay_{hit['id']}",
                        url=hit['largeImageURL'],
                        thumbnail_url=hit['previewURL'],
                        width=hit['imageWidth'],
                        height=hit['imageHeight'],
                        source="pixabay",
                        alt_text=hit.get('tags', query),
                        tags=hit.get('tags', '').split(', '),
                        license="Pixabay License",
                        attribution=f"Image by {hit['user']} from Pixabay"
                    )
                    for hit in data.get('hits', [])
                ]
    except Exception as e:
        print(f"Pixabay API error: {e}")
        return []

# ========================================================================================
# AGGREGATED IMAGE SEARCH
# ========================================================================================

@app.post("/api/images/search")
async def search_images(request: ImageRequest) -> Dict[str, Any]:
    """Search for images across multiple APIs"""
    
    results = []
    
    if request.source == "auto" or request.source == "pexels":
        pexels_results = await search_pexels_images(request.query, request.count // 3)
        results.extend(pexels_results)
    
    if request.source == "auto" or request.source == "unsplash":
        unsplash_results = await search_unsplash_images(request.query, request.count // 3)
        results.extend(unsplash_results)
    
    if request.source == "auto" or request.source == "pixabay":
        pixabay_results = await search_pixabay_images(request.query, request.count // 3)
        results.extend(pixabay_results)
    
    # Sort by quality and remove duplicates
    unique_results = []
    seen_urls = set()
    
    for result in results:
        if result.url not in seen_urls:
            unique_results.append(result)
            seen_urls.add(result.url)
    
    # Limit to requested count
    final_results = unique_results[:request.count]
    
    return {
        "query": request.query,
        "total_found": len(final_results),
        "images": [result.dict() for result in final_results],
        "sources_used": list(set([r.source for r in final_results])),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/images/product-images/{product_id}")
async def get_product_images(product_id: str, keywords: str = ""):
    """Get optimized images for a specific product"""
    
    # Enhanced query for product images
    enhanced_query = f"{keywords} product commercial lifestyle"
    
    request = ImageRequest(
        query=enhanced_query,
        category="product",
        count=8,
        min_width=1200,
        min_height=800,
        orientation="landscape"
    )
    
    results = await search_images(request)
    
    return {
        "product_id": product_id,
        "keywords": keywords,
        "enhanced_query": enhanced_query,
        **results
    }

@app.get("/api/images/blog-images")
async def get_blog_images(title: str, keywords: str = "", category: str = "business"):
    """Get images for blog posts"""
    
    # Create contextual query for blog images
    blog_query = f"{keywords} {category} professional business"
    
    request = ImageRequest(
        query=blog_query,
        category="blog",
        count=5,
        min_width=1200,
        min_height=600,
        orientation="landscape"
    )
    
    results = await search_images(request)
    
    return {
        "blog_title": title,
        "category": category,
        "keywords": keywords,
        "optimized_query": blog_query,
        **results
    }

@app.get("/api/images/amazon-product-images/{asin}")
async def get_amazon_product_images(asin: str):
    """Get product images from Amazon SP-API"""
    
    # Mock Amazon SP-API integration (implement actual API calls)
    mock_images = [
        {
            "id": f"amazon_{asin}_1",
            "url": f"https://images-na.ssl-images-amazon.com/images/I/{asin}_1.jpg",
            "thumbnail_url": f"https://images-na.ssl-images-amazon.com/images/I/{asin}_1._SL300_.jpg",
            "width": 1500,
            "height": 1500,
            "source": "amazon_sp_api",
            "alt_text": "Amazon Product Image",
            "tags": ["product", "amazon"],
            "license": "Amazon Product Image",
            "attribution": "Amazon Product Image"
        }
    ]
    
    return {
        "asin": asin,
        "images": mock_images,
        "source": "amazon_sp_api",
        "note": "Amazon SP-API integration pending - showing mock data"
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    api_status = {}
    
    for api_name, config in IMAGE_APIS.items():
        if api_name == "amazon_sp_api":
            api_status[api_name] = "configured" if config["access_key"] else "missing_credentials"
        else:
            api_status[api_name] = "configured" if config["api_key"] else "missing_credentials"
    
    return {
        "status": "healthy",
        "service": "Image Integration Service",
        "apis": api_status,
        "features": [
            "Multi-source image search",
            "Product image optimization",
            "Blog content images",
            "Amazon SP-API integration ready",
            "Automatic attribution handling"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4005, reload=True)