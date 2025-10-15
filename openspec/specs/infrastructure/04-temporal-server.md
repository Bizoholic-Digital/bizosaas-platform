# Temporal Server - Infrastructure

## Service Identity
- **Name**: Temporal Server
- **Type**: Infrastructure - Workflow Orchestration Engine
- **Container**: `bizosaas-temporal-server-staging` (NOT RUNNING - needs deployment)
- **Image**: `temporalio/auto-setup:latest`
- **Port**: `7233:7233` (gRPC), `7234:7234` (HTTP)
- **Network**: `dokploy-network`
- **Status**: ❌ Defined but not deployed

## Purpose
Durable workflow execution engine for long-running, distributed business processes including campaign automation, data processing pipelines, multi-step AI agent workflows, and scheduled tasks.

## Architecture

### Temporal Components
```
Temporal Server
├── Frontend Service (gRPC Gateway)
├── History Service (Workflow State Machine)
├── Matching Service (Task Queue Management)
├── Worker Service (Task Execution)
└── PostgreSQL (Persistence Layer)
```

### Workflow Types in BizOSaaS
```
Campaign Workflows:
├── Campaign Creation Workflow
├── Multi-Channel Publishing Workflow
├── Performance Monitoring Workflow
└── Campaign Optimization Workflow

AI Agent Workflows:
├── Digital Presence Audit Workflow (4-agent)
├── Content Generation Pipeline (3-agent)
├── SEO Analysis Workflow (2-agent)
└── Report Generation Workflow (single-agent)

Data Processing:
├── Analytics Aggregation Workflow
├── Lead Scoring Workflow
├── Data Sync Workflow
└── Backup/Archive Workflow

Scheduled Tasks:
├── Daily Report Generation
├── Weekly Performance Review
├── Monthly Billing Workflow
└── Quarterly Analytics Summary
```

## Dependencies

### Required By (Consumers)
- Brain API Gateway (workflow triggering)
- AI Agents Service (durable agent execution)
- Campaign Management (multi-step campaigns)
- Analytics Service (scheduled aggregations)
- Temporal UI (workflow monitoring)

### Dependencies (Requirements)
- PostgreSQL (workflow state persistence)
- Redis (optional caching)

## Configuration

### Environment Variables
```bash
# Temporal Server
TEMPORAL_ADDRESS=bizosaas-temporal-server-staging:7233
TEMPORAL_NAMESPACE=bizosaas
TEMPORAL_UI_ADDRESS=bizosaas-temporal-ui-staging:8080

# Database
DB=postgresql
DB_HOST=bizosaas-postgres-staging
DB_PORT=5432
DBNAME=temporal
POSTGRES_USER=postgres
POSTGRES_PWD=SharedInfra2024!SuperSecure

# Temporal Configuration
TEMPORAL_LOG_LEVEL=info
TEMPORAL_MAX_CONCURRENT_ACTIVITIES=1000
TEMPORAL_MAX_CONCURRENT_WORKFLOWS=1000
TEMPORAL_WORKFLOW_EXECUTION_TIMEOUT=24h
TEMPORAL_ACTIVITY_EXECUTION_TIMEOUT=1h
```

### Docker Compose Configuration
```yaml
services:
  temporal-server:
    image: temporalio/auto-setup:latest
    container_name: bizosaas-temporal-server-staging
    depends_on:
      - postgres
    environment:
      - DB=postgresql
      - DB_PORT=5432
      - POSTGRES_USER=postgres
      - POSTGRES_PWD=${POSTGRES_PASSWORD}
      - POSTGRES_SEEDS=bizosaas-postgres-staging
      - TEMPORAL_CLI_ADDRESS=bizosaas-temporal-server-staging:7233
      - DYNAMIC_CONFIG_FILE_PATH=config/dynamicconfig/development-sql.yaml
    ports:
      - "7233:7233"  # gRPC
      - "7234:7234"  # HTTP
    networks:
      - dokploy-network
    volumes:
      - ./temporal/dynamicconfig:/etc/temporal/config/dynamicconfig
    healthcheck:
      test: ["CMD", "tctl", "--address", "bizosaas-temporal-server-staging:7233", "cluster", "health"]
      interval: 10s
      timeout: 5s
      retries: 10
    restart: unless-stopped
```

## Workflow Definition Examples

