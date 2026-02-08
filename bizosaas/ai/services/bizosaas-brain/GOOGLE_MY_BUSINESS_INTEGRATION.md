# Google My Business Integration for BizOSaaS

A comprehensive Google My Business API integration that enables local business profile management, posts creation, review management, and business insights analytics within the BizOSaaS platform.

## Features

### 🏢 Business Location Management
- **Create Locations**: Add new business locations with complete address and contact information
- **Update Locations**: Modify existing business details, hours, and contact information  
- **Location Verification**: Track verification status and manage verification processes
- **Multi-Location Support**: Manage multiple business locations from one dashboard
- **Business Categories**: Support for all Google My Business category types

### 📝 Posts Management
- **Create Posts**: Standard posts, events, offers, and product announcements
- **Schedule Posts**: Plan content in advance with scheduling capabilities
- **Rich Media**: Support for images and videos in posts
- **Call-to-Action**: Add actionable buttons (Learn More, Call, Book, etc.)
- **Post Analytics**: Track post performance and engagement metrics

### ⭐ Reviews Management
- **Review Monitoring**: Real-time access to customer reviews and ratings
- **Response Management**: Reply to reviews directly from the dashboard
- **Review Analytics**: Track review trends and sentiment over time
- **Automated Alerts**: Notifications for new reviews requiring attention
- **Review Insights**: Detailed analysis of customer feedback

### 📊 Business Insights & Analytics
- **Search Performance**: Direct and indirect search query analytics
- **Map Views**: Track how often your business appears on Google Maps
- **Customer Actions**: Monitor website visits, calls, and direction requests
- **Time-based Analytics**: Historical data and trend analysis
- **Local SEO Metrics**: Performance indicators for local search optimization

### 📸 Photos & Media Management
- **Photo Upload**: Add business photos directly through the integration
- **Photo Organization**: Categorize photos (exterior, interior, team, products)
- **Image Optimization**: Automatic resizing and optimization for Google My Business
- **Media Analytics**: Track photo view counts and engagement

### ❓ Q&A Management
- **Customer Questions**: Monitor and respond to customer questions
- **FAQ Management**: Create and maintain frequently asked questions
- **Response Templates**: Quick replies for common questions
- **Q&A Analytics**: Track question trends and response effectiveness

## Architecture

### Backend Components

#### Core Integration (`google_my_business_integration.py`)
```python
class GoogleMyBusinessIntegration:
    - OAuth 2.0 flow implementation
    - Token management with refresh capabilities
    - API request handling with retry logic
    - Multi-tenant data isolation
    - Rate limiting and error handling
```

#### Data Models
```python
@dataclass
class GoogleMyBusinessLocation:
    name: str
    location_name: str
    primary_phone: str
    primary_category: str
    location_state: LocationState
    # ... additional fields

@dataclass  
class GoogleMyBusinessPost:
    topic_type: str
    summary: str
    state: PostState
    # ... additional fields

@dataclass
class GoogleMyBusinessReview:
    star_rating: int
    comment: str
    reviewer: dict
    # ... additional fields
```

#### API Endpoints (`simple_api.py`)
- `GET /api/integrations/google-my-business` - Connection status and data
- `POST /api/integrations/google-my-business/oauth` - OAuth flow management
- `GET|POST /api/integrations/google-my-business/locations` - Location management
- `GET|POST /api/integrations/google-my-business/locations/{id}/posts` - Post management
- `GET /api/integrations/google-my-business/locations/{id}/reviews` - Review access
- `POST /api/integrations/google-my-business/reviews/{id}/reply` - Review responses
- `POST /api/integrations/google-my-business/locations/{id}/insights` - Analytics data

### Frontend Components

#### Main Integration Component (`google-my-business-integration.tsx`)
- **Connection Management**: OAuth flow initiation and status monitoring
- **Location Selector**: Multi-location business support with easy switching
- **Tabbed Interface**: Organized access to all features (Overview, Posts, Reviews, Insights, Settings)
- **Real-time Updates**: Live data refresh and automatic synchronization
- **Responsive Design**: Mobile-friendly interface with touch-optimized controls

#### Key UI Features
- **Dashboard Overview**: Business stats, location health, and quick actions
- **Post Creator**: Rich text editor with media upload and scheduling
- **Review Monitor**: Real-time review feed with response capabilities
- **Analytics Charts**: Visual representation of business performance metrics
- **Location Manager**: Form-based location creation and editing

## Setup Instructions

### 1. Google Cloud Console Setup

1. **Create/Select Project**:
   ```bash
   # Go to Google Cloud Console
   # Create new project or select existing one
   ```

2. **Enable APIs**:
   - Google My Business API
   - Google+ API (for legacy support)
   - Places API (for location data)

3. **Create OAuth Credentials**:
   ```bash
   # Navigate to APIs & Services > Credentials
   # Create OAuth 2.0 Client ID
   # Add authorized redirect URIs
   ```

4. **Configure OAuth Consent Screen**:
   - Add required scopes
   - Set up privacy policy and terms of service
   - Submit for verification if needed

