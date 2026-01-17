-- Enhanced Business Directory for Static Site Presence
-- Adds support for rich content like amenities, tags, social media, events, products, and coupons.

ALTER TABLE directory_listings 
ADD COLUMN IF NOT EXISTS amenities JSONB DEFAULT '[]',
ADD COLUMN IF NOT EXISTS tags TEXT[] DEFAULT '{}',
ADD COLUMN IF NOT EXISTS social_media JSONB DEFAULT '{}',
ADD COLUMN IF NOT EXISTS pricing_info JSONB DEFAULT '{}',
ADD COLUMN IF NOT EXISTS events JSONB DEFAULT '[]',
ADD COLUMN IF NOT EXISTS products JSONB DEFAULT '[]',
ADD COLUMN IF NOT EXISTS coupons JSONB DEFAULT '[]',
ADD COLUMN IF NOT EXISTS canonical_url VARCHAR(255);

-- Index for tags searching
CREATE INDEX IF NOT EXISTS idx_directory_tags ON directory_listings USING GIN (tags);
