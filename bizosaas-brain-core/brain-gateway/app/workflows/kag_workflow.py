from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy

# Import activities
with workflow.unsafe.imports_passed_through():
    from app.core.kag_service import kag_service
    from app.core.intelligence import call_ai_agent_with_rag

@workflow.defn
class KAGExtractionWorkflow:
    """
    Workflow for extracting relationships from a knowledge chunk
    and linking them in the knowledge graph (PostgreSQL + Neo4j).
    """
    
    @workflow.run
    async def run(self, chunk_id: int, content: str, tenant_id: str = "global") -> dict:
        # Step 1: Extract relations using the RelationExtractionAgent
        # In a more complex setup, this would be a separate activity
        # But here we can call it via the intelligence layer
        
        # Define retry policy for AI agent calls
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=5),
            maximum_attempts=3,
            non_retryable_error_types=["ValueError"]
        )

        try:
            # We call the kag_service method which already uses the agent
            # However, for Temporal, it's better to have explicit steps
            
            # Step 1: AI-based Extraction
            extraction_result = await workflow.execute_activity(
                "extract_relations_activity",
                {
                    "content": content,
                    "chunk_id": chunk_id,
                    "tenant_id": tenant_id
                },
                start_to_close_timeout=timedelta(minutes=2),
                retry_policy=retry_policy
            )
            
            if not extraction_result or "relationships" not in extraction_result:
                return {"status": "skipped", "reason": "no_relations_found"}

            # Step 2: Linking in Graph
            link_count = await workflow.execute_activity(
                "link_graph_activity",
                {
                    "chunk_id": chunk_id,
                    "relationships": extraction_result["relationships"],
                    "tenant_id": tenant_id
                },
                start_to_close_timeout=timedelta(minutes=1),
                retry_policy=retry_policy
            )
            
            return {
                "status": "completed",
                "chunk_id": chunk_id,
                "links_created": link_count
            }

        except Exception as e:
            workflow.logger.error(f"KAG Extraction Workflow failed for chunk {chunk_id}: {e}")
            raise e
