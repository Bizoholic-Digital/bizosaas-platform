#!/usr/bin/env python3
"""
Test Suite for Supplier Validation Workflow [P9]
Comprehensive testing of all validation components
"""

import asyncio
import json
import pytest
import aiohttp
from datetime import datetime
from typing import Dict, Any
import uuid

# Test Configuration
API_BASE_URL = "http://localhost:8027"
TEST_TOKEN = "test-token-123"

class SupplierValidationTester:
    """Test suite for supplier validation system"""
    
    def __init__(self):
        self.base_url = API_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {TEST_TOKEN}",
            "Content-Type": "application/json"
        }
        self.test_supplier_id = None
    
    async def run_comprehensive_tests(self):
        """Run all test cases"""
        print("🚀 Starting Supplier Validation Workflow [P9] Tests")
        print("=" * 60)
        
        # Test Cases
        test_cases = [
            ("Health Check", self.test_health_check),
            ("Dashboard Access", self.test_dashboard_access),
            ("Supplier Registration", self.test_supplier_registration),
            ("Document Upload", self.test_document_upload),
            ("Risk Assessment", self.test_risk_assessment),
            ("Comprehensive Validation", self.test_comprehensive_validation),
            ("Workflow Management", self.test_workflow_management),
            ("Supplier Review", self.test_supplier_review),
            ("Analytics Dashboard", self.test_analytics_dashboard),
            ("Bulk Operations", self.test_bulk_operations)
        ]
        
        results = {}
        
        async with aiohttp.ClientSession() as session:
            self.session = session
            
            for test_name, test_func in test_cases:
                print(f"\n📋 Running Test: {test_name}")
                try:
                    result = await test_func()
                    results[test_name] = {"status": "PASS", "details": result}
                    print(f"✅ {test_name}: PASSED")
                except Exception as e:
                    results[test_name] = {"status": "FAIL", "error": str(e)}
                    print(f"❌ {test_name}: FAILED - {str(e)}")
        
        # Print Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(test_cases)
        passed_tests = sum(1 for r in results.values() if r["status"] == "PASS")
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ Failed Tests:")
            for test_name, result in results.items():
                if result["status"] == "FAIL":
                    print(f"  - {test_name}: {result['error']}")
        
        return results
    
    async def test_health_check(self):
        """Test health check endpoint"""
        async with self.session.get(f"{self.base_url}/health") as response:
            if response.status != 200:
                raise Exception(f"Health check failed with status {response.status}")
            
            data = await response.json()
            if data.get("status") != "healthy":
                raise Exception("Service not healthy")
            
            return {"status": data.get("status"), "service": data.get("service")}
    
    async def test_dashboard_access(self):
        """Test dashboard accessibility"""
        async with self.session.get(f"{self.base_url}/dashboard") as response:
            if response.status != 200:
                raise Exception(f"Dashboard access failed with status {response.status}")
            
            content = await response.text()
            if "Supplier Validation Dashboard" not in content:
                raise Exception("Dashboard content not properly loaded")
            
            return {"accessible": True, "content_length": len(content)}
    
    async def test_supplier_registration(self):
        """Test supplier registration"""
        supplier_data = {
            "company_name": f"Test Electronics Pvt Ltd {uuid.uuid4().hex[:8]}",
            "contact_person": "Test Manager",
            "email": f"test{uuid.uuid4().hex[:8]}@testcompany.com",
            "phone": "+91-9876543210",
            "address": "123 Test Street, Test Area",
            "city": "Mumbai",
            "state": "Maharashtra",
            "country": "India",
            "pincode": "400001",
            "website": "https://www.testcompany.com",
            "business_type": "Private Limited Company",
            "industry": "Electronics Manufacturing",
            "products_offered": ["Test Products", "Test Services"],
            "annual_revenue": 5000000,
            "employee_count": 25,
            "gst_number": "27AABCT1234M1Z5",
            "pan_number": "AABCT1234M"
        }
        
        async with self.session.post(
            f"{self.base_url}/suppliers/register",
            headers=self.headers,
            json=supplier_data
        ) as response:
            if response.status != 200:
                raise Exception(f"Supplier registration failed with status {response.status}")
            
            data = await response.json()
            self.test_supplier_id = data.get("supplier_id")
            
            if not self.test_supplier_id:
                raise Exception("No supplier ID returned")
            
            return {
                "supplier_id": self.test_supplier_id,
                "workflow_id": data.get("workflow_id"),
                "status": data.get("status")
            }
    
    async def test_document_upload(self):
        """Test document upload functionality"""
        if not self.test_supplier_id:
            raise Exception("No test supplier available")
        
        # Create a test document (simple text file)
        test_document_content = b"Test business license document content"
        
        # Prepare multipart form data
        form_data = aiohttp.FormData()
        form_data.add_field('document_type', 'business_license')
        form_data.add_field('file', test_document_content, 
                           filename='test_license.txt',
                           content_type='text/plain')
        
        async with self.session.post(
            f"{self.base_url}/suppliers/{self.test_supplier_id}/documents/upload",
            headers={"Authorization": f"Bearer {TEST_TOKEN}"},
            data=form_data
        ) as response:
            if response.status != 200:
                raise Exception(f"Document upload failed with status {response.status}")
            
            data = await response.json()
            return {
                "document_id": data.get("document_id"),
                "verification_status": data.get("verification_status"),
                "confidence_score": data.get("confidence_score")
            }
    
    async def test_risk_assessment(self):
        """Test risk assessment functionality"""
        if not self.test_supplier_id:
            raise Exception("No test supplier available")
        
        async with self.session.get(
            f"{self.base_url}/suppliers/{self.test_supplier_id}/risk-assessment",
            headers=self.headers
        ) as response:
            if response.status != 200:
                raise Exception(f"Risk assessment failed with status {response.status}")
            
            data = await response.json()
            return {
                "risk_level": data.get("risk_level"),
                "risk_score": data.get("risk_score"),
                "risk_factors_count": len(data.get("risk_factors", [])),
                "recommendations_count": len(data.get("recommendations", []))
            }
    
    async def test_comprehensive_validation(self):
        """Test comprehensive validation endpoint"""
        if not self.test_supplier_id:
            raise Exception("No test supplier available")
        
        async with self.session.post(
            f"{self.base_url}/suppliers/{self.test_supplier_id}/validate-comprehensive",
            headers=self.headers
        ) as response:
            if response.status != 200:
                raise Exception(f"Comprehensive validation failed with status {response.status}")
            
            data = await response.json()
            return {
                "overall_score": data.get("overall_score"),
                "validation_count": len(data.get("validation_results", {})),
                "confidence_level": data.get("validation_summary", {}).get("confidence_level")
            }
    
    async def test_workflow_management(self):
        """Test workflow management"""
        if not self.test_supplier_id:
            raise Exception("No test supplier available")
        
        # Get workflow history
        async with self.session.get(
            f"{self.base_url}/suppliers/{self.test_supplier_id}/workflow-history",
            headers=self.headers
        ) as response:
            if response.status != 200:
                raise Exception(f"Workflow history failed with status {response.status}")
            
            data = await response.json()
            return {
                "workflow_count": len(data.get("workflow_history", [])),
                "audit_count": len(data.get("audit_history", [])),
                "validation_count": len(data.get("validation_history", []))
            }
    
    async def test_supplier_review(self):
        """Test supplier review process"""
        if not self.test_supplier_id:
            raise Exception("No test supplier available")
        
        review_data = {
            "supplier_id": self.test_supplier_id,
            "decision": "approve",
            "comments": "Test supplier review - automated test approval"
        }
        
        async with self.session.post(
            f"{self.base_url}/suppliers/{self.test_supplier_id}/review",
            headers=self.headers,
            json=review_data
        ) as response:
            if response.status != 200:
                raise Exception(f"Supplier review failed with status {response.status}")
            
            data = await response.json()
            return {
                "workflow_id": data.get("workflow_id"),
                "current_step": data.get("current_step"),
                "status": data.get("status")
            }
    
    async def test_analytics_dashboard(self):
        """Test analytics dashboard"""
        async with self.session.get(
            f"{self.base_url}/dashboard/analytics",
            headers=self.headers
        ) as response:
            if response.status != 200:
                raise Exception(f"Analytics dashboard failed with status {response.status}")
            
            data = await response.json()
            return {
                "total_suppliers": data.get("summary", {}).get("total_suppliers", 0),
                "has_status_distribution": bool(data.get("status_distribution")),
                "has_risk_distribution": bool(data.get("risk_distribution")),
                "recent_activity_count": len(data.get("recent_activity", []))
            }
    
    async def test_bulk_operations(self):
        """Test bulk operations"""
        if not self.test_supplier_id:
            raise Exception("No test supplier available")
        
        bulk_data = {
            "action": "assign_analyst",
            "supplier_ids": [self.test_supplier_id],
            "comments": "Test bulk operation"
        }
        
        async with self.session.post(
            f"{self.base_url}/suppliers/bulk-action?action=assign_analyst&supplier_ids={self.test_supplier_id}&comments=Test bulk operation",
            headers=self.headers,
            json=bulk_data
        ) as response:
            if response.status != 200:
                raise Exception(f"Bulk operation failed with status {response.status}")
            
            data = await response.json()
            return {
                "action": data.get("action"),
                "total_suppliers": data.get("total_suppliers"),
                "successful": data.get("successful"),
                "failed": data.get("failed")
            }

