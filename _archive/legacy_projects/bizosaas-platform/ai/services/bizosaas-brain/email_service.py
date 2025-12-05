#!/usr/bin/env python3
"""
BizOSaaS Multi-Tenant Email Service
FastAPI-Mail integration with tenant-specific configurations and templates
"""

from fastapi import HTTPException
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from typing import Dict, Any, List, Optional, Union
from pydantic import BaseModel, EmailStr
from jinja2 import Environment, BaseLoader, TemplateNotFound
import os
import json
import asyncio
import logging
from dataclasses import dataclass
from datetime import datetime

# Set up logging
logger = logging.getLogger(__name__)

@dataclass
class TenantEmailConfig:
    """Email configuration for a specific tenant"""
    tenant_id: str
    smtp_host: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    from_email: str
    from_name: str
    use_tls: bool = True
    use_ssl: bool = False
    
class EmailTemplate(BaseModel):
    """Email template model"""
    name: str
    subject: str
    html_content: str
    text_content: Optional[str] = None
    variables: List[str] = []

class SendEmailRequest(BaseModel):
    """Request model for sending emails"""
    tenant_id: str
    template_name: Optional[str] = None
    to_emails: List[EmailStr]
    cc_emails: Optional[List[EmailStr]] = None
    bcc_emails: Optional[List[EmailStr]] = None
    subject: Optional[str] = None
    html_content: Optional[str] = None
    text_content: Optional[str] = None
    variables: Optional[Dict[str, Any]] = None
    attachments: Optional[List[str]] = None
    priority: int = 3  # 1-5, where 1 is highest priority

