# CoreLDove Comprehensive Product Requirements Document (PRD)

## Executive Summary

CoreLDove is being streamlined as the public-facing e-commerce platform of the Bizoholic ecosystem, focusing on providing a sophisticated yet accessible storefront for curated products while maintaining a private admin backend for advanced inventory management, sourcing automation, and AI-powered operations.

## Product Vision & Strategy

### Core Vision
Transform CoreLDove into a dual-mode e-commerce platform that serves as:
1. **Public Storefront**: Clean, modern e-commerce experience for customers
2. **Private Admin Hub**: Advanced AI-powered sourcing, inventory management, and automation center

### Strategic Positioning
- **Public Face**: Professional e-commerce website competing with standard online stores
- **Private Engine**: Advanced automation and AI-powered product sourcing backend
- **Integration Hub**: Central connection point for Bizoholic ecosystem services

## Architecture Overview

### Streamlined Architecture Design

```yaml
CoreLDove_Architecture:
  Public_Frontend:
    domain: "coreldove.local"
    purpose: "Customer-facing e-commerce store"
    technology: "Next.js 14 with Saleor GraphQL API backend"
    features:
      - Product browsing and search
      - Shopping cart and checkout
      - Customer accounts
      - Order tracking
      - Clean, professional UI
    
  Private_Admin:
    domain: "admin.coreldove.local"
    purpose: "AI-powered business operations center"
    technology: "FastAPI + CrewAI + N8N workflows"
    features:
      - AI product sourcing
      - Inventory automation
      - Market analysis
      - Competitor monitoring
      - N8N workflow management
      - Advanced analytics

  Integration_Layer:
    shared_database: "PostgreSQL with multi-tenant isolation"
    cache_layer: "Dragonfly for high-performance caching"
    message_queue: "Event-driven communication"
    ai_services: "CrewAI agents for automation"
```

### Technology Stack

**Public E-commerce (Customer-Facing)**
- **Frontend**: Next.js 14 with App Router (Custom BizOSaaS Integration)
- **E-commerce Engine**: Saleor (Official Docker Images)
- **API Layer**: GraphQL API with custom bridge service
- **UI Framework**: ShadCN/UI with Tailwind CSS
- **Payment Processing**: Multi-gateway support (Stripe, PayPal, Razorpay, PayU)
- **Search**: Built-in Saleor search with Elasticsearch

**Private Admin (Operations Center)**
- **Backend**: FastAPI with Python 3.11+
- **AI Framework**: CrewAI for intelligent automation
- **Workflow Engine**: N8N for visual process automation
- **Database**: PostgreSQL with pgvector for AI embeddings
- **Cache**: Dragonfly for high-performance data caching
- **Task Queue**: Temporal.io for reliable workflow orchestration

## CoreLDove-Saleor Integration Architecture

### Current Integration Status
- **Saleor Backend**: Official Docker images (API, Dashboard, Worker, Beat)
- **Bridge Service**: `/services/coreldove-bridge-saleor/` for GraphQL integration
- **Sourcing Service**: `/services/coreldove-sourcing/` with enhanced Saleor support
- **Frontend Integration**: Custom Next.js frontend connected to Saleor GraphQL
- **AI Agents**: Product sourcing, image enhancement, content generation
- **Database Schema**: Multi-tenant with AI vector storage and Saleor database
- **API Structure**: GraphQL API with RESTful bridge services

### Enhanced Integration Features

```python
# Enhanced AI Agent Capabilities
CrewAI_Agents:
  Product_Sourcing_Agent:
    purpose: "Intelligent product discovery and evaluation"
    capabilities:
      - Market trend analysis
      - Competitor price monitoring
      - Profit margin calculation
      - Supplier reliability scoring
    integrations: ["Amazon SP-API", "eBay API", "AliExpress API"]
  
  Inventory_Manager_Agent:
    purpose: "Automated inventory optimization"
    capabilities:
      - Stock level monitoring
      - Demand forecasting
      - Reorder point optimization
      - Multi-channel sync
    integrations: ["Saleor GraphQL API", "External Marketplaces"]
  
  Content_Creator_Agent:
    purpose: "AI-powered product content generation"
    capabilities:
      - SEO-optimized descriptions
      - Image enhancement and generation
      - Multi-language content
      - Brand voice consistency
    integrations: ["OpenAI GPT-4", "DALL-E", "Image Processing APIs"]
  
  Market_Analyst_Agent:
    purpose: "Competitive intelligence and market analysis"
    capabilities:
      - Price monitoring and alerts
      - Trend identification
      - Competitor analysis
      - Market opportunity scoring
    integrations: ["SERP APIs", "Social Media APIs", "Market Data APIs"]
```

