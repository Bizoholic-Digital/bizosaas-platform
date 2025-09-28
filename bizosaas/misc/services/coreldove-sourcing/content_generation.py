"""
AI Content Generation Service for CoreLDove
Generates optimized product descriptions, titles, and marketing copy
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import json
import openai
from datetime import datetime
import re
import nltk
from textstat import flesch_reading_ease, flesch_kincaid_grade
import aiohttp

logger = logging.getLogger(__name__)

class ContentType(Enum):
    TITLE = "title"
    DESCRIPTION = "description"
    BULLET_POINTS = "bullet_points"
    META_DESCRIPTION = "meta_description"
    TAGS = "tags"
    SHORT_DESCRIPTION = "short_description"
    FEATURES = "features"
    BENEFITS = "benefits"

class ToneType(Enum):
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    FRIENDLY = "friendly"
    AUTHORITATIVE = "authoritative"
    PERSUASIVE = "persuasive"
    INFORMATIVE = "informative"

@dataclass
class ContentGenerationRequest:
    product_id: str
    product_data: Dict[str, Any]
    keyword_research: Optional[Dict[str, Any]] = None
    content_types: List[ContentType] = None
    tone: ToneType = ToneType.PROFESSIONAL
    target_audience: str = "general consumers"
    include_seo_optimization: bool = True
    character_limits: Dict[str, int] = None
    generate_variations: bool = False
    variation_count: int = 3

@dataclass 
class GeneratedContent:
    content_type: ContentType
    content: str
    character_count: int
    word_count: int
    seo_score: float
    readability_score: float
    keyword_density: Dict[str, float]
    variations: List[str] = None

@dataclass
class ContentGenerationResult:
    request_id: str
    product_id: str
    generated_content: Dict[ContentType, GeneratedContent]
    overall_seo_score: float
    overall_readability_score: float
    processing_time_seconds: float
    tokens_used: int
    cost_usd: float
    recommendations: List[str]
    created_at: datetime

class SEOAnalyzer:
    """Analyzes content for SEO optimization"""
    
    def __init__(self):
        self.target_keyword_density_range = (1.0, 3.0)  # 1-3%
        self.ideal_readability_score = 60  # Flesch Reading Ease
        
    def analyze_content(self, content: str, target_keywords: List[str] = None) -> Dict[str, Any]:
        """Analyze content for SEO metrics"""
        
        if not content:
            return {"error": "No content provided"}
        
        # Basic metrics
        word_count = len(content.split())
        character_count = len(content)
        
        # Readability
        readability_score = flesch_reading_ease(content)
        grade_level = flesch_kincaid_grade(content)
        
        # Keyword density
        keyword_density = {}
        if target_keywords:
            content_lower = content.lower()
            for keyword in target_keywords:
                keyword_lower = keyword.lower()
                count = content_lower.count(keyword_lower)
                density = (count / word_count) * 100 if word_count > 0 else 0
                keyword_density[keyword] = round(density, 2)
        
        # SEO Score calculation
        seo_score = self._calculate_seo_score(
            word_count, readability_score, keyword_density
        )
        
        return {
            "word_count": word_count,
            "character_count": character_count,
            "readability_score": readability_score,
            "grade_level": grade_level,
            "keyword_density": keyword_density,
            "seo_score": seo_score,
            "recommendations": self._generate_recommendations(
                word_count, readability_score, keyword_density
            )
        }
    
    def _calculate_seo_score(self, word_count: int, readability_score: float, 
                           keyword_density: Dict[str, float]) -> float:
        """Calculate overall SEO score (0-100)"""
        
        score = 0.0
        max_score = 100.0
        
        # Word count score (25 points)
        if 50 <= word_count <= 300:
            score += 25
        elif 30 <= word_count < 50 or 300 < word_count <= 500:
            score += 15
        elif word_count > 10:
            score += 5
        
        # Readability score (25 points)
        if 50 <= readability_score <= 80:
            score += 25
        elif 40 <= readability_score < 50 or 80 < readability_score <= 90:
            score += 15
        elif readability_score > 0:
            score += 5
        
        # Keyword density score (25 points)
        if keyword_density:
            avg_density = sum(keyword_density.values()) / len(keyword_density)
            if self.target_keyword_density_range[0] <= avg_density <= self.target_keyword_density_range[1]:
                score += 25
            elif avg_density < 5.0:  # Not too high
                score += 15
            else:
                score += 5
        
        # Structure and formatting (25 points) - simplified for now
        score += 15  # Default good structure score
        
        return min(score, max_score)
    
    def _generate_recommendations(self, word_count: int, readability_score: float,
                                keyword_density: Dict[str, float]) -> List[str]:
        """Generate SEO improvement recommendations"""
        
        recommendations = []
        
        if word_count < 50:
            recommendations.append("Consider adding more content to improve SEO value")
        elif word_count > 500:
            recommendations.append("Consider shortening content for better readability")
        
        if readability_score < 40:
            recommendations.append("Simplify language to improve readability")
        elif readability_score > 90:
            recommendations.append("Add more descriptive language for better engagement")
        
        if keyword_density:
            for keyword, density in keyword_density.items():
                if density < 1.0:
                    recommendations.append(f"Consider using '{keyword}' more frequently")
                elif density > 4.0:
                    recommendations.append(f"Reduce usage of '{keyword}' to avoid keyword stuffing")
        
        return recommendations

class ContentGenerator:
    """AI-powered content generator using OpenAI API"""
    
    def __init__(self, openai_api_key: str, model: str = "gpt-4"):
        openai.api_key = openai_api_key
        self.model = model
        self.seo_analyzer = SEOAnalyzer()
        self.tokens_used = 0
        self.cost_per_token = 0.00003  # Approximate cost for GPT-4
        
    async def generate_content(self, request: ContentGenerationRequest) -> ContentGenerationResult:
        """Generate all requested content types"""
        
        start_time = datetime.utcnow()
        generated_content = {}
        total_tokens = 0
        
        # Extract keywords from research
        keywords = self._extract_keywords(request.keyword_research)
        
        # Generate each content type
        for content_type in (request.content_types or [ContentType.TITLE, ContentType.DESCRIPTION]):
            try:
                content_result = await self._generate_single_content(
                    content_type, request, keywords
                )
                generated_content[content_type] = content_result
                total_tokens += content_result.word_count * 1.3  # Estimate tokens
                
            except Exception as e:
                logger.error(f"Error generating {content_type.value}: {e}")
                continue
        
        # Calculate overall scores
        overall_seo_score = self._calculate_overall_seo_score(generated_content)
        overall_readability_score = self._calculate_overall_readability_score(generated_content)
        
        # Generate recommendations
        recommendations = self._generate_overall_recommendations(generated_content)
        
        end_time = datetime.utcnow()
        processing_time = (end_time - start_time).total_seconds()
        cost_usd = total_tokens * self.cost_per_token
        
        return ContentGenerationResult(
            request_id=f"content_{int(start_time.timestamp())}",
            product_id=request.product_id,
            generated_content=generated_content,
            overall_seo_score=overall_seo_score,
            overall_readability_score=overall_readability_score,
            processing_time_seconds=processing_time,
            tokens_used=int(total_tokens),
            cost_usd=cost_usd,
            recommendations=recommendations,
            created_at=start_time
        )
    
    def _extract_keywords(self, keyword_research: Dict[str, Any]) -> List[str]:
        """Extract keywords from research data"""
        
        if not keyword_research:
            return []
        
        keywords = []
        
        # Primary keywords
        primary = keyword_research.get('primary_keywords', [])
        if isinstance(primary, list):
            keywords.extend(primary)
        
        # Suggested keywords with high volume
        suggested = keyword_research.get('suggested_keywords', [])
        for suggestion in suggested[:5]:  # Top 5 suggestions
            if isinstance(suggestion, dict) and 'keyword' in suggestion:
                keywords.append(suggestion['keyword'])
            elif isinstance(suggestion, str):
                keywords.append(suggestion)
        
        # Keyword groups
        groups = keyword_research.get('keyword_groups', {})
        for group_keywords in groups.values():
            if isinstance(group_keywords, list):
                keywords.extend(group_keywords[:3])  # Top 3 from each group
        
        return list(set(keywords))[:10]  # Unique keywords, max 10
    
    async def _generate_single_content(self, content_type: ContentType, 
                                     request: ContentGenerationRequest,
                                     keywords: List[str]) -> GeneratedContent:
        """Generate a single piece of content"""
        
        prompt = self._build_prompt(content_type, request, keywords)
        
        # Generate main content
        content = await self._call_openai(prompt)
        
        # Generate variations if requested
        variations = []
        if request.generate_variations:
            for i in range(request.variation_count):
                variation_prompt = f"{prompt}\n\nGenerate a different version with the same requirements:"
                variation = await self._call_openai(variation_prompt)
                variations.append(variation)
        
        # Analyze content
        analysis = self.seo_analyzer.analyze_content(content, keywords)
        
        return GeneratedContent(
            content_type=content_type,
            content=content,
            character_count=analysis['character_count'],
            word_count=analysis['word_count'],
            seo_score=analysis['seo_score'],
            readability_score=analysis['readability_score'],
            keyword_density=analysis['keyword_density'],
            variations=variations if variations else None
        )
    
    def _build_prompt(self, content_type: ContentType, request: ContentGenerationRequest,
                     keywords: List[str]) -> str:
        """Build AI prompt for content generation"""
        
        product_data = request.product_data
        
        base_prompt = f"""
