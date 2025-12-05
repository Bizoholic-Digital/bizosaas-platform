"""
Personal AI Assistant Service for BizOSaaS Platform
Leverages existing 88 AI agents for personal productivity, eldercare, and business assistance
"""

import os
import asyncio
import json
import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timezone, timedelta
from enum import Enum
from uuid import uuid4
import uuid

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import httpx
import redis.asyncio as redis
from sqlalchemy import create_engine, Column, String, Text, DateTime, Boolean, Integer, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
import speech_recognition as sr
from pydub import AudioSegment
import openai
import numpy as np

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:admin@localhost:5432/bizosaas_ai")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Redis setup
redis_client = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))

# OpenAI setup
openai.api_key = os.getenv("OPENAI_API_KEY")

logger = logging.getLogger(__name__)

# ========================================================================================
# ENUMS AND CONSTANTS
# ========================================================================================

class AssistantType(str, Enum):
    ELDERCARE = "eldercare"
    FOUNDER_PRODUCTIVITY = "founder_productivity"
    CLIENT_BUSINESS = "client_business"
    GENERAL = "general"

class MessagePriority(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"
    EMERGENCY = "emergency"

class ConversationStatus(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"

class ReminderType(str, Enum):
    MEDICATION = "medication"
    APPOINTMENT = "appointment"
    TASK = "task"
    HEALTH_CHECK = "health_check"
    EMERGENCY_CONTACT = "emergency_contact"

# ========================================================================================
# DATABASE MODELS
# ========================================================================================

class PersonalAssistantProfile(Base):
    __tablename__ = "personal_assistant_profiles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String(255), unique=True, nullable=False)
    telegram_user_id = Column(String(255), unique=True, nullable=False)
    telegram_username = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    
    # Assistant configuration
    assistant_type = Column(String(50), default=AssistantType.GENERAL)
    preferred_agents = Column(JSONB, default=list)
    personality_settings = Column(JSONB, default=dict)
    notification_preferences = Column(JSONB, default=dict)
    
    # ElderCare specific
    emergency_contacts = Column(JSONB, default=list)
    medical_conditions = Column(JSONB, default=list)
    medications = Column(JSONB, default=list)
    care_level = Column(String(50), default="independent")
    
    # Productivity settings
    work_schedule = Column(JSONB, default=dict)
    focus_times = Column(JSONB, default=list)
    productivity_goals = Column(JSONB, default=list)
    
    # Privacy and security
    data_retention_days = Column(Integer, default=30)
    encryption_enabled = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class ConversationSession(Base):
    __tablename__ = "conversation_sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(String(255), unique=True, nullable=False)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("personal_assistant_profiles.id"))
    telegram_chat_id = Column(String(255), nullable=False)
    
    # Session details
    status = Column(String(50), default=ConversationStatus.ACTIVE)
    context_summary = Column(Text)
    active_agents = Column(JSONB, default=list)
    conversation_goal = Column(String(500))
    
    # Timing
    started_at = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime)
    
    # Relationships
    profile = relationship("PersonalAssistantProfile", back_populates="conversations")

class ConversationMessage(Base):
    __tablename__ = "conversation_messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("conversation_sessions.id"))
    message_id = Column(String(255), unique=True, nullable=False)
    
    # Message content
    content = Column(Text, nullable=False)
    message_type = Column(String(50), nullable=False)  # user, agent, system
    sender_agent = Column(String(255))
    
    # Message metadata
    priority = Column(String(50), default=MessagePriority.NORMAL)
    sentiment_score = Column(String(50))
    intent_classification = Column(String(255))
    confidence_score = Column(String(50))
    
    # Voice message support
    is_voice_message = Column(Boolean, default=False)
    voice_file_path = Column(String(500))
    transcription = Column(Text)
    
    # Vector embedding for context search
    embedding = Column(String)  # Will store pgvector embedding
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    session = relationship("ConversationSession", back_populates="messages")

class PersonalReminder(Base):
    __tablename__ = "personal_reminders"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("personal_assistant_profiles.id"))
    
    # Reminder details
    title = Column(String(255), nullable=False)
    description = Column(Text)
    reminder_type = Column(String(50), nullable=False)
    priority = Column(String(50), default=MessagePriority.NORMAL)
    
    # Scheduling
    scheduled_at = Column(DateTime, nullable=False)
    repeat_pattern = Column(String(100))  # daily, weekly, monthly, custom
    repeat_until = Column(DateTime)
    
    # Completion tracking
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime)
    snooze_until = Column(DateTime)
    
    # Notification settings
    advance_notice_minutes = Column(Integer, default=15)
    notification_sent = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    profile = relationship("PersonalAssistantProfile", back_populates="reminders")