### Campaign Creation Workflow
```python
from temporalio import workflow, activity
from datetime import timedelta

@workflow.defn
class CampaignCreationWorkflow:
    @workflow.run
    async def run(self, campaign_data: dict) -> dict:
        # Step 1: Validate campaign data (5 min timeout)
        validated_data = await workflow.execute_activity(
            validate_campaign_data,
            campaign_data,
            start_to_close_timeout=timedelta(minutes=5)
        )

        # Step 2: Create campaign in database (2 min timeout)
        campaign_id = await workflow.execute_activity(
            create_campaign_record,
            validated_data,
            start_to_close_timeout=timedelta(minutes=2)
        )

        # Step 3: Generate AI content (15 min timeout)
        content = await workflow.execute_activity(
            generate_campaign_content,
            campaign_id,
            start_to_close_timeout=timedelta(minutes=15)
        )

        # Step 4: Publish to channels (10 min timeout)
        results = await workflow.execute_activity(
            publish_to_channels,
            {"campaign_id": campaign_id, "content": content},
            start_to_close_timeout=timedelta(minutes=10)
        )

        return {
            "campaign_id": campaign_id,
            "status": "published",
            "results": results
        }

@activity.defn
async def validate_campaign_data(data: dict) -> dict:
    # Validation logic
    return data

@activity.defn
async def create_campaign_record(data: dict) -> str:
    # Database insertion
    return "campaign-uuid-123"

@activity.defn
async def generate_campaign_content(campaign_id: str) -> dict:
    # AI content generation (may take 10+ minutes)
    return {"title": "...", "body": "..."}

@activity.defn
async def publish_to_channels(data: dict) -> list:
    # Publish to Google Ads, Meta, LinkedIn, etc.
    return [{"channel": "google", "status": "published"}]
```

### AI Agent Workflow (4-Agent Pattern)
```python
@workflow.defn
class DigitalPresenceAuditWorkflow:
    @workflow.run
    async def run(self, company_domain: str) -> dict:
        # Agent 1: Website Audit
        website_data = await workflow.execute_activity(
            website_audit_agent,
            company_domain,
            start_to_close_timeout=timedelta(minutes=10)
        )

        # Agent 2: Social Media Analysis (parallel)
        social_task = workflow.execute_activity(
            social_media_agent,
            company_domain,
            start_to_close_timeout=timedelta(minutes=10)
        )

        # Agent 3: SEO Analysis (parallel)
        seo_task = workflow.execute_activity(
            seo_analysis_agent,
            company_domain,
            start_to_close_timeout=timedelta(minutes=10)
        )

        # Wait for parallel tasks
        social_data, seo_data = await asyncio.gather(social_task, seo_task)

        # Agent 4: Report Generation (sequential)
        report = await workflow.execute_activity(
            report_generation_agent,
            {
                "website": website_data,
                "social": social_data,
                "seo": seo_data
            },
            start_to_close_timeout=timedelta(minutes=5)
        )

        return report
```

### Scheduled Workflow (Cron)
```python
@workflow.defn
class DailyAnalyticsWorkflow:
    @workflow.run
    async def run(self) -> dict:
        # Aggregate yesterday's data
        yesterday = datetime.now() - timedelta(days=1)

        # Fetch analytics
        analytics = await workflow.execute_activity(
            aggregate_daily_analytics,
            yesterday.strftime("%Y-%m-%d"),
            start_to_close_timeout=timedelta(minutes=30)
        )

        # Generate report
        report = await workflow.execute_activity(
            generate_analytics_report,
            analytics,
            start_to_close_timeout=timedelta(minutes=10)
        )

        # Send notifications
        await workflow.execute_activity(
            send_daily_report,
            report,
            start_to_close_timeout=timedelta(minutes=5)
        )

        return {"status": "completed", "date": str(yesterday)}
```

## Python Client Integration

### Install Temporal SDK
```bash
pip install temporalio
```

### Client Configuration
```python
from temporalio.client import Client

async def get_temporal_client() -> Client:
    """Get Temporal client"""
    return await Client.connect(
        "bizosaas-temporal-server-staging:7233",
        namespace="bizosaas"
    )

# Singleton
temporal_client = None

async def init_temporal():
    global temporal_client
    temporal_client = await get_temporal_client()
```

### Start Workflow
```python
from temporalio.client import Client

async def start_campaign_workflow(campaign_data: dict) -> str:
    """Start campaign creation workflow"""
    client = await get_temporal_client()

    # Start workflow
    handle = await client.start_workflow(
        CampaignCreationWorkflow.run,
        campaign_data,
        id=f"campaign-{campaign_data['id']}",
        task_queue="campaign-tasks",
        execution_timeout=timedelta(hours=24)
    )

    return handle.id

# Get workflow result
async def get_workflow_result(workflow_id: str):
    client = await get_temporal_client()
    handle = client.get_workflow_handle(workflow_id)
    return await handle.result()
```

### Query Workflow Status
```python
async def get_campaign_status(campaign_id: str) -> dict:
    """Get campaign workflow status"""
    client = await get_temporal_client()

    handle = client.get_workflow_handle(f"campaign-{campaign_id}")

    # Get workflow description
    description = await handle.describe()

    return {
        "workflow_id": description.id,
        "status": description.status,
        "start_time": description.start_time,
        "close_time": description.close_time,
        "execution_time": description.execution_time
    }
```

### Cancel Workflow
```python
async def cancel_campaign(campaign_id: str):
    """Cancel running campaign workflow"""
    client = await get_temporal_client()
    handle = client.get_workflow_handle(f"campaign-{campaign_id}")
    await handle.cancel()
```

## Worker Configuration

### Worker Process
```python
from temporalio.worker import Worker

async def run_campaign_worker():
    """Run Temporal worker for campaign workflows"""
    client = await get_temporal_client()

    # Create worker
    worker = Worker(
        client,
        task_queue="campaign-tasks",
        workflows=[
            CampaignCreationWorkflow,
            CampaignOptimizationWorkflow
        ],
        activities=[
            validate_campaign_data,
            create_campaign_record,
            generate_campaign_content,
            publish_to_channels
        ]
    )

    # Run worker
    await worker.run()

# Run in separate process
if __name__ == "__main__":
    asyncio.run(run_campaign_worker())
```

