from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
from app.models.directory import DirectoryListing, DirectoryAnalytics, DirectoryClaimRequest
from typing import List, Optional, Dict, Any
from datetime import datetime, date, timedelta
import os
import httpx
import json
import logging
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.connectors.twilio import TwilioConnector


logger = logging.getLogger(__name__)

class DirectoryService:
    def __init__(self, db: Session):
        self.db = db

    async def search(
        self,
        query: Optional[str] = None,
        location: Optional[str] = None,
        category: Optional[str] = None,
        page: int = 1,
        limit: int = 20,
        use_google: bool = True
    ) -> Dict[str, Any]:
        """Search directory listings with hybrid internal + Google logic"""
        # 1. Search internal DB
        db_q = self.db.query(DirectoryListing).filter(DirectoryListing.status == 'active')

        if query:
            search_filter = or_(
                DirectoryListing.business_name.ilike(f"%{query}%"),
                DirectoryListing.description.ilike(f"%{query}%"),
                DirectoryListing.category.ilike(f"%{query}%"),
                DirectoryListing.keywords.any(query)
            )
            db_q = db_q.filter(search_filter)

        if location:
            db_q = db_q.filter(or_(
                DirectoryListing.city.ilike(f"%{location}%"),
                DirectoryListing.address.ilike(f"%{location}%")
            ))

        if category:
            db_q = db_q.filter(DirectoryListing.category == category)

        total_internal = db_q.count()
        listings = db_q.order_by(desc(DirectoryListing.created_at)).offset((page - 1) * limit).limit(limit).all()

        # 2. If we have query and want to augment with Google
        if use_google and query and len(listings) < limit:
            google_results = await self._search_google_places(query, location)
            
            # Incorporate Google results that don't already exist in our DB
            existing_place_ids = {l.google_place_id for l in listings if l.google_place_id}
            
            for g_res in google_results:
                place_id = g_res.get("place_id")
                if place_id and place_id not in existing_place_ids:
                    # Check if it exists in DB but wasn't in the initial listing search
                    exists_in_db = self.db.query(DirectoryListing).filter(DirectoryListing.google_place_id == place_id).first()
                    
                    if not exists_in_db:
                        # Create a "ghost" listing to populate the directory
                        new_listing = await self._create_ghost_listing(g_res)
                        if new_listing:
                            listings.append(new_listing)
                            total_internal += 1
                    else:
                        # If it exists in DB but was missed by filters, add it to current view
                        if exists_in_db not in listings:
                            listings.append(exists_in_db)

        # Sort combined results: Featured/Claimed first, then by rating, then by date
        listings.sort(key=lambda x: (x.claimed, float(x.google_rating or 0), x.created_at), reverse=True)
        
        # Paginate the combined results
        paginated_listings = listings[(page - 1) * limit : page * limit]

        return {
            "businesses": paginated_listings,
            "total": total_internal,
            "page": page,
            "limit": limit,
            "source": "hybrid"
        }

    async def _search_google_places(self, query: str, location: Optional[str] = None) -> List[Dict[str, Any]]:
        """Helper to call Google Places Text Search API"""
        api_key = os.getenv("GOOGLE_MAPS_API_KEY", "AIzaSyBZxfvuglTrcCIZZfSVDTltjBWTgEuRLto")
        search_query = f"{query} {location}" if location else query
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    "https://maps.googleapis.com/maps/api/place/textsearch/json",
                    params={
                        "query": search_query,
                        "key": api_key
                    }
                )
                if response.status_code == 200:
                    data = response.json()
                    return data.get("results", [])
            except Exception as e:
                logger.error(f"Google Places search error: {e}")
        return []

    async def _create_ghost_listing(self, google_res: Dict[str, Any]) -> Optional[DirectoryListing]:
        """Create an unclaimed listing from Google data"""
        try:
            name = google_res.get("name")
            place_id = google_res.get("place_id")
            address = google_res.get("formatted_address")
            
            # Generate slug
            import re
            slug_base = f"{name} {address.split(',')[0] if address else ''}".lower()
            slug = re.sub(r'[^a-zA-Z0-9]', '-', slug_base)
            slug = re.sub(r'-+', '-', slug).strip('-')
            
            # Ensure unique slug
            unique_slug = slug
            counter = 1
            while self.db.query(DirectoryListing).filter(DirectoryListing.business_slug == unique_slug).first():
                unique_slug = f"{slug}-{counter}"
                counter += 1

            listing = DirectoryListing(
                business_slug=unique_slug,
                business_name=name,
                google_place_id=place_id,
                address=address,
                google_rating=google_res.get("rating"),
                google_reviews_count=google_res.get("user_ratings_total"),
                google_data=google_res,
                status='active',
                visibility='public',
                claimed=False,
                verification_status='unverified'
            )
            
            # Extract city/country from formatted address if possible
            if address:
                parts = address.split(',')
                if len(parts) >= 2:
                    listing.city = parts[-3].strip() if len(parts) >= 3 else parts[-2].strip()
                    listing.country = parts[-1].strip()

            self.db.add(listing)
            self.db.commit()
            self.db.refresh(listing)
            
            # Trigger AI optimization in background to enrich the listing
            import asyncio
            asyncio.create_task(self.optimize_listing_seo(listing.id))
            
            return listing
        except Exception as e:
            logger.error(f"Failed to create ghost listing: {e}")
            self.db.rollback()
            return None

    async def autocomplete(self, query: str, location: Optional[str] = None) -> List[Dict[str, Any]]:
        """Fast autocomplete for directory search"""
        # 1. Internal matches
        internal_matches = self.db.query(DirectoryListing).filter(
            DirectoryListing.business_name.ilike(f"%{query}%")
        ).limit(5).all()
        
        results = [
            {"text": l.business_name, "id": str(l.id), "type": "internal", "slug": l.business_slug}
            for l in internal_matches
        ]
        
        # 2. Add Google suggestions if needed
        if len(results) < 10:
            api_key = os.getenv("GOOGLE_MAPS_API_KEY", "AIzaSyBZxfvuglTrcCIZZfSVDTltjBWTgEuRLto")
            async with httpx.AsyncClient() as client:
                try:
                    params = {"input": query, "key": api_key, "types": "establishment"}
                    if location:
                        params["location"] = location # Note: This needs lat,lng or bias
                    
                    response = await client.get(
                        "https://maps.googleapis.com/maps/api/place/autocomplete/json",
                        params=params
                    )
                    if response.status_code == 200:
                        data = response.json()
                        for pred in data.get("predictions", []):
                            results.append({
                                "text": pred.get("description"),
                                "id": pred.get("place_id"),
                                "type": "google"
                            })
                except Exception as e:
                    logger.error(f"Google autocomplete error: {e}")
                    
        return results

    async def get_by_slug(self, slug: str) -> Optional[DirectoryListing]:
        """Get listing by business slug"""
        return self.db.query(DirectoryListing).filter(DirectoryListing.business_slug == slug).first()

    async def get_user_listings(self, user_id: UUID) -> List[DirectoryListing]:
        """Get all listings claimed by a user"""
        return self.db.query(DirectoryListing).filter(
            DirectoryListing.claimed == True,
            DirectoryListing.claimed_by == user_id
        ).order_by(desc(DirectoryListing.created_at)).all()

    async def create_from_places_data(self, data: Dict[str, Any], user_id: Optional[UUID] = None) -> DirectoryListing:
        """Create a listing from Google Places data"""
        slug = data.get("slug")
        if not slug:
            # Simple fallback slug generation
            name = data.get("name", "unknown")
            location = data.get("location", "")
            import re
            slug = re.sub(r'[^a-zA-Z0-9]', '-', f"{name} {location}".lower())
            slug = re.sub(r'-+', '-', slug).strip('-')

        # Check for existing
        existing = await self.get_by_slug(slug)
        if existing:
            return existing

        listing = DirectoryListing(
            business_slug=slug,
            business_name=data.get("name"),
            google_place_id=data.get("google_place_id"),
            address=data.get("location"),
            city=data.get("city"),
            state=data.get("state"),
            country=data.get("country"),
            postal_code=data.get("postal_code"),
            phone=data.get("phone"),
            website=data.get("website"),
            category=data.get("category"),
            google_data=data.get("google_data"),
            google_rating=data.get("google_rating"),
            google_reviews_count=data.get("google_reviews_count"),
            status='active',
            visibility='public'
        )

        if user_id:
            listing.claimed_by = user_id
            listing.claimed = True
            listing.claimed_at = datetime.utcnow()
            listing.verification_status = 'verified'

        self.db.add(listing)
        self.db.commit()
        self.db.refresh(listing)
        return listing

    async def log_view(self, listing_id: UUID):
        """Log a page view for a listing"""
        today = date.today()
        analytics = self.db.query(DirectoryAnalytics).filter(
            DirectoryAnalytics.listing_id == listing_id,
            DirectoryAnalytics.date == today
        ).first()

        if not analytics:
            analytics = DirectoryAnalytics(
                listing_id=listing_id,
                date=today,
                page_views=1,
                unique_visitors=1
            )
            self.db.add(analytics)
        else:
            analytics.page_views += 1
            # In a real app, unique visitors would check sessions/IP
            analytics.unique_visitors += 1 

        self.db.commit()

    async def log_click(self, listing_id: UUID, click_type: str):
        """Log engagement clicks (phone, website, directions)"""
        today = date.today()
        analytics = self.db.query(DirectoryAnalytics).filter(
            DirectoryAnalytics.listing_id == listing_id,
            DirectoryAnalytics.date == today
        ).first()

        if not analytics:
            analytics = DirectoryAnalytics(listing_id=listing_id, date=today)
            self.db.add(analytics)

        if click_type == 'phone':
            analytics.phone_clicks += 1
        elif click_type == 'website':
            analytics.website_clicks += 1
        elif click_type == 'directions':
            analytics.direction_clicks += 1

        self.db.commit()

    async def create_claim_request(self, listing_id: UUID, user_id: UUID, method: str, data: Dict[str, Any]) -> DirectoryClaimRequest:
        """Create a new claim request with a verification code"""
        # Generate 6-digit code
        code = ''.join(random.choices(string.digits, k=6))
        expiry = datetime.utcnow() + timedelta(minutes=60) # 1 hour expiry
        
        request = DirectoryClaimRequest(
            listing_id=listing_id,
            user_id=user_id,
            verification_method=method,
            verification_data=data,
            verification_code=code,
            verification_expiry=expiry,
            status='pending'
        )
        self.db.add(request)
        self.db.commit()
        self.db.refresh(request)
        
        # Try to send the code
        send_success = False
        try:
            if method == 'email' and data.get('email'):
                await self._send_email_code(data['email'], code)
                send_success = True
            elif method == 'phone' and data.get('phone'):
                await self._send_sms_code(data['phone'], code)
                send_success = True
            else:
                logger.warning(f"Unknown verification method or missing data: {method}, {data}")
        except Exception as e:
            logger.error(f"Failed to send verification code: {e}")
            # We don't raise here, we let the request be created but maybe show a warning?
            # For now, we assume it might be dev mode where we just log.
            pass

        # Log the code (dev mode / backup)
        target = data.get("email") or data.get("phone") or "unknown"
        logger.info(f"DIRECTORY CLAIM: Code {code} generated for listing {listing_id}. Method: {method}, Target: {target}. Send Success: {send_success}")
        
        return request

    async def resend_claim_code(self, claim_id: UUID, user_id: UUID) -> Dict[str, Any]:
        """Resend verification code for an existing claim"""
        from app.models.directory import DirectoryClaimRequest
        claim = self.db.query(DirectoryClaimRequest).filter(
            DirectoryClaimRequest.id == claim_id,
            DirectoryClaimRequest.user_id == user_id,
            DirectoryClaimRequest.status == 'pending'
        ).first()
        
        if not claim:
            return {"error": "Claim request not found"}
            
        # Generate new code
        code = ''.join(random.choices(string.digits, k=6))
        expiry = datetime.utcnow() + timedelta(minutes=60)
        
        claim.verification_code = code
        claim.verification_expiry = expiry
        self.db.commit()
        
        # Resend logic
        method = claim.verification_method
        data = claim.verification_data or {}
        
        try:
            if method == 'email' and data.get('email'):
                await self._send_email_code(data['email'], code)
            elif method == 'phone' and data.get('phone'):
                await self._send_sms_code(data['phone'], code)
            else:
                return {"error": "Invalid verification data for resend"}
        except Exception as e:
            logger.error(f"Failed to resend code: {e}")
            return {"error": str(e)}
            
        return {"success": True, "message": "Verification code resent successfully"}

    async def _send_email_code(self, to_email: str, code: str):
        """Send verification code via SMTP"""
        smtp_host = os.getenv("SMTP_HOST")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        smtp_user = os.getenv("SMTP_USER")
        smtp_pass = os.getenv("SMTP_PASSWORD")
        smtp_from = os.getenv("SMTP_FROM_EMAIL", "noreply@bizdirectory.com")

        if not (smtp_host and smtp_user and smtp_pass):
            logger.warning("SMTP not configured, skipping email send")
            return

        msg = MIMEMultipart()
        msg['From'] = smtp_from
        msg['To'] = to_email
        msg['Subject'] = "Your Business Verification Code"

        body = f"""
        <html>
            <body>
                <h2>Verify your Business Claim</h2>
                <p>Use the following code to verify your claim for the business listing:</p>
                <h1 style="font-size: 32px; letter-spacing: 5px; color: #333;">{code}</h1>
                <p>This code will expire in 1 hour.</p>
                <p>If you didn't request this, please ignore this email.</p>
            </body>
        </html>
        """
        msg.attach(MIMEText(body, 'html'))

        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
            
    async def _send_sms_code(self, to_phone: str, code: str):
        """Send verification code via Twilio"""
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        from_number = os.getenv("TWILIO_FROM_NUMBER")

        if not (account_sid and auth_token and from_number):
            logger.warning("Twilio not configured, skipping SMS send")
            return

        connector = TwilioConnector()
        # Manually inject credentials since we are using system envs
        connector.credentials = {
            "account_sid": account_sid,
            "auth_token": auth_token,
            "from_number": from_number
        }
        
        await connector.perform_action("send_sms", {
            "to": to_phone,
            "body": f"Your verification code is: {code}. Expires in 1 hour."
        })

    async def verify_claim_code(self, claim_id: UUID, user_id: UUID, code: str) -> Dict[str, Any]:
        """Verify the code and automatically approve claim if valid"""
        claim = self.db.query(DirectoryClaimRequest).filter(
            DirectoryClaimRequest.id == claim_id,
            DirectoryClaimRequest.user_id == user_id,
            DirectoryClaimRequest.status == 'pending'
        ).first()
        
        if not claim:
            return {"success": False, "error": "Claim request not found or unauthorized"}
            
        if datetime.utcnow() > claim.verification_expiry:
            return {"success": False, "error": "Verification code expired"}
            
        if claim.verification_code != code:
            return {"success": False, "error": "Invalid verification code"}
            
        # Success! Approve it
        await self.approve_claim(claim.id, user_id)
        
        return {
            "success": True, 
            "message": "Business claim verified and approved!",
            "listing_id": str(claim.listing_id)
        }

    async def get_directory_stats(self) -> Dict[str, Any]:
        """Get high-level stats for directory management"""
        from sqlalchemy import func
        total_listings = self.db.query(DirectoryListing).count()
        claimed_listings = self.db.query(DirectoryListing).filter(DirectoryListing.claimed == True).count()
        pending_claims = self.db.query(DirectoryClaimRequest).filter(DirectoryClaimRequest.status == 'pending').count()
        
        # Total views across all time
        total_views = self.db.query(func.sum(DirectoryAnalytics.page_views)).scalar() or 0
        
        return {
            "total_listings": total_listings,
            "claimed_listings": claimed_listings,
            "pending_claims": pending_claims,
            "total_views": int(total_views)
        }

    async def update_listing(self, listing_id: UUID, data: Dict[str, Any]) -> DirectoryListing:
        """Update an existing listing"""
        listing = self.db.query(DirectoryListing).filter(DirectoryListing.id == listing_id).first()
        if not listing:
            raise ValueError("Listing not found")
        
        for key, value in data.items():
            if hasattr(listing, key):
                setattr(listing, key, value)
        
        listing.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(listing)
        return listing

    async def create_enquiry(self, listing_id: UUID, data: dict):
        from app.models.directory import DirectoryEnquiry
        from fastapi import HTTPException
        
        enquiry = DirectoryEnquiry(
            listing_id=listing_id,
            name=data["name"],
            email=data["email"],
            phone=data.get("phone"),
            subject=data.get("subject"),
            message=data["message"]
        )
        self.db.add(enquiry)
        self.db.commit()
        self.db.refresh(enquiry)
        
        # TODO: Trigger automation workflow (email notification, AI enrichment)
        
        return enquiry

    async def get_enquiries(self, listing_id: UUID, user_id: UUID):
        from app.models.directory import DirectoryListing, DirectoryEnquiry
        from fastapi import HTTPException
        
        # Verify ownership
        listing = self.db.query(DirectoryListing).filter(
            DirectoryListing.id == listing_id,
            DirectoryListing.claimed == True,
            DirectoryListing.claimed_by == user_id
        ).first()
        
        if not listing:
            raise HTTPException(status_code=403, detail="Not authorized to view enquiries for this listing")
            
        return self.db.query(DirectoryEnquiry).filter(
            DirectoryEnquiry.listing_id == listing_id
        ).order_by(desc(DirectoryEnquiry.created_at)).all()

    async def update_enquiry_status(self, enquiry_id: UUID, user_id: UUID, status: str):
        from app.models.directory import DirectoryListing, DirectoryEnquiry
        from fastapi import HTTPException
        
        enquiry = self.db.query(DirectoryEnquiry).filter(DirectoryEnquiry.id == enquiry_id).first()
        if not enquiry:
            raise HTTPException(status_code=404, detail="Enquiry not found")
            
        # Verify ownership of the listing
        listing = self.db.query(DirectoryListing).filter(
            DirectoryListing.id == enquiry.listing_id,
            DirectoryListing.claimed == True,
            DirectoryListing.claimed_by == user_id
        ).first()
        
        if not listing:
            raise HTTPException(status_code=403, detail="Not authorized to update this enquiry")
            
        enquiry.status = status
        self.db.commit()
        self.db.refresh(enquiry)
        return enquiry

    async def get_events(self, listing_id: uuid.UUID):
        from app.models.directory import DirectoryEvent
        return self.db.query(DirectoryEvent).filter(
            DirectoryEvent.listing_id == listing_id,
            DirectoryEvent.status != 'cancelled'
        ).order_by(DirectoryEvent.start_date.asc()).all()

    async def create_event(self, listing_id: uuid.UUID, user_id: uuid.UUID, data: dict):
        from app.models.directory import DirectoryListing, DirectoryEvent
        from fastapi import HTTPException
        
        # Verify ownership
        listing = self.db.query(DirectoryListing).filter(
            DirectoryListing.id == listing_id,
            DirectoryListing.claimed == True,
            DirectoryListing.claimed_by == user_id
        ).first()
        
        if not listing:
            raise HTTPException(status_code=403, detail="Not authorized to add events to this listing")
            
        event = DirectoryEvent(
            listing_id=listing_id,
            **data
        )
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event

    async def get_coupons(self, listing_id: uuid.UUID):
        from app.models.directory import DirectoryCoupon
        return self.db.query(DirectoryCoupon).filter(
            DirectoryCoupon.listing_id == listing_id,
            DirectoryCoupon.status == 'active'
        ).order_by(DirectoryCoupon.created_at.desc()).all()

    async def create_coupon(self, listing_id: uuid.UUID, user_id: uuid.UUID, data: dict):
        from app.models.directory import DirectoryListing, DirectoryCoupon
        from fastapi import HTTPException
        
        # Verify ownership
        listing = self.db.query(DirectoryListing).filter(
            DirectoryListing.id == listing_id,
            DirectoryListing.claimed == True,
            DirectoryListing.claimed_by == user_id
        ).first()
        
        if not listing:
            raise HTTPException(status_code=403, detail="Not authorized to add coupons to this listing")
            
        coupon = DirectoryCoupon(
            listing_id=listing_id,
            **data
        )
        self.db.add(coupon)
        self.db.commit()
        self.db.refresh(coupon)
        return coupon

    async def approve_claim(self, claim_id: UUID, admin_id: UUID) -> DirectoryClaimRequest:
        from app.models.directory import DirectoryClaimRequest, DirectoryListing
        claim = self.db.query(DirectoryClaimRequest).filter(DirectoryClaimRequest.id == claim_id).first()
        if not claim:
            raise ValueError("Claim request not found")
        
        claim.status = 'approved'
        claim.reviewed_by = admin_id
        claim.reviewed_at = datetime.utcnow()
        
        # Update listing ownership
        listing = self.db.query(DirectoryListing).filter(DirectoryListing.id == claim.listing_id).first()
        if listing:
            listing.claimed = True
            listing.claimed_by = claim.user_id
            listing.claimed_at = datetime.utcnow()
            listing.verification_status = 'verified'
        
        self.db.commit()
        self.db.refresh(claim)
        return claim

    async def reject_claim(self, claim_id: UUID, admin_id: UUID, reason: str = None) -> DirectoryClaimRequest:
        from app.models.directory import DirectoryClaimRequest
        claim = self.db.query(DirectoryClaimRequest).filter(DirectoryClaimRequest.id == claim_id).first()
        if not claim:
            raise ValueError("Claim request not found")
        
        claim.status = 'rejected'
        claim.reviewed_by = admin_id
        claim.reviewed_at = datetime.utcnow()
        claim.rejection_reason = reason
        
        self.db.commit()
        self.db.refresh(claim)
        return claim

    async def soft_delete_listing(self, listing_id: UUID):
        listing = self.db.query(DirectoryListing).filter(DirectoryListing.id == listing_id).first()
        if not listing:
            raise ValueError("Listing not found")
        
        listing.status = 'deleted'
        self.db.commit()
        return True

    async def optimize_listing_seo(self, listing_id: UUID) -> Dict[str, Any]:
        """Use AI to optimize listing content for SEO"""
        listing = self.db.query(DirectoryListing).filter(DirectoryListing.id == listing_id).first()
        if not listing:
            raise ValueError("Listing not found")
            
        from app.dependencies import get_secret_service
        from app.connectors.registry import ConnectorRegistry
        secret_service = get_secret_service()
        
        # Determine which connector to use using SecretService
        connector_id = "openai"
        api_key = secret_service.get_secret("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
        
        # Check if OpenRouter is preferred/available
        openrouter_key = secret_service.get_secret("OPENROUTER_API_KEY") or os.getenv("OPENROUTER_API_KEY")
        if openrouter_key:
            connector_id = "openrouter"
            api_key = openrouter_key
            
        if not api_key:
            return {"error": "AI optimization not configured (missing API key)"}

        prompt = f"""
        Optimize the following business listing for SEO. 
        Business Name: {listing.business_name}
        Current Description: {listing.description or "No description provided."}
        Category: {listing.category or "General Business"}
        Location: {listing.city or "Unknown"}, {listing.state or ""}, {listing.country or ""}
        
        Provide the result in JSON format with the following fields:
        1. optimized_description: A rich, keyword-optimized description (100-150 words).
        2. meta_title: An SEO title (max 60 chars).
        3. meta_description: An SEO meta description (max 160 chars).
        4. suggested_tags: A list of 5-8 relevant tags like ["service", "keyword", ...].
        """

        try:
            # Instantiate the connector dynamically
            connector = ConnectorRegistry.create_connector(
                connector_id, 
                "system", 
                {"api_key": api_key}
            )
            
            payload = {
                "messages": [
                    {"role": "system", "content": "You are an SEO expert specializing in local business directories."},
                    {"role": "user", "content": prompt}
                ],
                "response_format": { "type": "json_object" },
                # OpenRouter might need full model name, OpenAI handles default if None, or we specify
                "model": "openai/gpt-4o-mini" if connector_id == "openrouter" else "gpt-4o-mini"
            }
            
            response_data = await connector.perform_action("chat", payload)
            
            if "error" in response_data:
                 raise Exception(response_data["error"])
                 
            result_text = response_data["choices"][0]["message"]["content"]
            optimization_data = json.loads(result_text)
            
            # Update listing with optimized data
            listing.description = optimization_data.get("optimized_description", listing.description)
            if "suggested_tags" in optimization_data:
                listing.tags = optimization_data["suggested_tags"]
            
            listing.updated_at = datetime.utcnow()
            self.db.commit()
            
            return optimization_data
        except Exception as e:
            logger.error(f"AI Optimization error: {e}")
            return {"error": str(e)}

    async def analyze_website(self, listing_id: UUID) -> Dict[str, Any]:
        """Analyze business website using AI to enrich profile"""
        import re
        
        listing = self.db.query(DirectoryListing).filter(DirectoryListing.id == listing_id).first()
        if not listing or not listing.website:
            return {"error": "Listing not found or missing website URL"}

        from app.dependencies import get_secret_service
        from app.connectors.registry import ConnectorRegistry
        secret_service = get_secret_service()
        
        # Determine which connector to use using SecretService
        connector_id = "openai"
        api_key = secret_service.get_secret("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
        
        # Check for OpenRouter configuration first
        openrouter_key = secret_service.get_secret("OPENROUTER_API_KEY") or os.getenv("OPENROUTER_API_KEY")
        if openrouter_key:
            connector_id = "openrouter"
            api_key = openrouter_key

        if not api_key:
            return {"error": "AI service not configured"}

        try:
            # 1. Fetch website content
            async with httpx.AsyncClient(verify=False, follow_redirects=True, timeout=10.0) as client:
                response = await client.get(listing.website)
                response.raise_for_status()
                html_content = response.text

            # 2. Extract text (simple regex cleanup)
            text_content = re.sub(r'<[^>]+>', ' ', html_content)
            text_content = re.sub(r'\s+', ' ', text_content).strip()[:4000] # Limit to ~4k chars

            # 3. Analyze with AI
            prompt = f"""
            Analyze the following business website text and extract structured data.
            Return ONLY valid JSON with these keys:
            - description (summary of business, max 300 chars)
            - keywords (list of 5-10 SEO keywords)
            - social_media (dict with keys like facebook, twitter, instagram if found)
            - amenities (list of features founds e.g. "Wifi", "Parking", "Wheelchair Accessible")
            - hours_text (raw hours text if found)

            Website Text:
            {text_content}
            """

            # Instantiate the connector dynamically
            connector = ConnectorRegistry.create_connector(
                connector_id, 
                "system", 
                {"api_key": api_key}
            )
            
            payload = {
                "messages": [
                    {"role": "system", "content": "You are a business data extraction assistant. Output JSON only."},
                    {"role": "user", "content": prompt}
                ],
                "response_format": { "type": "json_object" },
                "temperature": 0.3,
                "model": "openai/gpt-3.5-turbo-0125" if connector_id == "openrouter" else "gpt-3.5-turbo-0125"
            }
            
            ai_response = await connector.perform_action("chat", payload)
            
            if "error" in ai_response:
                 raise Exception(ai_response["error"])
                 
            content = ai_response["choices"][0]["message"]["content"]

            result = json.loads(content)
            
            # 4. Update Listing (Only fill missing fields or append)
            if result.get('description') and not listing.description:
                listing.description = result['description']
                
            if result.get('keywords'):
                existing_tags = set(listing.tags or [])
                new_tags = set(result['keywords'])
                listing.tags = list(existing_tags.union(new_tags))
                
            if result.get('social_media'):
                current_social = dict(listing.social_media or {})
                current_social.update(result['social_media'])
                listing.social_media = current_social
                
            if result.get('amenities'):
                listing.amenities = list(set((listing.amenities or []) + result['amenities']))
            
            listing.updated_at = datetime.utcnow()
            self.db.commit()
            
            return {"success": True, "enriched_data": result}

        except Exception as e:
            logger.error(f"Website analysis failed: {e}")
            return {"error": str(e)}
