#!/bin/bash

# CI/CD Setup Verification Script
# Checks all prerequisites before triggering first build

set -e

echo "=================================================="
echo "GitHub Actions CI/CD Setup Verification"
echo "=================================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
PASSED=0
FAILED=0
WARNINGS=0

# Helper functions
check_pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((PASSED++))
}

check_fail() {
    echo -e "${RED}✗${NC} $1"
    ((FAILED++))
}

check_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
    ((WARNINGS++))
}

echo "1. Checking Local Repository..."
echo "================================"

# Check if we're in the right directory
if [ -f ".github/workflows/deploy-staging.yml" ]; then
    check_pass "Workflow file exists"
else
    check_fail "Workflow file NOT found (.github/workflows/deploy-staging.yml)"
fi

# Check git remote
REMOTE_URL=$(git remote get-url origin 2>/dev/null || echo "")
if [[ "$REMOTE_URL" == *"Bizoholic-Digital/bizosaas-platform"* ]]; then
    check_pass "Git remote configured: $REMOTE_URL"
else
    check_fail "Git remote incorrect: $REMOTE_URL"
fi

# Check current branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [[ "$CURRENT_BRANCH" == "main" ]] || [[ "$CURRENT_BRANCH" == "staging" ]]; then
    check_pass "On deployable branch: $CURRENT_BRANCH"
else
    check_warn "On branch: $CURRENT_BRANCH (workflow triggers on main/staging)"
fi

# Check uncommitted changes
if git diff-index --quiet HEAD --; then
    check_pass "No uncommitted changes"
else
    check_warn "Uncommitted changes detected (workflow uses committed code only)"
fi

echo ""
echo "2. Checking Dockerfiles..."
echo "================================"

# Check Brain Gateway
if [ -f "bizosaas/ai/services/bizosaas-brain/Dockerfile" ]; then
    check_pass "Brain Gateway Dockerfile exists"
else
    check_fail "Brain Gateway Dockerfile NOT found"
fi

# Check Frontend Dockerfiles
FRONTEND_APPS=("bizoholic-frontend" "coreldove-frontend" "client-portal" "bizosaas-admin" "business-directory-frontend" "thrillring-gaming")

for app in "${FRONTEND_APPS[@]}"; do
    if [ -f "bizosaas/frontend/apps/$app/Dockerfile.production" ]; then
        check_pass "Frontend Dockerfile exists: $app"
    else
        check_fail "Frontend Dockerfile NOT found: $app"
    fi
done

echo ""
echo "3. Checking Network Connectivity..."
echo "================================"

# Check GitHub connectivity
if curl -s -o /dev/null -w "%{http_code}" https://github.com | grep -q "200\|301"; then
    check_pass "GitHub.com reachable"
else
    check_fail "Cannot reach GitHub.com"
fi

# Check GHCR connectivity
if curl -s -o /dev/null -w "%{http_code}" https://ghcr.io | grep -q "200\|301\|404"; then
    check_pass "GHCR (ghcr.io) reachable"
else
    check_fail "Cannot reach GHCR (ghcr.io)"
fi

# Check Dokploy connectivity
if curl -s -o /dev/null -w "%{http_code}" https://dk.bizoholic.com | grep -q "200\|301"; then
    check_pass "Dokploy (dk.bizoholic.com) reachable"
else
    check_fail "Cannot reach Dokploy (dk.bizoholic.com)"
fi

echo ""
echo "4. Testing Dokploy API..."
echo "================================"

# Test Dokploy API health (without API key)
DOKPLOY_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" https://dk.bizoholic.com/api/health 2>/dev/null || echo "000")

if [[ "$DOKPLOY_RESPONSE" =~ ^(200|401|403)$ ]]; then
    check_pass "Dokploy API endpoint responding (HTTP $DOKPLOY_RESPONSE)"
else
    check_warn "Dokploy API unexpected response: HTTP $DOKPLOY_RESPONSE"
