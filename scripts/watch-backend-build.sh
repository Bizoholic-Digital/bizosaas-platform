#!/bin/bash
while true; do
  clear
  echo "============================================"
  echo "Backend Build Progress - $(date +%H:%M:%S)"
  echo "============================================"
  echo ""
  docker ps --format "table {{.Names}}\t{{.Status}}" | grep -E "(brain|wagtail|django|business|coreldove|auth|temporal-integration|ai-agents|amazon)"
  echo ""
  running=$(docker ps --format "{{.Names}}" | grep -E "(brain|wagtail|django|business|coreldove|auth|temporal-integration|ai-agents|amazon)" | wc -l)
  echo "Running: $running/9"
  echo ""
  echo "Checking again in 30 seconds..."
  sleep 30
done
