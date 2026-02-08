# API-First Implementation Plan: Amazon Integration Service

## Implementation Strategy Overview

This document provides detailed implementation steps for transitioning from scraping-primary to API-first architecture for Amazon product data retrieval.

---

## 1. Enhanced PA-API Implementation

### Current State Analysis
- **Existing Code**: Complete PA-API signing logic in `AmazonPAAPIService` class
- **Missing**: Real credentials and proper error handling
- **Status**: Falls back to mock data when credentials fail

### Implementation Steps

#### Step 1: Enhanced PA-API Service with Real Credentials

```python
# Enhanced amazon_paapi_service.py
import os
import json
import hashlib
import hmac
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
import httpx
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class PAAPIConfig:
    def __init__(self):
        # Real credentials from environment
        self.access_key = os.getenv('AMAZON_PAAPI_ACCESS_KEY')
        self.secret_key = os.getenv('AMAZON_PAAPI_SECRET_KEY') 
        self.partner_tag = os.getenv('AMAZON_PAAPI_PARTNER_TAG')
        
        # Validate credentials are present
        if not all([self.access_key, self.secret_key, self.partner_tag]):
            logger.warning("PA-API credentials not configured. Service will use fallback methods.")
            self.enabled = False
        else:
            self.enabled = True
            
        # API Configuration
        self.host = "webservices.amazon.in"
        self.region = "eu-west-1"
        self.service = "ProductAdvertisingAPI"
        self.base_url = f"https://{self.host}/paapi5"
        
        # Rate limiting
        self.max_requests_per_second = 1
        self.max_requests_per_day = 8640

class EnhancedPAAPIService:
    def __init__(self):
        self.config = PAAPIConfig()
        self.client = httpx.AsyncClient(timeout=30.0)
        self.request_count = 0
        self.last_request_time = 0
        
    async def search_products(self, keywords: str, **filters) -> List[ProductDetails]:
        """Search products using PA-API SearchItems operation"""
        
        if not self.config.enabled:
            logger.info("PA-API not configured, using fallback method")
            return await self._fallback_search(keywords, **filters)
            
        try:
            # Rate limiting check
            await self._enforce_rate_limits()
            
            # Build PA-API request
            operation = "SearchItems"
            payload = {
                "PartnerTag": self.config.partner_tag,
                "PartnerType": "Associates",
                "Marketplace": "www.amazon.in",
                "Keywords": keywords,
                "SearchIndex": filters.get("category", "All"),
                "ItemCount": min(filters.get("limit", 10), 10),  # PA-API max is 10
                "Resources": [
                    "Images.Primary.Large",
                    "ItemInfo.Title",
                    "ItemInfo.Features", 
                    "ItemInfo.ProductInfo",
                    "Offers.Listings.Price",
                    "Offers.Listings.Availability.Message",
                    "CustomerReviews.StarRating",
                    "CustomerReviews.Count"
                ]
            }
            
            # Add price filters if provided
            if filters.get("min_price"):
                payload["MinPrice"] = int(filters["min_price"] * 100)  # Convert to paise
            if filters.get("max_price"):
                payload["MaxPrice"] = int(filters["max_price"] * 100)
                
            # Generate signature and send request
            response = await self._make_signed_request(operation, payload)
            
            if response.status_code == 200:
                data = response.json()
                products = self._parse_search_response(data)
                logger.info(f"PA-API returned {len(products)} products for '{keywords}'")
                return products
            else:
                logger.error(f"PA-API request failed: {response.status_code}")
                return await self._fallback_search(keywords, **filters)
                
        except Exception as e:
            logger.error(f"PA-API search failed: {str(e)}")
            return await self._fallback_search(keywords, **filters)
    
    async def get_product_details(self, asins: List[str]) -> List[ProductDetails]:
        """Get detailed product information using PA-API GetItems operation"""
        
        if not self.config.enabled:
            return await self._fallback_get_items(asins)
            
        try:
            await self._enforce_rate_limits()
            
            # PA-API GetItems operation (max 10 ASINs per request)
            chunks = [asins[i:i+10] for i in range(0, len(asins), 10)]
            all_products = []
            
            for chunk in chunks:
                operation = "GetItems"
                payload = {
                    "PartnerTag": self.config.partner_tag,
                    "PartnerType": "Associates", 
                    "Marketplace": "www.amazon.in",
                    "ItemIds": chunk,
                    "ItemIdType": "ASIN",
                    "Resources": [
                        "Images.Primary.Large",
                        "ItemInfo.Title",
                        "ItemInfo.Features",
                        "ItemInfo.ProductInfo", 
                        "Offers.Listings.Price",
                        "Offers.Listings.Availability.Message",
                        "CustomerReviews.StarRating",
                        "CustomerReviews.Count"
                    ]
                }
                
                response = await self._make_signed_request(operation, payload)
                
                if response.status_code == 200:
                    data = response.json()
                    products = self._parse_items_response(data)
                    all_products.extend(products)
                else:
                    logger.warning(f"PA-API GetItems failed for chunk: {chunk}")
                    # Try fallback for failed chunk
                    fallback_products = await self._fallback_get_items(chunk)
                    all_products.extend(fallback_products)
            
            return all_products
            
        except Exception as e:
            logger.error(f"PA-API GetItems failed: {str(e)}")
            return await self._fallback_get_items(asins)
    
    async def _make_signed_request(self, operation: str, payload: Dict) -> httpx.Response:
        """Make signed PA-API request with AWS4 signature"""
        
        timestamp = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
        payload_json = json.dumps(payload)
        
        # Create canonical request
        method = "POST"
        uri = f"/paapi5/{operation.lower()}"
        query_string = ""
        
        canonical_headers = f"host:{self.config.host}\nx-amz-date:{timestamp}\n"
        signed_headers = "host;x-amz-date"
        
        payload_hash = hashlib.sha256(payload_json.encode()).hexdigest()
        canonical_request = f"{method}\n{uri}\n{query_string}\n{canonical_headers}\n{signed_headers}\n{payload_hash}"
        
        # Create string to sign
        credential_scope = f"{timestamp[:8]}/{self.config.region}/{self.config.service}/aws4_request"
        string_to_sign = f"AWS4-HMAC-SHA256\n{timestamp}\n{credential_scope}\n{hashlib.sha256(canonical_request.encode()).hexdigest()}"
        
        # Calculate signature
        def sign(key: bytes, msg: str) -> bytes:
            return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()
        
        k_date = sign(('AWS4' + self.config.secret_key).encode(), timestamp[:8])
        k_region = sign(k_date, self.config.region)
        k_service = sign(k_region, self.config.service)
        k_signing = sign(k_service, 'aws4_request')
        
        signature = hmac.new(k_signing, string_to_sign.encode(), hashlib.sha256).hexdigest()
        
        # Create authorization header
        authorization = f"AWS4-HMAC-SHA256 Credential={self.config.access_key}/{credential_scope}, SignedHeaders={signed_headers}, Signature={signature}"
        
        # Send request
        headers = {
            "Authorization": authorization,
            "Content-Type": "application/json; charset=utf-8",
            "Host": self.config.host,
            "X-Amz-Date": timestamp,
            "X-Amz-Target": f"com.amazon.paapi5.v1.ProductAdvertisingAPIv1.{operation}"
        }
        
        url = f"{self.config.base_url}/{operation.lower()}"
        return await self.client.post(url, headers=headers, content=payload_json)
    
    async def _enforce_rate_limits(self):
        """Enforce PA-API rate limits"""
        import time
        
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        # Enforce 1 request per second
        if time_since_last < 1.0:
            sleep_time = 1.0 - time_since_last
            await asyncio.sleep(sleep_time)
        
        self.last_request_time = time.time()
        self.request_count += 1
        
        # Log rate limit status
        if self.request_count % 100 == 0:
            logger.info(f"PA-API requests made: {self.request_count}")
    
    def _parse_search_response(self, data: Dict) -> List[ProductDetails]:
        """Parse PA-API SearchItems response"""
        products = []
        
        search_result = data.get("SearchResult", {})
        items = search_result.get("Items", [])
        
        for item in items:
            try:
                product = self._parse_pa_api_item(item)
                if product:
                    products.append(product)
            except Exception as e:
                logger.warning(f"Failed to parse PA-API item: {str(e)}")
        
        return products
    
    def _parse_items_response(self, data: Dict) -> List[ProductDetails]:
        """Parse PA-API GetItems response"""
        products = []
        
        items_result = data.get("ItemsResult", {})
        items = items_result.get("Items", [])
        
        for item in items:
            try:
                product = self._parse_pa_api_item(item)
                if product:
                    products.append(product)
            except Exception as e:
                logger.warning(f"Failed to parse PA-API item: {str(e)}")
        
        return products
    
    def _parse_pa_api_item(self, item: Dict) -> Optional[ProductDetails]:
        """Parse individual PA-API item into ProductDetails"""
        
        try:
            asin = item.get("ASIN")
            if not asin:
                return None
            
            # Extract basic info
            item_info = item.get("ItemInfo", {})
            title = item_info.get("Title", {}).get("DisplayValue", "")
            
            # Extract price
            price = None
            currency = "INR"
            offers = item.get("Offers", {}).get("Listings", [])
            if offers:
                price_info = offers[0].get("Price", {})
                if price_info:
                    amount = price_info.get("Amount")
                    if amount:
                        price = Decimal(str(amount / 100))  # Convert from paise
                        currency = price_info.get("Currency", "INR")
            
            # Extract images
            image_url = None
            images = item.get("Images", {}).get("Primary", {})
            if images:
                large_image = images.get("Large", {})
                if large_image:
                    image_url = large_image.get("URL")
            
            # Extract features
            features = []
            feature_info = item_info.get("Features", {})
            if feature_info:
                display_values = feature_info.get("DisplayValues", [])
                features = [f.get("DisplayValue", "") for f in display_values]
            
            # Extract brand
            brand = None
            brand_info = item_info.get("ByLineInfo", {})
            if brand_info:
                brand_data = brand_info.get("Brand", {})
                if brand_data:
                    brand = brand_data.get("DisplayValue")
            
            # Extract reviews
            rating = None
            review_count = None
            reviews = item.get("CustomerReviews", {})
            if reviews:
                star_rating = reviews.get("StarRating", {})
                if star_rating:
                    rating = float(star_rating.get("Value", 0))
                
                count_info = reviews.get("Count", {})
                if count_info:
                    review_count = int(count_info.get("Value", 0))
            
            # Extract availability
            availability = "Unknown"
            if offers:
                availability_info = offers[0].get("Availability", {})
                if availability_info:
                    availability = availability_info.get("Message", "Unknown")
            
            return ProductDetails(
                asin=asin,
                title=title,
                price=price,
                currency=currency,
                image_url=image_url,
                product_url=f"https://www.amazon.in/dp/{asin}",
                brand=brand,
                features=features,
                rating=rating,
                review_count=review_count,
                availability=availability
            )
            
        except Exception as e:
            logger.error(f"Error parsing PA-API item: {str(e)}")
            return None
    
    async def _fallback_search(self, keywords: str, **filters) -> List[ProductDetails]:
        """Fallback to existing scraping method when PA-API fails"""
        from amazon_sourcing_service import generate_real_amazon_products
        
        # Convert to existing format
        search_request = ProductSearchRequest(
            query=keywords,
            category=filters.get("category"),
            min_price=filters.get("min_price"),
            max_price=filters.get("max_price"),
            limit=filters.get("limit", 10)
        )
        
        return await generate_real_amazon_products(search_request)
    
    async def _fallback_get_items(self, asins: List[str]) -> List[ProductDetails]:
        """Fallback to scraping for individual ASINs"""
        from amazon_sourcing_service import amazon_scraper
        
        products = []
        for asin in asins:
            try:
                scraped_data = await amazon_scraper.scrape_product_data(asin)
                if scraped_data.get("success"):
                    product = ProductDetails(
                        asin=asin,
                        title=scraped_data.get("title", ""),
                        price=Decimal(str(scraped_data.get("price", 0))) if scraped_data.get("price") else None,
                        currency="INR",
                        image_url=scraped_data.get("image_url"),
                        product_url=f"https://www.amazon.in/dp/{asin}",
                        rating=scraped_data.get("rating"),
                        review_count=scraped_data.get("review_count"),
                        availability=scraped_data.get("availability", "Unknown")
                    )
                    products.append(product)
            except Exception as e:
                logger.warning(f"Fallback failed for ASIN {asin}: {str(e)}")
        
        return products

    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()
```