fi

echo ""
echo "5. Checking Docker Build Requirements..."
echo "================================"

# Check if Docker is installed (optional, not needed for GitHub Actions)
if command -v docker &> /dev/null; then
    check_pass "Docker installed locally (version: $(docker --version | cut -d' ' -f3))"
else
    check_warn "Docker not installed locally (not required for GitHub Actions)"
fi

# Check for .dockerignore files
if [ -f "bizosaas/ai/services/bizosaas-brain/.dockerignore" ]; then
    check_pass "Brain Gateway .dockerignore exists (optimized builds)"
else
    check_warn "Brain Gateway .dockerignore missing (slower builds)"
fi

DOCKERIGNORE_COUNT=$(find bizosaas/frontend/apps -name ".dockerignore" | wc -l)
if [ "$DOCKERIGNORE_COUNT" -gt 0 ]; then
    check_pass "Frontend .dockerignore files found ($DOCKERIGNORE_COUNT apps)"
else
    check_warn "No frontend .dockerignore files (slower builds)"
fi

echo ""
echo "6. Checking Workflow Configuration..."
echo "================================"

# Check workflow_dispatch is enabled
if grep -q "workflow_dispatch" .github/workflows/deploy-staging.yml; then
    check_pass "Manual workflow trigger enabled (workflow_dispatch)"
else
    check_warn "Manual trigger NOT enabled (can only trigger via git push)"
fi

# Check if secrets are referenced
if grep -q "DOKPLOY_API_KEY" .github/workflows/deploy-staging.yml; then
    check_pass "DOKPLOY_API_KEY referenced in workflow"
else
    check_fail "DOKPLOY_API_KEY NOT found in workflow"
fi

if grep -q "GITHUB_TOKEN" .github/workflows/deploy-staging.yml; then
    check_pass "GITHUB_TOKEN referenced in workflow"
else
    check_fail "GITHUB_TOKEN NOT found in workflow"
fi

echo ""
echo "=================================================="
echo "Verification Summary"
echo "=================================================="
echo -e "${GREEN}Passed:${NC}   $PASSED"
echo -e "${YELLOW}Warnings:${NC} $WARNINGS"
echo -e "${RED}Failed:${NC}   $FAILED"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All critical checks passed!${NC}"
    echo ""
    echo "=================================================="
    echo "Next Steps:"
    echo "=================================================="
    echo "1. Add GitHub Secret:"
    echo "   https://github.com/Bizoholic-Digital/bizosaas-platform/settings/secrets/actions"
    echo ""
    echo "   Name: DOKPLOY_API_KEY"
    echo "   Value: bizoholicKRGZxqgQXBDBzumvvnMhiEZLmnetMTAWwTnFztwuGofadbHagGbJiiMZTqczBDKY"
    echo ""
    echo "2. Set Workflow Permissions:"
    echo "   https://github.com/Bizoholic-Digital/bizosaas-platform/settings/actions"
    echo "   Select: 'Read and write permissions'"
    echo ""
    echo "3. Trigger Build:"
    echo "   Option A: Empty commit"
    echo "   $ git commit --allow-empty -m 'chore: Trigger CI/CD deployment'"
    echo "   $ git push origin main"
    echo ""
    echo "   Option B: Manual trigger (if workflow_dispatch enabled)"
    echo "   Go to: https://github.com/Bizoholic-Digital/bizosaas-platform/actions"
    echo "   Click: 'Deploy to Staging' > 'Run workflow'"
    echo ""
    echo "4. Monitor Progress:"
    echo "   https://github.com/Bizoholic-Digital/bizosaas-platform/actions"
    echo ""
    exit 0
else
    echo -e "${RED}✗ Some checks failed. Please fix issues before deploying.${NC}"
    echo ""
    echo "See GITHUB_ACTIONS_SETUP_GUIDE.md for troubleshooting."
    exit 1
fi
