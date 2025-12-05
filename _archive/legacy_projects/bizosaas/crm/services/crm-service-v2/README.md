# CRM Service v2 - E-commerce Enhanced

A comprehensive Customer Relationship Management service with advanced e-commerce capabilities for CoreLDove. This service extends traditional CRM functionality with AI-powered product management, order processing, inventory optimization, and intelligent business logic.

## 🚀 Features

### Core CRM Features
- **Lead Management**: Multi-tenant lead tracking with AI scoring
- **Contact Management**: Customer relationship tracking
- **Deal Tracking**: Sales pipeline management
- **AI Lead Scoring**: Automated lead qualification

### E-commerce Features
- **Product Catalog Management**: Comprehensive product management with AI classification
- **Order Management**: Complete order lifecycle with fraud detection
- **Inventory Tracking**: Smart inventory management with automated alerts
- **Supplier Management**: Multi-marketplace supplier relationships
- **AI-Enhanced Business Logic**: Cross-selling, dynamic pricing, and optimization

### AI Integrations
- **Marketing Ecosystem Orchestrator**: Strategic marketing campaigns
- **Product Sourcing Crew**: Intelligent product discovery and analysis
- **Classification Crew**: AI-powered product classification
- **Fraud Detection**: Real-time fraud risk assessment

### Advanced Analytics
- **Dashboard Analytics**: Comprehensive business intelligence
- **Inventory Optimization**: AI-powered stock level recommendations  
- **Dynamic Pricing**: Market-driven price optimization
- **Cross-selling Engine**: Intelligent product recommendations

## 📋 Prerequisites

- Python 3.8+
- FastAPI
- Pydantic v2
- Async/await support
- Access to CrewAI agents (optional but recommended)

## 🛠 Installation

1. **Install Dependencies**
   ```bash
   pip install fastapi uvicorn pydantic[email] python-multipart
   ```

2. **Environment Variables**
   ```bash
   # Service Configuration
   HOST=0.0.0.0
   PORT=8004
   
   # Database Configuration  
   POSTGRES_HOST=postgres-pgvector.apps-platform.svc.cluster.local
   CACHE_HOST=dragonfly-cache.apps-platform.svc.cluster.local
   
   # AI Agents Configuration (Optional)
   CREWAI_HOST=localhost
   CREWAI_PORT=8000
   ```

3. **Run the Service**
   ```bash
   python main.py
   ```

## 🔌 API Endpoints

### Core CRM Endpoints

#### Health Check
```http
GET /health
```
Returns comprehensive service health including AI agents status.

#### Lead Management
```http
POST /leads              # Create new lead
GET /leads               # List leads with filtering
GET /leads/{lead_id}     # Get specific lead
GET /analytics/leads     # Lead analytics
```

### E-commerce Endpoints

#### Product Management
```http
POST /products                           # Create product with AI classification
GET /products                            # List products with filtering  
GET /products/{product_id}               # Get product details
PUT /products/{product_id}               # Update product
DELETE /products/{product_id}            # Soft delete product
POST /products/bulk-update               # Bulk product updates
```

#### Order Management
```http
POST /orders                    # Create order with fraud detection
GET /orders                     # List orders with filtering
GET /orders/{order_id}          # Get order details  
PUT /orders/{order_id}          # Update order status
```

#### Inventory Management
```http
GET /inventory                           # List inventory with alerts
PUT /inventory/{product_id}              # Update inventory levels
POST /inventory/{product_id}/optimize    # Get AI optimization recommendations
GET /analytics/inventory-alerts          # Comprehensive inventory alerts
```

#### Supplier Management
```http
POST /suppliers          # Create supplier
GET /suppliers           # List suppliers with filtering
```

### AI-Enhanced Features

