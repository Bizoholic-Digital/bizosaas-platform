#!/usr/bin/env python3
"""
Comprehensive Wizard Management Interface for All Platform Onboarding Workflows
Manages all onboarding, setup, and configuration wizards across the entire BizOSaaS platform
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Optional, Union
from datetime import datetime, timedelta
import sqlite3
from dataclasses import dataclass, asdict
from enum import Enum
import uuid

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WizardType(Enum):
    TENANT_ONBOARDING = "tenant_onboarding"
    USER_ONBOARDING = "user_onboarding"
    INTEGRATION_SETUP = "integration_setup"
    AI_AGENT_CONFIG = "ai_agent_config"
    ANALYTICS_SETUP = "analytics_setup"
    WORKFLOW_CREATION = "workflow_creation"
    BILLING_SETUP = "billing_setup"
    SECURITY_CONFIG = "security_config"
    BRANDING_SETUP = "branding_setup"
    NOTIFICATION_CONFIG = "notification_config"
    API_SETUP = "api_setup"
    TEAM_SETUP = "team_setup"
    PROJECT_INITIALIZATION = "project_initialization"
    MIGRATION_WIZARD = "migration_wizard"

class WizardStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DRAFT = "draft"
    ARCHIVED = "archived"
    MAINTENANCE = "maintenance"

class StepType(Enum):
    FORM_INPUT = "form_input"
    SELECTION = "selection"
    FILE_UPLOAD = "file_upload"
    API_CALL = "api_call"
    CONFIRMATION = "confirmation"
    PROGRESS_DISPLAY = "progress_display"
    CONDITIONAL_BRANCH = "conditional_branch"
    EXTERNAL_REDIRECT = "external_redirect"
    AI_ASSISTANCE = "ai_assistance"

@dataclass
class WizardStep:
    id: str
    title: str
    description: str
    step_type: StepType
    order: int
    is_required: bool
    config: Dict[str, Any]  # Step-specific configuration
    validation_rules: Dict[str, Any]
    help_text: str
    conditional_logic: Optional[Dict[str, Any]] = None
    ai_assistance_config: Optional[Dict[str, Any]] = None
    estimated_time: Optional[str] = None
    completion_criteria: Optional[Dict[str, Any]] = None

@dataclass
class Wizard:
    id: str
    name: str
    description: str
    wizard_type: WizardType
    target_audience: List[str]  # roles, user types, etc.
    steps: List[WizardStep]
    status: WizardStatus
    version: str
    created_at: datetime
    updated_at: datetime
    created_by: str
    estimated_completion_time: str
    success_rate: float
    average_completion_time: str
    prerequisites: List[str]
    post_completion_actions: List[Dict[str, Any]]
    tenant_specific: bool = False
    customizable: bool = True
    category: str = "general"
    tags: List[str] = None
    icon: str = "setup"
    color: str = "#3b82f6"

@dataclass
class WizardExecution:
    id: str
    wizard_id: str
    user_id: str
    tenant_id: str
    started_at: datetime
    completed_at: Optional[datetime]
    current_step: int
    status: str  # "in_progress", "completed", "abandoned", "failed"
    step_data: Dict[str, Any]  # Data collected from each step
    completion_percentage: int
    execution_metadata: Dict[str, Any]

class WizardManager:
    """Main class for managing all platform wizards"""
    
    def __init__(self, db_path: str = "/tmp/wizard_manager.db"):
        self.db_path = db_path
        self._init_database()
        self._load_default_wizards()
    
    def _init_database(self):
        """Initialize SQLite database for wizard management"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Wizards table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS wizards (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                wizard_type TEXT NOT NULL,
                target_audience TEXT,
                steps TEXT,
                status TEXT,
                version TEXT,
                created_at TEXT,
                updated_at TEXT,
                created_by TEXT,
                estimated_completion_time TEXT,
                success_rate REAL,
                average_completion_time TEXT,
                prerequisites TEXT,
                post_completion_actions TEXT,
                tenant_specific BOOLEAN,
                customizable BOOLEAN,
                category TEXT,
                tags TEXT,
                icon TEXT,
                color TEXT
            )
        ''')
        
        # Wizard executions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS wizard_executions (
                id TEXT PRIMARY KEY,
                wizard_id TEXT,
                user_id TEXT,
                tenant_id TEXT,
                started_at TEXT,
                completed_at TEXT,
                current_step INTEGER,
                status TEXT,
                step_data TEXT,
                completion_percentage INTEGER,
                execution_metadata TEXT,
                FOREIGN KEY (wizard_id) REFERENCES wizards (id)
            )
        ''')
        
        # Wizard analytics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS wizard_analytics (
                id TEXT PRIMARY KEY,
                wizard_id TEXT,
                metric_name TEXT,
                metric_value TEXT,
                timestamp TEXT,
                tenant_id TEXT,
                FOREIGN KEY (wizard_id) REFERENCES wizards (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _load_default_wizards(self):
        """Load default wizards for the platform"""
        default_wizards = [
            self._create_tenant_onboarding_wizard(),
            self._create_user_onboarding_wizard(),
            self._create_integration_setup_wizard(),
            self._create_ai_agent_config_wizard(),
            self._create_analytics_setup_wizard(),
            self._create_workflow_creation_wizard(),
            self._create_billing_setup_wizard(),
            self._create_security_config_wizard(),
            self._create_branding_setup_wizard(),
            self._create_team_setup_wizard(),
            self._create_project_initialization_wizard(),
            self._create_migration_wizard()
        ]
        
        for wizard in default_wizards:
            if not self._wizard_exists(wizard.id):
                self.create_wizard(wizard)
                logger.info(f"Loaded default wizard: {wizard.name}")
    
    def _create_tenant_onboarding_wizard(self) -> Wizard:
        """Create comprehensive tenant onboarding wizard"""
        steps = [
            WizardStep(
                id="welcome",
                title="Welcome to BizOSaaS",
                description="Introduction to the platform and overview of onboarding process",
                step_type=StepType.PROGRESS_DISPLAY,
                order=1,
                is_required=True,
                config={
                    "content": "Welcome to BizOSaaS! We'll help you set up your organization in just a few minutes.",
                    "video_url": "/onboarding/welcome-video.mp4",
                    "estimated_steps": 8
                },
                validation_rules={},
                help_text="This wizard will guide you through the complete setup process",
                estimated_time="2 minutes"
            ),
            WizardStep(
                id="organization_details",
                title="Organization Information",
                description="Basic information about your organization",
                step_type=StepType.FORM_INPUT,
                order=2,
                is_required=True,
                config={
                    "fields": [
                        {"name": "company_name", "type": "text", "label": "Company Name", "required": True},
                        {"name": "industry", "type": "select", "label": "Industry", "options": ["Technology", "Healthcare", "Finance", "Retail", "Manufacturing", "Other"], "required": True},
                        {"name": "company_size", "type": "select", "label": "Company Size", "options": ["1-10", "11-50", "51-200", "201-1000", "1000+"], "required": True},
                        {"name": "website", "type": "url", "label": "Website", "required": False},
                        {"name": "description", "type": "textarea", "label": "Company Description", "required": False}
                    ]
                },
                validation_rules={
                    "company_name": {"min_length": 2, "max_length": 100},
                    "website": {"format": "url"}
                },
                help_text="This information helps us customize your experience",
                estimated_time="3 minutes"
            ),
            WizardStep(
                id="admin_account",
                title="Administrator Account",
                description="Set up the primary administrator account",
                step_type=StepType.FORM_INPUT,
                order=3,
                is_required=True,
                config={
                    "fields": [
                        {"name": "admin_first_name", "type": "text", "label": "First Name", "required": True},
                        {"name": "admin_last_name", "type": "text", "label": "Last Name", "required": True},
                        {"name": "admin_email", "type": "email", "label": "Email Address", "required": True},
                        {"name": "admin_phone", "type": "tel", "label": "Phone Number", "required": False},
                        {"name": "admin_timezone", "type": "select", "label": "Timezone", "required": True, "options": ["UTC", "US/Eastern", "US/Central", "US/Mountain", "US/Pacific", "Europe/London", "Europe/Berlin", "Asia/Tokyo"]}
                    ]
                },
                validation_rules={
                    "admin_email": {"format": "email", "unique": True}
                },
                help_text="This will be the main administrator account for your organization",
                estimated_time="2 minutes"
            ),
            WizardStep(
                id="business_goals",
                title="Business Goals & Use Cases",
                description="Tell us about your primary goals and use cases",
                step_type=StepType.SELECTION,
                order=4,
                is_required=True,
                config={
                    "selection_type": "multiple",
                    "options": [
                        {"id": "marketing_automation", "label": "Marketing Automation", "description": "Automate marketing campaigns and lead nurturing"},
                        {"id": "analytics_reporting", "label": "Analytics & Reporting", "description": "Generate insights and custom reports"},
                        {"id": "crm_management", "label": "CRM Management", "description": "Manage customer relationships and sales pipeline"},
                        {"id": "workflow_automation", "label": "Workflow Automation", "description": "Automate business processes and workflows"},
                        {"id": "ai_assistance", "label": "AI Assistance", "description": "Leverage AI agents for various tasks"},
                        {"id": "integration_management", "label": "Integration Management", "description": "Connect and manage external services"},
                        {"id": "team_collaboration", "label": "Team Collaboration", "description": "Enable team collaboration and communication"}
                    ]
                },
                validation_rules={
                    "min_selections": 1,
                    "max_selections": 5
                },
                help_text="Select your primary use cases to help us recommend the best features",
                estimated_time="3 minutes"
            ),
            WizardStep(
                id="branding_setup",
                title="Brand Configuration",
                description="Set up your brand identity and appearance",
                step_type=StepType.FILE_UPLOAD,
                order=5,
                is_required=False,
                config={
                    "upload_types": ["logo", "favicon", "brand_colors"],
                    "logo": {"max_size": "2MB", "formats": ["png", "jpg", "svg"]},
                    "favicon": {"max_size": "1MB", "formats": ["png", "ico"]},
                    "brand_colors": {"primary_color": "#3b82f6", "secondary_color": "#64748b", "accent_color": "#10b981"}
                },
                validation_rules={
                    "file_size": {"max": "2MB"},
                    "file_format": ["png", "jpg", "svg", "ico"]
                },
                help_text="Upload your brand assets to personalize the platform",
                estimated_time="5 minutes"
            ),
            WizardStep(
                id="initial_integrations",
                title="Key Integrations",
                description="Connect your essential services",
                step_type=StepType.SELECTION,
                order=6,
                is_required=False,
                config={
                    "selection_type": "multiple",
                    "integration_categories": ["analytics", "crm", "marketing", "payment", "communication"],
                    "popular_integrations": [
                        {"id": "google_analytics", "name": "Google Analytics", "category": "analytics"},
                        {"id": "salesforce", "name": "Salesforce", "category": "crm"},
                        {"id": "hubspot", "name": "HubSpot", "category": "marketing"},
                        {"id": "stripe", "name": "Stripe", "category": "payment"},
                        {"id": "slack", "name": "Slack", "category": "communication"}
                    ]
                },
                validation_rules={},
                help_text="You can always add more integrations later",
                estimated_time="5 minutes",
                conditional_logic={
                    "show_if": {"business_goals": ["marketing_automation", "analytics_reporting", "crm_management"]}
                }
            ),
            WizardStep(
                id="ai_agent_selection",
                title="AI Agent Configuration",
                description="Choose and configure AI agents for your organization",
                step_type=StepType.AI_ASSISTANCE,
                order=7,
                is_required=False,
                config={
                    "ai_assistance_type": "recommendation_engine",
                    "agent_categories": ["marketing", "analytics", "content", "automation", "support"],
                    "recommended_agents": [
                        {"id": "marketing_campaign_manager", "name": "Marketing Campaign Manager", "category": "marketing"},
                        {"id": "analytics_reporter", "name": "Analytics Reporter", "category": "analytics"},
                        {"id": "content_generator", "name": "Content Generator", "category": "content"},
                        {"id": "workflow_automator", "name": "Workflow Automator", "category": "automation"}
                    ]
                },
                validation_rules={},
                help_text="AI agents will help automate various tasks based on your business goals",
                estimated_time="4 minutes",
                ai_assistance_config={
                    "enable_recommendations": True,
                    "personalization": True
                }
            ),
            WizardStep(
                id="completion_summary",
                title="Setup Complete!",
                description="Review your configuration and next steps",
                step_type=StepType.CONFIRMATION,
                order=8,
                is_required=True,
                config={
                    "summary_sections": ["organization", "admin", "goals", "branding", "integrations", "ai_agents"],
                    "next_steps": [
                        "Explore your dashboard",
                        "Invite team members",
                        "Create your first workflow",
                        "Connect additional integrations"
                    ],
                    "resource_links": [
                        {"title": "Getting Started Guide", "url": "/docs/getting-started"},
                        {"title": "Video Tutorials", "url": "/tutorials"},
                        {"title": "Support Center", "url": "/support"}
                    ]
                },
                validation_rules={},
                help_text="You're all set! Start exploring the platform.",
                estimated_time="2 minutes"
            )
        ]
        
        return Wizard(
            id="tenant_onboarding_v2",
            name="Organization Onboarding",
            description="Complete onboarding process for new organizations joining the platform",
            wizard_type=WizardType.TENANT_ONBOARDING,
            target_audience=["new_tenants", "administrators"],
            steps=steps,
            status=WizardStatus.ACTIVE,
            version="2.0",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            created_by="system",
            estimated_completion_time="20-25 minutes",
            success_rate=0.87,
            average_completion_time="22 minutes",
            prerequisites=[],
            post_completion_actions=[
                {"action": "send_welcome_email", "config": {"template": "tenant_welcome"}},
                {"action": "create_default_workflows", "config": {"templates": ["basic_lead_nurturing"]}},
                {"action": "schedule_follow_up", "config": {"delay_days": 3, "type": "onboarding_check_in"}}
            ],
            tenant_specific=False,
            customizable=True,
            category="onboarding",
            tags=["essential", "onboarding", "setup"],
            icon="building-office",
            color="#3b82f6"
        )
    
    def _create_user_onboarding_wizard(self) -> Wizard:
        """Create user onboarding wizard"""
        steps = [
            WizardStep(
                id="user_welcome",
                title="Welcome to the Team!",
                description="Introduction for new team members",
                step_type=StepType.PROGRESS_DISPLAY,
                order=1,
                is_required=True,
                config={
                    "content": "Welcome to your organization's BizOSaaS workspace!",
                    "estimated_steps": 5
                },
                validation_rules={},
                help_text="Let's get you set up quickly",
                estimated_time="1 minute"
            ),
            WizardStep(
                id="user_profile",
                title="User Profile",
                description="Set up your personal profile",
                step_type=StepType.FORM_INPUT,
                order=2,
                is_required=True,
                config={
                    "fields": [
                        {"name": "first_name", "type": "text", "label": "First Name", "required": True},
                        {"name": "last_name", "type": "text", "label": "Last Name", "required": True},
                        {"name": "job_title", "type": "text", "label": "Job Title", "required": False},
                        {"name": "department", "type": "select", "label": "Department", "options": ["Marketing", "Sales", "Operations", "IT", "Finance", "HR", "Other"], "required": False},
                        {"name": "bio", "type": "textarea", "label": "Bio", "required": False}
                    ]
                },
                validation_rules={},
                help_text="This information helps your team know more about you",
                estimated_time="2 minutes"
            ),
            WizardStep(
                id="role_permissions",
                title="Role & Permissions",
                description="Review your role and permissions",
                step_type=StepType.PROGRESS_DISPLAY,
                order=3,
                is_required=True,
                config={
                    "display_type": "permissions_overview",
                    "sections": ["your_role", "permissions", "access_levels"]
                },
                validation_rules={},
                help_text="Here's what you can access and do in the platform",
                estimated_time="2 minutes"
            ),
            WizardStep(
                id="notification_preferences",
                title="Notification Preferences",
                description="Configure how you'd like to receive notifications",
                step_type=StepType.SELECTION,
                order=4,
                is_required=False,
                config={
                    "selection_type": "multiple",
                    "notification_types": [
                        {"id": "email_summaries", "label": "Daily Email Summaries", "default": True},
                        {"id": "slack_notifications", "label": "Slack Notifications", "default": False},
                        {"id": "mobile_push", "label": "Mobile Push Notifications", "default": True},
                        {"id": "workflow_updates", "label": "Workflow Status Updates", "default": True},
                        {"id": "system_announcements", "label": "System Announcements", "default": True}
                    ]
                },
                validation_rules={},
                help_text="You can change these settings anytime",
                estimated_time="2 minutes"
            ),
            WizardStep(
                id="user_completion",
                title="You're Ready to Go!",
                description="Complete your user setup",
                step_type=StepType.CONFIRMATION,
                order=5,
                is_required=True,
                config={
                    "next_steps": [
                        "Explore your dashboard",
                        "Check out available workflows",
                        "Connect with your team",
                        "Review documentation"
                    ]
                },
                validation_rules={},
                help_text="Welcome to the team!",
                estimated_time="1 minute"
            )
        ]
        
        return Wizard(
            id="user_onboarding_v1",
            name="User Onboarding",
            description="Onboarding process for new users joining an existing organization",
            wizard_type=WizardType.USER_ONBOARDING,
            target_audience=["new_users", "team_members"],
            steps=steps,
            status=WizardStatus.ACTIVE,
            version="1.0",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            created_by="system",
            estimated_completion_time="8-10 minutes",
            success_rate=0.92,
            average_completion_time="9 minutes",
            prerequisites=[],
            post_completion_actions=[
                {"action": "send_welcome_email", "config": {"template": "user_welcome"}},
                {"action": "add_to_default_channels", "config": {"channels": ["general", "announcements"]}},
                {"action": "assign_onboarding_buddy", "config": {"auto_assign": True}}
            ],
            tenant_specific=True,
            customizable=True,
            category="onboarding",
            tags=["user", "onboarding", "team"],
            icon="user-plus",
            color="#10b981"
        )
    
    def _create_integration_setup_wizard(self) -> Wizard:
        """Create integration setup wizard"""
        steps = [
            WizardStep(
                id="integration_selection",
                title="Choose Integration",
                description="Select the service you want to integrate",
                step_type=StepType.SELECTION,
                order=1,
                is_required=True,
                config={
                    "selection_type": "single",
                    "integration_categories": {
                        "analytics": ["Google Analytics", "Adobe Analytics", "Mixpanel"],
                        "crm": ["Salesforce", "HubSpot", "Pipedrive"],
                        "marketing": ["Mailchimp", "Constant Contact", "SendGrid"],
                        "payment": ["Stripe", "PayPal", "Square"],
                        "social": ["Facebook", "LinkedIn", "Twitter"],
                        "communication": ["Slack", "Microsoft Teams", "Discord"]
                    }
                },
                validation_rules={
                    "required": True
                },
                help_text="Choose the service you want to connect to your account",
                estimated_time="1 minute"
            ),
            WizardStep(
                id="authentication_setup",
                title="Authentication",
                description="Connect your account securely",
                step_type=StepType.API_CALL,
                order=2,
                is_required=True,
                config={
                    "auth_type": "oauth2",
                    "redirect_uri": "/auth/callback",
                    "scopes": ["read", "write"],
                    "fallback_auth": "api_key"
                },
                validation_rules={
                    "auth_required": True
                },
                help_text="We'll securely connect to your account using industry-standard authentication",
                estimated_time="2 minutes"
            ),
            WizardStep(
                id="integration_configuration",
                title="Configuration",
                description="Configure integration settings",
                step_type=StepType.FORM_INPUT,
                order=3,
                is_required=True,
                config={
                    "dynamic_fields": True,
                    "fields_source": "integration_metadata"
                },
                validation_rules={},
                help_text="Configure how this integration should work with your account",
                estimated_time="3 minutes"
            ),
            WizardStep(
                id="test_connection",
                title="Test Connection",
                description="Verify the integration is working correctly",
                step_type=StepType.API_CALL,
                order=4,
                is_required=True,
                config={
                    "test_endpoint": "/test-connection",
                    "success_criteria": {"status": "connected", "data_accessible": True}
                },
                validation_rules={},
                help_text="We'll test the connection to make sure everything is working",
                estimated_time="1 minute"
            ),
            WizardStep(
                id="integration_complete",
                title="Integration Complete",
                description="Your integration is ready to use",
                step_type=StepType.CONFIRMATION,
                order=5,
                is_required=True,
                config={
                    "success_message": "Integration successfully configured!",
                    "next_steps": [
                        "View integration dashboard",
                        "Configure data sync settings",
                        "Set up automated workflows"
                    ]
                },
                validation_rules={},
                help_text="Your integration is now active and ready to use",
                estimated_time="1 minute"
            )
        ]
        
        return Wizard(
            id="integration_setup_v1",
            name="Integration Setup",
            description="Generic wizard for setting up external service integrations",
            wizard_type=WizardType.INTEGRATION_SETUP,
            target_audience=["administrators", "power_users"],
            steps=steps,
            status=WizardStatus.ACTIVE,
            version="1.0",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            created_by="system",
            estimated_completion_time="8-10 minutes",
            success_rate=0.84,
            average_completion_time="9 minutes",
            prerequisites=["admin_permissions"],
            post_completion_actions=[
                {"action": "enable_integration", "config": {"auto_enable": True}},
                {"action": "create_integration_dashboard", "config": {"template": "default"}},
                {"action": "schedule_sync", "config": {"initial_sync": True}}
            ],
            tenant_specific=True,
            customizable=True,
            category="integration",
            tags=["integration", "setup", "configuration"],
            icon="link",
            color="#8b5cf6"
        )
    
    # Additional wizard creation methods would continue here...
    # For brevity, I'm including a few key ones and indicating where others would go
    
    def _create_ai_agent_config_wizard(self) -> Wizard:
        """Create AI agent configuration wizard"""
        steps = [
            WizardStep(
                id="agent_category_selection",
                title="Select AI Agent Categories",
                description="Choose the types of AI agents you need",
                step_type=StepType.SELECTION,
                order=1,
                is_required=True,
                config={
                    "selection_type": "multiple",
                    "categories": ["marketing", "analytics", "content", "automation", "support", "sales", "ecommerce"],
                    "category_descriptions": {
                        "marketing": "Campaign management, lead generation, social media",
                        "analytics": "Data analysis, reporting, insights generation",
                        "content": "Content creation, copywriting, SEO optimization",
                        "automation": "Workflow automation, process optimization",
                        "support": "Customer support, ticket management",
                        "sales": "Sales pipeline, lead qualification, CRM management",
                        "ecommerce": "Product management, inventory, order processing"
                    }
                },
                validation_rules={"min_selections": 1},
                help_text="Select the AI agent categories that match your business needs",
                estimated_time="3 minutes"
            ),
            WizardStep(
                id="agent_configuration",
                title="Configure AI Agents",
                description="Set up individual AI agents",
                step_type=StepType.AI_ASSISTANCE,
                order=2,
                is_required=True,
                config={
                    "dynamic_agents": True,
                    "agent_customization": ["name", "personality", "expertise_level", "communication_style"]
                },
                validation_rules={},
                help_text="Customize AI agents to match your brand and requirements",
                estimated_time="10 minutes"
            )
        ]
        
        return Wizard(
            id="ai_agent_config_v1",
            name="AI Agent Configuration",
            description="Configure and customize AI agents for your organization",
            wizard_type=WizardType.AI_AGENT_CONFIG,
            target_audience=["administrators", "power_users"],
            steps=steps,
            status=WizardStatus.ACTIVE,
            version="1.0",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            created_by="system",
            estimated_completion_time="15 minutes",
            success_rate=0.89,
            average_completion_time="13 minutes",
            prerequisites=["basic_setup_complete"],
            post_completion_actions=[
                {"action": "deploy_agents", "config": {"auto_deploy": True}},
                {"action": "create_agent_dashboard", "config": {"template": "default"}}
            ],
            tenant_specific=True,
            customizable=True,
            category="ai",
            tags=["ai", "agents", "configuration"],
            icon="bot",
            color="#8b5cf6"
        )
    
    def _create_analytics_setup_wizard(self) -> Wizard:
        """Create analytics setup wizard"""
        steps = [
            WizardStep(
                id="analytics_goals",
                title="Analytics Goals",
                description="Define what you want to track and measure",
                step_type=StepType.SELECTION,
                order=1,
                is_required=True,
                config={
                    "selection_type": "multiple",
                    "goals": ["website_traffic", "user_engagement", "conversion_rates", "revenue_tracking", "campaign_performance"]
                },
                validation_rules={},
                help_text="Select your primary analytics objectives",
                estimated_time="3 minutes"
            )
        ]
        
        return Wizard(
            id="analytics_setup_v1",
            name="Analytics Setup",
            description="Set up comprehensive analytics tracking",
            wizard_type=WizardType.ANALYTICS_SETUP,
            target_audience=["analysts", "marketers", "administrators"],
            steps=steps,
            status=WizardStatus.ACTIVE,
            version="1.0",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            created_by="system",
            estimated_completion_time="10 minutes",
            success_rate=0.85,
            average_completion_time="9 minutes",
            prerequisites=[],
            post_completion_actions=[],
            tenant_specific=True,
            customizable=True,
            category="analytics",
            tags=["analytics", "tracking", "measurement"],
            icon="bar-chart-3",
            color="#10b981"
        )
    
    def _create_workflow_creation_wizard(self) -> Wizard:
        """Create workflow creation wizard"""
        return Wizard(
            id="workflow_creation_v1",
            name="Workflow Creation",
            description="Create automated workflows",
            wizard_type=WizardType.WORKFLOW_CREATION,
            target_audience=["power_users", "administrators"],
            steps=[],
            status=WizardStatus.DRAFT,
            version="1.0",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            created_by="system",
            estimated_completion_time="15 minutes",
            success_rate=0.82,
            average_completion_time="14 minutes",
            prerequisites=[],
            post_completion_actions=[],
            tenant_specific=True,
            customizable=True,
            category="automation",
            tags=["workflow", "automation"],
            icon="workflow",
            color="#f59e0b"
        )
    
    def _create_billing_setup_wizard(self) -> Wizard:
        """Create billing setup wizard"""
        return Wizard(
            id="billing_setup_v1",
            name="Billing Setup",
            description="Configure billing and payment processing",
            wizard_type=WizardType.BILLING_SETUP,
            target_audience=["administrators", "billing_managers"],
            steps=[],
            status=WizardStatus.DRAFT,
            version="1.0",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            created_by="system",
            estimated_completion_time="12 minutes",
            success_rate=0.78,
            average_completion_time="11 minutes",
            prerequisites=[],
            post_completion_actions=[],
            tenant_specific=True,
            customizable=True,
            category="billing",
            tags=["billing", "payments"],
            icon="credit-card",
            color="#ef4444"
        )
    
    def _create_security_config_wizard(self) -> Wizard:
        """Create security configuration wizard"""
        return Wizard(
            id="security_config_v1",
            name="Security Configuration",
            description="Set up security policies and access controls",
            wizard_type=WizardType.SECURITY_CONFIG,
            target_audience=["administrators", "security_managers"],
            steps=[],
            status=WizardStatus.DRAFT,
            version="1.0",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            created_by="system",
            estimated_completion_time="18 minutes",
            success_rate=0.91,
            average_completion_time="16 minutes",
            prerequisites=[],
            post_completion_actions=[],
            tenant_specific=True,
            customizable=True,
            category="security",
            tags=["security", "access", "policies"],
            icon="shield",
            color="#dc2626"
        )
    
    def _create_branding_setup_wizard(self) -> Wizard:
        """Create branding setup wizard"""
        return Wizard(
            id="branding_setup_v1",
            name="Branding Setup",
            description="Configure brand identity and appearance",
            wizard_type=WizardType.BRANDING_SETUP,
            target_audience=["administrators", "brand_managers"],
            steps=[],
            status=WizardStatus.ACTIVE,
            version="1.0",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            created_by="system",
            estimated_completion_time="20 minutes",
            success_rate=0.88,
            average_completion_time="18 minutes",
            prerequisites=[],
            post_completion_actions=[],
            tenant_specific=True,
            customizable=True,
            category="branding",
            tags=["branding", "design", "identity"],
            icon="palette",
            color="#ec4899"
        )
    
    def _create_team_setup_wizard(self) -> Wizard:
        """Create team setup wizard"""
        return Wizard(
            id="team_setup_v1",
            name="Team Setup",
            description="Set up teams and user roles",
            wizard_type=WizardType.TEAM_SETUP,
            target_audience=["administrators", "hr_managers"],
            steps=[],
            status=WizardStatus.ACTIVE,
            version="1.0",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            created_by="system",
            estimated_completion_time="25 minutes",
            success_rate=0.86,
            average_completion_time="22 minutes",
            prerequisites=[],
            post_completion_actions=[],
            tenant_specific=True,
            customizable=True,
            category="team",
            tags=["team", "users", "roles"],
            icon="users",
            color="#059669"
        )
    
    def _create_project_initialization_wizard(self) -> Wizard:
        """Create project initialization wizard"""
        return Wizard(
            id="project_init_v1",
            name="Project Initialization",
            description="Initialize new project with templates and configurations",
            wizard_type=WizardType.PROJECT_INITIALIZATION,
            target_audience=["project_managers", "administrators"],
            steps=[],
            status=WizardStatus.ACTIVE,
            version="1.0",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            created_by="system",
            estimated_completion_time="30 minutes",
            success_rate=0.83,
            average_completion_time="28 minutes",
            prerequisites=[],
            post_completion_actions=[],
            tenant_specific=True,
            customizable=True,
            category="project",
            tags=["project", "initialization", "setup"],
            icon="folder-plus",
            color="#0d9488"
        )
    
    def _create_migration_wizard(self) -> Wizard:
        """Create data migration wizard"""
        return Wizard(
            id="migration_wizard_v1",
            name="Data Migration",
            description="Migrate data from external systems",
            wizard_type=WizardType.MIGRATION_WIZARD,
            target_audience=["administrators", "data_engineers"],
            steps=[],
            status=WizardStatus.ACTIVE,
            version="1.0",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            created_by="system",
            estimated_completion_time="45 minutes",
            success_rate=0.79,
            average_completion_time="42 minutes",
            prerequisites=["backup_created"],
            post_completion_actions=[
                {"action": "validate_migration", "config": {"auto_validate": True}}
            ],
            tenant_specific=True,
            customizable=False,
            category="migration",
            tags=["migration", "data", "import"],
            icon="database",
            color="#7c3aed"
        )
    
    def _wizard_exists(self, wizard_id: str) -> bool:
        """Check if wizard already exists"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM wizards WHERE id = ?', (wizard_id,))
        exists = cursor.fetchone()[0] > 0
        conn.close()
        return exists
    
    def _serialize_step(self, step: WizardStep) -> Dict[str, Any]:
        """Convert WizardStep to JSON-serializable dictionary"""
        step_dict = asdict(step)
        step_dict['step_type'] = step.step_type.value  # Convert enum to string
        return step_dict
    
    def create_wizard(self, wizard: Wizard) -> str:
        """Create a new wizard"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Serialize steps with enum conversion
        serialized_steps = [self._serialize_step(step) for step in wizard.steps]
        
        cursor.execute('''
            INSERT INTO wizards 
            (id, name, description, wizard_type, target_audience, steps, status, version,
             created_at, updated_at, created_by, estimated_completion_time, success_rate,
             average_completion_time, prerequisites, post_completion_actions, tenant_specific,
             customizable, category, tags, icon, color)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            wizard.id, wizard.name, wizard.description, wizard.wizard_type.value,
            json.dumps(wizard.target_audience), json.dumps(serialized_steps),
            wizard.status.value, wizard.version, wizard.created_at.isoformat(),
            wizard.updated_at.isoformat(), wizard.created_by, wizard.estimated_completion_time,
            wizard.success_rate, wizard.average_completion_time, json.dumps(wizard.prerequisites),
            json.dumps(wizard.post_completion_actions), wizard.tenant_specific,
            wizard.customizable, wizard.category, json.dumps(wizard.tags or []),
            wizard.icon, wizard.color
        ))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Created wizard: {wizard.name} ({wizard.id})")
        return wizard.id
    
    def get_wizards(self, category: Optional[str] = None, wizard_type: Optional[WizardType] = None, 
                   status: Optional[WizardStatus] = None) -> List[Dict[str, Any]]:
        """Get wizards with optional filtering"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT * FROM wizards WHERE 1=1"
        params = []
        
        if category:
            query += " AND category = ?"
            params.append(category)
        
        if wizard_type:
            query += " AND wizard_type = ?"
            params.append(wizard_type.value)
        
        if status:
            query += " AND status = ?"
            params.append(status.value)
        
        query += " ORDER BY name"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        columns = ['id', 'name', 'description', 'wizard_type', 'target_audience', 'steps', 
                   'status', 'version', 'created_at', 'updated_at', 'created_by',
                   'estimated_completion_time', 'success_rate', 'average_completion_time',
                   'prerequisites', 'post_completion_actions', 'tenant_specific',
                   'customizable', 'category', 'tags', 'icon', 'color']
        
        wizards = []
        for row in rows:
            wizard_dict = dict(zip(columns, row))
            
            # Parse JSON fields
            json_fields = ['target_audience', 'steps', 'prerequisites', 'post_completion_actions', 'tags']
            for field in json_fields:
                try:
                    wizard_dict[field] = json.loads(wizard_dict[field]) if wizard_dict[field] else []
                except json.JSONDecodeError:
                    wizard_dict[field] = []
            
            wizards.append(wizard_dict)
        
        return wizards
    
    def start_wizard_execution(self, wizard_id: str, user_id: str, tenant_id: str) -> str:
        """Start a new wizard execution"""
        execution_id = str(uuid.uuid4())
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO wizard_executions
            (id, wizard_id, user_id, tenant_id, started_at, current_step, status,
             step_data, completion_percentage, execution_metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            execution_id, wizard_id, user_id, tenant_id, datetime.now().isoformat(),
            0, "in_progress", "{}", 0, "{}"
        ))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Started wizard execution: {execution_id} for wizard: {wizard_id}")
        return execution_id
    
    def update_wizard_execution(self, execution_id: str, step_data: Dict[str, Any], 
                               current_step: int, completion_percentage: int) -> bool:
        """Update wizard execution progress"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE wizard_executions
            SET step_data = ?, current_step = ?, completion_percentage = ?
            WHERE id = ?
        ''', (json.dumps(step_data), current_step, completion_percentage, execution_id))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success
    
    def complete_wizard_execution(self, execution_id: str) -> bool:
        """Mark wizard execution as completed"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE wizard_executions
            SET status = 'completed', completed_at = ?, completion_percentage = 100
            WHERE id = ?
        ''', (datetime.now().isoformat(), execution_id))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        if success:
            logger.info(f"Completed wizard execution: {execution_id}")
        
        return success
    
    def get_wizard_analytics(self, wizard_id: Optional[str] = None, 
                           timeframe_days: int = 30) -> Dict[str, Any]:
        """Get analytics for wizard performance"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get execution stats
        query = '''
            SELECT 
                wizard_id,
                COUNT(*) as total_starts,
                COUNT(CASE WHEN status = 'completed' THEN 1 END) as completions,
                COUNT(CASE WHEN status = 'abandoned' THEN 1 END) as abandonments,
                AVG(completion_percentage) as avg_completion,
                AVG(CASE WHEN status = 'completed' THEN 
                    (julianday(completed_at) - julianday(started_at)) * 24 * 60 END) as avg_completion_time_minutes
            FROM wizard_executions 
            WHERE started_at > datetime('now', '-{} days')
        '''.format(timeframe_days)
        
        if wizard_id:
            query += " AND wizard_id = ?"
            cursor.execute(query + " GROUP BY wizard_id", (wizard_id,))
        else:
            cursor.execute(query + " GROUP BY wizard_id")
        
        execution_stats = cursor.fetchall()
        
        # Get step-level analytics
        step_query = '''
            SELECT wizard_id, current_step, COUNT(*) as step_completions
            FROM wizard_executions 
            WHERE started_at > datetime('now', '-{} days')
        '''.format(timeframe_days)
        
        if wizard_id:
            step_query += " AND wizard_id = ?"
            cursor.execute(step_query + " GROUP BY wizard_id, current_step ORDER BY wizard_id, current_step", (wizard_id,))
        else:
            cursor.execute(step_query + " GROUP BY wizard_id, current_step ORDER BY wizard_id, current_step")
        
        step_stats = cursor.fetchall()
        conn.close()
        
        analytics = {
            "timeframe_days": timeframe_days,
            "execution_stats": [
                {
                    "wizard_id": row[0],
                    "total_starts": row[1],
                    "completions": row[2],
                    "abandonments": row[3],
                    "completion_rate": row[2] / row[1] if row[1] > 0 else 0,
                    "avg_completion_percentage": round(row[4], 2) if row[4] else 0,
                    "avg_completion_time_minutes": round(row[5], 2) if row[5] else 0
                }
                for row in execution_stats
            ],
            "step_completion_stats": [
                {
                    "wizard_id": row[0],
                    "step": row[1],
                    "completions": row[2]
                }
                for row in step_stats
            ]
        }
        
        return analytics

async def main():
    """Test the wizard manager"""
    print("🧙 BizOSaaS Comprehensive Wizard Management System")
    print("=" * 60)
    
    wizard_manager = WizardManager()
    
    # Get all wizards
    wizards = wizard_manager.get_wizards()
    print(f"Loaded {len(wizards)} default wizards:")
    
    for wizard in wizards:
        print(f"  • {wizard['name']} ({wizard['wizard_type']}) - {len(wizard['steps'])} steps")
    
    # Get analytics
    analytics = wizard_manager.get_wizard_analytics()
    print(f"\nAnalytics loaded for {len(analytics['execution_stats'])} wizards")

if __name__ == "__main__":
    asyncio.run(main())