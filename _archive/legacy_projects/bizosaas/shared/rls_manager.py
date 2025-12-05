"""
Row-Level Security (RLS) Manager for Multi-Platform Data Isolation
Provides Python utilities for managing tenant context and database access
"""

import asyncio
import asyncpg
import structlog
from typing import Dict, Any, Optional, List, Union
from uuid import UUID
from contextlib import asynccontextmanager
from dataclasses import dataclass
from enum import Enum

from .enhanced_tenant_context import EnhancedTenantContext, PlatformType

logger = structlog.get_logger(__name__)


class RLSAccessLevel(Enum):
    """Access levels for RLS policies"""
    TENANT_ONLY = "tenant"
    SHARED = "shared"
    PUBLIC = "public"
    ADMIN = "admin"


@dataclass
class RLSContext:
    """RLS context for database sessions"""
    tenant_id: str
    user_id: Optional[UUID] = None
    platform_access: Optional[Dict[str, bool]] = None
    access_level: RLSAccessLevel = RLSAccessLevel.TENANT_ONLY
    session_metadata: Optional[Dict[str, Any]] = None


class RLSManager:
    """
    Manages Row-Level Security contexts and database access
    Provides unified interface for multi-platform tenant isolation
    """

    def __init__(self, connection_pool: asyncpg.Pool):
        self.pool = connection_pool
        self.logger = logger.bind(component="rls_manager")

    async def set_tenant_context(
        self,
        connection: asyncpg.Connection,
        context: RLSContext
    ) -> None:
        """
        Set tenant context for the database connection

        Args:
            connection: Database connection
            context: RLS context with tenant and access information
        """
        try:
            # Set basic tenant context
            await connection.execute(
                "SELECT set_config('app.current_tenant_id', $1, true)",
                context.tenant_id
            )

            # Set user context if provided
            if context.user_id:
                await connection.execute(
                    "SELECT set_config('app.current_user_id', $1, true)",
                    str(context.user_id)
                )

            # Set platform access if provided
            if context.platform_access:
                import json
                platform_json = json.dumps(context.platform_access)
                await connection.execute(
                    "SELECT set_config('app.platform_access', $1, true)",
                    platform_json
                )

            # Set access level
            await connection.execute(
                "SELECT set_config('app.access_level', $1, true)",
                context.access_level.value
            )

            self.logger.info(
                "Tenant context set successfully",
                tenant_id=context.tenant_id,
                user_id=str(context.user_id) if context.user_id else None,
                platform_access=context.platform_access,
                access_level=context.access_level.value
            )

        except Exception as e:
            self.logger.error(
                "Failed to set tenant context",
                tenant_id=context.tenant_id,
                error=str(e)
            )
            raise

    async def clear_tenant_context(self, connection: asyncpg.Connection) -> None:
        """Clear tenant context from the database connection"""
        try:
            await connection.execute("SELECT clear_tenant_context()")
            self.logger.debug("Tenant context cleared")
        except Exception as e:
            self.logger.error("Failed to clear tenant context", error=str(e))
            raise

    async def get_current_context(
        self,
        connection: asyncpg.Connection
    ) -> Dict[str, Any]:
        """Get current tenant context from the database connection"""
        try:
            result = await connection.fetchval("SELECT get_current_tenant_context()")
            return result or {}
        except Exception as e:
            self.logger.error("Failed to get current context", error=str(e))
            return {}

    @asynccontextmanager
    async def tenant_session(self, context: RLSContext):
        """
        Context manager for tenant-scoped database operations

        Usage:
            async with rls_manager.tenant_session(context) as conn:
                # All queries within this block are tenant-scoped
                results = await conn.fetch("SELECT * FROM bizoholic_leads")
        """
        async with self.pool.acquire() as connection:
            try:
                await self.set_tenant_context(connection, context)
                yield connection
            finally:
                await self.clear_tenant_context(connection)

    async def create_tenant_context_from_enhanced(
        self,
        enhanced_context: EnhancedTenantContext,
        user_id: Optional[UUID] = None
    ) -> RLSContext:
        """
        Create RLS context from enhanced tenant context

        Args:
            enhanced_context: Enhanced tenant context object
            user_id: Optional user ID for the session

        Returns:
            RLS context ready for database operations
        """
        # Convert platform access to simple dict
        platform_access = {}
        for platform, access in enhanced_context.platform_access.items():
            platform_access[platform.value] = access.enabled

        return RLSContext(
            tenant_id=enhanced_context.tenant_id,
            user_id=user_id,
            platform_access=platform_access,
            access_level=RLSAccessLevel.TENANT_ONLY,
            session_metadata={
                "subscription_tier": enhanced_context.subscription_tier.value,
                "tenant_uuid": str(enhanced_context.tenant_uuid),
                "ai_context": enhanced_context.ai_context.dict()
            }
        )

    async def validate_platform_access(
        self,
        context: RLSContext,
        platform: PlatformType,
        operation: str = "read"
    ) -> bool:
        """
        Validate if tenant has access to specific platform operation

        Args:
            context: RLS context
            platform: Platform to check access for
            operation: Operation type (read, write, admin)

        Returns:
            True if access is allowed, False otherwise
        """
        if not context.platform_access:
            return False

        platform_enabled = context.platform_access.get(platform.value, False)

        if not platform_enabled:
            self.logger.warning(
                "Platform access denied",
                tenant_id=context.tenant_id,
                platform=platform.value,
                operation=operation
            )
            return False

        return True

    async def audit_data_access(
        self,
        connection: asyncpg.Connection,
        table_name: str,
        operation: str,
        record_count: int,
        query_metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Audit data access for compliance and monitoring

        Args:
            connection: Database connection
            table_name: Name of table accessed
            operation: Type of operation (SELECT, INSERT, UPDATE, DELETE)
            record_count: Number of records affected
            query_metadata: Additional query metadata
        """
        try:
            current_context = await self.get_current_context(connection)

            audit_data = {
                "table_name": table_name,
                "operation": operation,
                "record_count": record_count,
                "tenant_id": current_context.get("tenant_id"),
                "user_id": current_context.get("user_id"),
                "platform_access": current_context.get("platform_access", {}),
                "query_metadata": query_metadata or {}
            }

            # Log the audit event
            self.logger.info(
                "Data access audited",
                **audit_data
            )

            # Store in audit table if needed
            await connection.execute("""
                INSERT INTO security_events (
                    tenant_id, event_type, severity, description,
                    user_id, request_data, created_at
                ) VALUES (
                    $1, 'data_access', 'low', $2,
                    $3, $4, CURRENT_TIMESTAMP
                )
            """,
                current_context.get("tenant_id"),
                f"{operation} on {table_name} ({record_count} records)",
                UUID(current_context.get("user_id")) if current_context.get("user_id") else None,
                audit_data
            )

        except Exception as e:
            self.logger.error(
                "Failed to audit data access",
                table_name=table_name,
                operation=operation,
                error=str(e)
            )

    async def get_tenant_statistics(
        self,
        tenant_id: str,
        platforms: Optional[List[PlatformType]] = None
    ) -> Dict[str, Any]:
        """
        Get comprehensive statistics for a tenant across platforms

        Args:
            tenant_id: Tenant ID to get statistics for
            platforms: Optional list of platforms to include

        Returns:
            Dictionary with tenant statistics
        """
        context = RLSContext(tenant_id=tenant_id)

        async with self.tenant_session(context) as conn:
            stats = {
                "tenant_id": tenant_id,
                "platforms": {},
                "total_records": 0,
                "last_activity": None
            }

            platform_tables = {
                PlatformType.BIZOHOLIC: [
                    "bizoholic_leads",
                    "bizoholic_campaigns"
                ],
                PlatformType.CORELDOVE: [
                    "coreldove_products",
                    "coreldove_orders"
                ],
                PlatformType.BUSINESS_DIRECTORY: [
                    "directory_businesses",
                    "directory_reviews"
                ],
                PlatformType.THRILLRING: [
                    "thrillring_games",
                    "thrillring_tournaments"
                ],
                PlatformType.QUANTTRADE: [
                    "quanttrade_portfolios",
                    "quanttrade_trades"
                ]
            }

            platforms_to_check = platforms or list(PlatformType)

            for platform in platforms_to_check:
                platform_stats = {
                    "tables": {},
                    "total_records": 0,
                    "last_activity": None
                }

                tables = platform_tables.get(platform, [])

                for table in tables:
                    try:
                        # Get record count
                        count_result = await conn.fetchval(
                            f"SELECT COUNT(*) FROM {table}"
                        )

                        # Get last activity
                        last_activity = await conn.fetchval(
                            f"SELECT MAX(updated_at) FROM {table}"
                        )

                        platform_stats["tables"][table] = {
                            "record_count": count_result or 0,
                            "last_activity": last_activity.isoformat() if last_activity else None
                        }

                        platform_stats["total_records"] += count_result or 0

                        if last_activity and (
                            not platform_stats["last_activity"] or
                            last_activity > platform_stats["last_activity"]
                        ):
                            platform_stats["last_activity"] = last_activity.isoformat()

                    except Exception as e:
                        self.logger.warning(
                            "Failed to get stats for table",
                            table=table,
                            platform=platform.value,
                            error=str(e)
                        )
                        platform_stats["tables"][table] = {
                            "record_count": 0,
                            "last_activity": None,
                            "error": str(e)
                        }

                stats["platforms"][platform.value] = platform_stats
                stats["total_records"] += platform_stats["total_records"]

                if platform_stats["last_activity"] and (
                    not stats["last_activity"] or
                    platform_stats["last_activity"] > stats["last_activity"]
                ):
                    stats["last_activity"] = platform_stats["last_activity"]

            return stats

    async def migrate_tenant_data(
        self,
        source_tenant_id: str,
        target_tenant_id: str,
        platforms: List[PlatformType],
        dry_run: bool = True
    ) -> Dict[str, Any]:
        """
        Migrate tenant data between tenants (useful for tenant merging/splitting)

        Args:
            source_tenant_id: Source tenant ID
            target_tenant_id: Target tenant ID
            platforms: Platforms to migrate
            dry_run: If True, only count records without actual migration

        Returns:
            Migration results
        """
        results = {
            "source_tenant": source_tenant_id,
            "target_tenant": target_tenant_id,
            "dry_run": dry_run,
            "platforms": {},
            "total_records": 0,
            "errors": []
        }

        # Platform table mapping
        platform_tables = {
            PlatformType.BIZOHOLIC: ["bizoholic_leads", "bizoholic_campaigns"],
            PlatformType.CORELDOVE: ["coreldove_products", "coreldove_orders"],
            PlatformType.BUSINESS_DIRECTORY: ["directory_businesses", "directory_reviews"],
            PlatformType.THRILLRING: ["thrillring_games", "thrillring_tournaments"],
            PlatformType.QUANTTRADE: ["quanttrade_portfolios", "quanttrade_trades"]
        }

        async with self.pool.acquire() as conn:
            async with conn.transaction():
                for platform in platforms:
                    platform_results = {
                        "tables": {},
                        "total_records": 0,
                        "errors": []
                    }

                    tables = platform_tables.get(platform, [])

                    for table in tables:
                        try:
                            # Set source tenant context to count records
                            source_context = RLSContext(tenant_id=source_tenant_id)
                            await self.set_tenant_context(conn, source_context)

                            # Count records to migrate
                            record_count = await conn.fetchval(
                                f"SELECT COUNT(*) FROM {table}"
                            )

                            table_result = {
                                "record_count": record_count or 0,
                                "migrated": False
                            }

                            if record_count and not dry_run:
                                # Perform actual migration
                                await conn.execute(
                                    f"UPDATE {table} SET tenant_id = $1 WHERE tenant_id = $2",
                                    target_tenant_id,
                                    source_tenant_id
                                )
                                table_result["migrated"] = True

                            platform_results["tables"][table] = table_result
                            platform_results["total_records"] += record_count or 0

                        except Exception as e:
                            error_msg = f"Failed to migrate table {table}: {str(e)}"
                            platform_results["errors"].append(error_msg)
                            results["errors"].append(error_msg)
                            self.logger.error(
                                "Table migration failed",
                                table=table,
                                platform=platform.value,
                                error=str(e)
                            )

                    results["platforms"][platform.value] = platform_results
                    results["total_records"] += platform_results["total_records"]

                # Clear context
                await self.clear_tenant_context(conn)

        self.logger.info(
            "Tenant migration completed",
            source_tenant=source_tenant_id,
            target_tenant=target_tenant_id,
            dry_run=dry_run,
            total_records=results["total_records"],
            error_count=len(results["errors"])
        )

        return results


class RLSQueryBuilder:
    """
    Query builder with automatic tenant isolation
    Provides safe query construction with RLS enforcement
    """

    def __init__(self, rls_manager: RLSManager):
        self.rls_manager = rls_manager
        self.logger = logger.bind(component="rls_query_builder")

    async def safe_select(
        self,
        connection: asyncpg.Connection,
        table: str,
        columns: List[str] = None,
        where_clause: str = "",
        params: List[Any] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Execute SELECT query with automatic tenant isolation

        Args:
            connection: Database connection with tenant context set
            table: Table name
            columns: Columns to select (default: *)
            where_clause: Additional WHERE conditions
            params: Query parameters
            limit: Record limit
            offset: Record offset

        Returns:
            List of records as dictionaries
        """
        try:
            columns_str = ", ".join(columns) if columns else "*"
            query = f"SELECT {columns_str} FROM {table}"

            if where_clause:
                query += f" WHERE {where_clause}"

            if limit:
                query += f" LIMIT {limit}"

            if offset:
                query += f" OFFSET {offset}"

            # Execute query (RLS policies automatically applied)
            if params:
                result = await connection.fetch(query, *params)
            else:
                result = await connection.fetch(query)

            # Convert to list of dicts
            records = [dict(record) for record in result]

            # Audit the access
            await self.rls_manager.audit_data_access(
                connection, table, "SELECT", len(records),
                {"where_clause": where_clause, "limit": limit, "offset": offset}
            )

            return records

        except Exception as e:
            self.logger.error(
                "Safe select failed",
                table=table,
                where_clause=where_clause,
                error=str(e)
            )
            raise

    async def safe_insert(
        self,
        connection: asyncpg.Connection,
        table: str,
        data: Dict[str, Any],
        returning: List[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Execute INSERT query with automatic tenant context injection

        Args:
            connection: Database connection with tenant context set
            table: Table name
            data: Data to insert
            returning: Columns to return

        Returns:
            Inserted record if returning is specified
        """
        try:
            # Get current tenant context
            current_context = await self.rls_manager.get_current_context(connection)
            tenant_id = current_context.get("tenant_id")

            if not tenant_id:
                raise ValueError("No tenant context set for insert operation")

            # Inject tenant_id into data
            data_with_tenant = {**data, "tenant_id": tenant_id}

            # Build INSERT query
            columns = list(data_with_tenant.keys())
            placeholders = [f"${i+1}" for i in range(len(columns))]

            query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"

            if returning:
                query += f" RETURNING {', '.join(returning)}"

            # Execute query
            values = list(data_with_tenant.values())

            if returning:
                result = await connection.fetchrow(query, *values)
                record = dict(result) if result else None
            else:
                await connection.execute(query, *values)
                record = None

            # Audit the access
            await self.rls_manager.audit_data_access(
                connection, table, "INSERT", 1,
                {"columns": columns, "returning": returning}
            )

            return record

        except Exception as e:
            self.logger.error(
                "Safe insert failed",
                table=table,
                data=data,
                error=str(e)
            )
            raise

    async def safe_update(
        self,
        connection: asyncpg.Connection,
        table: str,
        data: Dict[str, Any],
        where_clause: str,
        params: List[Any] = None,
        returning: List[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Execute UPDATE query with tenant isolation

        Args:
            connection: Database connection with tenant context set
            table: Table name
            data: Data to update
            where_clause: WHERE conditions
            params: WHERE parameters
            returning: Columns to return

        Returns:
            Updated records if returning is specified
        """
        try:
            # Build UPDATE query
            set_clauses = []
            param_index = len(params) + 1 if params else 1
            update_params = list(params) if params else []

            for column, value in data.items():
                set_clauses.append(f"{column} = ${param_index}")
                update_params.append(value)
                param_index += 1

            query = f"UPDATE {table} SET {', '.join(set_clauses)} WHERE {where_clause}"

            if returning:
                query += f" RETURNING {', '.join(returning)}"

            # Execute query (RLS policies automatically applied)
            if returning:
                result = await connection.fetch(query, *update_params)
                records = [dict(record) for record in result]
            else:
                result = await connection.execute(query, *update_params)
                # Extract number of updated rows from result status
                updated_count = int(result.split()[-1]) if result else 0
                records = []

            # Audit the access
            await self.rls_manager.audit_data_access(
                connection, table, "UPDATE", len(records) or updated_count,
                {"set_data": data, "where_clause": where_clause}
            )

            return records

        except Exception as e:
            self.logger.error(
                "Safe update failed",
                table=table,
                data=data,
                where_clause=where_clause,
                error=str(e)
            )
            raise

    async def safe_delete(
        self,
        connection: asyncpg.Connection,
        table: str,
        where_clause: str,
        params: List[Any] = None,
        returning: List[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Execute DELETE query with tenant isolation

        Args:
            connection: Database connection with tenant context set
            table: Table name
            where_clause: WHERE conditions
            params: WHERE parameters
            returning: Columns to return

        Returns:
            Deleted records if returning is specified
        """
        try:
            query = f"DELETE FROM {table} WHERE {where_clause}"

            if returning:
                query += f" RETURNING {', '.join(returning)}"

            # Execute query (RLS policies automatically applied)
            if params:
                if returning:
                    result = await connection.fetch(query, *params)
                    records = [dict(record) for record in result]
                else:
                    result = await connection.execute(query, *params)
                    deleted_count = int(result.split()[-1]) if result else 0
                    records = []
            else:
                if returning:
                    result = await connection.fetch(query)
                    records = [dict(record) for record in result]
                else:
                    result = await connection.execute(query)
                    deleted_count = int(result.split()[-1]) if result else 0
                    records = []

            # Audit the access
            await self.rls_manager.audit_data_access(
                connection, table, "DELETE", len(records) or deleted_count,
                {"where_clause": where_clause}
            )

            return records

        except Exception as e:
            self.logger.error(
                "Safe delete failed",
                table=table,
                where_clause=where_clause,
                error=str(e)
            )
            raise


# Utility functions for common operations
async def create_rls_manager(database_url: str) -> RLSManager:
    """Create RLS manager with connection pool"""
    pool = await asyncpg.create_pool(database_url)
    return RLSManager(pool)


async def execute_with_tenant_context(
    rls_manager: RLSManager,
    context: RLSContext,
    operation: callable,
    *args,
    **kwargs
) -> Any:
    """
    Execute operation with tenant context

    Args:
        rls_manager: RLS manager instance
        context: Tenant context
        operation: Async function to execute
        *args, **kwargs: Arguments for the operation

    Returns:
        Result of the operation
    """
    async with rls_manager.tenant_session(context) as conn:
        return await operation(conn, *args, **kwargs)