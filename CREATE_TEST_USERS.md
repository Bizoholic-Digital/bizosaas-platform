# Create Test User Accounts - Quick Guide

## 🎯 Problem
The test credentials are not working because the users don't exist in the database yet.

## ✅ Solution
Run the seed script to create all test users.

## 🚀 Quick Fix (Run This Now)

```bash
./scripts/seed-users.sh
```

This will create all 5 test accounts with the correct passwords.

## 📝 Test Accounts That Will Be Created

| Role | Email | Password |
|------|-------|----------|
| **Admin** | admin@bizoholic.com | AdminDemo2024! |
| **Client** | client@bizosaas.com | ClientDemo2024! |
| **Super Admin** | superadmin@bizosaas.com | BizoSaaS2025!Admin |
| **Tenant Admin** | administrator@bizosaas.com | Bizoholic2025!Admin |
| **User** | user@bizosaas.com | Bizoholic2025!User |

## 🧪 After Running the Script

### Test Login:
1. Go to `http://localhost:3003/login`
2. Try any of the credentials above
3. Should successfully login and redirect to dashboard

### Verify in Database (Optional):
```bash
docker exec -it bizosaas-postgres-unified psql -U postgres -d bizosaas -c "SELECT email, role FROM users;"
```

## 🔧 Manual Method (If Script Fails)

If the script doesn't work, run manually:

```bash
cd shared/services/auth
export DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/bizosaas"
python3 seed_test_users.py
```

## ⚠️ Troubleshooting

### Issue 1: "Database connection error"
**Solution**: Make sure Postgres is running
```bash
docker ps | grep postgres
# If not running:
docker-compose -f shared/infrastructure/docker-compose.infrastructure.yml up -d postgres
```

### Issue 2: "Module not found"
**Solution**: Install dependencies
```bash
cd shared/services/auth
pip install -r requirements.txt
```

### Issue 3: "Users already exist"
**Solution**: The script will update existing users with new passwords, so this is fine.

## 📋 What the Script Does

1. Creates a default tenant (if doesn't exist)
2. Creates 5 test users with proper password hashing
3. Assigns correct roles to each user
4. Sets up allowed platforms for each user

## ✅ Verification Steps

After running the script:

1. **Test Admin Login**:
   ```
   Email: admin@bizoholic.com
   Password: AdminDemo2024!
   ```

2. **Test Client Login**:
   ```
   Email: client@bizosaas.com
   Password: ClientDemo2024!
   ```

3. **Check Dashboard Access**:
   - Should redirect to `/dashboard` after login
   - Should see role-appropriate features

## 🎯 Expected Output

When you run `./scripts/seed-users.sh`, you should see:

```
🌱 Seeding Test Users
====================

Creating test users with the following credentials:

1. Admin:        admin@bizoholic.com / AdminDemo2024!
2. Client:       client@bizosaas.com / ClientDemo2024!
3. Super Admin:  superadmin@bizosaas.com / BizoSaaS2025!Admin
4. Tenant Admin: administrator@bizosaas.com / Bizoholic2025!Admin
5. User:         user@bizosaas.com / Bizoholic2025!User

Running seed script...

✅ Created tenant: [UUID]
✅ Created user: admin@bizoholic.com
✅ Created user: client@bizosaas.com
✅ Created user: superadmin@bizosaas.com
✅ Created user: administrator@bizosaas.com
✅ Created user: user@bizosaas.com

✅ Test users created successfully!

You can now login at http://localhost:3003/login with any of the above credentials
```

## 🔐 Password Security

All passwords are hashed using bcrypt before being stored in the database. The seed script uses the same `PasswordHelper` class that the Auth Service uses, ensuring compatibility.

## 🎉 Next Steps

1. Run the seed script: `./scripts/seed-users.sh`
2. Wait for success message
3. Go to `http://localhost:3003/login`
4. Login with any test account
5. Explore the dashboard!

---

**Need Help?** If the script fails, check:
- Is Postgres running? (`docker ps | grep postgres`)
- Is the database accessible? (`docker exec bizosaas-postgres-unified pg_isready`)
- Are there any error messages in the output?
