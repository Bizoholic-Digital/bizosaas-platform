# Unified CMS Migration Guide: Strapi to Wagtail

## Overview

This guide documents the complete migration from Strapi CMS to Wagtail CMS for the BizOSaaS platform, creating a unified content management system with AI agent integration and multi-tenant support.

## Features Implemented

### 🎯 Core CMS Features
- **Multi-tenant Content Management**: Isolated content per tenant (Bizoholic, Coreldove, etc.)
- **Rich Content Types**: Landing pages, service pages, blog posts, FAQs
- **AI Agent Integration**: API endpoints for automated content creation and updates
- **Content Workflows**: Support for approval processes and scheduled publishing
- **Media Management**: Integrated image and document handling

### 🤖 AI Agent Integration
- **Content Creation API**: `POST /api/tenants/{tenant_id}/ai/content/`
- **Content Update API**: `PUT /api/tenants/{tenant_id}/ai/content/{content_id}/`
- **Template System**: AI content templates with variable substitution
- **Automated Workflows**: Support for AI-driven content generation

### 📊 Enhanced API Endpoints
```
GET  /api/tenants/                              # List all tenants
GET  /api/tenants/{tenant_id}/pages/            # All pages for tenant
GET  /api/tenants/{tenant_id}/content-summary/  # Content statistics
GET  /api/tenants/{tenant_id}/landing-pages/    # Landing pages
GET  /api/tenants/{tenant_id}/service-pages/    # Service pages  
GET  /api/tenants/{tenant_id}/content-pages/    # Blog posts/articles
GET  /api/tenants/{tenant_id}/team-members/     # Team profiles
GET  /api/tenants/{tenant_id}/testimonials/     # Client testimonials
GET  /api/tenants/{tenant_id}/navigation/       # Site navigation
GET  /api/cms/pages/                            # Unified pages endpoint
GET  /api/cms/content/{type}/                   # Content by type
POST /api/tenants/{tenant_id}/ai/content/       # AI content creation
PUT  /api/tenants/{tenant_id}/ai/content/{id}/  # AI content updates
```

## Content Types Migrated

### 1. Landing Pages (`LandingPage`)
- **Purpose**: Marketing campaign pages with A/B testing
- **Features**: CTA blocks, hero sections, conversion tracking
- **Fields**: Title, subtitle, campaign ID, variant name, conversion goals
- **StreamFields**: CTAs, features, testimonials, stats, pricing

### 2. Service Pages (`ServicePage`) 
- **Purpose**: Service descriptions and pricing
- **Features**: Pricing blocks, feature highlights, testimonials
- **Fields**: Description, icon, badge, category, pricing data
- **StreamFields**: Features, pricing plans, testimonials

### 3. Content Pages (`ContentPage`)
- **Purpose**: Blog posts and articles
- **Features**: SEO optimization, reading time, social sharing
- **Fields**: Author, publish date, excerpt, keywords
- **StreamFields**: Headings, paragraphs, images, quotes, code blocks

### 4. FAQ Pages (`FAQPage`)
- **Purpose**: Help and support content
- **Features**: Categorized Q&A sections
- **StreamFields**: FAQ sections with questions and answers

### 5. Team Members (`TeamMember`)
- **Purpose**: Team profile management
- **Fields**: Name, position, bio, photo, social links

### 6. Client Testimonials (`ClientTestimonial`)
- **Purpose**: Social proof and reviews
- **Fields**: Client info, testimonial text, rating, featured flag

### 7. AI Content Templates (`AIContentTemplate`)
- **Purpose**: Template-based content generation
- **Fields**: Template content, AI prompts, variables definition

## Migration Process

### Phase 1: Content Analysis & Mapping
1. **Strapi Content Audit**: Analyze existing content structure
2. **Field Mapping**: Map Strapi fields to Wagtail StreamFields
3. **Relationship Mapping**: Identify content relationships
4. **Media File Inventory**: Catalog images and documents

### Phase 2: Wagtail Setup & Enhancement
1. **Model Creation**: Enhanced Wagtail models with StreamFields
2. **API Development**: RESTful API for AI agent integration
3. **Multi-tenant Support**: Tenant-aware content isolation
4. **Admin Interface**: Configured admin panels and workflows