### 2. Environment Configuration

Create `.env.google-my-business` file:
```bash
# Copy example file
cp .env.google-my-business.example .env.google-my-business

# Edit with your credentials
GOOGLE_CLIENT_ID=your_client_id_here
GOOGLE_CLIENT_SECRET=your_client_secret_here
GOOGLE_REDIRECT_URI=http://localhost:3002/api/brain/integrations/google-my-business/oauth?action=callback
```

### 3. Required Scopes

The integration requires these OAuth scopes:
```python
SCOPES = [
    'https://www.googleapis.com/auth/business.manage',
    'https://www.googleapis.com/auth/plus.business.manage'
]
```

### 4. Database Setup

Ensure your tenant database includes:
```sql
-- Integration credentials table
CREATE TABLE IF NOT EXISTS tenant_integrations (
    id SERIAL PRIMARY KEY,
    tenant_id VARCHAR(255) NOT NULL,
    integration_type VARCHAR(100) NOT NULL,
    credentials JSONB NOT NULL,
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for performance
CREATE INDEX IF NOT EXISTS idx_tenant_integrations_tenant 
ON tenant_integrations(tenant_id, integration_type);
```

## Usage Examples

### Backend Usage

```python
from google_my_business_integration import google_my_business_integration

# Start OAuth flow
oauth_result = google_my_business_integration.generate_oauth_url(
    tenant_id="your_tenant", 
    scopes=['https://www.googleapis.com/auth/business.manage']
)

# Get business locations
locations = await google_my_business_integration.get_locations("your_tenant")

# Create a post
post_data = {
    "topicType": "STANDARD",
    "languageCode": "en-US", 
    "summary": "Join us for our grand opening celebration!",
    "callToAction": {
        "actionType": "LEARN_MORE",
        "url": "https://yourbusiness.com/grand-opening"
    }
}
result = await google_my_business_integration.create_post(
    "your_tenant", 
    "locations/123", 
    post_data
)

# Reply to a review
reply_result = await google_my_business_integration.reply_to_review(
    "your_tenant",
    "reviews/456",
    "Thank you for your feedback! We appreciate your business."
)
```

### Frontend Usage

```tsx
import GoogleMyBusinessIntegration from '@/components/integrations/google-my-business-integration'

function BusinessDashboard() {
  return (
    <GoogleMyBusinessIntegration 
      tenantId="your_tenant_id"
      onUpdate={(status) => console.log('GMB status:', status)}
    />
  )
}
```

## API Reference

### Authentication Endpoints

#### Start OAuth Flow
```http
POST /api/integrations/google-my-business/oauth
Content-Type: application/json

{
  "action": "start",
  "tenant_id": "demo"
}
```

Response:
```json
{
  "success": true,
  "auth_url": "https://accounts.google.com/o/oauth2/v2/auth?...",
  "state": "uuid-state-token",
  "expires_in": 900
}
```

#### Handle OAuth Callback
```http
POST /api/integrations/google-my-business/oauth
Content-Type: application/json

{
  "action": "callback",
  "code": "oauth_code",
  "state": "uuid-state-token",
  "tenant_id": "demo"
}
```

### Location Management

#### Get Locations
```http
GET /api/integrations/google-my-business/locations?tenant_id=demo
```

Response:
```json
{
  "success": true,
  "locations": [
    {
      "name": "accounts/123/locations/456",
      "location_name": "My Restaurant",
      "primary_phone": "+1-555-123-4567",
      "primary_category": "Restaurant",
      "location_state": "VERIFIED",
      "address": {...},
      "lat_lng": {...}
    }
  ],
  "count": 1
}
```

#### Create Location
```http
POST /api/integrations/google-my-business/locations
Content-Type: application/json

{
  "tenant_id": "demo",
  "title": "New Location",
  "primaryPhone": "+1-555-999-8888",
  "primaryCategory": "Restaurant",
  "address": {
    "addressLines": ["123 Main St"],
    "locality": "New York",
    "administrativeArea": "NY",
    "postalCode": "10001"
  }
}
```

### Post Management

#### Get Posts
```http
GET /api/integrations/google-my-business/locations/accounts%2F123%2Flocations%2F456/posts?tenant_id=demo
```

#### Create Post
```http
POST /api/integrations/google-my-business/locations/accounts%2F123%2Flocations%2F456/posts
Content-Type: application/json

{
  "tenant_id": "demo",
  "topicType": "STANDARD",
  "languageCode": "en-US",
  "summary": "Visit us for our weekend special!",
  "callToAction": {
    "actionType": "CALL",
    "url": "tel:+15551234567"
  }
}
```

### Review Management

#### Get Reviews
```http
GET /api/integrations/google-my-business/locations/accounts%2F123%2Flocations%2F456/reviews?tenant_id=demo
```

Response:
```json
{
  "success": true,
  "reviews": [
    {
      "name": "accounts/123/locations/456/reviews/789",
      "reviewer": {
        "displayName": "John Smith"
      },
      "star_rating": 5,
      "comment": "Great service!",
      "create_time": "2024-01-15T10:00:00Z"
    }
  ],
  "count": 1,
  "average_rating": 5.0
}
```

#### Reply to Review
```http
POST /api/integrations/google-my-business/reviews/accounts%2F123%2Flocations%2F456%2Freviews%2F789/reply
Content-Type: application/json

{
  "tenant_id": "demo",
  "reply": "Thank you for your kind words!"
}
```

### Analytics & Insights

#### Get Insights
```http
POST /api/integrations/google-my-business/locations/accounts%2F123%2Flocations%2F456/insights
Content-Type: application/json

{
  "tenant_id": "demo",
  "metric_requests": [
    {"metric": "QUERIES_DIRECT"},
    {"metric": "QUERIES_INDIRECT"},
    {"metric": "VIEWS_MAPS"},
    {"metric": "VIEWS_SEARCH"},
    {"metric": "ACTIONS_WEBSITE"},
    {"metric": "ACTIONS_PHONE"},
    {"metric": "ACTIONS_DRIVING_DIRECTIONS"}
  ]
}
```

## Error Handling

### Common Error Responses

#### Authentication Error
```json
{
  "success": false,
  "error": "No valid access token available"
}
```

#### API Quota Exceeded
```json
{
  "success": false,
  "error": "API quota exceeded. Please try again later."
}
```

#### Invalid Location
```json
{
  "success": false,
  "error": "Location not found or access denied"
}
```

### Error Handling Best Practices

1. **Token Refresh**: Automatically refresh expired tokens
2. **Retry Logic**: Implement exponential backoff for transient failures
3. **Rate Limiting**: Respect API quotas and implement client-side rate limiting
4. **User Feedback**: Provide clear error messages to users
5. **Logging**: Log all errors for debugging and monitoring

## Security Considerations

### Data Protection
- **Token Encryption**: All access tokens are encrypted before storage
- **Multi-tenant Isolation**: Data is completely isolated between tenants
- **Secure Communication**: All API calls use HTTPS
- **OAuth Best Practices**: State parameters and PKCE when available

### Rate Limiting
- **API Quotas**: Respect Google My Business API quotas
- **Request Throttling**: Implement client-side rate limiting
- **Error Handling**: Graceful degradation when limits are reached

### Access Control
- **Tenant-based Access**: All operations are tenant-scoped
- **Permission Checking**: Verify user permissions before API calls
- **Audit Logging**: Log all integration activities for compliance

## Testing

### Unit Tests
```bash
# Run integration tests
cd /path/to/bizosaas/services/bizosaas-brain
python test_google_my_business_integration.py
```

### Manual Testing Checklist
- [ ] OAuth flow completes successfully
- [ ] Locations load and display correctly
- [ ] Posts can be created and viewed
- [ ] Reviews load with correct ratings
- [ ] Review replies can be posted
- [ ] Insights data displays properly
- [ ] Error handling works as expected
- [ ] Multi-tenant isolation is maintained

## Production Deployment

### Pre-deployment Checklist
- [ ] Google Cloud Console project configured
- [ ] OAuth credentials created and configured
- [ ] API quotas sufficient for expected load
- [ ] Environment variables set correctly
- [ ] Database migrations run successfully
- [ ] SSL certificates configured for OAuth callbacks
- [ ] Monitoring and alerting configured

### Monitoring
- **API Response Times**: Track integration performance
- **Error Rates**: Monitor failed requests and their causes
- **Token Refresh**: Alert on token refresh failures
- **Quota Usage**: Monitor API quota consumption
- **User Activity**: Track integration usage patterns

### Maintenance
- **Token Cleanup**: Regular cleanup of expired tokens
- **Cache Management**: Implement appropriate TTL for cached data
- **API Updates**: Stay current with Google My Business API changes
- **Security Updates**: Regular security patches and updates

## Troubleshooting

### Common Issues

#### OAuth Redirect URI Mismatch
```bash
# Error: redirect_uri_mismatch
# Solution: Ensure redirect URI matches exactly in Google Cloud Console
```

#### Invalid Credentials
```bash
# Error: Invalid client credentials
# Solution: Verify GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET
```

#### API Not Enabled
```bash
# Error: Google My Business API has not been used
# Solution: Enable the API in Google Cloud Console
```

#### Quota Exceeded
```bash
# Error: Quota exceeded for quota metric 'Requests'
# Solution: Request quota increase or implement rate limiting
```

### Debug Mode
Enable debug mode for detailed logging:
```bash
export GMB_DEBUG_MODE=true
export GMB_LOG_LEVEL=DEBUG
```

## Support and Resources

### Documentation Links
- [Google My Business API](https://developers.google.com/my-business/content)
- [OAuth 2.0 Guide](https://developers.google.com/identity/protocols/oauth2)
- [API Quotas and Limits](https://developers.google.com/my-business/content/quota)

### Contact
For integration support, contact the BizOSaaS development team or create an issue in the project repository.

---

**Last Updated**: September 2024  
**API Version**: v1  
**Maintained By**: BizOSaaS Development Team