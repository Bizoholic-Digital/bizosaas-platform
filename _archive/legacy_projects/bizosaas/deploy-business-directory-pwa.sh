#!/bin/bash
# PWA Deployment Script for business-directory
echo "🚀 Deploying PWA files for business-directory"
sudo cp -r pwa-templates/business-directory-public/* frontend/apps/business-directory/public/
echo "✅ PWA deployment complete for business-directory"
