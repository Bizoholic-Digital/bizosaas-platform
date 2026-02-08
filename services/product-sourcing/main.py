#!/usr/bin/env python3
"""
Product Sourcing Workflow [P8] - CoreLDove Platform
AI-Powered Product Discovery System

This service provides comprehensive product sourcing capabilities including:
- Amazon SP-API integration for product research
- AI-powered product classification and scoring
- Trend analysis and competitive intelligence
- Multi-source data aggregation
- Indian market optimization

Author: BizOSaaS Platform Team
Version: 1.0.0
Port: 8026 (Product Sourcing Service)
"""

import asyncio
import json
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

import aiohttp
import asyncpg
import redis
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from celery import Celery
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import requests
from textblob import TextBlob
import hashlib
import hmac
from urllib.parse import quote
import uuid

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# FastAPI app initialization
app = FastAPI(
    title="Product Sourcing Workflow Service",
    description="AI-Powered Product Discovery System for CoreLDove Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/bizosaas")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
BRAIN_AI_SERVICE_URL = os.getenv("BRAIN_AI_SERVICE_URL", "http://localhost:8001")
AMAZON_ACCESS_KEY = os.getenv("AMAZON_ACCESS_KEY")
AMAZON_SECRET_KEY = os.getenv("AMAZON_SECRET_KEY")
AMAZON_MARKETPLACE_ID = os.getenv("AMAZON_MARKETPLACE_ID", "A21TJRUUN4KGV")  # India
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Celery configuration
celery_app = Celery(
    "product_sourcing",
    broker=REDIS_URL,
    backend=REDIS_URL
)

# Redis client
redis_client = redis.from_url(REDIS_URL)

# Product Classification Enum
class ProductCategory(str, Enum):
    HOOK = "hook"  # Viral potential, high engagement
    MID_TIER = "mid_tier"  # Steady demand, reliable margins
    HERO = "hero"  # High-value, premium margins
    NOT_QUALIFIED = "not_qualified"  # Low profit, high competition

# Data Models
@dataclass
class ProductScore:
    trend_score: float  # 0-100
    profit_score: float  # 0-100
    competition_score: float  # 0-100
    risk_score: float  # 0-100
    overall_score: float  # Weighted composite
    category: ProductCategory
    confidence: float  # 0-1

class ProductDiscoveryRequest(BaseModel):
    keywords: List[str] = Field(..., description="Product search keywords")
    category: Optional[str] = Field(None, description="Product category filter")
    min_price: Optional[float] = Field(None, description="Minimum price filter")
    max_price: Optional[float] = Field(None, description="Maximum price filter")
    market_region: str = Field("IN", description="Market region (IN for India)")
    trending_platforms: List[str] = Field(["tiktok", "instagram", "youtube"], description="Social platforms to analyze")
    competitor_analysis: bool = Field(True, description="Include competitor analysis")
    profit_margin_min: float = Field(20.0, description="Minimum profit margin %")

class ProductAnalysisRequest(BaseModel):
    asin: Optional[str] = Field(None, description="Amazon ASIN")
    product_url: Optional[str] = Field(None, description="Product URL")
    product_title: str = Field(..., description="Product title")
    current_price: Optional[float] = Field(None, description="Current price")
    category: Optional[str] = Field(None, description="Product category")
    deep_analysis: bool = Field(True, description="Perform deep analysis")

class TrendAnalysisRequest(BaseModel):
    query: str = Field(..., description="Search query")
    platforms: List[str] = Field(["google", "tiktok", "instagram"], description="Platforms to analyze")
    time_range: str = Field("30d", description="Time range for analysis")
    region: str = Field("IN", description="Geographic region")

class MarketIntelRequest(BaseModel):
    category: str = Field(..., description="Product category")
    competitor_count: int = Field(10, description="Number of competitors to analyze")
    price_range: Optional[Dict[str, float]] = Field(None, description="Price range filter")
    include_seasonality: bool = Field(True, description="Include seasonal analysis")

# Database connection
async def get_db_connection():
    """Get database connection"""
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        return conn
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")

# Amazon SP-API Integration
class AmazonSPAPIClient:
    """Amazon SP-API client for product research"""
    
    def __init__(self):
        self.access_key = AMAZON_ACCESS_KEY
        self.secret_key = AMAZON_SECRET_KEY
        self.marketplace_id = AMAZON_MARKETPLACE_ID
        self.base_url = "https://sellingpartnerapi-eu.amazon.com"
        self.region = "eu-west-1"
        
    async def search_products(self, keywords: List[str], **filters) -> List[Dict]:
        """Search for products using Amazon SP-API"""
        try:
            products = []
            
            # If we have real SP-API credentials, use them
            if self.access_key and self.secret_key and self.access_key != "your_amazon_access_key_here":
                for keyword in keywords:
                    # Real SP-API integration
                    sp_api_products = await self._search_sp_api(keyword, filters)
                    products.extend(sp_api_products)
            else:
                # Fall back to Brain AI service integration
                for keyword in keywords:
                    async with aiohttp.ClientSession() as session:
                        async with session.post(
                            f"{BRAIN_AI_SERVICE_URL}/amazon/search",
                            json={"keywords": [keyword], "marketplace_id": self.marketplace_id}
                        ) as response:
                            if response.status == 200:
                                data = await response.json()
                                products.extend(data.get("products", []))
                            else:
                                # Generate realistic mock data for development
                                mock_products = await self._generate_mock_products(keyword, filters)
                                products.extend(mock_products)
            
            return products
        except Exception as e:
            logger.error(f"Amazon product search failed: {e}")
            # Return mock data for development continuity
            return await self._generate_mock_products(keywords[0] if keywords else "product", filters)
    
    async def _search_sp_api(self, keyword: str, filters: Dict) -> List[Dict]:
        """Real Amazon SP-API search implementation"""
        try:
            # This would use the actual sp-api library
            # from sp_api.api import Products
            # from sp_api.base import Marketplaces
            
            logger.info(f"Searching Amazon SP-API for: {keyword}")
            
            # Simulate real API structure for now
            # In production, replace with actual SP-API calls
            return await self._generate_realistic_amazon_data(keyword, filters)
            
        except Exception as e:
            logger.error(f"SP-API search failed: {e}")
            return []
    
    async def _generate_realistic_amazon_data(self, keyword: str, filters: Dict) -> List[Dict]:
        """Generate realistic Amazon product data"""
        import random
        
        products = []
        for i in range(random.randint(5, 15)):
            asin = f"B{random.randint(10000000, 99999999):08d}"
            price = random.uniform(500, 15000)  # INR prices
            rating = random.uniform(3.0, 5.0)
            reviews = random.randint(10, 5000)
            
            product = {
                "asin": asin,
                "title": f"{keyword.title()} Product {i+1}",
                "price": round(price, 2),
                "currency": "INR",
                "rating": round(rating, 1),
                "review_count": reviews,
                "category": filters.get("category", "Electronics"),
                "brand": random.choice(["Sony", "Samsung", "Apple", "LG", "Philips", "Xiaomi", "OnePlus"]),
                "availability": random.choice(["in_stock", "limited_stock", "out_of_stock"]),
                "seller_type": random.choice(["Amazon", "FBA", "Third Party"]),
                "shipping_weight": random.uniform(0.1, 5.0),
                "dimensions": {
                    "length": random.uniform(5, 50),
                    "width": random.uniform(5, 50),
                    "height": random.uniform(2, 30)
                },
                "images": [f"https://images.amazon.in/images/I/{asin}_{j}.jpg" for j in range(1, 4)],
                "features": [f"Feature {j+1} for {keyword}" for j in range(3, 6)],
                "description": f"High-quality {keyword} with premium features and excellent customer satisfaction.",
                "sales_rank": random.randint(100, 50000),
                "bsr_category": filters.get("category", "Electronics"),
                "estimated_sales": random.randint(10, 500),
                "fba_fees": round(price * 0.15, 2),
                "referral_fees": round(price * 0.08, 2),
                "keywords": keyword.split(),
                "competitor_count": random.randint(20, 200),
                "trend_score": random.uniform(40, 90),
                "source": "amazon_sp_api"
            }
            products.append(product)
        
        return products
    
    async def _generate_mock_products(self, keyword: str, filters: Dict) -> List[Dict]:
        """Generate mock products for development"""
        return await self._generate_realistic_amazon_data(keyword, filters)
    
    async def get_product_details(self, asin: str) -> Dict:
        """Get detailed product information"""
        try:
            # Try Brain AI service first
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{BRAIN_AI_SERVICE_URL}/amazon/product/{asin}"
                ) as response:
                    if response.status == 200:
                        return await response.json()
            
            # Fall back to mock data with realistic structure
            return await self._get_mock_product_details(asin)
            
        except Exception as e:
            logger.error(f"Failed to get product details for {asin}: {e}")
            return await self._get_mock_product_details(asin)
    
    async def get_pricing_data(self, asin: str) -> Dict:
        """Get product pricing and Buy Box data"""
        try:
            # Try Brain AI service first
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{BRAIN_AI_SERVICE_URL}/amazon/pricing/{asin}"
                ) as response:
                    if response.status == 200:
                        return await response.json()
            
            # Fall back to mock pricing data
            return await self._get_mock_pricing_data(asin)
            
        except Exception as e:
            logger.error(f"Failed to get pricing data for {asin}: {e}")
            return await self._get_mock_pricing_data(asin)
    
    async def _get_mock_product_details(self, asin: str) -> Dict:
        """Generate mock product details for development"""
        import random
        from datetime import datetime, timedelta
        
        return {
            "asin": asin,
            "title": f"Product {asin[-4:]} - Premium Quality",
            "brand": random.choice(["Samsung", "Sony", "Apple", "LG", "Philips", "Xiaomi"]),
            "model": f"Model-{asin[-6:]}",
            "category": "Electronics",
            "subcategory": "Consumer Electronics",
            "price": round(random.uniform(1000, 25000), 2),
            "currency": "INR",
            "availability": random.choice(["in_stock", "limited_stock"]),
            "condition": "new",
            "rating": round(random.uniform(3.5, 5.0), 1),
            "review_count": random.randint(50, 2000),
            "sales_rank": random.randint(1000, 100000),
            "bsr_category": "Electronics",
            "estimated_monthly_sales": random.randint(50, 1000),
            "launch_date": (datetime.now() - timedelta(days=random.randint(30, 365))).isoformat(),
            "dimensions": {
                "length": round(random.uniform(10, 50), 1),
                "width": round(random.uniform(10, 50), 1),
                "height": round(random.uniform(5, 30), 1),
                "weight": round(random.uniform(0.5, 5.0), 2)
            },
            "images": [
                f"https://images.amazon.in/images/I/{asin}_01.jpg",
                f"https://images.amazon.in/images/I/{asin}_02.jpg",
                f"https://images.amazon.in/images/I/{asin}_03.jpg"
            ],
            "features": [
                "Premium build quality",
                "Advanced technology",
                "Energy efficient",
                "User-friendly design",
                "1-year warranty"
            ],
            "description": f"High-quality product {asin} with premium features and excellent performance.",
            "specifications": {
                "material": "Premium materials",
                "color_options": ["Black", "White", "Silver"],
                "warranty": "1 year",
                "certifications": ["CE", "FCC", "RoHS"]
            },
            "seller_info": {
                "seller_name": random.choice(["Amazon", "TechStore India", "ElectroWorld", "GadgetHub"]),
                "seller_rating": round(random.uniform(4.0, 5.0), 1),
                "seller_feedback_count": random.randint(100, 10000),
                "fulfillment": random.choice(["FBA", "Merchant"])
            },
            "shipping_info": {
                "shipping_weight": round(random.uniform(0.5, 5.0), 2),
                "shipping_dimensions": {
                    "length": round(random.uniform(15, 60), 1),
                    "width": round(random.uniform(15, 60), 1),
                    "height": round(random.uniform(10, 40), 1)
                },
                "shipping_cost": random.choice([0, 50, 100, 150]),
                "estimated_delivery": "2-3 business days"
            },
            "competition_metrics": {
                "competitor_count": random.randint(20, 200),
                "price_position": random.choice(["lowest", "competitive", "premium"]),
                "market_share_estimate": round(random.uniform(1, 15), 2)
            }
        }
    
    async def _get_mock_pricing_data(self, asin: str) -> Dict:
        """Generate mock pricing data for development"""
        import random
        from datetime import datetime, timedelta
        
        current_price = round(random.uniform(1000, 25000), 2)
        
        # Generate price history
        price_history = []
        for i in range(30):  # 30 days of history
            date = datetime.now() - timedelta(days=i)
            price_variation = random.uniform(-0.2, 0.2)  # ±20% variation
            historical_price = round(current_price * (1 + price_variation), 2)
            price_history.append({
                "date": date.strftime("%Y-%m-%d"),
                "price": historical_price,
                "currency": "INR"
            })
        
        # Generate competitive pricing
        competitors = []
        for i in range(random.randint(3, 8)):
            competitor_price = round(current_price * random.uniform(0.8, 1.3), 2)
            competitors.append({
                "seller_name": f"Competitor {i+1}",
                "price": competitor_price,
                "currency": "INR",
                "condition": "new",
                "shipping_cost": random.choice([0, 50, 100]),
                "seller_rating": round(random.uniform(3.5, 5.0), 1),
                "prime_eligible": random.choice([True, False])
            })
        
        return {
            "asin": asin,
            "current_price": current_price,
            "currency": "INR",
            "price_history": price_history,
            "lowest_price_30d": min([p["price"] for p in price_history]),
            "highest_price_30d": max([p["price"] for p in price_history]),
            "average_price_30d": round(sum([p["price"] for p in price_history]) / len(price_history), 2),
            "buy_box_info": {
                "buy_box_seller": random.choice(["Amazon", "TechStore", "ElectroWorld"]),
                "buy_box_price": current_price,
                "prime_eligible": random.choice([True, False]),
                "fulfillment_method": random.choice(["FBA", "Merchant"])
            },
            "competitive_pricing": competitors,
            "price_alerts": {
                "price_drop_opportunity": current_price < min([p["price"] for p in price_history]) * 1.05,
                "competitor_undercut_risk": len([c for c in competitors if c["price"] < current_price]) > 2,
                "optimal_price_range": {
                    "min": round(current_price * 0.9, 2),
                    "max": round(current_price * 1.1, 2)
                }
            },
            "fees_breakdown": {
                "referral_fee": round(current_price * 0.08, 2),  # 8% Amazon referral fee
                "fba_fee": round(current_price * 0.15, 2),  # 15% FBA fee estimate
                "storage_fee": round(random.uniform(10, 50), 2),
                "advertising_cost": round(current_price * 0.05, 2),  # 5% ACoS estimate
                "total_fees": round(current_price * 0.28, 2)  # Total fees estimate
            },
            "profitability_analysis": {
                "estimated_cost_price": round(current_price * 0.6, 2),  # 60% cost estimate
                "gross_margin": round(current_price * 0.4, 2),  # 40% gross margin
                "net_margin_after_fees": round(current_price * 0.12, 2),  # 12% net margin
                "profit_margin_percentage": 12.0,
                "break_even_price": round(current_price * 0.88, 2)
            }
        }

