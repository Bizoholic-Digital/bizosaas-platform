#!/bin/bash

echo "=========================================="
echo "Opening BizOSaaS Staging Ports"
echo "=========================================="
echo ""

# Backend ports
echo "Opening backend service ports..."
sudo ufw allow 8001/tcp comment "Brain API"
sudo ufw allow 8002/tcp comment "Wagtail CMS"
sudo ufw allow 8004/tcp comment "Business Directory"
sudo ufw allow 8007/tcp comment "Temporal Integration"
sudo ufw allow 8009/tcp comment "Amazon Sourcing"

# Frontend ports
echo ""
echo "Opening frontend service ports..."
sudo ufw allow 3000/tcp comment "Client Portal"
sudo ufw allow 3001/tcp comment "Bizoholic Frontend"
sudo ufw allow 3002/tcp comment "CorelDove Frontend"
sudo ufw allow 3003/tcp comment "Business Directory Frontend"
sudo ufw allow 3005/tcp comment "Admin Dashboard"

# Reload firewall
echo ""
echo "Reloading firewall..."
sudo ufw reload

# Show status
echo ""
echo "Firewall status:"
sudo ufw status | grep -E "(3000|3001|3002|3003|3005|8001|8002|8004|8007|8009)"

echo ""
echo "=========================================="
echo "✅ All staging ports opened!"
echo "=========================================="
echo ""
echo "Test access with:"
echo "curl http://194.238.16.237:8001/health  # Brain API"
echo "curl http://194.238.16.237:3001/        # Bizoholic Frontend"
