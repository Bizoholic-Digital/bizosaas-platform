#!/usr/bin/env python3

"""
BizOSaaS Data Synchronization - Conflict Resolution Module
Handles data conflicts and version control across platforms
"""

import logging
import json
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List, Tuple
from enum import Enum
from dataclasses import dataclass

logger = logging.getLogger(__name__)

class ConflictType(str, Enum):
    VERSION_CONFLICT = "version_conflict"
    DATA_MISMATCH = "data_mismatch"
    CONCURRENT_UPDATE = "concurrent_update"
    SCHEMA_CHANGE = "schema_change"
    BUSINESS_RULE_VIOLATION = "business_rule_violation"

class ResolutionStrategy(str, Enum):
    LATEST_WINS = "latest_wins"
    SOURCE_WINS = "source_wins"
    MERGE_SMART = "merge_smart"
    MANUAL_REVIEW = "manual_review"
    CUSTOM_LOGIC = "custom_logic"

@dataclass
class ConflictContext:
    conflict_id: str
    conflict_type: ConflictType
    source_platform: str
    target_platform: str
    entity_type: str
    entity_id: str
    tenant_id: str
    source_data: Dict[str, Any]
    target_data: Dict[str, Any]
    source_timestamp: datetime
    target_timestamp: datetime
    metadata: Dict[str, Any]

@dataclass
class ResolutionResult:
    conflict_id: str
    strategy_used: ResolutionStrategy
    resolved_data: Dict[str, Any]
    confidence_score: float
    requires_manual_review: bool
    resolution_notes: str
    applied_rules: List[str]

