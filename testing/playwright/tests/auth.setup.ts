import { test as setup, expect } from '@playwright/test';
import path from 'path';

const ADMIN_AUTH_FILE = path.join(__dirname, '../.auth/admin-user.json');
const CLIENT_AUTH_FILE = path.join(__dirname, '../.auth/client-user.json');

/**
 * Authentication setup for E2E tests
 * Creates authenticated sessions for different user roles
 */

setup.describe('Authentication Setup', () => {

    setup('authenticate as admin user', async ({ page }) => {
        const adminEmail = process.env.TEST_ADMIN_EMAIL || 'admin@bizoholic.test';
        const adminPassword = process.env.TEST_ADMIN_PASSWORD || 'TestAdmin123!';

        // Navigate to admin login
        await page.goto(process.env.ADMIN_DASHBOARD_URL || 'http://localhost:3004/login');

        // Wait for login form
        await page.waitForSelector('[data-testid="login-form"]', { timeout: 10000 });

        // Fill credentials
        await page.fill('[data-testid="email-input"]', adminEmail);
        await page.fill('[data-testid="password-input"]', adminPassword);

        // Submit login
        await page.click('[data-testid="login-submit"]');

        // Wait for successful redirect to dashboard
        await page.waitForURL('**/dashboard**', { timeout: 30000 });

        // Verify we're authenticated
        await expect(page.locator('[data-testid="user-menu"]')).toBeVisible();

        // Save auth state
        await page.context().storageState({ path: ADMIN_AUTH_FILE });

        console.log('✅ Admin authentication saved');
    });

    setup('authenticate as client user', async ({ page }) => {
        const clientEmail = process.env.TEST_CLIENT_EMAIL || 'client@bizoholic.test';
        const clientPassword = process.env.TEST_CLIENT_PASSWORD || 'TestClient123!';

        // Navigate to client portal login
        await page.goto(process.env.CLIENT_PORTAL_URL || 'http://localhost:3003/login');

        // Wait for login form
        await page.waitForSelector('[data-testid="login-form"]', { timeout: 10000 });

        // Fill credentials
        await page.fill('[data-testid="email-input"]', clientEmail);
        await page.fill('[data-testid="password-input"]', clientPassword);

        // Submit login
        await page.click('[data-testid="login-submit"]');

        // Wait for successful redirect to dashboard
        await page.waitForURL('**/dashboard**', { timeout: 30000 });

        // Verify we're authenticated
        await expect(page.locator('[data-testid="user-menu"]')).toBeVisible();

        // Save auth state
        await page.context().storageState({ path: CLIENT_AUTH_FILE });

        console.log('✅ Client authentication saved');
    });

    setup('authenticate as billing admin', async ({ page }) => {
        const billingEmail = process.env.TEST_BILLING_EMAIL || 'billing@bizoholic.test';
        const billingPassword = process.env.TEST_BILLING_PASSWORD || 'TestBilling123!';

        const BILLING_AUTH_FILE = path.join(__dirname, '../.auth/billing-user.json');

        await page.goto(process.env.CLIENT_PORTAL_URL || 'http://localhost:3003/login');
        await page.waitForSelector('[data-testid="login-form"]', { timeout: 10000 });

        await page.fill('[data-testid="email-input"]', billingEmail);
        await page.fill('[data-testid="password-input"]', billingPassword);
        await page.click('[data-testid="login-submit"]');

        await page.waitForURL('**/dashboard**', { timeout: 30000 });
        await expect(page.locator('[data-testid="user-menu"]')).toBeVisible();

        await page.context().storageState({ path: BILLING_AUTH_FILE });

        console.log('✅ Billing admin authentication saved');
    });

    setup('authenticate as readonly user', async ({ page }) => {
        const readonlyEmail = process.env.TEST_READONLY_EMAIL || 'readonly@bizoholic.test';
        const readonlyPassword = process.env.TEST_READONLY_PASSWORD || 'TestReadonly123!';

        const READONLY_AUTH_FILE = path.join(__dirname, '../.auth/readonly-user.json');

        await page.goto(process.env.CLIENT_PORTAL_URL || 'http://localhost:3003/login');
        await page.waitForSelector('[data-testid="login-form"]', { timeout: 10000 });

        await page.fill('[data-testid="email-input"]', readonlyEmail);
        await page.fill('[data-testid="password-input"]', readonlyPassword);
        await page.click('[data-testid="login-submit"]');

        await page.waitForURL('**/dashboard**', { timeout: 30000 });
        await expect(page.locator('[data-testid="user-menu"]')).toBeVisible();

        await page.context().storageState({ path: READONLY_AUTH_FILE });

        console.log('✅ Readonly user authentication saved');
    });
});
