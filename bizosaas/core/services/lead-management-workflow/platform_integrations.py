"""
Platform Integrations for Lead Management Workflow
Integration with Django CRM, AI Crew System, Analytics, and Notification Services
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json
import aioredis
import asyncpg
import httpx
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IntegrationStatus(Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"
    SYNCING = "syncing"

class SyncDirection(Enum):
    BIDIRECTIONAL = "bidirectional"
    TO_PLATFORM = "to_platform"
    FROM_PLATFORM = "from_platform"

@dataclass
class IntegrationConfig:
    """Configuration for platform integrations"""
    service_name: str
    endpoint_url: str
    api_key: str
    sync_direction: SyncDirection = SyncDirection.BIDIRECTIONAL
    sync_interval_minutes: int = 15
    retry_attempts: int = 3
    timeout_seconds: int = 30
    enabled: bool = True
    
    # Mapping configuration
    field_mappings: Dict[str, str] = field(default_factory=dict)
    sync_filters: Dict[str, Any] = field(default_factory=dict)
    
    # Status tracking
    last_sync: Optional[datetime] = None
    status: IntegrationStatus = IntegrationStatus.DISCONNECTED
    error_count: int = 0

class DjangoCRMIntegration:
    """Integration with Django CRM system"""
    
    def __init__(self, config: IntegrationConfig):
        self.config = config
        self.base_url = config.endpoint_url.rstrip('/')
        self.headers = {
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json"
        }
        self.session = None
        
    async def initialize(self):
        """Initialize CRM integration"""
        try:
            self.session = httpx.AsyncClient(
                timeout=httpx.Timeout(self.config.timeout_seconds),
                headers=self.headers
            )
            
            # Test connection
            await self._test_connection()
            self.config.status = IntegrationStatus.CONNECTED
            
            logger.info("Django CRM integration initialized successfully")
            
        except Exception as e:
            self.config.status = IntegrationStatus.ERROR
            logger.error(f"Failed to initialize Django CRM integration: {e}")
            raise
    
    async def _test_connection(self):
        """Test connection to Django CRM API"""
        try:
            response = await self.session.get(f"{self.base_url}/api/health/")
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"CRM connection test failed: {e}")
            raise
    
    async def sync_lead_data(self, lead_id: str, lead_data: Dict[str, Any]) -> bool:
        """Sync lead data to Django CRM"""
        try:
            # Map fields according to CRM schema
            crm_lead_data = self._map_lead_data_to_crm(lead_data)
            
            # Check if lead exists in CRM
            existing_lead = await self._get_crm_lead(lead_id)
            
            if existing_lead:
                # Update existing lead
                response = await self.session.put(
                    f"{self.base_url}/api/leads/{lead_id}/",
                    json=crm_lead_data
                )
            else:
                # Create new lead
                crm_lead_data["external_id"] = lead_id
                response = await self.session.post(
                    f"{self.base_url}/api/leads/",
                    json=crm_lead_data
                )
            
            response.raise_for_status()
            
            logger.info(f"Successfully synced lead {lead_id} to CRM")
            return True
            
        except Exception as e:
            logger.error(f"Error syncing lead {lead_id} to CRM: {e}")
            self.config.error_count += 1
            return False
    
    async def sync_lead_assignment(self, assignment_data: Dict[str, Any]) -> bool:
        """Sync lead assignment to Django CRM"""
        try:
            crm_assignment_data = {
                "lead_id": assignment_data["lead_id"],
                "assigned_user_id": assignment_data["rep_id"],
                "assignment_strategy": assignment_data["strategy_used"],
                "assignment_score": assignment_data.get("assignment_score", 0),
                "assigned_at": assignment_data["assigned_at"],
                "priority": assignment_data.get("priority", "medium"),
                "metadata": assignment_data.get("metadata", {})
            }
            
            response = await self.session.post(
                f"{self.base_url}/api/lead-assignments/",
                json=crm_assignment_data
            )
            response.raise_for_status()
            
            logger.info(f"Successfully synced assignment for lead {assignment_data['lead_id']} to CRM")
            return True
            
        except Exception as e:
            logger.error(f"Error syncing assignment to CRM: {e}")
            return False
    
    async def sync_lead_score(self, lead_id: str, scoring_data: Dict[str, Any]) -> bool:
        """Sync lead score to Django CRM"""
        try:
            crm_score_data = {
                "lead_id": lead_id,
                "total_score": scoring_data["total_score"],
                "demographic_score": scoring_data["scores"].get("demographic", 0),
                "behavioral_score": scoring_data["scores"].get("behavioral", 0),
                "engagement_score": scoring_data["scores"].get("engagement", 0),
                "fit_score": scoring_data["scores"].get("fit", 0),
                "ai_qualification_score": scoring_data["scores"].get("ai_qualification", 0),
                "qualification_level": scoring_data["qualification_level"],
                "confidence": scoring_data.get("confidence", 0),
                "recommendations": scoring_data.get("recommendations", []),
                "scored_at": scoring_data["updated_at"]
            }
            
            response = await self.session.post(
                f"{self.base_url}/api/lead-scores/",
                json=crm_score_data
            )
            response.raise_for_status()
            
            logger.info(f"Successfully synced score for lead {lead_id} to CRM")
            return True
            
        except Exception as e:
            logger.error(f"Error syncing score to CRM: {e}")
            return False
    
    async def get_sales_representatives(self) -> List[Dict[str, Any]]:
        """Get sales representatives from Django CRM"""
        try:
            response = await self.session.get(f"{self.base_url}/api/users/?role=sales_rep")
            response.raise_for_status()
            
            crm_reps = response.json().get("results", [])
            
            # Map CRM rep data to our format
            mapped_reps = []
            for rep in crm_reps:
                mapped_rep = {
                    "rep_id": str(rep["id"]),
                    "name": f"{rep['first_name']} {rep['last_name']}",
                    "email": rep["email"],
                    "team": rep.get("team", "default"),
                    "skills": rep.get("skills", []),
                    "industries": rep.get("industries", []),
                    "territories": rep.get("territories", []),
                    "status": rep.get("status", "available"),
                    "max_daily_leads": rep.get("max_daily_leads", 10),
                    "max_concurrent_leads": rep.get("max_concurrent_leads", 50)
                }
                mapped_reps.append(mapped_rep)
            
            return mapped_reps
            
        except Exception as e:
            logger.error(f"Error getting sales reps from CRM: {e}")
            return []
    
    async def _get_crm_lead(self, lead_id: str) -> Optional[Dict[str, Any]]:
        """Get lead from CRM by external ID"""
        try:
            response = await self.session.get(
                f"{self.base_url}/api/leads/?external_id={lead_id}"
            )
            response.raise_for_status()
            
            results = response.json().get("results", [])
            return results[0] if results else None
            
        except Exception as e:
            logger.error(f"Error getting CRM lead {lead_id}: {e}")
            return None
    
    def _map_lead_data_to_crm(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Map lead data to Django CRM format"""
        return {
            "company_name": lead_data.get("company_name", ""),
            "contact_email": lead_data.get("email", ""),
            "contact_phone": lead_data.get("phone_number", ""),
            "industry": lead_data.get("industry", ""),
            "company_size": lead_data.get("company_size", 0),
            "location": lead_data.get("location", ""),
            "job_title": lead_data.get("job_title", ""),
            "budget": lead_data.get("budget", 0),
            "timeline": lead_data.get("timeline", ""),
            "source": lead_data.get("referral_source", "unknown"),
            "status": lead_data.get("status", "new"),
            "notes": lead_data.get("notes", ""),
            "tags": lead_data.get("service_requirements", []),
            "created_at": lead_data.get("created_at", datetime.utcnow().isoformat()),
            "updated_at": datetime.utcnow().isoformat()
        }
    
    async def cleanup(self):
        """Cleanup CRM integration"""
        if self.session:
            await self.session.aclose()

