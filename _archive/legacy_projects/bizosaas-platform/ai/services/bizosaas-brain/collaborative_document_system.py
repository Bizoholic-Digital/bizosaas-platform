"""
Collaborative Document Editing System for BizOSaaS Platform
Provides real-time collaborative editing capabilities with AI assistance
"""

import asyncio
import json
import structlog
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Set, Tuple
from uuid import UUID, uuid4
from enum import Enum
from dataclasses import dataclass, field
from pydantic import BaseModel, Field

import asyncpg
from difflib import unified_diff

from enhanced_tenant_context import EnhancedTenantContext, PlatformType
from shared.rls_manager import RLSManager
from realtime_collaboration_service import CollaborationEventType, CollaborationScope

logger = structlog.get_logger(__name__)


class DocumentType(str, Enum):
    """Types of collaborative documents"""
    CAMPAIGN_BRIEF = "campaign_brief"
    CONTENT_STRATEGY = "content_strategy"
    SEO_REPORT = "seo_report"
    SOCIAL_MEDIA_PLAN = "social_media_plan"
    WEBSITE_AUDIT = "website_audit"
    MARKET_RESEARCH = "market_research"
    COMPETITOR_ANALYSIS = "competitor_analysis"
    BRAND_GUIDELINES = "brand_guidelines"
    EMAIL_TEMPLATE = "email_template"
    AD_COPY = "ad_copy"
    BLOG_POST = "blog_post"
    LANDING_PAGE = "landing_page"
    GENERAL_DOCUMENT = "general_document"


class OperationType(str, Enum):
    """Types of document operations"""
    INSERT = "insert"
    DELETE = "delete"
    REPLACE = "replace"
    FORMAT = "format"
    COMMENT = "comment"
    SUGGESTION = "suggestion"


class ConflictResolution(str, Enum):
    """Conflict resolution strategies"""
    LAST_WRITE_WINS = "last_write_wins"
    OPERATIONAL_TRANSFORM = "operational_transform"
    MERGE_STRATEGIES = "merge_strategies"
    USER_CHOICE = "user_choice"


@dataclass
class DocumentOperation:
    """Represents a single document operation"""
    operation_id: str = field(default_factory=lambda: str(uuid4()))
    operation_type: OperationType = OperationType.INSERT
    position: int = 0
    length: int = 0
    content: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    user_id: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    parent_operation_id: Optional[str] = None


@dataclass
class DocumentState:
    """Current state of a collaborative document"""
    content: str = ""
    version: int = 0
    operations: List[DocumentOperation] = field(default_factory=list)
    last_modified: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    checksum: str = ""


