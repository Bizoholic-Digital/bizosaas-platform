#!/usr/bin/env node

/**
 * BizOSaaS Client Portal CI/CD Test Suite
 * 
 * Automated test suite for continuous integration
 * Run with: npm test (after adding to package.json scripts)
 */

import axios from 'axios';
import fs from 'fs';

const BASE_URL = process.env.TEST_BASE_URL || 'http://localhost:3000';
const TIMEOUT = parseInt(process.env.TEST_TIMEOUT) || 5000;

// Critical routes that must work for CI/CD to pass
const CRITICAL_ROUTES = [
  { path: '/', name: 'Dashboard Home', required: true },
  { path: '/analytics', name: 'Analytics Dashboard', required: true },
  { path: '/leads', name: 'Lead Management', required: true },
  { path: '/orders', name: 'Order Management', required: true },
  { path: '/crm', name: 'CRM Dashboard', required: true },
  { path: '/crm/contacts', name: 'CRM Contacts', required: true },
  { path: '/content', name: 'Content Management', required: true },
];

// Important but non-critical routes
const SECONDARY_ROUTES = [
  { path: '/login', name: 'Login Page', required: false },
  { path: '/settings', name: 'Settings', required: false },
  { path: '/chat', name: 'AI Assistant', required: false },
  { path: '/directory', name: 'Business Directory', required: false },
];

// API endpoints to validate
const CRITICAL_APIS = [
  { path: '/api/brain/analytics/dashboard', name: 'Analytics API' },
  { path: '/api/brain/wagtail/pages', name: 'Wagtail API' },
  { path: '/api/brain/integrations/overview', name: 'Integrations API' },
];

class CITestSuite {
  constructor() {
    this.results = {
      passed: 0,
      failed: 0,
      skipped: 0,
      total: 0,
      criticalFailures: [],
      warnings: [],
      startTime: Date.now()
    };
  }

  async log(level, message, details = null) {
    const timestamp = new Date().toISOString();
    console.log(`[${timestamp}] ${level.toUpperCase()}: ${message}`);
    if (details && process.env.VERBOSE) {
      console.log('Details:', JSON.stringify(details, null, 2));
    }
  }

  async testRoute(route) {
    try {
      const response = await axios.get(`${BASE_URL}${route.path}`, {
        timeout: TIMEOUT,
        validateStatus: () => true
      });

      const result = {
        ...route,
        status: response.status,
        success: response.status === 200,
        duration: response.config.timeout
      };

      this.results.total++;

      if (result.success) {
        this.results.passed++;
        await this.log('info', `✅ ${route.name}: PASS`);
      } else {
        this.results.failed++;
        await this.log('error', `❌ ${route.name}: FAIL (${response.status})`);
        
        if (route.required) {
          this.results.criticalFailures.push(`${route.name}: ${response.status}`);
        }
      }

      return result;
    } catch (error) {
      this.results.total++;
      this.results.failed++;
      
      const errorMsg = `${route.name}: ${error.code || error.message}`;
      await this.log('error', `❌ ${errorMsg}`);
      
      if (route.required) {
        this.results.criticalFailures.push(errorMsg);
      }

      return { ...route, error: error.message, success: false };
    }
  }

  async testAPI(api) {
    try {
      const response = await axios.get(`${BASE_URL}${api.path}`, {
        timeout: TIMEOUT,
        validateStatus: () => true
      });

      const success = response.status === 200;
      this.results.total++;

      if (success) {
        this.results.passed++;
        await this.log('info', `✅ API ${api.name}: PASS`);
      } else {
        this.results.failed++;
        await this.log('error', `❌ API ${api.name}: FAIL (${response.status})`);
        this.results.warnings.push(`API ${api.name}: Status ${response.status}`);
      }

      return { ...api, status: response.status, success };
    } catch (error) {
      this.results.total++;
      this.results.failed++;
      await this.log('error', `❌ API ${api.name}: ${error.message}`);
      this.results.warnings.push(`API ${api.name}: ${error.message}`);
      return { ...api, error: error.message, success: false };
    }
  }

