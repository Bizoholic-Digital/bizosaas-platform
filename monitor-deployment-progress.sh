#!/bin/bash

echo "=========================================="
echo "BizOSaaS Deployment Monitoring"
echo "Started: $(date)"
echo "=========================================="
echo ""

while true; do
    echo "=== Check $(date +%H:%M:%S) ==="

    # Count running staging containers
    BACKEND_COUNT=$(docker ps --filter "name=bizosaas-.*-staging" --format "{{.Names}}" | grep -E "brain|wagtail|django|business|coreldove|auth|temporal|ai-agents|amazon" | wc -l)
    FRONTEND_COUNT=$(docker ps --filter "name=bizosaas-.*-staging" --format "{{.Names}}" | grep -E "client-portal|bizoholic-frontend|coreldove-frontend|business-directory-frontend|thrillring|admin-dashboard" | wc -l)

    echo "Backend services running: $BACKEND_COUNT/9"
    echo "Frontend services running: $FRONTEND_COUNT/6"
    echo "Total: $((BACKEND_COUNT + FRONTEND_COUNT))/15"

    # List running services
    if [ $BACKEND_COUNT -gt 0 ] || [ $FRONTEND_COUNT -gt 0 ]; then
        echo ""
        echo "Running services:"
        docker ps --filter "name=bizosaas-.*-staging" --format "  - {{.Names}} ({{.Status}})"
    fi

    # Check if all services are running
    if [ $BACKEND_COUNT -eq 9 ] && [ $FRONTEND_COUNT -eq 6 ]; then
        echo ""
        echo "✓ All 15 services deployed successfully!"
        break
    fi

    echo ""
    echo "Waiting 30 seconds before next check..."
    sleep 30
done

echo ""
echo "=========================================="
echo "Deployment Complete: $(date)"
echo "=========================================="