#### Product Intelligence
```http
POST /products/{product_id}/recommendations     # AI product recommendations
POST /products/{product_id}/marketing-strategy  # Generate marketing strategy
POST /products/{product_id}/cross-sell          # Cross-selling recommendations
POST /products/{product_id}/optimize-pricing    # Dynamic pricing optimization
```

#### AI Workflows
```http
POST /ai-workflows/product-classification/{product_id}  # Run classification workflow
GET /ai-workflows/{workflow_id}                         # Get workflow status
```

#### Advanced Analytics
```http
GET /analytics/dashboard                        # Comprehensive dashboard
POST /analytics/bulk-pricing-optimization      # Bulk pricing analysis
```

#### Event Tracking
```http
GET /events              # List system events
```

## 🎯 Product Classification

The AI system classifies products into four categories:

- **HERO** (80+ score): High-profit potential, premium products
- **GOOD** (65-79 score): Solid performers, good margins  
- **MODERATE** (40-64 score): Test candidates, average performance
- **POOR** (<40 score): Not recommended for dropshipping

## 🔄 Event Bus Integration

The service publishes events for cross-service communication:

### Product Events
- `product.created` - New product added
- `product.analysis_started` - AI analysis initiated
- `marketing.strategy_generated` - Marketing strategy created

### Order Events  
- `order.created` - New order placed
- `order.processing_started` - Order processing initiated

### Inventory Events
- `inventory.low` - Low stock alert
- `inventory.insufficient` - Insufficient inventory warning
- `inventory.reorder_recommended` - Reorder suggestion

### Bulk Events
- `products.bulk_updated` - Bulk operation completed

## 🧠 AI Business Logic

### Cross-Selling Engine
Generates intelligent product recommendations:
- **Upselling**: Premium alternatives (20-300% price increase)
- **Cross-selling**: Related categories with affinity mapping
- **Complementary**: Accessories and add-ons (up to 150% of base price)

### Dynamic Pricing Engine
Optimizes pricing based on:
- Product classification multipliers
- Market demand conditions
- Competitive analysis
- Seasonal factors

### Inventory Optimizer
Calculates optimal stock levels using:
- Sales velocity estimation
- Lead time analysis
- Economic Order Quantity (EOQ)
- Seasonal adjustments
- Safety stock calculations

## 🛡 Fraud Detection

AI-powered fraud detection analyzes:
- Order value thresholds
- Item quantity patterns
- Address mismatches  
- Historical patterns
- Risk scoring (0.0-1.0 scale)

Risk levels:
- **LOW**: Standard processing
- **MEDIUM**: Enhanced monitoring
- **HIGH**: Manual review required
- **CRITICAL**: Hold for investigation

## 📊 Data Models

### Product Model
```python
{
    "id": "uuid",
    "tenant_id": 1,
    "asin": "B08N5WRWNW", 
    "sku": "PROD-001",
    "title": "Premium Fitness Tracker",
    "category": "fitness",
    "pricing": {
        "source_price": 49.99,
        "recommended_price": 74.99,
        "current_selling_price": 69.99
    },
    "ai_metrics": {
        "dropship_score": 85.0,
        "classification": "hero", 
        "profit_margin_estimate": 0.35
    }
}
```

### Order Model
```python
{
    "id": "uuid",
    "order_number": "ORD-20250105-0001",
    "customer_email": "customer@example.com",
    "items": [
        {
            "product_id": "uuid",
            "sku": "PROD-001", 
            "quantity": 2,
            "unit_price": 69.99,
            "total_price": 139.98
        }
    ],
    "total_amount": 139.98,
    "fraud_analysis": {
        "risk_level": "low",
        "risk_score": 0.15,
        "verification_required": false
    }
}
```

## 🔗 Integration Examples

### Create Product with AI Classification
```python
import requests

product_data = {
    "tenant_id": 1,
    "asin": "B08N5WRWNW",
    "sku": "FIT-001",
    "title": "Smart Fitness Tracker",
    "category": "fitness",
    "source_price": 49.99,
    "description": "Advanced health monitoring device"
}

response = requests.post("http://localhost:8004/products", json=product_data)
product = response.json()
print(f"Product classified as: {product['ai_metrics']['classification']}")
```

