import logging
from typing import Optional

logger = logging.getLogger(__name__)

async def send_sms(message: str, phone: str):
    """Send an SMS message."""
    logger.info(f"Sending SMS to {phone}: {message[:20]}...")
    # Mock implementation
    return {"status": "sent", "phone": phone}
