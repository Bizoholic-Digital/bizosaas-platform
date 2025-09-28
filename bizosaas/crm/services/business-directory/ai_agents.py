"""
CrewAI Agents for Business Directory Service
Provides AI-powered features for business listings, search, and optimization
"""

import os
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import logging

from crewai import Agent, Task, Crew, Process
from langchain.llms import OpenAI
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langchain.schema import BaseMessage

logger = logging.getLogger(__name__)

class DirectoryAIManager:
    """Manages all AI agents for the business directory service"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            temperature=0.7,
            model_name="gpt-4-turbo-preview",
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        self.agents = self._initialize_agents()
        self.tools = self._initialize_tools()
        
    def _initialize_agents(self) -> Dict[str, Agent]:
        """Initialize all specialized agents for business directory operations"""
        
        agents = {
            # Business Listing Optimizer Agent
            "listing_optimizer": Agent(
                role="Business Listing Optimization Specialist",
                goal="Enhance business descriptions, optimize keywords, and improve SEO for directory listings",
                backstory="""You are an expert in business listing optimization with deep knowledge of 
                SEO, local search, and directory-specific requirements. You help businesses create 
                compelling, search-friendly listings that attract customers and rank well.""",
                verbose=True,
                allow_delegation=False,
                llm=self.llm
            ),
            
            # Lead Scoring Agent  
            "lead_scorer": Agent(
                role="Lead Scoring and Qualification Specialist",
                goal="Score and qualify leads from directory interactions based on behavior and business fit",
                backstory="""You are a data-driven lead qualification expert who analyzes user 
                interactions, business profiles, and engagement patterns to identify high-quality 
                leads and score them for conversion probability.""",
                verbose=True,
                allow_delegation=False,
                llm=self.llm
            ),
            
            # Content Curator Agent
            "content_curator": Agent(
                role="Content Curation and Management Specialist", 
                goal="Manage and curate events, blog posts, and community content for optimal engagement",
                backstory="""You are a content strategist who understands what makes content 
                engaging and valuable for business audiences. You curate, create, and optimize 
                content to drive engagement and business growth.""",
                verbose=True,
                allow_delegation=False,
                llm=self.llm
            ),
            
            # Review Analysis Agent
            "review_analyzer": Agent(
                role="Review Analysis and Sentiment Specialist",
                goal="Analyze business reviews, extract insights, and provide actionable recommendations",
                backstory="""You are an expert in sentiment analysis and customer feedback 
                interpretation. You help businesses understand their customer sentiment, 
                identify improvement areas, and respond effectively to reviews.""",
                verbose=True,
                allow_delegation=False,
                llm=self.llm
            ),
            
            # Search Intelligence Agent
            "search_intelligence": Agent(
                role="Search Intelligence and Recommendation Specialist",
                goal="Provide personalized search recommendations and enhance search results with AI",
                backstory="""You are a search optimization expert who understands user intent, 
                search patterns, and personalization algorithms. You create intelligent search 
                experiences that help users find exactly what they're looking for.""",
                verbose=True,
                allow_delegation=False,
                llm=self.llm
            ),
            
            # Directory SEO Agent
            "seo_optimizer": Agent(
                role="Directory SEO and Visibility Specialist",
                goal="Optimize directory listings for search engines and improve local visibility",
                backstory="""You are an SEO expert specializing in local business optimization 
                and directory listings. You understand Google My Business, local search factors, 
                and directory-specific optimization strategies.""",
                verbose=True,
                allow_delegation=False,
                llm=self.llm
            )
        }
        
        return agents
    
    def _initialize_tools(self) -> List[Tool]:
        """Initialize tools available to agents"""
        
        tools = [
            Tool(
                name="keyword_analyzer",
                description="Analyze keywords for SEO optimization and search ranking",
                func=self._analyze_keywords
            ),
            Tool(
                name="sentiment_analyzer", 
                description="Analyze sentiment of text content and reviews",
                func=self._analyze_sentiment
            ),
            Tool(
                name="content_scorer",
                description="Score content quality and engagement potential",
                func=self._score_content
            ),
            Tool(
                name="search_optimizer",
                description="Optimize search queries and results for better matching",
                func=self._optimize_search
            )
        ]
        
        return tools
    
    def _analyze_keywords(self, text: str) -> str:
        """Analyze keywords in text for SEO optimization"""
        # Simple keyword analysis - in production, use more sophisticated NLP
        keywords = []
        common_business_terms = [
            'service', 'quality', 'professional', 'expert', 'local', 'trusted',
            'certified', 'experienced', 'affordable', 'premium', 'best', 'top'
        ]
        
        text_lower = text.lower()
        for term in common_business_terms:
            if term in text_lower:
                keywords.append(term)
                
        return json.dumps({
            'keywords_found': keywords,
            'keyword_density': len(keywords) / len(text.split()) if text else 0,
            'suggestions': ['Add location-specific terms', 'Include service-specific keywords']
        })
    
    def _analyze_sentiment(self, text: str) -> str:
        """Analyze sentiment of text content"""
        # Simple sentiment analysis - in production, use proper sentiment analysis
        positive_words = ['great', 'excellent', 'amazing', 'wonderful', 'outstanding', 'fantastic']
        negative_words = ['bad', 'terrible', 'awful', 'poor', 'disappointing', 'horrible']
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            sentiment = "positive"
            score = min(0.8, 0.5 + (positive_count - negative_count) * 0.1)
        elif negative_count > positive_count:
            sentiment = "negative"
            score = max(0.2, 0.5 - (negative_count - positive_count) * 0.1)
        else:
            sentiment = "neutral"
            score = 0.5
            
        return json.dumps({
            'sentiment': sentiment,
            'score': score,
            'positive_indicators': positive_count,
            'negative_indicators': negative_count
        })
    
    def _score_content(self, content: str) -> str:
        """Score content quality and engagement potential"""
        # Content scoring based on various factors
        word_count = len(content.split())
        
        # Score based on length
        if word_count < 50:
            length_score = 0.3
        elif word_count < 150:
            length_score = 0.7
        elif word_count < 300:
            length_score = 1.0
        else:
            length_score = 0.8  # Too long might be less engaging
            
        # Check for engagement factors
        has_numbers = any(char.isdigit() for char in content)
        has_questions = '?' in content
        has_calls_to_action = any(cta in content.lower() for cta in ['call', 'contact', 'visit', 'book', 'schedule'])
        
        engagement_score = 0.5
        if has_numbers:
            engagement_score += 0.2
        if has_questions:
            engagement_score += 0.15
        if has_calls_to_action:
            engagement_score += 0.25
            
        overall_score = (length_score + engagement_score) / 2
        
        return json.dumps({
            'overall_score': min(1.0, overall_score),
            'length_score': length_score,
            'engagement_score': engagement_score,
            'word_count': word_count,
            'has_call_to_action': has_calls_to_action
        })
    
    def _optimize_search(self, query: str) -> str:
        """Optimize search queries for better results"""
        # Simple search optimization
        query_words = query.lower().split()
        
        # Add common business search terms
        business_modifiers = ['near me', 'local', 'professional', 'services']
        suggestions = []
        
        for modifier in business_modifiers:
            if modifier not in query.lower():
                suggestions.append(f"{query} {modifier}")
                
        return json.dumps({
            'original_query': query,
            'optimized_suggestions': suggestions[:3],  # Top 3 suggestions
            'search_intent': 'local_business_search' if 'near' in query.lower() else 'general_business_search'
        })

    async def optimize_business_listing(self, business_data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize a business listing using AI"""
        
        try:
            # Create optimization task
            optimization_task = Task(
                description=f"""
                Optimize the business listing for: {business_data.get('name', 'Unknown Business')}
                
                Current business data:
                - Name: {business_data.get('name', '')}
                - Description: {business_data.get('description', '')}
                - Category: {business_data.get('category', '')}
                - Location: {business_data.get('address', '')}
                - Services: {business_data.get('services', [])}
                
                Tasks:
                1. Enhance the business description for better SEO and customer appeal
                2. Suggest optimal keywords for the business category and location
                3. Recommend directory categories for maximum visibility
                4. Provide content improvements for higher engagement
                5. Generate SEO-optimized title suggestions
                
                Focus on local SEO, customer appeal, and directory-specific optimization.
                """,
                agent=self.agents["listing_optimizer"],
                tools=self.tools,
                expected_output="JSON response with optimized listing data and recommendations"
            )
            
            # Create and run crew
            crew = Crew(
                agents=[self.agents["listing_optimizer"]],
                tasks=[optimization_task],
                process=Process.sequential,
                verbose=True
            )
            
            result = crew.kickoff()
            
            # Parse and structure result
            optimization_result = {
                "optimized_description": self._generate_optimized_description(business_data),
                "suggested_keywords": self._generate_keywords(business_data),
                "category_recommendations": self._recommend_categories(business_data),
                "seo_improvements": self._generate_seo_improvements(business_data),
                "engagement_score": self._calculate_engagement_score(business_data),
                "ai_confidence": 0.85
            }
            
            return optimization_result
            
        except Exception as e:
            logger.error(f"Error in listing optimization: {e}")
            return {
                "error": str(e),
                "fallback_optimizations": self._fallback_optimization(business_data)
            }
    
    async def analyze_reviews(self, business_id: str, reviews: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze business reviews and provide insights"""
        
        try:
            review_texts = [review.get('text', '') for review in reviews]
            combined_reviews = ' '.join(review_texts)
            
            analysis_task = Task(
                description=f"""
                Analyze customer reviews for business ID: {business_id}
                
                Reviews to analyze:
                {combined_reviews[:2000]}  # Limit for API
                
                Tasks:
                1. Perform sentiment analysis on all reviews
                2. Identify common themes and topics mentioned
                3. Extract key strengths and weaknesses
                4. Suggest response strategies for negative reviews
                5. Recommend business improvements based on feedback
                6. Calculate overall sentiment score
                
                Provide actionable insights for business improvement.
                """,
                agent=self.agents["review_analyzer"],
                tools=self.tools,
                expected_output="JSON response with detailed review analysis and recommendations"
            )
            
            crew = Crew(
                agents=[self.agents["review_analyzer"]],
                tasks=[analysis_task],
                process=Process.sequential,
                verbose=True
            )
            
            result = crew.kickoff()
            
            # Process analysis results
            analysis_result = {
                "overall_sentiment": self._calculate_overall_sentiment(reviews),
                "sentiment_distribution": self._calculate_sentiment_distribution(reviews),
                "key_themes": self._extract_themes(reviews),
                "strengths": self._identify_strengths(reviews),
                "areas_for_improvement": self._identify_improvements(reviews),
                "response_suggestions": self._generate_response_suggestions(reviews),
                "business_insights": self._generate_business_insights(reviews),
                "recommendation_score": self._calculate_recommendation_score(reviews)
            }
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"Error in review analysis: {e}")
            return {
                "error": str(e),
                "fallback_analysis": self._fallback_review_analysis(reviews)
            }
    
    async def generate_personalized_recommendations(self, user_id: str, search_history: List[str], preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate personalized business recommendations"""
        
        try:
            recommendation_task = Task(
                description=f"""
                Generate personalized business recommendations for user: {user_id}
                
                User data:
                - Search history: {search_history}
                - Preferences: {preferences}
                
                Tasks:
                1. Analyze user search patterns and preferences
                2. Identify business categories of interest
                3. Generate personalized recommendations based on behavior
                4. Score recommendations by relevance and quality
                5. Include reasoning for each recommendation
                
                Focus on relevance, quality, and user satisfaction.
                """,
                agent=self.agents["search_intelligence"],
                tools=self.tools,
                expected_output="JSON list of personalized business recommendations"
            )
            
            crew = Crew(
                agents=[self.agents["search_intelligence"]],
                tasks=[recommendation_task],
                process=Process.sequential,
                verbose=True
            )
            
            result = crew.kickoff()
            
            # Generate structured recommendations
            recommendations = self._generate_recommendations(user_id, search_history, preferences)
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error in recommendation generation: {e}")
            return self._fallback_recommendations()
    
    async def enhance_search_results(self, query: str, initial_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Enhance search results with AI-powered insights"""
        
        try:
            search_task = Task(
                description=f"""
                Enhance search results for query: "{query}"
                
                Initial results: {len(initial_results)} businesses found
                
                Tasks:
                1. Analyze search intent and user needs
                2. Re-rank results based on relevance and quality
                3. Generate search suggestions for better results
                4. Add semantic understanding to match user intent
                5. Provide additional context for results
                
                Improve search experience and result quality.
                """,
                agent=self.agents["search_intelligence"],
                tools=self.tools,
                expected_output="JSON response with enhanced search results and insights"
            )
            
            crew = Crew(
                agents=[self.agents["search_intelligence"]],
                tasks=[search_task],
                process=Process.sequential,
                verbose=True
            )
            
            result = crew.kickoff()
            
            enhanced_results = {
                "enhanced_results": self._enhance_results_ranking(query, initial_results),
                "search_suggestions": self._generate_search_suggestions(query),
                "semantic_matches": self._find_semantic_matches(query, initial_results),
                "search_intent": self._analyze_search_intent(query),
                "result_insights": self._generate_result_insights(initial_results)
            }
            
            return enhanced_results
            
        except Exception as e:
            logger.error(f"Error in search enhancement: {e}")
            return {
                "error": str(e),
                "fallback_results": initial_results
            }
    
    async def score_leads(self, lead_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Score and qualify leads from directory interactions"""
        
        try:
            scoring_task = Task(
                description=f"""
                Score and qualify {len(lead_data)} leads from directory interactions.
                
                Lead data includes user behavior, interaction patterns, and business fit.
                
                Tasks:
                1. Analyze lead quality based on interaction patterns
                2. Score leads for conversion probability
                3. Identify high-value prospects
                4. Categorize leads by intent and fit
                5. Recommend follow-up strategies
                
                Focus on conversion potential and business value.
                """,
                agent=self.agents["lead_scorer"],
                tools=self.tools,
                expected_output="JSON list of scored and qualified leads"
            )
            
            crew = Crew(
                agents=[self.agents["lead_scorer"]],
                tasks=[scoring_task],
                process=Process.sequential,
                verbose=True
            )
            
            result = crew.kickoff()
            
            scored_leads = []
            for lead in lead_data:
                scored_lead = self._score_individual_lead(lead)
                scored_leads.append(scored_lead)
            
            return scored_leads
            
        except Exception as e:
            logger.error(f"Error in lead scoring: {e}")
            return [{"error": str(e)} for _ in lead_data]
    
    async def generate_content(self, content_type: str, topic: str, target_audience: str) -> Dict[str, Any]:
        """Generate blog posts, events, and community content"""
        
        try:
            content_task = Task(
                description=f"""
                Generate {content_type} content about: {topic}
                Target audience: {target_audience}
                
                Content requirements:
                1. Engaging and informative for business audience
                2. SEO-optimized with relevant keywords
                3. Actionable insights and practical value
                4. Professional tone appropriate for business directory
                5. Include call-to-action where appropriate
                
                Create high-quality content that drives engagement.
                """,
                agent=self.agents["content_curator"],
                tools=self.tools,
                expected_output=f"JSON response with generated {content_type} content"
            )
            
            crew = Crew(
                agents=[self.agents["content_curator"]],
                tasks=[content_task],
                process=Process.sequential,
                verbose=True
            )
            
            result = crew.kickoff()
            
            generated_content = self._generate_structured_content(content_type, topic, target_audience)
            
            return generated_content
            
        except Exception as e:
            logger.error(f"Error in content generation: {e}")
            return {
                "error": str(e),
                "fallback_content": self._fallback_content(content_type, topic)
            }
    
    # Helper methods for AI processing
    def _generate_optimized_description(self, business_data: Dict[str, Any]) -> str:
        """Generate optimized business description"""
        name = business_data.get('name', 'Business')
        category = business_data.get('category', 'service')
        location = business_data.get('address', '')
        
        optimized = f"{name} is a trusted {category} provider"
        if location:
            optimized += f" serving {location}"
        optimized += ". We specialize in delivering professional, high-quality services with a focus on customer satisfaction. Our experienced team is committed to exceeding expectations and building lasting relationships with our clients."
        
        return optimized
    
    def _generate_keywords(self, business_data: Dict[str, Any]) -> List[str]:
        """Generate relevant keywords for business"""
        category = business_data.get('category', 'business')
        location = business_data.get('location', '')
        
        keywords = [category, 'professional', 'trusted', 'local', 'expert', 'quality']
        if location:
            keywords.extend([location, f"{location} {category}"])
            
        return keywords[:10]  # Top 10 keywords
    
    def _recommend_categories(self, business_data: Dict[str, Any]) -> List[str]:
        """Recommend directory categories"""
        category = business_data.get('category', '').lower()
        
        category_map = {
            'restaurant': ['Restaurants', 'Food & Dining', 'Local Business'],
            'retail': ['Shopping', 'Retail', 'Local Business'],
            'healthcare': ['Health & Medical', 'Healthcare', 'Professional Services'],
            'technology': ['IT Services', 'Technology', 'Professional Services'],
            'services': ['Professional Services', 'Local Business', 'Consulting']
        }
        
        return category_map.get(category, ['Local Business', 'Professional Services'])
    
    def _generate_seo_improvements(self, business_data: Dict[str, Any]) -> List[str]:
        """Generate SEO improvement suggestions"""
        improvements = [
            "Add location-specific keywords to description",
            "Include service-specific terms for better search matching",
            "Optimize business hours and contact information",
            "Add high-quality photos and visual content",
            "Encourage customer reviews and respond actively"
        ]
        return improvements
    
    def _calculate_engagement_score(self, business_data: Dict[str, Any]) -> float:
        """Calculate engagement potential score"""
        score = 0.5  # Base score
        
        if business_data.get('phone'):
            score += 0.1
        if business_data.get('website'):
            score += 0.1  
        if business_data.get('email'):
            score += 0.1
        if len(business_data.get('description', '')) > 100:
            score += 0.1
        if business_data.get('services'):
            score += 0.1
            
        return min(1.0, score)
    
    def _fallback_optimization(self, business_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback optimization when AI fails"""
        return {
            "basic_optimization": True,
            "suggested_keywords": self._generate_keywords(business_data),
            "category_recommendations": self._recommend_categories(business_data),
            "note": "Basic optimization applied due to AI service unavailability"
        }
    
    def _calculate_overall_sentiment(self, reviews: List[Dict[str, Any]]) -> str:
        """Calculate overall sentiment from reviews"""
        if not reviews:
            return "neutral"
        
        ratings = [review.get('rating', 3) for review in reviews]
        avg_rating = sum(ratings) / len(ratings)
        
        if avg_rating >= 4:
            return "positive"
        elif avg_rating <= 2:
            return "negative"
        else:
            return "neutral"
    
    def _calculate_sentiment_distribution(self, reviews: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate sentiment distribution"""
        if not reviews:
            return {"positive": 0, "neutral": 0, "negative": 0}
        
        positive = sum(1 for r in reviews if r.get('rating', 3) >= 4)
        negative = sum(1 for r in reviews if r.get('rating', 3) <= 2)
        neutral = len(reviews) - positive - negative
        
        total = len(reviews)
        return {
            "positive": positive / total,
            "neutral": neutral / total,
            "negative": negative / total
        }
    
    def _extract_themes(self, reviews: List[Dict[str, Any]]) -> List[str]:
        """Extract common themes from reviews"""
        # Simple theme extraction based on common business review topics
        themes = []
        all_text = ' '.join([review.get('text', '').lower() for review in reviews])
        
        common_themes = {
            'service': ['service', 'staff', 'customer service', 'helpful'],
            'quality': ['quality', 'excellent', 'good', 'great'],
            'price': ['price', 'cost', 'expensive', 'affordable', 'value'],
            'location': ['location', 'parking', 'convenient', 'accessible'],
            'speed': ['fast', 'quick', 'slow', 'wait', 'time']
        }
        
        for theme, keywords in common_themes.items():
            if any(keyword in all_text for keyword in keywords):
                themes.append(theme)
                
        return themes[:5]  # Top 5 themes
    
    def _identify_strengths(self, reviews: List[Dict[str, Any]]) -> List[str]:
        """Identify business strengths from reviews"""
        strengths = []
        positive_reviews = [r for r in reviews if r.get('rating', 3) >= 4]
        
        if positive_reviews:
            strengths = [
                "High customer satisfaction",
                "Quality service delivery",
                "Professional staff",
                "Good value for money"
            ]
            
        return strengths[:3]
    
    def _identify_improvements(self, reviews: List[Dict[str, Any]]) -> List[str]:
        """Identify areas for improvement from reviews"""
        improvements = []
        negative_reviews = [r for r in reviews if r.get('rating', 3) <= 2]
        
        if negative_reviews:
            improvements = [
                "Improve response time to customer inquiries",
                "Enhance service consistency",
                "Consider pricing adjustments",
                "Upgrade facilities or equipment"
            ]
            
        return improvements[:3]
    
    def _generate_response_suggestions(self, reviews: List[Dict[str, Any]]) -> List[str]:
        """Generate suggestions for responding to reviews"""
        return [
            "Thank customers for positive feedback and highlight your commitment",
            "Address negative reviews professionally and offer solutions",
            "Use reviews to showcase improvements and changes made",
            "Encourage satisfied customers to leave more reviews"
        ]
    
    def _generate_business_insights(self, reviews: List[Dict[str, Any]]) -> List[str]:
        """Generate business insights from reviews"""
        return [
            "Customer feedback indicates strong service quality",
            "Reviews suggest opportunities for operational improvements",
            "Positive sentiment supports brand reputation growth",
            "Review volume indicates good customer engagement"
        ]
    
    def _calculate_recommendation_score(self, reviews: List[Dict[str, Any]]) -> float:
        """Calculate business recommendation score"""
        if not reviews:
            return 0.5
        
        ratings = [review.get('rating', 3) for review in reviews]
        avg_rating = sum(ratings) / len(ratings)
        return min(1.0, avg_rating / 5.0)
    
    def _fallback_review_analysis(self, reviews: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Fallback analysis when AI fails"""
        return {
            "basic_analysis": True,
            "review_count": len(reviews),
            "average_rating": sum(r.get('rating', 3) for r in reviews) / len(reviews) if reviews else 0,
            "note": "Basic analysis applied due to AI service unavailability"
        }
    
    def _generate_recommendations(self, user_id: str, search_history: List[str], preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate personalized recommendations"""
        # Mock recommendations based on preferences
        categories = preferences.get('preferred_categories', ['restaurants', 'services'])
        
        recommendations = []
        for i, category in enumerate(categories[:5]):
            recommendations.append({
                "business_id": f"rec_{category}_{i}",
                "name": f"Recommended {category.title()} Business {i+1}",
                "category": category,
                "relevance_score": 0.9 - (i * 0.1),
                "reason": f"Based on your interest in {category}",
                "confidence": 0.85
            })
            
        return recommendations
    
    def _fallback_recommendations(self) -> List[Dict[str, Any]]:
        """Fallback recommendations when AI fails"""
        return [
            {
                "business_id": "fallback_1",
                "name": "Popular Local Business",
                "category": "services",
                "relevance_score": 0.7,
                "reason": "Generally popular choice",
                "confidence": 0.5
            }
        ]
    
    def _enhance_results_ranking(self, query: str, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Enhance search results ranking with AI"""
        # Simple enhancement based on query relevance
        enhanced = []
        for result in results:
            relevance_boost = 0
            if query.lower() in result.get('name', '').lower():
                relevance_boost += 0.2
            if query.lower() in result.get('description', '').lower():
                relevance_boost += 0.1
                
            result['ai_relevance_score'] = result.get('rating', 0) + relevance_boost
            enhanced.append(result)
        
        # Sort by AI relevance score
        enhanced.sort(key=lambda x: x.get('ai_relevance_score', 0), reverse=True)
        return enhanced
    
    def _generate_search_suggestions(self, query: str) -> List[str]:
        """Generate search suggestions"""
        suggestions = [
            f"{query} near me",
            f"best {query}",
            f"{query} reviews",
            f"professional {query}",
            f"{query} services"
        ]
        return suggestions[:3]
    
    def _find_semantic_matches(self, query: str, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Find semantic matches for query"""
        # Simple semantic matching
        semantic_matches = []
        query_lower = query.lower()
        
        for result in results:
            tags = result.get('tags', [])
            if any(tag.lower() in query_lower or query_lower in tag.lower() for tag in tags):
                semantic_matches.append(result)
                
        return semantic_matches[:3]
    
    def _analyze_search_intent(self, query: str) -> str:
        """Analyze search intent"""
        query_lower = query.lower()
        
        if 'near me' in query_lower or 'local' in query_lower:
            return 'local_search'
        elif 'best' in query_lower or 'top' in query_lower:
            return 'quality_focused'
        elif 'cheap' in query_lower or 'affordable' in query_lower:
            return 'price_focused'
        else:
            return 'general_search'
    
    def _generate_result_insights(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate insights about search results"""
        if not results:
            return {"insight": "No results found"}
        
        avg_rating = sum(r.get('rating', 0) for r in results) / len(results)
        categories = list(set(r.get('category', 'Unknown') for r in results))
        
        return {
            "result_count": len(results),
            "average_rating": round(avg_rating, 2),
            "categories_found": categories[:5],
            "quality_insight": "High quality results" if avg_rating >= 4 else "Mixed quality results"
        }
    
    def _score_individual_lead(self, lead: Dict[str, Any]) -> Dict[str, Any]:
        """Score an individual lead"""
        base_score = 0.5
        
        # Score based on engagement
        if lead.get('phone_clicked'):
            base_score += 0.2
        if lead.get('website_visited'):
            base_score += 0.15
        if lead.get('form_submitted'):
            base_score += 0.3
        if lead.get('review_left'):
            base_score += 0.1
        
        # Business fit scoring
        if lead.get('category_match'):
            base_score += 0.1
        if lead.get('location_match'):
            base_score += 0.1
        
        score = min(1.0, base_score)
        
        # Categorize lead
        if score >= 0.8:
            category = "hot"
        elif score >= 0.6:
            category = "warm"
        else:
            category = "cold"
        
        lead['ai_score'] = score
        lead['lead_category'] = category
        lead['follow_up_priority'] = "high" if score >= 0.7 else "medium" if score >= 0.5 else "low"
        
        return lead
    
    def _generate_structured_content(self, content_type: str, topic: str, target_audience: str) -> Dict[str, Any]:
        """Generate structured content"""
        
        content_templates = {
            "blog_post": {
                "title": f"The Ultimate Guide to {topic} for {target_audience}",
                "content": f"Discover everything you need to know about {topic}. This comprehensive guide covers best practices, expert tips, and actionable strategies specifically tailored for {target_audience}.",
                "meta_description": f"Expert guide on {topic} for {target_audience}. Learn proven strategies and best practices.",
                "tags": [topic.lower(), target_audience.lower(), "guide", "tips"],
                "estimated_read_time": "8 minutes"
            },
            "event": {
                "title": f"{topic} Workshop for {target_audience}",
                "description": f"Join us for an interactive workshop focused on {topic}. Perfect for {target_audience} looking to enhance their knowledge and skills.",
                "duration": "2 hours",
                "format": "Workshop",
                "target_attendees": 50,
                "learning_objectives": [f"Understand key concepts of {topic}", f"Apply best practices in {target_audience} context"]
            },
            "community_post": {
                "title": f"Discussion: Best {topic} Strategies for {target_audience}",
                "content": f"Let's discuss the most effective {topic} strategies. Share your experiences and learn from other {target_audience} in our community.",
                "category": "discussion",
                "tags": [topic.lower(), "community", "discussion"]
            }
        }
        
        base_content = content_templates.get(content_type, {
            "title": f"{topic} Content for {target_audience}",
            "content": f"Quality content about {topic} tailored for {target_audience}."
        })
        
        base_content.update({
            "content_type": content_type,
            "topic": topic,
            "target_audience": target_audience,
            "generated_at": datetime.now().isoformat(),
            "ai_generated": True,
            "quality_score": 0.8
        })
        
        return base_content
    
    def _fallback_content(self, content_type: str, topic: str) -> Dict[str, Any]:
        """Fallback content when AI fails"""
        return {
            "content_type": content_type,
            "topic": topic,
            "title": f"Content about {topic}",
            "content": f"This is basic content about {topic}. Please check back later for enhanced AI-generated content.",
            "fallback": True,
            "note": "Basic content provided due to AI service unavailability"
        }

# Initialize the AI manager singleton
ai_manager = None

def get_ai_manager() -> DirectoryAIManager:
    """Get or create the AI manager instance"""
    global ai_manager
    if ai_manager is None:
        ai_manager = DirectoryAIManager()
    return ai_manager