#!/usr/bin/env python3
"""
Governance Agents for BizOSaaS Platform
Specialized AI agents that monitor all 58 services with human oversight
"""

import asyncio
import httpx
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import psutil
import re
import hashlib
from sqlalchemy.orm import Session

# Import from main governance system
from main import (
    GovernanceAgentType, IssueType, IssueSeverity, ActionType,
    IssueDetectionRequest, AIGovernanceOrchestrator
)

logger = logging.getLogger(__name__)

# ========================================================================================
# SPECIALIZED GOVERNANCE AGENTS
# ========================================================================================

@dataclass
class ServiceMetrics:
    """Service metrics for monitoring"""
    service_name: str
    response_time_ms: float
    error_rate: float
    cpu_usage: float
    memory_usage: float
    request_count: int
    last_updated: datetime

@dataclass
class SecurityAlert:
    """Security alert data structure"""
    alert_type: str
    severity: str
    service: str
    description: str
    evidence: Dict[str, Any]
    timestamp: datetime

class BaseGovernanceAgent:
    """Base class for all governance agents"""
    
    def __init__(self, agent_type: GovernanceAgentType, orchestrator: AIGovernanceOrchestrator):
        self.agent_type = agent_type
        self.orchestrator = orchestrator
        self.service_registry = self._get_service_registry()
        self.is_running = False
        self.scan_interval = 300  # 5 minutes default
        
    def _get_service_registry(self) -> Dict[str, Dict[str, Any]]:
        """Get registry of organized BizOSaaS platform services (56 total)"""
        return {
            # Core Services (13) - Located in core/services/
            "auth-service": {"port": 3001, "health": "/health", "priority": "critical", "category": "core"},
            "auth-service-v2": {"port": 3002, "health": "/health", "priority": "critical", "category": "core"},
            "user-management": {"port": 8006, "health": "/health", "priority": "high", "category": "core"},
            "api-gateway": {"port": 8080, "health": "/health", "priority": "critical", "category": "core"},
            "ai-governance-layer": {"port": 8090, "health": "/health", "priority": "critical", "category": "core"},
            "gdpr-compliance-service": {"port": 8091, "health": "/health", "priority": "critical", "category": "core"},
            "wagtail-cms": {"port": 8010, "health": "/admin/", "priority": "high", "category": "core"},
            "vault-integration": {"port": 8200, "health": "/v1/sys/health", "priority": "critical", "category": "core"},
            "logging-service": {"port": 8024, "health": "/health", "priority": "critical", "category": "core"},
            "identity-service": {"port": 8025, "health": "/health", "priority": "high", "category": "core"},
            "event-bus": {"port": 8027, "health": "/health", "priority": "high", "category": "core"},
            "notification": {"port": 8005, "health": "/health", "priority": "high", "category": "core"},
            "byok-health-monitor": {"port": 8029, "health": "/health", "priority": "medium", "category": "core"},
            
            # E-commerce Services (10) - Located in ecommerce/services/
            "saleor-backend": {"port": 8011, "health": "/health/", "priority": "high", "category": "ecommerce"},
            "saleor-storefront": {"port": 3000, "health": "/health", "priority": "high", "category": "ecommerce"},
            "saleor-storage": {"port": 8012, "health": "/health", "priority": "medium", "category": "ecommerce"},
            "coreldove-saleor": {"port": 8013, "health": "/health", "priority": "high", "category": "ecommerce"},
            "coreldove-bridge-saleor": {"port": 8015, "health": "/health", "priority": "medium", "category": "ecommerce"},
            "coreldove-ai-sourcing": {"port": 8016, "health": "/health", "priority": "medium", "category": "ecommerce"},
            "coreldove-frontend": {"port": 3001, "health": "/health", "priority": "high", "category": "ecommerce"},
            "coreldove-storefront": {"port": 3002, "health": "/health", "priority": "high", "category": "ecommerce"},
            "payment-service": {"port": 8004, "health": "/health", "priority": "critical", "category": "ecommerce"},
            "amazon-integration-service": {"port": 8018, "health": "/health", "priority": "medium", "category": "ecommerce"},
            
            # AI Services (10) - Located in ai/services/
            "bizosaas-brain": {"port": 8001, "health": "/health", "priority": "high", "category": "ai"},
            "ai-agents": {"port": 8032, "health": "/health", "priority": "high", "category": "ai"},
            "ai-integration-service": {"port": 8002, "health": "/health", "priority": "high", "category": "ai"},
            "marketing-ai-service": {"port": 8004, "health": "/health", "priority": "medium", "category": "ai"},
            "analytics-ai-service": {"port": 8003, "health": "/health", "priority": "medium", "category": "ai"},
            "agent-orchestration-service": {"port": 8005, "health": "/health", "priority": "high", "category": "ai"},
            "agent-monitor": {"port": 8036, "health": "/health", "priority": "medium", "category": "ai"},
            "claude-telegram-bot": {"port": 4007, "health": "/health", "priority": "medium", "category": "ai"},
            "telegram-integration": {"port": 4007, "health": "/health", "priority": "high", "category": "ai"},
            "marketing-automation-service": {"port": 8009, "health": "/health", "priority": "high", "category": "ai"},
            
            # CRM Services (7) - Located in crm/services/
            "django-crm": {"port": 8007, "health": "/health/", "priority": "high", "category": "crm"},
            "crm-service": {"port": 8008, "health": "/health", "priority": "medium", "category": "crm"},
            "crm-service-v2": {"port": 8009, "health": "/health", "priority": "medium", "category": "crm"},
            "campaign-management": {"port": 8008, "health": "/health", "priority": "high", "category": "crm"},
            "campaign-service": {"port": 8030, "health": "/health", "priority": "medium", "category": "crm"},
            "business-directory": {"port": 8002, "health": "/health", "priority": "medium", "category": "crm"},
            "client-dashboard": {"port": 3005, "health": "/health", "priority": "high", "category": "crm"},
            
            # Integration Services (6) - Located in integration/services/
            "integration": {"port": 8021, "health": "/health", "priority": "medium", "category": "integration"},
            "marketing-apis-service": {"port": 8019, "health": "/health", "priority": "medium", "category": "integration"},
            "temporal-integration": {"port": 8022, "health": "/health", "priority": "medium", "category": "integration"},
            "temporal-orchestration": {"port": 8023, "health": "/health", "priority": "medium", "category": "integration"},
            "image-integration": {"port": 8020, "health": "/health", "priority": "low", "category": "integration"},
            "client-sites": {"port": 3007, "health": "/health", "priority": "medium", "category": "integration"},
            
            # Analytics Services (2) - Located in analytics/services/
            "analytics": {"port": 8028, "health": "/health", "priority": "medium", "category": "analytics"},
            "analytics-service": {"port": 8003, "health": "/health", "priority": "high", "category": "analytics"},
            
            # Frontend Applications (4) - Located in frontend/apps/
            "bizoholic-frontend": {"port": 3003, "health": "/health", "priority": "high", "category": "frontend"},
            "bizosaas-admin": {"port": 3004, "health": "/health", "priority": "high", "category": "frontend"},
            "client-portal": {"port": 3005, "health": "/health", "priority": "high", "category": "frontend"},
            "coreldove-frontend-app": {"port": 3006, "health": "/health", "priority": "high", "category": "frontend"},
            
            # Misc Services (8) - Located in misc/services/
            "frontend-nextjs": {"port": 3000, "health": "/api/health", "priority": "high", "category": "misc"},
            "domain-repository": {"port": 8026, "health": "/health", "priority": "medium", "category": "misc"},
            "gamification-service": {"port": 8031, "health": "/health", "priority": "medium", "category": "misc"},
            "coreldove-bridge": {"port": 8014, "health": "/health", "priority": "medium", "category": "misc"},
            "coreldove-sourcing": {"port": 8017, "health": "/health", "priority": "medium", "category": "misc"},
            "super-admin-dashboard": {"port": 3004, "health": "/health", "priority": "high", "category": "misc"},
            "unified-dashboard": {"port": 3006, "health": "/health", "priority": "high", "category": "misc"}
        }
    
    async def start_monitoring(self):
        """Start continuous monitoring"""
        self.is_running = True
        logger.info(f"Starting {self.agent_type.value} monitoring")
        
        while self.is_running:
            try:
                await self.scan_services()
                await asyncio.sleep(self.scan_interval)
            except Exception as e:
                logger.error(f"Error in {self.agent_type.value} monitoring: {e}")
                await asyncio.sleep(60)  # Wait before retrying
    
    async def stop_monitoring(self):
        """Stop monitoring"""
        self.is_running = False
        logger.info(f"Stopped {self.agent_type.value} monitoring")
    
    async def scan_services(self):
        """Abstract method - implemented by each agent"""
        raise NotImplementedError
    
    async def report_issue(
        self,
        service_name: str,
        issue_type: IssueType,
        severity: IssueSeverity,
        title: str,
        description: str,
        evidence: Dict[str, Any],
        recommended_action: ActionType,
        confidence: int = 85
    ):
        """Report issue to governance orchestrator with human review requirement"""
        
        detection_request = IssueDetectionRequest(
            agent_type=self.agent_type,
            service_name=service_name,
            issue_type=issue_type,
            severity=severity,
            title=title,
            description=description,
            evidence=evidence,
            ai_confidence=confidence,
            recommended_action=recommended_action
        )
        
        # All issues require human review before any action
        issue_id = await self.orchestrator.detect_issue(detection_request, db=None)  # Will need DB session
        
        logger.info(f"Issue reported: {issue_id} - {title} (requires human approval)")
        return issue_id

