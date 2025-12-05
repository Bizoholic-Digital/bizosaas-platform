# Facebook Ads Integration for BizOSaaS

This document provides comprehensive information about the Facebook Ads integration service for the BizOSaaS platform.

## Overview

The Facebook Ads integration provides comprehensive Facebook Business Manager integration with OAuth flows, campaign management, audience targeting, and real-time performance analytics. This integration follows the established patterns used in the BizOSaaS platform for other advertising integrations.

## Features

### 1. OAuth 2.0 Authentication
- **Secure OAuth Flow**: Complete OAuth 2.0 implementation with state validation
- **Multi-Tenant Support**: Each tenant can connect their own Facebook Business Manager
- **Automatic Token Refresh**: Handles token expiration and refresh automatically
- **Business Manager Integration**: Full access to Facebook Business Manager accounts

### 2. Ad Account Management
- **Multiple Account Support**: Select from available ad accounts
- **Account Health Monitoring**: Real-time account status and balance monitoring
- **Business Account Association**: Links to Business Manager accounts
- **Multi-Currency Support**: Handles different account currencies

### 3. Campaign Management
- **Full Campaign CRUD**: Create, read, update, and delete campaigns
- **Real-time Status Control**: Pause/resume campaigns instantly
- **Performance Analytics**: Comprehensive campaign metrics
- **Campaign Insights**: Detailed performance data with historical trends

### 4. Advanced Targeting
- **Custom Audiences**: Manage and create custom audiences
- **Lookalike Audiences**: Support for lookalike audience creation
- **Interest Targeting**: Advanced interest-based targeting options
- **Geographic Targeting**: Location-based targeting capabilities

### 5. Creative Management
- **Ad Creative Library**: Manage all ad creatives in one place
- **Creative Testing**: Support for A/B testing of creatives
- **Multi-Format Support**: Images, videos, carousels, and more
- **Performance Analytics**: Creative-level performance metrics

### 6. Real-time Analytics
- **Live Metrics**: Real-time campaign performance data
- **Historical Trends**: Performance data over custom time periods
- **ROI Tracking**: Return on ad spend (ROAS) calculation
- **Conversion Tracking**: Track conversions and attribution

## Architecture

### Backend Components

#### 1. FacebookAdsIntegration Class
The main service class that handles all Facebook Ads operations:

```python
from facebook_ads_integration import facebook_ads_integration

# Get connection status
status = await facebook_ads_integration.get_connection_status(tenant_id)

# Fetch campaigns
campaigns = await facebook_ads_integration.get_campaigns(tenant_id)

# Update campaign status
result = await facebook_ads_integration.update_campaign_status(
    tenant_id, campaign_id, 'pause'
)
```

#### 2. Data Models
Comprehensive data models for all Facebook Ads entities:

- `FacebookAdAccount`: Ad account information
- `FacebookCampaign`: Campaign data with insights
- `FacebookAudience`: Custom audience information
- `FacebookCreative`: Ad creative details

#### 3. API Endpoints
RESTful API endpoints for all operations:

- `GET /api/integrations/facebook-ads` - Connection status
- `POST /api/integrations/facebook-ads/oauth/start` - Start OAuth flow
- `GET /api/integrations/facebook-ads/oauth/callback` - OAuth callback
- `GET /api/integrations/facebook-ads/campaigns` - Get campaigns
- `POST /api/integrations/facebook-ads/campaigns/sync` - Sync campaigns
- `POST /api/integrations/facebook-ads/campaigns/{id}/{action}` - Control campaigns

### Frontend Components

#### 1. FacebookAdsIntegration React Component
Comprehensive React component with:

- OAuth flow management
- Ad account selection
- Campaign management interface
- Audience targeting controls
- Creative management
- Performance analytics dashboard

#### 2. API Integration Layer
Next.js API routes that proxy to the Brain API:

```typescript
// Frontend API route
app/api/brain/integrations/facebook-ads/route.ts

// Usage in React component
const response = await fetch('/api/brain/integrations/facebook-ads/campaigns');
const { campaigns } = await response.json();
```

## Setup Instructions

### 1. Facebook App Configuration

