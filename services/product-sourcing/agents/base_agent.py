#!/usr/bin/env python3
"""
Base Agent for Product Sourcing System
Provides common functionality for all product sourcing agents
"""

import logging
import json
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

import aiohttp
import openai
from pydantic import BaseModel

logger = logging.getLogger(__name__)

@dataclass
class AgentResponse:
    """Standard response format for all agents"""
    success: bool
    data: Dict[str, Any]
    confidence: float
    processing_time: float
    agent_name: str
    timestamp: str
    errors: List[str] = None

class BaseProductSourcingAgent(ABC):
    """Base class for all product sourcing agents"""
    
    def __init__(self, name: str, openai_api_key: str = None):
        self.name = name
        self.openai_client = openai.OpenAI(api_key=openai_api_key) if openai_api_key else None
        self.logger = logging.getLogger(f"agent.{name}")
        
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        """Process input data and return agent response"""
        pass
    
    def _create_response(
        self, 
        success: bool, 
        data: Dict[str, Any], 
        confidence: float = 1.0,
        processing_time: float = 0.0,
        errors: List[str] = None
    ) -> AgentResponse:
        """Create standardized agent response"""
        return AgentResponse(
            success=success,
            data=data,
            confidence=confidence,
            processing_time=processing_time,
            agent_name=self.name,
            timestamp=datetime.now().isoformat(),
            errors=errors or []
        )
    
    async def _make_openai_request(
        self, 
        prompt: str, 
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> Optional[str]:
        """Make request to OpenAI API"""
        try:
            if not self.openai_client:
                self.logger.warning("OpenAI client not configured")
                return None
                
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            self.logger.error(f"OpenAI request failed: {e}")
            return None
    
    async def _make_http_request(
        self, 
        url: str, 
        method: str = "GET",
        headers: Dict[str, str] = None,
        data: Dict[str, Any] = None
    ) -> Optional[Dict]:
        """Make HTTP request"""
        try:
            async with aiohttp.ClientSession() as session:
                kwargs = {"headers": headers or {}}
                if data:
                    kwargs["json"] = data
                    
                async with session.request(method, url, **kwargs) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        self.logger.warning(f"HTTP request failed: {response.status}")
                        return None
                        
        except Exception as e:
            self.logger.error(f"HTTP request failed: {e}")
            return None
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text"""
        try:
            # Simple keyword extraction
            words = text.lower().split()
            # Filter out common words
            stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
            keywords = [word for word in words if word not in stop_words and len(word) > 3]
            return list(set(keywords))[:10]  # Return top 10 unique keywords
            
        except Exception as e:
            self.logger.error(f"Keyword extraction failed: {e}")
            return []
    
    def _calculate_sentiment_score(self, text: str) -> float:
        """Calculate sentiment score for text"""
        try:
            from textblob import TextBlob
            blob = TextBlob(text)
            # Return sentiment polarity (-1 to 1)
            return float(blob.sentiment.polarity)
            
        except Exception as e:
            self.logger.error(f"Sentiment analysis failed: {e}")
            return 0.0
    
    def _normalize_score(self, value: float, min_val: float, max_val: float) -> float:
        """Normalize value to 0-100 scale"""
        try:
            if max_val == min_val:
                return 50.0
            normalized = ((value - min_val) / (max_val - min_val)) * 100
            return max(0.0, min(100.0, normalized))
        except Exception as e:
            self.logger.error(f"Score normalization failed: {e}")
            return 0.0