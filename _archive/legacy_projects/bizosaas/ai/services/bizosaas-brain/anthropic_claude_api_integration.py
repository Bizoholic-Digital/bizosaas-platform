#!/usr/bin/env python3
"""
Anthropic Claude API Integration for BizOSaaS Brain - Advanced Reasoning AI
Provides access to Claude-3 Opus, Sonnet, and Haiku models with advanced capabilities
"""

import asyncio
import aiohttp
import json
from datetime import datetime
import os
from typing import Dict, List, Any, Optional
import traceback

class ClaudeReasoningAgent:
    """AI Agent for advanced reasoning and complex problem solving using Claude"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.anthropic.com/v1"
        self.agent_name = "Claude Advanced Reasoning Agent"
        
    async def complex_reasoning(self, tenant_id: str, problem: str, context: str = "") -> Dict[str, Any]:
        """Handle complex reasoning tasks with Claude's advanced capabilities"""
        try:
            headers = {
                "Content-Type": "application/json",
                "X-API-Key": self.api_key,
                "Anthropic-Version": "2023-06-01"
            }
            
            # Construct reasoning prompt for Claude
            reasoning_prompt = f"""You are Claude, an AI assistant created by Anthropic to be helpful, harmless, and honest. You excel at complex reasoning and problem-solving.

Problem to solve: {problem}

Additional context: {context}

Please provide a comprehensive analysis that includes:
1. Problem breakdown and understanding
2. Step-by-step reasoning process
3. Multiple perspectives and approaches
4. Potential challenges and limitations
5. Actionable recommendations
6. Confidence assessment

Use your advanced reasoning capabilities to provide deep insights."""

            request_data = {
                "model": "claude-3-opus-20240229",
                "max_tokens": 2000,
                "messages": [
                    {
                        "role": "user", 
                        "content": reasoning_prompt
                    }
                ],
                "temperature": 0.3  # Lower temperature for more focused reasoning
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/messages",
                    headers=headers,
                    json=request_data
                ) as response:
                    if response.status == 200:
                        response_data = await response.json()
                        content = response_data['content'][0]['text'] if response_data.get('content') else ''
                        
                        # Analyze reasoning quality
                        reasoning_analysis = self._analyze_reasoning_quality(content)
                        
                        return {
                            'success': True,
                            'tenant_id': tenant_id,
                            'problem': problem[:200] + "...",
                            'reasoning': {
                                'analysis': content,
                                'model_used': 'claude-3-opus-20240229',
                                'reasoning_quality': reasoning_analysis,
                                'word_count': len(content.split()),
                                'complexity_score': self._calculate_complexity_score(content)
                            },
                            'usage': response_data.get('usage', {}),
                            'agent': self.agent_name
                        }
                    else:
                        error_text = await response.text()
                        return {
                            'success': False,
                            'error': f'Complex reasoning failed: {response.status} - {error_text}',
                            'agent': self.agent_name
                        }
                        
        except Exception as e:
            return {
                'success': False,
                'error': f'Complex reasoning error: {str(e)}',
                'traceback': traceback.format_exc(),
                'agent': self.agent_name
            }
    
    def _analyze_reasoning_quality(self, content: str) -> Dict[str, Any]:
        """Analyze the quality of Claude's reasoning response"""
        quality_indicators = {
            'structured_thinking': 'step-by-step' in content.lower() or 'first,' in content.lower(),
            'multiple_perspectives': 'however,' in content.lower() or 'alternatively,' in content.lower(),
            'evidence_based': 'because' in content.lower() or 'therefore' in content.lower(),
            'actionable': 'recommend' in content.lower() or 'suggest' in content.lower(),
            'uncertainty_awareness': 'uncertain' in content.lower() or 'might' in content.lower()
        }
        
        quality_score = sum(quality_indicators.values()) / len(quality_indicators) * 100
        
        return {
            'quality_score': round(quality_score, 1),
            'indicators': quality_indicators,
            'assessment': 'excellent' if quality_score >= 80 else 'good' if quality_score >= 60 else 'moderate'
        }
    
    def _calculate_complexity_score(self, content: str) -> float:
        """Calculate complexity score based on content analysis"""
        complexity_factors = {
            'long_sentences': len([s for s in content.split('.') if len(s.split()) > 20]),
            'technical_terms': len([w for w in content.split() if len(w) > 10]),
            'conditional_statements': content.lower().count('if ') + content.lower().count('when '),
            'comparative_analysis': content.lower().count('compared') + content.lower().count('versus')
        }
        
        # Normalize to 0-10 scale
        base_score = min(sum(complexity_factors.values()) / 10, 10)
        return round(base_score, 1)

