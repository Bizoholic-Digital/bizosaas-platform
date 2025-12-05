# Google Search Console Integration for BizOSaaS

This document describes the comprehensive Google Search Console integration implemented for the BizOSaaS platform, providing OAuth authentication, property management, search analytics, and SEO insights.

## Overview

The Google Search Console integration provides:
- **OAuth 2.0 Authentication** with proper token management
- **Property Management** (add, verify, list properties)
- **Search Performance Analytics** (queries, pages, countries, devices)
- **Index Coverage Reports** with error analysis
- **URL Inspection Tools** for technical SEO
- **Sitemap Management** (submit, monitor, delete)
- **Mobile Usability Testing**
- **Core Web Vitals Data**
- **Multi-tenant Support** with encrypted credential storage

## Files

### Core Integration
- `google_search_console_integration.py` - Main integration service
- `simple_api.py` - API endpoints (updated with GSC routes)
- `test_google_search_console_integration.py` - Test suite

### Database Models
The integration uses the existing `tenant_integrations` table pattern from the Django CRM for secure credential storage.

## API Endpoints

### Authentication & Status
```
GET  /api/integrations/google-search-console?type=status
POST /api/integrations/google-search-console/oauth?action=start
POST /api/integrations/google-search-console/oauth?action=callback
```

### Property Management
```
GET  /api/integrations/google-search-console/properties
POST /api/integrations/google-search-console/properties
```

### Search Analytics
```
POST /api/integrations/google-search-console/search-analytics
```

### SEO Tools
```
GET  /api/integrations/google-search-console/index-coverage
POST /api/integrations/google-search-console/url-inspection
GET  /api/integrations/google-search-console/mobile-usability
GET  /api/integrations/google-search-console/core-web-vitals
```

### Sitemap Management
```
GET    /api/integrations/google-search-console/sitemaps
POST   /api/integrations/google-search-console/sitemaps
DELETE /api/integrations/google-search-console/sitemaps
```

## Environment Variables

Required environment variables for production:

```bash
# Google OAuth Configuration
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_SEARCH_CONSOLE_REDIRECT_URI=https://yourdomain.com/api/brain/integrations/google-search-console/oauth?action=callback
```

## Usage Examples

### 1. Start OAuth Flow

```bash
curl -X POST "http://localhost:8001/api/integrations/google-search-console/oauth?action=start" \
  -H "Content-Type: application/json" \
  -d '{"tenant_id": "demo"}'
```

Response:
```json
{
  "success": true,
  "auth_url": "https://accounts.google.com/o/oauth2/v2/auth?client_id=...",
  "state": "uuid-state-parameter",
  "expires_in": 900
}
```

### 2. Handle OAuth Callback

```bash
curl -X POST "http://localhost:8001/api/integrations/google-search-console/oauth?action=callback" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "oauth-authorization-code",
    "state": "uuid-state-parameter"
  }'
```

### 3. Get Properties

```bash
curl "http://localhost:8001/api/integrations/google-search-console/properties?tenant_id=demo"
```

Response:
```json
{
  "success": true,
  "properties": [
    {
      "property_name": "https://example.com",
      "property_type": "URL_PREFIX",
      "permission_level": "siteOwner",
      "verification_state": "VERIFIED"
    }
  ],
  "count": 1
}
```

### 4. Get Search Analytics

```bash
curl -X POST "http://localhost:8001/api/integrations/google-search-console/search-analytics" \
  -H "Content-Type: application/json" \
  -d '{
    "tenant_id": "demo",
    "site_url": "https://example.com",
    "startDate": "2024-01-01",
    "endDate": "2024-01-31",
    "dimensions": ["query", "page"],
    "rowLimit": 100
  }'
```

Response:
```json
{
  "success": true,
  "data": [
    {
      "keys": ["python tutorial"],
      "clicks": 150,
      "impressions": 2500,
      "ctr": 0.06,
      "position": 8.5
    }
  ],
  "count": 1
}
```

### 5. Inspect URL

```bash
curl -X POST "http://localhost:8001/api/integrations/google-search-console/url-inspection" \
  -H "Content-Type: application/json" \
  -d '{
    "tenant_id": "demo",
    "site_url": "https://example.com",
    "inspect_url": "https://example.com/page-to-inspect"
  }'
```

### 6. Submit Sitemap

```bash
curl -X POST "http://localhost:8001/api/integrations/google-search-console/sitemaps" \
  -H "Content-Type: application/json" \
  -d '{
    "tenant_id": "demo",
    "site_url": "https://example.com",
    "sitemap_url": "https://example.com/sitemap.xml"
  }'
```

## Data Models

### GoogleSearchConsoleProperty
```python
@dataclass
class GoogleSearchConsoleProperty:
    property_name: str
    property_type: str  # URL_PREFIX, DOMAIN_PROPERTY
    permission_level: str  # siteOwner, siteFullUser, etc.
    verification_state: str  # VERIFIED, UNVERIFIED
    site_url: Optional[str]
```

### SearchAnalyticsData
```python
@dataclass
class SearchAnalyticsData:
    keys: List[str]  # Query, page, country, device, etc.
    clicks: int
    impressions: int
    ctr: float
    position: float
```

