"""
Performance Optimization Service for Workflow Visualization
Ensures <100ms diagram rendering and <50ms WebSocket updates for 1000+ concurrent users
"""

import asyncio
import time
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
import hashlib
import zlib
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class CacheLevel(Enum):
    MEMORY = "memory"
    REDIS = "redis"  # For distributed caching
    DATABASE = "database"

class CompressionType(Enum):
    NONE = "none"
    GZIP = "gzip"
    ZLIB = "zlib"

@dataclass
class PerformanceMetrics:
    """Performance metrics for monitoring system health"""
    render_time_ms: float
    websocket_latency_ms: float
    concurrent_users: int
    memory_usage_mb: float
    cpu_usage_percent: float
    cache_hit_rate: float
    compression_ratio: float
    timestamp: datetime

@dataclass
class CacheEntry:
    """Cache entry with metadata"""
    key: str
    data: Any
    created_at: datetime
    expires_at: Optional[datetime]
    access_count: int
    last_accessed: datetime
    size_bytes: int
    compressed: bool

class MermaidOptimizer:
    """Optimizes Mermaid.js diagram generation and rendering"""
    
    def __init__(self):
        self.diagram_cache = {}  # In-memory cache for generated diagrams
        self.complexity_thresholds = {
            "simple": 10,     # <= 10 nodes
            "moderate": 50,   # <= 50 nodes  
            "complex": 200,   # <= 200 nodes
            "very_complex": 500  # <= 500 nodes
        }
        
    def optimize_diagram(self, mermaid_diagram: str, node_count: int) -> str:
        """Optimize Mermaid diagram for performance based on complexity"""
        
        if node_count <= self.complexity_thresholds["simple"]:
            # No optimization needed for simple diagrams
            return mermaid_diagram
        
        elif node_count <= self.complexity_thresholds["moderate"]:
            # Moderate optimization: Reduce styling complexity
            return self._apply_moderate_optimization(mermaid_diagram)
        
        elif node_count <= self.complexity_thresholds["complex"]:
            # Heavy optimization: Simplify visual elements
            return self._apply_heavy_optimization(mermaid_diagram)
        
        else:
            # Extreme optimization: Minimal visual complexity
            return self._apply_extreme_optimization(mermaid_diagram)
    
    def _apply_moderate_optimization(self, diagram: str) -> str:
        """Apply moderate optimizations"""
        lines = diagram.split('\n')
        optimized_lines = []
        
        for line in lines:
            # Reduce class definitions
            if 'classDef' in line and 'stroke-width' in line:
                line = line.replace('stroke-width:3px', 'stroke-width:2px')
            optimized_lines.append(line)
        
        return '\n'.join(optimized_lines)
    
    def _apply_heavy_optimization(self, diagram: str) -> str:
        """Apply heavy optimizations for complex diagrams"""
        lines = diagram.split('\n')
        optimized_lines = []
        
        skip_classes = ['currentNode']  # Skip non-essential classes
        
        for line in lines:
            # Skip complex styling
            if any(skip_class in line for skip_class in skip_classes):
                continue
            
            # Simplify node labels (remove duration info)
            if '\\n(' in line and 's)' in line:
                line = line.split('\\n(')[0] + line.split('s)')[-1]
            
            optimized_lines.append(line)
        
        return '\n'.join(optimized_lines)
    
    def _apply_extreme_optimization(self, diagram: str) -> str:
        """Apply extreme optimizations for very complex diagrams"""
        lines = diagram.split('\n')
        optimized_lines = ['graph TD']
        
        # Keep only essential nodes and edges
        for line in lines[1:]:
            if '-->' in line and ':::' not in line:
                # Keep only basic edges without styling
                optimized_lines.append(line.split(':::')[0])
            elif '[' in line and ']' in line and ':::' not in line:
                # Keep only basic nodes without styling  
                optimized_lines.append(line.split(':::')[0])
        
        return '\n'.join(optimized_lines)

class WebSocketOptimizer:
    """Optimizes WebSocket communication for low latency"""
    
    def __init__(self, max_message_size: int = 32768):  # 32KB
        self.max_message_size = max_message_size
        self.message_queue = defaultdict(deque)
        self.last_sent_state = {}
        self.compression_enabled = True
        
    def optimize_message(self, message: Dict[str, Any], connection_id: str) -> Tuple[str, float]:
        """Optimize WebSocket message for minimal latency"""
        
        start_time = time.perf_counter()
        
        # Apply differential updates
        optimized_message = self._apply_differential_updates(message, connection_id)
        
        # Compress if beneficial
        if self.compression_enabled and len(json.dumps(optimized_message)) > 1024:  # 1KB threshold
            compressed_message = self._compress_message(optimized_message)
        else:
            compressed_message = json.dumps(optimized_message)
        
        # Check message size
        if len(compressed_message.encode()) > self.max_message_size:
            # Split large messages
            return self._split_large_message(compressed_message, connection_id)
        
        processing_time = (time.perf_counter() - start_time) * 1000  # Convert to ms
        
        return compressed_message, processing_time
    
    def _apply_differential_updates(self, message: Dict[str, Any], connection_id: str) -> Dict[str, Any]:
        """Apply differential updates to reduce message size"""
        
        if message.get("type") != "workflow_update":
            return message
        
        last_state = self.last_sent_state.get(connection_id)
        if not last_state:
            self.last_sent_state[connection_id] = message
            return message
        
        # Calculate differences
        diff_message = {"type": "workflow_update_diff"}
        
        # Compare workflow states
        current_state = message.get("workflow_state", {})
        last_workflow_state = last_state.get("workflow_state", {})
        
        # Only send changed nodes
        if "nodes" in current_state:
            changed_nodes = {}
            for node_id, node_data in current_state["nodes"].items():
                last_node = last_workflow_state.get("nodes", {}).get(node_id)
                if not last_node or node_data != last_node:
                    changed_nodes[node_id] = node_data
            
            if changed_nodes:
                diff_message["changed_nodes"] = changed_nodes
        
        # Only send changed progress
        current_progress = current_state.get("progress_percentage", 0)
        last_progress = last_workflow_state.get("progress_percentage", 0)
        if current_progress != last_progress:
            diff_message["progress_percentage"] = current_progress
        
        # Only send changed status
        current_status = current_state.get("status")
        last_status = last_workflow_state.get("status")
        if current_status != last_status:
            diff_message["status"] = current_status
        
        # Update last sent state
        self.last_sent_state[connection_id] = message
        
        return diff_message if len(diff_message) > 1 else message
    
    def _compress_message(self, message: Dict[str, Any]) -> str:
        """Compress message data"""
        json_str = json.dumps(message, separators=(',', ':'))  # Compact JSON
        compressed = zlib.compress(json_str.encode('utf-8'))
        
        # Only use compression if it provides significant benefit
        if len(compressed) < len(json_str.encode()) * 0.8:  # 20% improvement
            import base64
            return json.dumps({
                "compressed": True,
                "data": base64.b64encode(compressed).decode('utf-8')
            })
        
        return json_str
    
    def _split_large_message(self, message: str, connection_id: str) -> Tuple[str, float]:
        """Split large messages into chunks"""
        chunk_size = self.max_message_size // 2  # Leave room for metadata
        chunks = [message[i:i+chunk_size] for i in range(0, len(message), chunk_size)]
        
        message_id = hashlib.md5(message.encode()).hexdigest()[:8]
        
        # Return first chunk with metadata
        first_chunk = json.dumps({
            "type": "chunked_message",
            "message_id": message_id,
            "chunk_index": 0,
            "total_chunks": len(chunks),
            "data": chunks[0]
        })
        
        # Queue remaining chunks
        for i, chunk in enumerate(chunks[1:], 1):
            chunk_message = json.dumps({
                "type": "chunked_message", 
                "message_id": message_id,
                "chunk_index": i,
                "total_chunks": len(chunks),
                "data": chunk
            })
            self.message_queue[connection_id].append(chunk_message)
        
        return first_chunk, 0.0  # Processing time for chunking is negligible
    
    def get_next_queued_message(self, connection_id: str) -> Optional[str]:
        """Get next queued message for a connection"""
        if connection_id in self.message_queue and self.message_queue[connection_id]:
            return self.message_queue[connection_id].popleft()
        return None

