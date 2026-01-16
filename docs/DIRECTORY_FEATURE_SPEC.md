# Business Directory Feature Specification

## Overview
The Business Directory is a value-added feature that provides free landing pages for businesses discovered during onboarding, creating immediate value and generating leads for domain/website services.

## Business Goals
1. **Immediate Value**: Every business gets a free online presence
2. **Lead Generation**: Capture businesses without websites
3. **Upsell Opportunity**: Convert free listings to paid services
4. **SEO Benefit**: Build authority through comprehensive local business directory
5. **Data Collection**: Gather business information for market intelligence

## Technical Architecture

### Domain Strategy
- **Phase 1 (Current)**: Use `bizoholic.net` subdomains
  - Format: `{business-slug}.bizoholic.net`
  - Example: `pizza-hut-mumbai.bizoholic.net`
  
- **Phase 2 (Future)**: Migrate to dedicated domain
  - Format: `{business-slug}.bizolocal.com`
  - Example: `pizza-hut-mumbai.bizolocal.com`

### Slug Generation Algorithm
```
Business Name: "The Spot Café & Lounge"
Location: "Bandra, Mumbai"

Step 1: Normalize name
  → "the spot cafe lounge"

Step 2: Remove special characters
  → "the-spot-cafe-lounge"

Step 3: Add location identifier
  → "the-spot-cafe-lounge-bandra-mumbai"

Step 4: Ensure uniqueness (check DB)
  → "the-spot-cafe-lounge-bandra-mumbai-2" (if duplicate)

Final Slug: "the-spot-cafe-lounge-bandra-mumbai"
```

## Database Schema

### `directory_listings` Table
```sql
CREATE TABLE directory_listings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  business_slug VARCHAR(255) UNIQUE NOT NULL,
  business_name VARCHAR(255) NOT NULL,
  google_place_id VARCHAR(255) UNIQUE,
  
  -- Contact Information
  address TEXT,
  city VARCHAR(100),
  state VARCHAR(100),
  country VARCHAR(100),
  postal_code VARCHAR(20),
  phone VARCHAR(50),
  email VARCHAR(255),
  website VARCHAR(255),
  
  -- Business Details
  category VARCHAR(100),
  description TEXT,
  hours_of_operation JSONB,
  
  -- Google Places Data
  google_rating DECIMAL(2,1),
  google_reviews_count INTEGER,
  google_photos JSONB,
  google_data JSONB, -- Full place details
  
  -- Ownership & Claims
  claimed BOOLEAN DEFAULT FALSE,
  claimed_by UUID REFERENCES users(id),
  claimed_at TIMESTAMP,
  verification_status VARCHAR(50) DEFAULT 'unverified',
  
  -- SEO
  meta_title VARCHAR(255),
  meta_description TEXT,
  keywords TEXT[],
  
  -- Status
  status VARCHAR(50) DEFAULT 'active', -- active, inactive, suspended
  visibility VARCHAR(50) DEFAULT 'public', -- public, private, unlisted
  
  -- Timestamps
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  last_synced_at TIMESTAMP,
  
  -- Indexes
  CONSTRAINT valid_status CHECK (status IN ('active', 'inactive', 'suspended')),
  CONSTRAINT valid_visibility CHECK (visibility IN ('public', 'private', 'unlisted'))
);

CREATE INDEX idx_directory_slug ON directory_listings(business_slug);
CREATE INDEX idx_directory_place_id ON directory_listings(google_place_id);
CREATE INDEX idx_directory_city ON directory_listings(city);
CREATE INDEX idx_directory_claimed ON directory_listings(claimed);
```

### `directory_analytics` Table
```sql
CREATE TABLE directory_analytics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  listing_id UUID REFERENCES directory_listings(id) ON DELETE CASCADE,
  
  -- Traffic Metrics
  page_views INTEGER DEFAULT 0,
  unique_visitors INTEGER DEFAULT 0,
  
  -- Engagement Metrics
  phone_clicks INTEGER DEFAULT 0,
  website_clicks INTEGER DEFAULT 0,
  direction_clicks INTEGER DEFAULT 0,
  
  -- Conversion Metrics
  claim_requests INTEGER DEFAULT 0,
  upgrade_requests INTEGER DEFAULT 0,
  
  -- Time-based
  date DATE NOT NULL,
  
  -- Timestamps
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  
  UNIQUE(listing_id, date)
);

CREATE INDEX idx_analytics_listing ON directory_analytics(listing_id);
CREATE INDEX idx_analytics_date ON directory_analytics(date);
```

### `directory_claim_requests` Table
```sql
CREATE TABLE directory_claim_requests (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  listing_id UUID REFERENCES directory_listings(id),
  user_id UUID REFERENCES users(id),
  
  -- Verification Details
  verification_method VARCHAR(50), -- email, phone, document
  verification_data JSONB,
  
  -- Status
  status VARCHAR(50) DEFAULT 'pending', -- pending, approved, rejected
  reviewed_by UUID REFERENCES users(id),
  reviewed_at TIMESTAMP,
  rejection_reason TEXT,
  
  -- Timestamps
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  
  CONSTRAINT valid_claim_status CHECK (status IN ('pending', 'approved', 'rejected'))
);

CREATE INDEX idx_claim_listing ON directory_claim_requests(listing_id);
CREATE INDEX idx_claim_user ON directory_claim_requests(user_id);
CREATE INDEX idx_claim_status ON directory_claim_requests(status);
```