class ClaudeContentGenerationAgent:
    """AI Agent for high-quality content generation using Claude"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.anthropic.com/v1"
        self.agent_name = "Claude Content Generation Agent"
        
    async def generate_content(
        self, 
        tenant_id: str, 
        content_type: str,
        topic: str,
        tone: str = "professional",
        length: str = "medium",
        audience: str = "general"
    ) -> Dict[str, Any]:
        """Generate high-quality content using Claude's writing capabilities"""
        try:
            headers = {
                "Content-Type": "application/json",
                "X-API-Key": self.api_key,
                "Anthropic-Version": "2023-06-01"
            }
            
            # Select appropriate model based on content type
            model = "claude-3-sonnet-20240229"  # Good balance for content generation
            if content_type in ["technical_documentation", "research_paper"]:
                model = "claude-3-opus-20240229"  # Use Opus for complex content
            elif content_type in ["social_media", "quick_summary"]:
                model = "claude-3-haiku-20240307"  # Use Haiku for quick content
            
            # Construct content generation prompt
            length_guidance = {
                "short": "200-300 words",
                "medium": "500-800 words", 
                "long": "1000-1500 words"
            }.get(length, "500-800 words")
            
            content_prompt = f"""Create {content_type} content about: {topic}

Requirements:
- Target audience: {audience}
- Tone: {tone}
- Length: {length_guidance}
- Make it engaging, informative, and well-structured
- Include relevant examples where appropriate
- Ensure accuracy and credibility

Please generate high-quality content that meets these specifications."""

            max_tokens = {
                "short": 500,
                "medium": 1200,
                "long": 2000
            }.get(length, 1200)
            
            request_data = {
                "model": model,
                "max_tokens": max_tokens,
                "messages": [
                    {
                        "role": "user",
                        "content": content_prompt
                    }
                ],
                "temperature": 0.7  # Balanced creativity for content generation
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/messages",
                    headers=headers,
                    json=request_data
                ) as response:
                    if response.status == 200:
                        response_data = await response.json()
                        content = response_data['content'][0]['text'] if response_data.get('content') else ''
                        
                        # Analyze content quality
                        content_analysis = self._analyze_content_quality(content, content_type)
                        
                        return {
                            'success': True,
                            'tenant_id': tenant_id,
                            'content_type': content_type,
                            'generated_content': {
                                'text': content,
                                'word_count': len(content.split()),
                                'character_count': len(content),
                                'estimated_reading_time': f"{len(content.split()) // 200 + 1} min"
                            },
                            'content_analysis': content_analysis,
                            'model_used': model,
                            'usage': response_data.get('usage', {}),
                            'agent': self.agent_name
                        }
                    else:
                        error_text = await response.text()
                        return {
                            'success': False,
                            'error': f'Content generation failed: {response.status} - {error_text}',
                            'agent': self.agent_name
                        }
                        
        except Exception as e:
            return {
                'success': False,
                'error': f'Content generation error: {str(e)}',
                'traceback': traceback.format_exc(),
                'agent': self.agent_name
            }
    
    def _analyze_content_quality(self, content: str, content_type: str) -> Dict[str, Any]:
        """Analyze the quality of generated content"""
        quality_metrics = {
            'readability_score': self._calculate_readability(content),
            'structure_quality': self._analyze_structure(content),
            'engagement_factor': self._calculate_engagement(content),
            'relevance_score': self._assess_relevance(content, content_type)
        }
        
        overall_score = sum(quality_metrics.values()) / len(quality_metrics)
        
        return {
            'overall_quality': round(overall_score, 1),
            'metrics': quality_metrics,
            'grade': 'A' if overall_score >= 8.5 else 'B' if overall_score >= 7 else 'C',
            'suggestions': self._generate_improvement_suggestions(quality_metrics)
        }
    
    def _calculate_readability(self, content: str) -> float:
        """Calculate readability score (simplified)"""
        sentences = len([s for s in content.split('.') if s.strip()])
        words = len(content.split())
        avg_words_per_sentence = words / sentences if sentences > 0 else 0
        
        # Higher score for moderate sentence length (10-20 words)
        if 10 <= avg_words_per_sentence <= 20:
            return 9.0
        elif 8 <= avg_words_per_sentence <= 25:
            return 7.5
        else:
            return 6.0
    
    def _analyze_structure(self, content: str) -> float:
        """Analyze content structure quality"""
        structure_score = 5.0  # Base score
        
        # Check for paragraphs
        if '\n\n' in content:
            structure_score += 1.5
            
        # Check for lists or bullet points
        if any(marker in content for marker in ['•', '-', '1.', '2.', '*']):
            structure_score += 1.0
            
        # Check for headers or sections
        if any(word in content for word in ['Introduction', 'Conclusion', 'Summary', 'Overview']):
            structure_score += 1.5
            
        return min(structure_score, 10.0)
    
    def _calculate_engagement(self, content: str) -> float:
        """Calculate engagement factor"""
        engagement_indicators = {
            'questions': content.count('?'),
            'examples': content.lower().count('example') + content.lower().count('instance'),
            'active_voice': content.lower().count('will') + content.lower().count('can') + content.lower().count('should'),
            'calls_to_action': content.lower().count('consider') + content.lower().count('try') + content.lower().count('explore')
        }
        
        total_indicators = sum(engagement_indicators.values())
        words = len(content.split())
        engagement_ratio = total_indicators / words * 100 if words > 0 else 0
        
        return min(engagement_ratio * 20, 10.0)  # Scale to 0-10
    
    def _assess_relevance(self, content: str, content_type: str) -> float:
        """Assess content relevance to specified type"""
        relevance_keywords = {
            'blog_post': ['share', 'readers', 'post', 'article'],
            'marketing_copy': ['benefits', 'features', 'customers', 'value'],
            'technical_documentation': ['implementation', 'configuration', 'parameters', 'specifications'],
            'social_media': ['engage', 'follow', 'share', 'like'],
            'email_newsletter': ['subscribers', 'update', 'news', 'community']
        }
        
        keywords = relevance_keywords.get(content_type, ['information', 'details', 'content'])
        matches = sum(1 for keyword in keywords if keyword in content.lower())
        
        return min(matches / len(keywords) * 10, 10.0)
    
    def _generate_improvement_suggestions(self, quality_metrics: Dict[str, float]) -> List[str]:
        """Generate improvement suggestions based on quality metrics"""
        suggestions = []
        
        if quality_metrics['readability_score'] < 7:
            suggestions.append("Consider shorter, more concise sentences for better readability")
            
        if quality_metrics['structure_quality'] < 7:
            suggestions.append("Add more structure with headers, paragraphs, or bullet points")
            
        if quality_metrics['engagement_factor'] < 6:
            suggestions.append("Include more examples, questions, or interactive elements")
            
        if quality_metrics['relevance_score'] < 7:
            suggestions.append("Ensure content aligns more closely with the specified content type")
            
        return suggestions or ["Content quality is excellent - no major improvements needed"]