### N8N Template Integration Strategy

Based on the analysis of 2000+ N8N templates from the awesome-n8n-templates repository, CoreLDove will implement the following high-value workflows:

#### Priority 1: E-commerce Operations (Immediate Implementation)
1. **Product Listing Automation**
   - Template: "Optimize & Update Printify Title and Description Workflow"
   - Purpose: Automated product listing optimization
   - Complexity: Low
   - Business Value: High - Reduces manual product management overhead

2. **Inventory Synchronization**
   - Template: "Shopify Inventory Sync" (adapted for Saleor GraphQL API)
   - Purpose: Multi-channel inventory management
   - Complexity: Intermediate
   - Business Value: Critical - Prevents overselling and stock issues

3. **Price Monitoring & Competition Analysis**
   - Template: "Competitor Price Tracking"
   - Purpose: Automated competitor price monitoring with alerts
   - Complexity: Intermediate
   - Business Value: High - Maintains competitive pricing strategy

#### Priority 2: Customer Service & Marketing (Phase 2)
1. **Email Marketing Automation**
   - Template: "Gmail AI Auto-Responder: Create Draft Replies"
   - Purpose: Automated customer inquiry responses
   - Complexity: Moderate
   - Business Value: High - Improves response times and customer satisfaction

2. **Social Media Integration**
   - Template: "Generate Instagram Content from Top Trends with AI Image Generation"
   - Purpose: Automated social media content creation
   - Complexity: Advanced
   - Business Value: Medium - Enhances brand presence

#### Priority 3: Analytics & Intelligence (Phase 3)
1. **Customer Behavior Analysis**
   - Template: "UTM Link Creator & QR Code Generator with Scheduled Google Analytics Reports"
   - Purpose: Automated marketing performance tracking
   - Complexity: Moderate
   - Business Value: Medium - Data-driven decision making

2. **Review & Testimonial Management**
   - Template: "Automate testimonials in Strapi with n8n"
   - Purpose: Automated review collection and management
   - Complexity: Low
   - Business Value: Medium - Builds social proof

### Temporal Workflow Integration

**Current Temporal Status**:
- Docker Compose configuration available
- PostgreSQL backend configured
- Elasticsearch integration for visibility
- Web UI available at port 8088
- Development-optimized configuration

**Enhanced Temporal Workflows**:

```yaml
Workflow_Categories:
  Product_Lifecycle:
    - product_sourcing_workflow
    - inventory_management_workflow
    - price_monitoring_workflow
    - listing_optimization_workflow
  
  Order_Processing:
    - order_fulfillment_workflow
    - payment_processing_workflow
    - shipping_coordination_workflow
    - customer_notification_workflow
  
  Marketing_Automation:
    - email_campaign_workflow
    - social_media_posting_workflow
    - customer_segmentation_workflow
    - retention_campaign_workflow
  
  Analytics_Intelligence:
    - market_analysis_workflow
    - competitor_monitoring_workflow
    - performance_reporting_workflow
    - trend_identification_workflow
```

## Implementation Roadmap

### Phase 1: Foundation & Streamlining (Weeks 1-2)
**Objectives**: Establish clean public/private separation and core functionality

```yaml
Week_1_Tasks:
  - Deploy streamlined public frontend (coreldove.local)
  - Configure private admin backend (admin.coreldove.local)
  - Implement basic product catalog and search
  - Set up payment gateway integration
  - Configure domain routing and SSL

Week_2_Tasks:
  - Integrate Saleor GraphQL e-commerce API
  - Set up inventory management system
  - Implement user authentication and accounts
  - Configure order processing workflows
  - Set up basic analytics tracking
```

