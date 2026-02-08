# CoreLDove E-commerce Order Processing Workflow

A comprehensive, AI-powered order processing workflow system for the CoreLDove e-commerce platform. This system handles the complete order lifecycle from validation to fulfillment with intelligent automation, multi-gateway payment processing, and advanced inventory management.

## 🚀 Features

### Core Order Processing
- **Order Validation & Processing** - Complete order validation with address verification, payment authorization, and fraud detection
- **Real-time Inventory Management** - Multi-warehouse inventory tracking, reservation system, and automatic reordering
- **Multi-Gateway Payment Processing** - Support for Stripe, PayPal, Razorpay, PayU with fraud detection and compliance
- **Intelligent Fulfillment** - Warehouse optimization, shipping carrier integration, and route optimization
- **Customer Notifications** - Multi-channel notifications (email, SMS, push) throughout order lifecycle

### Advanced Automation
- **AI-Powered Optimization** - CrewAI integration for intelligent order routing, pricing, and fulfillment optimization
- **Fraud Detection** - ML-based fraud scoring with configurable risk thresholds
- **Dynamic Pricing** - AI-driven pricing optimization based on demand, inventory, and market conditions
- **Quality Control** - Automated QC checks with exception handling
- **Route Optimization** - AI-optimized shipping routes and batch processing

### Integration Capabilities
- **Saleor E-commerce Integration** - Seamless sync with existing Saleor backend via GraphQL
- **CrewAI System Integration** - Multi-agent AI system for workflow optimization
- **Multi-Carrier Shipping** - FedEx, UPS, DHL, USPS integration with real-time tracking
- **Analytics Integration** - Comprehensive metrics and reporting via Apache Superset
- **Webhook Support** - Real-time event notifications and third-party integrations

### Human-in-the-Loop (HITL)
- **High-Value Order Review** - Manual approval workflow for orders above configurable thresholds
- **Fraud Review Process** - Human review for suspicious transactions with detailed risk analysis
- **Inventory Override** - Manual inventory adjustments and allocation controls
- **Customer Service Escalation** - Integrated support ticket system for complex issues
- **Quality Control Exceptions** - Manual QC review for flagged items

## 🏗️ Architecture

### Service Architecture
```
Order Processing Workflow
├── Main API Layer (FastAPI)
├── Order Orchestrator (Workflow Coordination)
├── Service Layer
│   ├── Inventory Manager
│   ├── Payment Processor
│   ├── Fulfillment Manager
│   └── Notification Service
├── Integration Layer
│   ├── Saleor Integration
│   └── AI Crew Integration
└── Utility Layer
    ├── Security & Authentication
    ├── Performance Monitoring
    └── Error Handling
```

### Technology Stack
- **Backend**: FastAPI + Python 3.11
- **Database**: PostgreSQL with asyncpg
- **Cache**: Redis for session and data caching
- **AI/ML**: CrewAI + LangChain for intelligent automation
- **Payment**: Multi-gateway support (Stripe, PayPal, Razorpay, PayU)
- **Shipping**: Multi-carrier integration (FedEx, UPS, DHL, USPS)
- **Monitoring**: Prometheus metrics + custom performance monitoring
- **Security**: JWT authentication + API key authorization

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 14+
- Redis 6+
- Docker (optional)

### Installation

1. **Clone and Navigate**
```bash
cd /home/alagiri/projects/bizoholic/bizosaas-platform/core/services/order-processing-workflow
```

2. **Set up Python Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Configure Environment**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Set up Database**
```bash
# Create database
createdb bizosaas_orders

# Run migrations (when available)
alembic upgrade head
```

5. **Start the Service**
```bash
# Development
uvicorn main:app --reload --host 0.0.0.0 --port 8001

# Production
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8001
```

### Docker Setup

1. **Build and Run**
```bash
# Build image
docker build -t coreldove-order-processing .

# Run container
docker run -d \
  --name order-processing \
  -p 8001:8001 \
  --env-file .env \
  coreldove-order-processing
```

