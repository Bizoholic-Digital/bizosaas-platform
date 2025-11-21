#!/usr/bin/env python3
"""
BizOSaaS AI Chat Service
Role-based conversational AI interface for admin dashboards
Integrates with CrewAI agents and unified authentication system
"""

import asyncio
import json
import uuid
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional, Union, AsyncGenerator
from enum import Enum

from fastapi import (
    FastAPI, WebSocket, WebSocketDisconnect, HTTPException, 
    Depends, Request, UploadFile, File, Form, BackgroundTasks
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
import uvicorn
import httpx
import logging
from collections import defaultdict

# Import authentication system
import sys
sys.path.append('/home/alagiri/projects/bizoholic/bizosaas')

from shared.auth_system import (
    UserRole, User, Tenant, current_active_user, 
    require_role, get_async_session
)
from shared.logging_system import get_logger, LogLevel, LogCategory

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="BizOSaaS AI Chat Service",
    description="Role-based conversational AI interface for admin dashboards",
    version="1.0.0",
    docs_url="/chat/docs",
    redoc_url="/chat/redoc"
)

# CORS middleware for dashboard integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3001",  # TailAdmin dashboard
        "http://localhost:5000",  # SQLAdmin dashboard
        "http://localhost:3002",  # Auth service
        "http://localhost:8000",  # CrewAI agents
        "*"  # TODO: Restrict in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# HTTP Bearer security
security = HTTPBearer()

# Global logger instance
app_logger = None

# Import models and components
from app.models import (
    MessageType, ChatMessage, ChatSession, ChatRequest, AgentResponse,
    ConversationContext, WebSocketMessage, UserRole
)
from app.agents import crew_ai_integration, agent_selector, role_assistants
from app.chat_processor import EnhancedChatProcessor
from app.websocket_manager import websocket_manager, periodic_cleanup

# Initialize enhanced chat processor
chat_processor = EnhancedChatProcessor(
    openai_api_key=os.environ.get("OPENAI_API_KEY")
)

# Use the enhanced WebSocket manager from app module
# manager = websocket_manager (imported above)

# Use the enhanced CrewAI integration from app module
# crew_ai_integration (imported above)

# Use the enhanced chat processor from app module
# chat_processor (imported above)

# Authentication dependency
async def verify_auth_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Verify JWT token with auth service"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "http://localhost:3002/auth/me",
                headers={"Authorization": f"Bearer {credentials.credentials}"}
            )
            
            if response.status_code == 200:
                user_data = response.json()
                # Create a mock User object with the necessary fields
                user = type('User', (), {
                    'id': user_data['user']['id'],
                    'email': user_data['user']['email'],
                    'role': UserRole(user_data['permissions']['role']),
                    'tenant_id': user_data['tenant']['id'],
                    'tenant': type('Tenant', (), user_data['tenant'])()
                })()
                return user
            else:
                raise HTTPException(status_code=401, detail="Invalid authentication token")
                
    except Exception as e:
        logger.error(f"Authentication verification failed: {e}")
        raise HTTPException(status_code=401, detail="Authentication failed")

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize AI chat service"""
    global app_logger
    app_logger = get_logger()
    
    # Start periodic cleanup task
    asyncio.create_task(periodic_cleanup())
    
    await app_logger.log(
        LogLevel.INFO,
        LogCategory.SYSTEM,
        "ai-chat-service",
        "AI Chat Service started successfully",
        details={
            "version": "1.0.0",
            "port": 3003,
            "role_assistants": list(role_assistants.keys()),
            "enhanced_features": {
                "langchain_integration": chat_processor.llm is not None,
                "websocket_support": True,
                "conversation_memory": True,
                "file_upload_support": True
            }
        }
    )

# API Endpoints
@app.get("/")
async def root():
    """Service health check"""
    return {
        "service": "bizosaas-ai-chat-service",
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "supported_roles": list(ROLE_ASSISTANTS.keys())
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    # Test CrewAI connectivity
    crew_ai_health = await crew_ai_integration.health_check()
    
    # Get WebSocket connection stats
    ws_stats = websocket_manager.get_connection_stats()
    
    return {
        "status": "healthy",
        "crew_ai": crew_ai_health,
        "websocket_connections": ws_stats,
        "chat_processor": {
            "langchain_enabled": chat_processor.llm is not None,
            "total_conversations": len(chat_processor.conversation_history),
            "memory_sessions": len(chat_processor.memory_manager.session_memories)
        },
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/chat/assistants")
async def get_assistants(user: User = Depends(verify_auth_token)):
    """Get available AI assistants for user role"""
    assistant = role_assistants.get(user.role)
    
    if not assistant:
        raise HTTPException(status_code=403, detail="No AI assistant available for your role")
    
    return {
        "role": user.role,
        "assistant": assistant.dict(),
        "session_info": {
            "user_id": str(user.id),
            "tenant_id": str(user.tenant_id),
            "email": user.email
        }
    }

@app.post("/chat/message")
async def send_message(
    chat_request: ChatRequest,
    user: User = Depends(verify_auth_token)
) -> Dict[str, Any]:
    """Send a chat message and get AI response"""
    
    # Get or create session
    session_id = chat_request.session_id or str(uuid.uuid4())
    
    if session_id not in websocket_manager.user_sessions:
        # Create conversation context
        context = ConversationContext(
            tenant_id=str(user.tenant_id),
            user_role=user.role,
            dashboard_context=chat_request.context,
            preferences={}
        )
        
        websocket_manager.user_sessions[session_id] = ChatSession(
            id=session_id,
            user_id=str(user.id),
            tenant_id=str(user.tenant_id), 
            role=user.role,
            context=context
        )
    
    session = websocket_manager.user_sessions[session_id]
    
    # Create user message
    user_message = ChatMessage(
        type=MessageType.USER,
        content=chat_request.message,
        session_id=session_id,
        user_id=str(user.id)
    )
    
    # Add to session
    session.messages.append(user_message)
    session.last_activity = datetime.now(timezone.utc)
    
    # Process with enhanced AI
    ai_response = await chat_processor.process_message(
        chat_request.message, 
        session, 
        chat_request.file_attachments
    )
    session.messages.append(ai_response)
    
    # Send via WebSocket if connected
    if session_id in websocket_manager.connections:
        await websocket_manager.send_chat_message(session_id, ai_response)
    
    # Log the interaction
    await app_logger.log(
        LogLevel.INFO,
        LogCategory.API,
        "ai-chat-service", 
        f"Chat interaction: {user.role}",
        details={
            "user_id": str(user.id),
            "tenant_id": str(user.tenant_id),
            "session_id": session_id,
            "agent_used": ai_response.agent_name,
            "message_length": len(chat_request.message),
            "confidence": ai_response.confidence,
            "processing_time": ai_response.metadata.get("processing_time")
        }
    )
    
    return {
        "session_id": session_id,
        "user_message": user_message.dict(),
        "ai_response": ai_response.dict(),
        "conversation_length": len(session.messages),
        "suggested_actions": ai_response.suggested_actions
    }

@app.get("/chat/history/{session_id}")
async def get_chat_history(
    session_id: str,
    user: User = Depends(verify_auth_token)
) -> Dict[str, Any]:
    """Get chat history for a session"""
    
    if session_id not in websocket_manager.user_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = websocket_manager.user_sessions[session_id]
    
    # Verify user owns this session
    if session.user_id != str(user.id):
        raise HTTPException(status_code=403, detail="Access denied to this session")
    
    # Get analytics for the session
    analytics = chat_processor.get_session_analytics(session_id)
    
    return {
        "session": session.dict(),
        "message_count": len(session.messages),
        "last_activity": session.last_activity,
        "analytics": analytics
    }

@app.delete("/chat/session/{session_id}")
async def delete_session(
    session_id: str,
    user: User = Depends(verify_auth_token)
):
    """Delete a chat session"""
    
    if session_id not in websocket_manager.user_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = websocket_manager.user_sessions[session_id]
    
    # Verify user owns this session
    if session.user_id != str(user.id):
        raise HTTPException(status_code=403, detail="Access denied to this session")
    
    # Disconnect WebSocket if active
    if session_id in websocket_manager.connections:
        await websocket_manager.disconnect(session_id, "session_deleted")
    
    # Remove session
    del websocket_manager.user_sessions[session_id]
    
    # Clear conversation memory
    chat_processor.memory_manager.clear_session(session_id)
    
    # Clear conversation history
    if session_id in chat_processor.conversation_history:
        del chat_processor.conversation_history[session_id]
    
    return {"status": "Session deleted successfully"}

# WebSocket endpoint for real-time chat
@app.websocket("/chat/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str, token: Optional[str] = None):
    """WebSocket endpoint for real-time chat"""
    
    # Verify authentication token
    user = None
    if token:
        try:
            # Verify token with auth service
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "http://localhost:3002/auth/me",
                    headers={"Authorization": f"Bearer {token}"}
                )
                
                if response.status_code == 200:
                    user_data = response.json()
                    # Create mock user object
                    user = type('User', (), {
                        'id': user_data['user']['id'],
                        'email': user_data['user']['email'],
                        'role': UserRole(user_data['permissions']['role']),
                        'tenant_id': user_data['tenant']['id']
                    })()
        except Exception as e:
            logger.error(f"WebSocket auth failed: {e}")
    
    if not user:
        await websocket.close(code=1008, reason="Authentication required")
        return
    
    # Connect WebSocket
    connected = await websocket_manager.connect(
        websocket, session_id, str(user.id), str(user.tenant_id), user.role
    )
    
    if not connected:
        await websocket.close(code=1011, reason="Connection failed")
        return
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            message_type = message_data.get("type", "message")
            
            if message_type == "message":
                # Process chat message
                content = message_data.get("content", "")
                if content.strip():
                    session = websocket_manager.user_sessions.get(session_id)
                    if session:
                        # Process with AI
                        ai_response = await chat_processor.process_message(content, session)
                        
                        # Send response
                        await websocket_manager.send_chat_message(session_id, ai_response)
            
            elif message_type == "typing":
                # Handle typing indicator
                is_typing = message_data.get("is_typing", False)
                await websocket_manager.handle_typing_indicator(session_id, is_typing)
            
            elif message_type == "ping":
                # Handle ping/pong for connection keepalive
                pong_message = WebSocketMessage(
                    type="pong",
                    content="pong",
                    session_id=session_id,
                    user_id=str(user.id)
                )
                await websocket_manager.send_message(session_id, pong_message)
            
    except WebSocketDisconnect:
        await websocket_manager.disconnect(session_id, "client_disconnect")
        logger.info(f"WebSocket disconnected: {session_id}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket_manager.disconnect(session_id, "error")

# Embeddable chat widget endpoint
@app.get("/chat/widget", response_class=HTMLResponse)
async def chat_widget(request: Request):
    """Serve embeddable chat widget"""
    return templates.TemplateResponse("chat_widget.html", {"request": request})

@app.get("/chat/embed.js")
async def chat_embed_script():
    """JavaScript for embedding chat widget"""
    js_content = """
// BizOSaaS AI Chat Widget
class BizOSaaSChat {
    constructor(options = {}) {
        this.apiUrl = options.apiUrl || 'http://localhost:3003';
        this.authToken = options.authToken;
        this.container = options.container || 'bizosaas-chat';
        this.position = options.position || 'bottom-right';
        this.init();
    }
    
    init() {
        this.createChatInterface();
        this.bindEvents();
    }
    
    createChatInterface() {
        const chatContainer = document.createElement('div');
        chatContainer.id = 'bizosaas-chat-container';
        chatContainer.style.cssText = `
            position: fixed;
            ${this.position.includes('bottom') ? 'bottom: 20px;' : 'top: 20px;'}
            ${this.position.includes('right') ? 'right: 20px;' : 'left: 20px;'}
            width: 350px;
            height: 500px;
            background: white;
            border: 1px solid #ddd;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 10000;
            display: none;
            flex-direction: column;
        `;
        
        chatContainer.innerHTML = `
            <div id="chat-header" style="
                background: #2563eb;
                color: white;
                padding: 15px;
                border-radius: 10px 10px 0 0;
                font-weight: 600;
                display: flex;
                justify-content: space-between;
                align-items: center;
            ">
                <span>AI Assistant</span>
                <button id="chat-close" style="
                    background: none;
                    border: none;
                    color: white;
                    font-size: 18px;
                    cursor: pointer;
                ">×</button>
            </div>
            <div id="chat-messages" style="
                flex: 1;
                padding: 15px;
                overflow-y: auto;
                background: #f9fafb;
            "></div>
            <div id="chat-input-container" style="
                padding: 15px;
                border-top: 1px solid #e5e7eb;
                background: white;
                border-radius: 0 0 10px 10px;
            ">
                <div style="display: flex; gap: 10px;">
                    <input 
                        type="text" 
                        id="chat-input" 
                        placeholder="Ask me anything..."
                        style="
                            flex: 1;
                            padding: 10px;
                            border: 1px solid #d1d5db;
                            border-radius: 6px;
                            outline: none;
                        "
                    />
                    <button id="chat-send" style="
                        padding: 10px 15px;
                        background: #2563eb;
                        color: white;
                        border: none;
                        border-radius: 6px;
                        cursor: pointer;
                        font-weight: 500;
                    ">Send</button>
                </div>
            </div>
        `;
        
        document.body.appendChild(chatContainer);
        
        // Chat toggle button
        const toggleButton = document.createElement('button');
        toggleButton.id = 'bizosaas-chat-toggle';
        toggleButton.innerHTML = '💬';
        toggleButton.style.cssText = `
            position: fixed;
            ${this.position.includes('bottom') ? 'bottom: 20px;' : 'top: 20px;'}
            ${this.position.includes('right') ? 'right: 20px;' : 'left: 20px;'}
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: #2563eb;
            border: none;
            color: white;
            font-size: 24px;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 10001;
        `;
        
        document.body.appendChild(toggleButton);
    }
    
    bindEvents() {
        const toggle = document.getElementById('bizosaas-chat-toggle');
        const container = document.getElementById('bizosaas-chat-container');
        const close = document.getElementById('chat-close');
        const input = document.getElementById('chat-input');
        const send = document.getElementById('chat-send');
        
        toggle.addEventListener('click', () => {
            container.style.display = container.style.display === 'none' ? 'flex' : 'none';
        });
        
        close.addEventListener('click', () => {
            container.style.display = 'none';
        });
        
        send.addEventListener('click', () => this.sendMessage());
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });
    }
    
    async sendMessage() {
        const input = document.getElementById('chat-input');
        const message = input.value.trim();
        
        if (!message) return;
        
        // Add user message to chat
        this.addMessage('user', message);
        input.value = '';
        
        // Send to API
        try {
            const response = await fetch(`${this.apiUrl}/chat/message`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.authToken}`
                },
                body: JSON.stringify({ message })
            });
            
            const data = await response.json();
            this.addMessage('assistant', data.ai_response.content);
        } catch (error) {
            this.addMessage('assistant', 'Sorry, I am experiencing technical difficulties.');
        }
    }
    
    addMessage(type, content) {
        const messages = document.getElementById('chat-messages');
        const messageDiv = document.createElement('div');
        messageDiv.style.cssText = `
            margin-bottom: 15px;
            padding: 10px;
            border-radius: 8px;
            ${type === 'user' 
                ? 'background: #2563eb; color: white; margin-left: 20%; text-align: right;'
                : 'background: white; border: 1px solid #e5e7eb; margin-right: 20%;'
            }
        `;
        messageDiv.textContent = content;
        messages.appendChild(messageDiv);
        messages.scrollTop = messages.scrollHeight;
    }
}

// Auto-initialize if auth token is available
window.BizOSaaSChat = BizOSaaSChat;
    """.strip()
    
    return JSONResponse(
        content=js_content,
        headers={"Content-Type": "application/javascript"}
    )

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 3003))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )