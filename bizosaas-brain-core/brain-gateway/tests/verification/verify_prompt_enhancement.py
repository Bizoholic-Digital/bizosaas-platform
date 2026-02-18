import os
import sys
import asyncio
import json
import logging
from uuid import uuid4

# Setup paths
sys.path.append(os.getcwd())

from main import load_vault_secrets_sync
from app.dependencies import SessionLocal, engine
from app.models import Base, PromptTemplate, Tenant
from app.core.prompt_enhancer import prompt_enhancer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def verify_prompt_enhancement():
    logger.info("--- Starting Prompt Enhancement Verification ---")
    
    # 1. Load context
    load_vault_secrets_sync()
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    tenant_id = str(uuid4())
    
    try:
        # 2. Seed Test Tenant with Persona
        logger.info(f"Seeding test tenant: {tenant_id}")
        persona = {
            "name": "EcoGrowth",
            "voice": "professional yet eco-conscious",
            "bio": "A marketing agency focused on sustainable brands."
        }
        test_tenant = Tenant(
            id=tenant_id,
            name="EcoGrowth Agency",
            slug=f"ecogrowth-{tenant_id[:4]}",
            settings={"persona": persona}
        )
        db.add(test_tenant)
        
        # 3. Seed Prompt Template
        logger.info("Seeding prompt template for marketing_strategist")
        template = PromptTemplate(
            name="marketing_strategist",
            category="instruction",
            template_text="You are {brand_persona[name]}'s CMO. Task: {task}. Goal: {business_goal}",
            variables={"task": "str", "business_goal": "str"},
            strategy="chain_of_thought",
            is_default=True
        )
        db.add(template)
        db.commit()

        # 4. Test Enhancement
        logger.info("Testing enhancement logic...")
        raw_task = "Create a launch plan for a recyclable bottle."
        payload = {"business_goal": "Reach 1M ecologically conscious consumers."}
        
        enhanced = await prompt_enhancer.enhance_prompt(
            agent_type="marketing_strategist",
            task_description=raw_task,
            input_data=payload,
            tenant_id=tenant_id
        )
        
        enhanced_task = enhanced["task_description"]
        enhanced_payload = enhanced["input_data"]
        
        logger.info(f"Enhanced Task: \n{enhanced_task}")
        
        # 5. Assertions
        assert "EcoGrowth's CMO" in enhanced_task
        assert "Goal: Reach 1M ecologically conscious consumers" in enhanced_task
        assert "step by step" in enhanced_task # CoT
        assert "Respond only in valid JSON" in enhanced_task # Global grounding
        assert "brand_persona" in enhanced_payload
        assert enhanced_payload["brand_persona"]["name"] == "EcoGrowth"
        
        logger.info("✅ Prompt Enhancement Verification PASSED!")
        
    except Exception as e:
        logger.error(f"❌ Verification FAILED: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        db.query(PromptTemplate).filter(PromptTemplate.name == "marketing_strategist").delete()
        db.query(Tenant).filter(Tenant.id == tenant_id).delete()
        db.commit()
        db.close()

if __name__ == "__main__":
    asyncio.run(verify_prompt_enhancement())
