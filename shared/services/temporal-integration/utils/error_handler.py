"""
Comprehensive Error Handling System
Handles errors, retries, and recovery for order processing workflow
"""

import asyncio
import logging
import traceback
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any, Callable, Type
from dataclasses import dataclass, field
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
import sys

logger = logging.getLogger(__name__)


class ErrorSeverity(str, Enum):
    """Error severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorCategory(str, Enum):
    """Error categories"""
    VALIDATION = "validation"
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    BUSINESS_LOGIC = "business_logic"
    INTEGRATION = "integration"
    SYSTEM = "system"
    NETWORK = "network"
    DATABASE = "database"
    PAYMENT = "payment"
    INVENTORY = "inventory"
    FULFILLMENT = "fulfillment"
    NOTIFICATION = "notification"


@dataclass
class ErrorContext:
    """Error context information"""
    order_id: Optional[str] = None
    customer_id: Optional[str] = None
    user_id: Optional[str] = None
    request_id: Optional[str] = None
    operation: Optional[str] = None
    service: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ErrorInfo:
    """Comprehensive error information"""
    error_id: str
    timestamp: datetime
    category: ErrorCategory
    severity: ErrorSeverity
    message: str
    details: str
    context: ErrorContext
    stack_trace: Optional[str] = None
    recovery_suggestions: List[str] = field(default_factory=list)
    retry_count: int = 0
    max_retries: int = 3
    resolved: bool = False
    resolution_notes: Optional[str] = None


class BusinessLogicError(Exception):
    """Business logic validation error"""
    
    def __init__(self, message: str, error_code: str = None, context: Dict[str, Any] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code or "BUSINESS_LOGIC_ERROR"
        self.context = context or {}


class IntegrationError(Exception):
    """External service integration error"""
    
    def __init__(self, message: str, service: str, error_code: str = None, response_data: Dict[str, Any] = None):
        super().__init__(message)
        self.message = message
        self.service = service
        self.error_code = error_code or "INTEGRATION_ERROR"
        self.response_data = response_data or {}


class PaymentError(Exception):
    """Payment processing error"""
    
    def __init__(self, message: str, gateway: str, transaction_id: str = None, error_code: str = None):
        super().__init__(message)
        self.message = message
        self.gateway = gateway
        self.transaction_id = transaction_id
        self.error_code = error_code or "PAYMENT_ERROR"


class InventoryError(Exception):
    """Inventory management error"""
    
    def __init__(self, message: str, product_id: str = None, requested_quantity: int = None, available_quantity: int = None):
        super().__init__(message)
        self.message = message
        self.product_id = product_id
        self.requested_quantity = requested_quantity
        self.available_quantity = available_quantity


class FulfillmentError(Exception):
    """Fulfillment processing error"""
    
    def __init__(self, message: str, order_id: str = None, warehouse_id: str = None, error_code: str = None):
        super().__init__(message)
        self.message = message
        self.order_id = order_id
        self.warehouse_id = warehouse_id
        self.error_code = error_code or "FULFILLMENT_ERROR"


class RetryableError(Exception):
    """Error that can be retried"""
    
    def __init__(self, message: str, retry_after_seconds: int = 5, max_retries: int = 3):
        super().__init__(message)
        self.message = message
        self.retry_after_seconds = retry_after_seconds
        self.max_retries = max_retries


class ErrorHandler:
    """
    Comprehensive error handling system
    Handles error categorization, logging, recovery, and notifications
    """
    
    def __init__(self):
        self.error_history = {}
        self.error_counters = {}
        self.recovery_strategies = {}
        self.notification_callbacks = []
        
        # Configure error mapping
        self.error_mapping = {
            BusinessLogicError: {
                "category": ErrorCategory.BUSINESS_LOGIC,
                "severity": ErrorSeverity.MEDIUM,
                "retryable": False
            },
            IntegrationError: {
                "category": ErrorCategory.INTEGRATION,
                "severity": ErrorSeverity.HIGH,
                "retryable": True
            },
            PaymentError: {
                "category": ErrorCategory.PAYMENT,
                "severity": ErrorSeverity.HIGH,
                "retryable": True
            },
            InventoryError: {
                "category": ErrorCategory.INVENTORY,
                "severity": ErrorSeverity.MEDIUM,
                "retryable": False
            },
            FulfillmentError: {
                "category": ErrorCategory.FULFILLMENT,
                "severity": ErrorSeverity.HIGH,
                "retryable": True
            },
            ConnectionError: {
                "category": ErrorCategory.NETWORK,
                "severity": ErrorSeverity.HIGH,
                "retryable": True
            },
            TimeoutError: {
                "category": ErrorCategory.NETWORK,
                "severity": ErrorSeverity.MEDIUM,
                "retryable": True
            },
            ValueError: {
                "category": ErrorCategory.VALIDATION,
                "severity": ErrorSeverity.LOW,
                "retryable": False
            },
            KeyError: {
                "category": ErrorCategory.VALIDATION,
                "severity": ErrorSeverity.LOW,
                "retryable": False
            }
        }
        
        self._register_recovery_strategies()
    
    async def handle_error(self, error: Exception, context: Optional[ErrorContext] = None) -> JSONResponse:
        """Main error handling entry point"""
        
        try:
            # Create error info
            error_info = await self._create_error_info(error, context)
            
            # Log error
            await self._log_error(error_info)
            
            # Store error for analysis
            self._store_error(error_info)
            
            # Update error counters
            self._update_error_counters(error_info)
            
            # Attempt recovery if possible
            recovery_result = await self._attempt_recovery(error_info)
            
            # Send notifications if critical
            if error_info.severity in [ErrorSeverity.HIGH, ErrorSeverity.CRITICAL]:
                await self._send_error_notifications(error_info)
            
            # Return appropriate HTTP response
            return self._create_error_response(error_info, recovery_result)
            
        except Exception as handler_error:
            logger.critical(f"Error handler failed: {handler_error}")
            
            # Fallback error response
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": "Internal server error",
                    "message": "An unexpected error occurred",
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
    
    async def handle_order_error(self, error: Exception, order_id: str, operation: str) -> Dict[str, Any]:
        """Handle order-specific errors"""
        
        context = ErrorContext(
            order_id=order_id,
            operation=operation,
            service="order_processing"
        )
        
        error_info = await self._create_error_info(error, context)
        
        # Log error
        await self._log_error(error_info)
        
        # Store error
        self._store_error(error_info)
        
        # Attempt recovery
        recovery_result = await self._attempt_recovery(error_info)
        
        return {
            "error_id": error_info.error_id,
            "category": error_info.category,
            "severity": error_info.severity,
            "message": error_info.message,
            "recovery_attempted": recovery_result.get("attempted", False),
            "recovery_successful": recovery_result.get("successful", False),
            "retry_recommended": recovery_result.get("retry_recommended", False),
            "retry_after_seconds": recovery_result.get("retry_after_seconds", 60)
        }
    
    async def retry_with_backoff(
        self,
        operation: Callable,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        backoff_factor: float = 2.0,
        retryable_exceptions: Optional[List[Type[Exception]]] = None
    ) -> Any:
        """Retry operation with exponential backoff"""
        
        if retryable_exceptions is None:
            retryable_exceptions = [ConnectionError, TimeoutError, IntegrationError, RetryableError]
        
        last_exception = None
        
        for attempt in range(max_retries + 1):
            try:
                # Execute operation
                if asyncio.iscoroutinefunction(operation):
                    result = await operation()
                else:
                    result = operation()
                
                # Success - return result
                if attempt > 0:
                    logger.info(f"Operation succeeded after {attempt} retries")
                
                return result
                
            except Exception as e:
                last_exception = e
                
                # Check if exception is retryable
                if not any(isinstance(e, exc_type) for exc_type in retryable_exceptions):
                    logger.error(f"Non-retryable error: {e}")
                    raise e
                
                # If this was the last attempt, raise the exception
                if attempt == max_retries:
                    logger.error(f"Operation failed after {max_retries} retries: {e}")
                    raise e
                
                # Calculate delay with exponential backoff
                delay = min(base_delay * (backoff_factor ** attempt), max_delay)
                
                logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay:.2f}s")
                
                await asyncio.sleep(delay)
        
        # This should never be reached, but just in case
        raise last_exception
    
    def add_recovery_strategy(self, error_type: Type[Exception], strategy: Callable[[ErrorInfo], Dict[str, Any]]):
        """Add custom recovery strategy for error type"""
        self.recovery_strategies[error_type] = strategy
    
    def add_notification_callback(self, callback: Callable[[ErrorInfo], None]):
        """Add callback for error notifications"""
        self.notification_callbacks.append(callback)
    
    def get_error_statistics(self, time_range_hours: int = 24) -> Dict[str, Any]:
        """Get error statistics for specified time range"""
        
        cutoff_time = datetime.utcnow() - timedelta(hours=time_range_hours)
        
        # Filter recent errors
        recent_errors = [
            error for error in self.error_history.values()
            if error.timestamp > cutoff_time
        ]
        
        # Count by category
        category_counts = {}
        for category in ErrorCategory:
            category_counts[category.value] = len([
                e for e in recent_errors if e.category == category
            ])
        
        # Count by severity
        severity_counts = {}
        for severity in ErrorSeverity:
            severity_counts[severity.value] = len([
                e for e in recent_errors if e.severity == severity
            ])
        
        # Calculate error rate
        total_errors = len(recent_errors)
        error_rate_per_hour = total_errors / time_range_hours if time_range_hours > 0 else 0
        
        return {
            "time_range_hours": time_range_hours,
            "total_errors": total_errors,
            "error_rate_per_hour": error_rate_per_hour,
            "errors_by_category": category_counts,
            "errors_by_severity": severity_counts,
            "most_common_errors": self._get_most_common_errors(recent_errors),
            "recovery_success_rate": self._calculate_recovery_success_rate(recent_errors)
        }
    
    def get_error_trends(self, days: int = 7) -> Dict[str, Any]:
        """Get error trends over specified days"""
        
        trends = {}
        
        for day in range(days):
            day_start = datetime.utcnow() - timedelta(days=day+1)
            day_end = datetime.utcnow() - timedelta(days=day)
            
            day_errors = [
                error for error in self.error_history.values()
                if day_start <= error.timestamp < day_end
            ]
            
            trends[day_start.strftime("%Y-%m-%d")] = {
                "total_errors": len(day_errors),
                "critical_errors": len([e for e in day_errors if e.severity == ErrorSeverity.CRITICAL]),
                "resolved_errors": len([e for e in day_errors if e.resolved])
            }
        
        return trends
    
    # Private methods
    
    async def _create_error_info(self, error: Exception, context: Optional[ErrorContext] = None) -> ErrorInfo:
        """Create comprehensive error information"""
        
        error_id = f"err_{int(datetime.utcnow().timestamp() * 1000)}"
        
        # Determine error category and severity
        error_type = type(error)
        error_config = self.error_mapping.get(error_type, {
            "category": ErrorCategory.SYSTEM,
            "severity": ErrorSeverity.MEDIUM,
            "retryable": False
        })
        
        # Get stack trace
        stack_trace = traceback.format_exc()
        
        # Generate recovery suggestions
        recovery_suggestions = self._generate_recovery_suggestions(error, error_config)
        
        return ErrorInfo(
            error_id=error_id,
            timestamp=datetime.utcnow(),
            category=error_config["category"],
            severity=error_config["severity"],
            message=str(error),
            details=self._extract_error_details(error),
            context=context or ErrorContext(),
            stack_trace=stack_trace,
            recovery_suggestions=recovery_suggestions,
            max_retries=3 if error_config.get("retryable", False) else 0
        )
    
    def _extract_error_details(self, error: Exception) -> str:
        """Extract detailed error information"""
        
        details = []
        
        # Add error type
        details.append(f"Error Type: {type(error).__name__}")
        
        # Add specific error attributes
        if hasattr(error, 'error_code'):
            details.append(f"Error Code: {error.error_code}")
        
        if hasattr(error, 'service'):
            details.append(f"Service: {error.service}")
        
        if hasattr(error, 'gateway'):
            details.append(f"Gateway: {error.gateway}")
        
        if hasattr(error, 'transaction_id'):
            details.append(f"Transaction ID: {error.transaction_id}")
        
        if hasattr(error, 'product_id'):
            details.append(f"Product ID: {error.product_id}")
        
        if hasattr(error, 'response_data'):
            details.append(f"Response Data: {error.response_data}")
        
        return " | ".join(details)
    
    def _generate_recovery_suggestions(self, error: Exception, error_config: Dict[str, Any]) -> List[str]:
        """Generate recovery suggestions based on error type"""
        
        suggestions = []
        
        if isinstance(error, ConnectionError):
            suggestions.extend([
                "Check network connectivity",
                "Verify service endpoints are accessible",
                "Retry operation after a short delay"
            ])
        
        elif isinstance(error, TimeoutError):
            suggestions.extend([
                "Increase timeout duration",
                "Check service performance",
                "Retry with exponential backoff"
            ])
        
        elif isinstance(error, PaymentError):
            suggestions.extend([
                "Verify payment gateway credentials",
                "Check payment method validity",
                "Review transaction limits",
                "Contact payment provider if issue persists"
            ])
        
        elif isinstance(error, InventoryError):
            suggestions.extend([
                "Check inventory levels",
                "Update product availability",
                "Consider backorder or substitute products",
                "Notify customer of availability issues"
            ])
        
        elif isinstance(error, IntegrationError):
            suggestions.extend([
                "Verify API credentials",
                "Check service status",
                "Review API rate limits",
                "Retry operation"
            ])
        
        elif isinstance(error, BusinessLogicError):
            suggestions.extend([
                "Review business rules",
                "Validate input data",
                "Check order requirements",
                "Contact system administrator"
            ])
        
        # Add generic suggestions
        if error_config.get("retryable", False):
            suggestions.append("Operation can be retried")
        else:
            suggestions.append("Manual intervention may be required")
        
        return suggestions
    
    async def _log_error(self, error_info: ErrorInfo):
        """Log error with appropriate level"""
        
        log_message = f"[{error_info.error_id}] {error_info.category.value.upper()}: {error_info.message}"
        
        context_info = []
        if error_info.context.order_id:
            context_info.append(f"Order: {error_info.context.order_id}")
        if error_info.context.customer_id:
            context_info.append(f"Customer: {error_info.context.customer_id}")
        if error_info.context.operation:
            context_info.append(f"Operation: {error_info.context.operation}")
        
        if context_info:
            log_message += f" | Context: {', '.join(context_info)}"
        
        if error_info.severity == ErrorSeverity.CRITICAL:
            logger.critical(log_message)
        elif error_info.severity == ErrorSeverity.HIGH:
            logger.error(log_message)
        elif error_info.severity == ErrorSeverity.MEDIUM:
            logger.warning(log_message)
        else:
            logger.info(log_message)
        
        # Log stack trace for high severity errors
        if error_info.severity in [ErrorSeverity.HIGH, ErrorSeverity.CRITICAL] and error_info.stack_trace:
            logger.error(f"Stack trace for {error_info.error_id}:\n{error_info.stack_trace}")
    
    def _store_error(self, error_info: ErrorInfo):
        """Store error for analysis"""
        self.error_history[error_info.error_id] = error_info
        
        # Cleanup old errors (keep last 1000)
        if len(self.error_history) > 1000:
            oldest_errors = sorted(self.error_history.items(), key=lambda x: x[1].timestamp)[:100]
            for error_id, _ in oldest_errors:
                del self.error_history[error_id]
    
    def _update_error_counters(self, error_info: ErrorInfo):
        """Update error counters for monitoring"""
        
        # Count by category
        category_key = f"errors_{error_info.category.value}"
        self.error_counters[category_key] = self.error_counters.get(category_key, 0) + 1
        
        # Count by severity
        severity_key = f"errors_{error_info.severity.value}"
        self.error_counters[severity_key] = self.error_counters.get(severity_key, 0) + 1
        
        # Total error count
        self.error_counters["total_errors"] = self.error_counters.get("total_errors", 0) + 1
    
    async def _attempt_recovery(self, error_info: ErrorInfo) -> Dict[str, Any]:
        """Attempt to recover from error"""
        
        recovery_result = {
            "attempted": False,
            "successful": False,
            "retry_recommended": False,
            "retry_after_seconds": 60
        }
        
        # Check if error type has a recovery strategy
        error_type = type(sys.exc_info()[1]) if sys.exc_info()[1] else Exception
        
        if error_type in self.recovery_strategies:
            try:
                recovery_result["attempted"] = True
                strategy_result = self.recovery_strategies[error_type](error_info)
                recovery_result.update(strategy_result)
                
                if recovery_result["successful"]:
                    error_info.resolved = True
                    error_info.resolution_notes = "Automatically recovered"
                
            except Exception as recovery_error:
                logger.error(f"Recovery strategy failed: {recovery_error}")
        
        # Check if error is retryable
        elif error_info.max_retries > 0 and error_info.retry_count < error_info.max_retries:
            recovery_result["retry_recommended"] = True
            recovery_result["retry_after_seconds"] = 2 ** error_info.retry_count  # Exponential backoff
        
        return recovery_result
    
    async def _send_error_notifications(self, error_info: ErrorInfo):
        """Send error notifications"""
        
        for callback in self.notification_callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(error_info)
                else:
                    callback(error_info)
            except Exception as notification_error:
                logger.error(f"Error notification failed: {notification_error}")
    
    def _create_error_response(self, error_info: ErrorInfo, recovery_result: Dict[str, Any]) -> JSONResponse:
        """Create HTTP error response"""
        
        # Determine HTTP status code
        if error_info.category == ErrorCategory.AUTHENTICATION:
            status_code = status.HTTP_401_UNAUTHORIZED
        elif error_info.category == ErrorCategory.AUTHORIZATION:
            status_code = status.HTTP_403_FORBIDDEN
        elif error_info.category == ErrorCategory.VALIDATION:
            status_code = status.HTTP_400_BAD_REQUEST
        elif error_info.category in [ErrorCategory.BUSINESS_LOGIC, ErrorCategory.INVENTORY]:
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        elif error_info.category in [ErrorCategory.INTEGRATION, ErrorCategory.PAYMENT]:
            status_code = status.HTTP_502_BAD_GATEWAY
        elif error_info.severity == ErrorSeverity.CRITICAL:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        
        # Create response content
        response_content = {
            "error": {
                "id": error_info.error_id,
                "category": error_info.category.value,
                "severity": error_info.severity.value,
                "message": error_info.message,
                "timestamp": error_info.timestamp.isoformat(),
                "recovery_suggestions": error_info.recovery_suggestions
            }
        }
        
        # Add recovery information
        if recovery_result["attempted"]:
            response_content["recovery"] = {
                "attempted": True,
                "successful": recovery_result["successful"],
                "retry_recommended": recovery_result["retry_recommended"]
            }
            
            if recovery_result["retry_recommended"]:
                response_content["recovery"]["retry_after_seconds"] = recovery_result["retry_after_seconds"]
        
        # Add context if available
        if error_info.context.order_id:
            response_content["context"] = {
                "order_id": error_info.context.order_id,
                "operation": error_info.context.operation
            }
        
        return JSONResponse(
            status_code=status_code,
            content=response_content
        )
    
    def _register_recovery_strategies(self):
        """Register default recovery strategies"""
        
        def connection_error_recovery(error_info: ErrorInfo) -> Dict[str, Any]:
            """Recovery strategy for connection errors"""
            return {
                "successful": False,
                "retry_recommended": True,
                "retry_after_seconds": 5
            }
        
        def payment_error_recovery(error_info: ErrorInfo) -> Dict[str, Any]:
            """Recovery strategy for payment errors"""
            # Could attempt with different gateway or payment method
            return {
                "successful": False,
                "retry_recommended": True,
                "retry_after_seconds": 30
            }
        
        def inventory_error_recovery(error_info: ErrorInfo) -> Dict[str, Any]:
            """Recovery strategy for inventory errors"""
            # Could suggest alternative products or backorder
            return {
                "successful": False,
                "retry_recommended": False,
                "alternative_actions": ["suggest_alternatives", "enable_backorder"]
            }
        
        self.recovery_strategies[ConnectionError] = connection_error_recovery
        self.recovery_strategies[PaymentError] = payment_error_recovery
        self.recovery_strategies[InventoryError] = inventory_error_recovery
    
    def _get_most_common_errors(self, errors: List[ErrorInfo]) -> List[Dict[str, Any]]:
        """Get most common error types"""
        
        error_counts = {}
        
        for error in errors:
            key = f"{error.category.value}:{error.message}"
            if key not in error_counts:
                error_counts[key] = {
                    "category": error.category.value,
                    "message": error.message,
                    "count": 0
                }
            error_counts[key]["count"] += 1
        
        # Sort by count and return top 5
        sorted_errors = sorted(error_counts.values(), key=lambda x: x["count"], reverse=True)
        return sorted_errors[:5]
    
    def _calculate_recovery_success_rate(self, errors: List[ErrorInfo]) -> float:
        """Calculate recovery success rate"""
        
        total_recovery_attempts = len([e for e in errors if e.retry_count > 0])
        successful_recoveries = len([e for e in errors if e.resolved])
        
        if total_recovery_attempts > 0:
            return (successful_recoveries / total_recovery_attempts) * 100
        return 0.0


# Global error handler instance
error_handler = ErrorHandler()


# Decorator for automatic error handling
def handle_errors(operation_name: str = None):
    """Decorator to automatically handle errors in functions"""
    
    def decorator(func):
        async def async_wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                context = ErrorContext(
                    operation=operation_name or func.__name__,
                    service="order_processing"
                )
                
                error_result = await error_handler.handle_order_error(e, "unknown", operation_name or func.__name__)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=error_result
                )
        
        def sync_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                context = ErrorContext(
                    operation=operation_name or func.__name__,
                    service="order_processing"
                )
                
                logger.error(f"Error in {func.__name__}: {e}")
                raise
        
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    
    return decorator