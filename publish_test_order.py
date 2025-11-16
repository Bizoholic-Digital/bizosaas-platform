#!/usr/bin/env python3
"""
Publish test order to RabbitMQ auto_orders queue
"""
import pika
import json

# Test order data
test_order = {
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

# Convert to JSON string
message = json.dumps(test_order, indent=2)

# Connect to RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='infrastructureservices-rabbitmq-gktndk-rabbitmq-1',
        port=5672,
        virtual_host='/',
        credentials=pika.PlainCredentials('admin', 'lemn3f1e')
    )
)

channel = connection.channel()

# Publish to auto_orders queue
channel.basic_publish(
    exchange='',
    routing_key='auto_orders',
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=2,  # Persistent
        priority=10
    )
)

print('✅ Test order published to auto_orders queue')
print(f'📨 Message: {message[:100]}...')
connection.close()
