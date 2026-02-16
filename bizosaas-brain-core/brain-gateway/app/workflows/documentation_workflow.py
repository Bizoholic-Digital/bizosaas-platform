from datetime import timedelta
from typing import Dict, Any, List
from temporalio import workflow
import logging

# Import activities
with workflow.unsafe.imports_passed_through():
    from app.activities.documentation import (
        generate_documentation_activity,
        update_docusaurus_content_activity
    )

logger = logging.getLogger(__name__)

@workflow.defn
class DocumentationWorkflow:
    \"\"\"
    Workflow to orchestrate the generation and update of BizoSaaS documentation.
    \"\"\"
    @workflow.run
    async def run(self, params: Dict[str, Any]) -> Dict[str, Any]:
        tenant_id = params.get("tenant_id", "default")
        tasks = params.get("tasks", [])  # List of documentation tasks to perform
        
        results = []
        
        for task in tasks:
            task_type = task.get("task_type")
            input_data = task.get("input_data", {})
            relative_path = task.get("relative_path")
            
            # 1. Generate documentation via DocumentationAgent
            gen_result = await workflow.execute_activity(
                generate_documentation_activity,
                {
                    "tenant_id": tenant_id,
                    "task_type": task_type,
                    "input_data": input_data
                },
                start_to_close_timeout=timedelta(minutes=5)
            )
            
            if gen_result.get("status") == "success":
                doc_content = gen_result.get("result", {}).get("documentation")
                
                # 2. Update Docusaurus if content was generated and a path is provided
                if doc_content and relative_path:
                    update_result = await workflow.execute_activity(
                        update_docusaurus_content_activity,
                        {
                            "content": doc_content,
                            "relative_path": relative_path
                        },
                        start_to_close_timeout=timedelta(minutes=1)
                    )
                    results.append({
                        "task_type": task_type,
                        "generation": "success",
                        "deployment": update_result.get("status"),
                        "file_path": update_result.get("file_path")
                    })
                else:
                    results.append({
                        "task_type": task_type,
                        "generation": "success",
                        "deployment": "skipped",
                        "reason": "Missing documentation content or relative_path"
                    })
            else:
                results.append({
                    "task_type": task_type,
                    "generation": "failed",
                    "error": gen_result.get("message")
                })
                
        return {
            "status": "completed",
            "results": results,
            "tenant_id": tenant_id
        }
