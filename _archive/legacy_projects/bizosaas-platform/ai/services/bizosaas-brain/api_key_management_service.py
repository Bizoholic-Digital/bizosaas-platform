"""
Secure API Key Management Service for BizOSaaS Brain
Handles enterprise-grade API key generation, validation, storage, and rotation
"""
import asyncio
import secrets
import string
import hashlib
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import aiohttp
import re

# Import Vault client
from vault_client import VaultClient, get_vault_client

logger = logging.getLogger(__name__)

class SecurityLevel(Enum):
    BASIC = "basic"
    ENHANCED = "enhanced"
    ENTERPRISE = "enterprise"

class KeyStatus(Enum):
    GENERATING = "generating"
    GENERATED = "generated"
    VALIDATED = "validated"
    STORED = "stored"
    ACTIVE = "active"
    ROTATING = "rotating"
    EXPIRED = "expired"
    REVOKED = "revoked"
    ERROR = "error"

class ServiceCategory(Enum):
    PAYMENT = "payment"
    MARKETING = "marketing"
    AI = "ai"
    ANALYTICS = "analytics"
    INFRASTRUCTURE = "infrastructure"
    ECOMMERCE = "ecommerce"
    EMAIL = "email"

@dataclass
class KeyConfiguration:
    """Configuration for generating specific API keys"""
    service_id: str
    key_type: str
    prefix: str
    length: int
    description: str
    pattern: Optional[str] = None
    validation_endpoint: Optional[str] = None
    required_scopes: List[str] = None
    expiry_days: Optional[int] = None

@dataclass
class GeneratedAPIKey:
    """Represents a generated API key with metadata"""
    key_id: str
    tenant_id: str
    service_id: str
    service_name: str
    key_type: str
    key_value: str
    masked_value: str
    status: KeyStatus
    strength_score: int
    security_level: SecurityLevel
    created_at: datetime
    expires_at: Optional[datetime]
    last_rotated_at: Optional[datetime]
    usage_count: int = 0
    vault_path: Optional[str] = None
    backup_vault_path: Optional[str] = None
    metadata: Dict[str, Any] = None

@dataclass
class KeyValidationResult:
    """Result of key validation"""
    is_valid: bool
    strength_score: int
    entropy_score: float
    issues: List[str]
    recommendations: List[str]
    compliance_status: Dict[str, bool]

@dataclass
class SecurityConfiguration:
    """Security configuration for key generation"""
    environment: str
    security_level: SecurityLevel
    key_rotation_policy: str
    custom_rotation_days: Optional[int]
    require_two_factor: bool
    ip_whitelist: List[str]
    geo_restrictions: List[str]
    permission_level: str
    encryption_algorithm: str = "AES-256"
    backup_enabled: bool = True

# Comprehensive service catalog with key configurations
SERVICE_CATALOG = {
    # Payment Services
    "stripe": {
        "name": "Stripe",
        "category": ServiceCategory.PAYMENT,
        "keys": [
            KeyConfiguration("stripe", "publishable_key", "pk_", 107, "Client-side public key"),
            KeyConfiguration("stripe", "secret_key", "sk_", 107, "Server-side secret key"),
            KeyConfiguration("stripe", "webhook_secret", "whsec_", 64, "Webhook endpoint verification"),
        ],
        "validation_endpoint": "https://api.stripe.com/v1/payment_methods",
        "compliance": ["PCI-DSS", "SOC2", "GDPR"]
    },
    "paypal": {
        "name": "PayPal",
        "category": ServiceCategory.PAYMENT,
        "keys": [
            KeyConfiguration("paypal", "client_id", "", 80, "PayPal application client ID"),
            KeyConfiguration("paypal", "client_secret", "", 80, "PayPal application secret"),
        ],
        "validation_endpoint": "https://api.paypal.com/v1/identity/oauth2/token",
        "compliance": ["PCI-DSS", "SOC2"]
    },
    "razorpay": {
        "name": "Razorpay",
        "category": ServiceCategory.PAYMENT,
        "keys": [
            KeyConfiguration("razorpay", "key_id", "rzp_", 24, "Razorpay key identifier"),
            KeyConfiguration("razorpay", "key_secret", "", 32, "Razorpay secret key"),
        ],
        "validation_endpoint": "https://api.razorpay.com/v1/payments",
        "compliance": ["PCI-DSS", "RBI"]
    },
    
    # Marketing Services
    "google-ads": {
        "name": "Google Ads",
        "category": ServiceCategory.MARKETING,
        "keys": [
            KeyConfiguration("google-ads", "developer_token", "", 22, "Google Ads developer token"),
            KeyConfiguration("google-ads", "client_id", "", 72, "OAuth 2.0 client ID"),
            KeyConfiguration("google-ads", "client_secret", "", 24, "OAuth 2.0 client secret"),
            KeyConfiguration("google-ads", "refresh_token", "", 64, "OAuth 2.0 refresh token"),
        ],
        "validation_endpoint": "https://googleads.googleapis.com/v14/customers",
        "compliance": ["SOC2", "GDPR"]
    },
    "facebook-ads": {
        "name": "Meta Ads",
        "category": ServiceCategory.MARKETING,
        "keys": [
            KeyConfiguration("facebook-ads", "app_id", "", 16, "Facebook app identifier"),
            KeyConfiguration("facebook-ads", "app_secret", "", 32, "Facebook app secret"),
            KeyConfiguration("facebook-ads", "access_token", "", 195, "Facebook access token"),
        ],
        "validation_endpoint": "https://graph.facebook.com/v18.0/me/adaccounts",
        "compliance": ["SOC2", "GDPR"]
    },
    
    # AI Services
    "openai": {
        "name": "OpenAI",
        "category": ServiceCategory.AI,
        "keys": [
            KeyConfiguration("openai", "api_key", "sk-", 51, "OpenAI API secret key"),
            KeyConfiguration("openai", "organization", "org-", 28, "Organization identifier"),
        ],
        "validation_endpoint": "https://api.openai.com/v1/models",
        "compliance": ["SOC2", "GDPR"]
    },
    "anthropic": {
        "name": "Anthropic Claude",
        "category": ServiceCategory.AI,
        "keys": [
            KeyConfiguration("anthropic", "api_key", "sk-ant-", 108, "Anthropic API key"),
        ],
        "validation_endpoint": "https://api.anthropic.com/v1/messages",
        "compliance": ["SOC2", "GDPR"]
    },
    
    # Analytics Services
    "google-analytics": {
        "name": "Google Analytics",
        "category": ServiceCategory.ANALYTICS,
        "keys": [
            KeyConfiguration("google-analytics", "measurement_id", "G-", 11, "GA4 measurement ID"),
            KeyConfiguration("google-analytics", "api_secret", "", 22, "Measurement Protocol secret"),
        ],
        "validation_endpoint": "https://analyticsreporting.googleapis.com/v4/reports:batchGet",
        "compliance": ["SOC2", "GDPR"]
    },
    
    # Infrastructure Services
    "aws-s3": {
        "name": "AWS S3",
        "category": ServiceCategory.INFRASTRUCTURE,
        "keys": [
            KeyConfiguration("aws-s3", "access_key", "AKIA", 20, "AWS access key ID"),
            KeyConfiguration("aws-s3", "secret_key", "", 40, "AWS secret access key"),
            KeyConfiguration("aws-s3", "region", "", 15, "AWS region identifier"),
        ],
        "validation_endpoint": "https://s3.amazonaws.com",
        "compliance": ["SOC2", "GDPR", "HIPAA"]
    }
}

class APIKeyManager:
    """Enterprise-grade API Key Management System"""
    
    def __init__(self, vault_client: VaultClient = None):
        self.vault = vault_client or get_vault_client()
        self.encryption_key = self._get_or_create_encryption_key()
        self.cipher = Fernet(self.encryption_key)
    
    def _get_or_create_encryption_key(self) -> bytes:
        """Get or create encryption key for local encryption"""
        try:
            # Try to get key from Vault
            vault_data = self.vault.get_secret("bizosaas/encryption/api-keys")
            if vault_data and "key" in vault_data:
                return vault_data["key"].encode()
        except Exception as e:
            logger.warning(f"Could not retrieve encryption key from Vault: {e}")
        
        # Generate new key
        key = Fernet.generate_key()
        
        # Store in Vault
        try:
            self.vault.put_secret("bizosaas/encryption/api-keys", {"key": key.decode()})
        except Exception as e:
            logger.error(f"Could not store encryption key in Vault: {e}")
        
        return key
    
    async def generate_api_keys(
        self,
        tenant_id: str,
        service_ids: List[str],
        security_config: SecurityConfiguration
    ) -> List[GeneratedAPIKey]:
        """Generate API keys for multiple services"""
        generated_keys = []
        
        for service_id in service_ids:
            if service_id not in SERVICE_CATALOG:
                logger.warning(f"Service {service_id} not found in catalog")
                continue
            
            service_config = SERVICE_CATALOG[service_id]
            
            for key_config in service_config["keys"]:
                try:
                    api_key = await self._generate_single_key(
                        tenant_id, service_config, key_config, security_config
                    )
                    generated_keys.append(api_key)
                    
                    # Generate backup key for enterprise security
                    if security_config.security_level == SecurityLevel.ENTERPRISE:
                        backup_key = await self._generate_backup_key(api_key, security_config)
                        if backup_key:
                            generated_keys.append(backup_key)
                            
                except Exception as e:
                    logger.error(f"Failed to generate key for {service_id}.{key_config.key_type}: {e}")
                    # Create error record
                    error_key = GeneratedAPIKey(
                        key_id=self._generate_key_id(),
                        tenant_id=tenant_id,
                        service_id=service_id,
                        service_name=service_config["name"],
                        key_type=key_config.key_type,
                        key_value="",
                        masked_value="ERROR",
                        status=KeyStatus.ERROR,
                        strength_score=0,
                        security_level=security_config.security_level,
                        created_at=datetime.utcnow(),
                        expires_at=None,
                        last_rotated_at=None,
                        metadata={"error": str(e)}
                    )
                    generated_keys.append(error_key)
        
        return generated_keys
    
    async def _generate_single_key(
        self,
        tenant_id: str,
        service_config: Dict,
        key_config: KeyConfiguration,
        security_config: SecurityConfiguration
    ) -> GeneratedAPIKey:
        """Generate a single API key"""
        
        # Generate the key value
        key_value = self._generate_secure_key(
            key_config.prefix,
            key_config.length,
            security_config.security_level
        )
        
        # Validate the key
        validation_result = await self._validate_key(key_value, key_config, service_config)
        
        # Calculate expiration
        expires_at = self._calculate_expiration(security_config)
        
        # Create API key object
        api_key = GeneratedAPIKey(
            key_id=self._generate_key_id(),
            tenant_id=tenant_id,
            service_id=key_config.service_id,
            service_name=service_config["name"],
            key_type=key_config.key_type,
            key_value=key_value,
            masked_value=self._mask_key(key_value),
            status=KeyStatus.GENERATED if validation_result.is_valid else KeyStatus.ERROR,
            strength_score=validation_result.strength_score,
            security_level=security_config.security_level,
            created_at=datetime.utcnow(),
            expires_at=expires_at,
            last_rotated_at=None,
            metadata={
                "validation": asdict(validation_result),
                "security_config": asdict(security_config),
                "compliance": service_config.get("compliance", [])
            }
        )
        
        # Store in Vault
        await self._store_key_in_vault(api_key, security_config)
        
        return api_key
    
    def _generate_secure_key(self, prefix: str, length: int, security_level: SecurityLevel) -> str:
        """Generate cryptographically secure API key"""
        
        # Determine character set based on security level
        if security_level == SecurityLevel.ENTERPRISE:
            # Maximum entropy for enterprise
            chars = string.ascii_letters + string.digits + "-_"
        elif security_level == SecurityLevel.ENHANCED:
            # Good entropy for enhanced
            chars = string.ascii_letters + string.digits
        else:
            # Basic entropy for basic security
            chars = string.ascii_letters + string.digits
        
        # Calculate remaining length after prefix
        remaining_length = length - len(prefix)
        
        # Generate random portion
        random_part = ''.join(secrets.choice(chars) for _ in range(remaining_length))
        
        # Combine prefix and random part
        return prefix + random_part
    
    async def _validate_key(
        self,
        key_value: str,
        key_config: KeyConfiguration,
        service_config: Dict
    ) -> KeyValidationResult:
        """Validate generated API key"""
        
        issues = []
        recommendations = []
        
        # Basic validation
        if len(key_value) < key_config.length:
            issues.append(f"Key length {len(key_value)} is less than required {key_config.length}")
        
        # Pattern validation
        if key_config.pattern and not re.match(key_config.pattern, key_value):
            issues.append(f"Key does not match required pattern: {key_config.pattern}")
        
        # Strength calculation
        strength_score = self._calculate_key_strength(key_value)
        
        # Entropy calculation
        entropy_score = self._calculate_entropy(key_value)
        
        # Compliance checks
        compliance_status = {}
        for compliance in service_config.get("compliance", []):
            compliance_status[compliance] = self._check_compliance(key_value, compliance)
        
        # Recommendations based on analysis
        if strength_score < 80:
            recommendations.append("Consider using a longer key for better security")
        
        if entropy_score < 4.0:
            recommendations.append("Increase character variety for better entropy")
        
        return KeyValidationResult(
            is_valid=len(issues) == 0,
            strength_score=strength_score,
            entropy_score=entropy_score,
            issues=issues,
            recommendations=recommendations,
            compliance_status=compliance_status
        )
    
    def _calculate_key_strength(self, key: str) -> int:
        """Calculate key strength score (0-100)"""
        score = 0
        
        # Length scoring
        if len(key) >= 64:
            score += 30
        elif len(key) >= 32:
            score += 20
        elif len(key) >= 16:
            score += 10
        
        # Character variety scoring
        if any(c.isupper() for c in key):
            score += 15
        if any(c.islower() for c in key):
            score += 15
        if any(c.isdigit() for c in key):
            score += 15
        if any(c in "-_" for c in key):
            score += 10
        
        # Entropy bonus
        entropy = self._calculate_entropy(key)
        if entropy > 4.5:
            score += 15
        elif entropy > 3.5:
            score += 10
        elif entropy > 2.5:
            score += 5
        
        return min(score, 100)
    
    def _calculate_entropy(self, key: str) -> float:
        """Calculate Shannon entropy of the key"""
        if not key:
            return 0.0
        
        # Count frequency of each character
        freq = {}
        for char in key:
            freq[char] = freq.get(char, 0) + 1
        
        # Calculate entropy
        entropy = 0.0
        key_length = len(key)
        
        for count in freq.values():
            probability = count / key_length
            if probability > 0:
                entropy -= probability * (probability.bit_length() - 1)
        
        return entropy
    
    def _check_compliance(self, key: str, compliance: str) -> bool:
        """Check if key meets specific compliance requirements"""
        
        compliance_rules = {
            "PCI-DSS": len(key) >= 32 and self._calculate_key_strength(key) >= 80,
            "SOC2": len(key) >= 24 and self._calculate_key_strength(key) >= 70,
            "GDPR": len(key) >= 16 and self._calculate_key_strength(key) >= 60,
            "HIPAA": len(key) >= 32 and self._calculate_key_strength(key) >= 85,
            "RBI": len(key) >= 24 and self._calculate_key_strength(key) >= 75
        }
        
        return compliance_rules.get(compliance, True)
    
    def _calculate_expiration(self, security_config: SecurityConfiguration) -> Optional[datetime]:
        """Calculate key expiration date based on rotation policy"""
        
        if security_config.key_rotation_policy == "never":
            return None
        
        days_map = {
            "30-days": 30,
            "60-days": 60,
            "90-days": 90,
            "custom": security_config.custom_rotation_days or 90
        }
        
        days = days_map.get(security_config.key_rotation_policy, 90)
        return datetime.utcnow() + timedelta(days=days)
    
    def _generate_key_id(self) -> str:
        """Generate unique key identifier"""
        return f"key_{secrets.token_hex(16)}"
    
    def _mask_key(self, key: str) -> str:
        """Mask key for display purposes"""
        if len(key) <= 8:
            return "••••••••"
        
        return key[:4] + "••••••••••••••••••••••••••••" + key[-4:]
    
    async def _store_key_in_vault(self, api_key: GeneratedAPIKey, security_config: SecurityConfiguration):
        """Store API key securely in Vault"""
        
        vault_path = f"bizosaas/tenants/{api_key.tenant_id}/api-keys/{api_key.service_id}/{api_key.key_type}"
        
        # Encrypt the key value
        encrypted_value = self.cipher.encrypt(api_key.key_value.encode()).decode()
        
        vault_data = {
            "key_id": api_key.key_id,
            "encrypted_value": encrypted_value,
            "service_id": api_key.service_id,
            "service_name": api_key.service_name,
            "key_type": api_key.key_type,
            "created_at": api_key.created_at.isoformat(),
            "expires_at": api_key.expires_at.isoformat() if api_key.expires_at else None,
            "strength_score": api_key.strength_score,
            "security_level": api_key.security_level.value,
            "metadata": api_key.metadata
        }
        
        try:
            success = self.vault.put_secret(vault_path, vault_data)
            if success:
                api_key.vault_path = vault_path
                api_key.status = KeyStatus.STORED
                logger.info(f"Stored API key {api_key.key_id} in Vault at {vault_path}")
            else:
                logger.error(f"Failed to store API key {api_key.key_id} in Vault")
                api_key.status = KeyStatus.ERROR
        except Exception as e:
            logger.error(f"Error storing API key in Vault: {e}")
            api_key.status = KeyStatus.ERROR
    
    async def _generate_backup_key(
        self, 
        primary_key: GeneratedAPIKey, 
        security_config: SecurityConfiguration
    ) -> Optional[GeneratedAPIKey]:
        """Generate backup key for enterprise security"""
        
        try:
            backup_key = GeneratedAPIKey(
                key_id=self._generate_key_id(),
                tenant_id=primary_key.tenant_id,
                service_id=primary_key.service_id,
                service_name=primary_key.service_name,
                key_type=f"{primary_key.key_type}_backup",
                key_value=self._generate_secure_key(
                    "",  # No prefix for backup keys
                    64,  # Standard backup key length
                    security_config.security_level
                ),
                masked_value="",
                status=KeyStatus.GENERATED,
                strength_score=0,
                security_level=security_config.security_level,
                created_at=datetime.utcnow(),
                expires_at=primary_key.expires_at,
                last_rotated_at=None,
                metadata={
                    "is_backup": True,
                    "primary_key_id": primary_key.key_id,
                    "backup_created_at": datetime.utcnow().isoformat()
                }
            )
            
            # Update masked value and strength
            backup_key.masked_value = self._mask_key(backup_key.key_value)
            backup_key.strength_score = self._calculate_key_strength(backup_key.key_value)
            
            # Store backup key in separate Vault path
            backup_vault_path = f"bizosaas/tenants/{backup_key.tenant_id}/api-keys-backup/{backup_key.service_id}/{backup_key.key_type}"
            
            # Store in Vault
            await self._store_backup_key_in_vault(backup_key, backup_vault_path)
            
            return backup_key
            
        except Exception as e:
            logger.error(f"Failed to generate backup key: {e}")
            return None
    
    async def _store_backup_key_in_vault(self, backup_key: GeneratedAPIKey, vault_path: str):
        """Store backup key in Vault"""
        
        # Encrypt the backup key
        encrypted_value = self.cipher.encrypt(backup_key.key_value.encode()).decode()
        
        vault_data = {
            "key_id": backup_key.key_id,
            "encrypted_value": encrypted_value,
            "service_id": backup_key.service_id,
            "key_type": backup_key.key_type,
            "created_at": backup_key.created_at.isoformat(),
            "expires_at": backup_key.expires_at.isoformat() if backup_key.expires_at else None,
            "strength_score": backup_key.strength_score,
            "metadata": backup_key.metadata
        }
        
        try:
            success = self.vault.put_secret(vault_path, vault_data)
            if success:
                backup_key.backup_vault_path = vault_path
                backup_key.status = KeyStatus.STORED
                logger.info(f"Stored backup key {backup_key.key_id} in Vault")
            else:
                logger.error(f"Failed to store backup key {backup_key.key_id} in Vault")
        except Exception as e:
            logger.error(f"Error storing backup key in Vault: {e}")
    
    async def get_tenant_api_keys(self, tenant_id: str) -> List[GeneratedAPIKey]:
        """Retrieve all API keys for a tenant"""
        
        keys = []
        vault_path_prefix = f"bizosaas/tenants/{tenant_id}/api-keys"
        
        try:
            # This would need to be implemented in the Vault client
            # For now, return empty list
            logger.info(f"Retrieving API keys for tenant {tenant_id}")
            return keys
        except Exception as e:
            logger.error(f"Error retrieving tenant API keys: {e}")
            return []
    
    async def rotate_api_key(self, tenant_id: str, key_id: str) -> Optional[GeneratedAPIKey]:
        """Rotate an existing API key"""
        
        try:
            # This would retrieve the existing key, generate a new one,
            # and update the Vault storage
            logger.info(f"Rotating API key {key_id} for tenant {tenant_id}")
            return None
        except Exception as e:
            logger.error(f"Error rotating API key: {e}")
            return None
    
    async def revoke_api_key(self, tenant_id: str, key_id: str) -> bool:
        """Revoke an API key"""
        
        try:
            # This would mark the key as revoked in Vault
            logger.info(f"Revoking API key {key_id} for tenant {tenant_id}")
            return True
        except Exception as e:
            logger.error(f"Error revoking API key: {e}")
            return False
    
    async def validate_external_key(
        self, 
        service_id: str, 
        key_type: str, 
        key_value: str
    ) -> KeyValidationResult:
        """Validate an externally provided API key"""
        
        if service_id not in SERVICE_CATALOG:
            return KeyValidationResult(
                is_valid=False,
                strength_score=0,
                entropy_score=0.0,
                issues=["Unknown service"],
                recommendations=[],
                compliance_status={}
            )
        
        service_config = SERVICE_CATALOG[service_id]
        key_configs = [k for k in service_config["keys"] if k.key_type == key_type]
        
        if not key_configs:
            return KeyValidationResult(
                is_valid=False,
                strength_score=0,
                entropy_score=0.0,
                issues=["Unknown key type"],
                recommendations=[],
                compliance_status={}
            )
        
        key_config = key_configs[0]
        return await self._validate_key(key_value, key_config, service_config)

# Global instance
api_key_manager = None

def get_api_key_manager() -> APIKeyManager:
    """Get global API Key Manager instance"""
    global api_key_manager
    if api_key_manager is None:
        api_key_manager = APIKeyManager()
    return api_key_manager