#!/bin/bash

# BizOSaaS Platform UX Validation Runner
# Quick execution script for immediate UX testing

echo "🚀 BizOSaaS Platform UX Validation Framework"
echo "============================================="
echo ""

# Check if Node.js is available
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed."
    echo "Please install Node.js from https://nodejs.org/"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "ux-validation-checklist.js" ]; then
    echo "❌ UX validation scripts not found in current directory"
    echo "Please run this script from the bizosaas-platform directory"
    exit 1
fi

echo "📦 Checking dependencies..."

# Install dependencies if package.json exists
if [ -f "package.json" ]; then
    echo "Installing required packages..."
    npm install --silent
    if [ $? -ne 0 ]; then
        echo "⚠️  Some dependencies may be missing, continuing with basic validation..."
    fi
else
    echo "⚠️  package.json not found, running basic validation..."
fi

echo ""
echo "🎯 Running Quick UX Validation..."
echo "=================================="

# Run the quick validation
node ux-validation-checklist.js

# Check if the validation was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Quick validation completed successfully!"
    echo ""
    
    # Check if comprehensive framework is available
    if [ -f "ux-testing-framework.js" ]; then
        echo "🔍 Comprehensive UX Testing Framework Available"
        echo "To run full testing suite:"
        echo "  node ux-testing-framework.js"
        echo ""
    fi
    
    # Check if reports were generated
    if [ -f "quick-ux-validation-report.json" ]; then
        echo "📊 Reports Generated:"
        echo "  - quick-ux-validation-report.json (detailed results)"
        echo "  - ux-validation-summary.md (executive summary)"
        echo "  - ux-research-methodology.md (research framework)"
        echo ""
    fi
    
    echo "📋 Next Steps:"
    echo "1. Review the generated reports"
    echo "2. Address any critical issues identified"
    echo "3. Run comprehensive testing with: node ux-testing-framework.js"
    echo "4. Implement recommended UX improvements"
    echo ""
    
    echo "🌐 Platform URLs for Manual Testing:"
    echo "  - Client Portal: http://localhost:3000"
    echo "  - Bizoholic Frontend: http://localhost:3001"
    echo "  - CoreLDove Frontend: http://localhost:3002"
    echo "  - Business Directory: http://localhost:3004"
    echo "  - BizOSaaS Admin: http://localhost:3009"
    
else
    echo ""
    echo "❌ Quick validation encountered errors"
    echo "Please check the output above for details"
    exit 1
fi

echo ""
echo "🎉 UX Validation Framework Setup Complete!"