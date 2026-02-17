from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.auth import UserSignup, UserLogin, AuthResponse
from app.dependencies import get_identity_port
from app.domain.ports.identity_port import IdentityPort
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=AuthResponse)
async def signup(
    user_data: UserSignup,
    identity: IdentityPort = Depends(get_identity_port)
):
    """
    Register a new user via Authentik.
    """
    logger.info(f"Attempting signup for {user_data.email}")
    
    # 1. Check if user exists
    # Note: Authentik might handle this check internally during create, 
    # but explicit check is safer for custom error messages.
    if hasattr(identity, 'check_user_exists'):
        exists = await identity.check_user_exists(user_data.email)
        if exists:
            logger.warning(f"Signup failed: User {user_data.email} already exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="User with this email already exists"
            )
    
    # 2. Prepare attributes
    attributes = {}
    if user_data.company:
        attributes["company"] = user_data.company
    if user_data.phone:
        attributes["phone"] = user_data.phone
        
    # 3. Create User
    # Note: We need to cast identity to AuthentikAdapter to access create_user 
    # if it's not in the IdentityPort interface, but we added it to the class.
    # Ideally, we should update the interface, but Python is dynamic.
    if not hasattr(identity, 'create_user'):
         logger.error("Identity adapter does not support user creation")
         raise HTTPException(
             status_code=status.HTTP_501_NOT_IMPLEMENTED,
             detail="Signup not supported by current identity provider"
         )

    new_user = await identity.create_user(
        email=user_data.email,
        name=user_data.name,
        password=user_data.password,
        attributes=attributes
    )
    
    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user. Please try again later."
        )

    logger.info(f"User created successfully: {new_user.id}")

    # Return success
    # We don't have a token yet because we haven't logged in.
    return {
        "token": "", # No token generated on signup yet
        "user": {
            "id": new_user.id,
            "email": new_user.email,
            "name": new_user.name,
            "role": "client", # Default
            "tenant_id": new_user.tenant_id
        },
        "message": "Account created successfully. Please log in."
    }

@router.post("/login")
async def login(
    credentials: UserLogin,
    identity: IdentityPort = Depends(get_identity_port)
):
    # TODO: Implement Login Proxy to Authentik
    # For now, we return 501 or try to implement if we figure out the flow
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Backend login proxy not yet implemented. Please use frontend direct auth or SSO."
    )
