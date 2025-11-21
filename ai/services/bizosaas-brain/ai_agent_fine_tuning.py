"""
AI Agent Fine-Tuning Interface for Tenant-Specific Customization

This module provides comprehensive fine-tuning capabilities for AI agents on a per-tenant basis,
allowing tenants to customize agent behavior, prompts, parameters, and execution patterns
to match their specific business needs and preferences.

Features:
- Tenant-specific agent configuration
- Custom prompt templates
- Behavior modification parameters
- Performance tuning settings
- Agent personality customization
- Industry-specific adaptations
"""

from typing import Dict, List, Optional, Any, Union
from enum import Enum
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from pydantic import BaseModel, Field
import asyncio
import json
import uuid

# Import AI agents and tenant management
from ai_agents_management import (
    AgentCategory, AgentPriority, AgentStatus,
    get_available_agents_by_category, get_agent_by_id
)
from tenant_middleware import get_current_tenant, TenantContext


class FineTuningParameterType(str, Enum):
    """Types of fine-tuning parameters"""
    PROMPT_TEMPLATE = "prompt_template"
    SYSTEM_MESSAGE = "system_message"
    TEMPERATURE = "temperature"
    MAX_TOKENS = "max_tokens"
    FREQUENCY_PENALTY = "frequency_penalty"
    PRESENCE_PENALTY = "presence_penalty"
    STOP_SEQUENCES = "stop_sequences"
    CUSTOM_INSTRUCTIONS = "custom_instructions"
    INDUSTRY_CONTEXT = "industry_context"
    BRAND_VOICE = "brand_voice"
    COMMUNICATION_STYLE = "communication_style"
    OUTPUT_FORMAT = "output_format"
    EXECUTION_PRIORITY = "execution_priority"
    RETRY_LOGIC = "retry_logic"
    TIMEOUT_SETTINGS = "timeout_settings"


class IndustryType(str, Enum):
    """Industry types for context-specific tuning"""
    MARKETING_AGENCY = "marketing_agency"
    ECOMMERCE = "ecommerce"
    ENTERTAINMENT = "entertainment"
    TRADING_FINANCE = "trading_finance"
    HEALTHCARE = "healthcare"
    TECHNOLOGY = "technology"
    EDUCATION = "education"
    REAL_ESTATE = "real_estate"
    MANUFACTURING = "manufacturing"
    RETAIL = "retail"
    CONSULTING = "consulting"
    GENERAL = "general"


class CommunicationStyle(str, Enum):
    """Communication styles for agent personality"""
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    TECHNICAL = "technical"
    CREATIVE = "creative"
    ANALYTICAL = "analytical"
    EMPATHETIC = "empathetic"
    AUTHORITATIVE = "authoritative"
    COLLABORATIVE = "collaborative"
    CONSULTATIVE = "consultative"
    DIRECT = "direct"


@dataclass
class FineTuningParameter:
    """Individual fine-tuning parameter configuration"""
    parameter_type: FineTuningParameterType
    parameter_name: str
    parameter_value: Any
    parameter_description: str
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class AgentFineTuningConfig:
    """Complete fine-tuning configuration for an AI agent"""
    tenant_id: str
    agent_id: str
    agent_name: str
    agent_category: AgentCategory
    config_name: str
    config_description: str
    parameters: List[FineTuningParameter]
    industry_context: IndustryType = IndustryType.GENERAL
    communication_style: CommunicationStyle = CommunicationStyle.PROFESSIONAL
    is_active: bool = True
    version: str = "1.0.0"
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    created_by: str = "system"


class FineTuningTemplate(BaseModel):
    """Pydantic model for fine-tuning template"""
    template_name: str = Field(..., description="Name of the fine-tuning template")
    template_description: str = Field(..., description="Description of the template")
    industry_type: IndustryType = Field(..., description="Target industry for this template")
    communication_style: CommunicationStyle = Field(..., description="Communication style")
    parameters: Dict[str, Any] = Field(..., description="Template parameters")
    tags: List[str] = Field(default_factory=list, description="Template tags")


