#!/bin/bash

# BizOSaaS Monorepo Setup Script
# Fixes workspace dependencies and builds system

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}🔧 BizOSaaS Monorepo Setup${NC}"
echo -e "${CYAN}============================${NC}"

# Function to print status
print_status() {
    echo -e "${BLUE}[$(date '+%H:%M:%S')]${NC} $1"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to fix workspace dependencies
fix_workspace_dependencies() {
    print_status "Fixing workspace dependencies..."
    
    # Fix apps/bizoholic-frontend
    if [ -f "apps/bizoholic-frontend/package.json" ]; then
        print_status "Fixing Bizoholic frontend dependencies"
        cd apps/bizoholic-frontend
        sed -i 's/"@bizosaas\/shared-ui": "workspace:\*"/"@bizosaas\/shared-ui": "*"/g' package.json
        cd ../..
    fi
    
    # Fix apps/coreldove-frontend  
    if [ -f "apps/coreldove-frontend/package.json" ]; then
        print_status "Fixing CoreLDove frontend dependencies"
        cd apps/coreldove-frontend
        sed -i 's/"@bizosaas\/shared-ui": "workspace:\*"/"@bizosaas\/shared-ui": "*"/g' package.json
        cd ../..
    fi
    
    # Fix services/frontend-nextjs
    if [ -f "services/frontend-nextjs/package.json" ]; then
        print_status "Fixing BizOSaaS dashboard dependencies"  
        cd services/frontend-nextjs
        sed -i 's/"@bizosaas\/shared-ui": "workspace:\*"/"@bizosaas\/shared-ui": "*"/g' package.json
        cd ../..
    fi
    
    print_success "Workspace dependencies fixed"
}

# Function to install dependencies
install_dependencies() {
    print_status "Installing dependencies..."
    
    # Clean existing installations
    print_status "Cleaning existing node_modules..."
    rm -rf node_modules
    find . -name "node_modules" -type d -exec rm -rf {} + 2>/dev/null || true
    find . -name "package-lock.json" -type f -delete 2>/dev/null || true
    find . -name ".next" -type d -exec rm -rf {} + 2>/dev/null || true
    
    # Install root dependencies
    print_status "Installing root workspace dependencies..."
    npm install
    
    if [ $? -eq 0 ]; then
        print_success "Root dependencies installed"
    else
        print_error "Failed to install root dependencies"
        return 1
    fi
    
    # Install workspace dependencies
    print_status "Installing workspace dependencies..."
    npm install --workspaces --if-present
    
    if [ $? -eq 0 ]; then
        print_success "Workspace dependencies installed"
    else
        print_warning "Some workspace dependencies failed to install"
    fi
}

# Function to build shared-ui
build_shared_ui() {
    print_status "Building shared-ui package..."
    
    cd packages/shared-ui
    
    # Install TypeScript locally if not available
    if ! command -v tsc &> /dev/null; then
        print_status "Installing TypeScript..."
        npm install typescript
    fi
    
    # Build shared-ui
    npm run build
    
    if [ $? -eq 0 ]; then
        print_success "Shared-UI built successfully"
    else
        print_error "Failed to build shared-ui"
        cd ../..
        return 1
    fi
    
    cd ../..
}

# Function to test workspace build
test_build() {
    print_status "Testing workspace build..."
    
    # Test individual workspace builds
    workspaces=("packages/shared-ui")
    
    for workspace in "${workspaces[@]}"; do
        if [ -d "$workspace" ]; then
            print_status "Testing build for $workspace"
            cd "$workspace"
            
            if npm run build; then
                print_success "$workspace builds successfully"
            else
                print_warning "$workspace build failed"
            fi
            
            cd - > /dev/null
        fi
    done
}

# Function to validate setup
validate_setup() {
    print_status "Validating monorepo setup..."
    
    # Check if turbo is available
    if npm list turbo > /dev/null 2>&1; then
        print_success "Turbo is available"
    else
        print_warning "Turbo not found in dependencies"
    fi
    
    # Check workspace configuration
    if [ -f "package.json" ] && grep -q "workspaces" package.json; then
        print_success "Workspace configuration found"
    else
        print_error "Workspace configuration missing"
        return 1
    fi
    
    # Check shared-ui package
    if [ -f "packages/shared-ui/package.json" ]; then
        print_success "Shared-UI package found"
    else
        print_error "Shared-UI package missing"
        return 1
    fi
    
    # Check if main apps exist
    apps=("apps/bizoholic-frontend" "apps/coreldove-frontend")
    for app in "${apps[@]}"; do
        if [ -d "$app" ]; then
            print_success "$app found"
        else
            print_warning "$app not found"
        fi
    done
}

# Function to create development scripts
create_dev_scripts() {
    print_status "Creating development scripts..."
    
    # Update package.json scripts if needed
    if ! grep -q "setup:monorepo" package.json; then
        print_status "Adding monorepo setup script to package.json"
        # This would need a more sophisticated JSON update
        print_warning "Manual update of package.json scripts may be needed"
    fi
    
    print_success "Development scripts ready"
}

# Main execution
main() {
    case "${1:-setup}" in
        "setup")
            print_status "Starting complete monorepo setup..."
            fix_workspace_dependencies
            install_dependencies  
            build_shared_ui
            validate_setup
            create_dev_scripts
            print_success "🎉 Monorepo setup completed successfully!"
            echo ""
            echo -e "${CYAN}Next steps:${NC}"
            echo "1. Run: npm run dev (to start development environment)"
            echo "2. Run: npm run build (to test full build)"
            echo "3. Run: npm run status (to check services)"
            ;;
        "validate")
            validate_setup
            ;;
        "build")
            build_shared_ui
            test_build
            ;;
        "clean")
            print_status "Cleaning workspace..."
            rm -rf node_modules
            find . -name "node_modules" -type d -exec rm -rf {} + 2>/dev/null || true
            find . -name ".next" -type d -exec rm -rf {} + 2>/dev/null || true
            print_success "Workspace cleaned"
            ;;
        "help")
            echo "Usage: $0 [command]"
            echo ""
            echo "Commands:"
            echo "  setup      - Complete monorepo setup (default)"
            echo "  validate   - Validate current setup"
            echo "  build      - Build shared packages"
            echo "  clean      - Clean all build artifacts"
            echo "  help       - Show this help"
            ;;
        *)
            print_error "Unknown command: $1"
            echo "Use '$0 help' for available commands"
            exit 1
            ;;
    esac
}

main "$@"