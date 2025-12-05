#!/bin/bash
# PWA Deployment Script for bizosaas-admin
echo "🚀 Deploying PWA files for bizosaas-admin"
sudo cp -r pwa-templates/bizosaas-admin-public/* frontend/apps/bizosaas-admin/public/
echo "✅ PWA deployment complete for bizosaas-admin"
