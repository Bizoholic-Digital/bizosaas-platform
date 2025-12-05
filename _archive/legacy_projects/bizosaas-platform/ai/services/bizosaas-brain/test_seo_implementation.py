#!/usr/bin/env python3
"""
SEO Implementation Test Script
Validates the Bizoholic SEO Service Delivery Workflow implementation

This script tests the core functionality of the SEO system to ensure
proper integration and functionality before deployment.
"""

import asyncio
import sys
import os
import json
from datetime import datetime
from typing import Dict, Any

# Add the current directory to Python path
sys.path.append(os.path.dirname(__file__))

# Test imports
try:
    from bizoholic_seo_agents import (
        BizoholicSEOOrchestrator,
        SEOWorkflowType,
        SEOWorkflowConfig,
        HITLApprovalLevel,
        TechnicalSEOAgent,
        KeywordResearchAgent,
        ContentOptimizationAgent,
        LinkBuildingAgent,
        seo_orchestrator
    )
    print("✅ SEO Agents import successful")
except ImportError as e:
    print(f"❌ SEO Agents import failed: {e}")
    sys.exit(1)

try:
    from bizoholic_seo_service import (
        SEOWorkflowRequest,
        SEOWorkflowResponse,
        BizoholicSEOService,
        seo_service
    )
    print("✅ SEO Service import successful")
except ImportError as e:
    print(f"❌ SEO Service import failed: {e}")
    sys.exit(1)

try:
    from app.models.seo_models import (
        SEOWorkflowCreate,
        SEOWorkflowResponse as ModelResponse,
        SEOInsightResponse
    )
    print("✅ SEO Models import successful")
except ImportError as e:
    print(f"❌ SEO Models import failed: {e}")
    sys.exit(1)

