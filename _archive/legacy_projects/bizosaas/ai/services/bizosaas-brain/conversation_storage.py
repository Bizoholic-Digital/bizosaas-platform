#!/usr/bin/env python3
"""
Conversation Storage Layer - PostgreSQL Database Integration
Handles persistent storage of conversation sessions, messages, and context for the conversational AI interface.
"""

from sqlalchemy import create_engine, Column, String, DateTime, Integer, Text, JSON, Boolean, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from datetime import datetime
from typing import Dict, Any, List, Optional
import uuid
import json
import asyncio
import asyncpg
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from contextlib import asynccontextmanager
import logging
from vault_client import get_vault_client

logger = logging.getLogger(__name__)

Base = declarative_base()

class ConversationSession(Base):
    """
    Conversation session model - represents a chat session with context and metadata
    """
    __tablename__ = 'conversation_sessions'
    
    id = Column(String, primary_key=True, default=lambda: f"session_{uuid.uuid4().hex}")
    tenant_id = Column(String, nullable=False, index=True)
    user_id = Column(String, nullable=False, index=True)
    title = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    message_count = Column(Integer, default=0)
    status = Column(String, default='active')  # active, completed, archived
    tags = Column(ARRAY(String), default=list)
    summary = Column(Text)
    
    # JSON context field for conversation state
    context = Column(JSON, default=dict)
    
    # Relationships
    messages = relationship("ConversationMessage", back_populates="session", cascade="all, delete-orphan")
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_session_tenant_user', 'tenant_id', 'user_id'),
        Index('idx_session_status', 'status'),
        Index('idx_session_updated', 'updated_at'),
    )

class ConversationMessage(Base):
    """
    Individual conversation message model with metadata and context
    """
    __tablename__ = 'conversation_messages'
    
    id = Column(String, primary_key=True, default=lambda: f"msg_{uuid.uuid4().hex}")
    session_id = Column(String, ForeignKey('conversation_sessions.id'), nullable=False, index=True)
    type = Column(String, nullable=False)  # user, ai, system, action_result
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # JSON metadata field for additional context
    msg_metadata = Column(JSON, default=dict)
    
    # Relationships
    session = relationship("ConversationSession", back_populates="messages")
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_message_session', 'session_id'),
        Index('idx_message_type', 'type'),
        Index('idx_message_timestamp', 'timestamp'),
        Index('idx_message_content_search', 'content'),  # For text search
    )

