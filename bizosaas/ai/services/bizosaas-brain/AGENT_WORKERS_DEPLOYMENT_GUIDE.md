# BizOSaaS Agent Workers - Full Deployment Guide

**Deployment Type:** Option B - Full Worker Implementation
**Target:** KVM4 Server (72.60.219.244)
**Duration:** 4-6 hours
**Status:** In Progress

---

## Infrastructure Connection Details

### RabbitMQ Service
- **Service Name:** `infrastructureservices-rabbitmq-gktndk`
- **Internal Hostname:** `infrastructureservices-rabbitmq-gktndk` (Docker network)
- **Port:** 5672 (AMQP)
- **Management UI Port:** 15672
- **VHost:** `/` (default)
- **Credentials:** Set via environment variables in infrastructure project

### Kafka Service
- **Service Name:** `infrastructureservices-kafka-ill4q0`
- **Internal Hostname:** `infrastructureservices-kafka-ill4q0`
- **Port:** 9092
- **Zookeeper:** Required dependency (should be deployed)

### Redis Service
- **Service Name:** `infrastructureservices-bizosaasredis-w0gw3g`
- **Port:** 6379
- **Database:** 1 (for HITL queue)

---

## Implementation Steps

### Step 1: Update Setup Scripts with Correct Hostnames ✅
File: `setup_queues.py` (already created)

**Required Changes:**
```python
# Update these defaults:
RABBITMQ_HOST = 'infrastructureservices-rabbitmq-gktndk'  # Docker service name
RABBITMQ_PORT = 5672
RABBITMQ_VHOST = '/'
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'admin')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', 'BizOSaaS2025@RabbitMQ!Secure')
```

### Step 2: Create Kafka Topics Setup Script ⏳
File: `setup_kafka_topics.py`

**Kafka Connection:**
```python
KAFKA_BOOTSTRAP_SERVERS = 'infrastructureservices-kafka-ill4q0:9092'
```

### Step 3: Create Worker Directory Structure ⏳
```bash
cd /home/alagiri/projects/bizosaas-platform/bizosaas/ai/services/bizosaas-brain
mkdir -p workers
```

**Directory Layout:**
```
workers/
├── __init__.py
├── base_worker.py          # Base CrewAI worker (100-150 lines)
├── order_agent.py          # Order processing (60-80 lines)
├── support_agent.py        # Support tickets (60-80 lines)
├── marketing_agent.py      # Marketing campaigns (60-80 lines)
└── requirements.txt        # Dependencies
```

### Step 4: Implement Base Worker Class ⏳
**Key Features:**
- RabbitMQ connection with retry logic
- CrewAI agent integration
- Kafka event publishing
- Error handling with DLQ
- Metrics collection
- Graceful shutdown

### Step 5: Implement Specific Workers ⏳
Each worker will:
- Extend `base_worker.CrewAIWorker`
- Define CrewAI Agent with role, goal, backstory
- Implement task processing logic
- Handle results (success/failure)
- Publish completion events to Kafka

### Step 6: Create Dockerfile.workers ⏳
**Base Image:** `python:3.11-slim`

**Dependencies:**
- crewai
- pika (RabbitMQ)
- kafka-python
- redis
- httpx
- openai / anthropic (LLM providers)

### Step 7: Build Worker Image ⏳
```bash
docker build -t ghcr.io/bizoholic-digital/bizosaas-agent-workers:latest \
  -f Dockerfile.workers .
```

### Step 8: Push to GHCR ⏳
```bash
docker push ghcr.io/bizoholic-digital/bizosaas-agent-workers:latest
```

### Step 9: Deploy Workers to Docker Swarm ⏳
Deploy as Docker services with different entry points:

