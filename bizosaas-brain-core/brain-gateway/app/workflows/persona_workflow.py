from datetime import timedelta
from typing import Dict, Any, List
from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from app.activities.persona import (
        analyze_website_activity,
        extract_brand_voice_activity,
        generate_core_persona_activity,
        adapt_platform_personas_activity,
    )

@workflow.defn
class PersonaGenerationWorkflow:
    """
    Brand Persona System: Analyzes website/onboarding data to create 
    consistent brand voice across platforms.
    """
    
    @workflow.run
    async def run(self, params: Dict[str, Any]) -> Dict[str, Any]:
        tenant_id = params["tenant_id"]
        website_url = params.get("website_url")
        onboarding_data = params.get("onboarding_data", {})

        # Step 1: Website Analysis (if URL provided)
        website_insights = {}
        if website_url:
            website_insights = await workflow.execute_activity(
                analyze_website_activity,
                args=[tenant_id, website_url],
                start_to_close_timeout=timedelta(minutes=10)
            )

        # Step 2: Brand Voice Extraction
        brand_voice = await workflow.execute_activity(
            extract_brand_voice_activity,
            args=[tenant_id, website_insights, onboarding_data],
            start_to_close_timeout=timedelta(minutes=5)
        )

        # Step 3: Core Persona Generation
        core_persona = await workflow.execute_activity(
            generate_core_persona_activity,
            args=[tenant_id, brand_voice],
            start_to_close_timeout=timedelta(minutes=5)
        )

        # Step 4: Platform Adaptation (LinkedIn, IG, Twitter, Email)
        platform_personas = await workflow.execute_activity(
            adapt_platform_personas_activity,
            args=[tenant_id, core_persona],
            start_to_close_timeout=timedelta(minutes=5)
        )

        # Step 5: Store results (handled within activities or separate store activity)
        # For simplicity in this workflow, we'll return the final package
        # which will be stored by the calling activity or service.
        
        return {
            "status": "completed",
            "tenant_id": tenant_id,
            "core_persona": core_persona,
            "platform_variants": platform_personas
        }
