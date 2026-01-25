#!/bin/bash

# Authentik User Reset Script
# Usage: ./reset_authentik_user.sh <ssh_password>

echo "🔑 Resetting Authentik User..."

# SSH Configuration
HOST="root@194.238.16.237"
CONTAINER="authentik-sso-hxogz6-authentik-server-1"

# Command to execute in container
CMD="
from authentik.core.models import User
try:
    u, created = User.objects.get_or_create(username='admin@bizoholic.net', defaults={'email': 'admin@bizoholic.net', 'name': 'Admin User'})
    u.set_password('Bangalore@123')
    u.save()
    if created:
        print('✅ User Created: admin@bizoholic.net')
    else:
        print('✅ Password Reset: admin@bizoholic.net')
except Exception as e:
    print(f'❌ Error: {e}')
"

echo "Connecting to $HOST..."
ssh -o StrictHostKeyChecking=no $HOST "docker exec $CONTAINER ak shell_plus -c \"$CMD\""

echo "Done."