class ProductivityTask(Base):
    __tablename__ = "productivity_tasks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("personal_assistant_profiles.id"))
    
    # Task details
    title = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(String(100))
    priority = Column(String(50), default=MessagePriority.NORMAL)
    
    # Progress tracking
    status = Column(String(50), default="pending")  # pending, in_progress, completed, cancelled
    progress_percentage = Column(Integer, default=0)
    estimated_duration_minutes = Column(Integer)
    actual_duration_minutes = Column(Integer)
    
    # Scheduling
    due_date = Column(DateTime)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    
    # AI insights
    ai_suggestions = Column(JSONB, default=list)
    difficulty_score = Column(String(50))
    focus_time_required = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Add relationships
PersonalAssistantProfile.conversations = relationship("ConversationSession", back_populates="profile")
PersonalAssistantProfile.reminders = relationship("PersonalReminder", back_populates="profile")
ConversationSession.messages = relationship("ConversationMessage", back_populates="session")

# ========================================================================================
# PYDANTIC MODELS
# ========================================================================================

class ProfileCreate(BaseModel):
    telegram_user_id: str
    telegram_username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    assistant_type: AssistantType = AssistantType.GENERAL
    emergency_contacts: List[Dict[str, Any]] = Field(default_factory=list)
    medical_conditions: List[str] = Field(default_factory=list)
    medications: List[Dict[str, Any]] = Field(default_factory=list)

class ProfileResponse(BaseModel):
    id: str
    user_id: str
    telegram_user_id: str
    telegram_username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    assistant_type: str
    is_active: bool
    created_at: datetime

class MessageRequest(BaseModel):
    telegram_chat_id: str
    content: str
    is_voice_message: bool = False
    voice_file_path: Optional[str] = None
    priority: MessagePriority = MessagePriority.NORMAL

class MessageResponse(BaseModel):
    message_id: str
    response: str
    suggestions: List[str] = Field(default_factory=list)
    actions: List[Dict[str, Any]] = Field(default_factory=list)
    agent_used: Optional[str] = None
    confidence_score: Optional[float] = None

class ReminderCreate(BaseModel):
    title: str
    description: Optional[str] = None
    reminder_type: ReminderType
    scheduled_at: datetime
    repeat_pattern: Optional[str] = None
    advance_notice_minutes: int = 15
    priority: MessagePriority = MessagePriority.NORMAL

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    priority: MessagePriority = MessagePriority.NORMAL
    due_date: Optional[datetime] = None
    estimated_duration_minutes: Optional[int] = None

# ========================================================================================
# CORE ASSISTANT LOGIC
# ========================================================================================

