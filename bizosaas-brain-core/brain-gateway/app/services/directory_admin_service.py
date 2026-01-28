"""
Directory Task Management Service
Handles administrative tasks for the Business Directory, including SEO optimization,
claim verification audits, and directory crawling configurations.
"""

import logging
from typing import Dict, Any, List, Optional
from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.directory import DirectoryListing, DirectoryClaimRequest
from app.services.directory_service import DirectoryService

logger = logging.getLogger(__name__)

class DirectoryTaskService:
    """
    Service for administrative management of Directory AI tasks.
    Enables fine-tuning and oversight of autonomous directory operations.
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.directory_service = DirectoryService(db)
        
    async def run_seo_audit(self, listing_ids: Optional[List[UUID]] = None) -> Dict[str, Any]:
        """
        Trigger an SEO optimization audit for specified listings or a sample of unoptimized listings.
        """
        if not listing_ids:
            # Pick top 10 listings missing meta descriptions or descriptions
            unoptimized = self.db.query(DirectoryListing).filter(
                (DirectoryListing.description == None) | (DirectoryListing.meta_description == None)
            ).limit(10).all()
            listing_ids = [l.id for l in unoptimized]
            
        results = []
        for lid in listing_ids:
            try:
                # Reuse the existing optimize_listing_seo method from DirectoryService
                optimization = await self.directory_service.optimize_listing_seo(lid)
                results.append({"listing_id": str(lid), "status": "optimized", "data": optimization})
            except Exception as e:
                logger.error(f"SEO audit failed for {lid}: {e}")
                results.append({"listing_id": str(lid), "status": "failed", "error": str(e)})
                
        return {
            "task": "seo_audit",
            "timestamp": datetime.utcnow().isoformat(),
            "processed": len(results),
            "results": results
        }
    
    async def audit_pending_claims(self) -> Dict[str, Any]:
        """
        Review all pending claim requests and flag potential issues or auto-approve based on verification.
        """
        claims = self.db.query(DirectoryClaimRequest).filter(
            DirectoryClaimRequest.status == 'pending'
        ).all()
        
        audited = []
        for claim in claims:
            # Intelligent verification logic could be added here
            # For now, we identify claims where verification expiry is near or reached
            status = "pending"
            if claim.verification_expiry and datetime.utcnow() > claim.verification_expiry:
                status = "expired"
            
            audited.append({
                "claim_id": str(claim.id),
                "listing_id": str(claim.listing_id),
                "user_id": str(claim.user_id),
                "status": status,
                "verification_method": claim.verification_method,
                "created_at": claim.created_at.isoformat() if claim.created_at else None
            })
            
        return {
            "task": "claim_audit",
            "pending_count": len(claims),
            "audited_claims": audited
        }

    async def approve_claim(self, claim_id: UUID, admin_id: UUID) -> Dict[str, Any]:
        """
        Approve a business claim request and transfer ownership of the listing.
        """
        claim = self.db.query(DirectoryClaimRequest).filter(DirectoryClaimRequest.id == claim_id).first()
        if not claim:
            raise ValueError("Claim request not found")
        
        if claim.status != 'pending':
            raise ValueError(f"Claim is already {claim.status}")

        # Update Claim Status
        claim.status = 'approved'
        claim.reviewed_by = admin_id
        claim.reviewed_at = datetime.utcnow()

        # Update Listing Ownership
        listing = self.db.query(DirectoryListing).filter(DirectoryListing.id == claim.listing_id).first()
        if listing:
            listing.claimed = True
            listing.claimed_by = claim.user_id
            listing.claimed_at = datetime.utcnow()
            listing.verification_status = "verified"

        self.db.commit()
        return {"status": "success", "claim_id": str(claim_id), "listing_id": str(claim.listing_id)}

    async def reject_claim(self, claim_id: UUID, admin_id: UUID, reason: str) -> Dict[str, Any]:
        """
        Reject a business claim request with a reason.
        """
        claim = self.db.query(DirectoryClaimRequest).filter(DirectoryClaimRequest.id == claim_id).first()
        if not claim:
            raise ValueError("Claim request not found")
        
        claim.status = 'rejected'
        claim.reviewed_by = admin_id
        claim.reviewed_at = datetime.utcnow()
        claim.rejection_reason = reason

        self.db.commit()
        return {"status": "success", "claim_id": str(claim_id)}

    async def get_crawling_stats(self) -> Dict[str, Any]:
        """
        Fetch statistics about the directory's autonomous growth (ghost listings, sync rates).
        """
        total = self.db.query(DirectoryListing).count()
        ghosts = self.db.query(DirectoryListing).filter(DirectoryListing.claimed == False).count()
        synced_recently = self.db.query(DirectoryListing).filter(
            DirectoryListing.last_synced_at >= datetime.utcnow() - timedelta(days=7)
        ).count()
        
        # Add pending claims count
        pending_claims = self.db.query(DirectoryClaimRequest).filter(DirectoryClaimRequest.status == 'pending').count()
        
        return {
            "total_listings": total,
            "autonomous_listings": ghosts,
            "claimed_listings": total - ghosts,
            "pending_claims": pending_claims,
            "sync_rate_7d": (synced_recently / total * 100) if total > 0 else 0
        }

class DirectoryFineTuner:
    """
    Manages fine-tuning configurations for directory agents.
    Allows admins to override default AI behavior.
    """
    
    # Global overrides in memory (in production, use Redis or a config table)
    _config = {
        "seo_model": "gpt-4o-mini",
        "seo_prompt_template": "Optimize this listing focusing on high-intent local keywords.",
        "crawl_depth_limit": 5,
        "auto_approve_verified": True,
        "claim_expiry_minutes": 60
    }
    
    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        return cls._config
        
    @classmethod
    def update_config(cls, new_config: Dict[str, Any]) -> Dict[str, Any]:
        cls._config.update(new_config)
        return cls._config
