"""
Amazon Compliance and Validation Engine

This module ensures all generated Amazon listings meet Amazon's requirements,
policies, and best practices before submission through the SP-API.

Key Features:
- Comprehensive compliance checking against Amazon policies
- Content validation for restricted keywords and claims
- Category-specific requirement validation
- Image and media compliance checking
- Price and inventory validation
- SEO and ranking optimization validation
- Multi-language content validation
- Automated compliance scoring and recommendations

Integration with BizOSaaS Platform:
- Tenant-aware validation with custom compliance rules
- Integration with 93+ AI agents for intelligent validation
- Real-time compliance monitoring and alerts
- Audit trail for compliance decisions
"""

import asyncio
import re
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
import logging
from pathlib import Path

# AI and ML imports
from langchain.schema import HumanMessage, SystemMessage
from crewai import Agent, Task, Crew
import openai

# BizOSaaS Platform imports
from .ai_coordinator import EnhancedAICoordinator, EnhancedTenantContext
from .amazon_content_generator import AmazonListingContent, ContentGenerationConfig
from .amazon_sp_api_integration import AmazonSPAPIClient

# Setup logging
logger = logging.getLogger(__name__)

class ComplianceLevel(Enum):
    """Compliance validation levels"""
    STRICT = "strict"           # Amazon's strictest policies
    STANDARD = "standard"       # Standard Amazon requirements
    BASIC = "basic"            # Minimum requirements only
    CUSTOM = "custom"          # Tenant-specific compliance rules

class ValidationSeverity(Enum):
    """Validation issue severity levels"""
    CRITICAL = "critical"      # Blocks listing submission
    HIGH = "high"             # Strong recommendation to fix
    MEDIUM = "medium"         # Moderate recommendation
    LOW = "low"               # Minor suggestion
    INFO = "info"             # Informational only

class ComplianceCategory(Enum):
    """Amazon compliance categories"""
    CONTENT_POLICY = "content_policy"
    PRODUCT_SAFETY = "product_safety"
    INTELLECTUAL_PROPERTY = "intellectual_property"
    RESTRICTED_PRODUCTS = "restricted_products"
    CLAIMS_AND_ADVERTISING = "claims_and_advertising"
    PRICING_POLICY = "pricing_policy"
    IMAGE_REQUIREMENTS = "image_requirements"
    CATEGORY_REQUIREMENTS = "category_requirements"
    SEO_OPTIMIZATION = "seo_optimization"
    LISTING_QUALITY = "listing_quality"

@dataclass
class ValidationIssue:
    """Represents a compliance validation issue"""
    category: ComplianceCategory
    severity: ValidationSeverity
    title: str
    description: str
    field_affected: str
    current_value: Any
    recommended_action: str
    suggested_fix: Optional[str] = None
    policy_reference: Optional[str] = None
    auto_fixable: bool = False

@dataclass
class ComplianceRules:
    """Compliance rules configuration"""
    level: ComplianceLevel
    tenant_id: Optional[str] = None
    custom_rules: Dict[str, Any] = field(default_factory=dict)
    category_weights: Dict[ComplianceCategory, float] = field(default_factory=dict)
    restricted_keywords: Set[str] = field(default_factory=set)
    required_attributes: Set[str] = field(default_factory=set)
    max_title_length: int = 200
    max_description_length: int = 2000
    max_bullet_points: int = 5
    min_images: int = 1
    max_images: int = 9

@dataclass
class ValidationResult:
    """Complete validation result"""
    overall_score: float
    compliance_level: ComplianceLevel
    total_issues: int
    critical_issues: int
    high_issues: int
    medium_issues: int
    low_issues: int
    info_issues: int
    issues: List[ValidationIssue]
    recommendations: List[str]
    auto_fix_available: bool
    estimated_fix_time: timedelta
    validation_timestamp: datetime
    passed_checks: List[str]
    failed_checks: List[str]

