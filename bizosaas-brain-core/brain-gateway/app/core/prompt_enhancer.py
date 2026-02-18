import logging
import json
import re
from typing import Dict, Any, List, Optional
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from app.core.vault import get_config_val
from app.models.prompt import PromptTemplate
from app.models.user import Tenant

logger = logging.getLogger(__name__)

class PromptEnhancer:
    """
    Service for enhancing AI prompts using structured templates, 
    tenant-specific personas, and advanced reasoning strategies.
    """
    
    def __init__(self):
        self.db_url = get_config_val("DATABASE_URL") or "postgresql://postgres:postgres@localhost:5432/bizoholic"
        self.engine = sa.create_engine(self.db_url, pool_pre_ping=True)
        self.Session = sessionmaker(bind=self.engine)

    async def enhance_prompt(
        self, 
        agent_type: str, 
        task_description: str, 
        input_data: Dict[str, Any],
        tenant_id: str = "global",
        overrides: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Main entry point for prompt enhancement.
        Returns potentially modified task_description and input_data.
        """
        enhanced_task = task_description
        enhanced_payload = input_data.copy()
        
        # 1. Fetch Brand Persona
        persona = await self._get_tenant_persona(tenant_id)
        if persona:
            enhanced_payload["brand_persona"] = persona
            logger.debug(f"Injected brand persona for tenant {tenant_id}")

        # 2. Find and apply relevant template
        template = await self._find_template(agent_type, tenant_id)
        if template:
            enhanced_task = self._apply_template(template, enhanced_task, enhanced_payload)
            
            # 3. Apply Reasoning Strategies (CoT, etc.)
            if template.strategy == "chain_of_thought":
                enhanced_task = self._apply_cot_strategy(enhanced_task)
            elif template.strategy == "few_shot":
                 enhanced_task = self._apply_few_shot_strategy(enhanced_task, template)

        # 4. Global safety/formatting grounding
        enhanced_task = self._apply_global_grounding(enhanced_task)

        return {
            "task_description": enhanced_task,
            "input_data": enhanced_payload
        }

    async def _get_tenant_persona(self, tenant_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve brand persona from tenant settings"""
        if tenant_id == "global":
            return None
            
        with self.Session() as session:
            try:
                # Need to handle GUID vs string if needed, but usually sa handles it
                tenant = session.query(Tenant).filter(Tenant.id == tenant_id).first()
                if tenant and tenant.settings:
                    return tenant.settings.get("persona")
            except Exception as e:
                logger.error(f"Failed to fetch persona for tenant {tenant_id}: {e}")
        return None

    async def _find_template(self, agent_type: str, tenant_id: str) -> Optional[PromptTemplate]:
        """Find the best matching template (tenant-specific > platform default)"""
        with self.Session() as session:
            try:
                # 1. Try tenant-specific template
                template = session.query(PromptTemplate).filter(
                    PromptTemplate.name == agent_type,
                    PromptTemplate.tenant_id == tenant_id
                ).order_by(PromptTemplate.updated_at.desc()).first()
                
                if template:
                    return template
                
                # 2. Try platform default
                template = session.query(PromptTemplate).filter(
                    PromptTemplate.name == agent_type,
                    PromptTemplate.is_default == True
                ).first()
                
                return template
            except Exception as e:
                logger.error(f"Failed to find template for {agent_type}: {e}")
        return None

    def _apply_template(self, template: PromptTemplate, task: str, payload: Dict[str, Any]) -> str:
        """Merge task description into the template if variables match"""
        text = template.template_text
        
        # Merge payload variables
        try:
            # We assume {task} is a standard variable if not present in payload
            merged_payload = payload.copy()
            if "task" not in merged_payload:
                merged_payload["task"] = task
                
            return text.format(**merged_payload)
        except KeyError as e:
            logger.warning(f"Template {template.name} missing variable: {e}. Returning raw task.")
            return task
        except Exception as e:
            logger.error(f"Error applying template {template.name}: {e}")
            return task

    def _apply_cot_strategy(self, task: str) -> str:
        """Apply Chain of Thought strategy"""
        cot_suffix = "\n\nLet's think step by step to ensure a high-quality, reasoned result."
        if cot_suffix not in task:
            return task + cot_suffix
        return task

    def _apply_few_shot_strategy(self, task: str, template: PromptTemplate) -> str:
        """Append examples if available in metadata"""
        # Metadata check? For now just return task as placeholder
        return task

    def _apply_global_grounding(self, task: str) -> str:
        """Inject universal instruction for format and safety"""
        grounding = "\n\nRespond only in valid JSON format unless specified otherwise. Maintain professional tone."
        if grounding not in task:
            return task + grounding
        return task

# Singleton
prompt_enhancer = PromptEnhancer()