---

## 2. Data Orchestration Layer

### Implementation: Smart Data Retrieval Orchestrator

```python
# data_orchestrator.py
import asyncio
import logging
from typing import List, Optional, Dict, Any
from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class DataSource(Enum):
    PA_API = "pa_api"
    SP_API = "sp_api"
    SCRAPING = "scraping"
    CACHE = "cache"

@dataclass
class DataQualityScore:
    completeness: float  # 0-1 score for data completeness
    accuracy: float      # 0-1 score for data accuracy
    freshness: float     # 0-1 score for data freshness
    source: DataSource
    
    @property
    def overall_score(self) -> float:
        return (self.completeness * 0.4 + self.accuracy * 0.4 + self.freshness * 0.2)

class DataRetrievalOrchestrator:
    """Orchestrates data retrieval from multiple sources with intelligent fallbacks"""
    
    def __init__(self):
        self.pa_api_service = EnhancedPAAPIService()
        self.sp_api_service = AmazonSPAPIService()  # From existing code
        self.scraper = AmazonDataScraper()         # From existing code
        self.cache = {}  # In production, use Redis or similar
        
        # Performance tracking
        self.performance_stats = {
            DataSource.PA_API: {"requests": 0, "successes": 0, "avg_time": 0},
            DataSource.SP_API: {"requests": 0, "successes": 0, "avg_time": 0},
            DataSource.SCRAPING: {"requests": 0, "successes": 0, "avg_time": 0},
        }
    
    async def get_product_data(self, asin: str, require_real_time: bool = False) -> Optional[ProductDetails]:
        """Get product data with intelligent source selection"""
        
        # Check cache first (unless real-time data required)
        if not require_real_time:
            cached_data = self._get_cached_data(asin)
            if cached_data and self._is_cache_fresh(cached_data):
                return cached_data.product
        
        # Try data sources in order of preference
        strategies = [
            (DataSource.PA_API, self._get_from_pa_api),
            (DataSource.SP_API, self._get_from_sp_api),
            (DataSource.SCRAPING, self._get_from_scraping)
        ]
        
        for source, method in strategies:
            try:
                start_time = datetime.now()
                product = await method(asin)
                duration = (datetime.now() - start_time).total_seconds()
                
                self._update_performance_stats(source, duration, success=product is not None)
                
                if product:
                    # Score the data quality
                    quality_score = self._calculate_data_quality(product, source)
                    
                    # Cache the result if quality is acceptable
                    if quality_score.overall_score >= 0.7:
                        self._cache_product_data(asin, product, quality_score)
                        logger.info(f"Retrieved {asin} from {source.value} (quality: {quality_score.overall_score:.2f})")
                        return product
                    else:
                        logger.warning(f"Low quality data from {source.value} for {asin} (score: {quality_score.overall_score:.2f})")
                
            except Exception as e:
                logger.warning(f"Failed to get {asin} from {source.value}: {str(e)}")
                self._update_performance_stats(source, 0, success=False)
        
        # All sources failed, try cache as last resort
        cached_data = self._get_cached_data(asin)
        if cached_data:
            logger.info(f"Returning stale cached data for {asin}")
            return cached_data.product
        
        logger.error(f"All data sources failed for ASIN {asin}")
        return None
    
    async def search_products(self, query: str, **filters) -> List[ProductDetails]:
        """Search for products with smart source selection"""
        
        # Try PA-API first for search (best for discovery)
        try:
            products = await self.pa_api_service.search_products(query, **filters)
            if products:
                logger.info(f"PA-API search returned {len(products)} products for '{query}'")
                return products
        except Exception as e:
            logger.warning(f"PA-API search failed for '{query}': {str(e)}")
        
        # Fallback to existing search implementation
        from amazon_sourcing_service import generate_real_amazon_products
        search_request = ProductSearchRequest(
            query=query,
            category=filters.get("category"),
            min_price=filters.get("min_price"),
            max_price=filters.get("max_price"),
            limit=filters.get("limit", 10)
        )
        
        return await generate_real_amazon_products(search_request)
    
    async def bulk_get_products(self, asins: List[str]) -> List[ProductDetails]:
        """Efficiently retrieve multiple products"""
        
        # Separate cached vs non-cached ASINs
        cached_products = []
        uncached_asins = []
        
        for asin in asins:
            cached_data = self._get_cached_data(asin)
            if cached_data and self._is_cache_fresh(cached_data):
                cached_products.append(cached_data.product)
            else:
                uncached_asins.append(asin)
        
        logger.info(f"Retrieved {len(cached_products)} products from cache, fetching {len(uncached_asins)} from APIs")
        
        # Fetch uncached products
        fetched_products = []
        
        if uncached_asins:
            # Try PA-API batch fetch first
            try:
                pa_api_products = await self.pa_api_service.get_product_details(uncached_asins)
                fetched_products.extend(pa_api_products)
                
                # Track which ASINs still need fetching
                fetched_asins = {p.asin for p in pa_api_products}
                remaining_asins = [asin for asin in uncached_asins if asin not in fetched_asins]
                
            except Exception as e:
                logger.warning(f"PA-API batch fetch failed: {str(e)}")
                remaining_asins = uncached_asins
            
            # Fetch remaining ASINs individually using fallback methods
            for asin in remaining_asins:
                product = await self.get_product_data(asin)
                if product:
                    fetched_products.append(product)
        
        return cached_products + fetched_products
    
    async def _get_from_pa_api(self, asin: str) -> Optional[ProductDetails]:
        """Get product from PA-API"""
        products = await self.pa_api_service.get_product_details([asin])
        return products[0] if products else None
    
    async def _get_from_sp_api(self, asin: str) -> Optional[ProductDetails]:
        """Get product from SP-API"""
        # Implementation would depend on SP-API setup
        # For now, return None to skip to next method
        return None
    
    async def _get_from_scraping(self, asin: str) -> Optional[ProductDetails]:
        """Get product from scraping"""
        scraped_data = await self.scraper.scrape_product_data(asin)
        
        if scraped_data.get("success"):
            return ProductDetails(
                asin=asin,
                title=scraped_data.get("title", ""),
                price=Decimal(str(scraped_data.get("price", 0))) if scraped_data.get("price") else None,
                currency="INR",
                image_url=scraped_data.get("image_url"),
                product_url=f"https://www.amazon.in/dp/{asin}",
                rating=scraped_data.get("rating"),
                review_count=scraped_data.get("review_count"),
                availability=scraped_data.get("availability", "Unknown")
            )
        return None
    
    def _calculate_data_quality(self, product: ProductDetails, source: DataSource) -> DataQualityScore:
        """Calculate data quality score for a product"""
        
        # Completeness score (0-1)
        fields = [product.title, product.price, product.image_url, product.rating]
        completeness = sum(1 for field in fields if field is not None) / len(fields)
        
        # Accuracy score (based on source reliability)
        accuracy_by_source = {
            DataSource.PA_API: 0.95,
            DataSource.SP_API: 0.90,
            DataSource.SCRAPING: 0.75,
            DataSource.CACHE: 0.80
        }
        accuracy = accuracy_by_source.get(source, 0.5)
        
        # Freshness score (always 1.0 for real-time data)
        freshness = 1.0
        
        return DataQualityScore(
            completeness=completeness,
            accuracy=accuracy,
            freshness=freshness,
            source=source
        )
    
    def _cache_product_data(self, asin: str, product: ProductDetails, quality_score: DataQualityScore):
        """Cache product data with metadata"""
        cache_entry = {
            "product": product,
            "quality_score": quality_score,
            "cached_at": datetime.now(),
            "ttl": timedelta(hours=1 if quality_score.source == DataSource.PA_API else 0.5)
        }
        self.cache[asin] = cache_entry
    
    def _get_cached_data(self, asin: str) -> Optional[Dict]:
        """Get cached product data"""
        return self.cache.get(asin)
    
    def _is_cache_fresh(self, cached_data: Dict) -> bool:
        """Check if cached data is still fresh"""
        cached_at = cached_data["cached_at"]
        ttl = cached_data["ttl"]
        return datetime.now() - cached_at < ttl
    
    def _update_performance_stats(self, source: DataSource, duration: float, success: bool):
        """Update performance statistics"""
        stats = self.performance_stats[source]
        stats["requests"] += 1
        if success:
            stats["successes"] += 1
        
        # Update average time (simple moving average)
        if stats["requests"] == 1:
            stats["avg_time"] = duration
        else:
            stats["avg_time"] = (stats["avg_time"] * 0.9) + (duration * 0.1)
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get performance report for monitoring"""
        report = {}
        for source, stats in self.performance_stats.items():
            success_rate = stats["successes"] / stats["requests"] if stats["requests"] > 0 else 0
            report[source.value] = {
                "success_rate": success_rate,
                "average_response_time": stats["avg_time"],
                "total_requests": stats["requests"]
            }
        return report
    
    async def close(self):
        """Close all services"""
        await self.pa_api_service.close()
        await self.scraper.close()
```

---

## 3. Integration with Existing Service

### Updated Main Service Integration

```python
# Updated endpoints in amazon_sourcing_service.py

# Global orchestrator instance
data_orchestrator = DataRetrievalOrchestrator()

@app.post("/sourcing/search", response_model=List[ProductDetails])
async def search_products_for_sourcing_enhanced(search_request: ProductSearchRequest):
    """Enhanced search using API-first approach"""
    logger.info(f"🔍 Enhanced search for: {search_request.query}")
    
    try:
        # Use the orchestrator for intelligent source selection
        products = await data_orchestrator.search_products(
            query=search_request.query,
            category=search_request.category,
            min_price=search_request.min_price,
            max_price=search_request.max_price,
            limit=search_request.limit
        )
        
        logger.info(f"✅ Enhanced search returned {len(products)} products")
        return products
        
    except Exception as e:
        logger.error(f"Enhanced search failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Enhanced search failed: {str(e)}")

@app.get("/products/{asin}/enhanced", response_model=ProductDetails)
async def get_product_enhanced(asin: str, real_time: bool = False):
    """Get product using enhanced API-first approach"""
    logger.info(f"🔍 Enhanced product fetch for: {asin}")
    
    try:
        product = await data_orchestrator.get_product_data(asin, require_real_time=real_time)
        
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {asin} not found")
        
        return product
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Enhanced product fetch failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Enhanced fetch failed: {str(e)}")

@app.post("/products/bulk-enhanced", response_model=List[ProductDetails])
async def bulk_get_products_enhanced(asins: List[str]):
    """Bulk product retrieval using enhanced API-first approach"""
    logger.info(f"🔍 Enhanced bulk fetch for {len(asins)} ASINs")
    
    try:
        if len(asins) > 50:
            raise HTTPException(status_code=400, detail="Maximum 50 ASINs per request")
        
        products = await data_orchestrator.bulk_get_products(asins)
        
        logger.info(f"✅ Enhanced bulk fetch returned {len(products)} products")
        return products
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Enhanced bulk fetch failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Enhanced bulk fetch failed: {str(e)}")

@app.get("/analytics/data-sources")
async def get_data_source_analytics():
    """Get analytics about data source performance"""
    try:
        performance_report = data_orchestrator.get_performance_report()
        
        return {
            "data_sources": performance_report,
            "cache_size": len(data_orchestrator.cache),
            "recommendations": generate_source_recommendations(performance_report),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Analytics fetch failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analytics failed: {str(e)}")

def generate_source_recommendations(performance_report: Dict) -> List[str]:
    """Generate recommendations based on performance data"""
    recommendations = []
    
    pa_api_success = performance_report.get("pa_api", {}).get("success_rate", 0)
    scraping_success = performance_report.get("scraping", {}).get("success_rate", 0)
    
    if pa_api_success < 0.5:
        recommendations.append("PA-API success rate is low. Check credentials and rate limits.")
    
    if scraping_success > 0.8 and pa_api_success < 0.8:
        recommendations.append("Scraping is outperforming PA-API. Consider credential issues.")
    
    if pa_api_success > 0.9:
        recommendations.append("PA-API performing well. Consider reducing scraping dependency.")
    
    return recommendations

@app.on_event("shutdown")
async def enhanced_shutdown():
    """Enhanced shutdown with orchestrator cleanup"""
    await data_orchestrator.close()
    await amazon_scraper.close()
    await asin_validator.client.aclose()
    logger.info("Enhanced Amazon integration service shutdown complete")
```

