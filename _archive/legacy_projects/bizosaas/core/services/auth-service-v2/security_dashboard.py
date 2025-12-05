#!/usr/bin/env python3

"""
BizOSaaS Security Monitoring Dashboard
Real-time security monitoring and threat detection
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from aiohttp import web
import aiohttp_cors
from dataclasses import asdict

from auth_security import AuthenticationService, SecurityEvent, SecurityEventType

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecurityDashboard:
    """Security monitoring and analytics dashboard"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.auth_service = AuthenticationService(config)
        
        # Risk thresholds
        self.risk_thresholds = {
            'low': 25,
            'medium': 50,
            'high': 75,
            'critical': 90
        }
        
        # Alert rules
        self.alert_rules = {
            'failed_login_threshold': 10,  # Alert after 10 failed logins in 1 hour
            'suspicious_ip_threshold': 5,   # Alert if IP has 5+ security events
            'session_hijack_attempts': 1,   # Alert immediately on session hijacking
            'privilege_escalation': 1,      # Alert on role changes
            'rate_limit_violations': 20     # Alert after 20 rate limit violations
        }
    
    async def initialize(self):
        """Initialize the security dashboard"""
        await self.auth_service.initialize()
        logger.info("Security dashboard initialized")
    
    async def get_security_overview(self, request):
        """Get security overview statistics"""
        # Time ranges
        last_24h = datetime.utcnow() - timedelta(days=1)
        last_7d = datetime.utcnow() - timedelta(days=7)
        last_30d = datetime.utcnow() - timedelta(days=30)
        
        async with self.auth_service.db_pool.acquire() as conn:
            # Total security events
            total_events = await conn.fetchval(
                "SELECT COUNT(*) FROM security_events WHERE created_at >= $1",
                last_24h
            )
            
            # High risk events
            high_risk_events = await conn.fetchval(
                "SELECT COUNT(*) FROM security_events WHERE risk_score >= $1 AND created_at >= $2",
                self.risk_thresholds['high'], last_24h
            )
            
            # Failed login attempts
            failed_logins = await conn.fetchval(
                "SELECT COUNT(*) FROM security_events WHERE event_type = $1 AND created_at >= $2",
                SecurityEventType.LOGIN_FAILED.value, last_24h
            )
            
            # Active sessions
            active_sessions = await conn.fetchval(
                "SELECT COUNT(*) FROM user_sessions WHERE is_active = true AND expires_at > NOW()"
            )
            
            # Blocked IPs (based on rate limiting)
            blocked_ips = await conn.fetchval(
                "SELECT COUNT(DISTINCT ip_address) FROM security_events WHERE event_type = $1 AND created_at >= $2",
                SecurityEventType.RATE_LIMIT_EXCEEDED.value, last_24h
            )
            
            # Security events by type (last 24h)
            events_by_type = await conn.fetch("""
                SELECT event_type, COUNT(*) as count
                FROM security_events 
                WHERE created_at >= $1
                GROUP BY event_type
                ORDER BY count DESC
            """, last_24h)
            
            # Risk score distribution
            risk_distribution = await conn.fetch("""
                SELECT 
                    CASE 
                        WHEN risk_score < $1 THEN 'low'
                        WHEN risk_score < $2 THEN 'medium' 
                        WHEN risk_score < $3 THEN 'high'
                        ELSE 'critical'
                    END as risk_level,
                    COUNT(*) as count
                FROM security_events
                WHERE created_at >= $4
                GROUP BY risk_level
                ORDER BY risk_level
            """, 
            self.risk_thresholds['low'],
            self.risk_thresholds['medium'], 
            self.risk_thresholds['high'],
            last_24h
            )
            
            # Top suspicious IPs
            suspicious_ips = await conn.fetch("""
                SELECT ip_address, COUNT(*) as event_count, MAX(risk_score) as max_risk
                FROM security_events
                WHERE created_at >= $1 AND risk_score > 0
                GROUP BY ip_address
                ORDER BY event_count DESC, max_risk DESC
                LIMIT 10
            """, last_24h)
            
            # Recent critical events
            critical_events = await conn.fetch("""
                SELECT event_type, ip_address, event_data, risk_score, created_at
                FROM security_events
                WHERE risk_score >= $1 AND created_at >= $2
                ORDER BY created_at DESC
                LIMIT 20
            """, self.risk_thresholds['critical'], last_24h)
        
        return web.json_response({
            'summary': {
                'total_events_24h': total_events,
                'high_risk_events_24h': high_risk_events,
                'failed_logins_24h': failed_logins,
                'active_sessions': active_sessions,
                'blocked_ips_24h': blocked_ips
            },
            'events_by_type': [
                {'type': row['event_type'], 'count': row['count']}
                for row in events_by_type
            ],
            'risk_distribution': [
                {'level': row['risk_level'], 'count': row['count']}
                for row in risk_distribution
            ],
            'suspicious_ips': [
                {
                    'ip_address': row['ip_address'],
                    'event_count': row['event_count'],
                    'max_risk_score': row['max_risk']
                }
                for row in suspicious_ips
            ],
            'critical_events': [
                {
                    'type': row['event_type'],
                    'ip_address': row['ip_address'],
                    'details': json.loads(row['event_data']),
                    'risk_score': row['risk_score'],
                    'timestamp': row['created_at'].isoformat()
                }
                for row in critical_events
            ],
            'timestamp': datetime.utcnow().isoformat()
        })
    
    async def get_security_alerts(self, request):
        """Get active security alerts"""
        alerts = []
        
        # Check for various alert conditions
        async with self.auth_service.db_pool.acquire() as conn:
            last_hour = datetime.utcnow() - timedelta(hours=1)
            
            # Failed login threshold alert
            failed_logins = await conn.fetchval(
                "SELECT COUNT(*) FROM security_events WHERE event_type = $1 AND created_at >= $2",
                SecurityEventType.LOGIN_FAILED.value, last_hour
            )
            
            if failed_logins >= self.alert_rules['failed_login_threshold']:
                alerts.append({
                    'id': 'failed_login_spike',
                    'severity': 'high',
                    'title': 'High number of failed login attempts',
                    'description': f'{failed_logins} failed login attempts in the last hour',
                    'count': failed_logins,
                    'threshold': self.alert_rules['failed_login_threshold'],
                    'timestamp': datetime.utcnow().isoformat()
                })
            
            # Session hijacking attempts
            hijack_attempts = await conn.fetchval(
                "SELECT COUNT(*) FROM security_events WHERE event_type = $1 AND created_at >= $2",
                SecurityEventType.SESSION_HIJACK_ATTEMPT.value, last_hour
            )
            
            if hijack_attempts > 0:
                alerts.append({
                    'id': 'session_hijacking',
                    'severity': 'critical',
                    'title': 'Session hijacking attempts detected',
                    'description': f'{hijack_attempts} session hijacking attempts detected',
                    'count': hijack_attempts,
                    'timestamp': datetime.utcnow().isoformat()
                })
            
            # Rate limit violations
            rate_limit_violations = await conn.fetchval(
                "SELECT COUNT(*) FROM security_events WHERE event_type = $1 AND created_at >= $2",
                SecurityEventType.RATE_LIMIT_EXCEEDED.value, last_hour
            )
            
            if rate_limit_violations >= self.alert_rules['rate_limit_violations']:
                alerts.append({
                    'id': 'rate_limit_spike',
                    'severity': 'medium',
                    'title': 'High number of rate limit violations',
                    'description': f'{rate_limit_violations} rate limit violations in the last hour',
                    'count': rate_limit_violations,
                    'threshold': self.alert_rules['rate_limit_violations'],
                    'timestamp': datetime.utcnow().isoformat()
                })
            
            # Suspicious IP activity
            suspicious_ips = await conn.fetch("""
                SELECT ip_address, COUNT(*) as event_count
                FROM security_events
                WHERE created_at >= $1 AND risk_score > 0
                GROUP BY ip_address
                HAVING COUNT(*) >= $2
                ORDER BY event_count DESC
            """, last_hour, self.alert_rules['suspicious_ip_threshold'])
            
            for ip_row in suspicious_ips:
                alerts.append({
                    'id': f'suspicious_ip_{ip_row["ip_address"]}',
                    'severity': 'high',
                    'title': f'Suspicious activity from IP {ip_row["ip_address"]}',
                    'description': f'{ip_row["event_count"]} security events from this IP',
                    'ip_address': ip_row['ip_address'],
                    'count': ip_row['event_count'],
                    'timestamp': datetime.utcnow().isoformat()
                })
        
        return web.json_response({
            'alerts': alerts,
            'total_alerts': len(alerts),
            'timestamp': datetime.utcnow().isoformat()
        })
    
    async def get_user_security_report(self, request):
        """Get security report for a specific user"""
        user_id = request.match_info.get('user_id')
        if not user_id:
            return web.json_response({'error': 'User ID required'}, status=400)
        
        # Time range from query params
        days = int(request.query.get('days', 30))
        start_date = datetime.utcnow() - timedelta(days=days)
        
        async with self.auth_service.db_pool.acquire() as conn:
            # User info
            user = await conn.fetchrow(
                "SELECT email, role, last_login_at, mfa_enabled FROM users WHERE id = $1",
                user_id
            )
            
            if not user:
                return web.json_response({'error': 'User not found'}, status=404)
            
            # Security events for user
            events = await conn.fetch("""
                SELECT event_type, ip_address, event_data, risk_score, created_at
                FROM security_events
                WHERE user_id = $1 AND created_at >= $2
                ORDER BY created_at DESC
                LIMIT 100
            """, user_id, start_date)
            
            # Login patterns
            login_stats = await conn.fetch("""
                SELECT DATE(created_at) as login_date, 
                       event_type,
                       COUNT(*) as count
                FROM security_events
                WHERE user_id = $1 AND created_at >= $2
                  AND event_type IN ($3, $4)
                GROUP BY DATE(created_at), event_type
                ORDER BY login_date DESC
            """, 
            user_id, start_date,
            SecurityEventType.LOGIN_SUCCESS.value,
            SecurityEventType.LOGIN_FAILED.value
            )
            
            # IP addresses used
            ip_addresses = await conn.fetch("""
                SELECT ip_address, COUNT(*) as usage_count, MAX(created_at) as last_seen
                FROM security_events
                WHERE user_id = $1 AND created_at >= $2
                GROUP BY ip_address
                ORDER BY usage_count DESC
            """, user_id, start_date)
            
            # Active sessions
            active_sessions = await conn.fetch("""
                SELECT session_id, ip_address, created_at, last_activity, expires_at
                FROM user_sessions
                WHERE user_id = $1 AND is_active = true
                ORDER BY last_activity DESC
            """, user_id)
        
        return web.json_response({
            'user': {
                'email': user['email'],
                'role': user['role'],
                'last_login_at': user['last_login_at'].isoformat() if user['last_login_at'] else None,
                'mfa_enabled': user['mfa_enabled']
            },
            'security_events': [
                {
                    'type': event['event_type'],
                    'ip_address': event['ip_address'],
                    'details': json.loads(event['event_data']),
                    'risk_score': event['risk_score'],
                    'timestamp': event['created_at'].isoformat()
                }
                for event in events
            ],
            'login_patterns': [
                {
                    'date': row['login_date'].isoformat(),
                    'type': row['event_type'],
                    'count': row['count']
                }
                for row in login_stats
            ],
            'ip_addresses': [
                {
                    'ip_address': row['ip_address'],
                    'usage_count': row['usage_count'],
                    'last_seen': row['last_seen'].isoformat()
                }
                for row in ip_addresses
            ],
            'active_sessions': [
                {
                    'session_id': session['session_id'],
                    'ip_address': session['ip_address'],
                    'created_at': session['created_at'].isoformat(),
                    'last_activity': session['last_activity'].isoformat(),
                    'expires_at': session['expires_at'].isoformat()
                }
                for session in active_sessions
            ],
            'period_days': days,
            'timestamp': datetime.utcnow().isoformat()
        })
    
    async def get_security_metrics(self, request):
        """Get security metrics for monitoring systems"""
        # Time ranges
        last_24h = datetime.utcnow() - timedelta(days=1)
        last_7d = datetime.utcnow() - timedelta(days=7)
        
        async with self.auth_service.db_pool.acquire() as conn:
            # Authentication metrics
            auth_metrics = await conn.fetchrow("""
                SELECT 
                    SUM(CASE WHEN event_type = $1 THEN 1 ELSE 0 END) as successful_logins,
                    SUM(CASE WHEN event_type = $2 THEN 1 ELSE 0 END) as failed_logins,
                    SUM(CASE WHEN event_type = $3 THEN 1 ELSE 0 END) as blocked_attempts
                FROM security_events
                WHERE created_at >= $4
            """, 
            SecurityEventType.LOGIN_SUCCESS.value,
            SecurityEventType.LOGIN_FAILED.value,
            SecurityEventType.LOGIN_BLOCKED.value,
            last_24h
            )
            
            # Calculate authentication success rate
            total_attempts = auth_metrics['successful_logins'] + auth_metrics['failed_logins']
            success_rate = (auth_metrics['successful_logins'] / total_attempts * 100) if total_attempts > 0 else 100
            
            # Risk metrics
            risk_metrics = await conn.fetchrow("""
                SELECT 
                    AVG(risk_score) as avg_risk_score,
                    MAX(risk_score) as max_risk_score,
                    COUNT(*) as total_events,
                    SUM(CASE WHEN risk_score >= $1 THEN 1 ELSE 0 END) as high_risk_events
                FROM security_events
                WHERE created_at >= $2
            """, self.risk_thresholds['high'], last_24h)
            
            # Session metrics
            session_metrics = await conn.fetchrow("""
                SELECT 
                    COUNT(*) as total_sessions,
                    COUNT(CASE WHEN is_active = true THEN 1 END) as active_sessions,
                    AVG(EXTRACT(EPOCH FROM (last_activity - created_at))/3600) as avg_session_duration_hours
                FROM user_sessions
                WHERE created_at >= $1
            """, last_24h)
            
            # Geographic distribution of events
            geo_distribution = await conn.fetch("""
                SELECT 
                    substring(host(ip_address) from 1 for 8) as ip_prefix,
                    COUNT(*) as event_count
                FROM security_events
                WHERE created_at >= $1
                GROUP BY ip_prefix
                ORDER BY event_count DESC
                LIMIT 10
            """, last_24h)
        
        # Calculate security health score
        health_score = 100
        
        # Deduct points for failed logins
        if auth_metrics['failed_logins'] > 10:
            health_score -= min(20, auth_metrics['failed_logins'] // 5)
        
        # Deduct points for high risk events
        if risk_metrics['high_risk_events'] > 0:
            health_score -= min(30, risk_metrics['high_risk_events'] * 5)
        
        # Deduct points for blocked attempts
        if auth_metrics['blocked_attempts'] > 0:
            health_score -= min(25, auth_metrics['blocked_attempts'] * 3)
        
        health_score = max(0, health_score)  # Ensure it's not negative
        
        return web.json_response({
            'authentication': {
                'successful_logins_24h': auth_metrics['successful_logins'],
                'failed_logins_24h': auth_metrics['failed_logins'],
                'blocked_attempts_24h': auth_metrics['blocked_attempts'],
                'success_rate_percent': round(success_rate, 2)
            },
            'risk': {
                'avg_risk_score': round(risk_metrics['avg_risk_score'] or 0, 2),
                'max_risk_score': risk_metrics['max_risk_score'] or 0,
                'total_events_24h': risk_metrics['total_events'],
                'high_risk_events_24h': risk_metrics['high_risk_events']
            },
            'sessions': {
                'total_sessions_24h': session_metrics['total_sessions'],
                'active_sessions': session_metrics['active_sessions'],
                'avg_session_duration_hours': round(session_metrics['avg_session_duration_hours'] or 0, 2)
            },
            'geographic_distribution': [
                {
                    'ip_prefix': row['ip_prefix'],
                    'event_count': row['event_count']
                }
                for row in geo_distribution
            ],
            'security_health_score': health_score,
            'timestamp': datetime.utcnow().isoformat()
        })
    
    async def render_dashboard(self, request):
        """Render security dashboard HTML"""
        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BizOSaaS Security Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0f0f23;
            color: #cccccc;
            line-height: 1.6;
        }
        
        .header {
            background: #1a1a3a;
            padding: 1rem 2rem;
            border-bottom: 2px solid #4CAF50;
        }
        
        .header h1 {
            color: #4CAF50;
            font-size: 2rem;
        }
        
        .subtitle {
            color: #888;
            font-size: 0.9rem;
            margin-top: 0.5rem;
        }
        
        .dashboard {
            padding: 2rem;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
        }
        
        .card {
            background: #1a1a3a;
            border-radius: 8px;
            padding: 1.5rem;
            border: 1px solid #333;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }
        
        .card h2 {
            color: #4CAF50;
            margin-bottom: 1rem;
            font-size: 1.3rem;
        }
        
        .stat-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 1rem;
            margin: 1rem 0;
        }
        
        .stat {
            text-align: center;
            padding: 1rem;
            background: #252545;
            border-radius: 6px;
        }
        
        .stat-value {
            font-size: 2rem;
            font-weight: bold;
            color: #4CAF50;
        }
        
        .stat-label {
            font-size: 0.8rem;
            color: #888;
            margin-top: 0.5rem;
        }
        
        .alert {
            background: #3d1a1a;
            border: 1px solid #d32f2f;
            border-radius: 6px;
            padding: 1rem;
            margin: 0.5rem 0;
        }
        
        .alert-critical {
            border-color: #d32f2f;
            background: #3d1a1a;
        }
        
        .alert-high {
            border-color: #f57c00;
            background: #3d2a1a;
        }
        
        .alert-medium {
            border-color: #fbc02d;
            background: #3d3d1a;
        }
        
        .alert-title {
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        
        .chart-container {
            position: relative;
            height: 300px;
            margin: 1rem 0;
        }
        
        .refresh-btn {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 4px;
            cursor: pointer;
            float: right;
        }
        
        .refresh-btn:hover {
            background: #45a049;
        }
        
        .timestamp {
            color: #666;
            font-size: 0.8rem;
            text-align: right;
            margin-top: 1rem;
        }
        
        .event-log {
            max-height: 400px;
            overflow-y: auto;
        }
        
        .event {
            padding: 0.5rem;
            margin: 0.25rem 0;
            background: #252545;
            border-radius: 4px;
            font-size: 0.9rem;
        }
        
        .event-timestamp {
            color: #666;
            font-size: 0.8rem;
        }
        
        .risk-high { color: #f44336; }
        .risk-medium { color: #ff9800; }
        .risk-low { color: #4caf50; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🛡️ BizOSaaS Security Dashboard</h1>
        <div class="subtitle">Real-time security monitoring and threat detection</div>
    </div>
    
    <div class="dashboard">
        <!-- Security Overview -->
        <div class="card">
            <h2>Security Overview (24h)</h2>
            <button class="refresh-btn" onclick="refreshData()">Refresh</button>
            <div class="stat-grid" id="overview-stats">
                <div class="stat">
                    <div class="stat-value" id="total-events">--</div>
                    <div class="stat-label">Total Events</div>
                </div>
                <div class="stat">
                    <div class="stat-value" id="high-risk-events">--</div>
                    <div class="stat-label">High Risk Events</div>
                </div>
                <div class="stat">
                    <div class="stat-value" id="failed-logins">--</div>
                    <div class="stat-label">Failed Logins</div>
                </div>
                <div class="stat">
                    <div class="stat-value" id="active-sessions">--</div>
                    <div class="stat-label">Active Sessions</div>
                </div>
            </div>
            <div class="timestamp" id="overview-timestamp">--</div>
        </div>
        
        <!-- Security Alerts -->
        <div class="card">
            <h2>🚨 Active Security Alerts</h2>
            <div id="alerts-container">
                <div class="alert">No active alerts</div>
            </div>
        </div>
        
        <!-- Risk Distribution Chart -->
        <div class="card">
            <h2>Risk Distribution</h2>
            <div class="chart-container">
                <canvas id="risk-chart"></canvas>
            </div>
        </div>
        
        <!-- Event Types Chart -->
        <div class="card">
            <h2>Security Events by Type</h2>
            <div class="chart-container">
                <canvas id="events-chart"></canvas>
            </div>
        </div>
        
        <!-- Suspicious IPs -->
        <div class="card">
            <h2>🔍 Suspicious IP Addresses</h2>
            <div id="suspicious-ips">
                <div>No suspicious activity detected</div>
            </div>
        </div>
        
        <!-- Critical Events Log -->
        <div class="card">
            <h2>⚠️ Recent Critical Events</h2>
            <div class="event-log" id="critical-events">
                <div class="event">No critical events</div>
            </div>
        </div>
    </div>
    
    <script>
        let riskChart, eventsChart;
        
        async function fetchData(endpoint) {
            try {
                const response = await fetch('/api/security/' + endpoint);
                return await response.json();
            } catch (error) {
                console.error('Error fetching data:', error);
                return null;
            }
        }
        
        async function refreshData() {
            // Fetch overview data
            const overview = await fetchData('overview');
            if (overview) {
                document.getElementById('total-events').textContent = overview.summary.total_events_24h;
                document.getElementById('high-risk-events').textContent = overview.summary.high_risk_events_24h;
                document.getElementById('failed-logins').textContent = overview.summary.failed_logins_24h;
                document.getElementById('active-sessions').textContent = overview.summary.active_sessions;
                document.getElementById('overview-timestamp').textContent = 'Last updated: ' + new Date(overview.timestamp).toLocaleString();
                
                // Update risk distribution chart
                updateRiskChart(overview.risk_distribution);
                
                // Update events chart
                updateEventsChart(overview.events_by_type);
                
                // Update suspicious IPs
                updateSuspiciousIPs(overview.suspicious_ips);
                
                // Update critical events
                updateCriticalEvents(overview.critical_events);
            }
            
            // Fetch alerts
            const alerts = await fetchData('alerts');
            if (alerts) {
                updateAlerts(alerts.alerts);
            }
        }
        
        function updateRiskChart(data) {
            const ctx = document.getElementById('risk-chart').getContext('2d');
            
            if (riskChart) {
                riskChart.destroy();
            }
            
            riskChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: data.map(item => item.level.charAt(0).toUpperCase() + item.level.slice(1)),
                    datasets: [{
                        data: data.map(item => item.count),
                        backgroundColor: [
                            '#4CAF50',  // Low
                            '#FFC107',  // Medium
                            '#FF9800',  // High
                            '#F44336'   // Critical
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            labels: {
                                color: '#cccccc'
                            }
                        }
                    }
                }
            });
        }
        
        function updateEventsChart(data) {
            const ctx = document.getElementById('events-chart').getContext('2d');
            
            if (eventsChart) {
                eventsChart.destroy();
            }
            
            eventsChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.map(item => item.type.replace(/_/g, ' ').replace(/\\b\\w/g, l => l.toUpperCase())),
                    datasets: [{
                        label: 'Event Count',
                        data: data.map(item => item.count),
                        backgroundColor: '#4CAF50',
                        borderColor: '#45a049',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            grid: {
                                color: '#333'
                            },
                            ticks: {
                                color: '#cccccc'
                            }
                        },
                        x: {
                            grid: {
                                color: '#333'
                            },
                            ticks: {
                                color: '#cccccc'
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            labels: {
                                color: '#cccccc'
                            }
                        }
                    }
                }
            });
        }
        
        function updateAlerts(alerts) {
            const container = document.getElementById('alerts-container');
            
            if (alerts.length === 0) {
                container.innerHTML = '<div class="alert">✅ No active alerts</div>';
                return;
            }
            
            container.innerHTML = alerts.map(alert => `
                <div class="alert alert-${alert.severity}">
                    <div class="alert-title">${getSeverityIcon(alert.severity)} ${alert.title}</div>
                    <div>${alert.description}</div>
                    <div class="event-timestamp">${new Date(alert.timestamp).toLocaleString()}</div>
                </div>
            `).join('');
        }
        
        function updateSuspiciousIPs(ips) {
            const container = document.getElementById('suspicious-ips');
            
            if (ips.length === 0) {
                container.innerHTML = '<div>✅ No suspicious activity detected</div>';
                return;
            }
            
            container.innerHTML = ips.map(ip => `
                <div class="event">
                    <strong>${ip.ip_address}</strong> - ${ip.event_count} events (Max risk: ${ip.max_risk_score})
                </div>
            `).join('');
        }
        
        function updateCriticalEvents(events) {
            const container = document.getElementById('critical-events');
            
            if (events.length === 0) {
                container.innerHTML = '<div class="event">✅ No critical events</div>';
                return;
            }
            
            container.innerHTML = events.map(event => `
                <div class="event">
                    <div><strong>${event.type.replace(/_/g, ' ')}</strong> from ${event.ip_address}</div>
                    <div class="risk-${getRiskLevel(event.risk_score)}">Risk Score: ${event.risk_score}</div>
                    <div class="event-timestamp">${new Date(event.timestamp).toLocaleString()}</div>
                </div>
            `).join('');
        }
        
        function getSeverityIcon(severity) {
            switch(severity) {
                case 'critical': return '🚨';
                case 'high': return '⚠️';
                case 'medium': return '🟡';
                default: return 'ℹ️';
            }
        }
        
        function getRiskLevel(score) {
            if (score >= 75) return 'high';
            if (score >= 50) return 'medium';
            return 'low';
        }
        
        // Initialize dashboard
        refreshData();
        
        // Auto-refresh every 30 seconds
        setInterval(refreshData, 30000);
    </script>
