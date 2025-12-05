#!/usr/bin/env python3
"""
Direct Wagtail Admin Creator
Creates admin user by connecting to the container's database directly
"""

import os
import sys
import django
import psycopg2
from psycopg2.extras import RealDictCursor
import requests
import time

def create_superuser_via_container():
    """Create superuser by executing Django commands in the container process"""
    
    print("🔧 Creating Wagtail superuser via container process...")
    
    # Get the Wagtail master process PID
    import subprocess
    result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
    
    wagtail_master_pid = None
    for line in result.stdout.split('\n'):
        if 'gunicorn' in line and 'wagtail_cms.wsgi' in line and '--bind 0.0.0.0:8006' in line:
            # Get the master process (not worker)
            parts = line.split()
            if len(parts) >= 2:
                pid = parts[1]
                # Check if this is the master process by looking at the command
                if '--workers' in line:  # Master process has --workers
                    wagtail_master_pid = pid
                    break
    
    if not wagtail_master_pid:
        print("❌ Could not find Wagtail master process")
        return False
    
    print(f"✅ Found Wagtail master process PID: {wagtail_master_pid}")
    
    # Create the Django shell command
    django_shell_command = """
import os
import django
from django.conf import settings
from django.contrib.auth import get_user_model

# Initialize Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wagtail_cms.settings.development')
django.setup()

User = get_user_model()

print('🔍 Checking existing users...')
existing_users = User.objects.all()
print(f'Found {existing_users.count()} existing users:')
for user in existing_users:
    print(f'  - {user.username} ({user.email}) - Superuser: {user.is_superuser}')

print('\\n🔧 Creating admin superuser...')

# Delete existing admin user if exists
if User.objects.filter(username='admin').exists():
    print('🗑️  Removing existing admin user...')
    User.objects.filter(username='admin').delete()

# Create new superuser
admin_user = User.objects.create_superuser(
    username='admin',
    email='admin@bizosaas.local',
    password='bizosaas123'
)

print('✅ Superuser created successfully!')
print(f'   👤 Username: {admin_user.username}')
print(f'   📧 Email: {admin_user.email}')
print(f'   🔐 Password: bizosaas123')
print(f'   🌐 Admin URL: http://localhost:8006/admin/')
print(f'   ⭐ Is superuser: {admin_user.is_superuser}')
print(f'   🔑 Is staff: {admin_user.is_staff}')

# Verify the user was created
verification_user = User.objects.get(username='admin')
print('\\n🔍 Verification:')
print(f'   User exists: {verification_user is not None}')
print(f'   Can access admin: {verification_user.is_superuser and verification_user.is_staff}')
"""
    
    # Write the command to a temporary file
    temp_script_path = "/tmp/create_wagtail_admin.py"
    with open(temp_script_path, 'w') as f:
        f.write(django_shell_command)
    
    # Execute using nsenter to run in the container's namespace
    try:
        nsenter_cmd = [
            'nsenter', '-t', wagtail_master_pid, '-p', '-m', '-n',
            '/usr/local/bin/python3.11', '-c', django_shell_command
        ]
        
        print("🚀 Executing admin creation command...")
        result = subprocess.run(nsenter_cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Command executed successfully!")
            print("📜 Output:")
            print(result.stdout)
            return True
        else:
            print(f"❌ Command failed with return code {result.returncode}")
            print(f"📜 STDOUT: {result.stdout}")
            print(f"📜 STDERR: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Command timed out")
        return False
    except PermissionError:
        print("❌ Permission denied. Need to run with proper privileges.")
        return False
    except Exception as e:
        print(f"❌ Error executing command: {e}")
        return False

def create_superuser_via_database():
    """Create superuser by directly manipulating the database"""
    
    print("🗄️  Creating Wagtail superuser via direct database access...")
    
    # Database connection parameters (same as container)
    db_params = {
        'host': 'localhost',  # Container uses host.docker.internal, we use localhost
        'port': 5432,
        'database': 'bizosaas',
        'user': 'admin',
        'password': 'securepassword'
    }
    
    try:
        # Connect to database
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        print("✅ Connected to database")
        
        # Check if auth_user table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'auth_user'
            );
        """)
        table_exists = cursor.fetchone()['exists']
        
        if not table_exists:
            print("❌ Django auth_user table doesn't exist. Need to run migrations first.")
            return False
        
        print("✅ Django auth_user table found")
        
        # Check existing users
        cursor.execute("SELECT username, email, is_superuser, is_staff FROM auth_user;")
        existing_users = cursor.fetchall()
        
        print(f"🔍 Found {len(existing_users)} existing users:")
        for user in existing_users:
            print(f"   - {user['username']} ({user['email']}) - Superuser: {user['is_superuser']}")
        
        # Delete existing admin user
        cursor.execute("DELETE FROM auth_user WHERE username = 'admin';")
        deleted_count = cursor.rowcount
        if deleted_count > 0:
            print(f"🗑️  Removed {deleted_count} existing admin user(s)")
        
        # Create new admin user with hashed password
        from django.contrib.auth.hashers import make_password
        
        # We need to set up Django to use the password hasher
        import django
        from django.conf import settings
        
        if not settings.configured:
            settings.configure(
                SECRET_KEY='temp-key-for-password-hashing',
                USE_TZ=True,
                PASSWORD_HASHERS=[
                    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
                ]
            )
            django.setup()
        
        hashed_password = make_password('bizosaas123')
        
        # Insert new admin user
        cursor.execute("""
            INSERT INTO auth_user (
                username, email, password, is_superuser, is_staff, 
                is_active, date_joined, first_name, last_name
            ) VALUES (
                'admin', 'admin@bizosaas.local', %s, true, true, 
                true, NOW(), '', ''
            );
        """, (hashed_password,))
        
        # Commit changes
        conn.commit()
        
        print("✅ Admin user created successfully!")
        print("   👤 Username: admin")
        print("   📧 Email: admin@bizosaas.local")
        print("   🔐 Password: bizosaas123")
        print("   🌐 Admin URL: http://localhost:8006/admin/")
        
        # Verify the user was created
        cursor.execute("SELECT username, email, is_superuser, is_staff FROM auth_user WHERE username = 'admin';")
        new_user = cursor.fetchone()
        
        if new_user:
            print("🔍 Verification:")
            print(f"   User exists: ✅")
            print(f"   Is superuser: {'✅' if new_user['is_superuser'] else '❌'}")
            print(f"   Is staff: {'✅' if new_user['is_staff'] else '❌'}")
            return True
        else:
            print("❌ Failed to verify user creation")
            return False
            
    except psycopg2.Error as e:
        print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def test_admin_login():
    """Test the created admin credentials"""
    
    print("🧪 Testing admin login...")
    
    session = requests.Session()
    login_url = "http://localhost:8006/admin/login/"
    
    try:
        # Get login page
        response = session.get(login_url, timeout=10)
        response.raise_for_status()
        
        # Extract CSRF token
        import re
        csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
        if not csrf_match:
            print("❌ Could not find CSRF token")
            return False
        
        csrf_token = csrf_match.group(1)
        
        # Attempt login
        login_data = {
            'username': 'admin',
            'password': 'bizosaas123',
            'csrfmiddlewaretoken': csrf_token,
        }
        
        headers = {
            'Referer': login_url,
            'X-CSRFToken': csrf_token,
        }
        
        response = session.post(login_url, data=login_data, headers=headers, timeout=10)
        
        # Check if login was successful
        if '/admin/' in response.url and response.status_code == 200 and 'login' not in response.url:
            print("✅ Login test successful!")
            print("🎉 Admin credentials are working!")
            return True
        else:
            print("❌ Login test failed")
            return False
            
    except requests.RequestException as e:
        print(f"❌ Login test error: {e}")
        return False

def main():
    print("🔧 Wagtail Admin User Creator")
    print("=" * 50)
    
    # Try container method first
    print("🚀 Method 1: Creating via container process...")
    success = create_superuser_via_container()
    
    if not success:
        print("\n🚀 Method 2: Creating via direct database access...")
        success = create_superuser_via_database()
    
    if success:
        print("\n🧪 Testing login credentials...")
        time.sleep(2)  # Give the system time to process
        login_success = test_admin_login()
        
        if login_success:
            print("\n🎉 SUCCESS!")
            print("=" * 50)
            print("✅ Admin user created and verified!")
            print("🔑 Login Credentials:")
            print("   Username: admin")
            print("   Password: bizosaas123")
            print("   URL: http://localhost:8006/admin/")
            return True
        else:
            print("\n⚠️  User created but login test failed")
            print("   Please try logging in manually")
            return False
    else:
        print("\n❌ Failed to create admin user")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)