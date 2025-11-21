#!/bin/bash

echo "🔧 Setting up Admin Accounts for BizOSaaS Platform"
echo "================================================="

echo ""
echo "📊 Saleor E-commerce Admin Setup"
echo "---------------------------------"
echo "Creating admin user for Saleor Dashboard..."

# Create Saleor admin via environment variables
docker exec saleor-api bash -c "
echo \"from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@coreldove.com', 'admin123')\" | python manage.py shell
"

if [ $? -eq 0 ]; then
    echo "✅ Saleor Admin Created Successfully!"
    echo "   • URL: http://localhost:9000"
    echo "   • Username: admin"  
    echo "   • Password: admin123"
    echo "   • Email: admin@coreldove.com"
else
    echo "⚠️ Saleor admin may already exist or needs manual setup"
fi

echo ""
echo "📝 Wagtail CMS Admin Setup"  
echo "-------------------------"
echo "Creating admin user for Wagtail Dashboard..."

# Wait for database connection and create Wagtail admin
sleep 5
docker exec wagtail-cms bash -c "
python manage.py migrate --noinput 2>/dev/null || true
echo \"from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@bizoholic.com', 'admin123')\" | python manage.py shell
" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ Wagtail Admin Created Successfully!"
    echo "   • URL: http://localhost:8006/admin/"
    echo "   • Username: admin"
    echo "   • Password: admin123"  
    echo "   • Email: admin@bizoholic.com"
else
    echo "⚠️ Wagtail admin creation failed - database connection issue"
fi

echo ""
echo "🔐 Vault Access Info"
echo "-------------------"
echo "✅ HashiCorp Vault Access:"
echo "   • URL: http://localhost:8200"
echo "   • Method: Token"
echo "   • Token: myroot"

echo ""
echo "⏰ Temporal Dashboard"
echo "--------------------"
echo "✅ Temporal Web UI:"
echo "   • URL: http://localhost:8233"
echo "   • No authentication required"

echo ""
echo "🚀 QUICK ACCESS SUMMARY"
echo "======================="
echo ""
echo "🛒 E-COMMERCE (CoreLDove)"
echo "  Frontend: http://localhost:3000/coreldove"
echo "  Admin: http://localhost:9000 (admin/admin123)"
echo "  API: http://localhost:8100/graphql/"
echo ""
echo "📢 MARKETING AGENCY (Bizoholic)"  
echo "  Frontend: http://localhost:3000"
echo "  CMS: http://localhost:8006/admin/ (admin/admin123)"
echo "  APIs: http://localhost:8004/docs (Payments)"
echo "        http://localhost:8008/docs (Marketing)"
echo "        http://localhost:8009/docs (Amazon)"
echo ""
echo "🏗️ INFRASTRUCTURE"
echo "  Vault: http://localhost:8200 (Token: myroot)"
echo "  Temporal: http://localhost:8233"
echo "  Database: localhost:5432 (postgres/postgres)"

echo ""
echo "✨ Setup Complete! All admin accounts ready for testing."