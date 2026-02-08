# Product Sourcing Workflow [P8] - API Documentation

## Overview

The Product Sourcing Workflow service provides AI-powered product discovery and analysis capabilities for the CoreLDove platform. It integrates with Amazon SP-API, social media platforms, and other data sources to provide comprehensive product sourcing intelligence.

**Base URL:** `http://localhost:8026`
**API Version:** 1.0.0
**Port:** 8026

## Authentication

All API endpoints require authentication. Include the JWT token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

## Core Endpoints

### 1. Health Check

**GET** `/health`

Check the health status of the service.

**Response:**
```json
{
  "status": "healthy",
  "service": "Product Sourcing Workflow",
  "version": "1.0.0",
  "timestamp": "2025-01-19T10:30:00Z"
}
```

### 2. Start Product Discovery

**POST** `/api/product-sourcing/discover`

Initiate a comprehensive product discovery process.

**Request Body:**
```json
{
  "keywords": ["wireless earbuds", "bluetooth headphones"],
  "category": "electronics",
  "min_price": 500,
  "max_price": 5000,
  "market_region": "IN",
  "trending_platforms": ["tiktok", "instagram", "youtube"],
  "competitor_analysis": true,
  "profit_margin_min": 20.0
}
```

**Response:**
```json
{
  "task_id": "discovery_12345",
  "status": "started",
  "message": "Product discovery process initiated",
  "estimated_completion": "2025-01-19T10:35:00Z"
}
```

### 3. Get Discovery Status

**GET** `/api/product-sourcing/discovery/{task_id}/status`

Get the status of a product discovery task.

**Response:**
```json
{
  "task_id": "discovery_12345",
  "status": "completed",
  "progress": 100,
  "completed_at": "2025-01-19T10:34:30Z",
  "results": {
    "discovered_products": 25,
    "high_potential_products": 8,
    "processing_time": 4.5
  }
}
```

### 4. Get Trending Products

**GET** `/api/product-sourcing/trends`

Get currently trending products in the market.

**Query Parameters:**
- `category` (optional): Filter by product category
- `region` (optional): Market region (default: "IN")
- `limit` (optional): Number of results (default: 20)

**Response:**
```json
{
  "trending_products": [
    {
      "id": "trend_1",
      "title": "Smart Fitness Watch",
      "category": "electronics",
      "trend_score": 87.5,
      "growth_rate": 45.2,
      "social_mentions": 2850,
      "estimated_demand": 15000
    }
  ],
  "region": "IN",
  "updated_at": "2025-01-19T10:30:00Z"
}
```

### 5. Analyze Specific Product

**POST** `/api/product-sourcing/analyze`

Perform detailed analysis of a specific product.

**Request Body:**
```json
{
  "asin": "B08N5WRWNW",
  "product_title": "Wireless Bluetooth Earbuds",
  "current_price": 2999,
  "category": "electronics",
  "deep_analysis": true
}
```

**Response:**
```json
{
  "product_analysis": {
    "product_data": {
      "title": "Wireless Bluetooth Earbuds",
      "price": 2999,
      "rating": 4.2,
      "review_count": 1250
    },
    "scoring": {
      "trend_score": 75.5,
      "profit_score": 68.2,
      "competition_score": 45.8,
      "risk_score": 32.1,
      "overall_score": 64.4,
      "category": "mid_tier",
      "confidence": 0.85
    },
    "market_intelligence": {
      "competitive_landscape": "medium_intensity",
      "market_opportunity": "good",
      "entry_barriers": "low"
    },
    "recommendations": [
      "Consider competitive pricing strategy",
      "Focus on quality differentiation",
      "Monitor competitor actions closely"
    ],
    "analyzed_at": "2025-01-19T10:30:00Z"
  }
}
```

### 6. Get Personalized Recommendations

**GET** `/api/product-sourcing/recommendations`

Get personalized product recommendations based on user profile.

**Query Parameters:**
- `user_id` (optional): User identifier
- `business_type` (optional): Type of business (default: "general")
- `budget_range` (optional): Budget range filter
- `limit` (optional): Number of recommendations (default: 10)

**Response:**
```json
{
  "recommendations": [
    {
      "product_id": "rec_1",
      "title": "Smart Home Security Camera",
      "category": "electronics",
      "overall_score": 82.5,
      "profit_potential": 45.0,
      "market_demand": "high",
      "competition_level": "low",
      "reason": "High profit margin with growing demand",
      "estimated_roi": 35.5
    }
  ],
  "user_id": "user_123",
  "business_type": "general",
  "generated_at": "2025-01-19T10:30:00Z"
}
```

