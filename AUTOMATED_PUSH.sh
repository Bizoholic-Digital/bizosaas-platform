#!/bin/bash
# 🚀 BizOSaaS Platform Automated Push Script
# This script will guide you through the GitHub push process

set -e

echo "🚀 BizOSaaS Platform - Automated GitHub Push"
echo "============================================"
echo ""

# Clean up Git configuration
echo "🔧 Cleaning Git configuration..."
git config --global --unset-all user.name || true
git config --global --unset-all user.email || true
git config --global user.name "alagirirajesh"
git config --global user.email "alagiri.rajesh@gmail.com"

echo "📊 Platform Status:"
echo "  - Repository: https://github.com/Bizoholic-Digital/bizosaas-platform"
echo "  - Branch: main"
echo "  - Files ready: $(git ls-files | wc -l)"
echo "  - Platform: BizOSaaS AI Marketing Automation"
echo ""

# Check repository status
echo "📋 Checking repository status..."
git status --porcelain | head -5
echo ""

# Show what we're about to push
echo "📦 Commit to push:"
git log --oneline -1
echo ""

echo "🔑 Authentication Required:"
echo "You'll be prompted for GitHub credentials in the next step."
echo "Use your GitHub username (alagirirajesh) and Personal Access Token as password."
echo ""
echo "If you don't have a token, generate one at:"
echo "https://github.com/settings/tokens"
echo "Required scopes: repo, workflow, admin:repo_hook"
echo ""

read -p "Press Enter to continue with the push..."

echo "🚀 Pushing to GitHub..."
echo "When prompted:"
echo "  Username: alagiri.rajesh@gmail.com"
echo "  Password: [Your Personal Access Token]"
echo ""

# Attempt the push
if git push -u origin main; then
    echo ""
    echo "✅ SUCCESS! Platform pushed to GitHub"
    echo "🔗 Repository: https://github.com/Bizoholic-Digital/bizosaas-platform"
    echo ""
    echo "📋 Next Steps:"
    echo "1. Configure GitHub Actions secrets"
    echo "2. Set up VPS deployment"
    echo "3. Test CI/CD pipeline"
    echo ""
    echo "📖 Full guide: IMMEDIATE_DEPLOYMENT_STEPS.md"
else
    echo ""
    echo "❌ Push failed. Common solutions:"
    echo "1. Generate Personal Access Token: https://github.com/settings/tokens"
    echo "2. Use token as password when prompted"
    echo "3. Or run: git remote set-url origin https://alagiri.rajesh@gmail.com:TOKEN@github.com/Bizoholic-Digital/bizosaas-platform.git"
    echo ""
    echo "Then retry: ./AUTOMATED_PUSH.sh"
fi