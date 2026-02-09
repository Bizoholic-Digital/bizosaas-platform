#!/usr/bin/env python3
"""
Wagtail Admin Creator for Shared PostgreSQL Infrastructure
This script tries multiple database configurations to find the right one
"""

import os
import sys
import django
import psycopg2
from psycopg2.extras import RealDictCursor
import requests
import time

# Possible database configurations to try
DB_CONFIGS = [
    # Shared infrastructure credentials (most likely)
    {
        'host': 'localhost',
        'port': 5432,
        'database': 'bizoholic',
        'user': 'bizoholic_user',
        'password': 'BizoHolic2024!Secure',
        'name': 'Shared Infrastructure - BizOholic Database'
    },
    {
        'host': 'localhost',
        'port': 5432,
        'database': 'postgres',
        'user': 'postgres',
        'password': 'SharedInfra2024!SuperSecure',
        'name': 'Shared Infrastructure - Postgres Database'
    },
    # Docker-compose credentials (fallback)
    {
        'host': 'localhost',
        'port': 5432,
        'database': 'bizosaas',
        'user': 'admin',
        'password': 'securepassword',
        'name': 'Docker Compose - BizOSaaS Database'
    },
    # Alternative configurations
    {
        'host': 'localhost',
        'port': 5432,
        'database': 'wagtail',
        'user': 'admin',
        'password': 'securepassword',
        'name': 'Docker Compose - Wagtail Database'
    }
]

def test_database_connection(config):
    """Test if we can connect to the database with given config"""
    try:
        conn = psycopg2.connect(
            host=config['host'],
            port=config['port'],
            database=config['database'],
            user=config['user'],
            password=config['password']
        )
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Test if we can query the database
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return True, version['version']
    except Exception as e:
        return False, str(e)

