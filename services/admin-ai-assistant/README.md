# BizOSaaS Admin AI Assistant [P10]

## 🤖 Overview

The BizOSaaS Admin AI Assistant is a comprehensive platform monitoring and operations service that provides intelligent administration capabilities for the entire BizOSaaS ecosystem. This service combines real-time monitoring, AI-powered analytics, automated operations, and an intelligent chat assistant to streamline platform management.

## 🌟 Features

### 🔍 **Real-time Platform Monitoring**
- Continuous health monitoring of all platform services
- Real-time metrics collection (CPU, memory, disk, network)
- Service availability tracking and response time monitoring
- WebSocket-based live updates to the dashboard

### 🧠 **AI-Powered Intelligence**
- Anomaly detection using machine learning algorithms
- Predictive analytics for resource usage and performance
- Intelligent recommendations for optimization
- Pattern recognition for proactive issue identification

### 💬 **Interactive AI Chat Assistant**
- Natural language interface for platform queries
- Context-aware responses about system status
- Troubleshooting guidance and step-by-step solutions
- Performance analysis and optimization suggestions

### 📊 **Comprehensive Analytics Dashboard**
- Real-time visualization of platform metrics
- Historical performance analysis and trends
- Service health overview with status indicators
- Alert management and notification center

### 🔧 **Automated Operations**
- Automated service restart capabilities
- Cache clearing and memory optimization
- Performance-based scaling recommendations
- Incident response automation

### 🚨 **Intelligent Alerting System**
- Configurable alert rules and thresholds
- Multi-level severity classification
- Automated notification routing
- Alert correlation and noise reduction

## 🏗️ Architecture

### Service Integration
The Admin AI Assistant integrates with all BizOSaaS platform services:

- **Brain API** (Port 8001) - Central intelligence hub
- **Integration Monitor** (Port 8025) - Third-party API monitoring
- **Product Sourcing** (Port 8026) - E-commerce workflow monitoring
- **Supplier Validation** (Port 8027) - HITL workflow monitoring

### Technology Stack
- **Backend**: FastAPI with async Python
- **Database**: PostgreSQL with advanced analytics tables
- **Cache**: Redis for real-time data and session management
- **AI/ML**: scikit-learn for anomaly detection and predictive analytics
- **Frontend**: Responsive HTML5 dashboard with real-time WebSocket updates
- **Visualization**: Chart.js and Plotly for interactive charts
- **Monitoring**: psutil for system metrics collection

### Database Schema
```sql
-- Core monitoring tables
- platform_metrics          # Historical performance data
- service_health_log        # Service status tracking
- platform_alerts          # Alert management
- admin_operations          # Operation tracking

-- AI and analytics tables
- ai_recommendations        # ML-generated recommendations
- performance_analysis      # AI analysis results
- chat_conversations        # Assistant interactions

-- Configuration tables
- alert_rules              # Configurable alert conditions
- automation_rules         # Automated operation rules
```

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- PostgreSQL 15+
- Redis 7+
- Python 3.11+ (for local development)

### 1. Clone and Setup
```bash
git clone <repository-url>
cd admin-ai-assistant
cp .env.example .env
# Edit .env with your configuration
```

### 2. Deploy with Docker
```bash
./deploy.sh
```

### 3. Access the Dashboard
- **Dashboard**: http://localhost:8028/dashboard
- **API Documentation**: http://localhost:8028/docs
- **Health Check**: http://localhost:8028/health

## 📖 API Documentation

### Health and Status Endpoints

#### GET /health
Returns service health status
```json
{
  "status": "healthy",
  "service": "Admin AI Assistant [P10]",
  "version": "1.0.0",
  "timestamp": "2024-01-20T10:30:00Z"
}
```

#### GET /api/platform/health
Returns comprehensive platform health
```json
{
  "overall_status": "healthy",
  "healthy_services": 4,
  "total_services": 4,
  "services": {
    "brain-api": {
      "status": "healthy",
      "response_time": 0.15,
      "last_check": "2024-01-20T10:30:00Z"
    }
  }
}
```

### Metrics Endpoints

#### GET /api/platform/metrics
Returns current platform metrics
```json
{
  "timestamp": "2024-01-20T10:30:00Z",
  "cpu_usage": 45.2,
  "memory_usage": 67.8,
  "disk_usage": 23.1,
  "response_time": 1.2,
  "error_rate": 0.01,
  "active_connections": 156
}
```

#### GET /api/platform/metrics/history
Returns historical metrics with filtering
- `hours`: Number of hours to retrieve (1-168)
- `interval`: Data point interval in seconds (60-3600)

### AI Analysis Endpoints

