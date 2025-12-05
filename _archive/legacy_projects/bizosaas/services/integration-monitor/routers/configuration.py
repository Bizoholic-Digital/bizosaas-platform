"""
Configuration Router
API endpoints for managing monitoring configuration
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

router = APIRouter()


class AlertRuleCreate(BaseModel):
    name: str
    description: str
    severity: str
    conditions: Dict[str, Any]
    channels: List[str]
    cooldown_minutes: int
    escalation_minutes: int
    enabled: bool = True


class IntegrationConfigUpdate(BaseModel):
    health_check_interval: Optional[int] = None
    timeout: Optional[int] = None
    retry_attempts: Optional[int] = None
    circuit_breaker_enabled: Optional[bool] = None
    rate_limit: Optional[int] = None
    alert_on_failure: Optional[bool] = None
    priority: Optional[str] = None


@router.get("/")
async def get_configuration():
    """Get current monitoring configuration"""
    
    config = {
        "service": {
            "name": "integration-monitor",
            "version": "1.0.0",
            "host": "0.0.0.0",
            "port": 8003,
            "debug": False
        },
        "monitoring": {
            "interval": 30,
            "timeout": 10,
            "failover_threshold": 3,
            "rate_limit_window": 60,
            "performance_thresholds": {
                "response_time_warning": 2.0,
                "response_time_critical": 5.0,
                "error_rate_warning": 0.02,
                "error_rate_critical": 0.05,
                "uptime_target": 0.999
            }
        },
        "alerts": {
            "cooldown": 300,
            "escalation": 900,
            "channels": {
                "email": {
                    "enabled": True,
                    "from": "alerts@bizosaas.com",
                    "to": ["ops@bizosaas.com"]
                },
                "slack": {
                    "enabled": True,
                    "webhook_url": "configured"
                },
                "sms": {
                    "enabled": False,
                    "provider": "twilio"
                }
            }
        },
        "database": {
            "url": "postgresql://localhost:5432/integration_monitor",
            "pool_size": 10,
            "max_overflow": 20
        },
        "redis": {
            "url": "redis://localhost:6379/3",
            "max_connections": 50
        },
        "security": {
            "api_key_expiry_days": 90,
            "max_login_attempts": 5,
            "login_lockout_duration": 900
        }
    }
    
    return {
        "success": True,
        "data": config
    }


@router.get("/integrations")
async def get_integrations_config():
    """Get configuration for all integrations"""
    
    integrations_config = {
        "stripe": {
            "enabled": True,
            "health_check_interval": 15,
            "timeout": 5,
            "retry_attempts": 3,
            "circuit_breaker_enabled": True,
            "rate_limit": 1000,
            "cost_tracking": True,
            "alert_on_failure": True,
            "priority": "critical",
            "sla_target": 0.9995,
            "failover_strategy": "primary_secondary"
        },
        "paypal": {
            "enabled": True,
            "health_check_interval": 30,
            "timeout": 10,
            "retry_attempts": 3,
            "circuit_breaker_enabled": True,
            "rate_limit": 500,
            "cost_tracking": True,
            "alert_on_failure": True,
            "priority": "critical",
            "sla_target": 0.999,
            "failover_strategy": "primary_secondary"
        },
        "google_ads": {
            "enabled": True,
            "health_check_interval": 30,
            "timeout": 15,
            "retry_attempts": 2,
            "circuit_breaker_enabled": True,
            "rate_limit": 10000,
            "cost_tracking": True,
            "alert_on_failure": True,
            "priority": "high",
            "sla_target": 0.995,
            "failover_strategy": "smart_routing"
        },
        "openai": {
            "enabled": True,
            "health_check_interval": 60,
            "timeout": 30,
            "retry_attempts": 2,
            "circuit_breaker_enabled": True,
            "rate_limit": 3000,
            "cost_tracking": True,
            "alert_on_failure": True,
            "priority": "medium",
            "sla_target": 0.99,
            "failover_strategy": "load_balancing"
        }
    }
    
    return {
        "success": True,
        "data": integrations_config
    }


@router.get("/integrations/{integration_name}")
async def get_integration_config(integration_name: str):
    """Get configuration for specific integration"""
    
    # Mock configuration data
    configs = {
        "stripe": {
            "enabled": True,
            "health_check_interval": 15,
            "timeout": 5,
            "retry_attempts": 3,
            "retry_delay": 1,
            "circuit_breaker_enabled": True,
            "circuit_breaker_threshold": 5,
            "circuit_breaker_timeout": 60,
            "rate_limit": 1000,
            "cost_tracking": True,
            "alert_on_failure": True,
            "alert_on_degradation": True,
            "priority": "critical",
            "sla_target": 0.9995,
            "failover_strategy": "primary_secondary",
            "custom_headers": {
                "X-Integration-Monitor": "BizOSaaS"
            },
            "authentication": {
                "type": "bearer",
                "header": "Authorization"
            },
            "endpoints": {
                "health_check": "https://api.stripe.com/v1/account",
                "primary": "https://api.stripe.com",
                "fallback": "https://api-backup.stripe.com"
            }
        }
    }
    
    if integration_name not in configs:
        raise HTTPException(status_code=404, detail="Integration configuration not found")
    
    return {
        "success": True,
        "data": configs[integration_name]
    }


@router.put("/integrations/{integration_name}")
async def update_integration_config(integration_name: str, config: IntegrationConfigUpdate):
    """Update configuration for specific integration"""
    
    # Would update actual configuration in real implementation
    updated_config = config.dict(exclude_unset=True)
    
    return {
        "success": True,
        "message": f"Configuration updated for {integration_name}",
        "data": {
            "integration": integration_name,
            "updated_fields": list(updated_config.keys()),
            "updated_at": "2024-01-19T10:30:00Z"
        }
    }


@router.get("/alert-rules")
async def get_alert_rules():
    """Get all alert rules configuration"""
    
    alert_rules = [
        {
            "id": "rule_001",
            "name": "integration_unhealthy",
            "description": "Trigger when integration becomes unhealthy",
            "severity": "critical",
            "conditions": {
                "status": "unhealthy",
                "consecutive_failures": ">=3"
            },
            "channels": ["email", "slack", "sms"],
            "cooldown_minutes": 5,
            "escalation_minutes": 15,
            "auto_resolve": False,
            "enabled": True,
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        },
        {
            "id": "rule_002",
            "name": "high_response_time",
            "description": "Trigger when response time exceeds threshold",
            "severity": "high",
            "conditions": {
                "response_time": ">5.0"
            },
            "channels": ["email", "slack"],
            "cooldown_minutes": 10,
            "escalation_minutes": 30,
            "auto_resolve": True,
            "enabled": True,
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        },
        {
            "id": "rule_003",
            "name": "high_error_rate",
            "description": "Trigger when error rate exceeds threshold",
            "severity": "high",
            "conditions": {
                "error_rate": ">0.05"
            },
            "channels": ["email", "slack"],
            "cooldown_minutes": 10,
            "escalation_minutes": 30,
            "auto_resolve": True,
            "enabled": True,
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        }
    ]
    
    return {
        "success": True,
        "data": alert_rules,
        "total": len(alert_rules)
    }


@router.post("/alert-rules")
async def create_alert_rule(rule: AlertRuleCreate):
    """Create new alert rule"""
    
    # Validate severity
    valid_severities = ["low", "medium", "high", "critical"]
    if rule.severity not in valid_severities:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid severity. Must be one of: {', '.join(valid_severities)}"
        )
    
    # Validate channels
    valid_channels = ["email", "slack", "discord", "sms", "webhook"]
    invalid_channels = [c for c in rule.channels if c not in valid_channels]
    if invalid_channels:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid channels: {', '.join(invalid_channels)}"
        )
    
    # Would create actual alert rule in real implementation
    rule_id = f"rule_{int(time.time())}"
    
    return {
        "success": True,
        "message": "Alert rule created successfully",
        "data": {
            "id": rule_id,
            "name": rule.name,
            "created_at": "2024-01-19T10:30:00Z"
        }
    }


@router.put("/alert-rules/{rule_id}")
async def update_alert_rule(rule_id: str, rule: AlertRuleCreate):
    """Update existing alert rule"""
    
    # Would update actual alert rule in real implementation
    
    return {
        "success": True,
        "message": f"Alert rule {rule_id} updated successfully",
        "data": {
            "id": rule_id,
            "name": rule.name,
            "updated_at": "2024-01-19T10:30:00Z"
        }
    }


@router.delete("/alert-rules/{rule_id}")
async def delete_alert_rule(rule_id: str):
    """Delete alert rule"""
    
    # Would delete actual alert rule in real implementation
    
    return {
        "success": True,
        "message": f"Alert rule {rule_id} deleted successfully",
        "data": {
            "id": rule_id,
            "deleted_at": "2024-01-19T10:30:00Z"
        }
    }


@router.get("/thresholds")
async def get_thresholds():
    """Get monitoring thresholds configuration"""
    
    thresholds = {
        "response_time": {
            "warning": 2.0,
            "critical": 5.0,
            "unit": "seconds"
        },
        "error_rate": {
            "warning": 0.02,
            "critical": 0.05,
            "unit": "percentage"
        },
        "uptime": {
            "target": 0.999,
            "warning": 0.995,
            "critical": 0.99,
            "unit": "percentage"
        },
        "cost": {
            "daily_warning": 100.0,
            "daily_critical": 200.0,
            "monthly_budget": 3000.0,
            "unit": "USD"
        },
        "rate_limit": {
            "warning": 0.8,
            "critical": 0.95,
            "unit": "percentage"
        }
    }
    
    return {
        "success": True,
        "data": thresholds
    }


@router.put("/thresholds")
async def update_thresholds(thresholds: Dict[str, Any]):
    """Update monitoring thresholds"""
    
    # Would validate and update actual thresholds in real implementation
    
    return {
        "success": True,
        "message": "Thresholds updated successfully",
        "data": {
            "updated_thresholds": list(thresholds.keys()),
            "updated_at": "2024-01-19T10:30:00Z"
        }
    }


@router.get("/failover")
async def get_failover_config():
    """Get failover configuration"""
    
    failover_config = {
        "strategies": {
            "payment": "primary_secondary",
            "marketing": "load_balancing",
            "communication": "circuit_breaker",
            "ecommerce": "graceful_degradation",
            "analytics": "smart_routing",
            "infrastructure": "primary_secondary",
            "ai": "load_balancing"
        },
        "circuit_breaker": {
            "failure_threshold": 5,
            "timeout_seconds": 60,
            "recovery_threshold": 3
        },
        "load_balancer": {
            "algorithm": "weighted_round_robin",
            "health_score_weight": 0.7,
            "response_time_weight": 0.3
        },
        "retry_policy": {
            "max_retries": 3,
            "backoff_factor": 2,
            "max_delay": 30
        },
        "health_check": {
            "interval": 30,
            "timeout": 10,
            "consecutive_failures": 3
        }
    }
    
    return {
        "success": True,
        "data": failover_config
    }


@router.put("/failover")
async def update_failover_config(config: Dict[str, Any]):
    """Update failover configuration"""
    
    # Would validate and update actual failover config in real implementation
    
    return {
        "success": True,
        "message": "Failover configuration updated successfully",
        "data": {
            "updated_at": "2024-01-19T10:30:00Z"
        }
    }


@router.get("/notifications")
async def get_notification_config():
    """Get notification channel configuration"""
    
    notification_config = {
        "email": {
            "enabled": True,
            "smtp_host": "smtp.resend.com",
            "smtp_port": 587,
            "from_address": "alerts@bizosaas.com",
            "to_addresses": ["ops@bizosaas.com", "admin@bizosaas.com"],
            "template": "default"
        },
        "slack": {
            "enabled": True,
            "webhook_configured": True,
            "channel": "#alerts",
            "mention_users": ["@ops-team"],
            "template": "detailed"
        },
        "discord": {
            "enabled": False,
            "webhook_configured": False,
            "channel": "alerts",
            "template": "compact"
        },
        "sms": {
            "enabled": False,
            "provider": "twilio",
            "phone_numbers": ["+1234567890"],
            "critical_only": True
        },
        "webhook": {
            "enabled": False,
            "url": "",
            "headers": {},
            "timeout": 30
        },
        "escalation": {
            "enabled": True,
            "levels": [
                {
                    "level": 1,
                    "delay_minutes": 15,
                    "channels": ["email", "slack"]
                },
                {
                    "level": 2,
                    "delay_minutes": 30,
                    "channels": ["email", "slack", "sms"]
                }
            ]
        }
    }
    
    return {
        "success": True,
        "data": notification_config
    }


@router.put("/notifications")
async def update_notification_config(config: Dict[str, Any]):
    """Update notification configuration"""
    
    # Would validate and update actual notification config in real implementation
    
    return {
        "success": True,
        "message": "Notification configuration updated successfully",
        "data": {
            "updated_channels": list(config.keys()),
            "updated_at": "2024-01-19T10:30:00Z"
        }
    }


@router.post("/test-notification")
async def test_notification(channel: str, message: str = "Test notification from Integration Monitor"):
    """Test notification channel"""
    
    valid_channels = ["email", "slack", "discord", "sms", "webhook"]
    
    if channel not in valid_channels:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid channel. Must be one of: {', '.join(valid_channels)}"
        )
    
    # Would send actual test notification in real implementation
    
    return {
        "success": True,
        "message": f"Test notification sent via {channel}",
        "data": {
            "channel": channel,
            "test_message": message,
            "sent_at": "2024-01-19T10:30:00Z",
            "delivery_status": "success"
        }
    }


@router.get("/backup")
async def backup_configuration():
    """Create backup of current configuration"""
    
    # Would create actual configuration backup in real implementation
    
    backup_data = {
        "backup_id": f"backup_{int(time.time())}",
        "created_at": "2024-01-19T10:30:00Z",
        "includes": [
            "integration_configs",
            "alert_rules",
            "thresholds",
            "failover_settings",
            "notification_settings"
        ],
        "size": "2.3 KB",
        "download_url": "/config/download/backup_1705662600.json"
    }
    
    return {
        "success": True,
        "message": "Configuration backup created successfully",
        "data": backup_data
    }


@router.post("/restore")
async def restore_configuration(backup_id: str):
    """Restore configuration from backup"""
    
    # Would restore actual configuration in real implementation
    
    return {
        "success": True,
        "message": f"Configuration restored from backup {backup_id}",
        "data": {
            "backup_id": backup_id,
            "restored_at": "2024-01-19T10:30:00Z",
            "restored_components": [
                "integration_configs",
                "alert_rules",
                "thresholds"
            ]
        }
    }


@router.get("/schema")
async def get_configuration_schema():
    """Get configuration schema for validation"""
    
    schema = {
        "integration_config": {
            "type": "object",
            "properties": {
                "enabled": {"type": "boolean"},
                "health_check_interval": {"type": "integer", "minimum": 10},
                "timeout": {"type": "integer", "minimum": 5},
                "retry_attempts": {"type": "integer", "minimum": 0, "maximum": 10},
                "circuit_breaker_enabled": {"type": "boolean"},
                "rate_limit": {"type": "integer", "minimum": 1},
                "priority": {"type": "string", "enum": ["low", "medium", "high", "critical"]}
            }
        },
        "alert_rule": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "minLength": 1},
                "severity": {"type": "string", "enum": ["low", "medium", "high", "critical"]},
                "conditions": {"type": "object"},
                "channels": {"type": "array", "items": {"type": "string"}},
                "cooldown_minutes": {"type": "integer", "minimum": 0},
                "escalation_minutes": {"type": "integer", "minimum": 0}
            },
            "required": ["name", "severity", "conditions", "channels"]
        },
        "threshold": {
            "type": "object",
            "properties": {
                "warning": {"type": "number"},
                "critical": {"type": "number"},
                "unit": {"type": "string"}
            }
        }
    }
    
    return {
        "success": True,
        "data": schema
    }