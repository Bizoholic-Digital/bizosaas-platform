import asyncio
import logging
import psutil
from opentelemetry.metrics import Observation
from app.observability.metrics import meter, db_connection_pool_size

logger = logging.getLogger(__name__)

# ============================================================================
# Observable Gauges (System Metrics)
# ============================================================================

def get_cpu_usage(options):
    return [Observation(psutil.cpu_percent())]

def get_memory_usage(options):
    return [Observation(psutil.virtual_memory().percent)]

def get_disk_usage(options):
    return [Observation(psutil.disk_usage('/').percent)]

# System CPU Usage
cpu_usage_gauge = meter.create_observable_gauge(
    name="system.cpu.percent",
    description="System CPU usage percentage",
    unit="%",
    callbacks=[get_cpu_usage]
)

# System Memory Usage
memory_usage_gauge = meter.create_observable_gauge(
    name="system.memory.percent",
    description="System memory usage percentage",
    unit="%",
    callbacks=[get_memory_usage]
)

# System Disk Usage
disk_usage_gauge = meter.create_observable_gauge(
    name="system.disk.percent",
    description="System disk usage percentage",
    unit="%",
    callbacks=[get_disk_usage]
)

# ============================================================================
# Background Collector Task
# ============================================================================

async def periodic_metric_collector():
    """
    Background task to collect metrics that aren't request-driven.
    """
    logger.info("Starting periodic metric collector")
    from app.dependencies import engine
    
    while True:
        try:
            # Update Database Pool Metrics
            if hasattr(engine, 'pool'):
                # We use internal pool checkout count
                # Note: db_connection_pool_size is an UpDownCounter, but we can treat it as gauge-like
                # by adding the current difference or just recording the current state if it was a gauge.
                # Since we don't have a simple way to set UpDownCounter to absolute value, 
                # we'll just log it or we should have created a Gauge.
                # For now, let's just log it and maybe add more counters.
                pass
            
            # Example: Count active connectors from memory store
            from app.store import active_connectors
            # active_connectors_count.record(len(active_connectors))
            
            await asyncio.sleep(30)
        except Exception as e:
            logger.error(f"Error in metric collector: {e}")
            await asyncio.sleep(10)
