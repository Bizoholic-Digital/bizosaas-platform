# Worker Services Deployment Guide - Dokploy

## Overview

Deploy the three CrewAI agent worker services via Dokploy dashboard to ensure proper DNS resolution with the existing infrastructure services.

**Important**: The infrastructure services (RabbitMQ, Kafka) are already deployed and running. We just need to deploy the worker services in the same Dokploy environment.

---

## Pre-requisites

✅ RabbitMQ running: `infrastructureservices-rabbitmq-gktndk-rabbitmq-1`
✅ Kafka running: `infrastructureservices-kafka-ill4q0-kafka-1`
✅ Docker image built and pushed: `ghcr.io/bizoholic-digital/bizosaas-agent-workers:latest`

---

## Deployment Location

- **Dokploy URL**: https://dk4.bizoholic.com
- **Project**: backend-services (Project ID: `c3-8-FgSCrNjun1eLfYOl`)
- **Environment**: staging (Environment ID: `4HC0mRr44YeYe5mq_oiho`)

---

## Service 1: Order Processing Workers

### Basic Configuration
1. Go to backend-services → staging environment
2. Click "Create Application"
3. Select "Docker Image"

### Application Settings
- **Name**: `agent-workers-order`
- **Description**: `Order Processing Workers - 4 replicas`
- **Docker Image**: `ghcr.io/bizoholic-digital/bizosaas-agent-workers:latest`

### Registry Credentials
- **Username**: `alagiri.rajesh@gmail.com`
- **Password**: `GITHUB_TOKEN_REDACTED`

### Command Override
```bash
python workers/order_agent.py
```

### Environment Variables
```bash
QUEUE_NAME=auto_orders
RABBITMQ_HOST=infrastructureservices-rabbitmq-gktndk-rabbitmq-1
RABBITMQ_PORT=5672
RABBITMQ_VHOST=/
RABBITMQ_USER=admin
RABBITMQ_PASS=BizOSaaS2025@RabbitMQ!Secure
KAFKA_BOOTSTRAP_SERVERS=infrastructureservices-kafka-ill4q0-kafka-1:9092
REDIS_HOST=infrastructure-shared-redis
REDIS_PORT=6379
OPENAI_API_KEY=OPENAI_KEY_REDACTED
OPENROUTER_API_KEY=OPENROUTER_KEY_REDACTED
ANTHROPIC_API_KEY=ANTHROPIC_KEY_REDACTED
PYTHONPATH=/app
PYTHONUNBUFFERED=1
```

### Resources
- **Replicas**: 4
- **CPU Limit**: 1.0
- **Memory Limit**: 1024 MB

---

## Service 2: Support Ticket Workers

### Basic Configuration
1. Go to backend-services → staging environment
2. Click "Create Application"
3. Select "Docker Image"

### Application Settings
- **Name**: `agent-workers-support`
- **Description**: `Support Ticket Workers - 6 replicas`
- **Docker Image**: `ghcr.io/bizoholic-digital/bizosaas-agent-workers:latest`

### Registry Credentials
- **Username**: `alagiri.rajesh@gmail.com`
- **Password**: `GITHUB_TOKEN_REDACTED`

### Command Override
```bash
python workers/support_agent.py
```

### Environment Variables
```bash
QUEUE_NAME=auto_support_tickets
RABBITMQ_HOST=infrastructureservices-rabbitmq-gktndk-rabbitmq-1
RABBITMQ_PORT=5672
RABBITMQ_VHOST=/
RABBITMQ_USER=admin
RABBITMQ_PASS=BizOSaaS2025@RabbitMQ!Secure
KAFKA_BOOTSTRAP_SERVERS=infrastructureservices-kafka-ill4q0-kafka-1:9092
REDIS_HOST=infrastructure-shared-redis
REDIS_PORT=6379
OPENAI_API_KEY=OPENAI_KEY_REDACTED
OPENROUTER_API_KEY=OPENROUTER_KEY_REDACTED
ANTHROPIC_API_KEY=ANTHROPIC_KEY_REDACTED
PYTHONPATH=/app
PYTHONUNBUFFERED=1
```

### Resources
- **Replicas**: 6
- **CPU Limit**: 1.0
- **Memory Limit**: 1024 MB

---

## Service 3: Marketing Campaign Workers

### Basic Configuration
1. Go to backend-services → staging environment
2. Click "Create Application"
3. Select "Docker Image"

### Application Settings
- **Name**: `agent-workers-marketing`
- **Description**: `Marketing Campaign Workers - 4 replicas`
- **Docker Image**: `ghcr.io/bizoholic-digital/bizosaas-agent-workers:latest`

### Registry Credentials
- **Username**: `alagiri.rajesh@gmail.com`
- **Password**: `GITHUB_TOKEN_REDACTED`

### Command Override
```bash
python workers/marketing_agent.py
```

### Environment Variables
```bash
QUEUE_NAME=auto_marketing
RABBITMQ_HOST=infrastructureservices-rabbitmq-gktndk-rabbitmq-1
RABBITMQ_PORT=5672
RABBITMQ_VHOST=/
RABBITMQ_USER=admin
RABBITMQ_PASS=BizOSaaS2025@RabbitMQ!Secure
KAFKA_BOOTSTRAP_SERVERS=infrastructureservices-kafka-ill4q0-kafka-1:9092
REDIS_HOST=infrastructure-shared-redis
REDIS_PORT=6379
OPENAI_API_KEY=OPENAI_KEY_REDACTED
OPENROUTER_API_KEY=OPENROUTER_KEY_REDACTED
ANTHROPIC_API_KEY=ANTHROPIC_KEY_REDACTED
PYTHONPATH=/app
PYTHONUNBUFFERED=1
```

### Resources
- **Replicas**: 4
- **CPU Limit**: 1.0
- **Memory Limit**: 1024 MB

---

## Important Notes

### Hostname Changes
The key difference from the previous guide is using the **actual Docker container names** for infrastructure services:

- ✅ **RabbitMQ**: `infrastructureservices-rabbitmq-gktndk-rabbitmq-1` (not `infrastructureservices-rabbitmq-gktndk`)
- ✅ **Kafka**: `infrastructureservices-kafka-ill4q0-kafka-1:9092` (not `infrastructureservices-kafka-ill4q0:9092`)
- ✅ **Redis**: `infrastructure-shared-redis` (existing shared Redis service)

### Network
All services will be deployed on the `dokploy-network` automatically when created via Dokploy.

---

## Verification

After deploying all three services:

1. **Check Service Status**:
   ```bash
   ssh root@72.60.219.244
   docker ps | grep agent-workers
   ```

2. **Check Worker Logs**:
   ```bash
   docker logs -f <container-name>
   ```

3. **Verify RabbitMQ Connection**:
   - Workers should show "Connected to RabbitMQ" in logs
   - No "Name or service not known" errors

---

## Next Steps

Once all workers are running successfully:

1. Run `setup_queues.py` to create RabbitMQ queues
2. Run `setup_kafka_topics.py` to create Kafka topics
3. Test end-to-end workflow by publishing a test task