### Phase 3: Migration Execution
1. **Data Export**: Extract content from Strapi database
2. **Data Transformation**: Convert to Wagtail format
3. **Content Import**: Create pages and relationships
4. **Media Migration**: Transfer and relink media files

### Phase 4: AI Integration Setup
1. **API Authentication**: Token-based access for AI agents
2. **Content Templates**: AI prompt templates
3. **Workflow Integration**: Content approval processes
4. **Testing & Validation**: API endpoint testing

## Deployment Instructions

### Prerequisites
- Docker and Docker Compose
- PostgreSQL database
- Python 3.8+
- Network access for API calls

### Quick Deployment
```bash
# 1. Navigate to Wagtail CMS directory
cd /home/alagiri/projects/bizoholic/bizosaas/services/wagtail-cms/

# 2. Make deployment script executable
chmod +x deploy_unified_cms.py

# 3. Run complete deployment
python3 deploy_unified_cms.py
```

### Manual Step-by-Step Deployment

#### Step 1: Start Services
```bash
# Start Wagtail CMS
docker-compose up -d wagtail-cms

# Check service status
docker-compose ps
```

#### Step 2: Database Setup
```bash
# Run migrations
docker exec wagtail-cms python manage.py makemigrations
docker exec wagtail-cms python manage.py migrate

# Create superuser
docker exec -it wagtail-cms python manage.py createsuperuser
```

#### Step 3: Content Migration
```bash
# Run migration preparation
python3 strapi_to_wagtail_migration_enhanced.py

# Copy migration script to container
docker cp /tmp/wagtail_content_migration.py wagtail-cms:/tmp/

# Execute migration
docker exec wagtail-cms python /tmp/wagtail_content_migration.py
```

#### Step 4: Verification
```bash
# Test API endpoints
curl http://localhost:8000/api/tenants/
curl http://localhost:8000/api/cms/pages/
curl http://localhost:8000/api/tenants/bizoholic-main/content-summary/
```

## AI Agent Integration

### Content Creation Example
```python
import requests

# Create new landing page via AI
data = {
    \"content_type\": \"landing_page\",\n    \"content\": {\n        \"title\": \"AI-Powered Marketing Solutions\",\n        \"subtitle\": \"Transform your business with intelligent marketing\",\n        \"campaign_id\": \"ai-marketing-q1-2025\",\n        \"content_blocks\": [\n            {\n                \"type\": \"cta\",\n                \"value\": {\n                    \"title\": \"Get Started Today\",\n                    \"button_text\": \"Free Consultation\",\n                    \"button_url\": \"/contact\"\n                }\n            }\n        ]\n    }\n}\n\nresponse = requests.post(\n    \"http://localhost:8000/api/tenants/bizoholic-main/ai/content/\",\n    json=data,\n    headers={\"Authorization\": \"Bearer YOUR_AI_TOKEN\"}\n)\n```\n\n### Content Update Example\n```python\n# Update existing content\nupdate_data = {\n    \"title\": \"Updated Title\",\n    \"content_blocks\": [\n        # Updated content blocks\n    ]\n}\n\nresponse = requests.put(\n    \"http://localhost:8000/api/tenants/bizoholic-main/ai/content/123/\",\n    json=update_data,\n    headers={\"Authorization\": \"Bearer YOUR_AI_TOKEN\"}\n)\n```\n\n## Content Workflow Configuration\n\n### AI Content Approval Process\n1. **AI Generation**: AI agent creates content via API\n2. **Draft Status**: Content saved as draft\n3. **Review Queue**: Content appears in admin review queue\n4. **Approval**: Human editor reviews and approves\n5. **Publication**: Approved content goes live\n\n### Template System\n```json\n{\n  \"name\": \"Blog Post Template\",\n  \"content_type\": \"blog_post\",\n  \"ai_prompt\": \"Write a {tone} blog post about {topic} for {industry} businesses\",\n  \"template_content\": \"# {title}\\n\\n{introduction}\\n\\n## Key Points\\n{main_content}\",\n  \"variables\": {\n    \"tone\": \"professional|casual|technical\",\n    \"topic\": \"string\",\n    \"industry\": \"string\",\n    \"title\": \"string\",\n    \"introduction\": \"text\",\n    \"main_content\": \"text\"\n  }\n}\n```\n\n## Security & Authentication\n\n### API Authentication\n- **JWT Tokens**: Secure API access for AI agents\n- **Role-Based Access**: Different permissions per tenant\n- **Rate Limiting**: API call limits to prevent abuse\n- **CORS Configuration**: Secure cross-origin requests\n\n### Multi-Tenant Security\n- **Row-Level Security**: Database-level tenant isolation\n- **API Filtering**: Automatic tenant filtering in API responses\n- **Content Isolation**: No cross-tenant content access\n- **Admin Permissions**: Tenant-specific admin access\n\n## Performance Optimization\n\n### Database Optimization\n```sql\n-- Indexes for performance\nCREATE INDEX idx_pages_tenant ON wagtailcore_page(tenant_id);\nCREATE INDEX idx_pages_live ON wagtailcore_page(live);\nCREATE INDEX idx_pages_path ON wagtailcore_page(path);\n```\n\n### Caching Strategy\n- **Page Caching**: Cache rendered pages\n- **API Response Caching**: Cache API responses\n- **Image Processing**: Optimized image delivery\n- **CDN Integration**: Static asset caching\n\n### StreamField Optimization\n- **Lazy Loading**: Load StreamField blocks on demand\n- **Minimal Queries**: Optimize database queries\n- **Block Caching**: Cache individual content blocks\n\n## Monitoring & Maintenance\n\n### Health Checks\n```bash\n# Service health\ncurl http://localhost:8000/health/\n\n# Database connectivity\ncurl http://localhost:8000/api/tenants/\n\n# Content availability\ncurl http://localhost:8000/api/cms/pages/\n```\n\n### Logging Configuration\n```python\nLOGGING = {\n    'version': 1,\n    'handlers': {\n        'file': {\n            'class': 'logging.FileHandler',\n            'filename': '/var/log/wagtail/cms.log',\n        },\n    },\n    'loggers': {\n        'cms': {\n            'handlers': ['file'],\n            'level': 'INFO',\n        },\n    },\n}\n```\n\n### Backup Strategy\n1. **Database Backups**: Daily PostgreSQL dumps\n2. **Media Backups**: S3/cloud storage sync\n3. **Configuration Backups**: Git repository\n4. **Migration Scripts**: Version controlled\n\n## Troubleshooting\n\n### Common Issues\n\n#### 1. Migration Fails\n```bash\n# Check database connection\npsql -h localhost -U postgres -d bizosaas_platform\n\n# Check Wagtail service logs\ndocker logs wagtail-cms\n\n# Verify migrations\ndocker exec wagtail-cms python manage.py showmigrations\n```\n\n#### 2. API Endpoints Not Working\n```bash\n# Check URL configuration\ndocker exec wagtail-cms python manage.py show_urls\n\n# Test individual endpoints\ncurl -v http://localhost:8000/api/tenants/\n\n# Check Django admin\nopen http://localhost:8000/admin/\n```\n\n#### 3. Content Not Appearing\n```bash\n# Check tenant assignment\ndocker exec wagtail-cms python manage.py shell -c \"from cms.models import *; print(Tenant.objects.all())\"\n\n# Verify page tree\nopen http://localhost:8000/admin/pages/\n\n# Check page status\ncurl http://localhost:8000/api/tenants/bizoholic-main/pages/\n```\n\n## Future Enhancements\n\n### Planned Features\n1. **Advanced AI Integration**: GPT-4 content generation\n2. **Workflow Automation**: n8n workflow triggers\n3. **A/B Testing**: Built-in testing framework\n4. **Analytics Integration**: Content performance tracking\n5. **Headless Mode**: API-first content delivery\n\n### Scalability Improvements\n1. **Microservices**: Split into smaller services\n2. **Caching Layer**: Redis/Memcached integration\n3. **CDN Integration**: Global content delivery\n4. **Load Balancing**: Multi-instance deployment\n\n## Support & Resources\n\n### Documentation\n- **Wagtail Docs**: https://docs.wagtail.org/\n- **Django REST Framework**: https://www.django-rest-framework.org/\n- **StreamFields**: https://docs.wagtail.org/en/stable/topics/streamfield.html\n\n### Contact Information\n- **Technical Issues**: Create GitHub issue\n- **Migration Questions**: Check migration logs\n- **API Documentation**: `/api/schema/` endpoint\n\n---\n\n*This migration guide was generated as part of the BizOSaaS platform unification initiative.*