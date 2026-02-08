import logging
from typing import Dict, Any, List, Optional
from app.connectors.plane import PlaneConnector
from app.domain.ports.project_port import Project, Issue
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

class PlanMigrationService:
    """
    Handles data migration from Plan.so (Plane) to BizOSaaS.
    Translates Plane entities to internal domain models and/or other connectors.
    """
    
    def __init__(self, db: Session):
        self.db = db

    async def migrate_workspace(self, tenant_id: str, credentials: Dict[str, Any], workspace_slug: str):
        """
        Migrate an entire Plane workspace.
        1. Initialize Plane connector
        2. Fetch projects
        3. Fetch issues for each project
        4. Store in internal database or relevant target connectors
        """
        logger.info(f"Starting Plan.so migration for tenant {tenant_id}, workspace {workspace_slug}")
        
        connector = PlaneConnector(tenant_id, credentials)
        
        # 1. Validate
        if not await connector.validate_credentials():
            raise ValueError("Invalid Plane credentials")

        # 2. Get Projects
        projects = await connector.get_projects()
        logger.info(f"Found {len(projects)} projects in workspace {workspace_slug}")
        
        results = {
            "projects_migrated": 0,
            "issues_migrated": 0,
            "errors": []
        }

        for project in projects:
            try:
                # 3. Get Issues for project
                issues = await connector.get_issues(project.id)
                logger.debug(f"Migrating project {project.name} with {len(issues)} issues")
                
                # In a real implementation, we would save these to the target system
                # For now, we simulate the storage logic
                results["projects_migrated"] += 1
                results["issues_migrated"] += len(issues)
                
            except Exception as e:
                logger.error(f"Failed to migrate project {project.name}: {e}")
                results["errors"].append(f"Project {project.name}: {str(e)}")

        return results

    async def get_migration_preview(self, tenant_id: str, credentials: Dict[str, Any]):
        """Fetch summary of data to be migrated without executing migration"""
        connector = PlaneConnector(tenant_id, credentials)
        workspace_slug = credentials.get("workspace_slug")
        
        projects = await connector.get_projects()
        
        return {
            "workspace": workspace_slug,
            "project_count": len(projects),
            "estimated_effort": "low" if len(projects) < 5 else "medium"
        }