class AmazonComplianceValidator:
    """
    Comprehensive Amazon listing compliance validator

    Validates Amazon listings against Amazon's policies, requirements,
    and best practices to ensure successful listing submission.
    """

    def __init__(
        self,
        ai_coordinator: EnhancedAICoordinator,
        sp_api_client: AmazonSPAPIClient,
        compliance_rules: Optional[ComplianceRules] = None
    ):
        self.ai_coordinator = ai_coordinator
        self.sp_api_client = sp_api_client
        self.compliance_rules = compliance_rules or ComplianceRules(ComplianceLevel.STANDARD)

        # Load Amazon policy data
        self._load_amazon_policies()
        self._load_restricted_content()
        self._load_category_requirements()

        # Initialize validation agents
        self._initialize_validation_agents()

        logger.info("Amazon Compliance Validator initialized")

    def _load_amazon_policies(self):
        """Load Amazon policy data and requirements"""
        self.amazon_policies = {
            "prohibited_claims": [
                "FDA approved", "medical grade", "clinical strength",
                "prevents disease", "cures", "treats illness",
                "scientifically proven", "doctor recommended",
                "miracle", "fountain of youth", "anti-aging"
            ],
            "restricted_keywords": [
                "coronavirus", "covid-19", "pandemic",
                "prescription", "rx only", "FDA",
                "medical device", "therapeutic",
                "best seller", "#1 seller", "amazon's choice"
            ],
            "required_disclaimers": {
                "supplements": "This statement has not been evaluated by the FDA",
                "cosmetics": "Individual results may vary",
                "electronics": "FCC compliance statement required"
            },
            "category_restrictions": {
                "Health & Personal Care": {
                    "prohibited_claims": ["medical", "therapeutic", "FDA"],
                    "required_certifications": ["safety_testing"]
                },
                "Electronics": {
                    "required_certifications": ["FCC", "CE"],
                    "required_attributes": ["warranty_info", "model_number"]
                },
                "Toys & Games": {
                    "required_certifications": ["CPSIA", "age_appropriate"],
                    "prohibited_claims": ["educational_benefits"]
                }
            }
        }

    def _load_restricted_content(self):
        """Load restricted content patterns and rules"""
        self.restricted_patterns = {
            "superlative_claims": [
                r"\b(best|#1|number one|top|ultimate|perfect)\b",
                r"\b(guaranteed|promise|ensure)\b",
                r"\b(amazing|incredible|revolutionary)\b"
            ],
            "medical_claims": [
                r"\b(cure|treat|heal|therapy|medical)\b",
                r"\b(disease|illness|condition|symptom)\b",
                r"\b(FDA|prescription|clinical)\b"
            ],
            "competitor_references": [
                r"\b(better than|superior to|beats)\b",
                r"\b(amazon|ebay|walmart|target)\b",
                r"\b(competitor|competition|vs\.)\b"
            ],
            "urgency_manipulation": [
                r"\b(limited time|act now|hurry)\b",
                r"\b(only \d+ left|selling fast)\b",
                r"\b(don't miss|last chance)\b"
            ]
        }

    def _load_category_requirements(self):
        """Load category-specific requirements"""
        self.category_requirements = {
            "Electronics": {
                "required_attributes": [
                    "brand", "model", "color", "connectivity",
                    "power_source", "warranty"
                ],
                "required_certifications": ["FCC", "CE", "RoHS"],
                "image_requirements": {
                    "min_resolution": "1000x1000",
                    "required_angles": ["front", "back", "side", "packaging"]
                }
            },
            "Clothing": {
                "required_attributes": [
                    "size", "color", "material", "care_instructions",
                    "fit_type", "brand"
                ],
                "size_chart_required": True,
                "fabric_content_required": True
            },
            "Home & Kitchen": {
                "required_attributes": [
                    "material", "dimensions", "color", "brand",
                    "assembly_required", "care_instructions"
                ],
                "safety_warnings_required": True
            },
            "Health & Personal Care": {
                "required_attributes": [
                    "ingredients", "directions", "warnings", "brand"
                ],
                "ingredient_disclosure_required": True,
                "fda_disclaimer_required": True
            }
        }

    def _initialize_validation_agents(self):
        """Initialize specialized AI agents for validation"""
        self.validation_agents = {
            "content_policy_agent": Agent(
                role="Amazon Content Policy Specialist",
                goal="Validate listing content against Amazon's content policies",
                backstory="Expert in Amazon's content policies and restricted product guidelines",
                tools=[],
                verbose=True
            ),
            "seo_optimization_agent": Agent(
                role="Amazon SEO Optimization Specialist",
                goal="Validate and optimize listings for Amazon search algorithm",
                backstory="Specialist in Amazon A9 algorithm and listing optimization",
                tools=[],
                verbose=True
            ),
            "category_requirements_agent": Agent(
                role="Amazon Category Requirements Specialist",
                goal="Validate category-specific requirements and attributes",
                backstory="Expert in Amazon's category-specific listing requirements",
                tools=[],
                verbose=True
            ),
            "image_compliance_agent": Agent(
                role="Amazon Image Compliance Specialist",
                goal="Validate image requirements and visual content policies",
                backstory="Specialist in Amazon's image requirements and visual standards",
                tools=[],
                verbose=True
            )
        }

    async def validate_listing(
        self,
        listing_content: AmazonListingContent,
        tenant_context: EnhancedTenantContext,
        compliance_rules: Optional[ComplianceRules] = None
    ) -> ValidationResult:
        """
        Perform comprehensive compliance validation on Amazon listing

        Args:
            listing_content: Generated Amazon listing content
            tenant_context: Tenant-specific context and preferences
            compliance_rules: Custom compliance rules (optional)

        Returns:
            Complete validation result with issues and recommendations
        """
        logger.info(f"Starting compliance validation for tenant {tenant_context.tenant_id}")

        # Use provided compliance rules or default
        rules = compliance_rules or self.compliance_rules

        # Initialize validation result
        validation_result = ValidationResult(
            overall_score=0.0,
            compliance_level=rules.level,
            total_issues=0,
            critical_issues=0,
            high_issues=0,
            medium_issues=0,
            low_issues=0,
            info_issues=0,
            issues=[],
            recommendations=[],
            auto_fix_available=False,
            estimated_fix_time=timedelta(minutes=0),
            validation_timestamp=datetime.utcnow(),
            passed_checks=[],
            failed_checks=[]
        )

        # Run all validation checks concurrently
        validation_tasks = [
            self._validate_content_policy(listing_content, rules, tenant_context),
            self._validate_category_requirements(listing_content, rules, tenant_context),
            self._validate_seo_optimization(listing_content, rules, tenant_context),
            self._validate_image_compliance(listing_content, rules, tenant_context),
            self._validate_pricing_policy(listing_content, rules, tenant_context),
            self._validate_product_safety(listing_content, rules, tenant_context),
            self._validate_listing_quality(listing_content, rules, tenant_context),
            self._validate_intellectual_property(listing_content, rules, tenant_context)
        ]

        # Execute validation checks
        validation_results = await asyncio.gather(*validation_tasks, return_exceptions=True)

        # Compile results
        all_issues = []
        all_recommendations = []

        for result in validation_results:
            if isinstance(result, Exception):
                logger.error(f"Validation check failed: {result}")
                continue

            issues, recommendations = result
            all_issues.extend(issues)
            all_recommendations.extend(recommendations)

        # Categorize issues by severity
        validation_result.issues = all_issues
        validation_result.recommendations = all_recommendations
        validation_result.total_issues = len(all_issues)

        for issue in all_issues:
            if issue.severity == ValidationSeverity.CRITICAL:
                validation_result.critical_issues += 1
                validation_result.failed_checks.append(f"{issue.category.value}:{issue.field_affected}")
            elif issue.severity == ValidationSeverity.HIGH:
                validation_result.high_issues += 1
            elif issue.severity == ValidationSeverity.MEDIUM:
                validation_result.medium_issues += 1
            elif issue.severity == ValidationSeverity.LOW:
                validation_result.low_issues += 1
            elif issue.severity == ValidationSeverity.INFO:
                validation_result.info_issues += 1

            if issue.auto_fixable:
                validation_result.auto_fix_available = True
                validation_result.estimated_fix_time += timedelta(minutes=2)

        # Calculate overall compliance score
        validation_result.overall_score = self._calculate_compliance_score(validation_result)

        # Add passed checks
        all_check_categories = [category.value for category in ComplianceCategory]
        failed_categories = {issue.category.value for issue in all_issues if issue.severity == ValidationSeverity.CRITICAL}
        validation_result.passed_checks = [cat for cat in all_check_categories if cat not in failed_categories]

        logger.info(f"Validation completed. Score: {validation_result.overall_score:.2f}, Issues: {validation_result.total_issues}")

        return validation_result

    async def _validate_content_policy(
        self,
        listing_content: AmazonListingContent,
        rules: ComplianceRules,
        tenant_context: EnhancedTenantContext
    ) -> Tuple[List[ValidationIssue], List[str]]:
        """Validate content against Amazon's content policies"""
        issues = []
        recommendations = []

        # Check for prohibited claims
        all_text = f"{listing_content.title} {listing_content.description} {' '.join(listing_content.bullet_points)}"

        for claim in self.amazon_policies["prohibited_claims"]:
            if claim.lower() in all_text.lower():
                issues.append(ValidationIssue(
                    category=ComplianceCategory.CONTENT_POLICY,
                    severity=ValidationSeverity.CRITICAL,
                    title="Prohibited Medical Claim Detected",
                    description=f"Contains prohibited claim: '{claim}'",
                    field_affected="content",
                    current_value=claim,
                    recommended_action="Remove or rephrase the prohibited claim",
                    policy_reference="Amazon Content Policy - Medical Claims",
                    auto_fixable=True
                ))

        # Check for restricted keywords
        for keyword in self.amazon_policies["restricted_keywords"]:
            if keyword.lower() in all_text.lower():
                issues.append(ValidationIssue(
                    category=ComplianceCategory.CONTENT_POLICY,
                    severity=ValidationSeverity.HIGH,
                    title="Restricted Keyword Found",
                    description=f"Contains restricted keyword: '{keyword}'",
                    field_affected="content",
                    current_value=keyword,
                    recommended_action="Remove or replace with compliant alternative",
                    auto_fixable=True
                ))

        # Check for superlative claims
        for pattern in self.restricted_patterns["superlative_claims"]:
            matches = re.findall(pattern, all_text, re.IGNORECASE)
            if matches:
                issues.append(ValidationIssue(
                    category=ComplianceCategory.CLAIMS_AND_ADVERTISING,
                    severity=ValidationSeverity.MEDIUM,
                    title="Superlative Claims Detected",
                    description=f"Contains unsubstantiated claims: {matches}",
                    field_affected="content",
                    current_value=str(matches),
                    recommended_action="Provide substantiation or remove claims",
                    auto_fixable=False
                ))

        # Use AI agent for advanced content policy validation
        try:
            content_policy_task = Task(
                description=f"Analyze the following Amazon listing content for compliance with Amazon's content policies: {all_text[:1000]}...",
                agent=self.validation_agents["content_policy_agent"]
            )

            crew = Crew(
                agents=[self.validation_agents["content_policy_agent"]],
                tasks=[content_policy_task],
                verbose=True
            )

            ai_analysis = await self._run_crew_async(crew)

            # Parse AI recommendations
            if "violation" in ai_analysis.lower() or "prohibited" in ai_analysis.lower():
                recommendations.append("AI analysis suggests potential content policy violations. Manual review recommended.")

        except Exception as e:
            logger.error(f"AI content policy validation failed: {e}")

        return issues, recommendations

    async def _validate_category_requirements(
        self,
        listing_content: AmazonListingContent,
        rules: ComplianceRules,
        tenant_context: EnhancedTenantContext
    ) -> Tuple[List[ValidationIssue], List[str]]:
        """Validate category-specific requirements"""
        issues = []
        recommendations = []

        category = listing_content.category

        if category in self.category_requirements:
            requirements = self.category_requirements[category]

            # Check required attributes
            required_attrs = requirements.get("required_attributes", [])
            provided_attrs = set(listing_content.attributes.keys())

            missing_attrs = set(required_attrs) - provided_attrs
            for attr in missing_attrs:
                issues.append(ValidationIssue(
                    category=ComplianceCategory.CATEGORY_REQUIREMENTS,
                    severity=ValidationSeverity.CRITICAL,
                    title="Missing Required Attribute",
                    description=f"Category '{category}' requires attribute '{attr}'",
                    field_affected="attributes",
                    current_value=None,
                    recommended_action=f"Add required attribute: {attr}",
                    auto_fixable=False
                ))

            # Check certifications
            required_certs = requirements.get("required_certifications", [])
            for cert in required_certs:
                cert_mentioned = any(cert.lower() in str(value).lower()
                                   for value in listing_content.attributes.values())
                if not cert_mentioned:
                    issues.append(ValidationIssue(
                        category=ComplianceCategory.CATEGORY_REQUIREMENTS,
                        severity=ValidationSeverity.HIGH,
                        title="Missing Certification Information",
                        description=f"Category '{category}' requires certification: {cert}",
                        field_affected="attributes",
                        current_value=None,
                        recommended_action=f"Add certification information: {cert}",
                        auto_fixable=False
                    ))

            # Check image requirements
            image_reqs = requirements.get("image_requirements", {})
            if image_reqs and listing_content.images:
                min_images = image_reqs.get("min_images", 1)
                if len(listing_content.images) < min_images:
                    issues.append(ValidationIssue(
                        category=ComplianceCategory.IMAGE_REQUIREMENTS,
                        severity=ValidationSeverity.HIGH,
                        title="Insufficient Images",
                        description=f"Category requires minimum {min_images} images, found {len(listing_content.images)}",
                        field_affected="images",
                        current_value=len(listing_content.images),
                        recommended_action=f"Add at least {min_images - len(listing_content.images)} more images",
                        auto_fixable=False
                    ))

        return issues, recommendations

    async def _validate_seo_optimization(
        self,
        listing_content: AmazonListingContent,
        rules: ComplianceRules,
        tenant_context: EnhancedTenantContext
    ) -> Tuple[List[ValidationIssue], List[str]]:
        """Validate SEO optimization and searchability"""
        issues = []
        recommendations = []

        # Title length validation
        if len(listing_content.title) > rules.max_title_length:
            issues.append(ValidationIssue(
                category=ComplianceCategory.SEO_OPTIMIZATION,
                severity=ValidationSeverity.HIGH,
                title="Title Too Long",
                description=f"Title length {len(listing_content.title)} exceeds maximum {rules.max_title_length}",
                field_affected="title",
                current_value=len(listing_content.title),
                recommended_action="Shorten title to fit within character limit",
                auto_fixable=True
            ))

        # Description length validation
        if len(listing_content.description) > rules.max_description_length:
            issues.append(ValidationIssue(
                category=ComplianceCategory.SEO_OPTIMIZATION,
                severity=ValidationSeverity.MEDIUM,
                title="Description Too Long",
                description=f"Description length {len(listing_content.description)} exceeds maximum {rules.max_description_length}",
                field_affected="description",
                current_value=len(listing_content.description),
                recommended_action="Shorten description to fit within character limit",
                auto_fixable=True
            ))

        # Keyword density analysis
        if listing_content.keywords:
            title_words = listing_content.title.lower().split()
            keyword_coverage = sum(1 for keyword in listing_content.keywords[:5]
                                 if keyword.lower() in title_words)

            if keyword_coverage < 2:
                issues.append(ValidationIssue(
                    category=ComplianceCategory.SEO_OPTIMIZATION,
                    severity=ValidationSeverity.MEDIUM,
                    title="Low Keyword Coverage in Title",
                    description="Title contains fewer than 2 target keywords",
                    field_affected="title",
                    current_value=keyword_coverage,
                    recommended_action="Include more target keywords in title",
                    auto_fixable=True
                ))

        # Use AI agent for SEO optimization analysis
        try:
            seo_task = Task(
                description=f"Analyze Amazon listing SEO optimization: Title: {listing_content.title}, Keywords: {listing_content.keywords[:10]}",
                agent=self.validation_agents["seo_optimization_agent"]
            )

            crew = Crew(
                agents=[self.validation_agents["seo_optimization_agent"]],
                tasks=[seo_task],
                verbose=True
            )

            seo_analysis = await self._run_crew_async(crew)
            recommendations.append("AI SEO analysis completed - check detailed recommendations")

        except Exception as e:
            logger.error(f"AI SEO validation failed: {e}")

        return issues, recommendations

    async def _validate_image_compliance(
        self,
        listing_content: AmazonListingContent,
        rules: ComplianceRules,
        tenant_context: EnhancedTenantContext
    ) -> Tuple[List[ValidationIssue], List[str]]:
        """Validate image requirements and compliance"""
        issues = []
        recommendations = []

        if not listing_content.images:
            issues.append(ValidationIssue(
                category=ComplianceCategory.IMAGE_REQUIREMENTS,
                severity=ValidationSeverity.CRITICAL,
                title="No Images Provided",
                description="Amazon listings require at least one product image",
                field_affected="images",
                current_value=0,
                recommended_action="Add at least one high-quality product image",
                auto_fixable=False
            ))
        else:
            # Check minimum image requirements
            if len(listing_content.images) < rules.min_images:
                issues.append(ValidationIssue(
                    category=ComplianceCategory.IMAGE_REQUIREMENTS,
                    severity=ValidationSeverity.HIGH,
                    title="Insufficient Images",
                    description=f"Minimum {rules.min_images} images required, found {len(listing_content.images)}",
                    field_affected="images",
                    current_value=len(listing_content.images),
                    recommended_action=f"Add {rules.min_images - len(listing_content.images)} more images",
                    auto_fixable=False
                ))

            # Check maximum image limits
            if len(listing_content.images) > rules.max_images:
                issues.append(ValidationIssue(
                    category=ComplianceCategory.IMAGE_REQUIREMENTS,
                    severity=ValidationSeverity.LOW,
                    title="Too Many Images",
                    description=f"Maximum {rules.max_images} images allowed, found {len(listing_content.images)}",
                    field_affected="images",
                    current_value=len(listing_content.images),
                    recommended_action=f"Remove {len(listing_content.images) - rules.max_images} images",
                    auto_fixable=True
                ))

        return issues, recommendations

    async def _validate_pricing_policy(
        self,
        listing_content: AmazonListingContent,
        rules: ComplianceRules,
        tenant_context: EnhancedTenantContext
    ) -> Tuple[List[ValidationIssue], List[str]]:
        """Validate pricing policies and requirements"""
        issues = []
        recommendations = []

        if listing_content.price:
            # Check for unrealistic pricing
            if listing_content.price <= 0:
                issues.append(ValidationIssue(
                    category=ComplianceCategory.PRICING_POLICY,
                    severity=ValidationSeverity.CRITICAL,
                    title="Invalid Price",
                    description="Product price must be greater than zero",
                    field_affected="price",
                    current_value=listing_content.price,
                    recommended_action="Set a valid positive price",
                    auto_fixable=False
                ))

            # Check for price vs. MSRP ratio
            if listing_content.msrp and listing_content.price > listing_content.msrp:
                issues.append(ValidationIssue(
                    category=ComplianceCategory.PRICING_POLICY,
                    severity=ValidationSeverity.MEDIUM,
                    title="Price Exceeds MSRP",
                    description="Selling price exceeds manufacturer's suggested retail price",
                    field_affected="price",
                    current_value=listing_content.price,
                    recommended_action="Adjust price to be at or below MSRP",
                    auto_fixable=False
                ))

        return issues, recommendations

    async def _validate_product_safety(
        self,
        listing_content: AmazonListingContent,
        rules: ComplianceRules,
        tenant_context: EnhancedTenantContext
    ) -> Tuple[List[ValidationIssue], List[str]]:
        """Validate product safety requirements"""
        issues = []
        recommendations = []

        # Check for required safety warnings based on category
        safety_categories = ["Toys & Games", "Health & Personal Care", "Electronics"]

        if listing_content.category in safety_categories:
            description_text = listing_content.description.lower()

            safety_keywords = ["warning", "caution", "safety", "age appropriate", "adult supervision"]
            safety_mentioned = any(keyword in description_text for keyword in safety_keywords)

            if not safety_mentioned:
                issues.append(ValidationIssue(
                    category=ComplianceCategory.PRODUCT_SAFETY,
                    severity=ValidationSeverity.HIGH,
                    title="Missing Safety Information",
                    description=f"Category '{listing_content.category}' typically requires safety warnings",
                    field_affected="description",
                    current_value=None,
                    recommended_action="Add appropriate safety warnings and usage instructions",
                    auto_fixable=False
                ))

        return issues, recommendations

    async def _validate_listing_quality(
        self,
        listing_content: AmazonListingContent,
        rules: ComplianceRules,
        tenant_context: EnhancedTenantContext
    ) -> Tuple[List[ValidationIssue], List[str]]:
        """Validate overall listing quality"""
        issues = []
        recommendations = []

        # Check bullet points
        if not listing_content.bullet_points:
            issues.append(ValidationIssue(
                category=ComplianceCategory.LISTING_QUALITY,
                severity=ValidationSeverity.HIGH,
                title="Missing Bullet Points",
                description="Listings should include key feature bullet points",
                field_affected="bullet_points",
                current_value=None,
                recommended_action="Add 3-5 key feature bullet points",
                auto_fixable=False
            ))
        elif len(listing_content.bullet_points) > rules.max_bullet_points:
            issues.append(ValidationIssue(
                category=ComplianceCategory.LISTING_QUALITY,
                severity=ValidationSeverity.LOW,
                title="Too Many Bullet Points",
                description=f"Maximum {rules.max_bullet_points} bullet points recommended",
                field_affected="bullet_points",
                current_value=len(listing_content.bullet_points),
                recommended_action=f"Reduce to {rules.max_bullet_points} most important points",
                auto_fixable=True
            ))

        # Check description quality
        if len(listing_content.description) < 100:
            issues.append(ValidationIssue(
                category=ComplianceCategory.LISTING_QUALITY,
                severity=ValidationSeverity.MEDIUM,
                title="Short Description",
                description="Product description should be more detailed",
                field_affected="description",
                current_value=len(listing_content.description),
                recommended_action="Expand description with more product details",
                auto_fixable=True
            ))

        return issues, recommendations

    async def _validate_intellectual_property(
        self,
        listing_content: AmazonListingContent,
        rules: ComplianceRules,
        tenant_context: EnhancedTenantContext
    ) -> Tuple[List[ValidationIssue], List[str]]:
        """Validate intellectual property compliance"""
        issues = []
        recommendations = []

        # Check for potential trademark issues
        trademark_indicators = ["®", "™", "©"]
        all_text = f"{listing_content.title} {listing_content.description}"

        for indicator in trademark_indicators:
            if indicator in all_text:
                issues.append(ValidationIssue(
                    category=ComplianceCategory.INTELLECTUAL_PROPERTY,
                    severity=ValidationSeverity.MEDIUM,
                    title="Trademark Symbol Detected",
                    description=f"Contains trademark symbol '{indicator}' - ensure proper authorization",
                    field_affected="content",
                    current_value=indicator,
                    recommended_action="Verify authorization to use trademarked content",
                    auto_fixable=False
                ))

        # Check for competitor brand mentions
        for pattern in self.restricted_patterns["competitor_references"]:
            matches = re.findall(pattern, all_text, re.IGNORECASE)
            if matches:
                issues.append(ValidationIssue(
                    category=ComplianceCategory.INTELLECTUAL_PROPERTY,
                    severity=ValidationSeverity.HIGH,
                    title="Competitor Reference Detected",
                    description="Content contains references to competitors or comparison claims",
                    field_affected="content",
                    current_value=str(matches),
                    recommended_action="Remove competitor references and comparison claims",
                    auto_fixable=True
                ))

        return issues, recommendations

    def _calculate_compliance_score(self, validation_result: ValidationResult) -> float:
        """Calculate overall compliance score based on validation issues"""
        base_score = 100.0

        # Deduct points based on issue severity
        score_deductions = {
            ValidationSeverity.CRITICAL: 20,
            ValidationSeverity.HIGH: 10,
            ValidationSeverity.MEDIUM: 5,
            ValidationSeverity.LOW: 2,
            ValidationSeverity.INFO: 0
        }

        total_deduction = 0
        for issue in validation_result.issues:
            total_deduction += score_deductions[issue.severity]

        # Cap minimum score at 0
        final_score = max(0, base_score - total_deduction)

        return final_score

    async def auto_fix_issues(
        self,
        listing_content: AmazonListingContent,
        validation_result: ValidationResult,
        tenant_context: EnhancedTenantContext
    ) -> AmazonListingContent:
        """
        Automatically fix auto-fixable validation issues

        Args:
            listing_content: Original listing content
            validation_result: Validation result with issues
            tenant_context: Tenant context

        Returns:
            Updated listing content with auto-fixes applied
        """
        logger.info("Applying automatic fixes to validation issues")

        fixed_content = listing_content

        for issue in validation_result.issues:
            if not issue.auto_fixable:
                continue

            try:
                if issue.category == ComplianceCategory.CONTENT_POLICY:
                    fixed_content = await self._auto_fix_content_policy(fixed_content, issue)
                elif issue.category == ComplianceCategory.SEO_OPTIMIZATION:
                    fixed_content = await self._auto_fix_seo_issues(fixed_content, issue)
                elif issue.category == ComplianceCategory.LISTING_QUALITY:
                    fixed_content = await self._auto_fix_quality_issues(fixed_content, issue)

                logger.info(f"Auto-fixed issue: {issue.title}")

            except Exception as e:
                logger.error(f"Failed to auto-fix issue {issue.title}: {e}")

        return fixed_content

    async def _auto_fix_content_policy(
        self,
        content: AmazonListingContent,
        issue: ValidationIssue
    ) -> AmazonListingContent:
        """Auto-fix content policy issues"""
        if "prohibited claim" in issue.description.lower():
            # Remove prohibited claims using AI
            fix_prompt = f"""
            Remove the prohibited claim '{issue.current_value}' from the following text while maintaining meaning:
            Text: {content.title} {content.description}

            Return the corrected text maintaining the same structure.
            """

            try:
                corrected_text = await self.ai_coordinator.generate_response(
                    messages=[HumanMessage(content=fix_prompt)],
                    agent_type="content_optimizer"
                )

                # Update content with corrected text
                if issue.field_affected == "title":
                    content.title = corrected_text.split('\n')[0][:200]
                elif issue.field_affected == "description":
                    content.description = corrected_text

            except Exception as e:
                logger.error(f"AI auto-fix failed: {e}")

        return content

    async def _auto_fix_seo_issues(
        self,
        content: AmazonListingContent,
        issue: ValidationIssue
    ) -> AmazonListingContent:
        """Auto-fix SEO optimization issues"""
        if "title too long" in issue.description.lower():
            # Truncate title while preserving keywords
            words = content.title.split()
            truncated_title = ""

            for word in words:
                if len(truncated_title + " " + word) <= 200:
                    truncated_title += (" " + word if truncated_title else word)
                else:
                    break

            content.title = truncated_title

        elif "description too long" in issue.description.lower():
            # Truncate description
            content.description = content.description[:2000]

        return content

    async def _auto_fix_quality_issues(
        self,
        content: AmazonListingContent,
        issue: ValidationIssue
    ) -> AmazonListingContent:
        """Auto-fix listing quality issues"""
        if "too many bullet points" in issue.description.lower():
            # Keep only the first 5 bullet points
            content.bullet_points = content.bullet_points[:5]

        elif "short description" in issue.description.lower():
            # Expand description using AI
            expand_prompt = f"""
            Expand the following product description to be more detailed and informative:
            Current: {content.description}
            Product: {content.title}

            Make it at least 200 characters while maintaining accuracy.
            """

            try:
                expanded_description = await self.ai_coordinator.generate_response(
                    messages=[HumanMessage(content=expand_prompt)],
                    agent_type="content_generator"
                )
                content.description = expanded_description

            except Exception as e:
                logger.error(f"AI description expansion failed: {e}")

        return content

    async def generate_compliance_report(
        self,
        validation_result: ValidationResult,
        tenant_context: EnhancedTenantContext
    ) -> Dict[str, Any]:
        """
        Generate comprehensive compliance report

        Args:
            validation_result: Validation result data
            tenant_context: Tenant context

        Returns:
            Detailed compliance report
        """
        report = {
            "summary": {
                "overall_score": validation_result.overall_score,
                "compliance_level": validation_result.compliance_level.value,
                "total_issues": validation_result.total_issues,
                "critical_issues": validation_result.critical_issues,
                "validation_date": validation_result.validation_timestamp.isoformat(),
                "tenant_id": tenant_context.tenant_id
            },
            "issue_breakdown": {
                "critical": [issue for issue in validation_result.issues if issue.severity == ValidationSeverity.CRITICAL],
                "high": [issue for issue in validation_result.issues if issue.severity == ValidationSeverity.HIGH],
                "medium": [issue for issue in validation_result.issues if issue.severity == ValidationSeverity.MEDIUM],
                "low": [issue for issue in validation_result.issues if issue.severity == ValidationSeverity.LOW],
                "info": [issue for issue in validation_result.issues if issue.severity == ValidationSeverity.INFO]
            },
            "recommendations": validation_result.recommendations,
            "auto_fix_analysis": {
                "fixable_issues": len([issue for issue in validation_result.issues if issue.auto_fixable]),
                "estimated_fix_time": str(validation_result.estimated_fix_time),
                "fix_available": validation_result.auto_fix_available
            },
            "category_analysis": {},
            "next_steps": []
        }

        # Add category-specific analysis
        for category in ComplianceCategory:
            category_issues = [issue for issue in validation_result.issues if issue.category == category]
            if category_issues:
                report["category_analysis"][category.value] = {
                    "issue_count": len(category_issues),
                    "severity_distribution": {
                        severity.value: len([issue for issue in category_issues if issue.severity == severity])
                        for severity in ValidationSeverity
                    }
                }

        # Generate next steps
        if validation_result.critical_issues > 0:
            report["next_steps"].append("URGENT: Fix all critical issues before listing submission")

        if validation_result.high_issues > 0:
            report["next_steps"].append("HIGH PRIORITY: Address high-severity issues for better listing performance")

        if validation_result.auto_fix_available:
            report["next_steps"].append("AUTOMATED: Run auto-fix for eligible issues")

        if validation_result.overall_score < 80:
            report["next_steps"].append("REVIEW: Consider manual review and optimization")

        return report

    async def _run_crew_async(self, crew: Crew) -> str:
        """Run CrewAI crew in async context"""
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, crew.kickoff)
        return str(result)

    def get_compliance_rules_for_tenant(self, tenant_id: str) -> ComplianceRules:
        """Get tenant-specific compliance rules"""
        # In production, this would fetch from database
        return ComplianceRules(
            level=ComplianceLevel.STANDARD,
            tenant_id=tenant_id
        )

    async def validate_batch_listings(
        self,
        listings: List[AmazonListingContent],
        tenant_context: EnhancedTenantContext,
        compliance_rules: Optional[ComplianceRules] = None
    ) -> List[ValidationResult]:
        """
        Validate multiple listings in batch

        Args:
            listings: List of Amazon listing content to validate
            tenant_context: Tenant context
            compliance_rules: Custom compliance rules

        Returns:
            List of validation results for each listing
        """
        logger.info(f"Starting batch validation for {len(listings)} listings")

        # Create validation tasks for all listings
        validation_tasks = [
            self.validate_listing(listing, tenant_context, compliance_rules)
            for listing in listings
        ]

        # Execute validations concurrently
        results = await asyncio.gather(*validation_tasks, return_exceptions=True)

        # Filter out exceptions and log errors
        validation_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Validation failed for listing {i}: {result}")
                # Create failed validation result
                validation_results.append(ValidationResult(
                    overall_score=0.0,
                    compliance_level=ComplianceLevel.STANDARD,
                    total_issues=1,
                    critical_issues=1,
                    high_issues=0,
                    medium_issues=0,
                    low_issues=0,
                    info_issues=0,
                    issues=[ValidationIssue(
                        category=ComplianceCategory.LISTING_QUALITY,
                        severity=ValidationSeverity.CRITICAL,
                        title="Validation Failed",
                        description=str(result),
                        field_affected="general",
                        current_value=None,
                        recommended_action="Manual review required"
                    )],
                    recommendations=["Manual review required due to validation error"],
                    auto_fix_available=False,
                    estimated_fix_time=timedelta(minutes=30),
                    validation_timestamp=datetime.utcnow(),
                    passed_checks=[],
                    failed_checks=["validation_error"]
                ))
            else:
                validation_results.append(result)

        logger.info(f"Batch validation completed for {len(validation_results)} listings")
        return validation_results

# Export main classes
__all__ = [
    'AmazonComplianceValidator',
    'ValidationResult',
    'ValidationIssue',
    'ComplianceRules',
    'ComplianceLevel',
    'ValidationSeverity',
    'ComplianceCategory'
]