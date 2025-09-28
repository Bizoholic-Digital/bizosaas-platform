#!/bin/bash
# 🚀 BizOSaaS Platform GitHub Push Script
# Execute this script after providing your GitHub Personal Access Token

set -e

echo "🚀 BizOSaaS Platform GitHub Push"
echo "================================"

# Check if token is provided
if [ -z "$1" ]; then
    echo "❌ Error: GitHub Personal Access Token required"
    echo ""
    echo "Usage: ./PUSH_TO_GITHUB.sh YOUR_GITHUB_TOKEN"
    echo ""
    echo "To generate a token:"
    echo "1. Go to: https://github.com/settings/tokens"
    echo "2. Click 'Generate new token (classic)'"
    echo "3. Select scopes: repo, workflow, admin:repo_hook"
    echo "4. Copy the token and run: ./PUSH_TO_GITHUB.sh ghp_your_token_here"
    exit 1
fi

GITHUB_TOKEN="$1"

echo "🔧 Configuring remote with token..."
git remote set-url origin "https://alagiri.rajesh@gmail.com:${GITHUB_TOKEN}@github.com/Bizoholic-Digital/bizosaas-platform.git"

echo "📊 Repository status:"
git status --porcelain | wc -l | xargs echo "  - Staged files:"
git log --oneline -1

echo "🚀 Pushing to GitHub..."
git push -u origin main

echo "✅ Push completed successfully!"
echo ""
echo "🔗 Repository: https://github.com/Bizoholic-Digital/bizosaas-platform"
echo "📋 Next steps:"
echo "  1. Configure GitHub Actions secrets"
echo "  2. Set up VPS deployment"
echo "  3. Test CI/CD pipeline"