class AICrewIntegration:
    """Integration with AI Crew System"""
    
    def __init__(self, config: IntegrationConfig):
        self.config = config
        self.base_url = config.endpoint_url.rstrip('/')
        self.headers = {
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json"
        }
        self.session = None
    
    async def initialize(self):
        """Initialize AI Crew integration"""
        try:
            self.session = httpx.AsyncClient(
                timeout=httpx.Timeout(self.config.timeout_seconds),
                headers=self.headers
            )
            
            # Test connection
            await self._test_connection()
            self.config.status = IntegrationStatus.CONNECTED
            
            logger.info("AI Crew integration initialized successfully")
            
        except Exception as e:
            self.config.status = IntegrationStatus.ERROR
            logger.error(f"Failed to initialize AI Crew integration: {e}")
            raise
    
    async def _test_connection(self):
        """Test connection to AI Crew API"""
        try:
            response = await self.session.get(f"{self.base_url}/health")
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"AI Crew connection test failed: {e}")
            raise
    
    async def trigger_lead_qualification(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Trigger AI crew for advanced lead qualification"""
        try:
            qualification_request = {
                "lead_id": lead_data["lead_id"],
                "company_data": {
                    "name": lead_data.get("company_name"),
                    "size": lead_data.get("company_size"),
                    "industry": lead_data.get("industry"),
                    "location": lead_data.get("location")
                },
                "contact_data": {
                    "job_title": lead_data.get("job_title"),
                    "email": lead_data.get("email"),
                    "phone": lead_data.get("phone_number")
                },
                "behavioral_data": {
                    "website_visits": lead_data.get("website_visits", 0),
                    "email_opens": lead_data.get("email_opens", 0),
                    "content_downloads": lead_data.get("content_downloads", 0)
                },
                "requirements": {
                    "budget": lead_data.get("budget"),
                    "timeline": lead_data.get("timeline"),
                    "services": lead_data.get("service_requirements", [])
                }
            }
            
            response = await self.session.post(
                f"{self.base_url}/agents/lead-qualification",
                json=qualification_request
            )
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"AI qualification completed for lead {lead_data['lead_id']}")
            
            return {
                "qualification_score": result.get("score", 0),
                "qualification_level": result.get("level", "unknown"),
                "ai_insights": result.get("insights", []),
                "recommended_actions": result.get("actions", []),
                "confidence": result.get("confidence", 0),
                "analysis_id": result.get("analysis_id")
            }
            
        except Exception as e:
            logger.error(f"Error in AI lead qualification: {e}")
            return {
                "qualification_score": 0,
                "qualification_level": "unknown",
                "ai_insights": [],
                "recommended_actions": [],
                "confidence": 0,
                "error": str(e)
            }
    
    async def trigger_campaign_optimization(self, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """Trigger AI crew for campaign optimization"""
        try:
            optimization_request = {
                "campaign_id": campaign_data["campaign_id"],
                "campaign_type": campaign_data["campaign_type"],
                "performance_data": campaign_data.get("performance_metrics", {}),
                "target_audience": campaign_data.get("target_segments", []),
                "current_content": campaign_data.get("content_analysis", {}),
                "goals": campaign_data.get("conversion_goals", [])
            }
            
            response = await self.session.post(
                f"{self.base_url}/agents/campaign-optimization",
                json=optimization_request
            )
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"AI campaign optimization completed for {campaign_data['campaign_id']}")
            
            return {
                "optimization_score": result.get("score", 0),
                "recommendations": result.get("recommendations", []),
                "content_suggestions": result.get("content_suggestions", []),
                "timing_optimization": result.get("timing_optimization", {}),
                "segment_insights": result.get("segment_insights", []),
                "predicted_improvement": result.get("predicted_improvement", 0)
            }
            
        except Exception as e:
            logger.error(f"Error in AI campaign optimization: {e}")
            return {
                "optimization_score": 0,
                "recommendations": [],
                "error": str(e)
            }
    
    async def generate_personalized_content(self, content_request: Dict[str, Any]) -> Dict[str, Any]:
        """Generate personalized content using AI crew"""
        try:
            response = await self.session.post(
                f"{self.base_url}/agents/content-generation",
                json=content_request
            )
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"AI content generation completed")
            
            return {
                "generated_content": result.get("content", ""),
                "personalization_score": result.get("personalization_score", 0),
                "tone_analysis": result.get("tone_analysis", {}),
                "suggestions": result.get("suggestions", [])
            }
            
        except Exception as e:
            logger.error(f"Error in AI content generation: {e}")
            return {"generated_content": "", "error": str(e)}
    
    async def cleanup(self):
        """Cleanup AI Crew integration"""
        if self.session:
            await self.session.aclose()

class AnalyticsIntegration:
    """Integration with Apache Superset Analytics"""
    
    def __init__(self, config: IntegrationConfig):
        self.config = config
        self.base_url = config.endpoint_url.rstrip('/')
        self.headers = {
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json"
        }
        self.session = None
    
    async def initialize(self):
        """Initialize Analytics integration"""
        try:
            self.session = httpx.AsyncClient(
                timeout=httpx.Timeout(self.config.timeout_seconds),
                headers=self.headers
            )
            
            # Test connection
            await self._test_connection()
            self.config.status = IntegrationStatus.CONNECTED
            
            logger.info("Analytics integration initialized successfully")
            
        except Exception as e:
            self.config.status = IntegrationStatus.ERROR
            logger.error(f"Failed to initialize Analytics integration: {e}")
            raise
    
    async def _test_connection(self):
        """Test connection to Superset API"""
        try:
            response = await self.session.get(f"{self.base_url}/api/v1/security/login")
            return True
        except Exception as e:
            logger.error(f"Analytics connection test failed: {e}")
            raise
    
    async def send_lead_metrics(self, metrics_data: Dict[str, Any]) -> bool:
        """Send lead metrics to analytics platform"""
        try:
            # Format metrics for Superset
            superset_metrics = {
                "dataset": "lead_metrics",
                "timestamp": datetime.utcnow().isoformat(),
                "metrics": {
                    "lead_score": metrics_data.get("total_score", 0),
                    "qualification_level": metrics_data.get("qualification_level", "unknown"),
                    "company_size": metrics_data.get("company_size", 0),
                    "industry": metrics_data.get("industry", ""),
                    "source": metrics_data.get("referral_source", "unknown"),
                    "conversion_probability": metrics_data.get("conversion_probability", 0)
                },
                "dimensions": {
                    "lead_id": metrics_data["lead_id"],
                    "date": datetime.utcnow().date().isoformat(),
                    "month": datetime.utcnow().strftime("%Y-%m"),
                    "quarter": f"Q{(datetime.utcnow().month - 1) // 3 + 1}-{datetime.utcnow().year}"
                }
            }
            
            # Send to analytics ingestion endpoint
            response = await self.session.post(
                f"{self.base_url}/api/v1/data/ingest",
                json=superset_metrics
            )
            response.raise_for_status()
            
            logger.info(f"Successfully sent lead metrics for {metrics_data['lead_id']}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending lead metrics: {e}")
            return False
    
    async def send_campaign_metrics(self, campaign_metrics: Dict[str, Any]) -> bool:
        """Send campaign metrics to analytics platform"""
        try:
            superset_metrics = {
                "dataset": "campaign_metrics",
                "timestamp": datetime.utcnow().isoformat(),
                "metrics": {
                    "enrollments": campaign_metrics.get("total_enrollments", 0),
                    "completion_rate": campaign_metrics.get("completion_rate", 0),
                    "conversion_rate": campaign_metrics.get("conversion_rate", 0),
                    "engagement_score": campaign_metrics.get("avg_engagement_score", 0),
                    "email_open_rate": campaign_metrics.get("email_open_rate", 0),
                    "click_through_rate": campaign_metrics.get("click_through_rate", 0)
                },
                "dimensions": {
                    "campaign_id": campaign_metrics["campaign_id"],
                    "campaign_type": campaign_metrics.get("campaign_type", ""),
                    "date": datetime.utcnow().date().isoformat(),
                    "month": datetime.utcnow().strftime("%Y-%m")
                }
            }
            
            response = await self.session.post(
                f"{self.base_url}/api/v1/data/ingest",
                json=superset_metrics
            )
            response.raise_for_status()
            
            logger.info(f"Successfully sent campaign metrics for {campaign_metrics['campaign_id']}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending campaign metrics: {e}")
            return False
    
    async def send_assignment_metrics(self, assignment_metrics: Dict[str, Any]) -> bool:
        """Send assignment metrics to analytics platform"""
        try:
            superset_metrics = {
                "dataset": "assignment_metrics",
                "timestamp": datetime.utcnow().isoformat(),
                "metrics": {
                    "assignment_score": assignment_metrics.get("assignment_score", 0),
                    "skill_match_score": assignment_metrics.get("skill_match_score", 0),
                    "workload_score": assignment_metrics.get("workload_score", 0),
                    "response_time_hours": assignment_metrics.get("response_time_hours", 0),
                    "conversion_achieved": 1 if assignment_metrics.get("conversion_achieved") else 0
                },
                "dimensions": {
                    "assignment_id": assignment_metrics["assignment_id"],
                    "lead_id": assignment_metrics["lead_id"],
                    "rep_id": assignment_metrics["rep_id"],
                    "strategy": assignment_metrics.get("strategy_used", ""),
                    "priority": assignment_metrics.get("priority", ""),
                    "date": datetime.utcnow().date().isoformat()
                }
            }
            
            response = await self.session.post(
                f"{self.base_url}/api/v1/data/ingest",
                json=superset_metrics
            )
            response.raise_for_status()
            
            logger.info(f"Successfully sent assignment metrics for {assignment_metrics['assignment_id']}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending assignment metrics: {e}")
            return False
    
    async def cleanup(self):
        """Cleanup Analytics integration"""
        if self.session:
            await self.session.aclose()

class NotificationIntegration:
    """Integration with Notification Service"""
    
    def __init__(self, config: IntegrationConfig, redis: aioredis.Redis):
        self.config = config
        self.redis = redis
        self.notification_templates = {}
    
    async def initialize(self):
        """Initialize notification integration"""
        try:
            # Load notification templates
            await self._load_notification_templates()
            self.config.status = IntegrationStatus.CONNECTED
            
            logger.info("Notification integration initialized successfully")
            
        except Exception as e:
            self.config.status = IntegrationStatus.ERROR
            logger.error(f"Failed to initialize Notification integration: {e}")
            raise
    
    async def _load_notification_templates(self):
        """Load notification templates"""
        self.notification_templates = {
            "lead_assigned": {
                "email": {
                    "subject": "New Lead Assigned: {company_name}",
                    "body": "You have been assigned a new lead: {company_name} ({lead_score} points). Please follow up within 24 hours."
                },
                "sms": {
                    "body": "New lead assigned: {company_name}. Score: {lead_score}. Follow up ASAP."
                }
            },
            "high_value_lead": {
                "email": {
                    "subject": "HIGH VALUE LEAD: {company_name}",
                    "body": "A high-value lead ({lead_score} points) has been assigned. Immediate attention required."
                },
                "slack": {
                    "body": "🚨 HIGH VALUE LEAD: {company_name} (Score: {lead_score}) assigned to {rep_name}"
                }
            },
            "campaign_completed": {
                "email": {
                    "subject": "Campaign Completed: {campaign_name}",
                    "body": "Lead {company_name} has completed the {campaign_name} campaign. Consider next steps."
                }
            },
            "assignment_escalation": {
                "email": {
                    "subject": "ESCALATION: Lead Assignment Requires Attention",
                    "body": "Lead {company_name} assigned to {rep_name} requires manager attention. Reason: {escalation_reason}"
                }
            }
        }
    
    async def send_lead_assignment_notification(self, assignment_data: Dict[str, Any], 
                                              rep_data: Dict[str, Any]) -> bool:
        """Send lead assignment notification"""
        try:
            template_data = {
                "company_name": assignment_data.get("company_name", "Unknown Company"),
                "lead_score": assignment_data.get("assignment_score", 0),
                "rep_name": rep_data.get("name", ""),
                "priority": assignment_data.get("priority", "medium")
            }
            
            # Determine notification channels based on priority
            channels = ["email"]
            if assignment_data.get("priority") in ["high", "urgent"]:
                channels.extend(["sms", "slack"])
            
            template_key = "high_value_lead" if assignment_data.get("priority") == "urgent" else "lead_assigned"
            
            success = True
            for channel in channels:
                if channel in self.notification_templates[template_key]:
                    notification_success = await self._send_notification(
                        channel, 
                        rep_data.get("email", ""),
                        self.notification_templates[template_key][channel],
                        template_data
                    )
                    success = success and notification_success
            
            return success
            
        except Exception as e:
            logger.error(f"Error sending assignment notification: {e}")
            return False
    
    async def send_campaign_notification(self, notification_type: str, 
                                       recipient: str, data: Dict[str, Any]) -> bool:
        """Send campaign-related notification"""
        try:
            if notification_type not in self.notification_templates:
                logger.warning(f"Unknown notification type: {notification_type}")
                return False
            
            template = self.notification_templates[notification_type]["email"]
            
            return await self._send_notification("email", recipient, template, data)
            
        except Exception as e:
            logger.error(f"Error sending campaign notification: {e}")
            return False
    
    async def send_escalation_notification(self, escalation_data: Dict[str, Any]) -> bool:
        """Send escalation notification to managers"""
        try:
            template = self.notification_templates["assignment_escalation"]["email"]
            
            # Send to multiple channels for escalations
            notification_data = {
                "type": "escalation_alert",
                "data": escalation_data,
                "template": template,
                "timestamp": datetime.utcnow().isoformat(),
                "priority": "urgent"
            }
            
            # Queue for immediate processing
            await self.redis.lpush("urgent_notifications", json.dumps(notification_data))
            
            logger.info(f"Escalation notification queued for assignment {escalation_data.get('assignment_id')}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending escalation notification: {e}")
            return False
    
    async def _send_notification(self, channel: str, recipient: str, 
                               template: Dict[str, str], data: Dict[str, Any]) -> bool:
        """Send notification through specified channel"""
        try:
            # Format template with data
            formatted_content = {}
            for key, content in template.items():
                formatted_content[key] = content.format(**data)
            
            notification_message = {
                "channel": channel,
                "recipient": recipient,
                "content": formatted_content,
                "data": data,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Queue notification for delivery
            queue_name = f"{channel}_notification_queue"
            await self.redis.lpush(queue_name, json.dumps(notification_message))
            
            logger.info(f"Notification queued for {channel}: {recipient}")
            return True
            
        except Exception as e:
            logger.error(f"Error queueing notification: {e}")
            return False

class PlatformIntegrationManager:
    """Main manager for all platform integrations"""
    
    def __init__(self, db_config: Dict[str, str], redis_config: Dict[str, str]):
        self.db_config = db_config
        self.redis_config = redis_config
        self.integrations = {}
        self.sync_tasks = {}
        
        # Integration configs
        self.integration_configs = {}
        
    async def initialize(self):
        """Initialize all platform integrations"""
        try:
            # Initialize database connection
            self.db_pool = await asyncpg.create_pool(**self.db_config)
            
            # Initialize Redis connection
            self.redis = await aioredis.from_url(
                f"redis://{self.redis_config['host']}:{self.redis_config['port']}"
            )
            
            # Load integration configurations
            await self._load_integration_configs()
            
            # Initialize integrations
            await self._initialize_integrations()
            
            # Start sync tasks
            await self._start_sync_tasks()
            
            logger.info("Platform integration manager initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize platform integration manager: {e}")
            raise
    
    async def _load_integration_configs(self):
        """Load integration configurations from database"""
        try:
            async with self.db_pool.acquire() as conn:
                rows = await conn.fetch("""
                    SELECT * FROM platform_integrations WHERE enabled = true
                """)
                
                for row in rows:
                    config = IntegrationConfig(
                        service_name=row["service_name"],
                        endpoint_url=row["endpoint_url"],
                        api_key=row["api_key"],
                        sync_direction=SyncDirection(row["sync_direction"]),
                        sync_interval_minutes=row["sync_interval_minutes"],
                        retry_attempts=row["retry_attempts"],
                        timeout_seconds=row["timeout_seconds"],
                        enabled=row["enabled"],
                        field_mappings=json.loads(row["field_mappings"]) if row["field_mappings"] else {},
                        sync_filters=json.loads(row["sync_filters"]) if row["sync_filters"] else {}
                    )
                    
                    self.integration_configs[row["service_name"]] = config
                
                logger.info(f"Loaded {len(self.integration_configs)} integration configurations")
                
        except Exception as e:
            logger.error(f"Error loading integration configs: {e}")
            # Create default configs if database is empty
            await self._create_default_configs()
    
    async def _create_default_configs(self):
        """Create default integration configurations"""
        default_configs = {
            "django_crm": IntegrationConfig(
                service_name="django_crm",
                endpoint_url="http://localhost:8001",
                api_key="your-crm-api-key",
                sync_direction=SyncDirection.BIDIRECTIONAL,
                sync_interval_minutes=15
            ),
            "ai_crew": IntegrationConfig(
                service_name="ai_crew",
                endpoint_url="http://localhost:8002",
                api_key="your-ai-crew-api-key",
                sync_direction=SyncDirection.TO_PLATFORM
            ),
            "analytics": IntegrationConfig(
                service_name="analytics",
                endpoint_url="http://localhost:8088",
                api_key="your-superset-api-key",
                sync_direction=SyncDirection.TO_PLATFORM
            )
        }
        
        self.integration_configs.update(default_configs)
    
    async def _initialize_integrations(self):
        """Initialize all configured integrations"""
        try:
            # Initialize Django CRM integration
            if "django_crm" in self.integration_configs:
                self.integrations["django_crm"] = DjangoCRMIntegration(
                    self.integration_configs["django_crm"]
                )
                await self.integrations["django_crm"].initialize()
            
            # Initialize AI Crew integration
            if "ai_crew" in self.integration_configs:
                self.integrations["ai_crew"] = AICrewIntegration(
                    self.integration_configs["ai_crew"]
                )
                await self.integrations["ai_crew"].initialize()
            
            # Initialize Analytics integration
            if "analytics" in self.integration_configs:
                self.integrations["analytics"] = AnalyticsIntegration(
                    self.integration_configs["analytics"]
                )
                await self.integrations["analytics"].initialize()
            
            # Initialize Notification integration
            self.integrations["notifications"] = NotificationIntegration(
                IntegrationConfig(
                    service_name="notifications",
                    endpoint_url="internal",
                    api_key="internal"
                ),
                self.redis
            )
            await self.integrations["notifications"].initialize()
            
            logger.info(f"Initialized {len(self.integrations)} integrations")
            
        except Exception as e:
            logger.error(f"Error initializing integrations: {e}")
            raise
    
    async def _start_sync_tasks(self):
        """Start background sync tasks for bidirectional integrations"""
        try:
            for service_name, config in self.integration_configs.items():
                if config.sync_direction == SyncDirection.BIDIRECTIONAL and config.enabled:
                    task = asyncio.create_task(self._sync_worker(service_name))
                    self.sync_tasks[service_name] = task
                    logger.info(f"Started sync task for {service_name}")
            
        except Exception as e:
            logger.error(f"Error starting sync tasks: {e}")
    
    async def _sync_worker(self, service_name: str):
        """Background worker for periodic synchronization"""
        config = self.integration_configs[service_name]
        integration = self.integrations.get(service_name)
        
        if not integration:
            logger.error(f"Integration {service_name} not found for sync worker")
            return
        
        while True:
            try:
                await asyncio.sleep(config.sync_interval_minutes * 60)
                
                if config.status != IntegrationStatus.CONNECTED:
                    logger.warning(f"Skipping sync for {service_name} - not connected")
                    continue
                
                # Perform synchronization based on service type
                if service_name == "django_crm":
                    await self._sync_with_crm(integration)
                
                config.last_sync = datetime.utcnow()
                logger.info(f"Completed sync for {service_name}")
                
            except Exception as e:
                logger.error(f"Error in sync worker for {service_name}: {e}")
                config.error_count += 1
                
                # Mark as error if too many failures
                if config.error_count > config.retry_attempts:
                    config.status = IntegrationStatus.ERROR
                
                await asyncio.sleep(300)  # Wait 5 minutes on error
    
    async def _sync_with_crm(self, crm_integration: DjangoCRMIntegration):
        """Sync data with Django CRM"""
        try:
            # Sync sales representatives
            crm_reps = await crm_integration.get_sales_representatives()
            
            # Update local sales rep data
            async with self.db_pool.acquire() as conn:
                for rep in crm_reps:
                    await conn.execute("""
                        INSERT INTO sales_representatives (
                            rep_id, name, email, team, skills, industries, territories,
                            status, max_daily_leads, max_concurrent_leads, updated_at
                        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
                        ON CONFLICT (rep_id) DO UPDATE SET
                            name = EXCLUDED.name,
                            email = EXCLUDED.email,
                            team = EXCLUDED.team,
                            skills = EXCLUDED.skills,
                            industries = EXCLUDED.industries,
                            territories = EXCLUDED.territories,
                            status = EXCLUDED.status,
                            max_daily_leads = EXCLUDED.max_daily_leads,
                            max_concurrent_leads = EXCLUDED.max_concurrent_leads,
                            updated_at = EXCLUDED.updated_at
                    """,
                        rep["rep_id"], rep["name"], rep["email"], rep["team"],
                        json.dumps(rep["skills"]), json.dumps(rep["industries"]),
                        json.dumps(rep["territories"]), rep["status"],
                        rep["max_daily_leads"], rep["max_concurrent_leads"],
                        datetime.utcnow()
                    )
            
            logger.info(f"Synced {len(crm_reps)} sales representatives from CRM")
            
        except Exception as e:
            logger.error(f"Error syncing with CRM: {e}")
    
    # Public interface methods
    
    async def sync_lead_to_crm(self, lead_data: Dict[str, Any]) -> bool:
        """Sync lead data to Django CRM"""
        crm_integration = self.integrations.get("django_crm")
        if not crm_integration:
            logger.warning("Django CRM integration not available")
            return False
        
        return await crm_integration.sync_lead_data(lead_data["lead_id"], lead_data)
    
    async def sync_assignment_to_crm(self, assignment_data: Dict[str, Any]) -> bool:
        """Sync assignment data to Django CRM"""
        crm_integration = self.integrations.get("django_crm")
        if not crm_integration:
            return False
        
        return await crm_integration.sync_lead_assignment(assignment_data)
    
    async def sync_score_to_crm(self, lead_id: str, scoring_data: Dict[str, Any]) -> bool:
        """Sync lead score to Django CRM"""
        crm_integration = self.integrations.get("django_crm")
        if not crm_integration:
            return False
        
        return await crm_integration.sync_lead_score(lead_id, scoring_data)
    
    async def get_ai_qualification(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get AI qualification for lead"""
        ai_integration = self.integrations.get("ai_crew")
        if not ai_integration:
            return {"error": "AI Crew integration not available"}
        
        return await ai_integration.trigger_lead_qualification(lead_data)
    
    async def optimize_campaign(self, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get AI campaign optimization recommendations"""
        ai_integration = self.integrations.get("ai_crew")
        if not ai_integration:
            return {"error": "AI Crew integration not available"}
        
        return await ai_integration.trigger_campaign_optimization(campaign_data)
    
    async def send_analytics_data(self, data_type: str, metrics_data: Dict[str, Any]) -> bool:
        """Send metrics data to analytics platform"""
        analytics_integration = self.integrations.get("analytics")
        if not analytics_integration:
            return False
        
        if data_type == "lead_metrics":
            return await analytics_integration.send_lead_metrics(metrics_data)
        elif data_type == "campaign_metrics":
            return await analytics_integration.send_campaign_metrics(metrics_data)
        elif data_type == "assignment_metrics":
            return await analytics_integration.send_assignment_metrics(metrics_data)
        else:
            logger.warning(f"Unknown analytics data type: {data_type}")
            return False
    
    async def send_notification(self, notification_type: str, data: Dict[str, Any]) -> bool:
        """Send notification through notification service"""
        notification_integration = self.integrations.get("notifications")
        if not notification_integration:
            return False
        
        if notification_type == "lead_assignment":
            return await notification_integration.send_lead_assignment_notification(
                data["assignment_data"], data["rep_data"]
            )
        elif notification_type == "campaign_completed":
            return await notification_integration.send_campaign_notification(
                "campaign_completed", data["recipient"], data
            )
        elif notification_type == "escalation":
            return await notification_integration.send_escalation_notification(data)
        else:
            logger.warning(f"Unknown notification type: {notification_type}")
            return False
    
    async def get_integration_status(self) -> Dict[str, Any]:
        """Get status of all integrations"""
        status_report = {
            "total_integrations": len(self.integrations),
            "connected": 0,
            "error": 0,
            "integrations": {}
        }
        
        for service_name, integration in self.integrations.items():
            config = self.integration_configs.get(service_name)
            if config:
                integration_status = {
                    "status": config.status.value,
                    "last_sync": config.last_sync.isoformat() if config.last_sync else None,
                    "error_count": config.error_count,
                    "enabled": config.enabled
                }
                
                status_report["integrations"][service_name] = integration_status
                
                if config.status == IntegrationStatus.CONNECTED:
                    status_report["connected"] += 1
                elif config.status == IntegrationStatus.ERROR:
                    status_report["error"] += 1
        
        return status_report
    
    async def cleanup(self):
        """Cleanup all integrations and resources"""
        try:
            # Cancel sync tasks
            for task_name, task in self.sync_tasks.items():
                if not task.done():
                    task.cancel()
                    logger.info(f"Cancelled sync task for {task_name}")
            
            # Cleanup integrations
            for integration_name, integration in self.integrations.items():
                if hasattr(integration, 'cleanup'):
                    await integration.cleanup()
                    logger.info(f"Cleaned up {integration_name} integration")
            
            # Close database and Redis connections
            if hasattr(self, 'db_pool'):
                await self.db_pool.close()
            if hasattr(self, 'redis'):
                await self.redis.close()
            
            logger.info("Platform integration manager cleanup completed")
            
        except Exception as e:
            logger.error(f"Error during integration cleanup: {e}")

# Example usage
async def main():
    """Example usage of platform integrations"""
    
    # Configuration
    db_config = {
        "host": "localhost",
        "port": 5432,
        "database": "bizosaas",
        "user": "postgres",
        "password": "password"
    }
    
    redis_config = {
        "host": "localhost",
        "port": 6379
    }
    
    # Initialize integration manager
    integration_manager = PlatformIntegrationManager(db_config, redis_config)
    await integration_manager.initialize()
    
    try:
        # Example: Sync lead to CRM
        lead_data = {
            "lead_id": "lead_123",
            "company_name": "Test Company",
            "email": "contact@testcompany.com",
            "industry": "technology",
            "company_size": 100
        }
        
        success = await integration_manager.sync_lead_to_crm(lead_data)
        print(f"CRM sync successful: {success}")
        
        # Example: Get AI qualification
        ai_result = await integration_manager.get_ai_qualification(lead_data)
        print(f"AI qualification: {ai_result}")
        
        # Example: Get integration status
        status = await integration_manager.get_integration_status()
        print(f"Integration status: {json.dumps(status, indent=2)}")
        
    finally:
        await integration_manager.cleanup()

if __name__ == "__main__":
    asyncio.run(main())