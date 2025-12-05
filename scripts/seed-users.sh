#!/bin/bash
# Seed Test Users - Creates all test accounts in the database

echo "🌱 Seeding Test Users"
echo "===================="

cd shared/services/auth

# Set database connection
export DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/bizosaas"

echo ""
echo "Creating test users with the following credentials:"
echo ""
echo "1. Admin:        admin@bizoholic.com / AdminDemo2024!"
echo "2. Client:       client@bizosaas.com / ClientDemo2024!"
echo "3. Super Admin:  superadmin@bizosaas.com / BizoSaaS2025!Admin"
echo "4. Tenant Admin: administrator@bizosaas.com / Bizoholic2025!Admin"
echo "5. User:         user@bizosaas.com / Bizoholic2025!User"
echo ""
echo "Running seed script..."
echo ""

python3 seed_test_users.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Test users created successfully!"
    echo ""
    echo "You can now login at http://localhost:3003/login with any of the above credentials"
else
    echo ""
    echo "❌ Failed to create test users"
    echo "Check the error message above"
fi
