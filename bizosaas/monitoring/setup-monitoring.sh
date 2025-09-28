#!/bin/bash

# BizOSaaS Platform Monitoring Setup Script
# This script sets up comprehensive monitoring and observability for the BizOSaaS platform

set -e  # Exit on any error

echo "🚀 BizOSaaS Platform Monitoring Setup"
echo "======================================="

# Configuration variables
MONITORING_DIR=$(dirname "$0")
PROJECT_ROOT="$(dirname "$MONITORING_DIR")"
DOCKER_COMPOSE_FILE="$MONITORING_DIR/docker-compose.monitoring.yml"
ENV_FILE="$PROJECT_ROOT/.env"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_status() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    # Check if main BizOSaaS platform is running
    if ! docker network ls | grep -q "bizosaas-platform-network"; then
        print_warning "BizOSaaS platform network not found. Creating it..."
        docker network create bizosaas-platform-network || true
    fi
    
    print_success "Prerequisites check completed"
}

# Create necessary directories
setup_directories() {
    print_status "Setting up monitoring directories..."
    
    directories=(
        "$MONITORING_DIR/prometheus/rules"
        "$MONITORING_DIR/grafana/dashboards/platform"
        "$MONITORING_DIR/grafana/dashboards/infrastructure" 
        "$MONITORING_DIR/grafana/dashboards/applications"
        "$MONITORING_DIR/grafana/dashboards/business"
        "$MONITORING_DIR/grafana/provisioning/datasources"
        "$MONITORING_DIR/grafana/provisioning/dashboards"
        "$MONITORING_DIR/grafana/provisioning/notifiers"
        "$MONITORING_DIR/alertmanager/templates"
        "$MONITORING_DIR/logstash/config"
        "$MONITORING_DIR/logstash/pipeline"
        "$MONITORING_DIR/uptime-kuma"
        "$MONITORING_DIR/dashboard"
    )
    
    for dir in "${directories[@]}"; do
        mkdir -p "$dir"
        print_success "Created directory: $dir"
    done
}

# Setup Logstash configuration
setup_logstash() {
    print_status "Setting up Logstash configuration..."
    
    # Logstash pipeline configuration
    cat > "$MONITORING_DIR/logstash/pipeline/logstash.conf" << 'EOF'
input {
  beats {
    port => 5044
  }
  
  syslog {
    port => 514
  }
  
  http {
    port => 8080
    codec => "json"
  }
}

filter {
  # Parse Docker logs
  if [docker][container][name] {
    mutate {
      add_field => { "service" => "%{[docker][container][name]}" }
      add_field => { "container_id" => "%{[docker][container][id]}" }
    }
  }
  
  # Parse application logs
  if [fields][service] {
    mutate {
      add_field => { "service" => "%{[fields][service]}" }
    }
  }
  
  # Parse BizOSaaS specific logs
  if [service] =~ /bizosaas/ {
    grok {
      match => { 
        "message" => "%{TIMESTAMP_ISO8601:timestamp} %{LOGLEVEL:level} %{GREEDYDATA:log_message}" 
      }
    }
    
    date {
      match => [ "timestamp", "ISO8601" ]
    }
  }
  
  # Add common fields
  mutate {
    add_field => { "environment" => "production" }
    add_field => { "platform" => "bizosaas" }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "bizosaas-logs-%{+YYYY.MM.dd}"
  }
  
  # Debug output (remove in production)
  stdout { 
    codec => rubydebug 
  }
}
EOF
    
    print_success "Logstash configuration created"
}

# Setup Grafana dashboard
setup_grafana_dashboard() {
    print_status "Setting up Grafana platform dashboard..."
    
    cat > "$MONITORING_DIR/grafana/dashboards/platform/bizosaas-overview.json" << 'EOF'
{
  "dashboard": {
    "id": null,
    "title": "BizOSaaS Platform Overview",
    "tags": ["bizosaas", "platform", "overview"],
    "timezone": "utc",
    "refresh": "30s",
    "time": {
      "from": "now-1h",
      "to": "now"
    },
    "panels": [
      {
        "id": 1,
        "title": "Platform Health Score",
        "type": "stat",
        "gridPos": { "h": 8, "w": 6, "x": 0, "y": 0 },
        "targets": [
          {
            "expr": "(sum(up{job=~\"bizosaas-.*\"}) / count(up{job=~\"bizosaas-.*\"})) * 100",
            "legendFormat": "Health %"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "color": { "mode": "thresholds" },
            "thresholds": {
              "steps": [
                { "color": "red", "value": 0 },
                { "color": "yellow", "value": 70 },
                { "color": "green", "value": 90 }
              ]
            },
            "unit": "percent"
          }
        }
      },
      {
        "id": 2,
        "title": "Service Status",
        "type": "table",
        "gridPos": { "h": 8, "w": 18, "x": 6, "y": 0 },
        "targets": [
          {
            "expr": "up{job=~\"bizosaas-.*\"}",
            "format": "table",
            "instant": true
          }
        ],
        "transformations": [
          {
            "id": "organize",
            "options": {
              "excludeByName": { "__name__": true, "Time": true },
              "renameByName": {
                "job": "Service",
                "instance": "Instance", 
                "Value": "Status"
              }
            }
          }
        ]
      },
      {
        "id": 3,
        "title": "Request Rate",
        "type": "timeseries",
        "gridPos": { "h": 8, "w": 12, "x": 0, "y": 8 },
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{job=~\"bizosaas-.*\"}[5m])) by (job)",
            "legendFormat": "{{ job }}"
          }
        ]
      },
      {
        "id": 4,
        "title": "Error Rate",
        "type": "timeseries", 
        "gridPos": { "h": 8, "w": 12, "x": 12, "y": 8 },
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{job=~\"bizosaas-.*\",status_code=~\"5..\"}[5m])) by (job)",
            "legendFormat": "{{ job }} errors"
          }
        ]
      }
    ]
  }
}
EOF
    
    print_success "Grafana dashboard created"
}