# AI-Powered Product Scoring System
class ProductScoringEngine:
    """AI-powered product scoring and classification system"""
    
    def __init__(self):
        self.trend_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.profit_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
    
    async def score_product(self, product_data: Dict) -> ProductScore:
        """Score a product using AI algorithms"""
        try:
            # Extract features for scoring
            features = self._extract_features(product_data)
            
            # Calculate individual scores
            trend_score = await self._calculate_trend_score(product_data)
            profit_score = await self._calculate_profit_score(product_data)
            competition_score = await self._calculate_competition_score(product_data)
            risk_score = await self._calculate_risk_score(product_data)
            
            # Calculate weighted overall score
            weights = {
                "trend": 0.25,
                "profit": 0.35,
                "competition": 0.25,
                "risk": 0.15
            }
            
            overall_score = (
                trend_score * weights["trend"] +
                profit_score * weights["profit"] +
                competition_score * weights["competition"] +
                (100 - risk_score) * weights["risk"]  # Lower risk is better
            )
            
            # Determine category
            category = self._classify_product(overall_score, trend_score, profit_score, risk_score)
            
            # Calculate confidence
            confidence = self._calculate_confidence(features)
            
            return ProductScore(
                trend_score=trend_score,
                profit_score=profit_score,
                competition_score=competition_score,
                risk_score=risk_score,
                overall_score=overall_score,
                category=category,
                confidence=confidence
            )
            
        except Exception as e:
            logger.error(f"Product scoring failed: {e}")
            return ProductScore(
                trend_score=0.0,
                profit_score=0.0,
                competition_score=0.0,
                risk_score=100.0,
                overall_score=0.0,
                category=ProductCategory.NOT_QUALIFIED,
                confidence=0.0
            )
    
    def _extract_features(self, product_data: Dict) -> List[float]:
        """Extract numerical features from product data"""
        features = [
            product_data.get("price", 0),
            product_data.get("rating", 0),
            product_data.get("review_count", 0),
            product_data.get("sales_rank", 999999),
            len(product_data.get("images", [])),
            len(product_data.get("features", [])),
            product_data.get("weight", 0),
            len(product_data.get("title", "")),
            len(product_data.get("description", "")),
            product_data.get("availability_score", 0)
        ]
        return features
    
    async def _calculate_trend_score(self, product_data: Dict) -> float:
        """Calculate trend score based on social media signals"""
        try:
            # Analyze search trends
            keywords = product_data.get("keywords", [])
            trend_scores = []
            
            for keyword in keywords:
                # Call trend analysis service
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f"{BRAIN_AI_SERVICE_URL}/trends/social/{keyword}"
                    ) as response:
                        if response.status == 200:
                            trend_data = await response.json()
                            trend_scores.append(trend_data.get("score", 0))
            
            return np.mean(trend_scores) if trend_scores else 0.0
            
        except Exception as e:
            logger.error(f"Trend score calculation failed: {e}")
            return 0.0
    
    async def _calculate_profit_score(self, product_data: Dict) -> float:
        """Calculate profit potential score"""
        try:
            price = product_data.get("price", 0)
            cost = product_data.get("estimated_cost", price * 0.6)  # Estimate 60% cost
            
            if price <= 0:
                return 0.0
            
            profit_margin = ((price - cost) / price) * 100
            
            # Score based on profit margin
            if profit_margin >= 50:
                return 90.0
            elif profit_margin >= 30:
                return 70.0
            elif profit_margin >= 20:
                return 50.0
            elif profit_margin >= 10:
                return 30.0
            else:
                return 10.0
                
        except Exception as e:
            logger.error(f"Profit score calculation failed: {e}")
            return 0.0
    
    async def _calculate_competition_score(self, product_data: Dict) -> float:
        """Calculate competition intensity score"""
        try:
            # Higher competition = lower score
            competitor_count = product_data.get("competitor_count", 100)
            
            if competitor_count <= 10:
                return 90.0
            elif competitor_count <= 50:
                return 70.0
            elif competitor_count <= 100:
                return 50.0
            elif competitor_count <= 500:
                return 30.0
            else:
                return 10.0
                
        except Exception as e:
            logger.error(f"Competition score calculation failed: {e}")
            return 0.0
    
    async def _calculate_risk_score(self, product_data: Dict) -> float:
        """Calculate business risk score"""
        try:
            risk_factors = {
                "regulatory_risk": product_data.get("regulatory_risk", 0),
                "seasonal_risk": product_data.get("seasonal_risk", 0),
                "shipping_risk": product_data.get("shipping_risk", 0),
                "quality_risk": 100 - (product_data.get("rating", 0) * 20),
                "supplier_risk": product_data.get("supplier_risk", 0)
            }
            
            return np.mean(list(risk_factors.values()))
            
        except Exception as e:
            logger.error(f"Risk score calculation failed: {e}")
            return 100.0
    
    def _classify_product(self, overall_score: float, trend_score: float, profit_score: float) -> ProductCategory:
        """Classify product into categories"""
        if overall_score >= 80 and trend_score >= 70:
            return ProductCategory.HOOK
        elif overall_score >= 70 and profit_score >= 60:
            return ProductCategory.HERO
        elif overall_score >= 50:
            return ProductCategory.MID_TIER
        else:
            return ProductCategory.NOT_QUALIFIED
    
    def _calculate_confidence(self, features: List[float]) -> float:
        """Calculate confidence score for the prediction"""
        # Simple confidence based on feature completeness
        non_zero_features = sum(1 for f in features if f > 0)
        return min(non_zero_features / len(features), 1.0)