```bash
# Order Processing Agents (4 replicas)
docker service create \
  --name agent-orders \
  --network dokploy-network \
  --replicas 4 \
  --env QUEUE_NAME=auto_orders \
  --env RABBITMQ_HOST=infrastructureservices-rabbitmq-gktndk \
  --env KAFKA_BOOTSTRAP_SERVERS=infrastructureservices-kafka-ill4q0:9092 \
  --env OPENAI_API_KEY=$OPENAI_API_KEY \
  ghcr.io/bizoholic-digital/bizosaas-agent-workers:latest \
  python workers/order_agent.py

# Support Ticket Agents (6 replicas)
docker service create \
  --name agent-support \
  --network dokploy-network \
  --replicas 6 \
  --env QUEUE_NAME=auto_support_tickets \
  --env RABBITMQ_HOST=infrastructureservices-rabbitmq-gktndk \
  --env KAFKA_BOOTSTRAP_SERVERS=infrastructureservices-kafka-ill4q0:9092 \
  --env OPENAI_API_KEY=$OPENAI_API_KEY \
  ghcr.io/bizoholic-digital/bizosaas-agent-workers:latest \
  python workers/support_agent.py

# Marketing Agents (4 replicas)
docker service create \
  --name agent-marketing \
  --network dokploy-network \
  --replicas 4 \
  --env QUEUE_NAME=auto_marketing \
  --env RABBITMQ_HOST=infrastructureservices-rabbitmq-gktndk \
  --env KAFKA_BOOTSTRAP_SERVERS=infrastructureservices-kafka-ill4q0:9092 \
  --env OPENAI_API_KEY=$OPENAI_API_KEY \
  ghcr.io/bizoholic-digital/bizosaas-agent-workers:latest \
  python workers/marketing_agent.py
```

### Step 10: Run Setup Scripts ⏳
From within the Docker network (via brain-gateway container or dedicated setup job):

```bash
# Create RabbitMQ queues
python setup_queues.py

# Create Kafka topics
python setup_kafka_topics.py
```

---

## Validation & Testing

### Test 1: Queue Creation
```bash
# Check queues via RabbitMQ Management API
curl -u admin:PASSWORD \
  http://infrastructureservices-rabbitmq-gktndk:15672/api/queues
```

Expected: 11 main queues + 11 DLQs = 22 total queues

### Test 2: Kafka Topics
```bash
# List Kafka topics
kafka-topics.sh --list \
  --bootstrap-server infrastructureservices-kafka-ill4q0:9092
```

Expected: 13 topics created

### Test 3: Worker Connectivity
Check worker logs:
```bash
docker service logs agent-orders -f
```

Expected: "✅ Connected to RabbitMQ" and "🎧 Agent worker started"

### Test 4: End-to-End Workflow
1. Publish test message to `auto_orders` queue
2. Worker picks up task
3. CrewAI processes task
4. Result published to Kafka
5. Check Kafka `ai.completions` topic for event

---

## Success Criteria

- ✅ 11 RabbitMQ queues operational
- ✅ 13 Kafka topics created
- ✅ 14 agent workers deployed and running
- ✅ Workers consuming from queues
- ✅ Events flowing to Kafka
- ✅ No error messages in logs
- ✅ Test task processed successfully

---

## Rollback Plan

If deployment fails:

```bash
# Remove all agent services
docker service rm agent-orders agent-support agent-marketing

# Remove queues (if needed)
# Queues auto-delete when empty with no consumers

# Remove Kafka topics (if needed)
kafka-topics.sh --delete --topic domain.orders \
  --bootstrap-server infrastructureservices-kafka-ill4q0:9092
```

---

## Next Steps After Deployment

1. **Integrate with Brain-Gateway**: Update brain-gateway to publish tasks to queues
2. **Add Monitoring**: Set up Prometheus metrics for worker performance
3. **Add More Agents**: Deploy remaining 80+ agents as needed
4. **Configure HITL**: Connect HITL queues to approval workflow
5. **Load Testing**: Test with production-like task volumes

---

## Files Created

- ✅ `setup_queues.py` - RabbitMQ queue creation
- ⏳ `setup_kafka_topics.py` - Kafka topic creation
- ⏳ `workers/base_worker.py` - Base worker class
- ⏳ `workers/order_agent.py` - Order processing
- ⏳ `workers/support_agent.py` - Support tickets
- ⏳ `workers/marketing_agent.py` - Marketing campaigns
- ⏳ `workers/requirements.txt` - Dependencies
- ⏳ `Dockerfile.workers` - Worker container image

---

**Status:** Ready to proceed with full implementation
**Estimated Completion:** 4-6 hours
**Current Task:** Creating Kafka setup script and worker infrastructure
