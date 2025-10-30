#!/bin/bash

# BizOSaaS - Publish All Shared Packages to GitHub Packages
# Date: October 30, 2025

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  BizOSaaS Package Publishing to GitHub Packages${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo

# Check if GITHUB_TOKEN is set
if [ -z "$GITHUB_TOKEN" ]; then
  echo -e "${RED}❌ Error: GITHUB_TOKEN environment variable is not set${NC}"
  echo
  echo "To set it up:"
  echo "  1. Create a GitHub Personal Access Token with 'write:packages' and 'repo' scopes"
  echo "  2. Export the token: export GITHUB_TOKEN='ghp_your_token_here'"
  echo "  3. Or see: GITHUB_TOKEN_SETUP.md for detailed instructions"
  echo
  exit 1
fi

echo -e "${GREEN}✓ GitHub token found${NC}"
echo

# Base directory
BASE_DIR="/home/alagiri/projects/bizosaas-platform"
cd "$BASE_DIR"

# Packages to publish
PACKAGES=(
  "auth"
  "ui-components"
  "api-client"
  "hooks"
  "utils"
  "animated-components"
)

# Track success/failure
SUCCESS_COUNT=0
FAIL_COUNT=0
FAILED_PACKAGES=()

# Function to create .npmrc
create_npmrc() {
  local package_dir=$1
  echo "@bizosaas:registry=https://npm.pkg.github.com" > "$package_dir/.npmrc"
  echo "//npm.pkg.github.com/:_authToken=\${GITHUB_TOKEN}" >> "$package_dir/.npmrc"
}

# Function to publish a package
publish_package() {
  local package_name=$1
  local package_dir="$BASE_DIR/packages/$package_name"

  echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo -e "${BLUE}📦 Processing: @bizosaas/$package_name${NC}"
  echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

  # Check if package directory exists
  if [ ! -d "$package_dir" ]; then
    echo -e "${RED}❌ Directory not found: $package_dir${NC}"
    ((FAIL_COUNT++))
    FAILED_PACKAGES+=("$package_name (directory not found)")
    return 1
  fi

  cd "$package_dir"

  # Create .npmrc
  echo -e "${BLUE}  → Creating .npmrc...${NC}"
  create_npmrc "$package_dir"

  # Install dependencies
  echo -e "${BLUE}  → Installing dependencies...${NC}"
  if ! npm install --legacy-peer-deps > /dev/null 2>&1; then
    echo -e "${RED}  ❌ Failed to install dependencies${NC}"
    rm -f .npmrc
    ((FAIL_COUNT++))
    FAILED_PACKAGES+=("$package_name (dependency install failed)")
    return 1
  fi

  # Build package
  echo -e "${BLUE}  → Building package...${NC}"
  if ! npm run build; then
    echo -e "${RED}  ❌ Build failed${NC}"
    rm -f .npmrc
    ((FAIL_COUNT++))
    FAILED_PACKAGES+=("$package_name (build failed)")
    return 1
  fi

  # Publish package
  echo -e "${BLUE}  → Publishing to GitHub Packages...${NC}"
  if npm publish 2>&1 | tee /tmp/npm-publish-output.txt; then
    echo -e "${GREEN}  ✅ Successfully published @bizosaas/$package_name${NC}"
    ((SUCCESS_COUNT++))
  else
    # Check if it's a version conflict (already published)
    if grep -q "cannot publish over the previously published versions" /tmp/npm-publish-output.txt; then
      echo -e "${YELLOW}  ⚠️  Version already published. Run 'npm version patch' to bump version.${NC}"
      ((SUCCESS_COUNT++))  # Count as success since package exists
    else
      echo -e "${RED}  ❌ Publish failed${NC}"
      cat /tmp/npm-publish-output.txt
      ((FAIL_COUNT++))
      FAILED_PACKAGES+=("$package_name (publish failed)")
    fi
  fi

  # Clean up .npmrc (security best practice)
  rm -f .npmrc
  rm -f /tmp/npm-publish-output.txt

  echo
}

# Publish all packages
for package in "${PACKAGES[@]}"; do
  publish_package "$package"
done

# Summary
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Publishing Summary${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo
echo -e "Total packages: ${#PACKAGES[@]}"
echo -e "${GREEN}Successful: $SUCCESS_COUNT${NC}"
echo -e "${RED}Failed: $FAIL_COUNT${NC}"
echo

if [ $FAIL_COUNT -gt 0 ]; then
  echo -e "${RED}Failed packages:${NC}"
  for failed in "${FAILED_PACKAGES[@]}"; do
    echo -e "${RED}  ❌ $failed${NC}"
  done
  echo
  exit 1
else
  echo -e "${GREEN}🎉 All packages published successfully!${NC}"
  echo
  echo -e "${BLUE}Next steps:${NC}"
  echo "  1. Update service package.json files to use published versions"
  echo "  2. Test Docker builds with published packages"
  echo "  3. Deploy microservices independently"
  echo
  exit 0
fi
