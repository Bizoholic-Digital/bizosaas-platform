# Phase 2: CrewAI Orchestration - Implementation Status

**Date:** November 15, 2025
**Status:** 57% Complete - Ready for Worker Deployment

---

## ✅ Completed Infrastructure

### 1. Message Queue Infrastructure
- **RabbitMQ Cluster**: `infrastructureservices-rabbitmq-gktndk`
  - Status: ✅ Deployed and running
  - Replicas: 2
  - Management UI: Available
  - Queues: Need to be created (see setup script below)

### 2. Event Streaming Infrastructure
- **Kafka Cluster**: `infrastructureservices-kafka-ill4q0`
  - Status: ✅ Deployed and running
  - Brokers: 2
  - Topics: Need to be created (see setup script below)

### 3. Brain Gateway Service
- **Service**: `backend-brain-gateway`
  - Dokploy Service ID: `3uYBtxpH1Qc7H8uTfmOfy`
  - Project: `c3-8-FgSCrNjun1eLfYOl`
  - Environment: `4HC0mRr44YeYe5mq_oiho`
  - Status: ✅ Deployed on KVM4
  - Location: `/home/alagiri/projects/bizosaas-platform/bizosaas/ai/services/bizosaas-brain`

### 4. Existing HITL Implementation
Brain-gateway already has extensive HITL functionality:

**Files:**
- `content_marketing_hitl_workflows.py` - Complete HITL workflow system
- `main.py` - Contains HITL API endpoints

**API Endpoints:**
```
POST /telegram/approval-request
GET  /telegram/approval-status/{request_id}
POST /telegram/approval-response
GET  /telegram/pending-approvals
POST /api/brain/seo/workflows/hitl/approve
POST /api/brain/content-marketing/workflows/hitl/approve
```

**Features Already Implemented:**
- Progressive automation levels (Level 1-5)
- Risk-based approval routing
- Telegram-based approval workflow
- Multi-stakeholder approval workflows
- Automated escalation
- Performance-based confidence scoring

---

## ⏳ Missing Components for Phase 2

### 1. RabbitMQ Queue Setup Script
**File to Create:** `/home/alagiri/projects/bizosaas-platform/bizosaas/ai/services/bizosaas-brain/setup_queues.py`

**Required Queues:**
```python
# AUTO-PROCESSING QUEUES
auto_orders              # High priority, 1h TTL
auto_support_tickets     # High priority, 2h TTL
auto_inventory           # Medium priority, 30min TTL
auto_marketing           # Medium priority, 4h TTL
auto_seo                 # Medium priority, 2h TTL
auto_social_media        # Medium priority, 1h TTL
auto_email_campaigns     # Medium priority, 2h TTL
auto_analytics           # Low priority, 4h TTL

# HITL QUEUES
hitl_approval            # Critical, 24h TTL
hitl_exceptions          # Critical, 12h TTL
hitl_training            # Training data, 7d TTL
```

### 2. Kafka Topics Setup Script
**File to Create:** `/home/alagiri/projects/bizosaas-platform/bizosaas/ai/services/bizosaas-brain/setup_kafka_topics.py`

**Required Topics:**
```python
# Domain Events
domain.orders            # 3 partitions, RF=2
domain.customers         # 3 partitions, RF=2
domain.products          # 3 partitions, RF=2
domain.leads             # 2 partitions, RF=2
domain.content           # 2 partitions, RF=2

# AI Agent Events
ai.decisions             # 3 partitions, RF=2
ai.completions           # 3 partitions, RF=2
ai.errors                # 2 partitions, RF=2

# HITL Events
hitl.requests            # 2 partitions, RF=2
hitl.decisions           # 2 partitions, RF=2
hitl.feedback            # 2 partitions, RF=2

# Audit & Analytics
audit.trail              # 5 partitions, RF=2
analytics.metrics        # 3 partitions, RF=2
```

### 3. Agent Worker Infrastructure
**Directory to Create:** `/home/alagiri/projects/bizosaas-platform/bizosaas/ai/services/bizosaas-brain/workers/`

**Files Needed:**
```
workers/
├── __init__.py
├── base_worker.py          # Base CrewAI worker class
├── order_agent.py          # E-commerce order processing
├── support_agent.py        # Support ticket automation
├── marketing_agent.py      # Marketing campaign automation
├── inventory_agent.py      # Inventory management
└── requirements.txt        # Worker dependencies
```

