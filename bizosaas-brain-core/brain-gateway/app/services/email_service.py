import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class EmailService:
    """Service for sending emails."""
    
    @staticmethod
    async def send_email(template: str, recipient: str, subject: Optional[str] = None, context: Optional[Dict[str, Any]] = None):
        """Send an email."""
        logger.info(f"Sending email to {recipient} using template {template}")
        # Mock implementation
        return {"status": "sent", "recipient": recipient}

    @staticmethod
    async def send_alert_email(alerts: List[Any], recipient: str):
        """Send an alert email."""
        logger.info(f"Sending alert email with {len(alerts)} alerts to {recipient}")
        # Mock implementation
        return {"status": "sent", "recipient": recipient}

async def send_email(template: str, recipient: str, **kwargs):
    """Functional interface for sending emails."""
    return await EmailService.send_email(template, recipient, **kwargs)
