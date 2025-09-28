"""
Enhanced chat processing with LangChain integration and conversation memory
"""

import asyncio
import json
import logging
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional, Tuple
from collections import defaultdict

from langchain.memory import ConversationBufferWindowMemory, ConversationSummaryBufferMemory
from langchain.schema import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain.llms.openai import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.runnable import RunnablePassthrough

from .models import (
    ChatMessage, ChatSession, MessageType, UserRole, 
    ConversationContext, AgentRequest, ConversationSummary
)
from .agents import crew_ai_integration, agent_selector, role_assistants

logger = logging.getLogger(__name__)

class ConversationMemoryManager:
    """Manages conversation memory and context for chat sessions"""
    
    def __init__(self):
        self.session_memories: Dict[str, ConversationBufferWindowMemory] = {}
        self.session_summaries: Dict[str, ConversationSummary] = {}
        self.context_store: Dict[str, Dict[str, Any]] = {}
        
    def get_memory(self, session_id: str, window_size: int = 10) -> ConversationBufferWindowMemory:
        """Get or create conversation memory for session"""
        if session_id not in self.session_memories:
            self.session_memories[session_id] = ConversationBufferWindowMemory(
                k=window_size,
                return_messages=True,
                memory_key="chat_history"
            )
        return self.session_memories[session_id]
    
    def add_message(self, session_id: str, message: ChatMessage):
        """Add message to conversation memory"""
        memory = self.get_memory(session_id)
        
        if message.type == MessageType.USER:
            memory.chat_memory.add_user_message(message.content)
        elif message.type == MessageType.ASSISTANT:
            memory.chat_memory.add_ai_message(message.content)
    
    def get_conversation_context(self, session_id: str) -> Dict[str, Any]:
        """Get conversation context for session"""
        memory = self.get_memory(session_id)
        
        return {
            "chat_history": memory.chat_memory.messages,
            "message_count": len(memory.chat_memory.messages),
            "context": self.context_store.get(session_id, {}),
            "summary": self.session_summaries.get(session_id)
        }
    
    def update_context(self, session_id: str, context_updates: Dict[str, Any]):
        """Update session context"""
        if session_id not in self.context_store:
            self.context_store[session_id] = {}
        
        self.context_store[session_id].update(context_updates)
    
    def clear_session(self, session_id: str):
        """Clear session memory and context"""
        if session_id in self.session_memories:
            del self.session_memories[session_id]
        if session_id in self.session_summaries:
            del self.session_summaries[session_id]
        if session_id in self.context_store:
            del self.context_store[session_id]

class EnhancedChatProcessor:
    """Enhanced chat processor with LangChain integration"""
    
    def __init__(self, openai_api_key: Optional[str] = None):
        self.memory_manager = ConversationMemoryManager()
        self.conversation_history = defaultdict(list)
        self.openai_api_key = openai_api_key
        
        # Initialize LangChain components if OpenAI key is available
        if openai_api_key:
            self.llm = ChatOpenAI(
                openai_api_key=openai_api_key,
                temperature=0.7,
                model_name="gpt-3.5-turbo"
            )
        else:
            self.llm = None
            logger.warning("OpenAI API key not provided. Advanced NLP features disabled.")
        
        # Role-based system prompts
        self.system_prompts = self._define_system_prompts()
    
    def _define_system_prompts(self) -> Dict[UserRole, str]:
        """Define system prompts for each user role"""
        return {
            UserRole.SUPER_ADMIN: """
You are InfraBot, an expert infrastructure management assistant for super administrators.
You have deep knowledge of:
- System monitoring and health checks
- Security analysis and threat detection
- Performance optimization and troubleshooting
- Infrastructure management and scaling
- DevOps practices and automation

Always provide:
1. Actionable technical recommendations
2. Specific metrics or data points when available
3. Potential risks or considerations
4. Clear next steps for implementation

Be precise, technical, and solution-oriented in your responses.
""",
            UserRole.TENANT_ADMIN: """
You are BizBot, a business operations and analytics assistant for tenant administrators.
You specialize in:
- Business analytics and KPI interpretation
- Customer insights and behavior analysis
- Revenue optimization strategies
- Team management and operational efficiency
- Integration management and automation

Always provide:
1. Data-driven insights with context
2. Business impact analysis
3. Actionable recommendations for growth
4. ROI considerations for decisions

Be strategic, analytical, and business-focused in your responses.
""",
            UserRole.USER: """
You are MarketBot, a marketing and campaign optimization assistant.
You excel at:
- Marketing campaign analysis and optimization
- Lead generation and nurturing strategies
- Content creation and marketing copy
- Social media strategy and engagement
- Conversion rate optimization

Always provide:
1. Campaign-specific recommendations
2. Creative ideas for content and messaging
3. Performance improvement suggestions
4. Best practices from successful campaigns

Be creative, results-driven, and marketing-focused in your responses.
""",
            UserRole.READONLY: """
You are InfoBot, a helpful information and support assistant.
You provide:
- Clear explanations of concepts and processes
- Step-by-step guidance and tutorials
- General business information and insights
- Support for common questions and issues
- Documentation and resource recommendations

Always provide:
1. Clear, easy-to-understand explanations
2. Step-by-step instructions when applicable
3. Helpful resources and links
4. Encouragement and support

Be friendly, helpful, and educational in your responses.
"""
        }
    
    async def process_message(
        self, 
        message: str, 
        session: ChatSession, 
        file_attachments: List[str] = None
    ) -> ChatMessage:
        """Process user message with enhanced AI capabilities"""
        
        try:
            # Get role-specific assistant configuration
            assistant = role_assistants.get(session.role)
            if not assistant:
                return self._create_error_message(
                    "Unknown user role. Please contact support.",
                    session.id
                )
            
            # Update conversation context
            context_updates = {
                "last_message_time": datetime.now(timezone.utc).isoformat(),
                "message_count": len(session.messages) + 1
            }
            self.memory_manager.update_context(session.id, context_updates)
            
            # Handle file attachments if provided
            attachment_context = ""
            if file_attachments:
                attachment_context = await self._process_file_attachments(file_attachments)
            
            # Select best agent for the query
            best_agent = agent_selector.select_best_agent(
                message, 
                assistant.available_agents, 
                session.role
            )
            
            # Prepare conversation context for agent
            conversation_context = ConversationContext(
                tenant_id=session.tenant_id,
                user_role=session.role,
                dashboard_context=session.context.get("dashboard_context"),
                current_page=session.context.get("current_page"),
                recent_actions=session.context.get("recent_actions", []),
                preferences=session.agent_preferences
            )
            
            # Get conversation history for context
            memory_context = self.memory_manager.get_conversation_context(session.id)
            
            # Create agent request
            agent_request = AgentRequest(
                agent_name=best_agent,
                query=message + (f"\n\nFile context: {attachment_context}" if attachment_context else ""),
                context=conversation_context,
                message_history=self._format_message_history(memory_context.get("chat_history", []))
            )
            
            # Query CrewAI agent
            agent_response = await crew_ai_integration.query_agent(agent_request)
            
            # Enhance response with LangChain if available
            enhanced_response = await self._enhance_response(
                agent_response.response,
                message,
                session,
                agent_response.metadata
            )
            
            # Create response message
            response_message = ChatMessage(
                type=MessageType.ASSISTANT,
                content=enhanced_response,
                session_id=session.id,
                agent_name=agent_response.agent_name,
                confidence=agent_response.confidence,
                suggested_actions=agent_response.suggested_actions,
                metadata={
                    "agent_metadata": agent_response.metadata,
                    "assistant_name": assistant.name,
                    "processing_time": agent_response.processing_time,
                    "tokens_used": agent_response.tokens_used,
                    "enhancement_applied": self.llm is not None,
                    "attachments_processed": len(file_attachments) if file_attachments else 0
                }
            )
            
            # Add to conversation memory
            user_message = ChatMessage(
                type=MessageType.USER,
                content=message,
                session_id=session.id,
                user_id=session.user_id
            )
            
            self.memory_manager.add_message(session.id, user_message)
            self.memory_manager.add_message(session.id, response_message)
            
            # Store in conversation history for analytics
            self.conversation_history[session.id].append({
                "user_message": message,
                "agent_response": enhanced_response,
                "agent_name": best_agent,
                "confidence": agent_response.confidence,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "processing_time": agent_response.processing_time
            })
            
            return response_message
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return self._create_error_message(
                "I'm experiencing technical difficulties. Please try again later.",
                session.id,
                {"error": str(e)}
            )
    
    async def _enhance_response(
        self, 
        agent_response: str, 
        user_message: str, 
        session: ChatSession,
        agent_metadata: Dict[str, Any]
    ) -> str:
        """Enhance agent response using LangChain"""
        
        if not self.llm:
            return agent_response
        
        try:
            # Get system prompt for user role
            system_prompt = self.system_prompts.get(session.role, "")
            
            # Create enhancement prompt
            enhancement_prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("system", """
                You are enhancing a response from a specialized AI agent. 
                Improve the response by:
                1. Making it more conversational and personalized
                2. Adding relevant context or examples
                3. Formatting it better for readability
                4. Ensuring it matches the user's role and needs
                
                Keep the core information intact but make it more engaging and helpful.
                If the original response is already excellent, return it unchanged.
                """),
                ("human", f"User asked: {user_message}"),
                ("human", f"Agent responded: {agent_response}"),
                ("human", "Please enhance this response:")
            ])
            
            # Generate enhanced response
            chain = enhancement_prompt | self.llm
            enhanced = await chain.ainvoke({})
            
            return enhanced.content if hasattr(enhanced, 'content') else str(enhanced)
            
        except Exception as e:
            logger.error(f"Error enhancing response: {e}")
            # Return original response if enhancement fails
            return agent_response
    
    async def _process_file_attachments(self, file_attachments: List[str]) -> str:
        """Process file attachments and extract relevant context"""
        # This is a placeholder for file processing
        # In a real implementation, you would:
        # 1. Download/read the files
        # 2. Extract text content
        # 3. Analyze for relevant information
        # 4. Return summary context
        
        if not file_attachments:
            return ""
        
        return f"User uploaded {len(file_attachments)} file(s) for analysis."
    
    def _format_message_history(self, messages: List[BaseMessage]) -> List[Dict[str, Any]]:
        """Format LangChain messages for agent context"""
        formatted_history = []
        
        for msg in messages[-10:]:  # Last 10 messages for context
            if isinstance(msg, HumanMessage):
                formatted_history.append({
                    "role": "user",
                    "content": msg.content,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                })
            elif isinstance(msg, AIMessage):
                formatted_history.append({
                    "role": "assistant", 
                    "content": msg.content,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                })
        
        return formatted_history
    
    def _create_error_message(
        self, 
        content: str, 
        session_id: str, 
        metadata: Dict[str, Any] = None
    ) -> ChatMessage:
        """Create error message"""
        return ChatMessage(
            type=MessageType.ERROR,
            content=content,
            session_id=session_id,
            metadata=metadata or {}
        )
    
    async def generate_conversation_summary(self, session_id: str) -> Optional[ConversationSummary]:
        """Generate summary of conversation for long-term context"""
        if not self.llm:
            return None
        
        try:
            memory_context = self.memory_manager.get_conversation_context(session_id)
            messages = memory_context.get("chat_history", [])
            
            if len(messages) < 3:  # Not enough for meaningful summary
                return None
            
            # Create summarization prompt
            conversation_text = "\n".join([
                f"{'User' if isinstance(msg, HumanMessage) else 'Assistant'}: {msg.content}"
                for msg in messages
            ])
            
            summary_prompt = f"""
            Summarize this conversation between a user and AI assistant:
            
            {conversation_text}
            
            Provide:
            1. A brief summary (2-3 sentences)
            2. Key topics discussed
            3. Any action items or follow-ups
            4. Overall sentiment (positive/neutral/negative)
            
            Format as JSON with keys: summary, key_topics, action_items, sentiment
            """
            
            response = await self.llm.ainvoke(summary_prompt)
            summary_data = json.loads(response.content)
            
            return ConversationSummary(
                session_id=session_id,
                summary=summary_data.get("summary", ""),
                key_topics=summary_data.get("key_topics", []),
                action_items=summary_data.get("action_items", []),
                sentiment=summary_data.get("sentiment", "neutral"),
                created_at=datetime.now(timezone.utc)
            )
            
        except Exception as e:
            logger.error(f"Error generating conversation summary: {e}")
            return None
    
    def get_session_analytics(self, session_id: str) -> Dict[str, Any]:
        """Get analytics for a chat session"""
        history = self.conversation_history[session_id]
        memory_context = self.memory_manager.get_conversation_context(session_id)
        
        if not history:
            return {"error": "No conversation history found"}
        
        # Calculate metrics
        total_messages = len(history)
        avg_response_time = sum(h.get("processing_time", 0) for h in history) / total_messages if total_messages > 0 else 0
        agents_used = {}
        confidence_scores = []
        
        for h in history:
            agent = h.get("agent_name", "unknown")
            agents_used[agent] = agents_used.get(agent, 0) + 1
            
            confidence = h.get("confidence", 0)
            if confidence > 0:
                confidence_scores.append(confidence)
        
        avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
        
        return {
            "session_id": session_id,
            "total_interactions": total_messages,
            "average_response_time": round(avg_response_time, 2),
            "average_confidence": round(avg_confidence, 2),
            "agents_used": agents_used,
            "most_used_agent": max(agents_used.items(), key=lambda x: x[1])[0] if agents_used else None,
            "message_count_in_memory": memory_context.get("message_count", 0),
            "has_context": bool(memory_context.get("context")),
            "has_summary": bool(memory_context.get("summary"))
        }
    
    def cleanup_old_sessions(self, max_age_hours: int = 24):
        """Clean up old conversation sessions"""
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=max_age_hours)
        
        sessions_to_remove = []
        for session_id, history in self.conversation_history.items():
            if history:
                last_interaction = datetime.fromisoformat(history[-1]["timestamp"].replace('Z', '+00:00'))
                if last_interaction < cutoff_time:
                    sessions_to_remove.append(session_id)
        
        for session_id in sessions_to_remove:
            self.memory_manager.clear_session(session_id)
            del self.conversation_history[session_id]
            logger.info(f"Cleaned up old session: {session_id}")
        
        return len(sessions_to_remove)