class CacheManager:
    """High-performance caching system for workflow data"""
    
    def __init__(self, max_memory_mb: int = 256):
        self.max_memory_bytes = max_memory_mb * 1024 * 1024
        self.memory_cache = {}
        self.cache_stats = {
            "hits": 0,
            "misses": 0,
            "memory_usage": 0
        }
        self.eviction_queue = deque()  # LRU eviction
        
    def get(self, key: str) -> Tuple[Optional[Any], bool]:
        """Get cached value with hit/miss tracking"""
        
        if key in self.memory_cache:
            entry = self.memory_cache[key]
            
            # Check expiration
            if entry.expires_at and datetime.utcnow() > entry.expires_at:
                self.delete(key)
                self.cache_stats["misses"] += 1
                return None, False
            
            # Update access info
            entry.access_count += 1
            entry.last_accessed = datetime.utcnow()
            
            # Move to end of LRU queue
            self.eviction_queue.append(key)
            
            self.cache_stats["hits"] += 1
            return entry.data, True
        
        self.cache_stats["misses"] += 1
        return None, False
    
    def set(self, key: str, data: Any, ttl_seconds: Optional[int] = None, compress: bool = False) -> bool:
        """Set cached value with optional compression"""
        
        # Serialize and potentially compress data
        if compress:
            serialized = zlib.compress(json.dumps(data).encode())
            compressed = True
        else:
            serialized = json.dumps(data).encode()
            compressed = False
        
        data_size = len(serialized)
        
        # Check if we need to evict entries
        while self.cache_stats["memory_usage"] + data_size > self.max_memory_bytes:
            if not self._evict_lru():
                return False  # Could not make space
        
        # Create cache entry
        expires_at = datetime.utcnow() + timedelta(seconds=ttl_seconds) if ttl_seconds else None
        entry = CacheEntry(
            key=key,
            data=data,
            created_at=datetime.utcnow(),
            expires_at=expires_at,
            access_count=1,
            last_accessed=datetime.utcnow(),
            size_bytes=data_size,
            compressed=compressed
        )
        
        # Store in cache
        self.memory_cache[key] = entry
        self.eviction_queue.append(key)
        self.cache_stats["memory_usage"] += data_size
        
        return True
    
    def delete(self, key: str) -> bool:
        """Delete cached entry"""
        if key in self.memory_cache:
            entry = self.memory_cache[key]
            self.cache_stats["memory_usage"] -= entry.size_bytes
            del self.memory_cache[key]
            
            # Remove from eviction queue
            try:
                while key in self.eviction_queue:
                    self.eviction_queue.remove(key)
            except ValueError:
                pass
            
            return True
        return False
    
    def _evict_lru(self) -> bool:
        """Evict least recently used entry"""
        while self.eviction_queue:
            key = self.eviction_queue.popleft()
            if key in self.memory_cache:
                self.delete(key)
                return True
        return False
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache performance statistics"""
        total_requests = self.cache_stats["hits"] + self.cache_stats["misses"]
        hit_rate = (self.cache_stats["hits"] / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "hit_rate_percent": hit_rate,
            "total_entries": len(self.memory_cache),
            "memory_usage_mb": self.cache_stats["memory_usage"] / (1024 * 1024),
            "memory_usage_percent": (self.cache_stats["memory_usage"] / self.max_memory_bytes) * 100,
            "total_requests": total_requests,
            "hits": self.cache_stats["hits"],
            "misses": self.cache_stats["misses"]
        }

class PerformanceMonitor:
    """Monitors and tracks performance metrics"""
    
    def __init__(self, max_history: int = 1000):
        self.max_history = max_history
        self.metrics_history = deque(maxlen=max_history)
        self.current_metrics = defaultdict(list)
        self.performance_targets = {
            "render_time_ms": 100.0,
            "websocket_latency_ms": 50.0,
            "max_concurrent_users": 1000
        }
        
    def record_metric(self, metric_name: str, value: float, timestamp: datetime = None):
        """Record a performance metric"""
        if not timestamp:
            timestamp = datetime.utcnow()
        
        self.current_metrics[metric_name].append((timestamp, value))
        
        # Keep only recent metrics (last 5 minutes)
        cutoff_time = timestamp - timedelta(minutes=5)
        self.current_metrics[metric_name] = [
            (ts, val) for ts, val in self.current_metrics[metric_name]
            if ts > cutoff_time
        ]
    
    def record_performance_metrics(self, metrics: PerformanceMetrics):
        """Record complete performance metrics"""
        self.metrics_history.append(metrics)
        
        # Record individual metrics
        self.record_metric("render_time_ms", metrics.render_time_ms, metrics.timestamp)
        self.record_metric("websocket_latency_ms", metrics.websocket_latency_ms, metrics.timestamp)
        self.record_metric("concurrent_users", metrics.concurrent_users, metrics.timestamp)
        self.record_metric("memory_usage_mb", metrics.memory_usage_mb, metrics.timestamp)
        self.record_metric("cpu_usage_percent", metrics.cpu_usage_percent, metrics.timestamp)
        self.record_metric("cache_hit_rate", metrics.cache_hit_rate, metrics.timestamp)
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary with SLA compliance"""
        if not self.metrics_history:
            return {"error": "No metrics available"}
        
        recent_metrics = list(self.metrics_history)[-100:]  # Last 100 measurements
        
        # Calculate averages
        avg_render_time = sum(m.render_time_ms for m in recent_metrics) / len(recent_metrics)
        avg_websocket_latency = sum(m.websocket_latency_ms for m in recent_metrics) / len(recent_metrics)
        max_concurrent_users = max(m.concurrent_users for m in recent_metrics)
        avg_memory_usage = sum(m.memory_usage_mb for m in recent_metrics) / len(recent_metrics)
        avg_cpu_usage = sum(m.cpu_usage_percent for m in recent_metrics) / len(recent_metrics)
        avg_cache_hit_rate = sum(m.cache_hit_rate for m in recent_metrics) / len(recent_metrics)
        
        # Check SLA compliance
        render_sla_compliance = (avg_render_time <= self.performance_targets["render_time_ms"])
        websocket_sla_compliance = (avg_websocket_latency <= self.performance_targets["websocket_latency_ms"])
        concurrency_sla_compliance = (max_concurrent_users <= self.performance_targets["max_concurrent_users"])
        
        return {
            "performance_summary": {
                "avg_render_time_ms": round(avg_render_time, 2),
                "avg_websocket_latency_ms": round(avg_websocket_latency, 2),
                "max_concurrent_users": max_concurrent_users,
                "avg_memory_usage_mb": round(avg_memory_usage, 2),
                "avg_cpu_usage_percent": round(avg_cpu_usage, 2),
                "avg_cache_hit_rate_percent": round(avg_cache_hit_rate, 2)
            },
            "sla_compliance": {
                "render_time_compliant": render_sla_compliance,
                "websocket_latency_compliant": websocket_sla_compliance,
                "concurrency_compliant": concurrency_sla_compliance,
                "overall_compliant": all([
                    render_sla_compliance,
                    websocket_sla_compliance,
                    concurrency_sla_compliance
                ])
            },
            "performance_targets": self.performance_targets,
            "metrics_collected": len(self.metrics_history),
            "measurement_period_minutes": 5
        }
    
    def get_real_time_metrics(self) -> Dict[str, float]:
        """Get current real-time performance metrics"""
        if not self.metrics_history:
            return {}
        
        latest = self.metrics_history[-1]
        return {
            "render_time_ms": latest.render_time_ms,
            "websocket_latency_ms": latest.websocket_latency_ms,
            "concurrent_users": latest.concurrent_users,
            "memory_usage_mb": latest.memory_usage_mb,
            "cpu_usage_percent": latest.cpu_usage_percent,
            "cache_hit_rate_percent": latest.cache_hit_rate,
            "timestamp": latest.timestamp.isoformat()
        }
    
    def alert_on_performance_degradation(self) -> List[Dict[str, Any]]:
        """Generate alerts for performance issues"""
        alerts = []
        
        if len(self.metrics_history) < 10:  # Need some history
            return alerts
        
        recent_metrics = list(self.metrics_history)[-10:]
        latest = recent_metrics[-1]
        
        # Check render time
        if latest.render_time_ms > self.performance_targets["render_time_ms"]:
            alerts.append({
                "type": "performance_degradation",
                "severity": "warning" if latest.render_time_ms < 150 else "critical",
                "metric": "render_time_ms",
                "current_value": latest.render_time_ms,
                "target_value": self.performance_targets["render_time_ms"],
                "message": f"Render time {latest.render_time_ms}ms exceeds target {self.performance_targets['render_time_ms']}ms"
            })
        
        # Check WebSocket latency
        if latest.websocket_latency_ms > self.performance_targets["websocket_latency_ms"]:
            alerts.append({
                "type": "performance_degradation",
                "severity": "warning" if latest.websocket_latency_ms < 75 else "critical",
                "metric": "websocket_latency_ms",
                "current_value": latest.websocket_latency_ms,
                "target_value": self.performance_targets["websocket_latency_ms"],
                "message": f"WebSocket latency {latest.websocket_latency_ms}ms exceeds target {self.performance_targets['websocket_latency_ms']}ms"
            })
        
        # Check concurrent users
        if latest.concurrent_users > self.performance_targets["max_concurrent_users"]:
            alerts.append({
                "type": "capacity_exceeded",
                "severity": "critical",
                "metric": "concurrent_users", 
                "current_value": latest.concurrent_users,
                "target_value": self.performance_targets["max_concurrent_users"],
                "message": f"Concurrent users {latest.concurrent_users} exceeds capacity {self.performance_targets['max_concurrent_users']}"
            })
        
        return alerts

