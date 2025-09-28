#!/bin/bash

# Setup Lens Desktop for K3s Cluster Connection
# This script will install Lens Desktop and configure it to connect to your K3s cluster

echo "=== Setting up Lens Desktop for K3s Cluster ==="

# Check if Lens Desktop is already installed
if command -v lens &> /dev/null; then
    echo "✅ Lens Desktop is already installed"
else
    echo "📥 Installing Lens Desktop..."
    
    # Download and install Lens Desktop AppImage
    cd /tmp
    wget https://api.k8slens.dev/binaries/Lens-2023.12.081355-latest.x86_64.AppImage
    chmod +x Lens-*.AppImage
    
    # Move to user applications
    mkdir -p ~/Applications
    mv Lens-*.AppImage ~/Applications/lens-desktop
    
    # Create desktop entry
    cat > ~/.local/share/applications/lens-desktop.desktop << EOF
[Desktop Entry]
Name=Lens Desktop
Exec=/home/alagiri/Applications/lens-desktop
Icon=/home/alagiri/Applications/lens-desktop
Type=Application
Categories=Development;
EOF
    
    echo "✅ Lens Desktop installed to ~/Applications/lens-desktop"
fi

# Check kubeconfig
echo ""
echo "🔍 Checking Kubernetes configuration..."
echo "Current context: $(kubectl config current-context)"
echo "Server: $(kubectl config view --minify -o jsonpath='{.clusters[0].cluster.server}')"

# Verify cluster connectivity
echo ""
echo "🔗 Testing cluster connectivity..."
if kubectl get nodes &> /dev/null; then
    echo "✅ kubectl can connect to cluster"
    echo "Nodes:"
    kubectl get nodes
    
    echo ""
    echo "📊 Available namespaces:"
    kubectl get namespaces
    
    echo ""
    echo "🏗️  BizoSaaS services in bizosaas-dev namespace:"
    kubectl get pods -n bizosaas-dev 2>/dev/null || echo "❌ Error accessing bizosaas-dev namespace - this may be a TLS issue"
    
else
    echo "❌ kubectl cannot connect to cluster"
    exit 1
fi

# Display kubeconfig info for Lens
echo ""
echo "📋 Lens Desktop Configuration Info:"
echo "=================================="
echo "Kubeconfig file: ~/.kube/config"
echo "Context name: k3s-local"
echo "Cluster name: k3s-local"
echo "Server URL: https://127.0.0.1:6443"

echo ""
echo "🎯 Instructions for Lens Desktop:"
echo "1. Launch Lens Desktop: ~/Applications/lens-desktop"
echo "2. On first launch, Lens should automatically detect your kubeconfig"
echo "3. Look for 'k3s-local' cluster in the catalog"
echo "4. Click on the cluster to connect"
echo "5. Navigate to different namespaces using the namespace selector"
echo "6. You should see the following namespaces:"
echo "   - bizosaas-dev (BizoSaaS services)"
echo "   - apps-platform"
echo "   - claude-monitoring"
echo "   - wordpress-namespace"

echo ""
echo "🔧 If Lens doesn't detect the cluster automatically:"
echo "1. Click '+ Add Cluster' in Lens"
echo "2. Select 'Add from kubeconfig'"
echo "3. Point to: ~/.kube/config"
echo "4. Select context: k3s-local"

echo ""
echo "✨ Setup complete! You can now launch Lens Desktop and connect to your K3s cluster."