1. **Create Facebook App**:
   - Go to [Facebook Developers](https://developers.facebook.com/apps/)
   - Create a new app with "Business" use case
   - Add "Marketing API" product

2. **Configure App Settings**:
   - Set up OAuth redirect URIs
   - Configure app domains
   - Set up webhooks (optional)

3. **Get App Credentials**:
   - Copy App ID and App Secret
   - Store securely in environment variables

### 2. Environment Configuration

Create `.env.facebook` file with your credentials:

```bash
# Copy example configuration
cp .env.facebook.example .env.facebook

# Edit with your credentials
FACEBOOK_APP_ID=your_app_id
FACEBOOK_APP_SECRET=your_app_secret
FACEBOOK_REDIRECT_URI=http://localhost:3002/api/brain/integrations/facebook-ads/oauth?action=callback
```

### 3. Required Permissions

The integration requests these Facebook permissions:

- `ads_management` - Manage ads and campaigns
- `ads_read` - Read ads data and insights
- `business_management` - Access Business Manager
- `pages_read_engagement` - Read Page insights
- `read_insights` - Access detailed analytics

### 4. Installation

```bash
# Install Python dependencies
cd /path/to/bizosaas/services/bizosaas-brain
pip install -r requirements.txt

# Start the Brain API service
python simple_api.py

# Start the frontend (in another terminal)
cd /path/to/bizosaas/frontend
npm run dev
```

## Usage Guide

### 1. Initial Setup

1. **Navigate to Integrations**: Go to the integrations page in BizOSaaS
2. **Find Facebook Ads**: Locate the Facebook Ads integration card
3. **Start Connection**: Click "Connect Facebook Account"
4. **OAuth Flow**: Complete the Facebook authorization
5. **Select Account**: Choose your ad account from the list
6. **Sync Data**: Wait for initial data synchronization

### 2. Campaign Management

```typescript
// Fetch all campaigns
const campaigns = await facebookAds.getCampaigns();

// Pause a campaign
await facebookAds.updateCampaignStatus(campaignId, 'pause');

// Resume a campaign
await facebookAds.updateCampaignStatus(campaignId, 'resume');

// Sync latest data
await facebookAds.syncCampaigns();
```

### 3. Audience Management

```typescript
// Get custom audiences
const audiences = await facebookAds.getAudiences();

// Filter by type
const lookalikes = await facebookAds.getAudiences({ type: 'LOOKALIKE' });

// Create new audience (future feature)
await facebookAds.createAudience({
  name: 'Website Visitors',
  description: 'People who visited our website'
});
```

### 4. Creative Management

```typescript
// Get all creatives
const creatives = await facebookAds.getCreatives();

// Filter active creatives
const activeCreatives = await facebookAds.getCreatives({ status: 'ACTIVE' });

// Sync creative library
await facebookAds.syncCreatives();
```

## API Reference

### Authentication Endpoints

#### Start OAuth Flow
```http
POST /api/integrations/facebook-ads/oauth/start
Content-Type: application/json

{
  "tenant_id": "demo",
  "scopes": ["ads_management", "ads_read"]
}
```

#### OAuth Callback
```http
GET /api/integrations/facebook-ads/oauth/callback?code=AUTH_CODE&state=STATE
```

### Campaign Endpoints

#### Get Campaigns
```http
GET /api/integrations/facebook-ads/campaigns?tenant_id=demo&status=active
```

#### Sync Campaigns
```http
POST /api/integrations/facebook-ads/campaigns/sync
Content-Type: application/json

{
  "tenant_id": "demo",
  "account_id": "act_123456789"
}
```

#### Update Campaign Status
```http
POST /api/integrations/facebook-ads/campaigns/{campaign_id}/pause
Content-Type: application/json

{
  "tenant_id": "demo",
  "account_id": "act_123456789"
}
```

### Account Endpoints

#### Get Ad Accounts
```http
GET /api/integrations/facebook-ads/accounts?tenant_id=demo
```

#### Connect Account
```http
POST /api/integrations/facebook-ads/connect
Content-Type: application/json

{
  "tenant_id": "demo",
  "account_id": "act_123456789",
  "account_data": {
    "name": "My Ad Account",
    "currency": "USD"
  }
}
```

## Data Models

### FacebookCampaign
```typescript
interface FacebookCampaign {
  id: string;
  name: string;
  status: 'active' | 'paused' | 'ended' | 'draft';
  objective: string;
  budget_remaining: number;
  daily_budget: number;
  lifetime_budget?: number;
  spend: number;
  impressions: number;
  clicks: number;
  ctr: number;
  cpc: number;
  cpm: number;
  reach: number;
  frequency: number;
  video_views: number;
  engagements: number;
  conversions: number;
  cost_per_conversion: number;
  roas: number;
  created_time: string;
  updated_time: string;
  start_time: string;
  end_time?: string;
}
```

### FacebookAudience
```typescript
interface FacebookAudience {
  id: string;
  name: string;
  description: string;
  subtype: string;
  approximate_count: number;
  status: string;
  retention_days: number;
}
```

### FacebookCreative
```typescript
interface FacebookCreative {
  id: string;
  name: string;
  title?: string;
  body?: string;
  image_url?: string;
  video_id?: string;
  call_to_action_type?: string;
  status: string;
  created_time: string;
}
```

## Error Handling

### Common Errors

1. **OAuth Errors**:
   - Invalid credentials
   - Expired authorization
   - Permission denied

2. **API Errors**:
   - Rate limiting
   - Invalid parameters
   - Account access denied

3. **Network Errors**:
   - Connection timeouts
   - Service unavailable
   - DNS resolution failures

### Error Response Format

```json
{
  "success": false,
  "error": "Error description",
  "error_code": "FB_API_ERROR",
  "details": {
    "facebook_error": {
      "code": 100,
      "message": "Invalid parameter",
      "type": "OAuthException"
    }
  }
}
```

## Performance Considerations

### Caching Strategy

1. **Campaign Data**: Cached for 5 minutes
2. **Audience Data**: Cached for 1 hour
3. **Creative Data**: Cached for 30 minutes
4. **Account Data**: Cached for 24 hours

### Rate Limiting

- **API Calls**: 200 requests per hour per app
- **Burst Limit**: 25 requests per minute
- **Retry Strategy**: Exponential backoff with jitter

### Optimization Tips

1. **Batch Requests**: Use batch API calls when possible
2. **Field Selection**: Only request needed fields
3. **Time-based Queries**: Use date ranges for insights
4. **Parallel Processing**: Fetch data concurrently

## Security Best Practices

### Token Management

1. **Secure Storage**: Store tokens encrypted
2. **Token Rotation**: Implement automatic token refresh
3. **Access Control**: Tenant-based token isolation
4. **Audit Logging**: Log all token operations

### API Security

1. **HTTPS Only**: All API calls over HTTPS
2. **Request Signing**: Verify webhook signatures
3. **Rate Limiting**: Implement request throttling
4. **Input Validation**: Sanitize all inputs

### Data Privacy

1. **GDPR Compliance**: Handle user data according to GDPR
2. **Data Retention**: Implement data retention policies
3. **Access Logs**: Maintain audit trails
4. **Anonymization**: Anonymize sensitive data

## Testing

### Unit Tests

```python
# Test campaign fetching
async def test_get_campaigns():
    integration = FacebookAdsIntegration()
    result = await integration.get_campaigns("test_tenant")
    assert result['success'] == True
    assert 'campaigns' in result

# Test OAuth flow
async def test_oauth_flow():
    integration = FacebookAdsIntegration()
    oauth_url = integration.generate_oauth_url("test_tenant", ["ads_read"])
    assert oauth_url['success'] == True
    assert 'auth_url' in oauth_url
```

### Integration Tests

```python
# Test full flow
async def test_full_integration():
    # 1. Start OAuth
    # 2. Handle callback
    # 3. Connect account
    # 4. Fetch campaigns
    # 5. Update campaign status
    pass
```

## Troubleshooting

### Common Issues

1. **OAuth Fails**:
   - Check app credentials
   - Verify redirect URI
   - Ensure proper permissions

2. **API Errors**:
   - Check rate limits
   - Verify account access
   - Validate request parameters

3. **No Data Returned**:
   - Check account permissions
   - Verify date ranges
   - Confirm account has data

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Health Checks

```http
GET /api/integrations/facebook-ads?type=health
```

## Future Enhancements

### Planned Features

1. **Webhook Support**: Real-time data updates
2. **Advanced Reporting**: Custom report builder
3. **Automation Rules**: AI-powered campaign optimization
4. **Budget Management**: Advanced budget allocation
5. **Creative Testing**: Automated A/B testing
6. **Audience Insights**: Advanced audience analytics

### API Extensions

1. **Bulk Operations**: Batch campaign management
2. **Scheduled Actions**: Time-based campaign control
3. **Custom Metrics**: User-defined KPIs
4. **Export Functions**: Data export capabilities

## Support

### Documentation
- [Facebook Marketing API Documentation](https://developers.facebook.com/docs/marketing-api/)
- [Facebook Business Manager Help](https://www.facebook.com/business/help/)

### Contact
- Technical Issues: Create GitHub issue
- Feature Requests: Submit enhancement request
- Security Issues: security@bizosaas.com

---

*Last Updated: September 14, 2025*
*Version: 1.0.0*