#!/usr/bin/env python3
"""
Wagtail Admin User Fix Script
This script will:
1. Check database connection
2. List existing users
3. Create a superuser if none exists
4. Verify the superuser can log in
"""

import os
import sys
import django
from django.db import connection
from django.contrib.auth import get_user_model

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wagtail_cms.settings.development')

# Add current directory to path
sys.path.insert(0, '/home/alagiri/projects/bizoholic/bizosaas/services/wagtail-cms')

try:
    django.setup()
except Exception as e:
    print(f"Error setting up Django: {e}")
    sys.exit(1)

def check_database_connection():
    """Check if database connection is working"""
    print("🔍 Checking database connection...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            result = cursor.fetchone()
            print(f"✅ Database connected successfully: {result[0]}")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def list_existing_users():
    """List all existing users in the database"""
    print("\n🔍 Checking existing users...")
    try:
        User = get_user_model()
        users = User.objects.all()
        
        if users.exists():
            print(f"📋 Found {users.count()} existing users:")
            for user in users:
                status = "Superuser" if user.is_superuser else "Regular User"
                active = "Active" if user.is_active else "Inactive"
                print(f"  - {user.username} ({user.email}) - {status} - {active}")
            return users
        else:
            print("📭 No users found in database")
            return []
    except Exception as e:
        print(f"❌ Error listing users: {e}")
        return []

def create_superuser(username="admin", email="admin@bizosaas.local", password="bizosaas123"):
    """Create a superuser if none exists"""
    print(f"\n🔧 Creating superuser: {username}")
    try:
        User = get_user_model()
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            print(f"⚠️  User '{username}' already exists")
            user = User.objects.get(username=username)
            if not user.is_superuser:
                print(f"🔧 Making '{username}' a superuser...")
                user.is_superuser = True
                user.is_staff = True
                user.save()
                print(f"✅ '{username}' is now a superuser")
            return user
        
        # Create new superuser
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        user.is_active = True
        user.save()
        
        print(f"✅ Superuser '{username}' created successfully!")
        print(f"   📧 Email: {email}")
        print(f"   🔑 Password: {password}")
        return user
        
    except Exception as e:
        print(f"❌ Error creating superuser: {e}")
        return None

def verify_credentials(username, password):
    """Verify that the credentials work"""
    print(f"\n🔍 Verifying credentials for: {username}")
    try:
        from django.contrib.auth import authenticate
        user = authenticate(username=username, password=password)
        
        if user is not None:
            if user.is_active:
                if user.is_superuser:
                    print(f"✅ Credentials verified! {username} can log in as superuser")
                    return True
                else:
                    print(f"⚠️  {username} can log in but is not a superuser")
                    return False
            else:
                print(f"❌ {username} account is inactive")
                return False
        else:
            print(f"❌ Invalid credentials for {username}")
            return False
            
    except Exception as e:
        print(f"❌ Error verifying credentials: {e}")
        return False

def check_wagtail_permissions():
    """Check if Wagtail permissions are properly set"""
    print("\n🔍 Checking Wagtail permissions...")
    try:
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType
        
        wagtail_permissions = Permission.objects.filter(
            content_type__app_label__in=['wagtailadmin', 'wagtailcore', 'wagtailimages', 'wagtaildocs']
        )
        
        print(f"📋 Found {wagtail_permissions.count()} Wagtail permissions")
        
        # Check if superuser has access
        User = get_user_model()
        superusers = User.objects.filter(is_superuser=True, is_active=True)
        
        if superusers.exists():
            print(f"✅ Found {superusers.count()} active superuser(s)")
            for user in superusers:
                print(f"   - {user.username} (has all permissions)")
        else:
            print("⚠️  No active superusers found")
            
        return True
        
    except Exception as e:
        print(f"❌ Error checking permissions: {e}")
        return False

def main():
    """Main execution function"""
    print("🚀 Wagtail Admin User Fix Script")
    print("=" * 50)
    
    # Step 1: Check database connection
    if not check_database_connection():
        print("\n❌ Cannot proceed without database connection")
        return False
    
    # Step 2: List existing users
    users = list_existing_users()
    
    # Step 3: Check if we have any superusers
    User = get_user_model()
    superusers = User.objects.filter(is_superuser=True, is_active=True)
    
    if not superusers.exists():
        print("\n⚠️  No active superusers found. Creating one...")
        superuser = create_superuser()
        if superuser is None:
            print("\n❌ Failed to create superuser")
            return False
    else:
        print(f"\n✅ Found {superusers.count()} active superuser(s)")
        superuser = superusers.first()
    
    # Step 4: Check permissions
    check_wagtail_permissions()
    
    # Step 5: Try some common credential combinations
    credentials_to_test = [
        ("admin", "bizosaas123"),
        ("admin", "admin123"),
        ("admin", "admin"),
        (superuser.username, "bizosaas123") if superuser else None,
    ]
    
    credentials_to_test = [cred for cred in credentials_to_test if cred is not None]
    
    print(f"\n🔍 Testing credential combinations...")
    working_credentials = []
    
    for username, password in credentials_to_test:
        if verify_credentials(username, password):
            working_credentials.append((username, password))
    
    # Step 6: Display results
    print("\n" + "=" * 50)
    print("🎯 FINAL RESULTS")
    print("=" * 50)
    
    if working_credentials:
        print("✅ WORKING CREDENTIALS FOUND:")
        for username, password in working_credentials:
            print(f"   🔑 Username: {username}")
            print(f"   🔑 Password: {password}")
            print(f"   🌐 Admin URL: http://localhost:8006/admin/")
        
        print(f"\n🎉 You can now log in to Wagtail admin!")
        return True
    else:
        print("❌ No working credentials found")
        
        # Try to reset the admin password
        print("\n🔧 Attempting to reset admin password...")
        try:
            User = get_user_model()
            admin_user = User.objects.filter(username="admin").first()
            
            if admin_user:
                admin_user.set_password("bizosaas123")
                admin_user.is_active = True
                admin_user.is_superuser = True
                admin_user.is_staff = True
                admin_user.save()
                
                print("✅ Admin password reset successfully!")
                print("   🔑 Username: admin")
                print("   🔑 Password: bizosaas123")
                print("   🌐 Admin URL: http://localhost:8006/admin/")
                return True
            else:
                print("❌ Admin user not found")
                
        except Exception as e:
            print(f"❌ Error resetting password: {e}")
        
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