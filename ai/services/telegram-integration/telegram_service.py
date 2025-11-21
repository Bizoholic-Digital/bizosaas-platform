"""
Telegram Bot Integration Service for BizOSaaS Platform
Manages 5 active Telegram bots with real credentials from ~/projects/credentials.md
"""

import os
import asyncio
from typing import Dict, List, Any, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import httpx
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="BizOSaaS Telegram Integration Service",
    description="Multi-bot Telegram integration with real bot tokens",
    version="1.0.0"
)

# Bot Configuration with Real Tokens
TELEGRAM_BOTS = {
    "jonnyai": {
        "token": "7200437482:AAF8aE2uymF5ukm-ntlEnXx1hfhX1Obcfaw",
        "username": "jonnyaibot",
        "url": "t.me/jonnyaibot",
        "description": "AI Assistant Bot",
        "status": "active"
    },
    "bizoholic": {
        "token": "7767279872:AAGxwC7AcjSpkdF3xdvuLAw1gfXAplYLhMw",
        "username": "BizoholicAIBot", 
        "url": "t.me/BizoholicAIBot",
        "description": "BizOSaaS Marketing Bot",
        "status": "active"
    },
    "deals4all": {
        "token": "1217910149:AAHZwP0RnxcaqMheU08so6hpyXL7H8tZfYw",
        "username": "Deals4all_bot",
        "url": "t.me/Deals4all_bot", 
        "description": "Deals and Offers Bot",
        "status": "active"
    },
    "bottrader": {
        "token": "7780097136:AAELAgYZsfmBCTuYxwHvqoITqwVjKZp-u0Y",
        "username": "BottraderAdmin_bot",
        "url": "t.me/BottraderAdmin_bot",
        "description": "Trading Administration Bot",
        "status": "active"
    },
    "gogofather": {
        "token": "1011283832:AAHtpTljpQFhypOaQJwWei4z4Y5hgoMNSmk",
        "username": "go_go_fatherbot",
        "url": "t.me/go_go_fatherbot",
        "description": "General Purpose Bot",
        "status": "active"
    }
}

class TelegramMessage(BaseModel):
    bot_name: str
    chat_id: str
    text: str
    parse_mode: str = "HTML"

class TelegramResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict] = None

# ========================================================================================
# TELEGRAM API CLIENT
# ========================================================================================

class TelegramBotClient:
    def __init__(self, bot_name: str, token: str):
        self.bot_name = bot_name
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{token}"
        
    async def send_message(self, chat_id: str, text: str, parse_mode: str = "HTML") -> Dict:
        """Send message via Telegram Bot API"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": text,
                        "parse_mode": parse_mode
                    },
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    return {"success": True, "data": response.json()}
                else:
                    logger.error(f"Telegram API error for {self.bot_name}: {response.text}")
                    return {"success": False, "error": response.text}
                    
            except Exception as e:
                logger.error(f"Error sending message via {self.bot_name}: {e}")
                return {"success": False, "error": str(e)}
    
    async def get_bot_info(self) -> Dict:
        """Get bot information"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.base_url}/getMe", timeout=5.0)
                if response.status_code == 200:
                    return {"success": True, "data": response.json()}
                else:
                    return {"success": False, "error": response.text}
            except Exception as e:
                return {"success": False, "error": str(e)}
    
    async def get_updates(self, offset: int = 0) -> Dict:
        """Get bot updates"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/getUpdates",
                    params={"offset": offset, "limit": 10},
                    timeout=5.0
                )
                if response.status_code == 200:
                    return {"success": True, "data": response.json()}
                else:
                    return {"success": False, "error": response.text}
            except Exception as e:
                return {"success": False, "error": str(e)}

# Initialize bot clients
bot_clients = {}
for bot_name, config in TELEGRAM_BOTS.items():
    bot_clients[bot_name] = TelegramBotClient(bot_name, config["token"])

# ========================================================================================
# API ENDPOINTS
# ========================================================================================

@app.get("/health")
async def health_check():
    """Health check with bot status verification"""
    bot_status = {}
    
    for bot_name, client in bot_clients.items():
        info = await client.get_bot_info()
        bot_status[bot_name] = {
            "configured": True,
            "api_accessible": info["success"],
            "bot_info": info.get("data", {}).get("result", {}) if info["success"] else None
        }
    
    return {
        "status": "healthy",
        "service": "Telegram Integration Service",
        "bots_count": len(TELEGRAM_BOTS),
        "bots_status": bot_status,
        "features": [
            "Multi-bot messaging",
            "Real-time bot status",
            "Broadcast capabilities",
            "Bot information retrieval",
            "Update polling"
        ]
    }

@app.get("/bots")
async def get_bots_info():
    """Get information about all configured bots"""
    bots_info = []
    
    for bot_name, config in TELEGRAM_BOTS.items():
        client = bot_clients[bot_name]
        api_info = await client.get_bot_info()
        
        bot_data = {
            "name": bot_name,
            "username": config["username"],
            "url": config["url"],
            "description": config["description"],
            "status": config["status"],
            "api_accessible": api_info["success"]
        }
        
        if api_info["success"]:
            bot_result = api_info["data"]["result"]
            bot_data.update({
                "telegram_id": bot_result.get("id"),
                "first_name": bot_result.get("first_name"),
                "can_join_groups": bot_result.get("can_join_groups", False),
                "can_read_all_group_messages": bot_result.get("can_read_all_group_messages", False),
                "supports_inline_queries": bot_result.get("supports_inline_queries", False)
            })
        
        bots_info.append(bot_data)
    
    return {
        "bots": bots_info,
        "total_count": len(bots_info),
        "active_count": len([b for b in bots_info if b["api_accessible"]])
    }

@app.post("/send-message")
async def send_message(message: TelegramMessage) -> TelegramResponse:
    """Send message via specified bot"""
    
    if message.bot_name not in bot_clients:
        raise HTTPException(status_code=404, detail=f"Bot '{message.bot_name}' not found")
    
    client = bot_clients[message.bot_name]
    result = await client.send_message(message.chat_id, message.text, message.parse_mode)
    
    if result["success"]:
        return TelegramResponse(
            success=True,
            message=f"Message sent successfully via {message.bot_name}",
            data=result["data"]
        )
    else:
        raise HTTPException(status_code=400, detail=result["error"])

@app.post("/broadcast")
async def broadcast_message(
    text: str,
    chat_ids: List[str],
    bot_name: str = "bizoholic",
    parse_mode: str = "HTML"
):
    """Broadcast message to multiple chats via specified bot"""
    
    if bot_name not in bot_clients:
        raise HTTPException(status_code=404, detail=f"Bot '{bot_name}' not found")
    
    client = bot_clients[bot_name]
    results = []
    
    for chat_id in chat_ids:
        result = await client.send_message(chat_id, text, parse_mode)
        results.append({
            "chat_id": chat_id,
            "success": result["success"],
            "error": result.get("error")
        })
    
    successful = len([r for r in results if r["success"]])
    
    return {
        "broadcast_completed": True,
        "total_chats": len(chat_ids),
        "successful_sends": successful,
        "failed_sends": len(chat_ids) - successful,
        "results": results
    }

@app.get("/bot/{bot_name}/updates")
async def get_bot_updates(bot_name: str, offset: int = 0):
    """Get recent updates for a specific bot"""
    
    if bot_name not in bot_clients:
        raise HTTPException(status_code=404, detail=f"Bot '{bot_name}' not found")
    
    client = bot_clients[bot_name]
    result = await client.get_updates(offset)
    
    if result["success"]:
        updates = result["data"]["result"]
        return {
            "bot_name": bot_name,
            "updates_count": len(updates),
            "updates": updates,
            "next_offset": max([u["update_id"] + 1 for u in updates]) if updates else offset
        }
    else:
        raise HTTPException(status_code=400, detail=result["error"])

# ========================================================================================
# BIZOSAAS INTEGRATION ENDPOINTS
# ========================================================================================

@app.post("/marketing/send-campaign")
async def send_marketing_campaign(
    campaign_text: str,
    target_chats: List[str],
    bot_name: str = "bizoholic"
):
    """Send marketing campaign via BizOSaaS bot"""
    
    # Enhance message with BizOSaaS branding
    branded_message = f"""
