#!/bin/bash

# Complete PWA Setup Script for All Containers
# This script completes the PWA implementation for all BizOSaaS containers

echo "🚀 Completing PWA Setup for All BizOSaaS Containers"
echo "=================================================="

# Container list
CONTAINERS=("client-portal" "bizosaas-admin" "business-directory")
SOURCE_CONTAINER="bizoholic-frontend"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}📋 Setup Summary:${NC}"
echo "  Source Container: $SOURCE_CONTAINER"
echo "  Target Containers: ${CONTAINERS[*]}"
echo ""

# Function to check if directory exists and is writable
check_permissions() {
    local container=$1
    local public_dir="frontend/apps/$container/public"
    
    if [ ! -d "$public_dir" ]; then
        echo -e "${RED}❌ Directory not found: $public_dir${NC}"
        return 1
    fi
    
    if [ ! -w "$public_dir" ]; then
        echo -e "${RED}❌ No write permission: $public_dir${NC}"
        echo -e "${YELLOW}   Run: sudo chown -R \$USER:\$USER $public_dir${NC}"
        return 1
    fi
    
    return 0
}

# Function to copy PWA files
copy_pwa_files() {
    local container=$1
    local source_dir="frontend/apps/$SOURCE_CONTAINER"
    local target_dir="frontend/apps/$container"
    
    echo -e "${BLUE}📁 Setting up PWA files for $container...${NC}"
    
    # Create directories if they don't exist
    mkdir -p "$target_dir/components/mobile"
    mkdir -p "$target_dir/lib/pwa"
    mkdir -p "$target_dir/public/icons"
    
    # Copy public PWA files
    if check_permissions "$container"; then
        echo "  📋 Copying manifest.json..."
        cp "$source_dir/public/manifest.json" "$target_dir/public/" 2>/dev/null || echo -e "${RED}    ⚠️  Failed to copy manifest.json${NC}"
        
        echo "  ⚙️  Copying service worker..."
        cp "$source_dir/public/sw.js" "$target_dir/public/" 2>/dev/null || echo -e "${RED}    ⚠️  Failed to copy sw.js${NC}"
        
        echo "  📱 Copying offline page..."
        cp "$source_dir/public/offline.html" "$target_dir/public/" 2>/dev/null || echo -e "${RED}    ⚠️  Failed to copy offline.html${NC}"
        
        echo "  🎨 Copying app icons..."
        cp -r "$source_dir/public/icons" "$target_dir/public/" 2>/dev/null || echo -e "${RED}    ⚠️  Failed to copy icons${NC}"
    else
        echo -e "${RED}  ❌ Skipping public files due to permission issues${NC}"
    fi
    
    # Copy component files (these should be writable)
    echo "  🔧 Copying PWA Provider..."
    cp "$source_dir/components/PWAProvider.tsx" "$target_dir/components/" 2>/dev/null || echo -e "${YELLOW}    ⚠️  PWAProvider.tsx not copied${NC}"
    
    echo "  💾 Copying IndexedDB utilities..."
    cp -r "$source_dir/lib/pwa" "$target_dir/lib/" 2>/dev/null || echo -e "${YELLOW}    ⚠️  PWA lib not copied${NC}"
    
    echo "  📱 Copying mobile components..."
    cp -r "$source_dir/components/mobile" "$target_dir/components/" 2>/dev/null || echo -e "${YELLOW}    ⚠️  Mobile components not copied${NC}"
    
    echo -e "${GREEN}  ✅ PWA setup completed for $container${NC}"
    echo ""
}

# Function to update manifest for container-specific settings
update_manifest() {
    local container=$1
    local manifest_file="frontend/apps/$container/public/manifest.json"
    
    if [ -f "$manifest_file" ] && [ -w "$manifest_file" ]; then
        echo -e "${BLUE}🔧 Customizing manifest for $container...${NC}"
        
        # Get container port
        local port=""
        case $container in
            "client-portal") port="3006" ;;
            "bizosaas-admin") port="3009" ;;
            "business-directory") port="3010" ;;
        esac
        
        # Update manifest with container-specific details
        if [ -n "$port" ]; then
            # Use sed to update the start_url in the manifest
            sed -i "s|\"start_url\": \".*\"|\"start_url\": \"http://localhost:$port/\"|g" "$manifest_file"
            echo -e "${GREEN}  ✅ Updated start_url to port $port${NC}"
        fi
    else
        echo -e "${YELLOW}  ⚠️  Cannot customize manifest (file not writable)${NC}"
    fi
}

