import asyncio
import json
import os
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from app.core.rag import rag_service
from app.core.vault import get_config_val

async def seed_mock_patterns():
    print("Seeding mock agent results for fine-tuning verification...")
    
    # Use real RAG service to ingest
    # We'll mock the effectiveness_score in metadata
    
    test_data = [
        {
            "content": "A high-quality 3-month marketing strategy for SaaS in the fintech space.",
            "metadata": {
                "source": "agent_result",
                "task": "Develop a fintech SaaS strategy",
                "effectiveness_score": 0.95
            },
            "agent_id": "marketing_strategist"
        },
        {
            "content": "A meta title and description for a shoe store.",
            "metadata": {
                "source": "agent_result",
                "task": "Generate meta tags",
                "effectiveness_score": 0.85
            },
            "agent_id": "seo_specialist"
        },
        {
            "content": "Low quality output that should be ignored.",
            "metadata": {
                "source": "agent_result",
                "task": "Poorly defined task",
                "effectiveness_score": 0.3
            },
            "agent_id": "content_creator"
        }
    ]
    
    for entry in test_data:
        doc_id = await rag_service.ingest_knowledge(
            content=entry["content"],
            metadata=entry["metadata"],
            tenant_id="test_tenant",
            agent_id=entry["agent_id"]
        )
        print(f"Ingested ID: {doc_id} for {entry['agent_id']}")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(seed_mock_patterns())
