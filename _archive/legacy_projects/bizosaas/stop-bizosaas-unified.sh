#!/bin/bash

# BizOSaaS Platform - Unified Stack Stop Script

set -e

echo "🛑 Stopping BizOSaaS Platform - Unified Stack"
echo "============================================="

# Stop all services
echo "⏹️ Stopping all services..."
docker-compose -f docker-compose.unified.yml down

# Show final status
echo ""
echo "✅ BizOSaaS Platform Stopped Successfully!"
echo "========================================="
echo ""
echo "💡 To start again: ./start-bizosaas-unified.sh"
echo "🗑️ To remove all data: docker-compose -f docker-compose.unified.yml down -v"
echo ""