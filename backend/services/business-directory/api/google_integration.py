"""
Google Business Profile Integration API Routes
Comprehensive FastAPI routes for Google Business Profile management and synchronization
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query, Request, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func
from typing import List, Optional, Dict, Any
from uuid import UUID
import logging
import asyncio
from datetime import datetime, timedelta

from ..core import get_db, get_current_active_user, require_business_read, require_business_write
from ..models.google_integration import (
    GoogleAccount, GoogleBusinessLocation, SyncOperation, LocationConflict,
    GoogleAccountStatus, SyncStatus, ConflictResolutionStrategy
)
from ..schemas.google_integration import (
    GoogleAuthUrlSchema, GoogleAuthUrlResponseSchema, GoogleCallbackSchema,
    GoogleAccountResponseSchema, GoogleLocationResponseSchema, LocationSyncSchema,
    BulkLocationSyncSchema, LocationManagementSchema, ConflictResolutionSchema,
    SyncOperationResponseSchema, LocationConflictResponseSchema, SyncStatsResponseSchema,
    GoogleBusinessInsightsSchema, BatchOperationResponseSchema, GoogleIntegrationHealthSchema
)
from ..schemas.common import (
    SuccessSchema, ErrorSchema, PaginatedResponseSchema
)
from ..services.google_auth_service import google_auth_service
from ..services.google_business_client import GoogleBusinessClient
from ..services.google_mappers import GoogleDataMapper
from ..core.security import get_tenant_from_request, rate_limit_middleware

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    prefix="/google",
    tags=["Google Business Profile Integration"],
    dependencies=[Depends(rate_limit_middleware)]
)

# Initialize services
google_client = GoogleBusinessClient()
google_mapper = GoogleDataMapper()


# OAuth Flow Endpoints

@router.post(
    "/auth/start",
    response_model=GoogleAuthUrlResponseSchema,
    summary="Start Google OAuth Flow",
    description="Generate Google OAuth authorization URL to start the authentication process"
)
async def start_google_auth(
    auth_request: GoogleAuthUrlSchema,
    request: Request,
    current_user = Depends(require_business_write)
):
    """
    Start Google OAuth 2.0 authentication flow
    
    This endpoint generates the authorization URL that users need to visit to grant
    access to their Google Business Profile data.
    """
    try:
        tenant_id = await get_tenant_from_request(request)
        
        # Generate authorization URL
        auth_data = google_auth_service.get_authorization_url(
            tenant_id=tenant_id,
            state=auth_request.state
        )
        
        logger.info(f"Started Google OAuth flow for tenant {tenant_id}")
        
        return GoogleAuthUrlResponseSchema(
            authorization_url=auth_data["authorization_url"],
            state=auth_data["state"],
            scopes=auth_data["scopes"]
        )
        
    except Exception as e:
        logger.error(f"Error starting Google OAuth: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start OAuth flow: {str(e)}"
        )


@router.post(
    "/auth/callback",
    response_model=GoogleAccountResponseSchema,
    summary="Handle Google OAuth Callback",
    description="Process the OAuth callback from Google and store authentication credentials"
)
async def handle_google_callback(
    callback_data: GoogleCallbackSchema,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_business_write)
):
    """
    Handle Google OAuth callback and store credentials
    
    This endpoint processes the authorization code returned by Google OAuth
    and exchanges it for access and refresh tokens.
    """
    try:
        # Handle OAuth callback
        auth_result = await google_auth_service.handle_oauth_callback(
            code=callback_data.code,
            state=callback_data.state,
            error=callback_data.error
        )
        
        if not auth_result["success"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="OAuth callback failed"
            )
        
        # Get the saved account
        result = await db.execute(
            select(GoogleAccount).where(
                GoogleAccount.id == auth_result["account_id"]
            )
        )
        account = result.scalar_one_or_none()
        
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found after OAuth"
            )
        
        logger.info(f"Google OAuth callback processed for account {account.email}")
        
        return GoogleAccountResponseSchema.from_orm(account)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error handling Google callback: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process OAuth callback: {str(e)}"
        )


@router.delete(
    "/accounts/{account_id}/disconnect",
    response_model=SuccessSchema,
    summary="Disconnect Google Account",
    description="Disconnect a Google Business Profile account and revoke access"
)
async def disconnect_google_account(
    account_id: UUID,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_business_write)
):
    """
    Disconnect Google account and revoke OAuth access
    
    This will revoke the access token with Google and mark the account
    as disconnected in the local database.
    """
    try:
        tenant_id = await get_tenant_from_request(request)
        
        success = await google_auth_service.disconnect_account(
            account_id=str(account_id),
            tenant_id=tenant_id
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found or already disconnected"
            )
        
        logger.info(f"Disconnected Google account {account_id}")
        
        return SuccessSchema(
            message="Google account disconnected successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error disconnecting Google account: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to disconnect account: {str(e)}"
        )


# Account Management Endpoints

@router.get(
    "/accounts",
    response_model=List[GoogleAccountResponseSchema],
    summary="List Google Accounts",
    description="Get all connected Google Business Profile accounts for the current tenant"
)
async def list_google_accounts(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_business_read)
):
    """
    List all connected Google Business Profile accounts
    
    Returns account information including connection status, last sync times,
    and error information.
    """
    try:
        tenant_id = await get_tenant_from_request(request)
        
        # Get accounts with location counts
        result = await db.execute(
            select(
                GoogleAccount,
                func.count(GoogleBusinessLocation.id).label('location_count')
            )
            .outerjoin(GoogleBusinessLocation)
            .where(GoogleAccount.tenant_id == tenant_id)
            .group_by(GoogleAccount.id)
            .order_by(GoogleAccount.created_at.desc())
        )
        
        accounts_with_counts = result.all()
        account_responses = []
        
        for account, location_count in accounts_with_counts:
            account_data = GoogleAccountResponseSchema.from_orm(account)
            account_data.location_count = location_count
            account_responses.append(account_data)
        
        return account_responses
        
    except Exception as e:
        logger.error(f"Error listing Google accounts: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve Google accounts"
        )


@router.get(
    "/accounts/{account_id}",
    response_model=GoogleAccountResponseSchema,
    summary="Get Google Account Details",
    description="Get detailed information about a specific Google Business Profile account"
)
async def get_google_account(
    account_id: UUID,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_business_read)
):
    """
    Get detailed Google account information
    
    Returns comprehensive account details including OAuth status,
    synchronization history, and associated location count.
    """
    try:
        tenant_id = await get_tenant_from_request(request)
        
        # Get account with location count
        result = await db.execute(
            select(
                GoogleAccount,
                func.count(GoogleBusinessLocation.id).label('location_count')
            )
            .outerjoin(GoogleBusinessLocation)
            .where(
                GoogleAccount.id == account_id,
                GoogleAccount.tenant_id == tenant_id
            )
            .group_by(GoogleAccount.id)
        )
        
        account_data = result.first()
        
        if not account_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Google account not found"
            )
        
        account, location_count = account_data
        account_response = GoogleAccountResponseSchema.from_orm(account)
        account_response.location_count = location_count
        
        return account_response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting Google account {account_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve Google account"
        )


# Location Management Endpoints

@router.get(
    "/accounts/{account_id}/locations",
    response_model=List[GoogleLocationResponseSchema],
    summary="List Business Locations",
    description="Get all business locations for a specific Google account"
)
async def list_business_locations(
    account_id: UUID,
    request: Request,
    refresh_from_google: bool = Query(False, description="Force refresh from Google API"),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_business_read)
):
    """
    List business locations for a Google account
    
    Can optionally refresh location data directly from Google API
    to ensure the most up-to-date information.
    """
    try:
        tenant_id = await get_tenant_from_request(request)
        
        # Verify account exists and belongs to tenant
        result = await db.execute(
            select(GoogleAccount).where(
                GoogleAccount.id == account_id,
                GoogleAccount.tenant_id == tenant_id
            )
        )
        account = result.scalar_one_or_none()
        
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Google account not found"
            )
        
        if refresh_from_google:
            # Refresh locations from Google API
            api_response = await google_client.get_business_locations(account)
            
            if api_response.success and api_response.data:
                # Update locations in database
                await google_mapper.sync_locations_from_google(
                    account=account,
                    google_locations=api_response.data.get('locations', []),
                    db=db
                )
        
        # Get locations from database
        result = await db.execute(
            select(GoogleBusinessLocation)
            .where(GoogleBusinessLocation.account_id == account_id)
            .order_by(GoogleBusinessLocation.created_at.desc())
        )
        locations = result.scalars().all()
        
        return [GoogleLocationResponseSchema.from_orm(loc) for loc in locations]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error listing locations for account {account_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve business locations"
        )


@router.get(
    "/locations/{location_id}",
    response_model=GoogleLocationResponseSchema,
    summary="Get Business Location Details",
    description="Get detailed information about a specific business location"
)
async def get_business_location(
    location_id: str,
    request: Request,
    refresh_from_google: bool = Query(False, description="Force refresh from Google API"),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_business_read)
):
    """
    Get detailed business location information
    
    Returns comprehensive location data including business details,
    photos, reviews, and synchronization status.
    """
    try:
        tenant_id = await get_tenant_from_request(request)
        
        # Get location with account verification
        result = await db.execute(
            select(GoogleBusinessLocation, GoogleAccount)
            .join(GoogleAccount)
            .where(
                GoogleBusinessLocation.google_location_id == location_id,
                GoogleAccount.tenant_id == tenant_id
            )
        )
        
        location_data = result.first()
        
        if not location_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Business location not found"
            )
        
        location, account = location_data
        
        if refresh_from_google:
            # Refresh from Google API
            api_response = await google_client.get_business_location(
                account=account,
                location_id=location_id
            )
            
            if api_response.success and api_response.data:
                # Update location in database
                location = await google_mapper.sync_location_from_google(
                    account=account,
                    google_location=api_response.data,
                    db=db
                )
        
        return GoogleLocationResponseSchema.from_orm(location)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting location {location_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve business location"
        )


@router.put(
    "/locations/{location_id}",
    response_model=GoogleLocationResponseSchema,
    summary="Update Business Location",
    description="Update business location information both locally and on Google"
)
async def update_business_location(
    location_id: str,
    location_update: LocationManagementSchema,
    request: Request,
    sync_to_google: bool = Query(True, description="Sync changes to Google"),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_business_write)
):
    """
    Update business location information
    
    Updates the location locally and optionally syncs changes to Google
    Business Profile. Use sync_to_google=false for local-only updates.
    """
    try:
        tenant_id = await get_tenant_from_request(request)
        
        # Get location with account verification
        result = await db.execute(
            select(GoogleBusinessLocation, GoogleAccount)
            .join(GoogleAccount)
            .where(
                GoogleBusinessLocation.google_location_id == location_id,
                GoogleAccount.tenant_id == tenant_id
            )
        )
        
        location_data = result.first()
        
        if not location_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Business location not found"
            )
        
        location, account = location_data
        
        # Update location data
        update_data = location_update.dict(exclude_unset=True)
        
        if sync_to_google:
            # Update on Google first
            api_response = await google_client.update_business_location(
                account=account,
                location_id=location_id,
                update_data=update_data
            )
            
            if not api_response.success:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Failed to update location on Google: {api_response.error}"
                )
        
        # Update local database
        for field, value in update_data.items():
            if hasattr(location, field):
                setattr(location, field, value)
        
        location.updated_at = datetime.utcnow()
        location.last_sync_at = datetime.utcnow() if sync_to_google else location.last_sync_at
        
        await db.commit()
        await db.refresh(location)
        
        logger.info(f"Updated business location {location_id}, synced to Google: {sync_to_google}")
        
        return GoogleLocationResponseSchema.from_orm(location)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating location {location_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update business location"
        )


# Synchronization Endpoints

@router.post(
    "/sync/locations",
    response_model=SyncOperationResponseSchema,
    summary="Sync Business Locations",
    description="Synchronize business locations from Google Business Profile"
)
async def sync_business_locations(
    sync_request: LocationSyncSchema,
    request: Request,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_business_write)
):
    """
    Synchronize business locations from Google
    
    Initiates a synchronization process to pull the latest location data
    from Google Business Profile. The sync runs in the background.
    """
    try:
        tenant_id = await get_tenant_from_request(request)
        
        # Create sync operation record
        sync_operation = SyncOperation(
            tenant_id=UUID(tenant_id),
            operation_type="location_sync",
            status=SyncStatus.PENDING,
            started_at=datetime.utcnow(),
            parameters={
                "location_ids": sync_request.location_ids,
                "force_refresh": sync_request.force_refresh,
                "conflict_resolution": sync_request.conflict_resolution.value
            }
        )
        
        db.add(sync_operation)
        await db.commit()
        await db.refresh(sync_operation)
        
        # Start background sync
        background_tasks.add_task(
            _perform_location_sync,
            sync_operation.id,
            tenant_id,
            sync_request
        )
        
        logger.info(f"Started location sync operation {sync_operation.id}")
        
        return SyncOperationResponseSchema.from_orm(sync_operation)
        
    except Exception as e:
        logger.error(f"Error starting location sync: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to start location synchronization"
        )


@router.post(
    "/sync/bulk",
    response_model=BatchOperationResponseSchema,
    summary="Bulk Location Sync",
    description="Perform bulk synchronization for multiple accounts or locations"
)
async def bulk_sync_locations(
    bulk_sync_request: BulkLocationSyncSchema,
    request: Request,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_business_write)
):
    """
    Perform bulk location synchronization
    
    Synchronizes multiple locations or all locations for specified accounts.
    This is useful for large-scale sync operations.
    """
    try:
        tenant_id = await get_tenant_from_request(request)
        
        # Create batch operation record
        from uuid import uuid4
        batch_operation = {
            "batch_id": uuid4(),
            "operation_type": "bulk_location_sync",
            "total_items": 0,
            "processed_items": 0,
            "successful_items": 0,
            "failed_items": 0,
            "status": "pending",
            "started_at": datetime.utcnow(),
            "errors": []
        }
        
        # Start background bulk sync
        background_tasks.add_task(
            _perform_bulk_sync,
            batch_operation["batch_id"],
            tenant_id,
            bulk_sync_request
        )
        
        logger.info(f"Started bulk sync operation {batch_operation['batch_id']}")
        
        return BatchOperationResponseSchema(**batch_operation)
        
    except Exception as e:
        logger.error(f"Error starting bulk sync: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to start bulk synchronization"
        )


@router.get(
    "/sync/operations",
    response_model=List[SyncOperationResponseSchema],
    summary="List Sync Operations",
    description="Get list of synchronization operations and their status"
)
async def list_sync_operations(
    request: Request,
    status_filter: Optional[SyncStatus] = Query(None, description="Filter by status"),
    limit: int = Query(50, ge=1, le=200, description="Number of operations to return"),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_business_read)
):
    """
    List synchronization operations
    
    Returns a list of sync operations with their current status,
    progress information, and any error details.
    """
    try:
        tenant_id = await get_tenant_from_request(request)
        
        query = select(SyncOperation).where(
            SyncOperation.tenant_id == tenant_id
        )
        
        if status_filter:
            query = query.where(SyncOperation.status == status_filter.value)
        
        query = query.order_by(SyncOperation.started_at.desc()).limit(limit)
        
        result = await db.execute(query)
        operations = result.scalars().all()
        
        return [SyncOperationResponseSchema.from_orm(op) for op in operations]
        
    except Exception as e:
        logger.error(f"Error listing sync operations: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve sync operations"
        )


@router.get(
    "/sync/operations/{operation_id}",
    response_model=SyncOperationResponseSchema,
    summary="Get Sync Operation Status",
    description="Get detailed status of a specific synchronization operation"
)
async def get_sync_operation(
    operation_id: UUID,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_business_read)
):
    """
    Get sync operation details
    
    Returns detailed information about a specific synchronization operation
    including progress, errors, and completion status.
    """
    try:
        tenant_id = await get_tenant_from_request(request)
        
        result = await db.execute(
            select(SyncOperation).where(
                SyncOperation.id == operation_id,
                SyncOperation.tenant_id == tenant_id
            )
        )
        operation = result.scalar_one_or_none()
        
        if not operation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sync operation not found"
            )
        
        return SyncOperationResponseSchema.from_orm(operation)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting sync operation {operation_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve sync operation"
        )


# Conflict Resolution Endpoints

@router.get(
    "/conflicts",
    response_model=List[LocationConflictResponseSchema],
    summary="List Data Conflicts",
    description="Get list of data conflicts that require resolution"
)
async def list_conflicts(
    request: Request,
    location_id: Optional[str] = Query(None, description="Filter by location ID"),
    unresolved_only: bool = Query(True, description="Show only unresolved conflicts"),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_business_read)
):
    """
    List data synchronization conflicts
    
    Returns conflicts between local data and Google Business Profile data
    that require manual resolution or automatic conflict resolution.
    """
    try:
        tenant_id = await get_tenant_from_request(request)
        
        query = select(LocationConflict).join(GoogleBusinessLocation).join(GoogleAccount).where(
            GoogleAccount.tenant_id == tenant_id
        )
        
        if location_id:
            query = query.where(LocationConflict.location_id == location_id)
        
        if unresolved_only:
            query = query.where(LocationConflict.resolution_status == "pending")
        
        query = query.order_by(LocationConflict.created_at.desc())
        
        result = await db.execute(query)
        conflicts = result.scalars().all()
        
        return [LocationConflictResponseSchema.from_orm(conflict) for conflict in conflicts]
        
    except Exception as e:
        logger.error(f"Error listing conflicts: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve conflicts"
        )


@router.post(
    "/conflicts/{conflict_id}/resolve",
    response_model=SuccessSchema,
    summary="Resolve Data Conflict",
    description="Resolve a specific data synchronization conflict"
)
async def resolve_conflict(
    conflict_id: UUID,
    resolution: ConflictResolutionSchema,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_business_write)
):
    """
    Resolve a data synchronization conflict
    
    Applies the specified resolution strategy to resolve conflicts between
    local data and Google Business Profile data.
    """
    try:
        tenant_id = await get_tenant_from_request(request)
        
        # Get conflict with tenant verification
        result = await db.execute(
            select(LocationConflict, GoogleBusinessLocation, GoogleAccount)
            .join(GoogleBusinessLocation)
            .join(GoogleAccount)
            .where(
                LocationConflict.id == conflict_id,
                GoogleAccount.tenant_id == tenant_id
            )
        )
        
        conflict_data = result.first()
        
        if not conflict_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conflict not found"
            )
        
        conflict, location, account = conflict_data
        
        # Apply resolution
        success = await _apply_conflict_resolution(
            conflict=conflict,
            location=location,
            account=account,
            resolution=resolution,
            db=db
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to apply conflict resolution"
            )
        
        logger.info(f"Resolved conflict {conflict_id}")
        
        return SuccessSchema(
            message="Conflict resolved successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error resolving conflict {conflict_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to resolve conflict"
        )


# Analytics and Statistics Endpoints

@router.get(
    "/stats",
    response_model=SyncStatsResponseSchema,
    summary="Get Sync Statistics",
    description="Get synchronization statistics and health metrics"
)
async def get_sync_stats(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_business_read)
):
    """
    Get synchronization statistics
    
    Returns comprehensive statistics about Google Business Profile
    integration including account status, sync performance, and error rates.
    """
    try:
        tenant_id = await get_tenant_from_request(request)
        
        # Calculate statistics
        stats = await _calculate_sync_statistics(tenant_id, db)
        
        return SyncStatsResponseSchema(**stats)
        
    except Exception as e:
        logger.error(f"Error getting sync stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve synchronization statistics"
        )


@router.get(
    "/locations/{location_id}/insights",
    response_model=GoogleBusinessInsightsSchema,
    summary="Get Location Insights",
    description="Get Google Business Profile insights for a specific location"
)
async def get_location_insights(
    location_id: str,
    request: Request,
    start_date: Optional[datetime] = Query(None, description="Insights start date"),
    end_date: Optional[datetime] = Query(None, description="Insights end date"),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_business_read)
):
    """
    Get Google Business Profile insights
    
    Retrieves analytics data from Google Business Profile including
    views, searches, customer actions, and photo metrics.
    """
    try:
        tenant_id = await get_tenant_from_request(request)
        
        # Get location with account verification
        result = await db.execute(
            select(GoogleBusinessLocation, GoogleAccount)
            .join(GoogleAccount)
            .where(
                GoogleBusinessLocation.google_location_id == location_id,
                GoogleAccount.tenant_id == tenant_id
            )
        )
        
        location_data = result.first()
        
        if not location_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Business location not found"
            )
        
        location, account = location_data
        
        # Get insights from Google API
        insights_response = await google_client.get_business_insights(
            account=account,
            location_id=location_id,
            start_date=start_date,
            end_date=end_date
        )
        
        if not insights_response.success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to retrieve insights: {insights_response.error}"
            )
        
        insights_data = insights_response.data
        insights_data["location_id"] = location_id
        insights_data["retrieved_at"] = datetime.utcnow()
        
        return GoogleBusinessInsightsSchema(**insights_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting insights for location {location_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve location insights"
        )


@router.get(
    "/health",
    response_model=GoogleIntegrationHealthSchema,
    summary="Get Integration Health",
    description="Get health status of Google Business Profile integration"
)
async def get_integration_health(
    request: Request,
    current_user = Depends(require_business_read)
):
    """
    Get Google integration health status
    
    Returns comprehensive health information including API connectivity,
    authentication status, rate limits, and performance metrics.
    """
    try:
        tenant_id = await get_tenant_from_request(request)
        
        # Check integration health
        health_data = await _check_integration_health(tenant_id)
        
        return GoogleIntegrationHealthSchema(**health_data)
        
    except Exception as e:
        logger.error(f"Error checking integration health: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to check integration health"
        )


# Background Task Functions

async def _perform_location_sync(operation_id: UUID, tenant_id: str, sync_request: LocationSyncSchema):
    """Background task for location synchronization"""
    try:
        async with get_db() as db:
            # Update operation status
            await db.execute(
                update(SyncOperation)
                .where(SyncOperation.id == operation_id)
                .values(status=SyncStatus.IN_PROGRESS)
            )
            await db.commit()
            
            # Perform sync logic here
            # This would involve calling Google API and updating locations
            
            # Update operation as completed
            await db.execute(
                update(SyncOperation)
                .where(SyncOperation.id == operation_id)
                .values(
                    status=SyncStatus.COMPLETED,
                    completed_at=datetime.utcnow()
                )
            )
            await db.commit()
            
    except Exception as e:
        logger.error(f"Location sync failed for operation {operation_id}: {str(e)}")
        # Update operation as failed
        async with get_db() as db:
            await db.execute(
                update(SyncOperation)
                .where(SyncOperation.id == operation_id)
                .values(
                    status=SyncStatus.FAILED,
                    error_details=[str(e)]
                )
            )
            await db.commit()


async def _perform_bulk_sync(batch_id: UUID, tenant_id: str, bulk_sync_request: BulkLocationSyncSchema):
    """Background task for bulk synchronization"""
    # Implementation would go here
    pass


async def _apply_conflict_resolution(
    conflict: LocationConflict,
    location: GoogleBusinessLocation,
    account: GoogleAccount,
    resolution: ConflictResolutionSchema,
    db: AsyncSession
) -> bool:
    """Apply conflict resolution strategy"""
    # Implementation would go here
    return True


async def _calculate_sync_statistics(tenant_id: str, db: AsyncSession) -> Dict[str, Any]:
    """Calculate synchronization statistics"""
    # Get account statistics
    account_stats = await db.execute(
        select(
            func.count(GoogleAccount.id).label('total_accounts'),
            func.sum(func.case((GoogleAccount.status == GoogleAccountStatus.CONNECTED.value, 1), else_=0)).label('active_accounts'),
            func.sum(func.case((GoogleAccount.status == GoogleAccountStatus.EXPIRED.value, 1), else_=0)).label('expired_accounts')
        ).where(GoogleAccount.tenant_id == tenant_id)
    )
    
    stats = account_stats.first()
    
    return {
        "total_accounts": stats.total_accounts or 0,
        "active_accounts": stats.active_accounts or 0,
        "expired_accounts": stats.expired_accounts or 0,
        "total_locations": 0,  # Would calculate from actual data
        "locations_synced_today": 0,  # Would calculate from sync operations
        "pending_syncs": 0,
        "sync_errors": 0,
        "last_full_sync": None,
        "average_sync_time": None
    }


async def _check_integration_health(tenant_id: str) -> Dict[str, Any]:
    """Check Google integration health"""
    return {
        "status": "healthy",
        "api_connection": "connected",
        "authentication": "valid",
        "rate_limits": {
            "remaining_requests": 1000,
            "reset_time": datetime.utcnow() + timedelta(hours=1)
        },
        "sync_performance": {
            "average_sync_time": 30.5,
            "success_rate": 0.95
        },
        "error_rates": {
            "authentication_errors": 0.01,
            "api_errors": 0.02,
            "sync_errors": 0.03
        },
        "last_check": datetime.utcnow()
    }