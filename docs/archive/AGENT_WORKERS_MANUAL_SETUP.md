# Agent Workers Manual Setup Guide

You've already created the **Order Workers** service. Here are the configurations for the remaining two services.

---

## Service 2: Support Workers

### Basic Info
- **Project:** backend-services
- **Environment:** staging
- **Service Name:** `agent-workers-support`
- **Description:** Customer Support Ticket Processing Workers - 6 replicas

### Docker Configuration
- **Application Type:** Docker Image
- **Image:** `ghcr.io/bizoholic-digital/bizosaas-agent-workers:latest`
- **Registry Username:** `alagiri.rajesh@gmail.com`
- **Registry Password:** `GITHUB_TOKEN_REDACTED`

### Command Override
```
python workers/support_agent.py
```

### Deployment Settings
- **Replicas:** 6
- **CPU Reservation:** 0.5
- **CPU Limit:** 1.0
- **Memory Reservation:** 512 MB
- **Memory Limit:** 1024 MB

### Environment Variables
```bash
QUEUE_NAME=auto_support_tickets
RABBITMQ_HOST=infrastructureservices-rabbitmq-gktndk
RABBITMQ_PORT=5672
RABBITMQ_VHOST=/
RABBITMQ_USER=admin
RABBITMQ_PASS=BizOSaaS2025@RabbitMQ!Secure
KAFKA_BOOTSTRAP_SERVERS=infrastructureservices-kafka-ill4q0:9092
REDIS_HOST=infrastructureservices-bizosaasredis-w0gw3g
REDIS_PORT=6379
REDIS_PASSWORD=BizOSaaS2025@redis
OPENAI_API_KEY=OPENAI_KEY_REDACTED
OPENROUTER_API_KEY=OPENROUTER_KEY_REDACTED
ANTHROPIC_API_KEY=ANTHROPIC_KEY_REDACTED
PYTHONPATH=/app
PYTHONUNBUFFERED=1
```

### Network
- **Network:** dokploy-network (auto-selected)
- **No port mappings needed**

### Health Check (Optional)
```bash
Test Command: pgrep -f "python.*workers" || exit 1
Interval: 30s
Timeout: 10s
Retries: 3
Start Period: 40s
```

---

## Service 3: Marketing Workers

### Basic Info
- **Project:** backend-services
- **Environment:** staging
- **Service Name:** `agent-workers-marketing`
- **Description:** Marketing Campaign Processing Workers - 4 replicas

### Docker Configuration
- **Application Type:** Docker Image
- **Image:** `ghcr.io/bizoholic-digital/bizosaas-agent-workers:latest`
- **Registry Username:** `alagiri.rajesh@gmail.com`
- **Registry Password:** `GITHUB_TOKEN_REDACTED`

### Command Override
```
python workers/marketing_agent.py
```

### Deployment Settings
- **Replicas:** 4
- **CPU Reservation:** 0.5
- **CPU Limit:** 1.0
- **Memory Reservation:** 512 MB
- **Memory Limit:** 1024 MB

### Environment Variables
```bash
QUEUE_NAME=auto_marketing
RABBITMQ_HOST=infrastructureservices-rabbitmq-gktndk
RABBITMQ_PORT=5672
RABBITMQ_VHOST=/
RABBITMQ_USER=admin
RABBITMQ_PASS=BizOSaaS2025@RabbitMQ!Secure
KAFKA_BOOTSTRAP_SERVERS=infrastructureservices-kafka-ill4q0:9092
REDIS_HOST=infrastructureservices-bizosaasredis-w0gw3g
REDIS_PORT=6379
REDIS_PASSWORD=BizOSaaS2025@redis
OPENAI_API_KEY=OPENAI_KEY_REDACTED
OPENROUTER_API_KEY=OPENROUTER_KEY_REDACTED
ANTHROPIC_API_KEY=ANTHROPIC_KEY_REDACTED
PYTHONPATH=/app
PYTHONUNBUFFERED=1
```

### Network
- **Network:** dokploy-network (auto-selected)
- **No port mappings needed**

### Health Check (Optional)
```bash
Test Command: pgrep -f "python.*workers" || exit 1
Interval: 30s
Timeout: 10s
Retries: 3
Start Period: 40s
```

---

## Summary

After creating all three services, you will have:

1. **agent-workers-order** (already created) - 4 replicas
   - Queue: `auto_orders`
   - Command: `python workers/order_agent.py`

2. **agent-workers-support** (create this next) - 6 replicas
   - Queue: `auto_support_tickets`
   - Command: `python workers/support_agent.py`

3. **agent-workers-marketing** (create last) - 4 replicas
   - Queue: `auto_marketing`
   - Command: `python workers/marketing_agent.py`

**Total:** 14 worker replicas processing tasks from RabbitMQ

---

## After Creating All Services

Once all three services are created and deployed, I'll help you:

1. ✅ Run the setup scripts to create RabbitMQ queues and Kafka topics
2. ✅ Verify workers are consuming from queues
3. ✅ Test the end-to-end workflow
4. ✅ Monitor worker performance

---

## Quick Copy-Paste Environment Variables

For easier setup, here are the environment variables in a format you can copy-paste directly into Dokploy:

### For Support Workers:
```
QUEUE_NAME=auto_support_tickets
RABBITMQ_HOST=infrastructureservices-rabbitmq-gktndk
RABBITMQ_PORT=5672
RABBITMQ_VHOST=/
RABBITMQ_USER=admin
RABBITMQ_PASS=BizOSaaS2025@RabbitMQ!Secure
KAFKA_BOOTSTRAP_SERVERS=infrastructureservices-kafka-ill4q0:9092
REDIS_HOST=infrastructureservices-bizosaasredis-w0gw3g
REDIS_PORT=6379
REDIS_PASSWORD=BizOSaaS2025@redis
OPENAI_API_KEY=OPENAI_KEY_REDACTED
OPENROUTER_API_KEY=OPENROUTER_KEY_REDACTED
ANTHROPIC_API_KEY=ANTHROPIC_KEY_REDACTED
PYTHONPATH=/app
PYTHONUNBUFFERED=1
```

### For Marketing Workers:
```
QUEUE_NAME=auto_marketing
RABBITMQ_HOST=infrastructureservices-rabbitmq-gktndk
RABBITMQ_PORT=5672
RABBITMQ_VHOST=/
RABBITMQ_USER=admin
RABBITMQ_PASS=BizOSaaS2025@RabbitMQ!Secure
KAFKA_BOOTSTRAP_SERVERS=infrastructureservices-kafka-ill4q0:9092
REDIS_HOST=infrastructureservices-bizosaasredis-w0gw3g
REDIS_PORT=6379
REDIS_PASSWORD=BizOSaaS2025@redis
OPENAI_API_KEY=OPENAI_KEY_REDACTED
OPENROUTER_API_KEY=OPENROUTER_KEY_REDACTED
ANTHROPIC_API_KEY=ANTHROPIC_KEY_REDACTED
PYTHONPATH=/app
PYTHONUNBUFFERED=1
```
