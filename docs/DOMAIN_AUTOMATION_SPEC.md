# Domain Automation Feature Specification

## Overview
Automated domain registration and management system integrated into BizoSaaS platform, enabling clients to search, purchase, and manage domains directly through the platform while generating additional revenue.

## Business Goals
1. **Revenue Generation**: Markup on domain sales (20-30% margin)
2. **Convenience**: One-stop shop for all business needs
3. **Retention**: Lock-in customers with domain ownership
4. **Upsell**: Gateway to hosting, email, SSL services
5. **Data**: Understand customer domain preferences

## Revenue Model

### Pricing Strategy
```
Provider Cost: $10.99 (Namecheap .com)
Platform Markup: $4.00 (36% margin)
Customer Price: $14.99
```

### Revenue Streams
1. **Domain Registration**: One-time markup
2. **Domain Renewal**: Annual recurring markup
3. **Premium Domains**: Higher margins (50-100%)
4. **Add-on Services**:
   - Privacy protection: +$2.99/year
   - Email hosting: +$9.99/year
   - SSL certificates: +$19.99/year

### Projected Revenue
```
Scenario: 100 clients/month
- 60% purchase domains = 60 domains
- Average sale: $14.99
- Monthly revenue: $899.40
- Annual revenue: $10,792.80

With renewals (Year 2):
- 60 renewals @ $14.99 = $899.40
- 60 new sales @ $14.99 = $899.40
- Total Year 2: $21,585.60
```

## Provider Integrations

### Namecheap API
**Priority**: High (Best margins, reliable)

**Capabilities**:
- Domain availability check
- Domain registration
- Domain transfer
- DNS management
- WHOIS privacy
- Email forwarding

**API Endpoints**:
```
domains.check          # Check availability
domains.create         # Register domain
domains.getList        # List domains
domains.dns.setHosts   # Configure DNS
```

**Pricing**: 
- .com: $10.99/year
- .net: $12.99/year
- .org: $13.99/year

### Hostinger API
**Priority**: Medium (Good for hosting bundles)

**Capabilities**:
- Domain registration
- Hosting packages
- Email accounts
- SSL certificates

**API Endpoints**:
```
/domains/check
/domains/register
/domains/list
/hosting/create
```

**Pricing**:
- .com: $9.99/year
- .net: $11.99/year
- Hosting: From $2.99/month

### GoDaddy API
**Priority**: Low (Higher costs, but brand recognition)

**Capabilities**:
- Domain search
- Domain purchase
- DNS management
- Domain forwarding

**API Endpoints**:
```
/v1/domains/available
/v1/domains/purchase
/v1/domains/{domain}/records
```

**Pricing**:
- .com: $17.99/year (higher)
- .net: $19.99/year

## Database Schema

### `domains` Table
```sql
CREATE TABLE domains (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- Domain Details
  domain_name VARCHAR(255) UNIQUE NOT NULL,
  tld VARCHAR(10) NOT NULL, -- com, net, org, etc.
  
  -- Ownership
  tenant_id UUID REFERENCES tenants(id) NOT NULL,
  user_id UUID REFERENCES users(id),
  
  -- Provider Information
  provider VARCHAR(50) NOT NULL, -- namecheap, hostinger, godaddy
  provider_domain_id VARCHAR(255),
  provider_order_id VARCHAR(255),
  
  -- Dates
  purchase_date TIMESTAMP NOT NULL,
  expiry_date TIMESTAMP NOT NULL,
  next_renewal_date TIMESTAMP,
  
  -- Pricing
  purchase_price DECIMAL(10,2) NOT NULL,
  renewal_price DECIMAL(10,2) NOT NULL,
  provider_cost DECIMAL(10,2) NOT NULL,
  markup_amount DECIMAL(10,2) NOT NULL,
  
  -- Settings
  auto_renew BOOLEAN DEFAULT TRUE,
  privacy_protection BOOLEAN DEFAULT FALSE,
  lock_status BOOLEAN DEFAULT TRUE,
  
  -- DNS Configuration
  dns_configured BOOLEAN DEFAULT FALSE,
  nameservers JSONB,
  dns_records JSONB,
  
  -- Status
  status VARCHAR(50) DEFAULT 'active',
  -- active, expired, pending_transfer, suspended, cancelled
  
  -- Integration
  connected_to_website BOOLEAN DEFAULT FALSE,
  website_id UUID REFERENCES websites(id),
  
  -- Timestamps
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  
  CONSTRAINT valid_status CHECK (status IN (
    'active', 'expired', 'pending_transfer', 
    'suspended', 'cancelled', 'pending_registration'
  ))
);

CREATE INDEX idx_domains_tenant ON domains(tenant_id);
CREATE INDEX idx_domains_provider ON domains(provider);
CREATE INDEX idx_domains_status ON domains(status);
CREATE INDEX idx_domains_expiry ON domains(expiry_date);
```