class CollaborativeDocument(BaseModel):
    """Collaborative document model"""
    document_id: str = Field(default_factory=lambda: str(uuid4()))
    tenant_id: str
    platform: PlatformType
    document_type: DocumentType
    title: str
    description: Optional[str] = None
    content: str = ""
    version: int = 0
    created_by: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Collaboration settings
    is_public: bool = False
    allowed_editors: List[str] = Field(default_factory=list)
    allowed_viewers: List[str] = Field(default_factory=list)
    conflict_resolution: ConflictResolution = ConflictResolution.OPERATIONAL_TRANSFORM
    auto_save_interval: int = 30  # seconds

    # Document state
    current_state: DocumentState = Field(default_factory=DocumentState)

    # AI assistance
    ai_suggestions_enabled: bool = True
    ai_auto_complete: bool = True
    ai_grammar_check: bool = True

    # Metadata
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class OperationalTransform:
    """
    Operational Transform implementation for conflict resolution
    """

    @staticmethod
    def transform_operations(
        op1: DocumentOperation,
        op2: DocumentOperation
    ) -> Tuple[DocumentOperation, DocumentOperation]:
        """
        Transform two concurrent operations to maintain consistency
        """
        # Create copies to avoid modifying original operations
        transformed_op1 = DocumentOperation(
            operation_id=op1.operation_id,
            operation_type=op1.operation_type,
            position=op1.position,
            length=op1.length,
            content=op1.content,
            metadata=op1.metadata.copy(),
            user_id=op1.user_id,
            timestamp=op1.timestamp
        )

        transformed_op2 = DocumentOperation(
            operation_id=op2.operation_id,
            operation_type=op2.operation_type,
            position=op2.position,
            length=op2.length,
            content=op2.content,
            metadata=op2.metadata.copy(),
            user_id=op2.user_id,
            timestamp=op2.timestamp
        )

        # Transform based on operation types
        if op1.operation_type == OperationType.INSERT and op2.operation_type == OperationType.INSERT:
            if op1.position <= op2.position:
                transformed_op2.position += len(op1.content)
            else:
                transformed_op1.position += len(op2.content)

        elif op1.operation_type == OperationType.DELETE and op2.operation_type == OperationType.DELETE:
            if op1.position < op2.position:
                transformed_op2.position -= op1.length
            elif op1.position > op2.position:
                transformed_op1.position -= op2.length
            else:
                # Same position - keep both but adjust lengths
                min_length = min(op1.length, op2.length)
                transformed_op1.length = max(0, op1.length - min_length)
                transformed_op2.length = max(0, op2.length - min_length)

        elif op1.operation_type == OperationType.INSERT and op2.operation_type == OperationType.DELETE:
            if op1.position <= op2.position:
                transformed_op2.position += len(op1.content)
            elif op1.position <= op2.position + op2.length:
                # Insert is within delete range
                transformed_op2.length += len(op1.content)

        elif op1.operation_type == OperationType.DELETE and op2.operation_type == OperationType.INSERT:
            if op2.position <= op1.position:
                transformed_op1.position += len(op2.content)
            elif op2.position <= op1.position + op1.length:
                # Insert is within delete range
                transformed_op1.length += len(op2.content)

        return transformed_op1, transformed_op2

    @staticmethod
    def apply_operation(content: str, operation: DocumentOperation) -> str:
        """
        Apply a document operation to content
        """
        try:
            if operation.operation_type == OperationType.INSERT:
                return content[:operation.position] + operation.content + content[operation.position:]

            elif operation.operation_type == OperationType.DELETE:
                end_pos = operation.position + operation.length
                return content[:operation.position] + content[end_pos:]

            elif operation.operation_type == OperationType.REPLACE:
                end_pos = operation.position + operation.length
                return content[:operation.position] + operation.content + content[end_pos:]

            else:
                # For FORMAT, COMMENT, SUGGESTION - don't modify content
                return content

        except Exception as e:
            logger.error(
                "Error applying operation",
                operation_id=operation.operation_id,
                error=str(e)
            )
            return content


class CollaborativeDocumentManager:
    """
    Manager for collaborative document operations
    """

    def __init__(self, rls_manager: RLSManager):
        self.rls_manager = rls_manager
        self.logger = logger.bind(component="collaborative_documents")

        # In-memory cache for active documents
        self.active_documents: Dict[str, CollaborativeDocument] = {}
        self.document_locks: Dict[str, Dict[str, str]] = {}  # doc_id -> {range_id -> user_id}

        # Operation queues for processing
        self.operation_queues: Dict[str, asyncio.Queue] = {}

        # Background tasks
        self.background_tasks: Set[asyncio.Task] = set()

        # Start background processing
        asyncio.create_task(self._auto_save_documents())
        asyncio.create_task(self._cleanup_inactive_documents())

    async def create_document(
        self,
        tenant_context: EnhancedTenantContext,
        document_type: DocumentType,
        title: str,
        description: Optional[str] = None,
        initial_content: str = "",
        user_id: str = "",
        platform: Optional[PlatformType] = None
    ) -> CollaborativeDocument:
        """
        Create a new collaborative document
        """
        try:
            if not platform:
                platform = PlatformType.BIZOHOLIC  # Default platform

            document = CollaborativeDocument(
                tenant_id=tenant_context.tenant_id,
                platform=platform,
                document_type=document_type,
                title=title,
                description=description,
                content=initial_content,
                created_by=user_id,
                allowed_editors=[user_id]  # Creator is automatically an editor
            )

            document.current_state.content = initial_content
            document.current_state.checksum = self._calculate_checksum(initial_content)

            # Save to database
            async with self.rls_manager.tenant_context(tenant_context.tenant_id) as conn:
                await conn.execute("""
                    INSERT INTO collaborative_documents (
                        document_id, tenant_id, platform, document_type, title, description,
                        content, version, created_by, created_at, updated_at,
                        is_public, allowed_editors, allowed_viewers, conflict_resolution,
                        ai_suggestions_enabled, ai_auto_complete, ai_grammar_check,
                        tags, metadata
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20)
                """,
                    document.document_id, document.tenant_id, document.platform.value,
                    document.document_type.value, document.title, document.description,
                    document.content, document.version, document.created_by,
                    document.created_at, document.updated_at, document.is_public,
                    document.allowed_editors, document.allowed_viewers,
                    document.conflict_resolution.value, document.ai_suggestions_enabled,
                    document.ai_auto_complete, document.ai_grammar_check,
                    document.tags, document.metadata
                )

            # Cache the document
            self.active_documents[document.document_id] = document
            self.operation_queues[document.document_id] = asyncio.Queue()

            # Start operation processing for this document
            task = asyncio.create_task(self._process_document_operations(document.document_id))
            self.background_tasks.add(task)

            self.logger.info(
                "Collaborative document created",
                document_id=document.document_id,
                title=title,
                tenant_id=tenant_context.tenant_id
            )

            return document

        except Exception as e:
            self.logger.error(
                "Error creating collaborative document",
                error=str(e),
                title=title,
                tenant_id=tenant_context.tenant_id
            )
            raise

    async def get_document(
        self,
        document_id: str,
        tenant_context: EnhancedTenantContext,
        user_id: str
    ) -> Optional[CollaborativeDocument]:
        """
        Get a collaborative document
        """
        try:
            # Check cache first
            if document_id in self.active_documents:
                document = self.active_documents[document_id]
                if await self._has_access(document, user_id, "read"):
                    return document
                else:
                    return None

            # Load from database
            async with self.rls_manager.tenant_context(tenant_context.tenant_id) as conn:
                row = await conn.fetchrow("""
                    SELECT * FROM collaborative_documents
                    WHERE document_id = $1 AND tenant_id = $2
                """, document_id, tenant_context.tenant_id)

                if not row:
                    return None

                document = CollaborativeDocument(
                    document_id=row['document_id'],
                    tenant_id=row['tenant_id'],
                    platform=PlatformType(row['platform']),
                    document_type=DocumentType(row['document_type']),
                    title=row['title'],
                    description=row['description'],
                    content=row['content'],
                    version=row['version'],
                    created_by=row['created_by'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at'],
                    is_public=row['is_public'],
                    allowed_editors=row['allowed_editors'] or [],
                    allowed_viewers=row['allowed_viewers'] or [],
                    conflict_resolution=ConflictResolution(row['conflict_resolution']),
                    ai_suggestions_enabled=row['ai_suggestions_enabled'],
                    ai_auto_complete=row['ai_auto_complete'],
                    ai_grammar_check=row['ai_grammar_check'],
                    tags=row['tags'] or [],
                    metadata=row['metadata'] or {}
                )

                # Check access
                if not await self._has_access(document, user_id, "read"):
                    return None

                # Initialize current state
                document.current_state.content = document.content
                document.current_state.version = document.version
                document.current_state.checksum = self._calculate_checksum(document.content)

                # Cache the document
                self.active_documents[document_id] = document
                self.operation_queues[document_id] = asyncio.Queue()

                # Start operation processing
                task = asyncio.create_task(self._process_document_operations(document_id))
                self.background_tasks.add(task)

                return document

        except Exception as e:
            self.logger.error(
                "Error getting collaborative document",
                document_id=document_id,
                error=str(e)
            )
            return None

    async def apply_operation(
        self,
        document_id: str,
        operation: DocumentOperation,
        tenant_context: EnhancedTenantContext
    ) -> bool:
        """
        Apply an operation to a collaborative document
        """
        try:
            document = await self.get_document(document_id, tenant_context, operation.user_id)
            if not document:
                return False

            # Check edit access
            if not await self._has_access(document, operation.user_id, "write"):
                return False

            # Add to operation queue for processing
            await self.operation_queues[document_id].put(operation)

            return True

        except Exception as e:
            self.logger.error(
                "Error applying document operation",
                document_id=document_id,
                operation_id=operation.operation_id,
                error=str(e)
            )
            return False

    async def get_document_history(
        self,
        document_id: str,
        tenant_context: EnhancedTenantContext,
        user_id: str,
        limit: int = 50
    ) -> List[DocumentOperation]:
        """
        Get document operation history
        """
        try:
            document = await self.get_document(document_id, tenant_context, user_id)
            if not document:
                return []

            async with self.rls_manager.tenant_context(tenant_context.tenant_id) as conn:
                rows = await conn.fetch("""
                    SELECT * FROM document_operations
                    WHERE document_id = $1
                    ORDER BY timestamp DESC
                    LIMIT $2
                """, document_id, limit)

                operations = []
                for row in rows:
                    operation = DocumentOperation(
                        operation_id=row['operation_id'],
                        operation_type=OperationType(row['operation_type']),
                        position=row['position'],
                        length=row['length'],
                        content=row['content'],
                        metadata=row['metadata'] or {},
                        user_id=row['user_id'],
                        timestamp=row['timestamp'],
                        parent_operation_id=row['parent_operation_id']
                    )
                    operations.append(operation)

                return operations

        except Exception as e:
            self.logger.error(
                "Error getting document history",
                document_id=document_id,
                error=str(e)
            )
            return []

    async def _process_document_operations(self, document_id: str) -> None:
        """
        Background task to process document operations
        """
        try:
            queue = self.operation_queues.get(document_id)
            if not queue:
                return

            while document_id in self.active_documents:
                try:
                    # Wait for next operation
                    operation = await asyncio.wait_for(queue.get(), timeout=30.0)

                    document = self.active_documents.get(document_id)
                    if not document:
                        break

                    # Apply operational transform if needed
                    await self._apply_operational_transform(document, operation)

                    # Apply the operation
                    new_content = OperationalTransform.apply_operation(
                        document.current_state.content,
                        operation
                    )

                    # Update document state
                    document.current_state.content = new_content
                    document.current_state.version += 1
                    document.current_state.operations.append(operation)
                    document.current_state.last_modified = datetime.now(timezone.utc)
                    document.current_state.checksum = self._calculate_checksum(new_content)
                    document.updated_at = datetime.now(timezone.utc)

                    # Save operation to database
                    await self._save_operation(document, operation)

                    # Broadcast to collaborators would happen here via WebSocket
                    # This would be integrated with the RealtimeCollaborationService

                except asyncio.TimeoutError:
                    # No operations - continue waiting
                    continue
                except Exception as e:
                    self.logger.error(
                        "Error processing document operation",
                        document_id=document_id,
                        error=str(e)
                    )

        except Exception as e:
            self.logger.error(
                "Error in document operation processor",
                document_id=document_id,
                error=str(e)
            )

    async def _apply_operational_transform(
        self,
        document: CollaborativeDocument,
        new_operation: DocumentOperation
    ) -> None:
        """
        Apply operational transform to resolve conflicts
        """
        if document.conflict_resolution != ConflictResolution.OPERATIONAL_TRANSFORM:
            return

        # Find concurrent operations (operations that haven't been seen by this user)
        concurrent_ops = []
        for op in document.current_state.operations:
            if (op.timestamp >= new_operation.timestamp and
                op.user_id != new_operation.user_id):
                concurrent_ops.append(op)

        # Transform against concurrent operations
        for concurrent_op in concurrent_ops:
            transformed_new, transformed_concurrent = OperationalTransform.transform_operations(
                new_operation, concurrent_op
            )
            new_operation = transformed_new

    async def _save_operation(
        self,
        document: CollaborativeDocument,
        operation: DocumentOperation
    ) -> None:
        """
        Save operation to database
        """
        try:
            async with self.rls_manager.tenant_context(document.tenant_id) as conn:
                await conn.execute("""
                    INSERT INTO document_operations (
                        operation_id, document_id, operation_type, position, length,
                        content, metadata, user_id, timestamp, parent_operation_id
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                """,
                    operation.operation_id, document.document_id,
                    operation.operation_type.value, operation.position,
                    operation.length, operation.content, operation.metadata,
                    operation.user_id, operation.timestamp, operation.parent_operation_id
                )
        except Exception as e:
            self.logger.error(
                "Error saving document operation",
                operation_id=operation.operation_id,
                error=str(e)
            )

    async def _has_access(
        self,
        document: CollaborativeDocument,
        user_id: str,
        access_type: str
    ) -> bool:
        """
        Check if user has access to document
        """
        if document.is_public and access_type == "read":
            return True

        if user_id == document.created_by:
            return True

        if access_type == "read":
            return user_id in document.allowed_viewers or user_id in document.allowed_editors

        if access_type == "write":
            return user_id in document.allowed_editors

        return False

    def _calculate_checksum(self, content: str) -> str:
        """
        Calculate checksum for content integrity
        """
        import hashlib
        return hashlib.md5(content.encode()).hexdigest()

    async def _auto_save_documents(self) -> None:
        """
        Background task to auto-save documents
        """
        while True:
            try:
                await asyncio.sleep(30)  # Save every 30 seconds

                for document in self.active_documents.values():
                    try:
                        async with self.rls_manager.tenant_context(document.tenant_id) as conn:
                            await conn.execute("""
                                UPDATE collaborative_documents
                                SET content = $1, version = $2, updated_at = $3
                                WHERE document_id = $4
                            """,
                                document.current_state.content,
                                document.current_state.version,
                                document.updated_at,
                                document.document_id
                            )
                    except Exception as e:
                        self.logger.error(
                            "Error auto-saving document",
                            document_id=document.document_id,
                            error=str(e)
                        )

            except Exception as e:
                self.logger.error("Error in auto-save task", error=str(e))

    async def _cleanup_inactive_documents(self) -> None:
        """
        Background task to clean up inactive documents
        """
        while True:
            try:
                await asyncio.sleep(600)  # Check every 10 minutes

                current_time = datetime.now(timezone.utc)
                inactive_docs = []

                for doc_id, document in self.active_documents.items():
                    # Remove if inactive for more than 1 hour
                    if (current_time - document.current_state.last_modified).total_seconds() > 3600:
                        inactive_docs.append(doc_id)

                for doc_id in inactive_docs:
                    if doc_id in self.active_documents:
                        del self.active_documents[doc_id]
                    if doc_id in self.operation_queues:
                        del self.operation_queues[doc_id]
                    if doc_id in self.document_locks:
                        del self.document_locks[doc_id]

                if inactive_docs:
                    self.logger.info(
                        "Cleaned up inactive documents",
                        count=len(inactive_docs)
                    )

            except Exception as e:
                self.logger.error("Error in cleanup task", error=str(e))


# Global instance
document_manager: Optional[CollaborativeDocumentManager] = None


def get_document_manager() -> CollaborativeDocumentManager:
    """Get the global document manager instance"""
    global document_manager
    if document_manager is None:
        raise RuntimeError("Document manager not initialized")
    return document_manager


def initialize_document_manager(rls_manager: RLSManager) -> CollaborativeDocumentManager:
    """Initialize the global document manager"""
    global document_manager
    document_manager = CollaborativeDocumentManager(rls_manager)
    return document_manager