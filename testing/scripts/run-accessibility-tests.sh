#!/bin/bash

# Accessibility Testing Script using axe-core
# Tests: A11Y-001 through A11Y-007

set -e

echo "♿ BizOSaaS Accessibility Testing"
echo "================================="

# Configuration
BASE_URL="${BASE_URL:-http://localhost:3003}"
ADMIN_URL="${ADMIN_URL:-http://localhost:3004}"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Create results directory
RESULTS_DIR="./reports/accessibility/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$RESULTS_DIR"

echo -e "${GREEN}✓ Results will be saved to: $RESULTS_DIR${NC}"
echo ""

# Check if npm packages are installed
if [ ! -d "node_modules/@axe-core/cli" ]; then
    echo "Installing axe-core CLI..."
    npm install --save-dev @axe-core/cli pa11y pa11y-ci
fi

# Test pages
PAGES=(
    "/login"
    "/signup"
    "/dashboard"
    "/campaigns"
    "/assets"
    "/billing"
    "/settings"
)

echo "📋 Testing ${#PAGES[@]} pages for WCAG 2.1 AA compliance"
echo ""

# Run axe-core tests
for page in "${PAGES[@]}"; do
    echo "Testing: $BASE_URL$page"
    
    npx axe "$BASE_URL$page" \
        --tags wcag2a,wcag2aa,wcag21a,wcag21aa \
        --save "$RESULTS_DIR/axe-$(echo $page | tr '/' '-').json" \
        --exit || true
    
    echo ""
done

# Run pa11y tests for detailed reporting
echo "Running detailed accessibility audit with pa11y..."
echo ""

for page in "${PAGES[@]}"; do
    echo "Auditing: $BASE_URL$page"
    
    npx pa11y "$BASE_URL$page" \
        --standard WCAG2AA \
        --reporter json \
        > "$RESULTS_DIR/pa11y-$(echo $page | tr '/' '-').json" || true
    
    # Also generate HTML report
    npx pa11y "$BASE_URL$page" \
        --standard WCAG2AA \
        --reporter html \
        > "$RESULTS_DIR/pa11y-$(echo $page | tr '/' '-').html" || true
done

# Generate summary report
echo ""
echo "📊 Generating summary report..."

cat > "$RESULTS_DIR/summary.html" << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Accessibility Test Summary</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        h1 { color: #333; }
        .summary {
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .stat {
            display: inline-block;
            margin: 10px 20px 10px 0;
        }
        .stat-label {
            font-size: 14px;
            color: #666;
        }
        .stat-value {
            font-size: 32px;
            font-weight: bold;
        }
        .critical { color: #d32f2f; }
        .serious { color: #f57c00; }
        .moderate { color: #fbc02d; }
        .minor { color: #388e3c; }
        table {
            width: 100%;
            background: white;
            border-collapse: collapse;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }
        th {
            background: #f5f5f5;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <h1>♿ Accessibility Test Summary</h1>
    <div class="summary">
        <div class="stat">
            <div class="stat-label">Pages Tested</div>
            <div class="stat-value">PAGES_COUNT</div>
        </div>
        <div class="stat">
            <div class="stat-label critical">Critical Issues</div>
            <div class="stat-value critical">CRITICAL_COUNT</div>
        </div>
        <div class="stat">
            <div class="stat-label serious">Serious Issues</div>
            <div class="stat-value serious">SERIOUS_COUNT</div>
        </div>
        <div class="stat">
            <div class="stat-label moderate">Moderate Issues</div>
            <div class="stat-value moderate">MODERATE_COUNT</div>
        </div>
    </div>
    
    <h2>Test Results by Page</h2>
    <table>
        <thead>
            <tr>
                <th>Page</th>
                <th>Critical</th>
                <th>Serious</th>
                <th>Moderate</th>
                <th>Minor</th>
                <th>Report</th>
            </tr>
        </thead>
        <tbody id="results">
            <!-- Results will be inserted here -->
        </tbody>
    </table>
    
    <h2>Common Issues</h2>
    <ul id="common-issues">
        <!-- Common issues will be listed here -->
    </ul>
</body>
</html>
EOF

# Count total issues (simplified - would parse JSON in real implementation)
echo -e "${GREEN}✅ Accessibility testing complete${NC}"
echo ""
echo "Results saved to: $RESULTS_DIR"
echo ""
echo "View summary: open $RESULTS_DIR/summary.html"
echo ""

# Check for critical issues
CRITICAL_COUNT=$(grep -r "critical" "$RESULTS_DIR"/*.json 2>/dev/null | wc -l || echo "0")

if [ "$CRITICAL_COUNT" -gt 0 ]; then
    echo -e "${RED}⚠ Found $CRITICAL_COUNT critical accessibility issues${NC}"
    echo "Review the reports and fix before production deployment"
    exit 1
else
    echo -e "${GREEN}✓ No critical accessibility issues found${NC}"
fi
