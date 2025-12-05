#!/usr/bin/env python3
"""
BizOSaaS Real-time Analytics Monitoring Dashboard
=================================================

Provides real-time monitoring of analytics capabilities, data flows, and system health
across the BizOSaaS platform with interactive dashboard and alerts.
"""

import json
import time
import threading
from datetime import datetime, timedelta
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
import socketserver

class AnalyticsMonitor:
    """Real-time analytics monitoring system"""
    
    def __init__(self):
        self.services = {
            'central_hub': {'url': 'http://localhost:8001', 'name': 'Central Hub API', 'critical': True},
            'superset': {'url': 'http://localhost:8088', 'name': 'Apache Superset', 'critical': True},
            'client_portal': {'url': 'http://localhost:3000', 'name': 'Client Portal', 'critical': True},
            'business_directory': {'url': 'http://localhost:8004', 'name': 'Business Directory', 'critical': False},
            'auth_service': {'url': 'http://localhost:8007', 'name': 'Auth Service', 'critical': True},
            'wagtail_cms': {'url': 'http://localhost:8002', 'name': 'Wagtail CMS', 'critical': False},
            'saleor_backend': {'url': 'http://localhost:8000', 'name': 'Saleor E-commerce', 'critical': True},
            'ai_agents': {'url': 'http://localhost:8010', 'name': 'AI Agents', 'critical': False},
            'sqladmin': {'url': 'http://localhost:8005', 'name': 'SQL Admin', 'critical': False},
            'temporal': {'url': 'http://localhost:8009', 'name': 'Temporal Workflow', 'critical': False}
        }
        
        self.analytics_endpoints = {
            'overview': '/api/analytics/overview',
            'users': '/api/analytics/users',
            'revenue': '/api/analytics/revenue',
            'performance': '/api/analytics/performance',
            'metrics': '/api/metrics',
            'health': '/health'
        }
        
        self.monitoring_data = {
            'last_update': None,
            'service_status': {},
            'analytics_status': {},
            'system_health': {
                'overall_score': 0,
                'critical_services_up': 0,
                'total_critical_services': 0,
                'analytics_endpoints_available': 0,
                'total_analytics_endpoints': 0
            },
            'historical_data': [],
            'alerts': []
        }
        
        self.is_monitoring = False
        
    def check_service_health(self, service_key, service_info):
        """Check individual service health"""
        try:
            req = Request(f"{service_info['url']}/health", 
                         headers={'User-Agent': 'BizOSaaS-Monitor'})
            response = urlopen(req, timeout=3)
            status_code = response.getcode()
            
            return {
                'status': 'healthy' if status_code == 200 else 'responsive',
                'status_code': status_code,
                'response_time': 'fast',
                'last_check': datetime.now().isoformat(),
                'error': None
            }
        except HTTPError as e:
            return {
                'status': 'error',
                'status_code': e.code,
                'response_time': 'slow',
                'last_check': datetime.now().isoformat(),
                'error': f"HTTP {e.code}"
            }
        except URLError as e:
            return {
                'status': 'unreachable',
                'status_code': 0,
                'response_time': 'timeout',
                'last_check': datetime.now().isoformat(),
                'error': 'Connection failed'
            }
        except Exception as e:
            return {
                'status': 'unknown',
                'status_code': 0,
                'response_time': 'error',
                'last_check': datetime.now().isoformat(),
                'error': str(e)
            }
    
    def check_analytics_endpoints(self):
        """Check analytics-specific endpoints"""
        analytics_status = {}
        central_hub_url = self.services['central_hub']['url']
        
        for endpoint_name, endpoint_path in self.analytics_endpoints.items():
            try:
                req = Request(f"{central_hub_url}{endpoint_path}",
                             headers={'User-Agent': 'BizOSaaS-Monitor'})
                response = urlopen(req, timeout=2)
                status_code = response.getcode()
                
                analytics_status[endpoint_name] = {
                    'status': 'available' if status_code == 200 else 'exists',
                    'status_code': status_code,
                    'last_check': datetime.now().isoformat()
                }
            except HTTPError as e:
                analytics_status[endpoint_name] = {
                    'status': 'exists' if e.code in [401, 403, 404, 405] else 'error',
                    'status_code': e.code,
                    'last_check': datetime.now().isoformat()
                }
            except:
                analytics_status[endpoint_name] = {
                    'status': 'unavailable',
                    'status_code': 0,
                    'last_check': datetime.now().isoformat()
                }
        
        return analytics_status
    
    def check_superset_specifically(self):
        """Check Apache Superset BI platform"""
        superset_url = self.services['superset']['url']
        superset_tests = {}
        
        superset_endpoints = {
            'main': '/',
            'login': '/login/',
            'api': '/api/v1/security/csrf_token/',
            'health': '/health'
        }
        
        for test_name, endpoint in superset_endpoints.items():
            try:
                req = Request(f"{superset_url}{endpoint}",
                             headers={'User-Agent': 'BizOSaaS-Monitor'})
                response = urlopen(req, timeout=3)
                status_code = response.getcode()
                
                superset_tests[test_name] = {
                    'status': 'available',
                    'status_code': status_code
                }
            except HTTPError as e:
                superset_tests[test_name] = {
                    'status': 'exists' if e.code in [302, 401, 403] else 'error',
                    'status_code': e.code
                }
            except:
                superset_tests[test_name] = {
                    'status': 'unavailable',
                    'status_code': 0
                }
        
        return superset_tests
    
    def update_monitoring_data(self):
        """Update all monitoring data"""
        print(f"🔄 Updating monitoring data at {datetime.now().strftime('%H:%M:%S')}")
        
        # Check all services
        for service_key, service_info in self.services.items():
            self.monitoring_data['service_status'][service_key] = self.check_service_health(service_key, service_info)
        
        # Check analytics endpoints
        self.monitoring_data['analytics_status'] = self.check_analytics_endpoints()
        
        # Check Superset specifically
        self.monitoring_data['superset_detailed'] = self.check_superset_specifically()
        
        # Calculate system health metrics
        self.calculate_system_health()
        
        # Check for alerts
        self.check_alerts()
        
        # Store historical data (keep last 100 entries)
        current_snapshot = {
            'timestamp': datetime.now().isoformat(),
            'overall_score': self.monitoring_data['system_health']['overall_score'],
            'critical_services_up': self.monitoring_data['system_health']['critical_services_up'],
            'analytics_available': self.monitoring_data['system_health']['analytics_endpoints_available']
        }
        
        self.monitoring_data['historical_data'].append(current_snapshot)
        if len(self.monitoring_data['historical_data']) > 100:
            self.monitoring_data['historical_data'].pop(0)
        
        self.monitoring_data['last_update'] = datetime.now().isoformat()
    
    def calculate_system_health(self):
        """Calculate overall system health metrics"""
        # Count critical services
        critical_services = [k for k, v in self.services.items() if v['critical']]
        critical_services_up = sum(1 for service_key in critical_services 
                                 if self.monitoring_data['service_status'].get(service_key, {}).get('status') in ['healthy', 'responsive'])
        
        # Count analytics endpoints
        analytics_available = sum(1 for status in self.monitoring_data['analytics_status'].values()
                                if status.get('status') in ['available', 'exists'])
        
        # Calculate overall score (0-100)
        critical_score = (critical_services_up / len(critical_services)) * 70 if critical_services else 0
        analytics_score = (analytics_available / len(self.analytics_endpoints)) * 30 if self.analytics_endpoints else 0
        overall_score = critical_score + analytics_score
        
        self.monitoring_data['system_health'] = {
            'overall_score': round(overall_score, 1),
            'critical_services_up': critical_services_up,
            'total_critical_services': len(critical_services),
            'analytics_endpoints_available': analytics_available,
            'total_analytics_endpoints': len(self.analytics_endpoints)
        }
    
    def check_alerts(self):
        """Check for system alerts"""
        alerts = []
        current_time = datetime.now()
        
        # Critical service down alerts
        for service_key, service_info in self.services.items():
            if service_info['critical']:
                service_status = self.monitoring_data['service_status'].get(service_key, {})
                if service_status.get('status') not in ['healthy', 'responsive']:
                    alerts.append({
                        'type': 'critical',
                        'service': service_info['name'],
                        'message': f"{service_info['name']} is {service_status.get('status', 'unknown')}",
                        'timestamp': current_time.isoformat()
                    })
        
        # Overall health alerts
        overall_score = self.monitoring_data['system_health']['overall_score']
        if overall_score < 50:
            alerts.append({
                'type': 'critical',
                'service': 'Platform',
                'message': f"Platform health critically low: {overall_score}%",
                'timestamp': current_time.isoformat()
            })
        elif overall_score < 70:
            alerts.append({
                'type': 'warning',
                'service': 'Platform',
                'message': f"Platform health degraded: {overall_score}%",
                'timestamp': current_time.isoformat()
            })
        
        # Analytics endpoints alerts
        analytics_available = self.monitoring_data['system_health']['analytics_endpoints_available']
        if analytics_available == 0:
            alerts.append({
                'type': 'critical',
                'service': 'Analytics',
                'message': "No analytics endpoints are available",
                'timestamp': current_time.isoformat()
            })
        
        # Superset alerts
        superset_status = self.monitoring_data['service_status'].get('superset', {})
        if superset_status.get('status') not in ['healthy', 'responsive']:
            alerts.append({
                'type': 'warning',
                'service': 'Superset',
                'message': "Apache Superset BI platform is not accessible",
                'timestamp': current_time.isoformat()
            })
        
        # Keep only recent alerts (last 10)
        self.monitoring_data['alerts'] = alerts[-10:]
    
    def start_monitoring(self, interval=30):
        """Start continuous monitoring"""
        self.is_monitoring = True
        print(f"🚀 Starting BizOSaaS Analytics Monitoring (interval: {interval}s)")
        
        def monitoring_loop():
            while self.is_monitoring:
                try:
                    self.update_monitoring_data()
                    self.print_status_summary()
                    time.sleep(interval)
                except KeyboardInterrupt:
                    self.is_monitoring = False
                    break
                except Exception as e:
                    print(f"❌ Monitoring error: {e}")
                    time.sleep(5)
        
        monitoring_thread = threading.Thread(target=monitoring_loop, daemon=True)
        monitoring_thread.start()
        
        return monitoring_thread
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.is_monitoring = False
        print("🛑 Stopping monitoring...")
    
    def print_status_summary(self):
        """Print current status summary"""
        health = self.monitoring_data['system_health']
        
        print(f"\n📊 Analytics Platform Status - {datetime.now().strftime('%H:%M:%S')}")
        print("=" * 60)
        
        # Overall health
        score = health['overall_score']
        if score >= 80:
            status_icon = "🟢"
            status_text = "EXCELLENT"
        elif score >= 70:
            status_icon = "🟡"
            status_text = "GOOD"
        elif score >= 50:
            status_icon = "🟠"
            status_text = "DEGRADED"
        else:
            status_icon = "🔴"
            status_text = "CRITICAL"
        
        print(f"{status_icon} Overall Health: {score}% - {status_text}")
        print(f"🏗️ Critical Services: {health['critical_services_up']}/{health['total_critical_services']} operational")
        print(f"📈 Analytics Endpoints: {health['analytics_endpoints_available']}/{health['total_analytics_endpoints']} available")
        
        # Service status
        print(f"\n🔧 Service Status:")
        for service_key, service_info in self.services.items():
            service_status = self.monitoring_data['service_status'].get(service_key, {})
            status = service_status.get('status', 'unknown')
            
            if status == 'healthy':
                icon = "✅"
            elif status == 'responsive':
                icon = "🟡"
            elif status == 'unreachable':
                icon = "🔴"
            else:
                icon = "❌"
            
            critical_flag = " [CRITICAL]" if service_info['critical'] else ""
            print(f"   {icon} {service_info['name']}: {status.upper()}{critical_flag}")
        
        # Analytics endpoints
        print(f"\n📊 Analytics Endpoints:")
        for endpoint_name, endpoint_status in self.monitoring_data['analytics_status'].items():
            status = endpoint_status.get('status', 'unknown')
            icon = "✅" if status == 'available' else "🟡" if status == 'exists' else "❌"
            print(f"   {icon} {endpoint_name}: {status.upper()}")
        
        # Active alerts
        alerts = self.monitoring_data['alerts']
        if alerts:
            print(f"\n🚨 Active Alerts ({len(alerts)}):")
            for alert in alerts[-3:]:  # Show last 3 alerts
                alert_icon = "🔴" if alert['type'] == 'critical' else "⚠️"
                print(f"   {alert_icon} {alert['service']}: {alert['message']}")
        
        print("-" * 60)
    
    def get_monitoring_data_json(self):
        """Get current monitoring data as JSON"""
        return json.dumps(self.monitoring_data, indent=2)
    
    def generate_dashboard_html(self):
        """Generate HTML dashboard"""
        health = self.monitoring_data['system_health']
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BizOSaaS Analytics Dashboard</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
        .dashboard {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }}
        .metrics-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 20px; }}
        .metric-card {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .metric-value {{ font-size: 2em; font-weight: bold; margin-bottom: 5px; }}
        .metric-label {{ color: #666; font-size: 0.9em; }}
        .services-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
        .service-card {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .service-item {{ display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid #eee; }}
        .status-healthy {{ color: #28a745; }}
        .status-responsive {{ color: #ffc107; }}
        .status-error {{ color: #dc3545; }}
        .status-unreachable {{ color: #dc3545; }}
        .alerts {{ background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 10px; padding: 20px; margin-bottom: 20px; }}
        .alert-item {{ margin-bottom: 10px; padding: 10px; background: white; border-radius: 5px; border-left: 4px solid #ff6b6b; }}
        .refresh-btn {{ background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; }}
        .timestamp {{ color: #666; font-size: 0.8em; }}
    </style>
    <script>
        function refreshData() {{
            location.reload();
        }}
        
        // Auto-refresh every 30 seconds
        setTimeout(function() {{
            location.reload();
        }}, 30000);
    </script>
</head>
<body>
    <div class="dashboard">
        <div class="header">
            <h1>🚀 BizOSaaS Analytics Dashboard</h1>
            <p>Real-time monitoring of analytics platform health and performance</p>
            <div class="timestamp">Last Updated: {self.monitoring_data.get('last_update', 'Never')}</div>
        </div>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-value" style="color: {'#28a745' if health['overall_score'] >= 80 else '#ffc107' if health['overall_score'] >= 70 else '#dc3545'}">{health['overall_score']}%</div>
                <div class="metric-label">Overall Health</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{health['critical_services_up']}/{health['total_critical_services']}</div>
                <div class="metric-label">Critical Services</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{health['analytics_endpoints_available']}/{health['total_analytics_endpoints']}</div>
                <div class="metric-label">Analytics Endpoints</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{len(self.monitoring_data.get('alerts', []))}</div>
                <div class="metric-label">Active Alerts</div>
            </div>
        </div>
        """
        
        # Add alerts section
        alerts = self.monitoring_data.get('alerts', [])
        if alerts:
            html_content += """
        <div class="alerts">
            <h3>🚨 Active Alerts</h3>
            """
            for alert in alerts[-5:]:
                html_content += f"""
            <div class="alert-item">
                <strong>{alert.get('service', 'Unknown')}:</strong> {alert.get('message', 'No message')}
                <div class="timestamp">{alert.get('timestamp', 'Unknown time')}</div>
            </div>
            """
            html_content += "</div>"
        
        html_content += """
        <div class="services-grid">
            <div class="service-card">
                <h3>🔧 Service Status</h3>
                """
        
        # Add service status
        for service_key, service_info in self.services.items():
            service_status = self.monitoring_data['service_status'].get(service_key, {})
            status = service_status.get('status', 'unknown')
            status_class = f"status-{status}"
            critical_flag = " [CRITICAL]" if service_info['critical'] else ""
            
            html_content += f"""
                <div class="service-item">
                    <span>{service_info['name']}{critical_flag}</span>
                    <span class="{status_class}">{status.upper()}</span>
                </div>
            """
        
        html_content += """
            </div>
            
            <div class="service-card">
                <h3>📊 Analytics Endpoints</h3>
                """
        
        # Add analytics endpoints
        for endpoint_name, endpoint_status in self.monitoring_data.get('analytics_status', {}).items():
            status = endpoint_status.get('status', 'unknown')
            status_class = f"status-{status}"
            
            html_content += f"""
                <div class="service-item">
                    <span>{endpoint_name.title()}</span>
                    <span class="{status_class}">{status.upper()}</span>
                </div>
            """
        
        html_content += """
            </div>
        </div>
        
        <div style="text-align: center; margin-top: 30px;">
            <button class="refresh-btn" onclick="refreshData()">🔄 Refresh Data</button>
        </div>
        
    </div>
</body>
</html>
        """
        
        return html_content

class DashboardHandler(BaseHTTPRequestHandler):
    """HTTP handler for dashboard"""
    
    def __init__(self, monitor, *args, **kwargs):
        self.monitor = monitor
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html_content = self.monitor.generate_dashboard_html()
            self.wfile.write(html_content.encode())
        
        elif self.path == '/api/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            json_data = self.monitor.get_monitoring_data_json()
            self.wfile.write(json_data.encode())
        
        else:
            self.send_error(404)
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass

def main():
    """Main execution function"""
    
    print("🚀 BizOSaaS Analytics Monitoring Dashboard")
    print("=" * 50)
    
    monitor = AnalyticsMonitor()
    
    # Initial data update
    monitor.update_monitoring_data()
    monitor.print_status_summary()
    
    # Start monitoring in background
    monitoring_thread = monitor.start_monitoring(interval=30)
    
    # Start web dashboard
    PORT = 8080
    
    def create_handler(*args, **kwargs):
        return DashboardHandler(monitor, *args, **kwargs)
    
    try:
        with socketserver.TCPServer(("", PORT), create_handler) as httpd:
            print(f"\n🌐 Dashboard available at: http://localhost:{PORT}")
            print(f"📊 JSON API available at: http://localhost:{PORT}/api/status")
            print("\n🔄 Monitoring active - Press Ctrl+C to stop")
            
            # Try to open browser
            try:
                webbrowser.open(f"http://localhost:{PORT}")
            except:
                pass
            
            httpd.serve_forever()
    
    except KeyboardInterrupt:
        print("\n🛑 Stopping dashboard...")
        monitor.stop_monitoring()
    except Exception as e:
        print(f"❌ Dashboard error: {e}")
        monitor.stop_monitoring()

if __name__ == "__main__":
    main()