#!/bin/bash
# Quick push script with manual authentication prompt

echo "🚀 Pushing infrastructure port fix to GitHub..."
echo ""
echo "Current changes:"
git status --short
echo ""

# Try to push
git push origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    echo "Next step: Redeploy in Dokploy"
    echo "  1. Go to dk.bizoholic.com"
    echo "  2. Navigate to bizosaas_infrastructure_staging → staging → infrastructure_services"
    echo "  3. Click 'Redeploy'"
else
    echo ""
    echo "❌ Push failed. Please authenticate with GitHub."
    echo ""
    echo "You may need to:"
    echo "  1. Update your GitHub personal access token"
    echo "  2. Or manually update the file at:"
    echo "     https://github.com/Bizoholic-Digital/bizosaas-platform/edit/main/dokploy-infrastructure-staging.yml"
fi