You are an expert e-commerce copywriter specializing in creating high-converting product content.

PRODUCT INFORMATION:
- Title: {product_data.get('title', 'N/A')}
- Category: {product_data.get('category', 'N/A')}
- Brand: {product_data.get('brand', 'N/A')}
- Price: ${product_data.get('price', 'N/A')}
- Key Features: {', '.join(product_data.get('features', []))}
- Benefits: {', '.join(product_data.get('benefits', []))}

TARGET AUDIENCE: {request.target_audience}
TONE: {request.tone.value}
TARGET KEYWORDS: {', '.join(keywords) if keywords else 'None provided'}

"""
        
        character_limit = request.character_limits.get(content_type.value) if request.character_limits else None
        
        content_instructions = {
            ContentType.TITLE: f"""
Create a compelling product title that:
- Includes the main keyword naturally
- Highlights key benefits or features
- Is clear and descriptive
- Follows e-commerce best practices
{f"- Must be under {character_limit} characters" if character_limit else "- Should be 50-80 characters"}

Generate only the title, no additional text.
""",
            
            ContentType.DESCRIPTION: f"""
Write a detailed product description that:
- Starts with an engaging hook
- Clearly explains what the product is and does
- Highlights key features and benefits
- Uses bullet points for easy scanning
- Includes target keywords naturally (1-2% density)
- Ends with a compelling call-to-action
- Is written in {request.tone.value} tone for {request.target_audience}
{f"- Must be under {character_limit} characters" if character_limit else "- Should be 200-500 words"}

