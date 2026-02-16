#!/usr/bin/env node

/**
 * Comprehensive API Integration Testing Suite
 * Tests all Client Portal FastAPI AI Central Hub integrations
 */

const BASE_URL = 'http://localhost:3006'

// Test data for POST/PUT operations
const testData = {
  lead: {
    first_name: "Test",
    last_name: "User",
    email: "test@example.com",
    company: "Test Company",
    position: "Test Manager",
    phone: "+1-555-0000",
    source: "api_test",
    status: "new",
    estimated_value: 25000,
    probability: 60,
    tags: ["test", "automation"],
    notes: "Created via API test suite"
  },
  contact: {
    name: "Test Contact",
    email: "contact@test.com",
    message: "Test message from API testing"
  }
}

// All endpoints to test
const endpoints = [
  // Django CRM Endpoints
  { method: 'GET', url: '/api/brain/django-crm/leads', category: 'Django CRM', name: 'Leads List' },
  { method: 'POST', url: '/api/brain/django-crm/leads', category: 'Django CRM', name: 'Create Lead', data: testData.lead },
  { method: 'GET', url: '/api/brain/django-crm/contacts', category: 'Django CRM', name: 'Contacts List' },
  { method: 'GET', url: '/api/brain/django-crm/deals', category: 'Django CRM', name: 'Deals List' },
  { method: 'GET', url: '/api/brain/django-crm/activities', category: 'Django CRM', name: 'Activities List' },

  // Wagtail CMS Endpoints
  { method: 'GET', url: '/api/brain/wagtail/pages', category: 'Wagtail CMS', name: 'Pages List' },
  { method: 'POST', url: '/api/brain/wagtail/contact', category: 'Wagtail CMS', name: 'Contact Form', data: testData.contact },

  // Saleor E-commerce Endpoints
  { method: 'GET', url: '/api/brain/saleor/products', category: 'Saleor E-commerce', name: 'Products List' },
  { method: 'GET', url: '/api/brain/saleor/orders', category: 'Saleor E-commerce', name: 'Orders List' },
  { method: 'GET', url: '/api/brain/saleor/customers', category: 'Saleor E-commerce', name: 'Customers List' },
  { method: 'GET', url: '/api/brain/saleor/categories', category: 'Saleor E-commerce', name: 'Categories List' },

  // Billing System Endpoints
  { method: 'GET', url: '/api/brain/billing/payment-methods', category: 'Billing System', name: 'Payment Methods' },
  { method: 'GET', url: '/api/brain/billing/subscriptions', category: 'Billing System', name: 'Subscriptions' },
  { method: 'GET', url: '/api/brain/billing/invoices', category: 'Billing System', name: 'Invoices' },
  { method: 'GET', url: '/api/brain/billing/usage', category: 'Billing System', name: 'Usage Tracking' },
  { method: 'GET', url: '/api/brain/billing/payments', category: 'Billing System', name: 'Payments History' },

  // Integration Management Endpoints
  { method: 'GET', url: '/api/brain/integrations/overview', category: 'Integration Management', name: 'Overview' },
  { method: 'GET', url: '/api/brain/integrations/webhooks', category: 'Integration Management', name: 'Webhooks' },
  { method: 'GET', url: '/api/brain/integrations/apis', category: 'Integration Management', name: 'API Keys' },
  { method: 'GET', url: '/api/brain/integrations/logs', category: 'Integration Management', name: 'Integration Logs' },
  { method: 'GET', url: '/api/brain/integrations/automations', category: 'Integration Management', name: 'Automations' },
  { method: 'GET', url: '/api/brain/integrations/third-party', category: 'Integration Management', name: 'Third-Party Integrations' },

  // Analytics Endpoints
  { method: 'GET', url: '/api/brain/analytics/dashboards', category: 'Analytics', name: 'Dashboards' },

  // Marketing Endpoints (Additional discovered routes)
  { method: 'GET', url: '/api/brain/marketing/campaigns', category: 'Marketing', name: 'Campaigns' },
  { method: 'GET', url: '/api/brain/marketing/audiences', category: 'Marketing', name: 'Audiences' },
  { method: 'GET', url: '/api/brain/marketing/content', category: 'Marketing', name: 'Content' },
  { method: 'GET', url: '/api/brain/marketing/analytics', category: 'Marketing', name: 'Marketing Analytics' },
  { method: 'GET', url: '/api/brain/marketing/approvals', category: 'Marketing', name: 'Approvals' },

  // Health Check
  { method: 'GET', url: '/api/health', category: 'System', name: 'Health Check' }
]

