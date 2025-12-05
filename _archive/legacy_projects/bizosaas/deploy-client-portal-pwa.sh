#!/bin/bash
# PWA Deployment Script for client-portal
echo "🚀 Deploying PWA files for client-portal"
sudo cp -r pwa-templates/client-portal-public/* frontend/apps/client-portal/public/
echo "✅ PWA deployment complete for client-portal"