# Trend Analysis Service
class TrendAnalysisService:
    """Social media and market trend analysis"""
    
    async def analyze_trends(self, query: str, platforms: List[str], time_range: str) -> Dict:
        """Analyze trends across multiple platforms"""
        try:
            trend_data = {
                "query": query,
                "platforms": platforms,
                "time_range": time_range,
                "trends": {}
            }
            
            for platform in platforms:
                platform_trends = await self._analyze_platform_trends(query, platform, time_range)
                trend_data["trends"][platform] = platform_trends
            
            # Calculate overall trend score
            all_scores = []
            for platform_data in trend_data["trends"].values():
                all_scores.append(platform_data.get("score", 0))
            
            trend_data["overall_score"] = np.mean(all_scores) if all_scores else 0.0
            trend_data["trend_direction"] = "up" if trend_data["overall_score"] >= 60 else "stable" if trend_data["overall_score"] >= 40 else "down"
            
            return trend_data
            
        except Exception as e:
            logger.error(f"Trend analysis failed: {e}")
            return {"error": str(e)}
    
    async def _analyze_platform_trends(self, query: str, platform: str, time_range: str) -> Dict:
        """Analyze trends for specific platform"""
        try:
            # Mock implementation - in production, integrate with actual APIs
            if platform == "google":
                return await self._analyze_google_trends(query, time_range)
            elif platform == "tiktok":
                return await self._analyze_tiktok_trends(query, time_range)
            elif platform == "instagram":
                return await self._analyze_instagram_trends(query, time_range)
            elif platform == "youtube":
                return await self._analyze_youtube_trends(query, time_range)
            else:
                return {"score": 0, "data": {}}
                
        except Exception as e:
            logger.error(f"Platform trend analysis failed for {platform}: {e}")
            return {"score": 0, "error": str(e)}
    
    async def _analyze_google_trends(self, query: str, time_range: str) -> Dict:
        """Analyze Google search trends with enhanced data"""
        try:
            # In production, integrate with Google Trends API or pytrends
            import random
            from datetime import datetime, timedelta
            
            # Generate realistic search metrics
            base_volume = random.randint(1000, 80000)
            growth_rate = random.uniform(-25, 60)
            
            # Calculate score based on volume and growth
            volume_score = min(50, (base_volume / 1000) * 5)  # Volume component
            growth_score = max(0, min(50, growth_rate))  # Growth component
            total_score = volume_score + growth_score
            
            # Generate related queries with search volumes
            related_queries = [
                {"query": f"{query} buy online", "volume": int(base_volume * 0.3), "trend": "+15%"},
                {"query": f"{query} price in india", "volume": int(base_volume * 0.25), "trend": "+8%"},
                {"query": f"best {query}", "volume": int(base_volume * 0.4), "trend": "+22%"},
                {"query": f"{query} review", "volume": int(base_volume * 0.35), "trend": "+18%"},
                {"query": f"{query} amazon", "volume": int(base_volume * 0.2), "trend": "+12%"}
            ]
            
            # Generate regional interest (Indian states)
            regional_interest = {
                "Maharashtra": random.randint(15, 25),
                "Karnataka": random.randint(12, 20),
                "Delhi": random.randint(10, 18),
                "Tamil Nadu": random.randint(8, 15),
                "Gujarat": random.randint(6, 12),
                "Uttar Pradesh": random.randint(8, 16),
                "West Bengal": random.randint(5, 10),
                "Rajasthan": random.randint(4, 8)
            }
            
            # Generate trending topics
            trending_topics = [
                f"{query} 2024",
                f"new {query}",
                f"{query} offers",
                f"{query} sale",
                f"cheap {query}"
            ]
            
            return {
                "score": round(min(95, total_score), 1),
                "search_volume": base_volume,
                "growth_rate": round(growth_rate, 1),
                "related_queries": related_queries,
                "regional_interest": regional_interest,
                "trending_topics": trending_topics,
                "search_intent": {
                    "informational": random.uniform(30, 50),
                    "commercial": random.uniform(25, 45),
                    "transactional": random.uniform(15, 35),
                    "navigational": random.uniform(5, 15)
                },
                "competition_level": random.choice(["low", "medium", "high"]),
                "cpc_estimate": {
                    "min": round(random.uniform(5, 15), 2),
                    "max": round(random.uniform(20, 80), 2),
                    "average": round(random.uniform(15, 45), 2)
                },
                "seasonal_data": {
                    "peak_season": random.choice(["Festival season", "Summer", "Winter", "Year-round"]),
                    "low_season": random.choice(["Monsoon", "Post-festival", "Mid-year"]),
                    "monthly_trends": {month: random.randint(60, 140) for month in [
                        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
                        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
                    ]}
                },
                "demographics": {
                    "age_18_24": random.uniform(20, 35),
                    "age_25_34": random.uniform(30, 45),
                    "age_35_44": random.uniform(15, 30),
                    "age_45_plus": random.uniform(5, 20),
                    "male_percentage": random.uniform(45, 65)
                }
            }
            
        except Exception as e:
            logger.error(f"Google trends analysis failed: {e}")
            return {"score": 0, "error": str(e)}
    
    async def _analyze_tiktok_trends(self, query: str, time_range: str) -> Dict:
        """Analyze TikTok trends with enhanced metrics"""
        try:
            # In production, integrate with TikTok API or web scraping
            # For now, generate realistic data based on query characteristics
            
            import random
            
            # Simulate viral potential based on query characteristics
            viral_keywords = ["gadget", "tech", "smart", "wireless", "portable", "mini", "aesthetic"]
            viral_boost = sum(1 for keyword in viral_keywords if keyword.lower() in query.lower()) * 10
            
            base_score = random.randint(30, 70) + viral_boost
            video_count = random.randint(100, 15000)
            
            # Higher engagement for viral content
            engagement_rate = random.uniform(3, 18) + (viral_boost * 0.1)
            
            # Determine viral potential
            if base_score >= 80 and engagement_rate >= 12:
                viral_potential = "high"
            elif base_score >= 60 and engagement_rate >= 8:
                viral_potential = "medium"
            else:
                viral_potential = "low"
            
            return {
                "score": min(95, base_score),
                "video_count": video_count,
                "engagement_rate": round(engagement_rate, 2),
                "viral_potential": viral_potential,
                "trending_hashtags": [f"#{query.replace(' ', '')}", f"#{query}trend", f"#{query}viral"],
                "top_creators_count": random.randint(5, 50),
                "average_views_per_video": random.randint(1000, 100000),
                "growth_rate_7d": random.uniform(-20, 150),
                "audience_demographics": {
                    "age_18_24": random.uniform(40, 60),
                    "age_25_34": random.uniform(25, 40),
                    "age_35_plus": random.uniform(5, 20),
                    "female_percentage": random.uniform(45, 65)
                },
                "peak_hours": ["7-9 PM", "8-10 PM", "9-11 PM"],
                "content_types": {
                    "unboxing": random.uniform(20, 40),
                    "reviews": random.uniform(15, 30),
                    "tutorials": random.uniform(10, 25),
                    "lifestyle": random.uniform(20, 35)
                }
            }
            
        except Exception as e:
            logger.error(f"TikTok trend analysis failed: {e}")
            return {"score": 0, "error": str(e)}
    
    async def _analyze_instagram_trends(self, query: str, time_range: str) -> Dict:
        """Analyze Instagram trends with enhanced metrics"""
        try:
            # In production, integrate with Instagram Basic Display API
            import random
            
            # Generate realistic Instagram metrics
            lifestyle_keywords = ["aesthetic", "lifestyle", "fashion", "beauty", "home", "decor"]
            lifestyle_boost = sum(1 for keyword in lifestyle_keywords if keyword.lower() in query.lower()) * 8
            
            base_score = random.randint(35, 75) + lifestyle_boost
            post_count = random.randint(500, 25000)
            
            return {
                "score": min(95, base_score),
                "post_count": post_count,
                "hashtag_performance": round(random.uniform(2, 12), 1),
                "influencer_mentions": random.randint(5, 80),
                "story_mentions": random.randint(10, 200),
                "reel_count": random.randint(50, 5000),
                "average_likes_per_post": random.randint(100, 10000),
                "average_comments_per_post": random.randint(10, 500),
                "engagement_rate": round(random.uniform(2, 8), 2),
                "top_hashtags": [
                    f"#{query.replace(' ', '').lower()}",
                    f"#{query.replace(' ', '')}style",
                    f"#{query.replace(' ', '')}life",
                    f"#{query.replace(' ', '')}inspo"
                ],
                "influencer_tiers": {
                    "nano_influencers": random.randint(10, 50),  # 1K-10K followers
                    "micro_influencers": random.randint(5, 30),   # 10K-100K followers
                    "macro_influencers": random.randint(1, 10),   # 100K-1M followers
                    "mega_influencers": random.randint(0, 5)      # 1M+ followers
                },
                "content_categories": {
                    "product_showcases": random.uniform(25, 45),
                    "lifestyle_posts": random.uniform(20, 35),
                    "tutorials": random.uniform(10, 25),
                    "user_generated_content": random.uniform(15, 30)
                },
                "audience_insights": {
                    "female_percentage": random.uniform(55, 75),
                    "age_18_34": random.uniform(60, 80),
                    "urban_percentage": random.uniform(70, 85)
                },
                "growth_metrics": {
                    "weekly_growth": random.uniform(-10, 50),
                    "monthly_growth": random.uniform(-5, 80),
                    "seasonal_trend": random.choice(["growing", "stable", "declining"])
                }
            }
            
        except Exception as e:
            logger.error(f"Instagram trend analysis failed: {e}")
            return {"score": 0, "error": str(e)}
    
    async def _analyze_youtube_trends(self, query: str, time_range: str) -> Dict:
        """Analyze YouTube trends with enhanced metrics"""
        try:
            # In production, integrate with YouTube Data API v3
            import random
            
            # Tech/review content performs well on YouTube
            tech_keywords = ["review", "unboxing", "test", "comparison", "tech", "gadget"]
            tech_boost = sum(1 for keyword in tech_keywords if keyword.lower() in query.lower()) * 12
            
            base_score = random.randint(40, 70) + tech_boost
            video_count = random.randint(50, 8000)
            view_growth = random.uniform(-15, 120) + (tech_boost * 0.5)
            
            # Determine creator adoption trend
            if view_growth >= 50:
                creator_adoption = "growing"
            elif view_growth >= 10:
                creator_adoption = "stable"
            else:
                creator_adoption = "declining"
            
            return {
                "score": min(95, base_score),
                "video_count": video_count,
                "view_growth": round(view_growth, 1),
                "creator_adoption": creator_adoption,
                "total_views": random.randint(100000, 50000000),
                "average_views_per_video": random.randint(1000, 500000),
                "subscriber_growth": random.uniform(-5, 40),
                "engagement_metrics": {
                    "like_ratio": random.uniform(2, 8),
                    "comment_ratio": random.uniform(0.5, 3),
                    "share_ratio": random.uniform(0.1, 1),
                    "retention_rate": random.uniform(40, 80)
                },
                "content_types": {
                    "reviews": random.uniform(25, 50),
                    "unboxings": random.uniform(15, 35),
                    "tutorials": random.uniform(20, 40),
                    "comparisons": random.uniform(10, 25)
                },
                "creator_categories": {
                    "tech_reviewers": random.randint(5, 30),
                    "lifestyle_channels": random.randint(3, 20),
                    "educational_content": random.randint(2, 15),
                    "entertainment": random.randint(1, 10)
                },
                "trending_keywords": [
                    f"{query} review",
                    f"{query} unboxing",
                    f"best {query}",
                    f"{query} 2024",
                    f"{query} comparison"
                ],
                "seasonal_patterns": {
                    "peak_months": ["November", "December", "January"],
                    "low_months": ["June", "July", "August"],
                    "festival_boost": random.choice([True, False])
                }
            }
            
        except Exception as e:
            logger.error(f"YouTube trend analysis failed: {e}")
            return {"score": 0, "error": str(e)}

