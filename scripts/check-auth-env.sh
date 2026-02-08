#!/bin/bash
# Quick diagnostic script to check NextAuth environment variables

echo "🔍 Checking NextAuth Configuration..."
echo ""

# Check Client Portal
echo "📱 CLIENT PORTAL (Port 3004):"
docker exec bizosaas-client-portal-staging env | grep -E "NEXTAUTH|AUTHENTIK" | sort
echo ""

# Check Admin Dashboard  
echo "🔧 ADMIN DASHBOARD (Port 3009):"
docker exec bizosaas-admin-dashboard env | grep -E "NEXTAUTH|AUTHENTIK" | sort
echo ""

echo "✅ Diagnostic complete"
