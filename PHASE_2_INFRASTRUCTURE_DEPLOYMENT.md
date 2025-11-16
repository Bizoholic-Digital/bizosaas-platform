# Phase 2: Infrastructure Services Deployment

## Overview

Before deploying the CrewAI agent workers, we need to deploy the required infrastructure services on KVM4 (dk4.bizoholic.com).

## Required Infrastructure Services

### 1. RabbitMQ Service
**Service Name**: `infrastructureservices-rabbitmq-gktndk`
**Purpose**: Message queue for task distribution

**Dokploy Configuration**:
- Project: infrastructure-services
- Environment: staging (or production)
- Application Type: Docker Image
- Image: `rabbitmq:3.13-management`
- Container Name: `infrastructureservices-rabbitmq-gktndk`

**Ports**:
- 5672 (AMQP)
- 15672 (Management UI)

**Environment Variables**:
```bash
RABBITMQ_DEFAULT_USER=admin
RABBITMQ_DEFAULT_PASS=BizOSaaS2025@RabbitMQ!Secure
RABBITMQ_DEFAULT_VHOST=/
```

**Resource Limits**:
- Memory: 1024 MB
- CPU: 1.0

**Volumes**:
- `/var/lib/rabbitmq` (for persistence)

---

### 2. Kafka Service
**Service Name**: `infrastructureservices-kafka-ill4q0`
**Purpose**: Event streaming platform

**Dokploy Configuration**:
- Project: infrastructure-services
- Environment: staging (or production)
- Application Type: Docker Image
- Image: `bitnami/kafka:3.6`
- Container Name: `infrastructureservices-kafka-ill4q0`

**Ports**:
- 9092 (Kafka broker)
- 9093 (Controller)

**Environment Variables**:
```bash
KAFKA_CFG_NODE_ID=1
KAFKA_CFG_PROCESS_ROLES=controller,broker
KAFKA_CFG_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093
KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT
KAFKA_CFG_CONTROLLER_QUORUM_VOTERS=1@infrastructureservices-kafka-ill4q0:9093
KAFKA_CFG_CONTROLLER_LISTENER_NAMES=CONTROLLER
KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://infrastructureservices-kafka-ill4q0:9092
KAFKA_CFG_AUTO_CREATE_TOPICS_ENABLE=true
ALLOW_PLAINTEXT_LISTENER=yes
```

**Resource Limits**:
- Memory: 2048 MB
- CPU: 2.0

**Volumes**:
- `/bitnami/kafka` (for persistence)

---

### 3. BizOSaaS Redis Service
**Service Name**: `infrastructureservices-bizosaasredis-w0gw3g`
**Purpose**: Caching and session storage

**Dokploy Configuration**:
- Project: infrastructure-services
- Environment: staging (or production)
- Application Type: Docker Image
- Image: `redis:7-alpine`
- Container Name: `infrastructureservices-bizosaasredis-w0gw3g`

**Ports**:
- 6379 (Redis)

**Command Override**:
```bash
redis-server --requirepass BizOSaaS2025@redis
```

**Environment Variables**:
```bash
REDIS_PASSWORD=BizOSaaS2025@redis
```

**Resource Limits**:
- Memory: 512 MB
- CPU: 0.5

**Volumes**:
- `/data` (for persistence)

---

## Deployment Order

1. **Deploy RabbitMQ first** - Workers depend on this for task queues
2. **Deploy Kafka second** - Workers publish events here
3. **Deploy BizOSaaS Redis third** - Workers use this for caching
4. **Verify all services are running** - Check health and connectivity
5. **Run setup scripts**:
   - Execute `setup_queues.py` to create RabbitMQ queues
   - Execute `setup_kafka_topics.py` to create Kafka topics
6. **Deploy worker services** - Use the manual guide in AGENT_WORKERS_MANUAL_SETUP.md

---

## Verification Steps

After deploying each service, verify it's accessible:

### RabbitMQ Verification
```bash
ssh root@72.60.219.244
docker exec -it $(docker ps | grep rabbitmq | awk '{print $1}') rabbitmqctl status
```

### Kafka Verification
```bash
docker exec -it $(docker ps | grep kafka | awk '{print $1}') kafka-topics.sh --list --bootstrap-server localhost:9092
```

### Redis Verification
```bash
docker exec -it $(docker ps | grep bizosaasredis | awk '{print $1}') redis-cli -a BizOSaaS2025@redis ping
```

---

## Network Configuration

All services must be on the `dokploy-network` to communicate with each other and with the worker services.

---

## Next Steps

Once all infrastructure services are deployed and verified:
1. Use [AGENT_WORKERS_MANUAL_SETUP.md](./AGENT_WORKERS_MANUAL_SETUP.md) to deploy the three worker services
2. Run the queue and topic setup scripts
3. Test end-to-end workflow
