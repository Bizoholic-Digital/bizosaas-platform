#!/usr/bin/env node

/**
 * API Integration Test Suite
 * Tests all backend API integrations after fixes
 */

const baseUrl = 'http://localhost:3000';

// Test configurations
const tests = [
  {
    name: 'Authentication - Valid Login',
    method: 'POST',
    endpoint: '/api/auth/login',
    body: {
      email: 'demo@bizosaas.com',
      password: 'demo123'
    },
    expectedStatus: 200,
    expectedFields: ['success', 'token', 'user']
  },
  {
    name: 'Authentication - Invalid Login', 
    method: 'POST',
    endpoint: '/api/auth/login',
    body: {
      email: 'wrong@email.com',
      password: 'wrongpass'
    },
    expectedStatus: 401,
    expectedFields: ['success', 'error']
  },
  {
    name: 'CRM Leads - Get All',
    method: 'GET',
    endpoint: '/api/brain/django-crm/leads',
    expectedStatus: 200,
    expectedFields: ['success', 'leads']
  },
  {
    name: 'CRM Contacts - Get All (Fallback)',
    method: 'GET',
    endpoint: '/api/brain/django-crm/contacts',
    expectedStatus: 200,
    expectedFields: ['contacts', 'pagination', 'source']
  },
  {
    name: 'CRM Deals - Get All (Fallback)',
    method: 'GET',
    endpoint: '/api/brain/django-crm/deals',
    expectedStatus: 200,
    expectedFields: ['deals', 'pagination', 'source']
  },
  {
    name: 'Settings - Get All',
    method: 'GET',
    endpoint: '/api/settings',
    expectedStatus: 200,
    expectedFields: ['success', 'data', 'source']
  },
  {
    name: 'Media - Get Library',
    method: 'GET',
    endpoint: '/api/media',
    expectedStatus: 200,
    expectedFields: ['success', 'data', 'source']
  },
  {
    name: 'E-commerce - Get Dashboard',
    method: 'GET',
    endpoint: '/api/ecommerce',
    expectedStatus: 200,
    expectedFields: ['success', 'data', 'source']
  },
  {
    name: 'Analytics - Get Dashboards',
    method: 'GET',
    endpoint: '/api/brain/analytics/dashboard',
    expectedStatus: 200,
    expectedFields: ['dashboards', 'count']
  }
];

// Test runner function
async function runTest(test) {
  try {
    const url = `${baseUrl}${test.endpoint}`;
    const options = {
      method: test.method,
      headers: {
        'Content-Type': 'application/json',
      }
    };

    if (test.body) {
      options.body = JSON.stringify(test.body);
    }

    console.log(`\n🔍 Testing: ${test.name}`);
    console.log(`   ${test.method} ${test.endpoint}`);

    const startTime = Date.now();
    const response = await fetch(url, options);
    const endTime = Date.now();
    const responseTime = endTime - startTime;

    let responseData;
    const contentType = response.headers.get('content-type');
    
    if (contentType && contentType.includes('application/json')) {
      responseData = await response.json();
    } else {
      responseData = await response.text();
    }

    // Check status code
    const statusMatch = response.status === test.expectedStatus;
    
    // Check expected fields
    let fieldsMatch = true;
    let missingFields = [];
    
    if (test.expectedFields && typeof responseData === 'object') {
      for (const field of test.expectedFields) {
        if (!responseData.hasOwnProperty(field)) {
          fieldsMatch = false;
          missingFields.push(field);
        }
      }
    }

    // Determine test result
    const passed = statusMatch && fieldsMatch;

    // Log results
    if (passed) {
      console.log(`   ✅ PASS (${responseTime}ms)`);
      console.log(`      Status: ${response.status} ✓`);
      if (test.expectedFields) {
        console.log(`      Fields: ${test.expectedFields.join(', ')} ✓`);
      }
    } else {
      console.log(`   ❌ FAIL (${responseTime}ms)`);
      console.log(`      Status: ${response.status} ${statusMatch ? '✓' : '✗ (expected ' + test.expectedStatus + ')'}`);
      if (!fieldsMatch) {
        console.log(`      Missing fields: ${missingFields.join(', ')}`);
      }
      console.log(`      Response: ${JSON.stringify(responseData, null, 2)}`);
    }

    return {
      name: test.name,
      passed,
      responseTime,
      status: response.status,
      expectedStatus: test.expectedStatus,
      hasExpectedFields: fieldsMatch,
      responseSize: JSON.stringify(responseData).length
    };

  } catch (error) {
    console.log(`   ❌ ERROR: ${error.message}`);
    return {
      name: test.name,
      passed: false,
      error: error.message,
      responseTime: 0,
      status: 0,
      expectedStatus: test.expectedStatus
    };
  }
}