Format with proper paragraphs and bullet points.
""",
            
            ContentType.BULLET_POINTS: f"""
Create 3-5 key bullet points that highlight:
- Most important product features
- Key benefits to the customer
- Unique selling propositions
- Technical specifications if relevant

Each bullet point should:
- Be concise and scannable
- Start with a strong action word or benefit
- Include relevant keywords naturally
{f"- Total content under {character_limit} characters" if character_limit else "- Be 15-25 words each"}

Format as bullet points with • symbols.
""",
            
            ContentType.META_DESCRIPTION: f"""
Write a meta description for search engines that:
- Summarizes the product clearly
- Includes the primary keyword
- Encourages clicks with compelling language
- Follows SEO best practices
{f"- Must be exactly under {character_limit} characters" if character_limit else "- Must be 150-160 characters"}

Generate only the meta description, no additional text.
""",
            
            ContentType.TAGS: f"""
Generate 8-12 relevant tags/keywords for this product:
- Include primary keywords
- Add related terms customers might search for
- Mix of broad and specific terms
- Include brand name if applicable
- Consider synonyms and variations

Format as comma-separated values.
"""
        }
        
        instruction = content_instructions.get(content_type, "Generate appropriate content for this product.")
        
        return base_prompt + instruction
    
    async def _call_openai(self, prompt: str) -> str:
        """Make API call to OpenAI"""
        
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert e-commerce copywriter focused on creating high-converting, SEO-optimized product content."
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            content = response.choices[0].message.content.strip()
            self.tokens_used += response.usage.total_tokens
            
            return content
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise
    
    def _calculate_overall_seo_score(self, generated_content: Dict[ContentType, GeneratedContent]) -> float:
        """Calculate overall SEO score across all content"""
        
        if not generated_content:
            return 0.0
        
        scores = [content.seo_score for content in generated_content.values()]
        return sum(scores) / len(scores)
    
    def _calculate_overall_readability_score(self, generated_content: Dict[ContentType, GeneratedContent]) -> float:
        """Calculate overall readability score"""
        
        if not generated_content:
            return 0.0
        
        scores = [content.readability_score for content in generated_content.values()]
        return sum(scores) / len(scores)
    
    def _generate_overall_recommendations(self, generated_content: Dict[ContentType, GeneratedContent]) -> List[str]:
        """Generate overall content recommendations"""
        
        recommendations = []
        
        # Analyze keyword consistency across content types
        all_densities = {}
        for content in generated_content.values():
            for keyword, density in content.keyword_density.items():
                if keyword not in all_densities:
                    all_densities[keyword] = []
                all_densities[keyword].append(density)
        
        # Check for keyword consistency
        for keyword, densities in all_densities.items():
            avg_density = sum(densities) / len(densities)
            if avg_density < 1.0:
                recommendations.append(f"Consider using '{keyword}' more consistently across all content")
        
        # Check content length balance
        has_title = ContentType.TITLE in generated_content
        has_description = ContentType.DESCRIPTION in generated_content
        
        if has_title and has_description:
            title_length = generated_content[ContentType.TITLE].character_count
            desc_length = generated_content[ContentType.DESCRIPTION].character_count
            
            if desc_length < title_length * 3:
                recommendations.append("Consider expanding the product description for better SEO value")
        
        # SEO score recommendations
        overall_seo = self._calculate_overall_seo_score(generated_content)
        if overall_seo < 70:
            recommendations.append("Overall SEO score could be improved with better keyword usage and structure")
        
        return recommendations

class ContentOptimizer:
    """Optimizes generated content for specific platforms"""
    
    def __init__(self):
        self.platform_requirements = {
            'amazon': {
                'title_max_chars': 200,
                'description_max_chars': 2000,
                'bullet_points': 5,
                'keywords_in_title': True,
                'html_allowed': False
            },
            'ebay': {
                'title_max_chars': 80,
                'description_max_chars': None,
                'html_allowed': True,
                'keywords_in_title': True
            },
            'shopify': {
                'title_max_chars': 255,
                'description_max_chars': None,
                'html_allowed': True,
                'meta_description_required': True
            }
        }
    
    def optimize_for_platform(self, content: Dict[ContentType, GeneratedContent], 
                            platform: str) -> Dict[ContentType, GeneratedContent]:
        """Optimize content for specific e-commerce platform"""
        
        requirements = self.platform_requirements.get(platform, {})
        optimized_content = {}
        
        for content_type, generated in content.items():
            optimized = self._optimize_single_content(generated, content_type, requirements)
            optimized_content[content_type] = optimized
        
        return optimized_content
    
    def _optimize_single_content(self, content: GeneratedContent, content_type: ContentType,
                               requirements: Dict[str, Any]) -> GeneratedContent:
        """Optimize a single piece of content"""
        
        optimized_text = content.content
        
        # Apply character limits
        if content_type == ContentType.TITLE and requirements.get('title_max_chars'):
            max_chars = requirements['title_max_chars']
            if len(optimized_text) > max_chars:
                optimized_text = optimized_text[:max_chars-3] + "..."
        
        elif content_type == ContentType.DESCRIPTION and requirements.get('description_max_chars'):
            max_chars = requirements['description_max_chars'] 
            if len(optimized_text) > max_chars:
                optimized_text = optimized_text[:max_chars-3] + "..."
        
        # Remove HTML if not allowed
        if not requirements.get('html_allowed', True):
            optimized_text = re.sub(r'<[^>]+>', '', optimized_text)
        
        # Create optimized version
        optimized_content = GeneratedContent(
            content_type=content.content_type,
            content=optimized_text,
            character_count=len(optimized_text),
            word_count=len(optimized_text.split()),
            seo_score=content.seo_score,  # Recalculate if needed
            readability_score=content.readability_score,
            keyword_density=content.keyword_density,
            variations=content.variations
        )
        
        return optimized_content

# Usage example
async def generate_product_content_example():
    """Example usage of the content generation service"""
    
    # Initialize generator
    generator = ContentGenerator(openai_api_key="your-openai-api-key")
    
    # Sample product data
    product_data = {
        "title": "Wireless Bluetooth Earbuds Pro",
        "category": "Electronics",
        "brand": "TechAudio",
        "price": 89.99,
        "features": [
            "Active Noise Cancellation",
            "30-hour battery life", 
            "IPX7 water resistance",
            "Quick charge"
        ],
        "benefits": [
            "Crystal clear sound quality",
            "All-day comfort",
            "Perfect for workouts",
            "Hands-free calling"
        ]
    }
    
    # Sample keyword research
    keyword_research = {
        "primary_keywords": ["wireless bluetooth earbuds", "noise cancelling headphones"],
        "suggested_keywords": [
            {"keyword": "wireless earbuds", "volume": 12000, "competition": "medium"},
            {"keyword": "bluetooth headphones", "volume": 8500, "competition": "high"}
        ],
        "keyword_groups": {
            "product_features": ["noise cancelling", "wireless", "bluetooth"],
            "use_cases": ["workout", "commute", "office"]
        }
    }
    
    # Create generation request
    request = ContentGenerationRequest(
        product_id="prod_123",
        product_data=product_data,
        keyword_research=keyword_research,
        content_types=[ContentType.TITLE, ContentType.DESCRIPTION, ContentType.BULLET_POINTS],
        tone=ToneType.PROFESSIONAL,
        target_audience="tech-savvy consumers",
        include_seo_optimization=True,
        generate_variations=True,
        variation_count=2
    )
    
    # Generate content
    result = await generator.generate_content(request)
    
    # Print results
    print(f"Generated content for product {result.product_id}")
    print(f"Overall SEO Score: {result.overall_seo_score:.1f}")
    print(f"Processing time: {result.processing_time_seconds:.2f}s")
    print(f"Cost: ${result.cost_usd:.4f}")
    
    for content_type, content in result.generated_content.items():
        print(f"\n{content_type.value.upper()}:")
        print(f"Content: {content.content}")
        print(f"SEO Score: {content.seo_score:.1f}")
        print(f"Readability: {content.readability_score:.1f}")
        
        if content.variations:
            print("Variations:")
            for i, variation in enumerate(content.variations, 1):
                print(f"  {i}. {variation}")

if __name__ == "__main__":
    asyncio.run(generate_product_content_example())