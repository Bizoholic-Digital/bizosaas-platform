"""
Configuration settings for Integration Monitor service
"""

import os
from typing import List
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application settings"""
    
    # Service Configuration
    SERVICE_NAME: str = "integration-monitor"
    SERVICE_HOST: str = "0.0.0.0"
    SERVICE_PORT: int = 8003
    DEBUG: bool = False
    
    # Database Configuration
    DATABASE_URL: str = Field(
        default="postgresql://bizosaas_user:secure_password@localhost:5432/bizosaas_integration_monitor",
        env="DATABASE_URL"
    )
    
    # Redis Configuration
    REDIS_URL: str = Field(
        default="redis://localhost:6379/3",
        env="REDIS_URL"
    )
    
    # Security
    SECRET_KEY: str = Field(
        default="integration-monitor-secret-key-change-in-production",
        env="SECRET_KEY"
    )
    
    # CORS Settings
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8001",
        "http://localhost:8002",
        "http://localhost:8003",
        "https://bizosaas.com",
        "https://app.bizosaas.com"
    ]
    
    # Monitoring Configuration
    MONITOR_INTERVAL: int = 30  # seconds
    HEALTH_CHECK_TIMEOUT: int = 10  # seconds
    FAILOVER_THRESHOLD: int = 3  # consecutive failures
    RATE_LIMIT_WINDOW: int = 60  # seconds
    
    # Alert Configuration
    ALERT_COOLDOWN: int = 300  # 5 minutes between similar alerts
    CRITICAL_ALERT_ESCALATION: int = 900  # 15 minutes
    
    # External Service URLs
    BIZOSAAS_BRAIN_URL: str = "http://localhost:8001"
    VAULT_URL: str = "http://localhost:8200"
    
    # Webhook URLs for alerts
    SLACK_WEBHOOK_URL: str = Field(default="", env="SLACK_WEBHOOK_URL")
    DISCORD_WEBHOOK_URL: str = Field(default="", env="DISCORD_WEBHOOK_URL")
    
    # Email Configuration
    SMTP_HOST: str = Field(default="smtp.resend.com", env="SMTP_HOST")
    SMTP_PORT: int = Field(default=587, env="SMTP_PORT")
    SMTP_USERNAME: str = Field(default="", env="SMTP_USERNAME")
    SMTP_PASSWORD: str = Field(default="", env="SMTP_PASSWORD")
    ALERT_EMAIL_FROM: str = Field(default="alerts@bizosaas.com", env="ALERT_EMAIL_FROM")
    ALERT_EMAIL_TO: List[str] = Field(default=["ops@bizosaas.com"], env="ALERT_EMAIL_TO")
    
    # SMS Configuration (for critical alerts)
    SMS_API_KEY: str = Field(default="", env="SMS_API_KEY")
    SMS_API_URL: str = Field(default="", env="SMS_API_URL")
    ONCALL_PHONE_NUMBERS: List[str] = Field(default=[], env="ONCALL_PHONE_NUMBERS")
    
    # Performance Thresholds
    RESPONSE_TIME_WARNING: float = 2.0  # seconds
    RESPONSE_TIME_CRITICAL: float = 5.0  # seconds
    ERROR_RATE_WARNING: float = 0.02  # 2%
    ERROR_RATE_CRITICAL: float = 0.05  # 5%
    UPTIME_TARGET: float = 0.999  # 99.9%
    
    # Cost Monitoring
    COST_ALERT_THRESHOLD: float = 1000.0  # USD per month
    COST_WARNING_THRESHOLD: float = 800.0  # USD per month
    
    # Integration Categories
    PAYMENT_INTEGRATIONS: List[str] = [
        "stripe", "paypal", "razorpay", "payu", "ccavenue"
    ]
    
    MARKETING_INTEGRATIONS: List[str] = [
        "google_ads", "facebook_ads", "linkedin_marketing", 
        "tiktok_ads", "twitter_ads", "pinterest_ads"
    ]
    
    COMMUNICATION_INTEGRATIONS: List[str] = [
        "resend_smtp", "twilio_sms", "whatsapp_business",
        "sendgrid", "mailchimp", "constant_contact"
    ]
    
    ECOMMERCE_INTEGRATIONS: List[str] = [
        "saleor_graphql", "amazon_sp_api", "shopify",
        "woocommerce", "magento", "bigcommerce"
    ]
    
    ANALYTICS_INTEGRATIONS: List[str] = [
        "google_analytics", "facebook_pixel", "linkedin_insights",
        "hotjar", "mixpanel", "amplitude"
    ]
    
    INFRASTRUCTURE_INTEGRATIONS: List[str] = [
        "aws_s3", "cloudflare", "digitalocean_spaces",
        "google_cloud_storage", "azure_blob"
    ]
    
    AI_INTEGRATIONS: List[str] = [
        "openai", "anthropic", "synthesia", "midjourney",
        "stability_ai", "cohere", "huggingface"
    ]
    
    # Failover Configuration
    FAILOVER_STRATEGIES: dict = {
        "payment": "primary_secondary",  # Critical - immediate failover
        "marketing": "load_balancing",   # Distribute load
        "communication": "circuit_breaker",  # Temporary isolation
        "ecommerce": "graceful_degradation",  # Fallback to essentials
        "analytics": "smart_routing",    # Route based on health
        "infrastructure": "primary_secondary",  # Critical - immediate failover
        "ai": "load_balancing"           # Distribute AI workload
    }
    
    # Circuit Breaker Configuration
    CIRCUIT_BREAKER_FAILURE_THRESHOLD: int = 5
    CIRCUIT_BREAKER_TIMEOUT: int = 60  # seconds
    CIRCUIT_BREAKER_RECOVERY_THRESHOLD: int = 3
    
    # Load Balancing Configuration
    LOAD_BALANCER_ALGORITHM: str = "weighted_round_robin"
    HEALTH_SCORE_WEIGHT: float = 0.7
    RESPONSE_TIME_WEIGHT: float = 0.3
    
    # API Rate Limiting
    DEFAULT_RATE_LIMIT: int = 1000  # requests per minute
    PREMIUM_RATE_LIMIT: int = 5000  # requests per minute
    BURST_LIMIT: int = 100  # requests per second
    
    # Metrics Collection
    METRICS_RETENTION_DAYS: int = 90
    DETAILED_METRICS_RETENTION_DAYS: int = 7
    AGGREGATION_INTERVALS: List[int] = [60, 300, 900, 3600]  # 1m, 5m, 15m, 1h
    
    # Dashboard Configuration
    DASHBOARD_REFRESH_INTERVAL: int = 5  # seconds
    DASHBOARD_AUTO_REFRESH: bool = True
    MAX_WEBSOCKET_CONNECTIONS: int = 100
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE: str = "integration_monitor.log"
    LOG_ROTATION: str = "daily"
    LOG_RETENTION: int = 30  # days
    
    # Security Configuration
    API_KEY_EXPIRY_DAYS: int = 90
    MAX_LOGIN_ATTEMPTS: int = 5
    LOGIN_LOCKOUT_DURATION: int = 900  # 15 minutes
    
    # Cache Configuration
    CACHE_TTL: int = 300  # 5 minutes
    HEALTH_STATUS_CACHE_TTL: int = 30  # 30 seconds
    METRICS_CACHE_TTL: int = 60  # 1 minute
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()


def get_integration_config(integration_name: str) -> dict:
    """Get configuration for specific integration"""
    
    # Default configuration template
    default_config = {
        "enabled": True,
        "health_check_interval": settings.MONITOR_INTERVAL,
        "timeout": settings.HEALTH_CHECK_TIMEOUT,
        "retry_attempts": 3,
        "retry_delay": 1,
        "circuit_breaker_enabled": True,
        "rate_limit": settings.DEFAULT_RATE_LIMIT,
        "cost_tracking": True,
        "alert_on_failure": True,
        "alert_on_degradation": True,
        "priority": "medium"
    }
    
    # Integration-specific overrides
    integration_configs = {
        # Payment Gateways - Critical Priority
        "stripe": {
            **default_config,
            "priority": "critical",
            "health_check_interval": 15,
            "timeout": 5,
            "failover_strategy": "primary_secondary",
            "sla_target": 0.9995,  # 99.95%
        },
        "paypal": {
            **default_config,
            "priority": "critical",
            "health_check_interval": 15,
            "failover_strategy": "primary_secondary",
            "sla_target": 0.999,
        },
        "razorpay": {
            **default_config,
            "priority": "high",
            "failover_strategy": "primary_secondary",
            "sla_target": 0.999,
        },
        
        # Marketing Platforms - High Priority
        "google_ads": {
            **default_config,
            "priority": "high",
            "rate_limit": 10000,  # Higher for Google
            "cost_tracking": True,
            "failover_strategy": "smart_routing",
            "sla_target": 0.995,
        },
        "facebook_ads": {
            **default_config,
            "priority": "high",
            "rate_limit": 5000,
            "failover_strategy": "smart_routing",
            "sla_target": 0.995,
        },
        
        # AI Services - Medium Priority
        "openai": {
            **default_config,
            "priority": "medium",
            "timeout": 30,  # AI calls can be slower
            "rate_limit": 3000,
            "cost_tracking": True,
            "failover_strategy": "load_balancing",
            "sla_target": 0.99,
        },
        "anthropic": {
            **default_config,
            "priority": "medium",
            "timeout": 30,
            "failover_strategy": "load_balancing",
            "sla_target": 0.99,
        },
        
        # Infrastructure - Critical Priority
        "aws_s3": {
            **default_config,
            "priority": "critical",
            "health_check_interval": 10,
            "failover_strategy": "primary_secondary",
            "sla_target": 0.9999,  # 99.99%
        },
        "cloudflare": {
            **default_config,
            "priority": "critical",
            "health_check_interval": 10,
            "failover_strategy": "smart_routing",
            "sla_target": 0.9999,
        },
    }
    
    return integration_configs.get(integration_name, default_config)


def get_alert_escalation_rules() -> dict:
    """Get alert escalation rules based on severity"""
    return {
        "low": {
            "channels": ["email"],
            "delay": 0,
            "escalation_time": None
        },
        "medium": {
            "channels": ["email", "slack"],
            "delay": 0,
            "escalation_time": 1800  # 30 minutes
        },
        "high": {
            "channels": ["email", "slack", "discord"],
            "delay": 0,
            "escalation_time": 600  # 10 minutes
        },
        "critical": {
            "channels": ["email", "slack", "discord", "sms"],
            "delay": 0,
            "escalation_time": 300  # 5 minutes
        }
    }