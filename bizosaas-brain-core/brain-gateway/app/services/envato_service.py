import httpx
import logging
import os
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from app.models.marketplace import AffiliatePartner, ThemeTemplate
from app.core.vault import vault_service

logger = logging.getLogger(__name__)

class EnvatoService:
    """
    Service for interacting with the Envato Market API.
    Handles theme discovery, metadata fetching, and synchronization.
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.base_url = "https://api.envato.com/v3"

    async def _get_api_key(self, partner: AffiliatePartner) -> Optional[str]:
        """Fetch API key from Vault if possible, otherwise check api_config."""
        if partner.api_key_vault_path:
            secret = await vault_service.get_secret(partner.api_key_vault_path)
            if secret:
                return secret.get("api_key")
        
        return partner.api_config.get("api_key")

    async def sync_themes(self, partner_slug: str = "envato") -> Dict[str, Any]:
        """
        Synchronizes themes from Envato for a specific partner.
        """
        partner = self.db.query(AffiliatePartner).filter(AffiliatePartner.slug == partner_slug).first()
        if not partner:
            logger.error(f"Affiliate partner '{partner_slug}' not found")
            return {"success": False, "error": "Partner not found"}

        api_key = await self._get_api_key(partner)
        if not api_key:
            logger.error(f"API key missing for partner '{partner_slug}'")
            return {"success": False, "error": "API key missing"}

        headers = {
            "Authorization": f"Bearer {api_key}",
            "User-Agent": "BizOSaaS-Platform-Marketplace"
        }

        # Example: Search for WordPress themes
        search_url = f"{self.base_url}/market/search/item?site=themeforest.net&category=wordpress&sort_by=trending-desc"

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.get(search_url, headers=headers)
                response.raise_for_status()
                data = response.json()
                
                items = data.get("matches", [])
                synced_count = 0
                
                for item in items:
                    # Map Envato item to ThemeTemplate
                    theme_data = {
                        "partner_id": partner.id,
                        "name": item.get("name"),
                        "slug": f"envato-{item.get('id')}",
                        "description": item.get("description"),
                        "category": "wordpress", # Or refine based on item tags
                        "price": item.get("price_cents", 0) / 100.0,
                        "preview_url": item.get("previews", {}).get("live_site", {}).get("url"),
                        "thumbnail_url": item.get("previews", {}).get("icon_with_landscape_preview", {}).get("landscape_url"),
                        "affiliate_link": f"{item.get('url')}?ref=bizoholic", # Custom ref
                        "tags": item.get("tags", [])
                    }
                    
                    # Update or Create
                    theme = self.db.query(ThemeTemplate).filter(ThemeTemplate.slug == theme_data["slug"]).first()
                    if theme:
                        for key, value in theme_data.items():
                            setattr(theme, key, value)
                    else:
                        theme = ThemeTemplate(**theme_data)
                        self.db.add(theme)
                    
                    synced_count += 1
                
                self.db.commit()
                logger.info(f"Successfully synced {synced_count} themes from Envato")
                return {"success": True, "count": synced_count}

            except Exception as e:
                logger.error(f"Envato sync failed: {e}")
                self.db.rollback()
                return {"success": False, "error": str(e)}
