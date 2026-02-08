"""
Enhanced Telegram Bot Integration Service for Personal AI Assistant
Combines existing telegram service with Personal AI Assistant capabilities
"""

import os
import asyncio
import json
import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timezone
from uuid import uuid4
import aiofiles

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Depends, BackgroundTasks, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import httpx
from telegram import Update, Bot, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, CallbackContext
from sqlalchemy.orm import Session

# Import existing telegram service
from telegram_service import TelegramBotClient, TELEGRAM_BOTS, bot_clients

# Import personal AI assistant
from personal_ai_assistant import (
    PersonalAIAssistant, VoiceProcessor, get_db, create_tables,
    PersonalAssistantProfile, ConversationSession, ConversationMessage, PersonalReminder, ProductivityTask,
    AssistantType, MessagePriority, ProfileCreate, ProfileResponse, MessageRequest, MessageResponse,
    ReminderCreate, TaskCreate
)

logger = logging.getLogger(__name__)

# ========================================================================================
# ENHANCED TELEGRAM MODELS
# ========================================================================================

class TelegramUser(BaseModel):
    telegram_user_id: str
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    language_code: Optional[str] = "en"

class AssistantSetupRequest(BaseModel):
    telegram_user_id: str
    assistant_type: AssistantType
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    emergency_contacts: List[Dict[str, Any]] = Field(default_factory=list)
    medical_conditions: List[str] = Field(default_factory=list)
    medications: List[Dict[str, Any]] = Field(default_factory=list)

class WebhookUpdate(BaseModel):
    update_id: int
    message: Optional[Dict[str, Any]] = None
    callback_query: Optional[Dict[str, Any]] = None

# ========================================================================================
# ENHANCED TELEGRAM SERVICE CLASS
# ========================================================================================

class EnhancedTelegramService:
    """Enhanced Telegram service with Personal AI Assistant integration"""
    
    def __init__(self):
        self.assistant = PersonalAIAssistant()
        self.voice_processor = VoiceProcessor()
        self.active_conversations: Dict[str, str] = {}  # chat_id -> session_id
        
        # Initialize Telegram bot applications
        self.bot_applications = {}
        for bot_name, config in TELEGRAM_BOTS.items():
            self.bot_applications[bot_name] = Application.builder().token(config["token"]).build()
    
    async def setup_assistant_profile(self, setup_request: AssistantSetupRequest, 
                                    db: Session) -> PersonalAssistantProfile:
        """Setup or update assistant profile for Telegram user"""
        
        # Check if profile exists
        existing_profile = db.query(PersonalAssistantProfile).filter(
            PersonalAssistantProfile.telegram_user_id == setup_request.telegram_user_id
        ).first()
        
        if existing_profile:
            # Update existing profile
            existing_profile.assistant_type = setup_request.assistant_type
            existing_profile.telegram_username = setup_request.username
            existing_profile.first_name = setup_request.first_name
            existing_profile.last_name = setup_request.last_name
            existing_profile.emergency_contacts = setup_request.emergency_contacts
            existing_profile.medical_conditions = setup_request.medical_conditions
            existing_profile.medications = setup_request.medications
            existing_profile.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(existing_profile)
            return existing_profile
        else:
            # Create new profile
            profile = PersonalAssistantProfile(
                user_id=f"tg_{setup_request.telegram_user_id}",
                telegram_user_id=setup_request.telegram_user_id,
                telegram_username=setup_request.username,
                first_name=setup_request.first_name,
                last_name=setup_request.last_name,
                assistant_type=setup_request.assistant_type,
                emergency_contacts=setup_request.emergency_contacts,
                medical_conditions=setup_request.medical_conditions,
                medications=setup_request.medications
            )
            
            db.add(profile)
            db.commit()
            db.refresh(profile)
            return profile
    
    async def process_telegram_message(self, chat_id: str, message_text: str, 
                                     telegram_user_id: str, db: Session,
                                     is_voice: bool = False, voice_file_path: Optional[str] = None) -> str:
        """Process incoming Telegram message through Personal AI Assistant"""
        
        try:
            # Get user profile
            profile = db.query(PersonalAssistantProfile).filter(
                PersonalAssistantProfile.telegram_user_id == telegram_user_id
            ).first()
            
            if not profile:
                return self._get_setup_message()
            
            # Get or create conversation session
            session_id = self.active_conversations.get(chat_id)
            if not session_id:
                session_id = str(uuid4())
                self.active_conversations[chat_id] = session_id
                
                # Create database session record
                db_session = ConversationSession(
                    session_id=session_id,
                    profile_id=profile.id,
                    telegram_chat_id=chat_id,
                    conversation_goal="General assistance"
                )
                db.add(db_session)
                db.commit()
            
            # Handle voice message transcription
            if is_voice and voice_file_path:
                transcription = await self.voice_processor.transcribe_voice_message(voice_file_path)
                message_text = f"[Voice Message] {transcription}"
            
            # Store user message
            user_message = ConversationMessage(
                session_id=db.query(ConversationSession).filter(
                    ConversationSession.session_id == session_id
                ).first().id,
                message_id=str(uuid4()),
                content=message_text,
                message_type="user",
                is_voice_message=is_voice,
                voice_file_path=voice_file_path
            )
            db.add(user_message)
            db.commit()
            
            # Process message through AI assistant
            response = await self.assistant.process_message(
                profile, message_text, session_id, is_voice
            )
            
            # Store agent response
            agent_message = ConversationMessage(
                session_id=user_message.session_id,
                message_id=response.message_id,
                content=response.response,
                message_type="agent",
                sender_agent=response.agent_used
            )
            db.add(agent_message)
            db.commit()
            
            # Format response for Telegram
            formatted_response = self._format_telegram_response(response, profile.assistant_type)
            
            return formatted_response
            
        except Exception as e:
            logger.error(f"Error processing Telegram message: {e}")
            return "I apologize, but I'm having trouble processing your message right now. Please try again in a moment."
    
    def _get_setup_message(self) -> str:
        """Get setup message for new users"""
        return """
🤖 Welcome to your Personal AI Assistant!

To get started, please use the /setup command to configure your assistant:

• /setup eldercare - For elder care assistance
• /setup productivity - For founder productivity 
• /setup business - For client business support
• /setup general - For general assistance

Example: /setup eldercare

Once configured, I'll be able to help you with personalized assistance! 🚀
"""
    
    def _format_telegram_response(self, response: MessageResponse, assistant_type: AssistantType) -> str:
        """Format AI response for Telegram with proper styling"""
        
        # Base response
        formatted = f"🤖 {response.response}\n"
        
        # Add suggestions if available
        if response.suggestions:
            formatted += "\n💡 Suggestions:\n"
            for i, suggestion in enumerate(response.suggestions[:3], 1):
                formatted += f"{i}. {suggestion}\n"
        
        # Add assistant type specific emojis
        type_emojis = {
            AssistantType.ELDERCARE: "👨‍⚕️",
            AssistantType.FOUNDER_PRODUCTIVITY: "🚀", 
            AssistantType.CLIENT_BUSINESS: "💼",
            AssistantType.GENERAL: "🤖"
        }
        
        if assistant_type in type_emojis:
            formatted = f"{type_emojis[assistant_type]} " + formatted
        
        # Add agent attribution if available
        if response.agent_used and response.agent_used != "fallback":
            formatted += f"\n\n🔧 Powered by: {response.agent_used.replace('_', ' ').title()}"
        
        return formatted
    
    async def create_telegram_keyboard(self, actions: List[Dict[str, Any]]) -> InlineKeyboardMarkup:
        """Create Telegram inline keyboard from actions"""
        
        keyboard = []
        for action in actions:
            button = InlineKeyboardButton(
                text=action.get("text", "Action"),
                callback_data=action.get("type", "action")
            )
            keyboard.append([button])
        
        return InlineKeyboardMarkup(keyboard)
    
    async def handle_callback_query(self, callback_data: str, chat_id: str, 
                                  telegram_user_id: str, db: Session) -> str:
        """Handle Telegram callback query from inline keyboards"""
        
        # Get user profile
        profile = db.query(PersonalAssistantProfile).filter(
            PersonalAssistantProfile.telegram_user_id == telegram_user_id
        ).first()
        
        if not profile:
            return "Please setup your assistant first using /setup"
        
        # Handle different callback types
        if callback_data == "emergency_contact":
            return await self._handle_emergency_contact(profile)
        elif callback_data == "create_task":
            return "📝 Please describe the task you'd like to create:"
        elif callback_data == "view_tasks":
            return await self._get_user_tasks(profile, db)
        elif callback_data == "set_reminder":
            return "⏰ Please describe what you'd like to be reminded about:"
        else:
            return "Action processed! How else can I help you?"
    
    async def _handle_emergency_contact(self, profile: PersonalAssistantProfile) -> str:
        """Handle emergency contact action"""
        
        if not profile.emergency_contacts:
            return "⚠️ No emergency contacts configured. Please update your profile."
        
        contacts_text = "🚨 Emergency Contacts:\n\n"
        for i, contact in enumerate(profile.emergency_contacts, 1):
            contacts_text += f"{i}. {contact.get('name', 'Unknown')}: {contact.get('phone', 'No phone')}\n"
        
        contacts_text += "\n🆘 Call emergency services (911/112) for immediate medical emergencies!"
        
        return contacts_text
    
    async def _get_user_tasks(self, profile: PersonalAssistantProfile, db: Session) -> str:
        """Get user's current tasks"""
        
        tasks = db.query(ProductivityTask).filter(
            ProductivityTask.profile_id == profile.id,
            ProductivityTask.status != "completed"
        ).order_by(ProductivityTask.created_at.desc()).limit(5).all()
        
        if not tasks:
            return "📝 No active tasks found. Create one by saying 'create task' or using the /task command!"
        
        tasks_text = "📋 Your Active Tasks:\n\n"
        for i, task in enumerate(tasks, 1):
            status_emoji = "⏳" if task.status == "in_progress" else "📌"
            priority_emoji = "🔥" if task.priority == MessagePriority.HIGH else "📋"
            
            tasks_text += f"{i}. {priority_emoji} {task.title}\n"
            if task.due_date:
                tasks_text += f"   Due: {task.due_date.strftime('%Y-%m-%d')}\n"
            tasks_text += f"   Status: {status_emoji} {task.status}\n\n"
        
        return tasks_text

# ========================================================================================
# TELEGRAM BOT HANDLERS
# ========================================================================================

# Global service instance
telegram_service = EnhancedTelegramService()

async def start_command(update: Update, context: CallbackContext) -> None:
    """Handle /start command"""
    welcome_message = """
🤖 Welcome to your Personal AI Assistant!

I'm powered by 88+ specialized AI agents and can help you with:

👨‍⚕️ ElderCare: Medication reminders, health monitoring, emergency assistance
🚀 Founder Productivity: Task management, goal tracking, focus sessions  
💼 Business Support: Client management, marketing, analytics
🤖 General Assistance: Various daily tasks and questions

Use /setup to configure your assistant type and preferences.
Use /help to see all available commands.

How can I help you today? 🌟
"""
    await update.message.reply_text(welcome_message)

async def setup_command(update: Update, context: CallbackContext) -> None:
    """Handle /setup command"""
    if not context.args:
        setup_message = """
🛠️ Setup Your Personal AI Assistant

Choose your assistant type:
• `/setup eldercare` - Elder care assistance
• `/setup productivity` - Founder productivity
• `/setup business` - Client business support  
• `/setup general` - General assistance

Example: `/setup eldercare`
"""
        await update.message.reply_text(setup_message)
        return
    
    assistant_type_map = {
        "eldercare": AssistantType.ELDERCARE,
        "productivity": AssistantType.FOUNDER_PRODUCTIVITY,
        "business": AssistantType.CLIENT_BUSINESS,
        "general": AssistantType.GENERAL
    }
    
    assistant_type_str = context.args[0].lower()
    if assistant_type_str not in assistant_type_map:
        await update.message.reply_text("Invalid assistant type. Use: eldercare, productivity, business, or general")
        return
    
    # Get database session
    db = next(get_db())
    
    try:
        # Setup assistant profile
        setup_request = AssistantSetupRequest(
            telegram_user_id=str(update.effective_user.id),
            assistant_type=assistant_type_map[assistant_type_str],
            username=update.effective_user.username,
            first_name=update.effective_user.first_name,
            last_name=update.effective_user.last_name
        )
        
        profile = await telegram_service.setup_assistant_profile(setup_request, db)
        
        success_message = f"""
✅ Assistant Setup Complete!

🤖 Type: {assistant_type_str.title()}
👤 Name: {profile.first_name or 'Not provided'}
🆔 User ID: {profile.user_id}

Your personal AI assistant is now ready! Send me any message and I'll help you using our 88+ specialized AI agents.

Type /help to see available commands.
"""
        await update.message.reply_text(success_message)
        
    except Exception as e:
        logger.error(f"Setup error: {e}")
        await update.message.reply_text("Setup failed. Please try again or contact support.")
    finally:
        db.close()

async def help_command(update: Update, context: CallbackContext) -> None:
    """Handle /help command"""
    help_message = """
🆘 Personal AI Assistant Commands

**Setup & Configuration:**
• `/start` - Welcome message
• `/setup <type>` - Configure assistant (eldercare/productivity/business/general)
• `/profile` - View your profile
• `/settings` - Update settings

**Task & Productivity:**
• `/task <description>` - Create new task
• `/tasks` - View your tasks
• `/remind <description>` - Set reminder
• `/reminders` - View reminders

**Assistant Features:**
• `/focus` - Start focus session
• `/goals` - View/update goals
• `/emergency` - Emergency contacts (ElderCare)
• `/health` - Health check-in (ElderCare)

**General:**
• `/help` - This help message
• `/status` - Assistant status

Just send me any message and I'll respond using the most appropriate AI agent! 🤖✨
"""
    await update.message.reply_text(help_message)

async def handle_message(update: Update, context: CallbackContext) -> None:
    """Handle regular text messages"""
    chat_id = str(update.effective_chat.id)
    telegram_user_id = str(update.effective_user.id)
    message_text = update.message.text
    
    # Get database session
    db = next(get_db())
    
    try:
        # Process message through enhanced telegram service
        response = await telegram_service.process_telegram_message(
            chat_id, message_text, telegram_user_id, db
        )
        
        await update.message.reply_text(response)
        
    except Exception as e:
        logger.error(f"Message handling error: {e}")
        await update.message.reply_text("Sorry, I'm having trouble right now. Please try again.")
    finally:
        db.close()

async def handle_voice(update: Update, context: CallbackContext) -> None:
    """Handle voice messages"""
    chat_id = str(update.effective_chat.id)
    telegram_user_id = str(update.effective_user.id)
    
    # Get database session
    db = next(get_db())
    
    try:
        # Download voice file
        voice_file = await update.message.voice.get_file()
        voice_path = f"/tmp/voice_{update.message.message_id}.ogg"
        await voice_file.download_to_drive(voice_path)
        
        # Process voice message
        response = await telegram_service.process_telegram_message(
            chat_id, "[Voice Message]", telegram_user_id, db,
            is_voice=True, voice_file_path=voice_path
        )
        
        await update.message.reply_text(response)
        
        # Clean up file
        if os.path.exists(voice_path):
            os.remove(voice_path)
        
    except Exception as e:
        logger.error(f"Voice handling error: {e}")
        await update.message.reply_text("Sorry, I couldn't process your voice message. Please try typing instead.")
    finally:
        db.close()

async def handle_callback_query(update: Update, context: CallbackContext) -> None:
    """Handle callback queries from inline keyboards"""
    query = update.callback_query
    await query.answer()
    
    chat_id = str(query.message.chat_id)
    telegram_user_id = str(query.from_user.id)
    callback_data = query.data
    
    # Get database session
    db = next(get_db())
    
    try:
        response = await telegram_service.handle_callback_query(
            callback_data, chat_id, telegram_user_id, db
        )
        
        await query.edit_message_text(response)
        
    except Exception as e:
        logger.error(f"Callback query error: {e}")
        await query.edit_message_text("Action failed. Please try again.")
    finally:
        db.close()

# ========================================================================================
# FASTAPI APPLICATION
# ========================================================================================

# Create FastAPI app
app = FastAPI(
    title="Personal AI Assistant Telegram Service",
    description="Enhanced Telegram integration with Personal AI Assistant capabilities",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize service on startup"""
    create_tables()
    
    # Setup Telegram bot handlers for all bots
    for bot_name, app_instance in telegram_service.bot_applications.items():
        app_instance.add_handler(CommandHandler("start", start_command))
        app_instance.add_handler(CommandHandler("setup", setup_command))
        app_instance.add_handler(CommandHandler("help", help_command))
        app_instance.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        app_instance.add_handler(MessageHandler(filters.VOICE, handle_voice))
        app_instance.add_handler(CallbackQueryHandler(handle_callback_query))
        
        logger.info(f"Telegram bot handlers configured for {bot_name}")

# Include existing telegram service endpoints
from telegram_service import app as telegram_app
app.mount("/telegram", telegram_app)

# ========================================================================================
# PERSONAL ASSISTANT API ENDPOINTS
# ========================================================================================

@app.post("/assistant/profiles", response_model=ProfileResponse)
async def create_assistant_profile(setup_request: AssistantSetupRequest, db: Session = Depends(get_db)):
    """Create or update assistant profile"""
    profile = await telegram_service.setup_assistant_profile(setup_request, db)
    
    return ProfileResponse(
        id=str(profile.id),
        user_id=profile.user_id,
        telegram_user_id=profile.telegram_user_id,
        telegram_username=profile.telegram_username,
        first_name=profile.first_name,
        last_name=profile.last_name,
        assistant_type=profile.assistant_type,
        is_active=profile.is_active,
        created_at=profile.created_at
    )

@app.get("/assistant/profiles/{telegram_user_id}", response_model=ProfileResponse)
async def get_assistant_profile(telegram_user_id: str, db: Session = Depends(get_db)):
    """Get assistant profile by Telegram user ID"""
    profile = db.query(PersonalAssistantProfile).filter(
        PersonalAssistantProfile.telegram_user_id == telegram_user_id
    ).first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    return ProfileResponse(
        id=str(profile.id),
        user_id=profile.user_id,
        telegram_user_id=profile.telegram_user_id,
        telegram_username=profile.telegram_username,
        first_name=profile.first_name,
        last_name=profile.last_name,
        assistant_type=profile.assistant_type,
        is_active=profile.is_active,
        created_at=profile.created_at
    )

@app.post("/assistant/message")
async def send_assistant_message(request: MessageRequest, db: Session = Depends(get_db)):
    """Send message to personal AI assistant"""
    response = await telegram_service.process_telegram_message(
        request.telegram_chat_id,
        request.content,
        request.telegram_chat_id,  # Assuming chat_id maps to user_id
        db,
        request.is_voice_message,
        request.voice_file_path
    )
    
    return {"response": response}

@app.post("/assistant/reminders")
async def create_reminder(reminder_request: ReminderCreate, telegram_user_id: str, db: Session = Depends(get_db)):
    """Create personal reminder"""
    profile = db.query(PersonalAssistantProfile).filter(
        PersonalAssistantProfile.telegram_user_id == telegram_user_id
    ).first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    reminder = PersonalReminder(
        profile_id=profile.id,
        title=reminder_request.title,
        description=reminder_request.description,
        reminder_type=reminder_request.reminder_type,
        scheduled_at=reminder_request.scheduled_at,
        repeat_pattern=reminder_request.repeat_pattern,
        advance_notice_minutes=reminder_request.advance_notice_minutes,
        priority=reminder_request.priority
    )
    
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    
    return {"message": "Reminder created successfully", "reminder_id": str(reminder.id)}

@app.post("/assistant/tasks")
async def create_task(task_request: TaskCreate, telegram_user_id: str, db: Session = Depends(get_db)):
    """Create productivity task"""
    profile = db.query(PersonalAssistantProfile).filter(
        PersonalAssistantProfile.telegram_user_id == telegram_user_id
    ).first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    task = ProductivityTask(
        profile_id=profile.id,
        title=task_request.title,
        description=task_request.description,
        category=task_request.category,
        priority=task_request.priority,
        due_date=task_request.due_date,
        estimated_duration_minutes=task_request.estimated_duration_minutes
    )
    
    db.add(task)
    db.commit()
    db.refresh(task)
    
    return {"message": "Task created successfully", "task_id": str(task.id)}

@app.get("/health")
async def health_check():
    """Enhanced health check"""
    # Check database connection
    try:
        db = next(get_db())
        db.execute("SELECT 1")
        db_status = "healthy"
        db.close()
    except:
        db_status = "unhealthy"
    
    # Check existing telegram service
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:4006/health", timeout=5.0)
            telegram_status = "healthy" if response.status_code == 200 else "unhealthy"
    except:
        telegram_status = "unhealthy"
    
    return {
        "status": "healthy",
        "service": "Personal AI Assistant Telegram Service",
        "components": {
            "database": db_status,
            "telegram_service": telegram_status,
            "ai_assistant": "healthy",
            "voice_processor": "healthy"
        },
        "features": [
            "Personal AI Assistant with 88+ agents",
            "Multi-type assistant support (ElderCare, Productivity, Business)",
            "Voice message processing",
            "Telegram bot integration",
            "Task and reminder management",
            "Context-aware conversations",
            "Emergency contact system"
        ],
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4007, reload=True)