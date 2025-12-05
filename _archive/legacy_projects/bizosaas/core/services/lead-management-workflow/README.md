# Lead Management Workflow System

A comprehensive, AI-powered lead management workflow system for the BizOSaaS platform that provides intelligent lead scoring, automated assignment, multi-stage nurturing campaigns, and human-in-the-loop oversight capabilities.

## 🚀 Features

### 1. **AI-Powered Lead Scoring**
- **Multi-dimensional scoring**: Demographic, behavioral, engagement, fit, and AI qualification scores
- **Machine learning models**: Random Forest classifier with continuous learning
- **Real-time scoring**: Instant lead qualification with confidence metrics
- **CrewAI integration**: Advanced AI agents for lead qualification and analysis
- **Manual override**: Human-supervised score adjustments with audit trails

### 2. **Intelligent Assignment System**
- **Multiple strategies**: Round-robin, skill-based, territory-based, workload-balanced, performance-weighted, and hybrid
- **Automatic routing**: Rules-based assignment with configurable criteria
- **Workload balancing**: Real-time capacity management and fair distribution
- **Escalation handling**: Automatic escalation for unresponsive assignments
- **Performance tracking**: Assignment success metrics and optimization

### 3. **Multi-Stage Nurturing Campaigns**
- **Campaign types**: Welcome series, educational, product demo, case study, trial nurture, re-engagement
- **Personalized content**: AI-driven content personalization based on lead characteristics
- **Multi-channel delivery**: Email, SMS, social media, phone calls, retargeting ads
- **Trigger-based execution**: Time-based, behavior-based, score-based, and lifecycle triggers
- **Performance analytics**: Campaign effectiveness tracking and optimization

### 4. **Platform Integrations**
- **Django CRM**: Bidirectional sync with existing CRM system
- **AI Crew System**: Advanced AI qualification and campaign optimization
- **Apache Superset**: Real-time analytics and reporting
- **Notification Service**: Multi-channel notifications and alerts
- **External APIs**: Flexible integration architecture

### 5. **Human-in-the-Loop (HITL) Management**
- **Manual overrides**: Score and assignment overrides with approval workflows
- **Quality control**: Random sampling and quality reviews of automated decisions
- **Approval workflows**: Multi-level approvals for high-value campaigns and decisions
- **Escalation management**: Automatic escalation with role-based routing
- **Audit trails**: Complete tracking of human interventions and decisions

### 6. **Workflow Orchestration**
- **Event-driven architecture**: Asynchronous event processing with queues
- **Rule engine**: Configurable workflow rules and automation
- **Performance monitoring**: Real-time metrics and health checks
- **Error handling**: Retry mechanisms and fallback strategies
- **Scalability**: Horizontal scaling with worker processes

## 🏗️ Architecture

The system follows a microservices architecture with clear separation of concerns:

```
Lead Management Workflow
├── Lead Scoring Engine          # AI-powered lead qualification
├── Assignment System           # Intelligent lead routing
├── Nurturing Campaigns        # Multi-stage automation
├── Platform Integrations      # External system connectivity
├── HITL Management            # Human oversight and control
└── Workflow Orchestrator     # Central coordination
```

### Key Components

1. **Lead Scoring Engine** (`lead_scoring_engine.py`)
   - Multi-dimensional scoring algorithms
   - AI-powered qualification using CrewAI
   - Machine learning model with continuous improvement
   - Caching for performance optimization

2. **Assignment System** (`assignment_system.py`)
   - Multiple assignment strategies
   - Real-time workload balancing
   - Territory and skill-based routing
   - Escalation and reassignment handling

3. **Nurturing Campaigns** (`nurturing_campaigns.py`)
   - Campaign creation and management
   - Multi-channel content delivery
   - Personalization engine with AI
   - Trigger-based automation

4. **Platform Integrations** (`platform_integrations.py`)
   - Django CRM synchronization
   - AI Crew system integration
   - Analytics data pipeline
   - Notification service

