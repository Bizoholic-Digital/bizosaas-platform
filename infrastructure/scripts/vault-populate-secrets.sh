#!/bin/bash

# Vault Setup Script - Populate all credentials from credentials.md
# This script securely stores all credentials in HashiCorp Vault

export VAULT_ADDR="http://localhost:8200"
export VAULT_TOKEN="bizosaas-root-token"

echo "🔐 Populating HashiCorp Vault with BizOSaaS Credentials..."

# Wait for Vault to be ready
until curl -s $VAULT_ADDR/v1/sys/health > /dev/null 2>&1; do
  echo "Waiting for Vault to be ready..."
  sleep 2
done

echo "✅ Vault is ready. Starting credential population..."

# Enable KV secrets engine if not already enabled
vault secrets enable -path=bizosaas kv-v2 2>/dev/null || echo "KV engine already enabled"

# =============================================================================
# DOKPLOY CREDENTIALS
# =============================================================================
echo "📦 Setting Dokploy credentials..."
vault kv put bizosaas/dokploy \
  admin_email="bizoholic.digital@gmail.com" \
  admin_password="25IKC#1XiKABRo" \
  api_key="VumUVyBHPJQUlXiGnwVxeyKYBeGOLOttGjkgkGiwpSHLiEYegUBkCSTPFmQqMbtC" \
  domain="dk.bizoholic.com"

# =============================================================================
# WORDPRESS CREDENTIALS
# =============================================================================
echo "🌐 Setting WordPress credentials..."
vault kv put bizosaas/wordpress \
  admin_username="superadmin" \
  admin_password="BizoSaaS2024!Admin" \
  site_url="https://www.bizoholic.com" \
  admin_url="https://www.bizoholic.com/wp-admin/"

# =============================================================================
# N8N AUTOMATION CREDENTIALS
# =============================================================================
echo "🤖 Setting n8n credentials..."
vault kv put bizosaas/n8n \
  admin_email="bizoholic.com@gmail.com" \
  admin_password="EGEw887eU\$l\$pf" \
  jwt_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmMGRmNmU1OC04MTI4LTQ0ZWEtOWMyMS0xYTU3ODNmN2Y5MDciLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzU1NTEwNDI2LCJleHAiOjE3NTgwNjAwMDB9.3L-Y1HzZzA11ebsYeikmg6W4o481clKuSnjhvSvces8" \
  webhook_url="https://automationhub-n8n-91feb0-194-238-16-237.traefik.me/" \
  host="automationhub-n8n-91feb0-194-238-16-237.traefik.me" \
  protocol="https"

# =============================================================================
# DATABASE CREDENTIALS
# =============================================================================
echo "🗄️ Setting database credentials..."

# PostgreSQL Main
vault kv put bizosaas/postgresql/main \
  host="postgres" \
  port="5432" \
  user="postgres" \
  password="SharedInfra2024!SuperSecure" \
  database="postgres"

# Project-specific database passwords
vault kv put bizosaas/postgresql/coreldove \
  password="CorelDove2024!Secure"

vault kv put bizosaas/postgresql/bizoholic \
  password="BizoHolic2024!Secure"

vault kv put bizosaas/postgresql/thrillring \
  password="ThrillRing2024!Secure"

vault kv put bizosaas/postgresql/analytics \
  password="SharedAnalytics2024!"

vault kv put bizosaas/postgresql/readonly \
  password="ReadOnly2024!Reports"

# N8N Database
vault kv put bizosaas/postgresql/n8n \
  host="postgres" \
  port="5432" \
  user="n8n" \
  password="n8npass" \
  database="n8ndb"

# pgAdmin
vault kv put bizosaas/pgadmin \
  email="admin@coreldove.com" \
  password="SharedPgAdmin2024!Secure" \
  domain="pgadmin.bizoholic.com"

# =============================================================================
# DRAGONFLY/REDIS CREDENTIALS
# =============================================================================
echo "🔴 Setting Dragonfly/Redis credentials..."
vault kv put bizosaas/dragonfly \
  password="SharedDragonfly2024!Secure" \
  host="dragonfly" \
  port="6379"

# =============================================================================
# EXTERNAL API KEYS
# =============================================================================
echo "🔑 Setting external API keys..."

# OpenRouter for CrewAI
vault kv put bizosaas/api-keys/openrouter \
  api_key="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"

# Amazon Seller Central
vault kv put bizosaas/api-keys/amazon \
  seller_email="wahie.reema@outlook.com" \
  seller_password="QrDM474ckcbG87" \
  marketplace="sellercentral.amazon.in"

# =============================================================================
# SERVER/INFRASTRUCTURE CREDENTIALS
# =============================================================================
echo "🖥️ Setting server credentials..."

# Hostinger VPS
vault kv put bizosaas/infrastructure/hostinger \
  ssh_user="root" \
  ssh_host="194.238.16.237" \
  ssh_password="&k3civYG5Q6YPb" \
  api_token="xki5zwT4cvMXVY7OzqfJV8p1q77icPqGcf4G8PDN3abc2a2d" \
  server_id="894670"

# =============================================================================
# TELEGRAM BOT TOKENS
# =============================================================================
echo "📱 Setting Telegram bot tokens..."

vault kv put bizosaas/telegram-bots/jonnyai \
  token="7200437482:AAF8aE2uymF5ukm-ntlEnXx1hfhX1Obcfaw" \
  username="jonnyaibot"

vault kv put bizosaas/telegram-bots/bizoholic \
  token="7767279872:AAGxwC7AcjSpkdF3xdvuLAw1gfXAplYLhMw" \
  username="BizoholicAIBot"

vault kv put bizosaas/telegram-bots/deals4all \
  token="1217910149:AAHZwP0RnxcaqMheU08so6hpyXL7H8tZfYw" \
  username="Deals4all_bot"

vault kv put bizosaas/telegram-bots/bottrader \
  token="7780097136:AAELAgYZsfmBCTuYxwHvqoITqwVjKZp-u0Y" \
  username="BottraderAdmin_bot"

vault kv put bizosaas/telegram-bots/fatherbot \
  token="1011283832:AAHtpTljpQFhypOaQJwWei4z4Y5hgoMNSmk" \
  username="go_go_fatherbot"

# =============================================================================
# BACKUP CONFIGURATION
# =============================================================================
echo "💾 Setting backup configuration..."
vault kv put bizosaas/backup \
  retention_days="30" \
  s3_bucket="shared-infrastructure-backups" \
  network="dokploy-network"

echo ""
echo "🎉 All credentials have been securely stored in Vault!"
echo ""
echo "📋 Available secret paths:"
echo "  • bizosaas/dokploy"
echo "  • bizosaas/wordpress"
echo "  • bizosaas/n8n"
echo "  • bizosaas/postgresql/*"
echo "  • bizosaas/pgadmin"
echo "  • bizosaas/dragonfly"
echo "  • bizosaas/api-keys/*"
echo "  • bizosaas/infrastructure/*"
echo "  • bizosaas/telegram-bots/*"
echo "  • bizosaas/backup"
echo ""
echo "🔐 Access Vault UI at: http://localhost:8200"
echo "🗝️  Root token: bizosaas-root-token"
echo ""
echo "✅ Vault setup complete!"