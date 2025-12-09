-- Migration: Add OAuth Accounts table for SSO integration
-- Created: 2025-11-13
-- Description: Stores OAuth provider account linkages for users

CREATE TABLE IF NOT EXISTS oauth_accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    provider VARCHAR(50) NOT NULL,  -- 'google', 'microsoft', 'github', 'slack', 'linkedin'
    provider_user_id VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    picture TEXT,
    access_token TEXT,
    refresh_token TEXT,
    token_expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    -- Constraints
    UNIQUE(provider, provider_user_id),  -- One OAuth account per provider per provider_user_id
    UNIQUE(provider, user_id)  -- One account per provider per user
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_oauth_provider_user ON oauth_accounts(provider, provider_user_id);
CREATE INDEX IF NOT EXISTS idx_oauth_user_id ON oauth_accounts(user_id);
CREATE INDEX IF NOT EXISTS idx_oauth_email ON oauth_accounts(email);

-- Updated timestamp trigger
CREATE OR REPLACE FUNCTION update_oauth_accounts_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_oauth_accounts_updated_at
    BEFORE UPDATE ON oauth_accounts
    FOR EACH ROW
    EXECUTE FUNCTION update_oauth_accounts_updated_at();

-- Comments for documentation
COMMENT ON TABLE oauth_accounts IS 'Stores OAuth provider account linkages for SSO authentication';
COMMENT ON COLUMN oauth_accounts.provider IS 'OAuth provider name: google, microsoft, github, slack, linkedin';
COMMENT ON COLUMN oauth_accounts.provider_user_id IS 'Unique user identifier from OAuth provider';
COMMENT ON COLUMN oauth_accounts.access_token IS 'OAuth access token (encrypted in production)';
COMMENT ON COLUMN oauth_accounts.refresh_token IS 'OAuth refresh token (encrypted in production)';
