#!/bin/bash
set -e

# --- 1. Fix Admin Portal ---
ADMIN_DIR="/etc/dokploy/compose/compose-index-primary-transmitter-1m7zzg/code"
ADMIN_FILE="$ADMIN_DIR/docker-compose.admin-portal.yml"

echo "Updating Admin Portal labels..."
cat > "$ADMIN_FILE" << 'EOF'
version: "3.8"
services:
  admin-dashboard:
    image: ghcr.io/bizoholic-digital/bizosaas-platform/admin-dashboard:staging
    container_name: admin-dashboard
    environment:
      - NEXT_PUBLIC_API_URL=https://api.bizoholic.net
      - API_URL=https://api.bizoholic.net
      - AUTH_AUTHENTIK_ID=bizosaas-portal
      - NEXT_PUBLIC_AUTH_AUTHENTIK_ID=bizosaas-portal
      - AUTH_AUTHENTIK_SECRET=BizOSaaS2024!AuthentikSecret
      - AUTH_AUTHENTIK_ISSUER=https://auth-sso.bizoholic.net/application/o/bizosaas-platform/
      - NEXTAUTH_URL=https://admin.bizoholic.net
      - AUTH_URL=https://admin.bizoholic.net
      - NEXTAUTH_SECRET=BizOSaaS2025!Secret!NextAuth
      - AUTH_SECRET=BizOSaaS2025!Secret!NextAuth
      - AUTH_TRUST_HOST=true
      - AUTH_SUCCESS_URL=https://admin.bizoholic.net/dashboard
      - NODE_ENV=production
      - NEXT_PUBLIC_APP_URL=https://admin.bizoholic.net
      - PORT=3004
    labels:
      - "traefik.enable=true"
      - "traefik.docker.network=dokploy-network"
      - "traefik.http.routers.admin-dashboard.rule=Host(`admin.bizoholic.net`)"
      - "traefik.http.routers.admin-dashboard.entrypoints=websecure"
      - "traefik.http.routers.admin-dashboard.tls.certresolver=letsencrypt"
      - "traefik.http.services.admin-dashboard.loadbalancer.server.port=3004"
    networks:
      - dokploy-network
    expose:
      - 3004
    restart: unless-stopped
    healthcheck:
      test: [ "CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://127.0.0.1:3004/login" ]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M

networks:
  dokploy-network:
    external: true
    name: dokploy-network
EOF

cd "$ADMIN_DIR"
docker rm -f admin-dashboard || true
docker compose -f docker-compose.admin-portal.yml up -d

# --- 2. Fix Core Stack ---
CORE_DIR="/etc/dokploy/compose/compose-synthesize-online-feed-gb95pq/code"
CORE_FILE="$CORE_DIR/docker-compose.core.yml"
ONBOARDING_FILE="./bizosaas-brain-core/brain-gateway/app/api/onboarding.py"

echo "Updating Core Stack volumes..."
# We use a backup to be safe
cp "$CORE_FILE" "$CORE_FILE.bak"

# Use python to safely add the volume mount to brain-gateway service
python3 - << 'PYEOF'
import yaml
import sys

with open('docker-compose.core.yml', 'r') as f:
    data = yaml.safe_load(f)

if 'brain-gateway' in data['services']:
    service = data['services']['brain-gateway']
    volumes = service.get('volumes', [])
    mount = "./bizosaas-brain-core/brain-gateway/app/api/onboarding.py:/app/app/api/onboarding.py"
    if mount not in volumes:
        volumes.append(mount)
    service['volumes'] = volumes

with open('docker-compose.core.yml', 'w') as f:
    yaml.dump(data, f, default_flow_style=False)
PYEOF

cd "$CORE_DIR"
docker restart bizosaas-brain-staging

echo "System fixed. Verifying..."
sleep 5
docker ps | grep -E 'admin|brain'
