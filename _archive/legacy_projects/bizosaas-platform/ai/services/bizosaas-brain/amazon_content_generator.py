"""
Automated Content Generation Engine for Amazon Listings

AI-powered content generator that creates optimized Amazon listing content
using the 93+ CrewAI agents ecosystem with specialized content creation agents.
"""

import asyncio
import json
import logging
import re
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
import uuid

from shared.enhanced_tenant_context import EnhancedTenantContext
from ai.services.bizosaas_brain.tenant_aware_ai_coordinator import TenantAwareAICoordinator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContentStyle(str, Enum):
    """Content style options"""
    CASUAL = "casual"
    PROFESSIONAL = "professional"
    PREMIUM = "premium"
    TECHNICAL = "technical"
    CONVERSATIONAL = "conversational"

class ContentTone(str, Enum):
    """Content tone options"""
    FRIENDLY = "friendly"
    AUTHORITATIVE = "authoritative"
    PERSUASIVE = "persuasive"
    INFORMATIVE = "informative"
    ENTHUSIASTIC = "enthusiastic"

class TargetAudience(str, Enum):
    """Target audience types"""
    GENERAL = "general_consumers"
    PROFESSIONALS = "professionals"
    STUDENTS = "students"
    FAMILIES = "families"
    TECH_SAVVY = "tech_savvy"
    BUDGET_CONSCIOUS = "budget_conscious"
    PREMIUM_BUYERS = "premium_buyers"

@dataclass
class ContentGenerationConfig:
    """Configuration for content generation"""
    style: ContentStyle = ContentStyle.PROFESSIONAL
    tone: ContentTone = ContentTone.PERSUASIVE
    target_audience: TargetAudience = TargetAudience.GENERAL

    # Length constraints
    max_title_length: int = 200
    max_description_length: int = 2000
    max_bullet_points: int = 5
    min_description_length: int = 300

    # SEO optimization
    seo_focus: bool = True
    keyword_density: float = 0.02
    include_trending_keywords: bool = True

    # Market specifics
    target_market: str = "indian_consumers"
    local_language_hints: bool = True
    cultural_adaptation: bool = True

    # Content enhancement
    include_benefits: bool = True
    include_specifications: bool = True
    include_usage_scenarios: bool = True
    include_comparisons: bool = False

    # Amazon specific
    optimize_for_amazon_algorithm: bool = True
    include_search_terms: bool = True
    emphasize_features: bool = True

@dataclass
class ContentPrompt:
    """AI prompt configuration for content generation"""
    agent_type: str
    system_context: str
    user_prompt: str
    expected_output_format: str
    constraints: Dict[str, Any]
    priority: int = 5  # 1-10 scale

@dataclass
class GeneratedContent:
    """Generated content result"""
    content_type: str
    content: str
    quality_score: float
    seo_score: float
    readability_score: float
    generation_time: float
    agent_confidence: float
    used_keywords: List[str]
    suggestions: List[str] = None
    warnings: List[str] = None

@dataclass
class AmazonListingContent:
    """Complete Amazon listing content"""
    # Core content
    title: GeneratedContent
    description: GeneratedContent
    bullet_points: List[GeneratedContent]

    # SEO content
    keywords: List[str]
    search_terms: List[str]
    backend_keywords: List[str]

    # Product information
    product_features: List[str]
    specifications: Dict[str, str]

    # Marketing content
    value_propositions: List[str]
    unique_selling_points: List[str]
    target_keywords: List[str]

    # Quality metrics
    overall_quality_score: float
    seo_optimization_score: float
    readability_score: float
    amazon_compliance_score: float

    # Metadata
    generation_config: ContentGenerationConfig
    generated_at: datetime
    content_id: str