### Multiple Task Queues
```python
# Brain Gateway worker (high priority)
worker_brain = Worker(
    client,
    task_queue="brain-gateway-tasks",
    workflows=[...],
    activities=[...],
    max_concurrent_activities=100
)

# AI Agents worker (resource intensive)
worker_ai = Worker(
    client,
    task_queue="ai-agent-tasks",
    workflows=[...],
    activities=[...],
    max_concurrent_activities=10  # Limit concurrent AI tasks
)

# Analytics worker (scheduled)
worker_analytics = Worker(
    client,
    task_queue="analytics-tasks",
    workflows=[...],
    activities=[...],
    max_concurrent_activities=50
)
```

## Scheduled Workflows (Cron)

### Daily Reports
```python
from temporalio.client import Client, ScheduleActionStartWorkflow, ScheduleSpec, ScheduleIntervalSpec

async def schedule_daily_reports():
    """Schedule daily analytics reports"""
    client = await get_temporal_client()

    await client.create_schedule(
        id="daily-analytics-report",
        schedule=ScheduleActionStartWorkflow(
            DailyAnalyticsWorkflow.run,
            id="daily-analytics",
            task_queue="analytics-tasks"
        ),
        spec=ScheduleSpec(
            # Run every day at 2 AM UTC
            cron_expressions=["0 2 * * *"]
        )
    )
```

### Weekly Performance Review
```python
await client.create_schedule(
    id="weekly-performance-review",
    schedule=ScheduleActionStartWorkflow(
        WeeklyPerformanceWorkflow.run,
        id="weekly-performance",
        task_queue="analytics-tasks"
    ),
    spec=ScheduleSpec(
        # Run every Monday at 9 AM UTC
        cron_expressions=["0 9 * * 1"]
    )
)
```

## Integration with Brain API Gateway

### FastAPI Endpoint to Start Workflow
```python
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/campaigns")
async def create_campaign(campaign_data: dict):
    """Create campaign via Temporal workflow"""
    try:
        # Start workflow
        workflow_id = await start_campaign_workflow(campaign_data)

        return {
            "workflow_id": workflow_id,
            "status": "started",
            "message": "Campaign workflow initiated"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/campaigns/{campaign_id}/status")
async def get_campaign_status(campaign_id: str):
    """Get campaign workflow status"""
    try:
        status = await get_campaign_status(campaign_id)
        return status
    except Exception as e:
        raise HTTPException(status_code=404, detail="Workflow not found")
```

## Health Checks

### Container Health Check
```bash
# Check Temporal server health
docker exec bizosaas-temporal-server-staging tctl --address bizosaas-temporal-server-staging:7233 cluster health
```

### Application Health Check
```python
async def check_temporal_health():
    try:
        client = await Client.connect("bizosaas-temporal-server-staging:7233")
        await client.list_workflows()  # Test connection
        return True
    except Exception as e:
        return False
```

## Monitoring

### Key Metrics
- Workflow execution count
- Activity task latency
- Workflow execution time
- Failed workflows
- Task queue backlog

### Temporal Web UI Queries
```
# Failed workflows
WorkflowStatus = "Failed"

# Long-running workflows
ExecutionTime > "1h"

# Workflows by type
WorkflowType = "CampaignCreationWorkflow"
```

## Common Issues

### Issue 1: Workflow Stuck
**Symptom**: Workflow not progressing
**Diagnosis**: Check activity timeouts
**Solution**:
- Increase activity timeout
- Check worker is running
- Verify network connectivity

### Issue 2: Worker Not Processing Tasks
**Symptom**: Tasks queued but not executed
**Diagnosis**: Worker process down
**Solution**:
- Start worker process
- Check task queue name matches
- Verify worker has correct workflows/activities registered

### Issue 3: Database Connection Failed
**Symptom**: Temporal server cannot start
**Diagnosis**: PostgreSQL unreachable
**Solution**:
- Verify PostgreSQL container running
- Check network connectivity
- Verify credentials in environment variables

## Deployment Checklist

- [ ] PostgreSQL temporal database created
- [ ] Temporal Server container deployed
- [ ] Temporal UI can connect to server
- [ ] Worker processes deployed and running
- [ ] Test workflow executed successfully
- [ ] Scheduled workflows configured
- [ ] Health checks passing
- [ ] Monitoring dashboards created

## References
- [Temporal Documentation](https://docs.temporal.io/)
- [Python SDK Guide](https://docs.temporal.io/dev-guide/python)
- [Workflow Patterns](https://docs.temporal.io/workflows)
- BizOSaaS PRD: `/home/alagiri/projects/bizoholic/comprehensive_prd_06092025.md`

---
**Status**: ❌ Pending Deployment
**Priority**: HIGH (required for workflow orchestration)
**Last Updated**: October 15, 2025
**Owner**: Infrastructure Team
