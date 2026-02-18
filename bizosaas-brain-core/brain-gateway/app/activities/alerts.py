"""
Alert system activities.

Activities for monitoring metrics, evaluating alert rules, and sending notifications.
"""

import logging
from typing import Dict, Any, List
from datetime import datetime, timezone

from temporalio import activity
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.settings import settings
from app.config.alert_rules import alert_config, get_default_alert_rules
from app.models.alert_history import AlertHistory
from app.models.platform_metrics import PlatformMetrics
from app.services.email_service import EmailService  # Assumed existing or to be created
# from app.services.slack_service import SlackService  # Future integration

logger = logging.getLogger(__name__)

# Activity logger
activity_logger = logging.getLogger("temporal_activity")


@activity.defn
async def check_platform_alerts_activity() -> Dict[str, Any]:
    """
    Check platform metrics against alert rules and trigger notifications.
    
    Returns:
        Summary of alerts processed
    """
    if not alert_config.alerts_enabled:
        activity_logger.info("Alerts are disabled globally.")
        return {"status": "disabled", "alerts_triggered": 0}

    engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True, pool_recycle=300, pool_size=5, max_overflow=10)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    triggered_alerts = []
    
    try:
        # Get latest platform metrics
        latest_metrics = db.query(PlatformMetrics).order_by(
            PlatformMetrics.snapshot_time.desc()
        ).first()
        
        if not latest_metrics:
            activity_logger.warning("No platform metrics found for alert evaluation.")
            return {"status": "no_metrics", "alerts_triggered": 0}
        
        # Flatten metrics for easy evaluation
        metrics_map = {
            "workflow_failure_rate": 0.0, # Calculated below if possible
            "avg_duration_seconds": latest_metrics.avg_workflow_duration,
            "total_cost_usd": latest_metrics.total_workflow_cost,
            "platform_ctr": latest_metrics.platform_ctr,
            "platform_conversion_rate": latest_metrics.platform_conversion_rate,
            "active_campaigns": latest_metrics.active_campaigns
        }
        
        # Calculate derived metrics if needed
        # Example: workflow_failure_rate is not directly in PlatformMetrics summary but 
        # success_rate is. So failure rate = 1 - success_rate or similar.
        # Assuming workflow_success_rate is 0.0 to 1.0
        if hasattr(latest_metrics, 'workflow_success_rate'):
             metrics_map["workflow_failure_rate"] = 1.0 - latest_metrics.workflow_success_rate

        
        rules = get_default_alert_rules()
        activity_logger.info(f"Evaluating {len(rules)} alert rules against metrics check.")

        for rule in rules:
            metric_name = rule["metric"]
            threshold = rule["threshold"]
            operator = rule["operator"]
            
            current_value = metrics_map.get(metric_name)
            
            if current_value is None:
                continue
                
            is_triggered = False
            if operator == "gt" and current_value > threshold:
                is_triggered = True
            elif operator == "lt" and current_value < threshold:
                is_triggered = True
            elif operator == "eq" and current_value == threshold:
                is_triggered = True
                
            if is_triggered:
                # Create alert history record
                alert = AlertHistory(
                    id=f"alert_{datetime.now(timezone.utc).timestamp()}_{rule['id']}", # Simple ID generation
                    rule_id=rule["id"],
                    rule_name=rule["name"],
                    severity=rule["severity"],
                    category=rule["category"],
                    metric_name=metric_name,
                    metric_value=current_value,
                    threshold_value=threshold,
                    message=rule["description"],
                    status="active",
                    created_at=datetime.now(timezone.utc)
                )
                db.add(alert)
                triggered_alerts.append(alert)
                activity_logger.warning(f"Alert triggered: {rule['name']} - Value: {current_value}")
        
        db.commit()
        
        # Process notifications for triggered alerts
        if triggered_alerts:
             await process_notifications(triggered_alerts, db)

        return {
            "status": "success",
            "alerts_evaluated": len(rules),
            "alerts_triggered": len(triggered_alerts),
            "triggered_rules": [a.rule_name for a in triggered_alerts]
        }
        
    except Exception as e:
        activity_logger.error(f"Error checking platform alerts: {e}")
        return {"status": "error", "error": str(e)}
    finally:
        db.close()

async def process_notifications(alerts: List[AlertHistory], db):
    """
    Send notifications for triggered alerts.
    
    Args:
        alerts: List of AlertHistory objects
        db: Database session
    """
    # Group alerts by channel preference (simplified for now)
    
    # Webhook Notification
    if alert_config.alert_webhook_url:
        try:
             import aiohttp
             async with aiohttp.ClientSession() as session:
                 payload = {
                     "text": f"Running Platform Alerts: {len(alerts)} alerts triggered.",
                     "alerts": [a.to_dict() for a in alerts]
                 }
                 async with session.post(alert_config.alert_webhook_url, json=payload) as resp:
                     if resp.status in [200, 201, 204]:
                         activity_logger.info("Webhook notification sent successfully.")
                         for alert in alerts:
                             alert.notification_sent = True
                             current_channels = alert.notification_channels or []
                             if "webhook" not in current_channels:
                                 current_channels.append("webhook")
                             alert.notification_channels = current_channels
                     else:
                         activity_logger.error(f"Webhook notification failed with status {resp.status}")
        except Exception as e:
            activity_logger.error(f"Failed to send webhook notification: {e}")

    # Email Notification
    if alert_config.alert_email_enabled and alert_config.alert_email_to:
        # Placeholder for email logic
        activity_logger.info("Email notification enabled but not fully implemented in this MVP activity.")
        # Future: await EmailService.send_alert_email(...)
    
    db.commit()