class AmazonContentGenerator:
    """AI-powered Amazon listing content generator"""

    def __init__(self, ai_coordinator: TenantAwareAICoordinator):
        self.ai_coordinator = ai_coordinator
        self.content_templates = self._load_content_templates()
        self.seo_guidelines = self._load_seo_guidelines()
        self.amazon_requirements = self._load_amazon_requirements()

    async def generate_complete_listing_content(
        self,
        research_data: Dict[str, Any],
        config: ContentGenerationConfig,
        tenant_context: EnhancedTenantContext
    ) -> AmazonListingContent:
        """Generate complete Amazon listing content using AI agents"""

        logger.info("🎨 Starting AI-powered Amazon listing content generation")

        content_id = str(uuid.uuid4())
        start_time = datetime.utcnow()

        try:
            # Extract product information from research
            product_info = self._extract_product_information(research_data)

            # Generate content components concurrently
            content_tasks = [
                self._generate_optimized_title(product_info, config, tenant_context),
                self._generate_enhanced_description(product_info, config, tenant_context),
                self._generate_bullet_points(product_info, config, tenant_context),
                self._generate_keywords_and_search_terms(product_info, config, tenant_context),
                self._generate_marketing_content(product_info, config, tenant_context)
            ]

            (title_content, description_content, bullet_points_content,
             keywords_data, marketing_content) = await asyncio.gather(*content_tasks)

            # Calculate overall quality scores
            quality_scores = self._calculate_quality_scores([
                title_content, description_content, *bullet_points_content
            ])

            # Construct final listing content
            listing_content = AmazonListingContent(
                title=title_content,
                description=description_content,
                bullet_points=bullet_points_content,
                keywords=keywords_data["keywords"],
                search_terms=keywords_data["search_terms"],
                backend_keywords=keywords_data["backend_keywords"],
                product_features=marketing_content["features"],
                specifications=marketing_content["specifications"],
                value_propositions=marketing_content["value_propositions"],
                unique_selling_points=marketing_content["unique_selling_points"],
                target_keywords=keywords_data["target_keywords"],
                overall_quality_score=quality_scores["overall"],
                seo_optimization_score=quality_scores["seo"],
                readability_score=quality_scores["readability"],
                amazon_compliance_score=quality_scores["compliance"],
                generation_config=config,
                generated_at=start_time,
                content_id=content_id
            )

            generation_time = (datetime.utcnow() - start_time).total_seconds()
            logger.info(f"✅ Content generation completed in {generation_time:.2f}s with quality score: {quality_scores['overall']:.2f}")

            return listing_content

        except Exception as e:
            logger.error(f"❌ Content generation failed: {str(e)}")
            raise

    def _extract_product_information(self, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract key product information from research data"""

        product_info = {
            "basic_info": {},
            "features": [],
            "benefits": [],
            "specifications": {},
            "competitive_advantages": [],
            "target_audience": [],
            "use_cases": [],
            "pricing_info": {},
            "quality_indicators": []
        }

        # Extract from discovery stage
        discovery_data = research_data.get("stage_2_discovery", {})
        products = discovery_data.get("products", [])

        if products:
            primary_product = products[0]
            product_info["basic_info"] = {
                "title": primary_product.get("title", ""),
                "description": primary_product.get("description", ""),
                "brand": primary_product.get("brand", ""),
                "category": primary_product.get("category", ""),
                "price": primary_product.get("price", 0),
                "rating": primary_product.get("rating", 0),
                "images": primary_product.get("images", [])
            }

            product_info["features"] = primary_product.get("features", [])
            product_info["specifications"] = primary_product.get("specifications", {})

        # Extract competitive advantages
        competition_data = research_data.get("stage_3_competition", {})
        product_info["competitive_advantages"] = competition_data.get("differentiation_opportunities", [])

        # Extract quality indicators
        quality_data = research_data.get("stage_5_quality_risk", {})
        quality_summary = quality_data.get("summary", {})
        product_info["quality_indicators"] = [
            f"Quality Score: {quality_summary.get('average_quality', 0):.1f}/100",
            f"Low Risk Product: {quality_summary.get('low_risk_products', 0)} verified",
            f"Recommended Status: {quality_summary.get('recommended_products', 0) > 0}"
        ]

        # Extract market insights
        market_insights = research_data.get("market_insights", {})
        product_info["target_audience"] = market_insights.get("target_demographics", [])
        product_info["use_cases"] = market_insights.get("primary_use_cases", [])

        # Extract pricing information
        profit_data = research_data.get("stage_4_profitability", {})
        if profit_data:
            individual_analyses = profit_data.get("individual_analyses", [])
            if individual_analyses:
                profit_analysis = individual_analyses[0].get("profit_analysis", {})
                product_info["pricing_info"] = {
                    "profit_margin": profit_analysis.get("profit_margin_percent", 0),
                    "recommended_price": profit_analysis.get("recommended_selling_price", 0),
                    "cost_breakdown": profit_analysis.get("cost_breakdown", {})
                }

        return product_info

    async def _generate_optimized_title(
        self,
        product_info: Dict[str, Any],
        config: ContentGenerationConfig,
        tenant_context: EnhancedTenantContext
    ) -> GeneratedContent:
        """Generate SEO-optimized Amazon title using AI agents"""

        # Prepare AI prompt for title generation
        title_prompt = self._create_title_generation_prompt(product_info, config)

        # Use AI coordinator with specialized agents
        ai_response = await self.ai_coordinator.coordinate_analysis(
            tenant_context=tenant_context,
            analysis_type="amazon_title_generation",
            data={
                "product_info": product_info,
                "config": asdict(config),
                "prompt": title_prompt
            },
            agent_specializations=[
                "seo_specialist",
                "content_creator",
                "amazon_listing_expert",
                "copywriter"
            ]
        )

        if not ai_response.get("success", False):
            raise Exception(f"Title generation failed: {ai_response.get('error', 'Unknown error')}")

        # Extract and process AI response
        ai_data = ai_response.get("data", {})
        generated_title = ai_data.get("optimized_title", "")

        # Validate and enhance title
        enhanced_title = self._enhance_title_with_seo(generated_title, product_info, config)

        # Calculate quality scores
        quality_score = self._calculate_title_quality_score(enhanced_title, product_info)
        seo_score = self._calculate_title_seo_score(enhanced_title, product_info)
        readability_score = self._calculate_readability_score(enhanced_title)

        # Extract used keywords
        used_keywords = self._extract_keywords_from_content(enhanced_title)

        return GeneratedContent(
            content_type="title",
            content=enhanced_title,
            quality_score=quality_score,
            seo_score=seo_score,
            readability_score=readability_score,
            generation_time=0.0,  # Will be set by caller
            agent_confidence=ai_data.get("confidence", 0.8),
            used_keywords=used_keywords,
            suggestions=ai_data.get("suggestions", []),
            warnings=ai_data.get("warnings", [])
        )

    def _create_title_generation_prompt(
        self,
        product_info: Dict[str, Any],
        config: ContentGenerationConfig
    ) -> ContentPrompt:
        """Create AI prompt for title generation"""

        basic_info = product_info["basic_info"]
        features = product_info["features"][:3]  # Top 3 features
        competitive_advantages = product_info["competitive_advantages"][:2]  # Top 2 advantages

        system_context = f"""
        You are an expert Amazon listing specialist with deep knowledge of Amazon's search algorithm
        and SEO best practices for the Indian marketplace. Your task is to create compelling,
        SEO-optimized product titles that drive visibility and conversions.

        Target Audience: {config.target_audience.value}
        Content Style: {config.style.value}
        Content Tone: {config.tone.value}
        Market: {config.target_market}
        """

        user_prompt = f"""
        Create an optimized Amazon product title for the following product:

        Product Information:
        - Original Title: {basic_info.get('title', '')}
        - Brand: {basic_info.get('brand', '')}
        - Category: {basic_info.get('category', '')}
        - Key Features: {', '.join(features)}
        - Competitive Advantages: {', '.join(competitive_advantages)}
        - Price Range: ₹{basic_info.get('price', 0):,.0f}

        Requirements:
        1. Maximum {config.max_title_length} characters
        2. Include brand name and key features
        3. Optimize for Amazon search algorithm
        4. Use persuasive language that drives clicks
        5. Include relevant keywords naturally
        6. Follow Amazon's title guidelines
        7. Make it appealing to Indian consumers
        8. Ensure it stands out from competitors

        Style Guidelines:
        - Use {config.style.value} style
        - Maintain {config.tone.value} tone
        - Target {config.target_audience.value}
        - Include power words and emotional triggers
        - Use proper capitalization
        - Avoid excessive punctuation

        Generate 3 title variations and select the best one.
        """

        return ContentPrompt(
            agent_type="seo_specialist",
            system_context=system_context,
            user_prompt=user_prompt,
            expected_output_format="optimized_title, confidence_score, suggestions, warnings",
            constraints={
                "max_length": config.max_title_length,
                "required_elements": ["brand", "key_feature", "category"],
                "forbidden_elements": ["excessive_punctuation", "promotional_text", "price"]
            },
            priority=9
        )

    def _enhance_title_with_seo(
        self,
        generated_title: str,
        product_info: Dict[str, Any],
        config: ContentGenerationConfig
    ) -> str:
        """Enhance generated title with additional SEO optimizations"""

        if not generated_title:
            return ""

        enhanced_title = generated_title.strip()

        # Ensure brand is present
        brand = product_info["basic_info"].get("brand", "")
        if brand and brand.lower() not in enhanced_title.lower():
            if len(enhanced_title + f" by {brand}") <= config.max_title_length:
                enhanced_title = f"{brand} {enhanced_title}"

        # Add category hint if not present
        category = product_info["basic_info"].get("category", "")
        if category and category.lower() not in enhanced_title.lower():
            category_hint = self._get_category_hint(category)
            if category_hint and len(enhanced_title + f" - {category_hint}") <= config.max_title_length:
                enhanced_title += f" - {category_hint}"

        # Ensure proper capitalization
        enhanced_title = self._optimize_title_capitalization(enhanced_title)

        # Final length check
        if len(enhanced_title) > config.max_title_length:
            enhanced_title = enhanced_title[:config.max_title_length - 3] + "..."

        return enhanced_title

    def _get_category_hint(self, category: str) -> str:
        """Get category hint for title enhancement"""

        category_hints = {
            "electronics": "Electronic Device",
            "mobile": "Smartphone",
            "computer": "PC Accessory",
            "clothing": "Apparel",
            "home": "Home Essential",
            "health": "Health Product",
            "beauty": "Beauty Essential",
            "sports": "Sports Equipment",
            "toys": "Educational Toy",
            "books": "Book",
            "automotive": "Car Accessory"
        }

        category_lower = category.lower()
        for key, hint in category_hints.items():
            if key in category_lower:
                return hint

        return ""

    def _optimize_title_capitalization(self, title: str) -> str:
        """Optimize title capitalization for Amazon"""

        # Words that should not be capitalized (unless they're the first word)
        lowercase_words = {
            'a', 'an', 'and', 'as', 'at', 'but', 'by', 'for', 'if', 'in', 'of',
            'on', 'or', 'the', 'to', 'up', 'via', 'with', 'from', 'into', 'onto'
        }

        words = title.split()
        optimized_words = []

        for i, word in enumerate(words):
            if i == 0:  # First word is always capitalized
                optimized_words.append(word.capitalize())
            elif word.lower() in lowercase_words:
                optimized_words.append(word.lower())
            else:
                optimized_words.append(word.capitalize())

        return ' '.join(optimized_words)

    async def _generate_enhanced_description(
        self,
        product_info: Dict[str, Any],
        config: ContentGenerationConfig,
        tenant_context: EnhancedTenantContext
    ) -> GeneratedContent:
        """Generate enhanced product description using AI agents"""

        # Prepare AI prompt for description generation
        description_prompt = self._create_description_generation_prompt(product_info, config)

        # Use AI coordinator with specialized agents
        ai_response = await self.ai_coordinator.coordinate_analysis(
            tenant_context=tenant_context,
            analysis_type="amazon_description_generation",
            data={
                "product_info": product_info,
                "config": asdict(config),
                "prompt": description_prompt
            },
            agent_specializations=[
                "content_creator",
                "marketing_strategist",
                "seo_specialist",
                "copywriter"
            ]
        )

        if not ai_response.get("success", False):
            raise Exception(f"Description generation failed: {ai_response.get('error', 'Unknown error')}")

        # Extract and process AI response
        ai_data = ai_response.get("data", {})
        generated_description = ai_data.get("enhanced_description", "")

        # Enhance description with structured content
        enhanced_description = self._structure_description_content(
            generated_description, product_info, config
        )

        # Calculate quality scores
        quality_score = self._calculate_description_quality_score(enhanced_description, product_info)
        seo_score = self._calculate_description_seo_score(enhanced_description, product_info)
        readability_score = self._calculate_readability_score(enhanced_description)

        # Extract used keywords
        used_keywords = self._extract_keywords_from_content(enhanced_description)

        return GeneratedContent(
            content_type="description",
            content=enhanced_description,
            quality_score=quality_score,
            seo_score=seo_score,
            readability_score=readability_score,
            generation_time=0.0,
            agent_confidence=ai_data.get("confidence", 0.8),
            used_keywords=used_keywords,
            suggestions=ai_data.get("suggestions", []),
            warnings=ai_data.get("warnings", [])
        )

    def _create_description_generation_prompt(
        self,
        product_info: Dict[str, Any],
        config: ContentGenerationConfig
    ) -> ContentPrompt:
        """Create AI prompt for description generation"""

        basic_info = product_info["basic_info"]
        features = product_info["features"]
        benefits = product_info["benefits"]
        specifications = product_info["specifications"]
        competitive_advantages = product_info["competitive_advantages"]
        use_cases = product_info["use_cases"]

        system_context = f"""
        You are an expert copywriter specializing in Amazon product descriptions that convert browsers
        into buyers. You understand the psychology of online shopping and know how to present products
        in the most compelling way for Indian consumers.

        Target Audience: {config.target_audience.value}
        Content Style: {config.style.value}
        Content Tone: {config.tone.value}
        Market: {config.target_market}
        """

        user_prompt = f"""
        Create a compelling Amazon product description for:

        Product Information:
        - Title: {basic_info.get('title', '')}
        - Brand: {basic_info.get('brand', '')}
        - Category: {basic_info.get('category', '')}
        - Features: {', '.join(features[:10])}
        - Specifications: {', '.join([f'{k}: {v}' for k, v in specifications.items()][:5])}
        - Competitive Advantages: {', '.join(competitive_advantages)}
        - Use Cases: {', '.join(use_cases)}

        Requirements:
        1. Length: {config.min_description_length}-{config.max_description_length} characters
        2. Structure: Opening hook, benefits, features, specifications, call-to-action
        3. Include emotional triggers and logical appeals
        4. Optimize for Amazon search algorithm
        5. Use persuasive copywriting techniques
        6. Include social proof elements
        7. Address common customer concerns
        8. Use Indian context and references where appropriate

        Content Structure:
        1. Compelling opening (2-3 sentences)
        2. Key benefits (3-5 bullet points)
        3. Feature highlights (3-5 points)
        4. Technical specifications (if applicable)
        5. Usage scenarios and applications
        6. Quality assurance and trust signals
        7. Strong closing with call-to-action

        Style Guidelines:
        - Use {config.style.value} writing style
        - Maintain {config.tone.value} tone throughout
        - Target {config.target_audience.value}
        - Include power words and emotional triggers
        - Use short paragraphs for readability
        - Include relevant keywords naturally
        - Add sensory descriptions where appropriate
        """

        return ContentPrompt(
            agent_type="content_creator",
            system_context=system_context,
            user_prompt=user_prompt,
            expected_output_format="enhanced_description, confidence_score, suggestions, warnings",
            constraints={
                "min_length": config.min_description_length,
                "max_length": config.max_description_length,
                "required_sections": ["benefits", "features", "call_to_action"],
                "tone": config.tone.value
            },
            priority=8
        )

    def _structure_description_content(
        self,
        generated_description: str,
        product_info: Dict[str, Any],
        config: ContentGenerationConfig
    ) -> str:
        """Structure description content for optimal readability"""

        if not generated_description:
            return ""

        # Split description into sections
        sections = []

        # Add structured elements if missing
        description_parts = generated_description.split('\n\n')

        # Ensure we have an opening section
        if description_parts:
            sections.append(description_parts[0])

        # Add benefits section if not present
        if 'benefit' not in generated_description.lower():
            benefits = product_info.get("benefits", [])
            if benefits:
                benefits_section = "Key Benefits:\n" + "\n".join([f"• {benefit}" for benefit in benefits[:5]])
                sections.append(benefits_section)

        # Add remaining sections
        sections.extend(description_parts[1:])

        # Add quality assurance if not present
        if 'quality' not in generated_description.lower():
            quality_indicators = product_info.get("quality_indicators", [])
            if quality_indicators:
                quality_section = "Quality Assurance:\n" + "\n".join([f"• {indicator}" for indicator in quality_indicators[:3]])
                sections.append(quality_section)

        # Join sections with proper spacing
        structured_description = '\n\n'.join(sections)

        # Ensure length constraints
        if len(structured_description) > config.max_description_length:
            structured_description = structured_description[:config.max_description_length - 3] + "..."
        elif len(structured_description) < config.min_description_length:
            # Add padding content if too short
            padding = self._generate_padding_content(product_info, config.min_description_length - len(structured_description))
            structured_description += f"\n\n{padding}"

        return structured_description

    def _generate_padding_content(self, product_info: Dict[str, Any], needed_length: int) -> str:
        """Generate additional content to meet minimum length requirements"""

        padding_content = []

        # Add usage tips
        padding_content.append("Usage Tips: This product is designed for optimal performance and user satisfaction.")

        # Add care instructions
        padding_content.append("Care Instructions: Follow manufacturer guidelines for best results and longevity.")

        # Add customer support information
        padding_content.append("Customer Support: Our dedicated team is available to assist with any questions or concerns.")

        # Add warranty information
        padding_content.append("Warranty: Product comes with standard manufacturer warranty for peace of mind.")

        # Join content until we meet length requirement
        padding_text = " ".join(padding_content)

        if len(padding_text) < needed_length:
            # Repeat content if still not enough
            multiplier = (needed_length // len(padding_text)) + 1
            padding_text = (padding_text + " ") * multiplier

        return padding_text[:needed_length]

    async def _generate_bullet_points(
        self,
        product_info: Dict[str, Any],
        config: ContentGenerationConfig,
        tenant_context: EnhancedTenantContext
    ) -> List[GeneratedContent]:
        """Generate Amazon bullet points using AI agents"""

        # Prepare AI prompt for bullet points generation
        bullet_prompt = self._create_bullet_points_generation_prompt(product_info, config)

        # Use AI coordinator with specialized agents
        ai_response = await self.ai_coordinator.coordinate_analysis(
            tenant_context=tenant_context,
            analysis_type="amazon_bullet_points_generation",
            data={
                "product_info": product_info,
                "config": asdict(config),
                "prompt": bullet_prompt
            },
            agent_specializations=[
                "content_creator",
                "amazon_listing_expert",
                "marketing_strategist"
            ]
        )

        if not ai_response.get("success", False):
            raise Exception(f"Bullet points generation failed: {ai_response.get('error', 'Unknown error')}")

        # Extract and process AI response
        ai_data = ai_response.get("data", {})
        generated_bullets = ai_data.get("bullet_points", [])

        # Convert to GeneratedContent objects
        bullet_contents = []
        for i, bullet in enumerate(generated_bullets[:config.max_bullet_points]):
            # Calculate quality scores for each bullet point
            quality_score = self._calculate_bullet_quality_score(bullet, product_info)
            seo_score = self._calculate_bullet_seo_score(bullet, product_info)
            readability_score = self._calculate_readability_score(bullet)

            # Extract used keywords
            used_keywords = self._extract_keywords_from_content(bullet)

            bullet_content = GeneratedContent(
                content_type=f"bullet_point_{i+1}",
                content=bullet,
                quality_score=quality_score,
                seo_score=seo_score,
                readability_score=readability_score,
                generation_time=0.0,
                agent_confidence=ai_data.get("confidence", 0.8),
                used_keywords=used_keywords
            )

            bullet_contents.append(bullet_content)

        return bullet_contents

    def _create_bullet_points_generation_prompt(
        self,
        product_info: Dict[str, Any],
        config: ContentGenerationConfig
    ) -> ContentPrompt:
        """Create AI prompt for bullet points generation"""

        basic_info = product_info["basic_info"]
        features = product_info["features"]
        competitive_advantages = product_info["competitive_advantages"]
        specifications = product_info["specifications"]

        system_context = f"""
        You are an Amazon listing expert who creates compelling bullet points that highlight
        the most important product benefits and features. Your bullet points drive purchase
        decisions by addressing customer needs and pain points.

        Target Audience: {config.target_audience.value}
        Content Style: {config.style.value}
        Content Tone: {config.tone.value}
        """

        user_prompt = f"""
        Create {config.max_bullet_points} compelling Amazon bullet points for:

        Product Information:
        - Title: {basic_info.get('title', '')}
        - Brand: {basic_info.get('brand', '')}
        - Key Features: {', '.join(features[:10])}
        - Competitive Advantages: {', '.join(competitive_advantages)}
        - Specifications: {', '.join([f'{k}: {v}' for k, v in specifications.items()][:5])}

        Bullet Point Requirements:
        1. Each bullet point should be 150-200 characters
        2. Start with a benefit, followed by the feature that delivers it
        3. Use action words and emotional triggers
        4. Address specific customer pain points
        5. Include relevant keywords naturally
        6. Make each point unique and valuable
        7. Use bullet point format (• or ✓)
        8. End with impact or benefit to customer

        Content Priorities:
        1. Most important benefit/feature (primary selling point)
        2. Unique differentiator (competitive advantage)
        3. Quality/reliability feature
        4. Convenience/ease of use feature
        5. Value proposition/additional benefit

        Style Guidelines:
        - Use {config.style.value} writing style
        - Maintain {config.tone.value} tone
        - Include power words (premium, advanced, superior, etc.)
        - Focus on customer benefits, not just features
        - Use specific measurements and numbers when available
        - Appeal to emotions while providing logical reasons

        Format each bullet point as: • [BENEFIT]: [Feature explanation] - [Customer impact]
        """

        return ContentPrompt(
            agent_type="amazon_listing_expert",
            system_context=system_context,
            user_prompt=user_prompt,
            expected_output_format="bullet_points_list, confidence_score, suggestions",
            constraints={
                "max_bullet_points": config.max_bullet_points,
                "max_length_per_bullet": 200,
                "required_format": "benefit_feature_impact"
            },
            priority=7
        )

    async def _generate_keywords_and_search_terms(
        self,
        product_info: Dict[str, Any],
        config: ContentGenerationConfig,
        tenant_context: EnhancedTenantContext
    ) -> Dict[str, List[str]]:
        """Generate keywords and search terms using AI agents"""

        # Prepare AI prompt for keyword generation
        keyword_prompt = self._create_keyword_generation_prompt(product_info, config)

        # Use AI coordinator with specialized agents
        ai_response = await self.ai_coordinator.coordinate_analysis(
            tenant_context=tenant_context,
            analysis_type="amazon_keyword_generation",
            data={
                "product_info": product_info,
                "config": asdict(config),
                "prompt": keyword_prompt
            },
            agent_specializations=[
                "seo_specialist",
                "amazon_listing_expert",
                "keyword_researcher"
            ]
        )

        if not ai_response.get("success", False):
            raise Exception(f"Keyword generation failed: {ai_response.get('error', 'Unknown error')}")

        # Extract and process AI response
        ai_data = ai_response.get("data", {})

        return {
            "keywords": ai_data.get("primary_keywords", []),
            "search_terms": ai_data.get("search_terms", []),
            "backend_keywords": ai_data.get("backend_keywords", []),
            "target_keywords": ai_data.get("target_keywords", [])
        }

    def _create_keyword_generation_prompt(
        self,
        product_info: Dict[str, Any],
        config: ContentGenerationConfig
    ) -> ContentPrompt:
        """Create AI prompt for keyword generation"""

        basic_info = product_info["basic_info"]
        features = product_info["features"]
        competitive_advantages = product_info["competitive_advantages"]

        system_context = f"""
        You are an Amazon SEO specialist with deep knowledge of keyword research and
        Amazon's search algorithm. You understand how Indian consumers search for products
        and can identify high-converting keywords.

        Target Market: {config.target_market}
        Target Audience: {config.target_audience.value}
        """

        user_prompt = f"""
        Generate comprehensive keywords for Amazon listing optimization:

        Product Information:
        - Title: {basic_info.get('title', '')}
        - Brand: {basic_info.get('brand', '')}
        - Category: {basic_info.get('category', '')}
        - Features: {', '.join(features[:10])}
        - Competitive Advantages: {', '.join(competitive_advantages)}

        Generate 4 types of keywords:

        1. Primary Keywords (15-20 keywords):
        - High-volume, high-intent keywords
        - Brand + product type combinations
        - Category-specific keywords
        - Feature-based keywords

        2. Search Terms (10-15 terms):
        - Long-tail keywords
        - Question-based searches
        - Problem-solving keywords
        - Indian market specific terms

        3. Backend Keywords (20-25 keywords):
        - Alternative spellings and variations
        - Competitor brand keywords
        - Related product keywords
        - Seasonal/occasion keywords

        4. Target Keywords (5-8 keywords):
        - High-converting commercial keywords
        - Purchase-intent keywords
        - Comparison keywords

        Requirements:
        - Focus on Indian market search behavior
        - Include Hindi-English mixed terms where appropriate
        - Consider mobile search patterns
        - Include voice search friendly phrases
        - Avoid keyword stuffing
        - Prioritize relevance over volume
        """

        return ContentPrompt(
            agent_type="seo_specialist",
            system_context=system_context,
            user_prompt=user_prompt,
            expected_output_format="primary_keywords, search_terms, backend_keywords, target_keywords",
            constraints={
                "max_primary_keywords": 20,
                "max_search_terms": 15,
                "max_backend_keywords": 25,
                "max_target_keywords": 8
            },
            priority=8
        )

    async def _generate_marketing_content(
        self,
        product_info: Dict[str, Any],
        config: ContentGenerationConfig,
        tenant_context: EnhancedTenantContext
    ) -> Dict[str, Any]:
        """Generate additional marketing content"""

        # Prepare AI prompt for marketing content generation
        marketing_prompt = self._create_marketing_content_prompt(product_info, config)

        # Use AI coordinator with specialized agents
        ai_response = await self.ai_coordinator.coordinate_analysis(
            tenant_context=tenant_context,
            analysis_type="amazon_marketing_content_generation",
            data={
                "product_info": product_info,
                "config": asdict(config),
                "prompt": marketing_prompt
            },
            agent_specializations=[
                "marketing_strategist",
                "content_creator",
                "brand_specialist"
            ]
        )

        if not ai_response.get("success", False):
            raise Exception(f"Marketing content generation failed: {ai_response.get('error', 'Unknown error')}")

        # Extract and process AI response
        ai_data = ai_response.get("data", {})

        return {
            "features": ai_data.get("product_features", []),
            "specifications": ai_data.get("specifications", {}),
            "value_propositions": ai_data.get("value_propositions", []),
            "unique_selling_points": ai_data.get("unique_selling_points", [])
        }

    def _create_marketing_content_prompt(
        self,
        product_info: Dict[str, Any],
        config: ContentGenerationConfig
    ) -> ContentPrompt:
        """Create AI prompt for marketing content generation"""

        basic_info = product_info["basic_info"]
        features = product_info["features"]
        competitive_advantages = product_info["competitive_advantages"]
        specifications = product_info["specifications"]

        system_context = f"""
        You are a marketing strategist specializing in product positioning and value proposition
        development. You excel at identifying what makes products unique and compelling to customers.

        Target Audience: {config.target_audience.value}
        Content Style: {config.style.value}
        """

        user_prompt = f"""
        Create comprehensive marketing content for product positioning:

        Product Information:
        - Title: {basic_info.get('title', '')}
        - Brand: {basic_info.get('brand', '')}
        - Features: {', '.join(features)}
        - Competitive Advantages: {', '.join(competitive_advantages)}
        - Specifications: {', '.join([f'{k}: {v}' for k, v in specifications.items()])}

        Generate:

        1. Product Features (8-10 features):
        - Key functional features
        - Design features
        - Performance features
        - Convenience features

        2. Value Propositions (5-7 propositions):
        - Primary value delivered to customer
        - Problem solved by the product
        - Benefit statements
        - ROI/value statements

        3. Unique Selling Points (3-5 USPs):
        - What makes this product different
        - Competitive advantages
        - Exclusive features or benefits
        - Brand differentiators

        4. Technical Specifications:
        - Enhanced specification descriptions
        - Performance metrics
        - Compatibility information
        - Standard compliance

        Focus on customer benefits and competitive differentiation.
        """

        return ContentPrompt(
            agent_type="marketing_strategist",
            system_context=system_context,
            user_prompt=user_prompt,
            expected_output_format="product_features, value_propositions, unique_selling_points, specifications",
            constraints={
                "max_features": 10,
                "max_value_propositions": 7,
                "max_usps": 5
            },
            priority=6
        )

    def _calculate_quality_scores(self, content_list: List[GeneratedContent]) -> Dict[str, float]:
        """Calculate overall quality scores for generated content"""

        if not content_list:
            return {"overall": 0.0, "seo": 0.0, "readability": 0.0, "compliance": 0.0}

        # Calculate averages
        overall_quality = sum(c.quality_score for c in content_list) / len(content_list)
        seo_quality = sum(c.seo_score for c in content_list) / len(content_list)
        readability_quality = sum(c.readability_score for c in content_list) / len(content_list)

        # Calculate compliance score based on Amazon requirements
        compliance_score = self._calculate_amazon_compliance_score(content_list)

        return {
            "overall": overall_quality,
            "seo": seo_quality,
            "readability": readability_quality,
            "compliance": compliance_score
        }

    def _calculate_title_quality_score(self, title: str, product_info: Dict[str, Any]) -> float:
        """Calculate quality score for title"""

        if not title:
            return 0.0

        score = 0.0

        # Length check (50-200 characters is optimal)
        if 50 <= len(title) <= 200:
            score += 25.0
        elif 30 <= len(title) < 50 or 200 < len(title) <= 250:
            score += 15.0

        # Brand presence
        brand = product_info["basic_info"].get("brand", "")
        if brand and brand.lower() in title.lower():
            score += 20.0

        # Feature inclusion
        features = product_info.get("features", [])
        feature_mentions = sum(1 for feature in features[:5] if feature.lower() in title.lower())
        score += min(20.0, feature_mentions * 4.0)

        # Keyword optimization
        title_words = title.lower().split()
        if len(title_words) >= 5:  # Good keyword coverage
            score += 15.0

        # Readability
        if not re.search(r'[!@#$%^&*()_+=\[\]{}|;:,.<>?]', title):  # No special characters
            score += 10.0

        # Capitalization
        if title.istitle() or all(word[0].isupper() for word in title.split() if word):
            score += 10.0

        return min(100.0, score)

    def _calculate_title_seo_score(self, title: str, product_info: Dict[str, Any]) -> float:
        """Calculate SEO score for title"""

        if not title:
            return 0.0

        score = 0.0

        # Keyword density
        title_words = title.lower().split()
        unique_words = set(title_words)

        # Good word variety
        if len(unique_words) / len(title_words) > 0.7:  # Low repetition
            score += 20.0

        # Brand positioning (brand in first 3 words)
        brand = product_info["basic_info"].get("brand", "")
        if brand and brand.lower() in " ".join(title_words[:3]):
            score += 25.0

        # Category relevance
        category = product_info["basic_info"].get("category", "")
        if category and category.lower() in title.lower():
            score += 20.0

        # Feature keywords
        features = product_info.get("features", [])
        feature_keywords = []
        for feature in features:
            feature_keywords.extend(feature.lower().split())

        feature_coverage = sum(1 for word in title_words if word in feature_keywords)
        score += min(25.0, feature_coverage * 5.0)

        # Length optimization
        if 60 <= len(title) <= 150:  # Optimal for search
            score += 10.0

        return min(100.0, score)

    def _calculate_description_quality_score(self, description: str, product_info: Dict[str, Any]) -> float:
        """Calculate quality score for description"""

        if not description:
            return 0.0

        score = 0.0

        # Length check
        if 300 <= len(description) <= 2000:
            score += 20.0
        elif 200 <= len(description) < 300:
            score += 15.0

        # Structure check
        paragraphs = description.split('\n\n')
        if len(paragraphs) >= 3:  # Well-structured
            score += 15.0

        # Feature coverage
        features = product_info.get("features", [])
        feature_mentions = sum(1 for feature in features if feature.lower() in description.lower())
        score += min(20.0, feature_mentions * 2.0)

        # Benefit statements
        benefit_words = ['benefit', 'advantage', 'improve', 'enhance', 'better', 'superior', 'quality']
        benefit_mentions = sum(1 for word in benefit_words if word in description.lower())
        score += min(15.0, benefit_mentions * 3.0)

        # Call to action
        cta_phrases = ['buy now', 'order today', 'get yours', 'experience', 'discover', 'transform']
        if any(phrase in description.lower() for phrase in cta_phrases):
            score += 10.0

        # Readability
        sentences = description.split('.')
        avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
        if 10 <= avg_sentence_length <= 20:  # Good readability
            score += 10.0

        # Professional language
        if not re.search(r'[!]{2,}|[?]{2,}|[A-Z]{3,}', description):  # No excessive punctuation or caps
            score += 10.0

        return min(100.0, score)

    def _calculate_description_seo_score(self, description: str, product_info: Dict[str, Any]) -> float:
        """Calculate SEO score for description"""

        if not description:
            return 0.0

        score = 0.0

        # Keyword density
        description_words = description.lower().split()
        word_count = len(description_words)

        # Brand mentions
        brand = product_info["basic_info"].get("brand", "")
        if brand:
            brand_mentions = description.lower().count(brand.lower())
            if 1 <= brand_mentions <= 3:  # Optimal brand mention frequency
                score += 20.0

        # Category relevance
        category = product_info["basic_info"].get("category", "")
        if category and category.lower() in description.lower():
            score += 15.0

        # Feature keywords
        features = product_info.get("features", [])
        feature_coverage = 0
        for feature in features[:10]:
            if feature.lower() in description.lower():
                feature_coverage += 1

        score += min(25.0, feature_coverage * 2.5)

        # Long-tail keywords
        phrases = [' '.join(description_words[i:i+3]) for i in range(len(description_words)-2)]
        unique_phrases = len(set(phrases))
        if unique_phrases / len(phrases) > 0.8:  # Good phrase variety
            score += 20.0

        # Semantic keywords
        semantic_words = ['quality', 'premium', 'durable', 'reliable', 'efficient', 'innovative']
        semantic_coverage = sum(1 for word in semantic_words if word in description.lower())
        score += min(20.0, semantic_coverage * 3.0)

        return min(100.0, score)

    def _calculate_bullet_quality_score(self, bullet: str, product_info: Dict[str, Any]) -> float:
        """Calculate quality score for bullet point"""

        if not bullet:
            return 0.0

        score = 0.0

        # Length check (100-200 characters is optimal)
        if 100 <= len(bullet) <= 200:
            score += 30.0
        elif 80 <= len(bullet) < 100 or 200 < len(bullet) <= 250:
            score += 20.0

        # Structure check (benefit + feature + impact)
        if ':' in bullet or '-' in bullet:  # Structured format
            score += 20.0

        # Action words
        action_words = ['improve', 'enhance', 'provide', 'deliver', 'ensure', 'guarantee', 'offer']
        if any(word in bullet.lower() for word in action_words):
            score += 15.0

        # Specific details
        if re.search(r'\d+', bullet):  # Contains numbers/measurements
            score += 10.0

        # Feature relevance
        features = product_info.get("features", [])
        if any(feature.lower() in bullet.lower() for feature in features):
            score += 15.0

        # Professional language
        if bullet.startswith('•') or bullet.startswith('✓'):
            score += 10.0

        return min(100.0, score)

    def _calculate_bullet_seo_score(self, bullet: str, product_info: Dict[str, Any]) -> float:
        """Calculate SEO score for bullet point"""

        if not bullet:
            return 0.0

        score = 0.0

        # Keyword inclusion
        bullet_words = bullet.lower().split()

        # Brand mention
        brand = product_info["basic_info"].get("brand", "")
        if brand and brand.lower() in bullet.lower():
            score += 25.0

        # Feature keywords
        features = product_info.get("features", [])
        feature_mentions = sum(1 for feature in features if feature.lower() in bullet.lower())
        score += min(25.0, feature_mentions * 5.0)

        # Category relevance
        category = product_info["basic_info"].get("category", "")
        if category and category.lower() in bullet.lower():
            score += 20.0

        # Power words
        power_words = ['premium', 'advanced', 'superior', 'exclusive', 'professional', 'high-quality']
        power_word_count = sum(1 for word in power_words if word in bullet.lower())
        score += min(15.0, power_word_count * 5.0)

        # Specificity
        if re.search(r'\d+|\b(best|top|leading|ultimate)\b', bullet.lower()):
            score += 15.0

        return min(100.0, score)

    def _calculate_readability_score(self, text: str) -> float:
        """Calculate readability score for text"""

        if not text:
            return 0.0

        # Simple readability metrics
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        if not sentences:
            return 0.0

        words = text.split()
        total_words = len(words)
        total_sentences = len(sentences)

        # Average sentence length
        avg_sentence_length = total_words / total_sentences if total_sentences > 0 else 0

        # Average word length
        avg_word_length = sum(len(word) for word in words) / total_words if total_words > 0 else 0

        score = 0.0

        # Optimal sentence length (10-20 words)
        if 10 <= avg_sentence_length <= 20:
            score += 40.0
        elif 5 <= avg_sentence_length < 10 or 20 < avg_sentence_length <= 30:
            score += 25.0

        # Optimal word length (4-6 characters)
        if 4 <= avg_word_length <= 6:
            score += 30.0
        elif 3 <= avg_word_length < 4 or 6 < avg_word_length <= 8:
            score += 20.0

        # Simple language preference
        complex_words = [word for word in words if len(word) > 10]
        if len(complex_words) / total_words < 0.1:  # Less than 10% complex words
            score += 30.0

        return min(100.0, score)

    def _calculate_amazon_compliance_score(self, content_list: List[GeneratedContent]) -> float:
        """Calculate Amazon compliance score"""

        score = 0.0
        checks = 0

        for content in content_list:
            checks += 1

            # Length compliance
            if content.content_type == "title":
                if len(content.content) <= 200:
                    score += 20.0
            elif content.content_type == "description":
                if 100 <= len(content.content) <= 2000:
                    score += 20.0
            elif "bullet_point" in content.content_type:
                if 50 <= len(content.content) <= 255:
                    score += 20.0

            # Content quality
            if content.quality_score >= 70:
                score += 10.0

            # No prohibited content
            prohibited_terms = ['best', 'number 1', '#1', 'amazon', 'free shipping', 'guaranteed']
            if not any(term in content.content.lower() for term in prohibited_terms):
                score += 10.0

        return score / checks if checks > 0 else 0.0

    def _extract_keywords_from_content(self, content: str) -> List[str]:
        """Extract keywords from generated content"""

        if not content:
            return []

        # Extract meaningful words (3+ characters, not stop words)
        words = re.findall(r'\b[a-zA-Z]{3,}\b', content.lower())

        # Remove stop words
        stop_words = {
            'the', 'and', 'for', 'with', 'this', 'that', 'from', 'are', 'was', 'will',
            'can', 'has', 'have', 'had', 'been', 'you', 'your', 'our', 'their', 'they',
            'when', 'where', 'what', 'how', 'why', 'who', 'which', 'than', 'more',
            'most', 'very', 'just', 'only', 'also', 'even', 'much', 'many', 'some'
        }

        keywords = [word for word in words if word not in stop_words]

        # Return unique keywords
        return list(set(keywords))

    def _load_content_templates(self) -> Dict[str, str]:
        """Load content generation templates"""
        # In production, this would load from database or external service
        return {
            "title_template": "{brand} {product_name} - {key_feature} | {category}",
            "description_opening": "Discover the {product_type} that transforms your {use_case} experience.",
            "bullet_format": "• {benefit}: {feature} - {customer_impact}",
            "cta_templates": ["Order now and experience the difference!", "Get yours today!", "Transform your experience!"]
        }

    def _load_seo_guidelines(self) -> Dict[str, Any]:
        """Load SEO guidelines and best practices"""
        return {
            "keyword_density": 0.02,
            "title_length": {"min": 50, "max": 200, "optimal": 150},
            "description_length": {"min": 300, "max": 2000, "optimal": 1000},
            "bullet_length": {"min": 100, "max": 200, "optimal": 150}
        }

    def _load_amazon_requirements(self) -> Dict[str, Any]:
        """Load Amazon listing requirements and restrictions"""
        return {
            "prohibited_words": ["best", "number 1", "#1", "amazon", "free shipping"],
            "required_elements": ["brand", "product_type", "key_feature"],
            "character_limits": {
                "title": 200,
                "description": 2000,
                "bullet_point": 255,
                "search_terms": 250
            }
        }

# Export main class
__all__ = ["AmazonContentGenerator", "ContentGenerationConfig", "AmazonListingContent"]