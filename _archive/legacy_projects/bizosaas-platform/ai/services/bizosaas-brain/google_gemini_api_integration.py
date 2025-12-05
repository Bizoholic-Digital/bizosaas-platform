#!/usr/bin/env python3
"""
Google Gemini API Integration for Brain API Gateway
Implements 4-agent architecture for comprehensive Gemini AI capabilities

Agents:
1. GeminiContentGenerationAgent - Advanced text generation and creative content
2. GeminiConversationAgent - Multi-turn conversations and context handling  
3. GeminiVisionAgent - Image analysis and visual understanding
4. GeminiAnalyticsAgent - Performance monitoring and usage optimization

Features:
- Gemini Pro and Gemini Pro Vision model support
- Multi-modal AI (text + image processing)
- Advanced reasoning and creative generation
- Context-aware conversations
- Usage analytics and cost optimization
- Safety filtering and content moderation
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

class GeminiContentGenerationAgent:
    """Agent for advanced content generation using Google Gemini"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.session = None
        
    async def _ensure_session(self):
        """Ensure aiohttp session exists"""
        if not self.session:
            self.session = aiohttp.ClientSession()
            
    async def generate_content(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate content using Gemini Pro
        
        Args:
            request_data: {
                "prompt": str,
                "model": str (optional, defaults to "gemini-pro"),
                "temperature": float (optional),
                "max_output_tokens": int (optional),
                "safety_settings": list (optional)
            }
            
        Returns:
            Dict with generated content and metadata
        """
        await self._ensure_session()
        
        try:
            model = request_data.get("model", "gemini-pro")
            prompt = request_data.get("prompt", "")
            
            # Prepare request payload
            payload = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }],
                "generationConfig": {
                    "temperature": request_data.get("temperature", 0.7),
                    "maxOutputTokens": request_data.get("max_output_tokens", 2048)
                }
            }
            
            # Add safety settings if provided
            if "safety_settings" in request_data:
                payload["safetySettings"] = request_data["safety_settings"]
                
            url = f"{self.base_url}/models/{model}:generateContent"
            params = {"key": self.api_key}
            
            async with self.session.post(url, json=payload, params=params) as response:
                result = await response.json()
                
                if response.status == 200:
                    # Extract generated text
                    candidates = result.get("candidates", [])
                    if candidates and "content" in candidates[0]:
                        text = candidates[0]["content"]["parts"][0]["text"]
                        
                        return {
                            "status": "success",
                            "content": text,
                            "model_used": model,
                            "usage": result.get("usageMetadata", {}),
                            "safety_ratings": candidates[0].get("safetyRatings", []),
                            "timestamp": datetime.now().isoformat()
                        }
                        
                return {
                    "status": "error",
                    "error": result.get("error", "Content generation failed"),
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Gemini content generation error: {str(e)}")
            return {
                "status": "error", 
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            
    async def generate_creative_content(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate creative content with specialized prompting
        
        Args:
            request_data: {
                "content_type": str ("blog_post", "social_media", "email", "ad_copy"),
                "topic": str,
                "tone": str (optional),
                "target_audience": str (optional),
                "length": str (optional, "short", "medium", "long")
            }
            
        Returns:
            Dict with creative content
        """
        content_type = request_data.get("content_type", "blog_post")
        topic = request_data.get("topic", "")
        tone = request_data.get("tone", "professional")
        audience = request_data.get("target_audience", "general audience")
        length = request_data.get("length", "medium")
        
        # Create specialized prompts for different content types
        prompts = {
            "blog_post": f"Write a {length} {tone} blog post about {topic} for {audience}. Include an engaging title, introduction, main points, and conclusion.",
            "social_media": f"Create {tone} social media posts about {topic} for {audience}. Include hashtags and engaging copy.",
            "email": f"Write a {tone} email about {topic} for {audience}. Include subject line and compelling content.",
            "ad_copy": f"Create {tone} advertising copy about {topic} for {audience}. Focus on benefits and call-to-action."
        }
        
        prompt = prompts.get(content_type, prompts["blog_post"])
        
        return await self.generate_content({
            "prompt": prompt,
            "temperature": 0.8,  # Higher creativity
            "max_output_tokens": 2048
        })
        
    async def close(self):
        """Close the aiohttp session"""
        if self.session:
            await self.session.close()

class GeminiConversationAgent:
    """Agent for multi-turn conversations with Google Gemini"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.session = None
        self.conversation_history = {}
        
    async def _ensure_session(self):
        """Ensure aiohttp session exists"""
        if not self.session:
            self.session = aiohttp.ClientSession()
            
    async def start_conversation(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Start a new conversation session
        
        Args:
            request_data: {
                "conversation_id": str,
                "system_prompt": str (optional),
                "context": str (optional)
            }
            
        Returns:
            Dict with conversation initialization status
        """
        conversation_id = request_data.get("conversation_id", f"conv_{int(time.time())}")
        system_prompt = request_data.get("system_prompt", "You are a helpful AI assistant.")
        context = request_data.get("context", "")
        
        # Initialize conversation history
        self.conversation_history[conversation_id] = {
            "system_prompt": system_prompt,
            "context": context,
            "messages": [],
            "created_at": datetime.now().isoformat()
        }
        
        return {
            "status": "success",
            "conversation_id": conversation_id,
            "message": "Conversation started successfully",
            "timestamp": datetime.now().isoformat()
        }
        
    async def send_message(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send message in ongoing conversation
        
        Args:
            request_data: {
                "conversation_id": str,
                "message": str,
                "model": str (optional),
                "temperature": float (optional)
            }
            
        Returns:
            Dict with AI response and conversation context
        """
        await self._ensure_session()
        
        conversation_id = request_data.get("conversation_id")
        user_message = request_data.get("message", "")
        model = request_data.get("model", "gemini-pro")
        
        if conversation_id not in self.conversation_history:
            return {
                "status": "error",
                "error": "Conversation not found. Please start a conversation first.",
                "timestamp": datetime.now().isoformat()
            }
            
        try:
            conversation = self.conversation_history[conversation_id]
            
            # Add user message to history
            conversation["messages"].append({
                "role": "user",
                "content": user_message,
                "timestamp": datetime.now().isoformat()
            })
            
            # Prepare conversation context
            contents = []
            
            # Add system prompt and context
            if conversation["system_prompt"] or conversation["context"]:
                system_text = f"{conversation['system_prompt']}\n{conversation['context']}".strip()
                contents.append({"parts": [{"text": system_text}]})
                
            # Add conversation history
            for msg in conversation["messages"]:
                role = "user" if msg["role"] == "user" else "model"
                contents.append({"parts": [{"text": msg["content"]}], "role": role})
                
            payload = {
                "contents": contents,
                "generationConfig": {
                    "temperature": request_data.get("temperature", 0.7),
                    "maxOutputTokens": 2048
                }
            }
            
            url = f"{self.base_url}/models/{model}:generateContent"
            params = {"key": self.api_key}
            
            async with self.session.post(url, json=payload, params=params) as response:
                result = await response.json()
                
                if response.status == 200:
                    candidates = result.get("candidates", [])
                    if candidates and "content" in candidates[0]:
                        ai_response = candidates[0]["content"]["parts"][0]["text"]
                        
                        # Add AI response to history
                        conversation["messages"].append({
                            "role": "assistant",
                            "content": ai_response,
                            "timestamp": datetime.now().isoformat()
                        })
                        
                        return {
                            "status": "success",
                            "response": ai_response,
                            "conversation_id": conversation_id,
                            "message_count": len(conversation["messages"]),
                            "usage": result.get("usageMetadata", {}),
                            "timestamp": datetime.now().isoformat()
                        }
                        
                return {
                    "status": "error",
                    "error": result.get("error", "Conversation failed"),
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Gemini conversation error: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            
    async def get_conversation_history(self, conversation_id: str) -> Dict[str, Any]:
        """Get conversation history"""
        if conversation_id not in self.conversation_history:
            return {
                "status": "error",
                "error": "Conversation not found"
            }
            
        return {
            "status": "success",
            "conversation": self.conversation_history[conversation_id]
        }
        
    async def close(self):
        """Close the aiohttp session"""
        if self.session:
            await self.session.close()

class GeminiVisionAgent:
    """Agent for visual understanding using Gemini Pro Vision"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.session = None
        
    async def _ensure_session(self):
        """Ensure aiohttp session exists"""
        if not self.session:
            self.session = aiohttp.ClientSession()
            
    async def analyze_image(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze image using Gemini Pro Vision
        
        Args:
            request_data: {
                "image_data": str (base64 encoded),
                "prompt": str (optional, what to analyze),
                "mime_type": str (optional, defaults to "image/jpeg")
            }
            
        Returns:
            Dict with image analysis results
        """
        await self._ensure_session()
        
        try:
            image_data = request_data.get("image_data", "")
            prompt = request_data.get("prompt", "Describe this image in detail")
            mime_type = request_data.get("mime_type", "image/jpeg")
            
            payload = {
                "contents": [{
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": mime_type,
                                "data": image_data
                            }
                        }
                    ]
                }],
                "generationConfig": {
                    "temperature": 0.4,  # Lower temperature for accuracy
                    "maxOutputTokens": 2048
                }
            }
            
            url = f"{self.base_url}/models/gemini-pro-vision:generateContent"
            params = {"key": self.api_key}
            
            async with self.session.post(url, json=payload, params=params) as response:
                result = await response.json()
                
                if response.status == 200:
                    candidates = result.get("candidates", [])
                    if candidates and "content" in candidates[0]:
                        analysis = candidates[0]["content"]["parts"][0]["text"]
                        
                        return {
                            "status": "success",
                            "analysis": analysis,
                            "model_used": "gemini-pro-vision",
                            "usage": result.get("usageMetadata", {}),
                            "safety_ratings": candidates[0].get("safetyRatings", []),
                            "timestamp": datetime.now().isoformat()
                        }
                        
                return {
                    "status": "error",
                    "error": result.get("error", "Image analysis failed"),
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Gemini vision analysis error: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            
    async def extract_text_from_image(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract text from image (OCR functionality)
        
        Args:
            request_data: {
                "image_data": str (base64 encoded),
                "mime_type": str (optional)
            }
            
        Returns:
            Dict with extracted text
        """
        request_data["prompt"] = "Extract all text from this image. Provide the text exactly as it appears, maintaining formatting where possible."
        return await self.analyze_image(request_data)
        
    async def identify_objects(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Identify objects in image
        
        Args:
            request_data: {
                "image_data": str (base64 encoded),
                "mime_type": str (optional)
            }
            
        Returns:
            Dict with identified objects
        """
        request_data["prompt"] = "Identify and list all objects, people, animals, and notable features in this image. Provide a structured analysis."
        return await self.analyze_image(request_data)
        
    async def close(self):
        """Close the aiohttp session"""
        if self.session:
            await self.session.close()

class GeminiAnalyticsAgent:
    """Agent for Gemini API analytics and optimization"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.usage_data = []
        self.performance_metrics = {}
        
    async def track_api_usage(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Track API usage and performance
        
        Args:
            request_data: {
                "operation": str,
                "model": str,
                "tokens_used": int,
                "response_time": float,
                "status": str
            }
            
        Returns:
            Dict with usage tracking confirmation
        """
        usage_record = {
            "operation": request_data.get("operation"),
            "model": request_data.get("model"),
            "tokens_used": request_data.get("tokens_used", 0),
            "response_time": request_data.get("response_time", 0),
            "status": request_data.get("status"),
            "timestamp": datetime.now().isoformat()
        }
        
        self.usage_data.append(usage_record)
        
        return {
            "status": "success",
            "message": "Usage data tracked successfully",
            "total_records": len(self.usage_data)
        }
        
    async def get_usage_analytics(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get comprehensive usage analytics
        
        Args:
            request_data: {
                "time_period": str (optional, "last_24h", "last_7d", "last_30d"),
                "include_costs": bool (optional)
            }
            
        Returns:
            Dict with analytics data
        """
        time_period = request_data.get("time_period", "all_time")
        include_costs = request_data.get("include_costs", False)
        
        # Calculate basic metrics
        total_requests = len(self.usage_data)
        successful_requests = len([r for r in self.usage_data if r["status"] == "success"])
        failed_requests = total_requests - successful_requests
        
        # Model usage breakdown
        model_usage = {}
        total_tokens = 0
        total_response_time = 0
        
        for record in self.usage_data:
            model = record["model"]
            model_usage[model] = model_usage.get(model, 0) + 1
            total_tokens += record["tokens_used"]
            total_response_time += record["response_time"]
            
        avg_response_time = total_response_time / max(total_requests, 1)
        
        analytics = {
            "status": "success",
            "time_period": time_period,
            "total_requests": total_requests,
            "successful_requests": successful_requests,
            "failed_requests": failed_requests,
            "success_rate": (successful_requests / max(total_requests, 1)) * 100,
            "total_tokens_used": total_tokens,
            "average_response_time": avg_response_time,
            "model_usage_breakdown": model_usage,
            "timestamp": datetime.now().isoformat()
        }
        
        if include_costs:
            # Estimated costs (approximate Gemini pricing)
            estimated_cost = total_tokens * 0.000001  # $0.001 per 1K tokens (estimated)
            analytics["estimated_cost"] = f"${estimated_cost:.4f}"
            
        return analytics
        
    async def optimize_usage(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Provide usage optimization recommendations
        
        Returns:
            Dict with optimization suggestions
        """
        if not self.usage_data:
            return {
                "status": "info",
                "message": "No usage data available for optimization analysis"
            }
            
        # Analyze usage patterns
        model_performance = {}
        for record in self.usage_data:
            model = record["model"]
            if model not in model_performance:
                model_performance[model] = {
                    "requests": 0,
                    "total_tokens": 0,
                    "total_response_time": 0,
                    "failures": 0
                }
                
            model_performance[model]["requests"] += 1
            model_performance[model]["total_tokens"] += record["tokens_used"]
            model_performance[model]["total_response_time"] += record["response_time"]
            
            if record["status"] != "success":
                model_performance[model]["failures"] += 1
                
        recommendations = []
        
        for model, metrics in model_performance.items():
            avg_response_time = metrics["total_response_time"] / metrics["requests"]
            failure_rate = (metrics["failures"] / metrics["requests"]) * 100
            
            if avg_response_time > 5.0:
                recommendations.append(f"Consider reducing token limits for {model} to improve response times")
                
            if failure_rate > 10:
                recommendations.append(f"High failure rate for {model} ({failure_rate:.1f}%) - review API usage patterns")
                
        if not recommendations:
            recommendations.append("Your Gemini API usage is optimized. Continue monitoring for performance changes.")
            
        return {
            "status": "success",
            "recommendations": recommendations,
            "model_performance": model_performance,
            "timestamp": datetime.now().isoformat()
        }

# Factory function for creating Gemini API integrations
async def create_gemini_integration(api_key: str) -> Dict[str, Any]:
    """
    Create and return all Gemini agents
    
    Args:
        api_key: Google API key for Gemini access
        
    Returns:
        Dict containing all 4 specialized agents
    """
    agents = {
        "content_generation": GeminiContentGenerationAgent(api_key),
        "conversation": GeminiConversationAgent(api_key),
        "vision": GeminiVisionAgent(api_key),
        "analytics": GeminiAnalyticsAgent(api_key)
    }
    
    return {
        "status": "success",
        "message": "Google Gemini integration initialized successfully",
        "agents": agents,
        "capabilities": [
            "Advanced content generation",
            "Multi-turn conversations",
            "Visual understanding and OCR",
            "Image analysis and object detection",
            "Usage analytics and optimization",
            "Safety filtering and content moderation"
        ]
    }

# Main execution for testing
async def main():
    """Test the Gemini integration"""
    # Demo API key for testing
    demo_api_key = "AIzaSy_demo_gemini_key_12345"
    
    print("🧠 Initializing Google Gemini API Integration...")
    integration = await create_gemini_integration(demo_api_key)
    
    print(f"✅ Integration Status: {integration['status']}")
    print(f"📋 Capabilities: {', '.join(integration['capabilities'])}")
    
    # Close all agent sessions
    agents = integration.get("agents", {})
    for agent in agents.values():
        if hasattr(agent, 'close'):
            await agent.close()

if __name__ == "__main__":
    asyncio.run(main())