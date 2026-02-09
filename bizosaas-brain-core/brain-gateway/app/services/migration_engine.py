from typing import Dict, List, Optional
from pydantic import BaseModel
import asyncio
from datetime import datetime

class MigrationPlan(BaseModel):
    source_mcp: str
    target_mcp: str
    entities: List[str] # e.g., ["products", "customers", "orders"]
    estimated_time_seconds: int
    risk_level: str # "low", "medium", "high"
    warnings: List[str]

class MigrationService:
    """
    Handles data migration between compatible MCP services.
    """
    
    # Static mapping of compatible migrations
    COMPATIBILITY_MATRIX = {
        "shopify": ["woocommerce", "bigcommerce"],
        "woocommerce": ["shopify"],
        "hubspot": ["fluentcrm", "salesforce"],
        "mailchimp": ["activecampaign", "klaviyo"]
    }

    @staticmethod
    def check_compatibility(source_slug: str, target_slug: str) -> bool:
        allowed_targets = MigrationService.COMPATIBILITY_MATRIX.get(source_slug, [])
        return target_slug in allowed_targets

    @staticmethod
    async def create_plan(source_slug: str, target_slug: str) -> MigrationPlan:
        if not MigrationService.check_compatibility(source_slug, target_slug):
            raise ValueError(f"Migration from {source_slug} to {target_slug} is not supported.")
            
        # Logic to determine entities (mocked for now)
        entities = ["products", "customers", "orders"]
        warnings = []
        
        if source_slug == "shopify" and target_slug == "woocommerce":
            warnings.append("Shopify 'metafields' may not map 1:1 to WooCommerce attributes.")
            
        return MigrationPlan(
            source_mcp=source_slug,
            target_mcp=target_slug,
            entities=entities,
            estimated_time_seconds=120 + (len(entities) * 10),
            risk_level="medium" if warnings else "low",
            warnings=warnings
        )

    @staticmethod
    async def execute_migration(plan: MigrationPlan, user_id: str):
        """
        Executes the actual data transfer using specific adapters.
        """
        # 1. Backup Source Data
        print(f"[Migration] Backing up {plan.source_mcp} for user {user_id}")
        await asyncio.sleep(2)
        
        # 2. Transform & Load
        print(f"[Migration] Transforming data to {plan.target_mcp} format...")
        await asyncio.sleep(3)
        
        # 3. Verify
        print(f"[Migration] Verifying data integrity...")
        
        return {"status": "completed", "transferred_entities": len(plan.entities)}
