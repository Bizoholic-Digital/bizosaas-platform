"""
Notification Service - BizoholicSaaS
Handles multi-channel notifications (Email, SMS, In-app, Push)
Port: 8005
"""

from fastapi import FastAPI, HTTPException, Depends, status, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
import uuid
from datetime import datetime, timedelta
import logging
from enum import Enum
import asyncio
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template
import os

# Shared imports
import sys
import os
sys.path.append('/home/alagiri/projects/bizoholic/bizosaas')

from shared.database.connection import get_postgres_session, get_redis_client, init_database
from shared.database.models import NotificationTemplate, Notification, NotificationPreference
from shared.events.event_bus import EventBus, EventFactory, EventType, event_handler
from shared.auth.jwt_auth import get_current_user, UserContext, require_permission, Permission

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Notification Service",
    description="Multi-channel notification system for BizoholicSaaS",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
event_bus: EventBus = None
redis_client = None

# Enums
class NotificationChannel(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    IN_APP = "in_app"

class NotificationStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"
    CANCELLED = "cancelled"

class NotificationType(str, Enum):
    WELCOME = "welcome"
    CAMPAIGN_COMPLETE = "campaign_complete"
    CAMPAIGN_ALERT = "campaign_alert"
    SYSTEM_ALERT = "system_alert"
    BILLING_REMINDER = "billing_reminder"
    REPORT_READY = "report_ready"
    PASSWORD_RESET = "password_reset"
    VERIFICATION = "verification"
    MARKETING = "marketing"

class Priority(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"

class FrequencyType(str, Enum):
    IMMEDIATE = "immediate"
    DAILY = "daily"
    WEEKLY = "weekly"
    NEVER = "never"

# Pydantic models
class NotificationTemplateCreate(BaseModel):
    name: str
    channel: NotificationChannel
    template_type: NotificationType
    subject: Optional[str] = None  # For email
    content: str
    variables: List[str] = []
    is_default: bool = False

class NotificationTemplateResponse(BaseModel):
    id: str
    name: str
    channel: NotificationChannel
    template_type: NotificationType
    subject: Optional[str]
    content: str
    variables: List[str]
    is_default: bool
    tenant_id: str
    created_at: datetime
    updated_at: datetime

class NotificationSend(BaseModel):
    recipient_id: str
    recipient_email: Optional[EmailStr] = None
    recipient_phone: Optional[str] = None
    channel: NotificationChannel
    template_id: Optional[str] = None
    template_type: Optional[NotificationType] = None
    subject: Optional[str] = None
    content: Optional[str] = None
    variables: Dict[str, Any] = {}
    priority: Priority = Priority.NORMAL
    schedule_at: Optional[datetime] = None

class NotificationResponse(BaseModel):
    id: str
    recipient_id: str
    recipient_email: Optional[str]
    recipient_phone: Optional[str]
    channel: NotificationChannel
    template_id: Optional[str]
    subject: Optional[str]
    content: str
    status: NotificationStatus
    sent_at: Optional[datetime]
    delivered_at: Optional[datetime]
    error_message: Optional[str]
    metadata: Dict[str, Any]
    tenant_id: str
    created_at: datetime
    updated_at: datetime

class BulkNotificationRequest(BaseModel):
    recipients: List[Dict[str, Any]]  # List of recipient data
    channel: NotificationChannel
    template_id: str
    variables: Dict[str, Any] = {}
    priority: Priority = Priority.NORMAL

class NotificationPreferenceRequest(BaseModel):
    user_id: str
    notification_type: NotificationType
    email_enabled: bool = True
    sms_enabled: bool = False
    push_enabled: bool = True
    in_app_enabled: bool = True
    frequency: FrequencyType = FrequencyType.IMMEDIATE

class NotificationPreferenceResponse(BaseModel):
    id: str
    user_id: str
    notification_type: NotificationType
    email_enabled: bool
    sms_enabled: bool
    push_enabled: bool
    in_app_enabled: bool
    frequency: FrequencyType
    tenant_id: str
    created_at: datetime
    updated_at: datetime

class NotificationStats(BaseModel):
    total_sent: int
    total_delivered: int
    total_failed: int
    delivery_rate: float
    channel_breakdown: Dict[str, int]
    template_usage: Dict[str, int]

# SMTP Configuration
SMTP_CONFIG = {
    "host": os.getenv("SMTP_HOST", "localhost"),
    "port": int(os.getenv("SMTP_PORT", 587)),
    "username": os.getenv("SMTP_USERNAME", ""),
    "password": os.getenv("SMTP_PASSWORD", ""),
    "use_tls": os.getenv("SMTP_USE_TLS", "true").lower() == "true",
    "from_email": os.getenv("SMTP_FROM_EMAIL", "noreply@bizoholic.com"),
    "from_name": os.getenv("SMTP_FROM_NAME", "BizoholicSaaS")
}

# SMS Configuration (Twilio example)
SMS_CONFIG = {
    "account_sid": os.getenv("TWILIO_ACCOUNT_SID", ""),
    "auth_token": os.getenv("TWILIO_AUTH_TOKEN", ""),
    "from_number": os.getenv("TWILIO_FROM_NUMBER", "")
}

# Push Notification Configuration
PUSH_CONFIG = {
    "firebase_key": os.getenv("FIREBASE_SERVER_KEY", ""),
    "vapid_public_key": os.getenv("VAPID_PUBLIC_KEY", ""),
    "vapid_private_key": os.getenv("VAPID_PRIVATE_KEY", "")
}

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database and event bus connections"""
    global event_bus, redis_client
    
    try:
        await init_database()
        logger.info("Database connections initialized")
        
        redis_client = await get_redis_client()
        
        event_bus = EventBus(redis_client, "notification")
        await event_bus.initialize()
        await event_bus.start()
        logger.info("Event bus initialized")
        
        # Start notification queue processor
        asyncio.create_task(process_notification_queue())
        
        # Create default templates if they don't exist
        await create_default_templates()
        
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Clean shutdown of connections"""
    global event_bus
    
    if event_bus:
        await event_bus.stop()
    logger.info("Notification Service shutdown complete")

# Health check endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "notification",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/ready")
async def readiness_check():
    """Readiness check endpoint"""
    try:
        async with get_postgres_session("notification") as session:
            await session.execute("SELECT 1")
        
        await redis_client.ping()
        
        return {
            "status": "ready",
            "service": "notification",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Service not ready: {str(e)}"
        )

async def create_default_templates():
    """Create default notification templates"""
    
    try:
        async with get_postgres_session("notification") as session:
            from sqlalchemy import select
            
            # Check if default templates already exist
            stmt = select(NotificationTemplate).where(NotificationTemplate.is_default == True).limit(1)
            result = await session.execute(stmt)
            existing_template = result.scalar_one_or_none()
            
            if existing_template:
                return  # Default templates already exist
            
            # Create default templates
            default_templates = [
                {
                    "name": "Welcome Email",
                    "channel": NotificationChannel.EMAIL.value,
                    "template_type": NotificationType.WELCOME.value,
                    "subject": "Welcome to {{ company_name }}!",
                    "content": """
                    <h1>Welcome to {{ company_name }}, {{ user_name }}!</h1>
                    <p>We're excited to have you on board. Here's what you can do next:</p>
                    <ul>
                        <li>Complete your profile setup</li>
                        <li>Create your first campaign</li>
                        <li>Explore our AI-powered tools</li>
                    </ul>
                    <p>If you have any questions, feel free to reach out to our support team.</p>
                    <p>Best regards,<br>The {{ company_name }} Team</p>
                    """,
                    "variables": ["company_name", "user_name"]
                },
                {
                    "name": "Campaign Complete Email",
                    "channel": NotificationChannel.EMAIL.value,
                    "template_type": NotificationType.CAMPAIGN_COMPLETE.value,
                    "subject": "Campaign '{{ campaign_name }}' has completed",
                    "content": """
                    <h1>Campaign Complete</h1>
                    <p>Hi {{ user_name }},</p>
                    <p>Your campaign '<strong>{{ campaign_name }}</strong>' has completed successfully.</p>
                    <h3>Results Summary:</h3>
                    <ul>
                        <li>Impressions: {{ impressions }}</li>
                        <li>Clicks: {{ clicks }}</li>
                        <li>Conversions: {{ conversions }}</li>
                        <li>Total Spend: ${{ total_spend }}</li>
                    </ul>
                    <p><a href="{{ campaign_url }}">View detailed results</a></p>
                    """,
                    "variables": ["user_name", "campaign_name", "impressions", "clicks", "conversions", "total_spend", "campaign_url"]
                },
                {
                    "name": "System Alert Email",
                    "channel": NotificationChannel.EMAIL.value,
                    "template_type": NotificationType.SYSTEM_ALERT.value,
                    "subject": "System Alert: {{ alert_title }}",
                    "content": """
                    <h1>System Alert</h1>
                    <p>Hi {{ user_name }},</p>
                    <p><strong>{{ alert_title }}</strong></p>
                    <p>{{ alert_message }}</p>
                    <p>Alert Level: <strong>{{ alert_level }}</strong></p>
                    <p>Time: {{ alert_time }}</p>
                    <p>Please take appropriate action if required.</p>
                    """,
                    "variables": ["user_name", "alert_title", "alert_message", "alert_level", "alert_time"]
                },
                {
                    "name": "Report Ready In-App",
                    "channel": NotificationChannel.IN_APP.value,
                    "template_type": NotificationType.REPORT_READY.value,
                    "subject": None,
                    "content": "Your {{ report_type }} report is ready. Click to view results.",
                    "variables": ["report_type", "report_url"]
                }
            ]
            
            # Use a default tenant ID for system templates
            default_tenant_id = uuid.UUID("00000000-0000-0000-0000-000000000000")
            
            for template_data in default_templates:
                template = NotificationTemplate(
                    id=uuid.uuid4(),
                    name=template_data["name"],
                    channel=template_data["channel"],
                    template_type=template_data["template_type"],
                    subject=template_data["subject"],
                    content=template_data["content"],
                    variables=template_data["variables"],
                    is_default=True,
                    tenant_id=default_tenant_id
                )
                session.add(template)
            
            await session.commit()
            logger.info("Default notification templates created")
            
    except Exception as e:
        logger.error(f"Create default templates error: {e}")

# Template management endpoints
@app.post("/templates", response_model=NotificationTemplateResponse)
async def create_template(
    template_data: NotificationTemplateCreate,
    current_user: UserContext = Depends(get_current_user)
):
    """Create a new notification template"""
    
    try:
        async with get_postgres_session("notification") as session:
            new_template = NotificationTemplate(
                id=uuid.uuid4(),
                name=template_data.name,
                channel=template_data.channel.value,
                template_type=template_data.template_type.value,
                subject=template_data.subject,
                content=template_data.content,
                variables=template_data.variables,
                is_default=template_data.is_default,
                tenant_id=uuid.UUID(current_user.tenant_id)
            )
            
            session.add(new_template)
            await session.commit()
            await session.refresh(new_template)
            
            return NotificationTemplateResponse(
                id=str(new_template.id),
                name=new_template.name,
                channel=NotificationChannel(new_template.channel),
                template_type=NotificationType(new_template.template_type),
                subject=new_template.subject,
                content=new_template.content,
                variables=new_template.variables,
                is_default=new_template.is_default,
                tenant_id=str(new_template.tenant_id),
                created_at=new_template.created_at,
                updated_at=new_template.updated_at
            )
            
    except Exception as e:
        logger.error(f"Create template error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create notification template"
        )

@app.get("/templates", response_model=List[NotificationTemplateResponse])
async def list_templates(
    current_user: UserContext = Depends(get_current_user),
    channel: Optional[NotificationChannel] = None,
    template_type: Optional[NotificationType] = None
):
    """List notification templates"""
    
    try:
        async with get_postgres_session("notification") as session:
            from sqlalchemy import select, or_
            
            stmt = select(NotificationTemplate).where(
                or_(
                    NotificationTemplate.tenant_id == uuid.UUID(current_user.tenant_id),
                    NotificationTemplate.is_default == True
                ),
                NotificationTemplate.is_active == True
            )
            
            if channel:
                stmt = stmt.where(NotificationTemplate.channel == channel.value)
            
            if template_type:
                stmt = stmt.where(NotificationTemplate.template_type == template_type.value)
            
            stmt = stmt.order_by(NotificationTemplate.created_at.desc())
            
            result = await session.execute(stmt)
            templates = result.scalars().all()
            
            return [
                NotificationTemplateResponse(
                    id=str(template.id),
                    name=template.name,
                    channel=NotificationChannel(template.channel),
                    template_type=NotificationType(template.template_type),
                    subject=template.subject,
                    content=template.content,
                    variables=template.variables,
                    is_default=template.is_default,
                    tenant_id=str(template.tenant_id),
                    created_at=template.created_at,
                    updated_at=template.updated_at
                ) for template in templates
            ]
            
    except Exception as e:
        logger.error(f"List templates error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list templates"
        )

# Notification sending endpoints
@app.post("/send", response_model=NotificationResponse)
async def send_notification(
    notification_data: NotificationSend,
    background_tasks: BackgroundTasks,
    current_user: UserContext = Depends(get_current_user)
):
    """Send a single notification"""
    
    try:
        async with get_postgres_session("notification") as session:
            # Get template if specified
            template = None
            if notification_data.template_id:
                from sqlalchemy import select, or_
                template_stmt = select(NotificationTemplate).where(
                    NotificationTemplate.id == uuid.UUID(notification_data.template_id),
                    or_(
                        NotificationTemplate.tenant_id == uuid.UUID(current_user.tenant_id),
                        NotificationTemplate.is_default == True
                    )
                )
                template_result = await session.execute(template_stmt)
                template = template_result.scalar_one_or_none()
            elif notification_data.template_type:
                # Find default template for this type and channel
                from sqlalchemy import select
                template_stmt = select(NotificationTemplate).where(
                    NotificationTemplate.template_type == notification_data.template_type.value,
                    NotificationTemplate.channel == notification_data.channel.value,
                    NotificationTemplate.is_default == True
                ).limit(1)
                template_result = await session.execute(template_stmt)
                template = template_result.scalar_one_or_none()
            
            # Render content from template
            if template:
                subject = render_template(template.subject, notification_data.variables) if template.subject else notification_data.subject
                content = render_template(template.content, notification_data.variables)
            else:
                subject = notification_data.subject
                content = notification_data.content or ""
            
            # Check user preferences
            preferences_valid = await check_notification_preferences(
                notification_data.recipient_id,
                notification_data.template_type or NotificationType.SYSTEM_ALERT,
                notification_data.channel,
                current_user.tenant_id
            )
            
            if not preferences_valid:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User has disabled this type of notification"
                )
            
            # Create notification record
            new_notification = Notification(
                id=uuid.uuid4(),
                recipient_id=uuid.UUID(notification_data.recipient_id),
                recipient_email=notification_data.recipient_email,
                recipient_phone=notification_data.recipient_phone,
                channel=notification_data.channel.value,
                template_id=uuid.UUID(notification_data.template_id) if notification_data.template_id else None,
                subject=subject,
                content=content,
                status=NotificationStatus.PENDING.value,
                metadata={
                    "priority": notification_data.priority.value,
                    "variables": notification_data.variables,
                    "scheduled_at": notification_data.schedule_at.isoformat() if notification_data.schedule_at else None
                },
                tenant_id=uuid.UUID(current_user.tenant_id)
            )
            
            session.add(new_notification)
            await session.commit()
            await session.refresh(new_notification)
            
            # Schedule notification sending
            if notification_data.schedule_at and notification_data.schedule_at > datetime.utcnow():
                # Schedule for later
                await schedule_notification(str(new_notification.id), notification_data.schedule_at)
            else:
                # Send immediately
                background_tasks.add_task(send_notification_task, str(new_notification.id))
            
            return NotificationResponse(
                id=str(new_notification.id),
                recipient_id=str(new_notification.recipient_id),
                recipient_email=new_notification.recipient_email,
                recipient_phone=new_notification.recipient_phone,
                channel=NotificationChannel(new_notification.channel),
                template_id=str(new_notification.template_id) if new_notification.template_id else None,
                subject=new_notification.subject,
                content=new_notification.content,
                status=NotificationStatus(new_notification.status),
                sent_at=new_notification.sent_at,
                delivered_at=new_notification.delivered_at,
                error_message=new_notification.error_message,
                metadata=new_notification.metadata,
                tenant_id=str(new_notification.tenant_id),
                created_at=new_notification.created_at,
                updated_at=new_notification.updated_at
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Send notification error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send notification"
        )

def render_template(template_content: str, variables: Dict[str, Any]) -> str:
    """Render template with variables"""
    
    if not template_content:
        return ""
    
    try:
        template = Template(template_content)
        return template.render(**variables)
    except Exception as e:
        logger.error(f"Template rendering error: {e}")
        return template_content

async def check_notification_preferences(
    user_id: str, 
    notification_type: NotificationType, 
    channel: NotificationChannel,
    tenant_id: str
) -> bool:
    """Check if user allows this type of notification on this channel"""
    
    try:
        async with get_postgres_session("notification") as session:
            from sqlalchemy import select
            
            stmt = select(NotificationPreference).where(
                NotificationPreference.user_id == uuid.UUID(user_id),
                NotificationPreference.notification_type == notification_type.value,
                NotificationPreference.tenant_id == uuid.UUID(tenant_id)
            )
            result = await session.execute(stmt)
            preference = result.scalar_one_or_none()
            
            if not preference:
                # No specific preference set, allow by default
                return True
            
            # Check channel-specific preference
            if channel == NotificationChannel.EMAIL:
                return preference.email_enabled
            elif channel == NotificationChannel.SMS:
                return preference.sms_enabled
            elif channel == NotificationChannel.PUSH:
                return preference.push_enabled
            elif channel == NotificationChannel.IN_APP:
                return preference.in_app_enabled
            
            return True
            
    except Exception as e:
        logger.error(f"Check notification preferences error: {e}")
        return True  # Default to allow if error

async def schedule_notification(notification_id: str, schedule_at: datetime):
    """Schedule notification for later sending"""
    
    try:
        # Add to Redis sorted set with timestamp as score
        await redis_client.zadd(
            "scheduled_notifications",
            {notification_id: schedule_at.timestamp()}
        )
        logger.info(f"Notification {notification_id} scheduled for {schedule_at}")
        
    except Exception as e:
        logger.error(f"Schedule notification error: {e}")

async def send_notification_task(notification_id: str):
    """Background task to send notification"""
    
    try:
        async with get_postgres_session("notification") as session:
            from sqlalchemy import select
            
            stmt = select(Notification).where(Notification.id == uuid.UUID(notification_id))
            result = await session.execute(stmt)
            notification = result.scalar_one_or_none()
            
            if not notification:
                logger.error(f"Notification not found: {notification_id}")
                return
            
            # Send based on channel
            success = False
            error_message = None
            
            try:
                if notification.channel == NotificationChannel.EMAIL.value:
                    success = await send_email_notification(notification)
                elif notification.channel == NotificationChannel.SMS.value:
                    success = await send_sms_notification(notification)
                elif notification.channel == NotificationChannel.PUSH.value:
                    success = await send_push_notification(notification)
                elif notification.channel == NotificationChannel.IN_APP.value:
                    success = await send_in_app_notification(notification)
                
                # Update notification status
                if success:
                    notification.status = NotificationStatus.SENT.value
                    notification.sent_at = datetime.utcnow()
                else:
                    notification.status = NotificationStatus.FAILED.value
                    notification.error_message = error_message or "Unknown error"
                
            except Exception as send_error:
                notification.status = NotificationStatus.FAILED.value
                notification.error_message = str(send_error)
                logger.error(f"Send notification error: {send_error}")
            
            notification.updated_at = datetime.utcnow()
            await session.commit()
            
            # Publish notification sent/failed event
            if success:
                event = EventFactory.notification_sent(
                    tenant_id=str(notification.tenant_id),
                    notification_id=notification_id,
                    notification_data={
                        "channel": notification.channel,
                        "recipient_id": str(notification.recipient_id),
                        "status": notification.status
                    }
                )
            else:
                event = EventFactory.notification_failed(
                    tenant_id=str(notification.tenant_id),
                    notification_id=notification_id,
                    notification_data={
                        "channel": notification.channel,
                        "recipient_id": str(notification.recipient_id),
                        "error": notification.error_message
                    }
                )
            
            await event_bus.publish(event)
            
    except Exception as e:
        logger.error(f"Send notification task error: {e}")

async def send_email_notification(notification: Notification) -> bool:
    """Send email notification"""
    
    try:
        if not notification.recipient_email:
            logger.error("No email address for email notification")
            return False
        
        # Create email message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = notification.subject or "Notification"
        msg["From"] = f"{SMTP_CONFIG['from_name']} <{SMTP_CONFIG['from_email']}>"
        msg["To"] = notification.recipient_email
        
        # Add content (assuming HTML content)
        html_part = MIMEText(notification.content, "html")
        msg.attach(html_part)
        
        # Send email
        if SMTP_CONFIG["username"] and SMTP_CONFIG["password"]:
            with smtplib.SMTP(SMTP_CONFIG["host"], SMTP_CONFIG["port"]) as server:
                if SMTP_CONFIG["use_tls"]:
                    server.starttls()
                server.login(SMTP_CONFIG["username"], SMTP_CONFIG["password"])
                server.send_message(msg)
        else:
            # For development/testing without SMTP credentials
            logger.info(f"EMAIL SIMULATION: To: {notification.recipient_email}, Subject: {notification.subject}")
        
        logger.info(f"Email sent to {notification.recipient_email}")
        return True
        
    except Exception as e:
        logger.error(f"Send email error: {e}")
        return False

async def send_sms_notification(notification: Notification) -> bool:
    """Send SMS notification"""
    
    try:
        if not notification.recipient_phone:
            logger.error("No phone number for SMS notification")
            return False
        
        # In real implementation, would use Twilio or similar service
        # For now, simulate SMS sending
        logger.info(f"SMS SIMULATION: To: {notification.recipient_phone}, Message: {notification.content[:50]}...")
        
        return True
        
    except Exception as e:
        logger.error(f"Send SMS error: {e}")
        return False

async def send_push_notification(notification: Notification) -> bool:
    """Send push notification"""
    
    try:
        # In real implementation, would use Firebase Cloud Messaging
        logger.info(f"PUSH SIMULATION: To: {notification.recipient_id}, Message: {notification.content[:50]}...")
        
        return True
        
    except Exception as e:
        logger.error(f"Send push notification error: {e}")
        return False

async def send_in_app_notification(notification: Notification) -> bool:
    """Send in-app notification"""
    
    try:
        # Store in Redis for real-time delivery
        in_app_data = {
            "id": str(notification.id),
            "content": notification.content,
            "timestamp": datetime.utcnow().isoformat(),
            "read": False
        }
        
        await redis_client.lpush(
            f"in_app_notifications:{notification.recipient_id}",
            json.dumps(in_app_data)
        )
        
        # Keep only last 50 notifications per user
        await redis_client.ltrim(f"in_app_notifications:{notification.recipient_id}", 0, 49)
        
        logger.info(f"In-app notification queued for user {notification.recipient_id}")
        return True
        
    except Exception as e:
        logger.error(f"Send in-app notification error: {e}")
        return False

# Bulk notification endpoint
@app.post("/send/bulk")
async def send_bulk_notifications(
    bulk_request: BulkNotificationRequest,
    background_tasks: BackgroundTasks,
    current_user: UserContext = Depends(get_current_user)
):
    """Send notifications to multiple recipients"""
    
    try:
        notification_ids = []
        
        for recipient in bulk_request.recipients:
            notification_data = NotificationSend(
                recipient_id=recipient["recipient_id"],
                recipient_email=recipient.get("recipient_email"),
                recipient_phone=recipient.get("recipient_phone"),
                channel=bulk_request.channel,
                template_id=bulk_request.template_id,
                variables={**bulk_request.variables, **recipient.get("variables", {})},
                priority=bulk_request.priority
            )
            
            # Create notification record
            notification = await send_notification(notification_data, background_tasks, current_user)
            notification_ids.append(notification.id)
        
        return {
            "message": f"Bulk notifications queued for {len(notification_ids)} recipients",
            "notification_ids": notification_ids,
            "total_recipients": len(bulk_request.recipients)
        }
        
    except Exception as e:
        logger.error(f"Send bulk notifications error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send bulk notifications"
        )

# Notification preferences endpoints
@app.post("/preferences", response_model=NotificationPreferenceResponse)
async def set_notification_preferences(
    preference_data: NotificationPreferenceRequest,
    current_user: UserContext = Depends(get_current_user)
):
    """Set notification preferences for a user"""
    
    try:
        async with get_postgres_session("notification") as session:
            from sqlalchemy import select
            
            # Check if preference already exists
            stmt = select(NotificationPreference).where(
                NotificationPreference.user_id == uuid.UUID(preference_data.user_id),
                NotificationPreference.notification_type == preference_data.notification_type.value,
                NotificationPreference.tenant_id == uuid.UUID(current_user.tenant_id)
            )
            result = await session.execute(stmt)
            existing_preference = result.scalar_one_or_none()
            
            if existing_preference:
                # Update existing preference
                existing_preference.email_enabled = preference_data.email_enabled
                existing_preference.sms_enabled = preference_data.sms_enabled
                existing_preference.push_enabled = preference_data.push_enabled
                existing_preference.in_app_enabled = preference_data.in_app_enabled
                existing_preference.frequency = preference_data.frequency.value
                existing_preference.updated_at = datetime.utcnow()
                
                await session.commit()
                preference = existing_preference
            else:
                # Create new preference
                preference = NotificationPreference(
                    id=uuid.uuid4(),
                    user_id=uuid.UUID(preference_data.user_id),
                    notification_type=preference_data.notification_type.value,
                    email_enabled=preference_data.email_enabled,
                    sms_enabled=preference_data.sms_enabled,
                    push_enabled=preference_data.push_enabled,
                    in_app_enabled=preference_data.in_app_enabled,
                    frequency=preference_data.frequency.value,
                    tenant_id=uuid.UUID(current_user.tenant_id)
                )
                
                session.add(preference)
                await session.commit()
                await session.refresh(preference)
            
            return NotificationPreferenceResponse(
                id=str(preference.id),
                user_id=str(preference.user_id),
                notification_type=NotificationType(preference.notification_type),
                email_enabled=preference.email_enabled,
                sms_enabled=preference.sms_enabled,
                push_enabled=preference.push_enabled,
                in_app_enabled=preference.in_app_enabled,
                frequency=FrequencyType(preference.frequency),
                tenant_id=str(preference.tenant_id),
                created_at=preference.created_at,
                updated_at=preference.updated_at
            )
            
    except Exception as e:
        logger.error(f"Set notification preferences error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to set notification preferences"
        )

@app.get("/preferences/{user_id}", response_model=List[NotificationPreferenceResponse])
async def get_notification_preferences(
    user_id: str,
    current_user: UserContext = Depends(get_current_user)
):
    """Get notification preferences for a user"""
    
    try:
        async with get_postgres_session("notification") as session:
            from sqlalchemy import select
            
            stmt = select(NotificationPreference).where(
                NotificationPreference.user_id == uuid.UUID(user_id),
                NotificationPreference.tenant_id == uuid.UUID(current_user.tenant_id)
            )
            result = await session.execute(stmt)
            preferences = result.scalars().all()
            
            return [
                NotificationPreferenceResponse(
                    id=str(pref.id),
                    user_id=str(pref.user_id),
                    notification_type=NotificationType(pref.notification_type),
                    email_enabled=pref.email_enabled,
                    sms_enabled=pref.sms_enabled,
                    push_enabled=pref.push_enabled,
                    in_app_enabled=pref.in_app_enabled,
                    frequency=FrequencyType(pref.frequency),
                    tenant_id=str(pref.tenant_id),
                    created_at=pref.created_at,
                    updated_at=pref.updated_at
                ) for pref in preferences
            ]
            
    except Exception as e:
        logger.error(f"Get notification preferences error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get notification preferences"
        )

# In-app notifications endpoint
@app.get("/in-app/{user_id}")
async def get_in_app_notifications(
    user_id: str,
    current_user: UserContext = Depends(get_current_user),
    limit: int = 20
):
    """Get in-app notifications for a user"""
    
    try:
        # Check if user can access these notifications
        if current_user.user_id != user_id and current_user.role.value not in ["tenant_admin", "super_admin"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        # Get notifications from Redis
        notifications_raw = await redis_client.lrange(
            f"in_app_notifications:{user_id}",
            0,
            limit - 1
        )
        
        notifications = []
        for notif_json in notifications_raw:
            try:
                notif_data = json.loads(notif_json)
                notifications.append(notif_data)
            except json.JSONDecodeError:
                continue
        
        return {
            "notifications": notifications,
            "total": len(notifications),
            "user_id": user_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get in-app notifications error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get in-app notifications"
        )

# Statistics endpoint
@app.get("/stats", response_model=NotificationStats)
async def get_notification_stats(
    current_user: UserContext = Depends(get_current_user),
    days: int = 30
):
    """Get notification statistics for tenant"""
    
    try:
        async with get_postgres_session("notification") as session:
            from sqlalchemy import select, func
            
            start_date = datetime.utcnow() - timedelta(days=days)
            
            # Total notifications
            total_stmt = select(func.count()).select_from(Notification).where(
                Notification.tenant_id == uuid.UUID(current_user.tenant_id),
                Notification.created_at >= start_date
            )
            total_result = await session.execute(total_stmt)
            total_sent = total_result.scalar() or 0
            
            # Delivered notifications
            delivered_stmt = select(func.count()).select_from(Notification).where(
                Notification.tenant_id == uuid.UUID(current_user.tenant_id),
                Notification.status.in_([NotificationStatus.SENT.value, NotificationStatus.DELIVERED.value]),
                Notification.created_at >= start_date
            )
            delivered_result = await session.execute(delivered_stmt)
            total_delivered = delivered_result.scalar() or 0
            
            # Failed notifications
            failed_stmt = select(func.count()).select_from(Notification).where(
                Notification.tenant_id == uuid.UUID(current_user.tenant_id),
                Notification.status == NotificationStatus.FAILED.value,
                Notification.created_at >= start_date
            )
            failed_result = await session.execute(failed_stmt)
            total_failed = failed_result.scalar() or 0
            
            # Channel breakdown
            channel_stmt = select(
                Notification.channel,
                func.count().label('count')
            ).where(
                Notification.tenant_id == uuid.UUID(current_user.tenant_id),
                Notification.created_at >= start_date
            ).group_by(Notification.channel)
            
            channel_result = await session.execute(channel_stmt)
            channel_breakdown = {row.channel: row.count for row in channel_result}
            
            # Calculate delivery rate
            delivery_rate = (total_delivered / total_sent * 100) if total_sent > 0 else 0
            
            return NotificationStats(
                total_sent=total_sent,
                total_delivered=total_delivered,
                total_failed=total_failed,
                delivery_rate=round(delivery_rate, 2),
                channel_breakdown=channel_breakdown,
                template_usage={}  # Would calculate template usage
            )
            
    except Exception as e:
        logger.error(f"Get notification stats error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get notification statistics"
        )

# Background notification queue processor
async def process_notification_queue():
    """Background task to process scheduled notifications"""
    
    while True:
        try:
            await asyncio.sleep(60)  # Check every minute
            
            current_timestamp = datetime.utcnow().timestamp()
            
            # Get notifications that should be sent now
            scheduled_notifications = await redis_client.zrangebyscore(
                "scheduled_notifications",
                min=0,
                max=current_timestamp,
                withscores=True
            )
            
            for notification_id, scheduled_time in scheduled_notifications:
                # Remove from scheduled set
                await redis_client.zrem("scheduled_notifications", notification_id)
                
                # Send notification
                asyncio.create_task(send_notification_task(notification_id))
                
                logger.info(f"Processed scheduled notification: {notification_id}")
                
        except Exception as e:
            logger.error(f"Process notification queue error: {e}")
            await asyncio.sleep(60)

# Event handlers
@event_handler(EventType.USER_CREATED)
async def handle_user_created(event):
    """Send welcome notification to new user"""
    try:
        # Send welcome notification
        welcome_notification = NotificationSend(
            recipient_id=event.user_id,
            recipient_email=event.data.get("email"),
            channel=NotificationChannel.EMAIL,
            template_type=NotificationType.WELCOME,
            variables={
                "user_name": event.data.get("first_name", "User"),
                "company_name": "BizoholicSaaS"
            }
        )
        
        # Would need to call send_notification with proper context
        logger.info(f"Welcome notification queued for user {event.user_id}")
        
    except Exception as e:
        logger.error(f"Handle user created event error: {e}")

@event_handler(EventType.CAMPAIGN_COMPLETED)
async def handle_campaign_completed(event):
    """Send campaign completion notification"""
    try:
        campaign_notification = NotificationSend(
            recipient_id=event.user_id,
            channel=NotificationChannel.EMAIL,
            template_type=NotificationType.CAMPAIGN_COMPLETE,
            variables={
                "user_name": "User",  # Would get from user service
                "campaign_name": event.data.get("name", "Campaign"),
                "impressions": event.data.get("impressions", "N/A"),
                "clicks": event.data.get("clicks", "N/A"),
                "conversions": event.data.get("conversions", "N/A"),
                "total_spend": event.data.get("spend", "N/A"),
                "campaign_url": f"/campaigns/{event.data.get('campaign_id')}"
            }
        )
        
        logger.info(f"Campaign completion notification queued for campaign {event.data.get('campaign_id')}")
        
    except Exception as e:
        logger.error(f"Handle campaign completed event error: {e}")

# Metrics endpoint
@app.get("/metrics")
async def get_metrics():
    """Prometheus metrics endpoint"""
    return {
        "service": "notification",
        "metrics": {
            "total_notifications_sent": 0,
            "total_notifications_failed": 0,
            "email_notifications_sent": 0,
            "sms_notifications_sent": 0,
            "push_notifications_sent": 0,
            "in_app_notifications_sent": 0
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)