#!/bin/bash

echo "🔍 Finding Wagtail container process..."

# Get the Wagtail process PID
WAGTAIL_PID=$(ps aux | grep "gunicorn.*wagtail_cms" | grep -v grep | head -1 | awk '{print $2}')

if [ -z "$WAGTAIL_PID" ]; then
    echo "❌ Wagtail process not found"
    exit 1
fi

echo "✅ Found Wagtail process PID: $WAGTAIL_PID"

echo "🔧 Creating superuser in Wagtail container namespace..."

# Try to enter the container namespace and create superuser
if nsenter -t $WAGTAIL_PID -p -m -n /usr/local/bin/python3.11 /app/manage.py shell -c "
import os
from django.contrib.auth import get_user_model

User = get_user_model()

print('Current users in database:')
for user in User.objects.all():
    print(f'  - {user.username} ({user.email}) - Superuser: {user.is_superuser}')

print('\\nCreating superuser...')

# Delete existing admin user if exists
if User.objects.filter(username='admin').exists():
    print('Removing existing admin user...')
    User.objects.filter(username='admin').delete()

# Create new superuser
user = User.objects.create_superuser(
    username='admin',
    email='admin@bizosaas.local',  
    password='bizosaas123'
)

print(f'✅ Superuser created: {user.username}')
print(f'   📧 Email: {user.email}')
print(f'   🔑 Password: bizosaas123')
print(f'   🌐 Admin URL: http://localhost:8006/admin/')
"; then
    echo "✅ Superuser creation completed!"
else
    echo "❌ Failed to execute in container namespace"
    echo "🔧 Trying alternative approach..."
    
    # Try using the manage.py from the host with container environment
    export DJANGO_SETTINGS_MODULE=wagtail_cms.settings.development
    export POSTGRES_HOST=localhost
    export POSTGRES_USER=admin
    export POSTGRES_PASSWORD=securepassword
    export POSTGRES_DB=bizosaas
    export SECRET_KEY=wagtail-secret-key-for-development-only
    export DEBUG=true
    
    cd /home/alagiri/projects/bizoholic/bizosaas/services/wagtail-cms
    
    echo "🔧 Attempting to create superuser with host environment..."
    echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').delete(); user = User.objects.create_superuser('admin', 'admin@bizosaas.local', 'bizosaas123'); print(f'Created: {user.username}')" | python3 manage.py shell
fi