class SecurityMonitorAgent(BaseGovernanceAgent):
    """Agent that monitors security across all services"""
    
    def __init__(self, orchestrator: AIGovernanceOrchestrator):
        super().__init__(GovernanceAgentType.SECURITY_MONITOR, orchestrator)
        self.scan_interval = 60  # 1 minute for security
        self.security_patterns = self._load_security_patterns()
    
    def _load_security_patterns(self) -> Dict[str, List[str]]:
        """Load security vulnerability patterns"""
        return {
            "sql_injection": [
                r"SELECT.*FROM.*WHERE.*=.*'",
                r"UNION.*SELECT",
                r"DROP.*TABLE",
                r"INSERT.*INTO.*VALUES"
            ],
            "xss_attempts": [
                r"<script.*>",
                r"javascript:",
                r"on\w+\s*=",
                r"eval\s*\("
            ],
            "authentication_bypass": [
                r"admin.*password.*=.*''",
                r"OR.*1=1",
                r"bypass.*auth",
                r"skip.*login"
            ],
            "suspicious_file_access": [
                r"\.\.\/",
                r"\/etc\/passwd",
                r"\/etc\/shadow",
                r"config\.php"
            ]
        }
    
    async def scan_services(self):
        """Scan all services for security vulnerabilities"""
        
        for service_name, config in self.service_registry.items():
            try:
                # Check service health and response
                security_status = await self._check_service_security(service_name, config)
                
                if security_status["vulnerabilities"]:
                    for vuln in security_status["vulnerabilities"]:
                        await self.report_issue(
                            service_name=service_name,
                            issue_type=IssueType.SECURITY_VULNERABILITY,
                            severity=self._assess_security_severity(vuln),
                            title=f"Security Vulnerability: {vuln['type']}",
                            description=f"Security vulnerability detected in {service_name}: {vuln['description']}",
                            evidence={
                                "vulnerability_type": vuln["type"],
                                "detection_method": vuln["method"],
                                "risk_level": vuln["risk"],
                                "affected_endpoint": vuln.get("endpoint"),
                                "scan_timestamp": datetime.utcnow().isoformat()
                            },
                            recommended_action=ActionType.SECURITY_PATCH,
                            confidence=vuln["confidence"]
                        )
                
            except Exception as e:
                logger.error(f"Security scan failed for {service_name}: {e}")
    
    async def _check_service_security(self, service_name: str, config: Dict) -> Dict[str, Any]:
        """Check security of individual service"""
        
        vulnerabilities = []
        
        try:
            # Check for insecure endpoints
            insecure_endpoints = await self._scan_endpoints(service_name, config)
            vulnerabilities.extend(insecure_endpoints)
            
            # Check for weak authentication
            auth_issues = await self._check_authentication(service_name, config)
            vulnerabilities.extend(auth_issues)
            
            # Check for exposed sensitive data
            data_exposure = await self._check_data_exposure(service_name, config)
            vulnerabilities.extend(data_exposure)
            
            # Check for outdated dependencies
            dependency_issues = await self._check_dependencies(service_name)
            vulnerabilities.extend(dependency_issues)
            
        except Exception as e:
            logger.error(f"Security check failed for {service_name}: {e}")
        
        return {
            "service": service_name,
            "scan_timestamp": datetime.utcnow().isoformat(),
            "vulnerabilities": vulnerabilities,
            "security_score": self._calculate_security_score(vulnerabilities)
        }
    
    async def _scan_endpoints(self, service_name: str, config: Dict) -> List[Dict]:
        """Scan service endpoints for vulnerabilities"""
        vulnerabilities = []
        
        try:
            base_url = f"http://localhost:{config['port']}"
            
            # Test common vulnerable endpoints
            test_endpoints = [
                "/admin",
                "/debug",
                "/test",
                "/api/users",
                "/api/admin",
                config.get("health", "/health")
            ]
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                for endpoint in test_endpoints:
                    try:
                        # Test for SQL injection
                        sqli_payload = "' OR '1'='1"
                        response = await client.get(f"{base_url}{endpoint}?id={sqli_payload}")
                        
                        if self._detect_sql_injection_response(response.text):
                            vulnerabilities.append({
                                "type": "sql_injection",
                                "endpoint": endpoint,
                                "method": "payload_injection",
                                "risk": "high",
                                "confidence": 90,
                                "description": f"Potential SQL injection vulnerability at {endpoint}"
                            })
                        
                        # Test for XSS
                        xss_payload = "<script>alert('xss')</script>"
                        response = await client.get(f"{base_url}{endpoint}?data={xss_payload}")
                        
                        if xss_payload in response.text:
                            vulnerabilities.append({
                                "type": "xss",
                                "endpoint": endpoint,
                                "method": "script_injection",
                                "risk": "medium",
                                "confidence": 85,
                                "description": f"Potential XSS vulnerability at {endpoint}"
                            })
                        
                        # Check for sensitive information exposure
                        if self._detect_sensitive_data(response.text):
                            vulnerabilities.append({
                                "type": "information_disclosure",
                                "endpoint": endpoint,
                                "method": "response_analysis",
                                "risk": "medium",
                                "confidence": 75,
                                "description": f"Sensitive information exposed at {endpoint}"
                            })
                        
                    except Exception as e:
                        logger.debug(f"Endpoint scan failed for {endpoint}: {e}")
                        
        except Exception as e:
            logger.error(f"Endpoint scanning failed for {service_name}: {e}")
        
        return vulnerabilities
    
    async def _check_authentication(self, service_name: str, config: Dict) -> List[Dict]:
        """Check for authentication vulnerabilities"""
        vulnerabilities = []
        
        try:
            base_url = f"http://localhost:{config['port']}"
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Test for missing authentication
                auth_endpoints = ["/api/admin", "/admin", "/dashboard"]
                
                for endpoint in auth_endpoints:
                    try:
                        response = await client.get(f"{base_url}{endpoint}")
                        
                        if response.status_code == 200 and "login" not in response.text.lower():
                            vulnerabilities.append({
                                "type": "missing_authentication",
                                "endpoint": endpoint,
                                "method": "access_control_test",
                                "risk": "high",
                                "confidence": 80,
                                "description": f"Protected endpoint {endpoint} accessible without authentication"
                            })
                    except:
                        pass
                
                # Test for weak session management
                login_endpoints = ["/login", "/auth", "/api/auth/login"]
                
                for endpoint in login_endpoints:
                    try:
                        # Test for session fixation
                        response = await client.post(f"{base_url}{endpoint}", 
                                                   data={"username": "test", "password": "test"})
                        
                        if "session" in response.headers.get("set-cookie", "").lower():
                            # Check for secure session cookies
                            cookie_header = response.headers.get("set-cookie", "")
                            if "secure" not in cookie_header.lower() or "httponly" not in cookie_header.lower():
                                vulnerabilities.append({
                                    "type": "insecure_session",
                                    "endpoint": endpoint,
                                    "method": "cookie_analysis",
                                    "risk": "medium",
                                    "confidence": 70,
                                    "description": f"Insecure session cookies at {endpoint}"
                                })
                    except:
                        pass
                        
        except Exception as e:
            logger.error(f"Authentication check failed for {service_name}: {e}")
        
        return vulnerabilities
    
    async def _check_data_exposure(self, service_name: str, config: Dict) -> List[Dict]:
        """Check for sensitive data exposure"""
        vulnerabilities = []
        
        try:
            base_url = f"http://localhost:{config['port']}"
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Check common endpoints for data exposure
                data_endpoints = [
                    "/api/users",
                    "/api/config", 
                    "/api/debug",
                    "/debug",
                    "/.env",
                    "/config.json"
                ]
                
                for endpoint in data_endpoints:
                    try:
                        response = await client.get(f"{base_url}{endpoint}")
                        
                        if response.status_code == 200:
                            # Check for exposed sensitive data patterns
                            sensitive_patterns = [
                                r"password.*[:=].*['\"].*['\"]",
                                r"api_key.*[:=].*['\"].*['\"]",
                                r"secret.*[:=].*['\"].*['\"]",
                                r"token.*[:=].*['\"].*['\"]",
                                r"database.*[:=].*['\"].*['\"]"
                            ]
                            
                            for pattern in sensitive_patterns:
                                if re.search(pattern, response.text, re.IGNORECASE):
                                    vulnerabilities.append({
                                        "type": "sensitive_data_exposure",
                                        "endpoint": endpoint,
                                        "method": "pattern_matching",
                                        "risk": "high",
                                        "confidence": 85,
                                        "description": f"Sensitive data exposed at {endpoint}"
                                    })
                                    break
                    except:
                        pass
                        
        except Exception as e:
            logger.error(f"Data exposure check failed for {service_name}: {e}")
        
        return vulnerabilities
    
    async def _check_dependencies(self, service_name: str) -> List[Dict]:
        """Check for vulnerable dependencies"""
        vulnerabilities = []
        
        # This would integrate with vulnerability databases
        # For now, return placeholder
        return vulnerabilities
    
    def _detect_sql_injection_response(self, response_text: str) -> bool:
        """Detect SQL injection vulnerability indicators"""
        sql_error_patterns = [
            "sql syntax",
            "mysql_fetch",
            "ora-\d+",
            "postgresql.*error",
            "sqlite.*error",
            "database error"
        ]
        
        for pattern in sql_error_patterns:
            if re.search(pattern, response_text, re.IGNORECASE):
                return True
        return False
    
    def _detect_sensitive_data(self, response_text: str) -> bool:
        """Detect sensitive information in response"""
        sensitive_patterns = [
            r"password.*[:=]",
            r"api_key.*[:=]",
            r"secret.*[:=]",
            r"token.*[:=]",
            r"credit_card.*[:=]",
            r"ssn.*[:=]"
        ]
        
        for pattern in sensitive_patterns:
            if re.search(pattern, response_text, re.IGNORECASE):
                return True
        return False
    
    def _calculate_security_score(self, vulnerabilities: List[Dict]) -> int:
        """Calculate security score (0-100)"""
        if not vulnerabilities:
            return 100
        
        total_risk = 0
        for vuln in vulnerabilities:
            risk_scores = {"low": 10, "medium": 30, "high": 50, "critical": 100}
            total_risk += risk_scores.get(vuln["risk"], 10)
        
        # Cap at 100 and invert (higher vulnerabilities = lower score)
        security_score = max(0, 100 - min(100, total_risk))
        return security_score
    
    def _assess_security_severity(self, vulnerability: Dict) -> IssueSeverity:
        """Assess severity of security vulnerability"""
        risk_to_severity = {
            "critical": IssueSeverity.CRITICAL,
            "high": IssueSeverity.HIGH,
            "medium": IssueSeverity.MEDIUM,
            "low": IssueSeverity.LOW
        }
        return risk_to_severity.get(vulnerability["risk"], IssueSeverity.MEDIUM)