---

## 4. Environment Configuration

### Required Environment Variables

```bash
# .env.production
# Amazon PA-API Credentials (Required for API-first approach)
AMAZON_PAAPI_ACCESS_KEY=your_real_access_key_here
AMAZON_PAAPI_SECRET_KEY=your_real_secret_key_here
AMAZON_PAAPI_PARTNER_TAG=your_associate_id_here

# Amazon SP-API Credentials (Optional, for enhanced features)
AMAZON_SPAPI_CLIENT_ID=amzn1.application-oa2-client.your_client_id
AMAZON_SPAPI_CLIENT_SECRET=your_client_secret_here
AMAZON_SPAPI_REFRESH_TOKEN=your_refresh_token_here

# Service Configuration
API_FIRST_MODE=true
SCRAPING_FALLBACK_ENABLED=true
CACHE_TTL_HOURS=1
MAX_REQUESTS_PER_SECOND=1
MAX_DAILY_REQUESTS=8640

# Monitoring and Logging
LOG_LEVEL=INFO
PERFORMANCE_TRACKING_ENABLED=true
ALERT_ON_LOW_SUCCESS_RATE=0.8
```

### Docker Compose Enhancement

```yaml
# docker-compose.enhanced.yml
version: '3.8'

services:
  amazon-integration-enhanced:
    build: .
    container_name: amazon-integration-enhanced
    ports:
      - "8080:8080"
    environment:
      - AMAZON_PAAPI_ACCESS_KEY=${AMAZON_PAAPI_ACCESS_KEY}
      - AMAZON_PAAPI_SECRET_KEY=${AMAZON_PAAPI_SECRET_KEY}
      - AMAZON_PAAPI_PARTNER_TAG=${AMAZON_PAAPI_PARTNER_TAG}
      - API_FIRST_MODE=true
      - SCRAPING_FALLBACK_ENABLED=true
    volumes:
      - ./logs:/app/logs
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped
    
  redis-cache:
    image: redis:7-alpine
    container_name: amazon-integration-cache
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  redis_data:
```

