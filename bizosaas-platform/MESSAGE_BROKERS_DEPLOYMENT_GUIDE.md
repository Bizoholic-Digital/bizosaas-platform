# 🚀 MESSAGE BROKERS - COMPLETE DEPLOYMENT GUIDE

**Using Official Docker Hub Images for RabbitMQ & Apache Kafka**

This guide shows you how to deploy RabbitMQ and Apache Kafka to your BizOSaaS platform using official Docker images through Dokploy UI.

---

## 📦 OFFICIAL DOCKER IMAGES USED

### ✅ RabbitMQ
- **Image**: `rabbitmq:4.1-management` (Official Docker Library)
- **Source**: https://hub.docker.com/_/rabbitmq
- **Maintained By**: Docker Official Images + RabbitMQ Team
- **Latest Stable**: 4.1.4 (January 2025)

### ✅ Apache Kafka
- **Image**: `apache/kafka:4.0.1` (Apache Software Foundation)
- **Source**: https://hub.docker.com/r/apache/kafka
- **Maintained By**: Apache Kafka Community
- **Mode**: KRaft (no Zookeeper required - modern architecture)
- **Latest Stable**: 4.0.1 (December 2024)

### ✅ Kafka UI
- **Image**: `provectuslabs/kafka-ui:latest`
- **Source**: https://hub.docker.com/r/provectuslabs/kafka-ui
- **Purpose**: Web-based Kafka management interface

---

## 🎯 WHY USE DOCKER HUB IMAGES INSTEAD OF RAW COMPOSE?

### Benefits of Docker Hub Integration in Dokploy:

1. **Automatic Updates**: Dokploy can check for new image versions
2. **Better Visibility**: Services show up in Dokploy UI with proper management
3. **Health Monitoring**: Built-in health checks and status tracking
4. **Restart Policies**: Automated restart and recovery
5. **Resource Tracking**: CPU/memory monitoring in Dokploy dashboard
6. **Log Management**: Centralized log viewing in Dokploy UI
7. **Rollback Support**: Easy rollback to previous versions

### Why Not Raw Compose?

Raw compose files deployed via CLI:
- ❌ Don't show up in Dokploy UI
- ❌ Can't be managed from Dokploy dashboard
- ❌ No automatic health monitoring
- ❌ No restart/rollback controls in UI
- ❌ Manual log viewing only

---

## 📋 PRE-DEPLOYMENT CHECKLIST

### Step 1: Remove Existing Manual Services

If you previously deployed RabbitMQ manually (via `docker service create`), remove it first:

```bash
ssh root@72.60.219.244
docker service rm rabbitmq
docker volume ls | grep rabbitmq  # Check if volumes exist
exit
```

### Step 2: Verify Dokploy Access

- **URL**: https://dk4.bizoholic.com
- **Email**: bizoholic.digital@gmail.com
- **Password**: 25IKC#1XiKABRo

### Step 3: Check infrastructure-services Project

1. Login to Dokploy UI
2. Navigate to **Projects**
3. Find **infrastructure-services** project
4. Project ID should be: `qXd3_A4MnUDcmgPhCj731`

---

## 🚀 DEPLOYMENT METHOD 1: Via Git Repository (Recommended)

This method provides automatic deployments, version control, and best practices.

### Step 1: Prepare Git Repository

```bash
cd /home/alagiri/projects/bizoholic/bizosaas-platform

# Verify the compose file exists
ls -la infrastructure/message-brokers/docker-compose.yml

# Commit to Git
git add infrastructure/message-brokers/
git commit -m "Add official RabbitMQ and Kafka message brokers with Dokploy integration"
git push origin main
```

### Step 2: Deploy via Dokploy UI

1. **Login to Dokploy**: https://dk4.bizoholic.com

2. **Navigate to Infrastructure Services Project**:
   - Click **"Projects"** in sidebar
   - Select **"infrastructure-services"**

3. **Create New Compose Service**:
   - Click **"+ New Service"** button
   - Select **"Compose"** service type

4. **Configure Git Source**:
   - **Service Name**: `message-brokers`
   - **Description**: `RabbitMQ and Apache Kafka message brokers for AI agents`
   - **Source Type**: Select **"GitHub"**
   - **Repository**: Select your `bizosaas-platform` repository
   - **Branch**: `main`
   - **Compose Path**: `infrastructure/message-brokers/docker-compose.yml`
   - **Auto Deploy**: ✅ Enable (redeploy on git push)