🚀 <b>BizOSaaS Marketing Update</b> 🚀

{campaign_text}

━━━━━━━━━━━━━━━━━━━━
🎯 <i>Powered by BizOSaaS AI Marketing Platform</i>
🌐 Visit: bizoholic.com
"""
    
    return await broadcast_message(
        text=branded_message,
        chat_ids=target_chats,
        bot_name=bot_name,
        parse_mode="HTML"
    )

@app.post("/client-notification")
async def send_client_notification(
    client_name: str,
    notification_text: str,
    chat_id: str,
    bot_name: str = "bizoholic"
):
    """Send personalized client notification"""
    
    personalized_message = f"""
👋 Hi {client_name}!

{notification_text}

━━━━━━━━━━━━━━━━━━━━
📊 <i>Your BizOSaaS Dashboard: </i>
🔗 <a href="https://dashboard.bizoholic.com">Access Dashboard</a>

Need help? Reply to this message! 💬
"""
    
    message = TelegramMessage(
        bot_name=bot_name,
        chat_id=chat_id,
        text=personalized_message,
        parse_mode="HTML"
    )
    
    return await send_message(message)

@app.post("/deals-alert")
async def send_deals_alert(
    deal_title: str,
    deal_description: str,
    deal_link: str,
    target_chats: List[str]
):
    """Send deal alerts via Deals4All bot"""
    
    deal_message = f"""
🔥 <b>HOT DEAL ALERT!</b> 🔥

💰 <b>{deal_title}</b>

{deal_description}

🛒 <a href="{deal_link}">Get Deal Now!</a>

━━━━━━━━━━━━━━━━━━━━
⚡ <i>Limited Time Offer!</i>
📱 <i>via Deals4All Bot</i>
"""
    
    return await broadcast_message(
        text=deal_message,
        chat_ids=target_chats,
        bot_name="deals4all",
        parse_mode="HTML"
    )

# ========================================================================================
# WEBHOOK ENDPOINT (for receiving updates)
# ========================================================================================

@app.post("/webhook/{bot_name}")
async def telegram_webhook(bot_name: str, update: Dict):
    """Handle incoming Telegram updates via webhook"""
    
    if bot_name not in TELEGRAM_BOTS:
        raise HTTPException(status_code=404, detail="Bot not found")
    
    logger.info(f"Received webhook update for {bot_name}: {update}")
    
    # Process the update (implement your logic here)
    if "message" in update:
        message = update["message"]
        chat_id = message["chat"]["id"]
        text = message.get("text", "")
        
        # Example: Auto-reply to certain messages
        if "hello" in text.lower():
            response_text = f"Hello! This is {bot_name} from BizOSaaS platform. How can I help you today?"
            
            client = bot_clients[bot_name]
            await client.send_message(str(chat_id), response_text)
    
    return {"status": "ok", "processed": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4006, reload=True)