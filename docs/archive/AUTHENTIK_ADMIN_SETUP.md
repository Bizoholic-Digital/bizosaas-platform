# Complete Authentik Admin Setup Guide
**Date**: 2026-01-25

## 🎯 Current Status
- ✅ You are logged in as `testadmin`
- ❌ You need to access the Admin Interface to create applications

---

## 📋 Step-by-Step Instructions

### Step 1: Ensure testadmin has Admin Rights

**Run this in your SSH terminal (on the server):**

```bash
docker exec -i authentik-sso-hxogz6-authentik-server-1 ak shell <<'EOF'
from authentik.core.models import User

# Update testadmin
u = User.objects.get(username='testadmin')
u.is_superuser = True
u.is_staff = True
u.is_active = True
u.save()
print(f'✅ {u.username} is now a superuser')

# Also fix admin@bizoholic.net
try:
    admin = User.objects.get(username='admin@bizoholic.net')
    admin.delete()
    print('✅ Deleted old admin@bizoholic.net')
except:
    pass

admin = User.objects.create_user(
    username='admin@bizoholic.net',
    email='admin@bizoholic.net',
    password='Bangalore@123',
    name='Admin User'
)
admin.is_active = True
admin.is_superuser = True
admin.is_staff = True
admin.save()
print(f'✅ Created fresh admin@bizoholic.net with password: Bangalore@123')
EOF
```

### Step 2: Access Admin Interface

1. **Logout** from Authentik (click your username → Logout)
2. **Login again** as `testadmin` / `TestPassword123!`
3. Look in the **top-right corner** for:
   - A button labeled **"Admin Interface"** OR
   - A **gear/settings icon** OR
   - Your username dropdown → **"Admin Interface"**
4. Click it to go to: `https://auth-sso.bizoholic.net/if/admin/`

### Step 3: Create OAuth Provider

Once in Admin Interface:

1. Go to **Applications** → **Providers** (left sidebar)
2. Click **Create** button
3. Select **OAuth2/OpenID Provider**
4. Fill in:
   - **Name**: `BizOSaaS Platform Provider`
   - **Authorization flow**: Select `default-provider-authorization-explicit-consent`
   - **Client type**: `Confidential`
   - **Client ID**: `bizosaas-portal`
   - **Client Secret**: `BizOSaaS2024!AuthentikSecret`
   - **Redirect URIs** (add these one by one):
     ```
     https://admin.bizoholic.net/api/auth/callback/authentik
     https://app.bizoholic.net/api/auth/callback/authentik
     https://directory.bizoholic.net/api/auth/callback/authentik
     ```
   - **Signing Key**: Select the auto-generated certificate
5. Click **Create**

### Step 4: Create Application

1. Go to **Applications** → **Applications** (left sidebar)
2. Click **Create**
3. Fill in:
   - **Name**: `BizOSaaS Platform`
   - **Slug**: `bizosaas-platform` ⚠️ **CRITICAL - must be exact**
   - **Provider**: Select `BizOSaaS Platform Provider` (from Step 3)
   - **Launch URL**: `https://app.bizoholic.net`
4. Click **Create**

### Step 5: Verify

Now when you go to the User Dashboard (`/if/user/#/library`), you should see:
- **BizOSaaS Platform** application card
- Click it to launch `https://app.bizoholic.net`

---

## 🔍 Troubleshooting

**If you still don't see "Admin Interface" button:**
- Clear browser cache and cookies
- Try incognito/private window
- Verify the command in Step 1 ran successfully

**If applications don't appear in User Dashboard:**
- Make sure the Application is not set to "Hide in Library"
- Check that your user has access (no policy restrictions)