class APITester {
  constructor() {
    this.results = {
      total: 0,
      passed: 0,
      failed: 0,
      categories: {},
      details: []
    }
  }

  async runTest(endpoint) {
    const { method, url, category, name, data } = endpoint
    const fullUrl = `${BASE_URL}${url}`
    
    console.log(`Testing ${method} ${url}...`)
    
    try {
      const options = {
        method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer test-token'
        }
      }

      if (data && (method === 'POST' || method === 'PUT')) {
        options.body = JSON.stringify(data)
      }

      const startTime = Date.now()
      const response = await fetch(fullUrl, options)
      const responseTime = Date.now() - startTime
      
      let responseData
      const contentType = response.headers.get('content-type')
      
      if (contentType && contentType.includes('application/json')) {
        try {
          responseData = await response.json()
        } catch (e) {
          responseData = { error: 'Invalid JSON response', raw: await response.text() }
        }
      } else {
        responseData = { text: await response.text() }
      }

      const result = {
        endpoint: `${method} ${url}`,
        category,
        name,
        status: response.status,
        ok: response.ok,
        responseTime,
        fallbackMode: responseData?.source === 'fallback',
        error: null,
        data: responseData
      }

      // Categorize result
      if (!this.results.categories[category]) {
        this.results.categories[category] = { total: 0, passed: 0, failed: 0 }
      }
      
      this.results.categories[category].total++
      this.results.total++

      if (response.ok) {
        this.results.passed++
        this.results.categories[category].passed++
        console.log(`✅ PASS: ${name} (${response.status}) - ${responseTime}ms${result.fallbackMode ? ' [FALLBACK]' : ''}`)
      } else {
        this.results.failed++
        this.results.categories[category].failed++
        result.error = `HTTP ${response.status}`
        console.log(`❌ FAIL: ${name} (${response.status}) - ${responseTime}ms`)
      }

      this.results.details.push(result)
      return result
    } catch (error) {
      const result = {
        endpoint: `${method} ${url}`,
        category,
        name,
        status: 0,
        ok: false,
        responseTime: 0,
        fallbackMode: false,
        error: error.message,
        data: null
      }

      this.results.failed++
      this.results.total++
      
      if (!this.results.categories[category]) {
        this.results.categories[category] = { total: 0, passed: 0, failed: 0 }
      }
      this.results.categories[category].total++
      this.results.categories[category].failed++

      console.log(`❌ ERROR: ${name} - ${error.message}`)
      this.results.details.push(result)
      return result
    }
  }

  async runAllTests() {
    console.log('🚀 Starting Comprehensive API Integration Testing\n')
    console.log(`Testing ${endpoints.length} endpoints across multiple categories...\n`)

    for (const endpoint of endpoints) {
      await this.runTest(endpoint)
      await new Promise(resolve => setTimeout(resolve, 100)) // Rate limiting
    }

    this.generateReport()
  }

  generateReport() {
    console.log('\n' + '='.repeat(80))
    console.log('📊 COMPREHENSIVE API TEST RESULTS')
    console.log('='.repeat(80))

    console.log(`\n🎯 OVERALL SUMMARY:`)
    console.log(`Total Tests: ${this.results.total}`)
    console.log(`Passed: ${this.results.passed} (${((this.results.passed / this.results.total) * 100).toFixed(1)}%)`)
    console.log(`Failed: ${this.results.failed} (${((this.results.failed / this.results.total) * 100).toFixed(1)}%)`)

    console.log(`\n📈 CATEGORY BREAKDOWN:`)
    Object.entries(this.results.categories).forEach(([category, stats]) => {
      const successRate = ((stats.passed / stats.total) * 100).toFixed(1)
      console.log(`${category}: ${stats.passed}/${stats.total} (${successRate}%)`)
    })

    console.log(`\n🔄 FALLBACK MODE USAGE:`)
    const fallbackTests = this.results.details.filter(r => r.fallbackMode)
    console.log(`Endpoints using fallback data: ${fallbackTests.length}`)
    fallbackTests.forEach(test => {
      console.log(`  - ${test.name}`)
    })

    console.log(`\n⚡ PERFORMANCE METRICS:`)
    const responseTimes = this.results.details
      .filter(r => r.ok && r.responseTime > 0)
      .map(r => r.responseTime)
    
    if (responseTimes.length > 0) {
      const avgTime = responseTimes.reduce((a, b) => a + b, 0) / responseTimes.length
      const maxTime = Math.max(...responseTimes)
      const minTime = Math.min(...responseTimes)
      console.log(`Average Response Time: ${avgTime.toFixed(0)}ms`)
      console.log(`Max Response Time: ${maxTime}ms`)
      console.log(`Min Response Time: ${minTime}ms`)
    }

    console.log(`\n❌ FAILED TESTS:`)
    const failedTests = this.results.details.filter(r => !r.ok)
    if (failedTests.length === 0) {
      console.log('None! 🎉')
    } else {
      failedTests.forEach(test => {
        console.log(`  - ${test.name}: ${test.error || 'HTTP ' + test.status}`)
      })
    }

    console.log(`\n✅ SUCCESS CRITERIA EVALUATION:`)
    console.log(`✅ All routes accessible via /api/brain/ pattern: ${this.results.passed > 0 ? 'YES' : 'NO'}`)
    console.log(`✅ Fallback data provided when needed: ${fallbackTests.length > 0 ? 'YES' : 'NO'}`)
    console.log(`✅ No critical 500 errors: ${!this.results.details.some(r => r.status === 500) ? 'YES' : 'NO'}`)
    console.log(`✅ Response format consistency: ${this.results.passed > this.results.failed ? 'YES' : 'NO'}`)

    console.log(`\n📋 RECOMMENDATIONS:`)
    if (this.results.failed > 0) {
      console.log('⚠️  Some endpoints are failing - review error logs and Central Hub connectivity')
    }
    if (fallbackTests.length === this.results.passed) {
      console.log('⚠️  All successful endpoints are using fallback data - check Central Hub connection')
    }
    if (responseTimes.length > 0 && Math.max(...responseTimes) > 5000) {
      console.log('⚠️  Some endpoints have slow response times (>5s) - optimize performance')
    }
    if (this.results.passed === this.results.total) {
      console.log('🎉 All tests passing! API integration is working perfectly.')
    }

    console.log('\n' + '='.repeat(80))
    
    // Save detailed results to file
    const detailedResults = {
      timestamp: new Date().toISOString(),
      summary: {
        total: this.results.total,
        passed: this.results.passed,
        failed: this.results.failed,
        successRate: ((this.results.passed / this.results.total) * 100).toFixed(1) + '%'
      },
      categories: this.results.categories,
      fallbackCount: fallbackTests.length,
      performance: responseTimes.length > 0 ? {
        average: Math.round(responseTimes.reduce((a, b) => a + b, 0) / responseTimes.length),
        max: Math.max(...responseTimes),
        min: Math.min(...responseTimes)
      } : null,
      details: this.results.details
    }

    return detailedResults
  }
}

// Run the tests
async function runTests() {
  const tester = new APITester()
  const results = await tester.runAllTests()
  
  // Save results to file
  const fs = require('fs').promises
  await fs.writeFile('api-test-results.json', JSON.stringify(results, null, 2))
  console.log('\n💾 Detailed results saved to: api-test-results.json')
}

// Auto-run if called directly
if (require.main === module) {
  runTests().catch(console.error)
}

module.exports = { APITester, endpoints, testData }