"""
Decorators for instrumenting connector operations with observability
"""

import time
import functools
import logging
from typing import Callable, Any
from app.observability.metrics import record_connector_operation, record_connector_sync

logger = logging.getLogger(__name__)


def instrument_connector_operation(operation_name: str = None):
    """
    Decorator to instrument connector operations with metrics and tracing.
    
    Usage:
        @instrument_connector_operation("fetch_posts")
        async def get_posts(self):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(self, *args, **kwargs) -> Any:
            # Get operation name from decorator or function name
            op_name = operation_name or func.__name__
            
            # Get connector info
            connector_type = getattr(self, 'config', None)
            connector_id = connector_type.id if connector_type else "unknown"
            tenant_id = getattr(self, 'tenant_id', 'unknown')
            
            # Start timing
            start_time = time.time()
            success = True
            result = None
            
            try:
                # Execute the function
                result = await func(self, *args, **kwargs)
                return result
            except Exception as e:
                success = False
                logger.error(f"Connector operation failed: {connector_id}.{op_name} - {str(e)}")
                raise
            finally:
                # Calculate duration
                duration_ms = (time.time() - start_time) * 1000
                
                # Record metrics
                try:
                    record_connector_operation(
                        connector_type=connector_id,
                        operation=op_name,
                        duration_ms=duration_ms,
                        success=success,
                        tenant_id=tenant_id
                    )
                except Exception as metric_error:
                    logger.warning(f"Failed to record connector metrics: {metric_error}")
        
        return wrapper
    return decorator


def instrument_sync_operation(resource_type: str = None):
    """
    Decorator specifically for sync operations that track record counts.
    
    Usage:
        @instrument_sync_operation("posts")
        async def sync_posts(self):
            ...
            return {"data": [...], "count": 10}
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(self, *args, **kwargs) -> Any:
            # Get connector info
            connector_type = getattr(self, 'config', None)
            connector_id = connector_type.id if connector_type else "unknown"
            tenant_id = getattr(self, 'tenant_id', 'unknown')
            
            # Determine resource type
            res_type = resource_type
            if not res_type and args:
                # Try to get from first argument
                res_type = args[0] if isinstance(args[0], str) else "unknown"
            if not res_type:
                res_type = func.__name__.replace('sync_', '').replace('get_', '')
            
            # Start timing
            start_time = time.time()
            success = True
            result = None
            record_count = 0
            
            try:
                # Execute the function
                result = await func(self, *args, **kwargs)
                
                # Try to extract record count from result
                if isinstance(result, dict):
                    if 'count' in result:
                        record_count = result['count']
                    elif 'data' in result and isinstance(result['data'], list):
                        record_count = len(result['data'])
                elif isinstance(result, list):
                    record_count = len(result)
                
                return result
            except Exception as e:
                success = False
                logger.error(f"Sync operation failed: {connector_id}.{res_type} - {str(e)}")
                raise
            finally:
                # Calculate duration
                duration_ms = (time.time() - start_time) * 1000
                
                # Record metrics
                try:
                    record_connector_operation(
                        connector_type=connector_id,
                        operation=f"sync_{res_type}",
                        duration_ms=duration_ms,
                        success=success,
                        tenant_id=tenant_id
                    )
                    
                    if success and record_count > 0:
                        record_connector_sync(
                            connector_type=connector_id,
                            resource_type=res_type,
                            record_count=record_count,
                            tenant_id=tenant_id
                        )
                except Exception as metric_error:
                    logger.warning(f"Failed to record sync metrics: {metric_error}")
        
        return wrapper
    return decorator