class ComplianceAuditorAgent(BaseGovernanceAgent):
    """Agent that monitors GDPR and compliance across all services"""
    
    def __init__(self, orchestrator: AIGovernanceOrchestrator):
        super().__init__(GovernanceAgentType.COMPLIANCE_AUDITOR, orchestrator)
        self.scan_interval = 300  # 5 minutes for compliance
    
    async def scan_services(self):
        """Scan all services for compliance violations"""
        
        for service_name, config in self.service_registry.items():
            try:
                compliance_status = await self._check_service_compliance(service_name, config)
                
                if compliance_status["violations"]:
                    for violation in compliance_status["violations"]:
                        await self.report_issue(
                            service_name=service_name,
                            issue_type=IssueType.GDPR_VIOLATION if violation["type"] == "gdpr" else IssueType.COMPLIANCE_VIOLATION,
                            severity=self._assess_compliance_severity(violation),
                            title=f"Compliance Violation: {violation['regulation']}",
                            description=f"Compliance violation in {service_name}: {violation['description']}",
                            evidence=violation["evidence"],
                            recommended_action=ActionType.COMPLIANCE_UPDATE,
                            confidence=violation["confidence"]
                        )
                
            except Exception as e:
                logger.error(f"Compliance scan failed for {service_name}: {e}")
    
    async def _check_service_compliance(self, service_name: str, config: Dict) -> Dict[str, Any]:
        """Check compliance of individual service"""
        
        violations = []
        
        # Check GDPR compliance
        gdpr_violations = await self._check_gdpr_compliance(service_name, config)
        violations.extend(gdpr_violations)
        
        # Check data retention policies
        retention_violations = await self._check_data_retention(service_name, config)
        violations.extend(retention_violations)
        
        # Check consent management
        consent_violations = await self._check_consent_management(service_name, config)
        violations.extend(consent_violations)
        
        return {
            "service": service_name,
            "scan_timestamp": datetime.utcnow().isoformat(),
            "violations": violations,
            "compliance_score": self._calculate_compliance_score(violations)
        }
    
    async def _check_gdpr_compliance(self, service_name: str, config: Dict) -> List[Dict]:
        """Check GDPR compliance"""
        violations = []
        
        try:
            base_url = f"http://localhost:{config['port']}"
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Check for GDPR endpoints
                gdpr_endpoints = [
                    "/api/gdpr/export",
                    "/api/gdpr/delete", 
                    "/api/data/export",
                    "/api/data/delete",
                    "/api/privacy/export",
                    "/api/privacy/delete"
                ]
                
                has_gdpr_endpoints = False
                for endpoint in gdpr_endpoints:
                    try:
                        response = await client.get(f"{base_url}{endpoint}")
                        if response.status_code in [200, 405]:  # 405 = Method not allowed (endpoint exists)
                            has_gdpr_endpoints = True
                            break
                    except:
                        pass
                
                if not has_gdpr_endpoints and service_name in ["user-management", "django-crm", "auth-service"]:
                    violations.append({
                        "type": "gdpr",
                        "regulation": "GDPR Article 17 & 20",
                        "description": "Missing GDPR data export/deletion endpoints",
                        "confidence": 90,
                        "risk": "high",
                        "evidence": {
                            "missing_endpoints": gdpr_endpoints,
                            "service_handles_personal_data": True
                        }
                    })
                
                # Check for privacy policy endpoint
                try:
                    response = await client.get(f"{base_url}/privacy-policy")
                    if response.status_code == 404:
                        violations.append({
                            "type": "gdpr",
                            "regulation": "GDPR Article 13",
                            "description": "Missing privacy policy endpoint",
                            "confidence": 85,
                            "risk": "medium",
                            "evidence": {
                                "missing_privacy_policy": True
                            }
                        })
                except:
                    pass
        
        except Exception as e:
            logger.error(f"GDPR compliance check failed for {service_name}: {e}")
        
        return violations
    
    async def _check_data_retention(self, service_name: str, config: Dict) -> List[Dict]:
        """Check data retention policies"""
        violations = []
        
        # This would check for proper data retention policies
        # For now, return placeholder
        return violations
    
    async def _check_consent_management(self, service_name: str, config: Dict) -> List[Dict]:
        """Check consent management implementation"""
        violations = []
        
        try:
            base_url = f"http://localhost:{config['port']}"
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                consent_endpoints = [
                    "/api/consent",
                    "/api/privacy/consent",
                    "/api/gdpr/consent"
                ]
                
                has_consent_management = False
                for endpoint in consent_endpoints:
                    try:
                        response = await client.get(f"{base_url}{endpoint}")
                        if response.status_code in [200, 405]:
                            has_consent_management = True
                            break
                    except:
                        pass
                
                if not has_consent_management and service_name in ["auth-service", "user-management"]:
                    violations.append({
                        "type": "gdpr",
                        "regulation": "GDPR Article 6 & 7",
                        "description": "Missing consent management system",
                        "confidence": 80,
                        "risk": "medium",
                        "evidence": {
                            "missing_consent_endpoints": consent_endpoints
                        }
                    })
        
        except Exception as e:
            logger.error(f"Consent management check failed for {service_name}: {e}")
        
        return violations
    
    def _calculate_compliance_score(self, violations: List[Dict]) -> int:
        """Calculate compliance score (0-100)"""
        if not violations:
            return 100
        
        total_risk = 0
        for violation in violations:
            risk_scores = {"low": 5, "medium": 15, "high": 30, "critical": 50}
            total_risk += risk_scores.get(violation["risk"], 5)
        
        compliance_score = max(0, 100 - min(100, total_risk))
        return compliance_score
    
    def _assess_compliance_severity(self, violation: Dict) -> IssueSeverity:
        """Assess severity of compliance violation"""
        if violation["type"] == "gdpr":
            # GDPR violations are always high priority
            risk_to_severity = {
                "critical": IssueSeverity.CRITICAL,
                "high": IssueSeverity.HIGH,
                "medium": IssueSeverity.HIGH,  # Elevated for GDPR
                "low": IssueSeverity.MEDIUM
            }
        else:
            risk_to_severity = {
                "critical": IssueSeverity.CRITICAL,
                "high": IssueSeverity.HIGH,
                "medium": IssueSeverity.MEDIUM,
                "low": IssueSeverity.LOW
            }
        
        return risk_to_severity.get(violation["risk"], IssueSeverity.MEDIUM)

