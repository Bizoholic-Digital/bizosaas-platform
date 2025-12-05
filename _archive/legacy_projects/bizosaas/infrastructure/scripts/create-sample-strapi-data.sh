#!/bin/bash

echo "🔧 Setting up Strapi sample data and permissions..."

STRAPI_URL="http://localhost:1337"

echo "📋 Manual Setup Instructions:"
echo ""
echo "1. Open Strapi Admin: ${STRAPI_URL}/admin"
echo "2. Create admin user (first time setup)"
echo "3. Go to Settings → Users & Permissions Plugin → Roles → Public"
echo "4. Enable the following permissions:"
echo ""
echo "   📝 Blog Post:"
echo "   ☐ find (get all blog posts)"
echo "   ☐ findOne (get single blog post)"
echo ""
echo "   🛠️ Service:"
echo "   ☐ find (get all services)"
echo "   ☐ findOne (get single service)"
echo ""
echo "   📄 Page:"
echo "   ☐ find (get all pages)"
echo "   ☐ findOne (get single page)"
echo ""
echo "   📊 Case Study:"
echo "   ☐ find (get all case studies)"
echo "   ☐ findOne (get single case study)"
echo ""
echo "5. Click Save"
echo ""
echo "🔗 Then test endpoints:"
echo "   curl \"${STRAPI_URL}/api/blog-posts\""
echo "   curl \"${STRAPI_URL}/api/services\""
echo "   curl \"${STRAPI_URL}/api/pages\""
echo "   curl \"${STRAPI_URL}/api/case-studies\""
echo ""

# Test if admin is accessible
echo "🔍 Testing Strapi Admin accessibility..."
if curl -s "${STRAPI_URL}/admin" >/dev/null 2>&1; then
    echo "✅ Strapi admin is accessible at: ${STRAPI_URL}/admin"
    
    # Test current API status
    echo ""
    echo "📊 Current API Status:"
    
    endpoints=("/api/blog-posts" "/api/services" "/api/pages" "/api/case-studies")
    
    for endpoint in "${endpoints[@]}"; do
        status=$(curl -s -o /dev/null -w "%{http_code}" "${STRAPI_URL}${endpoint}")
        if [ "$status" = "200" ]; then
            echo "  ✅ ${endpoint} - Working (200)"
        elif [ "$status" = "403" ]; then
            echo "  ❌ ${endpoint} - Forbidden (403) - Needs permissions"
        else
            echo "  ⚠️  ${endpoint} - Status: ${status}"
        fi
    done
    
    echo ""
    echo "If all endpoints show '403 Forbidden', please set up permissions in admin panel."
    
else
    echo "❌ Strapi admin not accessible. Please check if Strapi is running."
fi

echo ""
echo "🚀 Once permissions are set, the frontend will automatically display content!"