### Phase 2: AI Integration & Automation (Weeks 3-4)
**Objectives**: Deploy AI agents and workflow automation

```yaml
Week_3_Tasks:
  - Deploy CrewAI agent system
  - Implement product sourcing automation
  - Set up N8N workflow engine integration
  - Configure Temporal workflow orchestration
  - Implement basic AI content generation

Week_4_Tasks:
  - Deploy Priority 1 N8N templates
  - Set up automated inventory synchronization
  - Implement price monitoring workflows
  - Configure competitor analysis automation
  - Set up performance monitoring dashboards
```

### Phase 3: Advanced Features & Optimization (Weeks 5-6)
**Objectives**: Deploy advanced AI features and optimization workflows

```yaml
Week_5_Tasks:
  - Deploy Priority 2 N8N templates
  - Implement advanced email automation
  - Set up social media integration workflows
  - Configure customer service automation
  - Deploy marketing automation workflows

Week_6_Tasks:
  - Deploy Priority 3 N8N templates
  - Implement advanced analytics workflows
  - Set up review and testimonial automation
  - Configure performance optimization workflows
  - Complete end-to-end testing and optimization
```

## Technical Specifications

### Database Schema
```sql
-- Enhanced multi-tenant schema with AI capabilities
CREATE TABLE tenant_products (
    id UUID PRIMARY KEY,
    tenant_id UUID NOT NULL,
    saleor_product_id VARCHAR(255),
    ai_sourcing_data JSONB,
    market_analysis JSONB,
    content_optimization JSONB,
    performance_metrics JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE ai_workflows (
    id UUID PRIMARY KEY,
    tenant_id UUID NOT NULL,
    workflow_type VARCHAR(100) NOT NULL,
    n8n_workflow_id VARCHAR(255),
    temporal_workflow_id VARCHAR(255),
    configuration JSONB,
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE market_intelligence (
    id UUID PRIMARY KEY,
    tenant_id UUID NOT NULL,
    product_id UUID REFERENCES tenant_products(id),
    competitor_data JSONB,
    pricing_history JSONB,
    trend_analysis JSONB,
    ai_recommendations JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### API Endpoints

**Public API (Customer-facing)**
```
GET  /api/products                    # Product catalog
GET  /api/products/{id}              # Product details
POST /api/cart                       # Add to cart
POST /api/orders                     # Create order
GET  /api/orders/{id}                # Order status
```

**Private API (Admin-facing)**
```
POST /api/admin/products/source      # AI product sourcing
GET  /api/admin/analytics/market     # Market analysis
POST /api/admin/workflows/deploy     # Deploy N8N template
GET  /api/admin/workflows/status     # Workflow status
POST /api/admin/ai/optimize          # AI-powered optimization
```

## Success Metrics

### Business Metrics
- **Revenue Growth**: 25% increase in monthly revenue within 3 months
- **Conversion Rate**: Improve from baseline to 3.5%+ conversion rate
- **Average Order Value**: Increase by 20% through AI-powered recommendations
- **Customer Acquisition Cost**: Reduce by 30% through automation
- **Time to Market**: 75% reduction in product listing time

### Technical Metrics
- **Page Load Speed**: <2 seconds for product pages
- **API Response Time**: <200ms for critical endpoints
- **Uptime**: 99.9% availability
- **Automation Coverage**: 80% of manual tasks automated
- **AI Accuracy**: 85%+ accuracy in product sourcing recommendations

### Operational Metrics
- **Manual Task Reduction**: 70% reduction in manual operations
- **Content Generation Speed**: 10x faster content creation with AI
- **Inventory Accuracy**: 99%+ inventory accuracy across channels
- **Customer Support Response**: <1 hour average response time
- **Workflow Success Rate**: 95%+ automated workflow completion rate

## Risk Assessment & Mitigation

### Technical Risks
1. **N8N Template Compatibility**: Some templates may require modification
   - *Mitigation*: Thorough testing and gradual rollout
   
2. **AI Model Performance**: Potential accuracy issues with sourcing decisions
   - *Mitigation*: Human oversight workflows and feedback loops
   
3. **Temporal Workflow Complexity**: Complex workflow debugging challenges
   - *Mitigation*: Comprehensive logging and monitoring

### Business Risks
1. **Customer Experience Disruption**: Changes might impact user experience
   - *Mitigation*: A/B testing and gradual feature rollout
   
2. **Integration Complexity**: Multiple system integration challenges
   - *Mitigation*: Phased implementation with fallback options

## Current Implementation Status

### ✅ Completed Components (as of September 7, 2025)

**Infrastructure & Foundation**
- **CoreLDove Frontend Container**: Successfully containerized with proper dependency resolution for React 19 RC conflicts
  - Location: `/home/alagiri/projects/bizoholic/coreldove-ecommerce/backend-storefront/`
  - Port: `http://localhost:3002`
  - Status: Functional with red/blue theme and AI-powered dropshipping branding