5. **Deploy the Stack**:
   - Click **"Create Service"**
   - Click **"Deploy"** button
   - Wait 3-5 minutes for all containers to start

6. **Monitor Deployment**:
   - Watch logs in real-time
   - Check health status indicators
   - Verify all 3 services show "Running" (green)

---

## 🚀 DEPLOYMENT METHOD 2: Upload Compose File (Quick)

If you don't want Git integration, upload the compose file directly.

### Step 1: Upload Compose File to Server

```bash
scp infrastructure/message-brokers/docker-compose.yml root@72.60.219.244:/root/message-brokers-compose.yml
```

### Step 2: Deploy via Dokploy UI

1. Login to Dokploy UI: https://dk4.bizoholic.com

2. Go to **infrastructure-services** project

3. Click **"+ New Service"** → **"Compose"**

4. **Configure**:
   - **Service Name**: `message-brokers`
   - **Description**: `RabbitMQ and Kafka message brokers`
   - **Source Type**: Select **"Raw"**
   - Paste the contents from `/root/message-brokers-compose.yml`

5. Click **"Create Service"** → **"Deploy"**

---

## 🚀 DEPLOYMENT METHOD 3: Docker Hub Registry (Alternative)

Deploy individual services using Docker Hub images directly.

### For RabbitMQ:

1. Go to **infrastructure-services** project
2. Click **"+ New Service"** → **"Application"**
3. Configure:
   - **Name**: `rabbitmq`
   - **Source Type**: **"Docker Registry"**
   - **Docker Image**: `rabbitmq:4.1-management`
   - **Registry**: Docker Hub (public)
   - **Restart Policy**: Unless Stopped
4. Add environment variables (from compose file)
5. Configure ports: `5672`, `15672`, `15692`
6. Add Traefik labels for domain routing
7. Deploy

### For Apache Kafka:

1. Click **"+ New Service"** → **"Application"**
2. Configure:
   - **Name**: `kafka`
   - **Source Type**: **"Docker Registry"**
   - **Docker Image**: `apache/kafka:4.0.1`
   - **Registry**: Docker Hub (public)
3. Add environment variables (from compose file)
4. Configure ports: `9092`, `9093`, `9094`
5. Deploy

### For Kafka UI:

1. Click **"+ New Service"** → **"Application"**
2. Configure:
   - **Name**: `kafka-ui`
   - **Source Type**: **"Docker Registry"**
   - **Docker Image**: `provectuslabs/kafka-ui:latest`
3. Add environment variables
4. Configure port: `8080`
5. Add Traefik labels
6. Deploy

---

## 🌐 ACCESS URLS AFTER DEPLOYMENT

### RabbitMQ Management UI
- **URL**: https://stg.bizoholic.com/rabbitmq/
- **Username**: `admin`
- **Password**: `BizOSaaS2025@RabbitMQ`
- **Features**:
  - Dashboard overview
  - Queue management
  - Exchange configuration
  - Connection monitoring
  - User management

### Kafka UI (Management Interface)
- **URL**: https://stg.bizoholic.com/kafka-ui/
- **Auth**: Disabled (internal network only)
- **Features**:
  - Cluster overview
  - Topic management
  - Consumer group monitoring
  - Message browser
  - Schema registry

### Internal Connections (for applications)

**RabbitMQ AMQP Connection:**
```
amqp://admin:BizOSaaS2025@RabbitMQ@rabbitmq:5672/
```

**Kafka Bootstrap Servers:**
```
kafka:9092  (internal)
stg.bizoholic.com:9093  (external)
```

---

## ✅ POST-DEPLOYMENT VERIFICATION

### 1. Check Dokploy UI

In **infrastructure-services** project, verify all 3 services:

- [x] **rabbitmq**: Status = Running (green) | Replicas = 1/1
- [x] **kafka**: Status = Running (green) | Replicas = 1/1
- [x] **kafka-ui**: Status = Running (green) | Replicas = 1/1

### 2. Test Management UIs

**RabbitMQ:**
```bash
curl -u admin:BizOSaaS2025@RabbitMQ https://stg.bizoholic.com/rabbitmq/api/overview
```
Expected: JSON response with cluster overview

**Kafka UI:**
```bash
curl https://stg.bizoholic.com/kafka-ui/actuator/health
```
Expected: `{"status":"UP"}`

### 3. Check Service Logs in Dokploy

