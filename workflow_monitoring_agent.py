#!/usr/bin/env python3
"""
BizOSaaS Platform - Workflow Monitoring Agent
==============================================

A standalone monitoring agent that continuously validates workflow implementations
and provides real-time status updates for the BizOSaaS platform.

Author: Claude Code
Date: September 26, 2025
Version: 1.0.0
"""

import asyncio
import json
import logging
import time
import signal
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import requests
import threading
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/bizosaas_monitoring.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class MonitoringConfig:
    """Configuration for monitoring agent"""
    check_interval: int = 60  # seconds
    alert_threshold: int = 3  # consecutive failures
    performance_threshold: float = 5.0  # seconds
    services_config: Dict[str, Any] = None

    def __post_init__(self):
        if self.services_config is None:
            self.services_config = self._default_services_config()

    def _default_services_config(self) -> Dict[str, Any]:
        return {
            "client_portal": {"port": 3000, "path": "/", "critical": True},
            "bizoholic_frontend": {"port": 3001, "path": "/", "critical": True},
            "coreldove_frontend": {"port": 3002, "path": "/", "critical": True},
            "business_directory_frontend": {"port": 3004, "path": "/", "critical": False},
            "central_hub": {"port": 8001, "path": "/health", "critical": True},
            "wagtail_cms": {"port": 8002, "path": "/admin/", "critical": False},
            "business_directory_backend": {"port": 8004, "path": "/health", "critical": True},
            "sqladmin": {"port": 8005, "path": "/", "critical": False},
            "auth_service": {"port": 8007, "path": "/health", "critical": True},
            "temporal": {"port": 8009, "path": "/health", "critical": False},
            "ai_agents": {"port": 8010, "path": "/health", "critical": True},
            "superset": {"port": 8088, "path": "/health", "critical": False}
        }


@dataclass
class ServiceStatus:
    """Current status of a service"""
    name: str
    status: str  # healthy, unhealthy, down, timeout
    response_time: float
    last_check: datetime
    consecutive_failures: int = 0
    error_message: Optional[str] = None


@dataclass
class WorkflowStatus:
    """Status of a complete workflow"""
    name: str
    status: str  # pass, fail, partial, error
    steps_passed: int
    steps_total: int
    last_check: datetime
    issues: List[str] = None

    def __post_init__(self):
        if self.issues is None:
            self.issues = []


