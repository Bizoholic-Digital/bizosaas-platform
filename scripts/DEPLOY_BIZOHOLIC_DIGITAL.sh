#!/bin/bash
# 🏢 Bizoholic-Digital Organization Deployment Script
# Complete automation for BizOSaaS platform deployment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Configuration
ORG_NAME="Bizoholic-Digital"
REPO_NAME="bizosaas-platform"
USER_EMAIL="alagiri.rajesh@gmail.com"
REPO_URL="https://github.com/${ORG_NAME}/${REPO_NAME}.git"

echo -e "${BLUE}🏢 Bizoholic-Digital Organization Deployment${NC}"
echo -e "${BLUE}===========================================${NC}"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Step 1: Verify Git Configuration
echo -e "${YELLOW}📋 Step 1: Verifying Git Configuration...${NC}"
git config --global user.name "Bizoholic Digital"
git config --global user.email "$USER_EMAIL"

echo -e "${GREEN}✅ Git configured for:${NC}"
echo -e "   Name: $(git config user.name)"
echo -e "   Email: $(git config user.email)"
echo -e "   Repository: $REPO_URL"
echo ""

# Step 2: Repository Status
echo -e "${YELLOW}📊 Step 2: Repository Status...${NC}"
TOTAL_FILES=$(git ls-files | wc -l)
LAST_COMMIT=$(git log --oneline -1)

echo -e "${GREEN}✅ Platform Ready:${NC}"
echo -e "   Files: $TOTAL_FILES"
echo -e "   Latest: $LAST_COMMIT"
echo -e "   Branch: $(git branch --show-current)"
echo ""

# Step 3: Manual Repository Creation Instructions
echo -e "${PURPLE}🔧 Step 3: Manual Repository Creation Required${NC}"
echo -e "${YELLOW}Please complete these steps manually:${NC}"
echo ""
echo -e "${BLUE}1. Create Organization Repository:${NC}"
echo -e "   🌐 Go to: https://github.com/orgs/${ORG_NAME}/repositories"
echo -e "   ➕ Click: 'New repository'"
echo -e "   📝 Name: ${REPO_NAME}"
echo -e "   📄 Description: BizOSaaS AI-Powered Marketing Automation Platform - Enterprise SaaS Solution"
echo -e "   🔓 Visibility: Public"
echo -e "   ❌ Initialize: Do NOT add README, .gitignore, or license"
echo -e "   ✅ Click: 'Create repository'"
echo ""

echo -e "${BLUE}2. Generate Personal Access Token:${NC}"
echo -e "   🌐 Go to: https://github.com/settings/tokens"
echo -e "   ➕ Click: 'Generate new token (classic)'"
echo -e "   📝 Note: BizOSaaS Bizoholic-Digital Enterprise Deployment"
echo -e "   ⏰ Expiration: 90 days or No expiration"
echo -e "   🔑 Scopes: ✅ repo, ✅ workflow, ✅ admin:repo_hook, ✅ admin:org"
echo -e "   💾 Copy token (format: ghp_xxxxxxxxxx)"
echo ""

# Step 4: Wait for manual completion
echo -e "${YELLOW}⏳ Waiting for manual completion...${NC}"
echo -e "${BLUE}Press Enter after completing steps 1 and 2 above...${NC}"
read -r

# Step 5: Token Input
echo -e "${YELLOW}🔑 Step 5: Token Configuration...${NC}"
echo -e "${BLUE}Please enter your GitHub Personal Access Token:${NC}"
echo -n "Token (ghp_xxxxxxxxxx): "
read -r GITHUB_TOKEN

if [ -z "$GITHUB_TOKEN" ]; then
    echo -e "${RED}❌ Error: Token is required${NC}"
    exit 1
fi

# Step 6: Configure Remote with Token
echo -e "${YELLOW}🔧 Step 6: Configuring Remote with Token...${NC}"
git remote set-url origin "https://${USER_EMAIL}:${GITHUB_TOKEN}@github.com/${ORG_NAME}/${REPO_NAME}.git"

echo -e "${GREEN}✅ Remote configured with authentication${NC}"
echo ""

# Step 7: Push to Organization Repository
echo -e "${YELLOW}🚀 Step 7: Pushing to Organization Repository...${NC}"
echo -e "${BLUE}Pushing $TOTAL_FILES files to ${ORG_NAME}/${REPO_NAME}...${NC}"

if git push -u origin main; then
    echo ""
    echo -e "${GREEN}🎉 SUCCESS! Platform deployed to organization repository${NC}"
    echo -e "${GREEN}✅ Repository: https://github.com/${ORG_NAME}/${REPO_NAME}${NC}"
    echo ""
else
    echo ""
    echo -e "${RED}❌ Push failed. Please check:${NC}"
    echo -e "   1. Repository created correctly"
    echo -e "   2. Token has correct permissions"
    echo -e "   3. Organization access granted"
    exit 1
fi

# Step 8: Next Steps Instructions
echo -e "${PURPLE}📋 Step 8: Post-Deployment Configuration${NC}"
echo ""
echo -e "${BLUE}Configure GitHub Actions Secrets:${NC}"
echo -e "🌐 Go to: https://github.com/${ORG_NAME}/${REPO_NAME}/settings/secrets/actions"
echo ""
echo -e "${YELLOW}Required Secrets:${NC}"
cat << 'EOF'

# VPS & Infrastructure
VPS_HOST: 194.238.16.237
VPS_USER: root
VPS_PASSWORD: &k3civYG5Q6YPb

# Dokploy Integration
DOKPLOY_URL: http://194.238.16.237:3000
DOKPLOY_API_KEY: VumUVyBHPJQUlXiGnwVxeyKYBeGOLOttGjkgkGiwpSHLiEYegUBkCSTPFmQqMbtC

# Security & Database
POSTGRES_PASSWORD: SharedInfra2024!SuperSecure
JWT_SECRET: ultra-secure-jwt-secret-bizosaas-2025
DJANGO_SECRET_KEY: django-super-secret-key-bizosaas-2025

# AI Services
OPENAI_API_KEY: ${OPENAI_API_KEY}

# Business Communications
NOTIFICATION_EMAIL: alagiri.rajesh@gmail.com
BUSINESS_EMAIL: bizoholic.digital@gmail.com

EOF

echo ""
echo -e "${BLUE}Deploy to VPS:${NC}"
echo -e "   🚀 Run: ./deploy-to-vps.sh"
echo -e "   📊 Monitor: https://github.com/${ORG_NAME}/${REPO_NAME}/actions"
echo ""

echo -e "${GREEN}🏢 Bizoholic-Digital Organization Deployment Complete!${NC}"
echo -e "${BLUE}Professional business repository established for enterprise growth${NC}"