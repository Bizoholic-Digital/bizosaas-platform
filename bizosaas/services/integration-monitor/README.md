# BizOSaaS Integration Monitor

A comprehensive third-party API health monitoring and automatic failover system for the BizOSaaS ecosystem. Monitors 40+ external integrations with real-time alerting, automatic failover, and 99.9% availability targets.

## 🎯 Overview

The Integration Monitor service provides:

- **Real-time Health Monitoring**: Continuous monitoring of 40+ third-party APIs
- **Automatic Failover**: Smart failover strategies with multiple backup providers
- **Multi-channel Alerting**: Email, Slack, Discord, SMS notifications with escalation
- **Performance Analytics**: Response time, error rate, and cost optimization tracking
- **Live Dashboard**: Real-time monitoring dashboard with WebSocket updates
- **SLA Compliance**: Track and maintain 99.9% availability targets

## 🏗️ Architecture

### Core Components

1. **Monitor Engine**: Main monitoring orchestration and health checks
2. **Failover Controller**: Automatic switching logic and circuit breakers
3. **Alert Manager**: Multi-channel notifications with escalation
4. **Dashboard API**: Real-time data aggregation for dashboard
5. **WebSocket Manager**: Live updates and real-time communications

### Integration Categories

- **Payment Gateways**: Stripe, PayPal, Razorpay, PayU, CCAvenue
- **Marketing Platforms**: Google Ads, Facebook Ads, LinkedIn, TikTok, Twitter
- **Communication APIs**: Resend, Twilio SMS, WhatsApp Business
- **E-commerce**: Saleor GraphQL, Amazon SP-API, Shopify, WooCommerce
- **Analytics**: Google Analytics, Facebook Pixel, LinkedIn Insights
- **Infrastructure**: AWS S3, CloudFlare, DigitalOcean, Google Cloud
- **AI Services**: OpenAI, Anthropic Claude, Synthesia.io, Midjourney

## 🚀 Quick Start

### Using Docker Compose (Recommended)

```bash
# Clone and navigate to the service
cd /path/to/bizosaas-platform/services/integration-monitor

# Copy environment configuration
cp .env.example .env

# Edit .env with your API keys and configuration
nano .env

# Start the service
docker-compose up -d

# View logs
docker-compose logs -f integration-monitor
```

### Manual Installation

```bash
# Install Python dependencies
pip install -r requirements.txt

# Set up environment variables
export DATABASE_URL="postgresql://user:pass@localhost:5432/integration_monitor"
export REDIS_URL="redis://localhost:6379/3"

# Run database migrations
python -c "from database.models import create_tables; import asyncio; asyncio.run(create_tables())"

# Start the service
python main.py
```

## 📊 Dashboard Access

Once running, access the monitoring dashboard at:

- **Live Dashboard**: http://localhost:8003/dashboard
- **API Documentation**: http://localhost:8003/docs
- **Health Check**: http://localhost:8003/health
- **Real-time Metrics**: http://localhost:8003/metrics/real-time

## 🔧 Configuration

### Environment Variables

Key configuration options in `.env`:

```bash
# Service Configuration
SERVICE_PORT=8003
MONITOR_INTERVAL=30
HEALTH_CHECK_TIMEOUT=10

# Performance Thresholds
RESPONSE_TIME_WARNING=2.0
RESPONSE_TIME_CRITICAL=5.0
ERROR_RATE_WARNING=0.02
ERROR_RATE_CRITICAL=0.05

# Alert Configuration
SLACK_WEBHOOK_URL=your_slack_webhook
SMTP_USERNAME=your_smtp_user
SMTP_PASSWORD=your_smtp_password

# API Keys (add your keys)
STRIPE_API_KEY=sk_test_your_key
OPENAI_API_KEY=sk-your_openai_key
GOOGLE_ADS_DEVELOPER_TOKEN=your_token
```

### Failover Strategies

The system supports multiple failover strategies:

- **Primary/Secondary**: Immediate switch to backup provider (payments, infrastructure)
- **Load Balancing**: Distribute load across providers (AI services, marketing)
- **Circuit Breaker**: Temporary isolation of failing services (communication)
- **Graceful Degradation**: Fallback to essential functionality (e-commerce)
- **Smart Routing**: Route based on health scores (analytics, marketing)

## 📈 API Endpoints

### Health Monitoring

```bash
# Get all integration health status
GET /integrations/health/all

# Force health check for specific integration
POST /integrations/{integration_name}/health/check

# Get integration metrics
GET /integrations/{integration_name}/metrics?period=24h
```

### Alerts Management

```bash
# Get active alerts
GET /alerts/active

# Acknowledge alert
POST /alerts/{alert_id}/acknowledge

# Get alert statistics
GET /alerts/statistics
```

### Metrics & Analytics

```bash
# Get system metrics
GET /metrics/status

# Get performance analytics
GET /metrics/performance?period=24h

# Get cost analysis
GET /metrics/costs?period=30d
```

### Configuration

```bash
# Get monitoring configuration
GET /config

# Update integration settings
PUT /config/integrations/{integration_name}

# Get failover configuration
GET /config/failover
```

## 🔔 Alert Channels

### Supported Channels