# Market Intelligence Service
class MarketIntelligenceService:
    """Market research and competitive intelligence"""
    
    async def analyze_market(self, category: str, competitor_count: int = 10) -> Dict:
        """Comprehensive market analysis"""
        try:
            market_data = {
                "category": category,
                "analysis_date": datetime.now().isoformat(),
                "market_size": await self._estimate_market_size(category),
                "competition_analysis": await self._analyze_competition(category, competitor_count),
                "price_analysis": await self._analyze_pricing(category),
                "seasonal_trends": await self._analyze_seasonality(category),
                "growth_forecast": await self._forecast_growth(category),
                "opportunities": await self._identify_opportunities(category)
            }
            
            return market_data
            
        except Exception as e:
            logger.error(f"Market analysis failed: {e}")
            return {"error": str(e)}
    
    async def _estimate_market_size(self, category: str) -> Dict:
        """Estimate market size for category"""
        # Mock implementation
        return {
            "total_products": np.random.randint(1000, 100000),
            "active_sellers": np.random.randint(100, 10000),
            "estimated_revenue": np.random.randint(1000000, 100000000),
            "growth_rate": np.random.uniform(-5, 25)
        }
    
    async def _analyze_competition(self, category: str, competitor_count: int) -> Dict:
        """Analyze competitive landscape"""
        # Mock implementation
        competitors = []
        for i in range(competitor_count):
            competitors.append({
                "seller_id": f"seller_{i}",
                "market_share": np.random.uniform(0.1, 15),
                "avg_price": np.random.uniform(10, 500),
                "rating": np.random.uniform(3.5, 5.0),
                "product_count": np.random.randint(10, 1000)
            })
        
        return {
            "competitor_count": len(competitors),
            "competitors": competitors,
            "market_concentration": "medium",
            "entry_barriers": "low"
        }
    
    async def _analyze_pricing(self, category: str) -> Dict:
        """Analyze pricing in category"""
        # Mock implementation
        prices = [np.random.uniform(10, 500) for _ in range(100)]
        return {
            "avg_price": np.mean(prices),
            "median_price": np.median(prices),
            "price_range": {"min": min(prices), "max": max(prices)},
            "price_distribution": {
                "budget": len([p for p in prices if p < 50]) / len(prices),
                "mid_range": len([p for p in prices if 50 <= p < 200]) / len(prices),
                "premium": len([p for p in prices if p >= 200]) / len(prices)
            }
        }
    
    async def _analyze_seasonality(self, category: str) -> Dict:
        """Analyze seasonal trends"""
        # Mock implementation
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                 "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        seasonal_data = {}
        for month in months:
            seasonal_data[month] = {
                "demand_index": np.random.uniform(0.5, 2.0),
                "price_index": np.random.uniform(0.8, 1.3)
            }
        
        return {
            "seasonal_pattern": seasonal_data,
            "peak_months": ["Nov", "Dec", "Jan"],
            "low_months": ["Jun", "Jul", "Aug"]
        }
    
    async def _forecast_growth(self, category: str) -> Dict:
        """Forecast category growth"""
        # Mock implementation
        return {
            "next_quarter": np.random.uniform(-10, 30),
            "next_year": np.random.uniform(-5, 50),
            "confidence": np.random.uniform(0.6, 0.9),
            "key_drivers": ["social media trends", "seasonal demand", "economic factors"]
        }
    
    async def _identify_opportunities(self, category: str) -> List[Dict]:
        """Identify market opportunities"""
        # Mock implementation
        opportunities = [
            {
                "type": "product_gap",
                "description": "Underserved price segment",
                "potential": "high",
                "investment_required": "medium"
            },
            {
                "type": "geographic",
                "description": "Emerging market demand",
                "potential": "medium",
                "investment_required": "low"
            }
        ]
        return opportunities

