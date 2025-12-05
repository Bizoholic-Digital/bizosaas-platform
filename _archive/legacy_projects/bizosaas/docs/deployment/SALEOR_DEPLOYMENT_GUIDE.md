# CoreLDove Complete Saleor E-commerce Platform

## Overview

This deployment provides a complete Saleor e-commerce platform with full GraphQL schema support for the CoreLDove storefront. It replaces the simplified API at port 8024 with a production-ready Saleor backend that supports all standard e-commerce operations.

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Ports 8024, 9020, 5433, and 6380 available
- At least 4GB RAM available for containers
- Python 3.6+ for testing scripts

### Deployment

```bash
# Deploy complete Saleor infrastructure
./deploy-saleor-complete.sh deploy

# Check status
./deploy-saleor-complete.sh status

# Validate GraphQL schema
./deploy-saleor-complete.sh validate

# Run integration tests
python3 test-saleor-integration.py
```

## 📋 Services Overview

| Service | Port | Description | Health Check |
|---------|------|-------------|--------------|
| **Saleor API** | 8024 | Complete GraphQL API | `/health/` |
| **Saleor Dashboard** | 9020 | Admin interface | `/` |
| **PostgreSQL** | 5433 | Dedicated database | `pg_isready` |
| **Redis** | 6380 | Cache & task queue | `redis-cli ping` |
| **Celery Worker** | - | Background tasks | `celery inspect ping` |
| **Celery Beat** | - | Scheduled tasks | Django shell |

## 🔧 Configuration

### Environment Variables

The deployment uses `/home/alagiri/projects/bizoholic/bizosaas/.env.saleor` for configuration:

```bash
# Core configuration
DEBUG=true
SALEOR_SECRET_KEY=saleor-coreldove-production-secret-key-2025
SALEOR_DB_PASSWORD=saleor_secure_2025

# Email settings
DEFAULT_FROM_EMAIL=noreply@coreldove.com
EMAIL_URL=console://

# Payment gateways
STRIPE_PUBLIC_KEY=pk_test_development
STRIPE_SECRET_KEY=sk_test_development

# External services
VATLAYER_ACCESS_KEY=
OPENEXCHANGERATES_API_KEY=
```

### Saleor Configuration

Advanced settings in `/home/alagiri/projects/bizoholic/bizosaas/saleor-config/settings.py`:

- Shop name: "CoreLDove Marketplace"
- Default currency: USD
- Multi-channel support enabled
- Digital product fulfillment
- Worldwide shipping zones
- Tax calculation
- Payment gateways (Stripe, Dummy)

## 🔗 GraphQL Schema

### Key Features Enabled

✅ **Complete E-commerce Schema**
- Products, variants, and categories
- Shopping cart and checkout
- Order management
- Customer accounts
- Payment processing
- Shipping calculations
- Inventory management
- Multi-channel support

✅ **Advanced Features**
- Gift cards
- Discounts and promotions
- Stock reservations
- Warehouse management
- Tax calculations
- Webhooks
- Apps and plugins

### GraphQL Endpoints

- **Main API**: `http://localhost:8024/graphql/`
- **Playground**: `http://localhost:8024/graphql/` (with introspection)
- **Admin Dashboard**: `http://localhost:9020/`

### Example Queries

#### Shop Information
```graphql
query {
  shop {
    name
    description
    defaultCountry {
      code
      country
    }
  }
}
```

#### Products with Variants
```graphql
query {
  products(first: 10) {
    edges {
      node {
        id
        name
        slug
        variants {
          id
          name
          pricing {
            price {
              gross {
                amount
                currency
              }
            }
          }
        }
      }
    }
  }
}
```

#### Create Checkout
```graphql
mutation {
  checkoutCreate(input: {
    channel: "default-channel"
    lines: [
      {
        variantId: "UHJvZHVjdFZhcmlhbnQ6MQ=="
        quantity: 1
      }
    ]
  }) {
    checkout {
      id
      token
      lines {
        id
        quantity
      }
    }
    errors {
      field
      message
    }
  }
}
```

## 🔄 Integration with CoreLDove Storefront

### Storefront Configuration

Update your storefront environment variables:

```bash
# In your storefront .env file
NEXT_PUBLIC_SALEOR_API_URL=http://localhost:8024/graphql/
SALEOR_API_URL=http://localhost:8024/graphql/
```

### Required Schema Fields

The deployment provides all standard Saleor schema fields including:

- `channels` - Multi-channel support
- `checkoutLinesAdd` - Shopping cart operations
- `products` - Product catalog
- `productVariants` - Product variations
- `orders` - Order management
- `users` - Customer accounts
- `categories` - Product categorization
- `collections` - Product collections
- `shippingZones` - Shipping configuration
- `paymentGateways` - Payment processing
- `warehouses` - Inventory management
- `stocks` - Stock tracking

## 🧪 Testing

### Automated Testing

Run comprehensive integration tests:

