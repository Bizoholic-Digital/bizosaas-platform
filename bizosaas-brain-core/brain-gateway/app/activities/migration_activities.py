import logging
from typing import Dict, Any
from temporalio import activity
from app.services.plan_migration import PlanMigrationService
from app.dependencies import SessionLocal

logger = logging.getLogger(__name__)

@activity.defn
async def migrate_plane_workspace_activity(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Activity to execute a Plane workspace migration.
    """
    tenant_id = params.get("tenant_id")
    credentials = params.get("credentials", {})
    workspace_slug = params.get("workspace_slug") or credentials.get("workspace_slug")
    
    if not tenant_id or not credentials or not workspace_slug:
        return {"status": "error", "message": "Missing required migration parameters"}

    try:
        # Use a fresh DB session
        with SessionLocal() as db:
            migration_service = PlanMigrationService(db)
            results = await migration_service.migrate_workspace(
                tenant_id=tenant_id,
                credentials=credentials,
                workspace_slug=workspace_slug
            )
            return {
                "status": "completed",
                "projects_migrated": results.get("projects_migrated", 0),
                "issues_migrated": results.get("issues_migrated", 0),
                "errors": results.get("errors", [])
            }
    except Exception as e:
        logger.error(f"Migration activity failed: {e}")
        return {"status": "error", "message": str(e)}

@activity.defn
async def get_migration_preview_activity(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Activity to fetch a preview of the migration.
    """
    tenant_id = params.get("tenant_id")
    credentials = params.get("credentials", {})
    
    try:
        with SessionLocal() as db:
            migration_service = PlanMigrationService(db)
            preview = await migration_service.get_migration_preview(tenant_id, credentials)
            return {
                "status": "success",
                "preview": preview
            }
    except Exception as e:
        logger.error(f"Migration preview activity failed: {e}")
        return {"status": "error", "message": str(e)}
