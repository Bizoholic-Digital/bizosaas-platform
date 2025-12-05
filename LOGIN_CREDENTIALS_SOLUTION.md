# Login Credentials Issue - Solution Guide

## Current Status
✅ **Login Page**: Working correctly at `http://localhost:3003/login`
✅ **Auth Service**: Running and reachable on port 8008
❌ **Credentials**: Password verification failing

## The Issue
You're seeing "Invalid credentials" when trying to log in with `admin@bizoholic.com`.

## Solution Options

### Option 1: Create/Reset Admin User via Auth Service API

Since the Auth Service is running, you can use its API endpoints to create or reset the admin user.

**Using the browser or Postman:**

1. **Check if user exists:**
   ```
   GET http://localhost:8008/users?email=admin@bizoholic.com
   ```

2. **Create admin user (if doesn't exist):**
   ```
   POST http://localhost:8008/auth/register
   Content-Type: application/json
   
   {
     "email": "admin@bizoholic.com",
     "password": "AdminDemo2024!",
     "first_name": "Admin",
     "last_name": "User",
     "role": "super_admin",
     "platform": "bizoholic"
   }
   ```

### Option 2: Direct Database Access

If you have access to the database directly:

1. **Connect to PostgreSQL:**
   ```bash
   psql -h localhost -U postgres -d bizosaas
   ```

2. **Check if user exists:**
   ```sql
   SELECT id, email, role, is_active FROM users WHERE email='admin@bizoholic.com';
   ```

3. **If user doesn't exist, you need to create one using the Auth Service API (Option 1)**

4. **If user exists but password is wrong, use the reset script:**
   ```bash
   cd /home/alagiri/projects/bizosaas-platform/shared/services/auth
   export DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/bizosaas"
   python3 reset_password.py
   ```

### Option 3: Use Alternative Test Credentials

Try logging in with the client demo account instead:
- **Email**: `client@bizosaas.com`
- **Password**: `ClientDemo2024!`

If this works, it means the Auth Service is functioning correctly, and we just need to fix the admin account.

## Quick Test

Try this in your browser's developer console (F12) while on the login page:

```javascript
fetch('http://localhost:8008/health')
  .then(r => r.json())
  .then(d => console.log('Auth Service:', d))
  .catch(e => console.error('Auth Service Error:', e));
```

This will confirm the Auth Service is reachable from the browser.

## Next Steps

1. **Try Option 3 first** (client credentials) to verify the auth flow works
2. **If that works**, use Option 1 to create/reset the admin user
3. **If nothing works**, we may need to check the Auth Service logs for specific errors

## Files Created

I've created a password reset script at:
`/home/alagiri/projects/bizosaas-platform/shared/services/auth/reset_password.py`

This script will reset the password for `admin@bizoholic.com` to `AdminDemo2024!` when run.

## Important Notes

- The Auth Service is using `fastapi-users` with bcrypt password hashing
- Passwords must be hashed before storing in the database
- The demo credentials shown on the login page are: `admin@bizoholic.com / AdminDemo2024!`