class ConflictResolver:
    """Handles data conflicts between platforms"""
    
    def __init__(self, db_pool, redis_client):
        self.db_pool = db_pool
        self.redis_client = redis_client
        self.resolution_rules = self._load_resolution_rules()
    
    def _load_resolution_rules(self) -> Dict[str, Any]:
        """Load conflict resolution rules"""
        return {
            "user": {
                "email": {"strategy": ResolutionStrategy.SOURCE_WINS, "critical": True},
                "name": {"strategy": ResolutionStrategy.LATEST_WINS, "critical": False},
                "profile_data": {"strategy": ResolutionStrategy.MERGE_SMART, "critical": False},
                "preferences": {"strategy": ResolutionStrategy.MERGE_SMART, "critical": False}
            },
            "lead": {
                "status": {"strategy": ResolutionStrategy.LATEST_WINS, "critical": True},
                "score": {"strategy": ResolutionStrategy.CUSTOM_LOGIC, "critical": True},
                "contact_info": {"strategy": ResolutionStrategy.SOURCE_WINS, "critical": True},
                "notes": {"strategy": ResolutionStrategy.MERGE_SMART, "critical": False}
            },
            "order": {
                "status": {"strategy": ResolutionStrategy.LATEST_WINS, "critical": True},
                "amount": {"strategy": ResolutionStrategy.SOURCE_WINS, "critical": True},
                "items": {"strategy": ResolutionStrategy.MERGE_SMART, "critical": True},
                "shipping_info": {"strategy": ResolutionStrategy.LATEST_WINS, "critical": False}
            },
            "product": {
                "price": {"strategy": ResolutionStrategy.LATEST_WINS, "critical": True},
                "inventory": {"strategy": ResolutionStrategy.CUSTOM_LOGIC, "critical": True},
                "description": {"strategy": ResolutionStrategy.MERGE_SMART, "critical": False},
                "images": {"strategy": ResolutionStrategy.MERGE_SMART, "critical": False}
            }
        }
    
    async def detect_conflict(self, 
                            source_data: Dict[str, Any], 
                            target_data: Dict[str, Any],
                            entity_type: str,
                            entity_id: str,
                            source_platform: str,
                            target_platform: str,
                            tenant_id: str) -> Optional[ConflictContext]:
        """Detect if there's a conflict between source and target data"""
        
        conflicts = []
        
        # Check for version conflicts
        source_version = source_data.get("version", 0)
        target_version = target_data.get("version", 0)
        source_timestamp = self._parse_timestamp(source_data.get("updated_at"))
        target_timestamp = self._parse_timestamp(target_data.get("updated_at"))
        
        if source_version != target_version:
            conflicts.append(ConflictType.VERSION_CONFLICT)
        
        # Check for data mismatches in critical fields
        entity_rules = self.resolution_rules.get(entity_type, {})
        for field, rule in entity_rules.items():
            if rule.get("critical", False):
                source_value = source_data.get(field)
                target_value = target_data.get(field)
                
                if source_value != target_value:
                    conflicts.append(ConflictType.DATA_MISMATCH)
                    break
        
        # Check for concurrent updates (within 30 seconds)
        if source_timestamp and target_timestamp:
            time_diff = abs((source_timestamp - target_timestamp).total_seconds())
            if time_diff < 30:
                conflicts.append(ConflictType.CONCURRENT_UPDATE)
        
        # Check for business rule violations
        business_violations = await self._check_business_rules(
            source_data, target_data, entity_type, tenant_id
        )
        if business_violations:
            conflicts.append(ConflictType.BUSINESS_RULE_VIOLATION)
        
        if conflicts:
            conflict_id = f"conflict_{entity_type}_{entity_id}_{int(datetime.now().timestamp())}"
            
            return ConflictContext(
                conflict_id=conflict_id,
                conflict_type=conflicts[0],  # Primary conflict type
                source_platform=source_platform,
                target_platform=target_platform,
                entity_type=entity_type,
                entity_id=entity_id,
                tenant_id=tenant_id,
                source_data=source_data,
                target_data=target_data,
                source_timestamp=source_timestamp or datetime.now(timezone.utc),
                target_timestamp=target_timestamp or datetime.now(timezone.utc),
                metadata={"all_conflicts": conflicts}
            )
        
        return None
    
    async def resolve_conflict(self, context: ConflictContext) -> ResolutionResult:
        """Resolve data conflict using appropriate strategy"""
        
        # Store conflict for audit trail
        await self._store_conflict(context)
        
        # Determine resolution strategy
        strategy = self._determine_strategy(context)
        
        # Apply resolution strategy
        if strategy == ResolutionStrategy.LATEST_WINS:
            result = await self._resolve_latest_wins(context)
        elif strategy == ResolutionStrategy.SOURCE_WINS:
            result = await self._resolve_source_wins(context)
        elif strategy == ResolutionStrategy.MERGE_SMART:
            result = await self._resolve_merge_smart(context)
        elif strategy == ResolutionStrategy.CUSTOM_LOGIC:
            result = await self._resolve_custom_logic(context)
        else:
            result = await self._resolve_manual_review(context)
        
        # Store resolution result
        await self._store_resolution(result)
        
        return result
    
    def _determine_strategy(self, context: ConflictContext) -> ResolutionStrategy:
        """Determine the best resolution strategy for the conflict"""
        
        # Check if manual review is required for critical conflicts
        if context.conflict_type == ConflictType.BUSINESS_RULE_VIOLATION:
            return ResolutionStrategy.MANUAL_REVIEW
        
        # Use entity-specific rules
        entity_rules = self.resolution_rules.get(context.entity_type, {})
        
        # For complex conflicts, prefer manual review
        if len(context.metadata.get("all_conflicts", [])) > 2:
            return ResolutionStrategy.MANUAL_REVIEW
        
        # Default to latest wins for most cases
        return ResolutionStrategy.LATEST_WINS
    
    async def _resolve_latest_wins(self, context: ConflictContext) -> ResolutionResult:
        """Resolve conflict by using the most recent data"""
        
        if context.source_timestamp >= context.target_timestamp:
            resolved_data = context.source_data.copy()
            notes = f"Used source data (more recent: {context.source_timestamp})"
        else:
            resolved_data = context.target_data.copy()
            notes = f"Used target data (more recent: {context.target_timestamp})"
        
        # Increment version
        resolved_data["version"] = max(
            context.source_data.get("version", 0),
            context.target_data.get("version", 0)
        ) + 1
        resolved_data["updated_at"] = datetime.now(timezone.utc).isoformat()
        
        return ResolutionResult(
            conflict_id=context.conflict_id,
            strategy_used=ResolutionStrategy.LATEST_WINS,
            resolved_data=resolved_data,
            confidence_score=0.9,
            requires_manual_review=False,
            resolution_notes=notes,
            applied_rules=["latest_timestamp_wins"]
        )
    
    async def _resolve_source_wins(self, context: ConflictContext) -> ResolutionResult:
        """Resolve conflict by using source platform data"""
        
        resolved_data = context.source_data.copy()
        resolved_data["version"] = max(
            context.source_data.get("version", 0),
            context.target_data.get("version", 0)
        ) + 1
        resolved_data["updated_at"] = datetime.now(timezone.utc).isoformat()
        
        return ResolutionResult(
            conflict_id=context.conflict_id,
            strategy_used=ResolutionStrategy.SOURCE_WINS,
            resolved_data=resolved_data,
            confidence_score=0.8,
            requires_manual_review=False,
            resolution_notes=f"Source platform ({context.source_platform}) data takes precedence",
            applied_rules=["source_platform_priority"]
        )
    
    async def _resolve_merge_smart(self, context: ConflictContext) -> ResolutionResult:
        """Resolve conflict by intelligently merging data"""
        
        resolved_data = {}
        applied_rules = []
        
        # Start with newer base data
        if context.source_timestamp >= context.target_timestamp:
            resolved_data = context.source_data.copy()
        else:
            resolved_data = context.target_data.copy()
        
        # Merge specific fields based on rules
        entity_rules = self.resolution_rules.get(context.entity_type, {})
        
        for field in set(context.source_data.keys()) | set(context.target_data.keys()):
            source_value = context.source_data.get(field)
            target_value = context.target_data.get(field)
            
            if source_value is None:
                resolved_data[field] = target_value
            elif target_value is None:
                resolved_data[field] = source_value
            elif source_value == target_value:
                resolved_data[field] = source_value
            else:
                # Field-specific merge logic
                if field in entity_rules:
                    rule = entity_rules[field]
                    if rule["strategy"] == ResolutionStrategy.LATEST_WINS:
                        if context.source_timestamp >= context.target_timestamp:
                            resolved_data[field] = source_value
                        else:
                            resolved_data[field] = target_value
                        applied_rules.append(f"{field}_latest_wins")
                    elif rule["strategy"] == ResolutionStrategy.SOURCE_WINS:
                        resolved_data[field] = source_value
                        applied_rules.append(f"{field}_source_wins")
                    else:
                        # Smart merge for complex fields
                        merged_value = await self._merge_field_values(
                            field, source_value, target_value, context.entity_type
                        )
                        resolved_data[field] = merged_value
                        applied_rules.append(f"{field}_smart_merge")
                else:
                    # Default: use newer value
                    if context.source_timestamp >= context.target_timestamp:
                        resolved_data[field] = source_value
                    else:
                        resolved_data[field] = target_value
                    applied_rules.append(f"{field}_default_newer")
        
        # Update metadata
        resolved_data["version"] = max(
            context.source_data.get("version", 0),
            context.target_data.get("version", 0)
        ) + 1
        resolved_data["updated_at"] = datetime.now(timezone.utc).isoformat()
        
        return ResolutionResult(
            conflict_id=context.conflict_id,
            strategy_used=ResolutionStrategy.MERGE_SMART,
            resolved_data=resolved_data,
            confidence_score=0.85,
            requires_manual_review=False,
            resolution_notes="Intelligently merged conflicting fields",
            applied_rules=applied_rules
        )
    
    async def _resolve_custom_logic(self, context: ConflictContext) -> ResolutionResult:
        """Resolve conflict using custom business logic"""
        
        entity_type = context.entity_type
        resolved_data = context.source_data.copy()
        applied_rules = []
        
        if entity_type == "lead":
            # Lead scoring logic
            source_score = context.source_data.get("score", 0)
            target_score = context.target_data.get("score", 0)
            
            # Use higher score, but consider recency
            if abs(source_score - target_score) > 10:
                if source_score > target_score:
                    resolved_data["score"] = source_score
                    applied_rules.append("higher_lead_score_wins")
                else:
                    resolved_data["score"] = target_score
                    applied_rules.append("higher_lead_score_wins")
            else:
                # Scores are close, use newer data
                if context.source_timestamp >= context.target_timestamp:
                    resolved_data["score"] = source_score
                else:
                    resolved_data["score"] = target_score
                applied_rules.append("recent_score_for_close_values")
        
        elif entity_type == "product":
            # Inventory logic - sum quantities from different platforms
            source_inventory = context.source_data.get("inventory", 0)
            target_inventory = context.target_data.get("inventory", 0)
            
            # For inventory, we might want to sync separately
            # For now, use the maximum available
            resolved_data["inventory"] = max(source_inventory, target_inventory)
            applied_rules.append("max_inventory_wins")
        
        # Update metadata
        resolved_data["version"] = max(
            context.source_data.get("version", 0),
            context.target_data.get("version", 0)
        ) + 1
        resolved_data["updated_at"] = datetime.now(timezone.utc).isoformat()
        
        return ResolutionResult(
            conflict_id=context.conflict_id,
            strategy_used=ResolutionStrategy.CUSTOM_LOGIC,
            resolved_data=resolved_data,
            confidence_score=0.95,
            requires_manual_review=False,
            resolution_notes=f"Applied custom business logic for {entity_type}",
            applied_rules=applied_rules
        )
    
    async def _resolve_manual_review(self, context: ConflictContext) -> ResolutionResult:
        """Mark conflict for manual review"""
        
        # Store both versions for manual review
        resolved_data = {
            "conflict_status": "pending_manual_review",
            "source_data": context.source_data,
            "target_data": context.target_data,
            "conflict_id": context.conflict_id,
            "requires_action": True
        }
        
        return ResolutionResult(
            conflict_id=context.conflict_id,
            strategy_used=ResolutionStrategy.MANUAL_REVIEW,
            resolved_data=resolved_data,
            confidence_score=0.0,
            requires_manual_review=True,
            resolution_notes="Conflict requires manual review due to business rule violation",
            applied_rules=["manual_review_required"]
        )
    
    async def _merge_field_values(self, field: str, source_value: Any, target_value: Any, entity_type: str) -> Any:
        """Smart merge logic for specific field types"""
        
        # Handle different data types
        if isinstance(source_value, dict) and isinstance(target_value, dict):
            # Merge dictionaries
            merged = target_value.copy()
            merged.update(source_value)
            return merged
        
        elif isinstance(source_value, list) and isinstance(target_value, list):
            # Merge lists (remove duplicates)
            combined = source_value + target_value
            if all(isinstance(item, str) for item in combined):
                return list(set(combined))
            else:
                return combined
        
        elif field == "tags" or field == "categories":
            # Special handling for tags/categories
            source_tags = source_value if isinstance(source_value, list) else [source_value]
            target_tags = target_value if isinstance(target_value, list) else [target_value]
            return list(set(source_tags + target_tags))
        
        else:
            # Default: return source value
            return source_value
    
    async def _check_business_rules(self, source_data: Dict[str, Any], target_data: Dict[str, Any], 
                                  entity_type: str, tenant_id: str) -> List[str]:
        """Check for business rule violations"""
        violations = []
        
        if entity_type == "order":
            # Order amount shouldn't change dramatically
            source_amount = source_data.get("total_amount", 0)
            target_amount = target_data.get("total_amount", 0)
            
            if abs(source_amount - target_amount) > 100:  # $100 threshold
                violations.append("order_amount_significant_change")
        
        elif entity_type == "user":
            # Email changes need verification
            source_email = source_data.get("email", "")
            target_email = target_data.get("email", "")
            
            if source_email != target_email:
                violations.append("email_change_requires_verification")
        
        return violations
    
    def _parse_timestamp(self, timestamp_str: Optional[str]) -> Optional[datetime]:
        """Parse timestamp string to datetime object"""
        if not timestamp_str:
            return None
        
        try:
            if isinstance(timestamp_str, datetime):
                return timestamp_str
            return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            return None
    
    async def _store_conflict(self, context: ConflictContext):
        """Store conflict information for audit trail"""
        try:
            async with self.db_pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO sync_conflicts (
                        conflict_id, conflict_type, source_platform, target_platform,
                        entity_type, entity_id, tenant_id, source_data, target_data,
                        source_timestamp, target_timestamp, metadata, created_at
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
                """, context.conflict_id, context.conflict_type.value, context.source_platform,
                context.target_platform, context.entity_type, context.entity_id,
                context.tenant_id, json.dumps(context.source_data), 
                json.dumps(context.target_data), context.source_timestamp,
                context.target_timestamp, json.dumps(context.metadata),
                datetime.now(timezone.utc))
        except Exception as e:
            logger.error(f"Failed to store conflict: {e}")
    
    async def _store_resolution(self, result: ResolutionResult):
        """Store conflict resolution result"""
        try:
            async with self.db_pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO sync_conflict_resolutions (
                        conflict_id, strategy_used, resolved_data, confidence_score,
                        requires_manual_review, resolution_notes, applied_rules, created_at
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                """, result.conflict_id, result.strategy_used.value,
                json.dumps(result.resolved_data), result.confidence_score,
                result.requires_manual_review, result.resolution_notes,
                json.dumps(result.applied_rules), datetime.now(timezone.utc))
        except Exception as e:
            logger.error(f"Failed to store resolution: {e}")