5. **HITL Management** (`hitl_management.py`)
   - Approval workflow management
   - Quality control system
   - Manual override capabilities
   - Escalation handling

6. **Workflow Orchestrator** (`lead_workflow_orchestrator.py`)
   - Central event coordination
   - Rule engine execution
   - Performance monitoring
   - API gateway

## 🛠️ Installation

### Prerequisites

- Python 3.9+
- PostgreSQL 12+
- Redis 6+
- OpenAI API key
- Required system dependencies

### Setup

1. **Clone and navigate to the directory**:
   ```bash
   cd /home/alagiri/projects/bizoholic/bizosaas-platform/core/services/lead-management-workflow/
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup database**:
   ```bash
   # Create database
   createdb bizosaas
   
   # Run schema setup
   psql -d bizosaas -f database_schema.sql
   ```

4. **Configure environment**:
   ```bash
   # Copy example configuration
   cp .env.example .env
   
   # Edit configuration
   nano .env
   ```

5. **Environment variables**:
   ```env
   # Database Configuration
   DATABASE_HOST=localhost
   DATABASE_PORT=5432
   DATABASE_NAME=bizosaas
   DATABASE_USER=postgres
   DATABASE_PASSWORD=your_password
   
   # Redis Configuration
   REDIS_HOST=localhost
   REDIS_PORT=6379
   
   # OpenAI API
   OPENAI_API_KEY=your_openai_api_key
   
   # Integration Endpoints
   DJANGO_CRM_URL=http://localhost:8001
   DJANGO_CRM_API_KEY=your_crm_api_key
   
   AI_CREW_URL=http://localhost:8002
   AI_CREW_API_KEY=your_ai_crew_api_key
   
   SUPERSET_URL=http://localhost:8088
   SUPERSET_API_KEY=your_superset_api_key
   ```

## 🚀 Usage

### Starting the System

1. **Start the orchestrator**:
   ```bash
   python lead_workflow_orchestrator.py
   ```

2. **Access the API**:
   - **Base URL**: `http://localhost:8000`
   - **Documentation**: `http://localhost:8000/docs`
   - **Health Check**: `http://localhost:8000/health`

### API Examples

#### Create a Lead
```bash
curl -X POST "http://localhost:8000/leads" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@techcorp.com",
    "company_name": "TechCorp Inc",
    "company_size": 150,
    "industry": "technology",
    "job_title": "VP of Marketing",
    "location": "San Francisco, CA",
    "budget": 25000,
    "timeline": "1-3 months",
    "service_requirements": ["marketing automation", "crm integration"],
    "website_visits": 8,
    "email_opens": 5,
    "content_downloads": 2
  }'
```

#### Get Lead Status
```bash
curl -X GET "http://localhost:8000/leads/lead_123/status"
```

#### Override Lead Score
```bash
curl -X POST "http://localhost:8000/leads/lead_123/score-override" \
  -H "Content-Type: application/json" \
  -d '{
    "new_score": 85,
    "reason": "Strong interest shown in demo call",
    "override_by": "sales_manager_1"
  }'
```

#### Enroll in Campaign
```bash
curl -X POST "http://localhost:8000/leads/lead_123/enroll-campaign" \
  -H "Content-Type: application/json" \
  -d '{
    "campaign_id": "welcome_series_1",
    "enrollment_data": {
      "priority": "high",
      "personalization_context": "enterprise_focus"
    }
  }'
```

#### Get Analytics
```bash
curl -X GET "http://localhost:8000/analytics"
```

### Individual Component Usage

#### Lead Scoring Engine
```python
from lead_scoring_engine import LeadScoringEngine, LeadData

# Initialize
engine = LeadScoringEngine(db_config, redis_config, openai_api_key)
await engine.initialize()

# Create lead data
lead_data = LeadData(
    lead_id="lead_123",
    email="john.doe@techcorp.com",
    company_name="TechCorp Inc",
    # ... other fields
)

# Score the lead
result = await engine.score_lead(lead_data, use_ai=True)
print(f"Total Score: {result.total_score}")
print(f"Qualification: {result.qualification_level}")
```