2. **Using Docker Compose**
```bash
# Add to your docker-compose.yml
version: '3.8'
services:
  order-processing:
    build: ./core/services/order-processing-workflow
    ports:
      - "8001:8001"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/bizosaas_orders
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
```

## 📡 API Endpoints

### Order Management
```http
POST   /api/order-workflow/orders              # Create new order
PUT    /api/order-workflow/orders/{id}/status  # Update order status
GET    /api/order-workflow/orders/{id}         # Get order details
GET    /api/order-workflow/orders              # List orders
```

### Fulfillment
```http
POST   /api/order-workflow/orders/{id}/fulfill # Process fulfillment
GET    /api/order-workflow/orders/{id}/tracking # Get tracking info
```

### Payments & Refunds
```http
POST   /api/order-workflow/orders/{id}/refund  # Process refund
```

### Analytics & Monitoring
```http
GET    /api/order-workflow/analytics/performance # Performance metrics
GET    /api/order-workflow/analytics/inventory   # Inventory analytics
GET    /health                                   # Health check
```

## 🔧 Configuration

### Environment Variables

Key configuration options:

```bash
# Core Settings
ENVIRONMENT=development
PORT=8001
DATABASE_URL=postgresql://user:pass@host:port/db
REDIS_URL=redis://host:port/db

# Security
JWT_SECRET_KEY=your-secret-key
API_KEY_HEADER=X-API-Key
REQUIRE_HTTPS=false

# AI Integration
OPENAI_API_KEY=your-openai-key
ENABLE_AI_OPTIMIZATION=true
AI_CREW_API_URL=http://localhost:8002/api/crew

# Payment Gateways
STRIPE_SECRET_KEY=sk_test_...
PAYPAL_CLIENT_ID=your-paypal-id
RAZORPAY_KEY_ID=your-razorpay-key
PAYU_MERCHANT_KEY=your-payu-key

# Shipping Carriers
FEDEX_ACCOUNT_NUMBER=your-fedex-account
UPS_USERNAME=your-ups-username
USPS_USERNAME=your-usps-username
DHL_SITE_ID=your-dhl-site

# Business Rules
HIGH_VALUE_THRESHOLD=1000.00
FRAUD_SCORE_THRESHOLD=75.0
ENABLE_AUTO_REORDER=true
```

### Feature Flags

Enable/disable features via environment variables:

```bash
ENABLE_AI_CREW_INTEGRATION=true
ENABLE_SALEOR_INTEGRATION=true
ENABLE_MULTI_WAREHOUSE=true
ENABLE_DYNAMIC_PRICING=true
ENABLE_QUALITY_CONTROL=true
ENABLE_ROUTE_OPTIMIZATION=true
```

## 📊 Monitoring & Analytics

### Performance Metrics
- Order processing time (target: <2 minutes)
- Payment success rate (target: 98%+)
- Inventory accuracy (target: 99.5%+)
- Fulfillment accuracy (target: 99%+)
- System resource utilization

### Business KPIs
- Orders processed per minute
- Average order value
- Customer satisfaction scores
- Revenue per hour
- Return/refund rates

### Health Checks
```bash
# Check service health
curl http://localhost:8001/health

# Check performance metrics
curl http://localhost:8001/api/order-workflow/analytics/performance
```

## 🔒 Security

### Authentication & Authorization
- JWT-based authentication for users
- API key authentication for services
- Role-based permissions (admin, manager, operator, customer)
- Order-level access controls

### Security Features
- Input validation and sanitization
- Rate limiting (configurable per client)
- Fraud detection with ML models
- Audit logging for compliance
- Encrypted sensitive data storage

### Payment Security
- PCI DSS compliance ready
- Secure payment gateway integration
- Fraud scoring and risk assessment
- Transaction encryption

## 🔄 Workflow Examples

### Basic Order Processing
```python
# Create order
order_data = {
    "customer_id": "cust_123",
    "items": [
        {
            "product_id": "prod_456",
            "sku": "WIDGET-001",
            "name": "Premium Widget",
            "quantity": 2,
            "unit_price": "29.99",
            "total_price": "59.98"
        }
    ],
    "billing_address": {...},
    "shipping_address": {...},
    "payment_method": "credit_card",
    "shipping_method": "standard",
    "currency": "USD"
}

response = await order_orchestrator.process_order(order_data, user_context)
```

