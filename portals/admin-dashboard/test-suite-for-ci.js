#!/usr/bin/env node

/**
 * BizOSaaS Admin Dashboard CI/CD Test Suite - CJS version
 */

const axios = require('axios');

const BASE_URL = process.env.TEST_BASE_URL || 'http://localhost:3004';
const TIMEOUT = parseInt(process.env.TEST_TIMEOUT) || 5000;

const CRITICAL_ROUTES = [
    { path: '/', name: 'Admin Root', required: true },
    { path: '/dashboard', name: 'Admin Dashboard', required: true },
    { path: '/dashboard/agents', name: 'AI Agents Manager', required: true },
    { path: '/dashboard/billing/revenue', name: 'Revenue Dashboard', required: true },
    { path: '/tenants', name: 'Tenant Management', required: true },
    { path: '/users', name: 'User Management', required: true },
    { path: '/monitoring', name: 'Resource Monitoring', required: true },
];

const SECONDARY_ROUTES = [
    { path: '/login', name: 'Login Page', required: false },
    { path: '/system-health', name: 'System Health', required: false },
    { path: '/workflows', name: 'Global Workflows', required: false },
    { path: '/security', name: 'Security Audit', required: false },
];

class AdminTestSuite {
    constructor() {
        this.results = {
            passed: 0,
            failed: 0,
            total: 0,
            criticalFailures: [],
            startTime: Date.now()
        };
    }

    async log(level, message) {
        console.log(`[${new Date().toISOString()}] ${level.toUpperCase()}: ${message}`);
    }

    async testRoute(route) {
        try {
            const response = await axios.get(`${BASE_URL}${route.path}`, {
                timeout: TIMEOUT,
                validateStatus: () => true
            });

            const success = response.status === 200;
            this.results.total++;

            if (success) {
                this.results.passed++;
                await this.log('info', `✅ ${route.name}: PASS`);
            } else {
                this.results.failed++;
                await this.log('error', `❌ ${route.name}: FAIL (${response.status})`);
                if (route.required) {
                    this.results.criticalFailures.push(`${route.name}: ${response.status}`);
                }
            }
        } catch (error) {
            this.results.total++;
            this.results.failed++;
            await this.log('error', `❌ ${route.name}: ${error.message}`);
            if (route.required) {
                this.results.criticalFailures.push(`${route.name}: ${error.message}`);
            }
        }
    }

    async runTests() {
        console.log('🚀 BizOSaaS Admin Dashboard Test Suite');
        console.log('='.repeat(50));

        // Health check with 30s timeout for local dev
        try {
            await this.log('info', `Running health check against ${BASE_URL}/login...`);
            const response = await axios.get(`${BASE_URL}/login`, { timeout: 30000 });
            if (response.status === 200) {
                await this.log('info', '✅ Server is responsive (Login page OK)');
            } else {
                throw new Error(`Status ${response.status}`);
            }
        } catch (e) {
            console.error(`💥 Server not reachable at ${BASE_URL}/login: ${e.message}`);
            process.exit(1);
        }

        console.log('\n📋 Testing Critical Routes...');
        for (const route of CRITICAL_ROUTES) await this.testRoute(route);

        console.log('\n📋 Testing Secondary Routes...');
        for (const route of SECONDARY_ROUTES) await this.testRoute(route);

        this.printReport();
    }

    printReport() {
        const successRate = ((this.results.passed / this.results.total) * 100).toFixed(1);
        console.log('\n' + '='.repeat(50));
        console.log(`Total: ${this.results.total} | Passed: ${this.results.passed} | Failed: ${this.results.failed}`);
        console.log(`Success Rate: ${successRate}%`);

        if (this.results.criticalFailures.length > 0) {
            console.log('❌ STATUS: FAILED (Critical routes unavailable)');
            process.exit(1);
        } else {
            console.log('✅ STATUS: PASSED');
            process.exit(0);
        }
    }
}

const suite = new AdminTestSuite();
suite.runTests();
