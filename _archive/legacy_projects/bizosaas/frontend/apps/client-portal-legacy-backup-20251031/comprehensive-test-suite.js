#!/usr/bin/env node

/**
 * Comprehensive BizOSaaS Client Portal Testing Suite
 * Tests authentication, navigation, pages, components, and performance
 * 
 * Run with: node comprehensive-test-suite.js
 */

import axios from 'axios';
import fs from 'fs';
import path from 'path';

const BASE_URL = 'http://localhost:3000';
const TEST_RESULTS = [];
const CONSOLE_ERRORS = [];

// Test configuration
const TEST_CONFIG = {
  timeout: 10000,
  retries: 3,
  demo_credentials: {
    email: 'demo@bizosaas.com',
    password: 'demo123'
  }
};

// Define all routes to test
const ROUTES_TO_TEST = [
  // Authentication routes
  { path: '/login', name: 'Login Page', auth_required: false },
  
  // Main dashboard
  { path: '/', name: 'Dashboard Home', auth_required: true },
  
  // CRM routes
  { path: '/crm', name: 'CRM Dashboard', auth_required: true },
  { path: '/crm/leads', name: 'CRM Leads', auth_required: true },
  { path: '/crm/customers', name: 'CRM Customers', auth_required: true },
  { path: '/crm/pipeline', name: 'CRM Pipeline', auth_required: true },
  
  // E-commerce routes
  { path: '/ecommerce', name: 'E-commerce Dashboard', auth_required: true },
  { path: '/ecommerce/orders', name: 'E-commerce Orders', auth_required: true },
  { path: '/coreldove', name: 'Coreldove Storefront', auth_required: true },
  
  // Content management
  { path: '/cms', name: 'Content Management', auth_required: true },
  { path: '/analytics', name: 'Analytics Dashboard', auth_required: true },
  
  // Settings and account
  { path: '/settings', name: 'Settings Page', auth_required: true },
  { path: '/account', name: 'Account Page', auth_required: true },
  
  // Additional feature pages
  { path: '/integrations', name: 'Integrations', auth_required: true },
  { path: '/workflows', name: 'Workflows', auth_required: true },
  { path: '/reports', name: 'Reports', auth_required: true },
];

// API endpoints to test
const API_ENDPOINTS = [
  '/api/brain/analytics/dashboard',
  '/api/brain/django-crm/leads',
  '/api/brain/django-crm/contacts',
  '/api/brain/django-crm/deals',
  '/api/brain/wagtail/pages',
  '/api/brain/integrations/overview',
  '/api/brain/review-management/summary',
];

class TestRunner {
  constructor() {
    this.results = {
      total_tests: 0,
      passed: 0,
      failed: 0,
      skipped: 0,
      start_time: new Date(),
      errors: [],
      warnings: [],
      performance: {}
    };
  }

  async log(level, message, details = null) {
    const timestamp = new Date().toISOString();
    const logEntry = {
      timestamp,
      level,
      message,
      details
    };
    
    console.log(`[${timestamp}] ${level.toUpperCase()}: ${message}`);
    if (details) {
      console.log('Details:', JSON.stringify(details, null, 2));
    }
    
    TEST_RESULTS.push(logEntry);
    
    if (level === 'error') {
      this.results.errors.push(logEntry);
    } else if (level === 'warn') {
      this.results.warnings.push(logEntry);
    }
  }

  async makeRequest(url, options = {}) {
    const fullUrl = `${BASE_URL}${url}`;
    const startTime = performance.now();
    
    try {
      const response = await axios({
        url: fullUrl,
        method: options.method || 'GET',
        timeout: TEST_CONFIG.timeout,
        headers: {
          'User-Agent': 'BizOSaaS-Test-Suite/1.0',
          ...options.headers
        },
        data: options.data,
        validateStatus: () => true // Accept all status codes
      });
      
      const endTime = performance.now();
      const duration = endTime - startTime;
      
      return {
        success: true,
        status: response.status,
        headers: response.headers,
        data: response.data,
        duration,
        size: response.headers['content-length'] || response.data?.length || 0
      };
    } catch (error) {
      const endTime = performance.now();
      const duration = endTime - startTime;
      
      return {
        success: false,
        error: error.message,
        duration,
        code: error.code
      };
    }
  }

