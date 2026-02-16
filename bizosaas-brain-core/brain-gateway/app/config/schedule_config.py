"""
Schedule configuration for analytics workflows.

Defines schedule intervals, retention policies, and default settings
for automated analytics aggregation.
"""

from datetime import timedelta
from typing import Dict, Any
from pydantic_settings import BaseSettings
from pydantic import Field


class ScheduleConfig(BaseSettings):
    """Configuration for analytics schedules."""
    
    # Schedule enablement
    analytics_schedule_hourly: bool = Field(
        default=True,
        description="Enable hourly analytics aggregation"
    )
    analytics_schedule_daily: bool = Field(
        default=True,
        description="Enable daily analytics aggregation"
    )
    analytics_schedule_weekly: bool = Field(
        default=True,
        description="Enable weekly analytics aggregation"
    )
    
    # Schedule timing (cron expressions)
    analytics_hourly_cron: str = Field(
        default="0 * * * *",  # Every hour at :00
        description="Cron expression for hourly analytics"
    )
    analytics_daily_cron: str = Field(
        default="0 2 * * *",  # Daily at 2:00 AM
        description="Cron expression for daily analytics"
    )
    analytics_weekly_cron: str = Field(
        default="0 3 * * 0",  # Sunday at 3:00 AM
        description="Cron expression for weekly analytics"
    )
    
    # Timezone
    analytics_timezone: str = Field(
        default="UTC",
        description="Timezone for schedule execution"
    )
    
    # Retention policies
    analytics_retention_days: int = Field(
        default=90,
        description="Days to retain analytics snapshots"
    )
    analytics_hourly_retention_days: int = Field(
        default=7,
        description="Days to retain hourly snapshots"
    )
    analytics_daily_retention_days: int = Field(
        default=30,
        description="Days to retain daily snapshots"
    )
    analytics_weekly_retention_days: int = Field(
        default=90,
        description="Days to retain weekly snapshots"
    )
    
    # Workflow parameters
    analytics_hourly_time_range: int = Field(
        default=1,
        description="Hours to analyze for hourly snapshots"
    )
    analytics_daily_time_range: int = Field(
        default=24,
        description="Hours to analyze for daily snapshots"
    )
    analytics_weekly_time_range: int = Field(
        default=168,  # 7 days
        description="Hours to analyze for weekly snapshots"
    )
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global schedule configuration instance
schedule_config = ScheduleConfig()


def get_schedule_specs() -> Dict[str, Dict[str, Any]]:
    """
    Get schedule specifications for all analytics schedules.
    
    Returns:
        Dictionary mapping schedule IDs to their specifications
    """
    specs = {}
    
    if schedule_config.analytics_schedule_hourly:
        specs["analytics-hourly"] = {
            "schedule_id": "analytics-hourly",
            "cron": schedule_config.analytics_hourly_cron,
            "timezone": schedule_config.analytics_timezone,
            "snapshot_type": "hourly",
            "time_range_hours": schedule_config.analytics_hourly_time_range,
            "retention_days": schedule_config.analytics_hourly_retention_days,
            "description": "Hourly platform analytics aggregation"
        }
    
    if schedule_config.analytics_schedule_daily:
        specs["analytics-daily"] = {
            "schedule_id": "analytics-daily",
            "cron": schedule_config.analytics_daily_cron,
            "timezone": schedule_config.analytics_timezone,
            "snapshot_type": "daily",
            "time_range_hours": schedule_config.analytics_daily_time_range,
            "retention_days": schedule_config.analytics_daily_retention_days,
            "description": "Daily platform analytics aggregation"
        }
    
    if schedule_config.analytics_schedule_weekly:
        specs["analytics-weekly"] = {
            "schedule_id": "analytics-weekly",
            "cron": schedule_config.analytics_weekly_cron,
            "timezone": schedule_config.analytics_timezone,
            "snapshot_type": "weekly",
            "time_range_hours": schedule_config.analytics_weekly_time_range,
            "retention_days": schedule_config.analytics_weekly_retention_days,
            "description": "Weekly platform analytics aggregation"
        }
    
    return specs


def get_retention_cutoff(snapshot_type: str) -> timedelta:
    """
    Get retention cutoff timedelta for a snapshot type.
    
    Args:
        snapshot_type: Type of snapshot (hourly, daily, weekly)
        
    Returns:
        Timedelta representing retention period
    """
    retention_map = {
        "hourly": timedelta(days=schedule_config.analytics_hourly_retention_days),
        "daily": timedelta(days=schedule_config.analytics_daily_retention_days),
        "weekly": timedelta(days=schedule_config.analytics_weekly_retention_days)
    }
    
    return retention_map.get(snapshot_type, timedelta(days=schedule_config.analytics_retention_days))