**RabbitMQ logs should show:**
```
Management plugin: HTTP (non-TLS) listener started on port 15672
Server startup complete; 5 plugins started
```

**Kafka logs should show:**
```
[KafkaRaftServer] Kafka Server started
[KafkaRaftServer] Kafka version: 4.0.1
```

**Kafka UI logs should show:**
```
Started KafkaUiApplication
Successfully connected to Kafka cluster: bizosaas-production
```

### 4. Test Internal Connectivity

SSH to server and test internal connections:

```bash
ssh root@72.60.219.244

# Test RabbitMQ AMQP port
nc -zv rabbitmq 5672
# Expected: Connection to rabbitmq 5672 port [tcp/*] succeeded!

# Test Kafka broker
nc -zv kafka 9092
# Expected: Connection to kafka 9092 port [tcp/*] succeeded!

exit
```

---

## 📊 MANAGING SERVICES IN DOKPLOY UI

Once deployed, you can manage all message brokers from Dokploy:

### Available Actions:
- ✅ **Start/Stop/Restart**: Control service state
- ✅ **View Logs**: Real-time log streaming
- ✅ **Edit Configuration**: Update environment variables
- ✅ **Scale**: Adjust replicas (for Kafka clustering)
- ✅ **Monitor Resources**: CPU, memory, network usage
- ✅ **Backup Volumes**: Scheduled backups for data persistence
- ✅ **Rollback**: Revert to previous versions
- ✅ **Auto-Deploy**: Redeploy on git push (if using Git source)

---

## 🔧 CREATING KAFKA TOPICS FOR AI AGENTS

### Via Kafka UI (https://stg.bizoholic.com/kafka-ui/)

1. Click **"Topics"** tab
2. Click **"Add Topic"** button
3. Create the following topics:

**Order Processing:**
```
Topic: ai.orders.processing
Partitions: 3
Replication Factor: 1
Retention: 7 days
```

**Support Tickets:**
```
Topic: ai.support.tickets
Partitions: 3
Replication Factor: 1
Retention: 30 days
```

**Inventory Management:**
```
Topic: ai.inventory.management
Partitions: 3
Replication Factor: 1
Retention: 7 days
```

**Marketing Content:**
```
Topic: ai.marketing.content
Partitions: 3
Replication Factor: 1
Retention: 90 days
```

**Data Analysis:**
```
Topic: ai.data.analysis
Partitions: 6
Replication Factor: 1
Retention: 7 days
```

**Audit Logs (Event Sourcing):**
```
Topic: bizosaas.audit.logs
Partitions: 6
Replication Factor: 1
Retention: 365 days
Cleanup Policy: compact
```

### Via Command Line

SSH to server and create topics:

```bash
ssh root@72.60.219.244

# Access Kafka container
docker exec -it bizosaas-kafka bash

# Create topics
kafka-topics.sh --bootstrap-server localhost:9092 --create --topic ai.orders.processing --partitions 3 --replication-factor 1

kafka-topics.sh --bootstrap-server localhost:9092 --create --topic ai.support.tickets --partitions 3 --replication-factor 1

kafka-topics.sh --bootstrap-server localhost:9092 --create --topic ai.inventory.management --partitions 3 --replication-factor 1

kafka-topics.sh --bootstrap-server localhost:9092 --create --topic ai.marketing.content --partitions 3 --replication-factor 1

kafka-topics.sh --bootstrap-server localhost:9092 --create --topic ai.data.analysis --partitions 6 --replication-factor 1

kafka-topics.sh --bootstrap-server localhost:9092 --create --topic bizosaas.audit.logs --partitions 6 --replication-factor 1 --config cleanup.policy=compact

# List all topics
kafka-topics.sh --bootstrap-server localhost:9092 --list

exit
exit
```

---

## 🔧 CREATING RABBITMQ QUEUES FOR AI AGENTS

### Via RabbitMQ Management UI (https://stg.bizoholic.com/rabbitmq/)

1. Login with: `admin` / `BizOSaaS2025@RabbitMQ`
2. Go to **"Queues"** tab
3. Click **"Add a new queue"**
4. Create the following queues:

**AI Agent Queues:**
- `ai.orders.processing` - Durable, Max length: 10000
- `ai.support.tickets` - Durable, Max length: 5000
- `ai.inventory.management` - Durable, Max length: 5000
- `ai.marketing.content` - Durable, Max length: 1000
- `ai.data.analysis` - Durable, Max length: 10000

