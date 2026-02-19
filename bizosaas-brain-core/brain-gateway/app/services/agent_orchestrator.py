
import logging
import json
import asyncio
from typing import Dict, Any, List, Optional
from app.core.intelligence import call_ai_agent_with_rag

logger = logging.getLogger(__name__)

class AgentOrchestrator:
    """
    Manages multi-agent collaboration and task delegation.
    Acts as the runtime engine for the Master Orchestrator's plans.
    """
    
    async def process_request(self, user_request: str, user: Any, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Main entry point for complex requests.
        1. Calls Master Orchestrator to plan.
        2. Executes the plan.
        3. Synthesizes results.
        """
        logger.info(f"Orchestrator received request: {user_request[:50]}...")
        tenant_id = user.tenant_id or "global"
        
        # 1. Get Plan from Master Orchestrator
        try:
            # We explicitly ask for a plan
            planning_task = f"Analyze this request and create a delegation plan: {user_request}"
            
            plan_response = await call_ai_agent_with_rag(
                agent_type="master_orchestrator",
                task_description=planning_task,
                payload=context or {},
                tenant_id=tenant_id,
                agent_id=str(user.id) if hasattr(user, 'id') else "system",
                priority="critical", 
                use_rag=True 
            )
            
            raw_response = plan_response.get("response", "{}")
            
            # Extract JSON if wrapped in markdown code blocks
            if "```json" in raw_response:
                raw_response = raw_response.split("```json")[1].split("```")[0]
            elif "```" in raw_response:
                raw_response = raw_response.split("```")[1].split("```")[0]
            
            # Clean up potential leading/trailing whitespace
            raw_response = raw_response.strip()
                
            plan_data = json.loads(raw_response)
            
            # Check if delegation is needed
            delegation_plan = plan_data.get("delegation_plan", [])
            if not delegation_plan:
                # Direct response logic
                return {
                    "response": plan_data.get("direct_response", "I processed your request."),
                    "agent_id": "master_orchestrator",
                    "orchestration_trace": plan_data
                }
                
            logger.info(f"Executing delegation plan with {len(delegation_plan)} steps.")
            
            # 2. Execute Plan
            execution_results = {}
            # TODO: Improve parallel execution for steps without dependencies
            for step in delegation_plan:
                step_id = step.get("step_id")
                agent_id = step.get("agent_id")
                task = step.get("task")
                step_context = step.get("context", "")
                
                # Resolve dependencies
                dependencies = step.get("dependencies", [])
                dep_context = ""
                for dep_id in dependencies:
                    # JSON keys might be strings/ints mismatch, handle both
                    if dep_id in execution_results:
                        dep_context += f"\n[Result from Step {dep_id}]: {execution_results[dep_id].get('response')}\n"
                    elif str(dep_id) in execution_results:
                        dep_context += f"\n[Result from Step {dep_id}]: {execution_results[str(dep_id)].get('response')}\n"

                
                full_task = f"{task}\n\n### Context:\n{step_context}\n\n### Previous Steps Data:\n{dep_context}"
                
                logger.info(f"Executing Step {step_id} with agent {agent_id}")
                
                step_result = await call_ai_agent_with_rag(
                    agent_type=agent_id,
                    task_description=full_task,
                    payload={"parent_task_id": "orchestrator_session"},
                    tenant_id=tenant_id,
                    agent_id="system_orchestrator"
                )
                
                execution_results[step_id] = step_result
            
            # 3. Final Synthesis
            synthesis_task = "Review the results from the specialized agents and provide a consolidated, user-friendly answer."
            # We avoid dumping massive JSON into payload if possible, but RAG helps here.
            # For now passing as string in payload
            synthesis_payload = {
                "original_request": user_request,
                "team_results": str(execution_results) # Convert to string representation
            }
            
            final_response = await call_ai_agent_with_rag(
                agent_type="master_orchestrator",
                task_description=synthesis_task,
                payload=synthesis_payload,
                tenant_id=tenant_id,
                agent_id="system_orchestrator"
            )
            
            return {
                "response": final_response.get("response"),
                "agent_id": "master_orchestrator",
                "orchestration_trace": {
                    "plan": plan_data,
                    "results": execution_results
                }
            }

        except json.JSONDecodeError:
            logger.error(f"Failed to parse Orchestrator JSON plan. Raw: {raw_response[:100]}...")
            # Fallback: Return raw text if it wasn't valid JSON, implies agent just talked
            return {
                "response": raw_response if raw_response else "I attempted to coordinate a plan but encountered an internal error.",
                "agent_id": "master_orchestrator",
                 "error": "JSON Parse Error"
            }
        except Exception as e:
            logger.error(f"Orchestration failed: {e}")
            import traceback
            traceback.print_exc()
            return {
                 "response": f"I encountered an error while coordinating the agents: {str(e)}",
                 "error": str(e)
            }

agent_orchestrator = AgentOrchestrator()