#### Assignment System
```python
from assignment_system import LeadAssignmentSystem, AssignmentStrategy

# Initialize
assignment_system = LeadAssignmentSystem(db_config, redis_config)
await assignment_system.initialize()

# Assign lead
assignment = await assignment_system.assign_lead(
    "lead_123",
    lead_data,
    strategy=AssignmentStrategy.HYBRID
)

print(f"Assigned to: {assignment.rep_id}")
print(f"Assignment Score: {assignment.assignment_score}")
```

#### Nurturing Campaigns
```python
from nurturing_campaigns import NurturingCampaignManager

# Initialize
campaign_manager = NurturingCampaignManager(db_config, redis_config, openai_api_key)
await campaign_manager.initialize()

# Enroll lead in campaign
enrollment = await campaign_manager.enroll_lead("lead_123", "welcome_series_1")
print(f"Enrollment ID: {enrollment.enrollment_id}")
```

## 📊 Monitoring and Analytics

### Performance Metrics

The system provides comprehensive monitoring and analytics:

- **Lead Processing**: Volume, scoring accuracy, processing time
- **Assignment Performance**: Distribution, success rates, response times
- **Campaign Effectiveness**: Enrollment rates, engagement, conversions
- **System Health**: Queue status, error rates, component status
- **Quality Control**: Review rates, accuracy scores, intervention frequency

### Dashboard Access

1. **System Analytics**: `GET /analytics`
2. **Component Health**: Individual component status and metrics
3. **Quality Dashboard**: HITL system performance and quality metrics
4. **Integration Status**: External system connectivity and sync status

### Logging

The system uses structured logging with different levels:

- **INFO**: Normal operations and successful events
- **WARNING**: Non-critical issues and degraded performance
- **ERROR**: System errors and failed operations
- **DEBUG**: Detailed execution information

Logs include:
- Event processing details
- Component health status
- Performance metrics
- Error traces and recovery actions

## 🔧 Configuration

### Workflow Rules

The system supports configurable workflow rules that define automation behavior:

```json
{
  "rule_id": "auto_assign_high_score",
  "name": "Auto-assign high-scoring leads",
  "conditions": {
    "total_score": {"operator": "greater_than", "value": 80}
  },
  "actions": {
    "assign_lead": true,
    "strategy": "performance_weighted",
    "notify_manager": true
  },
  "priority": 10
}
```

### Assignment Strategies

Configure assignment behavior for different scenarios:

- **Round Robin**: Fair distribution among available reps
- **Skill Based**: Match leads to rep expertise
- **Territory Based**: Geographic or market-based routing
- **Workload Balanced**: Consider current capacity
- **Performance Weighted**: Favor high-performing reps
- **Hybrid**: Combine multiple factors

### Campaign Configuration

Set up nurturing campaigns with:

- **Entry Criteria**: Rules for automatic enrollment
- **Content Templates**: Personalized messaging
- **Trigger Conditions**: When to send next steps
- **Success Metrics**: Conversion tracking
- **A/B Testing**: Campaign optimization

## 🔐 Security

### Authentication and Authorization

- **Role-based access control**: Different permissions for different user types
- **API key authentication**: Secure access to external integrations
- **Audit trails**: Complete tracking of all actions and changes
- **Data encryption**: Sensitive data protection

### Data Privacy

- **GDPR compliance**: Data protection and privacy controls
- **Data retention**: Configurable retention policies
- **Access controls**: Granular permissions on data access
- **Anonymization**: PII protection capabilities

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest test_lead_scoring.py

