# Authentication Credentials Fix - Troubleshooting Guide
**Date**: 2026-01-25  
**Issue**: Login credentials not working for Authentik and Lago

---

## 🔍 Problem Summary

1. **Authentik SSO** (`https://auth-sso.bizoholic.net`): Login page accessible but credentials not working
2. **Lago Billing** (`https://billing.bizoholic.net`): Login page accessible but credentials not working

---

## ✅ Solution Steps

### Quick Fix (Automated)

Run the automated fix script:

```bash
cd /home/alagiri/projects/bizosaas-platform
./fix_auth_credentials.sh
```

This script will:
1. Check service status
2. Reset Authentik admin password
3. Create Lago admin user
4. Display final credentials

---

### Manual Fix (If Automated Script Fails)

#### **Fix 1: Authentik Admin Access**

**Option A: Use Bootstrap Password**

The bootstrap password is set in the docker-compose file. Check if it's configured:

```bash
ssh root@194.238.16.237 "docker exec authentik-server env | grep AUTHENTIK_BOOTSTRAP_PASSWORD"
```

Expected output: `AUTHENTIK_BOOTSTRAP_PASSWORD=Bizoholic2025!Admin`

**Login with:**
- URL: https://auth-sso.bizoholic.net/if/flow/initial-setup/
- Username: `akadmin`
- Password: `Bizoholic2025!Admin`

**Option B: Reset Admin Password**

If the bootstrap password doesn't work, reset it manually:

```bash
# SSH into the server
ssh root@194.238.16.237

# Access Authentik container
docker exec -it authentik-server bash

# Run password reset command
ak create_recovery_key 10 akadmin

# This will output a recovery link - use it to set a new password
```

**Option C: Check Environment Variables**

Verify the docker-compose configuration has the bootstrap password:

```bash
ssh root@194.238.16.237 "docker inspect authentik-server | grep -A 5 AUTHENTIK_BOOTSTRAP"
```

If missing, update the docker-compose.authentik.yml and redeploy.

---

#### **Fix 2: Lago Admin Access**

Lago requires creating an admin user via Rails console.

**Step 1: Access Lago API Container**

```bash
ssh root@194.238.16.237
docker exec -it lago-api bash
```

**Step 2: Open Rails Console**

```bash
rails console
```

**Step 3: Create Admin User**

```ruby
# Create organization
org = Organization.find_or_create_by!(name: 'Bizoholic')

# Create user
user = User.find_or_initialize_by(email: 'admin@bizoholic.net')
user.password = 'Password123!'
user.password_confirmation = 'Password123!'
user.save!

# Create membership with admin role
membership = Membership.find_or_create_by!(user: user, organization: org) do |m|
  m.role = :admin
end

# Verify
puts "User created: #{user.email}"
puts "Organization: #{org.name}"
puts "Role: #{membership.role}"
```

**Step 4: Exit and Test**

```bash
exit  # Exit Rails console
exit  # Exit container
```

Now try logging in at https://billing.bizoholic.net with:
- Email: `admin@bizoholic.net`
- Password: `Password123!`

---

## 🔐 Final Credentials

### Authentik SSO
- **URL**: https://auth-sso.bizoholic.net/if/admin/
- **Username**: `akadmin`
- **Password**: `Bizoholic2025!Admin`
- **Alternative URL**: https://auth-sso.bizoholic.net/if/flow/initial-setup/

### Lago Billing
- **URL**: https://billing.bizoholic.net
- **Email**: `admin@bizoholic.net`
- **Password**: `Password123!`

---

## 🐛 Common Issues & Solutions

### Issue 1: "Invalid credentials" for Authentik

**Possible Causes:**
1. Bootstrap password not set in environment
2. Initial setup not completed
3. User doesn't exist

**Solutions:**
1. Check environment variables (see Option C above)
2. Use the initial setup flow: https://auth-sso.bizoholic.net/if/flow/initial-setup/
3. Create recovery key (see Option B above)

### Issue 2: "Invalid credentials" for Lago

**Possible Causes:**
1. Admin user not created
2. Database not initialized
3. Password mismatch

**Solutions:**
1. Create user via Rails console (see Fix 2 above)
2. Check database connection:
   ```bash
   docker exec lago-api rails db:migrate:status
   ```
3. Reset password via Rails console

### Issue 3: Authentik shows "Connection Refused"

**Cause:** Service not running

**Solution:**
```bash
ssh root@194.238.16.237
docker ps | grep authentik
docker logs authentik-server --tail 50
```

If not running, restart:
```bash
docker restart authentik-server authentik-worker
```

### Issue 4: Lago shows blank page or errors

**Cause:** API not responding or database issues

**Solution:**
```bash
ssh root@194.238.16.237
docker logs lago-api --tail 50
docker logs lago-worker --tail 50
```

Check for database connection errors. If found:
```bash
docker exec lago-api rails db:migrate
docker restart lago-api lago-worker
```

---

## 📋 Verification Checklist

After applying fixes, verify:

- [ ] Authentik login page loads: https://auth-sso.bizoholic.net
- [ ] Can login to Authentik admin: https://auth-sso.bizoholic.net/if/admin/
- [ ] Lago login page loads: https://billing.bizoholic.net
- [ ] Can login to Lago with admin credentials
- [ ] Authentik shows "BizOSaaS Platform" application (if configured)
- [ ] No errors in browser console
- [ ] No errors in container logs

---

## 🔧 Additional Commands

### Check Service Health

```bash
# Authentik
ssh root@194.238.16.237 "docker exec authentik-server ak healthcheck"

# Lago
ssh root@194.238.16.237 "docker exec lago-api rails runner 'puts User.count'"
```

### View Logs

```bash
# Authentik logs
ssh root@194.238.16.237 "docker logs authentik-server --tail 100 -f"

# Lago logs
ssh root@194.238.16.237 "docker logs lago-api --tail 100 -f"
```

### Restart Services

```bash
# Restart Authentik
ssh root@194.238.16.237 "docker restart authentik-server authentik-worker"

# Restart Lago
ssh root@194.238.16.237 "docker restart lago-api lago-worker lago-front"
```

---

## 📞 Next Steps After Login

### For Authentik:
1. Configure OAuth2/OIDC Provider
2. Create BizOSaaS Platform application
3. Add redirect URIs for portals
4. Create test users

### For Lago:
1. Configure billing plans
2. Set up payment integrations
3. Create customers
4. Configure webhooks

---

## 📝 Notes

- **Authentik** uses environment variable `AUTHENTIK_BOOTSTRAP_PASSWORD` for initial admin setup
- **Lago** requires manual user creation via Rails console
- Both services are deployed via Dokploy on KVM8 (194.238.16.237)
- Credentials are documented in `/home/alagiri/projects/bizosaas-platform/credentials.md`

---

**Last Updated**: 2026-01-25 08:52 UTC
