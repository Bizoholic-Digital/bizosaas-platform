"""
Claude Context Manager for BizoSaaS
Manages context storage and retrieval using PostgreSQL with pgvector
"""

import asyncio
import json
import logging
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import asyncpg
import openai
from openai import OpenAI
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ClaudeContextManager:
    def __init__(self):
        self.db_config = {
            'host': os.getenv('POSTGRES_HOST', 'shared-postgres'),
            'port': int(os.getenv('POSTGRES_PORT', '5432')),
            'database': os.getenv('POSTGRES_DB', 'postgres'),
            'user': os.getenv('POSTGRES_USER', 'postgres'),
            'password': os.getenv('POSTGRES_PASSWORD', 'SharedInfra2024!SuperSecure')
        }
        
        # OpenRouter client for embeddings
        self.openai_client = OpenAI(
            api_key=os.getenv('OPENAI_API_KEY', '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'),
            base_url="https://openrouter.ai/api/v1"
        )
        
        self.pool = None
    
    async def initialize(self):
        """Initialize database connection pool"""
        try:
            self.pool = await asyncpg.create_pool(**self.db_config)
            logger.info("Database connection pool initialized")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    async def close(self):
        """Close database connections"""
        if self.pool:
            await self.pool.close()
    
    def generate_context_id(self, content: str, project: str = "bizosaas") -> str:
        """Generate unique context ID from content"""
        hash_input = f"{project}:{content[:100]}:{datetime.now().isoformat()[:10]}"
        return hashlib.md5(hash_input.encode()).hexdigest()[:16]
    
    async def get_embedding(self, text: str) -> List[float]:
        """Generate embedding for text using OpenRouter"""
        try:
            response = self.openai_client.embeddings.create(
                model="text-embedding-3-small",
                input=text[:8000]  # Limit input length
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}")
            # Return zero vector as fallback
            return [0.0] * 1536
    
    async def store_context(
        self,
        content: str,
        title: str,
        project_name: str = "bizosaas",
        context_type: str = "workflow",
        metadata: Optional[Dict] = None,
        tags: Optional[List[str]] = None,
        expires_hours: Optional[int] = None,
        context_id: Optional[str] = None
    ) -> str:
        """Store context with automatic embedding generation"""
        
        if not self.pool:
            await self.initialize()
        
        # Generate context ID if not provided
        if not context_id:
            context_id = self.generate_context_id(content, project_name)
        
        # Generate embedding
        embedding = await self.get_embedding(f"{title}\n{content}")
        
        # Prepare data
        metadata = metadata or {}
        tags = tags or []
        
        try:
            async with self.pool.acquire() as conn:
                # Store context using the database function
                result = await conn.fetchval(
                    """
                    SELECT store_bizosaas_context($1, $2, $3, $4, $5, $6, $7, $8)
                    """,
                    context_id, project_name, context_type, title, content,
                    json.dumps(metadata), tags, expires_hours
                )
                
                # Update embedding separately (since function doesn't handle vectors well)
                await conn.execute(
                    """
                    UPDATE claude_context_store 
                    SET embedding = $1::vector, updated_at = CURRENT_TIMESTAMP
                    WHERE context_id = $2
                    """,
                    str(embedding), context_id
                )
                
                logger.info(f"Stored context {context_id} for project {project_name}")
                return context_id
                
        except Exception as e:
            logger.error(f"Failed to store context: {e}")
            raise
    
    async def search_context(
        self,
        query: str,
        project_name: Optional[str] = None,
        context_type: Optional[str] = None,
        limit: int = 5,
        similarity_threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """Search for similar contexts using semantic similarity"""
        
        if not self.pool:
            await self.initialize()
        
        # Generate query embedding
        query_embedding = await self.get_embedding(query)
        
        try:
            async with self.pool.acquire() as conn:
                # Use the search function
                rows = await conn.fetch(
                    """
                    SELECT * FROM search_claude_context($1::vector, $2, $3, $4, $5)
                    """,
                    str(query_embedding), project_name, context_type, limit, similarity_threshold
                )
                
                # Convert to list of dicts
                results = []
                for row in rows:
                    results.append({
                        'context_id': row['context_id'],
                        'project_name': row['project_name'],
                        'context_type': row['context_type'],
                        'title': row['title'],
                        'content': row['content'],
                        'similarity_score': float(row['similarity_score']),
                        'metadata': row['metadata'],
                        'created_at': row['created_at'].isoformat()
                    })
                
                logger.info(f"Found {len(results)} similar contexts for query: {query[:50]}...")
                return results
                
        except Exception as e:
            logger.error(f"Failed to search contexts: {e}")
            return []
    
    async def get_project_memory(
        self,
        project_name: str = "bizosaas",
        query_text: str = "",
        max_results: int = 10
    ) -> List[Dict[str, Any]]:
        """Get project-specific memory contexts"""
        
        if not self.pool:
            await self.initialize()
        
        try:
            async with self.pool.acquire() as conn:
                result = await conn.fetchval(
                    """
                    SELECT get_claude_memory_for_project($1, $2, $3)
                    """,
                    project_name, query_text, max_results
                )
                
                return json.loads(result) if result else []
                
        except Exception as e:
            logger.error(f"Failed to get project memory: {e}")
            return []
    
    async def store_workflow_execution(
        self,
        workflow_name: str,
        execution_data: Dict[str, Any],
        status: str = "completed",
        project_name: str = "bizosaas"
    ) -> str:
        """Store n8n workflow execution context"""
        
        title = f"Workflow Execution: {workflow_name}"
        content = f"""
Workflow: {workflow_name}
Status: {status}
Execution Time: {datetime.now().isoformat()}

Execution Data:
{json.dumps(execution_data, indent=2)}
"""
        
        metadata = {
            "workflow_name": workflow_name,
            "status": status,
            "execution_timestamp": datetime.now().isoformat(),
            "project": project_name
        }
        
        tags = ["workflow", "n8n", workflow_name, status]
        
        return await self.store_context(
            content=content,
            title=title,
            project_name=project_name,
            context_type="workflow_execution",
            metadata=metadata,
            tags=tags,
            expires_hours=168  # Keep for 1 week
        )
    
    async def store_agent_interaction(
        self,
        agent_name: str,
        interaction_data: Dict[str, Any],
        project_name: str = "bizosaas"
    ) -> str:
        """Store CrewAI agent interaction context"""
        
        title = f"Agent Interaction: {agent_name}"
        content = f"""
Agent: {agent_name}
Timestamp: {datetime.now().isoformat()}

Interaction:
{json.dumps(interaction_data, indent=2)}
"""
        
        metadata = {
            "agent_name": agent_name,
            "interaction_timestamp": datetime.now().isoformat(),
            "project": project_name
        }
        
        tags = ["agent", "crewai", agent_name]
        
        return await self.store_context(
            content=content,
            title=title,
            project_name=project_name,
            context_type="agent_interaction",
            metadata=metadata,
            tags=tags,
            expires_hours=72  # Keep for 3 days
        )
    
    async def store_deployment_event(
        self,
        event_type: str,
        event_data: Dict[str, Any],
        project_name: str = "bizosaas"
    ) -> str:
        """Store deployment/configuration events"""
        
        title = f"Deployment Event: {event_type}"
        content = f"""
Event: {event_type}
Timestamp: {datetime.now().isoformat()}

Event Data:
{json.dumps(event_data, indent=2)}
"""
        
        metadata = {
            "event_type": event_type,
            "timestamp": datetime.now().isoformat(),
            "project": project_name
        }
        
        tags = ["deployment", "configuration", event_type]
        
        return await self.store_context(
            content=content,
            title=title,
            project_name=project_name,
            context_type="deployment",
            metadata=metadata,
            tags=tags
        )
    
    async def cleanup_expired_contexts(self) -> int:
        """Clean up expired contexts"""
        
        if not self.pool:
            await self.initialize()
        
        try:
            async with self.pool.acquire() as conn:
                deleted_count = await conn.fetchval(
                    "SELECT cleanup_expired_contexts()"
                )
                
                logger.info(f"Cleaned up {deleted_count} expired contexts")
                return deleted_count
                
        except Exception as e:
            logger.error(f"Failed to cleanup contexts: {e}")
            return 0

# Global instance
context_manager = ClaudeContextManager()

# API functions for easy access
async def store_context(content: str, title: str, **kwargs) -> str:
    """Store context - convenience function"""
    return await context_manager.store_context(content, title, **kwargs)

async def search_context(query: str, **kwargs) -> List[Dict[str, Any]]:
    """Search context - convenience function"""  
    return await context_manager.search_context(query, **kwargs)

async def get_project_memory(project_name: str = "bizosaas", query: str = "") -> List[Dict[str, Any]]:
    """Get project memory - convenience function"""
    return await context_manager.get_project_memory(project_name, query)