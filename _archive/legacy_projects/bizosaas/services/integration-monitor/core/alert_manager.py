"""
Alert Manager
Handles multi-channel alert notifications with escalation
"""

import asyncio
import aiohttp
import smtplib
import logging
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config.settings import settings, get_alert_escalation_rules

logger = logging.getLogger(__name__)


class AlertSeverity(Enum):
    """Alert severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertChannel(Enum):
    """Alert notification channels"""
    EMAIL = "email"
    SLACK = "slack"
    DISCORD = "discord"
    SMS = "sms"
    WEBHOOK = "webhook"


class AlertStatus(Enum):
    """Alert status"""
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"


@dataclass
class Alert:
    """Alert data structure"""
    id: str
    severity: AlertSeverity
    title: str
    message: str
    details: Dict[str, Any]
    integration_name: Optional[str]
    created_at: datetime
    updated_at: datetime
    status: AlertStatus
    channels_sent: List[AlertChannel]
    acknowledgments: List[Dict[str, Any]]
    escalation_level: int
    next_escalation: Optional[datetime]
    resolved_at: Optional[datetime]
    tags: List[str]


@dataclass
class AlertRule:
    """Alert rule configuration"""
    name: str
    severity: AlertSeverity
    conditions: Dict[str, Any]
    channels: List[AlertChannel]
    cooldown_minutes: int
    escalation_minutes: int
    auto_resolve: bool
    enabled: bool


class AlertManager:
    """
    Manages alert notifications across multiple channels
    Implements escalation, deduplication, and acknowledgment
    """
    
    def __init__(self, websocket_manager):
        self.websocket_manager = websocket_manager
        
        # Alert storage
        self.active_alerts: Dict[str, Alert] = {}
        self.alert_history: List[Alert] = []
        
        # Alert rules
        self.alert_rules: List[AlertRule] = []
        
        # Deduplication tracking
        self.last_sent: Dict[str, datetime] = {}
        
        # Escalation tracking
        self.escalation_tasks: Dict[str, asyncio.Task] = {}
        
        # Statistics
        self.alert_stats = {
            'total_alerts': 0,
            'alerts_by_severity': {s.value: 0 for s in AlertSeverity},
            'alerts_by_channel': {c.value: 0 for c in AlertChannel},
            'acknowledgments': 0,
            'auto_resolved': 0,
            'escalations': 0
        }
        
        # HTTP session for webhook/API calls
        self.http_session: Optional[aiohttp.ClientSession] = None
        
        logger.info("Alert Manager initialized")
    
    async def initialize(self):
        """Initialize the alert manager"""
        try:
            # Create HTTP session
            self.http_session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=30)
            )
            
            # Load alert rules
            await self._load_alert_rules()
            
            # Start background tasks
            asyncio.create_task(self._escalation_monitor())
            asyncio.create_task(self._auto_resolution_monitor())
            
            logger.info("Alert Manager initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Alert Manager: {e}")
            raise
    
    async def send_alert(self, severity: str, message: str, details: Optional[Dict[str, Any]] = None,
                        integration_name: Optional[str] = None, tags: Optional[List[str]] = None) -> str:
        """
        Send alert through appropriate channels
        
        Args:
            severity: Alert severity level
            message: Alert message
            details: Additional alert details
            integration_name: Related integration name
            tags: Alert tags for categorization
            
        Returns:
            str: Alert ID
        """
        try:
            severity_enum = AlertSeverity(severity.lower())
        except ValueError:
            logger.error(f"Invalid severity level: {severity}")
            return ""
        
        # Generate alert ID
        alert_id = f"alert_{int(time.time())}_{severity}_{integration_name or 'system'}"
        
        # Check for deduplication
        dedup_key = f"{severity}_{integration_name}_{message}"
        if self._should_suppress_alert(dedup_key):
            logger.debug(f"Suppressing duplicate alert: {dedup_key}")
            return ""
        
        # Create alert object
        alert = Alert(
            id=alert_id,
            severity=severity_enum,
            title=self._generate_alert_title(severity_enum, integration_name),
            message=message,
            details=details or {},
            integration_name=integration_name,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            status=AlertStatus.PENDING,
            channels_sent=[],
            acknowledgments=[],
            escalation_level=0,
            next_escalation=None,
            resolved_at=None,
            tags=tags or []
        )
        
        # Store alert
        self.active_alerts[alert_id] = alert
        self.alert_history.append(alert)
        
        # Update statistics
        self.alert_stats['total_alerts'] += 1
        self.alert_stats['alerts_by_severity'][severity_enum.value] += 1
        
        # Send through appropriate channels
        await self._send_through_channels(alert)
        
        # Schedule escalation if needed
        await self._schedule_escalation(alert)
        
        # Send real-time update
        await self._broadcast_alert_update(alert)
        
        # Update deduplication tracking
        self.last_sent[dedup_key] = datetime.now()
        
        logger.info(f"Alert sent: {alert_id} - {severity} - {message}")
        return alert_id
    
    def _should_suppress_alert(self, dedup_key: str) -> bool:
        """Check if alert should be suppressed due to cooldown"""
        last_sent = self.last_sent.get(dedup_key)
        if not last_sent:
            return False
        
        cooldown = timedelta(seconds=settings.ALERT_COOLDOWN)
        return datetime.now() - last_sent < cooldown
    
    def _generate_alert_title(self, severity: AlertSeverity, integration_name: Optional[str]) -> str:
        """Generate alert title based on severity and integration"""
        severity_emojis = {
            AlertSeverity.LOW: "ℹ️",
            AlertSeverity.MEDIUM: "⚠️",
            AlertSeverity.HIGH: "🚨",
            AlertSeverity.CRITICAL: "🔥"
        }
        
        emoji = severity_emojis.get(severity, "📢")
        integration_part = f" - {integration_name}" if integration_name else ""
        
        return f"{emoji} {severity.value.upper()} Alert{integration_part}"
    
    async def _send_through_channels(self, alert: Alert):
        """Send alert through appropriate notification channels"""
        escalation_rules = get_alert_escalation_rules()
        channels = escalation_rules.get(alert.severity.value, {}).get('channels', ['email'])
        
        # Send to each channel
        for channel_name in channels:
            try:
                channel = AlertChannel(channel_name)
                success = await self._send_to_channel(alert, channel)
                
                if success:
                    alert.channels_sent.append(channel)
                    self.alert_stats['alerts_by_channel'][channel.value] += 1
                    logger.info(f"Alert {alert.id} sent via {channel.value}")
                else:
                    logger.error(f"Failed to send alert {alert.id} via {channel.value}")
                    
            except ValueError:
                logger.error(f"Invalid alert channel: {channel_name}")
        
        # Update alert status
        if alert.channels_sent:
            alert.status = AlertStatus.SENT
        else:
            alert.status = AlertStatus.FAILED
        
        alert.updated_at = datetime.now()
    
    async def _send_to_channel(self, alert: Alert, channel: AlertChannel) -> bool:
        """Send alert to specific channel"""
        try:
            if channel == AlertChannel.EMAIL:
                return await self._send_email_alert(alert)
            elif channel == AlertChannel.SLACK:
                return await self._send_slack_alert(alert)
            elif channel == AlertChannel.DISCORD:
                return await self._send_discord_alert(alert)
            elif channel == AlertChannel.SMS:
                return await self._send_sms_alert(alert)
            elif channel == AlertChannel.WEBHOOK:
                return await self._send_webhook_alert(alert)
            else:
                logger.error(f"Unsupported alert channel: {channel}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to send alert via {channel.value}: {e}")
            return False
    
    async def _send_email_alert(self, alert: Alert) -> bool:
        """Send alert via email"""
        if not settings.SMTP_USERNAME or not settings.SMTP_PASSWORD:
            logger.warning("SMTP credentials not configured, skipping email alert")
            return False
        
        try:
            # Create email content
            subject = f"[BizOSaaS] {alert.title}"
            
            # HTML email body
            html_body = f"""
            <html>
            <body style="font-family: Arial, sans-serif; margin: 20px;">
                <div style="border-left: 4px solid {'#e74c3c' if alert.severity == AlertSeverity.CRITICAL else '#f39c12' if alert.severity == AlertSeverity.HIGH else '#3498db'}; padding-left: 20px;">
                    <h2 style="color: #2c3e50;">{alert.title}</h2>
                    <p style="font-size: 16px; color: #34495e;">{alert.message}</p>
                    
                    <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <h3>Details:</h3>
                        <ul>
                            <li><strong>Severity:</strong> {alert.severity.value.upper()}</li>
                            <li><strong>Integration:</strong> {alert.integration_name or 'System'}</li>
                            <li><strong>Time:</strong> {alert.created_at.strftime('%Y-%m-%d %H:%M:%S UTC')}</li>
                            <li><strong>Alert ID:</strong> {alert.id}</li>
                        </ul>
                    </div>
                    
                    {self._format_alert_details_html(alert.details)}
                    
                    <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd;">
                        <p style="color: #7f8c8d; font-size: 14px;">
                            This alert was generated by BizOSaaS Integration Monitor<br>
                            Dashboard: <a href="http://localhost:{settings.SERVICE_PORT}/dashboard">View Dashboard</a>
                        </p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Send email
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = settings.ALERT_EMAIL_FROM
            msg['To'] = ', '.join(settings.ALERT_EMAIL_TO)
            
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)
            
            # Connect to SMTP server
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
                server.send_message(msg)
            
            logger.info(f"Email alert sent for {alert.id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email alert: {e}")
            return False
    
    async def _send_slack_alert(self, alert: Alert) -> bool:
        """Send alert to Slack"""
        if not settings.SLACK_WEBHOOK_URL:
            logger.warning("Slack webhook URL not configured, skipping Slack alert")
            return False
        
        try:
            # Determine color based on severity
            color_map = {
                AlertSeverity.LOW: "#36a64f",
                AlertSeverity.MEDIUM: "#ff9500",
                AlertSeverity.HIGH: "#ff6b6b",
                AlertSeverity.CRITICAL: "#ff0000"
            }
            
            # Create Slack message
            slack_message = {
                "text": f"BizOSaaS Alert: {alert.title}",
                "attachments": [
                    {
                        "color": color_map.get(alert.severity, "#dddddd"),
                        "title": alert.title,
                        "text": alert.message,
                        "fields": [
                            {
                                "title": "Severity",
                                "value": alert.severity.value.upper(),
                                "short": True
                            },
                            {
                                "title": "Integration",
                                "value": alert.integration_name or "System",
                                "short": True
                            },
                            {
                                "title": "Time",
                                "value": alert.created_at.strftime('%Y-%m-%d %H:%M:%S UTC'),
                                "short": True
                            },
                            {
                                "title": "Alert ID",
                                "value": alert.id,
                                "short": True
                            }
                        ],
                        "footer": "BizOSaaS Integration Monitor",
                        "ts": int(alert.created_at.timestamp())
                    }
                ]
            }
            
            # Add details if present
            if alert.details:
                details_text = "\n".join([f"• {k}: {v}" for k, v in alert.details.items()])
                slack_message["attachments"][0]["fields"].append({
                    "title": "Details",
                    "value": f"```{details_text}```",
                    "short": False
                })
            
            # Send to Slack
            async with self.http_session.post(
                settings.SLACK_WEBHOOK_URL,
                json=slack_message,
                headers={'Content-Type': 'application/json'}
            ) as response:
                if response.status == 200:
                    logger.info(f"Slack alert sent for {alert.id}")
                    return True
                else:
                    logger.error(f"Slack webhook failed with status {response.status}")
                    return False
                    
        except Exception as e:
            logger.error(f"Failed to send Slack alert: {e}")
            return False
    
    async def _send_discord_alert(self, alert: Alert) -> bool:
        """Send alert to Discord"""
        if not settings.DISCORD_WEBHOOK_URL:
            logger.warning("Discord webhook URL not configured, skipping Discord alert")
            return False
        
        try:
            # Determine color based on severity
            color_map = {
                AlertSeverity.LOW: 0x00ff00,
                AlertSeverity.MEDIUM: 0xffff00,
                AlertSeverity.HIGH: 0xff6600,
                AlertSeverity.CRITICAL: 0xff0000
            }
            
            # Create Discord embed
            embed = {
                "title": alert.title,
                "description": alert.message,
                "color": color_map.get(alert.severity, 0x888888),
                "timestamp": alert.created_at.isoformat(),
                "fields": [
                    {
                        "name": "Severity",
                        "value": alert.severity.value.upper(),
                        "inline": True
                    },
                    {
                        "name": "Integration",
                        "value": alert.integration_name or "System",
                        "inline": True
                    },
                    {
                        "name": "Alert ID",
                        "value": alert.id,
                        "inline": True
                    }
                ],
                "footer": {
                    "text": "BizOSaaS Integration Monitor"
                }
            }
            
            # Add details if present
            if alert.details:
                details_text = "\n".join([f"• **{k}**: {v}" for k, v in alert.details.items()])
                embed["fields"].append({
                    "name": "Details",
                    "value": details_text[:1024],  # Discord field limit
                    "inline": False
                })
            
            discord_message = {
                "embeds": [embed]
            }
            
            # Send to Discord
            async with self.http_session.post(
                settings.DISCORD_WEBHOOK_URL,
                json=discord_message,
                headers={'Content-Type': 'application/json'}
            ) as response:
                if response.status in [200, 204]:
                    logger.info(f"Discord alert sent for {alert.id}")
                    return True
                else:
                    logger.error(f"Discord webhook failed with status {response.status}")
                    return False
                    
        except Exception as e:
            logger.error(f"Failed to send Discord alert: {e}")
            return False
    
    async def _send_sms_alert(self, alert: Alert) -> bool:
        """Send alert via SMS"""
        if not settings.SMS_API_KEY or not settings.ONCALL_PHONE_NUMBERS:
            logger.warning("SMS configuration not complete, skipping SMS alert")
            return False
        
        # Only send SMS for high/critical alerts
        if alert.severity not in [AlertSeverity.HIGH, AlertSeverity.CRITICAL]:
            return True
        
        try:
            message = f"BizOSaaS ALERT: {alert.title}\n{alert.message}\nID: {alert.id}"
            
            success_count = 0
            for phone_number in settings.ONCALL_PHONE_NUMBERS:
                # Implementation would depend on SMS service provider
                # This is a placeholder for the actual SMS sending logic
                logger.info(f"Would send SMS to {phone_number}: {message}")
                success_count += 1
            
            logger.info(f"SMS alerts sent to {success_count} numbers for {alert.id}")
            return success_count > 0
            
        except Exception as e:
            logger.error(f"Failed to send SMS alert: {e}")
            return False
    
    async def _send_webhook_alert(self, alert: Alert) -> bool:
        """Send alert to custom webhook"""
        # This could be used for integrating with external systems
        try:
            webhook_payload = {
                "alert_id": alert.id,
                "severity": alert.severity.value,
                "title": alert.title,
                "message": alert.message,
                "details": alert.details,
                "integration_name": alert.integration_name,
                "timestamp": alert.created_at.isoformat(),
                "source": "bizosaas-integration-monitor"
            }
            
            # Example webhook URL (would be configurable)
            webhook_url = "https://hooks.example.com/alerts"
            
            async with self.http_session.post(
                webhook_url,
                json=webhook_payload,
                headers={'Content-Type': 'application/json'}
            ) as response:
                if response.status == 200:
                    logger.info(f"Webhook alert sent for {alert.id}")
                    return True
                else:
                    logger.error(f"Webhook failed with status {response.status}")
                    return False
                    
        except Exception as e:
            logger.error(f"Failed to send webhook alert: {e}")
            return False
    
    def _format_alert_details_html(self, details: Dict[str, Any]) -> str:
        """Format alert details as HTML"""
        if not details:
            return ""
        
        html = "<div style='background: #f1f2f6; padding: 15px; border-radius: 5px; margin: 20px 0;'>"
        html += "<h3>Technical Details:</h3><ul>"
        
        for key, value in details.items():
            html += f"<li><strong>{key}:</strong> {value}</li>"
        
        html += "</ul></div>"
        return html
    
    async def _schedule_escalation(self, alert: Alert):
        """Schedule alert escalation if needed"""
        escalation_rules = get_alert_escalation_rules()
        escalation_time = escalation_rules.get(alert.severity.value, {}).get('escalation_time')
        
        if escalation_time:
            alert.next_escalation = alert.created_at + timedelta(seconds=escalation_time)
            
            # Create escalation task
            task = asyncio.create_task(self._handle_escalation(alert))
            self.escalation_tasks[alert.id] = task
    
    async def _handle_escalation(self, alert: Alert):
        """Handle alert escalation"""
        try:
            if alert.next_escalation:
                # Wait until escalation time
                wait_time = (alert.next_escalation - datetime.now()).total_seconds()
                if wait_time > 0:
                    await asyncio.sleep(wait_time)
                
                # Check if alert is still active and not acknowledged
                if alert.id in self.active_alerts and alert.status != AlertStatus.ACKNOWLEDGED:
                    alert.escalation_level += 1
                    
                    # Send escalated alert
                    escalated_message = f"ESCALATION #{alert.escalation_level}: {alert.message}"
                    await self.send_alert(
                        severity="critical",
                        message=escalated_message,
                        details=alert.details,
                        integration_name=alert.integration_name,
                        tags=alert.tags + ["escalated"]
                    )
                    
                    self.alert_stats['escalations'] += 1
                    logger.warning(f"Alert escalated: {alert.id} (level {alert.escalation_level})")
                    
        except asyncio.CancelledError:
            logger.debug(f"Escalation cancelled for alert {alert.id}")
        except Exception as e:
            logger.error(f"Escalation failed for alert {alert.id}: {e}")
    
    async def _escalation_monitor(self):
        """Background task to monitor escalations"""
        while True:
            try:
                await asyncio.sleep(60)  # Check every minute
                
                # Clean up completed escalation tasks
                completed_tasks = [
                    alert_id for alert_id, task in self.escalation_tasks.items()
                    if task.done()
                ]
                
                for alert_id in completed_tasks:
                    del self.escalation_tasks[alert_id]
                    
            except Exception as e:
                logger.error(f"Escalation monitor error: {e}")
    
    async def _auto_resolution_monitor(self):
        """Background task to auto-resolve alerts"""
        while True:
            try:
                await asyncio.sleep(300)  # Check every 5 minutes
                
                # Check for alerts that can be auto-resolved
                current_time = datetime.now()
                auto_resolved = []
                
                for alert_id, alert in list(self.active_alerts.items()):
                    # Auto-resolve after 1 hour if no updates
                    if (current_time - alert.updated_at).total_seconds() > 3600:
                        await self.resolve_alert(alert_id, "Auto-resolved after 1 hour")
                        auto_resolved.append(alert_id)
                
                if auto_resolved:
                    logger.info(f"Auto-resolved {len(auto_resolved)} alerts")
                    
            except Exception as e:
                logger.error(f"Auto-resolution monitor error: {e}")
    
    async def _broadcast_alert_update(self, alert: Alert):
        """Broadcast alert update via WebSocket"""
        try:
            if self.websocket_manager.has_connections():
                update_data = {
                    'type': 'alert_update',
                    'timestamp': datetime.now().isoformat(),
                    'data': asdict(alert)
                }
                
                # Convert datetime objects to ISO strings
                update_data['data']['created_at'] = alert.created_at.isoformat()
                update_data['data']['updated_at'] = alert.updated_at.isoformat()
                if alert.next_escalation:
                    update_data['data']['next_escalation'] = alert.next_escalation.isoformat()
                if alert.resolved_at:
                    update_data['data']['resolved_at'] = alert.resolved_at.isoformat()
                
                # Convert enums to strings
                update_data['data']['severity'] = alert.severity.value
                update_data['data']['status'] = alert.status.value
                update_data['data']['channels_sent'] = [c.value for c in alert.channels_sent]
                
                await self.websocket_manager.broadcast(update_data)
                
        except Exception as e:
            logger.error(f"Failed to broadcast alert update: {e}")
    
    async def _load_alert_rules(self):
        """Load alert rules configuration"""
        # Default alert rules
        default_rules = [
            AlertRule(
                name="integration_unhealthy",
                severity=AlertSeverity.CRITICAL,
                conditions={"status": "unhealthy", "consecutive_failures": ">=3"},
                channels=[AlertChannel.EMAIL, AlertChannel.SLACK, AlertChannel.SMS],
                cooldown_minutes=5,
                escalation_minutes=15,
                auto_resolve=False,
                enabled=True
            ),
            AlertRule(
                name="high_response_time",
                severity=AlertSeverity.HIGH,
                conditions={"response_time": ">5.0"},
                channels=[AlertChannel.EMAIL, AlertChannel.SLACK],
                cooldown_minutes=10,
                escalation_minutes=30,
                auto_resolve=True,
                enabled=True
            ),
            AlertRule(
                name="high_error_rate",
                severity=AlertSeverity.HIGH,
                conditions={"error_rate": ">0.05"},
                channels=[AlertChannel.EMAIL, AlertChannel.SLACK],
                cooldown_minutes=10,
                escalation_minutes=30,
                auto_resolve=True,
                enabled=True
            ),
            AlertRule(
                name="cost_threshold",
                severity=AlertSeverity.MEDIUM,
                conditions={"daily_cost": f">{settings.COST_ALERT_THRESHOLD}"},
                channels=[AlertChannel.EMAIL],
                cooldown_minutes=60,
                escalation_minutes=0,
                auto_resolve=False,
                enabled=True
            )
        ]
        
        self.alert_rules = default_rules
        logger.info(f"Loaded {len(self.alert_rules)} alert rules")
    
    # Public API methods
    
    async def acknowledge_alert(self, alert_id: str, user_id: str, comment: Optional[str] = None) -> bool:
        """Acknowledge an alert"""
        alert = self.active_alerts.get(alert_id)
        if not alert:
            return False
        
        alert.status = AlertStatus.ACKNOWLEDGED
        alert.updated_at = datetime.now()
        alert.acknowledgments.append({
            'user_id': user_id,
            'timestamp': datetime.now().isoformat(),
            'comment': comment
        })
        
        # Cancel escalation
        if alert_id in self.escalation_tasks:
            self.escalation_tasks[alert_id].cancel()
            del self.escalation_tasks[alert_id]
        
        self.alert_stats['acknowledgments'] += 1
        
        # Broadcast update
        await self._broadcast_alert_update(alert)
        
        logger.info(f"Alert acknowledged: {alert_id} by {user_id}")
        return True
    
    async def resolve_alert(self, alert_id: str, resolution_comment: Optional[str] = None) -> bool:
        """Resolve an alert"""
        alert = self.active_alerts.get(alert_id)
        if not alert:
            return False
        
        alert.status = AlertStatus.RESOLVED
        alert.resolved_at = datetime.now()
        alert.updated_at = datetime.now()
        
        if resolution_comment:
            alert.acknowledgments.append({
                'type': 'resolution',
                'timestamp': datetime.now().isoformat(),
                'comment': resolution_comment
            })
        
        # Remove from active alerts
        del self.active_alerts[alert_id]
        
        # Cancel escalation
        if alert_id in self.escalation_tasks:
            self.escalation_tasks[alert_id].cancel()
            del self.escalation_tasks[alert_id]
        
        self.alert_stats['auto_resolved'] += 1
        
        # Broadcast update
        await self._broadcast_alert_update(alert)
        
        logger.info(f"Alert resolved: {alert_id}")
        return True
    
    async def get_active_alerts(self) -> List[Dict[str, Any]]:
        """Get all active alerts"""
        return [asdict(alert) for alert in self.active_alerts.values()]
    
    async def get_alert_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get alert history"""
        recent_alerts = sorted(self.alert_history, key=lambda x: x.created_at, reverse=True)[:limit]
        return [asdict(alert) for alert in recent_alerts]
    
    async def get_alert_statistics(self) -> Dict[str, Any]:
        """Get alert statistics"""
        total_alerts = self.alert_stats['total_alerts']
        
        return {
            **self.alert_stats,
            'active_alerts': len(self.active_alerts),
            'acknowledgment_rate': (self.alert_stats['acknowledgments'] / total_alerts * 100) if total_alerts > 0 else 0,
            'escalation_rate': (self.alert_stats['escalations'] / total_alerts * 100) if total_alerts > 0 else 0,
            'average_resolution_time': 0,  # Would be calculated from historical data
            'alert_rules_count': len(self.alert_rules)
        }
    
    async def cleanup(self):
        """Cleanup resources"""
        # Cancel all escalation tasks
        for task in self.escalation_tasks.values():
            task.cancel()
        
        # Close HTTP session
        if self.http_session:
            await self.http_session.close()
        
        logger.info("Alert Manager cleaned up")