</body>
</html>
        """
        
        return web.Response(text=html_content, content_type='text/html')
    
    async def health_check(self, request):
        """Health check endpoint"""
        return web.json_response({
            'status': 'healthy',
            'service': 'bizosaas-security-dashboard',
            'version': '1.0.0',
            'timestamp': datetime.utcnow().isoformat()
        })

async def create_dashboard_app(config: Dict[str, Any]) -> web.Application:
    """Create and configure the dashboard application"""
    
    dashboard = SecurityDashboard(config)
    await dashboard.initialize()
    
    # Create application
    app = web.Application()
    
    # Configure CORS
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
            allow_methods="*"
        )
    })
    
    # Routes
    app.router.add_get('/', dashboard.render_dashboard)
    app.router.add_get('/dashboard', dashboard.render_dashboard)
    app.router.add_get('/api/security/overview', dashboard.get_security_overview)
    app.router.add_get('/api/security/alerts', dashboard.get_security_alerts)
    app.router.add_get('/api/security/metrics', dashboard.get_security_metrics)
    app.router.add_get('/api/security/user/{user_id}', dashboard.get_user_security_report)
    app.router.add_get('/health', dashboard.health_check)
    
    # Add CORS to all routes
    for route in list(app.router.routes()):
        cors.add(route)
    
    return app

async def main():
    """Main application entry point"""
    
    # Load configuration
    config = {
        'postgres_host': os.getenv('POSTGRES_HOST', 'host.docker.internal'),
        'postgres_port': int(os.getenv('POSTGRES_PORT', 5432)),
        'postgres_user': os.getenv('POSTGRES_USER', 'admin'),
        'postgres_password': os.getenv('POSTGRES_PASSWORD', 'securepassword'),
        'postgres_db': os.getenv('POSTGRES_DB', 'bizosaas'),
        'redis_host': os.getenv('REDIS_HOST', 'host.docker.internal'),
        'redis_port': int(os.getenv('REDIS_PORT', 6379))
    }
    
    port = int(os.getenv('DASHBOARD_PORT', 8004))
    host = os.getenv('HOST', '0.0.0.0')
    
    print("📊 Starting BizOSaaS Security Dashboard...")
    print(f"🌐 Dashboard will be available at: http://{host}:{port}")
    print("🛡️ Security monitoring features:")
    print("   - Real-time threat detection")
    print("   - Risk scoring and analysis")
    print("   - User behavior monitoring") 
    print("   - Security event correlation")
    print("   - Automated alerting")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    app = await create_dashboard_app(config)
    runner = web.AppRunner(app)
    await runner.setup()
    
    site = web.TCPSite(runner, host, port)
    await site.start()
    
    print(f"✅ Security Dashboard started on port {port}")
    print("💡 Access points:")
    print(f"   Dashboard: http://{host}:{port}/")
    print(f"   API:       http://{host}:{port}/api/security/")
    print("🛑 Press Ctrl+C to stop the dashboard")
    
    # Keep the server running
    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down Security Dashboard...")
        await runner.cleanup()

if __name__ == '__main__':
    import os
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nDashboard stopped.")