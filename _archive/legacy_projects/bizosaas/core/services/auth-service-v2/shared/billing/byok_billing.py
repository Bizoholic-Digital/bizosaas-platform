"""
BYOK-Aware Billing Service
Handles different pricing models based on credential strategy
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from decimal import Decimal
from dataclasses import dataclass
from enum import Enum

from shared.credential_management import BillingModel, CredentialStrategy

logger = logging.getLogger(__name__)


class UsageType(Enum):
    """Types of billable usage"""
    API_CALL = "api_call"
    CAMPAIGN_EXECUTION = "campaign_execution"
    LEAD_PROCESSING = "lead_processing"
    REPORT_GENERATION = "report_generation"
    STORAGE_GB = "storage_gb"
    BANDWIDTH_GB = "bandwidth_gb"


@dataclass
class UsageRecord:
    """Individual usage record for billing"""
    tenant_id: str
    platform: str
    usage_type: UsageType
    quantity: int
    credential_strategy: CredentialStrategy
    billing_model: BillingModel
    unit_cost: Decimal
    total_cost: Decimal
    timestamp: datetime
    metadata: Dict[str, Any] = None


@dataclass
class BillingTier:
    """Billing tier configuration"""
    name: str
    billing_model: BillingModel
    monthly_base_fee: Decimal
    usage_rates: Dict[UsageType, Decimal]
    included_quotas: Dict[UsageType, int]
    overage_multiplier: Decimal = Decimal('1.0')


@dataclass
class TenantBill:
    """Complete billing information for a tenant"""
    tenant_id: str
    billing_period_start: datetime
    billing_period_end: datetime
    base_fees: Dict[str, Decimal]  # platform -> base fee
    usage_charges: List[UsageRecord]
    total_base_fees: Decimal
    total_usage_charges: Decimal
    total_amount: Decimal
    currency: str = "USD"


class BYOKBillingService:
    """
    BYOK-aware billing service that handles different pricing models:
    
    1. BYOK Tier (Discounted): Lower cost, tenant provides API keys
    2. Platform Tier (Full Service): Higher cost, platform provides keys
    3. Usage-Based: Pay per API call/usage regardless of key source
    4. Hybrid: Mixed billing based on actual key usage per platform
    """
    
    def __init__(self):
        self.billing_tiers = self._initialize_billing_tiers()
        self.currency = "USD"
    
    def _initialize_billing_tiers(self) -> Dict[BillingModel, BillingTier]:
        """Initialize billing tier configurations"""
        return {
            BillingModel.BYOK_TIER: BillingTier(
                name="BYOK Discounted",
                billing_model=BillingModel.BYOK_TIER,
                monthly_base_fee=Decimal('99.00'),  # Lower base fee
                usage_rates={
                    UsageType.API_CALL: Decimal('0.001'),       # $0.001 per API call
                    UsageType.CAMPAIGN_EXECUTION: Decimal('5.00'),  # $5 per campaign
                    UsageType.LEAD_PROCESSING: Decimal('0.10'),     # $0.10 per lead
                    UsageType.REPORT_GENERATION: Decimal('2.00'),   # $2 per report
                    UsageType.STORAGE_GB: Decimal('0.50'),          # $0.50 per GB
                    UsageType.BANDWIDTH_GB: Decimal('0.25'),        # $0.25 per GB
                },
                included_quotas={
                    UsageType.API_CALL: 10000,           # 10k free API calls
                    UsageType.CAMPAIGN_EXECUTION: 50,    # 50 free campaigns
                    UsageType.LEAD_PROCESSING: 1000,     # 1k free leads
                    UsageType.REPORT_GENERATION: 100,    # 100 free reports
                    UsageType.STORAGE_GB: 10,            # 10GB free storage
                    UsageType.BANDWIDTH_GB: 100,         # 100GB free bandwidth
                }
            ),
            
            BillingModel.PLATFORM_TIER: BillingTier(
                name="Full Service",
                billing_model=BillingModel.PLATFORM_TIER,
                monthly_base_fee=Decimal('299.00'),  # Higher base fee
                usage_rates={
                    UsageType.API_CALL: Decimal('0.002'),       # Higher per API call
                    UsageType.CAMPAIGN_EXECUTION: Decimal('8.00'),  # Higher per campaign
                    UsageType.LEAD_PROCESSING: Decimal('0.15'),     # Higher per lead
                    UsageType.REPORT_GENERATION: Decimal('3.00'),   # Higher per report
                    UsageType.STORAGE_GB: Decimal('0.75'),          # Higher per GB
                    UsageType.BANDWIDTH_GB: Decimal('0.40'),        # Higher per GB
                },
                included_quotas={
                    UsageType.API_CALL: 25000,           # More free API calls
                    UsageType.CAMPAIGN_EXECUTION: 100,   # More free campaigns
                    UsageType.LEAD_PROCESSING: 2500,     # More free leads
                    UsageType.REPORT_GENERATION: 250,    # More free reports
                    UsageType.STORAGE_GB: 25,            # More free storage
                    UsageType.BANDWIDTH_GB: 250,         # More free bandwidth
                }
            ),
            
            BillingModel.USAGE_BASED: BillingTier(
                name="Pay Per Use",
                billing_model=BillingModel.USAGE_BASED,
                monthly_base_fee=Decimal('29.00'),   # Lower base fee
                usage_rates={
                    UsageType.API_CALL: Decimal('0.0015'),      # Middle rate
                    UsageType.CAMPAIGN_EXECUTION: Decimal('6.00'),  # Middle rate
                    UsageType.LEAD_PROCESSING: Decimal('0.12'),     # Middle rate
                    UsageType.REPORT_GENERATION: Decimal('2.50'),   # Middle rate
                    UsageType.STORAGE_GB: Decimal('0.60'),          # Middle rate
                    UsageType.BANDWIDTH_GB: Decimal('0.30'),        # Middle rate
                },
                included_quotas={
                    UsageType.API_CALL: 5000,            # Minimal free tier
                    UsageType.CAMPAIGN_EXECUTION: 10,    # Minimal free campaigns
                    UsageType.LEAD_PROCESSING: 500,      # Minimal free leads
                    UsageType.REPORT_GENERATION: 25,     # Minimal free reports
                    UsageType.STORAGE_GB: 5,             # Minimal free storage
                    UsageType.BANDWIDTH_GB: 50,          # Minimal free bandwidth
                }
            )
        }
    
    def record_usage(
        self, 
        tenant_id: str, 
        platform: str,
        usage_type: UsageType, 
        quantity: int,
        credential_strategy: CredentialStrategy,
        metadata: Optional[Dict[str, Any]] = None
    ) -> UsageRecord:
        """Record billable usage for a tenant"""
        
        # Determine billing model from credential strategy
        billing_model = self._map_strategy_to_billing_model(credential_strategy)
        
        # Get billing tier configuration
        tier = self.billing_tiers[billing_model]
        
        # Calculate cost
        unit_cost = tier.usage_rates.get(usage_type, Decimal('0.00'))
        total_cost = unit_cost * Decimal(str(quantity))
        
        # Create usage record
        usage_record = UsageRecord(
            tenant_id=tenant_id,
            platform=platform,
            usage_type=usage_type,
            quantity=quantity,
            credential_strategy=credential_strategy,
            billing_model=billing_model,
            unit_cost=unit_cost,
            total_cost=total_cost,
            timestamp=datetime.utcnow(),
            metadata=metadata or {}
        )
        
        logger.info(f"Recorded usage: {tenant_id} - {usage_type.value} x{quantity} = ${total_cost}")
        
        # In real implementation, persist to database
        # await self._persist_usage_record(usage_record)
        
        return usage_record
    
    def calculate_monthly_bill(
        self, 
        tenant_id: str, 
        billing_period_start: datetime,
        billing_period_end: datetime,
        usage_records: List[UsageRecord]
    ) -> TenantBill:
        """Calculate complete monthly bill for tenant"""
        
        # Group usage by platform and billing model
        platform_usage = self._group_usage_by_platform(usage_records)
        
        base_fees = {}
        total_base_fees = Decimal('0.00')
        processed_usage = []
        total_usage_charges = Decimal('0.00')
        
        for platform, platform_records in platform_usage.items():
            # Determine primary billing model for this platform
            billing_model = self._get_platform_billing_model(platform_records)
            tier = self.billing_tiers[billing_model]
            
            # Calculate base fee (pro-rated if partial month)
            days_in_period = (billing_period_end - billing_period_start).days
            if days_in_period < 30:
                base_fee = tier.monthly_base_fee * (Decimal(str(days_in_period)) / Decimal('30'))
            else:
                base_fee = tier.monthly_base_fee
            
            base_fees[platform] = base_fee
            total_base_fees += base_fee
            
            # Calculate usage charges with included quotas
            platform_usage_charges = self._calculate_platform_usage_charges(
                platform_records, tier
            )
            
            processed_usage.extend(platform_usage_charges)
            total_usage_charges += sum(record.total_cost for record in platform_usage_charges)
        
        # Create bill
        bill = TenantBill(
            tenant_id=tenant_id,
            billing_period_start=billing_period_start,
            billing_period_end=billing_period_end,
            base_fees=base_fees,
            usage_charges=processed_usage,
            total_base_fees=total_base_fees,
            total_usage_charges=total_usage_charges,
            total_amount=total_base_fees + total_usage_charges,
            currency=self.currency
        )
        
        return bill
    
    def estimate_cost_savings(
        self, 
        tenant_id: str,
        current_strategy: CredentialStrategy,
        proposed_strategy: CredentialStrategy,
        projected_usage: Dict[UsageType, int]
    ) -> Dict[str, Any]:
        """Estimate cost savings from changing credential strategy"""
        
        current_model = self._map_strategy_to_billing_model(current_strategy)
        proposed_model = self._map_strategy_to_billing_model(proposed_strategy)
        
        current_tier = self.billing_tiers[current_model]
        proposed_tier = self.billing_tiers[proposed_model]
        
        # Calculate current costs
        current_base = current_tier.monthly_base_fee
        current_usage_cost = Decimal('0.00')
        
        for usage_type, quantity in projected_usage.items():
            included_quota = current_tier.included_quotas.get(usage_type, 0)
            billable_quantity = max(0, quantity - included_quota)
            unit_cost = current_tier.usage_rates.get(usage_type, Decimal('0.00'))
            current_usage_cost += unit_cost * Decimal(str(billable_quantity))
        
        current_total = current_base + current_usage_cost
        
        # Calculate proposed costs
        proposed_base = proposed_tier.monthly_base_fee
        proposed_usage_cost = Decimal('0.00')
        
        for usage_type, quantity in projected_usage.items():
            included_quota = proposed_tier.included_quotas.get(usage_type, 0)
            billable_quantity = max(0, quantity - included_quota)
            unit_cost = proposed_tier.usage_rates.get(usage_type, Decimal('0.00'))
            proposed_usage_cost += unit_cost * Decimal(str(billable_quantity))
        
        proposed_total = proposed_base + proposed_usage_cost
        
        # Calculate savings
        monthly_savings = current_total - proposed_total
        annual_savings = monthly_savings * Decimal('12')
        savings_percentage = (monthly_savings / current_total * Decimal('100')) if current_total > 0 else Decimal('0')
        
        return {
            "current_strategy": current_strategy.value,
            "proposed_strategy": proposed_strategy.value,
            "current_monthly_cost": float(current_total),
            "proposed_monthly_cost": float(proposed_total),
            "monthly_savings": float(monthly_savings),
            "annual_savings": float(annual_savings),
            "savings_percentage": float(savings_percentage),
            "recommendation": "switch" if monthly_savings > 0 else "stay",
            "breakeven_usage": self._calculate_breakeven_usage(current_tier, proposed_tier)
        }
    
    def get_billing_tier_comparison(self) -> Dict[str, Any]:
        """Get comparison of all billing tiers"""
        comparison = {}
        
        for billing_model, tier in self.billing_tiers.items():
            comparison[billing_model.value] = {
                "name": tier.name,
                "monthly_base_fee": float(tier.monthly_base_fee),
                "usage_rates": {ut.value: float(rate) for ut, rate in tier.usage_rates.items()},
                "included_quotas": {ut.value: quota for ut, quota in tier.included_quotas.items()},
                "best_for": self._get_tier_best_use_case(billing_model)
            }
        
        return comparison
    
    # Helper methods
    
    def _map_strategy_to_billing_model(self, strategy: CredentialStrategy) -> BillingModel:
        """Map credential strategy to billing model"""
        mapping = {
            CredentialStrategy.BYOK: BillingModel.BYOK_TIER,
            CredentialStrategy.PLATFORM: BillingModel.PLATFORM_TIER,
            CredentialStrategy.HYBRID: BillingModel.USAGE_BASED,  # Use usage-based for hybrid
            CredentialStrategy.AUTO: BillingModel.USAGE_BASED
        }
        return mapping.get(strategy, BillingModel.USAGE_BASED)
    
    def _group_usage_by_platform(self, usage_records: List[UsageRecord]) -> Dict[str, List[UsageRecord]]:
        """Group usage records by platform"""
        platform_usage = {}
        for record in usage_records:
            if record.platform not in platform_usage:
                platform_usage[record.platform] = []
            platform_usage[record.platform].append(record)
        return platform_usage
    
    def _get_platform_billing_model(self, platform_records: List[UsageRecord]) -> BillingModel:
        """Determine primary billing model for a platform based on usage"""
        # Use the most common billing model for this platform
        model_counts = {}
        for record in platform_records:
            model = record.billing_model
            model_counts[model] = model_counts.get(model, 0) + 1
        
        return max(model_counts.items(), key=lambda x: x[1])[0]
    
    def _calculate_platform_usage_charges(
        self, 
        platform_records: List[UsageRecord], 
        tier: BillingTier
    ) -> List[UsageRecord]:
        """Calculate usage charges for a platform with included quotas"""
        
        # Aggregate usage by type
        usage_totals = {}
        for record in platform_records:
            usage_type = record.usage_type
            if usage_type not in usage_totals:
                usage_totals[usage_type] = 0
            usage_totals[usage_type] += record.quantity
        
        # Calculate billable usage after included quotas
        processed_records = []
        for usage_type, total_quantity in usage_totals.items():
            included_quota = tier.included_quotas.get(usage_type, 0)
            billable_quantity = max(0, total_quantity - included_quota)
            
            if billable_quantity > 0:
                unit_cost = tier.usage_rates.get(usage_type, Decimal('0.00'))
                total_cost = unit_cost * Decimal(str(billable_quantity))
                
                # Create processed record
                processed_record = UsageRecord(
                    tenant_id=platform_records[0].tenant_id,
                    platform=platform_records[0].platform,
                    usage_type=usage_type,
                    quantity=billable_quantity,
                    credential_strategy=platform_records[0].credential_strategy,
                    billing_model=tier.billing_model,
                    unit_cost=unit_cost,
                    total_cost=total_cost,
                    timestamp=datetime.utcnow(),
                    metadata={"included_quota_used": included_quota}
                )
                processed_records.append(processed_record)
        
        return processed_records
    
    def _calculate_breakeven_usage(self, current_tier: BillingTier, proposed_tier: BillingTier) -> Dict[str, int]:
        """Calculate breakeven usage levels between tiers"""
        breakeven = {}
        
        base_fee_difference = proposed_tier.monthly_base_fee - current_tier.monthly_base_fee
        
        for usage_type in UsageType:
            current_rate = current_tier.usage_rates.get(usage_type, Decimal('0.00'))
            proposed_rate = proposed_tier.usage_rates.get(usage_type, Decimal('0.00'))
            
            rate_difference = current_rate - proposed_rate
            
            if rate_difference != 0:
                breakeven_quantity = abs(base_fee_difference / rate_difference)
                breakeven[usage_type.value] = int(breakeven_quantity)
            else:
                breakeven[usage_type.value] = 0
        
        return breakeven
    
    def _get_tier_best_use_case(self, billing_model: BillingModel) -> str:
        """Get best use case description for billing tier"""
        use_cases = {
            BillingModel.BYOK_TIER: "Best for enterprises with existing API accounts and high security requirements",
            BillingModel.PLATFORM_TIER: "Best for businesses wanting full-service management and premium support",
            BillingModel.USAGE_BASED: "Best for variable usage patterns and cost optimization"
        }
        return use_cases.get(billing_model, "General purpose")


# Global service instance
byok_billing_service: Optional[BYOKBillingService] = None

def get_byok_billing_service() -> BYOKBillingService:
    """Get global BYOK billing service instance"""
    global byok_billing_service
    if not byok_billing_service:
        byok_billing_service = BYOKBillingService()
    return byok_billing_service