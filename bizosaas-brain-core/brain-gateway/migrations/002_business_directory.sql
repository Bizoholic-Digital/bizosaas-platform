-- Business Directory Tables

-- Directory listings
CREATE TABLE IF NOT EXISTS directory_listings (
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
  
  -- Constraints
  CONSTRAINT valid_status CHECK (status IN ('active', 'inactive', 'suspended')),
  CONSTRAINT valid_visibility CHECK (visibility IN ('public', 'private', 'unlisted'))
);

CREATE INDEX IF NOT EXISTS idx_directory_slug ON directory_listings(business_slug);
CREATE INDEX IF NOT EXISTS idx_directory_place_id ON directory_listings(google_place_id);
CREATE INDEX IF NOT EXISTS idx_directory_city ON directory_listings(city);
CREATE INDEX IF NOT EXISTS idx_directory_claimed ON directory_listings(claimed);

-- Directory page views (analytics)
CREATE TABLE IF NOT EXISTS directory_analytics (
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

CREATE INDEX IF NOT EXISTS idx_analytics_listing ON directory_analytics(listing_id);
CREATE INDEX IF NOT EXISTS idx_analytics_date ON directory_analytics(date);

-- Directory claim requests
CREATE TABLE IF NOT EXISTS directory_claim_requests (
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

CREATE INDEX IF NOT EXISTS idx_claim_listing ON directory_claim_requests(listing_id);
CREATE INDEX IF NOT EXISTS idx_claim_user ON directory_claim_requests(user_id);
CREATE INDEX IF NOT EXISTS idx_claim_status ON directory_claim_requests(status);