---

## 5. Testing and Validation

### Enhanced Test Suite

```python
# test_api_first_implementation.py
import pytest
import asyncio
from data_orchestrator import DataRetrievalOrchestrator, DataSource

class TestAPIFirstImplementation:
    
    @pytest.fixture
    async def orchestrator(self):
        orchestrator = DataRetrievalOrchestrator()
        yield orchestrator
        await orchestrator.close()
    
    @pytest.mark.asyncio
    async def test_pa_api_product_fetch(self, orchestrator):
        """Test PA-API product retrieval"""
        # Use a known valid ASIN
        product = await orchestrator.get_product_data("B0CR7G9V56")
        
        assert product is not None
        assert product.asin == "B0CR7G9V56"
        assert product.title is not None
        assert product.price is not None
    
    @pytest.mark.asyncio
    async def test_fallback_mechanism(self, orchestrator):
        """Test fallback from PA-API to scraping"""
        # Temporarily disable PA-API
        orchestrator.pa_api_service.config.enabled = False
        
        product = await orchestrator.get_product_data("B0CR7G9V56")
        
        assert product is not None
        assert product.asin == "B0CR7G9V56"
    
    @pytest.mark.asyncio
    async def test_bulk_fetch_performance(self, orchestrator):
        """Test bulk fetch performance"""
        asins = ["B0CR7G9V56", "B0DX1QJFK4", "B0BLSQPPKT"]
        
        start_time = asyncio.get_event_loop().time()
        products = await orchestrator.bulk_get_products(asins)
        duration = asyncio.get_event_loop().time() - start_time
        
        assert len(products) >= 1  # At least one product should be fetched
        assert duration < 30  # Should complete in reasonable time
    
    @pytest.mark.asyncio
    async def test_cache_functionality(self, orchestrator):
        """Test caching behavior"""
        asin = "B0CR7G9V56"
        
        # First fetch (should be slow)
        start_time = asyncio.get_event_loop().time()
        product1 = await orchestrator.get_product_data(asin)
        first_duration = asyncio.get_event_loop().time() - start_time
        
        # Second fetch (should be fast due to cache)
        start_time = asyncio.get_event_loop().time()
        product2 = await orchestrator.get_product_data(asin)
        second_duration = asyncio.get_event_loop().time() - start_time
        
        assert product1 is not None
        assert product2 is not None
        assert product1.asin == product2.asin
        assert second_duration < first_duration  # Cache should be faster
    
    def test_data_quality_scoring(self, orchestrator):
        """Test data quality scoring"""
        from amazon_sourcing_service import ProductDetails
        from decimal import Decimal
        
        # Create a complete product
        complete_product = ProductDetails(
            asin="B0CR7G9V56",
            title="Complete Product",
            price=Decimal("100"),
            image_url="https://example.com/image.jpg",
            rating=4.5
        )
        
        quality_score = orchestrator._calculate_data_quality(complete_product, DataSource.PA_API)
        
        assert quality_score.completeness == 1.0  # All fields present
        assert quality_score.accuracy == 0.95     # PA-API is highly accurate
        assert quality_score.overall_score >= 0.9  # Should be high quality

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

---

## 6. Monitoring Dashboard

### Performance Monitoring Implementation

```python
# monitoring.py
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import json