# Function to verify setup
verify_setup() {
    local container=$1
    local score=0
    local total=7
    
    echo -e "${BLUE}🔍 Verifying PWA setup for $container...${NC}"
    
    # Check files exist
    [ -f "frontend/apps/$container/public/manifest.json" ] && ((score++)) && echo -e "${GREEN}  ✅ Manifest.json${NC}" || echo -e "${RED}  ❌ Manifest.json${NC}"
    [ -f "frontend/apps/$container/public/sw.js" ] && ((score++)) && echo -e "${GREEN}  ✅ Service Worker${NC}" || echo -e "${RED}  ❌ Service Worker${NC}"
    [ -f "frontend/apps/$container/public/offline.html" ] && ((score++)) && echo -e "${GREEN}  ✅ Offline Page${NC}" || echo -e "${RED}  ❌ Offline Page${NC}"
    [ -d "frontend/apps/$container/public/icons" ] && ((score++)) && echo -e "${GREEN}  ✅ App Icons${NC}" || echo -e "${RED}  ❌ App Icons${NC}"
    [ -f "frontend/apps/$container/components/PWAProvider.tsx" ] && ((score++)) && echo -e "${GREEN}  ✅ PWA Provider${NC}" || echo -e "${RED}  ❌ PWA Provider${NC}"
    [ -d "frontend/apps/$container/lib/pwa" ] && ((score++)) && echo -e "${GREEN}  ✅ IndexedDB Utils${NC}" || echo -e "${RED}  ❌ IndexedDB Utils${NC}"
    [ -d "frontend/apps/$container/components/mobile" ] && ((score++)) && echo -e "${GREEN}  ✅ Mobile Components${NC}" || echo -e "${RED}  ❌ Mobile Components${NC}"
    
    local percentage=$((score * 100 / total))
    echo -e "${BLUE}  📊 PWA Setup Score: $score/$total ($percentage%)${NC}"
    echo ""
    
    return $score
}

# Main execution
echo -e "${BLUE}🔍 Checking source container...${NC}"
if [ ! -d "frontend/apps/$SOURCE_CONTAINER" ]; then
    echo -e "${RED}❌ Source container not found: $SOURCE_CONTAINER${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Source container found${NC}"
echo ""

# Setup PWA for each container
total_score=0
max_score=0

for container in "${CONTAINERS[@]}"; do
    if [ -d "frontend/apps/$container" ]; then
        copy_pwa_files "$container"
        update_manifest "$container"
        verify_setup "$container"
        score=$?
        total_score=$((total_score + score))
        max_score=$((max_score + 7))
    else
        echo -e "${RED}❌ Container not found: $container${NC}"
        echo ""
    fi
done

# Final summary
echo -e "${BLUE}📊 Final PWA Setup Summary${NC}"
echo "=================================="
overall_percentage=$((total_score * 100 / max_score))
echo -e "${BLUE}Overall Score: $total_score/$max_score ($overall_percentage%)${NC}"

if [ $overall_percentage -ge 90 ]; then
    echo -e "${GREEN}🎉 Excellent! PWA setup is nearly complete${NC}"
elif [ $overall_percentage -ge 70 ]; then
    echo -e "${YELLOW}⚠️  Good progress, but some issues need fixing${NC}"
else
    echo -e "${RED}❌ Significant issues found, manual intervention required${NC}"
fi

echo ""
echo -e "${BLUE}💡 Next Steps:${NC}"
echo "1. Fix any permission issues shown above"
echo "2. Run: node test-pwa.js"
echo "3. Check mobile testing guide: mobile-pwa-testing-guide.md"
echo ""

# Permission fix reminder
echo -e "${YELLOW}🔐 To fix public directory permissions:${NC}"
for container in "${CONTAINERS[@]}"; do
    echo "sudo chown -R \$USER:\$USER frontend/apps/$container/public/"
done

echo ""
echo -e "${GREEN}✅ PWA setup script completed!${NC}"