def check_django_tables(config):
    """Check if Django auth tables exist in the database"""
    try:
        conn = psycopg2.connect(
            host=config['host'],
            port=config['port'],
            database=config['database'],
            user=config['user'],
            password=config['password']
        )
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Check for Django auth_user table
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'auth_user'
            );
        """)
        auth_user_exists = cursor.fetchone()['exists']
        
        # List all tables to understand the schema
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        table_names = [t['table_name'] for t in tables]
        
        cursor.close()
        conn.close()
        
        return auth_user_exists, table_names
    except Exception as e:
        return False, str(e)

def create_superuser_in_database(config):
    """Create superuser directly in the database"""
    try:
        conn = psycopg2.connect(
            host=config['host'],
            port=config['port'],
            database=config['database'],
            user=config['user'],
            password=config['password']
        )
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Check existing users
        cursor.execute("SELECT username, email, is_superuser, is_staff FROM auth_user;")
        existing_users = cursor.fetchall()
        
        print(f"🔍 Found {len(existing_users)} existing users in {config['name']}:")
        for user in existing_users:
            print(f"   - {user['username']} ({user['email']}) - Superuser: {user['is_superuser']}")
        
        # Delete existing admin user
        cursor.execute("DELETE FROM auth_user WHERE username = 'admin';")
        deleted_count = cursor.rowcount
        if deleted_count > 0:
            print(f"🗑️  Removed {deleted_count} existing admin user(s)")
        
        # Configure Django before importing password hasher
        if not django.conf.settings.configured:
            django.conf.settings.configure(
                SECRET_KEY='temp-key-for-password-hashing-only',
                USE_TZ=True,
                PASSWORD_HASHERS=[
                    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
                ],
                DATABASES={
                    'default': {
                        'ENGINE': 'django.db.backends.sqlite3',
                        'NAME': ':memory:',
                    }
                }
            )
            django.setup()
        
        # Create new admin user with hashed password
        from django.contrib.auth.hashers import make_password
        hashed_password = make_password('bizosaas123')
        
        # Insert new admin user
        cursor.execute("""
            INSERT INTO auth_user (
                username, email, password, is_superuser, is_staff, 
                is_active, date_joined, first_name, last_name
            ) VALUES (
                'admin', 'admin@bizosaas.local', %s, true, true, 
                true, NOW(), 'Admin', 'User'
            ) RETURNING id;
        """, (hashed_password,))
        
        user_id = cursor.fetchone()['id']
        
        # Commit changes
        conn.commit()
        
        print(f"✅ Admin user created successfully! (ID: {user_id})")
        print("   👤 Username: admin")
        print("   📧 Email: admin@bizosaas.local")
        print("   🔐 Password: bizosaas123")
        print("   🌐 Admin URL: http://localhost:8006/admin/")
        
        # Verify the user was created
        cursor.execute("SELECT username, email, is_superuser, is_staff FROM auth_user WHERE username = 'admin';")
        new_user = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if new_user:
            print("🔍 Verification:")
            print(f"   User exists: ✅")
            print(f"   Is superuser: {'✅' if new_user['is_superuser'] else '❌'}")
            print(f"   Is staff: {'✅' if new_user['is_staff'] else '❌'}")
            return True, config
        else:
            print("❌ Failed to verify user creation")
            return False, None
            
    except Exception as e:
        print(f"❌ Error creating user in {config['name']}: {e}")
        return False, None

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
            return True
        elif 'Please enter a correct username and password' in response.text:
            print("❌ Login failed: Invalid credentials")
            return False
        else:
            print(f"❌ Login failed: Unexpected response (Status: {response.status_code})")
            return False
            
    except requests.RequestException as e:
        print(f"❌ Login test error: {e}")
        return False

def main():
    print("🔧 Wagtail Admin Creator for Shared PostgreSQL")
    print("=" * 60)
    
    working_config = None
    
    # Step 1: Find the working database configuration
    print("🔍 Testing database configurations...")
    for i, config in enumerate(DB_CONFIGS, 1):
        print(f"\n[{i}/{len(DB_CONFIGS)}] Testing: {config['name']}")
        print(f"   Connection: {config['user']}@{config['host']}:{config['port']}/{config['database']}")
        
        # Test connection
        can_connect, result = test_database_connection(config)
        if can_connect:
            print(f"   ✅ Connection successful")
            print(f"   📊 PostgreSQL: {result.split(',')[0]}")
            
            # Check for Django tables
            has_auth_table, tables_info = check_django_tables(config)
            if has_auth_table:
                print(f"   ✅ Django auth_user table found")
                print(f"   📋 Total tables: {len(tables_info) if isinstance(tables_info, list) else 'Unknown'}")
                working_config = config
                break
            else:
                print(f"   ❌ Django auth_user table not found")
                if isinstance(tables_info, list):
                    print(f"   📋 Found {len(tables_info)} tables: {', '.join(tables_info[:5])}{' ...' if len(tables_info) > 5 else ''}")
        else:
            print(f"   ❌ Connection failed: {result}")
    
    if not working_config:
        print("\n❌ Could not find a working database configuration with Django tables")
        print("\n💡 Possible solutions:")
        print("1. Run Django migrations first: python manage.py migrate")
        print("2. Check if the database exists and has the correct permissions")
        print("3. Verify the database credentials in the docker-compose.yml")
        return False
    
    # Step 2: Create the admin user
    print(f"\n🚀 Creating admin user in: {working_config['name']}")
    success, used_config = create_superuser_in_database(working_config)
    
    if success:
        # Step 3: Test login
        print("\n🧪 Testing login credentials...")
        time.sleep(2)  # Give the system time to process
        login_success = test_admin_login()
        
        if login_success:
            print("\n🎉 SUCCESS!")
            print("=" * 60)
            print("✅ Wagtail admin user created and verified!")
            print("")
            print("🔑 LOGIN CREDENTIALS:")
            print("   Username: admin")
            print("   Password: bizosaas123")
            print("   URL: http://localhost:8006/admin/")
            print("")
            print(f"🗄️  DATABASE USED:")
            print(f"   {used_config['name']}")
            print(f"   Host: {used_config['host']}:{used_config['port']}")
            print(f"   Database: {used_config['database']}")
            print(f"   User: {used_config['user']}")
            return True
        else:
            print("\n⚠️  User created but login test failed")
            print("   Please try logging in manually with the credentials above")
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
        import traceback
        traceback.print_exc()
        sys.exit(1)