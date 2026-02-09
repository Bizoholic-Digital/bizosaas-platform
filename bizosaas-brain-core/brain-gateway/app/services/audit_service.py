from fastapi import Depends
from app.dependencies import get_db
import logging
from uuid import UUID
from typing import Any, Dict, Optional
from sqlalchemy.orm import Session
from app.models.user import AuditLog

logger = logging.getLogger(__name__)

class AuditService:
    def __init__(self, db: Session):
        self.db = db

    async def log_event(
        self,
        user_id: Optional[UUID],
        action: str,
        details: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None
    ):
        """
        Record a security-sensitive event in the audit log.
        """
        try:
            log = AuditLog(
                user_id=user_id,
                action=action,
                details=details,
                ip_address=ip_address
            )
            self.db.add(log)
            self.db.commit()
            self.db.refresh(log)
            
            logger.info(f"AUDIT: [{action}] by user {user_id} - {details}")
            return log
        except Exception as e:
            logger.error(f"Failed to write audit log: {e}")
            # We don't want audit logging failure to crash the main request, 
            # but in a production SOC2 environment, this might be a critical failure.
            # For now, we log the error and continue.
            return None

def get_audit_service(db: Session = Depends(get_db)):
    return AuditService(db)
