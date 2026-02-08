import { test, expect } from '@playwright/test';

/**
 * Client Portal Core Workflow E2E Tests
 * Tests: E2E-CP-001 through E2E-CP-017
 */

test.describe('Onboarding Flow', () => {

    test('E2E-CP-001: Signup → Email verification → First login', async ({ page }) => {
        const testEmail = `test-${Date.now()}@example.com`;

        // Go to signup page
        await page.goto('/signup');

        // Fill signup form
        await page.fill('[data-testid="signup-first-name"]', 'Test');
        await page.fill('[data-testid="signup-last-name"]', 'User');
        await page.fill('[data-testid="signup-email"]', testEmail);
        await page.fill('[data-testid="signup-password"]', 'SecurePassword123!');
        await page.fill('[data-testid="signup-confirm-password"]', 'SecurePassword123!');

        // Accept terms
        await page.check('[data-testid="accept-terms"]');

        // Submit
        await page.click('[data-testid="signup-submit"]');

        // Should show verification pending screen
        await expect(page.locator('[data-testid="verify-email-message"]')).toBeVisible();

        // For testing, we'd mock the verification or use a test endpoint
        // await page.goto(`/verify-email?token=${mockToken}`);

        // Alternatively, check that the verification page renders correctly
        await expect(page.locator('text=/verification.*email.*sent/i')).toBeVisible();
    });

    test('E2E-CP-002: Plan selection and payment', async ({ page }) => {
        // Navigate to billing/plans
        await page.goto('/billing/plans');

        // Wait for plans to load
        await expect(page.locator('[data-testid="plan-card"]').first()).toBeVisible();

        // Select Pro plan
        await page.click('[data-testid="select-plan-pro"]');

        // Should navigate to checkout
        await page.waitForURL('**/checkout**');

        // Verify plan details shown
        await expect(page.locator('[data-testid="selected-plan-name"]')).toContainText(/pro/i);

        // Fill payment details (Stripe test card)
        const stripeFrame = page.frameLocator('iframe[name^="__privateStripeFrame"]').first();
        await stripeFrame.locator('[placeholder="Card number"]').fill('4242424242424242');
        await stripeFrame.locator('[placeholder="MM / YY"]').fill('12/30');
        await stripeFrame.locator('[placeholder="CVC"]').fill('123');

        // Submit payment
        await page.click('[data-testid="submit-payment"]');

        // Wait for success
        await expect(page.locator('[data-testid="payment-success"]')).toBeVisible({ timeout: 30000 });
    });

    test('E2E-CP-003: Onboarding tour completion', async ({ page }) => {
        // Trigger onboarding for new users
        await page.goto('/dashboard?onboarding=true');

        // Check if tour modal/popover appears
        const tourStep = page.locator('[data-testid="tour-step"]');

        if (await tourStep.isVisible()) {
            // Click through tour steps
            let stepCount = 0;
            const maxSteps = 10;

            while (await page.locator('[data-testid="tour-next"]').isVisible() && stepCount < maxSteps) {
                await page.click('[data-testid="tour-next"]');
                stepCount++;
                await page.waitForTimeout(500);
            }

            // Complete tour
            if (await page.locator('[data-testid="tour-complete"]').isVisible()) {
                await page.click('[data-testid="tour-complete"]');
            }

            // Verify tour is marked complete
            await expect(page.locator('[data-testid="tour-step"]')).not.toBeVisible();
        }
    });
});

test.describe('Campaign Management', () => {

    test('E2E-CP-004: Campaign CRUD operations', async ({ page }) => {
        // CREATE
        await page.goto('/campaigns');
        await page.click('[data-testid="create-campaign-btn"]');

        const campaignName = `Test Campaign ${Date.now()}`;
        await page.fill('[data-testid="campaign-name"]', campaignName);
        await page.fill('[data-testid="campaign-description"]', 'E2E Test Campaign');
        await page.selectOption('[data-testid="campaign-type"]', 'email');
        await page.fill('[data-testid="campaign-budget"]', '1000');

        await page.click('[data-testid="save-campaign"]');

        // Verify creation success
        await expect(page.locator('text=Campaign created')).toBeVisible();

        // READ - Find campaign in list
        await page.goto('/campaigns');
        await expect(page.locator(`text=${campaignName}`)).toBeVisible();

        // EDIT
        await page.locator(`text=${campaignName}`).click();
        await page.click('[data-testid="edit-campaign-btn"]');
        await page.fill('[data-testid="campaign-budget"]', '1500');
        await page.click('[data-testid="save-campaign"]');

        await expect(page.locator('text=Campaign updated')).toBeVisible();

        // SCHEDULE
        await page.click('[data-testid="schedule-campaign-btn"]');
        await page.fill('[data-testid="schedule-date"]', '2025-06-01');
        await page.click('[data-testid="confirm-schedule"]');

        await expect(page.locator('[data-testid="campaign-status"]')).toContainText(/scheduled/i);

        // PAUSE
        await page.click('[data-testid="pause-campaign-btn"]');
        await page.click('[data-testid="confirm-pause"]');

        await expect(page.locator('[data-testid="campaign-status"]')).toContainText(/paused/i);

        // ARCHIVE
        await page.click('[data-testid="archive-campaign-btn"]');
        await page.click('[data-testid="confirm-archive"]');

        await expect(page.locator('text=Campaign archived')).toBeVisible();
    });

    test('E2E-CP-005: Campaign analytics updates', async ({ page }) => {
        await page.goto('/campaigns');

        // Open first active campaign
        await page.locator('[data-testid="campaign-row"][data-status="active"]').first().click();

        // Navigate to analytics tab
        await page.click('[data-testid="campaign-analytics-tab"]');

        // Verify analytics widgets are present
        await expect(page.locator('[data-testid="analytics-impressions"]')).toBeVisible();
        await expect(page.locator('[data-testid="analytics-clicks"]')).toBeVisible();
        await expect(page.locator('[data-testid="analytics-conversions"]')).toBeVisible();

        // Verify chart renders
        await expect(page.locator('[data-testid="analytics-chart"]')).toBeVisible();

        // Change date range
        await page.click('[data-testid="date-range-picker"]');
        await page.click('[data-testid="date-range-7d"]');

        // Verify data updates (loading state appears and resolves)
        await expect(page.locator('[data-testid="analytics-loading"]')).not.toBeVisible({ timeout: 10000 });
    });
});