```bash
# Full test suite
python3 test-saleor-integration.py

# Wait for services to start (if needed)
python3 test-saleor-integration.py --wait 60

# Test against different URL
python3 test-saleor-integration.py --url http://localhost:8024/graphql/
```

### Manual Testing

```bash
# Test basic connectivity
curl -X POST http://localhost:8024/graphql/ \
  -H "Content-Type: application/json" \
  -d '{"query": "{ shop { name } }"}'

# Test schema introspection
curl -X POST http://localhost:8024/graphql/ \
  -H "Content-Type: application/json" \
  -d '{"query": "{ __schema { queryType { name } } }"}'
```

## 📊 Monitoring & Management

### Health Checks

```bash
# Check all services
./deploy-saleor-complete.sh status

# View logs
./deploy-saleor-complete.sh logs

# View specific service logs
./deploy-saleor-complete.sh logs saleor-api
./deploy-saleor-complete.sh logs saleor-worker
```

### Database Management

```bash
# Access PostgreSQL
docker-compose -f docker-compose.saleor-full.yml exec saleor-postgres psql -U saleor -d saleor_coreldove

# Check database size
docker-compose -f docker-compose.saleor-full.yml exec saleor-postgres psql -U saleor -d saleor_coreldove -c "SELECT pg_size_pretty(pg_database_size('saleor_coreldove'));"
```

### Redis Management

```bash
# Access Redis CLI
docker-compose -f docker-compose.saleor-full.yml exec saleor-redis redis-cli

# Check Redis info
docker-compose -f docker-compose.saleor-full.yml exec saleor-redis redis-cli info memory
```

## 🔒 Security

### Production Checklist

Before deploying to production:

1. **Change Secret Keys**
   ```bash
   # Generate new secret key
   python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

2. **Update Database Credentials**
   ```bash
   # Use strong passwords
   SALEOR_DB_PASSWORD=your_secure_password_here
   ```

3. **Configure HTTPS**
   ```yaml
   # In docker-compose.saleor-full.yml
   environment:
     - SECURE_SSL_REDIRECT=True
     - SECURE_PROXY_SSL_HEADER=HTTP_X_FORWARDED_PROTO,https
   ```

4. **Restrict CORS Origins**
   ```bash
   CORS_ALLOW_ALL=False
   CORS_ALLOWED_ORIGINS=https://your-storefront-domain.com
   ```

5. **Enable Email Verification**
   ```bash
   ENABLE_EMAIL_CONFIRMATION=True
   EMAIL_URL=smtp://user:pass@mailhost:587/
   ```

## 🚨 Troubleshooting

### Common Issues

#### Port Conflicts
```bash
# Check what's using port 8024
lsof -i :8024

# Stop conflicting services
pkill -f "saleor.*8024"
```

#### Database Connection Issues
```bash
# Check PostgreSQL status
./deploy-saleor-complete.sh logs saleor-postgres

# Reset database
docker-compose -f docker-compose.saleor-full.yml exec saleor-postgres psql -U saleor -d saleor_coreldove -c "SELECT version();"
```

#### Schema Missing Fields
```bash
# Run migrations
docker-compose -f docker-compose.saleor-full.yml exec saleor-api python manage.py migrate

# Populate with sample data
docker-compose -f docker-compose.saleor-full.yml exec saleor-api python manage.py populatedb
```

### Performance Tuning

#### For Development
```yaml
# Reduce workers for development
environment:
  - GUNICORN_WORKERS=2
  - CELERY_CONCURRENCY=2
```

#### For Production
```yaml
# Increase resources
deploy:
  resources:
    limits:
      memory: 4G
      cpus: '2.0'
```

## 📚 Additional Resources

- [Saleor Documentation](https://docs.saleor.io/)
- [GraphQL API Reference](https://docs.saleor.io/docs/3.x/api-reference/intro)
- [Storefront Integration Guide](https://docs.saleor.io/docs/3.x/developer/extending/storefront)
- [Django Settings Reference](https://docs.djangoproject.com/en/stable/ref/settings/)

## 🛠️ Development

### Local Development

```bash
# Start services in development mode
DEBUG=true ./deploy-saleor-complete.sh deploy

# Enable debug toolbar
docker-compose -f docker-compose.saleor-full.yml exec saleor-api pip install django-debug-toolbar
```

### Custom Plugins

Place custom plugins in `/home/alagiri/projects/bizoholic/bizosaas/saleor-config/`:

```python
# Custom plugin example
INSTALLED_APPS += ['your_custom_plugin']
```

### Database Migrations

```bash
# Create migration
docker-compose -f docker-compose.saleor-full.yml exec saleor-api python manage.py makemigrations

# Apply migration
docker-compose -f docker-compose.saleor-full.yml exec saleor-api python manage.py migrate
```

---

## Support

For issues specific to this deployment, check:

1. Service logs: `./deploy-saleor-complete.sh logs`
2. Health status: `./deploy-saleor-complete.sh status`
3. Schema validation: `./deploy-saleor-complete.sh validate`
4. Integration tests: `python3 test-saleor-integration.py`