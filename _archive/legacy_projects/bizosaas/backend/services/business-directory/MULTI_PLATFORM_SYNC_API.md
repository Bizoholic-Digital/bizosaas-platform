# Multi-Platform Directory Sync API Documentation

## Overview

The **Multi-Platform Directory Sync Workflow** is the most comprehensive directory synchronization system available, covering 15+ major directory and mapping platforms with intelligent orchestration, AI-powered optimization, and advanced conflict resolution.

## Architecture

### Platform Abstraction Layer
- **Base Platform Client**: Abstract interface that all platform clients implement
- **Platform Factory**: Centralized platform client creation and management
- **Platform Registry**: Discovery and metadata management for all platforms
- **Unified Data Models**: Universal business data structures that work across platforms

### Supported Platforms

#### Tier 1 Platforms (Essential)
- ✅ **Google Business Profile**: Business listings, reviews, insights, photos
- 🆕 **Google Maps**: Places API for map presence and place data
- ✅ **Yelp**: Business listings, reviews, photos, check-ins
- ✅ **Facebook Business**: Business pages, posts, reviews, events
- ✅ **Apple Maps**: iOS/macOS map presence, business registration
- 🆕 **Bing Maps**: Microsoft's mapping platform
- 🆕 **Bing Places**: Bing's business listing platform

#### Tier 2 Platforms (Recommended)
- 🆕 **TripAdvisor**: Travel and hospitality reviews
- 🆕 **Foursquare**: Location intelligence platform
- 🆕 **HERE Maps**: Enterprise mapping solutions
- 🆕 **MapQuest**: Navigation and directions

#### Tier 3 Platforms (Industry-Specific)
- 🆕 **Yellow Pages**: Traditional business directory
- 🆕 **Superpages**: Verizon business directory

## API Endpoints

### Base URL
```
/api/brain/business-directory/multi-platform
```

### Authentication
All endpoints require proper authentication tokens. Platform-specific credentials must be provided for operations.

---

## Core Endpoints

### 1. List All Platforms
```http
GET /platforms
```

**Response:**
```json
{
  "platforms": [
    {
      "platform_name": "google_business",
      "client_available": true,
      "last_health_check": true,
      "metadata": {
        "display_name": "Google Business Profile",
        "tier": "tier_1",
        "category": "search_engine"
      },
      "capabilities": {
        "supported_operations": ["create_listing", "update_listing", "search_listings"],
        "read_only": false,
        "rate_limits": {
          "per_minute": 600,
          "per_day": 10000
        }
      }
    }
  ]
}
```

### 2. Get Platforms by Tier
```http
GET /platforms/tier/{tier}
```

**Parameters:**
- `tier`: Platform tier (tier_1, tier_2, tier_3)

**Response:**
```json
{
  "tier": "tier_1",
  "platforms": ["google_business", "google_maps", "yelp", "facebook", "apple_maps"],
  "count": 5
}
```

### 3. Get Platforms by Capability
```http
GET /platforms/capabilities/{capability}
```

**Capabilities:**
- `create_listing`
- `update_listing`
- `search_listings`
- `claim_listing`
- `verify_listing`
- `manage_reviews`
- `analytics`

### 4. Platform Health Check
```http
POST /platforms/health-check
```

Tests connectivity to all registered platforms.

**Response:**
```json
{
  "total_platforms": 12,
  "healthy_platforms": 10,
  "overall_health": 0.83,
  "platform_status": {
    "google_business": true,
    "google_maps": true,
    "yelp": false
  }
}
```

---

## Multi-Platform Sync

### 5. Intelligent Business Sync
```http
POST /sync
```

**Request Body:**
```json
{
  "business_id": "business_123",
  "strategy": "conservative",
  "operations": ["update"],
  "platforms": ["google_business", "yelp", "facebook"],
  "priority": "high",
  "max_concurrent": 3,
  "retry_failed": true,
  "notify_on_completion": true
}
```

**Sync Strategies:**
- `aggressive`: Sync to all available platforms
- `conservative`: Sync to Tier 1 platforms only
- `selective`: AI-powered platform selection
- `custom`: Use specified platforms only

**Response:**
```json
{
  "business_id": "business_123",
  "request_id": "sync_456",
  "overall_success": true,
  "total_platforms": 3,
  "successful_platforms": 3,
  "failed_platforms": 0,
  "execution_time": 12.5,
  "recommendations": [
    "All platforms synced successfully",
    "Consider adding TripAdvisor for restaurant businesses"
  ],
  "platform_results": {
    "google_business": {
      "success": true,
      "operation": "update",
      "platform_id": "ChIJ..."
    },
    "yelp": {
      "success": true,
      "operation": "claim",
      "platform_id": "yelp_123"
    },
    "facebook": {
      "success": true,
      "operation": "update",
      "platform_id": "fb_page_456"
    }
  }
}
```

### 6. Batch Sync Multiple Businesses
```http
POST /batch-sync
```

**Request Body:**
```json
{
  "business_ids": ["biz_1", "biz_2", "biz_3"],
  "strategy": "conservative",
  "platforms": ["google_business", "yelp"],
  "max_concurrent_businesses": 5
}
```

**Response:**
```json
{
  "total_businesses": 3,
  "successful_businesses": 2,
  "failed_businesses": 1,
  "success_rate": 0.67,
  "total_execution_time": 45.2,
  "results": [...]
}
```

---

## Business Intelligence

### 7. Platform Recommendations
```http
GET /business/{business_id}/recommendations
```

Get AI-powered platform recommendations for a specific business based on:
- Business type and industry
- Geographic location
- Existing platform presence
- Performance analytics

