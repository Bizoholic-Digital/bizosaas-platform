"""
News Sentiment Agent - Real-time news and social media sentiment analysis
"""

from typing import Dict, Any, List
from datetime import datetime, timedelta
from crewai import Agent
from langchain.tools import Tool
import structlog
import re

from agents.base_agent import BaseTradingAgent
from core.config import get_settings

logger = structlog.get_logger(__name__)
settings = get_settings()


class NewsSentimentAgent(BaseTradingAgent):
    """AI agent specialized in news and social media sentiment analysis"""

    def __init__(self):
        super().__init__(
            agent_id="news_sentiment",
            name="News Sentiment Analyzer",
            description="Real-time news and social media sentiment analysis for trading decisions"
        )

    def _create_agent(self) -> Agent:
        """Create the News Sentiment CrewAI agent"""
        return Agent(
            role="Senior Sentiment Analyst",
            goal="Analyze news sentiment, social media trends, and market-moving events to provide sentiment-based trading insights and early warning signals",
            backstory="""You are an expert in behavioral finance and sentiment analysis with extensive
            experience in analyzing news, social media, and market psychology. You have developed
            proprietary models for sentiment analysis that have successfully predicted market movements
            based on news flow and social sentiment. Your expertise includes NLP, social media analytics,
            and understanding how information flows impact financial markets.""",
            verbose=True,
            allow_delegation=False,
            tools=self.tools,
            max_iter=3,
            memory=True
        )

    def _create_tools(self) -> List[Tool]:
        """Create specialized tools for sentiment analysis"""
        base_tools = self._create_base_tools()

        specialized_tools = [
            Tool(
                name="analyze_news_sentiment",
                description="Analyze sentiment from recent news articles",
                func=self._analyze_news_sentiment
            ),
            Tool(
                name="analyze_social_media_sentiment",
                description="Analyze sentiment from social media platforms",
                func=self._analyze_social_media_sentiment
            ),
            Tool(
                name="detect_breaking_news",
                description="Detect breaking news and market-moving events",
                func=self._detect_breaking_news
            ),
            Tool(
                name="analyze_analyst_sentiment",
                description="Analyze sentiment from analyst reports and upgrades/downgrades",
                func=self._analyze_analyst_sentiment
            ),
            Tool(
                name="calculate_sentiment_momentum",
                description="Calculate sentiment momentum and trend changes",
                func=self._calculate_sentiment_momentum
            ),
            Tool(
                name="identify_sentiment_extremes",
                description="Identify extreme sentiment levels that may signal reversals",
                func=self._identify_sentiment_extremes
            )
        ]

        return base_tools + specialized_tools

    async def analyze(self, symbol: str, timeframe: str = "24h", **kwargs) -> Dict[str, Any]:
        """Perform comprehensive sentiment analysis"""
        try:
            logger.info("Starting sentiment analysis", symbol=symbol, timeframe=timeframe)

            # Get market data for context
            quote = await self._get_market_quote(symbol)

            # Perform sentiment analysis
            news_sentiment = self._analyze_news_sentiment(symbol, timeframe)
            social_sentiment = self._analyze_social_media_sentiment(symbol, timeframe)
            analyst_sentiment = self._analyze_analyst_sentiment(symbol)
            breaking_news = self._detect_breaking_news(symbol)
            sentiment_momentum = self._calculate_sentiment_momentum(symbol)
            sentiment_extremes = self._identify_sentiment_extremes(symbol)

            # Generate overall sentiment score and recommendation
            sentiment_analysis = self._generate_sentiment_recommendation(
                news_sentiment, social_sentiment, analyst_sentiment,
                sentiment_momentum, sentiment_extremes
            )

            analysis_result = {
                "agent_id": self.agent_id,
                "symbol": symbol,
                "timeframe": timeframe,
                "timestamp": datetime.now().isoformat(),
                "current_price": quote.get("price", 0),
                "sentiment_score": sentiment_analysis["overall_score"],
                "sentiment_label": sentiment_analysis["label"],
                "confidence": sentiment_analysis["confidence"],
                "recommendation": sentiment_analysis["recommendation"],
                "sentiment_breakdown": {
                    "news_sentiment": news_sentiment,
                    "social_media_sentiment": social_sentiment,
                    "analyst_sentiment": analyst_sentiment,
                    "sentiment_momentum": sentiment_momentum
                },
                "breaking_news": breaking_news,
                "sentiment_extremes": sentiment_extremes,
                "key_topics": sentiment_analysis.get("key_topics", []),
                "sentiment_trend": sentiment_analysis.get("trend", {}),
                "impact_prediction": sentiment_analysis.get("impact_prediction", {}),
                "reasoning": sentiment_analysis.get("reasoning", []),
                "risk_factors": sentiment_analysis.get("risk_factors", [])
            }

            logger.info("Sentiment analysis completed", symbol=symbol,
                       sentiment_score=sentiment_analysis["overall_score"])
            return analysis_result

        except Exception as e:
            logger.error("Error in sentiment analysis", symbol=symbol, error=str(e))
            return {"error": f"Sentiment analysis failed: {str(e)}"}

    def _analyze_news_sentiment(self, symbol: str, timeframe: str) -> Dict[str, Any]:
        """Analyze sentiment from recent news articles"""
        # Mock news sentiment analysis - in production, integrate with news APIs

        mock_articles = [
            {
                "headline": f"{symbol} reports strong Q4 earnings, beats expectations",
                "source": "Reuters",
                "sentiment_score": 0.85,
                "impact_score": 0.9,
                "published_at": "2024-01-15T14:30:00Z"
            },
            {
                "headline": f"Analysts upgrade {symbol} price target on strong fundamentals",
                "source": "Bloomberg",
                "sentiment_score": 0.72,
                "impact_score": 0.7,
                "published_at": "2024-01-15T13:45:00Z"
            },
            {
                "headline": f"Market volatility concerns weigh on {symbol} outlook",
                "source": "Yahoo Finance",
                "sentiment_score": -0.35,
                "impact_score": 0.5,
                "published_at": "2024-01-15T12:15:00Z"
            }
        ]

        # Calculate weighted sentiment
        total_weight = sum(article["impact_score"] for article in mock_articles)
        weighted_sentiment = sum(
            article["sentiment_score"] * article["impact_score"]
            for article in mock_articles
        ) / total_weight if total_weight > 0 else 0

        sentiment_distribution = {
            "positive": len([a for a in mock_articles if a["sentiment_score"] > 0.1]),
            "neutral": len([a for a in mock_articles if -0.1 <= a["sentiment_score"] <= 0.1]),
            "negative": len([a for a in mock_articles if a["sentiment_score"] < -0.1])
        }

        return {
            "articles_analyzed": len(mock_articles),
            "avg_sentiment": weighted_sentiment,
            "sentiment_distribution": sentiment_distribution,
            "key_articles": mock_articles[:3],
            "sentiment_sources": ["Reuters", "Bloomberg", "Yahoo Finance"],
            "sentiment_strength": "strong" if abs(weighted_sentiment) > 0.6 else "moderate" if abs(weighted_sentiment) > 0.3 else "weak"
        }

    def _analyze_social_media_sentiment(self, symbol: str, timeframe: str) -> Dict[str, Any]:
        """Analyze sentiment from social media platforms"""
        # Mock social media sentiment analysis

        platform_data = {
            "twitter": {
                "mentions": 1547,
                "sentiment_score": 0.64,
                "trending_hashtags": [f"#{symbol}", f"#{symbol}earnings", f"#{symbol}moon"],
                "influencer_sentiment": 0.71,
                "volume_trend": "increasing"
            },
            "reddit": {
                "mentions": 892,
                "sentiment_score": 0.58,
                "popular_threads": [
                    f"{symbol} DD: Why this is undervalued",
                    f"{symbol} earnings play discussion"
                ],
                "comment_sentiment": 0.62,
                "upvote_ratio": 0.78
            },
            "stocktwits": {
                "mentions": 234,
                "bullish_ratio": 0.73,
                "bearish_ratio": 0.27,
                "sentiment_score": 0.46,  # (bullish_ratio - bearish_ratio)
                "message_volume": "high"
            }
        }

        # Calculate overall social sentiment
        social_sentiment_score = (
            platform_data["twitter"]["sentiment_score"] * 0.5 +
            platform_data["reddit"]["sentiment_score"] * 0.3 +
            platform_data["stocktwits"]["sentiment_score"] * 0.2
        )

        total_mentions = sum(data.get("mentions", 0) for data in platform_data.values())

        return {
            "total_mentions": total_mentions,
            "avg_sentiment": social_sentiment_score,
            "platform_breakdown": platform_data,
            "sentiment_momentum": "positive" if social_sentiment_score > 0.1 else "negative" if social_sentiment_score < -0.1 else "neutral",
            "viral_potential": "high" if total_mentions > 2000 else "moderate" if total_mentions > 500 else "low",
            "key_themes": [
                "earnings_optimism",
                "technical_breakout",
                "institutional_buying"
            ]
        }

    def _analyze_analyst_sentiment(self, symbol: str) -> Dict[str, Any]:
        """Analyze sentiment from analyst reports"""
        # Mock analyst sentiment analysis

        analyst_data = {
            "recent_ratings": [
                {"analyst": "Goldman Sachs", "rating": "Buy", "price_target": 200.0, "date": "2024-01-12"},
                {"analyst": "Morgan Stanley", "rating": "Overweight", "price_target": 195.0, "date": "2024-01-10"},
                {"analyst": "JP Morgan", "rating": "Hold", "price_target": 180.0, "date": "2024-01-08"}
            ],
            "rating_changes_30d": {
                "upgrades": 2,
                "downgrades": 0,
                "initiations": 1,
                "reiterations": 3
            },
            "price_target_changes": {
                "increases": 3,
                "decreases": 0,
                "average_target": 191.7,
                "target_change_avg": 5.2
            }
        }

        # Calculate analyst sentiment score
        rating_scores = {"Strong Buy": 1.0, "Buy": 0.8, "Overweight": 0.6, "Hold": 0.0,
                        "Underweight": -0.6, "Sell": -0.8, "Strong Sell": -1.0}

        recent_ratings = analyst_data["recent_ratings"]
        avg_rating_score = sum(
            rating_scores.get(rating["rating"], 0) for rating in recent_ratings
        ) / len(recent_ratings) if recent_ratings else 0

        analyst_sentiment_score = (
            avg_rating_score * 0.5 +
            (analyst_data["rating_changes_30d"]["upgrades"] - analyst_data["rating_changes_30d"]["downgrades"]) * 0.1 +
            min(1.0, analyst_data["price_target_changes"]["target_change_avg"] / 10) * 0.4
        )

        return {
            "analyst_count": len(recent_ratings),
            "avg_sentiment": analyst_sentiment_score,
            "consensus_rating": "Buy" if avg_rating_score > 0.3 else "Hold" if avg_rating_score > -0.3 else "Sell",
            "recent_ratings": analyst_data["recent_ratings"],
            "rating_changes": analyst_data["rating_changes_30d"],
            "price_targets": analyst_data["price_target_changes"],
            "analyst_momentum": "positive" if analyst_sentiment_score > 0.1 else "negative" if analyst_sentiment_score < -0.1 else "neutral"
        }

    def _detect_breaking_news(self, symbol: str) -> Dict[str, Any]:
        """Detect breaking news and market-moving events"""
        # Mock breaking news detection

        breaking_news = [
            {
                "headline": f"{symbol} announces major product launch ahead of schedule",
                "urgency": "high",
                "sentiment_impact": 0.8,
                "market_impact_estimate": "positive_moderate",
                "published_at": "2024-01-15T15:45:00Z",
                "source": "Reuters",
                "relevance_score": 0.95
            }
        ]

        return {
            "breaking_news_count": len(breaking_news),
            "breaking_news": breaking_news,
            "market_moving_events": [
                {
                    "event": "earnings_announcement",
                    "impact": "high",
                    "sentiment": "positive",
                    "timing": "today"
                }
            ],
            "urgency_level": "moderate",
            "immediate_action_required": False
        }

    def _calculate_sentiment_momentum(self, symbol: str) -> Dict[str, Any]:
        """Calculate sentiment momentum and trend changes"""
        # Mock sentiment momentum calculation

        # Simulate sentiment over time periods
        sentiment_history = {
            "1_hour": 0.71,
            "4_hours": 0.68,
            "24_hours": 0.65,
            "7_days": 0.58,
            "30_days": 0.52
        }

        # Calculate momentum
        short_term_momentum = sentiment_history["1_hour"] - sentiment_history["4_hours"]
        medium_term_momentum = sentiment_history["4_hours"] - sentiment_history["24_hours"]
        long_term_momentum = sentiment_history["24_hours"] - sentiment_history["7_days"]

        trend_direction = "improving" if short_term_momentum > 0 else "deteriorating" if short_term_momentum < 0 else "stable"
        momentum_strength = "strong" if abs(short_term_momentum) > 0.1 else "moderate" if abs(short_term_momentum) > 0.05 else "weak"

        return {
            "sentiment_history": sentiment_history,
            "momentum_metrics": {
                "short_term": short_term_momentum,
                "medium_term": medium_term_momentum,
                "long_term": long_term_momentum
            },
            "trend_direction": trend_direction,
            "momentum_strength": momentum_strength,
            "sentiment_acceleration": medium_term_momentum - short_term_momentum,
            "trend_sustainability": "high" if long_term_momentum > 0 and short_term_momentum > 0 else "low"
        }

    def _identify_sentiment_extremes(self, symbol: str) -> Dict[str, Any]:
        """Identify extreme sentiment levels"""
        # Mock sentiment extremes analysis

        current_sentiment = 0.68
        sentiment_percentile = 78  # 78th percentile based on historical data

        extreme_analysis = {
            "current_sentiment": current_sentiment,
            "sentiment_percentile": sentiment_percentile,
            "is_extreme": sentiment_percentile > 90 or sentiment_percentile < 10,
            "extreme_type": None,
            "reversal_probability": 0.0,
            "historical_extremes": [
                {"date": "2024-01-01", "sentiment": 0.92, "market_reaction": "reversal_down"},
                {"date": "2023-12-15", "sentiment": -0.85, "market_reaction": "reversal_up"}
            ]
        }

        if sentiment_percentile > 90:
            extreme_analysis.update({
                "extreme_type": "euphoria",
                "reversal_probability": 0.65,
                "contrarian_signal": "strong_sell"
            })
        elif sentiment_percentile < 10:
            extreme_analysis.update({
                "extreme_type": "despair",
                "reversal_probability": 0.70,
                "contrarian_signal": "strong_buy"
            })
        else:
            extreme_analysis.update({
                "extreme_type": None,
                "reversal_probability": 0.15,
                "contrarian_signal": None
            })

        return extreme_analysis

    def _generate_sentiment_recommendation(
        self, news_sentiment: Dict, social_sentiment: Dict, analyst_sentiment: Dict,
        momentum: Dict, extremes: Dict
    ) -> Dict[str, Any]:
        """Generate overall sentiment recommendation"""

        # Weight the different sentiment sources
        weights = {
            "news": 0.4,
            "social": 0.3,
            "analyst": 0.2,
            "momentum": 0.1
        }

        # Calculate weighted sentiment score
        overall_score = (
            news_sentiment.get("avg_sentiment", 0) * weights["news"] +
            social_sentiment.get("avg_sentiment", 0) * weights["social"] +
            analyst_sentiment.get("avg_sentiment", 0) * weights["analyst"] +
            momentum.get("momentum_metrics", {}).get("short_term", 0) * weights["momentum"]
        )

        # Determine sentiment label
        if overall_score > 0.6:
            label = "very_positive"
        elif overall_score > 0.2:
            label = "positive"
        elif overall_score > -0.2:
            label = "neutral"
        elif overall_score > -0.6:
            label = "negative"
        else:
            label = "very_negative"

        # Generate recommendation
        if extremes.get("is_extreme") and extremes.get("extreme_type") == "euphoria":
            recommendation = "CAUTION_SELL"  # Contrarian signal
            confidence = 0.75
        elif extremes.get("is_extreme") and extremes.get("extreme_type") == "despair":
            recommendation = "STRONG_BUY"  # Contrarian signal
            confidence = 0.80
        elif overall_score > 0.4:
            recommendation = "BUY"
            confidence = min(0.85, overall_score + 0.2)
        elif overall_score < -0.4:
            recommendation = "SELL"
            confidence = min(0.85, abs(overall_score) + 0.2)
        else:
            recommendation = "HOLD"
            confidence = 0.60

        # Generate reasoning
        reasoning = []
        if news_sentiment.get("avg_sentiment", 0) > 0.5:
            reasoning.append("Strong positive news sentiment detected")
        if social_sentiment.get("total_mentions", 0) > 1000:
            reasoning.append("High social media engagement with positive sentiment")
        if analyst_sentiment.get("consensus_rating") == "Buy":
            reasoning.append("Analyst consensus supports positive outlook")
        if momentum.get("trend_direction") == "improving":
            reasoning.append("Sentiment momentum is improving")

        # Generate risk factors
        risk_factors = []
        if extremes.get("is_extreme"):
            risk_factors.append(f"Sentiment at extreme levels ({extremes.get('extreme_type')})")
        if social_sentiment.get("viral_potential") == "high":
            risk_factors.append("High viral potential could lead to sentiment volatility")

        return {
            "overall_score": overall_score,
            "label": label,
            "recommendation": recommendation,
            "confidence": confidence,
            "reasoning": reasoning,
            "risk_factors": risk_factors,
            "key_topics": [
                {"topic": "earnings_optimism", "sentiment": 0.85, "mentions": 45},
                {"topic": "product_innovation", "sentiment": 0.78, "mentions": 32},
                {"topic": "market_volatility", "sentiment": -0.23, "mentions": 18}
            ],
            "trend": momentum.get("trend_direction"),
            "impact_prediction": {
                "short_term": "positive" if overall_score > 0.2 else "negative" if overall_score < -0.2 else "neutral",
                "medium_term": "neutral" if extremes.get("is_extreme") else label,
                "confidence": confidence * 0.8  # Lower confidence for longer-term predictions
            }
        }