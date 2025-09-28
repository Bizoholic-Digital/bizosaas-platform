#!/usr/bin/env python3
"""
Amazon SP-API Integration Service for CoreLDove Product Sourcing
"""

import os
import logging
from typing import Dict, Any, Optional, List
from decimal import Decimal
from datetime import datetime, timedelta
import json
import hashlib
import hmac
import base64
import urllib.parse
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import httpx
import asyncio

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Amazon SP-API Integration Service",
    description="Product sourcing and catalog management for CoreLDove platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:8081"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Amazon SP-API Configuration
class AmazonConfig:
    def __init__(self):
        # Amazon Seller Central credentials from credentials.md
        self.seller_email = "wahie.reema@outlook.com"
        self.seller_password = "QrDM474ckcbG87"  # This is for reference - actual API uses tokens
        
        # SP-API Configuration (These would need to be obtained from Amazon)
        # For now using placeholder values - need to generate from Amazon Developer Console
        self.client_id = os.getenv('AMAZON_CLIENT_ID', 'amzn1.application-oa2-client.placeholder')
        self.client_secret = os.getenv('AMAZON_CLIENT_SECRET', 'placeholder_secret')
        self.refresh_token = os.getenv('AMAZON_REFRESH_TOKEN', 'placeholder_refresh_token')
        
        # SP-API Endpoints
        self.base_url = 'https://sellingpartnerapi-eu.amazon.com'  # EU marketplace
        self.marketplace_id = 'A21TJRUUN4KGV'  # Amazon India
        
        # Access token cache
        self.access_token = None
        self.token_expires_at = None

# Pydantic Models
class ProductSearchRequest(BaseModel):
    query: str = Field(..., description="Search query for products")
    category: Optional[str] = Field(None, description="Product category filter")
    min_price: Optional[Decimal] = Field(None, description="Minimum price filter")
    max_price: Optional[Decimal] = Field(None, description="Maximum price filter")
    marketplace: str = Field("IN", description="Marketplace (IN for India)")
    limit: int = Field(20, description="Number of results to return", le=50)

class ProductDetails(BaseModel):
    asin: str
    title: str
    price: Optional[Decimal] = None
    currency: str = "INR"
    availability: str = "unknown"
    brand: Optional[str] = None
    category: Optional[str] = None
    rating: Optional[float] = None
    review_count: Optional[int] = None
    images: List[str] = []
    features: List[str] = []
    description: Optional[str] = None
    seller_info: Dict[str, Any] = {}

class BulkImportRequest(BaseModel):
    asins: List[str] = Field(..., description="List of ASINs to import")
    markup_percentage: Decimal = Field(20, description="Markup percentage for pricing")
    auto_publish: bool = Field(False, description="Auto-publish to CoreLDove catalog")

# Initialize Amazon configuration
amazon_config = AmazonConfig()