### AI-Optimized Processing
```python
# Enable AI optimization
optimization_result = await ai_crew_integration.optimize_order(order)

# Apply recommendations
if optimization_result["optimization_applied"]:
    order.update(optimization_result["optimizations"])
```

### Multi-Gateway Payment
```python
# Payment processor automatically selects optimal gateway
payment_result = await payment_processor.authorize_payment(
    order_id=order_id,
    amount=total_amount,
    payment_method=payment_method,
    billing_address=billing_address
)
```

## 🧪 Testing

### Running Tests
```bash
# Install test dependencies
pip install -r requirements.txt

# Run all tests
pytest tests/

# Run with coverage
pytest --cov=. tests/

# Run specific test category
pytest tests/test_order_processing.py
pytest tests/test_payment_processing.py
pytest tests/test_fulfillment.py
```

### Test Configuration
```bash
# Test environment variables
TEST_DATABASE_URL=postgresql://postgres:password@localhost:5432/test_orders
TEST_REDIS_URL=redis://localhost:6379/1
TEST_API_KEY=test-api-key-123
TEST_MODE=true
```

## 🚀 Deployment

### Production Deployment
```bash
# Using Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8001

# With process management
supervisor -c supervisor.conf

# Environment setup
export ENVIRONMENT=production
export DEBUG=false
export REQUIRE_HTTPS=true
```

### Scaling Considerations
- Use load balancer for multiple instances
- Configure Redis cluster for high availability
- Set up database read replicas
- Implement proper monitoring and alerting

## 📈 Performance Tuning

### Database Optimization
- Connection pooling (20-30 connections)
- Query optimization with indexes
- Read replicas for analytics queries

### Caching Strategy
- Redis for session data
- Application-level caching for inventory
- CDN for static assets

### AI Optimization
- Cache AI model responses
- Batch process multiple orders
- Use async processing for non-critical AI tasks

## 🤝 Integration Guide

### Saleor Integration
```python
# Sync order to Saleor
await saleor_integration.sync_order_to_saleor(order)

# Handle Saleor webhooks
await saleor_integration.handle_saleor_webhook(event_type, payload)
```

### CrewAI Integration
```python
# Optimize order with AI crew
optimization = await ai_crew_integration.optimize_order(order)

# Fraud detection
fraud_result = await ai_crew_integration.detect_fraud(order)
```

### Custom Integrations
- Implement webhook endpoints for real-time updates
- Use API keys for secure service-to-service communication
- Follow OpenAPI specifications for consistent APIs

## 📋 Troubleshooting

### Common Issues

1. **Database Connection Issues**
   - Check DATABASE_URL configuration
   - Verify database is running and accessible
   - Check connection pool settings

2. **Payment Gateway Errors**
   - Verify API credentials
   - Check gateway-specific settings
   - Review transaction logs

3. **AI Integration Problems**
   - Ensure AI_CREW_API_URL is correct
   - Check API key configuration
   - Verify AI service is running

4. **Performance Issues**
   - Monitor database query performance
   - Check Redis connection
   - Review application logs

### Logging
```bash
# View application logs
tail -f logs/application.log

# Check error logs
grep ERROR logs/application.log

# Monitor performance
grep "PERFORMANCE" logs/application.log
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is part of the CoreLDove platform. See the main project license for details.

## 📞 Support

For technical support or questions:
- Create an issue in the repository
- Contact the development team
- Review the documentation

---

## 🎯 Success Metrics

The order processing workflow is designed to achieve:

- **Processing Speed**: Orders processed within 60 seconds
- **Scalability**: Handle 50,000+ orders per day
- **Reliability**: 99.9% uptime with automatic failover
- **Integration Performance**: <3 seconds for payment/shipping APIs
- **Customer Satisfaction**: 4.8+ rating for order experience

This comprehensive system provides enterprise-grade order processing with intelligent automation while maintaining human oversight for critical decisions.