class SEOImplementationTester:
    """Test suite for SEO implementation validation"""
    
    def __init__(self):
        self.test_results = {}
        self.failed_tests = 0
        self.passed_tests = 0
    
    def log_test(self, test_name: str, passed: bool, message: str = ""):
        """Log test results"""
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status}: {test_name}")
        if message:
            print(f"   {message}")
        
        self.test_results[test_name] = {
            "passed": passed,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        
        if passed:
            self.passed_tests += 1
        else:
            self.failed_tests += 1
    
    def test_agent_instantiation(self):
        """Test SEO agent instantiation"""
        try:
            technical_agent = TechnicalSEOAgent()
            keyword_agent = KeywordResearchAgent()
            content_agent = ContentOptimizationAgent()
            link_agent = LinkBuildingAgent()
            
            # Validate agent properties
            assert technical_agent.role == "Technical SEO Specialist"
            assert keyword_agent.role == "Keyword Research Specialist"
            assert content_agent.role == "Content Optimization Specialist"
            assert link_agent.role == "Link Building Specialist"
            
            self.log_test("Agent Instantiation", True, "All SEO agents created successfully")
            
        except Exception as e:
            self.log_test("Agent Instantiation", False, f"Error: {str(e)}")
    
    def test_workflow_config_creation(self):
        """Test workflow configuration creation"""
        try:
            config = SEOWorkflowConfig(
                workflow_type=SEOWorkflowType.TECHNICAL_AUDIT,
                domain="example.com",
                target_keywords=["digital marketing", "seo services"],
                competitor_domains=["competitor1.com", "competitor2.com"],
                hitl_level=HITLApprovalLevel.MEDIUM,
                conservative_estimation=True
            )
            
            assert config.workflow_type == SEOWorkflowType.TECHNICAL_AUDIT
            assert config.domain == "example.com"
            assert len(config.target_keywords) == 2
            assert config.hitl_level == HITLApprovalLevel.MEDIUM
            
            self.log_test("Workflow Config Creation", True, "Configuration created and validated")
            
        except Exception as e:
            self.log_test("Workflow Config Creation", False, f"Error: {str(e)}")
    
    def test_service_request_validation(self):
        """Test service request validation"""
        try:
            # Valid request
            valid_request = SEOWorkflowRequest(
                workflow_type="technical_audit",
                domain="test-domain.com",
                target_keywords=["test keyword"],
                hitl_level="medium"
            )
            
            assert valid_request.workflow_type == "technical_audit"
            assert valid_request.domain == "test-domain.com"
            
            self.log_test("Service Request Validation", True, "Request validation working correctly")
            
        except Exception as e:
            self.log_test("Service Request Validation", False, f"Error: {str(e)}")
    
    def test_orchestrator_initialization(self):
        """Test SEO orchestrator initialization"""
        try:
            orchestrator = BizoholicSEOOrchestrator()
            
            assert hasattr(orchestrator, 'active_workflows')
            assert hasattr(orchestrator, 'performance_metrics')
            assert hasattr(orchestrator, 'hitl_queue')
            
            self.log_test("Orchestrator Initialization", True, "Orchestrator initialized with required attributes")
            
        except Exception as e:
            self.log_test("Orchestrator Initialization", False, f"Error: {str(e)}")
    
    def test_service_initialization(self):
        """Test SEO service initialization"""
        try:
            service = BizoholicSEOService()
            
            assert hasattr(service, 'orchestrator')
            assert hasattr(service, 'active_subscriptions')
            
            self.log_test("Service Initialization", True, "Service initialized correctly")
            
        except Exception as e:
            self.log_test("Service Initialization", False, f"Error: {str(e)}")
    
    async def test_workflow_execution_mock(self):
        """Test workflow execution with mock data"""
        try:
            config = SEOWorkflowConfig(
                workflow_type=SEOWorkflowType.TECHNICAL_AUDIT,
                domain="mock-test.com",
                target_keywords=["test"],
                conservative_estimation=True
            )
            
            # This would normally execute the full workflow
            # For testing, we'll just validate the configuration
            orchestrator = BizoholicSEOOrchestrator()
            workflow_id = "test-workflow-123"
            
            # Mock workflow state
            orchestrator.active_workflows[workflow_id] = {
                "tenant_id": "test-tenant",
                "config": config,
                "status": "initializing",
                "start_time": datetime.now(),
                "progress": 0
            }
            
            # Validate workflow state
            workflow_status = await orchestrator.get_workflow_status(workflow_id)
            assert workflow_status is not None
            assert workflow_status["status"] == "initializing"
            
            self.log_test("Workflow Execution Mock", True, "Mock workflow created and retrieved successfully")
            
        except Exception as e:
            self.log_test("Workflow Execution Mock", False, f"Error: {str(e)}")
    
    async def test_performance_dashboard(self):
        """Test performance dashboard functionality"""
        try:
            orchestrator = BizoholicSEOOrchestrator()
            dashboard_data = await orchestrator.get_performance_dashboard()
            
            assert "active_workflows" in dashboard_data
            assert "completed_workflows" in dashboard_data
            assert "system_health" in dashboard_data
            
            self.log_test("Performance Dashboard", True, "Dashboard data structure validated")
            
        except Exception as e:
            self.log_test("Performance Dashboard", False, f"Error: {str(e)}")
    
    def test_enum_definitions(self):
        """Test enum definitions and values"""
        try:
            # Test workflow types
            assert SEOWorkflowType.TECHNICAL_AUDIT.value == "technical_audit"
            assert SEOWorkflowType.COMPREHENSIVE_AUDIT.value == "comprehensive_audit"
            
            # Test HITL levels
            assert HITLApprovalLevel.NONE.value == "none"
            assert HITLApprovalLevel.MEDIUM.value == "medium"
            assert HITLApprovalLevel.HIGH.value == "high"
            
            self.log_test("Enum Definitions", True, "All enum values validated")
            
        except Exception as e:
            self.log_test("Enum Definitions", False, f"Error: {str(e)}")
    
    def test_tool_functionality(self):
        """Test SEO tool functionality"""
        try:
            from bizoholic_seo_agents import (
                TechnicalSEOTool,
                KeywordResearchTool,
                ContentOptimizationTool,
                BacklinkAnalysisTool
            )
            
            # Test tool instantiation
            tech_tool = TechnicalSEOTool()
            keyword_tool = KeywordResearchTool()
            content_tool = ContentOptimizationTool()
            backlink_tool = BacklinkAnalysisTool()
            
            # Validate tool properties
            assert tech_tool.name == "technical_seo_analyzer"
            assert keyword_tool.name == "keyword_researcher"
            assert content_tool.name == "content_optimizer"
            assert backlink_tool.name == "backlink_analyzer"
            
            self.log_test("Tool Functionality", True, "All SEO tools instantiated successfully")
            
        except Exception as e:
            self.log_test("Tool Functionality", False, f"Error: {str(e)}")
    
    async def run_all_tests(self):
        """Run all tests in the test suite"""
        print("🚀 Starting SEO Implementation Test Suite")
        print("=" * 50)
        
        # Run synchronous tests
        self.test_agent_instantiation()
        self.test_workflow_config_creation()
        self.test_service_request_validation()
        self.test_orchestrator_initialization()
        self.test_service_initialization()
        self.test_enum_definitions()
        self.test_tool_functionality()
        
        # Run asynchronous tests
        await self.test_workflow_execution_mock()
        await self.test_performance_dashboard()
        
        # Print summary
        print("=" * 50)
        print("🎯 Test Suite Summary")
        print(f"✅ Passed: {self.passed_tests}")
        print(f"❌ Failed: {self.failed_tests}")
        print(f"📊 Total: {self.passed_tests + self.failed_tests}")
        
        if self.failed_tests == 0:
            print("🎉 All tests passed! SEO implementation is ready.")
            return True
        else:
            print("⚠️  Some tests failed. Please review and fix issues.")
            return False
    
    def generate_test_report(self) -> str:
        """Generate detailed test report"""
        report = {
            "test_suite": "Bizoholic SEO Implementation",
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_tests": self.passed_tests + self.failed_tests,
                "passed_tests": self.passed_tests,
                "failed_tests": self.failed_tests,
                "success_rate": (self.passed_tests / (self.passed_tests + self.failed_tests)) * 100
            },
            "test_results": self.test_results
        }
        
        return json.dumps(report, indent=2)

async def main():
    """Main test execution function"""
    print("Bizoholic SEO Service Delivery Workflow - Implementation Test")
    print("=" * 60)
    
    tester = SEOImplementationTester()
    success = await tester.run_all_tests()
    
    # Generate and save test report
    report = tester.generate_test_report()
    
    try:
        with open("seo_test_report.json", "w") as f:
            f.write(report)
        print(f"📄 Test report saved to: seo_test_report.json")
    except Exception as e:
        print(f"⚠️  Could not save test report: {e}")
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    asyncio.run(main())