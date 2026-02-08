"""
Centralized AI Agents Module for BizOSaas Core
All 35+ AI agents unified into single business logic layer
"""

from .marketing_agents import (
    MarketingStrategistAgent,
    ContentCreatorAgent,
    SEOSpecialistAgent,
    SocialMediaAgent,
    BrandPositioningAgent,
    CompetitiveAnalysisAgent,
    # LegacyMarketResearchAgent as MarketResearchAgent, 
)

from .business_intelligence_agents import (
    MarketResearchAgent as RefinedMarketResearchAgent,
    DataAnalyticsAgent as RefinedDataAnalyticsAgent,
    StrategicPlanningAgent as RefinedStrategicPlanningAgent,
    CompetitiveIntelligenceAgent as RefinedCompetitiveIntelligenceAgent
)

from .content_creative_agents import (
    ContentGenerationAgent as RefinedContentGenerationAgent,
    CreativeDesignAgent as RefinedCreativeDesignAgent,
    SEOOptimizationAgent as RefinedSEOOptimizationAgent,
    VideoMarketingAgent as RefinedVideoMarketingAgent
)

from .marketing_growth_agents import (
    CampaignOrchestrationAgent as RefinedCampaignOrchestrationAgent,
    ConversionOptimizationAgent as RefinedConversionOptimizationAgent,
    SocialMediaManagementAgent as RefinedSocialMediaManagementAgent
)

from .technical_agents import (
    CodeGenerationAgent as RefinedCodeGenerationAgent,
    DevOpsAutomationAgent as RefinedDevOpsAutomationAgent,
    TechnicalDocumentationAgent as RefinedTechnicalDocumentationAgent
)

from .customer_crm_agents import (
    CustomerEngagementAgent as RefinedCustomerEngagementAgent,
    SalesIntelligenceAgent as RefinedSalesIntelligenceAgent
)

from .quanttrade_agents import (
    TradingStrategyAgent as RefinedTradingStrategyAgent,
    FinancialAnalyticsAgent as RefinedFinancialAnalyticsAgent
)

from .thrillring_agents import (
    GamingExperienceAgent as RefinedGamingExperienceAgent,
    CommunityManagementAgent as RefinedCommunityManagementAgent
)

from .master_orchestrator import (
    MasterOrchestratorAgent as RefinedMasterOrchestratorAgent
)

from .refined_ecommerce_agents import (
    RefinedProductSourcingAgent,
    RefinedInventoryManagementAgent,
    RefinedOrderOrchestrationAgent
)

from .quality_assurance_agent import (
    RefinedQualityAssuranceAgent
)

from .ecommerce_agents import (
    ProductSourcingAgent,
    EcommerceAgent,
    PriceOptimizationAgent,
    InventoryManagementAgent,
    SupplierRelationsAgent,
    FraudDetectionAgent,
    CustomerSegmentationAgent,
    SalesForecastingAgent,
    ASOAgent,
    AmazonOptimizationAgent,
    EcommercePlatformIntegrationAgent,
    ReviewManagementAgent,
    ConversionRateOptimizationAgent
)

from .analytics_agents import (
    DigitalPresenceAuditAgent,
    PerformanceAnalyticsAgent,
    ReportGeneratorAgent,
    DataVisualizationAgent,
    ROIAnalysisAgent,
    TrendAnalysisAgent,
    InsightSynthesisAgent,
    PredictiveAnalyticsAgent
)

from .operations_agents import (
    CustomerSupportAgent,
    ComplianceAuditAgent,
    WorkflowOptimizationAgent,
    ResourcePlanningAgent,
    QualityAssuranceAgent,
    IncidentManagementAgent,
    KnowledgeManagementAgent,
    ProcessAutomationAgent
)

from .workflow_crews import (
    DigitalAuditCrew,
    CampaignLaunchCrew,
    ProductLaunchCrew,
    CompetitorAnalysisCrew,
    MarketResearchCrew,
    ContentStrategyCrew,
    ReputationManagementCrew,
    LeadQualificationCrew
)

from .orchestration import (
    HierarchicalCrewOrchestrator,
    WorkflowEngine
)

# Import Advanced CRM Agents
from .crm_agents import (
    ContactIntelligenceAgent,
    LeadScoringAgent, 
    SalesAssistantAgent,
    SentimentAnalysisAgent,
    EscalationPredictorAgent,
    PersonalizationAgent,
    PipelineManagementAgent
)

from .workflow_templates import (
    ContentCreationWorkflow,
    MarketingCampaignWorkflow,
    CompetitiveAnalysisWorkflow,
    DevelopmentSprintWorkflow,
    TradingStrategyWorkflow,
    GamingEventWorkflow,
    ECommerceSourcingWorkflow,
    ECommerceOperationsWorkflow,
    ECommerceInventoryLogisticsWorkflow,
    FullDigitalMarketing360Workflow,
    VideoContentMachineWorkflow,
    SEMAdCampaignWorkflow,
    OnboardingStrategyWorkflow
)