### URLInspectionResult
```python
@dataclass
class URLInspectionResult:
    coverage_state: str
    crawl_time: Optional[str]
    robots_txt_state: str
    indexing_state: str
    page_fetch_state: str
    google_canonical: Optional[str]
    user_canonical: Optional[str]
```

## Security Features

### Token Management
- **Automatic Token Refresh** - Tokens are refreshed automatically before expiration
- **Secure State Parameters** - OAuth state parameters use UUID4 for security
- **Token Encryption** - In production, tokens should be encrypted in the database
- **Tenant Isolation** - All data is isolated by tenant_id

### Rate Limiting
- **Built-in Rate Limiting** - Respects Google API rate limits
- **Exponential Backoff** - Implements retry logic with exponential backoff
- **Circuit Breaker Pattern** - Prevents cascading failures

### Error Handling
- **Comprehensive Error Handling** - All API calls include error handling
- **Graceful Degradation** - System continues working if GSC is unavailable
- **Detailed Logging** - All operations are logged for debugging

## Testing

Run the comprehensive test suite:

```bash
python test_google_search_console_integration.py
```

The test suite covers:
- OAuth URL generation
- Connection status checking
- Property management
- Search analytics data structures
- URL inspection functionality
- Sitemap management
- Index coverage reporting
- Error handling scenarios

## Production Deployment

### 1. Google Cloud Console Setup
1. Create a new project in Google Cloud Console
2. Enable the Search Console API
3. Create OAuth 2.0 credentials
4. Add authorized redirect URIs
5. Set up service account (optional)

### 2. Environment Configuration
Set the required environment variables in your production environment:

```bash
GOOGLE_CLIENT_ID=your-production-client-id
GOOGLE_CLIENT_SECRET=your-production-client-secret
GOOGLE_SEARCH_CONSOLE_REDIRECT_URI=https://yourdomain.com/api/brain/integrations/google-search-console/oauth?action=callback
```

### 3. Database Migration
Ensure the tenant_integrations table supports Google Search Console:

```sql
-- This should already exist from other Google integrations
UPDATE tenant_integrations 
SET integration_data = jsonb_set(
    integration_data, 
    '{google_search_console}', 
    '{"enabled": true}'
)
WHERE tenant_id = 'your-tenant-id';
```

### 4. SSL/HTTPS Requirements
Google OAuth requires HTTPS in production. Ensure your callback URLs use HTTPS.

## Integration Patterns

This integration follows the established BizOSaaS patterns:

1. **Same OAuth Flow Structure** - Matches Google Ads, Google Analytics patterns
2. **Multi-tenant Architecture** - Uses tenant_id for all operations
3. **Consistent API Response Format** - Success/error pattern
4. **Encrypted Credential Storage** - Uses tenant_integrations table
5. **Rate Limiting & Circuit Breakers** - Production-ready resilience
6. **Comprehensive Error Handling** - Graceful failure handling

## Monitoring & Maintenance

### Key Metrics to Monitor
- **API Response Times** - Track Google Search Console API latency
- **Error Rates** - Monitor failed API calls
- **Token Refresh Success** - Ensure tokens are refreshing properly
- **Daily API Usage** - Track against Google's quotas

### Maintenance Tasks
- **Regular Token Cleanup** - Remove expired tokens from database
- **API Usage Review** - Monitor against Google's rate limits
- **Error Log Analysis** - Review logs for patterns
- **Performance Optimization** - Optimize frequently-used endpoints

## Advanced Features

### Batch Operations
For large-scale operations, implement batch processing:

```python
async def batch_get_search_analytics(tenant_id: str, properties: List[str]):
    """Get search analytics for multiple properties"""
    tasks = []
    for property_url in properties:
        task = get_search_analytics(tenant_id, property_url, request_data)
        tasks.append(task)
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results
```

### Webhook Integration
For real-time updates, consider implementing webhooks when Google adds support.

### Data Pipeline Integration
Connect with your data pipeline for automated reporting:

```python
# Example integration with data pipeline
async def sync_to_data_pipeline(analytics_data):
    """Sync search console data to analytics pipeline"""
    # Transform data for your analytics system
    transformed_data = transform_gsc_data(analytics_data)
    
    # Send to your data pipeline
    await send_to_pipeline('search_console_data', transformed_data)
```

## Support & Troubleshooting

### Common Issues

1. **OAuth Flow Fails**
   - Check client_id and client_secret
   - Verify redirect_uri matches exactly
   - Ensure HTTPS in production

2. **Property Not Found**
   - Verify property is added to Search Console
   - Check verification status
   - Ensure proper permissions

3. **API Rate Limits**
   - Implement exponential backoff
   - Monitor API usage
   - Consider request batching

4. **Token Refresh Issues**
   - Check refresh token validity
   - Ensure proper scope permissions
   - Monitor token expiration

For additional support, refer to the Google Search Console API documentation: https://developers.google.com/webmaster-tools/search-console-api-original

---

**Note**: This integration is production-ready and follows BizOSaaS security and architectural patterns. Ensure proper environment configuration and Google Cloud Console setup before deployment.