  async runHealthCheck() {
    await this.log('info', 'Running application health check...');
    
    try {
      const response = await axios.get(BASE_URL, { timeout: 10000 });
      if (response.status === 200) {
        await this.log('info', '✅ Application is responding');
        return true;
      } else {
        await this.log('error', `❌ Application health check failed: ${response.status}`);
        return false;
      }
    } catch (error) {
      await this.log('error', `❌ Application is not accessible: ${error.message}`);
      return false;
    }
  }

  async runTests() {
    console.log('🚀 BizOSaaS Client Portal CI/CD Test Suite');
    console.log('=' .repeat(60));
    console.log(`Base URL: ${BASE_URL}`);
    console.log(`Timeout: ${TIMEOUT}ms`);
    console.log('');

    // Health check first
    const healthy = await this.runHealthCheck();
    if (!healthy) {
      console.log('💥 CRITICAL: Application is not accessible. Aborting tests.');
      process.exit(1);
    }

    console.log('\n📋 Testing Critical Routes...');
    console.log('-'.repeat(40));
    
    for (const route of CRITICAL_ROUTES) {
      await this.testRoute(route);
    }

    console.log('\n📋 Testing Secondary Routes...');
    console.log('-'.repeat(40));
    
    for (const route of SECONDARY_ROUTES) {
      await this.testRoute(route);
    }

    console.log('\n🔌 Testing API Endpoints...');
    console.log('-'.repeat(40));
    
    for (const api of CRITICAL_APIS) {
      await this.testAPI(api);
    }

    return this.generateReport();
  }

  generateReport() {
    const duration = Date.now() - this.results.startTime;
    const successRate = ((this.results.passed / this.results.total) * 100).toFixed(1);

    console.log('\n' + '='.repeat(60));
    console.log('📊 CI/CD TEST RESULTS');
    console.log('='.repeat(60));
    console.log(`Total Tests: ${this.results.total}`);
    console.log(`Passed: ${this.results.passed}`);
    console.log(`Failed: ${this.results.failed}`);
    console.log(`Success Rate: ${successRate}%`);
    console.log(`Duration: ${(duration/1000).toFixed(1)}s`);

    const report = {
      timestamp: new Date().toISOString(),
      baseUrl: BASE_URL,
      timeout: TIMEOUT,
      summary: {
        total: this.results.total,
        passed: this.results.passed,
        failed: this.results.failed,
        successRate: parseFloat(successRate),
        duration
      },
      criticalFailures: this.results.criticalFailures,
      warnings: this.results.warnings
    };

    // Determine CI/CD result
    const hasCriticalFailures = this.results.criticalFailures.length > 0;
    const minimumSuccessRate = 70; // 70% minimum for CI/CD pass
    const passesMinimumRate = parseFloat(successRate) >= minimumSuccessRate;

    if (hasCriticalFailures) {
      console.log('\n💥 CRITICAL FAILURES DETECTED:');
      this.results.criticalFailures.forEach(failure => {
        console.log(`  - ${failure}`);
      });
      report.cicdResult = 'FAIL';
      report.failureReason = 'Critical route failures';
    } else if (!passesMinimumRate) {
      console.log('\n⚠️  SUCCESS RATE BELOW MINIMUM THRESHOLD');
      console.log(`Required: ${minimumSuccessRate}%, Actual: ${successRate}%`);
      report.cicdResult = 'FAIL';
      report.failureReason = `Success rate ${successRate}% below minimum ${minimumSuccessRate}%`;
    } else {
      console.log('\n✅ CI/CD TESTS PASSED');
      report.cicdResult = 'PASS';
    }

    if (this.results.warnings.length > 0) {
      console.log('\n⚠️  WARNINGS:');
      this.results.warnings.forEach(warning => {
        console.log(`  - ${warning}`);
      });
    }

    // Save report
    fs.writeFileSync('ci-test-results.json', JSON.stringify(report, null, 2));
    console.log('\n📄 Report saved to: ci-test-results.json');

    return report;
  }
}

// Main execution
if (import.meta.url === `file://${process.argv[1]}`) {
  const testSuite = new CITestSuite();
  testSuite.runTests()
    .then(report => {
      // Exit with appropriate code for CI/CD
      const exitCode = report.cicdResult === 'PASS' ? 0 : 1;
      console.log(`\n🏁 Exiting with code: ${exitCode}`);
      process.exit(exitCode);
    })
    .catch(error => {
      console.error('💥 Test suite execution failed:', error);
      process.exit(1);
    });
}

export default CITestSuite;