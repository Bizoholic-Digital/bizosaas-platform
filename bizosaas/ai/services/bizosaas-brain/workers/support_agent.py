#!/usr/bin/env python3
"""
Support Ticket Agent Worker
Handles automated customer support ticket classification, sentiment analysis, and auto-responses
"""

import os
import sys
from crewai import Agent
from base_worker import CrewAIWorker

# Support Ticket Agent Definition
support_agent = Agent(
    role="Customer Support Specialist",
    goal="Provide exceptional customer support with fast response times and high satisfaction scores",
    backstory="""You are a highly skilled customer support specialist with expertise in:
    - Ticket classification and prioritization
    - Sentiment analysis and emotional intelligence
    - Product knowledge across all business domains
    - Conflict resolution and de-escalation
    - Multi-channel support (email, chat, phone)

    You have successfully resolved over 50,000 support tickets with a 95% customer
    satisfaction rating. You are known for your empathy, patience, and ability to
    explain complex technical concepts in simple terms.

    You follow these principles:
    1. Customer satisfaction is the top priority
    2. Fast response times are critical
    3. Clear communication prevents confusion
    4. Escalate when human judgment is needed
    5. Always maintain a professional and friendly tone

    You can auto-resolve simple issues but recognize when human expertise is required.""",

    verbose=True,
    allow_delegation=False,
    tools=[]  # Tools will be added based on task requirements
)

def handle_support_result(task_id: str, result: dict):
    """
    Custom result handler for support ticket processing

    Args:
        task_id: Support ticket ID
        result: Processing result
    """
    if result['status'] == 'completed':
        print(f"✅ Ticket {task_id} processed successfully")
        print(f"   Execution time: {result['execution_time_seconds']:.2f}s")

        # Additional support-specific logging
        # In production, this could:
        # - Update ticket status in CRM
        # - Send response to customer
        # - Log interaction history
        # - Update customer satisfaction metrics
        # - Route to appropriate department if needed

    else:
        print(f"❌ Ticket {task_id} processing failed")
        print(f"   Error: {result.get('error', 'Unknown error')}")

        # Support-specific error handling
        # In production, this could:
        # - Route ticket to human agent
        # - Send "we're looking into this" message to customer
        # - Alert support team lead
        # - Log for quality assurance review

def main():
    """Start support ticket processing worker"""

    # Queue configuration
    queue_name = os.getenv('QUEUE_NAME', 'auto_support_tickets')

    print("=" * 70)
    print("🎧 BizOSaaS Support Ticket Agent")
    print("=" * 70)
    print(f"Queue: {queue_name}")
    print(f"Agent: {support_agent.role}")
    print(f"Ready to process support tickets with sentiment analysis")
    print("=" * 70)
    print()

    # Create and start worker
    worker = CrewAIWorker(
        queue_name=queue_name,
        agent=support_agent,
        result_handler=handle_support_result
    )

    try:
        worker.start()
    except KeyboardInterrupt:
        print("\n🛑 Support agent shutting down...")
        worker.cleanup()
        sys.exit(0)
    except Exception as e:
        print(f"❌ Fatal error in support agent: {e}")
        worker.cleanup()
        sys.exit(1)

if __name__ == '__main__':
    main()