async def create_conflict_tables(db_pool):
    """Create conflict resolution tables"""
    try:
        async with db_pool.acquire() as conn:
            # Create conflicts table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS sync_conflicts (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    conflict_id VARCHAR(255) UNIQUE NOT NULL,
                    conflict_type VARCHAR(100) NOT NULL,
                    source_platform VARCHAR(50) NOT NULL,
                    target_platform VARCHAR(50) NOT NULL,
                    entity_type VARCHAR(100) NOT NULL,
                    entity_id VARCHAR(255) NOT NULL,
                    tenant_id UUID NOT NULL,
                    source_data JSONB NOT NULL,
                    target_data JSONB NOT NULL,
                    source_timestamp TIMESTAMP WITH TIME ZONE,
                    target_timestamp TIMESTAMP WITH TIME ZONE,
                    metadata JSONB DEFAULT '{}',
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                );
            """)
            
            # Create resolutions table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS sync_conflict_resolutions (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    conflict_id VARCHAR(255) NOT NULL,
                    strategy_used VARCHAR(50) NOT NULL,
                    resolved_data JSONB NOT NULL,
                    confidence_score FLOAT NOT NULL,
                    requires_manual_review BOOLEAN NOT NULL,
                    resolution_notes TEXT,
                    applied_rules JSONB DEFAULT '[]',
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    FOREIGN KEY (conflict_id) REFERENCES sync_conflicts(conflict_id)
                );
            """)
            
            # Create indexes
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_conflicts_entity ON sync_conflicts(entity_type, entity_id);")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_conflicts_tenant ON sync_conflicts(tenant_id);")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_resolutions_conflict ON sync_conflict_resolutions(conflict_id);")
            
            logger.info("✅ Conflict resolution tables created successfully")
    except Exception as e:
        logger.error(f"❌ Failed to create conflict tables: {e}")