# E-Commerce Workflows Testing & Deployment Strategy

**Project:** BizOSaaS E-Commerce AI Workflows  
**Date:** 2026-01-08  
**Status:** Ready for Testing  
**Workflows:** 3 (Sourcing, Operations, Inventory/Logistics)

---

## Executive Summary

All three e-commerce workflows are **fully implemented** and ready for testing. This document outlines the recommended testing strategy, comparing local vs. server-based testing, and provides a phased deployment plan.

---

## 📦 Implemented E-Commerce Workflows

### Workflow 7: ECommerceSourcingWorkflow ✅
**Purpose:** Product sourcing and market entry strategy for Coreldove brand

**Agents Orchestrated:**
1. Market Research Agent - Identify sourcing opportunities
2. Competitive Intelligence Agent - Analyze competitor suppliers
3. Product Sourcing Agent - Validate suppliers
4. Strategic Planning Agent - Develop sourcing strategy
5. Financial Analytics Agent - Forecast profitability

**Output:**
- Sourcing opportunities
- Supplier validation results
- Sourcing strategy
- Financial forecast
- Next steps for human approval

**Status:** ✅ Implemented, ⬜ Tested with LLM

---

### Workflow 9: ECommerceOperationsWorkflow ✅
**Purpose:** 360-degree order processing and management automation

**Agents Orchestrated:**
1. Order Orchestration Agent - Process orders, detect fraud
2. Data Analytics Agent - Analyze operational efficiency
3. Sales Intelligence Agent - Identify VIP customers

**Output:**
- Order processing results
- Operational analysis
- VIP customer triggers
- Batch processing status

**Status:** ✅ Implemented, ⬜ Tested with LLM

---

### Workflow 10: ECommerceInventoryLogisticsWorkflow ✅
**Purpose:** Intelligent inventory tracking and logistics optimization

**Agents Orchestrated:**
1. Inventory Management Agent - Audit and demand forecasting
2. Financial Analytics Agent - Logistics cost optimization
3. Strategic Planning Agent - Supply chain resilience plan

**Output:**
- Inventory audit results
- Cost optimization recommendations
- 90-day strategic plan
- Sync status

**Status:** ✅ Implemented, ⬜ Tested with LLM

---

## 🧪 Testing Strategy: Local vs. Server

### Option 1: Local Testing (RECOMMENDED for Initial Testing)

#### ✅ Advantages
1. **Fast Iteration:** Immediate feedback, no deployment delays
2. **Cost Control:** Can use cheaper LLM models or limit test runs
3. **Easy Debugging:** Full access to logs, breakpoints, and debugging tools
4. **No Downtime Risk:** Production services unaffected
5. **Environment Control:** Can test with different API keys, configurations
6. **Quick Fixes:** Edit code and retest immediately

#### ⚠️ Disadvantages
1. **Environment Differences:** Local may differ from production
2. **Limited Resources:** Local machine may have less RAM/CPU
3. **Network Differences:** Different latency, connectivity patterns

#### 📋 Local Testing Setup
```bash
# 1. Ensure virtual environment is active
source /home/alagiri/projects/bizosaas-platform/.venv/bin/activate

# 2. Set up environment variables
cat > .env.testing <<EOF
OPENAI_API_KEY=sk-your-real-api-key-here
CREWAI_TRACING_ENABLED=true
REDIS_URL=redis://localhost:6379
DATABASE_URL=postgresql://localhost/bizosaas_test
LOG_LEVEL=DEBUG
EOF

# 3. Create test script
python test_ecommerce_workflows_llm.py

# 4. Monitor costs and outputs
tail -f logs/workflow_execution.log
```

#### 💰 Cost Management for Local Testing
- **Start Small:** Test with 1-2 workflows first
- **Use GPT-3.5:** Cheaper than GPT-4 for initial tests
- **Limit Iterations:** Set max retries to 1-2
- **Cache Results:** Save successful outputs to avoid re-running
- **Budget Alert:** Set OpenAI usage alerts at $10, $25, $50

---

### Option 2: Server Testing (KVM8)

#### ✅ Advantages
1. **Production Environment:** Tests in actual deployment conditions
2. **Full Integration:** Tests with real databases, Redis, services
3. **Scalability Testing:** Can test under load
4. **Real Network Conditions:** Actual latency and connectivity
5. **Team Access:** Other team members can monitor/test

#### ⚠️ Disadvantages
1. **Slower Iteration:** Deploy → Test → Fix → Redeploy cycle
2. **Deployment Overhead:** Docker builds, container restarts
3. **Potential Downtime:** Could affect production if not isolated
4. **Harder Debugging:** Limited access to logs, no breakpoints
5. **Resource Contention:** May compete with other services

#### 📋 Server Testing Setup
```bash
# 1. Create staging environment on KVM8
# 2. Deploy AI agents service to staging
# 3. Configure separate API keys (staging budget)
# 4. Run tests via API endpoints
# 5. Monitor via Grafana/Prometheus
```

---

## 🎯 RECOMMENDED APPROACH: Hybrid Testing Strategy

### Phase 1: Local Development Testing (Day 1)
**Goal:** Validate workflow logic and LLM integration

```bash
Duration: 2-4 hours
Budget: $10-20
Environment: Local machine
```

**Steps:**
1. ✅ Create test script for e-commerce workflows
2. ✅ Test with real OpenAI API (GPT-3.5-turbo)
3. ✅ Validate output structure and quality
4. ✅ Fix any bugs or prompt issues
5. ✅ Document successful test cases

**Success Criteria:**
- All 3 workflows execute without errors
- LLM outputs are coherent and relevant
- Execution time < 5 minutes per workflow
- Cost per workflow < $3

---

### Phase 2: Local Integration Testing (Day 1-2)
**Goal:** Test workflows with realistic data

```bash
Duration: 2-3 hours
Budget: $15-25
Environment: Local machine
```

**Steps:**
1. ✅ Create realistic test data (Coreldove products, orders, inventory)
2. ✅ Test all 3 workflows with production-like scenarios
3. ✅ Validate inter-workflow data flow
4. ✅ Test error handling and edge cases
5. ✅ Optimize prompts for better outputs

**Success Criteria:**
- Workflows handle realistic data volumes
- Error handling works correctly
- Outputs are actionable and accurate
- Performance is acceptable

---

### Phase 3: Server Staging Deployment (Day 2)
**Goal:** Deploy to KVM8 staging environment

```bash
Duration: 3-4 hours
Budget: $0 (deployment only)
Environment: KVM8 staging
```

**Steps:**
1. ✅ Build Docker image with tested code
2. ✅ Deploy to KVM8 staging environment
3. ✅ Configure environment variables
4. ✅ Run smoke tests via API
5. ✅ Verify logging and monitoring

**Success Criteria:**
- Service deploys successfully
- Health checks pass
- API endpoints respond correctly
- Logs are accessible

---

### Phase 4: Server Integration Testing (Day 2-3)
**Goal:** Test in production-like environment

```bash
Duration: 2-3 hours
Budget: $20-30
Environment: KVM8 staging
```

**Steps:**
1. ✅ Test workflows via API endpoints
2. ✅ Verify database integration
3. ✅ Test with multiple concurrent requests
4. ✅ Monitor resource usage (CPU, RAM, network)
5. ✅ Validate end-to-end flow

**Success Criteria:**
- All workflows work via API
- Performance meets SLAs
- No resource bottlenecks
- Monitoring dashboards show correct metrics

---

### Phase 5: Production Deployment (Day 3-4)
**Goal:** Deploy to production with monitoring

```bash
Duration: 2-3 hours
Budget: $0 (deployment only)
Environment: KVM8 production
```

**Steps:**
1. ✅ Create production deployment plan
2. ✅ Deploy during low-traffic window
3. ✅ Run production smoke tests
4. ✅ Enable monitoring and alerts
5. ✅ Document rollback procedure

**Success Criteria:**
- Zero-downtime deployment
- All health checks pass
- Monitoring active
- Users can access workflows

---

## 🧪 Test Script for Local LLM Testing

I'll create a comprehensive test script for local testing:

### File: `test_ecommerce_workflows_llm.py`

```python
#!/usr/bin/env python3
"""
E-Commerce Workflows - Real LLM Testing Script
Tests all 3 e-commerce workflows with actual OpenAI API calls
"""
import asyncio
import os
import sys
import json
from datetime import datetime
from typing import Dict, Any

# Ensure we're using the real API key
if not os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY").startswith("sk-mock"):
    print("❌ ERROR: Real OPENAI_API_KEY required for LLM testing")
    print("Set it in .env.testing or export OPENAI_API_KEY=sk-...")
    sys.exit(1)

# Enable tracing for debugging
os.environ["CREWAI_TRACING_ENABLED"] = "true"

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import refined_agent_registry, setup_centralized_agents
from agents.base_agent import AgentTaskRequest

class TestResults:
    def __init__(self):
        self.results = []
        self.total_cost = 0.0
        self.total_time = 0.0
    
    def add_result(self, workflow_id: str, success: bool, duration: float, 
                   cost: float, output: Dict[str, Any], error: str = None):
        self.results.append({
            "workflow": workflow_id,
            "success": success,
            "duration_seconds": duration,
            "estimated_cost": cost,
            "output_summary": self._summarize_output(output) if output else None,
            "error": error,
            "timestamp": datetime.utcnow().isoformat()
        })
        self.total_cost += cost
        self.total_time += duration
    
    def _summarize_output(self, output: Dict[str, Any]) -> Dict[str, Any]:
        """Create a summary of the output for logging"""
        summary = {}
        for key, value in output.items():
            if isinstance(value, dict):
                summary[key] = f"<dict with {len(value)} keys>"
            elif isinstance(value, list):
                summary[key] = f"<list with {len(value)} items>"
            elif isinstance(value, str) and len(value) > 100:
                summary[key] = value[:100] + "..."
            else:
                summary[key] = value
        return summary
    
    def print_summary(self):
        print("\n" + "=" * 70)
        print("E-COMMERCE WORKFLOWS - LLM TEST RESULTS")
        print("=" * 70)
        
        for result in self.results:
            status = "✅ PASS" if result["success"] else "❌ FAIL"
            print(f"\n{result['workflow']:40} : {status}")
            print(f"  Duration: {result['duration_seconds']:.2f}s")
            print(f"  Est. Cost: ${result['estimated_cost']:.4f}")
            if result['error']:
                print(f"  Error: {result['error']}")
        
        print("\n" + "-" * 70)
        print(f"Total Tests: {len(self.results)}")
        print(f"Passed: {sum(1 for r in self.results if r['success'])}")
        print(f"Failed: {sum(1 for r in self.results if not r['success'])}")
        print(f"Total Time: {self.total_time:.2f}s")
        print(f"Total Cost: ${self.total_cost:.4f}")
        print("=" * 70)
    
    def save_to_file(self, filename: str):
        """Save detailed results to JSON file"""
        with open(filename, 'w') as f:
            json.dump({
                "test_run": datetime.utcnow().isoformat(),
                "summary": {
                    "total_tests": len(self.results),
                    "passed": sum(1 for r in self.results if r['success']),
                    "failed": sum(1 for r in self.results if not r['success']),
                    "total_time_seconds": self.total_time,
                    "total_cost_usd": self.total_cost
                },
                "results": self.results
            }, f, indent=2)
        print(f"\n📄 Detailed results saved to: {filename}")

async def test_workflow(workflow_id: str, input_data: Dict[str, Any], 
                       test_results: TestResults):
    """Test a single workflow with real LLM calls"""
    print(f"\n{'='*70}")
    print(f"Testing: {workflow_id}")
    print(f"Input: {json.dumps(input_data, indent=2)}")
    print(f"{'='*70}")
    
    if workflow_id not in refined_agent_registry:
        print(f"❌ Workflow '{workflow_id}' not found in registry!")
        test_results.add_result(workflow_id, False, 0, 0, None, "Not found in registry")
        return
    
    workflow = refined_agent_registry[workflow_id]
    
    request = AgentTaskRequest(
        tenant_id="test-tenant-llm",
        user_id="test-user-llm",
        task_type="workflow_execution",
        task_description=f"LLM test for {workflow_id}",
        input_data=input_data
    )
    
    start_time = datetime.utcnow()
    
    try:
        print(f"⏳ Executing workflow (this may take 2-5 minutes)...")
        result = await workflow.execute_task(request)
        
        end_time = datetime.utcnow()
        duration = (end_time - start_time).total_seconds()
        
        # Estimate cost (rough approximation)
        # Assume each agent call costs ~$0.50 on average
        num_agents = len(input_data.get('expected_agents', [3, 4, 5]))
        estimated_cost = num_agents * 0.50
        
        print(f"✅ Workflow completed successfully!")
        print(f"⏱️  Duration: {duration:.2f}s")
        print(f"💰 Estimated cost: ${estimated_cost:.4f}")
        
        if hasattr(result, 'result'):
            output = result.result
            print(f"\n📊 Output Summary:")
            for key, value in output.items():
                if isinstance(value, (dict, list)):
                    print(f"  {key}: {type(value).__name__} ({len(value)} items)")
                else:
                    print(f"  {key}: {value}")
            
            test_results.add_result(workflow_id, True, duration, estimated_cost, output)
        else:
            print(f"⚠️  Unexpected result format: {type(result)}")
            test_results.add_result(workflow_id, False, duration, estimated_cost, None, 
                                   "Unexpected result format")
        
    except Exception as e:
        end_time = datetime.utcnow()
        duration = (end_time - start_time).total_seconds()
        
        print(f"❌ Workflow failed: {e}")
        import traceback
        traceback.print_exc()
        
        test_results.add_result(workflow_id, False, duration, 0, None, str(e))

async def main():
    """Run all e-commerce workflow tests"""
    print("\n" + "🚀" * 35)
    print("E-COMMERCE WORKFLOWS - REAL LLM TESTING")
    print("🚀" * 35)
    print(f"\nTest Started: {datetime.utcnow().isoformat()}")
    print(f"OpenAI API Key: {os.getenv('OPENAI_API_KEY')[:20]}...")
    print(f"Tracing Enabled: {os.getenv('CREWAI_TRACING_ENABLED')}")
    
    # Initialize agents
    print("\n📦 Initializing AI agents...")
    await setup_centralized_agents()
    print("✅ Agents initialized")
    
    # Create test results tracker
    test_results = TestResults()
    
    # Define test cases with realistic data
    test_cases = [
        (
            "ecommerce_sourcing_workflow",
            {
                "brand": "Coreldove",
                "niche": "Sustainable Kitchen & Dining",
                "target_market": "European Union",
                "budget_range": "medium",
                "expected_agents": ["research", "intel", "sourcing", "strategic", "finance"]
            }
        ),
        (
            "ecommerce_operations_workflow",
            {
                "order_batch": [
                    {"order_id": "ORD-001", "customer": "John Doe", "total": 156.99, "items": 3},
                    {"order_id": "ORD-002", "customer": "Jane Smith", "total": 89.50, "items": 2},
                    {"order_id": "ORD-003", "customer": "Bob Johnson", "total": 234.00, "items": 5}
                ],
                "priority": "high",
                "expected_agents": ["orchestrator", "analytics", "sales_intel"]
            }
        ),
        (
            "ecommerce_inventory_workflow",
            {
                "warehouse_id": "WH-EU-001",
                "current_stock": {
                    "SKU-001": 150,
                    "SKU-002": 45,
                    "SKU-003": 200
                },
                "reorder_threshold": 50,
                "forecast_period_days": 90,
                "expected_agents": ["inventory", "financial", "strategic"]
            }
        )
    ]
    
    # Run tests sequentially to avoid rate limits
    for workflow_id, input_data in test_cases:
        await test_workflow(workflow_id, input_data, test_results)
        
        # Add delay between tests to avoid rate limiting
        if workflow_id != test_cases[-1][0]:
            print("\n⏸️  Waiting 30 seconds before next test (rate limit protection)...")
            await asyncio.sleep(30)
    
    # Print and save results
    test_results.print_summary()
    
    # Save detailed results
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    results_file = f"test_results_ecommerce_llm_{timestamp}.json"
    test_results.save_to_file(results_file)
    
    print(f"\n✅ Testing complete!")
    print(f"📊 Review detailed results in: {results_file}")
    
    # Return success if all tests passed
    all_passed = all(r["success"] for r in test_results.results)
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
```

---

## 💰 Cost Estimation

### Per Workflow Costs (Estimated)
| Workflow | Agents | Est. Tokens | Est. Cost |
|----------|--------|-------------|-----------|
| **Sourcing** | 5 | ~15,000 | $2.50 |
| **Operations** | 3 | ~8,000 | $1.50 |
| **Inventory** | 3 | ~8,000 | $1.50 |
| **TOTAL** | 11 | ~31,000 | **$5.50** |

### Testing Budget Recommendations
- **Initial Local Testing:** $10-20 (2-3 full test runs)
- **Integration Testing:** $20-30 (multiple scenarios)
- **Server Staging:** $30-50 (load testing, edge cases)
- **Total Testing Budget:** **$60-100**

---

## 📋 Testing Checklist

### Pre-Testing
- [ ] Virtual environment activated
- [ ] Real OpenAI API key configured
- [ ] Budget alerts set in OpenAI dashboard
- [ ] Test data prepared
- [ ] Logging configured

### Local Testing
- [ ] Run test script with 1 workflow first
- [ ] Verify output quality
- [ ] Check execution time
- [ ] Monitor costs
- [ ] Fix any issues
- [ ] Run all 3 workflows
- [ ] Document results

### Server Deployment
- [ ] Build Docker image
- [ ] Deploy to staging
- [ ] Configure environment
- [ ] Run smoke tests
- [ ] Monitor resources
- [ ] Verify API endpoints

### Production
- [ ] Create deployment plan
- [ ] Schedule deployment window
- [ ] Deploy to production
- [ ] Run health checks
- [ ] Enable monitoring
- [ ] Document rollback procedure

---

## 🎯 FINAL RECOMMENDATION

### Start with Local Testing ✅

**Rationale:**
1. **Faster feedback loop** - Fix issues immediately
2. **Lower risk** - No impact on production
3. **Cost control** - Can limit test runs easily
4. **Better debugging** - Full access to logs and code
5. **Proven approach** - OnboardingStrategyWorkflow tested locally first

### Timeline
- **Day 1 (Today):** Local LLM testing of all 3 workflows
- **Day 2:** Fix issues, optimize prompts, prepare for deployment
- **Day 3:** Deploy to KVM8 staging, run integration tests
- **Day 4:** Production deployment with monitoring

### Next Immediate Steps
1. ✅ Create `.env.testing` with real OpenAI API key
2. ✅ Run `test_ecommerce_workflows_llm.py` locally
3. ✅ Review outputs and costs
4. ✅ Iterate and optimize
5. ✅ Prepare for server deployment

---

**Document Version:** 1.0  
**Last Updated:** 2026-01-08T10:50:00Z  
**Recommended Approach:** Local Testing First, then Server Deployment
