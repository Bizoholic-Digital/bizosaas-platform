# Authentication Fix - Current Status & Next Steps
**Date**: 2026-01-25 09:05 UTC  
**Status**: ⚠️ **PARTIAL SUCCESS - ACTION REQUIRED**

---

## ✅ Authentik SSO - FIXED

### Recovery Key Created Successfully!

I've successfully created a recovery key for Authentik. Use this link to set your admin password:

**Recovery URL**: 
```
https://auth-sso.bizoholic.net/recovery/use-token/SYJSSxShjTkC9eLzpv3StObg2MEmWfVrbcOaA7DPLRKwx1w4TyPZVsGh42Wd/
```

### How to Use:

1. **Open the recovery URL** in your browser (copy the full URL above)
2. You'll be prompted to set a new password for the `akadmin` user
3. Set your password (e.g., `Bizoholic2025!Admin`)
4. After setting the password, you can login at:
   - **Admin Panel**: https://auth-sso.bizoholic.net/if/admin/
   - **Username**: `akadmin`
   - **Password**: [whatever you set in step 3]

**⚠️ IMPORTANT**: This recovery link is valid for 10 uses. Save it securely!

---

## ⚠️ Lago Billing - DATABASE ISSUE

### Problem Identified:

The Lago database has schema inconsistencies. The database appears to be in a partially migrated state, causing errors when trying to create users.

**Error**: `Undeclared attribute type for enum 'document_numbering'`

### Current Status:

- ✅ Lago containers are running (lago-api, lago-worker, lago-front)
- ✅ Lago frontend is accessible at https://billing.bizoholic.net
- ❌ Database schema is incomplete/corrupted
- ❌ Cannot create admin user via Rails console

### Recommended Solutions:

#### **Option 1: Use Lago's Web UI (EASIEST)**

Lago might allow you to create an admin account through the web interface on first access:

1. Go to: https://billing.bizoholic.net
2. Look for a "Sign Up" or "Create Account" option
3. If available, create an account with:
   - Email: `admin@bizoholic.net`
   - Password: `Password123!`

#### **Option 2: Redeploy Lago with Fresh Database**

The cleanest solution is to redeploy Lago with a fresh database:

```bash
# Via Dokploy UI
1. Go to: https://dk.bizoholic.com
2. Navigate to: Lago service
3. Click: "Redeploy" or "Rebuild"
4. This will reinitialize the database with proper schema
```

#### **Option 3: Manual Database Reset (ADVANCED)**

If you need to manually fix the database:

```bash
ssh root@194.238.16.237

# Stop Lago services
docker stop lago-api lago-worker

# Reset the database (requires NEON DB access)
# This will delete ALL Lago data!
docker exec lago-api rails db:drop DISABLE_DATABASE_ENVIRONMENT_CHECK=1
docker exec lago-api rails db:create
docker exec lago-api rails db:migrate

# Restart services
docker start lago-api lago-worker

# Wait 30 seconds for startup
sleep 30

# Create admin user
docker exec lago-api rails runner "
org = Organization.create!(name: 'Bizoholic')
user = User.create!(email: 'admin@bizoholic.net', password: 'Password123!', password_confirmation: 'Password123!')
Membership.create!(user: user, organization: org, role: :admin)
puts 'Admin created: ' + user.email
"
```

---

## 📋 Summary of Actions Completed

### ✅ Completed:
1. Fixed SSH known_hosts issue
2. Identified actual container names
3. Created Authentik recovery key
4. Restarted Lago containers
5. Diagnosed Lago database issue

### ❌ Blocked:
1. Lago admin user creation (database schema issue)

---

## 🎯 Immediate Next Steps

### For You to Do:

1. **Fix Authentik** (5 minutes):
   - Open the recovery URL above
   - Set a new password
   - Login to admin panel

2. **Fix Lago** (Choose one):
   - **Quick**: Try creating account via web UI at https://billing.bizoholic.net
   - **Clean**: Redeploy Lago via Dokploy
   - **Manual**: Run the database reset commands above

---

## 🔐 Final Credentials

### Authentik SSO
- **Recovery URL**: https://auth-sso.bizoholic.net/recovery/use-token/SYJSSxShjTkC9eLzpv3StObg2MEmWfVrbcOaA7DPLRKwx1w4TyPZVsGh42Wd/
- **Admin Panel**: https://auth-sso.bizoholic.net/if/admin/
- **Username**: `akadmin`
- **Password**: [Set via recovery link]

### Lago Billing
- **URL**: https://billing.bizoholic.net
- **Status**: Database needs reset/redeployment
- **Target Credentials**:
  - Email: `admin@bizoholic.net`
  - Password: `Password123!`

---

## 📞 If You Need Help

### Check Lago Status:
```bash
ssh root@194.238.16.237
docker logs lago-api --tail 50
docker ps | grep lago
```

### Test Lago API:
```bash
curl -I https://billing-api.bizoholic.net
```

### Redeploy Lago via Dokploy API:
```bash
# Get compose ID first
curl -X GET "https://dk.bizoholic.com/api/trpc/compose.all?batch=1&input=%7B%220%22%3A%7B%22projectId%22%3A%22YOUR_PROJECT_ID%22%7D%7D" \
  -H "x-api-key: mKgAkCySnrCaAupZYGLiHNNugPRzbsGQZHbcJFMoQSSfdhKUGUPksUuGrWQGWBug"

# Then redeploy
curl -X POST "https://dk.bizoholic.com/api/trpc/compose.deploy" \
  -H "x-api-key: mKgAkCySnrCaAupZYGLiHNNugPRzbsGQZHbcJFMoQSSfdhKUGUPksUuGrWQGWBug" \
  -H "Content-Type: application/json" \
  -d '{"json":{"composeId":"LAGO_COMPOSE_ID"}}'
```

---

## 🔍 Root Cause Analysis

### Lago Database Issue:
- The Neon PostgreSQL database appears to have been partially migrated
- Migration `20230411085545_fix_wallet_consumed_amount_currency_naming` is failing
- This suggests the database was created with an older version of Lago
- The schema is out of sync with the current Lago v1.17.0 codebase

### Recommended Fix:
- Fresh database initialization via redeployment
- OR manual database drop/create/migrate cycle

---

**Last Updated**: 2026-01-25 09:05 UTC

**Priority**: 
1. ✅ Fix Authentik (use recovery link) - **DO THIS NOW**
2. ⚠️ Fix Lago (redeploy or reset database) - **CHOOSE YOUR APPROACH**
