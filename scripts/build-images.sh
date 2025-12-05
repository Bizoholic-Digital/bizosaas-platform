#!/bin/bash
# Build all required Docker images for local development

set -e

echo "🏗️  Building BizOSaaS Docker Images"
echo "===================================="
echo ""

cd "$(dirname "$0")/bizosaas"

echo "📦 Building infrastructure images..."
echo ""

# Build Brain API
if [ -d "./ai/services/bizosaas-brain" ]; then
  echo "🧠 Building Brain API..."
  docker build -t bizosaas-brain:local ./ai/services/bizosaas-brain || echo "⚠️  Brain build failed, will try to continue"
fi

# Build Auth Service
if [ -d "./core/services/auth-service-v2" ]; then
  echo "🔐 Building Auth Service..."
  docker build -t bizosaas-auth:local ./core/services/auth-service-v2 || echo "⚠️  Auth build failed, will try to continue"
fi

# Build Wagtail CMS
if [ -d "./core/services/wagtail-cms" ]; then
  echo "📝 Building Wagtail CMS..."
  docker build -t bizosaas-wagtail:local ./core/services/wagtail-cms || echo "⚠️  Wagtail build failed, will try to continue"
fi

# Build Django CRM
if [ -d "./crm/services/django-crm" ]; then
  echo "📊 Building Django CRM..."
  docker build -t bizosaas-django-crm:local ./crm/services/django-crm || echo "⚠️  CRM build failed, will try to continue"
fi

echo ""
echo "📦 Building frontend images..."
echo ""

# Build Bizoholic Frontend
if [ -d "./frontend/apps/bizoholic-frontend" ]; then
  echo "🎨 Building Bizoholic Frontend..."
  docker build -t bizosaas-bizoholic:local ./frontend/apps/bizoholic-frontend || echo "⚠️  Bizoholic build failed, will try to continue"
fi

# Build CoreLDove Frontend
if [ -d "./frontend/apps/coreldove-frontend" ]; then
  echo "🛒 Building CoreLDove Frontend..."
  docker build -t bizosaas-coreldove:local ./frontend/apps/coreldove-frontend || echo "⚠️  CoreLDove build failed, will try to continue"
fi

# Build Admin Dashboard
if [ -d "./frontend/apps/bizosaas-admin" ]; then
  echo "⚙️  Building Admin Dashboard..."
  docker build -t bizosaas-admin:local ./frontend/apps/bizosaas-admin || echo "⚠️  Admin build failed, will try to continue"
fi

echo ""
echo "✅ Build process complete!"
echo ""
echo "📋 Built images:"
docker images | grep bizosaas | grep local
echo ""
echo "🚀 Now you can run:"
echo "  ./start-bizoholic.sh"
echo "  ./start-coreldove.sh"
echo ""
