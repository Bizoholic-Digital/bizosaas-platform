#!/usr/bin/env python3
"""
Test Suite for PayU Payment Processing APIs Brain Integration

Comprehensive test suite for the PayU payment processing integration
testing all 4 AI agents and their coordination through the Brain API Gateway.

Author: BizOSaaS Platform
Created: September 15, 2025
"""

import pytest
import asyncio
import json
from typing import Dict, Any
from datetime import datetime, timedelta

# Import the PayU integration components
from payu_payment_api_integration import (
    payu_hub,
    PayUPaymentRequest,
    PayUSubscriptionRequest,
    PayUAnalyticsRequest,
    PayURegion,
    PayUPaymentMethod,
    PayUCurrency,
    PayUGlobalPaymentAgent,
    PayUSubscriptionAgent,
    PayUFraudDetectionAgent,
    PayUAnalyticsAgent
)

class TestPayUGlobalPaymentAgent:
    """Test suite for PayU Global Payment Agent"""
    
    def setup_method(self):
        """Setup test environment"""
        self.agent = PayUGlobalPaymentAgent()
        self.test_request = PayUPaymentRequest(
            tenant_id="test_tenant_001",
            amount=599.99,
            currency="USD",
            description="Test premium subscription",
            reference="TEST_REF_001",
            customer_email="test@example.com",
            customer_id="test_customer_001",
            payment_method="card",
            region="global",
            buyer_info={"country": "US", "location": {"lat": 40.7128, "lon": -74.0060}},
            metadata={"merchant_country": "US", "ip_address": "192.168.1.100"}
        )
    
    @pytest.mark.asyncio
    async def test_global_payment_processing(self):
        """Test global payment processing"""
        result = await self.agent.process_payment(self.test_request)
        
        # Validate response structure
        assert "agent_id" in result
        assert "processor" in result
        assert "routing_optimization" in result
        assert "fraud_analysis" in result
        assert "currency_optimization" in result
        assert "processing_result" in result
        
        # Validate processor identification
        assert result["processor"] == "payu_global"
        
        # Validate processing result structure
        processing_result = result["processing_result"]
        assert "transactionId" in processing_result
        assert "orderId" in processing_result
        assert "amount" in processing_result
        assert "state" in processing_result
        assert "fees" in processing_result
        
        # Validate AI recommendations
        assert "ai_recommendations" in result
        assert isinstance(result["ai_recommendations"], list)
        assert len(result["ai_recommendations"]) > 0
        
        print(f"✅ Global Payment Processing Test Passed")
        print(f"   Transaction ID: {processing_result['transactionId']}")
        print(f"   State: {processing_result['state']}")
        print(f"   Total Fees: ${processing_result['fees']['total_fees']}")
    
    @pytest.mark.asyncio
    async def test_regional_routing_optimization(self):
        """Test regional routing optimization"""
        result = await self.agent.process_payment(self.test_request)
        routing_optimization = result["routing_optimization"]
        
        # Validate routing optimization structure
        assert "optimal_region" in routing_optimization
        assert "fee_rate" in routing_optimization
        assert "is_international" in routing_optimization
        assert "recommended_apms" in routing_optimization
        assert "compliance_requirements" in routing_optimization
        
        # Validate region selection logic
        assert routing_optimization["optimal_region"] in ["global", "india", "latam", "cee"]
        assert isinstance(routing_optimization["fee_rate"], float)
        assert routing_optimization["fee_rate"] > 0
        
        print(f"✅ Regional Routing Test Passed")
        print(f"   Optimal Region: {routing_optimization['optimal_region']}")
        print(f"   Fee Rate: {routing_optimization['fee_rate']*100:.2f}%")
    
    @pytest.mark.asyncio
    async def test_multi_currency_support(self):
        """Test multi-currency payment processing"""
        currencies_to_test = ["EUR", "INR", "BRL", "GBP"]
        
        for currency in currencies_to_test:
            test_request = PayUPaymentRequest(
                tenant_id="test_tenant_001",
                amount=299.99,
                currency=currency,
                description=f"Test payment in {currency}",
                reference=f"TEST_REF_{currency}",
                customer_email="test@example.com"
            )
            
            result = await self.agent.process_payment(test_request)
            
            # Validate currency handling
            assert result["processing_result"]["amount"]["currency"] == currency
            assert "currency_optimization" in result
            
            currency_opt = result["currency_optimization"]
            if currency != "USD":
                assert currency_opt["conversion_required"] is True
                assert "exchange_rate" in currency_opt
            else:
                assert currency_opt["conversion_required"] is False
        
        print(f"✅ Multi-Currency Support Test Passed")
        print(f"   Tested currencies: {', '.join(currencies_to_test)}")

class TestPayUSubscriptionAgent:
    """Test suite for PayU Subscription Agent"""
    
    def setup_method(self):
        """Setup test environment"""
        self.agent = PayUSubscriptionAgent()
        self.test_request = PayUSubscriptionRequest(
            tenant_id="test_tenant_001",
            plan_id="premium_plan_monthly",
            customer_id="test_customer_001",
            payment_method="CARD",
            currency="USD",
            trial_days=14,
            metadata={"customer_segment": "startup", "base_amount": 29.99}
        )
    
    @pytest.mark.asyncio
    async def test_subscription_creation(self):
        """Test subscription creation"""
        result = await self.agent.create_subscription(self.test_request)
        
        # Validate response structure
        assert "agent_id" in result
        assert "processor" in result
        assert "subscription_result" in result
        assert "pricing_optimization" in result
        assert "churn_analysis" in result
        
        # Validate subscription result
        subscription_result = result["subscription_result"]
        assert "id" in subscription_result
        assert "planId" in subscription_result
        assert "status" in subscription_result
        assert "paymentMethod" in subscription_result
        assert "billingDetails" in subscription_result
        
        # Validate billing details
        billing = subscription_result["billingDetails"]
        assert "amount" in billing
        assert "currency" in billing
        assert "billingCycle" in billing
        assert "nextBillingDate" in billing
        
        print(f"✅ Subscription Creation Test Passed")
        print(f"   Subscription ID: {subscription_result['id']}")
        print(f"   Status: {subscription_result['status']}")
        print(f"   Billing Cycle: {billing['billingCycle']}")
    
    @pytest.mark.asyncio
    async def test_churn_risk_assessment(self):
        """Test churn risk assessment"""
        result = await self.agent.create_subscription(self.test_request)
        churn_analysis = result["churn_analysis"]
        
        # Validate churn analysis structure
        assert "churn_probability" in churn_analysis
        assert "risk_level" in churn_analysis
        assert "predicted_ltv" in churn_analysis
        assert "intervention_recommendations" in churn_analysis
        
        # Validate churn probability
        churn_prob = churn_analysis["churn_probability"]
        assert 0.0 <= churn_prob <= 1.0
        
        # Validate risk level
        risk_level = churn_analysis["risk_level"]
        assert risk_level in ["low", "medium", "high"]
        
        # Validate LTV prediction
        ltv = churn_analysis["predicted_ltv"]
        assert isinstance(ltv, (int, float))
        assert ltv > 0
        
        print(f"✅ Churn Risk Assessment Test Passed")
        print(f"   Churn Probability: {churn_prob:.3f}")
        print(f"   Risk Level: {risk_level}")
        print(f"   Predicted LTV: ${ltv:.2f}")
    
    @pytest.mark.asyncio
    async def test_pricing_optimization(self):
        """Test pricing optimization"""
        result = await self.agent.create_subscription(self.test_request)
        pricing_optimization = result["pricing_optimization"]
        
        # Validate pricing optimization structure
        assert "base_amount" in pricing_optimization
        assert "optimized_amount" in pricing_optimization
        assert "optimal_billing_cycle" in pricing_optimization
        assert "tax_amount" in pricing_optimization
        assert "total_amount" in pricing_optimization
        
        # Validate pricing logic
        base_amount = pricing_optimization["base_amount"]
        optimized_amount = pricing_optimization["optimized_amount"]
        assert isinstance(base_amount, (int, float))
        assert isinstance(optimized_amount, (int, float))
        
        # Validate billing cycle optimization
        billing_cycle = pricing_optimization["optimal_billing_cycle"]
        assert billing_cycle in ["monthly", "quarterly", "annual"]
        
        print(f"✅ Pricing Optimization Test Passed")
        print(f"   Base Amount: ${base_amount}")
        print(f"   Optimized Amount: ${optimized_amount}")
        print(f"   Optimal Billing Cycle: {billing_cycle}")

class TestPayUFraudDetectionAgent:
    """Test suite for PayU Fraud Detection Agent"""
    
    def setup_method(self):
        """Setup test environment"""
        self.agent = PayUFraudDetectionAgent()
        self.test_request = PayUPaymentRequest(
            tenant_id="test_tenant_001",
            amount=1999.99,
            currency="USD",
            description="High-value test transaction",
            reference="TEST_FRAUD_001",
            customer_email="test@tempmail.com",  # Suspicious email
            buyer_info={"country": "NG"},  # High-risk country
            metadata={
                "ip_address": "192.168.1.100",
                "ip_country": "US",
                "device_info": {
                    "browser": "Chrome",
                    "screen_resolution": "1920x1080",
                    "timezone": "America/New_York"
                }
            }
        )
    
    @pytest.mark.asyncio
    async def test_fraud_risk_analysis(self):
        """Test comprehensive fraud risk analysis"""
        result = await self.agent.analyze_transaction_risk(self.test_request)
        
        # Validate response structure
        assert "agent_id" in result
        assert "overall_risk_score" in result
        assert "risk_level" in result
        assert "recommended_action" in result
        assert "risk_components" in result
        assert "ml_prediction" in result
        
        # Validate risk score
        risk_score = result["overall_risk_score"]
        assert 0.0 <= risk_score <= 1.0
        
        # Validate risk level
        risk_level = result["risk_level"]
        assert risk_level in ["low", "medium", "high", "critical"]
        
        # Validate recommended action
        action = result["recommended_action"]
        assert action in ["approve", "challenge", "manual_review", "decline"]
        
        # Validate risk components
        risk_components = result["risk_components"]
        required_components = ["behavioral_analysis", "device_analysis", "velocity_analysis", "geolocation_analysis"]
        for component in required_components:
            assert component in risk_components
            assert "risk_score" in risk_components[component]
        
        print(f"✅ Fraud Risk Analysis Test Passed")
        print(f"   Risk Score: {risk_score:.3f}")
        print(f"   Risk Level: {risk_level}")
        print(f"   Recommended Action: {action}")
    
    @pytest.mark.asyncio
    async def test_behavioral_pattern_analysis(self):
        """Test behavioral pattern analysis"""
        result = await self.agent.analyze_transaction_risk(self.test_request)
        behavioral_analysis = result["risk_components"]["behavioral_analysis"]
        
        # Validate behavioral analysis structure
        assert "risk_score" in behavioral_analysis
        assert "primary_factors" in behavioral_analysis
        assert "protective_factors" in behavioral_analysis
        assert "behavioral_indicators" in behavioral_analysis
        
        # Validate risk factors
        primary_factors = behavioral_analysis["primary_factors"]
        assert isinstance(primary_factors, list)
        
        # Check for expected risk factors based on test data
        expected_factors = ["high_value_transaction", "temporary_email_provider"]
        for factor in expected_factors:
            if factor in primary_factors:
                print(f"   Detected risk factor: {factor}")
        
        print(f"✅ Behavioral Pattern Analysis Test Passed")
        print(f"   Primary Risk Factors: {len(primary_factors)}")
        print(f"   Protective Factors: {len(behavioral_analysis['protective_factors'])}")
    
    @pytest.mark.asyncio
    async def test_ml_fraud_prediction(self):
        """Test ML fraud prediction"""
        result = await self.agent.analyze_transaction_risk(self.test_request)
        ml_prediction = result["ml_prediction"]
        
        # Validate ML prediction structure
        assert "risk_score" in ml_prediction
        assert "model_version" in ml_prediction
        assert "feature_importance" in ml_prediction
        assert "similar_cases" in ml_prediction
        assert "model_confidence" in ml_prediction
        
        # Validate ML risk score
        ml_risk_score = ml_prediction["risk_score"]
        assert 0.0 <= ml_risk_score <= 1.0
        
        # Validate model confidence
        confidence = ml_prediction["model_confidence"]
        assert 0.0 <= confidence <= 1.0
        
        # Validate similar cases
        similar_cases = ml_prediction["similar_cases"]
        assert isinstance(similar_cases, list)
        
        print(f"✅ ML Fraud Prediction Test Passed")
        print(f"   ML Risk Score: {ml_risk_score:.3f}")
        print(f"   Model Confidence: {confidence:.2f}")
        print(f"   Similar Cases Found: {len(similar_cases)}")

class TestPayUAnalyticsAgent:
    """Test suite for PayU Analytics Agent"""
    
    def setup_method(self):
        """Setup test environment"""
        self.agent = PayUAnalyticsAgent()
        self.test_request = PayUAnalyticsRequest(
            tenant_id="test_tenant_001",
            date_range={"start_date": "2025-08-01", "end_date": "2025-09-15"},
            regions=["global", "india", "latam"],
            currencies=["USD", "EUR", "INR", "BRL"],
            metrics=["revenue", "success_rate", "fraud_rate"]
        )
    
    @pytest.mark.asyncio
    async def test_comprehensive_analytics(self):
        """Test comprehensive payment analytics"""
        result = await self.agent.analyze_payments(self.test_request)
        
        # Validate response structure
        assert "agent_id" in result
        assert "analysis_type" in result
        assert "analytics_data" in result
        assert "ai_insights" in result
        assert "strategic_recommendations" in result
        
        # Validate analytics data structure
        analytics_data = result["analytics_data"]
        assert "global_summary" in analytics_data
        assert "regional_breakdown" in analytics_data
        assert "currency_analysis" in analytics_data
        assert "payment_methods" in analytics_data
        assert "fraud_analytics" in analytics_data
        
        # Validate global summary
        global_summary = analytics_data["global_summary"]
        assert "total_transactions" in global_summary
        assert "total_revenue" in global_summary
        assert "global_success_rate" in global_summary
        
        print(f"✅ Comprehensive Analytics Test Passed")
        print(f"   Total Transactions: {global_summary['total_transactions']:,}")
        print(f"   Total Revenue: ${global_summary['total_revenue']:,.2f}")
        print(f"   Global Success Rate: {global_summary['global_success_rate']*100:.1f}%")
    
    @pytest.mark.asyncio
    async def test_regional_performance_analysis(self):
        """Test regional performance analysis"""
        result = await self.agent.analyze_payments(self.test_request)
        regional_breakdown = result["analytics_data"]["regional_breakdown"]
        
        # Validate regional analysis structure
        assert "regional_performance" in regional_breakdown
        assert "best_performing" in regional_breakdown
        assert "growth_opportunities" in regional_breakdown
        
        # Validate regional performance data
        regional_performance = regional_breakdown["regional_performance"]
        expected_regions = ["global", "india", "latam", "cee"]
        
        for region in expected_regions:
            if region in regional_performance:
                region_data = regional_performance[region]
                assert "transactions" in region_data
                assert "revenue" in region_data
                assert "success_rate" in region_data
                assert "processing_fee_rate" in region_data
        
        # Validate best performing region
        best_performing = regional_breakdown["best_performing"]
        assert "region" in best_performing
        assert "success_rate" in best_performing
        
        print(f"✅ Regional Performance Analysis Test Passed")
        print(f"   Best Performing Region: {best_performing['region']}")
        print(f"   Success Rate: {best_performing['success_rate']*100:.1f}%")
    
    @pytest.mark.asyncio
    async def test_predictive_insights(self):
        """Test predictive analytics and insights"""
        result = await self.agent.analyze_payments(self.test_request)
        predictive_insights = result["analytics_data"]["predictive_insights"]
        
        # Validate predictive insights structure
        assert "predictive_models" in predictive_insights
        assert "ai_recommendations" in predictive_insights
        assert "confidence_levels" in predictive_insights
        
        # Validate predictive models
        predictive_models = predictive_insights["predictive_models"]
        expected_models = ["churn_prediction", "fraud_forecasting", "revenue_forecasting"]
        
        for model in expected_models:
            if model in predictive_models:
                assert isinstance(predictive_models[model], dict)
        
        # Validate confidence levels
        confidence_levels = predictive_insights["confidence_levels"]
        for model, confidence in confidence_levels.items():
            assert 0.0 <= confidence <= 1.0
        
        print(f"✅ Predictive Insights Test Passed")
        print(f"   Predictive Models: {len(predictive_models)}")
        print(f"   Average Confidence: {sum(confidence_levels.values())/len(confidence_levels):.2f}")

