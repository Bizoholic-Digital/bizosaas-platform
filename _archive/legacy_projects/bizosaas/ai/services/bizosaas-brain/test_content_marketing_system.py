"""
Comprehensive Test Suite for Content Marketing Automation System
Tests for all components of the content marketing automation workflow system

This module provides comprehensive testing for:
- Content marketing agents and orchestration
- HITL approval workflows  
- Conservative estimation framework
- Platform integrations
- API endpoints and service layers
- Database models and operations
"""

import asyncio
import pytest
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, List
from unittest.mock import AsyncMock, MagicMock, patch
import httpx

# Import content marketing components
from bizoholic_content_marketing_agents import (
    BizoholicContentMarketingOrchestrator,
    ContentWorkflowType,
    ContentWorkflowConfig,
    HITLContentApprovalLevel,
    ContentAgentRole,
    ContentTaskPriority,
    ContentStrategistAgent,
    ContentCreatorAgent,
    CommunityManagerAgent,
    PerformanceAnalystAgent,
    content_marketing_orchestrator
)

from bizoholic_content_marketing_service import (
    BizoholicContentMarketingService,
    ContentWorkflowRequest,
    ContentCreationRequest,
    ContentCalendarRequest,
    CommunityEngagementRequest,
    ContentPerformanceRequest,
    HITLContentApprovalRequest,
    content_marketing_service
)

from content_marketing_hitl_workflows import (
    ContentMarketingHITLWorkflows,
    ApprovalContext,
    ApprovalCriteria,
    ApprovalDecision,
    RiskLevel,
    ApprovalPriority,
    content_marketing_hitl
)

from content_marketing_conservative_estimation import (
    ContentMarketingConservativeEstimation,
    EstimationContext,
    EstimationType,
    ConfidenceLevel,
    RiskProfile,
    content_marketing_estimation
)

from content_marketing_platform_integrations import (
    ContentMarketingPlatformManager,
    LinkedInIntegration,
    FacebookIntegration,
    TwitterIntegration,
    ContentPost,
    PostingResult,
    PostingStatus,
    PlatformCredentials,
    platform_manager
)

from app.models.content_marketing_models import (
    ContentType,
    ContentStatus,
    ContentPlatform,
    HITLApprovalType,
    AutomationLevel
)

# Test Configuration
TEST_TENANT_ID = "test-tenant-123"
TEST_WORKFLOW_ID = str(uuid.uuid4())
TEST_CONTENT_ID = str(uuid.uuid4())

@pytest.fixture
def sample_brand_guidelines():
    """Sample brand guidelines for testing"""
    return {
        "brand_voice": {
            "tone": "professional",
            "personality": ["trustworthy", "innovative", "approachable"],
            "communication_style": "conversational",
            "vocabulary": ["accessible", "technical-when-needed"]
        },
        "visual_identity": {
            "colors": ["#1E3A8A", "#F59E0B", "#10B981"],
            "fonts": ["Inter", "Roboto"],
            "logo_usage": "always_include_on_branded_content"
        },
        "content_guidelines": {
            "max_paragraph_length": 150,
            "preferred_content_length": {"blog": 1500, "social": 120},
            "required_elements": ["call_to_action", "brand_mention"],
            "prohibited_topics": ["politics", "controversial_topics"]
        }
    }

@pytest.fixture
def sample_target_audience():
    """Sample target audience data for testing"""
    return {
        "primary_persona": {
            "name": "Tech-Savvy Manager",
            "age_range": "30-45",
            "job_title": "Marketing Manager",
            "industry": "Technology",
            "pain_points": ["time_constraints", "ROI_measurement", "keeping_up_with_trends"],
            "content_preferences": ["how_to_guides", "case_studies", "industry_insights"],
            "platforms": ["linkedin", "twitter", "industry_blogs"]
        },
        "secondary_persona": {
            "name": "Small Business Owner",
            "age_range": "25-55",
            "job_title": "Business Owner",
            "industry": "Service_Based",
            "pain_points": ["limited_budget", "limited_time", "marketing_knowledge"],
            "content_preferences": ["quick_tips", "cost_effective_strategies", "success_stories"],
            "platforms": ["facebook", "instagram", "local_websites"]
        }
    }

