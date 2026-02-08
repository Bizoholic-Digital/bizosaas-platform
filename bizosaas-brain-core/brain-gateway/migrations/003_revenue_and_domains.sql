-- Migration: 003_revenue_and_domains.sql
-- Description: Create tables for tracking platform revenue, affiliate commissions, and domain inventory.

-- Portal Revenue Table
CREATE TABLE IF NOT EXISTS portal_revenue (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id),
    user_id UUID REFERENCES users(id),
    source_type VARCHAR(50) NOT NULL,
    source_id VARCHAR(100),
    partner_name VARCHAR(100),
    amount FLOAT NOT NULL,
    currency VARCHAR(10) DEFAULT 'USD',
    commission_amount FLOAT DEFAULT 0.0,
    partner_payout FLOAT DEFAULT 0.0,
    status VARCHAR(20) DEFAULT 'pending',
    details JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_revenue_source_type ON portal_revenue(source_type);
CREATE INDEX IF NOT EXISTS idx_revenue_status ON portal_revenue(status);
CREATE INDEX IF NOT EXISTS idx_revenue_tenant ON portal_revenue(tenant_id);

-- Domain Inventory Table
CREATE TABLE IF NOT EXISTS domain_inventory (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id),
    user_id UUID NOT NULL REFERENCES users(id),
    domain_name VARCHAR(255) NOT NULL UNIQUE,
    registrar VARCHAR(50),
    status VARCHAR(20) DEFAULT 'active',
    expiry_date TIMESTAMP WITH TIME ZONE,
    target_service VARCHAR(50),
    target_slug VARCHAR(100),
    auto_renew BOOLEAN DEFAULT TRUE,
    dns_configured BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_domain_name ON domain_inventory(domain_name);
CREATE INDEX IF NOT EXISTS idx_domain_user ON domain_inventory(user_id);
CREATE INDEX IF NOT EXISTS idx_domain_tenant ON domain_inventory(tenant_id);
