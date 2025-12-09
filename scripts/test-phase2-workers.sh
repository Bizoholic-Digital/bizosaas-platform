#!/bin/bash

# Phase 2 End-to-End Test - Verify Workers Process Tasks
# Tests: RabbitMQ → Worker → Kafka flow

set -e

echo "=========================================="
echo "Phase 2 Worker Integration Test"
echo "=========================================="

SSH_PASS='&k3civYG5Q6YPb'
SSH_HOST='root@72.60.219.244'

echo ""
echo "1. Publishing test order to auto_orders queue..."

# Create test order task
TEST_ORDER=$(cat <<'EOF'
{
  "id": "test-order-001",
  "description": "Process test order for customer John Doe - Order #12345 for $99.99",
  "expected_output": "Order validated, inventory checked, payment processed",
  "task_data": {
    "order_id": "12345",
    "customer": "John Doe",
    "amount": 99.99,
    "items": [
      {"product_id": "PROD-001", "quantity": 2, "price": 49.99}
    ],
    "payment_method": "credit_card",
    "shipping_address": "123 Test St, Test City, TC 12345"
  }
}
EOF
)

# Publish to RabbitMQ - Using a simpler approach to avoid heredoc nesting
sshpass -p "$SSH_PASS" ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null $SSH_HOST bash << ENDSSH
docker run --rm --network dokploy-network \
  -e RABBITMQ_HOST='infrastructureservices-rabbitmq-gktndk-rabbitmq-1' \
  -e RABBITMQ_PASS='lemn3f1e' \
  python:3.11-slim bash -c "
    pip install -q pika && \
    cat > /tmp/publish.py << 'PYEOF'
import pika
import os

message = '''$TEST_ORDER'''

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=os.environ.get('RABBITMQ_HOST'),
        port=5672,
        virtual_host='/',
        credentials=pika.PlainCredentials('admin', os.environ.get('RABBITMQ_PASS'))
    )
)

channel = connection.channel()

channel.basic_publish(
    exchange='',
    routing_key='auto_orders',
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=2,
        priority=10
    )
)

print('✅ Test order published to auto_orders queue')
connection.close()
PYEOF
    python /tmp/publish.py
"
ENDSSH

echo ""
echo "2. Waiting 10 seconds for worker to process..."
sleep 10

echo ""
echo "3. Checking worker logs for processing confirmation..."
sshpass -p "$SSH_PASS" ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null $SSH_HOST \
  "docker service logs infrastructureservices-agentworkersorder-yeyxjf --tail 50" | grep -E "(Received task|Task completed|test-order-001)" || echo "⚠️ No processing logs found"

echo ""
echo "4. Checking RabbitMQ queue status..."
sshpass -p "$SSH_PASS" ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null $SSH_HOST << 'ENDSSH'
docker exec infrastructureservices-rabbitmq-gktndk-rabbitmq-1 \
  rabbitmqctl list_queues name messages consumers | grep auto_orders
ENDSSH

echo ""
echo "=========================================="
echo "Test Summary"
echo "=========================================="
echo ""
echo "✅ Test order published successfully"
echo "⏰ Worker had 10 seconds to process"
echo ""
echo "Next Steps:"
echo "1. Check worker logs above for 'Task completed' message"
echo "2. If successful, Phase 2 is FULLY COMPLETE"
echo "3. If no processing seen, investigate worker connectivity"
echo ""
echo "To view live worker logs:"
echo "  ssh root@72.60.219.244"
echo "  docker service logs -f infrastructureservices-agentworkersorder-yeyxjf"
