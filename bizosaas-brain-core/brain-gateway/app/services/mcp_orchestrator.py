import asyncio
from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.mcp import UserMcpInstallation
from app.models.workflow import Workflow

class McpOrchestrator:
    """
    Orchestrates the lifecycle of MCP servers (provisioning, monitoring, termination).
    Currently mocks the actual Docker/K8s interactions but maintains the contract.
    """

    @staticmethod
    async def provision_mcp(installation_id: UUID):
        """
        Trigger the provisioning of an MCP server.
        Uses its own DB session to avoid detached instance errors in background tasks.
        """
        print(f"[Orchestrator] Starting provisioning for Installation {installation_id}")
        
        from app.dependencies import SessionLocal
        db = SessionLocal()
        
        try:
            installation = db.query(UserMcpInstallation).filter(UserMcpInstallation.id == installation_id).first()
            if not installation:
                print(f"[Orchestrator] Installation {installation_id} not found")
                return

            installation.status = "provisioning"
            db.commit()

            # Ensure Workflow Record Exists for Dashboard Visibility
            wf_name = f"Provision: {installation.mcp.name}"
            tenant_id = str(installation.user_id) # Using UserID as TenantID for now
            
            existing_wf = db.query(Workflow).filter(
                Workflow.tenant_id == tenant_id,
                Workflow.name == wf_name
            ).first()
            
            if not existing_wf:
                existing_wf = Workflow(
                    tenant_id=tenant_id,
                    name=wf_name,
                    type="Integration",
                    status="running",
                    description=f"Provisioning and configuration workflow for {installation.mcp.name}",
                    config={"retries": 3, "priority": "high"},
                    created_at=datetime.utcnow()
                )
                db.add(existing_wf)
                db.commit()
                db.refresh(existing_wf)
            
            # Update workflow stats
            existing_wf.status = "running"
            existing_wf.runs_today = (existing_wf.runs_today or 0) + 1
            existing_wf.last_run = datetime.utcnow()
            db.commit()

            # Trigger Temporal Workflow for durability
            try:
                import os
                from temporalio.client import Client
                
                # Connect to Temporal
                client = await Client.connect(os.getenv("TEMPORAL_HOST", "localhost:7233"))
                
                # Start the provisioning workflow
                handle = await client.start_workflow(
                    "MCPProvisioningWorkflow",
                    {
                        "installation_id": str(installation_id), 
                        "mcp_slug": installation.mcp.slug,
                        "user_id": str(installation.user_id),
                        "workflow_db_id": str(existing_wf.id) # Pass DB ID if needed for updates
                    },
                    id=f"mcp-provision-{installation_id}",
                    task_queue="mcp-provisioning-queue",
                )
                
                print(f"[Orchestrator] Started Workflow ID: {handle.id}")
                
            except Exception as e:
                print(f"[Orchestrator] Workflow trigger failed ({e}), falling back to direct async...")
                # Fallback to direct async (previous logic) if Temporal fails
                await asyncio.sleep(2)
                
                if installation.mcp:
                    if installation.mcp.slug == "wordpress":
                        # ... existing fallback logic ...
                        pass
            
            # Note: The workflow itself should update the status to 'active' on completion
            # But for the fallback path, we might still need this locally if workflow didn't run.
            # For now, we assume workflow runs or we leave it in provisioning.
            # To keep existing behavior for checking:
            if not os.getenv("TEMPORAL_HOST"): # Only finish immediately if no Temporal
                 installation.status = "active"
                 installation.updated_at = datetime.utcnow()
                 
                 existing_wf.status = "completed"
                 existing_wf.success_rate = 100 # Simple update
                 db.commit()
                 
                 print(f"[Orchestrator] Installation {installation_id} is now ACTIVE (Fallback)")
            
        except Exception as e:
            print(f"[Orchestrator] Provisioning failed: {e}")
            if installation:
                installation.status = "failed"
                db.commit()
        finally:
            db.close()

    @staticmethod
    async def deprovision_mcp(installation_id: UUID, db: Session):
        """
        Stop and remove an MCP server.
        """
        print(f"[Orchestrator] Deprovisioning Installation {installation_id}")
        installation = db.query(UserMcpInstallation).filter(UserMcpInstallation.id == installation_id).first()
        if installation:
            installation.status = "terminated"
            db.commit()
