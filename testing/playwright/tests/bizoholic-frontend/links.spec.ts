import { test, expect } from '@playwright/test';

test.describe('Bizoholic Frontend Navigation', () => {
    test.beforeEach(async ({ page }) => {
        await page.goto('/');
    });

    test('should have correct metadata', async ({ page }) => {
        await expect(page).toHaveTitle(/BizOSaaS/);
    });

    // Skipped: Requires running backend (Brain Gateway) to fetch valid service links
    test.skip('should navigate to valid service pages', async ({ page }) => {
        // Check main navigation links
        const serviceLinks = await page.getByRole('link', { name: /Learn More/i }).all();

        // Verify at least some service links exist
        expect(serviceLinks.length).toBeGreaterThan(0);

        // Click first service link and verify navigation
        const firstLink = serviceLinks[0];
        const href = await firstLink.getAttribute('href');
        if (href && href.startsWith('/')) {
            await firstLink.click();
            await expect(page).toHaveURL(new RegExp(href));
        }
    });

    test('should display footer links', async ({ page }) => {
        await expect(page.locator('footer')).toBeVisible();
        await expect(page.getByRole('link', { name: /Privacy Policy/i })).toBeVisible();
        await expect(page.getByRole('link', { name: /Terms of Service/i })).toBeVisible();
    });

    test('should verify mobile menu behavior', async ({ page, isMobile }) => {
        if (isMobile) {
            // Mobile only test
            await page.getByLabel('Toggle menu').click();
            await expect(page.locator('nav')).toBeVisible();
        }
    });
});
