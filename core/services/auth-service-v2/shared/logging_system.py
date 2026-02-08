"""
Centralized Logging System for BizOSaas Platform
Provides structured logging, monitoring integration, and audit trails
"""

import asyncio
import json
import logging
import sys
import traceback
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from contextlib import asynccontextmanager
import aiofiles
import redis
from pydantic import BaseModel

# Import our existing systems
from .agent_monitor import get_agent_monitor, AgentActivityMonitor
from .vault_client import VaultClient

class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO" 
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    AUDIT = "AUDIT"

class LogCategory(str, Enum):
    SYSTEM = "system"
    AGENT = "agent"
    API = "api"
    DATABASE = "database"
    AUTHENTICATION = "auth"
    PAYMENT = "payment"
    INTEGRATION = "integration"
    SECURITY = "security"
    PERFORMANCE = "performance"
    USER_ACTION = "user_action"
    WORKFLOW = "workflow"

@dataclass
class LogEntry:
    timestamp: str
    level: LogLevel
    category: LogCategory
    service: str
    message: str
    details: Optional[Dict[str, Any]] = None
    user_id: Optional[str] = None
    tenant_id: Optional[str] = None
    session_id: Optional[str] = None
    trace_id: Optional[str] = None
    correlation_id: Optional[str] = None
    error_details: Optional[Dict[str, Any]] = None
    performance_metrics: Optional[Dict[str, Any]] = None

class LogConfig(BaseModel):
    log_level: LogLevel = LogLevel.INFO
    enable_console: bool = True
    enable_file: bool = True
    enable_redis: bool = True
    file_path: str = "/home/alagiri/projects/bizoholic/bizosaas/logs/"
    redis_key_prefix: str = "bizosaas:logs"
    max_log_size_mb: int = 100
    retention_days: int = 30
    enable_audit_trail: bool = True
    enable_performance_logging: bool = True
    structured_format: bool = True

