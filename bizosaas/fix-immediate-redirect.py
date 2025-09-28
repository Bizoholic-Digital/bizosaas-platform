#!/usr/bin/env python3

# Script to replace HTML redirect with immediate HTTP redirect
import re

# Read the current main.py
with open('temp-main-redirect-fixed.py', 'r') as f:
    content = f.read()

# Find the entire HTML redirect block and replace with HTTP redirect
old_pattern = r'if not user_session:\s+# Redirect to unified login page directly.*?"""\)'
new_code = '''if not user_session:
        # Direct HTTP redirect to login page (no intermediate page)
        login_url = f"{UNIFIED_AUTH_BROWSER_URL}/auth/login/?redirect=%2Fdashboard%2F"
        return RedirectResponse(url=login_url, status_code=302)'''

# Replace using regex with DOTALL flag to match across lines
new_content = re.sub(old_pattern, new_code, content, flags=re.DOTALL)

# Write the fixed version
with open('temp-main-immediate-redirect.py', 'w') as f:
    f.write(new_content)

print("Created immediate redirect version: temp-main-immediate-redirect.py")