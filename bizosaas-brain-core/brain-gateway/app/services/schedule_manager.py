"""
Temporal schedule management service.

Handles creation, updating, deletion, and lifecycle management
of Temporal schedules for analytics workflows.
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone, timedelta

from temporalio.client import Client, Schedule, ScheduleActionStartWorkflow, ScheduleSpec, ScheduleIntervalSpec, ScheduleCalendarSpec
from temporalio.common import RetryPolicy

from app.workflows.analytics_workflow import PlatformAnalyticsWorkflow
from app.config.schedule_config import get_schedule_specs

logger = logging.getLogger(__name__)


class ScheduleManager:
    """Manages Temporal schedules for analytics workflows."""
    
    def __init__(self, temporal_client: Client):
        """
        Initialize schedule manager.
        
        Args:
            temporal_client: Connected Temporal client
        """
        self.client = temporal_client
    
    async def create_analytics_schedule(
        self,
        schedule_id: str,
        cron: str,
        snapshot_type: str,
        time_range_hours: int,
        timezone_str: str = "UTC",
        description: str = ""
    ) -> None:
        """
        Create a Temporal schedule for analytics workflow.
        
        Args:
            schedule_id: Unique identifier for the schedule
            cron: Cron expression for schedule timing
            snapshot_type: Type of snapshot (hourly, daily, weekly)
            time_range_hours: Hours to analyze in each run
            timezone_str: Timezone for schedule execution
            description: Human-readable description
        """
        try:
            # Check if schedule already exists
            try:
                handle = self.client.get_schedule_handle(schedule_id)
                await handle.describe()
                logger.info(f"Schedule {schedule_id} already exists, skipping creation")
                return
            except Exception:
                # Schedule doesn't exist, proceed with creation
                pass
            
            # Create schedule spec with cron expression
            schedule_spec = ScheduleSpec(
                calendars=[
                    ScheduleCalendarSpec(
                        comment=description or f"{snapshot_type} analytics aggregation",
                        # Parse cron expression
                        # Format: minute hour day_of_month month day_of_week
                        **self._parse_cron(cron)
                    )
                ],
                time_zone_name=timezone_str
            )
            
            # Create workflow action
            action = ScheduleActionStartWorkflow(
                PlatformAnalyticsWorkflow.run,
                args=[snapshot_type, time_range_hours],
                id=f"{schedule_id}-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}",
                task_queue="default",
                retry_policy=RetryPolicy(
                    maximum_attempts=3,
                    initial_interval=timedelta(seconds=1),
                    maximum_interval=timedelta(seconds=10)
                )
            )
            
            # Create the schedule
            await self.client.create_schedule(
                schedule_id,
                Schedule(
                    action=action,
                    spec=schedule_spec,
                    state=None  # Default to running
                )
            )
            
            logger.info(f"Created schedule {schedule_id} with cron '{cron}'")
            
        except Exception as e:
            logger.error(f"Failed to create schedule {schedule_id}: {e}")
            raise
    
    async def initialize_default_schedules(self) -> None:
        """
        Initialize default analytics schedules based on configuration.
        
        Creates hourly, daily, and weekly schedules if enabled.
        """
        schedule_specs = get_schedule_specs()
        
        for schedule_id, spec in schedule_specs.items():
            try:
                await self.create_analytics_schedule(
                    schedule_id=spec["schedule_id"],
                    cron=spec["cron"],
                    snapshot_type=spec["snapshot_type"],
                    time_range_hours=spec["time_range_hours"],
                    timezone_str=spec["timezone"],
                    description=spec["description"]
                )
            except Exception as e:
                logger.error(f"Failed to initialize schedule {schedule_id}: {e}")
    
    async def list_schedules(self) -> List[Dict[str, Any]]:
        """
        List all analytics schedules.
        
        Returns:
            List of schedule information dictionaries
        """
        schedules = []
        
        try:
            async for schedule in self.client.list_schedules():
                # Filter for analytics schedules
                if schedule.id.startswith("analytics-"):
                    desc = await self.client.get_schedule_handle(schedule.id).describe()
                    
                    schedules.append({
                        "schedule_id": schedule.id,
                        "state": "running" if not desc.schedule.state.paused else "paused",
                        "next_run": desc.info.next_action_times[0] if desc.info.next_action_times else None,
                        "last_run": desc.info.recent_actions[0].actual_time if desc.info.recent_actions else None,
                        "spec": str(desc.schedule.spec)
                    })
        except Exception as e:
            logger.error(f"Failed to list schedules: {e}")
            raise
        
        return schedules
    
    async def pause_schedule(self, schedule_id: str, note: str = "") -> None:
        """
        Pause a schedule.
        
        Args:
            schedule_id: Schedule to pause
            note: Optional note explaining why schedule was paused
        """
        try:
            handle = self.client.get_schedule_handle(schedule_id)
            await handle.pause(note=note)
            logger.info(f"Paused schedule {schedule_id}")
        except Exception as e:
            logger.error(f"Failed to pause schedule {schedule_id}: {e}")
            raise
    
    async def resume_schedule(self, schedule_id: str, note: str = "") -> None:
        """
        Resume a paused schedule.
        
        Args:
            schedule_id: Schedule to resume
            note: Optional note explaining why schedule was resumed
        """
        try:
            handle = self.client.get_schedule_handle(schedule_id)
            await handle.unpause(note=note)
            logger.info(f"Resumed schedule {schedule_id}")
        except Exception as e:
            logger.error(f"Failed to resume schedule {schedule_id}: {e}")
            raise
    
    async def delete_schedule(self, schedule_id: str) -> None:
        """
        Delete a schedule.
        
        Args:
            schedule_id: Schedule to delete
        """
        try:
            handle = self.client.get_schedule_handle(schedule_id)
            await handle.delete()
            logger.info(f"Deleted schedule {schedule_id}")
        except Exception as e:
            logger.error(f"Failed to delete schedule {schedule_id}: {e}")
            raise
    
    async def trigger_schedule(self, schedule_id: str) -> None:
        """
        Manually trigger a schedule to run immediately.
        
        Args:
            schedule_id: Schedule to trigger
        """
        try:
            handle = self.client.get_schedule_handle(schedule_id)
            await handle.trigger()
            logger.info(f"Triggered schedule {schedule_id}")
        except Exception as e:
            logger.error(f"Failed to trigger schedule {schedule_id}: {e}")
            raise
    
    def _parse_cron(self, cron: str) -> Dict[str, Any]:
        """
        Parse cron expression into ScheduleCalendarSpec parameters.
        
        Args:
            cron: Cron expression (minute hour day month day_of_week)
            
        Returns:
            Dictionary of calendar spec parameters
        """
        parts = cron.split()
        if len(parts) != 5:
            raise ValueError(f"Invalid cron expression: {cron}")
        
        minute, hour, day, month, day_of_week = parts
        
        spec = {}
        
        # Parse minute
        if minute != "*":
            spec["minute"] = [int(m) for m in minute.split(",")] if "," in minute else [int(minute)]
        
        # Parse hour
        if hour != "*":
            spec["hour"] = [int(h) for h in hour.split(",")] if "," in hour else [int(hour)]
        
        # Parse day of month
        if day != "*":
            spec["day_of_month"] = [int(d) for d in day.split(",")] if "," in day else [int(day)]
        
        # Parse month
        if month != "*":
            spec["month"] = [int(m) for m in month.split(",")] if "," in month else [int(month)]
        
        # Parse day of week (0 = Sunday in cron, but Temporal uses 1 = Monday)
        if day_of_week != "*":
            dow_values = [int(d) for d in day_of_week.split(",")] if "," in day_of_week else [int(day_of_week)]
            # Convert from cron (0=Sunday) to Temporal (0=Monday, 6=Sunday)
            spec["day_of_week"] = [(d + 6) % 7 if d != 0 else 6 for d in dow_values]
        
        return spec


async def get_schedule_manager(temporal_client: Client) -> ScheduleManager:
    """
    Get a schedule manager instance.
    
    Args:
        temporal_client: Connected Temporal client
        
    Returns:
        ScheduleManager instance
    """
    return ScheduleManager(temporal_client)