### 7. Product Classification

**POST** `/api/product-sourcing/classify`

Classify a product into Hook/Mid-Tier/Hero/Not Qualified categories.

**Request Body:**
```json
{
  "product_title": "Premium Wireless Headphones",
  "current_price": 8999,
  "category": "electronics",
  "asin": "B08N5WRWNW"
}
```

**Response:**
```json
{
  "classification": {
    "category": "hero",
    "overall_score": 78.5,
    "confidence": 0.89,
    "breakdown": {
      "trend_score": 72.3,
      "profit_score": 85.7,
      "competition_score": 65.1,
      "risk_score": 28.4
    },
    "explanation": "Premium opportunity with profit score of 85.7. Build long-term business around this.",
    "classified_at": "2025-01-19T10:30:00Z"
  }
}
```

## Integration Endpoints

### 8. Amazon Product Details

**GET** `/api/amazon/product/{asin}`

Get detailed product information from Amazon SP-API.

**Response:**
```json
{
  "asin": "B08N5WRWNW",
  "title": "Premium Wireless Headphones",
  "price": 8999,
  "currency": "INR",
  "rating": 4.4,
  "review_count": 2847,
  "images": ["url1", "url2"],
  "features": ["Noise Cancellation", "30hr Battery"],
  "dimensions": {"length": 20, "width": 15, "height": 8},
  "weight": 250
}
```

### 9. Amazon Pricing Data

**GET** `/api/amazon/pricing/{asin}`

Get pricing and Buy Box information for an Amazon product.

**Response:**
```json
{
  "asin": "B08N5WRWNW",
  "current_price": 8999,
  "currency": "INR",
  "buy_box_seller": "Amazon",
  "price_history": [
    {"date": "2025-01-15", "price": 9499},
    {"date": "2025-01-10", "price": 8999}
  ],
  "competitive_prices": [
    {"seller": "TechStore", "price": 9199},
    {"seller": "GadgetHub", "price": 9299}
  ]
}
```

### 10. Social Media Trends

**GET** `/api/trends/social/{query}`

Analyze social media trends for a specific query.

**Response:**
```json
{
  "query": "wireless earbuds",
  "platforms": {
    "tiktok": {
      "score": 85.2,
      "video_count": 12500,
      "engagement_rate": 8.5,
      "viral_potential": "high"
    },
    "instagram": {
      "score": 72.8,
      "post_count": 8900,
      "hashtag_performance": 7.2,
      "influencer_mentions": 45
    }
  },
  "overall_score": 79.0,
  "trend_direction": "up",
  "analyzed_at": "2025-01-19T10:30:00Z"
}
```

### 11. Competitor Analysis

**GET** `/api/competitors/analysis/{category}`

Get competitive landscape analysis for a product category.

**Response:**
```json
{
  "category": "electronics",
  "total_competitors": 156,
  "market_leaders": [
    {"name": "TechBrand", "market_share": 15.2},
    {"name": "GadgetCorp", "market_share": 12.8}
  ],
  "competitive_intensity": "high",
  "entry_barriers": "medium",
  "average_margins": 25.5,
  "price_ranges": {
    "budget": {"min": 500, "max": 2000},
    "mid_range": {"min": 2000, "max": 8000},
    "premium": {"min": 8000, "max": 25000}
  }
}
```

### 12. Trend Analysis

**POST** `/api/trends/analyze`

Perform comprehensive trend analysis across multiple platforms.

**Request Body:**
```json
{
  "query": "smart fitness tracker",
  "platforms": ["google", "tiktok", "instagram", "youtube"],
  "time_range": "30d",
  "region": "IN"
}
```

**Response:**
```json
{
  "trend_analysis": {
    "query": "smart fitness tracker",
    "overall_score": 73.5,
    "trend_direction": "up",
    "platforms": {
      "google": {"score": 78.2, "search_volume": 45000},
      "tiktok": {"score": 82.1, "video_count": 8500},
      "instagram": {"score": 69.8, "post_count": 12000},
      "youtube": {"score": 71.3, "video_count": 2800}
    },
    "growth_momentum": 15.5,
    "viral_potential": "medium",
    "recommendations": [
      "Strong upward trend - good entry timing",
      "Focus on TikTok content strategy",
      "Monitor competitor response"
    ]
  },
  "analyzed_at": "2025-01-19T10:30:00Z"
}
```

### 13. Market Intelligence

**GET** `/api/product-sourcing/market-intel`

Get comprehensive market intelligence report.