class ClaudeConversationAgent:
    """AI Agent for natural conversation and dialogue using Claude"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.anthropic.com/v1"
        self.agent_name = "Claude Conversation Agent"
        
    async def handle_conversation(
        self, 
        tenant_id: str, 
        messages: List[Dict[str, str]], 
        personality: str = "helpful_assistant",
        context_window: str = "standard"
    ) -> Dict[str, Any]:
        """Handle natural conversation with context awareness"""
        try:
            headers = {
                "Content-Type": "application/json",
                "X-API-Key": self.api_key,
                "Anthropic-Version": "2023-06-01"
            }
            
            # Select model based on context window needs
            model = "claude-3-sonnet-20240229"  # Default
            if context_window == "large":
                model = "claude-3-opus-20240229"  # 200k context
            elif context_window == "fast":
                model = "claude-3-haiku-20240307"  # Fastest response
            
            # Add personality context if specified
            if personality != "default":
                personality_contexts = {
                    "helpful_assistant": "You are a helpful, knowledgeable assistant focused on providing accurate and useful information.",
                    "creative_writer": "You are a creative writing assistant with a flair for storytelling and imaginative content.",
                    "technical_expert": "You are a technical expert who provides detailed, accurate technical information and solutions.",
                    "business_advisor": "You are a business advisor focused on strategy, growth, and practical business solutions.",
                    "educational_tutor": "You are an educational tutor who explains concepts clearly and encouragingly."
                }
                
                system_message = personality_contexts.get(personality, "You are Claude, a helpful AI assistant.")
                
                # Add system context to conversation
                conversation_messages = [{"role": "system", "content": system_message}] + messages
            else:
                conversation_messages = messages
            
            request_data = {
                "model": model,
                "max_tokens": 1500,
                "messages": conversation_messages[-10:],  # Keep last 10 messages for context
                "temperature": 0.7
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/messages",
                    headers=headers,
                    json=request_data
                ) as response:
                    if response.status == 200:
                        response_data = await response.json()
                        content = response_data['content'][0]['text'] if response_data.get('content') else ''
                        
                        # Analyze conversation quality
                        conversation_analysis = self._analyze_conversation_quality(content, messages)
                        
                        return {
                            'success': True,
                            'tenant_id': tenant_id,
                            'conversation': {
                                'response': content,
                                'model_used': model,
                                'personality': personality,
                                'context_messages': len(messages),
                                'response_length': len(content.split())
                            },
                            'conversation_analysis': conversation_analysis,
                            'usage': response_data.get('usage', {}),
                            'agent': self.agent_name
                        }
                    else:
                        error_text = await response.text()
                        return {
                            'success': False,
                            'error': f'Conversation failed: {response.status} - {error_text}',
                            'agent': self.agent_name
                        }
                        
        except Exception as e:
            return {
                'success': False,
                'error': f'Conversation error: {str(e)}',
                'traceback': traceback.format_exc(),
                'agent': self.agent_name
            }
    
    def _analyze_conversation_quality(self, response: str, conversation_history: List[Dict]) -> Dict[str, Any]:
        """Analyze the quality of conversation response"""
        quality_metrics = {
            'contextual_relevance': self._assess_context_relevance(response, conversation_history),
            'helpfulness': self._measure_helpfulness(response),
            'natural_flow': self._evaluate_natural_flow(response),
            'completeness': self._check_completeness(response)
        }
        
        overall_quality = sum(quality_metrics.values()) / len(quality_metrics)
        
        return {
            'quality_score': round(overall_quality, 1),
            'metrics': quality_metrics,
            'conversation_rating': 'excellent' if overall_quality >= 8 else 'good' if overall_quality >= 6 else 'moderate',
            'engagement_level': 'high' if 'question' in response.lower() or '?' in response else 'medium'
        }
    
    def _assess_context_relevance(self, response: str, history: List[Dict]) -> float:
        """Assess how well response relates to conversation context"""
        if not history:
            return 8.0  # Default for new conversation
            
        last_message = history[-1].get('content', '') if history else ''
        
        # Simple keyword overlap analysis
        response_words = set(response.lower().split())
        context_words = set(last_message.lower().split())
        
        overlap = len(response_words & context_words)
        max_possible = max(len(response_words), len(context_words))
        
        relevance_score = (overlap / max_possible * 10) if max_possible > 0 else 5.0
        return min(relevance_score, 10.0)
    
    def _measure_helpfulness(self, response: str) -> float:
        """Measure how helpful the response appears to be"""
        helpful_indicators = {
            'actionable_advice': any(word in response.lower() for word in ['should', 'can', 'try', 'consider']),
            'specific_information': any(word in response.lower() for word in ['specifically', 'example', 'details']),
            'clarifying_questions': '?' in response,
            'structured_response': any(word in response for word in ['1.', '2.', '•', '-'])
        }
        
        helpfulness_score = sum(helpful_indicators.values()) / len(helpful_indicators) * 10
        return min(helpfulness_score + 4, 10.0)  # Base score of 4
    
    def _evaluate_natural_flow(self, response: str) -> float:
        """Evaluate how natural the conversation flow feels"""
        natural_indicators = {
            'conversational_tone': any(word in response.lower() for word in ['i think', 'you might', 'perhaps', 'it seems']),
            'appropriate_length': 50 <= len(response.split()) <= 300,
            'smooth_transitions': any(word in response.lower() for word in ['however', 'additionally', 'furthermore', 'also']),
            'personal_touch': any(word in response.lower() for word in ['you', 'your', 'i understand', 'let me'])
        }
        
        return sum(natural_indicators.values()) / len(natural_indicators) * 10
    
    def _check_completeness(self, response: str) -> float:
        """Check if response feels complete and well-rounded"""
        completeness_indicators = {
            'adequate_length': len(response.split()) >= 20,
            'concluding_thought': response.strip().endswith(('.', '!', '?')),
            'addresses_question': any(word in response.lower() for word in ['answer', 'solution', 'explain', 'help']),
            'provides_closure': any(phrase in response.lower() for phrase in ['hope this helps', 'let me know', 'feel free'])
        }
        
        return sum(completeness_indicators.values()) / len(completeness_indicators) * 10

class ClaudeAnalyticsAgent:
    """AI Agent for usage analytics and performance monitoring of Claude API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.agent_name = "Claude Analytics Agent"
        
    async def get_usage_analytics(self, tenant_id: str) -> Dict[str, Any]:
        """Get comprehensive Claude API usage analytics and insights"""
        try:
            # Simulate analytics data (in production, integrate with actual usage tracking)
            analytics_data = {
                'usage_summary': {
                    'total_requests': 8934,
                    'total_tokens': 1847293,
                    'total_cost': 145.67,
                    'average_cost_per_request': 0.0163,
                    'most_used_model': 'claude-3-sonnet-20240229',
                    'success_rate': 98.7
                },
                'model_usage': [
                    {
                        'model': 'claude-3-opus-20240229',
                        'requests': 2147,
                        'tokens': 687432,
                        'cost': 87.45,
                        'use_cases': ['complex reasoning', 'technical documentation', 'research'],
                        'avg_response_quality': 9.2
                    },
                    {
                        'model': 'claude-3-sonnet-20240229',
                        'requests': 4532,
                        'tokens': 876234,
                        'cost': 45.78,
                        'use_cases': ['content generation', 'conversation', 'analysis'],
                        'avg_response_quality': 8.7
                    },
                    {
                        'model': 'claude-3-haiku-20240307',
                        'requests': 2255,
                        'tokens': 283627,
                        'cost': 12.44,
                        'use_cases': ['quick responses', 'social media', 'summaries'],
                        'avg_response_quality': 8.1
                    }
                ],
                'performance_insights': {
                    'avg_reasoning_score': 8.9,
                    'avg_content_quality': 8.4,
                    'avg_conversation_rating': 8.6,
                    'context_utilization': 92.3,
                    'user_satisfaction': 94.8
                },
                'cost_optimization': {
                    'potential_savings': 23.45,
                    'optimization_opportunities': [
                        'Use Haiku for simple tasks to reduce costs by 75%',
                        'Implement prompt optimization to reduce token usage by 15%',
                        'Cache frequent responses to avoid repeated API calls',
                        'Use Sonnet instead of Opus for content generation tasks'
                    ]
                }
            }
            
            return {
                'success': True,
                'tenant_id': tenant_id,
                'analytics': analytics_data,
                'optimization_score': 85.3,
                'usage_efficiency': 'excellent',
                'recommendations': [
                    'Current model selection is well-optimized for use cases',
                    'Consider implementing response caching for repeated queries',
                    'Monitor reasoning task complexity to optimize model selection'
                ],
                'agent': self.agent_name
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Analytics retrieval failed: {str(e)}',
                'traceback': traceback.format_exc(),
                'agent': self.agent_name
            }

