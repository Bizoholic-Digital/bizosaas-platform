#!/usr/bin/env python3
"""
Order Processing Agent Worker
Handles automated order validation, fraud detection, and inventory checking
"""

import os
import sys
from crewai import Agent
from base_worker import CrewAIWorker

# Order Processing Agent Definition
order_agent = Agent(
    role="E-commerce Order Processing Specialist",
    goal="Process and validate customer orders with high accuracy and fraud prevention",
    backstory="""You are an experienced e-commerce operations specialist with expertise in:
    - Order validation and verification
    - Fraud detection and risk assessment
    - Inventory management and stock checking
    - Payment processing validation
    - Customer communication for order issues

    You have processed over 100,000 orders and have a 99.8% accuracy rate.
    You are meticulous about details and always prioritize customer satisfaction
    while protecting the business from fraudulent transactions.

    Your decisions are data-driven and you always document your reasoning
    for any order holds or rejections.""",

    verbose=True,
    allow_delegation=False,
    tools=[]  # Tools will be added based on task requirements
)

def handle_order_result(task_id: str, result: dict):
    """
    Custom result handler for order processing

    Args:
        task_id: Order task ID
        result: Processing result
    """
    if result['status'] == 'completed':
        print(f"✅ Order {task_id} processed successfully")
        print(f"   Execution time: {result['execution_time_seconds']:.2f}s")

        # Additional order-specific logging
        # In production, this could:
        # - Update order status in database
        # - Send confirmation email
        # - Trigger fulfillment workflow
        # - Update inventory

    else:
        print(f"❌ Order {task_id} processing failed")
        print(f"   Error: {result.get('error', 'Unknown error')}")

        # Order-specific error handling
        # In production, this could:
        # - Send alert to operations team
        # - Put order on manual review queue
        # - Notify customer of processing delay

def main():
    """Start order processing worker"""

    # Queue configuration
    queue_name = os.getenv('QUEUE_NAME', 'auto_orders')

    print("=" * 70)
    print("🛒 BizOSaaS Order Processing Agent")
    print("=" * 70)
    print(f"Queue: {queue_name}")
    print(f"Agent: {order_agent.role}")
    print(f"Ready to process orders with fraud detection and validation")
    print("=" * 70)
    print()

    # Create and start worker
    worker = CrewAIWorker(
        queue_name=queue_name,
        agent=order_agent,
        result_handler=handle_order_result
    )

    try:
        worker.start()
    except KeyboardInterrupt:
        print("\n🛑 Order agent shutting down...")
        worker.cleanup()
        sys.exit(0)
    except Exception as e:
        print(f"❌ Fatal error in order agent: {e}")
        worker.cleanup()
        sys.exit(1)

if __name__ == '__main__':
    main()
