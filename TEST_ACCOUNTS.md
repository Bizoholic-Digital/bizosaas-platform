# BizOSaaS Platform - Test Accounts

**Last Updated:** December 4, 2024, 9:45 PM IST

---

## 🔐 Test Account Credentials

### Super Admins (Platform Level)
**Full platform access, can manage all tenants and configure AI agents**

| Email | Password | Role | Access Level |
|-------|----------|------|--------------|
| admin@bizoholic.com | AdminDemo2024! | super_admin | ✅ All Features + AI Agents |
| superadmin@bizosaas.com | BizoSaaS2025!Admin | super_admin | ✅ All Features + AI Agents |

**Features:**
- ✅ AI Agents menu visible
- ✅ Can edit system prompts
- ✅ Can add fine-tuning instructions
- ✅ Full BYOK management
- ✅ View agent logs
- ✅ Manage all tenants

---

### Admins (Tenant Level)
**Tenant administration, can manage AI agents but not system prompts**

| Email | Password | Role | Access Level |
|-------|----------|------|--------------|
| admin@test.com | Admin2024!Test | admin | ✅ AI Agents (Limited) |
| administrator@bizosaas.com | Bizoholic2025!Admin | admin | ✅ AI Agents (Limited) |

**Features:**
- ✅ AI Agents menu visible
- ❌ Cannot edit system prompts
- ❌ Cannot add fine-tuning instructions
- ✅ Can configure LLM settings
- ✅ BYOK management
- ✅ Manage tools and services

---

### Managers
**Team management and reporting**

| Email | Password | Role | Access Level |
|-------|----------|------|--------------|
| manager@test.com | Manager2024!Test | manager | ❌ No AI Agents |

**Features:**
- ❌ AI Agents menu hidden
- ✅ Can use AI chat interface
- ✅ Team management
- ✅ View reports

---

### Regular Users
**Standard platform users**

| Email | Password | Role | Access Level |
|-------|----------|------|--------------|
| user@bizosaas.com | Bizoholic2025!User | user | ❌ No AI Agents |
| user@test.com | User2024!Test | user | ❌ No AI Agents |

**Features:**
- ❌ AI Agents menu hidden
- ✅ Can use AI chat interface
- ✅ Basic features

---

### Clients
**External clients with limited access**

| Email | Password | Role | Access Level |
|-------|----------|------|--------------|
| client@bizosaas.com | ClientDemo2024! | client | ❌ No AI Agents |
| client@test.com | Client2024!Test | client | ❌ No AI Agents |

**Features:**
- ❌ AI Agents menu hidden
- ✅ Can use AI chat interface
- ✅ View own data only

---

### Viewers
**Read-only access**

| Email | Password | Role | Access Level |
|-------|----------|------|--------------|
| viewer@test.com | Viewer2024!Test | viewer | ❌ No AI Agents |

**Features:**
- ❌ AI Agents menu hidden
- ✅ Read-only access
- ❌ Cannot modify data

---

## 🎯 AI Agents Menu Visibility

### Who Can See AI Agents Menu?

| Role | Menu Visible | Can Configure | Can Edit Prompts |
|------|-------------|---------------|------------------|
| super_admin | ✅ Yes | ✅ Yes | ✅ Yes |
| admin | ✅ Yes | ✅ Yes | ❌ No |
| manager | ❌ No | ❌ No | ❌ No |
| user | ❌ No | ❌ No | ❌ No |
| client | ❌ No | ❌ No | ❌ No |
| viewer | ❌ No | ❌ No | ❌ No |

---

## 🚀 How to Seed Test Accounts

### Method 1: Run Seed Script

```bash
# Navigate to auth service
cd /home/alagiri/projects/bizosaas-platform/shared/services/auth

# Run seed script
python3 seed_test_users.py
```

### Method 2: Docker Exec

```bash
# If auth service is running in Docker
docker exec -it auth-service python seed_test_users.py
```

---

## 🧪 Testing Different Roles

### Test Super Admin Features
1. Login with: `admin@bizoholic.com` / `AdminDemo2024!`
2. Check sidebar - should see "AI Agents (93)" menu
3. Navigate to AI Agents
4. Click any agent → Configure
5. Should see all 7 tabs including "System Prompt" and "Fine-Tuning"

### Test Admin Features
1. Login with: `admin@test.com` / `Admin2024!Test`
2. Check sidebar - should see "AI Agents (93)" menu
3. Navigate to AI Agents
4. Click any agent → Configure
5. Should see 5 tabs (no "System Prompt" or "Fine-Tuning")

### Test Regular User
1. Login with: `user@test.com` / `User2024!Test`
2. Check sidebar - should NOT see "AI Agents" menu
3. Can still use AI chat at `/chat`
4. Direct navigation to `/ai-agents` should redirect or show access denied

---

## 🔄 Account Management

### Reset Password
```sql
-- Connect to database
psql -U postgres -d bizosaas

-- Reset password for any user
UPDATE users 
SET hashed_password = '$2b$12$...' -- Use bcrypt hash
WHERE email = 'admin@bizoholic.com';
```

### Change User Role
```sql
-- Promote user to admin
UPDATE users 
SET role = 'admin' 
WHERE email = 'user@test.com';

-- Promote to super_admin
UPDATE users 
SET role = 'super_admin', is_superuser = true 
WHERE email = 'admin@test.com';
```

### Verify User Exists
```sql
SELECT id, email, role, is_active, is_verified 
FROM users 
WHERE email = 'admin@bizoholic.com';
```

---

## 📝 Notes

1. **Default Tenant:** All test users belong to "bizosaas-admin" tenant
2. **Email Login:** Platform uses email for authentication, not username
3. **Password Requirements:** 
   - Minimum 8 characters
   - At least one uppercase letter
   - At least one lowercase letter
   - At least one number
   - At least one special character

4. **Session Duration:** 24 hours by default
5. **2FA:** Disabled for all test accounts

---

## 🎨 UI Differences by Role

### Super Admin View
```
Sidebar:
├── Dashboard
├── My Services
├── Campaigns
├── Analytics
├── AI Agents (93) ⭐ VISIBLE
├── Billing
├── Team
├── Support
└── Settings
```

### Admin View
```
Sidebar:
├── Dashboard
├── My Services
├── Campaigns
├── Analytics
├── AI Agents (93) ⭐ VISIBLE
├── Billing
├── Team
├── Support
└── Settings
```

### Regular User View
```
Sidebar:
├── Dashboard
├── My Services
├── Campaigns
├── Analytics
├── Billing        ❌ AI Agents NOT VISIBLE
├── Team
├── Support
└── Settings
```

---

## 🔍 Troubleshooting

### "AI Agents menu not showing"
**Solution:** Check user role in database
```sql
SELECT email, role FROM users WHERE email = 'your@email.com';
```
Role must be 'admin' or 'super_admin'

### "Cannot login"
**Solution:** Verify account is active and verified
```sql
SELECT email, is_active, is_verified FROM users WHERE email = 'your@email.com';
```

### "Wrong password"
**Solution:** Re-seed the account or reset password

---

**For Production:** Remove or disable all test accounts before going live!
