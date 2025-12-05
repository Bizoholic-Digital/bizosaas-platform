#!/usr/bin/env node

/**
 * Route Validation Test - Test actual implemented routes
 */

import axios from 'axios';
import fs from 'fs';

const BASE_URL = 'http://localhost:3000';

// Actual implemented routes based on filesystem
const IMPLEMENTED_ROUTES = [
  // Core pages
  { path: '/', name: 'Dashboard Home', expected: 'working' },
  { path: '/login', name: 'Login Page', expected: 'working' },
  { path: '/settings', name: 'Settings', expected: 'working' },
  { path: '/test', name: 'Test Page', expected: 'working' },
  
  // Main feature areas  
  { path: '/analytics', name: 'Analytics Dashboard', expected: 'working' },
  { path: '/chat', name: 'AI Assistant Chat', expected: 'working' },
  { path: '/leads', name: 'Lead Management', expected: 'working' },
  { path: '/orders', name: 'Order Management', expected: 'working' },
  { path: '/directory', name: 'Business Directory', expected: 'working' },
  { path: '/review-management', name: 'Review Management', expected: 'working' },
  
  // CRM section
  { path: '/crm', name: 'CRM Dashboard', expected: 'working' },
  { path: '/crm/contacts', name: 'CRM Contacts', expected: 'working' },
  { path: '/crm/campaigns', name: 'CRM Campaigns', expected: 'working' },
  { path: '/crm/reports', name: 'CRM Reports', expected: 'working' },
  
  // Content management
  { path: '/content', name: 'Content Management', expected: 'working' },
  { path: '/content/pages', name: 'Content Pages', expected: 'working' },
  { path: '/content/blog', name: 'Content Blog', expected: 'working' },
  { path: '/content/forms', name: 'Content Forms', expected: 'working' },
  { path: '/content/media', name: 'Content Media', expected: 'working' },
  
  // E-commerce
  { path: '/ecommerce', name: 'E-commerce Dashboard', expected: 'working' },
];

// Routes that should return 404 (not implemented)
const MISSING_ROUTES = [
  '/crm/leads',    // Should be /leads  
  '/crm/customers', // Should be /crm/contacts
  '/crm/pipeline',  // Not implemented
  '/ecommerce/orders', // Should be /orders
  '/coreldove',     // Not implemented
  '/integrations',  // Not implemented
  '/workflows',     // Not implemented  
  '/reports',       // Should be /crm/reports
  '/account',       // Not implemented
  '/cms',          // Should be /content
];

async function testRoute(route) {
  try {
    console.log(`Testing ${route.name} (${route.path})...`);
    const response = await axios.get(`${BASE_URL}${route.path}`, { 
      timeout: 5000,
      validateStatus: () => true 
    });
    
    const result = {
      ...route,
      status: response.status,
      accessible: response.status === 200,
      redirected: response.status === 301 || response.status === 302,
      notFound: response.status === 404,
      serverError: response.status >= 500,
      size: response.data?.length || 0
    };
    
    // Analyze content for issues  
    if (typeof response.data === 'string' && response.status === 200) {
      result.hasLoadingState = response.data.includes('animate-pulse') || response.data.includes('Loading');
      result.hasHydrationMarkers = response.data.includes('$') && response.data.includes('ReactDOM');
      result.containsErrorContent = response.data.includes('500') || response.data.includes('404');
      result.isFullyLoaded = !result.hasLoadingState || response.data.length > 20000; // Rough heuristic
    }
    
    if (result.accessible) {
      console.log(`✅ ${route.name}: Working (${result.status})`);
    } else if (result.notFound) {
      console.log(`❌ ${route.name}: Not Found (404)`);
    } else if (result.serverError) {
      console.log(`🔥 ${route.name}: Server Error (${result.status})`);
    } else if (result.redirected) {
      console.log(`🔄 ${route.name}: Redirected (${result.status})`);
    } else {
      console.log(`⚠️  ${route.name}: Unexpected (${result.status})`);
    }
    
    return result;
    
  } catch (error) {
    console.log(`💥 ${route.name}: Failed - ${error.message}`);
    return {
      ...route,
      error: error.message,
      accessible: false
    };
  }
}

async function validateNavigation() {
  console.log('🧭 BizOSaaS Client Portal - Route Validation');
  console.log('=' .repeat(60));
  
  const results = {
    implemented: [],
    missing: [],
    summary: { total: 0, working: 0, broken: 0, missing: 0 }
  };
  
  // Test implemented routes
  console.log('\n📋 Testing Implemented Routes:');
  console.log('-'.repeat(40));
  
  for (const route of IMPLEMENTED_ROUTES) {
    const result = await testRoute(route);
    results.implemented.push(result);
    results.summary.total++;
    
    if (result.accessible) {
      results.summary.working++;
    } else {
      results.summary.broken++;
    }
    
    // Small delay
    await new Promise(resolve => setTimeout(resolve, 100));
  }
  
  // Test missing routes  
  console.log('\n🚫 Testing Expected Missing Routes:');
  console.log('-'.repeat(40));
  
  for (const path of MISSING_ROUTES) {
    const result = await testRoute({ path, name: `Missing: ${path}` });
    results.missing.push(result);
    
    if (result.notFound) {
      console.log(`✅ ${path}: Correctly returns 404`);
    } else if (result.accessible) {
      console.log(`⚠️  ${path}: Unexpectedly working - check navigation`);
    }
    
    await new Promise(resolve => setTimeout(resolve, 100));
  }
  
  // Summary
  console.log('\n' + '='.repeat(60));
  console.log('📊 ROUTE VALIDATION SUMMARY');
  console.log('='.repeat(60));
  console.log(`Total Implemented Routes: ${IMPLEMENTED_ROUTES.length}`);
  console.log(`Working Routes: ${results.summary.working}`);
  console.log(`Broken Routes: ${results.summary.broken}`);
  console.log(`Success Rate: ${(results.summary.working/IMPLEMENTED_ROUTES.length*100).toFixed(1)}%`);
  
  // Detailed analysis
  const brokenRoutes = results.implemented.filter(r => !r.accessible);
  if (brokenRoutes.length > 0) {
    console.log('\n❌ Broken Routes:');
    brokenRoutes.forEach(route => {
      console.log(`  - ${route.name} (${route.path}): ${route.status || route.error}`);
    });
  }
  
  const loadingIssues = results.implemented.filter(r => r.accessible && r.hasLoadingState);
  if (loadingIssues.length > 0) {
    console.log('\n⏳ Routes with Loading Issues:');
    loadingIssues.forEach(route => {
      console.log(`  - ${route.name}: Still showing loading state`);
    });
  }
  
  const errorContent = results.implemented.filter(r => r.accessible && r.containsErrorContent);
  if (errorContent.length > 0) {
    console.log('\n🚨 Routes with Error Content:');
    errorContent.forEach(route => {
      console.log(`  - ${route.name}: Contains error messages in content`);
    });
  }
  
  // Save detailed results  
  const report = {
    timestamp: new Date().toISOString(),
    summary: results.summary,
    implemented: results.implemented,
    missing: results.missing,
    navigation_issues: {
      broken_routes: brokenRoutes,
      loading_issues: loadingIssues,
      error_content: errorContent
    }
  };
  
  fs.writeFileSync('route-validation-results.json', JSON.stringify(report, null, 2));
  console.log('\n📄 Results saved to: route-validation-results.json');
  
  return report;
}

validateNavigation().catch(console.error);