class TestContentMarketingAgents:
    """Test content marketing AI agents"""
    
    @pytest.mark.asyncio
    async def test_content_strategist_agent(self, sample_brand_guidelines, sample_target_audience):
        """Test content strategist agent functionality"""
        
        agent = ContentStrategistAgent()
        
        # Test strategy development
        task_config = {
            "type": "strategy_development",
            "brand_data": sample_brand_guidelines,
            "business_goals": {
                "primary_goal": "increase_brand_awareness",
                "secondary_goals": ["lead_generation", "thought_leadership"],
                "target_metrics": {
                    "engagement_rate": 0.05,
                    "conversion_rate": 0.02,
                    "brand_mentions": 100
                }
            },
            "audience_segments": [sample_target_audience["primary_persona"]]
        }
        
        result = await agent.execute_task(task_config)
        
        assert result["status"] == "success"
        assert "content_strategy" in result["result"]
        assert "brand_voice" in result["result"]["content_strategy"]
        assert "content_pillars" in result["result"]["content_strategy"]
        assert "distribution_strategy" in result["result"]["content_strategy"]
        
    @pytest.mark.asyncio
    async def test_content_creator_agent(self, sample_brand_guidelines, sample_target_audience):
        """Test content creator agent functionality"""
        
        agent = ContentCreatorAgent()
        
        # Test blog content creation
        task_config = {
            "content_type": ContentType.BLOG_POST,
            "topic": "AI-Powered Marketing Automation",
            "keywords": ["marketing automation", "AI", "efficiency", "ROI"],
            "brand_voice": sample_brand_guidelines["brand_voice"],
            "target_audience": sample_target_audience["primary_persona"],
            "word_count": 1500,
            "include_seo": True
        }
        
        result = await agent.execute_task(task_config)
        
        assert result["status"] == "success"
        assert result["result"]["content_type"] == ContentType.BLOG_POST
        assert "content_data" in result["result"]
        assert "quality_metrics" in result["result"]
        assert result["result"]["quality_metrics"]["seo_score"] > 0.7
        
    @pytest.mark.asyncio
    async def test_community_manager_agent(self):
        """Test community manager agent functionality"""
        
        agent = CommunityManagerAgent()
        
        # Test engagement analysis
        sample_mentions = [
            {
                "id": "mention_1",
                "platform": "linkedin",
                "message": "Great insights on marketing automation! How do I get started?",
                "user": "john_doe",
                "timestamp": datetime.now().isoformat(),
                "sentiment": "positive"
            },
            {
                "id": "mention_2", 
                "platform": "twitter",
                "message": "Having trouble with your platform, need help urgently",
                "user": "frustrated_user",
                "timestamp": datetime.now().isoformat(),
                "sentiment": "negative"
            }
        ]
        
        task_config = {
            "type": "engagement_analysis",
            "platform": ContentPlatform.LINKEDIN,
            "mentions_data": sample_mentions,
            "time_period": "24h"
        }
        
        result = await agent.execute_task(task_config)
        
        assert result["status"] == "success"
        assert "engagement_analysis" in result["result"]
        assert "response_priorities" in result["result"]
        assert len(result["result"]["response_priorities"]) > 0
        
    @pytest.mark.asyncio
    async def test_performance_analyst_agent(self):
        """Test performance analyst agent functionality"""
        
        agent = PerformanceAnalystAgent()
        
        # Test performance analysis
        task_config = {
            "type": "performance_analysis",
            "performance_data": {
                "linkedin": {
                    "posts": 15,
                    "total_engagement": 1250,
                    "reach": 25000,
                    "clicks": 320
                },
                "twitter": {
                    "posts": 30,
                    "total_engagement": 800,
                    "reach": 15000,
                    "clicks": 180
                }
            },
            "time_period": "30d",
            "content_types": ["blog_post", "social_media_post"]
        }
        
        result = await agent.execute_task(task_config)
        
        assert result["status"] == "success"
        assert "performance_analysis" in result["result"]
        assert "benchmark_comparison" in result["result"]
        assert "predictive_insights" in result["result"]

