import asyncio
import sys
import os
import logging
from typing import List, Tuple

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("HandoffTest")

async def test_routing():
    logger.info("Starting Agent Handoff Routing Test...")
    
    try:
        from chat_api import chat_manager, AgentCategory
        
        test_cases: List[Tuple[str, str]] = [
            ("I need a new marketing strategy for 2024", "marketing_strategist"),
            ("Can you write a blog post about AI?", "content_creator"),
            ("What are the best keywords for 'SaaS Platform'?", "seo_specialist"),
            ("Score this lead: John Doe from Acme Corp", "lead_scoring"),
            ("Forecast our revenue for Q4 based on current pipeline", "sales_intelligence"),
            ("Analyze the sales pipeline deals", "sales_intelligence"),
            ("I have a problem with my account", "customer_support"),
            ("Audit my website presence", "digital_audit"),
        ]
        
        passed = 0
        failed = 0
        
        print("\n=== Routing Test Results ===")
        print(f"{'Query':<50} | {'Expected':<20} | {'Actual':<20} | {'Result'}")
        print("-" * 105)
        
        for query, expected_agent in test_cases:
            # We use the internal _select_best_agent method to test routing logic directly
            # avoiding full execution which requires API keys
            session_mock = type('obj', (object,), {'context': {}})
            selected_agent = await chat_manager._select_best_agent(query, session_mock)
            
            status = "✅ PASS" if selected_agent == expected_agent else "❌ FAIL"
            if selected_agent == expected_agent:
                passed += 1
            else:
                failed += 1
                
            print(f"{query[:47]+'...':<50} | {expected_agent:<20} | {selected_agent:<20} | {status}")
            
        print("-" * 105)
        print(f"Total: {len(test_cases)} | Passed: {passed} | Failed: {failed}")
        
        if failed == 0:
            logger.info("All routing tests passed successfully!")
            return True
        else:
            logger.error(f"{failed} routing tests failed.")
            return False
            
    except ImportError as e:
        logger.error(f"Import failed: {e}")
        return False
    except Exception as e:
        logger.error(f"Test failed with error: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_routing())
    sys.exit(0 if success else 1)