### Get Cross-selling Recommendations
```python
product_id = "your-product-uuid"
recommendations = requests.post(
    f"http://localhost:8004/products/{product_id}/cross-sell",
    params={"recommendation_type": "upsell", "limit": 5}
).json()

for rec in recommendations["recommendations"]:
    print(f"Recommend: {rec['title']} (Confidence: {rec['confidence']})")
```

### Monitor Inventory Alerts
```python
alerts = requests.get(
    "http://localhost:8004/analytics/inventory-alerts",
    params={"tenant_id": 1, "alert_type": "all"}
).json()

print(f"Critical alerts: {alerts['summary']['critical_alerts']}")
print(f"Reorder cost: ${alerts['summary']['total_estimated_reorder_cost']}")
```

## 🚀 Deployment

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8004
CMD ["python", "main.py"]
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: crm-service-v2
spec:
  replicas: 2
  selector:
    matchLabels:
      app: crm-service-v2
  template:
    spec:
      containers:
      - name: crm-service
        image: bizosaas/crm-service-v2:latest
        ports:
        - containerPort: 8004
        env:
        - name: POSTGRES_HOST
          value: "postgres-pgvector.apps-platform.svc.cluster.local"
        - name: CACHE_HOST  
          value: "dragonfly-cache.apps-platform.svc.cluster.local"
```

## 📈 Performance Features

- **Async Operations**: All AI integrations run asynchronously
- **Background Tasks**: Long-running processes don't block requests
- **Event-Driven**: Decoupled architecture with event bus
- **Caching Ready**: Prepared for Redis/Dragonfly integration
- **Multi-Tenant**: Efficient tenant isolation with proper indexing

## 🔧 Configuration

### AI Agent Integration
```python
# Configure AI agent endpoints
CREWAI_HOST = "localhost"  # CrewAI agents host
CREWAI_PORT = "8000"       # CrewAI agents port

# Timeout settings
AI_REQUEST_TIMEOUT = 30    # seconds
AI_RETRY_COUNT = 3         # retry attempts
```

### Business Logic Settings
```python
# Cross-selling price multipliers
UPSELL_RANGE = (1.2, 3.0)      # 20% to 300% price increase
CROSS_SELL_RANGE = (0.5, 2.0)   # 50% discount to 200% increase  
COMPLEMENT_RANGE = (0.3, 1.5)    # 70% discount to 50% increase

# Dynamic pricing
DEFAULT_MARGIN = 0.25            # 25% default margin
CLASSIFICATION_PREMIUM = 0.25    # 25% premium for HERO products
```

## 🧪 Testing

### Health Check
```bash
curl http://localhost:8004/health
```

### Create Test Product
```bash
curl -X POST http://localhost:8004/products \
  -H "Content-Type: application/json" \
  -d '{
    "tenant_id": 1,
    "asin": "TEST001", 
    "sku": "TEST-PRODUCT-001",
    "title": "Test Fitness Product",
    "category": "fitness",
    "source_price": 29.99
  }'
```

### Test AI Classification
```bash
curl -X POST http://localhost:8004/ai-workflows/product-classification/{product_id}?tenant_id=1
```

## 🤝 Contributing

1. Follow existing code patterns
2. Add proper error handling
3. Include comprehensive logging
4. Update tests for new features
5. Document API changes

## 📝 License

This service is part of the BizoSaaS platform. All rights reserved.

## 🆘 Support

For support and questions:
- Check service logs: `docker logs crm-service-v2`
- Verify AI agents connectivity: `GET /health`
- Monitor events: `GET /events`
- Review analytics: `GET /analytics/dashboard`

---

**Built with ❤️ for CoreLDove E-commerce Platform**