#### GET /api/platform/analysis
Returns AI-powered platform analysis
```json
{
  "health_score": 87.5,
  "status": "good",
  "anomalies": [],
  "trends": {
    "cpu_usage": {
      "direction": "stable",
      "change_rate": 2.1
    }
  },
  "recommendations": [
    {
      "title": "Memory Optimization",
      "description": "Consider implementing memory pooling",
      "priority": "medium"
    }
  ]
}
```

#### POST /api/chat
Chat with the AI assistant
```json
{
  "message": "What's the platform health status?",
  "context": {}
}
```

### Operations Endpoints

#### POST /api/operations/restart-service
Restart a specific service
```json
{
  "service_name": "brain-api"
}
```

#### POST /api/operations/clear-cache
Clear Redis cache
```json
{
  "cache_type": "all"
}
```

### WebSocket API

#### /ws
Real-time updates via WebSocket
```javascript
const ws = new WebSocket('ws://localhost:8028/ws');
ws.onmessage = function(event) {
  const data = JSON.parse(event.data);
  // Handle real-time updates
};
```

## 🔧 Configuration

### Environment Variables

#### Core Configuration
```bash
DATABASE_URL=postgresql://postgres:password@localhost:5432/bizosaas
REDIS_URL=redis://localhost:6379
ADMIN_API_KEY=your-secure-admin-key
```

#### Service URLs
```bash
BRAIN_API_URL=http://localhost:8001
INTEGRATION_MONITOR_URL=http://localhost:8025
PRODUCT_SOURCING_URL=http://localhost:8026
SUPPLIER_VALIDATION_URL=http://localhost:8027
```

#### Performance Thresholds
```bash
CPU_WARNING_THRESHOLD=80
CPU_CRITICAL_THRESHOLD=90
MEMORY_WARNING_THRESHOLD=85
MEMORY_CRITICAL_THRESHOLD=95
ERROR_RATE_WARNING_THRESHOLD=0.05
RESPONSE_TIME_WARNING_THRESHOLD=3.0
```

### Alert Rules Configuration

Alert rules can be configured in the database:

```sql
INSERT INTO alert_rules (name, condition_expression, threshold_value, severity, metric_name) 
VALUES ('High CPU Usage', 'cpu_usage > threshold', 85.0, 'high', 'cpu_usage');
```

### Automation Rules

Automation rules enable automatic responses to conditions:

```sql
INSERT INTO automation_rules (name, trigger_condition, action_type, action_parameters) 
VALUES ('Auto Restart High Error', 'error_rate > 0.20', 'restart_service', '{"max_restarts": 2}');
```

## 🤖 AI Assistant Commands

The AI assistant understands natural language queries about:

### Health and Status
- "What's the platform health status?"
- "Are all services running?"
- "Check system status"
- "Any issues I should know about?"

### Performance Monitoring
- "How is performance looking?"
- "Show me CPU usage"
- "Memory usage trends"
- "What's the response time?"

### Troubleshooting
- "Any errors detected?"
- "Help me troubleshoot issues"
- "What services are down?"
- "Diagnostic information"

### Recommendations
- "What optimizations do you recommend?"
- "How can I improve performance?"
- "Resource allocation suggestions"
- "Best practices advice"

## 📊 Dashboard Features

### Real-time Monitoring Cards
1. **Platform Health** - Overall system status with service count
2. **Real-time Metrics** - Live CPU, memory, disk usage with progress bars
3. **AI Chat Assistant** - Interactive chat interface
4. **Service Status** - Individual service health indicators
5. **Performance Analytics** - Historical charts and trends
6. **Alerts & Recommendations** - Active alerts and AI suggestions

### Interactive Features
- Real-time WebSocket updates every 30 seconds
- Responsive design for mobile and desktop
- Interactive charts with zoom and pan
- One-click service operations (restart, clear cache)
- Export capabilities for reports

## 🔍 Monitoring and Alerting

### Alert Severity Levels
- **Critical**: Immediate action required (>95% resource usage, service down)
- **High**: Action needed soon (>85% resource usage, high error rates)
- **Medium**: Monitor closely (trending issues, performance degradation)
- **Low**: Informational (minor issues, recommendations)

### Automated Responses
- Service restart on critical error rates
- Cache clearing on high memory usage
- Scaling recommendations on sustained high load
- Notification routing based on severity

### Metrics Collection
- **System Metrics**: CPU, memory, disk, network I/O
- **Application Metrics**: Response times, error rates, throughput
- **Service Metrics**: Health status, availability, performance
- **Business Metrics**: User activity, feature usage, conversion rates

## 🛠️ Development

### Local Development Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env file

# Run locally
python main.py
```

### Running Tests
```bash
pytest tests/ -v
```

### Code Structure
```
admin-ai-assistant/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── Dockerfile             # Container configuration
├── docker-compose.yml     # Multi-service deployment
├── deploy.sh              # Deployment script
├── init.sql               # Database initialization
├── .env.example           # Environment template
├── templates/             # HTML templates
│   └── dashboard.html     # Main dashboard
├── static/               # Static assets
│   ├── css/             # Stylesheets
│   ├── js/              # JavaScript files
│   └── images/          # Images and icons
└── tests/               # Test files
    └── test_main.py     # API tests