class CentralizedLogger:
    def __init__(self, config: LogConfig = None):
        self.config = config or LogConfig()
        self.redis_client: Optional[redis.Redis] = None
        self.agent_monitor: Optional[AgentActivityMonitor] = None
        self.vault_client = VaultClient()
        self._setup_logging()
        
    async def initialize(self):
        """Initialize connections to Redis and agent monitor"""
        try:
            # Get Redis connection
            redis_url = self.vault_client.get_redis_url()
            self.redis_client = redis.from_url(redis_url, decode_responses=True)
            
            # Connect to agent monitor
            self.agent_monitor = get_agent_monitor()
            
            # Create log directory
            Path(self.config.file_path).mkdir(parents=True, exist_ok=True)
            
            await self.log(LogLevel.INFO, LogCategory.SYSTEM, "centralized-logger", 
                         "Centralized logging system initialized successfully")
            
        except Exception as e:
            print(f"Failed to initialize centralized logger: {e}")
            raise

    def _setup_logging(self):
        """Setup Python logging configuration"""
        # Create custom formatter for structured logs
        class StructuredFormatter(logging.Formatter):
            def format(self, record):
                log_data = {
                    'timestamp': datetime.now(timezone.utc).isoformat(),
                    'level': record.levelname,
                    'category': getattr(record, 'category', 'system'),
                    'service': getattr(record, 'service', 'unknown'),
                    'message': record.getMessage(),
                    'logger': record.name,
                    'module': record.module,
                    'function': record.funcName,
                    'line': record.lineno
                }
                
                if record.exc_info:
                    log_data['error_details'] = {
                        'exception_type': record.exc_info[0].__name__,
                        'exception_message': str(record.exc_info[1]),
                        'traceback': traceback.format_exception(*record.exc_info)
                    }
                
                return json.dumps(log_data, default=str)
        
        # Configure root logger
        logger = logging.getLogger()
        logger.setLevel(getattr(logging, self.config.log_level.value))
        
        # Remove existing handlers
        logger.handlers.clear()
        
        if self.config.enable_console:
            console_handler = logging.StreamHandler(sys.stdout)
            if self.config.structured_format:
                console_handler.setFormatter(StructuredFormatter())
            else:
                console_handler.setFormatter(
                    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                )
            logger.addHandler(console_handler)

    async def log(self, 
                  level: LogLevel, 
                  category: LogCategory, 
                  service: str, 
                  message: str,
                  details: Optional[Dict[str, Any]] = None,
                  user_id: Optional[str] = None,
                  tenant_id: Optional[str] = None,
                  session_id: Optional[str] = None,
                  trace_id: Optional[str] = None,
                  error: Optional[Exception] = None,
                  performance_metrics: Optional[Dict[str, Any]] = None):
        """Log a message with full context"""
        
        # Create log entry
        log_entry = LogEntry(
            timestamp=datetime.now(timezone.utc).isoformat(),
            level=level,
            category=category,
            service=service,
            message=message,
            details=details,
            user_id=user_id,
            tenant_id=tenant_id,
            session_id=session_id,
            trace_id=trace_id,
            performance_metrics=performance_metrics
        )
        
        # Add error details if provided
        if error:
            log_entry.error_details = {
                'exception_type': type(error).__name__,
                'exception_message': str(error),
                'traceback': traceback.format_exc()
            }
        
        # Convert to dict for serialization
        log_dict = asdict(log_entry)
        
        try:
            # Log to console/file through Python logging
            python_logger = logging.getLogger(service)
            python_level = getattr(logging, level.value)
            python_logger.log(python_level, message, extra={
                'category': category.value,
                'service': service,
                'details': details
            })
            
            # Store in Redis for real-time monitoring
            if self.config.enable_redis and self.redis_client:
                await self._store_in_redis(log_dict)
            
            # Write to file for persistence
            if self.config.enable_file:
                await self._write_to_file(log_dict)
            
            # Send to agent monitor for dashboard integration
            if self.agent_monitor and category == LogCategory.AGENT:
                await self._integrate_with_agent_monitor(log_dict)
                
        except Exception as e:
            # Fallback logging to prevent loss of critical logs
            print(f"Failed to log message: {e}")
            print(f"Original message: {message}")

    async def _store_in_redis(self, log_dict: Dict[str, Any]):
        """Store log entry in Redis for real-time access"""
        try:
            # Store in time-series list
            key = f"{self.config.redis_key_prefix}:{log_dict['category']}:{log_dict['service']}"
            pipe = self.redis_client.pipeline()
            
            # Add log entry
            pipe.lpush(key, json.dumps(log_dict, default=str))
            
            # Keep only recent entries (last 1000)
            pipe.ltrim(key, 0, 999)
            
            # Set expiration
            pipe.expire(key, self.config.retention_days * 24 * 3600)
            
            pipe.execute()
            
            # Also store in global recent logs
            global_key = f"{self.config.redis_key_prefix}:recent"
            pipe = self.redis_client.pipeline()
            pipe.lpush(global_key, json.dumps(log_dict, default=str))
            pipe.ltrim(global_key, 0, 9999)  # Keep last 10k logs
            pipe.expire(global_key, 7 * 24 * 3600)  # 7 days
            pipe.execute()
            
        except Exception as e:
            print(f"Failed to store log in Redis: {e}")

    async def _write_to_file(self, log_dict: Dict[str, Any]):
        """Write log entry to file"""
        try:
            # Create filename based on date and category
            date_str = datetime.now().strftime("%Y-%m-%d")
            filename = f"{log_dict['category']}_{date_str}.log"
            filepath = Path(self.config.file_path) / filename
            
            # Write log entry
            async with aiofiles.open(filepath, 'a', encoding='utf-8') as f:
                await f.write(json.dumps(log_dict, default=str) + '\n')
                
        except Exception as e:
            print(f"Failed to write log to file: {e}")

    async def _integrate_with_agent_monitor(self, log_dict: Dict[str, Any]):
        """Integrate agent logs with monitoring system"""
        try:
            if not self.agent_monitor:
                return
                
            # Extract relevant information for monitoring
            service = log_dict.get('service')
            level = log_dict.get('level')
            message = log_dict.get('message')
            
            # Update agent monitor statistics
            if level in ['ERROR', 'CRITICAL']:
                # Log error event
                await self.agent_monitor.log_error_event(
                    service=service,
                    error_message=message,
                    error_details=log_dict.get('error_details'),
                    timestamp=log_dict['timestamp']
                )
            
            # Update performance metrics if available
            if log_dict.get('performance_metrics'):
                await self.agent_monitor.update_performance_metrics(
                    service=service,
                    metrics=log_dict['performance_metrics']
                )
                
        except Exception as e:
            print(f"Failed to integrate with agent monitor: {e}")

    async def get_recent_logs(self, 
                            category: Optional[LogCategory] = None,
                            service: Optional[str] = None,
                            level: Optional[LogLevel] = None,
                            limit: int = 100) -> List[Dict[str, Any]]:
        """Retrieve recent logs with filtering"""
        try:
            if not self.redis_client:
                return []
            
            # Build Redis key
            if category and service:
                key = f"{self.config.redis_key_prefix}:{category.value}:{service}"
            elif category:
                key = f"{self.config.redis_key_prefix}:{category.value}"
            else:
                key = f"{self.config.redis_key_prefix}:recent"
            
            # Get logs from Redis
            logs_data = self.redis_client.lrange(key, 0, limit - 1)
            logs = [json.loads(log_data) for log_data in logs_data]
            
            # Filter by level if specified
            if level:
                logs = [log for log in logs if log.get('level') == level.value]
            
            return logs
            
        except Exception as e:
            print(f"Failed to retrieve recent logs: {e}")
            return []

    async def get_log_statistics(self) -> Dict[str, Any]:
        """Get logging statistics for dashboard"""
        try:
            stats = {
                'total_logs_today': 0,
                'error_count_today': 0,
                'warning_count_today': 0,
                'categories': {},
                'services': {},
                'top_errors': []
            }
            
            if not self.redis_client:
                return stats
            
            # Get recent logs for analysis
            logs = await self.get_recent_logs(limit=10000)
            today = datetime.now().date()
            
            for log in logs:
                log_date = datetime.fromisoformat(log['timestamp'].replace('Z', '+00:00')).date()
                if log_date != today:
                    continue
                
                stats['total_logs_today'] += 1
                
                # Count by level
                if log['level'] == 'ERROR':
                    stats['error_count_today'] += 1
                elif log['level'] == 'WARNING':
                    stats['warning_count_today'] += 1
                
                # Count by category
                category = log.get('category', 'unknown')
                stats['categories'][category] = stats['categories'].get(category, 0) + 1
                
                # Count by service
                service = log.get('service', 'unknown')
                stats['services'][service] = stats['services'].get(service, 0) + 1
            
            return stats
            
        except Exception as e:
            print(f"Failed to get log statistics: {e}")
            return {}

    @asynccontextmanager
    async def performance_context(self, 
                                service: str, 
                                operation: str, 
                                tenant_id: Optional[str] = None,
                                user_id: Optional[str] = None):
        """Context manager for performance logging"""
        start_time = datetime.now(timezone.utc)
        
        try:
            yield
            
        except Exception as e:
            # Log the error with performance metrics
            end_time = datetime.now(timezone.utc)
            duration = (end_time - start_time).total_seconds()
            
            await self.log(
                level=LogLevel.ERROR,
                category=LogCategory.PERFORMANCE,
                service=service,
                message=f"Operation '{operation}' failed",
                performance_metrics={
                    'operation': operation,
                    'duration_seconds': duration,
                    'success': False
                },
                tenant_id=tenant_id,
                user_id=user_id,
                error=e
            )
            raise
            
        else:
            # Log successful operation
            end_time = datetime.now(timezone.utc)
            duration = (end_time - start_time).total_seconds()
            
            if self.config.enable_performance_logging:
                await self.log(
                    level=LogLevel.INFO,
                    category=LogCategory.PERFORMANCE,
                    service=service,
                    message=f"Operation '{operation}' completed successfully",
                    performance_metrics={
                        'operation': operation,
                        'duration_seconds': duration,
                        'success': True
                    },
                    tenant_id=tenant_id,
                    user_id=user_id
                )

    async def audit_log(self, 
                       user_id: str, 
                       action: str, 
                       resource: str, 
                       tenant_id: Optional[str] = None,
                       details: Optional[Dict[str, Any]] = None,
                       ip_address: Optional[str] = None):
        """Log audit trail for security and compliance"""
        await self.log(
            level=LogLevel.AUDIT,
            category=LogCategory.SECURITY,
            service="audit-trail",
            message=f"User {user_id} performed {action} on {resource}",
            details={
                'action': action,
                'resource': resource,
                'ip_address': ip_address,
                **(details or {})
            },
            user_id=user_id,
            tenant_id=tenant_id
        )