class FineTuningRequest(BaseModel):
    """Pydantic model for fine-tuning requests"""
    agent_id: str = Field(..., description="ID of the agent to fine-tune")
    config_name: str = Field(..., description="Name for this configuration")
    config_description: str = Field(..., description="Description of the configuration")
    parameters: Dict[str, Any] = Field(..., description="Fine-tuning parameters")
    industry_context: Optional[IndustryType] = Field(None, description="Industry context")
    communication_style: Optional[CommunicationStyle] = Field(None, description="Communication style")


class AIAgentFineTuner:
    """
    Comprehensive AI Agent Fine-Tuning System
    
    Provides tenant-specific customization capabilities for AI agents including
    prompt engineering, behavior modification, and performance optimization.
    """
    
    def __init__(self, vault_client=None, redis_client=None):
        self.vault_client = vault_client
        self.redis_client = redis_client
        
        # Industry-specific templates
        self.industry_templates = {
            IndustryType.MARKETING_AGENCY: {
                "system_message": "You are an expert marketing strategist focused on delivering measurable results for clients. Always consider ROI, target audience demographics, and campaign performance metrics.",
                "brand_voice": "Professional yet creative, data-driven with strategic insights",
                "custom_instructions": "Always include specific metrics, actionable recommendations, and timeline considerations in your responses.",
                "communication_style": CommunicationStyle.CONSULTATIVE
            },
            IndustryType.ECOMMERCE: {
                "system_message": "You are an e-commerce optimization specialist focused on increasing conversions, reducing cart abandonment, and improving customer experience.",
                "brand_voice": "Results-oriented, customer-centric, and conversion-focused",
                "custom_instructions": "Always consider conversion rates, customer lifetime value, inventory management, and seasonal trends.",
                "communication_style": CommunicationStyle.ANALYTICAL
            },
            IndustryType.ENTERTAINMENT: {
                "system_message": "You are a creative entertainment industry expert focused on audience engagement, content virality, and platform-specific optimization.",
                "brand_voice": "Creative, trendy, audience-aware, and engagement-focused",
                "custom_instructions": "Always consider audience demographics, platform algorithms, trending topics, and engagement metrics.",
                "communication_style": CommunicationStyle.CREATIVE
            },
            IndustryType.TRADING_FINANCE: {
                "system_message": "You are a quantitative trading analyst focused on risk management, performance optimization, and algorithmic strategy development.",
                "brand_voice": "Analytical, risk-aware, data-driven, and performance-focused",
                "custom_instructions": "Always consider risk metrics, market volatility, portfolio diversification, and regulatory compliance.",
                "communication_style": CommunicationStyle.TECHNICAL
            }
        }
        
        # Communication style templates
        self.style_templates = {
            CommunicationStyle.PROFESSIONAL: {
                "tone": "formal and authoritative",
                "language": "business-appropriate with industry terminology",
                "structure": "organized with clear headers and bullet points"
            },
            CommunicationStyle.CASUAL: {
                "tone": "friendly and approachable",
                "language": "conversational with minimal jargon",
                "structure": "flexible with natural flow"
            },
            CommunicationStyle.TECHNICAL: {
                "tone": "precise and detailed",
                "language": "technical with specific terminology",
                "structure": "systematic with detailed explanations"
            },
            CommunicationStyle.CREATIVE: {
                "tone": "inspiring and innovative",
                "language": "engaging with creative metaphors",
                "structure": "dynamic with storytelling elements"
            },
            CommunicationStyle.ANALYTICAL: {
                "tone": "objective and data-focused",
                "language": "metrics-driven with quantitative insights",
                "structure": "logical with clear reasoning chains"
            }
        }
    
    async def create_fine_tuning_config(
        self, 
        tenant_id: str, 
        fine_tuning_request: FineTuningRequest
    ) -> AgentFineTuningConfig:
        """Create a new fine-tuning configuration for a tenant's agent"""
        try:
            # Get base agent configuration
            base_agent = await get_agent_by_id(fine_tuning_request.agent_id)
            if not base_agent:
                raise ValueError(f"Agent {fine_tuning_request.agent_id} not found")
            
            # Convert request parameters to FineTuningParameter objects
            parameters = []
            for param_name, param_value in fine_tuning_request.parameters.items():
                try:
                    param_type = FineTuningParameterType(param_name)
                except ValueError:
                    param_type = FineTuningParameterType.CUSTOM_INSTRUCTIONS
                
                parameters.append(FineTuningParameter(
                    parameter_type=param_type,
                    parameter_name=param_name,
                    parameter_value=param_value,
                    parameter_description=f"Custom {param_name} configuration for tenant {tenant_id}"
                ))
            
            # Apply industry and style templates if specified
            if fine_tuning_request.industry_context:
                industry_params = self._apply_industry_template(fine_tuning_request.industry_context)
                parameters.extend(industry_params)
            
            if fine_tuning_request.communication_style:
                style_params = self._apply_style_template(fine_tuning_request.communication_style)
                parameters.extend(style_params)
            
            # Create configuration
            config = AgentFineTuningConfig(
                tenant_id=tenant_id,
                agent_id=fine_tuning_request.agent_id,
                agent_name=base_agent["name"],
                agent_category=AgentCategory(base_agent["category"]),
                config_name=fine_tuning_request.config_name,
                config_description=fine_tuning_request.config_description,
                parameters=parameters,
                industry_context=fine_tuning_request.industry_context or IndustryType.GENERAL,
                communication_style=fine_tuning_request.communication_style or CommunicationStyle.PROFESSIONAL
            )
            
            # Store configuration
            await self._store_fine_tuning_config(config)
            
            return config
            
        except Exception as e:
            raise Exception(f"Failed to create fine-tuning configuration: {str(e)}")
    
    async def get_tenant_fine_tuning_configs(self, tenant_id: str) -> List[AgentFineTuningConfig]:
        """Get all fine-tuning configurations for a tenant"""
        try:
            # In a real implementation, this would fetch from the database
            # For now, return mock data
            configs = []
            
            # Mock configurations for different agents
            mock_configs = [
                {
                    "agent_id": "seo_content_strategist",
                    "config_name": "Bizoholic SEO Focus",
                    "config_description": "Optimized for marketing agency SEO content creation",
                    "parameters": {
                        "industry_context": "marketing_agency",
                        "communication_style": "consultative",
                        "focus_keywords": True,
                        "competitor_analysis": True
                    }
                },
                {
                    "agent_id": "product_sourcing_specialist",
                    "config_name": "Coreldove E-commerce Sourcing",
                    "config_description": "Configured for intelligent product sourcing and validation",
                    "parameters": {
                        "industry_context": "ecommerce",
                        "communication_style": "analytical",
                        "profit_margin_focus": 25.0,
                        "quality_threshold": 0.85
                    }
                }
            ]
            
            for mock_config in mock_configs:
                parameters = []
                for param_name, param_value in mock_config["parameters"].items():
                    parameters.append(FineTuningParameter(
                        parameter_type=FineTuningParameterType.CUSTOM_INSTRUCTIONS,
                        parameter_name=param_name,
                        parameter_value=param_value,
                        parameter_description=f"Configuration for {param_name}"
                    ))
                
                config = AgentFineTuningConfig(
                    tenant_id=tenant_id,
                    agent_id=mock_config["agent_id"],
                    agent_name=mock_config["agent_id"].replace("_", " ").title(),
                    agent_category=AgentCategory.SEO_CONTENT if "seo" in mock_config["agent_id"] else AgentCategory.ECOMMERCE,
                    config_name=mock_config["config_name"],
                    config_description=mock_config["config_description"],
                    parameters=parameters,
                    created_at=datetime.now() - timedelta(days=5)
                )
                configs.append(config)
            
            return configs
            
        except Exception as e:
            raise Exception(f"Failed to get tenant fine-tuning configurations: {str(e)}")
    
    async def update_fine_tuning_config(
        self, 
        tenant_id: str, 
        config_id: str, 
        updates: Dict[str, Any]
    ) -> AgentFineTuningConfig:
        """Update an existing fine-tuning configuration"""
        try:
            # Get existing configuration
            config = await self._get_fine_tuning_config(tenant_id, config_id)
            if not config:
                raise ValueError(f"Configuration {config_id} not found for tenant {tenant_id}")
            
            # Update parameters
            if "parameters" in updates:
                new_parameters = []
                for param_name, param_value in updates["parameters"].items():
                    new_parameters.append(FineTuningParameter(
                        parameter_type=FineTuningParameterType.CUSTOM_INSTRUCTIONS,
                        parameter_name=param_name,
                        parameter_value=param_value,
                        parameter_description=f"Updated {param_name} configuration"
                    ))
                config.parameters.extend(new_parameters)
            
            # Update other fields
            if "config_name" in updates:
                config.config_name = updates["config_name"]
            if "config_description" in updates:
                config.config_description = updates["config_description"]
            if "industry_context" in updates:
                config.industry_context = IndustryType(updates["industry_context"])
            if "communication_style" in updates:
                config.communication_style = CommunicationStyle(updates["communication_style"])
            
            config.updated_at = datetime.now()
            config.version = self._increment_version(config.version)
            
            # Store updated configuration
            await self._store_fine_tuning_config(config)
            
            return config
            
        except Exception as e:
            raise Exception(f"Failed to update fine-tuning configuration: {str(e)}")
    
    async def delete_fine_tuning_config(self, tenant_id: str, config_id: str) -> bool:
        """Delete a fine-tuning configuration"""
        try:
            # In a real implementation, this would delete from the database
            # For now, return success
            return True
            
        except Exception as e:
            raise Exception(f"Failed to delete fine-tuning configuration: {str(e)}")
    
    async def get_available_templates(self, industry_type: Optional[IndustryType] = None) -> List[FineTuningTemplate]:
        """Get available fine-tuning templates"""
        try:
            templates = []
            
            # Industry-specific templates
            industries_to_process = [industry_type] if industry_type else list(IndustryType)
            
            for industry in industries_to_process:
                if industry in self.industry_templates:
                    template_data = self.industry_templates[industry]
                    
                    template = FineTuningTemplate(
                        template_name=f"{industry.value.replace('_', ' ').title()} Template",
                        template_description=f"Pre-configured template optimized for {industry.value.replace('_', ' ')} industry",
                        industry_type=industry,
                        communication_style=template_data.get("communication_style", CommunicationStyle.PROFESSIONAL),
                        parameters=template_data,
                        tags=[industry.value, "industry_template", "pre_configured"]
                    )
                    templates.append(template)
            
            # Communication style templates
            for style in CommunicationStyle:
                style_data = self.style_templates.get(style, {})
                
                template = FineTuningTemplate(
                    template_name=f"{style.value.replace('_', ' ').title()} Style Template",
                    template_description=f"Communication style template for {style.value.replace('_', ' ')} approach",
                    industry_type=IndustryType.GENERAL,
                    communication_style=style,
                    parameters=style_data,
                    tags=[style.value, "style_template", "communication"]
                )
                templates.append(template)
            
            return templates
            
        except Exception as e:
            raise Exception(f"Failed to get available templates: {str(e)}")
    
    async def apply_fine_tuning_to_agent(
        self, 
        tenant_id: str, 
        agent_id: str, 
        config_id: str
    ) -> Dict[str, Any]:
        """Apply fine-tuning configuration to an agent for execution"""
        try:
            # Get fine-tuning configuration
            config = await self._get_fine_tuning_config(tenant_id, config_id)
            if not config:
                raise ValueError(f"Configuration {config_id} not found")
            
            # Get base agent configuration
            base_agent = await get_agent_by_id(agent_id)
            if not base_agent:
                raise ValueError(f"Agent {agent_id} not found")
            
            # Apply fine-tuning parameters to create customized agent config
            customized_config = base_agent.copy()
            
            for parameter in config.parameters:
                if parameter.is_active:
                    customized_config[parameter.parameter_name] = parameter.parameter_value
            
            # Add industry and style context
            customized_config["industry_context"] = config.industry_context.value
            customized_config["communication_style"] = config.communication_style.value
            customized_config["fine_tuning_version"] = config.version
            customized_config["tenant_customized"] = True
            
            return {
                "success": True,
                "customized_agent_config": customized_config,
                "applied_config": {
                    "config_name": config.config_name,
                    "config_version": config.version,
                    "parameters_applied": len([p for p in config.parameters if p.is_active]),
                    "industry_context": config.industry_context.value,
                    "communication_style": config.communication_style.value
                },
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            raise Exception(f"Failed to apply fine-tuning to agent: {str(e)}")
    
    async def get_fine_tuning_analytics(self, tenant_id: str) -> Dict[str, Any]:
        """Get analytics for fine-tuning configurations and performance"""
        try:
            configs = await self.get_tenant_fine_tuning_configs(tenant_id)
            
            # Calculate analytics
            total_configs = len(configs)
            active_configs = len([c for c in configs if c.is_active])
            
            # Categories breakdown
            category_breakdown = {}
            for config in configs:
                category = config.agent_category.value
                if category not in category_breakdown:
                    category_breakdown[category] = 0
                category_breakdown[category] += 1
            
            # Industry breakdown
            industry_breakdown = {}
            for config in configs:
                industry = config.industry_context.value
                if industry not in industry_breakdown:
                    industry_breakdown[industry] = 0
                industry_breakdown[industry] += 1
            
            # Style breakdown
            style_breakdown = {}
            for config in configs:
                style = config.communication_style.value
                if style not in style_breakdown:
                    style_breakdown[style] = 0
                style_breakdown[style] += 1
            
            return {
                "tenant_id": tenant_id,
                "summary": {
                    "total_configurations": total_configs,
                    "active_configurations": active_configs,
                    "inactive_configurations": total_configs - active_configs,
                    "customization_rate": round((active_configs / max(total_configs, 1)) * 100, 2)
                },
                "breakdowns": {
                    "by_category": category_breakdown,
                    "by_industry": industry_breakdown,
                    "by_communication_style": style_breakdown
                },
                "recommendations": self._generate_tuning_recommendations(configs),
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            raise Exception(f"Failed to get fine-tuning analytics: {str(e)}")
    
    def _apply_industry_template(self, industry: IndustryType) -> List[FineTuningParameter]:
        """Apply industry-specific template parameters"""
        parameters = []
        
        if industry in self.industry_templates:
            template = self.industry_templates[industry]
            
            for param_name, param_value in template.items():
                if param_name != "communication_style":
                    try:
                        param_type = FineTuningParameterType(param_name)
                    except ValueError:
                        param_type = FineTuningParameterType.CUSTOM_INSTRUCTIONS
                    
                    parameters.append(FineTuningParameter(
                        parameter_type=param_type,
                        parameter_name=param_name,
                        parameter_value=param_value,
                        parameter_description=f"Industry template parameter for {industry.value}"
                    ))
        
        return parameters
    
    def _apply_style_template(self, style: CommunicationStyle) -> List[FineTuningParameter]:
        """Apply communication style template parameters"""
        parameters = []
        
        if style in self.style_templates:
            template = self.style_templates[style]
            
            for param_name, param_value in template.items():
                parameters.append(FineTuningParameter(
                    parameter_type=FineTuningParameterType.COMMUNICATION_STYLE,
                    parameter_name=f"style_{param_name}",
                    parameter_value=param_value,
                    parameter_description=f"Communication style parameter for {style.value}"
                ))
        
        return parameters
    
    async def _store_fine_tuning_config(self, config: AgentFineTuningConfig):
        """Store fine-tuning configuration (mock implementation)"""
        # In a real implementation, this would store to database
        pass
    
    async def _get_fine_tuning_config(self, tenant_id: str, config_id: str) -> Optional[AgentFineTuningConfig]:
        """Get fine-tuning configuration by ID (mock implementation)"""
        # In a real implementation, this would fetch from database
        configs = await self.get_tenant_fine_tuning_configs(tenant_id)
        return configs[0] if configs else None
    
    def _increment_version(self, current_version: str) -> str:
        """Increment version number"""
        try:
            major, minor, patch = current_version.split(".")
            patch = str(int(patch) + 1)
            return f"{major}.{minor}.{patch}"
        except:
            return "1.0.1"
    
    def _generate_tuning_recommendations(self, configs: List[AgentFineTuningConfig]) -> List[str]:
        """Generate recommendations based on current configurations"""
        recommendations = []
        
        if not configs:
            recommendations.append("Consider creating fine-tuning configurations for your most used AI agents")
        
        if len(configs) < 3:
            recommendations.append("Expand your AI customization by fine-tuning more agents")
        
        # Check for industry alignment
        industries = set(config.industry_context for config in configs)
        if len(industries) == 1 and IndustryType.GENERAL in industries:
            recommendations.append("Consider setting industry-specific contexts for better performance")
        
        # Check for style diversity
        styles = set(config.communication_style for config in configs)
        if len(styles) == 1:
            recommendations.append("Try different communication styles for various use cases")
        
        return recommendations


# Global fine-tuner instance
ai_agent_fine_tuner = AIAgentFineTuner()

# API helper functions
async def create_agent_fine_tuning(tenant_id: str, request: FineTuningRequest) -> AgentFineTuningConfig:
    """Create new fine-tuning configuration"""
    return await ai_agent_fine_tuner.create_fine_tuning_config(tenant_id, request)

async def get_tenant_fine_tuning_configurations(tenant_id: str) -> List[AgentFineTuningConfig]:
    """Get all fine-tuning configurations for tenant"""
    return await ai_agent_fine_tuner.get_tenant_fine_tuning_configs(tenant_id)

async def update_agent_fine_tuning(tenant_id: str, config_id: str, updates: Dict[str, Any]) -> AgentFineTuningConfig:
    """Update existing fine-tuning configuration"""
    return await ai_agent_fine_tuner.update_fine_tuning_config(tenant_id, config_id, updates)

async def delete_agent_fine_tuning(tenant_id: str, config_id: str) -> bool:
    """Delete fine-tuning configuration"""
    return await ai_agent_fine_tuner.delete_fine_tuning_config(tenant_id, config_id)

async def get_fine_tuning_templates(industry_type: Optional[IndustryType] = None) -> List[FineTuningTemplate]:
    """Get available fine-tuning templates"""
    return await ai_agent_fine_tuner.get_available_templates(industry_type)

async def apply_fine_tuning_configuration(tenant_id: str, agent_id: str, config_id: str) -> Dict[str, Any]:
    """Apply fine-tuning configuration to agent"""
    return await ai_agent_fine_tuner.apply_fine_tuning_to_agent(tenant_id, agent_id, config_id)

async def get_tenant_fine_tuning_analytics(tenant_id: str) -> Dict[str, Any]:
    """Get fine-tuning analytics for tenant"""
    return await ai_agent_fine_tuner.get_fine_tuning_analytics(tenant_id)