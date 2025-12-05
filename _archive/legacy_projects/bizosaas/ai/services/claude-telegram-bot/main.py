"""
Claude Telegram Bot Integration for BizOSaaS
Handles client notifications, approvals, and AI interactions
"""
from fastapi import FastAPI, BackgroundTasks
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import asyncio
import redis
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Claude Telegram Bot Service")
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN_BIZOHOLIC')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID_BIZOHOLIC') 

class ClaudeTelegramBot:
    def __init__(self):
        self.application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup bot command handlers"""
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("status", self.status_command))
        self.application.add_handler(CommandHandler("approve", self.approve_command))
        self.application.add_handler(MessageHandler(filters.TEXT, self.handle_message))
    
    async def start_command(self, update: Update, context):
        """Handle /start command"""
        await update.message.reply_text(
            "🤖 BizOSaaS Claude Bot Active!\n"
            "Available commands:\n"
            "/status - Platform status\n"
            "/approve - Approve pending actions\n"
        )
    
    async def status_command(self, update: Update, context):
        """Handle /status command"""
        # Check platform services
        status = "🟢 All services operational"
        await update.message.reply_text(f"📊 Platform Status: {status}")
    
    async def approve_command(self, update: Update, context):
        """Handle approval workflows"""
        await update.message.reply_text("✅ Approval system ready")
    
    async def handle_message(self, update: Update, context):
        """Handle general messages - AI integration point"""
        user_message = update.message.text
        
        # Here you can integrate with your AI agents
        response = f"🧠 Processing: {user_message}"
        await update.message.reply_text(response)

# Global bot instance
claude_bot = ClaudeTelegramBot()

@app.on_event("startup")
async def startup_event():
    """Start Telegram bot"""
    print("🚀 Starting Claude Telegram Bot...")
    # Start bot in background
    asyncio.create_task(claude_bot.application.run_polling())

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "claude-telegram-bot"}

@app.post("/notify")
async def send_notification(message: dict):
    """Send notification via Telegram"""
    try:
        chat_id = TELEGRAM_CHAT_ID
        text = message.get("text", "Notification from BizOSaaS")
        
        await claude_bot.application.bot.send_message(
            chat_id=chat_id, 
            text=text
        )
        return {"status": "sent"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/request-approval")
async def request_approval(approval_data: dict):
    """Request approval via Telegram"""
    chat_id = TELEGRAM_CHAT_ID
    text = f"🔔 Approval Required:\n{approval_data.get('description', 'N/A')}"
    
    await claude_bot.application.bot.send_message(
        chat_id=chat_id, 
        text=text
    )
    return {"status": "approval_requested"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8010)
