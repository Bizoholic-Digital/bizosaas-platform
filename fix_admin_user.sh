#!/bin/bash
# Fix admin@bizoholic.net account by recreating it

echo "🔧 Fixing admin@bizoholic.net account..."

docker exec -i authentik-sso-hxogz6-authentik-server-1 ak shell <<'EOF'
from authentik.core.models import User

# Delete the corrupted user if it exists
try:
    old_user = User.objects.get(username='admin@bizoholic.net')
    old_user.delete()
    print('✅ Deleted old admin@bizoholic.net user')
except User.DoesNotExist:
    print('ℹ️  User did not exist')

# Create fresh user
u = User.objects.create_user(
    username='admin@bizoholic.net',
    email='admin@bizoholic.net',
    password='Bangalore@123',
    name='Admin User'
)
u.is_active = True
u.is_superuser = True
u.is_staff = True
u.save()

print(f'\n✅ SUCCESS: Created fresh admin@bizoholic.net')
print(f'   Username: {u.username}')
print(f'   Password: Bangalore@123')
print(f'   Active: {u.is_active}')
print(f'   Superuser: {u.is_superuser}')
EOF

echo ""
echo "✅ Done! You can now login with:"
echo "   Username: admin@bizoholic.net"
echo "   Password: Bangalore@123"