# Run integration tests
pytest tests/integration/
```

### Test Categories

1. **Unit Tests**: Individual component testing
2. **Integration Tests**: Component interaction testing
3. **Performance Tests**: Load and stress testing
4. **API Tests**: Endpoint functionality testing
5. **Quality Tests**: HITL system validation

## 🚀 Deployment

### Production Deployment

1. **Environment Setup**:
   ```bash
   # Production environment variables
   export ENVIRONMENT=production
   export DATABASE_URL=postgresql://user:pass@host:port/db
   export REDIS_URL=redis://host:port
   ```

2. **Database Migration**:
   ```bash
   # Run production schema
   psql $DATABASE_URL -f database_schema.sql
   ```

3. **Service Deployment**:
   ```bash
   # Start with production configuration
   python lead_workflow_orchestrator.py --config production.yml
   ```

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "lead_workflow_orchestrator.py"]
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: lead-workflow
spec:
  replicas: 3
  selector:
    matchLabels:
      app: lead-workflow
  template:
    metadata:
      labels:
        app: lead-workflow
    spec:
      containers:
      - name: lead-workflow
        image: lead-workflow:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
```

## 📈 Scaling

### Horizontal Scaling

- **Worker Processes**: Scale event processing workers
- **Load Balancing**: Distribute API requests across instances
- **Database Sharding**: Partition data for performance
- **Cache Layers**: Multi-level caching strategy

### Performance Optimization

- **Database Indexes**: Optimized for common queries
- **Connection Pooling**: Efficient database connections
- **Async Processing**: Non-blocking operations
- **Batch Operations**: Bulk processing for efficiency

## 🤝 Contributing

### Development Setup

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Add tests**
5. **Submit a pull request**

### Code Standards

- **PEP 8**: Python code formatting
- **Type Hints**: Static type checking
- **Documentation**: Comprehensive docstrings
- **Testing**: Minimum 80% code coverage

## 🆘 Troubleshooting

### Common Issues

1. **Database Connection Errors**:
   ```bash
   # Check database connectivity
   psql -h localhost -p 5432 -U postgres -d bizosaas
   ```

2. **Redis Connection Issues**:
   ```bash
   # Test Redis connection
   redis-cli ping
   ```

3. **API Errors**:
   ```bash
   # Check service health
   curl http://localhost:8000/health
   ```

4. **Performance Issues**:
   ```bash
   # Monitor system metrics
   curl http://localhost:8000/analytics
   ```

### Log Analysis

```bash
# View application logs
tail -f lead_workflow.log

# Filter error logs
grep ERROR lead_workflow.log

# Monitor event processing
grep "event_worker" lead_workflow.log
```

## 📚 Documentation

### API Documentation

- **Interactive Docs**: http://localhost:8000/docs
- **OpenAPI Spec**: http://localhost:8000/openapi.json
- **ReDoc**: http://localhost:8000/redoc

### Component Documentation

Each component includes detailed docstrings and examples:

- **Lead Scoring Engine**: AI-powered qualification algorithms
- **Assignment System**: Intelligent routing strategies
- **Nurturing Campaigns**: Multi-channel automation
- **Platform Integrations**: External system connectivity
- **HITL Management**: Human oversight capabilities

## 📄 License

This project is part of the BizOSaaS platform and is proprietary software. See the main project license for details.

## 🔗 Related Projects

- **BizOSaaS Platform**: Main SaaS platform
- **Django CRM**: Customer relationship management
- **AI Crew System**: Advanced AI agents
- **Apache Superset**: Analytics and reporting

## 📞 Support

For support and questions:

- **Documentation**: See inline documentation and API docs
- **Issues**: Create issues in the main project repository
- **Performance**: Monitor system health via `/analytics` endpoint
- **Debugging**: Use structured logging and health check endpoints

---

**Built with ❤️ for the BizOSaaS Platform**

This comprehensive lead management workflow system provides enterprise-grade automation with human oversight, ensuring that your leads are properly qualified, intelligently assigned, and effectively nurtured through their journey to conversion.