# Quick Fix Commands for Authentication Issues
**Date**: 2026-01-25

---

## 🚀 Quick Commands to Run

### Step 1: Check Current Service Status

```bash
# Check Authentik
curl -I https://auth-sso.bizoholic.net

# Check Lago
curl -I https://billing.bizoholic.net
```

---

## 🔧 Fix Authentik Login

### Option 1: Try the Initial Setup Flow

Instead of the regular login, try the initial setup URL:

**URL**: https://auth-sso.bizoholic.net/if/flow/initial-setup/

This bypasses the regular login and lets you set up the admin account.

### Option 2: Check Bootstrap Password

The bootstrap password should be set in the docker-compose file. Let's verify:

```bash
# View the Authentik environment in Dokploy
# Go to: https://dk.bizoholic.com
# Navigate to: Authentik SSO service → Environment Variables
# Look for: AUTHENTIK_BOOTSTRAP_PASSWORD
```

Expected value: `Bizoholic2025!Admin`

### Option 3: Create Recovery Key

If the above doesn't work, create a recovery key:

```bash
# SSH into server (password: &k3civYG5Q6YPb)
ssh root@194.238.16.237

# Create recovery key for akadmin user
docker exec authentik-server ak create_recovery_key 10 akadmin

# This will output a URL like:
# https://auth-sso.bizoholic.net/if/flow/recovery/?key=XXXXX
# Open that URL in your browser to set a new password
```

---

## 🔧 Fix Lago Login

Lago requires creating an admin user via the Rails console. Here's the exact process:

### Step 1: SSH into Server

```bash
ssh root@194.238.16.237
# Password: &k3civYG5Q6YPb
```

### Step 2: Access Lago Rails Console

```bash
docker exec -it lago-api rails console
```

### Step 3: Create Admin User

Copy and paste this entire block into the Rails console:

```ruby
# Create organization
org = Organization.find_or_create_by!(name: 'Bizoholic')

# Create or update user
user = User.find_or_initialize_by(email: 'admin@bizoholic.net')
user.password = 'Password123!'
user.password_confirmation = 'Password123!'
user.save!

# Create admin membership
membership = Membership.find_or_create_by!(user: user, organization: org) do |m|
  m.role = :admin
end

# Verify creation
puts "\n✅ Admin user created successfully!"
puts "Email: #{user.email}"
puts "Organization: #{org.name}"
puts "Role: #{membership.role}"
puts "\nYou can now login at: https://billing.bizoholic.net"
```

### Step 4: Exit and Test

```bash
exit  # Exit Rails console
exit  # Exit SSH
```

Now try logging in at: https://billing.bizoholic.net
- Email: `admin@bizoholic.net`
- Password: `Password123!`

---

## 📋 Alternative Lago Credentials

If the above doesn't work, try the default Lago credentials:

- Email: `admin@getlago.com`
- Password: `password`

Or create a user with these credentials:

```ruby
# In Rails console
user = User.find_or_initialize_by(email: 'admin@getlago.com')
user.password = 'password'
user.password_confirmation = 'password'
user.save!

org = Organization.find_or_create_by!(name: 'Bizoholic')
Membership.find_or_create_by!(user: user, organization: org, role: :admin)
```

---

## 🔍 Troubleshooting Commands

### Check if Containers are Running

```bash
ssh root@194.238.16.237

# Check Authentik
docker ps | grep authentik

# Check Lago
docker ps | grep lago
```

### View Container Logs

```bash
# Authentik logs
docker logs authentik-server --tail 50

# Lago logs
docker logs lago-api --tail 50
```

### Restart Services

```bash
# Restart Authentik
docker restart authentik-server authentik-worker

# Restart Lago
docker restart lago-api lago-worker lago-front
```

---

## ✅ Expected Credentials After Fix

### Authentik SSO
- **Admin URL**: https://auth-sso.bizoholic.net/if/admin/
- **Initial Setup URL**: https://auth-sso.bizoholic.net/if/flow/initial-setup/
- **Username**: `akadmin`
- **Password**: `Bizoholic2025!Admin`

### Lago Billing
- **URL**: https://billing.bizoholic.net
- **Email**: `admin@bizoholic.net`
- **Password**: `Password123!`

---

## 🎯 Recommended Approach

1. **For Authentik**: Try the initial setup flow first (Option 1)
2. **For Lago**: Run the Rails console commands (Steps 1-4)
3. **If issues persist**: Check the troubleshooting commands
4. **Last resort**: Restart the services

---

## 📞 Quick Reference

**Server SSH**:
- Host: `194.238.16.237`
- User: `root`
- Password: `&k3civYG5Q6YPb`

**Dokploy**:
- URL: https://dk.bizoholic.com
- API Key: `mKgAkCySnrCaAupZYGLiHNNugPRzbsGQZHbcJFMoQSSfdhKUGUPksUuGrWQGWBug`

---

**Last Updated**: 2026-01-25 08:55 UTC