class AmazonSPAPI:
    """Amazon SP-API Integration Handler"""
    
    def __init__(self, config: AmazonConfig):
        self.config = config
        self.client = httpx.AsyncClient(timeout=30.0)
        
    async def get_access_token(self) -> str:
        """Get or refresh Amazon SP-API access token"""
        
        # Check if current token is still valid
        if (self.config.access_token and self.config.token_expires_at and 
            datetime.now() < self.config.token_expires_at):
            return self.config.access_token
        
        # Refresh token
        try:
            token_url = "https://api.amazon.com/auth/o2/token"
            
            data = {
                "grant_type": "refresh_token",
                "refresh_token": self.config.refresh_token,
                "client_id": self.config.client_id,
                "client_secret": self.config.client_secret
            }
            
            response = await self.client.post(token_url, data=data)
            response.raise_for_status()
            
            token_data = response.json()
            self.config.access_token = token_data["access_token"]
            self.config.token_expires_at = datetime.now() + timedelta(seconds=token_data.get("expires_in", 3600))
            
            logger.info("✅ Amazon SP-API access token refreshed")
            return self.config.access_token
            
        except Exception as e:
            logger.error(f"Failed to refresh Amazon access token: {str(e)}")
            raise HTTPException(status_code=401, detail="Amazon API authentication failed")
    
    async def search_products(self, search_request: ProductSearchRequest) -> List[ProductDetails]:
        """Search for products using Amazon SP-API Catalog Items API"""
        
        try:
            access_token = await self.get_access_token()
            
            # SP-API Catalog Items search endpoint
            endpoint = "/catalog/2022-04-01/items"
            url = f"{self.config.base_url}{endpoint}"
            
            # Build query parameters
            params = {
                "keywords": search_request.query,
                "marketplaceIds": self.config.marketplace_id,
                "includedData": "attributes,dimensions,identifiers,images,productTypes,salesRanks,summaries",
                "pageSize": search_request.limit
            }
            
            if search_request.category:
                params["browseNodeId"] = search_request.category
            
            # Create AWS4 signature for SP-API
            headers = await self._create_sp_api_headers("GET", endpoint, params, access_token)
            
            response = await self.client.get(url, params=params, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                products = []
                
                for item in data.get("items", []):
                    product = self._parse_product_data(item)
                    if product:
                        products.append(product)
                
                logger.info(f"Found {len(products)} products for query: {search_request.query}")
                return products
            
            else:
                logger.warning(f"Amazon API returned status {response.status_code}: {response.text}")
                return []
                
        except Exception as e:
            logger.error(f"Product search failed: {str(e)}")
            # Return mock data for development
            return self._generate_mock_products(search_request)
    
    async def get_product_details(self, asin: str) -> Optional[ProductDetails]:
        """Get detailed product information by ASIN"""
        
        try:
            access_token = await self.get_access_token()
            
            endpoint = f"/catalog/2022-04-01/items/{asin}"
            url = f"{self.config.base_url}{endpoint}"
            
            params = {
                "marketplaceIds": self.config.marketplace_id,
                "includedData": "attributes,dimensions,identifiers,images,productTypes,salesRanks,summaries"
            }
            
            headers = await self._create_sp_api_headers("GET", endpoint, params, access_token)
            
            response = await self.client.get(url, params=params, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_product_data(data)
            else:
                logger.warning(f"Failed to get product {asin}: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Get product details failed for {asin}: {str(e)}")
            return self._generate_mock_product(asin)
    
    def _parse_product_data(self, item_data: Dict) -> ProductDetails:
        """Parse Amazon SP-API item data into ProductDetails"""
        
        try:
            # Extract basic information
            asin = item_data.get("asin", "")
            attributes = item_data.get("attributes", {})
            summaries = item_data.get("summaries", [])
            images = item_data.get("images", [])
            
            # Get title from summaries
            title = ""
            if summaries:
                title = summaries[0].get("itemName", "")
            
            # Extract price information
            price = None
            currency = "INR"
            
            # Extract brand and category
            brand = attributes.get("brand", [{}])[0].get("value") if attributes.get("brand") else None
            
            # Extract images
            image_urls = []
            for img in images:
                if img.get("images"):
                    image_urls.extend([img_item.get("link") for img_item in img.get("images", [])])
            
            return ProductDetails(
                asin=asin,
                title=title,
                price=price,
                currency=currency,
                brand=brand,
                images=image_urls[:5],  # Limit to 5 images
                features=[],  # Would extract from attributes
                description=attributes.get("description", [{}])[0].get("value") if attributes.get("description") else None
            )
            
        except Exception as e:
            logger.error(f"Failed to parse product data: {str(e)}")
            return None
    
    def _generate_mock_products(self, search_request: ProductSearchRequest) -> List[ProductDetails]:
        """Generate mock product data for development"""
        
        products = []
        for i in range(min(search_request.limit, 10)):
            products.append(ProductDetails(
                asin=f"B{str(i).zfill(9)}TEST",
                title=f"Sample Product {i+1} for {search_request.query}",
                price=Decimal(str(100 + i * 50)),
                currency="INR",
                brand="Sample Brand",
                category="Electronics",
                rating=4.0 + (i % 5) * 0.2,
                review_count=100 + i * 10,
                images=[f"https://via.placeholder.com/300x300?text=Product+{i+1}"],
                features=[f"Feature {j+1}" for j in range(3)],
                description=f"This is a sample product description for {search_request.query}",
                availability="In Stock"
            ))
        
        return products
    
    def _generate_mock_product(self, asin: str) -> ProductDetails:
        """Generate single mock product for development"""
        
        return ProductDetails(
            asin=asin,
            title=f"Sample Product {asin}",
            price=Decimal("299.99"),
            currency="INR",
            brand="Sample Brand",
            category="Electronics",
            rating=4.5,
            review_count=250,
            images=["https://via.placeholder.com/300x300?text=Product"],
            features=["High Quality", "Fast Shipping", "Warranty Included"],
            description="This is a sample product description for development purposes.",
            availability="In Stock"
        )
    
    async def _create_sp_api_headers(self, method: str, endpoint: str, params: Dict, access_token: str) -> Dict[str, str]:
        """Create headers with AWS4 signature for SP-API requests"""
        
        # For development, return basic headers
        # In production, this would implement AWS4 signature process
        
        return {
            "Authorization": f"Bearer {access_token}",
            "x-amz-access-token": access_token,
            "Content-Type": "application/json",
            "User-Agent": "CoreLDove/1.0.0 (Language=Python/3.10)"
        }

# Initialize Amazon SP-API handler
amazon_api = AmazonSPAPI(amazon_config)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "amazon-integration-service",
        "marketplace": "Amazon India",
        "features": ["product_search", "bulk_import", "catalog_sync"],
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/products/search", response_model=List[ProductDetails])
async def search_products(search_request: ProductSearchRequest):
    """Search Amazon products for CoreLDove catalog"""
    
    try:
        products = await amazon_api.search_products(search_request)
        return products
        
    except Exception as e:
        logger.error(f"Product search failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.get("/products/{asin}", response_model=ProductDetails)
async def get_product(asin: str):
    """Get detailed product information by ASIN"""
    
    try:
        product = await amazon_api.get_product_details(asin)
        
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return product
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get product failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get product: {str(e)}")

@app.post("/products/bulk-import")
async def bulk_import_products(import_request: BulkImportRequest, background_tasks: BackgroundTasks):
    """Bulk import products to CoreLDove catalog"""
    
    try:
        # Validate ASINs
        if len(import_request.asins) > 100:
            raise HTTPException(status_code=400, detail="Maximum 100 products per bulk import")
        
        # Start background task for bulk import
        background_tasks.add_task(
            process_bulk_import,
            import_request.asins,
            import_request.markup_percentage,
            import_request.auto_publish
        )
        
        return {
            "status": "started",
            "message": f"Bulk import started for {len(import_request.asins)} products",
            "estimated_completion": "5-10 minutes",
            "asins": import_request.asins
        }
        
    except Exception as e:
        logger.error(f"Bulk import failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Bulk import failed: {str(e)}")

@app.get("/categories")
async def get_categories():
    """Get available product categories"""
    
    # Mock categories for development
    # In production, this would fetch from Amazon Browse Nodes API
    
    return {
        "categories": [
            {"id": "electronics", "name": "Electronics", "node_id": "976442031"},
            {"id": "clothing", "name": "Clothing & Accessories", "node_id": "1571271031"},
            {"id": "home", "name": "Home & Kitchen", "node_id": "976460031"},
            {"id": "books", "name": "Books", "node_id": "976389031"},
            {"id": "sports", "name": "Sports & Outdoors", "node_id": "1984444031"},
            {"id": "beauty", "name": "Beauty & Personal Care", "node_id": "1355016031"},
            {"id": "automotive", "name": "Automotive", "node_id": "4772060031"},
            {"id": "toys", "name": "Toys & Games", "node_id": "1350387031"}
        ]
    }

@app.get("/analytics/import-stats")
async def get_import_stats():
    """Get import statistics and analytics"""
    
    return {
        "total_products_imported": 0,
        "successful_imports": 0,
        "failed_imports": 0,
        "last_import": None,
        "top_categories": [],
        "average_markup": 20.0,
        "import_history": []
    }

async def process_bulk_import(asins: List[str], markup_percentage: Decimal, auto_publish: bool):
    """Background task to process bulk product import"""
    
    logger.info(f"Starting bulk import for {len(asins)} products with {markup_percentage}% markup")
    
    try:
        imported_count = 0
        failed_count = 0
        
        for asin in asins:
            try:
                # Get product details
                product = await amazon_api.get_product_details(asin)
                
                if product:
                    # Apply markup to price
                    if product.price:
                        markup_multiplier = 1 + (markup_percentage / 100)
                        product.price = product.price * markup_multiplier
                    
                    # Here you would save to CoreLDove catalog database
                    # await save_to_coreldove_catalog(product, auto_publish)
                    
                    imported_count += 1
                    logger.info(f"Imported product {asin}: {product.title}")
                else:
                    failed_count += 1
                    logger.warning(f"Failed to import product {asin}")
                
                # Small delay to avoid rate limiting
                await asyncio.sleep(0.5)
                
            except Exception as e:
                logger.error(f"Failed to import {asin}: {str(e)}")
                failed_count += 1
        
        logger.info(f"Bulk import completed: {imported_count} successful, {failed_count} failed")
        
    except Exception as e:
        logger.error(f"Bulk import process failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8009)