# Google My Business (GMB) Integration Strategy

## Current State Analysis

### What We Have Now
- Manual company name input
- Optional website URL
- Location field (free text)
- Industry dropdown
- GMB link field (paste Google Maps URL)

### What's Missing
- No real GMB API integration
- No auto-detection of GMB profiles
- No verification of business ownership
- No automatic data population from GMB

## Research: GMB Integration Approaches

### Option 1: Google Business Profile API (Recommended)

**How It Works:**
1. User authenticates with Google OAuth
2. API fetches all GMB locations user has access to
3. User selects their business from dropdown
4. All business data auto-populates (name, address, phone, hours, photos, etc.)

**Pros:**
✅ Official Google API - most reliable
✅ Auto-populates 20+ fields (name, address, phone, hours, categories, photos)
✅ Verifies business ownership automatically
✅ Can update GMB data from platform (two-way sync)
✅ Access to reviews, Q&A, insights, posts
✅ No manual data entry errors
✅ Can manage multiple locations

**Cons:**
❌ Requires Google account connection (OAuth)
❌ User must have GMB access/ownership
❌ API has quota limits (10,000 requests/day free tier)
❌ Requires Google Cloud project setup

**API Endpoints:**
```
GET /v1/accounts
GET /v1/accounts/{accountId}/locations
GET /v1/accounts/{accountId}/locations/{locationId}
PATCH /v1/accounts/{accountId}/locations/{locationId}
```

**Data Available:**
- Business name, category, description
- Full address, phone, website
- Business hours (regular + special)
- Service areas
- Photos (profile, cover, additional)
- Reviews and ratings
- Attributes (wheelchair accessible, etc.)
- Posts and updates
- Insights (views, searches, actions)

### Option 2: Google Places API (Alternative)

**How It Works:**
1. User types business name
2. Autocomplete suggests businesses from Google Places
3. User selects their business
4. Basic data auto-populates

**Pros:**
✅ No OAuth required initially
✅ Works for businesses not yet claimed on GMB
✅ Good UX with autocomplete
✅ Can search by name + location
✅ Simpler implementation