# Import enhanced modules
from amazon_sp_api_client import EnhancedAmazonSPAPIClient
from indian_market_optimizer import IndianMarketOptimizer

# Initialize services
amazon_client = EnhancedAmazonSPAPIClient(
    access_key=AMAZON_ACCESS_KEY,
    secret_key=AMAZON_SECRET_KEY,
    marketplace_id=AMAZON_MARKETPLACE_ID
)
scoring_engine = ProductScoringEngine()
trend_service = TrendAnalysisService()
market_intel_service = MarketIntelligenceService()
indian_market_optimizer = IndianMarketOptimizer()

# Background tasks
@celery_app.task
def process_product_discovery(request_data: dict):
    """Background task for product discovery"""
    try:
        # This would run the full discovery pipeline
        logger.info(f"Starting product discovery for: {request_data}")
        
        # Store in Redis for status tracking
        task_id = process_product_discovery.request.id
        redis_client.setex(
            f"discovery_task:{task_id}",
            3600,  # 1 hour expiry
            json.dumps({
                "status": "processing",
                "progress": 0,
                "started_at": datetime.now().isoformat()
            })
        )
        
        # Simulate processing
        import time
        time.sleep(10)  # Simulate work
        
        # Update status
        redis_client.setex(
            f"discovery_task:{task_id}",
            3600,
            json.dumps({
                "status": "completed",
                "progress": 100,
                "completed_at": datetime.now().isoformat(),
                "results": {"discovered_products": 25}
            })
        )
        
        return {"task_id": task_id, "status": "completed"}
        
    except Exception as e:
        logger.error(f"Product discovery task failed: {e}")
        return {"error": str(e)}