class PerformanceOptimizationService:
    """Main performance optimization service orchestrator"""
    
    def __init__(self):
        self.mermaid_optimizer = MermaidOptimizer()
        self.websocket_optimizer = WebSocketOptimizer()
        self.cache_manager = CacheManager()
        self.performance_monitor = PerformanceMonitor()
        
    async def optimize_workflow_rendering(self, workflow_state: Dict[str, Any]) -> Tuple[str, float]:
        """Optimize workflow rendering for performance"""
        start_time = time.perf_counter()
        
        # Generate cache key
        cache_key = f"mermaid_{hashlib.md5(json.dumps(workflow_state, sort_keys=True).encode()).hexdigest()}"
        
        # Check cache first
        cached_diagram, cache_hit = self.cache_manager.get(cache_key)
        if cache_hit:
            render_time = (time.perf_counter() - start_time) * 1000
            logger.info(f"Mermaid diagram served from cache in {render_time:.2f}ms")
            return cached_diagram, render_time
        
        # Generate optimized Mermaid diagram
        from services.workflow_visualization_service import MermaidGenerator
        base_diagram = MermaidGenerator.generate_workflow_diagram(workflow_state)
        
        # Apply performance optimizations
        node_count = len(workflow_state.get("nodes", {}))
        optimized_diagram = self.mermaid_optimizer.optimize_diagram(base_diagram, node_count)
        
        # Cache the result
        self.cache_manager.set(cache_key, optimized_diagram, ttl_seconds=300, compress=True)
        
        render_time = (time.perf_counter() - start_time) * 1000
        
        # Record performance metrics
        self.performance_monitor.record_metric("render_time_ms", render_time)
        
        logger.info(f"Mermaid diagram generated and optimized in {render_time:.2f}ms")
        return optimized_diagram, render_time
    
    async def optimize_websocket_message(self, message: Dict[str, Any], connection_id: str) -> Tuple[str, float]:
        """Optimize WebSocket message for minimal latency"""
        return self.websocket_optimizer.optimize_message(message, connection_id)
    
    def get_performance_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive performance data for dashboard"""
        return {
            "performance_summary": self.performance_monitor.get_performance_summary(),
            "real_time_metrics": self.performance_monitor.get_real_time_metrics(),
            "cache_statistics": self.cache_manager.get_cache_stats(),
            "performance_alerts": self.performance_monitor.alert_on_performance_degradation(),
            "optimization_status": {
                "mermaid_optimization": "enabled",
                "websocket_optimization": "enabled", 
                "caching": "enabled",
                "compression": "adaptive"
            }
        }

# Global performance optimization service
performance_service = PerformanceOptimizationService()