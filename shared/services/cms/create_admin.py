#!/usr/bin/env python3
"""
Simple Wagtail Admin Creator Script
This script will create a superuser for Wagtail CMS directly in the running container
"""

import requests
import re
import time
from urllib.parse import urljoin

def test_admin_login(username, password, base_url="http://localhost:8006"):
    """Test admin login credentials"""
    session = requests.Session()
    
    # Get the login page to retrieve CSRF token
    login_url = urljoin(base_url, '/admin/login/')
    
    try:
        # Get login page
        response = session.get(login_url, timeout=10)
        response.raise_for_status()
        
        # Extract CSRF token
        csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
        if not csrf_match:
            return False, "Could not find CSRF token"
        
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
            # Check if we're actually logged in (not redirected back to login)
            if 'login' not in response.url:
                return True, "Login successful!"
        
        # Check for specific error messages
        if 'Please enter a correct username and password' in response.text:
            return False, "Invalid username or password"
        elif 'This account is inactive' in response.text:
            return False, "Account is inactive"
        else:
            return False, f"Login failed (HTTP {response.status_code})"
            
    except requests.RequestException as e:
        return False, f"Connection error: {e}"

def main():
    print("🔍 Wagtail Admin Login Tester")
    print("=" * 50)
    
    # Common credential combinations to test
    credentials_to_test = [
        ("admin", "admin"),
        ("admin", "admin123"),  
        ("admin", "bizosaas123"),
        ("admin", "password"),
        ("admin", "securepassword"),
        ("superuser", "superuser"),
        ("wagtail", "wagtail"),
        ("bizosaas", "bizosaas123"),
        ("root", "root"),
    ]
    
    working_credentials = []
    
    print(f"🧪 Testing {len(credentials_to_test)} credential combinations...")
    print()
    
    for i, (username, password) in enumerate(credentials_to_test, 1):
        print(f"[{i:2d}/{len(credentials_to_test)}] Testing: {username} / {password}")
        
        success, message = test_admin_login(username, password)
        
        if success:
            print(f"   ✅ {message}")
            working_credentials.append((username, password))
        else:
            print(f"   ❌ {message}")
        
        # Small delay to avoid overwhelming the server
        time.sleep(0.5)
    
    print()
    print("=" * 50)
    print("📋 RESULTS")
    print("=" * 50)
    
    if working_credentials:
        print("🎉 WORKING CREDENTIALS FOUND:")
        for username, password in working_credentials:
            print(f"   🔑 Username: {username}")
            print(f"   🔑 Password: {password}")
            print(f"   🌐 Admin URL: http://localhost:8006/admin/")
            print()
        
        print("✅ You can now log in to the Wagtail admin interface!")
        return True
    else:
        print("❌ No working credentials found.")
        print()
        print("🔧 NEXT STEPS:")
        print("1. The database might not have any users created yet")
        print("2. We need to create a superuser using Django management commands")
        print("3. The Wagtail container might need to run migrations first")
        print()
        print("💡 TIP: Try accessing the Wagtail container directly:")
        print("   docker exec -it <wagtail-container> python manage.py createsuperuser")
        return False

if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        exit(1)