# Global logger instance
_logger_instance: Optional[CentralizedLogger] = None

def get_logger() -> CentralizedLogger:
    """Get global logger instance"""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = CentralizedLogger()
    return _logger_instance

async def init_logging_system():
    """Initialize the global logging system"""
    logger = get_logger()
    await logger.initialize()
    return logger

# Convenience functions for common logging patterns
async def log_info(service: str, message: str, **kwargs):
    logger = get_logger()
    await logger.log(LogLevel.INFO, LogCategory.SYSTEM, service, message, **kwargs)

async def log_error(service: str, message: str, error: Exception = None, **kwargs):
    logger = get_logger()
    await logger.log(LogLevel.ERROR, LogCategory.SYSTEM, service, message, error=error, **kwargs)

async def log_agent_activity(agent_name: str, activity: str, **kwargs):
    logger = get_logger()
    await logger.log(LogLevel.INFO, LogCategory.AGENT, agent_name, activity, **kwargs)

async def log_api_request(service: str, endpoint: str, method: str, status_code: int, 
                         duration: float, user_id: str = None, **kwargs):
    logger = get_logger()
    await logger.log(
        LogLevel.INFO, 
        LogCategory.API, 
        service, 
        f"{method} {endpoint} -> {status_code}",
        performance_metrics={
            'endpoint': endpoint,
            'method': method,
            'status_code': status_code,
            'duration_seconds': duration
        },
        user_id=user_id,
        **kwargs
    )