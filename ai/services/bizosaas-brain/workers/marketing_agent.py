#!/usr/bin/env python3
"""
Marketing Campaign Agent Worker
Handles automated marketing campaign analysis, content generation, and performance optimization
"""

import os
import sys
from crewai import Agent
from base_worker import CrewAIWorker

# Marketing Campaign Agent Definition
marketing_agent = Agent(
    role="Marketing Campaign Specialist",
    goal="Create and optimize high-performing marketing campaigns that drive engagement and conversions",
    backstory="""You are a seasoned digital marketing expert with expertise in:
    - Campaign strategy and planning
    - Content creation and copywriting
    - SEO and content optimization
    - Email marketing and automation
    - Social media marketing
    - Performance analytics and A/B testing
    - Customer segmentation and targeting

    You have managed over 500 successful campaigns across multiple industries,
    achieving an average ROI of 400%. You understand the psychology of persuasion
    and know how to craft compelling messages that resonate with target audiences.

    Your approach is data-driven and creative:
    1. Analyze audience demographics and behavior
    2. Craft compelling, authentic messaging
    3. Test multiple variations for optimization
    4. Monitor performance metrics continuously
    5. Adapt strategies based on results

    You excel at:
    - Writing attention-grabbing subject lines
    - Creating persuasive call-to-actions
    - Optimizing content for search engines
    - Identifying trending topics and hashtags
    - Recommending the best channels and timing

    You always balance creativity with measurable business outcomes.""",

    verbose=True,
    allow_delegation=False,
    tools=[]  # Tools will be added based on task requirements
)

def handle_marketing_result(task_id: str, result: dict):
    """
    Custom result handler for marketing campaign processing

    Args:
        task_id: Campaign task ID
        result: Processing result
    """
    if result['status'] == 'completed':
        print(f"✅ Campaign {task_id} processed successfully")
        print(f"   Execution time: {result['execution_time_seconds']:.2f}s")

        # Additional marketing-specific logging
        # In production, this could:
        # - Save campaign content to database
        # - Schedule campaign for publishing
        # - Update marketing automation platform
        # - Generate performance baseline
        # - Notify marketing team for review

    else:
        print(f"❌ Campaign {task_id} processing failed")
        print(f"   Error: {result.get('error', 'Unknown error')}")

        # Marketing-specific error handling
        # In production, this could:
        # - Alert marketing manager
        # - Save draft for manual review
        # - Log failure for quality analysis
        # - Suggest alternative approaches

def main():
    """Start marketing campaign processing worker"""

    # Queue configuration
    queue_name = os.getenv('QUEUE_NAME', 'auto_marketing')

    print("=" * 70)
    print("📢 BizOSaaS Marketing Campaign Agent")
    print("=" * 70)
    print(f"Queue: {queue_name}")
    print(f"Agent: {marketing_agent.role}")
    print(f"Ready to create and optimize marketing campaigns")
    print("=" * 70)
    print()

    # Create and start worker
    worker = CrewAIWorker(
        queue_name=queue_name,
        agent=marketing_agent,
        result_handler=handle_marketing_result
    )

    try:
        worker.start()
    except KeyboardInterrupt:
        print("\n🛑 Marketing agent shutting down...")
        worker.cleanup()
        sys.exit(0)
    except Exception as e:
        print(f"❌ Fatal error in marketing agent: {e}")
        worker.cleanup()
        sys.exit(1)

if __name__ == '__main__':
    main()