class PerformanceAnalyzerAgent(BaseGovernanceAgent):
    """Agent that monitors performance across all services"""
    
    def __init__(self, orchestrator: AIGovernanceOrchestrator):
        super().__init__(GovernanceAgentType.PERFORMANCE_ANALYZER, orchestrator)
        self.scan_interval = 120  # 2 minutes for performance
        self.performance_thresholds = {
            "response_time_ms": 2000,    # 2 seconds
            "error_rate_percent": 5,     # 5%
            "cpu_usage_percent": 80,     # 80%
            "memory_usage_percent": 85,  # 85%
            "disk_usage_percent": 90     # 90%
        }
    
    async def scan_services(self):
        """Scan all services for performance issues"""
        
        for service_name, config in self.service_registry.items():
            try:
                performance_metrics = await self._get_service_metrics(service_name, config)
                
                issues = self._analyze_performance_metrics(service_name, performance_metrics)
                
                for issue in issues:
                    await self.report_issue(
                        service_name=service_name,
                        issue_type=IssueType.PERFORMANCE_DEGRADATION,
                        severity=issue["severity"],
                        title=f"Performance Issue: {issue['metric']}",
                        description=issue["description"],
                        evidence=issue["evidence"],
                        recommended_action=ActionType.PERFORMANCE_OPTIMIZATION,
                        confidence=issue["confidence"]
                    )
                
            except Exception as e:
                logger.error(f"Performance scan failed for {service_name}: {e}")
    
    async def _get_service_metrics(self, service_name: str, config: Dict) -> Dict[str, Any]:
        """Get performance metrics for a service"""
        
        metrics = {
            "service_name": service_name,
            "timestamp": datetime.utcnow().isoformat(),
            "response_time_ms": 0,
            "error_rate_percent": 0,
            "cpu_usage_percent": 0,
            "memory_usage_percent": 0,
            "request_count": 0,
            "status": "unknown"
        }
        
        try:
            base_url = f"http://localhost:{config['port']}"
            health_endpoint = config.get("health", "/health")
            
            # Measure response time
            start_time = datetime.utcnow()
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{base_url}{health_endpoint}")
                
                end_time = datetime.utcnow()
                response_time_ms = (end_time - start_time).total_seconds() * 1000
                
                metrics.update({
                    "response_time_ms": response_time_ms,
                    "status": "healthy" if response.status_code == 200 else "unhealthy",
                    "http_status": response.status_code
                })
                
                # Try to get additional metrics from service if available
                try:
                    metrics_response = await client.get(f"{base_url}/metrics")
                    if metrics_response.status_code == 200:
                        service_metrics = metrics_response.json()
                        metrics.update(service_metrics)
                except:
                    pass
        
        except Exception as e:
            metrics.update({
                "status": "error",
                "error": str(e),
                "response_time_ms": 30000  # Timeout
            })
        
        # Get system metrics for the service (if accessible)
        try:
            # This would require process monitoring
            # For now, use placeholder values
            metrics.update({
                "cpu_usage_percent": 45,  # Placeholder
                "memory_usage_percent": 60  # Placeholder
            })
        except:
            pass
        
        return metrics
    
    def _analyze_performance_metrics(self, service_name: str, metrics: Dict[str, Any]) -> List[Dict]:
        """Analyze metrics and identify performance issues"""
        
        issues = []
        
        # Check response time
        if metrics["response_time_ms"] > self.performance_thresholds["response_time_ms"]:
            severity = IssueSeverity.HIGH if metrics["response_time_ms"] > 5000 else IssueSeverity.MEDIUM
            issues.append({
                "metric": "response_time",
                "severity": severity,
                "description": f"High response time: {metrics['response_time_ms']:.0f}ms (threshold: {self.performance_thresholds['response_time_ms']}ms)",
                "confidence": 95,
                "evidence": {
                    "current_response_time": metrics["response_time_ms"],
                    "threshold": self.performance_thresholds["response_time_ms"],
                    "service_status": metrics["status"]
                }
            })
        
        # Check CPU usage
        if metrics["cpu_usage_percent"] > self.performance_thresholds["cpu_usage_percent"]:
            severity = IssueSeverity.HIGH if metrics["cpu_usage_percent"] > 95 else IssueSeverity.MEDIUM
            issues.append({
                "metric": "cpu_usage",
                "severity": severity,
                "description": f"High CPU usage: {metrics['cpu_usage_percent']:.1f}% (threshold: {self.performance_thresholds['cpu_usage_percent']}%)",
                "confidence": 90,
                "evidence": {
                    "current_cpu_usage": metrics["cpu_usage_percent"],
                    "threshold": self.performance_thresholds["cpu_usage_percent"]
                }
            })
        
        # Check memory usage
        if metrics["memory_usage_percent"] > self.performance_thresholds["memory_usage_percent"]:
            severity = IssueSeverity.HIGH if metrics["memory_usage_percent"] > 95 else IssueSeverity.MEDIUM
            issues.append({
                "metric": "memory_usage",
                "severity": severity,
                "description": f"High memory usage: {metrics['memory_usage_percent']:.1f}% (threshold: {self.performance_thresholds['memory_usage_percent']}%)",
                "confidence": 90,
                "evidence": {
                    "current_memory_usage": metrics["memory_usage_percent"],
                    "threshold": self.performance_thresholds["memory_usage_percent"]
                }
            })
        
        # Check service availability
        if metrics["status"] != "healthy":
            issues.append({
                "metric": "availability",
                "severity": IssueSeverity.CRITICAL,
                "description": f"Service unavailable or unhealthy: {metrics['status']}",
                "confidence": 100,
                "evidence": {
                    "service_status": metrics["status"],
                    "http_status": metrics.get("http_status"),
                    "error": metrics.get("error")
                }
            })
        
        return issues

