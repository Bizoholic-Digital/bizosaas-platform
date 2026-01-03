"""
Strategy Validation Workflow - AI-powered feasibility engine.

Implements PRD Step 11: Loop where AI validates campaign strategy against:
1. Historical data from connected platforms
2. Industry benchmarks
3. Budget adequacy
4. Timeline realism

The workflow continues until the client accepts the recommendations or
manually approves their original strategy.
"""

from datetime import timedelta
from temporalio import workflow, activity
from typing import Dict, Any, List, Optional
import logging
import json

logger = logging.getLogger(__name__)


# --- Activities ---

@activity.defn
async def fetch_connector_insights(tenant_id: str, platforms: List[str]) -> Dict[str, Any]:
    """
    Fetch historical performance data from connected platforms.
    Used to inform the AI's feasibility analysis.
    """
    from app.store import active_connectors
    from app.connectors.registry import ConnectorRegistry
    
    insights = {}
    
    for platform in platforms:
        key = f"{tenant_id}:{platform}"
        if key in active_connectors:
            try:
                data = active_connectors[key]
                connector = ConnectorRegistry.create_connector(
                    platform, 
                    tenant_id, 
                    data.get("credentials", {})
                )
                
                # Try to get performance metrics
                if hasattr(connector, 'get_performance_metrics'):
                    metrics = await connector.get_performance_metrics()
                    insights[platform] = {
                        "connected": True,
                        "metrics": metrics
                    }
                else:
                    insights[platform] = {
                        "connected": True,
                        "metrics": None
                    }
            except Exception as e:
                logger.warning(f"Failed to fetch insights from {platform}: {e}")
                insights[platform] = {"connected": True, "error": str(e)}
        else:
            insights[platform] = {"connected": False}
    
    return insights


@activity.defn
async def get_industry_benchmarks(industry: str, goal: str) -> Dict[str, Any]:
    """
    Fetch industry benchmarks for the given goal type.
    In production, this would query a benchmarks database or API.
    """
    # Sample benchmark data - would be from real data sources
    benchmarks = {
        "lead_gen": {
            "avg_cpl_google": 50.0,  # Cost per lead
            "avg_cpl_facebook": 35.0,
            "avg_conversion_rate": 2.5,
            "recommended_min_budget": 1000,
            "recommended_timeline_months": 3,
        },
        "ecommerce_sales": {
            "avg_roas": 3.5,  # Return on ad spend
            "avg_cpc": 1.20,
            "avg_conversion_rate": 2.8,
            "recommended_min_budget": 2000,
            "recommended_timeline_months": 6,
        },
        "brand_awareness": {
            "avg_cpm": 8.0,  # Cost per 1000 impressions
            "avg_reach_per_dollar": 125,
            "recommended_min_budget": 500,
            "recommended_timeline_months": 2,
        },
        "app_installs": {
            "avg_cpi": 2.50,  # Cost per install
            "avg_install_rate": 1.8,
            "recommended_min_budget": 3000,
            "recommended_timeline_months": 4,
        }
    }
    
    return benchmarks.get(goal, benchmarks["lead_gen"])


