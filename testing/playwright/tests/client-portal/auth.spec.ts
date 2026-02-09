import { test, expect } from '@playwright/test';

/**
 * Client Portal Authentication & Access E2E Tests
 * Tests: E2E-AUTH-001 through E2E-AUTH-009
 */

test.describe('Authentication Flow', () => {

    test('E2E-AUTH-001: MFA enrollment flow', async ({ page }) => {
        // Skip if MFA already enabled
        await page.goto('/settings/security');

        const mfaButton = page.locator('[data-testid="enable-mfa-btn"]');
        if (await mfaButton.isVisible()) {
            await mfaButton.click();

            // Wait for QR code modal
            await expect(page.locator('[data-testid="mfa-qr-code"]')).toBeVisible();

            // Verify backup codes are shown
            await expect(page.locator('[data-testid="backup-codes"]')).toBeVisible();

            // Verify code input is present
            await expect(page.locator('[data-testid="mfa-code-input"]')).toBeVisible();
        }
    });

    test('E2E-AUTH-002: MFA backup codes generation', async ({ page }) => {
        await page.goto('/settings/security');

        const generateCodesBtn = page.locator('[data-testid="generate-backup-codes"]');
        if (await generateCodesBtn.isVisible()) {
            await generateCodesBtn.click();

            // Confirm action
            await page.click('[data-testid="confirm-generate-codes"]');

            // Wait for codes to be generated
            await expect(page.locator('[data-testid="backup-codes-list"]')).toBeVisible();

            // Verify we have 10 codes
            const codes = await page.locator('[data-testid="backup-code"]').count();
            expect(codes).toBe(10);
        }
    });

    test('E2E-AUTH-003: Session expiry and re-authentication', async ({ page, context }) => {
        await page.goto('/dashboard');
        await expect(page.locator('[data-testid="dashboard-content"]')).toBeVisible();

        // Clear session cookies to simulate expiry
        await context.clearCookies();

        // Try to access protected route
        await page.goto('/campaigns');

        // Should redirect to login
        await expect(page).toHaveURL(/.*login.*/);

        // Should show session expired message
        await expect(page.locator('text=/session.*expired/i')).toBeVisible();
    });

    test('E2E-AUTH-004: Remember-me functionality', async ({ page, context }) => {
        // Logout first
        await page.goto('/logout');

        await page.goto('/login');

        // Enable remember me
        await page.check('[data-testid="remember-me-checkbox"]');

        // Login
        await page.fill('[data-testid="email-input"]', process.env.TEST_CLIENT_EMAIL!);
        await page.fill('[data-testid="password-input"]', process.env.TEST_CLIENT_PASSWORD!);
        await page.click('[data-testid="login-submit"]');

        await page.waitForURL('**/dashboard**');

        // Verify persistent cookie is set
        const cookies = await context.cookies();
        const sessionCookie = cookies.find(c => c.name.includes('session') || c.name.includes('auth'));
        expect(sessionCookie).toBeDefined();

        // For remember-me, expiry should be > 24 hours
        if (sessionCookie?.expires) {
            const expiryDays = (sessionCookie.expires * 1000 - Date.now()) / (1000 * 60 * 60 * 24);
            expect(expiryDays).toBeGreaterThan(1);
        }
    });

    test('E2E-AUTH-005: Device revocation', async ({ page }) => {
        await page.goto('/settings/security');

        // View active sessions
        await page.click('[data-testid="view-sessions-btn"]');

        await expect(page.locator('[data-testid="active-sessions-list"]')).toBeVisible();

        // Find other device session (not current)
        const otherSession = page.locator('[data-testid="session-item"]:not([data-current="true"])').first();

        if (await otherSession.isVisible()) {
            await otherSession.locator('[data-testid="revoke-session-btn"]').click();

            // Confirm revocation
            await page.click('[data-testid="confirm-revoke"]');

            // Verify success message
            await expect(page.locator('text=/session.*revoked/i')).toBeVisible();
        }
    });
});

test.describe('RBAC Permissions', () => {

    test('E2E-AUTH-006: Role-based visibility per role', async ({ page }) => {
        await page.goto('/dashboard');

        // Client users should NOT see admin menu
        const adminMenu = page.locator('[data-testid="admin-menu"]');
        await expect(adminMenu).not.toBeVisible();

        // Client users should see these menu items
        await expect(page.locator('[data-testid="nav-dashboard"]')).toBeVisible();
        await expect(page.locator('[data-testid="nav-campaigns"]')).toBeVisible();
        await expect(page.locator('[data-testid="nav-assets"]')).toBeVisible();

        // Billing menu depends on user role
        const userRole = await page.locator('[data-testid="user-role"]').textContent();
        if (userRole?.includes('billing')) {
            await expect(page.locator('[data-testid="nav-billing"]')).toBeVisible();
        }
    });

    test('E2E-AUTH-007: Unauthorized route access attempts', async ({ page }) => {
        // Try to access admin-only routes
        const adminRoutes = [
            '/admin/tenants',
            '/admin/users',
            '/admin/agents',
            '/admin/settings',
        ];

        for (const route of adminRoutes) {
            await page.goto(route);

            // Should redirect to dashboard or show 403
            const url = page.url();
            const isRedirected = !url.includes('/admin');
            const is403 = await page.locator('text=/forbidden|unauthorized|access denied/i').isVisible();

            expect(isRedirected || is403).toBeTruthy();
        }
    });
});

test.describe('Tenant Isolation', () => {

    test('E2E-AUTH-008: Cross-tenant data access prevention', async ({ page }) => {
        // Get current tenant ID from page
        const tenantId = await page.locator('[data-testid="current-tenant-id"]').textContent();

        // Try to access another tenant's resources via API
        const response = await page.request.get('/api/campaigns', {
            headers: {
                'X-Tenant-Id': 'other-tenant-id-12345'
            }
        });

        // Should return 403 or empty/own-tenant data only
        if (response.ok()) {
            const data = await response.json();
            // Verify all returned data belongs to current tenant
            if (Array.isArray(data)) {
                data.forEach(item => {
                    expect(item.tenantId).toBe(tenantId);
                });
            }
        } else {
            expect(response.status()).toBe(403);
        }
    });

    test('E2E-AUTH-009: URL manipulation/IDOR prevention', async ({ page }) => {
        await page.goto('/campaigns');

        // Get a valid campaign ID
        const firstCampaign = page.locator('[data-testid="campaign-row"]').first();
        await firstCampaign.click();

        const validUrl = page.url();
        const campaignId = validUrl.split('/').pop();

        // Try to access a campaign with manipulated ID
        const fakeId = 'idor-test-' + Date.now();
        await page.goto(`/campaigns/${fakeId}`);

        // Should show 404 or redirect
        const is404 = await page.locator('text=/not found|404/i').isVisible();
        const isRedirected = page.url().includes('/campaigns') && !page.url().includes(fakeId);

        expect(is404 || isRedirected).toBeTruthy();
    });
});