class TestContentMarketingOrchestrator:
    """Test content marketing workflow orchestrator"""
    
    @pytest.mark.asyncio
    async def test_strategy_workflow_execution(self, sample_brand_guidelines, sample_target_audience):
        """Test content strategy development workflow"""
        
        orchestrator = BizoholicContentMarketingOrchestrator()
        
        workflow_config = ContentWorkflowConfig(
            workflow_type=ContentWorkflowType.CONTENT_STRATEGY_DEVELOPMENT,
            brand_guidelines=sample_brand_guidelines,
            target_audience=sample_target_audience,
            content_pillars=["thought_leadership", "product_education", "industry_insights"],
            platforms=[ContentPlatform.LINKEDIN, ContentPlatform.TWITTER],
            hitl_level=HITLContentApprovalLevel.MEDIUM,
            conservative_estimation=True
        )
        
        result = await orchestrator.execute_content_workflow(workflow_config, TEST_TENANT_ID)
        
        assert result["status"] == "completed"
        assert result["workflow_id"] is not None
        assert "result" in result
        assert result["result"]["workflow_type"] == "content_strategy_development"
        
    @pytest.mark.asyncio
    async def test_blog_creation_workflow(self, sample_brand_guidelines, sample_target_audience):
        """Test blog content creation workflow"""
        
        orchestrator = BizoholicContentMarketingOrchestrator()
        
        workflow_config = ContentWorkflowConfig(
            workflow_type=ContentWorkflowType.CONTENT_CREATION_BLOG,
            brand_guidelines=sample_brand_guidelines,
            target_audience=sample_target_audience,
            platforms=[ContentPlatform.WEBSITE_BLOG, ContentPlatform.LINKEDIN],
            custom_parameters={
                "topic": "The Future of AI in Marketing Automation",
                "keywords": ["AI marketing", "automation", "future trends"],
                "word_count": 2000
            }
        )
        
        result = await orchestrator.execute_content_workflow(workflow_config, TEST_TENANT_ID)
        
        assert result["status"] == "completed"
        assert "content_result" in result["result"]
        assert result["result"]["content_result"]["content_type"] == ContentType.BLOG_POST
        
    @pytest.mark.asyncio
    async def test_workflow_status_tracking(self):
        """Test workflow status and progress tracking"""
        
        orchestrator = BizoholicContentMarketingOrchestrator()
        
        # Test getting status of non-existent workflow
        status = await orchestrator.get_workflow_status("non-existent-id")
        assert status is None
        
        # Test performance dashboard
        dashboard = await orchestrator.get_performance_dashboard()
        assert "active_workflows" in dashboard
        assert "completed_workflows" in dashboard
        assert "system_health" in dashboard

class TestHITLApprovalWorkflows:
    """Test Human-in-the-Loop approval workflows"""
    
    @pytest.mark.asyncio
    async def test_approval_workflow_initiation(self, sample_brand_guidelines):
        """Test HITL approval workflow initiation"""
        
        hitl_workflows = ContentMarketingHITLWorkflows()
        
        context = ApprovalContext(
            tenant_id=TEST_TENANT_ID,
            content_id=TEST_CONTENT_ID,
            approval_type=HITLApprovalType.CONTENT_STRATEGY,
            automation_level=AutomationLevel.LEVEL_2_ASSISTED,
            priority=ApprovalPriority.MEDIUM,
            requester_id="test_user",
            business_impact="medium"
        )
        
        content_data = {
            "title": "AI Marketing Strategy Guide",
            "content": "A comprehensive guide to implementing AI in marketing...",
            "brand_compliance_score": 0.88,
            "quality_score": 0.85,
            "ai_confidence": 0.80
        }
        
        criteria = ApprovalCriteria(
            brand_compliance_threshold=0.85,
            quality_score_threshold=0.8,
            ai_confidence_threshold=0.75
        )
        
        approval_id = await hitl_workflows.initiate_approval_workflow(
            context, content_data, criteria
        )
        
        assert approval_id is not None
        assert approval_id in hitl_workflows.approval_queue
        
        # Test approval status
        status = await hitl_workflows.get_approval_status(approval_id)
        assert status["approval_id"] == approval_id
        assert "progress" in status
        assert "timeline" in status
        
    @pytest.mark.asyncio
    async def test_approval_decision_processing(self):
        """Test processing of approval decisions"""
        
        hitl_workflows = ContentMarketingHITLWorkflows()
        
        # Create a mock approval workflow
        approval_id = str(uuid.uuid4())
        workflow = {
            "approval_id": approval_id,
            "context": {"tenant_id": TEST_TENANT_ID},
            "status": "pending_review",
            "decisions": [],
            "timeline": [],
            "approval_path": {"required_approvers": ["reviewer_1", "reviewer_2"]}
        }
        
        hitl_workflows.approval_queue[approval_id] = workflow
        
        # Process first approval decision
        result1 = await hitl_workflows.process_approval_decision(
            approval_id,
            "reviewer_1",
            ApprovalDecision.APPROVED,
            "Looks good to proceed"
        )
        
        assert result1["decision_recorded"] is True
        assert result1["completion_status"] == "pending"
        
        # Process second approval decision
        result2 = await hitl_workflows.process_approval_decision(
            approval_id,
            "reviewer_2", 
            ApprovalDecision.APPROVED,
            "Approved with minor suggestions"
        )
        
        assert result2["completion_status"] == "completed"
        assert result2["final_decision"] == "approved"
        
    @pytest.mark.asyncio
    async def test_approval_dashboard(self):
        """Test approval dashboard functionality"""
        
        hitl_workflows = ContentMarketingHITLWorkflows()
        
        dashboard = await hitl_workflows.get_approval_dashboard(TEST_TENANT_ID)
        
        assert "total_approvals" in dashboard
        assert "pending_approvals" in dashboard
        assert "auto_approval_rate" in dashboard
        assert "approval_queue" in dashboard

