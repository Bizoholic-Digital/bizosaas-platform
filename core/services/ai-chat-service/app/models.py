"""
Data models for AI Chat Service
"""

from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from enum import Enum
from pydantic import BaseModel, Field
import uuid

class MessageType(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    AGENT = "agent"
    ERROR = "error"

class UserRole(str, Enum):
    SUPER_ADMIN = "super_admin"
    TENANT_ADMIN = "tenant_admin"
    USER = "user"
    READONLY = "readonly"
    AGENT = "agent"

class ConversationContext(BaseModel):
    """Context information for conversation"""
    tenant_id: str
    user_role: UserRole
    dashboard_context: Optional[Dict[str, Any]] = None
    current_page: Optional[str] = None
    recent_actions: List[str] = []
    preferences: Dict[str, Any] = {}

class ChatMessage(BaseModel):
    """Individual chat message"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: MessageType
    content: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    user_id: Optional[str] = None
    session_id: str
    metadata: Optional[Dict[str, Any]] = None
    agent_name: Optional[str] = None
    confidence: Optional[float] = None
    suggested_actions: List[str] = []

class ChatSession(BaseModel):
    """Chat session with conversation history"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    tenant_id: str
    role: UserRole
    messages: List[ChatMessage] = []
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_activity: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    context: ConversationContext
    agent_preferences: Dict[str, Any] = {}
    is_active: bool = True

class AgentCapability(BaseModel):
    """AI Agent capability definition"""
    name: str
    description: str
    keywords: List[str]
    confidence_threshold: float = 0.7
    requires_data_access: bool = False

class AIAssistant(BaseModel):
    """AI Assistant configuration for a role"""
    name: str
    description: str
    role: UserRole
    avatar: Optional[str] = None
    capabilities: List[AgentCapability]
    available_agents: List[str]
    default_agent: str
    greeting_message: str
    context_limits: Dict[str, int] = {}

class AgentRequest(BaseModel):
    """Request to CrewAI agent"""
    agent_name: str
    query: str
    context: ConversationContext
    message_history: List[Dict[str, Any]] = []
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None

class AgentResponse(BaseModel):
    """Response from CrewAI agent"""
    agent_name: str
    response: str
    confidence: float = 0.0
    suggested_actions: List[str] = []
    metadata: Dict[str, Any] = {}
    processing_time: Optional[float] = None
    tokens_used: Optional[int] = None

class ChatRequest(BaseModel):
    """Client chat request"""
    message: str
    session_id: Optional[str] = None
    agent_name: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    file_attachments: List[str] = []

class ChatResponse(BaseModel):
    """Chat API response"""
    session_id: str
    user_message: ChatMessage
    ai_response: ChatMessage
    conversation_length: int
    suggested_actions: List[str] = []
    context_updated: bool = False

class SessionStats(BaseModel):
    """Session statistics"""
    total_messages: int
    user_messages: int
    assistant_messages: int
    average_response_time: float
    agents_used: Dict[str, int]
    session_duration: int  # seconds
    
class ServiceHealth(BaseModel):
    """Service health status"""
    status: str
    timestamp: datetime
    crew_ai_status: str
    auth_service_status: str
    active_sessions: int
    total_conversations: int
    average_response_time: float
    error_rate: float

class WebSocketMessage(BaseModel):
    """WebSocket message format"""
    type: str  # message, typing, error, system
    content: str
    session_id: str
    user_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Optional[Dict[str, Any]] = None

class FileAttachment(BaseModel):
    """File attachment for chat"""
    filename: str
    content_type: str
    size: int
    url: str
    processed: bool = False
    extracted_text: Optional[str] = None
    metadata: Dict[str, Any] = {}

class ConversationSummary(BaseModel):
    """Conversation summary for context"""
    session_id: str
    summary: str
    key_topics: List[str]
    action_items: List[str]
    sentiment: str
    created_at: datetime