#!/usr/bin/env node

const axios = require('axios');
const cheerio = require('cheerio');

const BASE_URL = 'http://localhost:3000';

// All routes to test based on the found page components
const ROUTES = [
  { path: '/', name: 'Dashboard Home' },
  { path: '/analytics', name: 'Analytics Dashboard' },
  { path: '/chat', name: 'AI Assistant Chat' },
  { path: '/content', name: 'Content Management Dashboard' },
  { path: '/content/blog', name: 'Content Blog Management' },
  { path: '/content/forms', name: 'Content Forms Management' },
  { path: '/content/media', name: 'Content Media Management' },
  { path: '/content/pages', name: 'Content Pages Management' },
  { path: '/crm', name: 'CRM Dashboard' },
  { path: '/crm/campaigns', name: 'CRM Campaigns' },
  { path: '/crm/contacts', name: 'CRM Contacts' },
  { path: '/crm/reports', name: 'CRM Reports' },
  { path: '/directory', name: 'Business Directory' },
  { path: '/ecommerce', name: 'E-commerce Dashboard' },
  { path: '/leads', name: 'Lead Management' },
  { path: '/login', name: 'Login Page' },
  { path: '/orders', name: 'Order Management' },
  { path: '/review-management', name: 'Review Management' },
  { path: '/settings', name: 'Settings' },
  { path: '/test', name: 'Test Page' }
];

async function testRoute(route, timeout = 10000) {
  const result = {
    path: route.path,
    name: route.name,
    status: 'unknown',
    statusCode: null,
    error: null,
    loadTime: null,
    hasLoadingState: false,
    hasErrorContent: false,
    title: null,
    consoleErrors: [],
    hydrationIssues: [],
    responseSize: 0
  };

  const startTime = Date.now();
  
  try {
    const response = await axios.get(`${BASE_URL}${route.path}`, {
      timeout,
      headers: {
        'User-Agent': 'BizOSaaS-Test-Agent',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
      }
    });
    
    result.loadTime = Date.now() - startTime;
    result.statusCode = response.status;
    result.responseSize = response.data.length;
    
    if (response.status === 200) {
      const $ = cheerio.load(response.data);
      
      // Extract title
      result.title = $('title').text() || 'No title';
      
      // Check for loading states
      const loadingElements = $('.animate-pulse, .loading, [data-loading="true"]');
      result.hasLoadingState = loadingElements.length > 0;
      
      // Check for error content
      const errorElements = $('.error, .alert-error, [data-error="true"], .text-red');
      result.hasErrorContent = errorElements.length > 0;
      
      // Check for hydration mismatches by looking for common patterns
      const hydrationPatterns = [
        'suppressHydrationWarning',
        'hydration',
        'mismatch'
      ];
      
      hydrationPatterns.forEach(pattern => {
        if (response.data.includes(pattern)) {
          result.hydrationIssues.push(`Potential hydration issue: ${pattern} found in HTML`);
        }
      });
      
      // Check for console error patterns in the HTML
      const consoleErrorPatterns = [
        'console.error',
        'console.warn',
        'Error:',
        'TypeError:',
        'ReferenceError:'
      ];
      
      consoleErrorPatterns.forEach(pattern => {
        if (response.data.includes(pattern)) {
          result.consoleErrors.push(`Potential console issue: ${pattern} pattern found`);
        }
      });
      
      result.status = 'success';
      
      // Additional analysis based on content
      if (result.hasLoadingState && result.loadTime > 5000) {
        result.status = 'timeout';
        result.error = 'Page shows loading state and took too long to load';
      }
      
    } else {
      result.status = 'error';
      result.error = `HTTP ${response.status}: ${response.statusText}`;
    }
    
  } catch (error) {
    result.loadTime = Date.now() - startTime;
    
    if (error.code === 'ECONNABORTED') {
      result.status = 'timeout';
      result.error = `Timeout after ${timeout}ms`;
    } else if (error.response) {
      result.status = 'error';
      result.statusCode = error.response.status;
      result.error = `HTTP ${error.response.status}: ${error.response.statusText}`;
    } else {
      result.status = 'error';
      result.error = error.message || 'Network error';
    }
  }
  
  return result;
}