### `domain_transactions` Table
```sql
CREATE TABLE domain_transactions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  domain_id UUID REFERENCES domains(id),
  tenant_id UUID REFERENCES tenants(id),
  
  -- Transaction Details
  transaction_type VARCHAR(50) NOT NULL,
  -- purchase, renewal, transfer_in, transfer_out, upgrade
  
  -- Pricing
  amount DECIMAL(10,2) NOT NULL, -- Customer paid
  provider_cost DECIMAL(10,2) NOT NULL, -- What we paid
  markup_amount DECIMAL(10,2) NOT NULL, -- Our profit
  
  -- Payment
  payment_method VARCHAR(50),
  payment_status VARCHAR(50) DEFAULT 'pending',
  -- pending, completed, failed, refunded
  
  -- Integration
  lago_invoice_id VARCHAR(255),
  lago_subscription_id VARCHAR(255),
  provider_transaction_id VARCHAR(255),
  
  -- Timestamps
  created_at TIMESTAMP DEFAULT NOW(),
  completed_at TIMESTAMP,
  
  CONSTRAINT valid_transaction_type CHECK (transaction_type IN (
    'purchase', 'renewal', 'transfer_in', 'transfer_out', 'upgrade'
  ))
);

CREATE INDEX idx_transactions_domain ON domain_transactions(domain_id);
CREATE INDEX idx_transactions_tenant ON domain_transactions(tenant_id);
CREATE INDEX idx_transactions_type ON domain_transactions(transaction_type);
```

### `domain_search_history` Table
```sql
CREATE TABLE domain_search_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID REFERENCES tenants(id),
  user_id UUID REFERENCES users(id),
  
  -- Search Details
  search_query VARCHAR(255) NOT NULL,
  tlds_searched TEXT[], -- ['.com', '.net', '.org']
  
  -- Results
  available_domains JSONB,
  unavailable_domains JSONB,
  premium_domains JSONB,
  
  -- Conversion
  purchased BOOLEAN DEFAULT FALSE,
  purchased_domain VARCHAR(255),
  
  -- Timestamps
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_search_tenant ON domain_search_history(tenant_id);
CREATE INDEX idx_search_query ON domain_search_history(search_query);
```

### `provider_credentials` Table
```sql
CREATE TABLE provider_credentials (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- Provider
  provider_name VARCHAR(50) UNIQUE NOT NULL,
  
  -- API Credentials (encrypted)
  api_key TEXT NOT NULL,
  api_secret TEXT,
  username TEXT,
  
  -- Configuration
  sandbox_mode BOOLEAN DEFAULT FALSE,
  enabled BOOLEAN DEFAULT TRUE,
  
  -- Rate Limiting
  rate_limit_per_minute INTEGER DEFAULT 60,
  
  -- Timestamps
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

## API Endpoints

### Domain Search
```python
@router.get("/api/domains/search")
async def search_domains(
    query: str,
    tlds: List[str] = [".com", ".net", ".org"],
    tenant_id: UUID = Depends(get_current_tenant)
):
    """
    Search for available domains across all providers
    
    Returns:
    {
      "query": "mybusiness",
      "results": [
        {
          "domain": "mybusiness.com",
          "available": true,
          "price": 14.99,
          "provider": "namecheap",
          "premium": false
        },
        {
          "domain": "mybusiness.net",
          "available": false
        }
      ],
      "suggestions": [
        "mybusiness-online.com",
        "getmybusiness.com"
      ]
    }
    """
