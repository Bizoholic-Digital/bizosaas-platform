import { test, expect, devices } from '@playwright/test';

test.describe('Mobile Responsiveness', () => {
    test.use({ ...devices['iPhone 12'] });

    test('should show hamburger menu on mobile', async ({ page }) => {
        await page.goto('/dashboard');

        // Check if hamburger menu button is visible (assuming it has a specific aria-label or text)
        const menuButton = page.locator('button[aria-label="Toggle menu"], button:has-text("Menu")').first();
        await expect(menuButton).toBeVisible();

        // Open menu
        await menuButton.click();

        // Verify sidebar items are now visible or expanded
        await expect(page.locator('nav')).toBeVisible();
    });

    test('dashboard cards should stack vertically on small screens', async ({ page }) => {
        await page.goto('/dashboard');

        const cards = page.locator('.dashboard-card, .stats-card');
        const count = await cards.count();

        if (count > 1) {
            const firstCardRect = await cards.nth(0).boundingBox();
            const secondCardRect = await cards.nth(1).boundingBox();

            if (firstCardRect && secondCardRect) {
                // In a stacked layout, the Y coordinate of the second card should be greater than the first
                expect(secondCardRect.y).toBeGreaterThan(firstCardRect.y);
                // And they should have similar widths
                expect(Math.abs(firstCardRect.width - secondCardRect.width)).toBeLessThan(50);
            }
        }
    });
});