// Main test execution
async function runAllTests() {
  console.log('🚀 BizOSaaS Client Portal - API Integration Tests');
  console.log('=' .repeat(60));
  console.log(`Base URL: ${baseUrl}`);
  console.log(`Tests to run: ${tests.length}`);

  const results = [];
  
  for (const test of tests) {
    const result = await runTest(test);
    results.push(result);
    
    // Small delay between tests
    await new Promise(resolve => setTimeout(resolve, 100));
  }

  // Calculate summary
  const passed = results.filter(r => r.passed).length;
  const failed = results.length - passed;
  const avgResponseTime = results.reduce((sum, r) => sum + (r.responseTime || 0), 0) / results.length;

  // Print summary
  console.log('\n' + '=' .repeat(60));
  console.log('📊 Test Summary');
  console.log('=' .repeat(60));
  console.log(`Total Tests: ${results.length}`);
  console.log(`Passed: ${passed} (${Math.round(passed/results.length*100)}%)`);
  console.log(`Failed: ${failed}`);
  console.log(`Average Response Time: ${Math.round(avgResponseTime)}ms`);

  // Show failed tests
  const failedTests = results.filter(r => !r.passed);
  if (failedTests.length > 0) {
    console.log('\n❌ Failed Tests:');
    failedTests.forEach(test => {
      console.log(`   • ${test.name}: ${test.error || 'Assertion failed'}`);
    });
  }

  // Show performance insights
  console.log('\n⚡ Performance Summary:');
  const fastTests = results.filter(r => r.responseTime < 200).length;
  const mediumTests = results.filter(r => r.responseTime >= 200 && r.responseTime < 1000).length;
  const slowTests = results.filter(r => r.responseTime >= 1000).length;
  
  console.log(`   Fast (<200ms): ${fastTests} tests`);
  console.log(`   Medium (200-1000ms): ${mediumTests} tests`);
  console.log(`   Slow (>1000ms): ${slowTests} tests`);

  // Show API health status
  console.log('\n🩺 API Health Check:');
  const authWorking = results.find(r => r.name.includes('Authentication - Valid'))?.passed || false;
  const crmWorking = results.filter(r => r.name.includes('CRM')).every(r => r.passed);
  const settingsWorking = results.find(r => r.name.includes('Settings'))?.passed || false;
  const mediaWorking = results.find(r => r.name.includes('Media'))?.passed || false;
  const ecommerceWorking = results.find(r => r.name.includes('E-commerce'))?.passed || false;
  const analyticsWorking = results.find(r => r.name.includes('Analytics'))?.passed || false;

  console.log(`   Authentication: ${authWorking ? '✅' : '❌'}`);
  console.log(`   CRM System: ${crmWorking ? '✅' : '❌'}`);
  console.log(`   Settings Management: ${settingsWorking ? '✅' : '❌'}`);
  console.log(`   Media Management: ${mediaWorking ? '✅' : '❌'}`);
  console.log(`   E-commerce: ${ecommerceWorking ? '✅' : '❌'}`);
  console.log(`   Analytics: ${analyticsWorking ? '✅' : '❌'}`);

  // Overall status
  const overallHealth = (passed / results.length) * 100;
  console.log(`\n🎯 Overall API Health: ${Math.round(overallHealth)}%`);
  
  if (overallHealth >= 90) {
    console.log('🟢 Excellent - Ready for production');
  } else if (overallHealth >= 75) {
    console.log('🟡 Good - Minor issues to address');
  } else if (overallHealth >= 50) {
    console.log('🟠 Fair - Several issues need attention');
  } else {
    console.log('🔴 Poor - Major issues require immediate fixing');
  }

  // Save results to file
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const reportData = {
    timestamp: new Date().toISOString(),
    summary: {
      total: results.length,
      passed,
      failed,
      success_rate: Math.round(overallHealth),
      avg_response_time: Math.round(avgResponseTime)
    },
    tests: results,
    health_check: {
      authentication: authWorking,
      crm_system: crmWorking,
      settings: settingsWorking,
      media: mediaWorking,
      ecommerce: ecommerceWorking,
      analytics: analyticsWorking
    }
  };

  const fs = await import('fs');
  await fs.promises.writeFile(
    `api-integration-test-results-${timestamp}.json`,
    JSON.stringify(reportData, null, 2)
  );

  console.log(`\n💾 Report saved: api-integration-test-results-${timestamp}.json`);
  console.log('=' .repeat(60));

  // Exit with appropriate code
  process.exit(failed > 0 ? 1 : 0);
}

// Run the tests
runAllTests().catch(console.error);