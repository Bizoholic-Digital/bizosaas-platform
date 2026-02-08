import { test, expect } from '@playwright/test';
import { AxeBuilder } from '@axe-core/playwright';

test.describe('Accessibility Audits', () => {
    test('Dashboard should have no accessibility violations', async ({ page }) => {
        await page.goto('/dashboard');

        // Wait for content to load
        await page.waitForLoadState('networkidle');

        const accessibilityScanResults = await new AxeBuilder({ page }).analyze();

        expect(accessibilityScanResults.violations).toEqual([]);
    });

    test('Connectors page should have no accessibility violations', async ({ page }) => {
        await page.goto('/connectors');
        await page.waitForLoadState('networkidle');

        const accessibilityScanResults = await new AxeBuilder({ page }).analyze();

        expect(accessibilityScanResults.violations).toEqual([]);
    });

    test('Workflows page should have no accessibility violations', async ({ page }) => {
        await page.goto('/workflows');
        await page.waitForLoadState('networkidle');

        const accessibilityScanResults = await new AxeBuilder({ page }).analyze();

        expect(accessibilityScanResults.violations).toEqual([]);
    });
});