```

### Domain Purchase
```python
@router.post("/api/domains/purchase")
async def purchase_domain(
    domain: str,
    provider: str,
    privacy_protection: bool = False,
    auto_renew: bool = True,
    tenant_id: UUID = Depends(get_current_tenant)
):
    """
    Purchase a domain through selected provider
    
    Steps:
    1. Verify domain still available
    2. Calculate total cost
    3. Create Lago invoice
    4. Process payment
    5. Register domain with provider
    6. Store in database
    7. Send confirmation email
    """
```

### Domain Management
```python
@router.get("/api/domains/tenant/{tenant_id}")
async def get_tenant_domains(tenant_id: UUID):
    """Get all domains owned by tenant"""

@router.put("/api/domains/{domain_id}/renew")
async def renew_domain(domain_id: UUID):
    """Manually renew a domain"""

@router.put("/api/domains/{domain_id}/auto-renew")
async def toggle_auto_renew(domain_id: UUID, enabled: bool):
    """Enable/disable auto-renewal"""

@router.post("/api/domains/{domain_id}/dns")
async def configure_dns(domain_id: UUID, records: List[DNSRecord]):
    """Configure DNS records"""

@router.post("/api/domains/{domain_id}/transfer")
async def initiate_transfer(domain_id: UUID, auth_code: str):
    """Transfer domain to BizoSaaS"""
```

### Admin Endpoints
```python
@router.get("/api/admin/domains/inventory")
async def get_domain_inventory():
    """Get all domains across all tenants"""

@router.get("/api/admin/domains/revenue")
async def get_domain_revenue(start_date: date, end_date: date):
    """Get revenue analytics"""

@router.put("/api/admin/domains/providers/{provider}/credentials")
async def update_provider_credentials(provider: str, credentials: dict):
    """Update API credentials for provider"""

@router.get("/api/admin/domains/renewals")
async def get_upcoming_renewals(days: int = 30):
    """Get domains expiring in next N days"""
```

## Integration Architecture

### Namecheap Integration
```python
# app/connectors/namecheap/connector.py

class NamecheapConnector:
    def __init__(self):
        self.api_key = get_secret("NAMECHEAP_API_KEY")
        self.username = get_secret("NAMECHEAP_USERNAME")
        self.base_url = "https://api.namecheap.com/xml.response"
    
    async def check_availability(self, domain: str) -> bool:
        """Check if domain is available"""
        
    async def register_domain(
        self, 
        domain: str,
        years: int = 1,
        privacy: bool = False
    ) -> dict:
        """Register a new domain"""
        
    async def get_domain_info(self, domain: str) -> dict:
        """Get domain details"""
        
    async def set_nameservers(self, domain: str, nameservers: List[str]):
        """Configure nameservers"""
        
    async def set_dns_records(self, domain: str, records: List[DNSRecord]):
        """Configure DNS records"""
```

## User Flows

### Flow 1: Domain Search & Purchase (Client Portal)
```
1. User navigates to Domains section
2. Enters desired domain name
3. System checks availability across providers
4. Shows available options with pricing
5. User selects domain + add-ons
6. Reviews cart (domain + privacy + email)
7. Confirms purchase
8. Payment processed via Lago
9. Domain registered with provider
10. Confirmation email sent
11. Domain appears in "My Domains"
```

### Flow 2: Onboarding Domain Purchase
```
1. User completes company identity step
2. System suggests: "Secure your domain now!"
3. Pre-fills search with company name
4. Shows available options
5. User can skip or purchase
6. If purchased, auto-configures for website
```

### Flow 3: Domain Renewal (Automated)
```
1. Cron job runs daily
2. Checks domains expiring in 30 days
3. For auto-renew enabled:
   a. Create Lago invoice
   b. Process payment
   c. Renew with provider
   d. Update expiry date
   e. Send confirmation
