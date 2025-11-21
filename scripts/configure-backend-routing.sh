#!/bin/bash
# Configure backend services with Traefik routing labels

set -e

echo "🔧 Configuring Backend Service Routing..."
echo "========================================="

ssh root@72.60.219.244 << 'EOF'

# Function to update service with Traefik labels
update_service() {
  local service=$1
  local hostname=$2
  local path_prefix=$3
  local port=$4

  echo "Configuring $service → $hostname$path_prefix (port $port)"

  # Check if service exists
  if ! docker service ls --filter name=$service --format '{{.Name}}' | grep -q "^${service}$"; then
    echo "⚠️  Service $service not found, skipping..."
    return
  fi

  docker service update \
    --label-add "traefik.enable=true" \
    --label-add "traefik.http.routers.${service}.rule=Host(\`${hostname}\`) && PathPrefix(\`${path_prefix}\`)" \
    --label-add "traefik.http.routers.${service}.entrypoints=websecure" \
    --label-add "traefik.http.routers.${service}.tls.certresolver=letsencrypt" \
    --label-add "traefik.http.middlewares.${service}-strip.stripprefix.prefixes=${path_prefix}" \
    --label-add "traefik.http.routers.${service}.middlewares=${service}-strip@docker" \
    --label-add "traefik.http.services.${service}.loadbalancer.server.port=${port}" \
    $service

  echo "✅ $service configured"
}

# Configure all backend services

# 1. Brain Gateway (default catch-all)
update_service "backend-brain-gateway" "api.bizoholic.com" "/" "8001"

# 2. Auth Service
update_service "backendservices-authservice-ux07ss" "api.bizoholic.com" "/auth" "8002"

# 3. Django CRM
update_service "backend-django-crm" "api.bizoholic.com" "/crm" "8003"

# 4. Wagtail CMS
update_service "backend-wagtail-cms" "api.bizoholic.com" "/cms" "8004"

# 5. Business Directory Backend
update_service "backend-business-directory" "api.bizoholic.com" "/directory" "8005"

# 6. AI Agents Service
update_service "backend-ai-agents" "api.bizoholic.com" "/ai" "8008"

# 7. QuantTrade Backend
update_service "backend-quanttrade-backend" "api.bizoholic.com" "/trading" "8009"

# 8. Amazon Sourcing
update_service "backend-amazon-sourcing" "api.bizoholic.com" "/sourcing" "8010"

# CoreLDove Services (separate domain)

# 9. Saleor GraphQL API
update_service "backend-saleor-api" "api.coreldove.com" "/graphql" "8000"

# 10. CoreLDove Backend
update_service "backend-coreldove-backend" "api.coreldove.com" "/v1" "8006"

echo ""
echo "========================================="
echo "✅ All backend services configured!"
echo ""
echo "Services accessible via:"
echo "  - https://api.bizoholic.com/auth/*"
echo "  - https://api.bizoholic.com/crm/*"
echo "  - https://api.bizoholic.com/cms/*"
echo "  - https://api.bizoholic.com/directory/*"
echo "  - https://api.bizoholic.com/ai/*"
echo "  - https://api.bizoholic.com/trading/*"
echo "  - https://api.bizoholic.com/sourcing/*"
echo "  - https://api.coreldove.com/graphql"
echo "  - https://api.coreldove.com/v1/*"

EOF
