import strawberry
from typing import List
from ..services.project_service import ProjectService
from .types.project_types import ProjectType, TaskType

# Service Locator (simplified DI)
def get_project_service():
    return ProjectService()

@strawberry.type
class Query:
    @strawberry.field
    async def projects(self, tenant_id: str) -> List[ProjectType]:
        service = get_project_service()
        domain_projects = await service.get_all_projects(tenant_id)
        
        # Map domain entities to GraphQL types if needed
        # Since fields match, we can mostly just return objects or construct types
        return [
            ProjectType(
                id=p.id,
                name=p.name,
                description=p.description,
                status=p.status,
                source_system=p.source_system,
                external_id=p.external_id,
                external_url=p.external_url,
                created_at=p.created_at,
                updated_at=p.updated_at
            ) for p in domain_projects
        ]

    @strawberry.field
    async def tasks(self, tenant_id: str, project_id: str) -> List[TaskType]:
        service = get_project_service()
        domain_tasks = await service.get_project_tasks(tenant_id, project_id)
        
        return [
            TaskType(
                id=t.id,
                project_id=t.project_id,
                title=t.title,
                description=t.description,
                status=t.status.value,  # Enum value
                priority=t.priority.value,
                source_system=t.source_system,
                external_id=t.external_id,
                external_url=t.external_url,
                due_date=t.due_date,
                created_at=t.created_at,
                updated_at=t.updated_at
            ) for t in domain_tasks
        ]

schema = strawberry.Schema(query=Query)
