# BizOSaaS Unified Authentication Service

A production-ready FastAPI-Users based authentication service designed for multi-tenant SaaS platforms with enterprise-grade security, scalability, and reliability.

## 🚀 Features

### Core Authentication
- **FastAPI-Users Integration**: Built on the robust FastAPI-Users framework
- **Multi-Tenant Support**: Complete tenant isolation with role-based access control
- **JWT + Cookie Authentication**: Dual authentication backends for flexibility
- **Cross-Platform SSO**: Single sign-on across all BizOSaaS platforms
- **Password Security**: bcrypt hashing with configurable rounds

### Security Features
- **Account Lockout Protection**: Automatic lockout after failed attempts
- **Rate Limiting**: Redis-backed rate limiting with burst protection  
- **Session Management**: Secure session tracking with Redis storage
- **Audit Logging**: Comprehensive audit trail with structured logging
- **CORS Protection**: Configurable CORS policies for production
- **Input Validation**: Comprehensive input sanitization and validation

### Production Features  
- **Health Checks**: Comprehensive health monitoring endpoints
- **Prometheus Metrics**: Built-in metrics collection for monitoring
- **Circuit Breaker**: Resilient API calls with automatic fallback
- **Retry Logic**: Exponential backoff for transient failures
- **Structured Logging**: JSON logging with correlation IDs
- **Database Connection Pooling**: Optimized PostgreSQL connections

### API Integration
- **Production-Ready Client**: Feature-rich authentication client
- **Middleware Integration**: Drop-in middleware for other services
- **Real-time Validation**: JWT validation with Redis caching
- **Session Synchronization**: Cross-platform session management

## 🏗️ Architecture

### Database Schema
```
tenants/          # Tenant organizations
├── users/        # User accounts (tenant-scoped)
├── sessions/     # Active user sessions  
└── audit_logs/   # Security and activity audit trail
```

### Authentication Flow
```
Client → JWT/Cookie → Middleware → Service
   ↓         ↓           ↓
Redis Cache ← Auth Service → PostgreSQL
```

### Multi-Tenant Strategy
- **Single Database, Multiple Schemas**: Balanced isolation and resource efficiency
- **Tenant-Scoped Users**: All users belong to specific tenants
- **Platform Access Control**: Fine-grained platform permissions
- **Resource Isolation**: Tenant-level quotas and limits

## 📦 Installation

### Prerequisites
- Python 3.11+
- PostgreSQL 15+ with asyncpg
- Redis 7+ for caching and sessions
- Docker and Docker Compose (recommended)

### Quick Start with Docker

```bash
# Clone the repository
cd /path/to/bizosaas-platform/core/services/auth-service-unified

# Copy environment configuration
cp .env.example .env

# Edit configuration
nano .env

# Start the service
docker-compose up -d

# Check health
curl http://localhost:8007/health
```

### Manual Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\\Scripts\\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="postgresql+asyncpg://user:pass@localhost:5432/bizosaas"
export REDIS_URL="redis://localhost:6379/0"
export JWT_SECRET="your-super-secret-jwt-key"

# Run the service
python main.py
```

## ⚙️ Configuration

### Environment Variables

```bash
# Database Configuration
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/bizosaas

# Redis Configuration  
REDIS_URL=redis://localhost:6379/0

# JWT Configuration
JWT_SECRET=your-super-secret-jwt-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=30

# Service Configuration
ENVIRONMENT=production
PORT=8007

# CORS Configuration
ALLOWED_ORIGINS=https://bizoholic.com,https://coreldove.com,https://app.bizosaas.com

# Security Settings
BCRYPT_ROUNDS=12
SESSION_COOKIE_SECURE=true
SESSION_COOKIE_HTTPONLY=true

# Monitoring
ENABLE_METRICS=true
```

### Production Configuration

For production deployment:

1. **Security**:
   - Use a cryptographically strong JWT secret (256+ bits)
   - Enable HTTPS-only cookies (`SESSION_COOKIE_SECURE=true`)
   - Configure proper CORS origins
   - Use strong database passwords

2. **Performance**:
   - Configure connection pooling
   - Enable Redis persistence
   - Set up load balancing
   - Configure proper resource limits

3. **Monitoring**:
   - Enable Prometheus metrics endpoint
   - Set up health check monitoring
   - Configure structured logging
   - Set up alerting for failures

## 🔧 API Reference

### Authentication Endpoints

#### SSO Login
```http
POST /auth/sso/login
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "password123",
    "platform": "bizosaas",
    "remember_me": false,
    "device_fingerprint": "optional-device-id"
}
```

**Response:**
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh_token": "refresh-token-string",
    "token_type": "bearer",
    "expires_in": 1800,
    "user": {
        "id": "uuid",
        "email": "user@example.com",
        "role": "user",
        "tenant_id": "tenant-uuid"
    },
    "tenant": {
        "id": "tenant-uuid",
        "name": "Company Name",
        "slug": "company-name"
    },
    "permissions": ["user:read", "dashboard:access"]
}
```