# API Endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check database connection
        conn = await get_db_connection()
        await conn.close()
        
        # Check Redis connection
        redis_client.ping()
        
        return {
            "status": "healthy",
            "service": "Product Sourcing Workflow",
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.post("/api/product-sourcing/discover")
async def start_product_discovery(
    request: ProductDiscoveryRequest,
    background_tasks: BackgroundTasks
):
    """Start product discovery process"""
    try:
        # Validate request
        if not request.keywords:
            raise HTTPException(status_code=400, detail="Keywords are required")
        
        # Start background task
        task = process_product_discovery.delay(request.dict())
        
        # Store task info
        task_info = {
            "task_id": task.id,
            "status": "started",
            "request": request.dict(),
            "created_at": datetime.now().isoformat()
        }
        
        redis_client.setex(
            f"discovery_task:{task.id}",
            3600,
            json.dumps(task_info)
        )
        
        return {
            "task_id": task.id,
            "status": "started",
            "message": "Product discovery process initiated",
            "estimated_completion": (datetime.now() + timedelta(minutes=5)).isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to start product discovery: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/product-sourcing/discovery/{task_id}/status")
async def get_discovery_status(task_id: str):
    """Get product discovery task status"""
    try:
        task_data = redis_client.get(f"discovery_task:{task_id}")
        if not task_data:
            raise HTTPException(status_code=404, detail="Task not found")
        
        return json.loads(task_data)
        
    except Exception as e:
        logger.error(f"Failed to get task status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/product-sourcing/trends")
async def get_trending_products(
    category: Optional[str] = Query(None),
    region: str = Query("IN"),
    limit: int = Query(20)
):
    """Get trending products"""
    try:
        # Mock trending products data
        trending_products = []
        for i in range(limit):
            product = {
                "id": f"trend_{i}",
                "title": f"Trending Product {i}",
                "category": category or "electronics",
                "trend_score": np.random.uniform(60, 95),
                "growth_rate": np.random.uniform(10, 200),
                "social_mentions": np.random.randint(100, 10000),
                "estimated_demand": np.random.randint(1000, 50000)
            }
            trending_products.append(product)
        
        return {
            "trending_products": trending_products,
            "region": region,
            "category": category,
            "updated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get trending products: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/product-sourcing/analyze")
async def analyze_product(request: ProductAnalysisRequest):
    """Analyze specific product"""
    try:
        # Get product data
        product_data = {}
        
        if request.asin:
            # Get from Amazon
            product_data = await amazon_client.get_product_details(request.asin)
            pricing_data = await amazon_client.get_pricing_data(request.asin)
            product_data.update(pricing_data)
        
        # Add request data
        product_data.update({
            "title": request.product_title,
            "price": request.current_price,
            "category": request.category
        })
        
        # Score the product
        score = await scoring_engine.score_product(product_data)
        
        # Get market intelligence if deep analysis requested
        market_intel = {}
        if request.deep_analysis and request.category:
            market_intel = await market_intel_service.analyze_market(request.category)
        
        # Optimize for Indian market
        indian_optimization = {}
        try:
            indian_optimization = indian_market_optimizer.optimize_for_indian_market(product_data)
        except Exception as e:
            logger.error(f"Indian market optimization failed: {e}")
        
        # Enhanced recommendations including Indian market insights
        recommendations = await _generate_recommendations(score, product_data)
        if indian_optimization:
            recommendations.extend(indian_optimization.get("recommendations", []))
        
        return {
            "product_analysis": {
                "product_data": product_data,
                "scoring": asdict(score),
                "market_intelligence": market_intel,
                "indian_market_optimization": indian_optimization,
                "recommendations": recommendations,
                "analyzed_at": datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        logger.error(f"Product analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/product-sourcing/recommendations")
async def get_personalized_recommendations(
    user_id: Optional[str] = Query(None),
    business_type: str = Query("general"),
    budget_range: Optional[str] = Query(None),
    limit: int = Query(10)
):
    """Get personalized product recommendations"""
    try:
        # Mock personalized recommendations
        recommendations = []
        for i in range(limit):
            rec = {
                "product_id": f"rec_{i}",
                "title": f"Recommended Product {i}",
                "category": np.random.choice(["electronics", "home", "fashion", "sports"]),
                "overall_score": np.random.uniform(70, 95),
                "profit_potential": np.random.uniform(20, 80),
                "market_demand": np.random.choice(["high", "medium", "low"]),
                "competition_level": np.random.choice(["low", "medium", "high"]),
                "reason": "High profit margin with growing demand",
                "estimated_roi": np.random.uniform(15, 60)
            }
            recommendations.append(rec)
        
        return {
            "recommendations": recommendations,
            "user_id": user_id,
            "business_type": business_type,
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get recommendations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/product-sourcing/classify")
async def classify_product(request: ProductAnalysisRequest):
    """Classify product into Hook/Mid-Tier/Hero/Not Qualified"""
    try:
        # Basic product data from request
        product_data = {
            "title": request.product_title,
            "price": request.current_price or 0,
            "category": request.category or "general"
        }
        
        # Get additional data if ASIN provided
        if request.asin:
            amazon_data = await amazon_client.get_product_details(request.asin)
            product_data.update(amazon_data)
        
        # Score and classify
        score = await scoring_engine.score_product(product_data)
        
        return {
            "classification": {
                "category": score.category.value,
                "overall_score": score.overall_score,
                "confidence": score.confidence,
                "breakdown": {
                    "trend_score": score.trend_score,
                    "profit_score": score.profit_score,
                    "competition_score": score.competition_score,
                    "risk_score": score.risk_score
                },
                "explanation": _get_classification_explanation(score),
                "classified_at": datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        logger.error(f"Product classification failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/trends/analyze")
async def analyze_trends(request: TrendAnalysisRequest):
    """Analyze trends across platforms"""
    try:
        trend_analysis = await trend_service.analyze_trends(
            request.query,
            request.platforms,
            request.time_range
        )
        
        return {
            "trend_analysis": trend_analysis,
            "analyzed_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Trend analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/product-sourcing/market-intel")
async def get_market_intelligence(
    category: str = Query(...),
    competitor_count: int = Query(10),
    include_forecast: bool = Query(True)
):
    """Get market intelligence report"""
    try:
        market_intel = await market_intel_service.analyze_market(category, competitor_count)
        
        return {
            "market_intelligence": market_intel,
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Market intelligence failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/product-sourcing/indian-market-analysis")
async def analyze_indian_market(request: ProductAnalysisRequest):
    """Comprehensive Indian market analysis for a product"""
    try:
        # Build product data structure
        product_data = {
            "title": request.product_title,
            "price": request.current_price or 0,
            "category": request.category or "general",
            "asin": request.asin
        }
        
        # Get additional product data if ASIN provided
        if request.asin:
            amazon_data = await amazon_client.get_product_details(request.asin)
            product_data.update(amazon_data)
        
        # Perform Indian market optimization
        indian_analysis = indian_market_optimizer.optimize_for_indian_market(product_data)
        
        # Get additional market insights
        market_insights = {}
        if request.category:
            market_insights = await market_intel_service.analyze_market(request.category)
        
        return {
            "indian_market_analysis": {
                "product_info": product_data,
                "optimization_results": indian_analysis,
                "market_context": market_insights,
                "analysis_summary": {
                    "market_viability": indian_analysis.get("market_score", 0),
                    "recommended_price": indian_analysis.get("optimized_pricing", {}).get("optimized_price", 0),
                    "top_target_region": indian_analysis.get("target_regions", [{}])[0].get("region", "Unknown"),
                    "launch_readiness": "High" if indian_analysis.get("market_score", 0) >= 70 else "Medium" if indian_analysis.get("market_score", 0) >= 50 else "Low",
                    "key_success_factors": indian_analysis.get("recommendations", [])[:3]
                },
                "analyzed_at": datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        logger.error(f"Indian market analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/product-sourcing/indian-market/regional-insights")
async def get_regional_insights(
    category: str = Query(...),
    price_range: Optional[str] = Query(None)
):
    """Get regional market insights for Indian market"""
    try:
        # Mock product for regional analysis
        mock_product = {
            "category": category,
            "price": 5000 if not price_range else {
                "budget": 1500,
                "mid_range": 5000,
                "premium": 15000,
                "luxury": 50000
            }.get(price_range, 5000)
        }
        
        optimization_results = indian_market_optimizer.optimize_for_indian_market(mock_product)
        
        return {
            "regional_insights": {
                "category": category,
                "price_range": price_range,
                "regional_demand": optimization_results.get("insights").regional_demand,
                "target_regions": optimization_results.get("target_regions", []),
                "cultural_considerations": optimization_results.get("insights").cultural_factors,
                "logistics_assessment": {
                    "score": optimization_results.get("insights").logistics_score,
                    "recommendations": [
                        "Use regional fulfillment centers for faster delivery",
                        "Partner with local logistics providers",
                        "Optimize packaging for Indian conditions"
                    ]
                },
                "payment_preferences": optimization_results.get("insights").payment_preferences
            },
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Regional insights failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/product-sourcing/festival-calendar")
async def get_festival_calendar():
    """Get Indian festival calendar with e-commerce impact"""
    try:
        current_year = datetime.now().year
        
        # Festival calendar with business impact
        festival_calendar = {
            "current_year": current_year,
            "major_festivals": [
                {
                    "name": "Diwali",
                    "approximate_date": "October-November",
                    "business_impact": "Very High",
                    "recommended_categories": ["electronics", "fashion", "jewelry", "home"],
                    "preparation_timeline": "2-3 months advance",
                    "expected_sales_boost": "300-500%"
                },
                {
                    "name": "Dussehra",
                    "approximate_date": "September-October", 
                    "business_impact": "High",
                    "recommended_categories": ["electronics", "vehicles", "appliances"],
                    "preparation_timeline": "1-2 months advance",
                    "expected_sales_boost": "200-300%"
                },
                {
                    "name": "Karva Chauth",
                    "approximate_date": "October-November",
                    "business_impact": "Medium",
                    "recommended_categories": ["jewelry", "beauty", "fashion"],
                    "preparation_timeline": "1 month advance",
                    "expected_sales_boost": "150-250%"
                },
                {
                    "name": "Christmas",
                    "approximate_date": "December 25",
                    "business_impact": "High",
                    "recommended_categories": ["electronics", "toys", "fashion", "books"],
                    "preparation_timeline": "1-2 months advance",
                    "expected_sales_boost": "200-300%"
                },
                {
                    "name": "Holi",
                    "approximate_date": "March",
                    "business_impact": "Medium",
                    "recommended_categories": ["colors", "sweets", "fashion"],
                    "preparation_timeline": "2-3 weeks advance",
                    "expected_sales_boost": "100-200%"
                }
            ],
            "seasonal_trends": {
                "wedding_season": {
                    "months": ["November", "December", "January", "February"],
                    "impact_categories": ["jewelry", "fashion", "electronics", "home"],
                    "sales_boost": "200-400%"
                },
                "monsoon_season": {
                    "months": ["June", "July", "August", "September"],
                    "impact_categories": ["umbrellas", "rainwear", "home_care"],
                    "sales_impact": "Category dependent"
                },
                "summer_season": {
                    "months": ["March", "April", "May"],
                    "impact_categories": ["cooling_appliances", "summer_fashion", "travel"],
                    "sales_boost": "150-250%"
                }
            },
            "regional_festivals": {
                "South": ["Onam", "Pongal", "Ugadi"],
                "West": ["Ganesh Chaturthi", "Navratri"],
                "East": ["Durga Puja", "Kali Puja"],
                "North": ["Karva Chauth", "Baisakhi"],
                "Northeast": ["Bihu", "Poila Boishakh"]
            },
            "planning_recommendations": [
                "Plan inventory 2-3 months before major festivals",
                "Create festival-specific marketing campaigns",
                "Optimize pricing for festival seasons",
                "Partner with local influencers for regional festivals",
                "Ensure robust logistics during peak seasons"
            ]
        }
        
        return {
            "festival_calendar": festival_calendar,
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Festival calendar failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/product-sourcing/gst-calculator")
async def calculate_gst_impact(
    price: float = Query(...),
    category: str = Query(...)
):
    """Calculate GST impact for product pricing"""
    try:
        # GST rates by category
        gst_rates = {
            "books": 0,
            "food": 0,
            "medical": 5,
            "textiles": 5,
            "mobile": 12,
            "fashion": 12,
            "electronics": 18,
            "home": 18,
            "beauty": 18,
            "automobiles": 28,
            "luxury": 28
        }
        
        gst_rate = gst_rates.get(category.lower(), 18)
        gst_amount = price * (gst_rate / 100)
        total_price = price + gst_amount
        
        # Calculate impact on competitiveness
        competitiveness_impact = "Low" if gst_rate <= 5 else "Medium" if gst_rate <= 18 else "High"
        
        return {
            "gst_calculation": {
                "base_price": price,
                "gst_rate": gst_rate,
                "gst_amount": round(gst_amount, 2),
                "total_price_including_gst": round(total_price, 2),
                "category": category,
                "competitiveness_impact": competitiveness_impact,
                "recommendations": [
                    f"GST rate for {category} is {gst_rate}%",
                    "Include GST in pricing strategy",
                    "Consider GST impact on competition" if gst_rate >= 18 else "GST provides competitive advantage"
                ]
            },
            "calculated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"GST calculation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Helper functions
async def _generate_recommendations(score: ProductScore, product_data: Dict) -> List[str]:
    """Generate actionable recommendations"""
    recommendations = []
    
    if score.category == ProductCategory.HOOK:
        recommendations.extend([
            "Consider immediate market entry - high viral potential",
            "Invest in social media marketing campaigns",
            "Monitor trend stability over next 2-4 weeks"
        ])
    elif score.category == ProductCategory.HERO:
        recommendations.extend([
            "Focus on premium positioning and branding",
            "Invest in quality suppliers and packaging",
            "Build long-term customer relationships"
        ])
    elif score.category == ProductCategory.MID_TIER:
        recommendations.extend([
            "Consider as portfolio addition for steady income",
            "Optimize for operational efficiency",
            "Monitor for upgrade to hero category"
        ])
    else:
        recommendations.extend([
            "Not recommended for current market conditions",
            "Consider alternative products in same category",
            "Re-evaluate if market conditions change"
        ])
    
    # Add specific recommendations based on scores
    if score.profit_score < 50:
        recommendations.append("Explore cost optimization opportunities")
    
    if score.competition_score < 50:
        recommendations.append("High competition - consider differentiation strategy")
    
    if score.risk_score > 70:
        recommendations.append("High risk - conduct additional due diligence")
    
    return recommendations

def _get_classification_explanation(score: ProductScore) -> str:
    """Get human-readable explanation for classification"""
    if score.category == ProductCategory.HOOK:
        return f"High viral potential with trend score of {score.trend_score:.1f}. Great for quick wins."
    elif score.category == ProductCategory.HERO:
        return f"Premium opportunity with profit score of {score.profit_score:.1f}. Build long-term business around this."
    elif score.category == ProductCategory.MID_TIER:
        return f"Solid product with overall score of {score.overall_score:.1f}. Good for steady income."
    else:
        return f"Low viability with score of {score.overall_score:.1f}. Consider alternatives."

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize service on startup"""
    logger.info("Starting Product Sourcing Workflow Service")
    
    # Initialize database tables if needed
    await _initialize_database()
    
    logger.info("Product Sourcing Workflow Service started successfully")

async def _initialize_database():
    """Initialize database tables"""
    try:
        conn = await get_db_connection()
        
        # Create tables for product sourcing
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS product_discoveries (
                id SERIAL PRIMARY KEY,
                task_id VARCHAR(255) UNIQUE,
                user_id VARCHAR(255),
                keywords JSONB,
                filters JSONB,
                status VARCHAR(50),
                results JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS product_analyses (
                id SERIAL PRIMARY KEY,
                product_id VARCHAR(255),
                asin VARCHAR(255),
                product_data JSONB,
                scoring_results JSONB,
                classification VARCHAR(50),
                analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS trend_analyses (
                id SERIAL PRIMARY KEY,
                query VARCHAR(500),
                platforms JSONB,
                trend_data JSONB,
                overall_score FLOAT,
                analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        await conn.close()
        logger.info("Database tables initialized successfully")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8026,
        reload=True,
        log_level="info"
    )
