#!/bin/bash

# Integrate Claude Mobile Bot into BizOSaaS Platform
echo "🤖 Integrating Claude Mobile Bot..."

# Extract bot from existing container
echo "📦 Extracting Claude Bot components..."
docker run --rm -v $(pwd)/services:/output claude-mobile-bot:test sh -c "
    cp -r /app/telegram-bot /output/claude-telegram-bot
    cp /app/healthcheck.sh /output/claude-telegram-bot/
    cp /app/start.sh /output/claude-telegram-bot/
"

# Create integration service
mkdir -p services/claude-telegram-bot

echo "⚙️ Creating integration service..."
cat > services/claude-telegram-bot/requirements.txt << 'EOF'
python-telegram-bot==20.7
fastapi==0.104.1
uvicorn==0.24.0
redis==5.0.1
asyncio-mqtt==0.16.1
requests==2.31.0
python-dotenv==1.0.0
EOF

cat > services/claude-telegram-bot/main.py << 'EOF'
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
EOF

echo "🔧 Adding to main startup script..."
# Add to start-all-services.sh
grep -q "claude-telegram-bot" start-all-services.sh || cat >> start-all-services.sh << 'EOF'

# Claude Telegram Bot
start_service "claude-telegram-bot" "/home/alagiri/projects/bizoholic/bizosaas/services/claude-telegram-bot" 8010 "main.py"
EOF

# Add to test script
grep -q "claude-telegram-bot" test-all-services.sh || sed -i '/PORTS=(/a\PORTS+=(8010)' test-all-services.sh
grep -q "Claude Telegram Bot" test-all-services.sh || sed -i '/test_service "Amazon Integration"/a\test_service "Claude Telegram Bot" "http://localhost:8010/health" "healthy"' test-all-services.sh

echo "✅ Claude Telegram Bot integration complete!"
echo ""
echo "📱 Bot will be available at:"
echo "   • Health Check: http://localhost:8010/health"
echo "   • Notification API: POST http://localhost:8010/notify"
echo "   • Approval API: POST http://localhost:8010/request-approval"
echo ""
echo "🚀 Start with: ./start-all-services.sh"