class MultiTenantEmailService:
    """Multi-tenant email service with FastAPI-Mail"""
    
    def __init__(self):
        self.tenant_configs: Dict[str, TenantEmailConfig] = {}
        self.tenant_mailers: Dict[str, FastMail] = {}
        self.templates: Dict[str, Dict[str, EmailTemplate]] = {}  # tenant_id -> template_name -> template
        self.template_env = Environment(loader=BaseLoader())
        
        # Load default configurations
        self._load_default_configs()
        self._load_templates()
    
    def _load_default_configs(self):
        """Load default email configurations"""
        # Default BizOSaaS configuration
        default_config = TenantEmailConfig(
            tenant_id="default",
            smtp_host=os.getenv("SMTP_HOST", "smtp.gmail.com"),
            smtp_port=int(os.getenv("SMTP_PORT", "587")),
            smtp_username=os.getenv("SMTP_USERNAME", ""),
            smtp_password=os.getenv("SMTP_PASSWORD", ""),
            from_email=os.getenv("FROM_EMAIL", "noreply@bizosaas.com"),
            from_name=os.getenv("FROM_NAME", "BizOSaaS Platform"),
            use_tls=True,
            use_ssl=False
        )
        
        self.tenant_configs["default"] = default_config
        self._create_mailer("default", default_config)
        
        # Bizoholic tenant configuration
        bizoholic_config = TenantEmailConfig(
            tenant_id="bizoholic",
            smtp_host=os.getenv("BIZOHOLIC_SMTP_HOST", "smtp.gmail.com"),
            smtp_port=int(os.getenv("BIZOHOLIC_SMTP_PORT", "587")),
            smtp_username=os.getenv("BIZOHOLIC_SMTP_USERNAME", ""),
            smtp_password=os.getenv("BIZOHOLIC_SMTP_PASSWORD", ""),
            from_email=os.getenv("BIZOHOLIC_FROM_EMAIL", "hello@bizoholic.com"),
            from_name=os.getenv("BIZOHOLIC_FROM_NAME", "Bizoholic Digital"),
            use_tls=True,
            use_ssl=False
        )
        
        self.tenant_configs["bizoholic"] = bizoholic_config
        self._create_mailer("bizoholic", bizoholic_config)
        
        # CorelDove tenant configuration
        coreldove_config = TenantEmailConfig(
            tenant_id="coreldove",
            smtp_host=os.getenv("CORELDOVE_SMTP_HOST", "smtp.gmail.com"),
            smtp_port=int(os.getenv("CORELDOVE_SMTP_PORT", "587")),
            smtp_username=os.getenv("CORELDOVE_SMTP_USERNAME", ""),
            smtp_password=os.getenv("CORELDOVE_SMTP_PASSWORD", ""),
            from_email=os.getenv("CORELDOVE_FROM_EMAIL", "orders@coreldove.com"),
            from_name=os.getenv("CORELDOVE_FROM_NAME", "CorelDove"),
            use_tls=True,
            use_ssl=False
        )
        
        self.tenant_configs["coreldove"] = coreldove_config
        self._create_mailer("coreldove", coreldove_config)
    
    def _create_mailer(self, tenant_id: str, config: TenantEmailConfig):
        """Create FastMail instance for tenant"""
        try:
            connection_config = ConnectionConfig(
                MAIL_USERNAME=config.smtp_username,
                MAIL_PASSWORD=config.smtp_password,
                MAIL_FROM=config.from_email,
                MAIL_FROM_NAME=config.from_name,
                MAIL_PORT=config.smtp_port,
                MAIL_SERVER=config.smtp_host,
                MAIL_STARTTLS=config.use_tls,
                MAIL_SSL_TLS=config.use_ssl,
                USE_CREDENTIALS=True,
                VALIDATE_CERTS=True
            )
            
            self.tenant_mailers[tenant_id] = FastMail(connection_config)
            logger.info(f"Created email mailer for tenant: {tenant_id}")
            
        except Exception as e:
            logger.error(f"Failed to create mailer for tenant {tenant_id}: {e}")
    
    def _load_templates(self):
        """Load email templates for all tenants"""
        # Default welcome template
        welcome_template = EmailTemplate(
            name="welcome",
            subject="Welcome to {{tenant_name}}!",
            html_content="""
            <h2>Welcome {{user_name}}!</h2>
            <p>Thank you for joining {{tenant_name}}. We're excited to have you on board!</p>
            <p>Your account details:</p>
            <ul>
                <li>Email: {{user_email}}</li>
                <li>Account created: {{created_at}}</li>
            </ul>
            <p>Best regards,<br>{{tenant_name}} Team</p>
            """,
            text_content="""
            Welcome {{user_name}}!
            
            Thank you for joining {{tenant_name}}. We're excited to have you on board!
            
            Your account details:
            - Email: {{user_email}}
            - Account created: {{created_at}}
            
            Best regards,
            {{tenant_name}} Team
            """,
            variables=["user_name", "user_email", "tenant_name", "created_at"]
        )
        
        # Lead notification template
        lead_notification_template = EmailTemplate(
            name="lead_notification",
            subject="New Lead: {{lead_name}} - {{lead_company}}",
            html_content="""
            <h2>New Lead Received</h2>
            <p>You have a new lead from {{lead_source}}:</p>
            <table>
                <tr><td><strong>Name:</strong></td><td>{{lead_name}}</td></tr>
                <tr><td><strong>Email:</strong></td><td>{{lead_email}}</td></tr>
                <tr><td><strong>Phone:</strong></td><td>{{lead_phone}}</td></tr>
                <tr><td><strong>Company:</strong></td><td>{{lead_company}}</td></tr>
                <tr><td><strong>Message:</strong></td><td>{{lead_message}}</td></tr>
                <tr><td><strong>Score:</strong></td><td>{{lead_score}}/100</td></tr>
            </table>
            <p>Received at: {{received_at}}</p>
            """,
            variables=["lead_name", "lead_email", "lead_phone", "lead_company", "lead_message", "lead_score", "lead_source", "received_at"]
        )
        
        # Order confirmation template
        order_confirmation_template = EmailTemplate(
            name="order_confirmation",
            subject="Order Confirmation - #{{order_number}}",
            html_content="""
            <h2>Order Confirmation</h2>
            <p>Thank you for your order! Here are the details:</p>
            <table>
                <tr><td><strong>Order Number:</strong></td><td>#{{order_number}}</td></tr>
                <tr><td><strong>Total Amount:</strong></td><td>${{order_total}}</td></tr>
                <tr><td><strong>Status:</strong></td><td>{{order_status}}</td></tr>
                <tr><td><strong>Estimated Delivery:</strong></td><td>{{delivery_date}}</td></tr>
            </table>
            <h3>Items Ordered:</h3>
            <ul>
            {{#each items}}
                <li>{{name}} - Qty: {{quantity}} - ${{price}}</li>
            {{/each}}
            </ul>
            <p>We'll send you updates as your order progresses.</p>
            """,
            variables=["order_number", "order_total", "order_status", "delivery_date", "items"]
        )
        
        # Initialize templates for all tenants
        for tenant_id in ["default", "bizoholic", "coreldove"]:
            self.templates[tenant_id] = {
                "welcome": welcome_template,
                "lead_notification": lead_notification_template,
                "order_confirmation": order_confirmation_template
            }
    
    async def add_tenant_config(self, config: TenantEmailConfig):
        """Add or update tenant email configuration"""
        self.tenant_configs[config.tenant_id] = config
        self._create_mailer(config.tenant_id, config)
        
        # Initialize templates for new tenant
        if config.tenant_id not in self.templates:
            self.templates[config.tenant_id] = self.templates["default"].copy()
    
    async def get_tenant_config(self, tenant_id: str) -> Optional[TenantEmailConfig]:
        """Get tenant email configuration"""
        return self.tenant_configs.get(tenant_id)
    
    async def render_template(self, tenant_id: str, template_name: str, variables: Dict[str, Any]) -> tuple[str, str]:
        """Render email template with variables"""
        if tenant_id not in self.templates:
            tenant_id = "default"
        
        if template_name not in self.templates[tenant_id]:
            raise ValueError(f"Template '{template_name}' not found for tenant '{tenant_id}'")
        
        template = self.templates[tenant_id][template_name]
        
        try:
            # Render HTML content
            html_template = self.template_env.from_string(template.html_content)
            html_content = html_template.render(**variables)
            
            # Render text content if available
            text_content = ""
            if template.text_content:
                text_template = self.template_env.from_string(template.text_content)
                text_content = text_template.render(**variables)
            
            # Render subject
            subject_template = self.template_env.from_string(template.subject)
            subject = subject_template.render(**variables)
            
            return subject, html_content, text_content
            
        except Exception as e:
            logger.error(f"Template rendering error: {e}")
            raise ValueError(f"Failed to render template: {e}")
    
    async def send_email(self, request: SendEmailRequest) -> Dict[str, Any]:
        """Send email using tenant-specific configuration"""
        try:
            # Get tenant mailer
            tenant_id = request.tenant_id
            if tenant_id not in self.tenant_mailers:
                tenant_id = "default"  # Fallback to default
            
            mailer = self.tenant_mailers[tenant_id]
            
            # Prepare email content
            if request.template_name and request.variables:
                # Use template
                subject, html_content, text_content = await self.render_template(
                    tenant_id, request.template_name, request.variables
                )
            else:
                # Use provided content
                subject = request.subject or "No Subject"
                html_content = request.html_content or ""
                text_content = request.text_content or ""
            
            # Create message
            message = MessageSchema(
                subject=subject,
                recipients=request.to_emails,
                cc=request.cc_emails or [],
                bcc=request.bcc_emails or [],
                body=html_content,
                html=html_content,
                subtype=MessageType.html
            )
            
            # Send email
            await mailer.send_message(message)
            
            logger.info(f"Email sent successfully for tenant {tenant_id} to {request.to_emails}")
            
            return {
                "status": "success",
                "message": "Email sent successfully",
                "tenant_id": tenant_id,
                "recipients": request.to_emails,
                "subject": subject,
                "sent_at": datetime.utcnow().isoformat()
            }
            
        except ConnectionErrors as e:
            logger.error(f"Email connection error: {e}")
            raise HTTPException(status_code=500, detail=f"Email service connection failed: {str(e)}")
            
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")
    
    async def send_welcome_email(self, tenant_id: str, user_email: str, user_name: str) -> Dict[str, Any]:
        """Send welcome email to new user"""
        tenant_config = self.tenant_configs.get(tenant_id, self.tenant_configs["default"])
        
        variables = {
            "user_name": user_name,
            "user_email": user_email,
            "tenant_name": tenant_config.from_name,
            "created_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        }
        
        request = SendEmailRequest(
            tenant_id=tenant_id,
            template_name="welcome",
            to_emails=[user_email],
            variables=variables
        )
        
        return await self.send_email(request)
    
    async def send_lead_notification(self, tenant_id: str, lead_data: Dict[str, Any], notification_emails: List[str]) -> Dict[str, Any]:
        """Send lead notification to team"""
        variables = {
            "lead_name": lead_data.get("name", "Unknown"),
            "lead_email": lead_data.get("email", ""),
            "lead_phone": lead_data.get("phone", ""),
            "lead_company": lead_data.get("company", ""),
            "lead_message": lead_data.get("message", ""),
            "lead_score": lead_data.get("score", 0),
            "lead_source": lead_data.get("source", "Website"),
            "received_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        }
        
        request = SendEmailRequest(
            tenant_id=tenant_id,
            template_name="lead_notification",
            to_emails=notification_emails,
            variables=variables,
            priority=1  # High priority
        )
        
        return await self.send_email(request)
    
    async def send_order_confirmation(self, tenant_id: str, order_data: Dict[str, Any], customer_email: str) -> Dict[str, Any]:
        """Send order confirmation to customer"""
        variables = {
            "order_number": order_data.get("number", ""),
            "order_total": order_data.get("total", "0.00"),
            "order_status": order_data.get("status", "Processing"),
            "delivery_date": order_data.get("delivery_date", "TBD"),
            "items": order_data.get("items", [])
        }
        
        request = SendEmailRequest(
            tenant_id=tenant_id,
            template_name="order_confirmation",
            to_emails=[customer_email],
            variables=variables
        )
        
        return await self.send_email(request)
    
    async def health_check(self) -> Dict[str, Any]:
        """Check email service health"""
        health_status = {
            "service": "email",
            "status": "healthy",
            "tenants": {},
            "timestamp": datetime.utcnow().isoformat()
        }
        
        for tenant_id, config in self.tenant_configs.items():
            try:
                # Simple connection test
                mailer = self.tenant_mailers.get(tenant_id)
                if mailer:
                    health_status["tenants"][tenant_id] = {
                        "status": "configured",
                        "smtp_host": config.smtp_host,
                        "from_email": config.from_email
                    }
                else:
                    health_status["tenants"][tenant_id] = {
                        "status": "not_configured"
                    }
            except Exception as e:
                health_status["tenants"][tenant_id] = {
                    "status": "error",
                    "error": str(e)
                }
        
        return health_status

# Global email service instance
email_service = MultiTenantEmailService()