## API Endpoints

### Public Endpoints
```
GET  /api/directory/{slug}              # Get listing by slug
GET  /api/directory/search              # Search listings
GET  /api/directory/nearby              # Get nearby businesses
POST /api/directory/{slug}/view         # Track page view
POST /api/directory/{slug}/click        # Track click event
```

### Authenticated Endpoints
```
POST /api/directory/claim/{slug}        # Claim a listing
GET  /api/directory/my-listings         # Get user's claimed listings
PUT  /api/directory/{slug}              # Update listing (owner only)
```

### Admin Endpoints
```
GET  /api/admin/directory/listings      # Get all listings
GET  /api/admin/directory/claims        # Get claim requests
PUT  /api/admin/directory/claims/{id}   # Approve/reject claim
GET  /api/admin/directory/analytics     # Get analytics dashboard
```

## Landing Page Template

### Required Sections
1. **Header**
   - Business name
   - Category/industry
   - Rating & reviews count
   - "Claim this business" CTA

2. **Contact Information**
   - Address with map embed
   - Phone (click-to-call)
   - Website link
   - Email

3. **Business Details**
   - Description
   - Hours of operation
   - Photos gallery

4. **Social Proof**
   - Google reviews
   - Rating display

5. **Call-to-Actions**
   - "Get a Free Website" → Upsell to website builder
   - "Claim Your Business" → Lead capture
   - "Get Directions" → Google Maps

6. **Footer**
   - "Powered by Bizoholic Digital"
   - Links to platform
   - Privacy policy

### SEO Optimization
- **Title**: `{Business Name} - {City}, {State} | Bizoholic Local`
- **Meta Description**: `Find {Business Name} in {City}. Get address, phone, hours, and more. {Category} serving {Location}.`
- **Schema.org Markup**: LocalBusiness structured data
- **Open Graph Tags**: For social sharing

## User Flows

### Flow 1: Onboarding (Business Without Website)
```
1. User searches "The Spot" in onboarding
2. System finds Google Place but no website
3. System generates: the-spot-bandra-mumbai.bizoholic.net
4. System creates directory listing in database
5. User sees generated URL in website field
6. User completes onboarding
7. Landing page is live and indexed
```

### Flow 2: Business Owner Claims Listing
```
1. Business owner discovers their listing
2. Clicks "Claim this business"
3. Verifies ownership (email/phone/document)
4. Admin reviews claim request
5. Claim approved → owner gets dashboard access
6. Owner can update info, add photos, etc.
7. Upsell: "Upgrade to custom domain"
```

### Flow 3: Customer Discovers Business
```
1. Customer searches Google for "cafes in Bandra"
2. Finds listing in search results
3. Visits landing page
4. Clicks phone number to call
5. Clicks "Get Directions"
6. Analytics tracked for business owner
```

## Monetization Strategy

### Free Tier
- Basic directory listing
- Google Places data sync
- Contact information display
- "Powered by Bizoholic" branding

### Premium Tier ($29/month)
- Remove "Powered by" branding
- Custom photos & description
- Priority in search results
- Advanced analytics
- Lead capture forms

### Enterprise Tier ($99/month)
- Custom domain (e.g., thespotcafe.com)
- Full website builder
- Online ordering/booking
- CRM integration
- Multi-location support

## Success Metrics

### Technical Metrics
- Page load time < 2 seconds
- Mobile responsiveness score > 95
- SEO score > 90
- Uptime > 99.9%

### Business Metrics
- Listings created per month
- Claim rate (% of listings claimed)
- Conversion rate (free → paid)
- Average revenue per listing
- Customer acquisition cost

### User Metrics
- Page views per listing
- Average time on page
- Click-through rate (CTR)
- Bounce rate

## Implementation Phases

### Phase 1: MVP (Week 1-2)
- [x] Slug generation
- [x] Database schema
- [x] Basic landing page template
- [x] Google Places data sync
- [ ] Deploy to bizoholic.net

### Phase 2: Claims & Ownership (Week 3-4)
- [ ] Claim request flow
- [ ] Verification system
- [ ] Owner dashboard
- [ ] Admin approval interface

### Phase 3: Analytics & SEO (Week 5-6)
- [ ] Analytics tracking
- [ ] SEO optimization
- [ ] Sitemap generation
- [ ] Search functionality

### Phase 4: Monetization (Week 7-8)
- [ ] Premium tier features
- [ ] Payment integration
- [ ] Upgrade flows
- [ ] Revenue dashboard

## Technical Considerations

### Performance
- Use CDN for static assets
- Implement caching (Redis)
- Lazy load images
- Optimize database queries

### Security
- Rate limiting on public endpoints
- CAPTCHA on claim requests
- Input validation & sanitization
- XSS protection

### Scalability
- Horizontal scaling ready
- Database sharding by geography
- Async job processing for data sync
- Queue system for bulk operations

## Future Enhancements
- Multi-language support
- Review system (beyond Google)
- Booking/reservation system
- Online ordering integration
- Social media integration
- Email marketing for claimed businesses
- Mobile app for business owners

---

**Last Updated**: 2026-01-16
**Status**: In Development
**Owner**: Product Team
