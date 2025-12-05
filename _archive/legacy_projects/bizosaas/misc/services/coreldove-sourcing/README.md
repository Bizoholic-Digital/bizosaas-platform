# CoreLDove Product Sourcing & Automation System

A comprehensive AI-powered product sourcing and automation system designed for dropshipping and e-commerce operations. This system integrates Amazon product discovery, human-in-the-loop approval workflows, keyword research, AI content generation, image enhancement, and n8n workflow automation.

## 🚀 Features

### 1. **Amazon Product Sourcing**
- **Intelligent Product Discovery**: AI-powered search and filtering based on profitability, demand, and competition analysis
- **Real-time Market Analysis**: Automated scoring of products using demand metrics, competition levels, and profit potential
- **Multi-criteria Filtering**: Advanced filtering by price, rating, category, brand exclusions, and profit margin targets
- **Batch Processing**: Handle large-scale product discovery with background processing queues

### 2. **Human-in-the-Loop Approval**
- **Interactive Review Interface**: Clean, intuitive interface for human reviewers to approve/reject products
- **AI Analysis Integration**: Display AI-generated insights including demand scores, competition analysis, and profitability metrics
- **Approval Workflows**: Configurable approval processes with notes, feedback, and revision requests
- **Bulk Operations**: Process multiple products simultaneously with batch approval capabilities

### 3. **Keyword Research Integration**
- **Google Keyword Planner API**: Automatic keyword research for approved products
- **Multi-API Support**: Extensible architecture for additional keyword research APIs
- **SEO Optimization**: Generate keyword density recommendations and content optimization suggestions
- **Geographic Targeting**: Location-specific keyword research for different markets

### 4. **AI Content Generation**
- **Multi-format Content**: Generate titles, descriptions, bullet points, meta descriptions, and tags
- **SEO-Optimized**: Built-in SEO analysis and optimization for better search rankings
- **Tone Customization**: Professional, casual, friendly, authoritative, and persuasive tones
- **A/B Testing Support**: Generate multiple content variations for testing
- **Platform Optimization**: Content optimized for Amazon, eBay, Shopify, and other platforms

### 5. **Product Image Enhancement**
- **Branding Removal**: AI-powered detection and removal of competitor branding and watermarks
- **Quality Enhancement**: Automatic image sharpening, contrast adjustment, and color correction
- **Multi-format Output**: Support for JPG, PNG, WebP, and AVIF formats
- **Responsive Variants**: Generate multiple image sizes (main, thumbnail, mobile)
- **Watermark Addition**: Add custom branding and watermarks to processed images
- **Background Removal**: AI-powered background removal for clean product shots

### 6. **N8N Workflow Templates**
- **Awesome N8N Integration**: Connect to the awesome-n8n-templates repository (2000+ templates)
- **E-commerce Focused**: Curated templates for product sourcing, inventory management, and marketplace automation
- **Template Deployment**: One-click deployment of workflow templates to n8n instances
- **Custom Workflows**: Create and manage custom automation workflows
- **Multi-platform Support**: Templates for Amazon, eBay, Shopify, and other platforms

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend UI   │    │  FastAPI Main   │    │   PostgreSQL    │
│   (React/Next)  │◄──►│    Service      │◄──►│   Database      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Amazon Product  │    │ Keyword Research│    │ Content Gen     │
│   Sourcing      │    │   Integration   │    │   Service       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Image Enhancement│    │ N8N Templates  │    │ Approval       │
│   Pipeline      │    │   Manager       │    │ Workflows      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL 15+
- Redis 7+

### Environment Variables

Create a `.env` file in the service root:

```env
# Database Configuration
POSTGRES_HOST=localhost
POSTGRES_USER=admin
POSTGRES_PASSWORD=securepassword
POSTGRES_DB=bizosaas

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379

# AI Services
OPENROUTER_API_KEY=your_openrouter_key
OPENAI_API_KEY=your_openai_key
OPENAI_BASE_URL=https://openrouter.ai/api/v1

# E-commerce APIs
AMAZON_API_KEY=your_amazon_key
EBAY_API_KEY=your_ebay_key
GOOGLE_ADS_API_KEY=your_google_ads_key

# N8N Integration
N8N_API_URL=http://localhost:5678/api/v1
N8N_API_KEY=your_n8n_api_key

# Storage & CDN
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_S3_BUCKET=your_s3_bucket
CDN_BASE_URL=https://cdn.your-domain.com
```

### Quick Start with Docker

1. **Build and start the service:**
```bash
# From the project root
docker-compose up coreldove-sourcing --build
```

2. **Initialize the database:**
```bash
# Execute the database schema
psql -h localhost -U admin -d bizosaas -f services/coreldove-sourcing/database_schema.sql
```

3. **Access the service:**
- API: http://localhost:8010
- Documentation: http://localhost:8010/docs
- Frontend Integration: http://localhost:3000/coreldove/sourcing

### Manual Development Setup

1. **Install Python dependencies:**
```bash
cd services/coreldove-sourcing
pip install -r requirements.txt
```

2. **Install additional AI/ML dependencies:**
```bash
# For image processing
pip install opencv-python rembg
sudo apt-get install libmagickwand-dev

# For natural language processing
python -m nltk.downloader punkt stopwords
```

3. **Run the service:**
```bash
python main.py
```

## 📖 API Documentation

### Core Endpoints

#### Amazon Product Search
```http
POST /amazon/search
Content-Type: application/json

{
  "keywords": ["wireless bluetooth headphones"],
  "category": "electronics",
  "min_price": 20,
  "max_price": 100,
  "min_rating": 4.0,
  "max_results": 50,
  "profit_margin_target": 35.0
}
```

#### Product Approval
```http
POST /products/{product_id}/approve
Content-Type: application/json

{
  "notes": "Great profit potential and strong reviews",
  "feedback": {
    "market_demand": "high",
    "competition": "moderate"
  }
}
```

#### Keyword Research
```http
POST /products/{product_id}/keyword-research
Content-Type: application/json

{
  "primary_keywords": ["wireless headphones", "bluetooth earbuds"],
  "target_audience": "tech-savvy consumers",
  "geographic_location": "US"
}
```

#### Content Generation
```http
POST /products/{product_id}/generate-content
Content-Type: application/json

{
  "content_types": ["title", "description", "bullet_points"],
  "tone": "professional",
  "include_seo_optimization": true,
  "generate_variations": true
}
```

#### Image Enhancement
```http
POST /products/{product_id}/enhance-images
Content-Type: application/json

{
  "enhancement_types": ["remove_branding", "enhance_quality", "optimize_size"],
  "output_formats": ["jpg", "webp"],
  "target_dimensions": {
    "main": [1000, 1000],
    "thumbnail": [300, 300]
  }
}
```

### Workflow Automation
```http
POST /workflows/automation
Content-Type: application/json

{
  "product_ids": ["prod_1", "prod_2"],
  "workflow_template": "full_automation",
  "target_marketplaces": ["shopify", "ebay"],
  "skip_approval": false
}
```

## 🔧 Configuration

### Search Optimization
```python
# Customize search criteria in the frontend
search_criteria = {
    "keywords": ["your", "product", "keywords"],
    "category": "electronics",
    "min_price": 10,
    "max_price": 500,
    "min_rating": 3.5,
    "profit_margin_target": 30.0,
    "ai_optimization_enabled": True
}
```

### Content Generation Settings
```python
# Configure AI content generation
content_config = {
    "tone": "professional",
    "target_audience": "general consumers",
    "character_limits": {
        "title": 200,
        "description": 2000,
        "meta_description": 160
    },
    "seo_optimization": True
}
```

### Image Enhancement Pipeline
```python
# Configure image processing
enhancement_config = {
    "enhancement_types": [
        "remove_branding",
        "enhance_quality", 
        "optimize_size",
        "add_watermark"
    ],
    "target_dimensions": {
        "main": (1000, 1000),
        "thumbnail": (300, 300),
        "mobile": (600, 600)
    },
    "watermark_config": {
        "text": "Your Brand",
        "position": "bottom_right",
        "opacity": 0.3
    }
}
```

## 🧪 Testing

### Run Unit Tests
```bash
cd services/coreldove-sourcing
python -m pytest tests/ -v
```

### Integration Testing
```bash
# Test API endpoints
python -m pytest tests/integration/ -v

# Test image processing
python -m pytest tests/test_image_enhancement.py -v

# Test content generation
python -m pytest tests/test_content_generation.py -v
```

### Load Testing
```bash
# Install load testing tools
pip install locust

# Run load tests
locust -f tests/load_test.py --host=http://localhost:8010
```

## 📊 Monitoring & Analytics

### Built-in Metrics
- **Product Sourcing**: Success rates, processing times, API costs
- **Approval Workflow**: Approval rates, review times, rejection reasons
- **Content Generation**: Quality scores, SEO metrics, generation costs
- **Image Processing**: Enhancement success rates, file size reductions, quality improvements

### Prometheus Integration
The service exposes metrics at `/metrics`:
- `coreldove_products_sourced_total`
- `coreldove_approvals_processed_total`  
- `coreldove_content_generation_duration_seconds`
- `coreldove_image_processing_duration_seconds`

### Dashboard Access
- Service Health: http://localhost:8010/health
- API Documentation: http://localhost:8010/docs
- Metrics Endpoint: http://localhost:8010/metrics

## 🔄 Workflow Templates

### Available N8N Templates

| Template | Category | Use Case | Complexity |
|----------|----------|----------|------------|
| Amazon Product Monitor | Monitoring | Price Tracking | Intermediate |
| eBay Listing Automation | Automation | Marketplace Listing | Advanced |
| Shopify Inventory Sync | Synchronization | Inventory Management | Intermediate |
| Keyword Research Automation | Research | SEO Optimization | Advanced |
| Competitor Price Tracking | Monitoring | Competitive Analysis | Intermediate |
| Product Image Processor | Processing | Image Optimization | Advanced |

### Custom Workflow Creation
```python
# Create custom workflow
workflow_config = {
    "name": "Custom Product Pipeline",
    "steps": [
        {"type": "amazon_search", "config": {...}},
        {"type": "ai_analysis", "config": {...}},
        {"type": "human_approval", "config": {...}},
        {"type": "content_generation", "config": {...}},
        {"type": "image_enhancement", "config": {...}},
        {"type": "marketplace_listing", "config": {...}}
    ]
}
```

## 🔐 Security

### Authentication & Authorization
- JWT-based authentication
- Role-based access control (RBAC)
- Tenant-level data isolation
- API key management for external services

### Data Protection
- Row-level security (RLS) in PostgreSQL
- Encrypted API credentials storage
- Secure file upload and processing
- Rate limiting and request validation

### Compliance
- GDPR compliance for user data
- SOC 2 Type II security controls
- Regular security audits and penetration testing

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style
- Follow PEP 8 for Python code
- Use type hints for all functions
- Write comprehensive docstrings
- Add unit tests for new features

### Testing Requirements
- Minimum 80% code coverage
- All tests must pass
- Integration tests for API endpoints
- Load tests for performance-critical features

## 📚 Additional Resources

- [API Documentation](http://localhost:8010/docs)
- [N8N Templates Repository](https://github.com/enescingoz/awesome-n8n-templates)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Amazon Product Advertising API](https://webservices.amazon.com/paapi5/documentation/)
- [Google Ads API](https://developers.google.com/google-ads/api)

## 🐛 Troubleshooting

### Common Issues

**Service won't start:**
```bash
# Check logs
docker-compose logs coreldove-sourcing

# Verify environment variables
docker-compose exec coreldove-sourcing env | grep -E "(POSTGRES|REDIS|API_KEY)"
```

**Database connection errors:**
```bash
# Test database connectivity
docker-compose exec coreldove-sourcing python -c "
import asyncio
from shared.database.connection import get_postgres_session
asyncio.run(get_postgres_session('test')())
"
```

**API integration failures:**
- Verify API keys are correct and have proper permissions
- Check rate limits and usage quotas
- Review API endpoint URLs and authentication methods

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built with ❤️ by the CoreLDove Team**

For support, contact: support@coreldove.com