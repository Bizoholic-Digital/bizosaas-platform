#!/bin/bash
# Check Dokploy deployment logs for errors

echo "🔍 Checking Backend Deployment Logs"
echo "====================================="
echo ""

# Backend latest error log
echo "📋 Backend Log (commit 42889a5):"
echo "Log path: /etc/dokploy/logs/backend-services-azbmbl/backend-services-azbmbl-2025-10-13:11:35:19.log"
echo ""

sshpass -p '&k3civYG5Q6YPb' ssh -o StrictHostKeyChecking=no root@194.238.16.237 \
  "tail -100 /etc/dokploy/logs/backend-services-azbmbl/backend-services-azbmbl-2025-10-13:11:35:19.log"

echo ""
echo ""
echo "📋 Frontend Logs"
echo "=================="
# Need to get frontend log path
