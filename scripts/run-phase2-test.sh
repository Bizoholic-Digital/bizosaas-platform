#!/bin/bash

# Phase 2 End-to-End Test - Simplified Version
# Tests: RabbitMQ → Worker → Kafka flow

set -e

echo "=========================================="
echo "Phase 2 Worker Integration Test"
echo "=========================================="

SSH_PASS='&k3civYG5Q6YPb'
SSH_HOST='root@72.60.219.244'

echo ""
echo "1. Copying test script to server..."
sshpass -p "$SSH_PASS" scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
  publish_test_order.py $SSH_HOST:/tmp/

echo ""
echo "2. Publishing test order to auto_orders queue..."
sshpass -p "$SSH_PASS" ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null $SSH_HOST \
  "docker run --rm --network dokploy-network -v /tmp/publish_test_order.py:/app/publish.py python:3.11-slim bash -c 'pip install -q pika && python /app/publish.py'"

echo ""
echo "3. Waiting 10 seconds for worker to process..."
sleep 10

echo ""
echo "4. Checking worker logs for processing confirmation..."
sshpass -p "$SSH_PASS" ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null $SSH_HOST \
  "docker service logs infrastructureservices-agentworkersorder-yeyxjf --tail 50" | grep -E "(Received task|Task completed|test-order-001|Processing task)" || echo "⚠️ No processing logs found yet"

echo ""
echo "5. Checking RabbitMQ queue status..."
sshpass -p "$SSH_PASS" ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null $SSH_HOST \
  "docker exec infrastructureservices-rabbitmq-gktndk-rabbitmq-1 rabbitmqctl list_queues name messages consumers | grep auto_orders"

echo ""
echo "=========================================="
echo "Test Summary"
echo "=========================================="
echo ""
echo "✅ Test order published successfully"
echo "⏰ Worker had 10 seconds to process"
echo ""
echo "Next Steps:"
echo "1. Check worker logs above for 'Task completed' or 'Processing task' message"
echo "2. If successful, Phase 2 is FULLY COMPLETE"
echo "3. If no processing seen, check live logs with:"
echo "   ssh root@72.60.219.244"
echo "   docker service logs -f infrastructureservices-agentworkersorder-yeyxjf"
echo ""
