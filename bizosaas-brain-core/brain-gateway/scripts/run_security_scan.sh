#!/bin/bash

# BizOSaaS Security Scan Script (OWASP ZAP)
# This script runs a baseline scan against the Brain Gateway API.

TARGET_URL=${1:-"http://localhost:8000"}
REPORT_DIR="./reports/security"

mkdir -p $REPORT_DIR

echo "Starting OWASP ZAP Baseline Scan on $TARGET_URL..."

docker run --rm -v $(pwd)/$REPORT_DIR:/zap/wrk/:rw -t ghcr.io/zaproxy/zaproxy:stable zap-api-scan.py \
    -t $TARGET_URL/openapi.json \
    -f openapi \
    -r zap_report.html

echo "Scan complete. Report available in $REPORT_DIR/zap_report.html"
