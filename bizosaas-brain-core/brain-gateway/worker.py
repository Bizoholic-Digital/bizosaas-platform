import asyncio
import logging
from temporalio.client import Client
from temporalio.worker import Worker
from app.workflows.connector_setup import ConnectorSetupWorkflow, ConnectorSyncWorkflow
from app.workflows.marketing_workflow import LeadNurtureWorkflow
from app.activities import (
    validate_connector_credentials,
    save_connector_credentials,
    sync_connector_data,
    update_connector_status,
    check_fluent_crm_lead,
    tag_fluent_crm_contact,
    generate_ai_marketing_content
)
import app.connectors # Ensure connectors are registered

async def run_worker():
    # Connect to valid Temporal server. 
    # In dev, often localhost:7233. In docker, might be 'temporal:7233'
    client = await Client.connect("localhost:7233", namespace="default")
    
    worker = Worker(
        client,
        task_queue="connector-tasks",
        workflows=[ConnectorSetupWorkflow, ConnectorSyncWorkflow, LeadNurtureWorkflow],
        activities=[
            validate_connector_credentials,
            save_connector_credentials,
            sync_connector_data,
            update_connector_status,
            check_fluent_crm_lead,
            tag_fluent_crm_contact,
            generate_ai_marketing_content
        ],
    )
    
    logging.info("Starting Temporal Worker for Connectors...")
    await worker.run()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run_worker())
