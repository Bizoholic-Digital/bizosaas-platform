#!/bin/bash
# Stop all BizOSaaS services

set -e

cd "$(dirname "$0")/bizosaas"

echo "🛑 Stopping all BizOSaaS services..."
docker-compose -f docker-compose.unified.yml down

echo ""
echo "✅ All services stopped!"
echo ""
echo "🚀 To start again:"
echo "  ./start-bizoholic.sh  - Start Bizoholic"
echo "  ./start-coreldove.sh  - Start CoreLDove"
echo ""
