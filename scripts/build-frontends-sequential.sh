#!/bin/bash
set -e

echo "🚀 Starting Sequential Frontend Build Process..."
echo "⚠️  This prevents WSL2/Server freezes by building one app at a time."

# Function to build a service
build_service() {
    local name=$1
    local path=$2
    local image_name=$3
    
    echo "----------------------------------------------------------------"
    echo "📦 Building $name..."
    echo "📂 Path: $path"
    
    if [ ! -d "$path" ]; then
        echo "❌ Error: Directory $path not found!"
        return 1
    fi
    
    cd "$path"
    
    # Build Docker image
    docker build -t "$image_name" .
    
    if [ $? -eq 0 ]; then
        echo "✅ $name built successfully!"
    else
        echo "❌ $name build failed!"
        exit 1
    fi
    
    # Prune dangling images to save space
    echo "🧹 Cleaning up intermediate images..."
    docker image prune -f
    
    cd - > /dev/null
}

# 1. Build Shared Packages (Implicitly used by frontends, but good to verify)
# Note: In Docker builds, packages are usually copied or installed. 
# If we had a base image for packages, we'd build it here.

# 2. Build Bizoholic Frontend
build_service "Bizoholic Frontend" "brands/bizoholic/frontend" "bizosaas/bizoholic-frontend:latest"

# 3. Build Client Portal
build_service "Client Portal" "portals/client-portal" "bizosaas/client-portal:latest"

# 4. Build CoreLDove Frontend
build_service "CoreLDove Frontend" "brands/coreldove/frontend" "bizosaas/coreldove-frontend:latest"

# 5. Build ThrillRing Frontend
build_service "ThrillRing Frontend" "brands/thrillring/frontend" "bizosaas/thrillring-frontend:latest"

# 6. Build Admin Dashboard
build_service "Admin Dashboard" "portals/admin-portal" "bizosaas/admin-dashboard:latest"

echo "----------------------------------------------------------------"
echo "🎉 All frontends built successfully!"