class TestConservativeEstimation:
    """Test conservative estimation framework"""
    
    @pytest.mark.asyncio
    async def test_content_performance_estimation(self, sample_brand_guidelines, sample_target_audience):
        """Test content performance estimation"""
        
        estimation_engine = ContentMarketingConservativeEstimation()
        
        context = EstimationContext(
            tenant_id=TEST_TENANT_ID,
            content_type="blog_post",
            platforms=["linkedin", "twitter"],
            industry="technology",
            company_size="medium",
            historical_data_available=False,
            risk_tolerance=RiskProfile.CONSERVATIVE,
            confidence_level=ConfidenceLevel.CONSERVATIVE_95,
            time_horizon=90
        )
        
        content_data = {
            "topic": "AI Marketing Automation",
            "word_count": 1500,
            "ai_confidence": 0.85,
            "seo_optimization": {"score": 0.78},
            "brand_compliance_score": 0.88,
            "visual_assets": ["infographic", "chart"]
        }
        
        projection = await estimation_engine.estimate_content_performance(
            context, content_data
        )
        
        assert projection.metric_name == "content_performance"
        assert projection.projected_improvement.estimation_type == EstimationType.PERFORMANCE_METRICS
        assert projection.projected_improvement.conservative_estimate > 0
        assert projection.projected_improvement.confidence_level > 0.8
        assert projection.success_probability > 0.5
        
    @pytest.mark.asyncio
    async def test_over_delivery_tracking(self):
        """Test over-delivery tracking functionality"""
        
        estimation_engine = ContentMarketingConservativeEstimation()
        
        # Create a mock estimation
        estimation_id = str(uuid.uuid4())
        estimation_record = {
            "estimation_id": estimation_id,
            "tenant_id": TEST_TENANT_ID,
            "projection": {
                "conservative_estimate": 0.05,  # 5% engagement rate
                "timeline_estimate": 30,         # 30 days
                "roi_estimate": 2.5              # 250% ROI
            }
        }
        
        estimation_engine.estimation_history[estimation_id] = estimation_record
        
        # Track actual performance
        actual_performance = {
            "performance": 0.07,    # 7% actual engagement (over-delivery)
            "actual_timeline": 25,  # Completed 5 days early
            "roi": 3.2,            # 320% actual ROI
            "success": True
        }
        
        over_delivery = await estimation_engine.track_over_delivery(
            estimation_id, actual_performance
        )
        
        assert over_delivery["performance_over_delivery"] > 0  # Over-delivered
        assert over_delivery["timeline_over_delivery"] > 0     # Finished early
        assert over_delivery["roi_over_delivery"] > 0          # Better ROI
        assert over_delivery["achieved_success"] is True
        
    @pytest.mark.asyncio
    async def test_estimation_dashboard(self):
        """Test estimation dashboard functionality"""
        
        estimation_engine = ContentMarketingConservativeEstimation()
        
        dashboard = await estimation_engine.get_estimation_dashboard(TEST_TENANT_ID)
        
        assert "total_estimations" in dashboard
        assert "average_over_delivery" in dashboard
        assert "calibration_accuracy" in dashboard
        assert "success_rate" in dashboard