```

### Key Classes and Components

#### PlatformIntelligenceEngine
AI-powered analysis engine for:
- Anomaly detection using Isolation Forest
- Health score calculation
- Trend analysis and forecasting
- Recommendation generation

#### PlatformMonitoringEngine
Core monitoring functionality:
- Service health checking
- Metrics collection
- Performance analysis
- Alert condition evaluation

#### AdminChatAssistant
Natural language interface:
- Query processing and understanding
- Context-aware responses
- Integration with monitoring data
- Action recommendations

#### WebSocketManager
Real-time communication:
- Connection management
- Message broadcasting
- Live data streaming
- Client state synchronization

## 🚨 Troubleshooting

### Common Issues

#### Service Won't Start
```bash
# Check logs
docker-compose logs admin-ai-assistant

# Verify ports are available
netstat -tuln | grep 8028

# Check environment variables
docker-compose config
```

#### Database Connection Issues
```bash
# Test database connectivity
docker-compose exec postgres psql -U postgres -d bizosaas -c "SELECT 1;"

# Check database logs
docker-compose logs postgres
```

#### High Resource Usage
```bash
# Monitor resource usage
docker stats

# Check service metrics
curl http://localhost:8028/api/platform/metrics
```

### Performance Optimization

#### Database Optimization
```sql
-- Analyze query performance
EXPLAIN ANALYZE SELECT * FROM platform_metrics WHERE timestamp > NOW() - INTERVAL '1 day';

-- Vacuum and analyze tables
VACUUM ANALYZE platform_metrics;
```

#### Redis Optimization
```bash
# Check Redis memory usage
redis-cli info memory

# Monitor Redis performance
redis-cli monitor
```

## 📈 Scaling and Production

### Production Deployment Considerations

#### Security
- Change all default passwords and API keys
- Use environment-specific configurations
- Implement SSL/TLS encryption
- Set up firewall rules and network segmentation
- Enable audit logging

#### High Availability
- Deploy multiple instances behind a load balancer
- Use managed database services (RDS, Cloud SQL)
- Implement Redis clustering for cache
- Set up monitoring and alerting for the monitoring service itself

#### Performance
- Increase worker processes for high load
- Implement connection pooling
- Use CDN for static assets
- Optimize database queries and indexes
- Configure appropriate resource limits

#### Monitoring
- Set up external health checks
- Monitor service metrics and logs
- Implement distributed tracing
- Set up backup and disaster recovery procedures

### Horizontal Scaling
```yaml
# Example Kubernetes deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: admin-ai-assistant
spec:
  replicas: 3
  selector:
    matchLabels:
      app: admin-ai-assistant
  template:
    spec:
      containers:
      - name: admin-ai-assistant
        image: bizosaas/admin-ai-assistant:latest
        ports:
        - containerPort: 8028
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
```

## 🔄 Updates and Maintenance

### Regular Maintenance Tasks

#### Database Cleanup
```sql
-- Run cleanup function (automated daily)
SELECT cleanup_old_data();
```

#### Log Rotation
```bash
# Configure log rotation
echo "/var/log/admin-ai-assistant.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 644 app app
}" > /etc/logrotate.d/admin-ai-assistant
```

#### Health Checks
```bash
# Automated health check script
#!/bin/bash
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8028/health)
if [ $response != "200" ]; then
    echo "Service unhealthy, attempting restart..."
    docker-compose restart admin-ai-assistant
fi
```

### Backup Procedures

#### Database Backup
```bash
# Daily database backup
docker-compose exec postgres pg_dump -U postgres bizosaas > backup_$(date +%Y%m%d).sql
```

#### Configuration Backup
```bash
# Backup configuration files
tar -czf config_backup_$(date +%Y%m%d).tar.gz .env docker-compose.yml
```

## 📞 Support and Contributing

### Getting Help
- Check the troubleshooting section above
- Review logs: `docker-compose logs admin-ai-assistant`
- Check API documentation: http://localhost:8028/docs
- Verify service health: http://localhost:8028/health

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

### Reporting Issues
When reporting issues, please include:
- Service version and environment details
- Steps to reproduce the problem
- Relevant log files and error messages
- System resource information

---

## 📄 License

This project is part of the BizOSaaS platform. All rights reserved.

## 🙏 Acknowledgments

- FastAPI framework for robust API development
- scikit-learn for machine learning capabilities
- Chart.js and Plotly for visualization
- PostgreSQL and Redis for data storage
- Docker for containerization

---

**Made with ❤️ for the BizOSaaS Platform**