class BugHunterAgent(BaseGovernanceAgent):
    """Agent that detects bugs and anomalies across all services"""
    
    def __init__(self, orchestrator: AIGovernanceOrchestrator):
        super().__init__(GovernanceAgentType.BUG_HUNTER, orchestrator)
        self.scan_interval = 180  # 3 minutes for bug detection
    
    async def scan_services(self):
        """Scan all services for bugs and errors"""
        
        for service_name, config in self.service_registry.items():
            try:
                bug_analysis = await self._analyze_service_for_bugs(service_name, config)
                
                for bug in bug_analysis["bugs"]:
                    await self.report_issue(
                        service_name=service_name,
                        issue_type=IssueType.BUG_DETECTED,
                        severity=bug["severity"],
                        title=f"Bug Detected: {bug['type']}",
                        description=bug["description"],
                        evidence=bug["evidence"],
                        recommended_action=ActionType.AUTO_FIX,
                        confidence=bug["confidence"]
                    )
                
            except Exception as e:
                logger.error(f"Bug detection failed for {service_name}: {e}")
    
    async def _analyze_service_for_bugs(self, service_name: str, config: Dict) -> Dict[str, Any]:
        """Analyze service for potential bugs"""
        
        bugs = []
        
        try:
            # Check for error patterns in responses
            error_patterns = await self._check_error_patterns(service_name, config)
            bugs.extend(error_patterns)
            
            # Check for inconsistent behavior
            consistency_issues = await self._check_consistency(service_name, config)
            bugs.extend(consistency_issues)
            
            # Check for timeout issues
            timeout_issues = await self._check_timeouts(service_name, config)
            bugs.extend(timeout_issues)
            
        except Exception as e:
            logger.error(f"Bug analysis failed for {service_name}: {e}")
        
        return {
            "service": service_name,
            "scan_timestamp": datetime.utcnow().isoformat(),
            "bugs": bugs
        }
    
    async def _check_error_patterns(self, service_name: str, config: Dict) -> List[Dict]:
        """Check for error patterns in service responses"""
        bugs = []
        
        try:
            base_url = f"http://localhost:{config['port']}"
            
            # Test various endpoints for error patterns
            test_endpoints = [
                config.get("health", "/health"),
                "/api/status",
                "/api/version",
                "/debug"
            ]
            
            async with httpx.AsyncClient(timeout=5.0) as client:
                for endpoint in test_endpoints:
                    try:
                        response = await client.get(f"{base_url}{endpoint}")
                        
                        # Check for error indicators
                        if self._contains_error_indicators(response.text):
                            bugs.append({
                                "type": "error_in_response",
                                "severity": IssueSeverity.MEDIUM,
                                "description": f"Error indicators found in response from {endpoint}",
                                "confidence": 75,
                                "evidence": {
                                    "endpoint": endpoint,
                                    "status_code": response.status_code,
                                    "response_preview": response.text[:500]
                                }
                            })
                        
                        # Check for stack traces
                        if self._contains_stack_trace(response.text):
                            bugs.append({
                                "type": "exposed_stack_trace",
                                "severity": IssueSeverity.HIGH,
                                "description": f"Stack trace exposed in response from {endpoint}",
                                "confidence": 90,
                                "evidence": {
                                    "endpoint": endpoint,
                                    "status_code": response.status_code
                                }
                            })
                    
                    except httpx.TimeoutException:
                        bugs.append({
                            "type": "timeout",
                            "severity": IssueSeverity.MEDIUM,
                            "description": f"Timeout accessing {endpoint}",
                            "confidence": 85,
                            "evidence": {
                                "endpoint": endpoint,
                                "timeout_seconds": 5
                            }
                        })
                    except Exception as e:
                        if "connection" in str(e).lower():
                            bugs.append({
                                "type": "connection_error",
                                "severity": IssueSeverity.HIGH,
                                "description": f"Connection error accessing {endpoint}: {str(e)}",
                                "confidence": 90,
                                "evidence": {
                                    "endpoint": endpoint,
                                    "error": str(e)
                                }
                            })
        
        except Exception as e:
            logger.error(f"Error pattern check failed for {service_name}: {e}")
        
        return bugs
    
    async def _check_consistency(self, service_name: str, config: Dict) -> List[Dict]:
        """Check for inconsistent behavior"""
        bugs = []
        
        # This would check for inconsistent responses, data, etc.
        # For now, return placeholder
        return bugs
    
    async def _check_timeouts(self, service_name: str, config: Dict) -> List[Dict]:
        """Check for timeout issues"""
        bugs = []
        
        # This would check for systematic timeout issues
        # For now, return placeholder
        return bugs
    
    def _contains_error_indicators(self, response_text: str) -> bool:
        """Check if response contains error indicators"""
        error_indicators = [
            "error",
            "exception",
            "failed",
            "traceback",
            "internal server error",
            "500",
            "404",
            "timeout"
        ]
        
        response_lower = response_text.lower()
        return any(indicator in response_lower for indicator in error_indicators)
    
    def _contains_stack_trace(self, response_text: str) -> bool:
        """Check if response contains stack trace"""
        stack_trace_patterns = [
            r"traceback.*most recent call last",
            r"at.*\(.*\.py:\d+\)",
            r"file.*line \d+",
            r"stack trace:",
            r"exception.*:",
            r"error.*at line \d+"
        ]
        
        for pattern in stack_trace_patterns:
            if re.search(pattern, response_text, re.IGNORECASE):
                return True
        return False

