#!/bin/bash

echo "🚀 Starting Strapi v5 with Content Types..."

# Stop any existing container
docker stop bizoholic-strapi-v5 2>/dev/null || true
docker rm bizoholic-strapi-v5 2>/dev/null || true

# Start Strapi with proper volume mounting
echo "📦 Starting Strapi container..."
docker run -d \
  --name bizoholic-strapi-v5 \
  -p 1337:1337 \
  -v "/home/alagiri/projects/bizoholic/bizosaas/strapi-v5:/app" \
  -v "/app/node_modules" \
  -v "/app/.tmp" \
  -e NODE_ENV=development \
  -e HOST=0.0.0.0 \
  -e PORT=1337 \
  -e APP_KEYS=bizoholic-key1,bizoholic-key2,bizoholic-key3,bizoholic-key4 \
  -e API_TOKEN_SALT=bizoholic-api-token-salt \
  -e ADMIN_JWT_SECRET=bizoholic-admin-jwt-secret \
  -e TRANSFER_TOKEN_SALT=bizoholic-transfer-token-salt \
  -e JWT_SECRET=bizoholic-jwt-secret \
  strapi-v5-dev

echo "⏳ Waiting for Strapi to start..."
sleep 5

# Check if container is running
if [ "$(docker ps -q -f name=bizoholic-strapi-v5)" ]; then
    echo "✅ Container started successfully"
    
    # Wait for Strapi to be ready
    echo "⏳ Waiting for Strapi to be ready (this may take 30-60 seconds)..."
    for i in {1..30}; do
        if curl -s http://localhost:1337 >/dev/null 2>&1; then
            echo "✅ Strapi is ready!"
            echo ""
            echo "🎉 Setup Complete!"
            echo ""
            echo "📋 Next Steps:"
            echo "1. Open admin panel: http://localhost:1337/admin"
            echo "2. Create admin user (if first time)"
            echo "3. Go to Settings → Users & Permissions → Roles → Public"
            echo "4. Enable 'find' and 'findOne' permissions for:"
            echo "   - Blog Post"
            echo "   - Service" 
            echo "   - Page"
            echo "   - Case Study"
            echo ""
            echo "🔗 API Endpoints (after setting permissions):"
            echo "   http://localhost:1337/api/blog-posts"
            echo "   http://localhost:1337/api/services"
            echo "   http://localhost:1337/api/pages"
            echo "   http://localhost:1337/api/case-studies"
            echo ""
            echo "📝 To add sample data, run:"
            echo "   node create-strapi-content-types.js --sample-data"
            break
        fi
        echo "  Still waiting... ($i/30)"
        sleep 2
    done
    
    if [ $i -eq 30 ]; then
        echo "⚠️  Strapi is taking longer than expected to start"
        echo "📋 Check logs with: docker logs bizoholic-strapi-v5"
        echo "📋 Check container with: docker ps"
    fi
else
    echo "❌ Container failed to start"
    echo "📋 Check logs with: docker logs bizoholic-strapi-v5"
fi