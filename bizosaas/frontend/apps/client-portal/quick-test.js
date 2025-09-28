#!/usr/bin/env node

/**
 * Quick BizOSaaS Client Portal Test
 * Focused testing with faster execution
 */

import axios from 'axios';
import fs from 'fs';

const BASE_URL = 'http://localhost:3000';
const results = { tests: [], errors: [], warnings: [] };

async function quickTest(path, name) {
  try {
    console.log(`Testing ${name} (${path})...`);
    const start = Date.now();
    const response = await axios.get(`${BASE_URL}${path}`, { 
      timeout: 5000,
      validateStatus: () => true 
    });
    const duration = Date.now() - start;
    
    const result = {
      path,
      name,
      status: response.status,
      duration,
      size: response.data?.length || 0,
      accessible: response.status === 200,
      hasErrors: response.status >= 500,
      notFound: response.status === 404
    };
    
    // Check for common issues in content
    if (typeof response.data === 'string' && response.status === 200) {
      result.hasServerError = response.data.includes('500') || response.data.includes('Internal Server Error');
      result.has404Content = response.data.includes('404') || response.data.includes('Not Found');
      result.hasHydrationIssues = response.data.includes('Hydration') || response.data.includes('hydration');
      result.hasNextError = response.data.includes('Application error') || response.data.includes('unhandledRejection');
    }
    
    results.tests.push(result);
    
    if (result.accessible) {
      console.log(`✅ ${name}: ${result.status} (${duration}ms)`);
    } else if (result.notFound) {
      console.log(`❌ ${name}: 404 Not Found`);
      results.errors.push(`${name}: Route not implemented`);
    } else if (result.hasErrors) {
      console.log(`🔥 ${name}: ${result.status} Server Error`);  
      results.errors.push(`${name}: Server error (${result.status})`);
    } else {
      console.log(`⚠️  ${name}: ${result.status}`);
      results.warnings.push(`${name}: Unexpected status ${result.status}`);
    }
    
    if (result.hasServerError) results.warnings.push(`${name}: Contains 500 error content`);
    if (result.has404Content) results.warnings.push(`${name}: Contains 404 error content`);
    if (result.hasHydrationIssues) results.warnings.push(`${name}: Possible hydration issues`);
    if (result.hasNextError) results.warnings.push(`${name}: Next.js application errors`);
    
    return result;
  } catch (error) {
    console.log(`💥 ${name}: Request failed - ${error.message}`);
    results.errors.push(`${name}: ${error.message}`);
    return { path, name, error: error.message, accessible: false };
  }
}

async function quickAPITest(endpoint, name) {
  try {
    console.log(`Testing API ${name} (${endpoint})...`);
    const start = Date.now();
    const response = await axios.get(`${BASE_URL}${endpoint}`, { 
      timeout: 3000,
      validateStatus: () => true 
    });
    const duration = Date.now() - start;
    
    const result = {
      endpoint,
      name,
      status: response.status,
      duration,
      accessible: response.status === 200,
      auth_required: response.status === 401 || response.status === 403,
      not_found: response.status === 404,
      server_error: response.status >= 500
    };
    
    results.tests.push(result);
    
    if (result.accessible) {
      console.log(`✅ API ${name}: ${result.status} (${duration}ms)`);
    } else if (result.auth_required) {
      console.log(`🔐 API ${name}: Auth required (${result.status})`);
      results.warnings.push(`API ${name}: Authentication required`);
    } else if (result.not_found) {
      console.log(`❌ API ${name}: 404 Not Found`);
      results.errors.push(`API ${name}: Endpoint not found`);
    } else if (result.server_error) {
      console.log(`🔥 API ${name}: Server Error (${result.status})`);
      results.errors.push(`API ${name}: Server error`);
    } else {
      console.log(`⚠️  API ${name}: ${result.status}`);
    }
    
    return result;
  } catch (error) {
    console.log(`💥 API ${name}: Request failed - ${error.message}`);
    results.errors.push(`API ${name}: ${error.message}`);
    return { endpoint, name, error: error.message, accessible: false };
  }
}

async function runQuickTests() {
  console.log('🚀 Starting BizOSaaS Client Portal Quick Test Suite');
  console.log('='.repeat(60));
  
  const startTime = Date.now();
  
  // Core pages
  await quickTest('/', 'Dashboard Home');
  await quickTest('/login', 'Login Page');
  await quickTest('/settings', 'Settings Page');
  
  // Feature pages
  await quickTest('/crm', 'CRM Dashboard');
  await quickTest('/crm/leads', 'CRM Leads');
  await quickTest('/crm/customers', 'CRM Customers');
  await quickTest('/ecommerce', 'E-commerce Dashboard');
  await quickTest('/ecommerce/orders', 'E-commerce Orders');
  await quickTest('/analytics', 'Analytics Dashboard');
  
  // Additional routes
  await quickTest('/integrations', 'Integrations');
  await quickTest('/workflows', 'Workflows'); 
  await quickTest('/reports', 'Reports');
  await quickTest('/account', 'Account');
  await quickTest('/cms', 'Content Management');
  await quickTest('/coreldove', 'Coreldove');
  
  console.log('\n🔌 Testing API Endpoints');
  console.log('-'.repeat(40));
  
  // Key API endpoints
  await quickAPITest('/api/brain/analytics/dashboard', 'Analytics API');
  await quickAPITest('/api/brain/django-crm/leads', 'CRM Leads API');
  await quickAPITest('/api/brain/django-crm/contacts', 'CRM Contacts API');
  await quickAPITest('/api/brain/wagtail/pages', 'Wagtail Pages API');
  await quickAPITest('/api/brain/integrations/overview', 'Integrations API');
  
  const endTime = Date.now();
  const duration = endTime - startTime;
  
  // Summary
  const accessible = results.tests.filter(t => t.accessible).length;
  const total = results.tests.length;
  const successRate = ((accessible / total) * 100).toFixed(1);
  
  console.log('\n' + '='.repeat(60));
  console.log('📊 QUICK TEST SUMMARY');
  console.log('='.repeat(60));
  console.log(`Total Tests: ${total}`);
  console.log(`Accessible: ${accessible}`);
  console.log(`Success Rate: ${successRate}%`);
  console.log(`Duration: ${(duration/1000).toFixed(1)}s`);
  console.log(`Errors: ${results.errors.length}`);
  console.log(`Warnings: ${results.warnings.length}`);
  
  if (results.errors.length > 0) {
    console.log('\n❌ ERRORS:');
    results.errors.forEach(error => console.log(`  - ${error}`));
  }
  
  if (results.warnings.length > 0) {
    console.log('\n⚠️  WARNINGS:');
    results.warnings.forEach(warning => console.log(`  - ${warning}`));
  }
  
  // Save results
  const report = {
    timestamp: new Date().toISOString(),
    duration,
    total,
    accessible,
    successRate: parseFloat(successRate),
    errors: results.errors,
    warnings: results.warnings,
    tests: results.tests
  };
  
  fs.writeFileSync('quick-test-results.json', JSON.stringify(report, null, 2));
  console.log('\n📄 Results saved to: quick-test-results.json');
  
  return report;
}

runQuickTests().catch(console.error);