**HITL (Human-In-The-Loop) Queue:**
- `hitl.approval.required` - Durable, Max length: 1000, Priority: High

**Dead Letter Queue:**
- `dlq.failed.tasks` - Durable, TTL: 7 days

### Via Command Line

```bash
ssh root@72.60.219.244

# Access RabbitMQ container
docker exec -it bizosaas-rabbitmq bash

# Create queues
rabbitmqadmin -u admin -p BizOSaaS2025@RabbitMQ declare queue name=ai.orders.processing durable=true
rabbitmqadmin -u admin -p BizOSaaS2025@RabbitMQ declare queue name=ai.support.tickets durable=true
rabbitmqadmin -u admin -p BizOSaaS2025@RabbitMQ declare queue name=ai.inventory.management durable=true
rabbitmqadmin -u admin -p BizOSaaS2025@RabbitMQ declare queue name=ai.marketing.content durable=true
rabbitmqadmin -u admin -p BizOSaaS2025@RabbitMQ declare queue name=ai.data.analysis durable=true
rabbitmqadmin -u admin -p BizOSaaS2025@RabbitMQ declare queue name=hitl.approval.required durable=true
rabbitmqadmin -u admin -p BizOSaaS2025@RabbitMQ declare queue name=dlq.failed.tasks durable=true

# List all queues
rabbitmqadmin -u admin -p BizOSaaS2025@RabbitMQ list queues

exit
exit
```

---

## 🔗 INTEGRATING WITH BRAIN API GATEWAY

Update Brain API Gateway to connect to message brokers:

### File: `brain-gateway/config.py`

```python
# RabbitMQ Configuration
RABBITMQ_HOST = "rabbitmq"
RABBITMQ_PORT = 5672
RABBITMQ_USER = "admin"
RABBITMQ_PASS = "BizOSaaS2025@RabbitMQ"
RABBITMQ_VHOST = "/"
RABBITMQ_URL = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/{RABBITMQ_VHOST}"

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS = ["kafka:9092"]
KAFKA_PRODUCER_CONFIG = {
    "bootstrap_servers": KAFKA_BOOTSTRAP_SERVERS,
    "acks": "all",
    "retries": 3,
    "linger_ms": 10,
}
KAFKA_CONSUMER_CONFIG = {
    "bootstrap_servers": KAFKA_BOOTSTRAP_SERVERS,
    "group_id": "brain-gateway",
    "auto_offset_reset": "earliest",
}
```

### File: `brain-gateway/message_broker.py`

```python
from aiormq import connect as rabbitmq_connect
from kafka import KafkaProducer, KafkaConsumer
import json

class MessageBroker:
    """Unified message broker interface for RabbitMQ and Kafka"""

    def __init__(self):
        self.rabbitmq_connection = None
        self.kafka_producer = None

    async def connect_rabbitmq(self):
        """Connect to RabbitMQ"""
        self.rabbitmq_connection = await rabbitmq_connect(RABBITMQ_URL)

    def connect_kafka(self):
        """Connect to Kafka"""
        self.kafka_producer = KafkaProducer(
            **KAFKA_PRODUCER_CONFIG,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    async def publish_task(self, queue_name: str, task_data: dict):
        """Publish task to RabbitMQ queue"""
        channel = await self.rabbitmq_connection.channel()
        await channel.basic_publish(
            body=json.dumps(task_data).encode(),
            routing_key=queue_name
        )

    def publish_event(self, topic: str, event_data: dict):
        """Publish event to Kafka topic"""
        self.kafka_producer.send(topic, value=event_data)
        self.kafka_producer.flush()
```

---

## 📈 MONITORING & ALERTING

### Dokploy Built-in Monitoring

1. Go to **infrastructure-services** project
2. Click on **rabbitmq**, **kafka**, or **kafka-ui**
3. View **Monitoring** tab:
   - CPU usage
   - Memory usage
   - Network I/O
   - Disk I/O

### RabbitMQ Metrics (Prometheus)

RabbitMQ exposes Prometheus metrics on port 15692:

```
http://rabbitmq:15692/metrics
```

### Kafka Metrics

Kafka exposes JMX metrics. Access via Kafka UI:
- Go to https://stg.bizoholic.com/kafka-ui/
- View **Brokers** tab → **Metrics**

### Alerting Thresholds

Set up alerts for:
- RabbitMQ queue depth > 5000 messages
- Kafka consumer lag > 1000 messages
- Memory usage > 80%
- Disk usage > 85%