#### Get Current User
```http
GET /auth/me
Authorization: Bearer <access_token>
```

#### Platform Authorization
```http
GET /auth/authorize/bizoholic
Authorization: Bearer <access_token>
```

#### Logout
```http
POST /auth/sso/logout
Authorization: Bearer <access_token>
```

### FastAPI Users Endpoints

The service automatically includes all standard FastAPI Users endpoints:

- `POST /auth/jwt/login` - JWT login
- `POST /auth/cookie/login` - Cookie login
- `POST /auth/register` - User registration  
- `POST /auth/forgot-password` - Password reset request
- `POST /auth/reset-password` - Password reset
- `GET /users/me` - Current user info
- `PATCH /users/me` - Update user profile

### Health & Monitoring

```http
GET /health        # Detailed health check
GET /metrics       # Prometheus metrics
GET /             # Basic health check
```

## 🐍 Python Client Usage

### Basic Authentication

```python
import asyncio
from auth_client import AuthClient, LoginRequest

async def authenticate():
    async with AuthClient("http://localhost:8007") as client:
        # Login
        login_request = LoginRequest(
            email="user@example.com",
            password="password123",
            platform="bizosaas"
        )
        
        auth_response = await client.login(login_request)
        print(f"Authenticated as: {auth_response.user.email}")
        
        # Get current user info
        user_info = await client.get_current_user()
        print(f"User role: {user_info['permissions']['role']}")
        
        # Check platform access
        access = await client.authorize_platform("bizoholic")
        print(f"Platform access: {access['authorized']}")

asyncio.run(authenticate())
```

### Error Handling

```python
from auth_client import AuthError, RateLimitError, NetworkError

try:
    auth_response = await client.login(login_request)
except RateLimitError:
    print("Rate limit exceeded, please wait")
except NetworkError as e:
    print(f"Network error: {e}")
except AuthError as e:
    print(f"Authentication failed: {e}")
```

### Advanced Features

```python
# Circuit breaker and retry logic are built-in
client = AuthClient(
    base_url="http://localhost:8007",
    max_retries=3,
    timeout=30
)

# Session management
session_manager = SessionManager(max_concurrent_sessions=10)
client = await session_manager.create_session("user123")
```

## 🔧 Middleware Integration

### FastAPI Integration

```python
from fastapi import FastAPI, Depends
from middleware import setup_auth_middleware, require_authentication

app = FastAPI()

# Setup authentication middleware
setup_auth_middleware(
    app,
    auth_service_url="http://localhost:8007",
    secret_key="your-secret-key",
    platform_name="your-platform"
)

# Protected endpoint
@app.get("/protected")
async def protected_route(user = Depends(require_authentication)):
    return {"message": f"Hello {user['email']}"}

# Role-based endpoint
@app.get("/admin")
async def admin_route(user = Depends(require_role(["admin", "super_admin"]))):
    return {"message": "Admin access granted"}
```

### Manual Middleware Usage

```python
from middleware import AuthenticationMiddleware

app.add_middleware(
    AuthenticationMiddleware,
    auth_service_url="http://localhost:8007",
    secret_key="your-secret-key",
    platform_name="your-platform",
    excluded_paths=["/health", "/docs"]
)
```

## 🧪 Testing

### Running Tests

```bash
# Install test dependencies
pip install -r requirements.txt

# Run all tests
pytest test_auth_service.py -v

# Run specific test categories
pytest test_auth_service.py::TestAuthentication -v
pytest test_auth_service.py::TestSecurity -v

# Run with coverage
pytest test_auth_service.py --cov=main --cov-report=html
```

### Test Categories

- **Unit Tests**: Core authentication logic
- **Integration Tests**: Database and Redis integration
- **Security Tests**: Rate limiting, SQL injection protection
- **Performance Tests**: Load testing and benchmarks
- **API Tests**: Full API endpoint testing

### Mock Data

```python
# Test fixtures are provided for easy testing
@pytest.fixture
async def test_tenant():
    # Creates test tenant
    
@pytest.fixture  
async def test_user(test_tenant):
    # Creates test user in tenant
```

## 🚀 Deployment

### Docker Deployment

```bash
# Build and deploy
docker-compose up -d

# Scale for high availability
docker-compose up -d --scale bizosaas-auth-unified=3

# Update service
docker-compose pull && docker-compose up -d
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: bizosaas-auth-unified
spec:
  replicas: 3
  selector:
    matchLabels:
      app: bizosaas-auth-unified
  template:
    metadata:
      labels:
        app: bizosaas-auth-unified
    spec:
      containers:
      - name: auth-service
        image: bizosaas-auth-unified:latest
        ports:
        - containerPort: 8007
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: auth-secrets
              key: database-url
        - name: JWT_SECRET
          valueFrom:
            secretKeyRef:
              name: auth-secrets  
              key: jwt-secret
```