# ========================================================================================
# GOVERNANCE AGENT MANAGER
# ========================================================================================

class GovernanceAgentManager:
    """Manager for all governance agents with human oversight"""
    
    def __init__(self, orchestrator: AIGovernanceOrchestrator):
        self.orchestrator = orchestrator
        self.agents = {}
        self.is_running = False
    
    async def start_all_agents(self):
        """Start all governance agents"""
        
        # Initialize all agent types
        agent_classes = {
            GovernanceAgentType.SECURITY_MONITOR: SecurityMonitorAgent,
            GovernanceAgentType.COMPLIANCE_AUDITOR: ComplianceAuditorAgent,
            GovernanceAgentType.PERFORMANCE_ANALYZER: PerformanceAnalyzerAgent,
            GovernanceAgentType.BUG_HUNTER: BugHunterAgent
        }
        
        for agent_type, agent_class in agent_classes.items():
            agent = agent_class(self.orchestrator)
            self.agents[agent_type] = agent
            
            # Start monitoring in background
            asyncio.create_task(agent.start_monitoring())
        
        self.is_running = True
        logger.info(f"Started {len(self.agents)} governance agents with human oversight")
    
    async def stop_all_agents(self):
        """Stop all governance agents"""
        
        for agent in self.agents.values():
            await agent.stop_monitoring()
        
        self.is_running = False
        logger.info("Stopped all governance agents")
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        
        return {
            "total_agents": len(self.agents),
            "active_agents": sum(1 for agent in self.agents.values() if agent.is_running),
            "agents": {
                agent_type.value: {
                    "is_running": agent.is_running,
                    "scan_interval": agent.scan_interval,
                    "monitored_services": len(agent.service_registry)
                }
                for agent_type, agent in self.agents.items()
            },
            "human_oversight": {
                "all_issues_require_human_approval": True,
                "no_automated_actions_without_approval": True,
                "comprehensive_audit_trail": True
            }
        }

# Example usage
if __name__ == "__main__":
    async def main():
        orchestrator = AIGovernanceOrchestrator()
        agent_manager = GovernanceAgentManager(orchestrator)
        
        await agent_manager.start_all_agents()
        
        # Keep running
        try:
            while True:
                await asyncio.sleep(60)
                status = agent_manager.get_agent_status()
                logger.info(f"Agent status: {status['active_agents']}/{status['total_agents']} active")
        except KeyboardInterrupt:
            await agent_manager.stop_all_agents()
    
    asyncio.run(main())