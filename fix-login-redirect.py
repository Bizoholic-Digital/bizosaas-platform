#!/usr/bin/env python3

# Quick script to fix the redirect in main.py
import re

# Read the current main.py
with open('temp-main.py', 'r') as f:
    content = f.read()

# Find the redirect block and replace it with direct login page serving
old_pattern = r'if not user_session:\s+# Redirect to unified login page directly.*?"""\)'
new_code = '''if not user_session:
        # Serve login page directly instead of redirecting
        try:
            with open("/app/html/login.html", "r") as f:
                login_html = f.read()
            return HTMLResponse(login_html)
        except Exception as e:
            # Fallback if login.html is not found
            return HTMLResponse("""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>BizOSaaS Admin - Login</title>
                <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
            </head>
            <body class="bg-gray-50">
                <div class="min-h-screen flex items-center justify-center">
                    <div class="max-w-md w-full bg-white p-8 rounded-lg shadow">
                        <h2 class="text-2xl font-bold text-center mb-6">Sign in to BizOSaaS Admin</h2>
                        <p class="text-center text-red-600 mb-4">Login form temporarily unavailable. Please refresh the page.</p>
                        <button onclick="window.location.reload()" class="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700">
                            Refresh Page
                        </button>
                    </div>
                </div>
            </body>
            </html>
            """)'''

# Replace using regex with DOTALL flag
new_content = re.sub(old_pattern, new_code, content, flags=re.DOTALL)

# Write the fixed version
with open('temp-main-fixed.py', 'w') as f:
    f.write(new_content)

print("Fixed main.py created as temp-main-fixed.py")