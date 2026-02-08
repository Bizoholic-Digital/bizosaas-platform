-- Create directory_enquiries table
CREATE TABLE IF NOT EXISTS directory_enquiries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    listing_id UUID NOT NULL REFERENCES directory_listings(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    subject VARCHAR(255),
    message TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'new',
    source VARCHAR(50) DEFAULT 'directory',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Add missing columns to directory_listings
ALTER TABLE directory_listings ADD COLUMN IF NOT EXISTS whatsapp VARCHAR(50);
ALTER TABLE directory_listings ADD COLUMN IF NOT EXISTS video_url VARCHAR(512);

-- Create directory_events table
CREATE TABLE IF NOT EXISTS directory_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    listing_id UUID NOT NULL REFERENCES directory_listings(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    start_date TIMESTAMP WITH TIME ZONE NOT NULL,
    end_date TIMESTAMP WITH TIME ZONE,
    location VARCHAR(255),
    image_url VARCHAR(512),
    external_link VARCHAR(512),
    status VARCHAR(20) DEFAULT 'upcoming',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create directory_coupons table
CREATE TABLE IF NOT EXISTS directory_coupons (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    listing_id UUID NOT NULL REFERENCES directory_listings(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    code VARCHAR(50),
    discount_value VARCHAR(100),
    expiry_date TIMESTAMP WITH TIME ZONE,
    terms_link VARCHAR(512),
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Add indexes
CREATE INDEX IF NOT EXISTS idx_directory_enquiries_listing_id ON directory_enquiries(listing_id);
CREATE INDEX IF NOT EXISTS idx_directory_enquiries_status ON directory_enquiries(status);
CREATE INDEX IF NOT EXISTS idx_directory_events_listing_id ON directory_events(listing_id);
CREATE INDEX IF NOT EXISTS idx_directory_events_status ON directory_events(status);
CREATE INDEX IF NOT EXISTS idx_directory_coupons_listing_id ON directory_coupons(listing_id);
CREATE INDEX IF NOT EXISTS idx_directory_coupons_status ON directory_coupons(status);
