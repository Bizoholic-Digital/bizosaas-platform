# BizOSaaS Business Directory Service

A modern, AI-powered business directory microservice built with FastAPI, featuring semantic search, multi-tenant architecture, and comprehensive business management capabilities.

## 🚀 Features

### Core Functionality
- **Business Listings Management**: Complete CRUD operations for business listings
- **Hierarchical Categories**: Nested business categories with flexible organization
- **Reviews & Ratings**: Customer review system with moderation capabilities
- **Events Management**: Business events and announcements
- **Products & Services**: Product catalog management
- **Coupons & Promotions**: Promotional offers and discount management

### Advanced Features
- **AI-Powered Search**: Semantic search using vector embeddings
- **Geospatial Search**: Location-based business discovery
- **Multi-Tenant Architecture**: Complete tenant isolation with row-level security
- **Real-time Analytics**: Business performance tracking and insights
- **File Upload Support**: Image and media management
- **Business Claiming**: Owner verification and claiming system

### Technical Features
- **Vector Search**: pgvector integration for semantic similarity
- **Rate Limiting**: Configurable request throttling
- **Caching**: Redis-based performance optimization
- **Background Tasks**: Async processing for embeddings and notifications
- **Health Monitoring**: Comprehensive health checks and metrics
- **API Documentation**: Auto-generated OpenAPI/Swagger docs

## 🏗️ Architecture

### Technology Stack
- **Framework**: FastAPI 0.104+
- **Database**: PostgreSQL with pgvector extension
- **Cache**: Redis for session and data caching
- **AI/ML**: Sentence Transformers for embeddings
- **Authentication**: JWT with fastapi-users
- **Validation**: Pydantic schemas
- **ORM**: SQLAlchemy 2.0+ with async support

### Project Structure
```
business-directory/
├── core/                   # Core configuration and utilities
│   ├── config.py          # Application settings
│   ├── database.py        # Database connection and setup
│   └── security.py        # Authentication and security
├── models/                # SQLAlchemy database models
│   ├── base.py           # Base model classes and mixins
│   └── business.py       # Business-specific models
├── schemas/               # Pydantic validation schemas
│   ├── common.py         # Shared schemas
│   └── business.py       # Business-specific schemas
├── services/              # Business logic layer
│   ├── business_service.py # Business operations
│   └── search_service.py   # AI search functionality
├── api/                   # FastAPI route definitions
│   ├── businesses.py     # Business listing endpoints
│   └── categories.py     # Category management endpoints
├── migrations/            # Database migration scripts
├── tests/                # Test suite
├── main.py               # Application entry point
├── requirements.txt      # Python dependencies
├── Dockerfile           # Container configuration
└── docker-compose.yml  # Local development setup
```

## 🛠️ Installation

### Prerequisites
- Python 3.11+
- PostgreSQL 14+ with pgvector extension
- Redis 6+
- Docker & Docker Compose (optional)

### Local Development Setup

1. **Clone and Navigate**
   ```bash
   cd /path/to/bizosaas-platform/backend/services/business-directory
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Database Setup**
   ```bash
   # Ensure PostgreSQL is running with pgvector extension
   # Create database: bizosaas
   # The application will handle table creation
   ```

6. **Run the Service**
   ```bash
   python main.py
   ```

### Docker Development Setup

1. **Using Docker Compose**
   ```bash
   # Start all services
   docker-compose up -d
   
   # View logs
   docker-compose logs -f business-directory
   
   # Stop services
   docker-compose down
   ```

2. **Development with Debugging**
   ```bash
   # Start with dev profile (includes pgAdmin and Redis Commander)
   docker-compose --profile dev up -d
   ```

## 📡 API Endpoints

### Business Listings
- `GET /api/brain/business-directory/businesses` - Search and list businesses
- `POST /api/brain/business-directory/businesses` - Create new business
- `GET /api/brain/business-directory/businesses/{id}` - Get business details
- `PUT /api/brain/business-directory/businesses/{id}` - Update business
- `DELETE /api/brain/business-directory/businesses/{id}` - Delete business
- `POST /api/brain/business-directory/businesses/{id}/claim` - Claim business

### Categories
- `GET /api/brain/business-directory/categories` - List categories
- `POST /api/brain/business-directory/categories` - Create category
- `PUT /api/brain/business-directory/categories/{id}` - Update category

### Search & Discovery
- `GET /api/brain/business-directory/businesses/suggestions/autocomplete` - Business suggestions
- `GET /api/brain/business-directory/businesses/trending/searches` - Trending searches

### Analytics
- `GET /api/brain/business-directory/businesses/{id}/analytics` - Business analytics

### Health & Monitoring
- `GET /health` - Service health check
- `GET /ready` - Readiness probe
- `GET /live` - Liveness probe
- `GET /info` - Service information
- `GET /metrics` - Prometheus metrics (if enabled)

## 🔍 Search Capabilities

### Search Types
1. **Semantic Search**: AI-powered understanding of search intent
2. **Keyword Search**: Traditional text-based search
3. **Hybrid Search**: Combines semantic and keyword search
4. **Geospatial Search**: Location-based discovery with radius filtering

### Search Parameters
```json
{
  \"query\": \"italian restaurants\",
  \"search_type\": \"hybrid\",
  \"latitude\": 40.7128,
  \"longitude\": -74.0060,
  \"radius\": 10,
  \"category_id\": \"uuid\",
  \"city\": \"New York\",
  \"is_verified\": true,
  \"min_rating\": 4.0,
  \"page\": 1,
  \"size\": 20
}
```

## 🗄️ Database Schema

### Core Tables
- `business_listings` - Main business information
- `business_categories` - Hierarchical categories
- `business_reviews` - Customer reviews
- `business_events` - Business events
- `business_products` - Products/services
- `business_coupons` - Promotional offers
- `business_analytics` - Performance metrics

### Key Features
- **Multi-tenant isolation** with row-level security
- **Vector embeddings** for semantic search
- **Soft delete** support
- **Audit trails** with created/updated timestamps
- **Geospatial indexing** for location queries

## 🔐 Authentication & Security

### Authentication
- JWT-based authentication
- Token refresh mechanism
- API key support for external integrations

### Authorization
- Scope-based permissions
- Tenant-level isolation
- Role-based access control

### Security Features
- Rate limiting per endpoint
- CORS configuration
- Input validation and sanitization
- SQL injection prevention
- XSS protection

## 🚀 Deployment

### Environment Variables
Key configuration variables:

```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@host:port/db
REDIS_URL=redis://host:port/db

