import { test, expect } from '@playwright/test';

test.describe('Connector Lifecycle', () => {
    test.beforeEach(async ({ page }) => {
        // Assume auth is handled by global setup or auth storage
        await page.goto('/dashboard');
    });

    test('should allow user to view and search connectors', async ({ page }) => {
        await page.click('text=Connectors');
        await expect(page).toHaveURL(/.*connectors/);

        // Search for a connector
        const searchInput = page.locator('input[placeholder*="Search"]');
        await searchInput.fill('Shopify');

        await expect(page.locator('text=Shopify')).toBeVisible();
    });

    test('should navigate to connector details and back', async ({ page }) => {
        await page.goto('/connectors');

        // Click on Shopify card
        await page.click('text=Shopify');
        await expect(page.locator('h1')).toContainText('Shopify');

        // Go back
        await page.click('button:has-text("Back")');
        await expect(page).toHaveURL(/.*connectors/);
    });

    test('should show connector sync history', async ({ page }) => {
        await page.goto('/connectors');
        await page.click('text=Shopify');

        // Check for sync history table
        await expect(page.locator('text=Sync History')).toBeVisible();
        await expect(page.locator('table')).toBeVisible();
    });
});