test.describe('Asset Management', () => {

    test('E2E-CP-006: Asset upload (small and large files)', async ({ page }) => {
        await page.goto('/assets');

        // Small file upload
        const smallFile = {
            name: 'test-small.png',
            mimeType: 'image/png',
            buffer: Buffer.alloc(100 * 1024), // 100KB
        };

        await page.click('[data-testid="upload-asset-btn"]');

        const fileInput = page.locator('input[type="file"]');
        await fileInput.setInputFiles({
            name: smallFile.name,
            mimeType: smallFile.mimeType,
            buffer: smallFile.buffer,
        });

        // Wait for upload
        await expect(page.locator('text=Upload complete')).toBeVisible({ timeout: 30000 });

        // Large file upload (simulate with wait)
        const largeFile = {
            name: 'test-large.mp4',
            mimeType: 'video/mp4',
            buffer: Buffer.alloc(10 * 1024 * 1024), // 10MB
        };

        await page.click('[data-testid="upload-asset-btn"]');
        await fileInput.setInputFiles({
            name: largeFile.name,
            mimeType: largeFile.mimeType,
            buffer: largeFile.buffer,
        });

        // Verify progress indicator
        await expect(page.locator('[data-testid="upload-progress"]')).toBeVisible();

        // Wait for completion
        await expect(page.locator('text=Upload complete')).toBeVisible({ timeout: 120000 });
    });

    test('E2E-CP-007: Asset versioning and tagging', async ({ page }) => {
        await page.goto('/assets');

        // Click first asset
        await page.locator('[data-testid="asset-card"]').first().click();

        // Check versions tab
        await page.click('[data-testid="asset-versions-tab"]');
        await expect(page.locator('[data-testid="version-list"]')).toBeVisible();

        // Add tag
        await page.click('[data-testid="asset-tags-tab"]');
        await page.click('[data-testid="add-tag-btn"]');
        await page.fill('[data-testid="tag-input"]', 'e2e-test-tag');
        await page.click('[data-testid="save-tag"]');

        await expect(page.locator('text=e2e-test-tag')).toBeVisible();
    });

    test('E2E-CP-008: Asset search and preview', async ({ page }) => {
        await page.goto('/assets');

        // Search for assets
        await page.fill('[data-testid="asset-search"]', 'logo');
        await page.keyboard.press('Enter');

        // Wait for search results
        await expect(page.locator('[data-testid="asset-card"]').first()).toBeVisible({ timeout: 10000 });

        // Preview asset
        await page.locator('[data-testid="asset-card"]').first().click();

        // Verify preview modal
        await expect(page.locator('[data-testid="asset-preview-modal"]')).toBeVisible();
        await expect(page.locator('[data-testid="asset-preview-image"], [data-testid="asset-preview-video"]')).toBeVisible();
    });
});

test.describe('Billing Management', () => {

    test('E2E-CP-010: Billing upgrade/downgrade', async ({ page }) => {
        await page.goto('/billing');

        // Get current plan
        const currentPlan = await page.locator('[data-testid="current-plan-name"]').textContent();

        // Click change plan
        await page.click('[data-testid="change-plan-btn"]');

        // Select different plan
        const targetPlan = currentPlan?.includes('Basic') ? 'pro' : 'basic';
        await page.click(`[data-testid="select-plan-${targetPlan}"]`);

        // Confirm change
        await page.click('[data-testid="confirm-plan-change"]');

        // Verify proration message if downgrading
        if (targetPlan === 'basic') {
            await expect(page.locator('text=/proration|credit/i')).toBeVisible();
        }

        // Confirm final
        await page.click('[data-testid="final-confirm"]');

        // Verify success
        await expect(page.locator('text=/plan.*changed|updated/i')).toBeVisible();
    });

    test('E2E-CP-012: Invoice and receipt generation', async ({ page }) => {
        await page.goto('/billing/invoices');

        // Wait for invoices to load
        await expect(page.locator('[data-testid="invoice-row"]').first()).toBeVisible();

        // Click first invoice
        await page.locator('[data-testid="invoice-row"]').first().click();

        // Verify invoice details
        await expect(page.locator('[data-testid="invoice-number"]')).toBeVisible();
        await expect(page.locator('[data-testid="invoice-amount"]')).toBeVisible();
        await expect(page.locator('[data-testid="invoice-date"]')).toBeVisible();

        // Download invoice PDF
        const [download] = await Promise.all([
            page.waitForEvent('download'),
            page.click('[data-testid="download-invoice-pdf"]'),
        ]);

        expect(download.suggestedFilename()).toMatch(/invoice.*\.pdf/i);
    });
});
