#!/usr/bin/env python3

# Script to fix redirect URL to include proper redirect parameter
import re

# Read the original main.py
with open('temp-main.py', 'r') as f:
    content = f.read()

# Replace the redirect URL to include the proper format
# Change from: login_url = f"{UNIFIED_AUTH_BROWSER_URL}/auth/login/"
# To: login_url = f"{UNIFIED_AUTH_BROWSER_URL}/auth/login/?redirect=%2Fdashboard%2F"

content = content.replace(
    'login_url = f"{UNIFIED_AUTH_BROWSER_URL}/auth/login/"',
    'login_url = f"{UNIFIED_AUTH_BROWSER_URL}/auth/login/?redirect=%2Fdashboard%2F"'
)

# Write the updated version
with open('temp-main-redirect-fixed.py', 'w') as f:
    f.write(content)

print("Fixed redirect URL in temp-main-redirect-fixed.py")