**Cons:**
❌ Read-only (can't update GMB data)
❌ Limited data compared to Business Profile API
❌ No ownership verification
❌ Can't access reviews, insights, posts
❌ User might select wrong business
❌ Costs $17 per 1000 requests after free tier

**API Endpoints:**
```
GET /maps/api/place/autocomplete/json
GET /maps/api/place/details/json
```

**Data Available:**
- Business name, address, phone
- Website, rating, reviews count
- Photos (limited)
- Opening hours
- Place ID (for future reference)

### Option 3: Hybrid Approach (Best of Both Worlds)

**How It Works:**
1. **Step 1A - Quick Search**: User types business name → Places API autocomplete
2. **Step 1B - Claim & Connect**: "Is this your business?" → OAuth → Business Profile API
3. **Step 1C - Verify Ownership**: Check if user has GMB access
4. **Step 1D - Full Sync**: Populate all fields from GMB

**Pros:**
✅ Best UX - fast initial search
✅ Progressive enhancement
✅ Works for unclaimed businesses
✅ Full data access after OAuth
✅ Ownership verification
✅ Two-way sync capability

**Cons:**
❌ More complex implementation
❌ Uses both APIs (more quota)
❌ Requires careful error handling

## Recommended Implementation

### 🎯 **Hybrid Approach with Smart Fallbacks**

```typescript
// Step 1: Quick Business Search (Places API)
interface BusinessSearchFlow {
  1. User types business name
  2. Show autocomplete suggestions (Places API)
  3. User selects business
  4. Populate basic fields (name, address, phone, website)
  5. Show "Claim & Connect" button
}

// Step 2: Ownership Verification (Business Profile API)
interface OwnershipVerificationFlow {
  1. User clicks "Claim & Connect"
  2. Trigger Google OAuth
  3. Fetch user's GMB accounts
  4. Check if selected business is in their accounts
  5. If yes → Full sync
  6. If no → Show "Request Access" or "Continue without GMB"
}

// Step 3: Full Data Sync (Business Profile API)
interface FullSyncFlow {
  1. Fetch complete business data
  2. Populate all onboarding fields
  3. Store GMB account ID + location ID
  4. Enable ongoing sync
  5. Show "GMB Connected" badge
}
```

### Implementation Phases

#### Phase 1: Places API Autocomplete (Week 1)
```typescript
// Add to CompanyIdentityStep.tsx
const [searchQuery, setSearchQuery] = useState('');
const [suggestions, setSuggestions] = useState([]);

const searchBusiness = async (query: string) => {
  const res = await fetch(`/api/brain/onboarding/gmb/search?q=${query}`);
  const data = await res.json();
  setSuggestions(data.predictions);
};

const selectBusiness = async (placeId: string) => {
  const res = await fetch(`/api/brain/onboarding/gmb/details?placeId=${placeId}`);
  const business = await res.json();
  
  onUpdate({
    companyName: business.name,
    location: business.formatted_address,
    phone: business.formatted_phone_number,
    website: business.website,
    placeId: placeId // Store for later
  });
};
```

#### Phase 2: OAuth & Business Profile API (Week 2)
```typescript
// Add "Claim & Connect" button
const connectGMB = async () => {
  // Trigger OAuth
  const authUrl = await fetch('/api/brain/onboarding/gmb/auth-url');
  window.location.href = authUrl.url;
};

// After OAuth callback
const verifyOwnership = async () => {
  const accounts = await fetch('/api/brain/onboarding/gmb/accounts');
  const locations = await fetch(`/api/brain/onboarding/gmb/locations?accountId=${accountId}`);
  
  // Check if placeId matches any location
  const ownedLocation = locations.find(loc => loc.placeId === data.placeId);
  
  if (ownedLocation) {
    // Full sync
    await syncGMBData(ownedLocation.name);
  } else {
    // Show "You don't own this business" message
  }
};
```

#### Phase 3: Two-Way Sync (Week 3)
```typescript
// Sync GMB data to platform
const syncGMBData = async (locationName: string) => {
  const gmbData = await fetch(`/api/brain/onboarding/gmb/location?name=${locationName}`);
  
  onUpdate({
    companyName: gmbData.title,
    location: gmbData.address,
    phone: gmbData.phoneNumbers.primaryPhone,
    website: gmbData.websiteUri,
    description: gmbData.profile.description,
    businessHours: gmbData.regularHours,
    categories: gmbData.categories,
    photos: gmbData.media,
    gmbConnected: true,
    gmbLocationName: locationName // Store for updates
  });
};

// Update GMB from platform (future)
const updateGMB = async (updates: Partial<BusinessProfile>) => {
  await fetch('/api/brain/onboarding/gmb/update', {
    method: 'PATCH',
    body: JSON.stringify({
      locationName: data.gmbLocationName,
      updates: updates
    })
  });
};
```

### Backend Implementation

```python
# brain-gateway/app/api/gmb.py
from fastapi import APIRouter, Depends
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

router = APIRouter(prefix="/gmb")

@router.get("/search")
async def search_business(q: str):
    """Places API autocomplete"""
    places = build('places', 'v1')
    result = places.autocomplete(input=q, types='establishment').execute()
    return result

@router.get("/details")
async def get_business_details(placeId: str):
    """Places API details"""
    places = build('places', 'v1')
    result = places.details(place_id=placeId, fields='name,formatted_address,formatted_phone_number,website').execute()
    return result['result']

@router.get("/auth-url")
async def get_oauth_url():
    """Generate OAuth URL for GMB access"""
    # Return Google OAuth URL with GMB scopes
    return {"url": "https://accounts.google.com/o/oauth2/v2/auth?..."}

@router.get("/accounts")
async def get_gmb_accounts(credentials: Credentials = Depends(get_user_credentials)):
    """Fetch user's GMB accounts"""
    gmb = build('mybusinessaccountmanagement', 'v1', credentials=credentials)
    accounts = gmb.accounts().list().execute()
    return accounts

@router.get("/locations")
async def get_gmb_locations(accountId: str, credentials: Credentials = Depends(get_user_credentials)):
    """Fetch locations for an account"""
    gmb = build('mybusinessbusinessinformation', 'v1', credentials=credentials)
    locations = gmb.accounts().locations().list(parent=f'accounts/{accountId}').execute()
    return locations

@router.get("/location")
async def get_location_details(name: str, credentials: Credentials = Depends(get_user_credentials)):
    """Get full location data"""
    gmb = build('mybusinessbusinessinformation', 'v1', credentials=credentials)
    location = gmb.accounts().locations().get(name=name, readMask='*').execute()
    return location

@router.patch("/update")
async def update_location(locationName: str, updates: dict, credentials: Credentials = Depends(get_user_credentials)):
    """Update GMB location"""
    gmb = build('mybusinessbusinessinformation', 'v1', credentials=credentials)
    result = gmb.accounts().locations().patch(name=locationName, body=updates, updateMask=','.join(updates.keys())).execute()
    return result
```

## Cost Analysis

### Google Places API
- **Free Tier**: $200/month credit (~11,764 autocomplete requests)
- **After Free**: $2.83 per 1000 autocomplete, $17 per 1000 details
- **Estimated Monthly Cost**: $50-100 (for 1000 onboardings)

### Google Business Profile API
- **Free Tier**: 10,000 requests/day
- **After Free**: Contact Google for pricing
- **Estimated Monthly Cost**: $0 (within free tier for most use cases)

### Total Estimated Cost
- **Phase 1 Only**: $50-100/month
- **Phase 1 + 2**: $50-100/month (GMB API is free)
- **ROI**: Saves 5-10 minutes per onboarding = massive time savings

## Security Considerations

1. **OAuth Tokens**: Store encrypted in Vault
2. **API Keys**: Restrict by IP, domain, and API
3. **Rate Limiting**: Implement on backend to avoid quota exhaustion
4. **Data Privacy**: Only fetch data user has access to
5. **Consent**: Clear messaging about what data is accessed

## UX Flow Diagram

```
┌─────────────────────────────────────────────────────────┐
│ Step 1: Company Identity                                │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  [Search for your business]                             │
│  ┌──────────────────────────────────────────┐          │
│  │ Acme Corp                          🔍    │          │
│  └──────────────────────────────────────────┘          │
│                                                          │
│  Suggestions:                                            │
│  ┌──────────────────────────────────────────┐          │
│  │ ✓ Acme Corp - 123 Main St, NYC          │ ← Click   │
│  │   Acme Corporation - 456 Elm St, LA      │          │
│  │   Acme Industries - 789 Oak Ave, SF      │          │
│  └──────────────────────────────────────────┘          │
│                                                          │
│  ┌────────────────────────────────────────────────────┐│
│  │ ✓ Business Found!                                  ││
│  │                                                     ││
│  │ Name: Acme Corp                                    ││
│  │ Address: 123 Main St, New York, NY 10001          ││
│  │ Phone: +1 (555) 123-4567                          ││
│  │ Website: https://acmecorp.com                      ││
│  │                                                     ││
│  │ [Claim & Connect to Google] [Continue without GMB] ││
│  └────────────────────────────────────────────────────┘│
│                                                          │
│  ↓ User clicks "Claim & Connect"                        │
│                                                          │
│  [Google OAuth Screen]                                  │
│  "BizoSaaS wants to access your Google My Business"    │
│  [Allow] [Deny]                                         │
│                                                          │
│  ↓ After OAuth                                          │
│                                                          │
│  ┌────────────────────────────────────────────────────┐│
│  │ ✓ GMB Connected!                                   ││
│  │                                                     ││
│  │ We've synced all your business data:               ││
│  │ • Business hours                                   ││
│  │ • Categories                                       ││
│  │ • Photos (12)                                      ││
│  │ • Reviews (4.8 ⭐ from 127 reviews)                ││
│  │ • Recent posts (3)                                 ││
│  │                                                     ││
│  │ [Continue to Next Step →]                          ││
│  └────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────┘
```

## Recommendation Summary

### ✅ **Implement Hybrid Approach**

**Phase 1 (Immediate):**
- Add Places API autocomplete for business search
- Auto-populate basic fields (name, address, phone, website)
- Store Place ID for future reference

**Phase 2 (Next Sprint):**
- Add "Claim & Connect" button
- Implement Google OAuth for GMB
- Verify business ownership
- Full data sync from Business Profile API

**Phase 3 (Future):**
- Two-way sync (update GMB from platform)
- Multi-location support
- GMB insights dashboard
- Review management

**Why This Approach:**
1. **Progressive Enhancement**: Works immediately with Places API, enhances with GMB
2. **Best UX**: Fast autocomplete, optional deep integration
3. **Ownership Verification**: Only connects if user actually owns the business
4. **Future-Proof**: Can add GMB management features later
5. **Cost-Effective**: Stays within free tiers for most use cases

---

**Next Steps:**
1. Set up Google Cloud project
2. Enable Places API + Business Profile API
3. Implement Phase 1 (autocomplete)
4. Test with real businesses
5. Roll out Phase 2 (OAuth + full sync)