class TestPlatformIntegrations:
    """Test social media platform integrations"""
    
    def setup_mock_credentials(self, platform: ContentPlatform):
        """Setup mock credentials for testing"""
        return PlatformCredentials(
            platform=platform,
            tenant_id=TEST_TENANT_ID,
            access_token="mock_access_token",
            client_id="mock_client_id",
            account_id="mock_account_id"
        )
    
    @pytest.mark.asyncio
    async def test_linkedin_integration(self):
        """Test LinkedIn platform integration"""
        
        credentials = self.setup_mock_credentials(ContentPlatform.LINKEDIN)
        integration = LinkedInIntegration(credentials)
        
        # Test authentication
        with patch.object(integration, 'authenticate', return_value=True):
            auth_result = await integration.authenticate()
            assert auth_result is True
        
        # Test content validation
        content_post = ContentPost(
            post_id=TEST_CONTENT_ID,
            platform=ContentPlatform.LINKEDIN,
            content_type=ContentType.SOCIAL_MEDIA_POST,
            content="Excited to share insights on AI marketing automation! 🚀 #AI #Marketing",
            hashtags=["AI", "Marketing", "Automation"]
        )
        
        validation = await integration.validate_content(content_post)
        assert validation["valid"] is True
        
        # Test content posting (mocked)
        with patch.object(integration, 'publish_content') as mock_publish:
            mock_publish.return_value = PostingResult(
                post_id=TEST_CONTENT_ID,
                platform=ContentPlatform.LINKEDIN,
                status=PostingStatus.PUBLISHED,
                platform_post_id="linkedin_post_123",
                published_time=datetime.now()
            )
            
            result = await integration.publish_content(content_post)
            assert result.status == PostingStatus.PUBLISHED
            assert result.platform_post_id == "linkedin_post_123"
    
    @pytest.mark.asyncio
    async def test_platform_manager(self):
        """Test platform manager functionality"""
        
        manager = ContentMarketingPlatformManager()
        
        # Test platform initialization
        credentials = self.setup_mock_credentials(ContentPlatform.LINKEDIN)
        
        with patch.object(LinkedInIntegration, 'authenticate', return_value=True):
            init_result = await manager.initialize_platform(ContentPlatform.LINKEDIN, credentials)
            assert init_result is True
        
        # Test multi-platform publishing
        content_post = ContentPost(
            post_id=TEST_CONTENT_ID,
            platform=ContentPlatform.LINKEDIN,
            content_type=ContentType.SOCIAL_MEDIA_POST,
            content="Test content for multi-platform publishing"
        )
        
        platforms = [ContentPlatform.LINKEDIN]
        
        with patch.object(manager, 'publish_to_platforms') as mock_publish:
            mock_publish.return_value = {
                ContentPlatform.LINKEDIN: PostingResult(
                    post_id=TEST_CONTENT_ID,
                    platform=ContentPlatform.LINKEDIN,
                    status=PostingStatus.PUBLISHED
                )
            }
            
            results = await manager.publish_to_platforms(content_post, platforms, TEST_TENANT_ID)
            assert ContentPlatform.LINKEDIN in results
            assert results[ContentPlatform.LINKEDIN].status == PostingStatus.PUBLISHED

