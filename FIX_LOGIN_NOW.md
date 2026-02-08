# Fix Login Credentials - Quick Solution

## Problem
Login with `admin@bizoholic.com` shows "Invalid credentials"

## Solution
Run the seed script to create/update test users including the admin account.

## Steps to Fix

### Open a new terminal and run:

```bash
cd /home/alagiri/projects/bizosaas-platform/shared/services/auth

# Set the database URL
export DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/bizosaas"

# Run the seed script
python3 seed_test_users.py
```

### What this does:
- Creates a default tenant if it doesn't exist
- Creates/updates the following test users:
  - `admin@bizoholic.com` / `AdminDemo2024!` (super_admin)
  - `client@bizosaas.com` / `ClientDemo2024!` (user)
  - `superadmin@bizosaas.com` / `BizoSaaS2025!Admin` (super_admin)
  - `administrator@bizosaas.com` / `Bizoholic2025!Admin` (tenant_admin)
  - `user@bizosaas.com` / `Bizoholic2025!User` (user)

### After running the script:

1. Go to `http://localhost:3003/login`
2. Enter:
   - **Email**: `admin@bizoholic.com`
   - **Password**: `AdminDemo2024!`
3. Click "Sign In"
4. You should be redirected to the dashboard

## Alternative: If Python commands hang

If the Python script doesn't run, you can manually execute SQL:

```bash
# Connect to database
psql -h localhost -U postgres -d bizosaas

# Then run this SQL (replace the hash with a bcrypt hash of AdminDemo2024!)
# You can generate the hash at: https://bcrypt-generator.com/
# Use rounds: 10
# Password: AdminDemo2024!

UPDATE users 
SET hashed_password = '$2b$10$[YOUR_BCRYPT_HASH_HERE]'
WHERE email = 'admin@bizoholic.com';
```

## Verification

After fixing, test the login:
```bash
curl -X POST http://localhost:8008/auth/sso/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@bizoholic.com","password":"AdminDemo2024!","platform":"bizoholic","remember_me":true}'
```

You should get a JSON response with `access_token` and user details (not a 401 error).
