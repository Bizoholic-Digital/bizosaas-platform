# Fix Authentik User Login - Debugging
**Date**: 2026-01-25

If the main admin user is stuck, let's create a **Test Admin** to verify the system works.

## 🛠️ Instructions

### 1. Create Test User

Copy and paste this into your SSH terminal:

```bash
docker exec -i authentik-sso-hxogz6-authentik-server-1 ak shell <<EOF
from authentik.core.models import User
try:
    u, created = User.objects.get_or_create(username='testadmin', defaults={'email': 'testadmin@bizoholic.net', 'name': 'Test Admin'})
    u.set_password('TestPassword123!')
    u.is_active = True
    u.is_superuser = True
    u.is_staff = True
    u.save()
    print(f'\n✅ TEST USER READY: {u.username}')
    print('✅ Password: TestPassword123!')
except Exception as e:
    print(f'\n❌ Error: {e}')
EOF
```

### 2. Try Login with Test User
Go to: https://auth-sso.bizoholic.net
*   **Username**: `testadmin`
*   **Password**: `TestPassword123!`

---

**If this works:** The issue is specific to the `admin@bizoholic.net` account.
**If this fails:** There is a deeper system issue.
