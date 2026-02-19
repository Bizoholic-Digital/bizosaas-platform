import logging
import re
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class GovernanceAgent:
    """
    Guardian AI that enforces safety, security, and quality standards 
    on all agent interactions.
    """
    
    def __init__(self):
        # Basic regex patterns for PII detection
        self.pii_patterns = {
            "email_strict": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "phone_us": r"\b(?:\+?1[-. ]?)?\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})\b",
            "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
            "credit_card": r"\b(?:\d{4}[- ]?){3}\d{4}\b"
        }
        
        # Terms that might indicate prompt injection or policy violation
        self.banned_terms = [
            "ignore previous instructions", 
            "system prompt", 
            "internal_api_key",
            "reveal your instructions"
        ]

    async def review_input(self, tenant_id: str, message: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Review user input BEFORE it reaches the agent.
        """
        # 1. Tenant Isolation Check
        if not tenant_id:
            return {"allowed": False, "reason": "Missing tenant context"}

        # 2. Safety/Jailbreak Check
        lower_message = message.lower()
        for term in self.banned_terms:
            if term in lower_message:
                logger.warning(f"Security Alert: Potential jailbreak attempt by tenant {tenant_id}. Term: {term}")
                return {"allowed": False, "reason": "Security violation detected: Input contains restricted terms."}

        return {"allowed": True}

    async def review_output(self, tenant_id: str, agent_output: str) -> Dict[str, Any]:
        """
        Review agent output BEFORE it reaches the user.
        """
        if not agent_output:
            return {"allowed": True}

        # 1. PII Leakage Check
        # We redact PII but also flag it
        redacted_output = agent_output
        pii_found = False
        
        for pii_type, pattern in self.pii_patterns.items():
            if re.search(pattern, redacted_output):
                pii_found = True
                logger.warning(f"Privacy Alert: Agent generated potential {pii_type} for tenant {tenant_id}")
                # Redact
                redacted_output = re.sub(pattern, f"[REDACTED {pii_type.upper()}]", redacted_output)

        if pii_found:
             return {
                "allowed": True, # We allow it but redacted
                "original_content": agent_output,
                "cleaned_content": redacted_output,
                "warnings": ["PII redacted"]
            }

        # 2. Quality Assurance (Basic check)
        # If output is extremely short (e.g. empty or just whitespace/punctuation), might be a failure
        if len(agent_output.strip()) < 2:
             return {"allowed": False, "reason": "Response too short or empty"}

        return {"allowed": True, "cleaned_content": agent_output}

    async def check_budget(self, tenant_id: str, estimated_cost: float) -> bool:
        """
        Check if the tenant has sufficient budget/credits.
        """
        # Placeholder for BillingService integration
        # TODO: Integrate with app.services.billing_service
        if tenant_id == "demo_tenant":
            return True 
            
        return True

# Global instance
governance_agent = GovernanceAgent()