4. For auto-renew disabled:
   a. Send reminder email (30, 14, 7, 1 days before)
   b. Provide renewal link
```

### Flow 4: Admin Provider Management
```
1. Admin navigates to Domain Settings
2. Views all connected providers
3. Can add/edit API credentials
4. Set markup percentages
5. Enable/disable providers
6. View provider performance metrics
```

## Revenue Dashboard (Admin Portal)

### Key Metrics
```
┌─────────────────────────────────────────┐
│ Domain Revenue Overview                 │
├─────────────────────────────────────────┤
│ Total Domains: 247                      │
│ Active: 235 | Expired: 12              │
│                                         │
│ This Month Revenue: $3,247.53          │
│ Provider Cost: $2,156.35               │
│ Profit Margin: $1,091.18 (33.6%)      │
│                                         │
│ Upcoming Renewals (30 days): 45        │
│ Projected Revenue: $674.55             │
└─────────────────────────────────────────┘

Revenue by Provider:
- Namecheap: $1,847.20 (57%)
- Hostinger: $1,124.33 (35%)
- GoDaddy: $276.00 (8%)

Top TLDs:
- .com: 156 domains (63%)
- .net: 48 domains (19%)
- .org: 23 domains (9%)
- Other: 20 domains (8%)
```

## Automation & Cron Jobs

### Daily Tasks
```python
# Renewal reminders
@cron("0 9 * * *")  # 9 AM daily
async def send_renewal_reminders():
    """Send reminders for domains expiring soon"""
    
# Auto-renewals
@cron("0 2 * * *")  # 2 AM daily
async def process_auto_renewals():
    """Process domains set for auto-renewal"""
    
# Sync domain status
@cron("0 */6 * * *")  # Every 6 hours
async def sync_domain_status():
    """Sync status with providers"""
```

### Weekly Tasks
```python
@cron("0 10 * * 1")  # Monday 10 AM
async def generate_revenue_report():
    """Generate weekly revenue report for admins"""
```

## Security Considerations

### API Key Management
- Store in Vault (encrypted)
- Rotate keys quarterly
- Use separate keys for sandbox/production
- Audit all API calls

### Payment Security
- PCI compliance for card storage
- Use Lago for payment processing
- Implement fraud detection
- Require 2FA for large purchases

### Domain Security
- Enable domain lock by default
- Offer WHOIS privacy
- Implement transfer locks
- Monitor for unauthorized changes

## Testing Strategy

### Unit Tests
- Domain availability checks
- Price calculations
- Slug generation
- DNS record validation

### Integration Tests
- Provider API calls (sandbox)
- Payment processing
- Email notifications
- Database transactions

### E2E Tests
- Complete purchase flow
- Renewal process
- DNS configuration
- Transfer process

## Monitoring & Alerts

### Critical Alerts
- Provider API failures
- Payment processing errors
- Domain registration failures
- Renewal failures

### Performance Metrics
- API response times
- Purchase conversion rate
- Provider uptime
- Revenue per customer

## Future Enhancements

### Phase 2 Features
- Bulk domain purchase
- Domain marketplace (resell)
- Domain parking pages
- Domain appraisal tool
- WHOIS lookup tool

### Phase 3 Features
- Website builder integration
- Email hosting automation
- SSL certificate management
- CDN integration
- Advanced DNS management

---

**Last Updated**: 2026-01-16
**Status**: Planning
**Estimated Launch**: Q1 2026
