#!/bin/bash
# Quick reload images to VPS after cleanup
set -e

VPS_IP="194.238.16.237"
VPS_USER="root"
VPS_PASSWORD="&k3civYG5Q6YPb"

echo "🔄 Quick Image Reload to VPS"
echo "========================================="
echo ""

# Check if images still exist locally
if [ ! -d "./staging-deploy/backend" ] || [ ! -d "./staging-deploy/frontend" ]; then
    echo "❌ Local images not found. Need to rebuild."
    exit 1
fi

echo "📊 Local images found:"
ls -lh ./staging-deploy/backend/*.tar.gz 2>/dev/null | wc -l | xargs echo "   Backend images:"
ls -lh ./staging-deploy/frontend/*.tar.gz 2>/dev/null | wc -l | xargs echo "   Frontend images:"
echo ""

# Transfer and load backend images
echo "1️⃣ Transferring and loading backend images..."
sshpass -p "$VPS_PASSWORD" ssh -o StrictHostKeyChecking=no $VPS_USER@$VPS_IP "mkdir -p /tmp/bizosaas-reload"

for img in ./staging-deploy/backend/*.tar.gz; do
    imgname=$(basename "$img")
    echo "   → $imgname"
    sshpass -p "$VPS_PASSWORD" scp -o StrictHostKeyChecking=no "$img" $VPS_USER@$VPS_IP:/tmp/bizosaas-reload/
    sshpass -p "$VPS_PASSWORD" ssh -o StrictHostKeyChecking=no $VPS_USER@$VPS_IP "gunzip -c /tmp/bizosaas-reload/$imgname | docker load && rm /tmp/bizosaas-reload/$imgname"
done

echo "   ✅ Backend images loaded"
echo ""

# Transfer and load frontend images
echo "2️⃣ Transferring and loading frontend images..."
for img in ./staging-deploy/frontend/*.tar.gz; do
    imgname=$(basename "$img")
    echo "   → $imgname"
    sshpass -p "$VPS_PASSWORD" scp -o StrictHostKeyChecking=no "$img" $VPS_USER@$VPS_IP:/tmp/bizosaas-reload/
    sshpass -p "$VPS_PASSWORD" ssh -o StrictHostKeyChecking=no $VPS_USER@$VPS_IP "gunzip -c /tmp/bizosaas-reload/$imgname | docker load && rm /tmp/bizosaas-reload/$imgname"
done

echo "   ✅ Frontend images loaded"
echo ""

# Cleanup and verify
echo "3️⃣ Verifying images..."
sshpass -p "$VPS_PASSWORD" ssh -o StrictHostKeyChecking=no $VPS_USER@$VPS_IP "rm -rf /tmp/bizosaas-reload && docker images | grep -E 'bizosaas|bizoholic' | wc -l" | xargs echo "   Total images loaded:"
echo ""

echo "✅ Image reload complete!"
echo "   Ready for Dokploy deployment"
