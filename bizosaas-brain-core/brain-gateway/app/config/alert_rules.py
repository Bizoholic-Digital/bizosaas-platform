"""
Alert rule configuration.

Defines alert conditions, thresholds, and severity levels for
automated platform monitoring.
"""

from typing import Dict, Any, List
from pydantic_settings import BaseSettings
from pydantic import Field


class AlertConfig(BaseSettings):
    """Configuration for analytics alerts."""
    
    # Global alert switch
    alerts_enabled: bool = Field(
        default=True,
        description="Enable/disable all alerts"
    )
    
    # Workflow Alerts
    alert_workflow_failure_rate_threshold: float = Field(
        default=0.20,  # 20% failure rate
        description="Threshold for workflow failure rate alert"
    )
    alert_workflow_failure_rate_severity: str = Field(
        default="high",
        description="Severity for high failure rate"
    )
    
    alert_avg_duration_threshold_seconds: float = Field(
        default=300.0,  # 5 minutes
        description="Threshold for avg workflow duration alert"
    )
    
    # Cost Alerts
    alert_daily_cost_threshold_usd: float = Field(
        default=100.0,
        description="Threshold for daily platform cost"
    )
    alert_tenant_daily_cost_threshold_usd: float = Field(
        default=20.0,
        description="Threshold for single tenant daily cost"
    )
    
    # Campaign Alerts
    alert_campaign_ctr_low_threshold: float = Field(
        default=0.5,  # 0.5% CTR
        description="Threshold for low CTR alert"
    )
    alert_campaign_conversion_rate_low_threshold: float = Field(
        default=0.1,  # 0.1% Conv Rate
        description="Threshold for low conversion rate alert"
    )
    
    # Notification Channels
    alert_webhook_url: str = Field(
        default="",
        description="Webhook URL for alert notifications"
    )
    alert_email_enabled: bool = Field(
        default=False,
        description="Enable email notifications"
    )
    alert_email_to: str = Field(
        default="",
        description="Recipient email for alerts"
    )
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"


# Global alert configuration instance
alert_config = AlertConfig()


def get_default_alert_rules() -> List[Dict[str, Any]]:
    """
    Get default alert rules based on configuration.
    
    Returns:
        List of alert rule definitions
    """
    return [
        {
            "id": "workflow_failure_rate_high",
            "name": "High Workflow Failure Rate",
            "description": f"Workflow failure rate exceeds {alert_config.alert_workflow_failure_rate_threshold*100}%",
            "metric": "workflow_failure_rate",
            "operator": "gt",
            "threshold": alert_config.alert_workflow_failure_rate_threshold,
            "severity": alert_config.alert_workflow_failure_rate_severity,
            "category": "performance"
        },
        {
            "id": "workflow_duration_high",
            "name": "Slow Workflow Execution",
            "description": f"Average duration exceeds {alert_config.alert_avg_duration_threshold_seconds}s",
            "metric": "avg_duration_seconds",
            "operator": "gt",
            "threshold": alert_config.alert_avg_duration_threshold_seconds,
            "severity": "medium",
            "category": "performance"
        },
        {
            "id": "platform_cost_high",
            "name": "High Platform Cost",
            "description": f"Daily platform cost exceeds ${alert_config.alert_daily_cost_threshold_usd}",
            "metric": "total_cost_usd",
            "operator": "gt",
            "threshold": alert_config.alert_daily_cost_threshold_usd,
            "severity": "high",
            "category": "cost"
        },
        {
            "id": "campaign_ctr_low",
            "name": "Low Campaign CTR",
            "description": f"Platform CTR falls below {alert_config.alert_campaign_ctr_low_threshold}%",
            "metric": "platform_ctr",
            "operator": "lt",
            "threshold": alert_config.alert_campaign_ctr_low_threshold,
            "severity": "medium",
            "category": "marketing"
        }
    ]