# Fix immediate platform issues
fix_platform_issues() {
    print_status "Attempting to fix immediate platform issues..."
    
    # Check if main platform is running
    if docker ps | grep -q "bizosaas-"; then
        print_status "Restarting unhealthy containers..."
        
        # Restart auth service with fixed configuration
        if docker ps | grep -q "bizosaas-auth-unified"; then
            docker restart bizosaas-auth-unified
            print_success "Restarted auth service"
        fi
        
        # Restart Wagtail CMS
        if docker ps | grep -q "bizosaas-wagtail-cms"; then
            docker restart bizosaas-wagtail-cms-8002 || docker restart bizosaas-wagtail-unified
            print_success "Restarted Wagtail CMS"
        fi
        
        # Add health check endpoints to frontend apps (if they exist)
        print_status "Frontend health checks will be added via application updates"
    else
        print_warning "Main BizOSaaS platform containers not found. Please start the platform first."
    fi
}

# Deploy monitoring stack
deploy_monitoring() {
    print_status "Deploying monitoring stack..."
    
    cd "$MONITORING_DIR"
    
    # Pull latest images
    docker-compose -f docker-compose.monitoring.yml pull
    
    # Start monitoring services
    docker-compose -f docker-compose.monitoring.yml up -d
    
    print_success "Monitoring stack deployed successfully"
}

# Wait for services to be ready
wait_for_services() {
    print_status "Waiting for services to be ready..."
    
    services=(
        "prometheus:9090"
        "grafana:3100"
        "alertmanager:9093"
        "jaeger:16686"
    )
    
    for service in "${services[@]}"; do
        host=$(echo "$service" | cut -d':' -f1)
        port=$(echo "$service" | cut -d':' -f2)
        
        print_status "Waiting for $host to be ready..."
        
        for i in {1..30}; do
            if curl -s "http://localhost:$port" >/dev/null 2>&1; then
                print_success "$host is ready"
                break
            fi
            
            if [ $i -eq 30 ]; then
                print_warning "$host is not responding after 60 seconds"
            fi
            
            sleep 2
        done
    done
}

# Setup health check endpoints
setup_health_endpoints() {
    print_status "Setting up health check endpoints..."
    
    # Create health check template for Next.js apps
    cat > "/tmp/health-endpoint.js" << 'EOF'
// Health check endpoint for Next.js applications
// Add this to pages/api/health.js in each frontend app

export default function handler(req, res) {
  const healthCheck = {
    status: 'healthy',
    timestamp: new Date().toISOString(),
    service: process.env.SERVICE_NAME || 'frontend-app',
    version: process.env.npm_package_version || '1.0.0',
    uptime: process.uptime(),
    memory: process.memoryUsage(),
    environment: process.env.NODE_ENV || 'development'
  };
  
  res.status(200).json(healthCheck);
}
EOF
    
    print_success "Health check template created at /tmp/health-endpoint.js"
    print_warning "Please add this health endpoint to each frontend application manually"
}

# Display access information
show_access_info() {
    echo ""
    echo "🎉 BizOSaaS Platform Monitoring Setup Complete!"
    echo "=============================================="
    echo ""
    echo "📊 Monitoring Services Access:"
    echo "  • Grafana Dashboard:    http://localhost:3100 (admin/BizOSaaSAdmin2024)"
    echo "  • Prometheus:           http://localhost:9090"
    echo "  • AlertManager:         http://localhost:9093"
    echo "  • Jaeger Tracing:       http://localhost:16686"
    echo "  • Kibana Logs:          http://localhost:5601"
    echo "  • Uptime Monitor:       http://localhost:3101"
    echo ""
    echo "🚨 Alert Channels:"
    echo "  • Critical alerts will be sent to: oncall@bizosaas.com"
    echo "  • Warning alerts will go to: #alerts Slack channel"
    echo "  • Business metrics: business-ops@bizosaas.com"
    echo ""
    echo "📈 Key Dashboards:"
    echo "  • Platform Overview: Grafana → BizOSaaS Platform → Overview"
    echo "  • Service Health: Grafana → Infrastructure → Services"
    echo "  • Business Metrics: Grafana → Business Intelligence"
    echo ""
    echo "🔧 Next Steps:"
    echo "  1. Configure Slack webhook in alertmanager.yml"
    echo "  2. Add health endpoints to frontend applications"
    echo "  3. Configure email SMTP settings"
    echo "  4. Review and customize alert thresholds"
    echo "  5. Set up log shipping from application containers"
    echo ""
    echo "📚 Documentation:"
    echo "  • Runbooks: https://docs.bizosaas.com/runbooks/"
    echo "  • Monitoring Guide: https://docs.bizosaas.com/monitoring/"
    echo ""
}

# Cleanup function
cleanup() {
    if [ $? -ne 0 ]; then
        print_error "Setup failed. Cleaning up..."
        cd "$MONITORING_DIR" && docker-compose -f docker-compose.monitoring.yml down
    fi
}

trap cleanup EXIT

# Main execution
main() {
    echo "Starting BizOSaaS Platform Monitoring Setup..."
    echo ""
    
    check_prerequisites
    setup_directories
    setup_logstash
    setup_grafana_dashboard
    fix_platform_issues
    deploy_monitoring
    wait_for_services
    setup_health_endpoints
    
    show_access_info
}

# Check if running as script
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi