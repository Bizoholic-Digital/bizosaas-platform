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
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    # Check for OpenRouter key
    api_key = os.getenv("OPENROUTER_API_KEY")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
        print("✅ Using OPENROUTER_API_KEY")
    else:
        print("❌ ERROR: Real API key required for LLM testing")
        print("Set OPENAI_API_KEY or OPENROUTER_API_KEY in .env.testing")
        sys.exit(1)

# Check for custom base URL (e.g. OpenRouter)
if os.getenv("OPENROUTER_API_KEY") or "openrouter" in (os.getenv("OPENAI_API_BASE") or ""):
    if not os.getenv("OPENAI_API_BASE"):
        os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"
        print("✅ Using OpenRouter API Base: https://openrouter.ai/api/v1")
    
    # Default to a good model if not set
    if not os.getenv("OPENAI_MODEL_NAME"):
        os.environ["OPENAI_MODEL_NAME"] = "openai/gpt-3.5-turbo" # Or any default
        print(f"ℹ️  Using default model: {os.environ['OPENAI_MODEL_NAME']}")

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
