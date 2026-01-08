import { defineConfig, devices } from '@playwright/test';
import dotenv from 'dotenv';
import path from 'path';

// Load environment-specific config
dotenv.config({ path: path.resolve(__dirname, '.env.test') });

/**
 * BizOSaaS Production Readiness E2E Test Configuration
 * @see https://playwright.dev/docs/test-configuration
 */
export default defineConfig({
    testDir: './tests',

    /* Run tests in files in parallel */
    fullyParallel: true,

    /* Fail the build on CI if you accidentally left test.only in the source code */
    forbidOnly: !!process.env.CI,

    /* Retry on CI only */
    retries: process.env.CI ? 2 : 0,

    /* Opt out of parallel tests on CI */
    workers: process.env.CI ? 1 : undefined,

    /* Reporter to use */
    reporter: [
        ['html', { outputFolder: 'reports/html' }],
        ['json', { outputFile: 'reports/results.json' }],
        ['junit', { outputFile: 'reports/junit.xml' }],
        process.env.CI ? ['github'] : ['list']
    ],

    /* Shared settings for all the projects below */
    use: {
        /* Base URL to use in actions like `await page.goto('/')` */
        baseURL: process.env.BASE_URL || 'http://localhost:3003',

        /* Collect trace when retrying the failed test */
        trace: 'on-first-retry',

        /* Capture screenshot on failure */
        screenshot: 'only-on-failure',

        /* Record video on failure */
        video: 'on-first-retry',

        /* Maximum time each action can take */
        actionTimeout: 10000,

        /* Maximum time for navigation */
        navigationTimeout: 30000,
    },

    /* Configure projects for major browsers */
    projects: [
        // Setup project for authentication
        {
            name: 'setup',
            testMatch: /.*\.setup\.ts/,
        },

        // Client Portal Tests
        {
            name: 'client-portal-chromium',
            use: {
                ...devices['Desktop Chrome'],
                baseURL: process.env.CLIENT_PORTAL_URL || 'http://localhost:3003',
                storageState: '.auth/client-user.json',
            },
            dependencies: ['setup'],
            testDir: './tests/client-portal',
        },
        {
            name: 'client-portal-firefox',
            use: {
                ...devices['Desktop Firefox'],
                baseURL: process.env.CLIENT_PORTAL_URL || 'http://localhost:3003',
                storageState: '.auth/client-user.json',
            },
            dependencies: ['setup'],
            testDir: './tests/client-portal',
        },
        {
            name: 'client-portal-webkit',
            use: {
                ...devices['Desktop Safari'],
                baseURL: process.env.CLIENT_PORTAL_URL || 'http://localhost:3003',
                storageState: '.auth/client-user.json',
            },
            dependencies: ['setup'],
            testDir: './tests/client-portal',
        },

        // Admin Dashboard Tests
        {
            name: 'admin-dashboard-chromium',
            use: {
                ...devices['Desktop Chrome'],
                baseURL: process.env.ADMIN_DASHBOARD_URL || 'http://localhost:3004',
                storageState: '.auth/admin-user.json',
            },
            dependencies: ['setup'],
            testDir: './tests/admin-dashboard',
        },

        // Mobile Tests
        {
            name: 'mobile-chrome',
            use: {
                ...devices['Pixel 5'],
                baseURL: process.env.CLIENT_PORTAL_URL || 'http://localhost:3003',
                storageState: '.auth/client-user.json',
            },
            dependencies: ['setup'],
            testDir: './tests/client-portal',
        },
        {
            name: 'mobile-safari',
            use: {
                ...devices['iPhone 12'],
                baseURL: process.env.CLIENT_PORTAL_URL || 'http://localhost:3003',
                storageState: '.auth/client-user.json',
            },
            dependencies: ['setup'],
            testDir: './tests/client-portal',
        },

        // Security Tests (no auth)
        {
            name: 'security',
            use: {
                ...devices['Desktop Chrome'],
            },
            testDir: './tests/security',
        },

        // Accessibility Tests
        {
            name: 'accessibility',
            use: {
                ...devices['Desktop Chrome'],
                storageState: '.auth/client-user.json',
            },
            dependencies: ['setup'],
            testDir: './tests/accessibility',
        },
    ],

    /* Run your local dev server before starting the tests */
    webServer: process.env.CI ? undefined : [
        {
            command: 'cd ../../portals/client-portal && npm run dev',
            url: 'http://localhost:3003',
            reuseExistingServer: !process.env.CI,
            timeout: 120000,
        },
        {
            command: 'cd ../../portals/admin-dashboard && npm run dev',
            url: 'http://localhost:3004',
            reuseExistingServer: !process.env.CI,
            timeout: 120000,
        },
    ],

    /* Global setup and teardown */
    globalSetup: require.resolve('./global-setup.ts'),
    globalTeardown: require.resolve('./global-teardown.ts'),

    /* Timeout for each test */
    timeout: 60000,

    /* Expect timeout */
    expect: {
        timeout: 10000,
    },
});
