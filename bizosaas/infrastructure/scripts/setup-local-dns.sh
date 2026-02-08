#!/bin/bash

# BizoSaaS Local DNS Setup Script
echo "🌐 Setting up BizoSaaS local domains..."

# Check if running as root for /etc/hosts modification
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (sudo ./setup-local-dns.sh)"
    exit 1
fi

# Backup current hosts file
cp /etc/hosts /etc/hosts.backup.$(date +%Y%m%d_%H%M%S)
echo "✅ Backed up current hosts file"

# Define BizoSaaS domains
DOMAINS=(
    "bizosaas.local"
    "api.bizosaas.local"
    "traefik.bizosaas.local"
    "ai.bizosaas.local"
    "onboarding.bizosaas.local"
    "strategy.bizosaas.local"
    "marketing.bizosaas.local"
    "analytics.bizosaas.local"
    "cms.bizosaas.local"
    "vault.bizosaas.local"
    "crm.bizosaas.local"
    "auth.bizosaas.local"
    "payments.bizosaas.local"
    "orchestration.bizosaas.local"
)

# Add BizoSaaS section to hosts file
echo "" >> /etc/hosts
echo "# BizoSaaS Development Domains - Added $(date)" >> /etc/hosts

for domain in "${DOMAINS[@]}"; do
    # Check if domain already exists
    if ! grep -q "$domain" /etc/hosts; then
        echo "127.0.0.1 $domain" >> /etc/hosts
        echo "➕ Added: $domain"
    else
        echo "⏭️  Exists: $domain"
    fi
done

echo ""
echo "🎉 BizoSaaS domains setup complete!"
echo ""
echo "🚀 Available URLs:"
echo "   📊 Dashboard:    http://bizosaas.local"
echo "   🔧 Traefik:      http://traefik.bizosaas.local"  
echo "   🚀 API Gateway:  http://api.bizosaas.local"
echo "   🤖 AI Services:  http://ai.bizosaas.local"
echo "   📝 CMS:          http://cms.bizosaas.local"
echo "   🔐 Vault:        http://vault.bizosaas.local"
echo ""
echo "📋 Full domain list:"
for domain in "${DOMAINS[@]}"; do
    echo "   http://$domain"
done
echo ""
echo "🔍 To verify setup: ping bizosaas.local"