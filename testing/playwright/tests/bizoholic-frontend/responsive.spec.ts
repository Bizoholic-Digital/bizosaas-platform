import { test, expect } from '@playwright/test';

test.describe('Bizoholic Responsive UI', () => {
    test.beforeEach(async ({ page }) => {
        await page.goto('/');
    });

    test('should show hamburger menu on mobile', async ({ page, isMobile }) => {
        if (isMobile) {
            const menuButton = page.getByLabel('Toggle menu'); // Assuming aria-label
            await expect(menuButton).toBeVisible();

            await menuButton.click();
            const nav = page.locator('nav'); // Adjust selector as needed based on implementation
            await expect(nav).toBeVisible();
        } else {
            // On desktop, menu button should be hidden or non-existent
            const menuButton = page.getByLabel('Toggle menu');
            await expect(menuButton).not.toBeVisible();
        }
    });

    test('should display horizontal scroll areas on mobile', async ({ page, isMobile }) => {
        if (isMobile) {
            // Check for horizontal scroll classes or behavior
            const scrollContainers = await page.locator('.overflow-x-auto').all();
            expect(scrollContainers.length).toBeGreaterThan(0);

            // Verify first container is visible
            await expect(scrollContainers[0]).toBeVisible();
        }
    });

    test('should adjust header layout on mobile', async ({ page, isMobile }) => {
        const header = page.locator('header');
        await expect(header).toBeVisible();

        // Check logo visibility
        const logo = header.locator('a[href="/"]').first();
        await expect(logo).toBeVisible();
    });
});
