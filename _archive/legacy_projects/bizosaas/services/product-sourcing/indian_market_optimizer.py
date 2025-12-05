#!/usr/bin/env python3
"""
Indian Market Optimization Module
Specialized algorithms for Indian e-commerce market analysis and optimization
"""

import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import calendar

import numpy as np

logger = logging.getLogger(__name__)

@dataclass
class IndianMarketInsights:
    """Indian market insights data structure"""
    gst_impact: float
    regional_demand: Dict[str, float]
    festival_boost: float
    pricing_strategy: str
    local_competition: Dict[str, Any]
    cultural_factors: List[str]
    logistics_score: float
    payment_preferences: Dict[str, float]

class IndianMarketOptimizer:
    """
    Comprehensive Indian market optimization engine
    Handles GST, regional preferences, festivals, cultural factors
    """
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.IndianMarketOptimizer")
        
        # Indian market data
        self.gst_rates = self._load_gst_rates()
        self.regional_preferences = self._load_regional_preferences()
        self.festival_calendar = self._load_festival_calendar()
        self.cultural_keywords = self._load_cultural_keywords()
        self.tier_cities = self._load_tier_cities()
        self.logistics_hubs = self._load_logistics_hubs()
        
    def optimize_for_indian_market(self, product_data: Dict[str, Any]) -> IndianMarketInsights:
        """
        Comprehensive Indian market optimization analysis
        """
        try:
            self.logger.info(f"Optimizing product for Indian market: {product_data.get('title', 'Unknown')}")
            
            # Calculate GST impact
            gst_impact = self._calculate_gst_impact(product_data)
            
            # Analyze regional demand patterns
            regional_demand = self._analyze_regional_demand(product_data)
            
            # Calculate festival season boost
            festival_boost = self._calculate_festival_boost(product_data)
            
            # Determine optimal pricing strategy
            pricing_strategy = self._determine_pricing_strategy(product_data)
            
            # Analyze local competition
            local_competition = self._analyze_local_competition(product_data)
            
            # Identify cultural factors
            cultural_factors = self._identify_cultural_factors(product_data)
            
            # Calculate logistics score
            logistics_score = self._calculate_logistics_score(product_data)
            
            # Analyze payment preferences
            payment_preferences = self._analyze_payment_preferences(product_data)
            
            insights = IndianMarketInsights(
                gst_impact=gst_impact,
                regional_demand=regional_demand,
                festival_boost=festival_boost,
                pricing_strategy=pricing_strategy,
                local_competition=local_competition,
                cultural_factors=cultural_factors,
                logistics_score=logistics_score,
                payment_preferences=payment_preferences
            )
            
            # Add optimization recommendations
            recommendations = self._generate_optimization_recommendations(insights, product_data)
            
            return {
                "insights": insights,
                "recommendations": recommendations,
                "market_score": self._calculate_market_score(insights),
                "optimized_pricing": self._calculate_optimized_pricing(product_data, insights),
                "launch_timing": self._recommend_launch_timing(insights),
                "target_regions": self._recommend_target_regions(regional_demand),
                "marketing_angles": self._suggest_marketing_angles(cultural_factors, product_data)
            }
            
        except Exception as e:
            self.logger.error(f"Indian market optimization failed: {e}")
            return self._get_default_insights()
    
    def _calculate_gst_impact(self, product_data: Dict[str, Any]) -> float:
        """Calculate GST impact on pricing and profitability"""
        try:
            category = product_data.get("category", "").lower()
            price = product_data.get("price", 0)
            
            # Get applicable GST rate
            gst_rate = self.gst_rates.get(category, 18)  # Default 18%
            
            # Calculate GST amount
            gst_amount = price * (gst_rate / 100)
            
            # Calculate impact on competitiveness (higher GST = less competitive)
            gst_impact_score = max(0, 100 - (gst_rate * 2))  # Scale GST rate to 0-100
            
            # Special considerations
            if gst_rate <= 5:  # Essential goods
                gst_impact_score += 20
            elif gst_rate >= 28:  # Luxury goods
                gst_impact_score -= 15
            
            product_data["gst_analysis"] = {
                "applicable_rate": gst_rate,
                "gst_amount": round(gst_amount, 2),
                "price_including_gst": round(price + gst_amount, 2),
                "impact_score": round(gst_impact_score, 1)
            }
            
            return min(100, max(0, gst_impact_score))
            
        except Exception as e:
            self.logger.error(f"GST calculation failed: {e}")
            return 50.0
    
    def _analyze_regional_demand(self, product_data: Dict[str, Any]) -> Dict[str, float]:
        """Analyze demand patterns across Indian regions"""
        try:
            category = product_data.get("category", "").lower()
            price = product_data.get("price", 0)
            brand = product_data.get("brand", "").lower()
            
            regional_scores = {}
            
            # Base demand for major regions
            regions = ["North", "South", "West", "East", "Northeast", "Central"]
            
            for region in regions:
                base_score = 50  # Neutral baseline
                
                # Category preferences by region
                if category == "electronics":
                    if region in ["South", "West"]:  # Tech-savvy regions
                        base_score += 25
                    elif region in ["North", "Central"]:
                        base_score += 15
                elif category == "fashion":
                    if region in ["West", "North"]:  # Fashion-conscious regions
                        base_score += 20
                    elif region == "South":
                        base_score += 10
                elif category == "home":
                    if region in ["North", "West"]:  # Higher disposable income
                        base_score += 15
                
                # Price sensitivity by region
                if price <= 2000:  # Affordable products
                    if region in ["East", "Northeast", "Central"]:
                        base_score += 20
                elif price >= 15000:  # Premium products
                    if region in ["West", "South"]:
                        base_score += 15
                    else:
                        base_score -= 10
                
                # Brand preferences
                if brand in ["xiaomi", "realme", "vivo", "oppo"]:  # Chinese brands
                    if region in ["North", "East"]:
                        base_score += 10
                elif brand in ["samsung", "apple", "sony"]:  # Premium brands
                    if region in ["South", "West"]:
                        base_score += 15
                
                # Urban vs rural distribution
                urban_penetration = {
                    "West": 0.8, "South": 0.7, "North": 0.6,
                    "Central": 0.4, "East": 0.3, "Northeast": 0.3
                }
                
                # Adjust for e-commerce penetration
                ecommerce_factor = urban_penetration.get(region, 0.5)
                base_score *= (0.5 + ecommerce_factor)
                
                regional_scores[region] = round(min(100, max(0, base_score)), 1)
            
            return regional_scores
            
        except Exception as e:
            self.logger.error(f"Regional demand analysis failed: {e}")
            return {"North": 50, "South": 50, "West": 50, "East": 50, "Northeast": 50, "Central": 50}
    
    def _calculate_festival_boost(self, product_data: Dict[str, Any]) -> float:
        """Calculate festival season boost potential"""
        try:
            category = product_data.get("category", "").lower()
            current_month = datetime.now().month
            
            # Festival boost factors by category
            category_festival_affinity = {
                "electronics": 0.8,
                "fashion": 0.9,
                "home": 0.7,
                "beauty": 0.8,
                "jewelry": 0.95,
                "books": 0.5,
                "sports": 0.6
            }
            
            base_affinity = category_festival_affinity.get(category, 0.6)
            
            # Festival calendar impact
            current_season = self._get_current_festival_season(current_month)
            seasonal_multiplier = {
                "Diwali": 1.5,
                "Dussehra": 1.3,
                "Karva Chauth": 1.2,
                "Dhanteras": 1.4,
                "Holi": 1.1,
                "Eid": 1.2,
                "Christmas": 1.3,
                "New Year": 1.2,
                "Regular": 1.0
            }
            
            season_boost = seasonal_multiplier.get(current_season, 1.0)
            
            # Calculate final festival boost
            festival_boost = (base_affinity * season_boost * 100) - 100
            
            # Special category considerations
            if category in ["jewelry", "fashion"] and current_season in ["Diwali", "Dhanteras"]:
                festival_boost += 20
            elif category == "electronics" and current_season in ["Diwali", "Christmas"]:
                festival_boost += 15
            
            return round(min(80, max(0, festival_boost)), 1)
            
        except Exception as e:
            self.logger.error(f"Festival boost calculation failed: {e}")
            return 10.0
    
    def _determine_pricing_strategy(self, product_data: Dict[str, Any]) -> str:
        """Determine optimal pricing strategy for Indian market"""
        try:
            price = product_data.get("price", 0)
            category = product_data.get("category", "").lower()
            competition_count = product_data.get("competitor_count", 50)
            rating = product_data.get("rating", 4.0)
            
            # Price segment analysis
            if price <= 1000:
                price_segment = "budget"
            elif price <= 5000:
                price_segment = "mid_range"
            elif price <= 15000:
                price_segment = "premium"
            else:
                price_segment = "luxury"
            
            # Strategy determination logic
            if price_segment == "budget":
                if competition_count >= 100:
                    return "value_leadership"  # Compete on features at low price
                else:
                    return "penetration_pricing"  # Go even lower to gain market share
            
            elif price_segment == "mid_range":
                if rating >= 4.5:
                    return "quality_premium"  # Charge slightly more for quality
                elif competition_count <= 30:
                    return "market_skimming"  # Charge premium for uniqueness
                else:
                    return "competitive_parity"  # Match competitor prices
            
            elif price_segment == "premium":
                if category in ["electronics", "fashion"]:
                    return "premium_positioning"  # Maintain premium image
                else:
                    return "value_premium"  # Justify premium with value
            
            else:  # luxury
                return "prestige_pricing"  # Price for exclusivity
            
        except Exception as e:
            self.logger.error(f"Pricing strategy determination failed: {e}")
            return "competitive_parity"
    
    def _analyze_local_competition(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze local Indian competition landscape"""
        try:
            category = product_data.get("category", "").lower()
            price = product_data.get("price", 0)
            
            # Indian brand analysis
            indian_brands = {
                "electronics": ["micromax", "lava", "karbonn", "intex"],
                "fashion": ["fabindia", "w", "global desi", "biba"],
                "home": ["godrej", "bajaj", "orient", "crompton"],
                "beauty": ["lakme", "biotique", "himalaya", "dabur"]
            }
            
            category_indian_brands = indian_brands.get(category, [])
            
            # Competition intensity analysis
            competition_factors = {
                "indian_brand_presence": len(category_indian_brands) * 10,  # More local brands = more competition
                "price_sensitivity": min(30, (10000 / max(price, 1000)) * 10),  # Lower price = higher sensitivity
                "market_maturity": {
                    "electronics": 85,
                    "fashion": 75,
                    "home": 70,
                    "beauty": 80,
                    "books": 90
                }.get(category, 70)
            }
            
            # Calculate overall competition intensity
            intensity_score = np.mean(list(competition_factors.values()))
            
            # Competitive advantages for international brands
            international_advantages = []
            if price >= 5000:
                international_advantages.append("Premium positioning")
            if category == "electronics":
                international_advantages.append("Technology leadership")
            if product_data.get("rating", 0) >= 4.5:
                international_advantages.append("Quality reputation")
            
            # Local adaptation requirements
            adaptation_requirements = []
            if category in ["fashion", "beauty"]:
                adaptation_requirements.append("Local design preferences")
            if price >= 10000:
                adaptation_requirements.append("EMI options required")
            adaptation_requirements.append("Hindi/local language support")
            adaptation_requirements.append("Festival-themed marketing")
            
            return {
                "intensity_score": round(intensity_score, 1),
                "indian_competitors": category_indian_brands,
                "competition_level": "high" if intensity_score >= 75 else "medium" if intensity_score >= 50 else "low",
                "international_advantages": international_advantages,
                "adaptation_requirements": adaptation_requirements,
                "market_entry_difficulty": "high" if intensity_score >= 80 else "medium" if intensity_score >= 60 else "low"
            }
            
        except Exception as e:
            self.logger.error(f"Local competition analysis failed: {e}")
            return {"intensity_score": 50, "competition_level": "medium"}
    
    def _identify_cultural_factors(self, product_data: Dict[str, Any]) -> List[str]:
        """Identify relevant cultural factors for product positioning"""
        try:
            title = product_data.get("title", "").lower()
            category = product_data.get("category", "").lower()
            price = product_data.get("price", 0)
            
            cultural_factors = []
            
            # Religious/spiritual factors
            if any(keyword in title for keyword in ["gold", "silver", "brass", "copper"]):
                cultural_factors.append("Religious significance of metals")
            
            if category in ["beauty", "fashion"]:
                cultural_factors.append("Traditional vs modern preferences")
                cultural_factors.append("Regional fashion variations")
            
            # Family-oriented factors
            if category in ["home", "kitchen"]:
                cultural_factors.append("Joint family considerations")
                cultural_factors.append("Traditional cooking methods")
            
            # Festival considerations
            if category in ["electronics", "fashion", "jewelry"]:
                cultural_factors.append("Festival gifting culture")
                cultural_factors.append("Auspicious timing importance")
            
            # Value consciousness
            if price >= 5000:
                cultural_factors.append("Value for money emphasis")
                cultural_factors.append("Long-term durability expectations")
            
            # Status and prestige
            if price >= 15000:
                cultural_factors.append("Status symbol importance")
                cultural_factors.append("Brand prestige value")
            
            # Language and communication
            cultural_factors.append("Multilingual customer support needs")
            
            # Trust and credibility
            cultural_factors.append("Word-of-mouth influence")
            cultural_factors.append("Community recommendations importance")
            
            return cultural_factors
            
        except Exception as e:
            self.logger.error(f"Cultural factors identification failed: {e}")
            return ["Value for money emphasis", "Quality importance"]
    
    def _calculate_logistics_score(self, product_data: Dict[str, Any]) -> float:
        """Calculate logistics feasibility score for Indian market"""
        try:
            weight = product_data.get("shipping_weight", product_data.get("weight", 1.0))
            dimensions = product_data.get("dimensions", {})
            price = product_data.get("price", 0)
            category = product_data.get("category", "").lower()
            
            logistics_score = 80  # Base score
            
            # Weight considerations
            if weight <= 0.5:  # Very light
                logistics_score += 15
            elif weight <= 2.0:  # Light
                logistics_score += 10
            elif weight <= 10.0:  # Medium
                logistics_score += 0
            elif weight <= 25.0:  # Heavy
                logistics_score -= 15
            else:  # Very heavy
                logistics_score -= 30
            
            # Size considerations
            if dimensions:
                volume = dimensions.get("length", 10) * dimensions.get("width", 10) * dimensions.get("height", 10)
                if volume <= 1000:  # Small package
                    logistics_score += 10
                elif volume <= 10000:  # Medium package
                    logistics_score += 5
                elif volume >= 50000:  # Large package
                    logistics_score -= 10
            
            # Value-to-weight ratio
            if price > 0 and weight > 0:
                value_density = price / weight
                if value_density >= 5000:  # High value, low weight
                    logistics_score += 15
                elif value_density >= 1000:
                    logistics_score += 10
                elif value_density <= 200:  # Low value, high weight
                    logistics_score -= 15
            
            # Category-specific logistics challenges
            category_adjustments = {
                "electronics": -5,  # Fragile, theft risk
                "books": +10,       # Easy to ship
                "fashion": +5,      # Generally easy
                "home": -10,        # Often bulky
                "beauty": +5,       # Usually small
                "sports": -5        # Often bulky/heavy
            }
            
            logistics_score += category_adjustments.get(category, 0)
            
            # Special handling requirements
            if category in ["electronics", "beauty"]:
                logistics_score -= 5  # Temperature sensitivity
            
            return round(min(100, max(0, logistics_score)), 1)
            
        except Exception as e:
            self.logger.error(f"Logistics score calculation failed: {e}")
            return 70.0
    
    def _analyze_payment_preferences(self, product_data: Dict[str, Any]) -> Dict[str, float]:
        """Analyze preferred payment methods for Indian market"""
        try:
            price = product_data.get("price", 0)
            category = product_data.get("category", "").lower()
            
            # Base payment preferences in India
            base_preferences = {
                "upi": 35.0,
                "cards": 25.0,
                "net_banking": 15.0,
                "emi": 10.0,
                "cod": 10.0,
                "digital_wallets": 5.0
            }
            
            # Adjust based on price
            if price <= 1000:
                base_preferences["upi"] += 10
                base_preferences["cod"] += 15
                base_preferences["cards"] -= 10
                base_preferences["emi"] = 0
            elif price <= 5000:
                base_preferences["upi"] += 5
                base_preferences["cards"] += 5
                base_preferences["emi"] = 5
            elif price <= 15000:
                base_preferences["emi"] += 15
                base_preferences["cards"] += 10
                base_preferences["upi"] -= 5
                base_preferences["cod"] -= 5
            else:  # High-value items
                base_preferences["emi"] += 25
                base_preferences["cards"] += 15
                base_preferences["net_banking"] += 10
                base_preferences["cod"] = 0
                base_preferences["upi"] -= 10
            
            # Category adjustments
            if category == "electronics":
                base_preferences["emi"] += 10
                base_preferences["cards"] += 5
            elif category in ["books", "fashion"]:
                base_preferences["upi"] += 5
                base_preferences["cod"] += 5
            
            # Normalize to 100%
            total = sum(base_preferences.values())
            normalized_preferences = {k: round((v / total) * 100, 1) for k, v in base_preferences.items()}
            
            return normalized_preferences
            
        except Exception as e:
            self.logger.error(f"Payment preferences analysis failed: {e}")
            return {"upi": 35, "cards": 25, "net_banking": 15, "emi": 10, "cod": 10, "digital_wallets": 5}
    
    def _generate_optimization_recommendations(self, insights: IndianMarketInsights, product_data: Dict) -> List[str]:
        """Generate specific optimization recommendations"""
        recommendations = []
        
        # GST optimization
        if insights.gst_impact < 50:
            recommendations.append("Consider GST implications in pricing strategy")
        
        # Regional targeting
        top_region = max(insights.regional_demand.items(), key=lambda x: x[1])
        if top_region[1] >= 70:
            recommendations.append(f"Focus initial launch on {top_region[0]} region")
        
        # Festival timing
        if insights.festival_boost >= 20:
            recommendations.append("Plan inventory buildup for festival season")
            recommendations.append("Create festival-themed marketing campaigns")
        
        # Pricing strategy
        if insights.pricing_strategy == "penetration_pricing":
            recommendations.append("Consider aggressive pricing to gain market share")
        elif insights.pricing_strategy == "premium_positioning":
            recommendations.append("Emphasize premium features and brand value")
        
        # Cultural adaptation
        if "Traditional vs modern preferences" in insights.cultural_factors:
            recommendations.append("Create region-specific product variants")
        
        # Logistics optimization
        if insights.logistics_score < 60:
            recommendations.append("Optimize packaging for Indian logistics")
            recommendations.append("Consider regional fulfillment centers")
        
        # Payment methods
        top_payment = max(insights.payment_preferences.items(), key=lambda x: x[1])
        if top_payment[0] == "emi" and top_payment[1] >= 20:
            recommendations.append("Prominently feature EMI options")
        elif top_payment[0] == "cod":
            recommendations.append("Ensure robust COD capabilities")
        
        return recommendations
    
    def _calculate_market_score(self, insights: IndianMarketInsights) -> float:
        """Calculate overall Indian market viability score"""
        try:
            # Weighted scoring
            weights = {
                "gst_impact": 0.15,
                "regional_demand": 0.25,
                "festival_boost": 0.15,
                "logistics_score": 0.20,
                "competition": 0.25
            }
            
            # Calculate components
            avg_regional_demand = np.mean(list(insights.regional_demand.values()))
            competition_score = 100 - insights.local_competition.get("intensity_score", 50)
            
            # Weighted sum
            market_score = (
                insights.gst_impact * weights["gst_impact"] +
                avg_regional_demand * weights["regional_demand"] +
                insights.festival_boost * weights["festival_boost"] +
                insights.logistics_score * weights["logistics_score"] +
                competition_score * weights["competition"]
            )
            
            return round(min(100, max(0, market_score)), 1)
            
        except Exception as e:
            self.logger.error(f"Market score calculation failed: {e}")
            return 50.0
    
    def _calculate_optimized_pricing(self, product_data: Dict, insights: IndianMarketInsights) -> Dict[str, Any]:
        """Calculate optimized pricing for Indian market"""
        try:
            base_price = product_data.get("price", 0)
            
            # Apply optimization factors
            optimized_price = base_price
            
            # GST consideration
            gst_rate = product_data.get("gst_analysis", {}).get("applicable_rate", 18)
            
            # Regional adjustment (target highest demand region)
            max_regional_demand = max(insights.regional_demand.values())
            if max_regional_demand >= 80:
                optimized_price *= 1.05  # Slight premium possible
            elif max_regional_demand <= 40:
                optimized_price *= 0.95  # Discount needed
            
            # Festival boost consideration
            if insights.festival_boost >= 30:
                festival_price = optimized_price * 1.08  # Festival premium
            else:
                festival_price = optimized_price
            
            # Competition adjustment
            competition_intensity = insights.local_competition.get("intensity_score", 50)
            if competition_intensity >= 80:
                competitive_price = optimized_price * 0.92  # Aggressive pricing
            elif competition_intensity <= 30:
                competitive_price = optimized_price * 1.10  # Premium possible
            else:
                competitive_price = optimized_price
            
            return {
                "base_price": round(base_price, 2),
                "optimized_price": round(optimized_price, 2),
                "festival_season_price": round(festival_price, 2),
                "competitive_price": round(competitive_price, 2),
                "price_including_gst": round(optimized_price * (1 + gst_rate/100), 2),
                "recommended_strategy": insights.pricing_strategy,
                "price_optimization_factors": {
                    "regional_adjustment": round((optimized_price - base_price) / base_price * 100, 2),
                    "gst_rate": gst_rate,
                    "competition_pressure": competition_intensity
                }
            }
            
        except Exception as e:
            self.logger.error(f"Optimized pricing calculation failed: {e}")
            return {"optimized_price": product_data.get("price", 0)}
    
    def _recommend_launch_timing(self, insights: IndianMarketInsights) -> Dict[str, Any]:
        """Recommend optimal launch timing"""
        try:
            current_month = datetime.now().month
            
            # Festival calendar consideration
            upcoming_festivals = self._get_upcoming_festivals()
            
            if insights.festival_boost >= 20:
                # Launch before major festivals
                recommended_timing = "Pre-festival launch recommended"
                optimal_months = [10, 11]  # Before Diwali season
            else:
                # Avoid festival competition
                recommended_timing = "Post-festival launch recommended"
                optimal_months = [1, 2, 3, 7, 8]  # Avoid festival months
            
            # Regional considerations
            top_regions = sorted(insights.regional_demand.items(), key=lambda x: x[1], reverse=True)[:2]
            
            return {
                "recommended_timing": recommended_timing,
                "optimal_months": optimal_months,
                "upcoming_festivals": upcoming_festivals,
                "target_regions_for_launch": [region[0] for region in top_regions],
                "launch_sequence": "Tier-1 cities first, then expand to Tier-2/3"
            }
            
        except Exception as e:
            self.logger.error(f"Launch timing recommendation failed: {e}")
            return {"recommended_timing": "Q1 launch recommended"}
    
    def _recommend_target_regions(self, regional_demand: Dict[str, float]) -> List[Dict[str, Any]]:
        """Recommend target regions based on demand analysis"""
        try:
            sorted_regions = sorted(regional_demand.items(), key=lambda x: x[1], reverse=True)
            
            recommendations = []
            for i, (region, score) in enumerate(sorted_regions):
                priority = "High" if i < 2 else "Medium" if i < 4 else "Low"
                
                recommendations.append({
                    "region": region,
                    "demand_score": score,
                    "priority": priority,
                    "recommended_action": self._get_regional_action(region, score)
                })
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Regional recommendations failed: {e}")
            return []
    
    def _suggest_marketing_angles(self, cultural_factors: List[str], product_data: Dict) -> List[str]:
        """Suggest marketing angles based on cultural factors"""
        try:
            marketing_angles = []
            
            # Cultural factor based angles
            if "Festival gifting culture" in cultural_factors:
                marketing_angles.append("Position as perfect festival gift")
                marketing_angles.append("Create festival-themed packaging")
            
            if "Value for money emphasis" in cultural_factors:
                marketing_angles.append("Emphasize cost-per-use value")
                marketing_angles.append("Compare with premium alternatives")
            
            if "Traditional vs modern preferences" in cultural_factors:
                marketing_angles.append("Blend traditional appeal with modern features")
                marketing_angles.append("Use traditional spokespersons/influencers")
            
            if "Joint family considerations" in cultural_factors:
                marketing_angles.append("Highlight family benefits")
                marketing_angles.append("Show multi-generational usage")
            
            # Category-specific angles
            category = product_data.get("category", "").lower()
            if category == "electronics":
                marketing_angles.append("Emphasize technology leadership")
                marketing_angles.append("Highlight convenience features")
            elif category == "fashion":
                marketing_angles.append("Celebrity endorsements")
                marketing_angles.append("Regional style adaptation")
            
            return marketing_angles
            
        except Exception as e:
            self.logger.error(f"Marketing angles suggestion failed: {e}")
            return ["Value proposition emphasis", "Quality assurance"]
    
    # Data Loading Methods
    
    def _load_gst_rates(self) -> Dict[str, float]:
        """Load GST rates for different categories"""
        return {
            "books": 0,
            "food": 0,
            "agriculture": 0,
            "medical": 5,
            "education": 5,
            "textiles": 5,
            "footwear": 5,
            "mobile": 12,
            "computers": 18,
            "electronics": 18,
            "fashion": 12,
            "home": 18,
            "beauty": 18,
            "automobiles": 28,
            "luxury": 28
        }
    
    def _load_regional_preferences(self) -> Dict[str, Dict]:
        """Load regional preference data"""
        return {
            "North": {"tech_adoption": 0.7, "price_sensitivity": 0.6, "brand_consciousness": 0.8},
            "South": {"tech_adoption": 0.9, "price_sensitivity": 0.5, "brand_consciousness": 0.7},
            "West": {"tech_adoption": 0.8, "price_sensitivity": 0.4, "brand_consciousness": 0.9},
            "East": {"tech_adoption": 0.6, "price_sensitivity": 0.8, "brand_consciousness": 0.6},
            "Northeast": {"tech_adoption": 0.5, "price_sensitivity": 0.9, "brand_consciousness": 0.5},
            "Central": {"tech_adoption": 0.6, "price_sensitivity": 0.7, "brand_consciousness": 0.6}
        }
    
    def _load_festival_calendar(self) -> Dict[str, List[int]]:
        """Load Indian festival calendar"""
        return {
            "Diwali": [10, 11],
            "Dussehra": [9, 10],
            "Holi": [3],
            "Eid": [5, 7],  # Varies by year
            "Christmas": [12],
            "New Year": [1],
            "Dhanteras": [10, 11],
            "Karva Chauth": [10, 11]
        }
    
    def _load_cultural_keywords(self) -> Dict[str, List[str]]:
        """Load cultural keywords for different contexts"""
        return {
            "traditional": ["ethnic", "traditional", "classical", "heritage"],
            "modern": ["smart", "digital", "tech", "advanced"],
            "family": ["family", "home", "together", "shared"],
            "festival": ["celebration", "festive", "special", "gift"],
            "value": ["affordable", "budget", "economic", "value"]
        }
    
    def _load_tier_cities(self) -> Dict[str, List[str]]:
        """Load tier-wise city classification"""
        return {
            "tier_1": ["Mumbai", "Delhi", "Bangalore", "Chennai", "Hyderabad", "Kolkata", "Pune", "Ahmedabad"],
            "tier_2": ["Jaipur", "Lucknow", "Kanpur", "Nagpur", "Indore", "Thane", "Bhopal", "Visakhapatnam"],
            "tier_3": ["Agra", "Nashik", "Faridabad", "Meerut", "Rajkot", "Varanasi", "Srinagar", "Amritsar"]
        }
    
    def _load_logistics_hubs(self) -> List[str]:
        """Load major logistics hubs"""
        return ["Mumbai", "Delhi", "Bangalore", "Chennai", "Hyderabad", "Kolkata", "Pune", "Gurgaon"]
    
    # Helper Methods
    
    def _get_current_festival_season(self, month: int) -> str:
        """Get current festival season"""
        festival_months = {
            10: "Dussehra", 11: "Diwali", 12: "Christmas",
            1: "New Year", 3: "Holi", 5: "Eid", 7: "Eid"
        }
        return festival_months.get(month, "Regular")
    
    def _get_upcoming_festivals(self) -> List[Dict[str, Any]]:
        """Get upcoming festivals in next 3 months"""
        current_month = datetime.now().month
        upcoming = []
        
        festivals = {
            "Diwali": {"month": 11, "boost": "High"},
            "Christmas": {"month": 12, "boost": "Medium"},
            "New Year": {"month": 1, "boost": "Medium"},
            "Holi": {"month": 3, "boost": "Medium"}
        }
        
        for festival, data in festivals.items():
            months_away = (data["month"] - current_month) % 12
            if 0 <= months_away <= 3:
                upcoming.append({
                    "festival": festival,
                    "months_away": months_away,
                    "expected_boost": data["boost"]
                })
        
        return sorted(upcoming, key=lambda x: x["months_away"])
    
    def _get_regional_action(self, region: str, score: float) -> str:
        """Get recommended action for region based on score"""
        if score >= 70:
            return "Priority launch market"
        elif score >= 50:
            return "Secondary market expansion"
        else:
            return "Monitor and evaluate"
    
    def _get_default_insights(self) -> IndianMarketInsights:
        """Get default insights in case of error"""
        return IndianMarketInsights(
            gst_impact=50.0,
            regional_demand={"North": 50, "South": 50, "West": 50, "East": 50, "Northeast": 50, "Central": 50},
            festival_boost=10.0,
            pricing_strategy="competitive_parity",
            local_competition={"intensity_score": 50, "competition_level": "medium"},
            cultural_factors=["Value for money emphasis"],
            logistics_score=70.0,
            payment_preferences={"upi": 35, "cards": 25, "net_banking": 15, "emi": 10, "cod": 10, "digital_wallets": 5}
        )

# Example usage
async def main():
    """Example usage of Indian Market Optimizer"""
    optimizer = IndianMarketOptimizer()
    
    sample_product = {
        "title": "Wireless Bluetooth Earbuds",
        "price": 2999,
        "category": "electronics",
        "brand": "TechBrand",
        "rating": 4.2,
        "review_count": 500,
        "competitor_count": 75,
        "weight": 0.1
    }
    
    insights = optimizer.optimize_for_indian_market(sample_product)
    print(f"Market Score: {insights['market_score']}")
    print(f"Optimized Price: ₹{insights['optimized_pricing']['optimized_price']}")
    print(f"Top Region: {insights['target_regions'][0]['region']}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())