**Saleor E-commerce Integration**
- **Saleor GraphQL API**: Running on `http://localhost:8020/graphql/`
- **Saleor Dashboard**: Accessible at `http://localhost:9020`
- **Database Integration**: Dedicated Saleor database created in shared PostgreSQL
- **Worker Services**: Celery worker and beat services running for background tasks

**BizOSaaS Platform Integration**
- **Unified Dashboard**: Super admin dashboard with direct links to all platform components
- **Workflow Management**: Custom React-based workflow dashboard with real-time monitoring
- **SSO Architecture**: JWT-based authentication bridge designed and partially implemented

**Backend Services**
- **Wagtail CMS**: Running on `http://localhost:8006/admin/` with SSO integration
- **Temporal Web UI**: Accessible at `http://localhost:8088` for workflow debugging
- **AI Orchestrator**: Available at `http://localhost:8002` for agent management
- **Identity Service**: Core authentication running on `http://localhost:8001`

### 🔄 In Progress Components

**Multi-Platform Navigation**
- Enhanced super admin sidebar with direct access to:
  - BizOholic Marketing: `http://localhost:3001`
  - CoreLDove E-commerce: `http://localhost:3002`
  - Saleor Admin Dashboard: `http://localhost:9020`
  - Wagtail CMS: `http://localhost:8006/admin/`
  - Temporal Workflows: `http://localhost:8088`

### 📋 Pending Implementation

**Core Workflow Components**
- AI-powered product sourcing workflow with human-in-the-loop approval
- Multi-platform publishing system (Saleor + Amazon + Flipkart + Facebook + Instagram + WhatsApp)
- Automated marketing campaign generation for published products
- Performance monitoring and scalability optimization

**CMS Migration**
- Strapi to Wagtail data migration scripts
- Complete removal of Strapi services after successful migration
- Comprehensive SSO testing across all platforms

**Advanced Features**
- AI agents for keyword research and content generation  
- CoreLDove product dashboard with category selection and filtering
- Google Keyword Research API integration
- SEO content creation automation

### 🎯 Next Priority Actions

1. **Unified SSO Implementation**: Complete single sign-on across all three platforms
2. **Product Sourcing Workflow**: Implement Amazon sourcing → AI analysis → human approval flow
3. **Multi-Platform Publishing**: Build API integrations for cross-platform product publishing
4. **Performance Optimization**: Implement caching, rate limiting, and monitoring systems

## Conclusion

The CoreLDove streamlining strategy focuses on creating a powerful dual-mode platform that serves both customers and operators effectively. By leveraging the extensive N8N template library, advanced AI agents, and robust workflow orchestration, CoreLDove will become a highly automated, intelligent e-commerce platform that can scale efficiently while maintaining excellent user experience.

The integration of 2000+ N8N templates provides immediate access to proven automation patterns, while the FastAPICrewAI framework ensures scalable, intelligent operations. The Temporal workflow engine adds reliability and visibility to complex business processes, creating a robust foundation for long-term growth.

This comprehensive approach positions CoreLDove as a next-generation e-commerce platform that combines the best of modern web technologies with advanced AI automation, setting it apart from traditional e-commerce solutions.