class TestContentMarketingService:
    """Test FastAPI service layer"""
    
    @pytest.mark.asyncio
    async def test_content_workflow_execution(self, sample_brand_guidelines, sample_target_audience):
        """Test content workflow execution endpoint"""
        
        service = BizoholicContentMarketingService()
        
        request = ContentWorkflowRequest(
            workflow_type="content_strategy_development",
            brand_guidelines=sample_brand_guidelines,
            target_audience=sample_target_audience,
            content_pillars=["thought_leadership", "product_education"],
            platforms=["linkedin", "twitter"],
            hitl_level="medium",
            conservative_estimation=True
        )
        
        from fastapi import BackgroundTasks
        background_tasks = BackgroundTasks()
        
        with patch.object(service.orchestrator, 'execute_content_workflow') as mock_execute:
            mock_execute.return_value = {
                "workflow_id": TEST_WORKFLOW_ID,
                "status": "completed",
                "execution_time": 45.0,
                "result": {"workflow_type": "content_strategy_development"}
            }
            
            response = await service.execute_content_workflow(request, TEST_TENANT_ID, background_tasks)
            
            assert response.workflow_id == TEST_WORKFLOW_ID
            assert response.status == "completed"
            assert response.tenant_id == TEST_TENANT_ID
    
    @pytest.mark.asyncio
    async def test_content_creation(self, sample_brand_guidelines, sample_target_audience):
        """Test AI content creation endpoint"""
        
        service = BizoholicContentMarketingService()
        
        request = ContentCreationRequest(
            content_type="blog_post",
            topic="The Future of Marketing Automation",
            keywords=["marketing", "automation", "AI", "future"],
            platforms=["blog", "linkedin"],
            brand_voice=sample_brand_guidelines["brand_voice"],
            target_audience=sample_target_audience["primary_persona"],
            word_count=1500,
            include_seo=True
        )
        
        with patch.object(service.orchestrator, 'execute_content_workflow') as mock_execute:
            mock_execute.return_value = {
                "workflow_id": TEST_WORKFLOW_ID,
                "status": "completed",
                "result": {
                    "content_result": {
                        "content_data": {
                            "title": "The Future of Marketing Automation",
                            "content": "AI is transforming marketing...",
                            "seo_optimization": {"score": 0.85}
                        },
                        "quality_metrics": {"seo_score": 0.85, "brand_alignment": 0.88},
                        "performance_prediction": {"engagement_rate": 0.07},
                        "approval_required": False,
                        "brand_alignment": 0.88
                    }
                }
            }
            
            response = await service.create_content_piece(request, TEST_TENANT_ID)
            
            assert response.content_type == "blog_post"
            assert response.title == "The Future of Marketing Automation"
            assert response.brand_compliance_score > 0.8
    
    @pytest.mark.asyncio
    async def test_dashboard_functionality(self):
        """Test dashboard data retrieval"""
        
        service = BizoholicContentMarketingService()
        
        with patch.object(service.orchestrator, 'get_performance_dashboard') as mock_dashboard:
            mock_dashboard.return_value = {
                "active_workflows": 5,
                "completed_workflows": 25,
                "failed_workflows": 1,
                "workflow_performance": {"success_rate": 0.96},
                "hitl_queue_size": 3,
                "system_health": "optimal"
            }
            
            response = await service.get_content_marketing_dashboard(TEST_TENANT_ID)
            
            assert response.active_workflows == 5
            assert response.completed_workflows == 25
            assert response.system_health == "optimal"
            assert "content_creation_stats" in response.__dict__
            assert "community_engagement_stats" in response.__dict__

class TestDatabaseModels:
    """Test database models and operations"""
    
    def test_content_strategy_model(self):
        """Test ContentStrategy model creation"""
        from app.models.content_marketing_models import ContentStrategy
        
        strategy = ContentStrategy(
            tenant_id=TEST_TENANT_ID,
            strategy_name="Q4 Content Strategy",
            brand_voice={"tone": "professional", "style": "conversational"},
            target_audience={"primary": "marketing_managers"},
            content_pillars=["thought_leadership", "product_education"],
            content_goals={"awareness": "increase_by_25_percent"},
            kpi_definitions={"engagement_rate": "target_5_percent"},
            success_metrics={"monthly_leads": 100},
            editorial_calendar_framework={"frequency": "weekly"},
            content_format_strategy={"blog": "weekly", "social": "daily"},
            seo_integration_config={"keyword_density": 0.02},
            automation_level=AutomationLevel.LEVEL_2_ASSISTED,
            hitl_approval_rules={"high_impact": "requires_approval"},
            created_by="test_user"
        )
        
        assert strategy.tenant_id == TEST_TENANT_ID
        assert strategy.strategy_name == "Q4 Content Strategy"
        assert strategy.automation_level == AutomationLevel.LEVEL_2_ASSISTED
        assert strategy.is_active is True
    
    def test_content_piece_model(self):
        """Test ContentPiece model creation"""
        from app.models.content_marketing_models import ContentPiece
        
        content_piece = ContentPiece(
            tenant_id=TEST_TENANT_ID,
            strategy_id=uuid.uuid4(),
            title="AI Marketing Guide",
            content_type=ContentType.BLOG_POST,
            platforms=["blog", "linkedin"],
            status=ContentStatus.DRAFT,
            content_data={
                "title": "Complete Guide to AI Marketing",
                "content": "Artificial intelligence is revolutionizing...",
                "meta_description": "Learn how AI can transform your marketing",
                "word_count": 1500
            },
            seo_optimization={
                "primary_keyword": "AI marketing",
                "secondary_keywords": ["automation", "machine learning"],
                "keyword_density": 0.02
            },
            ai_generated=True,
            generation_prompt="Create a comprehensive guide about AI in marketing",
            ai_model_used="gpt-4",
            scheduled_publish_time=datetime.now() + timedelta(hours=24),
            distribution_config={
                "blog": {"featured": True},
                "linkedin": {"post_time": "09:00"}
            },
            created_by="test_user"
        )
        
        assert content_piece.tenant_id == TEST_TENANT_ID
        assert content_piece.content_type == ContentType.BLOG_POST
        assert content_piece.ai_generated is True
        assert "AI marketing" in content_piece.seo_optimization["primary_keyword"]