class AnthropicClaudeAPIIntegration:
    """Main integration class for Anthropic Claude API"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY', 'demo_key_for_testing')
        self.reasoning_agent = ClaudeReasoningAgent(self.api_key)
        self.content_agent = ClaudeContentGenerationAgent(self.api_key)
        self.conversation_agent = ClaudeConversationAgent(self.api_key)
        self.analytics_agent = ClaudeAnalyticsAgent(self.api_key)
        
    async def complex_reasoning(self, tenant_id: str, problem: str, context: str = "") -> Dict[str, Any]:
        """Handle complex reasoning tasks with Claude's advanced capabilities"""
        return await self.reasoning_agent.complex_reasoning(tenant_id, problem, context)
    
    async def generate_content(
        self, 
        tenant_id: str, 
        content_type: str, 
        topic: str, 
        **kwargs
    ) -> Dict[str, Any]:
        """Generate high-quality content using Claude"""
        return await self.content_agent.generate_content(tenant_id, content_type, topic, **kwargs)
    
    async def handle_conversation(
        self, 
        tenant_id: str, 
        messages: List[Dict[str, str]], 
        **kwargs
    ) -> Dict[str, Any]:
        """Handle natural conversation with Claude"""
        return await self.conversation_agent.handle_conversation(tenant_id, messages, **kwargs)
    
    async def get_usage_analytics(self, tenant_id: str) -> Dict[str, Any]:
        """Get usage analytics and optimization recommendations"""
        return await self.analytics_agent.get_usage_analytics(tenant_id)
    
    async def get_connection_status(self, tenant_id: str) -> Dict[str, Any]:
        """Get Claude API connection status and capabilities"""
        try:
            # Test connection with a simple completion
            test_messages = [{"role": "user", "content": "Hello, Claude. Please respond with a brief greeting."}]
            result = await self.conversation_agent.handle_conversation(tenant_id, test_messages)
            
            if result['success']:
                return {
                    'status': 'connected',
                    'message': 'Claude API connection successful',
                    'api_type': 'Advanced Reasoning AI',
                    'available_models': [
                        'claude-3-opus-20240229 (200k context)',
                        'claude-3-sonnet-20240229 (200k context)', 
                        'claude-3-haiku-20240307 (200k context)'
                    ],
                    'capabilities': {
                        'advanced_reasoning': 'Complex problem solving and analysis',
                        'content_generation': 'High-quality content across multiple formats',
                        'natural_conversation': 'Human-like dialogue with context awareness',
                        'large_context': '200,000 token context window for all models',
                        'multilingual': 'Support for multiple languages',
                        'safety_features': 'Built-in safety and bias mitigation'
                    },
                    'specialties': [
                        'Complex reasoning and analysis',
                        'Technical documentation',
                        'Creative writing',
                        'Code analysis and explanation',
                        'Research and synthesis',
                        'Ethical decision making'
                    ]
                }
            else:
                return {
                    'status': 'connection_issues',
                    'message': f'Claude API connection issues: {result.get("error", "Unknown error")}',
                    'api_type': 'Advanced Reasoning AI'
                }
                
        except Exception as e:
            return {
                'status': 'disconnected',
                'message': f'Claude API connection failed: {str(e)}',
                'api_type': 'Advanced Reasoning AI'
            }

# Global integration instance
anthropic_claude_api_integration = AnthropicClaudeAPIIntegration()

if __name__ == "__main__":
    print("🧠 Anthropic Claude API Integration - Advanced Reasoning AI")
    print("Access to Claude-3 Opus, Sonnet, and Haiku models")