__all__ = [
    # Marketing Agents
    "MarketingStrategistAgent",
    "ContentCreatorAgent", 
    "SEOSpecialistAgent",
    "SocialMediaAgent",
    "BrandPositioningAgent",
    "CompetitiveAnalysisAgent",
    "MarketResearchAgent",
    "GEOAgent",
    "InfluencerMarketingAgent",
    
    # E-commerce Agents
    "ProductSourcingAgent",
    "EcommerceAgent",
    "PriceOptimizationAgent",
    "InventoryManagementAgent",
    "SupplierRelationsAgent",
    "FraudDetectionAgent",
    "CustomerSegmentationAgent",
    "SalesForecastingAgent",
    "ASOAgent",
    "AmazonOptimizationAgent",
    "EcommercePlatformIntegrationAgent",
    "ReviewManagementAgent",
    "ConversionRateOptimizationAgent",
    
    # Analytics Agents
    "DigitalPresenceAuditAgent",
    "PerformanceAnalyticsAgent",
    "ReportGeneratorAgent",
    "DataVisualizationAgent",
    "ROIAnalysisAgent",
    "TrendAnalysisAgent",
    "InsightSynthesisAgent",
    "PredictiveAnalyticsAgent",
    
    # Operations Agents
    "CustomerSupportAgent",
    "ComplianceAuditAgent",
    "WorkflowOptimizationAgent",
    "ResourcePlanningAgent",
    "QualityAssuranceAgent",
    "IncidentManagementAgent",
    "KnowledgeManagementAgent",
    "ProcessAutomationAgent",
    
    # Workflow Crews
    "DigitalAuditCrew",
    "CampaignLaunchCrew",
    "ProductLaunchCrew",
    "CompetitorAnalysisCrew",
    "MarketResearchCrew",
    "ContentStrategyCrew",
    "ReputationManagementCrew",
    "LeadQualificationCrew",
    
    # Orchestration
    "HierarchicalCrewOrchestrator",
    "WorkflowEngine",
    
    # Advanced CRM Agents
    "ContactIntelligenceAgent",
    "LeadScoringAgent", 
    "SalesAssistantAgent",
    "SentimentAnalysisAgent",
    "EscalationPredictorAgent",
    "PersonalizationAgent",
    "PipelineManagementAgent",
    
    # Refined AI Ecosystem - Category 1
    "RefinedMarketResearchAgent",
    "RefinedDataAnalyticsAgent",
    "RefinedStrategicPlanningAgent",
    "RefinedCompetitiveIntelligenceAgent",

    # Refined AI Ecosystem - Category 2
    "RefinedContentGenerationAgent",
    "RefinedCreativeDesignAgent",
    "RefinedSEOOptimizationAgent",
    "RefinedVideoMarketingAgent",

    # Refined AI Ecosystem - Category 3
    "RefinedCampaignOrchestrationAgent",
    "RefinedConversionOptimizationAgent",
    "RefinedSocialMediaManagementAgent",

    # Refined AI Ecosystem - Category 4
    "RefinedCodeGenerationAgent",
    "RefinedDevOpsAutomationAgent",
    "RefinedTechnicalDocumentationAgent",

    # Refined AI Ecosystem - Category 5
    "RefinedCustomerEngagementAgent",
    "RefinedSalesIntelligenceAgent",

    # Refined AI Ecosystem - Category 6
    "RefinedTradingStrategyAgent",
    "RefinedFinancialAnalyticsAgent",

    # Refined AI Ecosystem - Category 7
    "RefinedGamingExperienceAgent",
    "RefinedCommunityManagementAgent",

    # Refined AI Ecosystem - Category 8 (Master)
    "RefinedMasterOrchestratorAgent",
    
    # Refined AI Ecosystem - Category 9 (E-commerce)
    "RefinedProductSourcingAgent",
    "RefinedInventoryManagementAgent",
    "RefinedOrderOrchestrationAgent",

    # Refined AI Ecosystem - Category 10 (QA)
    "RefinedQualityAssuranceAgent",
    
    # Refined Workflows
    "ContentCreationWorkflow",
    "MarketingCampaignWorkflow",
    "CompetitiveAnalysisWorkflow",
    "DevelopmentSprintWorkflow",
    "TradingStrategyWorkflow",
    "GamingEventWorkflow",
    "ECommerceSourcingWorkflow",
    "ECommerceOperationsWorkflow",
    "ECommerceInventoryLogisticsWorkflow",
    "FullDigitalMarketing360Workflow",
    "VideoContentMachineWorkflow",
    "SEMAdCampaignWorkflow"
]