class PersonalAIAssistant:
    """Core Personal AI Assistant using existing BizOSaaS agents"""
    
    def __init__(self):
        self.ai_agents_url = os.getenv("AI_AGENTS_URL", "http://localhost:4000")
        self.chat_api_url = os.getenv("CHAT_API_URL", "http://localhost:4001")
        
    async def process_message(self, profile: PersonalAssistantProfile, message: str, 
                            session_id: str, is_voice: bool = False) -> MessageResponse:
        """Process incoming message using appropriate agents"""
        
        try:
            # Determine intent and select appropriate agents
            intent_result = await self._classify_intent(message, profile.assistant_type)
            selected_agents = await self._select_agents(intent_result, profile.preferred_agents)
            
            # Create chat session if needed
            chat_session = await self._get_or_create_chat_session(session_id, profile)
            
            # Route message to Chat API
            chat_request = {
                "session_id": session_id,
                "message": message,
                "agent_name": selected_agents[0] if selected_agents else "customer_support",
                "platform": "telegram",
                "context": {
                    "assistant_type": profile.assistant_type,
                    "user_preferences": profile.personality_settings,
                    "emergency_contacts": profile.emergency_contacts if profile.assistant_type == AssistantType.ELDERCARE else [],
                    "is_voice_message": is_voice
                }
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.chat_api_url}/chat/message",
                    json=chat_request,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    chat_response = response.json()
                    
                    # Enhance response based on assistant type
                    enhanced_response = await self._enhance_response(
                        chat_response, profile.assistant_type, intent_result
                    )
                    
                    return MessageResponse(
                        message_id=enhanced_response["message_id"],
                        response=enhanced_response["response"],
                        suggestions=enhanced_response.get("suggestions", []),
                        actions=enhanced_response.get("actions", []),
                        agent_used=enhanced_response.get("agent_name"),
                        confidence_score=enhanced_response.get("confidence_score")
                    )
                else:
                    logger.error(f"Chat API error: {response.text}")
                    return await self._fallback_response(message, profile.assistant_type)
                    
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return await self._fallback_response(message, profile.assistant_type)
    
    async def _classify_intent(self, message: str, assistant_type: AssistantType) -> Dict[str, Any]:
        """Classify message intent based on assistant type"""
        
        # Define intent patterns for different assistant types
        eldercare_intents = {
            "medication_reminder": ["medicine", "medication", "pills", "take", "dose"],
            "health_concern": ["pain", "sick", "doctor", "health", "feeling"],
            "emergency": ["help", "emergency", "urgent", "call", "ambulance"],
            "appointment": ["appointment", "doctor", "visit", "schedule"],
            "daily_check": ["how are you", "feeling", "today", "morning", "evening"]
        }
        
        productivity_intents = {
            "task_management": ["task", "todo", "deadline", "project", "work"],
            "schedule": ["meeting", "calendar", "schedule", "time", "appointment"],
            "focus_mode": ["focus", "concentrate", "deep work", "distraction"],
            "goal_tracking": ["goal", "progress", "achievement", "target"],
            "time_management": ["time", "productive", "efficiency", "manage"]
        }
        
        business_intents = {
            "client_management": ["client", "customer", "lead", "prospect"],
            "marketing": ["marketing", "campaign", "promotion", "ads"],
            "analytics": ["analytics", "metrics", "performance", "data"],
            "sales": ["sales", "revenue", "profit", "conversion"]
        }
        
        message_lower = message.lower()
        intent_scores = {}
        
        # Select appropriate intent patterns
        if assistant_type == AssistantType.ELDERCARE:
            intent_patterns = eldercare_intents
        elif assistant_type == AssistantType.FOUNDER_PRODUCTIVITY:
            intent_patterns = productivity_intents
        elif assistant_type == AssistantType.CLIENT_BUSINESS:
            intent_patterns = business_intents
        else:
            intent_patterns = {**eldercare_intents, **productivity_intents, **business_intents}
        
        # Calculate intent scores
        for intent, keywords in intent_patterns.items():
            score = sum(1 for keyword in keywords if keyword in message_lower)
            if score > 0:
                intent_scores[intent] = score / len(keywords)
        
        # Return best intent or default
        if intent_scores:
            best_intent = max(intent_scores.items(), key=lambda x: x[1])
            return {
                "intent": best_intent[0],
                "confidence": best_intent[1],
                "all_scores": intent_scores
            }
        else:
            return {
                "intent": "general_conversation",
                "confidence": 0.5,
                "all_scores": {}
            }
    
    async def _select_agents(self, intent_result: Dict[str, Any], 
                           preferred_agents: List[str]) -> List[str]:
        """Select appropriate agents based on intent"""
        
        intent_to_agents = {
            # ElderCare intents
            "medication_reminder": ["customer_support", "process_automation"],
            "health_concern": ["customer_support", "digital_audit"],
            "emergency": ["customer_support", "incident_management"],
            "appointment": ["customer_support", "process_automation"],
            "daily_check": ["customer_support"],
            
            # Productivity intents
            "task_management": ["process_automation", "customer_support"],
            "schedule": ["process_automation", "customer_support"],
            "focus_mode": ["process_automation", "performance_analytics"],
            "goal_tracking": ["performance_analytics", "roi_analysis"],
            "time_management": ["process_automation", "performance_analytics"],
            
            # Business intents
            "client_management": ["lead_scoring", "customer_segmentation", "sales_assistant"],
            "marketing": ["marketing_strategist", "content_creator", "seo_specialist"],
            "analytics": ["performance_analytics", "digital_audit", "roi_analysis"],
            "sales": ["sales_assistant", "lead_scoring", "roi_analysis"],
            
            # Default
            "general_conversation": ["customer_support"]
        }
        
        intent = intent_result.get("intent", "general_conversation")
        suggested_agents = intent_to_agents.get(intent, ["customer_support"])
        
        # Merge with preferred agents
        if preferred_agents:
            suggested_agents = list(set(preferred_agents + suggested_agents))
        
        return suggested_agents[:3]  # Limit to 3 agents max
    
    async def _enhance_response(self, chat_response: Dict[str, Any], 
                              assistant_type: AssistantType, 
                              intent_result: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance response based on assistant type"""
        
        enhanced_response = chat_response.copy()
        
        # Add assistant-specific enhancements
        if assistant_type == AssistantType.ELDERCARE:
            enhanced_response = await self._add_eldercare_enhancements(enhanced_response, intent_result)
        elif assistant_type == AssistantType.FOUNDER_PRODUCTIVITY:
            enhanced_response = await self._add_productivity_enhancements(enhanced_response, intent_result)
        elif assistant_type == AssistantType.CLIENT_BUSINESS:
            enhanced_response = await self._add_business_enhancements(enhanced_response, intent_result)
        
        return enhanced_response
    
    async def _add_eldercare_enhancements(self, response: Dict[str, Any], 
                                        intent_result: Dict[str, Any]) -> Dict[str, Any]:
        """Add ElderCare specific enhancements"""
        
        intent = intent_result.get("intent")
        
        if intent == "emergency":
            response["priority"] = MessagePriority.EMERGENCY
            response["actions"] = response.get("actions", []) + [
                {"type": "emergency_contact", "text": "Contact Emergency Services"},
                {"type": "family_alert", "text": "Alert Family Members"}
            ]
        elif intent == "medication_reminder":
            response["suggestions"] = response.get("suggestions", []) + [
                "Set up medication reminders",
                "Review medication schedule",
                "Contact pharmacist"
            ]
        elif intent == "health_concern":
            response["suggestions"] = response.get("suggestions", []) + [
                "Schedule doctor appointment",
                "Log symptoms",
                "Contact healthcare provider"
            ]
        
        return response
    
    async def _add_productivity_enhancements(self, response: Dict[str, Any], 
                                           intent_result: Dict[str, Any]) -> Dict[str, Any]:
        """Add Founder Productivity enhancements"""
        
        intent = intent_result.get("intent")
        
        if intent == "task_management":
            response["actions"] = response.get("actions", []) + [
                {"type": "create_task", "text": "Create New Task"},
                {"type": "view_tasks", "text": "View All Tasks"},
                {"type": "priority_tasks", "text": "High Priority Tasks"}
            ]
        elif intent == "focus_mode":
            response["suggestions"] = response.get("suggestions", []) + [
                "Start focus session",
                "Block distractions",
                "Set deep work timer"
            ]
        elif intent == "goal_tracking":
            response["actions"] = response.get("actions", []) + [
                {"type": "view_goals", "text": "View Goals Progress"},
                {"type": "update_goal", "text": "Update Goal Status"}
            ]
        
        return response
    
    async def _add_business_enhancements(self, response: Dict[str, Any], 
                                       intent_result: Dict[str, Any]) -> Dict[str, Any]:
        """Add Client Business enhancements"""
        
        intent = intent_result.get("intent")
        
        if intent == "client_management":
            response["actions"] = response.get("actions", []) + [
                {"type": "view_clients", "text": "View Client Dashboard"},
                {"type": "add_client", "text": "Add New Client"},
                {"type": "client_analytics", "text": "Client Analytics"}
            ]
        elif intent == "marketing":
            response["suggestions"] = response.get("suggestions", []) + [
                "Create marketing campaign",
                "Analyze campaign performance",
                "Content creation ideas"
            ]
        
        return response
    
    async def _get_or_create_chat_session(self, session_id: str, 
                                        profile: PersonalAssistantProfile) -> Dict[str, Any]:
        """Get or create chat session with Chat API"""
        
        async with httpx.AsyncClient() as client:
            # Try to get existing session
            try:
                response = await client.get(
                    f"{self.chat_api_url}/chat/sessions/{session_id}",
                    timeout=10.0
                )
                if response.status_code == 200:
                    return response.json()
            except:
                pass
            
            # Create new session
            session_request = {
                "user_id": profile.user_id,
                "tenant_id": profile.user_id,  # Use user_id as tenant for personal assistant
                "platform": "telegram"
            }
            
            response = await client.post(
                f"{self.chat_api_url}/chat/sessions",
                params=session_request,
                timeout=10.0
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=500, detail="Failed to create chat session")
    
    async def _fallback_response(self, message: str, assistant_type: AssistantType) -> MessageResponse:
        """Provide fallback response when AI agents are unavailable"""
        
        fallback_responses = {
            AssistantType.ELDERCARE: "I'm here to help you. If this is an emergency, please call emergency services immediately. Otherwise, I'll do my best to assist you.",
            AssistantType.FOUNDER_PRODUCTIVITY: "I'm your productivity assistant. I can help you manage tasks, schedule, and achieve your goals. What would you like to work on?",
            AssistantType.CLIENT_BUSINESS: "I'm here to help with your business needs. I can assist with client management, marketing, and analytics. How can I help?",
            AssistantType.GENERAL: "I'm your personal AI assistant. I'm here to help with various tasks and questions. How can I assist you today?"
        }
        
        return MessageResponse(
            message_id=str(uuid4()),
            response=fallback_responses.get(assistant_type, fallback_responses[AssistantType.GENERAL]),
            suggestions=["Try rephrasing your question", "Ask for help", "Contact support"],
            agent_used="fallback"
        )

# ========================================================================================
# VOICE MESSAGE PROCESSING
# ========================================================================================

class VoiceProcessor:
    """Handle voice message transcription and processing"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        
    async def transcribe_voice_message(self, file_path: str) -> str:
        """Transcribe voice message to text"""
        try:
            # Convert to WAV if needed
            audio = AudioSegment.from_file(file_path)
            wav_path = file_path.replace('.ogg', '.wav')
            audio.export(wav_path, format="wav")
            
            # Transcribe using speech recognition
            with sr.AudioFile(wav_path) as source:
                audio_data = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio_data)
                
            return text
            
        except Exception as e:
            logger.error(f"Voice transcription failed: {e}")
            return "[Voice message - transcription failed]"

# ========================================================================================
# DATABASE UTILITIES
# ========================================================================================

def get_db():
    """Database dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Create database tables"""
    Base.metadata.create_all(bind=engine)

# Initialize voice processor
voice_processor = VoiceProcessor()
assistant = PersonalAIAssistant()

if __name__ == "__main__":
    create_tables()
    print("Personal AI Assistant Service initialized")