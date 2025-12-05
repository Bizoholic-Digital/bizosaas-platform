#!/bin/bash
# 🔐 Secure Deployment Script for Bizoholic-Digital
# Handles token securely and executes deployment

set -e

echo "🏢 Bizoholic-Digital Secure Deployment"
echo "====================================="
echo ""

# Check if token is provided as argument
if [ -n "$1" ]; then
    GITHUB_TOKEN="$1"
    echo "✅ Token provided via argument"
elif [ -n "$GITHUB_TOKEN" ]; then
    echo "✅ Token found in environment"
else
    echo "🔑 Please provide your GitHub Personal Access Token:"
    echo "Usage: ./SECURE_DEPLOY.sh ghp_your_token_here"
    echo "Or: export GITHUB_TOKEN=ghp_your_token_here && ./SECURE_DEPLOY.sh"
    exit 1
fi

# Validate token format
if [[ ! "$GITHUB_TOKEN" =~ ^ghp_[a-zA-Z0-9]{36}$ ]]; then
    echo "⚠️  Warning: Token format doesn't match expected pattern ghp_xxxxxxxxxx"
    echo "Proceeding anyway..."
fi

echo "📊 Repository Status:"
echo "  - Organization: Bizoholic-Digital"
echo "  - Repository: bizosaas-platform"
echo "  - Files Ready: $(git ls-files | wc -l)"
echo "  - Latest Commit: $(git log --oneline -1)"
echo ""

echo "🔧 Configuring remote with token..."
git remote set-url origin "https://alagiri.rajesh@gmail.com:${GITHUB_TOKEN}@github.com/Bizoholic-Digital/bizosaas-platform.git"

echo "🚀 Pushing to Bizoholic-Digital organization..."
if git push -u origin main; then
    echo ""
    echo "🎉 SUCCESS! BizOSaaS Platform deployed to organization!"
    echo "🔗 Repository: https://github.com/Bizoholic-Digital/bizosaas-platform"
    echo ""
    echo "📋 Next Steps:"
    echo "1. Configure GitHub Actions secrets"
    echo "2. Deploy to VPS: ./deploy-to-vps.sh"
    echo "3. Monitor CI/CD: https://github.com/Bizoholic-Digital/bizosaas-platform/actions"
    echo ""
    echo "✅ Professional Bizoholic-Digital organization repository established!"
else
    echo ""
    echo "❌ Deployment failed. Please check:"
    echo "1. Repository created at: https://github.com/Bizoholic-Digital/bizosaas-platform"
    echo "2. Token has correct permissions (repo, workflow, admin:repo_hook, admin:org)"
    echo "3. Organization access granted"
    exit 1
fi

# Clean up token from git config for security
echo "🔐 Cleaning up credentials..."
git remote set-url origin "https://github.com/Bizoholic-Digital/bizosaas-platform.git"
echo "✅ Credentials cleaned from git config"