class ConversationDatabaseManager:
    """
    Async database manager for conversation persistence
    """
    
    def __init__(self):
        self.engine = None
        self.async_session_maker = None
        self._initialized = False
    
    async def initialize(self):
        """Initialize database connection and create tables"""
        if self._initialized:
            return
            
        try:
            # Get database config from Vault
            vault_client = get_vault_client()
            db_config = vault_client.get_database_config()
            
            # Create async engine
            database_url = f"postgresql+asyncpg://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
            
            self.engine = create_async_engine(
                database_url,
                echo=False,  # Set to True for SQL debugging
                pool_size=5,
                max_overflow=10,
                pool_pre_ping=True
            )
            
            # Create session maker
            self.async_session_maker = async_sessionmaker(
                self.engine,
                class_=AsyncSession,
                expire_on_commit=False
            )
            
            # Create tables
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            
            self._initialized = True
            logger.info("Conversation database initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize conversation database: {e}")
            # Fallback to in-memory storage (for development)
            self._initialized = False
            raise
    
    @asynccontextmanager
    async def get_session(self):
        """Get async database session"""
        if not self._initialized:
            await self.initialize()
            
        async with self.async_session_maker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
    
    async def create_session(self, tenant_id: str, user_id: str, title: str = None) -> Dict[str, Any]:
        """Create new conversation session"""
        if not title:
            title = f"Conversation {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            
        session_data = ConversationSession(
            tenant_id=tenant_id,
            user_id=user_id,
            title=title,
            context={
                'tenant_id': tenant_id,
                'user_role': 'user',
                'user_preferences': {},
                'recent_actions': [],
                'active_workflows': [],
                'mentioned_entities': {},
                'current_focus': 'general',
                'session_goals': [],
                'conversation_mode': 'general',
                'last_dashboard_tab': 'ai-command',
                'frequently_asked': [],
                'context_thread': []
            }
        )
        
        async with self.get_session() as db_session:
            db_session.add(session_data)
            await db_session.commit()
            await db_session.refresh(session_data)
            
        return self._session_to_dict(session_data)
    
    async def get_session_by_id(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get conversation session by ID"""
        async with self.get_session() as db_session:
            result = await db_session.get(ConversationSession, session_id)
            return self._session_to_dict(result) if result else None
    
    async def get_user_sessions(self, tenant_id: str, user_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get conversation sessions for a user"""
        from sqlalchemy import select
        
        async with self.get_session() as db_session:
            query = (
                select(ConversationSession)
                .where(ConversationSession.tenant_id == tenant_id)
                .where(ConversationSession.user_id == user_id)
                .order_by(ConversationSession.updated_at.desc())
                .limit(limit)
            )
            
            result = await db_session.execute(query)
            sessions = result.scalars().all()
            
        return [self._session_to_dict(session) for session in sessions]
    
    async def add_message(self, session_id: str, message_type: str, content: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Add message to conversation session"""
        message_data = ConversationMessage(
            session_id=session_id,
            type=message_type,
            content=content,
            msg_metadata=metadata or {}
        )
        
        async with self.get_session() as db_session:
            # Add message
            db_session.add(message_data)
            
            # Update session message count and timestamp
            session = await db_session.get(ConversationSession, session_id)
            if session:
                session.message_count = session.message_count + 1
                session.updated_at = datetime.utcnow()
            
            await db_session.commit()
            await db_session.refresh(message_data)
            
        return self._message_to_dict(message_data)
    
    async def get_session_messages(self, session_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get messages for a conversation session"""
        from sqlalchemy import select
        
        async with self.get_session() as db_session:
            query = (
                select(ConversationMessage)
                .where(ConversationMessage.session_id == session_id)
                .order_by(ConversationMessage.timestamp.asc())
                .limit(limit)
            )
            
            result = await db_session.execute(query)
            messages = result.scalars().all()
            
        return [self._message_to_dict(message) for message in messages]
    
    async def search_conversations(self, tenant_id: str, user_id: str, query: str, session_id: str = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Search conversation messages"""
        from sqlalchemy import select, and_, or_
        
        async with self.get_session() as db_session:
            # Build search query
            search_query = select(ConversationMessage).join(ConversationSession)
            
            # Filter by tenant and user
            search_query = search_query.where(
                and_(
                    ConversationSession.tenant_id == tenant_id,
                    ConversationSession.user_id == user_id
                )
            )
            
            # Filter by session if specified
            if session_id:
                search_query = search_query.where(ConversationMessage.session_id == session_id)
            
            # Text search in content
            search_query = search_query.where(
                ConversationMessage.content.ilike(f'%{query}%')
            )
            
            # Order by timestamp descending
            search_query = search_query.order_by(ConversationMessage.timestamp.desc()).limit(limit)
            
            result = await db_session.execute(search_query)
            messages = result.scalars().all()
            
        return [self._message_to_dict(message) for message in messages]
    
    async def update_session_context(self, session_id: str, context_updates: Dict[str, Any]) -> bool:
        """Update conversation session context"""
        async with self.get_session() as db_session:
            session = await db_session.get(ConversationSession, session_id)
            if not session:
                return False
                
            # Merge context updates
            current_context = session.context or {}
            updated_context = {**current_context, **context_updates}
            session.context = updated_context
            session.updated_at = datetime.utcnow()
            
            await db_session.commit()
            return True
    
    async def archive_session(self, session_id: str) -> bool:
        """Archive conversation session"""
        async with self.get_session() as db_session:
            session = await db_session.get(ConversationSession, session_id)
            if not session:
                return False
                
            session.status = 'archived'
            session.updated_at = datetime.utcnow()
            
            await db_session.commit()
            return True
    
    def _session_to_dict(self, session: ConversationSession) -> Dict[str, Any]:
        """Convert session model to dictionary"""
        return {
            'id': session.id,
            'tenant_id': session.tenant_id,
            'user_id': session.user_id,
            'title': session.title,
            'created_at': session.created_at.isoformat(),
            'updated_at': session.updated_at.isoformat(),
            'message_count': session.message_count,
            'status': session.status,
            'tags': session.tags or [],
            'summary': session.summary,
            'context': session.context or {}
        }
    
    def _message_to_dict(self, message: ConversationMessage) -> Dict[str, Any]:
        """Convert message model to dictionary"""
        return {
            'id': message.id,
            'session_id': message.session_id,
            'type': message.type,
            'content': message.content,
            'timestamp': message.timestamp.isoformat(),
            'metadata': message.msg_metadata or {}
        }

# Global database manager instance
conversation_db = ConversationDatabaseManager()

async def get_conversation_db() -> ConversationDatabaseManager:
    """Get conversation database manager instance"""
    if not conversation_db._initialized:
        await conversation_db.initialize()
    return conversation_db

# Health check function
async def check_conversation_db_health() -> Dict[str, Any]:
    """Check conversation database health"""
    try:
        async with conversation_db.get_session() as session:
            # Simple query to check connection
            from sqlalchemy import text
            result = await session.execute(text("SELECT 1"))
            result.fetchone()
            
        return {
            "status": "healthy",
            "initialized": conversation_db._initialized,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "initialized": conversation_db._initialized,
            "timestamp": datetime.utcnow().isoformat()
        }