1. **Email**: SMTP-based email notifications
2. **Slack**: Webhook-based Slack notifications
3. **Discord**: Webhook-based Discord notifications
4. **SMS**: Twilio-based SMS for critical alerts
5. **Webhook**: Custom webhook integrations

### Alert Escalation

Automatic escalation based on severity:

- **Critical**: Immediate notification via all channels + SMS
- **High**: Email + Slack/Discord, escalate to SMS after 10 minutes
- **Medium**: Email + Slack/Discord, escalate after 30 minutes
- **Low**: Email only, no escalation

## 🔄 Failover Configuration

### Circuit Breaker Settings

```python
CIRCUIT_BREAKER_FAILURE_THRESHOLD = 5  # failures before opening
CIRCUIT_BREAKER_TIMEOUT = 60  # seconds before retry
CIRCUIT_BREAKER_RECOVERY_THRESHOLD = 3  # successes to close
```

### Load Balancing

```python
LOAD_BALANCER_ALGORITHM = "weighted_round_robin"
HEALTH_SCORE_WEIGHT = 0.7
RESPONSE_TIME_WEIGHT = 0.3
```

## 📊 Monitoring & Observability

### Prometheus Metrics

The service exposes Prometheus metrics at `/metrics`:

- `integration_health_score`: Current health score per integration
- `integration_response_time`: Response time per integration
- `integration_error_rate`: Error rate per integration
- `failover_events_total`: Total failover events
- `alerts_total`: Total alerts by severity

### Grafana Dashboards

Pre-configured Grafana dashboards for:

- Integration health overview
- Performance trends
- Error rate analysis
- Cost tracking
- Alert volume and resolution times

## 🛠️ Development

### Project Structure

```
integration-monitor/
├── main.py                    # Application entry point
├── config/
│   └── settings.py           # Configuration management
├── core/
│   ├── monitor_engine.py     # Main monitoring engine
│   ├── failover_controller.py # Failover logic
│   ├── alert_manager.py      # Alert handling
│   ├── health_checker.py     # Health check implementation
│   ├── integration_registry.py # Integration definitions
│   ├── metrics_collector.py # Metrics aggregation
│   ├── dashboard_api.py      # Dashboard data API
│   └── websocket_manager.py  # Real-time updates
├── routers/
│   ├── health.py            # Health endpoints
│   ├── integrations.py      # Integration management
│   ├── alerts.py            # Alert management
│   ├── metrics.py           # Metrics endpoints
│   └── configuration.py     # Configuration endpoints
├── database/
│   ├── models.py            # SQLAlchemy models
│   └── connection.py        # Database connectivity
├── templates/
│   └── dashboard.html       # Monitoring dashboard
└── static/                  # Dashboard assets
```

### Adding New Integrations

1. **Define Integration**: Add to `core/integration_registry.py`
2. **Health Check Logic**: Implement in `core/health_checker.py`
3. **Failover Strategy**: Configure in `core/failover_controller.py`
4. **Alert Rules**: Set up in alert rules configuration

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=core --cov-report=html
```

## 🔒 Security

### Best Practices

- Store API keys in environment variables or Vault
- Use least-privilege access for database connections
- Enable HTTPS in production
- Implement rate limiting for API endpoints
- Regular security updates and dependency scanning

### Authentication

The service supports:

- API key authentication for programmatic access
- JWT-based authentication for dashboard access
- Role-based access control (RBAC)

## 🚀 Production Deployment

### Docker Deployment

```bash
# Build production image
docker build -t bizosaas/integration-monitor:latest .

# Run with production settings
docker run -d \
  --name integration-monitor \
  -p 8003:8003 \
  --env-file .env.production \
  bizosaas/integration-monitor:latest
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: integration-monitor
spec:
  replicas: 2
  selector:
    matchLabels:
      app: integration-monitor
  template:
    metadata:
      labels:
        app: integration-monitor
    spec:
      containers:
      - name: integration-monitor
        image: bizosaas/integration-monitor:latest
        ports:
        - containerPort: 8003
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: integration-monitor-secrets
              key: database-url
```

### Health Checks

Configure health checks for load balancers:

- **Liveness**: `/health/liveness`
- **Readiness**: `/health/readiness`
- **Startup**: `/health/startup`

## 📋 Troubleshooting

### Common Issues

1. **Database Connection Failed**
   ```bash
   # Check database connectivity
   curl http://localhost:8003/health/dependencies
   ```

2. **High Memory Usage**
   ```bash
   # Clear metrics cache
   curl -X POST http://localhost:8003/admin/clear-cache
   ```

3. **Failed Health Checks**
   ```bash
   # Check specific integration
   curl http://localhost:8003/integrations/stripe/health
   ```

### Logs

View detailed logs:

```bash
# Docker Compose
docker-compose logs -f integration-monitor

# Direct logs
tail -f integration_monitor.log
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Submit a pull request

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Add docstrings for public methods
- Maintain test coverage above 90%

## 📄 License

This project is part of the BizOSaaS ecosystem and follows the main project licensing.

## 🆘 Support

For support and questions:

- Create an issue in the repository
- Contact the BizOSaaS team
- Check the documentation at `/docs`

---

**BizOSaaS Integration Monitor** - Ensuring 99.9% availability for your third-party integrations! 🚀