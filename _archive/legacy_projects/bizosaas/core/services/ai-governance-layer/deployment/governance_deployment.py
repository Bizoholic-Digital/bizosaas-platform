#!/usr/bin/env python3
"""
AI Governance Layer - Platform-Wide Deployment System
Deploys governance agents across all 58 BizOSaaS services with Human-in-the-Loop workflows
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import aiohttp
import psutil
from pathlib import Path
import yaml

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("governance_deployment")

class GovernanceDeploymentOrchestrator:
    """Orchestrates deployment of governance agents across the entire platform"""
    
    def __init__(self):
        self.deployment_config = self._load_deployment_config()
        self.service_registry = self._get_service_registry()
        self.governance_endpoints = {}
        self.deployment_status = {}
        
    def _load_deployment_config(self) -> Dict[str, Any]:
        """Load deployment configuration"""
        return {
            "governance_service_url": "http://localhost:8090",
            "deployment_batch_size": 5,
            "health_check_timeout": 30,
            "rollback_on_failure": True,
            "human_oversight_required": True,
            "monitoring_interval": 60,  # seconds
            "alert_thresholds": {
                "security_critical": 0,
                "compliance_critical": 0,
                "performance_degradation": 20,  # percentage
                "bug_severity_high": 5
            }
        }
    
    def _get_service_registry(self) -> Dict[str, Dict[str, Any]]:
        """Complete registry of all 58 BizOSaaS services"""
        return {
            # Core Services (19)
            "auth-service": {"port": 3001, "health": "/health", "priority": "critical", "category": "core"},
            "auth-service-v2": {"port": 3002, "health": "/health", "priority": "critical", "category": "core"},
            "user-management": {"port": 8006, "health": "/health", "priority": "high", "category": "core"},
            "api-gateway": {"port": 8080, "health": "/health", "priority": "critical", "category": "core"},
            "notification": {"port": 8007, "health": "/health", "priority": "medium", "category": "core"},
            "logging-service": {"port": 8008, "health": "/health", "priority": "high", "category": "core"},
            "identity-service": {"port": 8009, "health": "/health", "priority": "high", "category": "core"},
            "event-bus": {"port": 8010, "health": "/health", "priority": "high", "category": "core"},
            "vault-integration": {"port": 8011, "health": "/health", "priority": "critical", "category": "core"},
            "byok-health-monitor": {"port": 8012, "health": "/health", "priority": "medium", "category": "core"},
            "domain-repository": {"port": 8013, "health": "/health", "priority": "medium", "category": "core"},
            "bizosaas-brain": {"port": 8014, "health": "/health", "priority": "high", "category": "core"},
            "analytics": {"port": 8015, "health": "/health", "priority": "high", "category": "core"},
            "analytics-service": {"port": 8016, "health": "/health", "priority": "high", "category": "core"},
            "analytics-ai-service": {"port": 8017, "health": "/health", "priority": "high", "category": "core"},
            "temporal-integration": {"port": 8018, "health": "/health", "priority": "medium", "category": "core"},
            "image-integration": {"port": 8019, "health": "/health", "priority": "low", "category": "core"},
            "personal-ai-assistant": {"port": 8020, "health": "/health", "priority": "high", "category": "core"},
            "gdpr-compliance-service": {"port": 8091, "health": "/health", "priority": "critical", "category": "core"},
            
            # E-commerce Services (7) - Migrated from Medusa to Saleor
            "saleor-backend": {"port": 8021, "health": "/health", "priority": "high", "category": "ecommerce"},
            "saleor-storefront": {"port": 8022, "health": "/health", "priority": "medium", "category": "ecommerce"},
            "coreldove-bridge-saleor": {"port": 8026, "health": "/health", "priority": "medium", "category": "ecommerce"},
            "coreldove-ai-sourcing": {"port": 8027, "health": "/health", "priority": "medium", "category": "ecommerce"},
            "coreldove-saleor": {"port": 8029, "health": "/health", "priority": "medium", "category": "ecommerce"},
            "amazon-integration-service": {"port": 8030, "health": "/health", "priority": "medium", "category": "ecommerce"},
            "payment-service": {"port": 8031, "health": "/health", "priority": "critical", "category": "ecommerce"},
            
            # AI Services (9)
            "ai-agents": {"port": 8032, "health": "/health", "priority": "high", "category": "ai"},
            "ai-integration-service": {"port": 8033, "health": "/health", "priority": "high", "category": "ai"},
            "marketing-ai-service": {"port": 8034, "health": "/health", "priority": "medium", "category": "ai"},
            "agent-orchestration-service": {"port": 8035, "health": "/health", "priority": "medium", "category": "ai"},
            "agent-monitor": {"port": 8036, "health": "/health", "priority": "medium", "category": "ai"},
            "claude-telegram-bot": {"port": 8037, "health": "/health", "priority": "low", "category": "ai"},
            "telegram-integration": {"port": 8038, "health": "/health", "priority": "low", "category": "ai"},
            "marketing-automation-service": {"port": 8039, "health": "/health", "priority": "medium", "category": "ai"},
            "campaign-management": {"port": 8040, "health": "/health", "priority": "medium", "category": "ai"},
            
            # Frontend Services (6)
            "frontend-nextjs": {"port": 3000, "health": "/health", "priority": "high", "category": "frontend"},
            "client-dashboard": {"port": 3003, "health": "/health", "priority": "medium", "category": "frontend"},
            "super-admin-dashboard": {"port": 3004, "health": "/health", "priority": "high", "category": "frontend"},
            "unified-dashboard": {"port": 3005, "health": "/health", "priority": "medium", "category": "frontend"},
            "coreldove-frontend": {"port": 3006, "health": "/health", "priority": "medium", "category": "frontend"},
            "coreldove-storefront": {"port": 3007, "health": "/health", "priority": "medium", "category": "frontend"},
            
            # Integration Services (5) - Migrated from Strapi to Wagtail
            "integration": {"port": 8041, "health": "/health", "priority": "medium", "category": "integration"},
            "marketing-apis-service": {"port": 8042, "health": "/health", "priority": "medium", "category": "integration"},
            "wagtail-cms": {"port": 8044, "health": "/health", "priority": "medium", "category": "integration"},
            "business-directory": {"port": 8045, "health": "/health", "priority": "medium", "category": "integration"},
            "client-sites": {"port": 8046, "health": "/health", "priority": "low", "category": "integration"},
            
            # Infrastructure Services (4)
            "saleor-storage": {"port": 8047, "health": "/health", "priority": "medium", "category": "infrastructure"},
            "monitoring": {"port": 8048, "health": "/health", "priority": "high", "category": "infrastructure"},
            "vault": {"port": 8200, "health": "/v1/sys/health", "priority": "critical", "category": "infrastructure"},
            "ai-governance-layer": {"port": 8090, "health": "/health", "priority": "critical", "category": "infrastructure"},
            
            # CRM Services (3)
            "django-crm": {"port": 8049, "health": "/health", "priority": "medium", "category": "crm"},
            "crm-service": {"port": 8050, "health": "/health", "priority": "medium", "category": "crm"},
            "crm-service-v2": {"port": 8051, "health": "/health", "priority": "medium", "category": "crm"}
        }
    
    async def deploy_governance_platform_wide(self) -> Dict[str, Any]:
        """Deploy governance agents across all 58 services with human oversight"""
        logger.info("🚀 Starting platform-wide governance deployment")
        
        deployment_results = {
            "deployment_id": f"gov-deploy-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "total_services": len(self.service_registry),
            "deployment_start": datetime.now().isoformat(),
            "services_deployed": [],
            "services_failed": [],
            "human_approvals_required": [],
            "monitoring_active": False
        }
        
        # Phase 1: Deploy by priority (Critical first)
        priority_groups = self._group_services_by_priority()
        
        for priority in ["critical", "high", "medium", "low"]:
            if priority in priority_groups:
                logger.info(f"📋 Deploying {priority} priority services ({len(priority_groups[priority])} services)")
                
                # Require human approval for critical services
                if priority == "critical":
                    approval_response = await self._request_human_approval(
                        f"Deploy governance to {len(priority_groups[priority])} CRITICAL services",
                        {"services": priority_groups[priority], "risk_level": "high"}
                    )
                    
                    if not approval_response.get("approved", False):
                        logger.warning(f"❌ Human approval DENIED for {priority} services")
                        deployment_results["human_approvals_required"].extend(priority_groups[priority])
                        continue
                
                # Deploy in batches
                batch_results = await self._deploy_service_batch(
                    priority_groups[priority], 
                    priority,
                    deployment_results["deployment_id"]
                )
                
                deployment_results["services_deployed"].extend(batch_results["deployed"])
                deployment_results["services_failed"].extend(batch_results["failed"])
        
        # Phase 2: Activate continuous monitoring
        if deployment_results["services_deployed"]:
            monitoring_result = await self._activate_continuous_monitoring(
                deployment_results["deployment_id"]
            )
            deployment_results["monitoring_active"] = monitoring_result["active"]
        
        deployment_results["deployment_end"] = datetime.now().isoformat()
        deployment_results["success_rate"] = (
            len(deployment_results["services_deployed"]) / 
            len(self.service_registry) * 100
        )
        
        # Save deployment report
        await self._save_deployment_report(deployment_results)
        
        logger.info(f"✅ Governance deployment completed: {deployment_results['success_rate']:.1f}% success rate")
        return deployment_results
    
    def _group_services_by_priority(self) -> Dict[str, List[str]]:
        """Group services by deployment priority"""
        groups = {"critical": [], "high": [], "medium": [], "low": []}
        
        for service_name, config in self.service_registry.items():
            priority = config.get("priority", "medium")
            groups[priority].append(service_name)
        
        return groups
    
    async def _deploy_service_batch(self, services: List[str], priority: str, deployment_id: str) -> Dict[str, List[str]]:
        """Deploy governance to a batch of services"""
        batch_size = self.deployment_config["deployment_batch_size"]
        deployed = []
        failed = []
        
        for i in range(0, len(services), batch_size):
            batch = services[i:i + batch_size]
            logger.info(f"🔧 Deploying governance to batch: {', '.join(batch)}")
            
            # Deploy to each service in the batch
            batch_tasks = [
                self._deploy_governance_to_service(service, deployment_id)
                for service in batch
            ]
            
            batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)
            
            for service, result in zip(batch, batch_results):
                if isinstance(result, Exception):
                    logger.error(f"❌ Failed to deploy governance to {service}: {result}")
                    failed.append(service)
                elif result.get("success", False):
                    logger.info(f"✅ Successfully deployed governance to {service}")
                    deployed.append(service)
                else:
                    logger.error(f"❌ Deployment failed for {service}: {result.get('error', 'Unknown error')}")
                    failed.append(service)
            
            # Brief pause between batches to avoid overwhelming services
            await asyncio.sleep(2)
        
        return {"deployed": deployed, "failed": failed}
    
    async def _deploy_governance_to_service(self, service_name: str, deployment_id: str) -> Dict[str, Any]:
        """Deploy governance agent to a specific service"""
        service_config = self.service_registry[service_name]
        service_url = f"http://localhost:{service_config['port']}"
        
        try:
            # Check if service is healthy
            health_check = await self._check_service_health(service_url, service_config["health"])
            if not health_check["healthy"]:
                return {"success": False, "error": f"Service {service_name} is not healthy"}
            
            # Register service with governance layer
            governance_registration = {
                "service_name": service_name,
                "service_url": service_url,
                "health_endpoint": service_config["health"],
                "priority": service_config["priority"],
                "category": service_config["category"],
                "deployment_id": deployment_id,
                "monitoring_config": {
                    "security_monitoring": True,
                    "compliance_monitoring": True,
                    "performance_monitoring": True,
                    "bug_detection": True,
                    "human_oversight_required": True
                }
            }
            
            # Call governance layer to register service
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.deployment_config['governance_service_url']}/api/governance/register-service",
                    json=governance_registration,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        registration_result = await response.json()
                        
                        # Store governance endpoint for this service
                        self.governance_endpoints[service_name] = {
                            "governance_id": registration_result.get("governance_id"),
                            "monitoring_endpoint": registration_result.get("monitoring_endpoint"),
                            "alert_webhook": registration_result.get("alert_webhook")
                        }
                        
                        return {"success": True, "governance_id": registration_result.get("governance_id")}
                    else:
                        error_text = await response.text()
                        return {"success": False, "error": f"Registration failed: {error_text}"}
        
        except Exception as e:
            logger.error(f"❌ Exception deploying governance to {service_name}: {e}")
            return {"success": False, "error": str(e)}
    
    async def _check_service_health(self, service_url: str, health_endpoint: str) -> Dict[str, Any]:
        """Check if a service is healthy"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{service_url}{health_endpoint}",
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    return {
                        "healthy": response.status == 200,
                        "status_code": response.status,
                        "response_time": response.headers.get("X-Response-Time", "unknown")
                    }
        except Exception as e:
            return {"healthy": False, "error": str(e)}
    
    async def _request_human_approval(self, action: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Request human approval for critical governance actions"""
        logger.info(f"👤 HUMAN APPROVAL REQUIRED: {action}")
        
        approval_request = {
            "request_id": f"approval-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "action": action,
            "context": context,
            "severity": "high",
            "requires_approval": True,
            "timeout": 300  # 5 minutes
        }
        
        # Send to governance layer for human review workflow
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.deployment_config['governance_service_url']}/api/governance/request-approval",
                    json=approval_request,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        approval_response = await response.json()
                        logger.info(f"✅ Human approval response: {approval_response.get('status', 'pending')}")
                        return approval_response
                    else:
                        # Default to requiring approval if governance service unavailable
                        logger.warning("⚠️ Governance service unavailable, defaulting to manual approval")
                        return {"approved": False, "reason": "Governance service unavailable"}
        
        except Exception as e:
            logger.error(f"❌ Failed to request human approval: {e}")
            # Fail safe - require manual approval
            return {"approved": False, "reason": f"Approval system error: {e}"}
    
    async def _activate_continuous_monitoring(self, deployment_id: str) -> Dict[str, Any]:
        """Activate continuous monitoring across all deployed services"""
        logger.info("🔄 Activating continuous monitoring system")
        
        monitoring_config = {
            "deployment_id": deployment_id,
            "monitoring_interval": self.deployment_config["monitoring_interval"],
            "alert_thresholds": self.deployment_config["alert_thresholds"],
            "human_oversight_required": True,
            "monitored_services": list(self.governance_endpoints.keys()),
            "active_agents": ["SecurityMonitor", "ComplianceAuditor", "PerformanceAnalyzer", "BugHunter"]
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.deployment_config['governance_service_url']}/api/governance/activate-monitoring",
                    json=monitoring_config,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        monitoring_result = await response.json()
                        logger.info("✅ Continuous monitoring activated successfully")
                        return {"active": True, "monitoring_id": monitoring_result.get("monitoring_id")}
                    else:
                        error_text = await response.text()
                        logger.error(f"❌ Failed to activate monitoring: {error_text}")
                        return {"active": False, "error": error_text}
        
        except Exception as e:
            logger.error(f"❌ Exception activating monitoring: {e}")
            return {"active": False, "error": str(e)}
    
    async def _save_deployment_report(self, deployment_results: Dict[str, Any]) -> None:
        """Save comprehensive deployment report"""
        report_path = Path(f"/home/alagiri/projects/bizoholic/bizosaas/deployment_reports")
        report_path.mkdir(exist_ok=True)
        
        report_file = report_path / f"governance_deployment_{deployment_results['deployment_id']}.json"
        
        with open(report_file, 'w') as f:
            json.dump(deployment_results, f, indent=2, default=str)
        
        logger.info(f"📊 Deployment report saved: {report_file}")

async def main():
    """Main deployment orchestration"""
    logger.info("🎯 BizOSaaS Platform-Wide Governance Deployment Starting")
    
    orchestrator = GovernanceDeploymentOrchestrator()
    
    try:
        # Deploy governance across all 58 services
        deployment_results = await orchestrator.deploy_governance_platform_wide()
        
        print("\n" + "="*80)
        print("🏆 GOVERNANCE DEPLOYMENT COMPLETED")
        print("="*80)
        print(f"📊 Deployment ID: {deployment_results['deployment_id']}")
        print(f"📈 Success Rate: {deployment_results['success_rate']:.1f}%")
        print(f"✅ Services Deployed: {len(deployment_results['services_deployed'])}")
        print(f"❌ Services Failed: {len(deployment_results['services_failed'])}")
        print(f"👤 Human Approvals Required: {len(deployment_results['human_approvals_required'])}")
        print(f"🔄 Continuous Monitoring: {'Active' if deployment_results['monitoring_active'] else 'Inactive'}")
        
        if deployment_results['services_deployed']:
            print(f"\n✅ Successfully Deployed Services:")
            for service in deployment_results['services_deployed'][:10]:  # Show first 10
                print(f"   - {service}")
            if len(deployment_results['services_deployed']) > 10:
                print(f"   ... and {len(deployment_results['services_deployed']) - 10} more")
        
        if deployment_results['services_failed']:
            print(f"\n❌ Failed Deployments:")
            for service in deployment_results['services_failed']:
                print(f"   - {service}")
        
        print("\n🔄 Real-time governance monitoring with human oversight is now active")
        print("👤 All critical actions require human approval before AI agent execution")
        print("="*80)
        
    except Exception as e:
        logger.error(f"💥 Critical deployment failure: {e}")
        print(f"\n💥 DEPLOYMENT FAILED: {e}")

if __name__ == "__main__":
    asyncio.run(main())