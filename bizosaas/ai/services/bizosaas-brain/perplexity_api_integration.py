#!/usr/bin/env python3
"""
Perplexity API Integration for Brain API Gateway
Implements 4-agent architecture for comprehensive Perplexity AI capabilities

Agents:
1. PerplexitySearchAgent - AI-powered search and web reasoning
2. PerplexityResearchAgent - Comprehensive research with citations
3. PerplexitySummarizationAgent - Content summarization and analysis
4. PerplexityAnalyticsAgent - Usage tracking and performance optimization

Features:
- Real-time web search with AI reasoning
- Comprehensive research with source citations
- Content summarization and fact-checking
- Multi-turn conversations with web knowledge
- Usage analytics and cost optimization
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
import aiohttp
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PerplexitySearchAgent:
    """Agent for AI-powered search using Perplexity"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.perplexity.ai"
        self.session = None
        
    async def _ensure_session(self):
        """Ensure aiohttp session exists"""
        if not self.session:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            self.session = aiohttp.ClientSession(headers=headers)
            
    async def search(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform AI-powered search with reasoning
        
        Args:
            request_data: {
                "query": str,
                "model": str (optional, defaults to "llama-3.1-sonar-small-128k-online"),
                "max_tokens": int (optional),
                "temperature": float (optional),
                "return_citations": bool (optional, default True),
                "return_images": bool (optional, default False)
            }
            
        Returns:
            Dict with search results and AI analysis
        """
        await self._ensure_session()
        
        try:
            query = request_data.get("query", "")
            if not query:
                return {
                    "status": "error",
                    "error": "Query is required",
                    "timestamp": datetime.now().isoformat()
                }
                
            payload = {
                "model": request_data.get("model", "llama-3.1-sonar-small-128k-online"),
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful AI assistant that provides accurate, well-researched answers with citations."
                    },
                    {
                        "role": "user", 
                        "content": query
                    }
                ],
                "max_tokens": request_data.get("max_tokens", 1024),
                "temperature": request_data.get("temperature", 0.2),
                "return_citations": request_data.get("return_citations", True),
                "return_images": request_data.get("return_images", False)
            }
            
            async with self.session.post(f"{self.base_url}/chat/completions", json=payload) as response:
                result = await response.json()
                
                if response.status == 200:
                    choice = result.get("choices", [{}])[0]
                    message = choice.get("message", {})
                    
                    return {
                        "status": "success",
                        "query": query,
                        "answer": message.get("content", ""),
                        "citations": result.get("citations", []),
                        "images": result.get("images", []),
                        "model_used": payload["model"],
                        "usage": result.get("usage", {}),
                        "timestamp": datetime.now().isoformat()
                    }
                    
                return {
                    "status": "error",
                    "error": result.get("error", {}).get("message", "Search failed"),
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Perplexity search error: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            
    async def realtime_search(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform real-time search with latest information
        
        Args:
            request_data: {
                "query": str,
                "focus": str (optional, "news", "academic", "general"),
                "time_range": str (optional, "last_24h", "last_week", "last_month")
            }
            
        Returns:
            Dict with real-time search results
        """
        query = request_data.get("query", "")
        focus = request_data.get("focus", "general")
        time_range = request_data.get("time_range", "")
        
        # Enhance query based on focus and time range
        enhanced_query = query
        if time_range:
            enhanced_query += f" (from {time_range})"
        if focus == "news":
            enhanced_query += " latest news updates"
        elif focus == "academic":
            enhanced_query += " research papers academic sources"
            
        return await self.search({
            "query": enhanced_query,
            "model": "llama-3.1-sonar-large-128k-online",
            "return_citations": True,
            "return_images": focus == "news"
        })
        
    async def fact_check(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fact-check statements using web search
        
        Args:
            request_data: {
                "statement": str,
                "context": str (optional)
            }
            
        Returns:
            Dict with fact-checking results
        """
        statement = request_data.get("statement", "")
        context = request_data.get("context", "")
        
        fact_check_query = f"Fact-check this statement: '{statement}'"
        if context:
            fact_check_query += f" Context: {context}"
            
        fact_check_query += ". Please verify the accuracy and provide sources."
        
        return await self.search({
            "query": fact_check_query,
            "model": "llama-3.1-sonar-large-128k-online",
            "temperature": 0.1,  # Lower temperature for accuracy
            "return_citations": True
        })
        
    async def close(self):
        """Close the aiohttp session"""
        if self.session:
            await self.session.close()

class PerplexityResearchAgent:
    """Agent for comprehensive research using Perplexity"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.search_agent = PerplexitySearchAgent(api_key)
        
    async def research_topic(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Conduct comprehensive research on a topic
        
        Args:
            request_data: {
                "topic": str,
                "depth": str ("basic", "intermediate", "comprehensive"),
                "focus_areas": List[str] (optional),
                "exclude_areas": List[str] (optional)
            }
            
        Returns:
            Dict with comprehensive research results
        """
        topic = request_data.get("topic", "")
        depth = request_data.get("depth", "intermediate")
        focus_areas = request_data.get("focus_areas", [])
        exclude_areas = request_data.get("exclude_areas", [])
        
        if not topic:
            return {
                "status": "error",
                "error": "Topic is required for research",
                "timestamp": datetime.now().isoformat()
            }
            
        # Build research queries based on depth
        research_queries = []
        
        if depth == "basic":
            research_queries = [
                f"What is {topic}? Provide a basic overview.",
                f"Key facts about {topic}",
                f"Current status of {topic}"
            ]
        elif depth == "intermediate":
            research_queries = [
                f"Comprehensive overview of {topic}",
                f"Recent developments in {topic}",
                f"Key players and stakeholders in {topic}",
                f"Challenges and opportunities in {topic}"
            ]
        else:  # comprehensive
            research_queries = [
                f"Detailed analysis of {topic}",
                f"Historical context and evolution of {topic}",
                f"Current market analysis of {topic}",
                f"Future trends and predictions for {topic}",
                f"Expert opinions on {topic}",
                f"Case studies related to {topic}"
            ]
            
        # Add focus areas if specified
        if focus_areas:
            for area in focus_areas:
                research_queries.append(f"{topic} specifically related to {area}")
                
        # Exclude areas if specified
        exclude_filter = ""
        if exclude_areas:
            exclude_filter = f" (exclude information about: {', '.join(exclude_areas)})"
            
        research_results = []
        
        for query in research_queries:
            enhanced_query = query + exclude_filter
            result = await self.search_agent.search({
                "query": enhanced_query,
                "model": "llama-3.1-sonar-large-128k-online",
                "max_tokens": 1500,
                "return_citations": True
            })
            
            if result["status"] == "success":
                research_results.append({
                    "query": query,
                    "answer": result["answer"],
                    "citations": result["citations"]
                })
                
        return {
            "status": "success",
            "topic": topic,
            "depth": depth,
            "research_sections": research_results,
            "total_sections": len(research_results),
            "focus_areas": focus_areas,
            "timestamp": datetime.now().isoformat()
        }
        
    async def competitive_analysis(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Conduct competitive analysis research
        
        Args:
            request_data: {
                "company_or_product": str,
                "industry": str (optional),
                "competitors": List[str] (optional, will discover if not provided)
            }
            
        Returns:
            Dict with competitive analysis
        """
        subject = request_data.get("company_or_product", "")
        industry = request_data.get("industry", "")
        known_competitors = request_data.get("competitors", [])
        
        analysis_queries = [
            f"Market analysis of {subject} in {industry}" if industry else f"Market analysis of {subject}",
            f"Main competitors of {subject}",
            f"Competitive advantages and disadvantages of {subject}",
            f"Market position of {subject}",
            f"SWOT analysis of {subject}"
        ]
        
        # Add competitor-specific queries
        if known_competitors:
            for competitor in known_competitors:
                analysis_queries.append(f"Compare {subject} vs {competitor}")
                
        competitive_results = []
        
        for query in analysis_queries:
            result = await self.search_agent.search({
                "query": query,
                "model": "llama-3.1-sonar-large-128k-online",
                "max_tokens": 1200,
                "return_citations": True
            })
            
            if result["status"] == "success":
                competitive_results.append({
                    "analysis_type": query,
                    "findings": result["answer"],
                    "sources": result["citations"]
                })
                
        return {
            "status": "success",
            "subject": subject,
            "industry": industry,
            "competitive_analysis": competitive_results,
            "total_analyses": len(competitive_results),
            "timestamp": datetime.now().isoformat()
        }
        
    async def trend_analysis(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze trends in a specific domain
        
        Args:
            request_data: {
                "domain": str,
                "time_period": str (optional, "current", "emerging", "future"),
                "geographic_focus": str (optional)
            }
            
        Returns:
            Dict with trend analysis
        """
        domain = request_data.get("domain", "")
        time_period = request_data.get("time_period", "current")
        geographic_focus = request_data.get("geographic_focus", "")
        
        trend_queries = []
        
        if time_period == "current":
            trend_queries = [
                f"Current trends in {domain}",
                f"What's happening now in {domain}",
                f"Latest developments in {domain}"
            ]
        elif time_period == "emerging":
            trend_queries = [
                f"Emerging trends in {domain}",
                f"New developments in {domain}",
                f"Rising opportunities in {domain}"
            ]
        else:  # future
            trend_queries = [
                f"Future predictions for {domain}",
                f"Expected trends in {domain}",
                f"What experts predict for {domain}"
            ]
            
        if geographic_focus:
            trend_queries = [q + f" in {geographic_focus}" for q in trend_queries]
            
        trend_results = []
        
        for query in trend_queries:
            result = await self.search_agent.search({
                "query": query,
                "model": "llama-3.1-sonar-large-128k-online",
                "max_tokens": 1000,
                "return_citations": True
            })
            
            if result["status"] == "success":
                trend_results.append({
                    "trend_category": query,
                    "analysis": result["answer"],
                    "sources": result["citations"]
                })
                
        return {
            "status": "success",
            "domain": domain,
            "time_period": time_period,
            "geographic_focus": geographic_focus,
            "trend_analysis": trend_results,
            "total_trends": len(trend_results),
            "timestamp": datetime.now().isoformat()
        }
        
    async def close(self):
        """Close the search agent session"""
        await self.search_agent.close()

class PerplexitySummarizationAgent:
    """Agent for content summarization using Perplexity"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.search_agent = PerplexitySearchAgent(api_key)
        
    async def summarize_url(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Summarize content from a URL
        
        Args:
            request_data: {
                "url": str,
                "summary_length": str ("short", "medium", "long"),
                "focus": str (optional, what to focus on)
            }
            
        Returns:
            Dict with content summary
        """
        url = request_data.get("url", "")
        summary_length = request_data.get("summary_length", "medium")
        focus = request_data.get("focus", "")
        
        if not url:
            return {
                "status": "error",
                "error": "URL is required",
                "timestamp": datetime.now().isoformat()
            }
            
        length_instructions = {
            "short": "Provide a brief 2-3 sentence summary",
            "medium": "Provide a comprehensive paragraph summary", 
            "long": "Provide a detailed summary with key points"
        }
        
        query = f"Summarize the content from {url}. {length_instructions.get(summary_length, '')}"
        if focus:
            query += f" Focus specifically on {focus}."
            
        return await self.search_agent.search({
            "query": query,
            "model": "llama-3.1-sonar-large-128k-online",
            "max_tokens": 800 if summary_length == "long" else 400,
            "return_citations": True
        })
        
    async def summarize_multiple_sources(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Summarize and synthesize information from multiple sources
        
        Args:
            request_data: {
                "sources": List[str] (URLs or topics),
                "synthesis_goal": str (what to achieve from synthesis),
                "format": str (optional, "bullet_points", "narrative", "comparison")
            }
            
        Returns:
            Dict with synthesized summary
        """
        sources = request_data.get("sources", [])
        synthesis_goal = request_data.get("synthesis_goal", "")
        output_format = request_data.get("format", "narrative")
        
        if not sources:
            return {
                "status": "error",
                "error": "At least one source is required",
                "timestamp": datetime.now().isoformat()
            }
            
        format_instructions = {
            "bullet_points": "Format the summary as clear bullet points",
            "narrative": "Write a flowing narrative summary",
            "comparison": "Structure as a comparison highlighting similarities and differences"
        }
        
        sources_text = ", ".join(sources)
        query = f"Analyze and synthesize information from these sources: {sources_text}. "
        
        if synthesis_goal:
            query += f"Goal: {synthesis_goal}. "
            
        query += format_instructions.get(output_format, "")
        
        return await self.search_agent.search({
            "query": query,
            "model": "llama-3.1-sonar-large-128k-online", 
            "max_tokens": 1200,
            "return_citations": True
        })
        
    async def extract_key_insights(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract key insights from research or content
        
        Args:
            request_data: {
                "topic": str,
                "insight_type": str ("market_insights", "technical_insights", "strategic_insights"),
                "audience": str (optional, target audience)
            }
            
        Returns:
            Dict with key insights
        """
        topic = request_data.get("topic", "")
        insight_type = request_data.get("insight_type", "market_insights")
        audience = request_data.get("audience", "business professionals")
        
        insight_prompts = {
            "market_insights": f"What are the key market insights about {topic} that {audience} should know?",
            "technical_insights": f"What are the important technical insights and innovations in {topic}?",
            "strategic_insights": f"What strategic insights and recommendations emerge from current {topic} analysis?"
        }
        
        query = insight_prompts.get(insight_type, insight_prompts["market_insights"])
        query += " Provide actionable insights with supporting evidence."
        
        return await self.search_agent.search({
            "query": query,
            "model": "llama-3.1-sonar-large-128k-online",
            "max_tokens": 1000,
            "return_citations": True
        })
        
    async def close(self):
        """Close the search agent session"""
        await self.search_agent.close()

class PerplexityAnalyticsAgent:
    """Agent for Perplexity API analytics and optimization"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.usage_data = []
        self.query_performance = {}
        
    async def track_query_usage(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Track query usage and performance
        
        Args:
            request_data: {
                "query": str,
                "model": str,
                "response_time": float,
                "tokens_used": int,
                "citations_count": int,
                "status": str
            }
            
        Returns:
            Dict with usage tracking confirmation
        """
        usage_record = {
            "query": request_data.get("query", ""),
            "model": request_data.get("model", ""),
            "response_time": request_data.get("response_time", 0),
            "tokens_used": request_data.get("tokens_used", 0),
            "citations_count": request_data.get("citations_count", 0),
            "status": request_data.get("status", ""),
            "timestamp": datetime.now().isoformat()
        }
        
        self.usage_data.append(usage_record)
        
        return {
            "status": "success",
            "message": "Query usage tracked successfully",
            "total_queries": len(self.usage_data)
        }
        
    async def get_usage_analytics(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get comprehensive usage analytics
        
        Args:
            request_data: {
                "time_period": str (optional),
                "include_costs": bool (optional)
            }
            
        Returns:
            Dict with analytics data
        """
        if not self.usage_data:
            return {
                "status": "info",
                "message": "No usage data available",
                "timestamp": datetime.now().isoformat()
            }
            
        # Calculate basic metrics
        total_queries = len(self.usage_data)
        successful_queries = len([r for r in self.usage_data if r["status"] == "success"])
        
        # Model usage breakdown
        model_usage = {}
        total_tokens = 0
        total_response_time = 0
        total_citations = 0
        
        for record in self.usage_data:
            model = record["model"]
            model_usage[model] = model_usage.get(model, 0) + 1
            total_tokens += record["tokens_used"]
            total_response_time += record["response_time"]
            total_citations += record["citations_count"]
            
        avg_response_time = total_response_time / max(total_queries, 1)
        avg_citations = total_citations / max(total_queries, 1)
        
        analytics = {
            "status": "success",
            "total_queries": total_queries,
            "successful_queries": successful_queries,
            "success_rate": (successful_queries / max(total_queries, 1)) * 100,
            "total_tokens_used": total_tokens,
            "average_response_time": avg_response_time,
            "average_citations_per_query": avg_citations,
            "model_usage_breakdown": model_usage,
            "timestamp": datetime.now().isoformat()
        }
        
        if request_data.get("include_costs", False):
            # Estimated costs (Perplexity pricing approximate)
            estimated_cost = total_tokens * 0.002 / 1000  # Estimated $0.002 per 1K tokens
            analytics["estimated_cost"] = f"${estimated_cost:.4f}"
            
        return analytics
        
    async def optimize_query_performance(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Provide query optimization recommendations
        
        Returns:
            Dict with optimization suggestions
        """
        if not self.usage_data:
            return {
                "status": "info",
                "message": "No usage data available for optimization analysis"
            }
            
        # Analyze query patterns
        model_performance = {}
        query_patterns = {}
        
        for record in self.usage_data:
            model = record["model"]
            query_length = len(record["query"].split())
            
            if model not in model_performance:
                model_performance[model] = {
                    "queries": 0,
                    "avg_response_time": 0,
                    "avg_citations": 0,
                    "failure_rate": 0
                }
                
            model_performance[model]["queries"] += 1
            model_performance[model]["avg_response_time"] += record["response_time"]
            model_performance[model]["avg_citations"] += record["citations_count"]
            
            if record["status"] != "success":
                model_performance[model]["failure_rate"] += 1
                
            # Track query length patterns
            length_category = "short" if query_length < 10 else "medium" if query_length < 25 else "long"
            if length_category not in query_patterns:
                query_patterns[length_category] = {"count": 0, "avg_response_time": 0}
            query_patterns[length_category]["count"] += 1
            query_patterns[length_category]["avg_response_time"] += record["response_time"]
            
        # Calculate averages and generate recommendations
        recommendations = []
        
        for model, metrics in model_performance.items():
            if metrics["queries"] > 0:
                avg_time = metrics["avg_response_time"] / metrics["queries"]
                avg_citations = metrics["avg_citations"] / metrics["queries"]
                failure_rate = (metrics["failure_rate"] / metrics["queries"]) * 100
                
                if avg_time > 8.0:
                    recommendations.append(f"Consider using faster model alternatives to {model} (avg response: {avg_time:.1f}s)")
                    
                if avg_citations < 2:
                    recommendations.append(f"Queries using {model} have low citation counts - consider more specific queries")
                    
                if failure_rate > 10:
                    recommendations.append(f"High failure rate for {model} ({failure_rate:.1f}%) - review query formatting")
                    
        # Query length recommendations
        for length, data in query_patterns.items():
            if data["count"] > 0:
                avg_time = data["avg_response_time"] / data["count"]
                if length == "long" and avg_time > 10:
                    recommendations.append("Long queries have high response times - consider breaking them into shorter, focused queries")
                    
        if not recommendations:
            recommendations.append("Your Perplexity API usage is well optimized. Continue monitoring for performance changes.")
            
        return {
            "status": "success",
            "recommendations": recommendations,
            "model_performance": {
                model: {
                    "queries": metrics["queries"],
                    "avg_response_time": metrics["avg_response_time"] / max(metrics["queries"], 1),
                    "avg_citations": metrics["avg_citations"] / max(metrics["queries"], 1),
                    "failure_rate": (metrics["failure_rate"] / max(metrics["queries"], 1)) * 100
                }
                for model, metrics in model_performance.items()
            },
            "query_patterns": {
                category: {
                    "count": data["count"],
                    "avg_response_time": data["avg_response_time"] / max(data["count"], 1)
                }
                for category, data in query_patterns.items()
            },
            "timestamp": datetime.now().isoformat()
        }

# Factory function for creating Perplexity API integrations
async def create_perplexity_integration(api_key: str) -> Dict[str, Any]:
    """
    Create and return all Perplexity agents
    
    Args:
        api_key: Perplexity API key
        
    Returns:
        Dict containing all 4 specialized agents
    """
    agents = {
        "search": PerplexitySearchAgent(api_key),
        "research": PerplexityResearchAgent(api_key),
        "summarization": PerplexitySummarizationAgent(api_key),
        "analytics": PerplexityAnalyticsAgent(api_key)
    }
    
    return {
        "status": "success",
        "message": "Perplexity integration initialized successfully",
        "agents": agents,
        "capabilities": [
            "Real-time web search with AI reasoning",
            "Comprehensive research with source citations",
            "Content summarization and synthesis",
            "Fact-checking and verification", 
            "Competitive analysis and trend research",
            "Multi-source information synthesis",
            "Usage analytics and query optimization"
        ]
    }

# Main execution for testing
async def main():
    """Test the Perplexity integration"""
    # Demo API key for testing
    demo_api_key = "pplx-demo_api_key_12345"
    
    print("🔍 Initializing Perplexity API Integration...")
    integration = await create_perplexity_integration(demo_api_key)
    
    print(f"✅ Integration Status: {integration['status']}")
    print(f"📋 Capabilities: {', '.join(integration['capabilities'])}")
    
    # Close all agent sessions
    agents = integration.get("agents", {})
    for agent in agents.values():
        if hasattr(agent, 'close'):
            await agent.close()

if __name__ == "__main__":
    asyncio.run(main())