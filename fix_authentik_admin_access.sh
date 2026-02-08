#!/bin/bash
# Fix Authentik Admin Access - Add to authentik Admins group

echo "🔧 Fixing admin access for testadmin and admin@bizoholic.net..."

cat > /tmp/fix_admin_access.py <<'PYTHON'
from authentik.core.models import User, Group

# Get or create the authentik Admins group
admin_group, created = Group.objects.get_or_create(
    name='authentik Admins',
    defaults={'is_superuser': True}
)
admin_group.is_superuser = True
admin_group.save()

if created:
    print(f'✅ Created "authentik Admins" group')
else:
    print(f'✅ Found "authentik Admins" group')

# Fix testadmin
try:
    testadmin = User.objects.get(username='testadmin')
    testadmin.is_superuser = True
    testadmin.is_staff = True
    testadmin.is_active = True
    testadmin.save()
    testadmin.ak_groups.add(admin_group)
    print(f'✅ testadmin: superuser={testadmin.is_superuser}, in group={admin_group.name}')
except Exception as e:
    print(f'❌ testadmin error: {e}')

# Fix admin@bizoholic.net
try:
    admin_user = User.objects.get(username='admin@bizoholic.net')
    admin_user.is_superuser = True
    admin_user.is_staff = True
    admin_user.is_active = True
    admin_user.save()
    admin_user.ak_groups.add(admin_group)
    print(f'✅ admin@bizoholic.net: superuser={admin_user.is_superuser}, in group={admin_group.name}')
except Exception as e:
    print(f'❌ admin@bizoholic.net error: {e}')

print('\n✅ Done! Now LOGOUT completely and login again.')
PYTHON

docker exec -i authentik-sso-hxogz6-authentik-server-1 ak shell < /tmp/fix_admin_access.py
rm /tmp/fix_admin_access.py

echo ""
echo "🎯 IMPORTANT: You MUST do these steps:"
echo "1. LOGOUT from Authentik completely"
echo "2. Close all browser tabs for auth-sso.bizoholic.net"
echo "3. Clear cookies for auth-sso.bizoholic.net (or use incognito)"
echo "4. Login again"
echo "5. Try accessing /if/admin/"