# Security
SECRET_KEY=your-secret-key
CORS_ORIGINS=https://yourdomain.com

# AI Features
OPENAI_API_KEY=your-openai-key
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Business Configuration
BUSINESS_APPROVAL_REQUIRED=true
REVIEW_MODERATION_REQUIRED=true
```

### Production Deployment

1. **Build Docker Image**
   ```bash
   docker build -t bizosaas/business-directory:latest .
   ```

2. **Deploy with Environment**
   ```bash
   docker run -d \\
     --name business-directory \\
     --env-file .env.production \\
     -p 8003:8003 \\
     bizosaas/business-directory:latest
   ```

3. **Kubernetes Deployment**
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: business-directory
   spec:
     replicas: 3
     selector:
       matchLabels:
         app: business-directory
     template:
       metadata:
         labels:
           app: business-directory
       spec:
         containers:
         - name: business-directory
           image: bizosaas/business-directory:latest
           ports:
           - containerPort: 8003
           env:
           - name: DATABASE_URL
             valueFrom:
               secretKeyRef:
                 name: database-secret
                 key: url
   ```

## 📊 Monitoring & Observability

### Health Checks
- `/health` - Comprehensive health status
- `/ready` - Kubernetes readiness probe
- `/live` - Kubernetes liveness probe

### Metrics
- Prometheus metrics endpoint
- Request duration and count
- Database connection pool status
- Cache hit/miss rates
- Search performance metrics

### Logging
- Structured JSON logging
- Request/response logging
- Error tracking and alerting
- Performance monitoring

## 🧪 Testing

### Run Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-mock

# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_business_service.py
```

### Test Categories
- Unit tests for business logic
- Integration tests for database operations
- API endpoint tests
- Search functionality tests
- Authentication and authorization tests

## 🤝 API Integration

### FastAPI Central Hub Integration
The service integrates with the FastAPI AI Central Hub:

```python
# Register with central hub
@app.get(\"/api/brain/business-directory/businesses\")
async def search_businesses():
    # Business directory search endpoint
    pass
```

### Client Integration Example
```python
import httpx

# Search businesses
async with httpx.AsyncClient() as client:
    response = await client.get(
        \"http://localhost:8003/api/brain/business-directory/businesses\",
        params={
            \"query\": \"coffee shops\",
            \"latitude\": 40.7128,
            \"longitude\": -74.0060,
            \"radius\": 5
        },
        headers={
            \"Authorization\": \"Bearer your-jwt-token\",
            \"X-Tenant-ID\": \"your-tenant-id\"
        }
    )
    businesses = response.json()
```

## 📝 Development Guidelines

### Code Style
- Follow PEP 8 Python style guide
- Use type hints throughout
- Document functions and classes
- Write comprehensive tests

### Git Workflow
- Feature branches for new functionality
- Pull requests for code review
- Automated testing in CI/CD
- Semantic versioning for releases

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Issues**
   ```bash
   # Check PostgreSQL status
   pg_isready -h localhost -p 5432
   
   # Verify pgvector extension
   psql -d bizosaas -c \"SELECT * FROM pg_extension WHERE extname='vector';\"
   ```

2. **Redis Connection Issues**
   ```bash
   # Test Redis connectivity
   redis-cli ping
   ```

3. **Vector Search Not Working**
   ```bash
   # Check if embedding model is loaded
   curl http://localhost:8003/health
   ```

### Performance Optimization
- Enable Redis caching
- Optimize database queries
- Use connection pooling
- Monitor search performance

## 📄 License

This project is part of the BizOSaaS platform and is subject to the platform's licensing terms.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📞 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

---

**BizOSaaS Business Directory Service** - Powering intelligent business discovery with AI and modern architecture.