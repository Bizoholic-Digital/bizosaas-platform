#!/usr/bin/env python3
"""
Raw PostgreSQL approach to create Wagtail superuser
This bypasses Django and directly manipulates the database
"""

import hashlib
import psycopg2
from psycopg2.extras import RealDictCursor
import json
import sys
from datetime import datetime

def get_password_hash(password):
    """Create Django-compatible password hash using PBKDF2"""
    import hashlib
    import base64
    import os
    
    # Django's default password hasher: PBKDF2PasswordHasher
    algorithm = 'pbkdf2_sha256'
    iterations = 390000  # Django 4.x default
    salt = base64.b64encode(os.urandom(12)).decode('ascii')
    
    hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), iterations)
    b64_hash = base64.b64encode(hash).decode('ascii').strip()
    
    return f"{algorithm}${iterations}${salt}${b64_hash}"

def test_database_connections():
    """Test different database connection configurations"""
    
    # Connection configurations to try
    configs = [
        {
            'name': 'Docker internal (host.docker.internal)',
            'host': 'host.docker.internal',
            'port': 5432,
            'user': 'admin',
            'password': 'securepassword',
            'database': 'bizosaas'
        },
        {
            'name': 'Localhost direct',
            'host': 'localhost',
            'port': 5432,
            'user': 'admin', 
            'password': 'securepassword',
            'database': 'bizosaas'
        },
        {
            'name': 'Docker internal (postgres user)',
            'host': 'host.docker.internal',
            'port': 5432,
            'user': 'postgres',
            'password': 'securepassword',
            'database': 'bizosaas'
        },
        {
            'name': 'Shared dev database',
            'host': 'localhost',
            'port': 5432,
            'user': 'postgres',
            'password': 'postgres',
            'database': 'bizosaas'
        }
    ]
    
    working_config = None
    
    print("🔍 Testing database connections...")
    
    for config in configs:
        print(f"  Testing: {config['name']}")
        try:
            conn = psycopg2.connect(
                host=config['host'],
                port=config['port'],
                user=config['user'],
                password=config['password'],
                database=config['database'],
                connect_timeout=5
            )
            
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"    ✅ Connected: {version[:50]}...")
            
            cursor.close()
            conn.close()
            
            working_config = config
            break
            
        except Exception as e:
            print(f"    ❌ Failed: {str(e)}")
            continue
    
    return working_config

def create_wagtail_superuser(config, username='admin', email='admin@bizosaas.local', password='bizosaas123'):
    """Create superuser directly in PostgreSQL database"""
    
    try:
        print(f"\n🔧 Creating superuser using {config['name']}...")
        
        conn = psycopg2.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database=config['database'],
            cursor_factory=RealDictCursor
        )
        
        cursor = conn.cursor()
        
        # Check if auth_user table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'auth_user'
            );
        """)
        
        if not cursor.fetchone()['exists']:
            print("❌ auth_user table doesn't exist. Run Django migrations first.")
            return False
        
        # Check existing users
        cursor.execute("SELECT id, username, email, is_superuser, is_active FROM auth_user;")
        existing_users = cursor.fetchall()
        
        print(f"📋 Found {len(existing_users)} existing users:")
        for user in existing_users:
            print(f"  - {user['username']} ({user['email']}) - Superuser: {user['is_superuser']}")
        
        # Delete existing admin user if exists
        cursor.execute("DELETE FROM auth_user WHERE username = %s;", (username,))
        deleted_count = cursor.rowcount
        if deleted_count > 0:
            print(f"🗑️  Deleted {deleted_count} existing user(s) with username '{username}'")
        
        # Generate password hash
        password_hash = get_password_hash(password)
        
        # Create new superuser
        cursor.execute("""
            INSERT INTO auth_user (
                password, last_login, is_superuser, username, first_name, 
                last_name, email, is_staff, is_active, date_joined
            ) VALUES (
                %s, NULL, TRUE, %s, '', '', %s, TRUE, TRUE, %s
            ) RETURNING id;
        """, (password_hash, username, email, datetime.now()))
        
        user_id = cursor.fetchone()['id']
        
        # Commit changes
        conn.commit()
        
        print(f"✅ Superuser created successfully!")
        print(f"   👤 User ID: {user_id}")
        print(f"   📧 Username: {username}")
        print(f"   📧 Email: {email}")
        print(f"   🔑 Password: {password}")
        print(f"   🌐 Admin URL: http://localhost:8006/admin/")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating superuser: {e}")
        return False

def verify_login_via_http(username, password):
    """Verify login works via HTTP"""
    print(f"\n🧪 Verifying login credentials...")
    
    try:
        import requests
        import re
        
        session = requests.Session()
        login_url = 'http://localhost:8006/admin/login/'
        
        # Get login page
        response = session.get(login_url, timeout=10)
        response.raise_for_status()
        
        # Extract CSRF token
        csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
        if not csrf_match:
            print("❌ Could not find CSRF token")
            return False
        
        csrf_token = csrf_match.group(1)
        
        # Attempt login
        login_data = {
            'username': username,
            'password': password,
            'csrfmiddlewaretoken': csrf_token,
        }
        
        headers = {
            'Referer': login_url,
            'X-CSRFToken': csrf_token,
        }
        
        response = session.post(login_url, data=login_data, headers=headers, timeout=10)
        
        # Check if login was successful
        if '/admin/' in response.url and response.status_code == 200:
            if 'login' not in response.url:
                print("✅ Login verification successful!")
                return True
        
        print("❌ Login verification failed")
        return False
        
    except Exception as e:
        print(f"❌ Error verifying login: {e}")
        return False

def main():
    """Main execution"""
    print("🚀 Wagtail Superuser Creator (Raw PostgreSQL)")
    print("=" * 60)
    
    # Test database connections
    config = test_database_connections()
    
    if not config:
        print("\n❌ No working database connection found!")
        print("\n💡 Possible solutions:")
        print("1. Ensure PostgreSQL is running")
        print("2. Check database credentials")
        print("3. Verify network connectivity")
        return False
    
    print(f"\n✅ Using database connection: {config['name']}")
    
    # Create superuser
    success = create_wagtail_superuser(config)
    
    if not success:
        return False
    
    # Verify login
    login_success = verify_login_via_http('admin', 'bizosaas123')
    
    if login_success:
        print(f"\n🎉 SUCCESS!")
        print("=" * 60)
        print("✅ Wagtail superuser created and verified")
        print("🔑 Login credentials:")
        print("   Username: admin")
        print("   Password: bizosaas123")
        print("   Admin URL: http://localhost:8006/admin/")
        print("=" * 60)
        return True
    else:
        print(f"\n⚠️  Superuser created but login verification failed")
        print("🔑 Try these credentials manually:")
        print("   Username: admin")
        print("   Password: bizosaas123")
        print("   Admin URL: http://localhost:8006/admin/")
        return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)