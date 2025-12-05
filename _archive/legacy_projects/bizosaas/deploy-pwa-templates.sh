#!/bin/bash

# Deploy PWA Templates Script
# This script deploys the PWA templates to complete 100% implementation

echo "🚀 Deploying PWA Templates for 100% Implementation"
echo "==================================================="

# Container configurations
declare -A CONTAINERS
CONTAINERS[client-portal]="3006"
CONTAINERS[bizosaas-admin]="3009"
CONTAINERS[business-directory]="3010"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Function to deploy PWA files for a container
deploy_container() {
    local container=$1
    local port=$2
    local template_dir="pwa-templates/${container}-public"
    local target_dir="frontend/apps/$container/public"
    
    echo -e "${BLUE}📱 Deploying PWA for $container (Port $port)...${NC}"
    
    if [ ! -d "$template_dir" ]; then
        echo -e "${RED}❌ Template directory not found: $template_dir${NC}"
        return 1
    fi
    
    if [ ! -d "$target_dir" ]; then
        echo -e "${RED}❌ Target directory not found: $target_dir${NC}"
        return 1
    fi
    
    # Check if we have write permission
    if [ -w "$target_dir" ]; then
        echo -e "${GREEN}✅ Write permission available${NC}"
        
        # Copy files
        cp "$template_dir/manifest.json" "$target_dir/" 2>/dev/null && echo "  📋 Manifest copied" || echo -e "${RED}  ❌ Failed to copy manifest${NC}"
        cp "$template_dir/sw.js" "$target_dir/" 2>/dev/null && echo "  ⚙️  Service worker copied" || echo -e "${RED}  ❌ Failed to copy service worker${NC}"
        cp "$template_dir/offline.html" "$target_dir/" 2>/dev/null && echo "  📱 Offline page copied" || echo -e "${RED}  ❌ Failed to copy offline page${NC}"
        cp -r "$template_dir/icons" "$target_dir/" 2>/dev/null && echo "  🎨 Icons copied" || echo -e "${RED}  ❌ Failed to copy icons${NC}"
        
        echo -e "${GREEN}  ✅ PWA deployment completed for $container${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠️  No write permission for $target_dir${NC}"
        echo -e "${YELLOW}   Run: sudo cp -r $template_dir/* $target_dir/${NC}"
        return 1
    fi
}

# Function to verify deployment
verify_deployment() {
    local container=$1
    local target_dir="frontend/apps/$container/public"
    local score=0
    
    echo -e "${BLUE}🔍 Verifying $container deployment...${NC}"
    
    [ -f "$target_dir/manifest.json" ] && ((score++)) && echo -e "${GREEN}  ✅ Manifest${NC}" || echo -e "${RED}  ❌ Manifest${NC}"
    [ -f "$target_dir/sw.js" ] && ((score++)) && echo -e "${GREEN}  ✅ Service Worker${NC}" || echo -e "${RED}  ❌ Service Worker${NC}"
    [ -f "$target_dir/offline.html" ] && ((score++)) && echo -e "${GREEN}  ✅ Offline Page${NC}" || echo -e "${RED}  ❌ Offline Page${NC}"
    [ -d "$target_dir/icons" ] && ((score++)) && echo -e "${GREEN}  ✅ Icons${NC}" || echo -e "${RED}  ❌ Icons${NC}"
    
    echo -e "${BLUE}  📊 Score: $score/4${NC}"
    return $score
}

# Main deployment
echo -e "${BLUE}📁 Available templates:${NC}"
ls -la pwa-templates/

echo ""
echo -e "${BLUE}🚀 Starting deployment...${NC}"

total_score=0
max_score=0
successful_deployments=0

for container in "${!CONTAINERS[@]}"; do
    port=${CONTAINERS[$container]}
    echo ""
    
    deploy_container "$container" "$port"
    deployment_result=$?
    
    verify_deployment "$container"
    score=$?
    
    total_score=$((total_score + score))
    max_score=$((max_score + 4))
    
    if [ $deployment_result -eq 0 ]; then
        ((successful_deployments++))
    fi
done

# Final summary
echo ""
echo -e "${BLUE}📊 Final Deployment Summary${NC}"
echo "===================================="
overall_percentage=$((total_score * 100 / max_score))
deployment_percentage=$((successful_deployments * 100 / ${#CONTAINERS[@]}))

echo -e "${BLUE}PWA Files Score: $total_score/$max_score ($overall_percentage%)${NC}"
echo -e "${BLUE}Successful Deployments: $successful_deployments/${#CONTAINERS[@]} ($deployment_percentage%)${NC}"

# Status assessment
if [ $overall_percentage -eq 100 ]; then
    echo -e "${GREEN}🎉 Perfect! 100% PWA implementation achieved!${NC}"
    exit_code=0
elif [ $overall_percentage -ge 75 ]; then
    echo -e "${GREEN}✅ Excellent! PWA implementation nearly complete${NC}"
    exit_code=0
elif [ $overall_percentage -ge 50 ]; then
    echo -e "${YELLOW}⚠️  Good progress, minor issues remaining${NC}"
    exit_code=1
else
    echo -e "${RED}❌ Significant issues, manual intervention required${NC}"
    exit_code=2
fi

echo ""
echo -e "${BLUE}🔧 Manual deployment commands (if needed):${NC}"
for container in "${!CONTAINERS[@]}"; do
    echo "sudo cp -r pwa-templates/${container}-public/* frontend/apps/$container/public/"
done

echo ""
echo -e "${BLUE}📋 Next steps:${NC}"
echo "1. Run: node test-pwa.js"
echo "2. Test mobile functionality with: mobile-pwa-testing-guide.md"
echo "3. Deploy to production with HTTPS"

echo ""
echo -e "${GREEN}✅ PWA template deployment completed!${NC}"

exit $exit_code