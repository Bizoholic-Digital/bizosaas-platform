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
    MarketResearchAgent,
    GEOAgent,
    InfluencerMarketingAgent
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
    LeadQualificationAgent,
    ClientOnboardingAgent,
    ProjectCoordinationAgent,
    CommunicationManagementAgent,
    QualityAssuranceAgent,
    SupportAutomationAgent,
    WorkflowOptimizationAgent,
    PartnerPerformanceMonitoringAgent
)

from .workflow_crews import (
    OnboardingCrew,
    CampaignStrategyCrew,
    CampaignExecutionCrew,
    ContentApprovalCrew,
    DataOptimizationCrew,
    ConservativeEstimationCrew,
    UserJourneyOptimizationCrew,
    SelfMarketingCrew,
    ClassificationCrew,
    KeywordResearchCrew
)

from .orchestration import (
    HierarchicalCrewOrchestrator,
    WorkflowEngine,
    AgentCoordinator
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
    "LeadQualificationAgent",
    "ClientOnboardingAgent",
    "ProjectCoordinationAgent",
    "CommunicationManagementAgent",
    "QualityAssuranceAgent",
    "SupportAutomationAgent",
    "WorkflowOptimizationAgent",
    "PartnerPerformanceMonitoringAgent",
    
    # Workflow Crews
    "OnboardingCrew",
    "CampaignStrategyCrew",
    "CampaignExecutionCrew",
    "ContentApprovalCrew",
    "DataOptimizationCrew",
    "ConservativeEstimationCrew",
    "UserJourneyOptimizationCrew",
    "SelfMarketingCrew",
    "ClassificationCrew",
    "KeywordResearchCrew",
    
    # Orchestration
    "HierarchicalCrewOrchestrator",
    "WorkflowEngine",
    "AgentCoordinator",
    
    # Advanced CRM Agents
    "ContactIntelligenceAgent",
    "LeadScoringAgent", 
    "SalesAssistantAgent",
    "SentimentAnalysisAgent",
    "EscalationPredictorAgent",
    "PersonalizationAgent",
    "PipelineManagementAgent"
]