**Response:**
```json
{
  "business_id": "business_123",
  "recommendations": [
    {
      "platform": "tripadvisor",
      "priority": "high",
      "rationale": "Restaurant businesses show 85% higher engagement on TripAdvisor",
      "expected_roi": 0.85,
      "estimated_setup_time": 20
    }
  ],
  "total_recommended": 5
}
```

### 8. Sync Analytics
```http
GET /analytics?business_id={id}&timeframe_days=30
```

**Response:**
```json
{
  "total_syncs": 150,
  "success_rate": 0.92,
  "avg_execution_time": 8.5,
  "platform_performance": {
    "google_business": {
      "success_rate": 0.98,
      "total_attempts": 50,
      "successful_attempts": 49
    },
    "yelp": {
      "success_rate": 0.85,
      "total_attempts": 50,
      "successful_attempts": 42
    }
  },
  "recommendations": [
    "Google Business shows excellent reliability",
    "Consider reviewing Yelp API configuration due to lower success rate"
  ]
}
```

### 9. Business Sync Status
```http
GET /business/{business_id}/sync-status
```

**Response:**
```json
{
  "business_id": "business_123",
  "total_platforms": 8,
  "synced_platforms": 7,
  "verified_platforms": 5,
  "claimed_platforms": 3,
  "platform_status": {
    "google_business": {
      "platform_id": "ChIJ...",
      "last_synced": "2025-01-15T10:30:00Z",
      "sync_status": "success",
      "is_verified": true,
      "is_claimed": true
    }
  }
}
```

---

## Platform Management

### 10. Validate Credentials
```http
POST /credentials/validate
```

**Request Body:**
```json
{
  "credentials": [
    {
      "platform": "google_business",
      "credentials": {
        "api_key": "AIza...",
        "client_id": "123..."
      },
      "expires_at": "2025-12-31T23:59:59Z"
    }
  ]
}
```

**Response:**
```json
{
  "total_platforms": 3,
  "valid_credentials": 2,
  "validation_rate": 0.67,
  "results": {
    "google_business": {
      "valid": true,
      "expires_at": "2025-12-31T23:59:59Z"
    },
    "yelp": {
      "valid": false,
      "expires_at": null
    }
  }
}
```

### 11. Platform Registry Summary
```http
GET /registry/summary
```

**Response:**
```json
{
  "total_platforms": 12,
  "by_tier": {
    "tier_1": 7,
    "tier_2": 4,
    "tier_3": 2
  },
  "by_category": {
    "search_engine": 3,
    "mapping_service": 5,
    "review_platform": 2,
    "directory": 2
  },
  "capabilities_summary": {
    "create_listing": 5,
    "update_listing": 7,
    "search_listings": 12
  },
  "active_platforms": 12,
  "validation_issues": {
    "missing_tier_1": [],
    "configuration_errors": [],
    "inactive_important": []
  }
}
```

---

## Advanced Features

### Intelligent Platform Selection
The system uses AI to recommend optimal platforms based on:
- Business type and industry vertical
- Geographic location and market presence
- Existing platform performance
- ROI analysis and cost-effectiveness

### Smart Conflict Resolution
- Automatic conflict detection across platforms
- AI-powered resolution suggestions
- Priority-based conflict handling
- Manual override capabilities

### Rate Limiting & Optimization
- Platform-specific rate limit management
- Intelligent request queuing
- Automatic retry with exponential backoff
- Concurrent request optimization

### Real-time Analytics
- Platform performance monitoring
- Success rate tracking
- ROI measurement
- Comprehensive reporting

---

## Error Handling

### Standard Error Response
```json
{
  "error": "Validation error",
  "detail": "Invalid platform specified",
  "status_code": 422
}
```

### Common Error Codes
- `400`: Bad Request - Invalid parameters
- `401`: Unauthorized - Missing or invalid authentication
- `422`: Validation Error - Invalid data format
- `429`: Rate Limited - Too many requests
- `500`: Internal Error - Server-side issue

---

## Rate Limits

Platform-specific rate limits are automatically managed:

| Platform | Per Minute | Per Day |
|----------|------------|---------|
| Google Business | 600 | 10,000 |
| Google Maps | 600 | 10,000 |
| Yelp | 5,000 | 25,000 |
| Facebook | 200 | 25,000 |
| Apple Maps | 1,000 | 100,000 |
| Bing Maps | 250 | 125,000 |
| TripAdvisor | 500 | 50,000 |

---

## Getting Started

### 1. Platform Setup
1. Obtain API credentials for desired platforms
2. Configure authentication in your application
3. Test connectivity using health check endpoints

### 2. Basic Sync
```bash
curl -X POST "/api/brain/business-directory/multi-platform/sync" \
  -H "Content-Type: application/json" \
  -d '{
    "business_id": "your_business_id",
    "strategy": "conservative",
    "operations": ["update"]
  }'
```

### 3. Monitor Progress
```bash
curl "/api/brain/business-directory/multi-platform/business/{id}/sync-status"
```

### 4. Analytics & Optimization
```bash
curl "/api/brain/business-directory/multi-platform/analytics?timeframe_days=30"
```

---

## Best Practices

### 1. Strategy Selection
- **Conservative**: Start with Tier 1 platforms for guaranteed reach
- **Selective**: Use AI recommendations for optimal ROI
- **Aggressive**: Maximum coverage for established businesses

### 2. Credential Management
- Regularly validate API credentials
- Monitor rate limit usage
- Set up proper error notifications

### 3. Conflict Resolution
- Review conflicts promptly
- Establish data quality standards
- Use Google Business as primary source for consistency

### 4. Performance Monitoring
- Track success rates by platform
- Monitor execution times
- Review AI recommendations quarterly

---

This comprehensive API provides unprecedented control over multi-platform directory synchronization, giving businesses complete market coverage with intelligent automation and optimization.