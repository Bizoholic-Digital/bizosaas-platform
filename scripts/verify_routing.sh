#!/bin/bash

# BizOSaaS Platform - Routing Verification Matrix
# Usage: ./verify_routing.sh [ENVIRONMENT]

ENV=${1:-"production"}
DOMAINS=(
    "bizoholic.com"
    "www.bizoholic.com"
    "app.bizoholic.net"
    "admin.bizoholic.net"
    "api.bizoholic.net"
    "temporal.bizoholic.net"
    "cms.bizoholic.net"
    "directory.bizoholic.net"
)

echo "--- BizOSaaS Routing Verification Matrix ($ENV) ---"
echo "Timestamp: $(date)"
echo ""

for domain in "${DOMAINS[@]}"; do
    echo -n "Checking $domain... "
    RESPONSE=$(curl -s -I "https://$domain" | head -n 1)
    if [[ $RESPONSE == *"200"* ]] || [[ $RESPONSE == *"302"* ]] || [[ $RESPONSE == *"301"* ]] || [[ $RESPONSE == *"401"* ]]; then
        echo -e "\e[32m[OK]\e[0m $RESPONSE"
    else
        echo -e "\e[31m[FAIL]\e[0m $RESPONSE"
    fi
done

echo ""
echo "Verification Complete."
