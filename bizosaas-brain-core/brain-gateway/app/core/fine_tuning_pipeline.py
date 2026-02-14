import os
import json
import logging
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from app.core.rag import rag_service
from app.connectors.registry import ConnectorRegistry
from app.core.vault import get_config_val

logger = logging.getLogger(__name__)

class FineTuningPipeline:
    """
    Continuous Learning Pipeline that exports high-quality RAG data 
    for LLM fine-tuning via Together AI.
    """
    
    def __init__(self):
        self.db_url = get_config_val("VECTOR_DB_URL") or get_config_val("DATABASE_URL")
        self.engine = sa.create_engine(self.db_url)
        self.Session = sessionmaker(bind=self.engine)
        self.base_model = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"

    async def export_training_corpus(self, min_effectiveness: float = 0.8, output_file: str = "training_data.jsonl") -> str:
        """
        Extract high-quality agent interactions from knowledge_chunks 
        and format them as JSONL for Together AI.
        """
        logger.info(f"Exporting training corpus with min_effectiveness >= {min_effectiveness}")
        
        training_data = []
        
        with self.Session() as session:
            try:
                # Query for agent results with high effectiveness
                # Also include analytics insights for grounding
                query = sa.text("""
                    SELECT content, metadata:text as metadata, agent_id, tenant_id
                    FROM (
                        SELECT content, metadata, agent_id, tenant_id
                        FROM knowledge_chunks
                        WHERE metadata->>'source' = 'agent_result'
                        AND (metadata->>'effectiveness_score')::float >= :min_effectiveness
                        
                        UNION ALL
                        
                        SELECT content, metadata, 'analytics_expert' as agent_id, tenant_id
                        FROM knowledge_chunks
                        WHERE metadata->>'source' = 'analytics_insight'
                    ) AS combined_data
                """)
                
                result = session.execute(query, {"min_effectiveness": min_effectiveness})
                
                for row in result:
                    content = row.content
                    meta = row.metadata
                    agent_id = row.agent_id
                    
                    # Reconstruct ChatML format
                    if meta.get("source") == "analytics_insight":
                        prompt = f"Analyze the following performance metric: {content}"
                        system_msg = "You are a specialized Analytics Expert AI. Your goal is to ground your recommendations in real-world performance data."
                    else:
                        prompt = meta.get("task", "Perform the following task")
                        system_msg = f"You are a helpful AI assistant specialized as a {agent_id}."
                        
                    chat_entry = {
                        "messages": [
                            {"role": "system", "content": system_msg},
                            {"role": "user", "content": prompt},
                            {"role": "assistant", "content": content}
                        ]
                    }
                    training_data.append(chat_entry)

                
                if not training_data:
                    logger.warning("No high-quality interactions found to export.")
                    return ""
                
                # Write to JSONL
                with open(output_file, "w") as f:
                    for entry in training_data:
                        f.write(json.dumps(entry) + "\n")
                
                logger.info(f"Exported {len(training_data)} entries to {output_file}")
                return os.path.abspath(output_file)
                
            except Exception as e:
                logger.error(f"Failed to export training corpus: {e}")
                return ""

    async def run_pipeline(self, tenant_id: str = "default"):
        """
        Execute the full pipeline: Export -> Upload -> Fine-tune
        """
        if not self.db_url:
            logger.error("DATABASE_URL not configured. Cannot run pipeline.")
            return None
            
        # 1. Export
        corpus_path = await self.export_training_corpus()
        if not corpus_path:
            return None
            
        # 2. Get Together AI Connector
        try:
            api_key = get_config_val("TOGETHER_AI_API_KEY")
            if not api_key:
                logger.error("Together AI API key not found in Vault")
                return None
                
            connector = ConnectorRegistry.create_connector(
                "together_ai", 
                tenant_id=tenant_id, 
                credentials={"api_key": api_key}
            )
            
            # 3. Upload
            logger.info("Uploading training corpus to Together AI...")
            upload_resp = await connector.upload_file(corpus_path)
            file_id = upload_resp.get("id")
            if not file_id:
                logger.error("Failed to get file ID from Together AI upload")
                return None
                
            # 4. Trigger Fine-tuning
            logger.info(f"Triggering fine-tuning job for file {file_id}")
            job_resp = await connector.create_fine_tune_job(
                training_file_id=file_id,
                model=self.base_model,
                n_epochs=3
            )
            
            job_id = job_resp.get("id")
            logger.info(f"Fine-tuning job started: {job_id}")
            return job_id
            
        except Exception as e:
            logger.error(f"Fine-tuning pipeline failed: {e}")
            return None

# Export the class 
__all__ = ["FineTuningPipeline"]

if __name__ == "__main__":
    # Allow running via CLI
    import sys
    pipeline = FineTuningPipeline()
    loop = asyncio.get_event_loop()
    if len(sys.argv) > 1 and sys.argv[1] == "--export-only":
        loop.run_until_complete(pipeline.export_training_corpus())
    else:
        loop.run_until_complete(pipeline.run_pipeline())

