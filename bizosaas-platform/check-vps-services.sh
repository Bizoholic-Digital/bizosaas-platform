#!/bin/bash

# Check what's currently running on VPS
# VPS: 194.238.16.237
# This script is READ-ONLY - it won't delete anything

VPS_HOST="root@194.238.16.237"
VPS_PASSWORD="&k3civYG5Q6YPb"

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  BizOSaaS VPS - Current Services Inventory                 ║"
echo "║  READ-ONLY CHECK - No deletions                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

run_ssh() {
    sshpass -p "$VPS_PASSWORD" ssh -o StrictHostKeyChecking=no "$VPS_HOST" "$1"
}

echo "📊 ALL RUNNING CONTAINERS:"
echo "════════════════════════════════════════════════════════════"
run_ssh "docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'"
echo ""

echo "📊 DOCKER IMAGES ON VPS:"
echo "════════════════════════════════════════════════════════════"
run_ssh "docker images --format 'table {{.Repository}}\t{{.Tag}}\t{{.Size}}' | head -50"
echo ""

echo "📊 DOCKER VOLUMES:"
echo "════════════════════════════════════════════════════════════"
run_ssh "docker volume ls"
echo ""

echo "📊 DOCKER NETWORKS:"
echo "════════════════════════════════════════════════════════════"
run_ssh "docker network ls"
echo ""

echo "📊 DISK USAGE:"
echo "════════════════════════════════════════════════════════════"
run_ssh "df -h | grep -E 'Filesystem|/dev/sda|/dev/vda'"
echo ""

echo "📊 DOCKER DISK USAGE:"
echo "════════════════════════════════════════════════════════════"
run_ssh "docker system df"
echo ""

echo "✓ Inventory complete - No changes made"