class WorkflowMonitoringAgent:
    """Main monitoring agent for BizOSaaS platform"""

    def __init__(self, config: MonitoringConfig = None):
        self.config = config or MonitoringConfig()
        self.service_statuses = {}
        self.workflow_statuses = {}
        self.monitoring_active = False
        self.alert_history = []
        
        # Initialize service statuses
        for service_name in self.config.services_config.keys():
            self.service_statuses[service_name] = ServiceStatus(
                name=service_name,
                status="unknown",
                response_time=0.0,
                last_check=datetime.now(),
                consecutive_failures=0
            )

    def start_monitoring(self):
        """Start continuous monitoring"""
        logger.info("🚀 Starting BizOSaaS Platform Monitoring Agent")
        self.monitoring_active = True
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        # Start monitoring loop
        try:
            asyncio.run(self._monitoring_loop())
        except KeyboardInterrupt:
            logger.info("⚠️  Monitoring interrupted by user")
        except Exception as e:
            logger.error(f"❌ Monitoring failed: {e}")
        finally:
            self._cleanup()

    async def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                # Check service health
                await self._check_all_services()
                
                # Check workflow status
                await self._check_workflow_status()
                
                # Generate alerts if needed
                self._process_alerts()
                
                # Generate status report
                self._generate_status_report()
                
                # Wait for next check
                await asyncio.sleep(self.config.check_interval)
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(10)  # Short delay on error

    async def _check_all_services(self):
        """Check health of all services"""
        logger.info("🔍 Checking service health...")
        
        # Create tasks for concurrent checking
        tasks = []
        for service_name, service_config in self.config.services_config.items():
            task = asyncio.create_task(
                self._check_single_service(service_name, service_config)
            )
            tasks.append(task)
        
        # Wait for all checks to complete
        await asyncio.gather(*tasks, return_exceptions=True)

    async def _check_single_service(self, service_name: str, service_config: Dict[str, Any]):
        """Check health of a single service"""
        port = service_config["port"]
        path = service_config["path"]
        url = f"http://localhost:{port}{path}"
        
        start_time = time.time()
        
        try:
            # Make request with timeout
            response = await asyncio.to_thread(
                requests.get, url, timeout=10
            )
            
            response_time = time.time() - start_time
            
            # Determine status
            if response.status_code in [200, 302]:
                status = "healthy"
                error_message = None
                consecutive_failures = 0
            else:
                status = "unhealthy"
                error_message = f"HTTP {response.status_code}"
                consecutive_failures = self.service_statuses[service_name].consecutive_failures + 1
            
        except requests.exceptions.ConnectionError:
            response_time = time.time() - start_time
            status = "down"
            error_message = "Connection refused"
            consecutive_failures = self.service_statuses[service_name].consecutive_failures + 1
            
        except requests.exceptions.Timeout:
            response_time = self.config.performance_threshold
            status = "timeout"
            error_message = "Request timeout"
            consecutive_failures = self.service_statuses[service_name].consecutive_failures + 1
            
        except Exception as e:
            response_time = time.time() - start_time
            status = "error"
            error_message = str(e)
            consecutive_failures = self.service_statuses[service_name].consecutive_failures + 1
        
        # Update service status
        self.service_statuses[service_name] = ServiceStatus(
            name=service_name,
            status=status,
            response_time=response_time,
            last_check=datetime.now(),
            consecutive_failures=consecutive_failures,
            error_message=error_message
        )

    async def _check_workflow_status(self):
        """Check status of critical workflows"""
        logger.info("🛤️  Checking workflow status...")
        
        workflows = {
            "user_onboarding": self._check_user_onboarding_workflow,
            "coreldove_ecommerce": self._check_coreldove_workflow,
            "api_integration": self._check_api_integration_workflow
        }
        
        for workflow_name, check_function in workflows.items():
            try:
                workflow_status = await check_function()
                self.workflow_statuses[workflow_name] = workflow_status
            except Exception as e:
                logger.error(f"Error checking workflow {workflow_name}: {e}")
                self.workflow_statuses[workflow_name] = WorkflowStatus(
                    name=workflow_name,
                    status="error",
                    steps_passed=0,
                    steps_total=1,
                    last_check=datetime.now(),
                    issues=[str(e)]
                )

    async def _check_user_onboarding_workflow(self) -> WorkflowStatus:
        """Check user onboarding workflow"""
        steps = [
            ("client_portal", "http://localhost:3000"),
            ("auth_endpoints", "http://localhost:3000/auth/login"),
            ("onboarding_wizard", "http://localhost:3000/onboarding")
        ]
        
        passed = 0
        issues = []
        
        for step_name, url in steps:
            try:
                response = await asyncio.to_thread(
                    requests.get, url, timeout=10
                )
                if response.status_code in [200, 302]:
                    passed += 1
                else:
                    issues.append(f"{step_name}: HTTP {response.status_code}")
            except Exception as e:
                issues.append(f"{step_name}: {str(e)}")
        
        status = "pass" if passed == len(steps) else "partial" if passed > 0 else "fail"
        
        return WorkflowStatus(
            name="user_onboarding",
            status=status,
            steps_passed=passed,
            steps_total=len(steps),
            last_check=datetime.now(),
            issues=issues
        )

    async def _check_coreldove_workflow(self) -> WorkflowStatus:
        """Check CoreLDove e-commerce workflow"""
        steps = [
            ("frontend", "http://localhost:3002"),
            ("sourcing", "http://localhost:3002/sourcing"),
            ("amazon", "http://localhost:3002/amazon"),
            ("dashboard", "http://localhost:3002/dashboard")
        ]
        
        passed = 0
        issues = []
        
        for step_name, url in steps:
            try:
                response = await asyncio.to_thread(
                    requests.get, url, timeout=10
                )
                if response.status_code in [200, 302]:
                    passed += 1
                else:
                    issues.append(f"{step_name}: HTTP {response.status_code}")
            except Exception as e:
                issues.append(f"{step_name}: {str(e)}")
        
        status = "pass" if passed == len(steps) else "partial" if passed > 0 else "fail"
        
        return WorkflowStatus(
            name="coreldove_ecommerce",
            status=status,
            steps_passed=passed,
            steps_total=len(steps),
            last_check=datetime.now(),
            issues=issues
        )

    async def _check_api_integration_workflow(self) -> WorkflowStatus:
        """Check API integration workflow"""
        api_endpoints = [
            ("ai_agents", "http://localhost:8010/health"),
            ("auth_service", "http://localhost:8007/health"),
            ("directory_backend", "http://localhost:8004/health")
        ]
        
        passed = 0
        issues = []
        
        for endpoint_name, url in api_endpoints:
            try:
                response = await asyncio.to_thread(
                    requests.get, url, timeout=5
                )
                if response.status_code in [200, 302]:
                    passed += 1
                else:
                    issues.append(f"{endpoint_name}: HTTP {response.status_code}")
            except Exception as e:
                issues.append(f"{endpoint_name}: {str(e)}")
        
        status = "pass" if passed == len(api_endpoints) else "partial" if passed > 0 else "fail"
        
        return WorkflowStatus(
            name="api_integration",
            status=status,
            steps_passed=passed,
            steps_total=len(api_endpoints),
            last_check=datetime.now(),
            issues=issues
        )

    def _process_alerts(self):
        """Process and generate alerts for service issues"""
        current_time = datetime.now()
        new_alerts = []
        
        # Check for services that need alerts
        for service_name, status in self.service_statuses.items():
            service_config = self.config.services_config[service_name]
            
            # Critical service down alert
            if (service_config.get("critical", False) and 
                status.status in ["down", "error"] and
                status.consecutive_failures >= self.config.alert_threshold):
                
                alert = {
                    "type": "critical_service_down",
                    "service": service_name,
                    "message": f"Critical service {service_name} has been down for {status.consecutive_failures} consecutive checks",
                    "timestamp": current_time,
                    "severity": "critical"
                }
                new_alerts.append(alert)
            
            # Performance degradation alert
            elif (status.response_time > self.config.performance_threshold and
                  status.status == "healthy"):
                
                alert = {
                    "type": "performance_degradation",
                    "service": service_name,
                    "message": f"Service {service_name} response time {status.response_time:.2f}s exceeds threshold",
                    "timestamp": current_time,
                    "severity": "warning"
                }
                new_alerts.append(alert)
        
        # Check for workflow failures
        for workflow_name, status in self.workflow_statuses.items():
            if status.status == "fail":
                alert = {
                    "type": "workflow_failure",
                    "workflow": workflow_name,
                    "message": f"Workflow {workflow_name} is failing: {len(status.issues)} issues detected",
                    "timestamp": current_time,
                    "severity": "high"
                }
                new_alerts.append(alert)
        
        # Add new alerts to history
        self.alert_history.extend(new_alerts)
        
        # Log new alerts
        for alert in new_alerts:
            severity_emoji = {"critical": "🚨", "high": "⚠️", "warning": "⚠️"}.get(alert["severity"], "ℹ️")
            logger.warning(f"{severity_emoji} ALERT: {alert['message']}")

    def _generate_status_report(self):
        """Generate current status report"""
        current_time = datetime.now()
        
        # Count service statuses
        healthy_services = sum(1 for s in self.service_statuses.values() if s.status == "healthy")
        total_services = len(self.service_statuses)
        
        # Count workflow statuses
        passing_workflows = sum(1 for w in self.workflow_statuses.values() if w.status == "pass")
        total_workflows = len(self.workflow_statuses)
        
        # Calculate platform health
        service_health = (healthy_services / total_services) * 100 if total_services > 0 else 0
        workflow_health = (passing_workflows / total_workflows) * 100 if total_workflows > 0 else 0
        overall_health = (service_health + workflow_health) / 2
        
        status_report = {
            "timestamp": current_time.isoformat(),
            "platform_health": {
                "overall_score": round(overall_health, 1),
                "services": f"{healthy_services}/{total_services}",
                "workflows": f"{passing_workflows}/{total_workflows}"
            },
            "services": {name: asdict(status) for name, status in self.service_statuses.items()},
            "workflows": {name: asdict(status) for name, status in self.workflow_statuses.items()},
            "recent_alerts": len([a for a in self.alert_history if a["timestamp"] > current_time - timedelta(minutes=5)])
        }
        
        # Save status report
        status_file = "/tmp/bizosaas_current_status.json"
        try:
            with open(status_file, 'w') as f:
                json.dump(status_report, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to save status report: {e}")
        
        # Log summary
        health_emoji = "🟢" if overall_health > 80 else "🟡" if overall_health > 60 else "🔴"
        logger.info(f"{health_emoji} Platform Health: {overall_health:.1f}% | Services: {healthy_services}/{total_services} | Workflows: {passing_workflows}/{total_workflows}")

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"🛑 Received signal {signum}, shutting down monitoring...")
        self.monitoring_active = False

    def _cleanup(self):
        """Cleanup resources"""
        logger.info("🧹 Cleaning up monitoring agent...")
        
        # Save final report
        final_report = {
            "shutdown_time": datetime.now().isoformat(),
            "total_alerts": len(self.alert_history),
            "final_service_statuses": {name: asdict(status) for name, status in self.service_statuses.items()},
            "final_workflow_statuses": {name: asdict(status) for name, status in self.workflow_statuses.items()}
        }
        
        try:
            with open("/tmp/bizosaas_monitoring_final_report.json", 'w') as f:
                json.dump(final_report, f, indent=2, default=str)
            logger.info("📄 Final monitoring report saved")
        except Exception as e:
            logger.error(f"Failed to save final report: {e}")

    def get_current_status(self) -> Dict[str, Any]:
        """Get current platform status"""
        return {
            "services": self.service_statuses,
            "workflows": self.workflow_statuses,
            "alerts": self.alert_history[-10:]  # Last 10 alerts
        }

    def display_status_dashboard(self):
        """Display real-time status dashboard"""
        print("\n" + "="*80)
        print("🚀 BizOSaaS Platform - Real-Time Status Dashboard")
        print("="*80)
        
        # Service Status
        print("\n🌐 SERVICE STATUS")
        print("-" * 50)
        for name, status in self.service_statuses.items():
            status_emoji = {"healthy": "✅", "unhealthy": "❌", "down": "🔴", "timeout": "⏰", "error": "💥"}.get(status.status, "❓")
            print(f"{status_emoji} {name:<30} {status.status:<12} {status.response_time:.3f}s")
        
        # Workflow Status
        print("\n🛤️  WORKFLOW STATUS")
        print("-" * 50)
        for name, status in self.workflow_statuses.items():
            status_emoji = {"pass": "✅", "partial": "⚠️", "fail": "❌", "error": "💥"}.get(status.status, "❓")
            print(f"{status_emoji} {name:<30} {status.status:<12} {status.steps_passed}/{status.steps_total}")
        
        # Recent Alerts
        recent_alerts = [a for a in self.alert_history if a["timestamp"] > datetime.now() - timedelta(minutes=30)]
        if recent_alerts:
            print(f"\n🚨 RECENT ALERTS ({len(recent_alerts)})")
            print("-" * 50)
            for alert in recent_alerts[-5:]:  # Show last 5
                severity_emoji = {"critical": "🚨", "high": "⚠️", "warning": "⚠️"}.get(alert["severity"], "ℹ️")
                print(f"{severity_emoji} {alert['message']}")


def main():
    """Main execution function"""
    print("🚀 BizOSaaS Platform - Workflow Monitoring Agent")
    print("=" * 60)
    print("Starting continuous monitoring of all platform services and workflows...")
    print("Press Ctrl+C to stop monitoring")
    print("=" * 60)
    
    # Create and start monitoring agent
    config = MonitoringConfig(
        check_interval=30,  # Check every 30 seconds
        alert_threshold=2,  # Alert after 2 consecutive failures
        performance_threshold=3.0  # Alert if response time > 3 seconds
    )
    
    monitoring_agent = WorkflowMonitoringAgent(config)
    monitoring_agent.start_monitoring()


if __name__ == "__main__":
    main()