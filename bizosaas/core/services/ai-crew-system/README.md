# BizOSaaS AI Crew System

A sophisticated hierarchical AI agent orchestration system for intelligent business automation throughout the BizOSaaS platform.

## Overview

The AI Crew System implements a three-tier hierarchical structure of AI agents using CrewAI to provide intelligent automation for complex business processes:

- **Supervisor Agents**: Handle task delegation and coordination
- **Specialist Agents**: Execute domain-specific tasks (CRM, E-commerce, Analytics, etc.)
- **Worker Agents**: Perform specific operations within each domain

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend Applications                     │
│              (Client Portal, Admin Dashboard)               │
└─────────────────────┬───────────────────────────────────────┘
                      │ HTTP Requests
┌─────────────────────▼───────────────────────────────────────┐
│                 FastAPI Brain API (Port 8001)               │
│                   Central Routing Layer                     │
└─────────────────────┬───────────────────────────────────────┘
                      │ /api/brain/crew/* routes
┌─────────────────────▼───────────────────────────────────────┐
│              AI Crew System (Port 8002)                     │
│                Smart Delegation Engine                      │
└─────┬───────────────┬───────────────┬─────────────────────────┘
      │               │               │
┌─────▼─────┐  ┌─────▼─────┐  ┌─────▼─────┐
│   Direct  │  │   AI      │  │   Crew    │
│ DB/API    │  │  Agent    │  │ Workflow  │
│   Calls   │  │ Execution │  │Orchestration│
└───────────┘  └───────────┘  └───────────┘
```

## Key Features

### 🎯 Smart Delegation Logic
- **Simple CRUD Operations**: Direct database/API calls
- **Moderate Complexity**: Single AI agent execution
- **Complex Operations**: Multi-agent coordination
- **Expert Workflows**: Full crew orchestration

### 🏗️ Agent Hierarchy
- **Master Business Supervisor**: Coordinates all business operations
- **Domain Supervisors**: CRM, E-commerce, Analytics, Billing, CMS, Integrations
- **Specialist Agents**: Domain-specific intelligent processing
- **Worker Agents**: Operational task execution

### 📊 Performance Monitoring
- Real-time execution metrics
- Performance optimization recommendations
- Bottleneck identification
- Success rate tracking

### 🔄 Integration Points
- Seamless integration with existing FastAPI Brain (port 8001)
- Backwards compatibility with current frontend applications
- Tenant-aware routing and processing
- Error handling and fallback mechanisms

## Quick Start

### 1. Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit with your API keys and configuration
nano .env
```

Required environment variables:
- `OPENAI_API_KEY`: OpenAI API key for agent operations
- `POSTGRES_PASSWORD`: Database password
- `BRAIN_API_URL`: URL to the FastAPI Brain API

### 2. Docker Deployment

```bash
# Start the AI Crew System
docker-compose up -d

# Check system health
curl http://localhost:8002/api/crew/health
```

### 3. Integration with Brain API

```bash
# Register crew routes with Brain API
curl -X POST http://localhost:8002/api/crew/brain/register-routes

# Validate integration
curl http://localhost:8002/api/crew/brain/validate-integration
```

## API Endpoints

### Core Crew Operations

#### Execute Crew Task
```http
POST /api/crew/execute
Content-Type: application/json

{
  "type": "crm_lead_scoring",
  "description": "Score and qualify incoming leads",
  "tenant_id": "client_123",
  "domain": "crm",
  "parameters": {
    "lead_data": {...},
    "scoring_criteria": {...}
  },
  "requires_ai": true,
  "priority": 8
}
```

#### Get Task Status
```http
GET /api/crew/task/{task_id}
```

#### Cancel Task
```http
DELETE /api/crew/task/{task_id}
```

### Specialized CRM Operations

#### Lead Scoring
```http
POST /api/crew/crm/lead-scoring
Content-Type: application/json

{
  "lead_data": {
    "email": "prospect@company.com",
    "company": "TechCorp Inc",
    "role": "CTO",
    "engagement_score": 85,
    "website_visits": 12
  },
  "scoring_criteria": {
    "engagement_weight": 0.3,
    "demographic_weight": 0.4,
    "behavior_weight": 0.3
  }
}
```

#### Customer Segmentation
```http
POST /api/crew/crm/customer-segmentation
Content-Type: application/json

{
  "customer_data": [
    {
      "customer_id": "cust_001",
      "ltv": 15000,
      "engagement_score": 92,
      "churn_risk": 0.1
    }
  ],
  "segmentation_type": "behavioral",
  "segment_count": 5
}
```

#### Nurturing Campaign Creation
```http
POST /api/crew/crm/nurturing-campaign
Content-Type: application/json

{
  "lead_segments": ["high_value_prospects", "warm_leads"],
  "campaign_objective": "Convert prospects to demos",
  "duration_days": 30,
  "touchpoint_frequency": "weekly"
}
```

#### Pipeline Optimization
```http
POST /api/crew/crm/pipeline-optimization
Content-Type: application/json

{
  "pipeline_data": {
    "stages": {...},
    "conversion_rates": {...},
    "average_deal_size": 25000,
    "sales_cycle_length": 45
  }
}
```

### System Management

#### System Status
```http
GET /api/crew/status
```

#### Performance Summary
```http
GET /api/crew/performance/summary
```

#### Detailed Metrics
```http
GET /api/crew/performance/metrics?metric_type=execution_time&hours=24
```

#### System Optimization
```http
POST /api/crew/optimize
```

## Task Delegation Logic

The Smart Delegation Engine automatically determines the best execution strategy:

### Decision Matrix

| Task Complexity | Data Volume | AI Required | Strategy | Example |
|-----------------|-------------|-------------|----------|---------|
| Simple | < 1K | No | Direct DB | GET /api/customers |
| Simple | < 1K | No | Direct API | POST /api/sync |
| Moderate | < 10K | Yes | Single Agent | Lead scoring |
| Complex | < 100K | Yes | Multi-Agent | Customer segmentation |
| Expert | Any | Yes | Crew Workflow | Multi-domain analysis |

### Example Routing Decisions

```javascript
// Simple CRUD operation
{
  "type": "get_customer_list",
  "description": "Fetch customer list",
  "data_volume": 500
}
// → Direct Database Query (< 1 second)

// AI-powered analysis
{
  "type": "analyze_customer_churn",
  "description": "Predict customer churn risk",
  "requires_ai": true,
  "data_volume": 5000
}
// → Single Agent Execution (15-30 seconds)

// Complex workflow
{
  "type": "comprehensive_crm_analysis",
  "description": "Full CRM performance analysis",
  "multi_domain": true,
  "requires_ai": true
}
// → Crew Orchestration (60-120 seconds)
```

## Integration with Brain API

The AI Crew System integrates seamlessly with the existing FastAPI Brain API:

### Routing Through Brain API

```http
# Frontend makes request to Brain API
POST /api/brain/crew/crm/lead-scoring
# Brain API routes to Crew System
POST /api/crew/crm/lead-scoring
# Response flows back through Brain API
```

### Tenant-Aware Processing

```javascript
// Request includes tenant context
{
  "tenant_id": "client_123",
  "user_id": "user_456",
  "session_id": "session_789",
  // ... task data
}
```

### Error Handling and Fallbacks

- **Primary**: AI Crew System execution
- **Fallback 1**: Direct agent execution
- **Fallback 2**: Direct database/API operation
- **Fallback 3**: Error response with guidance

## Performance Monitoring

### Real-Time Metrics

- **Execution Time**: Average, median, 95th percentile
- **Success Rate**: Per strategy, per domain, overall
- **Resource Usage**: Agent utilization, memory usage
- **Cost Tracking**: API costs, execution costs

### Alerts and Notifications

```javascript
// Performance alert example
{
  "level": "warning",
  "message": "High execution time detected: 120.5s",
  "metric_type": "execution_time",
  "current_value": 120.5,
  "threshold": 60.0,
  "suggested_actions": [
    "Review task complexity",
    "Consider optimizing agent selection"
  ]
}
```

### Optimization Recommendations

The system provides automatic optimization suggestions:

- **Strategy Optimization**: When to use different execution strategies
- **Agent Selection**: Best agents for specific task types
- **Resource Scaling**: When to scale up agent capacity
- **Cost Optimization**: Reducing unnecessary AI API calls

## Development and Testing

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
python -m uvicorn main:app --reload --port 8002

# Run tests
python -m pytest tests/
```

### Testing Endpoints

```bash
# Test simple task execution
curl -X POST http://localhost:8002/api/crew/test/simple-task

# Test complex workflow
curl -X POST http://localhost:8002/api/crew/test/complex-workflow

# Test CRM lead scoring
curl -X POST http://localhost:8002/api/crew/crm/lead-scoring \
  -H "Content-Type: application/json" \
  -d '{"lead_data": {"email": "test@example.com", "score": 85}}'
```

### Performance Testing

```bash
# Load test the system
ab -n 100 -c 10 http://localhost:8002/api/crew/health

# Monitor performance
curl http://localhost:8002/api/crew/performance/summary
```

## Production Deployment

### Environment Configuration

```bash
# Production environment variables
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=WARNING
CORS_ORIGINS=https://app.bizosaas.com,https://admin.bizosaas.com

# Scale configuration
MAX_CONCURRENT_WORKFLOWS=50
DEFAULT_CREW_TIMEOUT=600
ENABLE_CREW_CACHING=true
```

### Monitoring Setup

```bash
# Start with monitoring stack
docker-compose -f docker-compose.yml -f docker-compose.monitoring.yml up -d

# Access Grafana dashboards
http://localhost:3001
```

### Health Checks

```bash
# Kubernetes health check
livenessProbe:
  httpGet:
    path: /api/crew/health
    port: 8002
  initialDelaySeconds: 30
  periodSeconds: 10
```

## Troubleshooting

### Common Issues

1. **Agent Timeout Errors**
   ```bash
   # Increase timeout in environment
   DEFAULT_CREW_TIMEOUT=600
   AGENT_EXECUTION_TIMEOUT=300
   ```

2. **Memory Issues**
   ```bash
   # Limit agent memory usage
   CREW_MEMORY_LIMIT=1000
   ENABLE_AGENT_MEMORY=false
   ```

3. **API Rate Limits**
   ```bash
   # Configure rate limiting
   MAX_RPM=100
   ENABLE_CREW_CACHING=true
   ```

### Debug Mode

```bash
# Enable debug logging
LOG_LEVEL=DEBUG
DEBUG=true

# Check agent status
curl http://localhost:8002/api/crew/statistics
```

### Performance Issues

```bash
# Analyze performance bottlenecks
curl http://localhost:8002/api/crew/performance/metrics

# Get optimization recommendations
curl -X POST http://localhost:8002/api/crew/optimize
```

## Contributing

### Development Setup

1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-crew-capability`
3. Install dependencies: `pip install -r requirements.txt`
4. Make changes and add tests
5. Run tests: `python -m pytest`
6. Submit pull request

### Adding New Specialized Crews

1. Create new crew file in `specialized_crews/`
2. Implement crew class with required methods
3. Add crew routes to `main.py`
4. Update documentation
5. Add tests

### Code Style

- Use Black for code formatting: `black .`
- Use isort for imports: `isort .`
- Use mypy for type checking: `mypy .`
- Follow PEP 8 guidelines

## License

This project is part of the BizOSaaS platform and is proprietary software.

## Support

For support and questions:
- Internal Documentation: [BizOSaaS Wiki]
- Development Team: [Slack Channel]
- Issues: [GitHub Issues]

---

**BizOSaaS AI Crew System** - Intelligent Business Automation through Hierarchical AI Agents