async function runComprehensiveTest() {
  console.log('🚀 Starting comprehensive BizOSaaS Client Portal test...');
  console.log(`Testing ${ROUTES.length} routes at ${BASE_URL}`);
  console.log('=' * 60);
  
  const results = [];
  const issues = [];
  
  for (const route of ROUTES) {
    console.log(`\n📍 Testing ${route.name} (${route.path})...`);
    
    try {
      const result = await testRoute(route);
      results.push(result);
      
      // Immediate feedback
      const statusEmoji = result.status === 'success' ? '✅' : 
                         result.status === 'timeout' ? '⏰' : '❌';
      
      console.log(`   ${statusEmoji} Status: ${result.status.toUpperCase()}`);
      console.log(`   ⚡ Load Time: ${result.loadTime}ms`);
      console.log(`   📄 Status Code: ${result.statusCode || 'N/A'}`);
      console.log(`   📝 Title: ${result.title || 'N/A'}`);
      
      if (result.error) {
        console.log(`   ⚠️  Error: ${result.error}`);
      }
      
      if (result.hasLoadingState) {
        console.log(`   🔄 Loading state detected`);
      }
      
      if (result.hydrationIssues.length > 0) {
        console.log(`   💧 Hydration issues: ${result.hydrationIssues.length}`);
      }
      
      if (result.consoleErrors.length > 0) {
        console.log(`   🚨 Console errors: ${result.consoleErrors.length}`);
      }
      
      // Collect issues
      if (result.status !== 'success') {
        issues.push({
          route: route.path,
          name: route.name,
          issue: result.error || result.status,
          type: result.status,
          loadTime: result.loadTime
        });
      }
      
      if (result.hydrationIssues.length > 0) {
        issues.push({
          route: route.path,
          name: route.name,
          issue: 'Hydration issues detected',
          type: 'hydration',
          details: result.hydrationIssues
        });
      }
      
    } catch (testError) {
      console.log(`   ❌ Test failed: ${testError.message}`);
      issues.push({
        route: route.path,
        name: route.name,
        issue: `Test failed: ${testError.message}`,
        type: 'test_error'
      });
    }
    
    // Add small delay between requests
    await new Promise(resolve => setTimeout(resolve, 200));
  }
  
  // Generate summary report
  console.log('\n' + '=' * 80);
  console.log('📊 COMPREHENSIVE TEST SUMMARY');
  console.log('=' * 80);
  
  const successful = results.filter(r => r.status === 'success').length;
  const timeouts = results.filter(r => r.status === 'timeout').length;
  const errors = results.filter(r => r.status === 'error').length;
  const withLoadingStates = results.filter(r => r.hasLoadingState).length;
  const withHydrationIssues = results.filter(r => r.hydrationIssues.length > 0).length;
  
  console.log(`\n📈 Results Overview:`);
  console.log(`   ✅ Successful: ${successful}/${ROUTES.length} (${Math.round(successful/ROUTES.length*100)}%)`);
  console.log(`   ⏰ Timeouts: ${timeouts}`);
  console.log(`   ❌ Errors: ${errors}`);
  console.log(`   🔄 With Loading States: ${withLoadingStates}`);
  console.log(`   💧 With Hydration Issues: ${withHydrationIssues}`);
  
  console.log(`\n📋 Detailed Issues Found (${issues.length} total):`);
  issues.forEach((issue, index) => {
    console.log(`\n${index + 1}. ${issue.name} (${issue.route})`);
    console.log(`   Type: ${issue.type}`);
    console.log(`   Issue: ${issue.issue}`);
    if (issue.loadTime) {
      console.log(`   Load Time: ${issue.loadTime}ms`);
    }
    if (issue.details) {
      console.log(`   Details: ${JSON.stringify(issue.details, null, 4)}`);
    }
  });
  
  // Performance Analysis
  const loadTimes = results
    .filter(r => r.loadTime !== null)
    .map(r => r.loadTime);
  
  if (loadTimes.length > 0) {
    const avgLoadTime = Math.round(loadTimes.reduce((a, b) => a + b) / loadTimes.length);
    const maxLoadTime = Math.max(...loadTimes);
    const minLoadTime = Math.min(...loadTimes);
    
    console.log(`\n⚡ Performance Summary:`);
    console.log(`   Average Load Time: ${avgLoadTime}ms`);
    console.log(`   Fastest: ${minLoadTime}ms`);
    console.log(`   Slowest: ${maxLoadTime}ms`);
  }
  
  // Working Routes List
  const workingRoutes = results.filter(r => r.status === 'success');
  console.log(`\n✅ Working Routes (${workingRoutes.length}):`);
  workingRoutes.forEach(route => {
    console.log(`   ${route.path} - ${route.name} (${route.loadTime}ms)`);
  });
  
  // Broken Routes List
  const brokenRoutes = results.filter(r => r.status !== 'success');
  console.log(`\n❌ Broken/Problem Routes (${brokenRoutes.length}):`);
  brokenRoutes.forEach(route => {
    console.log(`   ${route.path} - ${route.name}: ${route.error || route.status}`);
  });
  
  // Generate JSON report
  const report = {
    timestamp: new Date().toISOString(),
    totalRoutes: ROUTES.length,
    summary: {
      successful,
      timeouts,
      errors,
      withLoadingStates,
      withHydrationIssues,
      successRate: Math.round(successful/ROUTES.length*100)
    },
    performance: loadTimes.length > 0 ? {
      averageLoadTime: Math.round(loadTimes.reduce((a, b) => a + b) / loadTimes.length),
      minLoadTime: Math.min(...loadTimes),
      maxLoadTime: Math.max(...loadTimes)
    } : null,
    detailedResults: results,
    issues: issues,
    workingRoutes: workingRoutes.map(r => ({ path: r.path, name: r.name, loadTime: r.loadTime })),
    brokenRoutes: brokenRoutes.map(r => ({ path: r.path, name: r.name, error: r.error, status: r.status }))
  };
  
  // Save report
  const fs = require('fs');
  const reportFilename = `route-test-report-${new Date().toISOString().replace(/[:.]/g, '-')}.json`;
  fs.writeFileSync(reportFilename, JSON.stringify(report, null, 2));
  
  console.log(`\n💾 Detailed report saved to: ${reportFilename}`);
  console.log('\n🏁 Test completed!');
  
  // Return summary for programmatic use
  return report;
}

// Only run if called directly
if (require.main === module) {
  runComprehensiveTest()
    .then(report => {
      process.exit(report.summary.successful === report.totalRoutes ? 0 : 1);
    })
    .catch(error => {
      console.error('Test suite failed:', error);
      process.exit(1);
    });
}

module.exports = { runComprehensiveTest, testRoute };