class ValidationEngineUnitTests:
    """Unit tests for validation engine components"""
    
    async def run_validation_engine_tests(self):
        """Run validation engine unit tests"""
        print("\n🔬 Running Validation Engine Unit Tests")
        print("=" * 50)
        
        from validation_engine import (
            IndianBusinessValidator,
            EmailPhoneValidator,
            WebsiteValidator,
            BusinessProfileValidator,
            ComprehensiveSupplierValidator
        )
        
        # Test GST validation
        business_validator = IndianBusinessValidator()
        gst_result = await business_validator.validate_gst_number("27AABCT1234M1Z5", "Maharashtra")
        print(f"✅ GST Validation: {gst_result.is_valid} (Score: {gst_result.confidence_score})")
        
        # Test PAN validation
        pan_result = await business_validator.validate_pan_number("AABCT1234M")
        print(f"✅ PAN Validation: {pan_result.is_valid} (Score: {pan_result.confidence_score})")
        
        # Test email validation
        contact_validator = EmailPhoneValidator()
        email_result = await contact_validator.validate_email("test@company.com")
        print(f"✅ Email Validation: {email_result.is_valid} (Score: {email_result.confidence_score})")
        
        # Test phone validation
        phone_result = await contact_validator.validate_phone("+91-9876543210")
        print(f"✅ Phone Validation: {phone_result.is_valid} (Score: {phone_result.confidence_score})")
        
        # Test business profile validation
        profile_validator = BusinessProfileValidator()
        profile_data = {
            'company_name': 'Test Electronics Pvt Ltd',
            'industry': 'Electronics Manufacturing',
            'products_offered': ['Smartphones', 'Laptops', 'Accessories'],
            'employee_count': 25,
            'annual_revenue': 5000000,
            'business_type': 'Private Limited Company'
        }
        profile_result = await profile_validator.validate_business_profile(profile_data)
        print(f"✅ Business Profile Validation: {profile_result.is_valid} (Score: {profile_result.confidence_score})")
        
        return True

async def main():
    """Run comprehensive test suite"""
    print("🧪 BizOSaaS Supplier Validation Workflow [P9] Test Suite")
    print("=" * 70)
    
    # Run unit tests first
    unit_tester = ValidationEngineUnitTests()
    await unit_tester.run_validation_engine_tests()
    
    # Run integration tests
    integration_tester = SupplierValidationTester()
    results = await integration_tester.run_comprehensive_tests()
    
    print("\n🎯 Testing Complete!")
    print("For detailed logs, check the service logs at: docker-compose logs supplier-validation")
    
    return results

if __name__ == "__main__":
    asyncio.run(main())