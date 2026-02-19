import os
import sys
import asyncio
import logging
from uuid import uuid4

# Setup paths
sys.path.append(os.getcwd())

from main import load_vault_secrets_sync
from app.dependencies import SessionLocal, engine
from app.models import Base, PromptTemplate, McpCategory, McpRegistry
from app.core.prompt_enhancer import prompt_enhancer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def verify_design_integration():
    logger.info("--- Starting Phase 7F: Design Tool Integration Verification ---")
    
    load_vault_secrets_sync()
    db = SessionLocal()
    
    try:
        # 1. Verify Category
        design_cat = db.query(McpCategory).filter(McpCategory.slug == "design-uiux").first()
        assert design_cat is not None, "Design & UI/UX category missing in registry"
        logger.info(f"✅ Verified category: {design_cat.name}")

        # 2. Verify MCP Registry Entries
        expected_mcps = ["stitch-mcp", "figma-mcp", "canva-mcp", "v0-dev-mcp"]
        for slug in expected_mcps:
            mcp = db.query(McpRegistry).filter(McpRegistry.slug == slug).first()
            assert mcp is not None, f"MCP entry missing: {slug}"
            logger.info(f"✅ Verified MCP registry entry: {mcp.name} ({slug})")

        # 3. Verify Prompt Enhancement for UI Specialist
        logger.info("Testing prompt enhancement for UI/UX Specialist...")
        raw_task = "Extract design styles from Figma and generate a hero section."
        payload = {"context": "Brand: EcoGrowth, Target: High-end sustainable retail."}
        
        enhanced = await prompt_enhancer.enhance_prompt(
            agent_type="ui_ux_specialist",
            task_description=raw_task,
            input_data=payload
        )
        
        enhanced_task = enhanced["task_description"]
        logger.debug(f"Enhanced Task Content:\n{enhanced_task}")
        
        assert "Google Stitch" in enhanced_task
        assert "v0.dev" in enhanced_task.lower()
        assert "Extract design styles" in enhanced_task
        assert "EcoGrowth" in enhanced_task
        logger.info("✅ Verified UI/UX Specialist Prompt Enhancement")

        logger.info("🎉 Phase 7F Verification PASSED!")
        
    except Exception as e:
        logger.error(f"❌ Verification FAILED: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(verify_design_integration())