monitoring_app = FastAPI(title="Amazon Integration Monitoring")

@monitoring_app.get("/dashboard", response_class=HTMLResponse)
async def monitoring_dashboard():
    """Simple monitoring dashboard"""
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Amazon Integration Monitoring</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .metric-card { 
                border: 1px solid #ddd; 
                padding: 20px; 
                margin: 10px; 
                border-radius: 8px;
                display: inline-block;
                width: 200px;
            }
            .status-ok { border-left: 5px solid #28a745; }
            .status-warning { border-left: 5px solid #ffc107; }
            .status-error { border-left: 5px solid #dc3545; }
        </style>
    </head>
    <body>
        <h1>Amazon Integration Service Monitoring</h1>
        
        <div id="metrics">
            <!-- Metrics will be loaded here -->
        </div>
        
        <canvas id="performanceChart" width="400" height="200"></canvas>
        
        <script>
            async function loadMetrics() {
                try {
                    const response = await fetch('/analytics/data-sources');
                    const data = await response.json();
                    
                    const metricsDiv = document.getElementById('metrics');
                    metricsDiv.innerHTML = '';
                    
                    for (const [source, stats] of Object.entries(data.data_sources)) {
                        const successRate = stats.success_rate * 100;
                        const status = successRate > 90 ? 'ok' : successRate > 70 ? 'warning' : 'error';
                        
                        const card = document.createElement('div');
                        card.className = `metric-card status-${status}`;
                        card.innerHTML = `
                            <h3>${source.toUpperCase()}</h3>
                            <p>Success Rate: ${successRate.toFixed(1)}%</p>
                            <p>Avg Response: ${stats.average_response_time.toFixed(2)}s</p>
                            <p>Requests: ${stats.total_requests}</p>
                        `;
                        metricsDiv.appendChild(card);
                    }
                    
                } catch (error) {
                    console.error('Failed to load metrics:', error);
                }
            }
            
            // Load metrics on page load
            loadMetrics();
            
            // Refresh every 30 seconds
            setInterval(loadMetrics, 30000);
        </script>
    </body>
    </html>
    """
    
    return html_content
```

This implementation plan provides a complete transition strategy from scraping-primary to API-first architecture while maintaining backward compatibility and ensuring robust fallback mechanisms.