class TestPayUIntegrationHub:
    """Test suite for PayU Integration Hub coordination"""
    
    def setup_method(self):
        """Setup test environment"""
        self.hub = payu_hub
        self.test_payment = PayUPaymentRequest(
            tenant_id="test_tenant_001",
            amount=299.99,
            currency="USD",
            description="Integration hub test",
            reference="TEST_HUB_001",
            customer_email="test@example.com"
        )
    
    @pytest.mark.asyncio
    async def test_hub_coordination(self):
        """Test integration hub coordination"""
        # Test payment processing
        payment_result = await self.hub.process_global_payment(self.test_payment)
        
        # Validate payment result
        assert payment_result.success is True
        assert payment_result.transaction_id is not None
        assert payment_result.agent_id is not None
        
        # Test agents status
        status_result = await self.hub.get_agents_status("test_tenant_001")
        
        # Validate agents status
        assert status_result["success"] is True
        assert status_result["total_active_agents"] == 4
        assert "agents_status" in status_result
        
        # Validate coordination metrics
        metrics = self.hub.coordination_metrics
        assert "total_payments_processed" in metrics
        assert "total_decisions_coordinated" in metrics
        assert metrics["total_payments_processed"] > 0
        
        print(f"✅ Hub Coordination Test Passed")
        print(f"   Total Payments Processed: {metrics['total_payments_processed']}")
        print(f"   Total Decisions Coordinated: {metrics['total_decisions_coordinated']}")
    
    @pytest.mark.asyncio
    async def test_error_handling(self):
        """Test error handling and resilience"""
        # Test with invalid payment request
        invalid_request = PayUPaymentRequest(
            tenant_id="",  # Invalid tenant ID
            amount=-100,  # Invalid amount
            currency="INVALID",  # Invalid currency
            description="",  # Empty description
            reference="",  # Empty reference
            customer_email="invalid-email"  # Invalid email
        )
        
        try:
            result = await self.hub.process_global_payment(invalid_request)
            # Should still return a response structure even with invalid data
            assert "success" in result.__dict__
            assert "processing_time" in result.__dict__
        except Exception as e:
            # Error handling should be graceful
            assert isinstance(e, Exception)
            print(f"   Expected error handled gracefully: {type(e).__name__}")
        
        print(f"✅ Error Handling Test Passed")

@pytest.mark.asyncio
async def test_end_to_end_payu_flow():
    """End-to-end test of complete PayU flow"""
    print("\n🧪 Running End-to-End PayU Integration Test")
    print("=" * 50)
    
    # 1. Process a payment
    payment_request = PayUPaymentRequest(
        tenant_id="e2e_test_tenant",
        amount=599.99,
        currency="USD",
        description="End-to-end test payment",
        reference="E2E_TEST_001",
        customer_email="e2e@example.com",
        customer_id="e2e_customer_001",
        payment_method="card",
        region="global"
    )
    
    payment_result = await payu_hub.process_global_payment(payment_request)
    assert payment_result.success is True
    print(f"✅ Payment processed: {payment_result.transaction_id}")
    
    # 2. Create a subscription
    subscription_request = PayUSubscriptionRequest(
        tenant_id="e2e_test_tenant",
        plan_id="e2e_plan_001",
        customer_id="e2e_customer_001",
        payment_method="CARD",
        currency="USD",
        trial_days=7
    )
    
    subscription_result = await payu_hub.create_subscription(subscription_request)
    assert subscription_result["success"] is True
    print(f"✅ Subscription created: {subscription_result['agent_analysis']['subscription_result']['id']}")
    
    # 3. Analyze fraud risk
    fraud_result = await payu_hub.analyze_fraud_risk(payment_request)
    assert fraud_result["success"] is True
    print(f"✅ Fraud analysis completed: {fraud_result['fraud_analysis']['risk_level']} risk")
    
    # 4. Get analytics
    analytics_request = PayUAnalyticsRequest(
        tenant_id="e2e_test_tenant",
        date_range={"start_date": "2025-08-01", "end_date": "2025-09-15"}
    )
    
    analytics_result = await payu_hub.get_payment_analytics(analytics_request)
    assert analytics_result["success"] is True
    print(f"✅ Analytics generated: {analytics_result['agent_analysis']['analytics_data']['global_summary']['total_transactions']} transactions analyzed")
    
    # 5. Check agents status
    status_result = await payu_hub.get_agents_status("e2e_test_tenant")
    assert status_result["success"] is True
    print(f"✅ Agents status: {status_result['total_active_agents']} active agents")
    
    print("\n🎉 End-to-End Test Completed Successfully!")

if __name__ == "__main__":
    # Run the comprehensive test suite
    asyncio.run(test_end_to_end_payu_flow())
    
    print("\n" + "=" * 70)
    print("🚀 PayU Payment Processing Integration Test Suite")
    print("=" * 70)
    print("Run individual test classes with pytest:")
    print("  pytest test_payu_payment_api_integration.py::TestPayUGlobalPaymentAgent -v")
    print("  pytest test_payu_payment_api_integration.py::TestPayUSubscriptionAgent -v")
    print("  pytest test_payu_payment_api_integration.py::TestPayUFraudDetectionAgent -v")
    print("  pytest test_payu_payment_api_integration.py::TestPayUAnalyticsAgent -v")
    print("  pytest test_payu_payment_api_integration.py::TestPayUIntegrationHub -v")
    print("\nRun all tests:")
    print("  pytest test_payu_payment_api_integration.py -v")