class TestAPIEndpoints:
    """Test API endpoints integration"""
    
    @pytest.mark.asyncio
    async def test_workflow_endpoints(self):
        """Test workflow-related API endpoints"""
        
        # This would require setting up a test client
        # For now, testing the endpoint functions directly
        
        from bizoholic_content_marketing_service import (
            execute_content_workflow_endpoint,
            get_content_workflow_status_endpoint
        )
        
        # Test workflow execution endpoint
        request = ContentWorkflowRequest(
            workflow_type="content_strategy_development",
            brand_guidelines={"brand_voice": {"tone": "professional"}},
            target_audience={"primary_persona": "marketing_manager"},
            platforms=["linkedin"]
        )
        
        from fastapi import BackgroundTasks
        background_tasks = BackgroundTasks()
        
        with patch('bizoholic_content_marketing_service.content_marketing_service') as mock_service:
            mock_service.execute_content_workflow.return_value = MagicMock(
                workflow_id=TEST_WORKFLOW_ID,
                status="completed",
                tenant_id=TEST_TENANT_ID
            )
            
            # Would normally test with actual endpoint, but testing service call
            result = await mock_service.execute_content_workflow(request, TEST_TENANT_ID, background_tasks)
            assert result.workflow_id == TEST_WORKFLOW_ID
    
    @pytest.mark.asyncio
    async def test_content_creation_endpoints(self):
        """Test content creation API endpoints"""
        
        from bizoholic_content_marketing_service import create_content_piece_endpoint
        
        request = ContentCreationRequest(
            content_type="blog_post",
            topic="Marketing Automation Best Practices",
            platforms=["blog", "linkedin"],
            brand_voice={"tone": "professional"},
            target_audience={"persona": "marketing_manager"}
        )
        
        with patch('bizoholic_content_marketing_service.content_marketing_service') as mock_service:
            mock_response = MagicMock()
            mock_response.content_id = TEST_CONTENT_ID
            mock_response.content_type = "blog_post"
            mock_response.title = "Marketing Automation Best Practices"
            
            mock_service.create_content_piece.return_value = mock_response
            
            result = await mock_service.create_content_piece(request, TEST_TENANT_ID)
            assert result.content_id == TEST_CONTENT_ID

@pytest.mark.asyncio
async def test_integration_workflow():
    """Integration test for complete content marketing workflow"""
    
    # This test simulates a complete workflow from strategy to content creation
    
    # 1. Initialize orchestrator
    orchestrator = BizoholicContentMarketingOrchestrator()
    
    # 2. Create workflow configuration
    workflow_config = ContentWorkflowConfig(
        workflow_type=ContentWorkflowType.CONTENT_STRATEGY_DEVELOPMENT,
        brand_guidelines={
            "brand_voice": {"tone": "professional", "style": "conversational"},
            "visual_identity": {"primary_color": "#1E3A8A"}
        },
        target_audience={
            "primary_persona": {
                "role": "marketing_manager",
                "industry": "technology",
                "pain_points": ["time_constraints", "ROI_measurement"]
            }
        },
        content_pillars=["thought_leadership", "product_education"],
        platforms=[ContentPlatform.LINKEDIN, ContentPlatform.TWITTER],
        conservative_estimation=True
    )
    
    # 3. Execute workflow
    result = await orchestrator.execute_content_workflow(workflow_config, TEST_TENANT_ID)
    
    # 4. Verify results
    assert result["status"] == "completed"
    assert "result" in result
    assert result["result"]["workflow_type"] == "content_strategy_development"
    
    # 5. Test workflow status tracking
    workflow_id = result["workflow_id"]
    status = await orchestrator.get_workflow_status(workflow_id)
    
    assert status is not None
    assert status["workflow_id"] == workflow_id
    assert status["status"] == "completed"

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])