### Production Checklist

- [ ] Strong JWT secret configured
- [ ] Database connection pooling enabled
- [ ] Redis persistence configured
- [ ] HTTPS certificates installed
- [ ] CORS origins properly configured
- [ ] Rate limiting enabled
- [ ] Health checks configured
- [ ] Monitoring and alerting set up
- [ ] Log aggregation configured
- [ ] Backup strategy implemented

## 📊 Monitoring & Observability

### Prometheus Metrics

```
# Authentication metrics
auth_requests_total{method="sso_login", status="success"}
auth_request_duration_seconds{quantile="0.95"}

# Health metrics  
auth_service_health_status
database_connection_pool_size
redis_connection_status
```

### Health Checks

```http
GET /health
{
    "service": "bizosaas-auth-unified",
    "status": "healthy",
    "database": "connected",
    "redis": "connected", 
    "timestamp": "2024-01-15T10:30:00Z"
}
```

### Structured Logging

```json
{
    "timestamp": "2024-01-15T10:30:00Z",
    "level": "info",
    "logger": "auth-service",
    "message": "User authenticated successfully",
    "user_id": "uuid",
    "tenant_id": "tenant-uuid",
    "platform": "bizosaas"
}
```

## 🔒 Security Considerations

### Authentication Security
- JWT tokens are signed with HS256 algorithm
- Passwords hashed with bcrypt (12 rounds default)
- Account lockout after 5 failed attempts (1 hour lockout)
- Session tokens are cryptographically random UUIDs

### Network Security  
- All API communications should use HTTPS in production
- CORS configured with specific allowed origins
- Rate limiting prevents brute force attacks
- Input validation prevents injection attacks

### Data Security
- Multi-tenant data isolation at database level
- Sensitive data encrypted at rest
- Audit logging for all authentication events
- Session management with secure cookies

### Operational Security
- Health checks don't expose sensitive information
- Error messages don't leak system details
- Database credentials stored securely
- Container runs as non-root user

## 🤝 Integration Examples

### Central Brain Hub Integration

```python
# brain_gateway.py
from middleware import setup_auth_middleware

app = FastAPI()
setup_auth_middleware(
    app, 
    platform_name="brain-gateway",
    auth_service_url="http://bizosaas-auth-unified:8007"
)

@app.get("/brain/analyze")
async def analyze(user = Depends(require_platform_access(["bizosaas"]))):
    return await brain_service.analyze(user["tenant_id"])
```

### Frontend Integration

```javascript
// auth.js
class AuthService {
    constructor(baseURL = 'http://localhost:8007') {
        this.baseURL = baseURL;
    }
    
    async login(email, password, platform = 'bizosaas') {
        const response = await fetch(`${this.baseURL}/auth/sso/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password, platform })
        });
        
        if (!response.ok) throw new Error('Login failed');
        
        const auth = await response.json();
        localStorage.setItem('access_token', auth.access_token);
        return auth;
    }
    
    async getCurrentUser() {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`${this.baseURL}/auth/me`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        return response.json();
    }
}
```

## 📚 Best Practices

### Development
- Use environment-specific configuration
- Enable debug logging in development
- Use test database for development
- Mock external dependencies in tests

### Production
- Use production-grade secret management
- Enable comprehensive monitoring
- Implement proper backup strategies  
- Use connection pooling for databases
- Configure proper resource limits

### Security
- Rotate JWT secrets regularly
- Use strong passwords for all accounts
- Enable audit logging for all environments
- Monitor for suspicious authentication patterns
- Implement IP-based access controls if needed

## 🆘 Troubleshooting

### Common Issues

**Service won't start:**
```bash
# Check database connectivity
docker exec -it bizosaas-auth-unified python -c "import asyncpg; print('PostgreSQL available')"

# Check Redis connectivity  
docker exec -it bizosaas-auth-unified python -c "import redis; r=redis.Redis(); r.ping(); print('Redis available')"
```

**Authentication failures:**
```bash
# Check logs
docker logs bizosaas-auth-unified

# Verify JWT secret
docker exec -it bizosaas-auth-unified printenv JWT_SECRET
```

**Performance issues:**
```bash
# Check metrics
curl http://localhost:8007/metrics

# Monitor connections
docker stats bizosaas-auth-unified
```

### Debug Mode

```bash
# Enable debug logging
docker-compose -f docker-compose.yml -f docker-compose.debug.yml up

# Or set environment variable
export LOG_LEVEL=DEBUG
python main.py
```

## 📄 License

This project is part of the BizOSaaS platform and is proprietary software. All rights reserved.

## 🤝 Support

For issues and questions:
- Check the troubleshooting section above
- Review the comprehensive test suite for examples
- Check the health endpoints for service status
- Review structured logs for detailed error information

---

**Built with ❤️ for the BizOSaaS Platform**

*Production-ready authentication that scales with your business*