#!/usr/bin/env python3
"""
Test Suite for Amazon Business Integration
BizOSaaS Brain AI Agentic API Gateway

This test suite provides comprehensive testing for the Amazon Business API integration
covering all 4 specialized AI agents and their Brain API Gateway endpoints.

Test Coverage:
- Business Procurement AI Agent: B2B purchasing optimization and supplier management
- Business Account Management AI Agent: User roles, permissions, and workflow management  
- Business Analytics AI Agent: Spend analysis, procurement insights, and cost optimization
- Business Compliance AI Agent: Tax exemption management and regulatory compliance

API Endpoints Tested:
- /api/brain/integrations/amazon-business/ai-procurement-optimization
- /api/brain/integrations/amazon-business/ai-account-management
- /api/brain/integrations/amazon-business/ai-business-analytics
- /api/brain/integrations/amazon-business/ai-compliance-management
- /api/brain/integrations/amazon-business/ai-agents-status
"""

import asyncio
import json
import time
import requests
from typing import Dict, List, Any
from datetime import datetime, timedelta
import random

# Test configuration
BASE_URL = "http://localhost:8001"
TEST_TENANT_ID = "amazon_business_test_tenant"

class AmazonBusinessIntegrationTester:
    """Comprehensive test suite for Amazon Business Integration"""
    
    def __init__(self):
        self.base_url = BASE_URL
        self.tenant_id = TEST_TENANT_ID
        self.test_results = {
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "test_details": []
        }
        
    def log_test_result(self, test_name: str, success: bool, details: str, response_time: float = 0.0):
        """Log individual test results"""
        self.test_results["total_tests"] += 1
        if success:
            self.test_results["passed_tests"] += 1
            status = "✅ PASS"
        else:
            self.test_results["failed_tests"] += 1
            status = "❌ FAIL"
            
        self.test_results["test_details"].append({
            "test_name": test_name,
            "status": status,
            "details": details,
            "response_time": f"{response_time:.3f}s",
            "timestamp": datetime.now().isoformat()
        })
        
        print(f"{status} {test_name}: {details} ({response_time:.3f}s)")
    
    def test_procurement_optimization_endpoint(self) -> bool:
        """Test the procurement optimization AI agent endpoint"""
        try:
            start_time = time.time()
            
            # Test data with realistic B2B procurement scenarios
            test_data = {
                "tenant_id": self.tenant_id,
                "business_account_id": "business_account_12345",
                "procurement_categories": [
                    "office_supplies",
                    "it_equipment", 
                    "industrial_supplies",
                    "laboratory_equipment"
                ],
                "budget_constraints": {
                    "annual_budget": 2500000.0,
                    "quarterly_limit": 625000.0,
                    "monthly_average": 208333.33,
                    "emergency_fund": 50000.0
                },
                "supplier_preferences": [
                    "Office Pro Solutions",
                    "TechBusiness Direct",
                    "Industrial Supply Co",
                    "Lab Equipment Inc"
                ],
                "department_requirements": [
                    {
                        "department": "IT",
                        "budget": 800000.0,
                        "priority": "high",
                        "categories": ["it_equipment", "office_supplies"],
                        "approval_limit": 10000.0
                    },
                    {
                        "department": "Operations",
                        "budget": 600000.0,
                        "priority": "medium",
                        "categories": ["industrial_supplies", "safety_equipment"],
                        "approval_limit": 5000.0
                    },
                    {
                        "department": "R&D",
                        "budget": 900000.0,
                        "priority": "high",
                        "categories": ["laboratory_equipment", "research_materials"],
                        "approval_limit": 25000.0
                    },
                    {
                        "department": "Admin",
                        "budget": 200000.0,
                        "priority": "low",
                        "categories": ["office_supplies", "furniture"],
                        "approval_limit": 2500.0
                    }
                ],
                "approval_workflows": [
                    "standard_approval",
                    "emergency_procurement",
                    "bulk_order_approval",
                    "contract_negotiation"
                ],
                "compliance_requirements": [
                    "tax_exempt",
                    "government_procurement",
                    "healthcare_compliance",
                    "educational_discount"
                ]
            }
            
            response = requests.post(
                f"{self.base_url}/api/brain/integrations/amazon-business/ai-procurement-optimization",
                json=test_data,
                timeout=30
            )
            
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    # Validate response structure
                    agent_analysis = result.get("agent_analysis", {})
                    business_result = result.get("business_result", {})
                    
                    required_fields = [
                        "optimization_metrics", "supplier_analysis", 
                        "category_insights", "budget_optimization",
                        "ai_recommendations", "contract_management"
                    ]
                    
                    missing_fields = [field for field in required_fields if field not in agent_analysis]
                    
                    if not missing_fields:
                        cost_savings = business_result.get("total_cost_savings", 0)
                        savings_percentage = business_result.get("savings_percentage", 0)
                        
                        self.log_test_result(
                            "Procurement Optimization",
                            True,
                            f"Successfully analyzed {business_result.get('categories_analyzed', 0)} categories, "
                            f"evaluated {business_result.get('suppliers_evaluated', 0)} suppliers, "
                            f"achieved ${cost_savings:,.2f} savings ({savings_percentage}%)",
                            response_time
                        )
                        return True
                    else:
                        self.log_test_result(
                            "Procurement Optimization",
                            False,
                            f"Missing required fields in response: {missing_fields}",
                            response_time
                        )
                        return False
                else:
                    self.log_test_result(
                        "Procurement Optimization",
                        False,
                        f"API returned success=false: {result.get('error', 'Unknown error')}",
                        response_time
                    )
                    return False
            else:
                self.log_test_result(
                    "Procurement Optimization",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    response_time
                )
                return False
                
        except Exception as e:
            self.log_test_result("Procurement Optimization", False, f"Exception: {str(e)}")
            return False
    
    def test_account_management_endpoint(self) -> bool:
        """Test the account management AI agent endpoint"""
        try:
            start_time = time.time()
            
            # Test data with realistic business account management scenarios
            test_data = {
                "tenant_id": self.tenant_id,
                "business_account_id": "business_account_12345",
                "user_management": [
                    {
                        "user_id": "admin_001",
                        "email": "admin@company.com",
                        "role": "admin",
                        "department": "IT",
                        "spending_limit": 50000.0,
                        "approval_authority": True
                    },
                    {
                        "user_id": "buyer_001",
                        "email": "buyer1@company.com",
                        "role": "buyer",
                        "department": "Operations", 
                        "spending_limit": 10000.0,
                        "approval_authority": False
                    },
                    {
                        "user_id": "manager_001",
                        "email": "manager@company.com",
                        "role": "procurement_manager",
                        "department": "Admin",
                        "spending_limit": 25000.0,
                        "approval_authority": True
                    },
                    {
                        "user_id": "requester_001",
                        "email": "requester@company.com",
                        "role": "requester",
                        "department": "R&D",
                        "spending_limit": 1000.0,
                        "approval_authority": False
                    }
                ],
                "role_assignments": {
                    "admin": ["admin_001"],
                    "procurement_manager": ["manager_001"],
                    "buyer": ["buyer_001"],
                    "approver": ["admin_001", "manager_001"],
                    "requester": ["requester_001"]
                },
                "approval_policies": [
                    {
                        "policy_name": "Standard Purchase Approval",
                        "amount_threshold": 5000.0,
                        "required_approvers": 1,
                        "approval_roles": ["procurement_manager", "admin"],
                        "auto_approval": False
                    },
                    {
                        "policy_name": "Emergency Procurement",
                        "amount_threshold": 50000.0,
                        "required_approvers": 2,
                        "approval_roles": ["admin"],
                        "auto_approval": False
                    },
                    {
                        "policy_name": "Small Purchase Auto-Approval",
                        "amount_threshold": 500.0,
                        "required_approvers": 0,
                        "approval_roles": [],
                        "auto_approval": True
                    }
                ],
                "budget_allocations": {
                    "IT": 800000.0,
                    "Operations": 600000.0,
                    "R&D": 900000.0,
                    "Admin": 200000.0
                },
                "spending_controls": [
                    "daily_spending_limits",
                    "category_restrictions",
                    "approval_workflows", 
                    "budget_alerts",
                    "compliance_checks"
                ]
            }
            
            response = requests.post(
                f"{self.base_url}/api/brain/integrations/amazon-business/ai-account-management",
                json=test_data,
                timeout=30
            )
            
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    # Validate response structure
                    agent_analysis = result.get("agent_analysis", {})
                    business_result = result.get("business_result", {})
                    
                    required_fields = [
                        "management_metrics", "role_optimization",
                        "workflow_analysis", "budget_controls",
                        "user_insights", "ai_recommendations"
                    ]
                    
                    missing_fields = [field for field in required_fields if field not in agent_analysis]
                    
                    if not missing_fields:
                        total_users = business_result.get("total_users_managed", 0)
                        workflow_efficiency = business_result.get("approval_workflow_efficiency", 0)
                        
                        self.log_test_result(
                            "Account Management",
                            True,
                            f"Successfully managed {total_users} users, "
                            f"workflow efficiency: {workflow_efficiency:.1%}, "
                            f"{business_result.get('workflow_optimizations', 0)} optimizations identified",
                            response_time
                        )
                        return True
                    else:
                        self.log_test_result(
                            "Account Management",
                            False,
                            f"Missing required fields in response: {missing_fields}",
                            response_time
                        )
                        return False
                else:
                    self.log_test_result(
                        "Account Management",
                        False,
                        f"API returned success=false: {result.get('error', 'Unknown error')}",
                        response_time
                    )
                    return False
            else:
                self.log_test_result(
                    "Account Management",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    response_time
                )
                return False
                
        except Exception as e:
            self.log_test_result("Account Management", False, f"Exception: {str(e)}")
            return False
    
    def test_business_analytics_endpoint(self) -> bool:
        """Test the business analytics AI agent endpoint"""
        try:
            start_time = time.time()
            
            # Test data with realistic business analytics scenarios
            test_data = {
                "tenant_id": self.tenant_id,
                "business_account_id": "business_account_12345",
                "date_range": {
                    "start_date": "2025-01-01",
                    "end_date": "2025-09-14",
                    "comparison_period": "previous_year",
                    "fiscal_year": "2025"
                },
                "departments": [
                    "IT",
                    "Operations", 
                    "R&D",
                    "Admin",
                    "Marketing",
                    "Finance"
                ],
                "cost_centers": [
                    "CC_001_IT_Infrastructure",
                    "CC_002_Manufacturing",
                    "CC_003_Research",
                    "CC_004_Administration",
                    "CC_005_Marketing",
                    "CC_006_Finance"
                ],
                "analysis_scope": [
                    "spend_analysis",
                    "supplier_performance",
                    "cost_optimization",
                    "trend_analysis",
                    "benchmarking",
                    "predictive_analytics"
                ],
                "reporting_preferences": {
                    "report_format": "detailed",
                    "visualization_type": "charts_and_tables",
                    "frequency": "monthly",
                    "stakeholders": ["CFO", "Procurement Manager", "Department Heads"],
                    "delivery_method": "email_and_dashboard"
                }
            }
            
            response = requests.post(
                f"{self.base_url}/api/brain/integrations/amazon-business/ai-business-analytics",
                json=test_data,
                timeout=30
            )
            
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    # Validate response structure
                    agent_analysis = result.get("agent_analysis", {})
                    business_result = result.get("business_result", {})
                    
                    required_fields = [
                        "business_metrics", "departmental_analysis",
                        "cost_center_analysis", "supplier_analytics",
                        "cost_optimization", "predictive_insights"
                    ]
                    
                    missing_fields = [field for field in required_fields if field not in agent_analysis]
                    
                    if not missing_fields:
                        total_spend = business_result.get("total_spend_analyzed", 0)
                        savings_achieved = business_result.get("cost_savings_achieved", 0)
                        forecast_accuracy = business_result.get("forecast_accuracy", 0)
                        
                        self.log_test_result(
                            "Business Analytics",
                            True,
                            f"Analyzed ${total_spend:,.2f} total spend, "
                            f"achieved ${savings_achieved:,.2f} savings, "
                            f"forecast accuracy: {forecast_accuracy:.1%}",
                            response_time
                        )
                        return True
                    else:
                        self.log_test_result(
                            "Business Analytics",
                            False,
                            f"Missing required fields in response: {missing_fields}",
                            response_time
                        )
                        return False
                else:
                    self.log_test_result(
                        "Business Analytics",
                        False,
                        f"API returned success=false: {result.get('error', 'Unknown error')}",
                        response_time
                    )
                    return False
            else:
                self.log_test_result(
                    "Business Analytics",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    response_time
                )
                return False
                
        except Exception as e:
            self.log_test_result("Business Analytics", False, f"Exception: {str(e)}")
            return False
    
    def test_compliance_management_endpoint(self) -> bool:
        """Test the compliance management AI agent endpoint"""
        try:
            start_time = time.time()
            
            # Test data with realistic compliance management scenarios
            test_data = {
                "tenant_id": self.tenant_id,
                "business_account_id": "business_account_12345",
                "compliance_types": [
                    "tax_exempt",
                    "government_procurement",
                    "healthcare_compliance",
                    "educational_discount",
                    "non_profit_pricing",
                    "international_trade"
                ],
                "tax_jurisdictions": [
                    "federal",
                    "california",
                    "texas",
                    "new_york",
                    "florida",
                    "international"
                ],
                "regulatory_requirements": [
                    "GSA_pricing_compliance",
                    "HIPAA_healthcare_requirements",
                    "Export_control_regulations",
                    "State_tax_exemption_rules",
                    "Educational_institution_discounts",
                    "Non_profit_organization_benefits"
                ],
                "audit_scope": [
                    "tax_exemption_certificates",
                    "invoice_compliance",
                    "regulatory_adherence",
                    "documentation_completeness",
                    "process_compliance",
                    "risk_assessment"
                ],
                "reporting_format": "comprehensive"
            }
            
            response = requests.post(
                f"{self.base_url}/api/brain/integrations/amazon-business/ai-compliance-management",
                json=test_data,
                timeout=30
            )
            
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    # Validate response structure
                    agent_analysis = result.get("agent_analysis", {})
                    business_result = result.get("business_result", {})
                    
                    required_fields = [
                        "compliance_metrics", "tax_exemption_analysis",
                        "regulatory_compliance", "invoice_management",
                        "risk_assessment", "audit_preparation"
                    ]
                    
                    missing_fields = [field for field in required_fields if field not in agent_analysis]
                    
                    if not missing_fields:
                        compliance_score = business_result.get("compliance_score", 0)
                        tax_savings = business_result.get("annual_tax_savings", 0)
                        certificates = business_result.get("valid_exemption_certificates", 0)
                        
                        self.log_test_result(
                            "Compliance Management",
                            True,
                            f"Compliance score: {compliance_score:.1%}, "
                            f"annual tax savings: ${tax_savings:,.2f}, "
                            f"{certificates} valid certificates",
                            response_time
                        )
                        return True
                    else:
                        self.log_test_result(
                            "Compliance Management",
                            False,
                            f"Missing required fields in response: {missing_fields}",
                            response_time
                        )
                        return False
                else:
                    self.log_test_result(
                        "Compliance Management",
                        False,
                        f"API returned success=false: {result.get('error', 'Unknown error')}",
                        response_time
                    )
                    return False
            else:
                self.log_test_result(
                    "Compliance Management",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    response_time
                )
                return False
                
        except Exception as e:
            self.log_test_result("Compliance Management", False, f"Exception: {str(e)}")
            return False
    
    def test_agents_status_endpoint(self) -> bool:
        """Test the agents status endpoint"""
        try:
            start_time = time.time()
            
            response = requests.get(
                f"{self.base_url}/api/brain/integrations/amazon-business/ai-agents-status",
                params={"tenant_id": self.tenant_id},
                timeout=15
            )
            
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    # Validate response structure
                    required_fields = [
                        "total_active_agents", "agents_status", "supported_account_types",
                        "supported_regions", "coordination_metrics", "performance_stats"
                    ]
                    
                    missing_fields = [field for field in required_fields if field not in result]
                    
                    if not missing_fields:
                        total_agents = result.get("total_active_agents", 0)
                        avg_savings = result.get("coordination_metrics", {}).get("average_cost_savings", "N/A")
                        
                        self.log_test_result(
                            "Agents Status",
                            True,
                            f"{total_agents} active agents, average cost savings: {avg_savings}",
                            response_time
                        )
                        return True
                    else:
                        self.log_test_result(
                            "Agents Status",
                            False,
                            f"Missing required fields in response: {missing_fields}",
                            response_time
                        )
                        return False
                else:
                    self.log_test_result(
                        "Agents Status",
                        False,
                        f"API returned success=false: {result.get('error', 'Unknown error')}",
                        response_time
                    )
                    return False
            else:
                self.log_test_result(
                    "Agents Status",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    response_time
                )
                return False
                
        except Exception as e:
            self.log_test_result("Agents Status", False, f"Exception: {str(e)}")
            return False
    
    def test_integration_reliability(self) -> bool:
        """Test integration reliability with multiple rapid requests"""
        try:
            success_count = 0
            total_requests = 5
            
            for i in range(total_requests):
                start_time = time.time()
                
                test_data = {
                    "tenant_id": f"{self.tenant_id}_reliability_{i}",
                    "business_account_id": f"test_account_{i}",
                    "procurement_categories": ["office_supplies", "it_equipment"],
                    "budget_constraints": {"annual_budget": 100000.0 * (i + 1)},
                    "supplier_preferences": [f"supplier_{i}"],
                    "department_requirements": [{"department": "IT", "budget": 50000.0}],
                    "approval_workflows": ["standard_approval"],
                    "compliance_requirements": ["tax_exempt"]
                }
                
                try:
                    response = requests.post(
                        f"{self.base_url}/api/brain/integrations/amazon-business/ai-procurement-optimization",
                        json=test_data,
                        timeout=15
                    )
                    
                    if response.status_code == 200 and response.json().get("success"):
                        success_count += 1
                    
                except Exception:
                    pass
                
                # Small delay between requests
                time.sleep(0.5)
            
            response_time = time.time() - start_time
            success_rate = success_count / total_requests
            
            if success_rate >= 0.8:  # 80% success rate threshold
                self.log_test_result(
                    "Integration Reliability",
                    True,
                    f"{success_count}/{total_requests} requests successful ({success_rate:.1%} success rate)",
                    response_time
                )
                return True
            else:
                self.log_test_result(
                    "Integration Reliability",
                    False,
                    f"Only {success_count}/{total_requests} requests successful ({success_rate:.1%} success rate)",
                    response_time
                )
                return False
                
        except Exception as e:
            self.log_test_result("Integration Reliability", False, f"Exception: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all test cases"""
        print("=" * 80)
        print("🚀 Starting Amazon Business Integration Test Suite")
        print(f"📍 Base URL: {self.base_url}")
        print(f"🏢 Tenant ID: {self.tenant_id}")
        print(f"⏰ Started at: {datetime.now().isoformat()}")
        print("=" * 80)
        
        # Run individual tests
        test_methods = [
            self.test_procurement_optimization_endpoint,
            self.test_account_management_endpoint,
            self.test_business_analytics_endpoint,
            self.test_compliance_management_endpoint,
            self.test_agents_status_endpoint,
            self.test_integration_reliability
        ]
        
        for test_method in test_methods:
            try:
                test_method()
            except Exception as e:
                self.log_test_result(
                    test_method.__name__.replace("test_", "").replace("_", " ").title(),
                    False,
                    f"Test method failed: {str(e)}"
                )
        
        # Print summary
        print("=" * 80)
        print("📊 AMAZON BUSINESS INTEGRATION TEST RESULTS")
        print("=" * 80)
        
        success_rate = (self.test_results["passed_tests"] / self.test_results["total_tests"]) * 100 if self.test_results["total_tests"] > 0 else 0
        
        print(f"✅ Passed Tests: {self.test_results['passed_tests']}")
        print(f"❌ Failed Tests: {self.test_results['failed_tests']}")
        print(f"📈 Total Tests: {self.test_results['total_tests']}")
        print(f"🎯 Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 95:
            print("🌟 EXCELLENT: Integration is working perfectly!")
        elif success_rate >= 80:
            print("✅ GOOD: Integration is working well with minor issues")
        elif success_rate >= 60:
            print("⚠️ FAIR: Integration has some issues that need attention")
        else:
            print("❌ POOR: Integration has significant issues requiring immediate attention")
        
        print("=" * 80)
        
        # Detailed results
        if self.test_results["failed_tests"] > 0:
            print("🔍 FAILED TEST DETAILS:")
            for test in self.test_results["test_details"]:
                if test["status"] == "❌ FAIL":
                    print(f"   {test['test_name']}: {test['details']}")
            print("=" * 80)
        
        # Save results to file
        with open("/tmp/amazon_business_test_results.json", "w") as f:
            json.dump(self.test_results, f, indent=2)
        
        print(f"📄 Detailed results saved to: /tmp/amazon_business_test_results.json")
        print(f"⏰ Test completed at: {datetime.now().isoformat()}")
        
        return success_rate >= 95

if __name__ == "__main__":
    tester = AmazonBusinessIntegrationTester()
    success = tester.run_all_tests()
    
    # Exit with appropriate code
    import sys
    sys.exit(0 if success else 1)