### 4. Dockerfile for Agent Workers
**File to Create:** `/home/alagiri/projects/bizosaas-platform/bizosaas/ai/services/bizosaas-brain/Dockerfile.workers`

Should include:
- Python 3.11 base image
- CrewAI dependencies
- RabbitMQ client (pika)
- Kafka client (kafka-python)
- Redis client
- Environment variable configuration

---

## 📋 Implementation Tasks (Remaining)

### Task 1: Create RabbitMQ Queue Setup Script (30 min)
```bash
cd /home/alagiri/projects/bizosaas-platform/bizosaas/ai/services/bizosaas-brain
# Create setup_queues.py based on implementation plan lines 1110-1183
# Run: python setup_queues.py
```

### Task 2: Create Kafka Topics Setup Script (30 min)
```bash
# Create setup_kafka_topics.py based on implementation plan lines 1232-1279
# Run: python setup_kafka_topics.py
```

### Task 3: Implement Base Agent Worker (1-2 hours)
```bash
mkdir -p workers
# Create workers/base_worker.py based on implementation plan lines 1286-1415
# Features:
# - RabbitMQ connection and consumption
# - CrewAI agent integration
# - Kafka event publishing
# - Error handling with DLQ
# - Metrics collection
```

### Task 4: Implement Specific Agent Workers (2-3 hours)
```bash
# Create workers/order_agent.py (lines 1420-1468)
# Create workers/support_agent.py (similar structure)
# Create workers/marketing_agent.py (similar structure)
```

### Task 5: Build Agent Workers Docker Image (30 min)
```bash
# Create Dockerfile.workers
docker build -t ghcr.io/bizoholic-digital/bizosaas-agent-workers:latest \
  -f Dockerfile.workers .
docker push ghcr.io/bizoholic-digital/bizosaas-agent-workers:latest
```

### Task 6: Deploy Agent Workers to Docker Swarm (1 hour)
Based on implementation plan lines 1473-1535:
```bash
# Deploy 4 order processing agents
# Deploy 6 support ticket agents
# Deploy 4 marketing agents
# Total: 14 initial workers
```

### Task 7: Enhance HITL API (1-2 hours)
Add missing general-purpose HITL endpoints:
```
GET  /api/hitl/pending         # Get all pending approvals
POST /api/hitl/decision         # Submit approval decision
GET  /api/hitl/metrics          # Get HITL metrics
GET  /api/hitl/dashboard        # Real-time dashboard
```

Currently only SEO and content-marketing specific endpoints exist.

---

## 🎯 Recommended Next Steps

### Option A: Quick Win (Setup Scripts) - 1 hour
1. Create `setup_queues.py`
2. Create `setup_kafka_topics.py`
3. Run both scripts to initialize infrastructure
4. Verify queues and topics are created

### Option B: Full Worker Deployment - 4-6 hours
1. Complete Option A first
2. Implement base worker class
3. Implement 3 specific agent workers
4. Build and deploy Docker image
5. Deploy 14 workers to Docker Swarm
6. Test end-to-end workflow

### Option C: HITL Enhancement - 2-3 hours
1. Add general-purpose HITL endpoints to brain-gateway
2. Create HITL decision engine (if not exists)
3. Integrate with Redis for real-time queue
4. Test approval workflow end-to-end

---

## 📊 Success Metrics

When Phase 2 is complete, we should have:
- ✅ 11 RabbitMQ queues operational
- ✅ 13 Kafka topics created
- ✅ 14 agent workers deployed and processing tasks
- ✅ HITL API fully functional
- ✅ End-to-end test: Task → Agent → HITL → Completion

---

## 🔗 Related Files

- Implementation Plan: `/home/alagiri/projects/bizoholic/BIZOSAAS_COMPLETE_IMPLEMENTATION_PLAN.md`
- Brain Gateway: `/home/alagiri/projects/bizosaas-platform/bizosaas/ai/services/bizosaas-brain/`
- Dokploy URL: https://dk4.bizoholic.com/dashboard/project/c3-8-FgSCrNjun1eLfYOl
- Dokploy API Key: `dk4ixNgzxiGcZWrjlvocbOJqTLjlZsJUEgmTJjjXYvLVSwiUBUPARxklyNFyVQRDHBa`

---

**Status:** Ready to proceed with worker implementation once v2.2.16 build completes.