---

## 🔒 SECURITY BEST PRACTICES

### 1. Change Default Passwords

Update RabbitMQ password after deployment:

```bash
docker exec -it bizosaas-rabbitmq rabbitmqctl change_password admin "NEW_SECURE_PASSWORD_HERE"
```

### 2. Enable Authentication for Kafka UI

Edit compose file and enable authentication:

```yaml
kafka-ui:
  environment:
    AUTH_TYPE: "LOGIN_FORM"
    SPRING_SECURITY_USER_NAME: admin
    SPRING_SECURITY_USER_PASSWORD: "SECURE_PASSWORD_HERE"
```

### 3. Use TLS/SSL for Kafka

For production, enable SSL:

```yaml
kafka:
  environment:
    KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: SSL:SSL,CONTROLLER:PLAINTEXT
    KAFKA_SSL_KEYSTORE_LOCATION: /etc/kafka/secrets/keystore.jks
    KAFKA_SSL_TRUSTSTORE_LOCATION: /etc/kafka/secrets/truststore.jks
```

### 4. Network Isolation

Ensure message brokers are only accessible via:
- Internal `dokploy-network` for services
- Traefik reverse proxy for web UIs
- No direct external access to AMQP/Kafka ports

---

## 🚨 TROUBLESHOOTING

### RabbitMQ Not Starting

**Check logs:**
```bash
docker logs bizosaas-rabbitmq
```

**Common issues:**
- Volume permission errors: `chown -R 999:999 /var/lib/docker/volumes/rabbitmq-data`
- Memory limits too low: Increase to at least 512MB
- Port conflicts: Ensure 5672, 15672 are not in use

### Kafka Not Starting

**Check logs:**
```bash
docker logs bizosaas-kafka
```

**Common issues:**
- KRaft format not initialized: Delete volume and recreate
- Cluster ID mismatch: Generate new UUID with `kafka-storage random-uuid`
- Insufficient memory: Increase heap size to at least 2GB

### Services Not Showing in Dokploy UI

**Cause:** Service deployed manually via `docker service create` instead of Dokploy

**Solution:**
1. Remove manual service: `docker service rm rabbitmq`
2. Deploy via Dokploy UI using methods above

### Cannot Access Management UIs

**Check Traefik routing:**
```bash
docker logs dokploy-traefik | grep -i rabbitmq
docker logs dokploy-traefik | grep -i kafka
```

**Verify SSL certificates:**
```bash
docker exec dokploy-traefik ls /letsencrypt/acme.json
```

---

## 🎉 SUCCESS CHECKLIST

Once deployment is complete, verify:

- [x] RabbitMQ service running in Dokploy UI (green status)
- [x] Kafka service running in Dokploy UI (green status)
- [x] Kafka UI service running in Dokploy UI (green status)
- [x] RabbitMQ Management UI accessible: https://stg.bizoholic.com/rabbitmq/
- [x] Kafka UI accessible: https://stg.bizoholic.com/kafka-ui/
- [x] Can login to RabbitMQ with admin credentials
- [x] Kafka cluster shows healthy in Kafka UI
- [x] All services have health checks passing
- [x] Volumes created for data persistence
- [x] Traefik routing configured with SSL
- [x] Services are manageable from Dokploy UI

---

## 📚 ADDITIONAL RESOURCES

### Official Documentation:
- **RabbitMQ**: https://www.rabbitmq.com/documentation.html
- **Apache Kafka**: https://kafka.apache.org/documentation/
- **Kafka UI**: https://docs.kafka-ui.provectus.io/

### Related Files:
- [docker-compose.yml](infrastructure/message-brokers/docker-compose.yml:1) - Complete stack configuration
- [AI_AGENT_AUTONOMOUS_PLATFORM.md](AI_AGENT_AUTONOMOUS_PLATFORM.md:1) - AI agent architecture
- [MESSAGE_BROKER_RECOMMENDATIONS.md](MESSAGE_BROKER_RECOMMENDATIONS.md:1) - Broker strategy

---

**Last Updated**: 2025-10-27 07:00 UTC
**Official Images**: ✅ RabbitMQ 4.1, Apache Kafka 4.0.1
**Deployment Method**: Dokploy UI with Docker Hub images
**Estimated Deployment Time**: 10-15 minutes
**Ready for Production**: ✅ Yes (after security hardening)