**Query Parameters:**
- `category` (required): Product category
- `competitor_count` (optional): Number of competitors to analyze (default: 10)
- `include_forecast` (optional): Include growth forecasts (default: true)

**Response:**
```json
{
  "market_intelligence": {
    "category": "electronics",
    "market_size": {
      "current_size": 15000000,
      "projected_size": 18750000,
      "growth_rate": 25.0
    },
    "competitive_landscape": {
      "total_competitors": 245,
      "market_concentration": "medium",
      "new_entrants_monthly": 12
    },
    "opportunities": [
      {
        "type": "price_gap",
        "description": "Underserved ₹3000-5000 segment",
        "potential": "high"
      }
    ],
    "forecasting": {
      "demand_forecast": "growing",
      "price_trends": "stable",
      "competition_evolution": "intensifying"
    }
  },
  "generated_at": "2025-01-19T10:30:00Z"
}
```

## Error Responses

All endpoints follow standard HTTP status codes and return errors in this format:

```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Keywords are required for product discovery",
    "details": "Please provide at least one keyword for product search",
    "timestamp": "2025-01-19T10:30:00Z"
  }
}
```

### Common Error Codes:
- `400` - Bad Request (missing required parameters)
- `401` - Unauthorized (invalid or missing authentication)
- `404` - Not Found (resource doesn't exist)
- `429` - Too Many Requests (rate limit exceeded)
- `500` - Internal Server Error (service error)

## Rate Limits

- **General API calls:** 60 requests per minute per user
- **Discovery tasks:** 10 requests per hour per user
- **Analysis requests:** 30 requests per hour per user

## SDKs and Examples

### Python SDK Example

```python
import requests

class ProductSourcingClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
    
    def discover_products(self, keywords, category=None):
        payload = {
            'keywords': keywords,
            'category': category,
            'market_region': 'IN'
        }
        
        response = requests.post(
            f"{self.base_url}/api/product-sourcing/discover",
            json=payload,
            headers=self.headers
        )
        
        return response.json()
    
    def get_trends(self, category=None, limit=20):
        params = {'limit': limit}
        if category:
            params['category'] = category
            
        response = requests.get(
            f"{self.base_url}/api/product-sourcing/trends",
            params=params,
            headers=self.headers
        )
        
        return response.json()

# Usage
client = ProductSourcingClient("http://localhost:8026", "your_api_key")
result = client.discover_products(["wireless earbuds", "bluetooth headphones"])
print(result)
```

### JavaScript SDK Example

```javascript
class ProductSourcingAPI {
    constructor(baseUrl, apiKey) {
        this.baseUrl = baseUrl;
        this.headers = {
            'Authorization': `Bearer ${apiKey}`,
            'Content-Type': 'application/json'
        };
    }
    
    async discoverProducts(keywords, options = {}) {
        const payload = {
            keywords,
            market_region: 'IN',
            ...options
        };
        
        const response = await fetch(`${this.baseUrl}/api/product-sourcing/discover`, {
            method: 'POST',
            headers: this.headers,
            body: JSON.stringify(payload)
        });
        
        return response.json();
    }
    
    async analyzeProduct(productData) {
        const response = await fetch(`${this.baseUrl}/api/product-sourcing/analyze`, {
            method: 'POST',
            headers: this.headers,
            body: JSON.stringify(productData)
        });
        
        return response.json();
    }
}

// Usage
const api = new ProductSourcingAPI("http://localhost:8026", "your_api_key");
const result = await api.discoverProducts(["smart watch", "fitness tracker"]);
console.log(result);
```

## Webhook Support

The service supports webhooks for notifying external systems about completed tasks:

### Webhook Payload Example

```json
{
  "event": "discovery.completed",
  "task_id": "discovery_12345",
  "timestamp": "2025-01-19T10:30:00Z",
  "data": {
    "products_discovered": 25,
    "high_potential_count": 8,
    "processing_time": 4.5,
    "download_url": "https://api.example.com/download/discovery_12345"
  }
}
```

## Data Export

Results can be exported in multiple formats:

### CSV Export
**GET** `/api/product-sourcing/export/{task_id}/csv`

### Excel Export
**GET** `/api/product-sourcing/export/{task_id}/excel`

### JSON Export
**GET** `/api/product-sourcing/export/{task_id}/json`

## Support and Resources

- **Documentation:** [API Docs](http://localhost:8026/docs)
- **Interactive API:** [Swagger UI](http://localhost:8026/redoc)
- **Status Page:** [Service Status](http://localhost:8026/health)
- **Monitoring:** [Metrics Dashboard](http://localhost:3001)

For technical support, contact the BizOSaaS development team.