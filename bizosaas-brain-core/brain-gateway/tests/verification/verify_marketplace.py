import os
import sys
import asyncio
import logging
from uuid import uuid4

# Setup paths
sys.path.append(os.getcwd())

from main import load_vault_secrets_sync
from app.dependencies import SessionLocal, engine
from app.models.marketplace import AffiliatePartner, ThemeTemplate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def verify_marketplace():
    logger.info("--- Starting Phase 7G: Theme Marketplace Verification ---")
    
    load_vault_secrets_sync()
    db = SessionLocal()
    
    try:
        # 1. Create a Test Affiliate Partner
        partner_slug = f"test-partner-{uuid4().hex[:4]}"
        logger.info(f"Creating test partner: {partner_slug}")
        partner = AffiliatePartner(
            name="Test Partner",
            slug=partner_slug,
            website_url="https://test-partner.com",
            is_active=True
        )
        db.add(partner)
        db.commit()
        db.refresh(partner)
        assert partner.id is not None
        logger.info(f"✅ Created affiliate partner: {partner.name}")

        # 2. Create a Test Theme
        theme_slug = f"test-theme-{uuid4().hex[:4]}"
        logger.info(f"Creating test theme: {theme_slug}")
        theme = ThemeTemplate(
            partner_id=partner.id,
            name="Test Modern Theme",
            slug=theme_slug,
            category="modern",
            price=49.99,
            is_active=True,
            tags=["responsive", "clean"]
        )
        db.add(theme)
        db.commit()
        db.refresh(theme)
        assert theme.id is not None
        logger.info(f"✅ Created theme template: {theme.name}")

        # 3. Verify Retrieval via "API-like" Query
        themes = db.query(ThemeTemplate).filter(ThemeTemplate.category == "modern").all()
        assert len(themes) >= 1
        assert any(t.slug == theme_slug for t in themes)
        logger.info("✅ Verified theme retrieval and filtering")

        # 4. Clean up
        db.delete(theme)
        db.delete(partner)
        db.commit()
        logger.info("✅ Cleanup successful")

        logger.info("🎉 Phase 7G Verification PASSED!")
        
    except Exception as e:
        logger.error(f"❌ Verification FAILED: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(verify_marketplace())
