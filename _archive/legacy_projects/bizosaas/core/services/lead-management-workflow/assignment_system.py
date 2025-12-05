"""
Automated Lead Assignment System for BizOSaaS Platform
Intelligent lead routing with multiple assignment strategies
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json
import math
import random
from collections import defaultdict, deque
import aioredis
import asyncpg
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AssignmentStrategy(Enum):
    ROUND_ROBIN = "round_robin"
    SKILL_BASED = "skill_based"
    TERRITORY_BASED = "territory_based"
    WORKLOAD_BALANCED = "workload_balanced"
    PERFORMANCE_WEIGHTED = "performance_weighted"
    HYBRID = "hybrid"

class LeadPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class SalesRepStatus(Enum):
    AVAILABLE = "available"
    BUSY = "busy"
    AWAY = "away"
    OFFLINE = "offline"

@dataclass
class SalesRepresentative:
    """Sales representative data structure"""
    rep_id: str
    name: str
    email: str
    team: str
    status: SalesRepStatus = SalesRepStatus.AVAILABLE
    
    # Skills and specializations
    skills: List[str] = field(default_factory=list)
    industries: List[str] = field(default_factory=list)
    languages: List[str] = field(default_factory=list)
    
    # Territory and capacity
    territories: List[str] = field(default_factory=list)
    max_daily_leads: int = 10
    max_concurrent_leads: int = 50
    
    # Performance metrics
    conversion_rate: float = 0.0
    average_response_time: float = 0.0
    customer_satisfaction: float = 0.0
    total_closed_deals: int = 0
    total_revenue: float = 0.0
    
    # Current workload
    active_leads: int = 0
    leads_today: int = 0
    last_assignment: Optional[datetime] = None
    
    # Preferences and settings
    working_hours: Dict[str, Any] = field(default_factory=dict)
    notification_preferences: Dict[str, bool] = field(default_factory=dict)
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class LeadAssignment:
    """Lead assignment record"""
    assignment_id: str
    lead_id: str
    rep_id: str
    strategy_used: AssignmentStrategy
    priority: LeadPriority
    assigned_at: datetime = field(default_factory=datetime.utcnow)
    assigned_by: str = "system"
    
    # Assignment scoring
    assignment_score: float = 0.0
    skill_match_score: float = 0.0
    territory_match_score: float = 0.0
    workload_score: float = 0.0
    performance_score: float = 0.0
    
    # Status tracking
    acknowledged_at: Optional[datetime] = None
    first_contact_at: Optional[datetime] = None
    converted_at: Optional[datetime] = None
    
    # Escalation
    escalated: bool = False
    escalated_at: Optional[datetime] = None
    escalation_reason: Optional[str] = None
    
    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)

class AssignmentRule(BaseModel):
    """Assignment rule configuration"""
    rule_id: str
    name: str
    strategy: AssignmentStrategy
    priority: int
    conditions: Dict[str, Any]
    actions: Dict[str, Any]
    enabled: bool = True

class WorkloadBalancer:
    """Manages workload balancing across sales representatives"""
    
    def __init__(self):
        self.rep_workloads = defaultdict(lambda: {"leads": 0, "score": 0.0})
        self.assignment_queue = deque()
        self.performance_weights = {
            "conversion_rate": 0.4,
            "response_time": 0.3,
            "satisfaction": 0.3
        }
    
    def calculate_workload_score(self, rep: SalesRepresentative) -> float:
        """Calculate normalized workload score (0-100, lower is better)"""
        try:
            # Current workload factors
            lead_capacity_ratio = rep.active_leads / max(1, rep.max_concurrent_leads)
            daily_lead_ratio = rep.leads_today / max(1, rep.max_daily_leads)
            
            # Time since last assignment
            time_since_assignment = 0.0
            if rep.last_assignment:
                hours_since = (datetime.utcnow() - rep.last_assignment).total_seconds() / 3600
                time_since_assignment = min(1.0, hours_since / 24)  # Normalize to 0-1 over 24 hours
            
            # Calculate base workload score
            workload_score = (lead_capacity_ratio * 50 + daily_lead_ratio * 30) * (1 - time_since_assignment * 0.2)
            
            return min(100.0, max(0.0, workload_score))
            
        except Exception as e:
            logger.error(f"Error calculating workload score for rep {rep.rep_id}: {e}")
            return 50.0  # Default neutral score
    
    def calculate_performance_score(self, rep: SalesRepresentative) -> float:
        """Calculate performance-weighted score (0-100, higher is better)"""
        try:
            # Normalize metrics (0-1)
            conversion_score = min(1.0, rep.conversion_rate)
            
            # Response time score (faster is better, max 24 hours)
            response_score = max(0.0, 1.0 - (rep.average_response_time / 24))
            
            # Customer satisfaction score
            satisfaction_score = rep.customer_satisfaction / 5.0  # Assuming 1-5 scale
            
            # Weighted performance score
            performance_score = (
                conversion_score * self.performance_weights["conversion_rate"] +
                response_score * self.performance_weights["response_time"] +
                satisfaction_score * self.performance_weights["satisfaction"]
            ) * 100
            
            return performance_score
            
        except Exception as e:
            logger.error(f"Error calculating performance score for rep {rep.rep_id}: {e}")
            return 50.0  # Default neutral score
    
    def get_balanced_assignment_score(self, rep: SalesRepresentative, lead_data: Dict[str, Any]) -> float:
        """Calculate balanced assignment score considering workload and performance"""
        workload_score = self.calculate_workload_score(rep)
        performance_score = self.calculate_performance_score(rep)
        
        # Combined score (lower workload + higher performance = better assignment)
        # Invert workload score so lower workload gives higher score
        balanced_score = (100 - workload_score) * 0.6 + performance_score * 0.4
        
        return balanced_score

class SkillMatcher:
    """Matches leads to sales reps based on skills and specializations"""
    
    def __init__(self):
        self.skill_weights = {
            "industry": 0.4,
            "service_type": 0.3,
            "company_size": 0.2,
            "language": 0.1
        }
    
    def calculate_skill_match_score(self, rep: SalesRepresentative, lead_data: Dict[str, Any]) -> float:
        """Calculate skill match score between rep and lead"""
        try:
            total_score = 0.0
            
            # Industry match
            lead_industry = lead_data.get("industry", "").lower()
            if lead_industry and lead_industry in [ind.lower() for ind in rep.industries]:
                total_score += self.skill_weights["industry"] * 100
            
            # Service type match
            lead_services = lead_data.get("service_requirements", [])
            rep_skills_lower = [skill.lower() for skill in rep.skills]
            service_matches = sum(1 for service in lead_services 
                                if any(skill in service.lower() for skill in rep_skills_lower))
            if lead_services:
                service_match_ratio = service_matches / len(lead_services)
                total_score += self.skill_weights["service_type"] * service_match_ratio * 100
            
            # Company size match
            lead_company_size = lead_data.get("company_size", 0)
            if "enterprise" in rep.skills and lead_company_size > 500:
                total_score += self.skill_weights["company_size"] * 100
            elif "smb" in rep.skills and 10 <= lead_company_size <= 500:
                total_score += self.skill_weights["company_size"] * 100
            elif "startup" in rep.skills and lead_company_size < 10:
                total_score += self.skill_weights["company_size"] * 100
            
            # Language match (if specified)
            lead_language = lead_data.get("preferred_language", "english").lower()
            if lead_language in [lang.lower() for lang in rep.languages]:
                total_score += self.skill_weights["language"] * 100
            
            return min(100.0, total_score)
            
        except Exception as e:
            logger.error(f"Error calculating skill match for rep {rep.rep_id}: {e}")
            return 0.0

class TerritoryManager:
    """Manages territory-based lead assignment"""
    
    def __init__(self):
        self.territory_hierarchies = {}
        self.timezone_mappings = {}
    
    def calculate_territory_match_score(self, rep: SalesRepresentative, lead_data: Dict[str, Any]) -> float:
        """Calculate territory match score"""
        try:
            lead_location = lead_data.get("location", "").lower()
            if not lead_location:
                return 0.0
            
            # Direct territory match
            for territory in rep.territories:
                if territory.lower() in lead_location:
                    return 100.0
            
            # Country/region match
            for territory in rep.territories:
                if self._is_region_match(territory, lead_location):
                    return 75.0
            
            # Timezone compatibility
            if self._is_timezone_compatible(rep, lead_location):
                return 50.0
            
            return 0.0
            
        except Exception as e:
            logger.error(f"Error calculating territory match for rep {rep.rep_id}: {e}")
            return 0.0
    
    def _is_region_match(self, territory: str, location: str) -> bool:
        """Check if territory and location are in the same region"""
        region_mappings = {
            "north_america": ["usa", "canada", "mexico"],
            "europe": ["uk", "germany", "france", "spain", "italy", "netherlands"],
            "asia_pacific": ["australia", "new zealand", "singapore", "japan"],
            "global": ["*"]  # Global reps can handle any territory
        }
        
        territory_lower = territory.lower()
        location_lower = location.lower()
        
        for region, countries in region_mappings.items():
            if territory_lower in countries or territory_lower == region:
                return any(country in location_lower for country in countries)
        
        return False
    
    def _is_timezone_compatible(self, rep: SalesRepresentative, location: str) -> bool:
        """Check timezone compatibility between rep and lead"""
        # Simplified timezone check - in production, use proper timezone libraries
        timezone_regions = {
            "americas": ["usa", "canada", "mexico", "brazil"],
            "europe": ["uk", "germany", "france", "spain"],
            "asia": ["japan", "singapore", "australia", "india"]
        }
        
        rep_timezone = rep.metadata.get("timezone_region", "americas")
        lead_timezone = self._get_location_timezone(location)
        
        return rep_timezone == lead_timezone
    
    def _get_location_timezone(self, location: str) -> str:
        """Get timezone region for location"""
        location_lower = location.lower()
        
        if any(country in location_lower for country in ["usa", "canada", "mexico"]):
            return "americas"
        elif any(country in location_lower for country in ["uk", "germany", "france", "spain"]):
            return "europe"
        elif any(country in location_lower for country in ["japan", "singapore", "australia"]):
            return "asia"
        else:
            return "americas"  # Default

class EscalationManager:
    """Manages lead escalation and reassignment"""
    
    def __init__(self):
        self.escalation_rules = [
            {"trigger": "no_response_24h", "action": "notify_manager"},
            {"trigger": "no_response_48h", "action": "reassign_senior"},
            {"trigger": "high_value_lead", "action": "notify_senior_manager"},
            {"trigger": "complaint_received", "action": "escalate_immediately"}
        ]
    
    async def check_escalation_needed(self, assignment: LeadAssignment, 
                                    lead_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Check if lead assignment needs escalation"""
        try:
            now = datetime.utcnow()
            hours_since_assignment = (now - assignment.assigned_at).total_seconds() / 3600
            
            escalation_needed = None
            
            # Check response time escalation
            if not assignment.acknowledged_at and hours_since_assignment > 24:
                escalation_needed = {
                    "type": "no_acknowledgment",
                    "trigger": "no_response_24h",
                    "hours_elapsed": hours_since_assignment,
                    "recommended_action": "notify_manager"
                }
            
            elif not assignment.first_contact_at and hours_since_assignment > 48:
                escalation_needed = {
                    "type": "no_contact",
                    "trigger": "no_response_48h", 
                    "hours_elapsed": hours_since_assignment,
                    "recommended_action": "reassign_senior"
                }
            
            # Check high-value lead escalation
            lead_score = lead_data.get("total_score", 0)
            if lead_score > 80 and not assignment.acknowledged_at and hours_since_assignment > 2:
                escalation_needed = {
                    "type": "high_value_urgent",
                    "trigger": "high_value_lead",
                    "lead_score": lead_score,
                    "recommended_action": "notify_senior_manager"
                }
            
            return escalation_needed
            
        except Exception as e:
            logger.error(f"Error checking escalation for assignment {assignment.assignment_id}: {e}")
            return None

class LeadAssignmentSystem:
    """Main lead assignment system with multiple strategies"""
    
    def __init__(self, db_config: Dict[str, str], redis_config: Dict[str, str]):
        self.db_config = db_config
        self.redis_config = redis_config
        
        # Assignment components
        self.workload_balancer = WorkloadBalancer()
        self.skill_matcher = SkillMatcher()
        self.territory_manager = TerritoryManager()
        self.escalation_manager = EscalationManager()
        
        # Assignment tracking
        self.round_robin_index = 0
        self.assignment_history = deque(maxlen=1000)
        
        # Performance metrics
        self.assignment_metrics = {
            "total_assignments": 0,
            "assignment_distribution": defaultdict(int),
            "average_assignment_time": 0.0,
            "escalation_rate": 0.0
        }
    
    async def initialize(self):
        """Initialize database connections and load configurations"""
        try:
            # Initialize database connection
            self.db_pool = await asyncpg.create_pool(**self.db_config)
            
            # Initialize Redis connection
            self.redis = await aioredis.from_url(
                f"redis://{self.redis_config['host']}:{self.redis_config['port']}"
            )
            
            # Load sales representatives and assignment rules
            await self._load_sales_representatives()
            await self._load_assignment_rules()
            
            # Start background tasks
            asyncio.create_task(self._escalation_monitor())
            asyncio.create_task(self._performance_updater())
            
            logger.info("Lead assignment system initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize lead assignment system: {e}")
            raise
    
    async def _load_sales_representatives(self):
        """Load sales representatives from database"""
        try:
            async with self.db_pool.acquire() as conn:
                rows = await conn.fetch("""
                    SELECT sr.*, 
                           COALESCE(stats.conversion_rate, 0) as conversion_rate,
                           COALESCE(stats.avg_response_time, 24) as average_response_time,
                           COALESCE(stats.customer_satisfaction, 3.0) as customer_satisfaction,
                           COALESCE(stats.total_closed_deals, 0) as total_closed_deals,
                           COALESCE(stats.total_revenue, 0) as total_revenue,
                           COALESCE(workload.active_leads, 0) as active_leads,
                           COALESCE(workload.leads_today, 0) as leads_today
                    FROM sales_representatives sr
                    LEFT JOIN sales_rep_stats stats ON sr.rep_id = stats.rep_id
                    LEFT JOIN sales_rep_workload workload ON sr.rep_id = workload.rep_id
                    WHERE sr.active = true
                """)
                
                self.sales_reps = {}
                for row in rows:
                    rep = SalesRepresentative(
                        rep_id=row["rep_id"],
                        name=row["name"],
                        email=row["email"],
                        team=row["team"],
                        status=SalesRepStatus(row["status"]),
                        skills=json.loads(row["skills"]) if row["skills"] else [],
                        industries=json.loads(row["industries"]) if row["industries"] else [],
                        languages=json.loads(row["languages"]) if row["languages"] else [],
                        territories=json.loads(row["territories"]) if row["territories"] else [],
                        max_daily_leads=row["max_daily_leads"],
                        max_concurrent_leads=row["max_concurrent_leads"],
                        conversion_rate=float(row["conversion_rate"]),
                        average_response_time=float(row["average_response_time"]),
                        customer_satisfaction=float(row["customer_satisfaction"]),
                        total_closed_deals=int(row["total_closed_deals"]),
                        total_revenue=float(row["total_revenue"]),
                        active_leads=int(row["active_leads"]),
                        leads_today=int(row["leads_today"]),
                        last_assignment=row.get("last_assignment"),
                        working_hours=json.loads(row["working_hours"]) if row["working_hours"] else {},
                        notification_preferences=json.loads(row["notification_preferences"]) if row["notification_preferences"] else {}
                    )
                    self.sales_reps[rep.rep_id] = rep
                
                logger.info(f"Loaded {len(self.sales_reps)} sales representatives")
                
        except Exception as e:
            logger.error(f"Error loading sales representatives: {e}")
            self.sales_reps = {}
    
    async def _load_assignment_rules(self):
        """Load assignment rules from database"""
        try:
            async with self.db_pool.acquire() as conn:
                rows = await conn.fetch("""
                    SELECT * FROM assignment_rules 
                    WHERE enabled = true 
                    ORDER BY priority DESC
                """)
                
                self.assignment_rules = []
                for row in rows:
                    rule = AssignmentRule(
                        rule_id=row["rule_id"],
                        name=row["name"],
                        strategy=AssignmentStrategy(row["strategy"]),
                        priority=row["priority"],
                        conditions=json.loads(row["conditions"]),
                        actions=json.loads(row["actions"]),
                        enabled=row["enabled"]
                    )
                    self.assignment_rules.append(rule)
                
                logger.info(f"Loaded {len(self.assignment_rules)} assignment rules")
                
        except Exception as e:
            logger.error(f"Error loading assignment rules: {e}")
            self.assignment_rules = []
    
    async def assign_lead(self, lead_id: str, lead_data: Dict[str, Any], 
                         strategy: Optional[AssignmentStrategy] = None,
                         manual_rep_id: Optional[str] = None) -> Optional[LeadAssignment]:
        """Main method to assign a lead to a sales representative"""
        start_time = datetime.utcnow()
        
        try:
            # Check for manual assignment
            if manual_rep_id:
                return await self._manual_assignment(lead_id, lead_data, manual_rep_id)
            
            # Determine assignment strategy
            if not strategy:
                strategy = await self._determine_assignment_strategy(lead_data)
            
            # Get available representatives
            available_reps = await self._get_available_representatives(lead_data)
            
            if not available_reps:
                logger.warning(f"No available representatives for lead {lead_id}")
                return None
            
            # Assign based on strategy
            selected_rep = await self._execute_assignment_strategy(
                strategy, available_reps, lead_data
            )
            
            if not selected_rep:
                logger.warning(f"No suitable representative found for lead {lead_id}")
                return None
            
            # Create assignment record
            assignment = LeadAssignment(
                assignment_id=f"assign_{lead_id}_{int(datetime.utcnow().timestamp())}",
                lead_id=lead_id,
                rep_id=selected_rep.rep_id,
                strategy_used=strategy,
                priority=self._determine_lead_priority(lead_data),
                assignment_score=self._calculate_assignment_score(selected_rep, lead_data),
                skill_match_score=self.skill_matcher.calculate_skill_match_score(selected_rep, lead_data),
                territory_match_score=self.territory_manager.calculate_territory_match_score(selected_rep, lead_data),
                workload_score=self.workload_balancer.calculate_workload_score(selected_rep),
                performance_score=self.workload_balancer.calculate_performance_score(selected_rep)
            )
            
            # Store assignment and update workload
            await self._store_assignment(assignment, lead_data)
            await self._update_rep_workload(selected_rep.rep_id, 1)
            
            # Send notifications
            await self._send_assignment_notifications(assignment, selected_rep, lead_data)
            
            # Update metrics
            assignment_time = (datetime.utcnow() - start_time).total_seconds()
            await self._update_assignment_metrics(assignment_time, strategy)
            
            logger.info(f"Lead {lead_id} assigned to {selected_rep.name} using {strategy.value} strategy")
            
            return assignment
            
        except Exception as e:
            logger.error(f"Error assigning lead {lead_id}: {e}")
            return None
    
    async def _determine_assignment_strategy(self, lead_data: Dict[str, Any]) -> AssignmentStrategy:
        """Determine the best assignment strategy for a lead"""
        try:
            # Check assignment rules first
            for rule in self.assignment_rules:
                if await self._rule_matches(rule, lead_data):
                    return rule.strategy
            
            # Default strategy based on lead characteristics
            lead_score = lead_data.get("total_score", 0)
            company_size = lead_data.get("company_size", 0)
            
            if lead_score > 80:
                return AssignmentStrategy.PERFORMANCE_WEIGHTED
            elif company_size > 500:
                return AssignmentStrategy.SKILL_BASED
            elif lead_data.get("location"):
                return AssignmentStrategy.TERRITORY_BASED
            else:
                return AssignmentStrategy.HYBRID
                
        except Exception as e:
            logger.error(f"Error determining assignment strategy: {e}")
            return AssignmentStrategy.ROUND_ROBIN
    
    async def _rule_matches(self, rule: AssignmentRule, lead_data: Dict[str, Any]) -> bool:
        """Check if assignment rule matches lead data"""
        try:
            conditions = rule.conditions
            
            for field, condition in conditions.items():
                lead_value = lead_data.get(field)
                
                if isinstance(condition, dict):
                    operator = condition.get("operator", "equals")
                    value = condition.get("value")
                    
                    if operator == "equals" and lead_value != value:
                        return False
                    elif operator == "greater_than" and (not lead_value or lead_value <= value):
                        return False
                    elif operator == "less_than" and (not lead_value or lead_value >= value):
                        return False
                    elif operator == "contains" and (not lead_value or value not in str(lead_value).lower()):
                        return False
                    elif operator == "in" and lead_value not in value:
                        return False
                
                elif lead_value != condition:
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error matching rule {rule.rule_id}: {e}")
            return False
    
    async def _get_available_representatives(self, lead_data: Dict[str, Any]) -> List[SalesRepresentative]:
        """Get list of available sales representatives"""
        try:
            available_reps = []
            
            for rep in self.sales_reps.values():
                # Check availability status
                if rep.status not in [SalesRepStatus.AVAILABLE, SalesRepStatus.BUSY]:
                    continue
                
                # Check workload limits
                if rep.active_leads >= rep.max_concurrent_leads:
                    continue
                
                if rep.leads_today >= rep.max_daily_leads:
                    continue
                
                # Check working hours (simplified)
                current_hour = datetime.utcnow().hour
                working_hours = rep.working_hours
                if working_hours and "start" in working_hours and "end" in working_hours:
                    if not (working_hours["start"] <= current_hour <= working_hours["end"]):
                        continue
                
                available_reps.append(rep)
            
            return available_reps
            
        except Exception as e:
            logger.error(f"Error getting available representatives: {e}")
            return []
    
    async def _execute_assignment_strategy(self, strategy: AssignmentStrategy, 
                                         available_reps: List[SalesRepresentative],
                                         lead_data: Dict[str, Any]) -> Optional[SalesRepresentative]:
        """Execute the specified assignment strategy"""
        try:
            if strategy == AssignmentStrategy.ROUND_ROBIN:
                return self._round_robin_assignment(available_reps)
            
            elif strategy == AssignmentStrategy.SKILL_BASED:
                return self._skill_based_assignment(available_reps, lead_data)
            
            elif strategy == AssignmentStrategy.TERRITORY_BASED:
                return self._territory_based_assignment(available_reps, lead_data)
            
            elif strategy == AssignmentStrategy.WORKLOAD_BALANCED:
                return self._workload_balanced_assignment(available_reps, lead_data)
            
            elif strategy == AssignmentStrategy.PERFORMANCE_WEIGHTED:
                return self._performance_weighted_assignment(available_reps, lead_data)
            
            elif strategy == AssignmentStrategy.HYBRID:
                return self._hybrid_assignment(available_reps, lead_data)
            
            else:
                return self._round_robin_assignment(available_reps)
                
        except Exception as e:
            logger.error(f"Error executing assignment strategy {strategy}: {e}")
            return None
    
    def _round_robin_assignment(self, available_reps: List[SalesRepresentative]) -> Optional[SalesRepresentative]:
        """Round-robin assignment strategy"""
        if not available_reps:
            return None
        
        # Sort by last assignment time for fair distribution
        sorted_reps = sorted(available_reps, 
                           key=lambda x: x.last_assignment or datetime.min)
        
        return sorted_reps[0]
    
    def _skill_based_assignment(self, available_reps: List[SalesRepresentative], 
                               lead_data: Dict[str, Any]) -> Optional[SalesRepresentative]:
        """Skill-based assignment strategy"""
        if not available_reps:
            return None
        
        # Score representatives by skill match
        scored_reps = []
        for rep in available_reps:
            skill_score = self.skill_matcher.calculate_skill_match_score(rep, lead_data)
            scored_reps.append((rep, skill_score))
        
        # Sort by skill score (highest first)
        scored_reps.sort(key=lambda x: x[1], reverse=True)
        
        return scored_reps[0][0]
    
    def _territory_based_assignment(self, available_reps: List[SalesRepresentative],
                                   lead_data: Dict[str, Any]) -> Optional[SalesRepresentative]:
        """Territory-based assignment strategy"""
        if not available_reps:
            return None
        
        # Score representatives by territory match
        scored_reps = []
        for rep in available_reps:
            territory_score = self.territory_manager.calculate_territory_match_score(rep, lead_data)
            scored_reps.append((rep, territory_score))
        
        # Sort by territory score (highest first)
        scored_reps.sort(key=lambda x: x[1], reverse=True)
        
        return scored_reps[0][0]
    
    def _workload_balanced_assignment(self, available_reps: List[SalesRepresentative],
                                     lead_data: Dict[str, Any]) -> Optional[SalesRepresentative]:
        """Workload-balanced assignment strategy"""
        if not available_reps:
            return None
        
        # Score representatives by workload (lower is better)
        scored_reps = []
        for rep in available_reps:
            workload_score = self.workload_balancer.calculate_workload_score(rep)
            scored_reps.append((rep, workload_score))
        
        # Sort by workload score (lowest first)
        scored_reps.sort(key=lambda x: x[1])
        
        return scored_reps[0][0]
    
    def _performance_weighted_assignment(self, available_reps: List[SalesRepresentative],
                                        lead_data: Dict[str, Any]) -> Optional[SalesRepresentative]:
        """Performance-weighted assignment strategy"""
        if not available_reps:
            return None
        
        # Score representatives by performance
        scored_reps = []
        for rep in available_reps:
            performance_score = self.workload_balancer.calculate_performance_score(rep)
            scored_reps.append((rep, performance_score))
        
        # Sort by performance score (highest first)
        scored_reps.sort(key=lambda x: x[1], reverse=True)
        
        return scored_reps[0][0]
    
    def _hybrid_assignment(self, available_reps: List[SalesRepresentative],
                          lead_data: Dict[str, Any]) -> Optional[SalesRepresentative]:
        """Hybrid assignment strategy combining multiple factors"""
        if not available_reps:
            return None
        
        # Score representatives with combined metrics
        scored_reps = []
        for rep in available_reps:
            skill_score = self.skill_matcher.calculate_skill_match_score(rep, lead_data)
            territory_score = self.territory_manager.calculate_territory_match_score(rep, lead_data)
            balanced_score = self.workload_balancer.get_balanced_assignment_score(rep, lead_data)
            
            # Weighted combination
            combined_score = (
                skill_score * 0.3 +
                territory_score * 0.2 +
                balanced_score * 0.5
            )
            
            scored_reps.append((rep, combined_score))
        
        # Sort by combined score (highest first)
        scored_reps.sort(key=lambda x: x[1], reverse=True)
        
        return scored_reps[0][0]
    
    async def _manual_assignment(self, lead_id: str, lead_data: Dict[str, Any], 
                               rep_id: str) -> Optional[LeadAssignment]:
        """Handle manual lead assignment"""
        try:
            if rep_id not in self.sales_reps:
                logger.error(f"Sales rep {rep_id} not found for manual assignment")
                return None
            
            selected_rep = self.sales_reps[rep_id]
            
            # Check if rep can handle the assignment
            if selected_rep.active_leads >= selected_rep.max_concurrent_leads:
                logger.warning(f"Rep {rep_id} is at capacity for manual assignment")
                # Allow manual override but log warning
            
            assignment = LeadAssignment(
                assignment_id=f"manual_{lead_id}_{int(datetime.utcnow().timestamp())}",
                lead_id=lead_id,
                rep_id=rep_id,
                strategy_used=AssignmentStrategy.ROUND_ROBIN,  # Manual assignments use round_robin as placeholder
                priority=self._determine_lead_priority(lead_data),
                assigned_by="manual",
                assignment_score=self._calculate_assignment_score(selected_rep, lead_data)
            )
            
            await self._store_assignment(assignment, lead_data)
            await self._update_rep_workload(rep_id, 1)
            
            logger.info(f"Manual assignment: Lead {lead_id} assigned to {selected_rep.name}")
            
            return assignment
            
        except Exception as e:
            logger.error(f"Error in manual assignment: {e}")
            return None
    
    def _determine_lead_priority(self, lead_data: Dict[str, Any]) -> LeadPriority:
        """Determine lead priority based on data"""
        try:
            lead_score = lead_data.get("total_score", 0)
            company_size = lead_data.get("company_size", 0)
            budget = lead_data.get("budget", 0)
            
            if lead_score > 90 or budget > 100000:
                return LeadPriority.URGENT
            elif lead_score > 70 or (company_size > 500 and budget > 50000):
                return LeadPriority.HIGH
            elif lead_score > 50 or budget > 10000:
                return LeadPriority.MEDIUM
            else:
                return LeadPriority.LOW
                
        except Exception as e:
            logger.error(f"Error determining lead priority: {e}")
            return LeadPriority.MEDIUM
    
    def _calculate_assignment_score(self, rep: SalesRepresentative, lead_data: Dict[str, Any]) -> float:
        """Calculate overall assignment score"""
        try:
            skill_score = self.skill_matcher.calculate_skill_match_score(rep, lead_data)
            territory_score = self.territory_manager.calculate_territory_match_score(rep, lead_data)
            workload_score = 100 - self.workload_balancer.calculate_workload_score(rep)  # Invert for scoring
            performance_score = self.workload_balancer.calculate_performance_score(rep)
            
            # Weighted average
            total_score = (
                skill_score * 0.25 +
                territory_score * 0.15 +
                workload_score * 0.3 +
                performance_score * 0.3
            )
            
            return total_score
            
        except Exception as e:
            logger.error(f"Error calculating assignment score: {e}")
            return 50.0
    
    async def _store_assignment(self, assignment: LeadAssignment, lead_data: Dict[str, Any]):
        """Store assignment in database"""
        try:
            async with self.db_pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO lead_assignments (
                        assignment_id, lead_id, rep_id, strategy_used, priority,
                        assignment_score, skill_match_score, territory_match_score,
                        workload_score, performance_score, assigned_at, assigned_by, metadata
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
                """,
                    assignment.assignment_id, assignment.lead_id, assignment.rep_id,
                    assignment.strategy_used.value, assignment.priority.value,
                    assignment.assignment_score, assignment.skill_match_score,
                    assignment.territory_match_score, assignment.workload_score,
                    assignment.performance_score, assignment.assigned_at,
                    assignment.assigned_by, json.dumps(assignment.metadata)
                )
                
                # Update lead status
                await conn.execute("""
                    UPDATE leads SET 
                        status = 'assigned',
                        assigned_rep_id = $1,
                        assigned_at = $2
                    WHERE lead_id = $3
                """, assignment.rep_id, assignment.assigned_at, assignment.lead_id)
            
            # Cache assignment for quick access
            cache_key = f"assignment:{assignment.lead_id}"
            cache_data = {
                "assignment_id": assignment.assignment_id,
                "rep_id": assignment.rep_id,
                "strategy": assignment.strategy_used.value,
                "priority": assignment.priority.value,
                "assigned_at": assignment.assigned_at.isoformat()
            }
            
            await self.redis.setex(cache_key, 3600, json.dumps(cache_data, default=str))
            
        except Exception as e:
            logger.error(f"Error storing assignment {assignment.assignment_id}: {e}")
    
    async def _update_rep_workload(self, rep_id: str, change: int):
        """Update representative workload"""
        try:
            async with self.db_pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO sales_rep_workload (rep_id, active_leads, leads_today, updated_at)
                    VALUES ($1, $2, $3, $4)
                    ON CONFLICT (rep_id) DO UPDATE SET
                        active_leads = sales_rep_workload.active_leads + $2,
                        leads_today = CASE 
                            WHEN DATE(sales_rep_workload.updated_at) = CURRENT_DATE 
                            THEN sales_rep_workload.leads_today + $3
                            ELSE $3
                        END,
                        updated_at = $4
                """, rep_id, change, change if change > 0 else 0, datetime.utcnow())
            
            # Update in-memory representation
            if rep_id in self.sales_reps:
                self.sales_reps[rep_id].active_leads += change
                if change > 0:
                    self.sales_reps[rep_id].leads_today += change
                    self.sales_reps[rep_id].last_assignment = datetime.utcnow()
                
        except Exception as e:
            logger.error(f"Error updating workload for rep {rep_id}: {e}")
    
    async def _send_assignment_notifications(self, assignment: LeadAssignment, 
                                           rep: SalesRepresentative, lead_data: Dict[str, Any]):
        """Send notifications for new assignment"""
        try:
            # Notification data
            notification_data = {
                "type": "lead_assignment",
                "assignment_id": assignment.assignment_id,
                "lead_id": assignment.lead_id,
                "rep_id": assignment.rep_id,
                "rep_name": rep.name,
                "priority": assignment.priority.value,
                "lead_company": lead_data.get("company_name", "Unknown"),
                "lead_score": lead_data.get("total_score", 0),
                "assigned_at": assignment.assigned_at.isoformat()
            }
            
            # Send to notification service (placeholder)
            # In production, this would integrate with email, SMS, Slack, etc.
            await self._send_notification(rep.email, "new_lead_assignment", notification_data)
            
            # Send to manager if high priority
            if assignment.priority in [LeadPriority.HIGH, LeadPriority.URGENT]:
                manager_email = await self._get_manager_email(rep.team)
                if manager_email:
                    await self._send_notification(manager_email, "high_priority_assignment", notification_data)
            
        except Exception as e:
            logger.error(f"Error sending assignment notifications: {e}")
    
    async def _send_notification(self, recipient: str, notification_type: str, data: Dict[str, Any]):
        """Send notification to recipient"""
        try:
            # Publish to notification queue
            notification_message = {
                "recipient": recipient,
                "type": notification_type,
                "data": data,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            await self.redis.lpush("notification_queue", json.dumps(notification_message))
            
        except Exception as e:
            logger.error(f"Error sending notification to {recipient}: {e}")
    
    async def _get_manager_email(self, team: str) -> Optional[str]:
        """Get manager email for team"""
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow("""
                    SELECT manager_email FROM teams WHERE team_name = $1
                """, team)
                
                return row["manager_email"] if row else None
                
        except Exception as e:
            logger.error(f"Error getting manager email for team {team}: {e}")
            return None
    
    async def _update_assignment_metrics(self, assignment_time: float, strategy: AssignmentStrategy):
        """Update assignment performance metrics"""
        try:
            self.assignment_metrics["total_assignments"] += 1
            self.assignment_metrics["assignment_distribution"][strategy.value] += 1
            
            # Update average assignment time
            total_assignments = self.assignment_metrics["total_assignments"]
            current_avg = self.assignment_metrics["average_assignment_time"]
            self.assignment_metrics["average_assignment_time"] = (
                (current_avg * (total_assignments - 1) + assignment_time) / total_assignments
            )
            
        except Exception as e:
            logger.error(f"Error updating assignment metrics: {e}")
    
    async def _escalation_monitor(self):
        """Background task to monitor assignments for escalation"""
        while True:
            try:
                await asyncio.sleep(300)  # Check every 5 minutes
                
                # Get assignments that might need escalation
                async with self.db_pool.acquire() as conn:
                    rows = await conn.fetch("""
                        SELECT la.*, l.* FROM lead_assignments la
                        JOIN leads l ON la.lead_id = l.lead_id
                        WHERE la.escalated = false
                        AND la.assigned_at > NOW() - INTERVAL '72 hours'
                    """)
                    
                    for row in rows:
                        assignment = LeadAssignment(
                            assignment_id=row["assignment_id"],
                            lead_id=row["lead_id"],
                            rep_id=row["rep_id"],
                            strategy_used=AssignmentStrategy(row["strategy_used"]),
                            priority=LeadPriority(row["priority"]),
                            assigned_at=row["assigned_at"],
                            acknowledged_at=row["acknowledged_at"],
                            first_contact_at=row["first_contact_at"],
                            escalated=row["escalated"]
                        )
                        
                        # Convert row to lead_data dict
                        lead_data = {
                            "total_score": row.get("total_score", 0),
                            "company_name": row.get("company_name"),
                            "priority": row.get("priority")
                        }
                        
                        escalation_needed = await self.escalation_manager.check_escalation_needed(
                            assignment, lead_data
                        )
                        
                        if escalation_needed:
                            await self._handle_escalation(assignment, escalation_needed)
                
            except Exception as e:
                logger.error(f"Error in escalation monitor: {e}")
                await asyncio.sleep(60)  # Wait before retrying
    
    async def _handle_escalation(self, assignment: LeadAssignment, escalation_data: Dict[str, Any]):
        """Handle lead assignment escalation"""
        try:
            # Mark assignment as escalated
            async with self.db_pool.acquire() as conn:
                await conn.execute("""
                    UPDATE lead_assignments SET
                        escalated = true,
                        escalated_at = $1,
                        escalation_reason = $2
                    WHERE assignment_id = $3
                """, datetime.utcnow(), escalation_data["type"], assignment.assignment_id)
            
            # Send escalation notifications
            escalation_notification = {
                "type": "assignment_escalation",
                "assignment_id": assignment.assignment_id,
                "lead_id": assignment.lead_id,
                "rep_id": assignment.rep_id,
                "escalation_type": escalation_data["type"],
                "escalation_reason": escalation_data.get("trigger"),
                "recommended_action": escalation_data.get("recommended_action")
            }
            
            # Notify manager
            rep = self.sales_reps.get(assignment.rep_id)
            if rep:
                manager_email = await self._get_manager_email(rep.team)
                if manager_email:
                    await self._send_notification(manager_email, "escalation_alert", escalation_notification)
            
            # Update escalation metrics
            self.assignment_metrics["escalation_rate"] = (
                self.assignment_metrics.get("total_escalations", 0) + 1
            ) / self.assignment_metrics["total_assignments"]
            
            logger.info(f"Escalated assignment {assignment.assignment_id}: {escalation_data['type']}")
            
        except Exception as e:
            logger.error(f"Error handling escalation for assignment {assignment.assignment_id}: {e}")
    
    async def _performance_updater(self):
        """Background task to update sales rep performance metrics"""
        while True:
            try:
                await asyncio.sleep(3600)  # Update every hour
                
                async with self.db_pool.acquire() as conn:
                    # Update conversion rates
                    await conn.execute("""
                        INSERT INTO sales_rep_stats (rep_id, conversion_rate, updated_at)
                        SELECT 
                            la.rep_id,
                            COUNT(CASE WHEN l.status = 'closed_won' THEN 1 END)::float / 
                            NULLIF(COUNT(*), 0) as conversion_rate,
                            NOW()
                        FROM lead_assignments la
                        JOIN leads l ON la.lead_id = l.lead_id
                        WHERE la.assigned_at > NOW() - INTERVAL '30 days'
                        GROUP BY la.rep_id
                        ON CONFLICT (rep_id) DO UPDATE SET
                            conversion_rate = EXCLUDED.conversion_rate,
                            updated_at = EXCLUDED.updated_at
                    """)
                    
                    # Update average response times
                    await conn.execute("""
                        UPDATE sales_rep_stats SET
                            avg_response_time = subquery.avg_response_time
                        FROM (
                            SELECT 
                                la.rep_id,
                                AVG(EXTRACT(EPOCH FROM (la.acknowledged_at - la.assigned_at))/3600) as avg_response_time
                            FROM lead_assignments la
                            WHERE la.acknowledged_at IS NOT NULL
                            AND la.assigned_at > NOW() - INTERVAL '30 days'
                            GROUP BY la.rep_id
                        ) subquery
                        WHERE sales_rep_stats.rep_id = subquery.rep_id
                    """)
                
                # Reload sales representatives with updated stats
                await self._load_sales_representatives()
                
            except Exception as e:
                logger.error(f"Error in performance updater: {e}")
                await asyncio.sleep(600)  # Wait before retrying
    
    async def get_assignment_analytics(self, date_range: Optional[Tuple[datetime, datetime]] = None) -> Dict[str, Any]:
        """Get assignment analytics and performance metrics"""
        try:
            if not date_range:
                end_date = datetime.utcnow()
                start_date = end_date - timedelta(days=30)
            else:
                start_date, end_date = date_range
            
            async with self.db_pool.acquire() as conn:
                # Assignment distribution by strategy
                strategy_distribution = await conn.fetch("""
                    SELECT strategy_used, COUNT(*) as count
                    FROM lead_assignments
                    WHERE assigned_at BETWEEN $1 AND $2
                    GROUP BY strategy_used
                """, start_date, end_date)
                
                # Assignment distribution by rep
                rep_distribution = await conn.fetch("""
                    SELECT sr.name, COUNT(la.*) as assignments,
                           AVG(la.assignment_score) as avg_score
                    FROM lead_assignments la
                    JOIN sales_representatives sr ON la.rep_id = sr.rep_id
                    WHERE la.assigned_at BETWEEN $1 AND $2
                    GROUP BY sr.rep_id, sr.name
                    ORDER BY assignments DESC
                """, start_date, end_date)
                
                # Escalation metrics
                escalation_stats = await conn.fetchrow("""
                    SELECT 
                        COUNT(*) as total_assignments,
                        COUNT(CASE WHEN escalated = true THEN 1 END) as escalated_assignments,
                        AVG(EXTRACT(EPOCH FROM (acknowledged_at - assigned_at))/3600) as avg_acknowledgment_time,
                        AVG(EXTRACT(EPOCH FROM (first_contact_at - assigned_at))/3600) as avg_first_contact_time
                    FROM lead_assignments
                    WHERE assigned_at BETWEEN $1 AND $2
                """, start_date, end_date)
            
            return {
                "date_range": {"start": start_date.isoformat(), "end": end_date.isoformat()},
                "strategy_distribution": {row["strategy_used"]: row["count"] for row in strategy_distribution},
                "rep_distribution": [
                    {
                        "name": row["name"],
                        "assignments": row["assignments"],
                        "avg_score": float(row["avg_score"]) if row["avg_score"] else 0.0
                    }
                    for row in rep_distribution
                ],
                "escalation_metrics": {
                    "total_assignments": escalation_stats["total_assignments"],
                    "escalated_assignments": escalation_stats["escalated_assignments"],
                    "escalation_rate": (escalation_stats["escalated_assignments"] / 
                                      max(1, escalation_stats["total_assignments"])),
                    "avg_acknowledgment_time_hours": float(escalation_stats["avg_acknowledgment_time"]) if escalation_stats["avg_acknowledgment_time"] else 0.0,
                    "avg_first_contact_time_hours": float(escalation_stats["avg_first_contact_time"]) if escalation_stats["avg_first_contact_time"] else 0.0
                },
                "system_metrics": self.assignment_metrics
            }
            
        except Exception as e:
            logger.error(f"Error getting assignment analytics: {e}")
            return {}
    
    async def reassign_lead(self, lead_id: str, new_rep_id: Optional[str] = None, 
                           reason: str = "manual_reassignment") -> Optional[LeadAssignment]:
        """Reassign a lead to a different representative"""
        try:
            # Get current assignment
            async with self.db_pool.acquire() as conn:
                current_assignment = await conn.fetchrow("""
                    SELECT * FROM lead_assignments 
                    WHERE lead_id = $1 
                    ORDER BY assigned_at DESC 
                    LIMIT 1
                """, lead_id)
                
                if not current_assignment:
                    logger.error(f"No existing assignment found for lead {lead_id}")
                    return None
                
                # Get lead data
                lead_row = await conn.fetchrow("SELECT * FROM leads WHERE lead_id = $1", lead_id)
                if not lead_row:
                    logger.error(f"Lead {lead_id} not found")
                    return None
                
                lead_data = dict(lead_row)
                
                # Update workload for previous rep
                await self._update_rep_workload(current_assignment["rep_id"], -1)
                
                # Mark previous assignment as reassigned
                await conn.execute("""
                    UPDATE lead_assignments SET
                        metadata = metadata || '{"reassigned": true, "reassigned_at": "' || NOW() || '", "reassignment_reason": "' || $2 || '"}'
                    WHERE assignment_id = $1
                """, current_assignment["assignment_id"], reason)
                
            # Create new assignment
            if new_rep_id:
                # Manual reassignment
                new_assignment = await self._manual_assignment(lead_id, lead_data, new_rep_id)
            else:
                # Automatic reassignment
                new_assignment = await self.assign_lead(lead_id, lead_data)
            
            if new_assignment:
                logger.info(f"Lead {lead_id} reassigned from {current_assignment['rep_id']} to {new_assignment.rep_id}")
            
            return new_assignment
            
        except Exception as e:
            logger.error(f"Error reassigning lead {lead_id}: {e}")
            return None
    
    async def get_rep_workload(self, rep_id: str) -> Dict[str, Any]:
        """Get current workload information for a sales representative"""
        try:
            if rep_id not in self.sales_reps:
                return {}
            
            rep = self.sales_reps[rep_id]
            
            async with self.db_pool.acquire() as conn:
                # Get detailed workload stats
                stats = await conn.fetchrow("""
                    SELECT 
                        COUNT(CASE WHEN l.status NOT IN ('closed_won', 'closed_lost') THEN 1 END) as active_leads,
                        COUNT(CASE WHEN DATE(la.assigned_at) = CURRENT_DATE THEN 1 END) as leads_today,
                        AVG(la.assignment_score) as avg_assignment_score,
                        COUNT(CASE WHEN la.priority = 'urgent' THEN 1 END) as urgent_leads,
                        COUNT(CASE WHEN la.priority = 'high' THEN 1 END) as high_priority_leads
                    FROM lead_assignments la
                    JOIN leads l ON la.lead_id = l.lead_id
                    WHERE la.rep_id = $1
                    AND la.assigned_at > NOW() - INTERVAL '30 days'
                """, rep_id)
            
            workload_score = self.workload_balancer.calculate_workload_score(rep)
            performance_score = self.workload_balancer.calculate_performance_score(rep)
            
            return {
                "rep_id": rep_id,
                "name": rep.name,
                "status": rep.status.value,
                "active_leads": stats["active_leads"] or 0,
                "leads_today": stats["leads_today"] or 0,
                "max_concurrent_leads": rep.max_concurrent_leads,
                "max_daily_leads": rep.max_daily_leads,
                "capacity_utilization": (stats["active_leads"] or 0) / rep.max_concurrent_leads,
                "daily_utilization": (stats["leads_today"] or 0) / rep.max_daily_leads,
                "workload_score": workload_score,
                "performance_score": performance_score,
                "avg_assignment_score": float(stats["avg_assignment_score"]) if stats["avg_assignment_score"] else 0.0,
                "urgent_leads": stats["urgent_leads"] or 0,
                "high_priority_leads": stats["high_priority_leads"] or 0,
                "last_assignment": rep.last_assignment.isoformat() if rep.last_assignment else None
            }
            
        except Exception as e:
            logger.error(f"Error getting workload for rep {rep_id}: {e}")
            return {}
    
    async def cleanup(self):
        """Cleanup resources"""
        try:
            if hasattr(self, 'db_pool'):
                await self.db_pool.close()
            if hasattr(self, 'redis'):
                await self.redis.close()
            logger.info("Lead assignment system cleanup completed")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

# Example usage and testing
async def main():
    """Example usage of the lead assignment system"""
    
    # Configuration
    db_config = {
        "host": "localhost",
        "port": 5432,
        "database": "bizosaas",
        "user": "postgres",
        "password": "password"
    }
    
    redis_config = {
        "host": "localhost",
        "port": 6379
    }
    
    # Initialize system
    assignment_system = LeadAssignmentSystem(db_config, redis_config)
    await assignment_system.initialize()
    
    try:
        # Sample lead data
        lead_data = {
            "lead_id": "lead_456",
            "company_name": "TechStart Inc",
            "company_size": 75,
            "industry": "technology",
            "location": "San Francisco, CA",
            "budget": 35000,
            "service_requirements": ["marketing automation", "crm"],
            "total_score": 85
        }
        
        # Assign lead
        assignment = await assignment_system.assign_lead(
            lead_data["lead_id"], 
            lead_data,
            strategy=AssignmentStrategy.HYBRID
        )
        
        if assignment:
            print(f"Assignment Result:")
            print(f"Lead ID: {assignment.lead_id}")
            print(f"Rep ID: {assignment.rep_id}")
            print(f"Strategy: {assignment.strategy_used.value}")
            print(f"Priority: {assignment.priority.value}")
            print(f"Assignment Score: {assignment.assignment_score:.2f}")
            print(f"Skill Match: {assignment.skill_match_score:.2f}")
            print(f"Territory Match: {assignment.territory_match_score:.2f}")
        
        # Get analytics
        analytics = await assignment_system.get_assignment_analytics()
        print(f"\nAssignment Analytics:")
        print(json.dumps(analytics, indent=2, default=str))
        
    finally:
        await assignment_system.cleanup()

if __name__ == "__main__":
    asyncio.run(main())