@activity.defn
async def analyze_strategy_with_ai(
    strategy: Dict[str, Any],
    connector_insights: Dict[str, Any],
    benchmarks: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Use AI to analyze the proposed strategy and provide recommendations.
    """
    import os
    
    # Prepare context for AI
    context = f"""
You are a digital marketing strategy analyst. Analyze this campaign strategy and provide a feasibility assessment.

PROPOSED STRATEGY:
- Goal: {strategy['goal']}
- Budget: ${strategy['budget']} {strategy.get('currency', 'USD')} per month
- Platforms: {', '.join(strategy.get('platforms', []))}
- Target Audience: {json.dumps(strategy.get('target_audience', {}))}
- Timeline: {strategy.get('timeline_months', 3)} months

INDUSTRY BENCHMARKS:
{json.dumps(benchmarks, indent=2)}

CONNECTED PLATFORM DATA:
{json.dumps(connector_insights, indent=2)}

Provide your analysis in the following JSON format:
{{
    "feasibility_score": <0-100>,
    "budget_adequacy_score": <0-100>,
    "platform_fit_score": <0-100>,
    "audience_reach_score": <0-100>,
    "timeline_realism_score": <0-100>,
    "analysis": "<detailed analysis text>",
    "recommendations": [
        {{"type": "budget|platform|audience|timeline", "priority": "high|medium|low", "message": "<recommendation>"}},
    ],
    "suggested_adjustments": {{
        "budget": <suggested monthly budget or null>,
        "platforms": [<suggested platforms or null>],
        "timeline_months": <suggested timeline or null>
    }}
}}
"""
    
    try:
        # Try OpenAI first
        openai_key = os.environ.get("OPENAI_API_KEY")
        if openai_key:
            import httpx
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {openai_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "gpt-4o-mini",
                        "messages": [
                            {"role": "system", "content": "You are a digital marketing expert. Always respond with valid JSON."},
                            {"role": "user", "content": context}
                        ],
                        "temperature": 0.3,
                        "max_tokens": 1500
                    },
                    timeout=60.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    content = result["choices"][0]["message"]["content"]
                    # Parse JSON from response
                    try:
                        return json.loads(content)
                    except json.JSONDecodeError:
                        # Try to extract JSON from markdown code block
                        import re
                        json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
                        if json_match:
                            return json.loads(json_match.group(1))
                        raise
    except Exception as e:
        logger.error(f"AI analysis failed: {e}")
    
    # Fallback: Rule-based analysis
    min_budget = benchmarks.get("recommended_min_budget", 1000)
    budget = strategy.get("budget", 0)
    
    budget_score = min(100, int((budget / min_budget) * 100)) if min_budget > 0 else 50
    platform_score = 80 if strategy.get("platforms") else 40
    audience_score = 70 if strategy.get("target_audience") else 50
    timeline_score = 80 if strategy.get("timeline_months", 0) >= benchmarks.get("recommended_timeline_months", 3) else 60
    
    feasibility = int((budget_score + platform_score + audience_score + timeline_score) / 4)
    
    return {
        "feasibility_score": feasibility,
        "budget_adequacy_score": budget_score,
        "platform_fit_score": platform_score,
        "audience_reach_score": audience_score,
        "timeline_realism_score": timeline_score,
        "analysis": f"Based on industry benchmarks, your ${budget}/month budget {'meets' if budget >= min_budget else 'is below'} the recommended minimum of ${min_budget} for {strategy['goal']} campaigns.",
        "recommendations": [
            {"type": "budget", "priority": "high" if budget < min_budget else "low", 
             "message": f"Consider increasing budget to at least ${min_budget}/month" if budget < min_budget else "Budget is adequate for your goals"}
        ],
        "suggested_adjustments": {
            "budget": min_budget if budget < min_budget else None,
            "platforms": None,
            "timeline_months": None
        }
    }


@activity.defn
async def save_validation_result(
    tenant_id: str,
    user_id: str,
    strategy: Dict[str, Any],
    analysis: Dict[str, Any],
    iteration: int = 1,
    previous_id: str = None
) -> str:
    """
    Save the validation result to the database.
    Returns the validation ID.
    """
    from app.dependencies import get_db
    from app.models.strategy_validation import StrategyValidation, ValidationStatus
    import uuid
    
    db = next(get_db())
    try:
        validation = StrategyValidation(
            tenant_id=tenant_id,
            user_id=user_id,
            proposed_goal=strategy.get("goal"),
            proposed_budget=strategy.get("budget", 0),
            proposed_currency=strategy.get("currency", "USD"),
            proposed_platforms=strategy.get("platforms", []),
            target_audience=strategy.get("target_audience", {}),
            timeline_months=strategy.get("timeline_months", 3),
            status=ValidationStatus.NEEDS_REFINEMENT.value if analysis.get("feasibility_score", 0) < 60 else ValidationStatus.APPROVED.value,
            feasibility_score=analysis.get("feasibility_score"),
            budget_adequacy_score=analysis.get("budget_adequacy_score"),
            platform_fit_score=analysis.get("platform_fit_score"),
            audience_reach_score=analysis.get("audience_reach_score"),
            timeline_realism_score=analysis.get("timeline_realism_score"),
            ai_analysis=analysis.get("analysis"),
            recommendations=analysis.get("recommendations", []),
            suggested_adjustments=analysis.get("suggested_adjustments", {}),
            iteration_number=iteration,
            previous_validation_id=uuid.UUID(previous_id) if previous_id else None
        )
        
        db.add(validation)
        db.commit()
        db.refresh(validation)
        
        return str(validation.id)
    finally:
        db.close()


# --- Workflow ---

@workflow.defn
class StrategyValidationWorkflow:
    """
    Validates a campaign strategy using AI analysis.
    
    Input:
        - tenant_id: Client tenant identifier
        - user_id: User requesting validation
        - strategy: Proposed strategy details
        - iteration: Current iteration number (for loops)
        - previous_id: Previous validation ID if refining
    
    Output:
        - validation_id: ID of the saved validation
        - is_feasible: Whether strategy meets minimum threshold
        - analysis: AI analysis results
    """
    
    @workflow.run
    async def run(
        self,
        tenant_id: str,
        user_id: str,
        strategy: Dict[str, Any],
        iteration: int = 1,
        previous_id: str = None
    ) -> Dict[str, Any]:
        
        # 1. Fetch insights from connected platforms
        connector_insights = await workflow.execute_activity(
            fetch_connector_insights,
            args=[tenant_id, strategy.get("platforms", [])],
            start_to_close_timeout=timedelta(seconds=30)
        )
        
        # 2. Get industry benchmarks
        benchmarks = await workflow.execute_activity(
            get_industry_benchmarks,
            args=[strategy.get("industry", "general"), strategy.get("goal", "lead_gen")],
            start_to_close_timeout=timedelta(seconds=10)
        )
        
        # 3. AI Analysis
        analysis = await workflow.execute_activity(
            analyze_strategy_with_ai,
            args=[strategy, connector_insights, benchmarks],
            start_to_close_timeout=timedelta(seconds=90)
        )
        
        # 4. Save results
        validation_id = await workflow.execute_activity(
            save_validation_result,
            args=[tenant_id, user_id, strategy, analysis, iteration, previous_id],
            start_to_close_timeout=timedelta(seconds=10)
        )
        
        return {
            "validation_id": validation_id,
            "is_feasible": analysis.get("feasibility_score", 0) >= 60,
            "feasibility_score": analysis.get("feasibility_score"),
            "analysis": analysis.get("analysis"),
            "recommendations": analysis.get("recommendations", []),
            "suggested_adjustments": analysis.get("suggested_adjustments", {})
        }