  async testAuthentication() {
    await this.log('info', 'Starting Authentication Flow Tests');
    
    // Test login page accessibility
    const loginPageTest = await this.makeRequest('/login');
    this.results.total_tests++;
    
    if (loginPageTest.success && loginPageTest.status === 200) {
      this.results.passed++;
      await this.log('info', 'Login page accessible', {
        status: loginPageTest.status,
        duration: loginPageTest.duration
      });
    } else {
      this.results.failed++;
      await this.log('error', 'Login page not accessible', loginPageTest);
    }

    // Test login functionality (if login form exists)
    const loginTest = await this.makeRequest('/api/auth/login', {
      method: 'POST',
      data: TEST_CONFIG.demo_credentials,
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    this.results.total_tests++;
    
    if (loginTest.success) {
      if (loginTest.status === 200 || loginTest.status === 302) {
        this.results.passed++;
        await this.log('info', 'Login endpoint responsive', {
          status: loginTest.status,
          duration: loginTest.duration
        });
      } else if (loginTest.status === 404) {
        this.results.skipped++;
        await this.log('warn', 'Login API endpoint not found - may use client-side auth');
      } else {
        this.results.failed++;
        await this.log('error', 'Login endpoint error', loginTest);
      }
    } else {
      this.results.failed++;
      await this.log('error', 'Login request failed', loginTest);
    }
  }

  async testRoutes() {
    await this.log('info', 'Starting Route Testing');
    
    for (const route of ROUTES_TO_TEST) {
      this.results.total_tests++;
      
      const test = await this.makeRequest(route.path);
      
      if (test.success) {
        if (test.status === 200) {
          this.results.passed++;
          await this.log('info', `Route accessible: ${route.name}`, {
            path: route.path,
            status: test.status,
            duration: test.duration,
            size: test.size
          });
          
          // Check for common issues in HTML content
          if (typeof test.data === 'string') {
            if (test.data.includes('500') || test.data.includes('Internal Server Error')) {
              await this.log('warn', `Route may have server errors: ${route.name}`);
            }
            
            if (test.data.includes('404') || test.data.includes('Not Found')) {
              await this.log('warn', `Route may show 404 content: ${route.name}`);
            }
            
            if (test.data.includes('Hydration') || test.data.includes('hydration')) {
              await this.log('warn', `Possible hydration issues detected: ${route.name}`);
            }
          }
        } else if (test.status === 302 || test.status === 301) {
          this.results.passed++;
          await this.log('info', `Route redirects (expected for auth): ${route.name}`, {
            path: route.path,
            status: test.status,
            duration: test.duration
          });
        } else if (test.status === 404) {
          this.results.failed++;
          await this.log('error', `Route not found: ${route.name}`, {
            path: route.path,
            status: test.status
          });
        } else {
          this.results.failed++;
          await this.log('error', `Route error: ${route.name}`, test);
        }
      } else {
        this.results.failed++;
        await this.log('error', `Route request failed: ${route.name}`, test);
      }
      
      // Small delay to prevent overwhelming the server
      await new Promise(resolve => setTimeout(resolve, 100));
    }
  }

  async testAPIEndpoints() {
    await this.log('info', 'Starting API Endpoint Testing');
    
    for (const endpoint of API_ENDPOINTS) {
      this.results.total_tests++;
      
      const test = await this.makeRequest(endpoint);
      
      if (test.success) {
        if (test.status === 200) {
          this.results.passed++;
          await this.log('info', `API endpoint accessible: ${endpoint}`, {
            status: test.status,
            duration: test.duration,
            size: test.size
          });
          
          // Validate JSON response
          try {
            if (typeof test.data === 'string') {
              JSON.parse(test.data);
            }
            await this.log('info', `API returns valid JSON: ${endpoint}`);
          } catch {
            await this.log('warn', `API does not return valid JSON: ${endpoint}`);
          }
        } else if (test.status === 401 || test.status === 403) {
          this.results.skipped++;
          await this.log('warn', `API endpoint requires authentication: ${endpoint}`, {
            status: test.status
          });
        } else if (test.status === 404) {
          this.results.failed++;
          await this.log('error', `API endpoint not found: ${endpoint}`, {
            status: test.status
          });
        } else {
          this.results.failed++;
          await this.log('error', `API endpoint error: ${endpoint}`, test);
        }
      } else {
        this.results.failed++;
        await this.log('error', `API request failed: ${endpoint}`, test);
      }
      
      await new Promise(resolve => setTimeout(resolve, 100));
    }
  }

  async testPerformance() {
    await this.log('info', 'Starting Performance Testing');
    
    // Test main page load time
    const performanceTests = [
      '/',
      '/login',
      '/crm',
      '/ecommerce'
    ];
    
    for (const path of performanceTests) {
      const iterations = 3;
      const times = [];
      
      for (let i = 0; i < iterations; i++) {
        const test = await this.makeRequest(path);
        if (test.success) {
          times.push(test.duration);
        }
        await new Promise(resolve => setTimeout(resolve, 200));
      }
      
      if (times.length > 0) {
        const avgTime = times.reduce((a, b) => a + b) / times.length;
        const minTime = Math.min(...times);
        const maxTime = Math.max(...times);
        
        this.results.performance[path] = {
          average: avgTime,
          minimum: minTime,
          maximum: maxTime,
          samples: times.length
        };
        
        await this.log('info', `Performance for ${path}`, {
          average_ms: avgTime.toFixed(2),
          min_ms: minTime.toFixed(2),
          max_ms: maxTime.toFixed(2)
        });
        
        if (avgTime > 5000) {
          await this.log('warn', `Slow page load detected: ${path} (${avgTime.toFixed(2)}ms)`);
        }
      }
    }
  }

  async testStaticAssets() {
    await this.log('info', 'Starting Static Asset Testing');
    
    const staticAssets = [
      '/_next/static/css',
      '/_next/static/chunks',
      '/favicon.ico',
      '/robots.txt'
    ];
    
    for (const asset of staticAssets) {
      this.results.total_tests++;
      
      const test = await this.makeRequest(asset);
      
      if (test.success && (test.status === 200 || test.status === 404)) {
        if (test.status === 200) {
          this.results.passed++;
          await this.log('info', `Static asset accessible: ${asset}`);
        } else {
          this.results.skipped++;
          await this.log('info', `Static asset not found (may be normal): ${asset}`);
        }
      } else {
        this.results.failed++;
        await this.log('error', `Static asset error: ${asset}`, test);
      }
    }
  }

  async generateReport() {
    this.results.end_time = new Date();
    this.results.duration = this.results.end_time - this.results.start_time;
    
    const report = {
      test_suite: 'BizOSaaS Client Portal Comprehensive Test',
      timestamp: this.results.end_time.toISOString(),
      summary: {
        total_tests: this.results.total_tests,
        passed: this.results.passed,
        failed: this.results.failed,
        skipped: this.results.skipped,
        success_rate: ((this.results.passed / this.results.total_tests) * 100).toFixed(2) + '%',
        duration_ms: this.results.duration
      },
      performance: this.results.performance,
      errors: this.results.errors,
      warnings: this.results.warnings,
      detailed_logs: TEST_RESULTS
    };
    
    // Write report to file
    const reportPath = './test-report-' + new Date().toISOString().slice(0, 19).replace(/:/g, '-') + '.json';
    fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
    
    // Write markdown report
    const mdReport = this.generateMarkdownReport(report);
    const mdReportPath = reportPath.replace('.json', '.md');
    fs.writeFileSync(mdReportPath, mdReport);
    
    console.log('\n' + '='.repeat(80));
    console.log('TEST SUITE SUMMARY');
    console.log('='.repeat(80));
    console.log(`Total Tests: ${report.summary.total_tests}`);
    console.log(`Passed: ${report.summary.passed}`);
    console.log(`Failed: ${report.summary.failed}`);
    console.log(`Skipped: ${report.summary.skipped}`);
    console.log(`Success Rate: ${report.summary.success_rate}`);
    console.log(`Duration: ${(report.summary.duration_ms / 1000).toFixed(2)} seconds`);
    console.log(`Report saved to: ${reportPath}`);
    console.log(`Markdown report: ${mdReportPath}`);
    console.log('='.repeat(80));
    
    return report;
  }

  generateMarkdownReport(report) {
    return `# BizOSaaS Client Portal Test Report

**Generated:** ${report.timestamp}
**Duration:** ${(report.summary.duration_ms / 1000).toFixed(2)} seconds

## Summary

| Metric | Value |
|--------|-------|
| Total Tests | ${report.summary.total_tests} |
| Passed | ${report.summary.passed} |
| Failed | ${report.summary.failed} |
| Skipped | ${report.summary.skipped} |
| Success Rate | ${report.summary.success_rate} |

## Performance Metrics

${Object.entries(report.performance).map(([path, metrics]) => 
  `**${path}**
- Average: ${metrics.average.toFixed(2)}ms
- Min: ${metrics.minimum.toFixed(2)}ms  
- Max: ${metrics.maximum.toFixed(2)}ms`
).join('\n\n')}

## Errors (${report.errors.length})

${report.errors.map(error => 
  `**${error.timestamp}:** ${error.message}
\`\`\`
${JSON.stringify(error.details, null, 2)}
\`\`\``
).join('\n\n')}

## Warnings (${report.warnings.length})

${report.warnings.map(warning => 
  `**${warning.timestamp}:** ${warning.message}`
).join('\n\n')}

## Recommendations

${this.generateRecommendations(report)}
`;
  }

  generateRecommendations(report) {
    const recommendations = [];
    
    if (report.summary.failed > 0) {
      recommendations.push('- Fix failed tests to improve system reliability');
    }
    
    if (Object.values(report.performance).some(p => p.average > 3000)) {
      recommendations.push('- Optimize slow-loading pages for better user experience');
    }
    
    if (report.errors.length > 0) {
      recommendations.push('- Address error conditions for better stability');
    }
    
    if (report.warnings.length > 0) {
      recommendations.push('- Review warnings for potential improvements');
    }
    
    if (report.summary.skipped > report.summary.total_tests * 0.2) {
      recommendations.push('- Investigate skipped tests - may indicate missing functionality');
    }
    
    return recommendations.length > 0 ? recommendations.join('\n') : '- No major issues detected';
  }

  async runFullTestSuite() {
    await this.log('info', 'Starting BizOSaaS Client Portal Comprehensive Test Suite');
    
    try {
      await this.testAuthentication();
      await this.testRoutes();
      await this.testAPIEndpoints();
      await this.testPerformance();
      await this.testStaticAssets();
      
      const report = await this.generateReport();
      return report;
    } catch (error) {
      await this.log('error', 'Test suite execution failed', error);
      throw error;
    }
  }
}

// Run the test suite
if (import.meta.url === `file://${process.argv[1]}`) {
  const runner = new TestRunner();
  runner.runFullTestSuite()
    .then(report => {
      process.exit(report.summary.failed > 0 ? 1 : 0);
    })
    .catch(error => {
      console.error('Test suite failed:', error);
      process.exit(1);
    });
}

export default TestRunner;