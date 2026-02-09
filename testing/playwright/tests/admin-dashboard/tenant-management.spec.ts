import { test, expect } from '@playwright/test';

/**
 * Admin Dashboard Tenant Management E2E Tests
 * Tests: E2E-AD-001 through E2E-AD-008
 */

test.describe('Tenant Management', () => {

    test('E2E-AD-001: Tenant provisioning', async ({ page }) => {
        await page.goto('/admin/tenants');

        // Click create tenant
        await page.click('[data-testid="create-tenant-btn"]');

        // Fill tenant details
        const tenantName = `E2E Test Tenant ${Date.now()}`;
        await page.fill('[data-testid="tenant-name"]', tenantName);
        await page.fill('[data-testid="tenant-slug"]', `e2e-test-${Date.now()}`);
        await page.fill('[data-testid="tenant-admin-email"]', `admin-${Date.now()}@test.com`);

        // Select plan
        await page.selectOption('[data-testid="tenant-plan"]', 'pro');

        // Submit
        await page.click('[data-testid="create-tenant-submit"]');

        // Verify success
        await expect(page.locator('text=Tenant created successfully')).toBeVisible();

        // Verify tenant appears in list
        await page.goto('/admin/tenants');
        await expect(page.locator(`text=${tenantName}`)).toBeVisible();
    });

    test('E2E-AD-002: Plan entitlement management', async ({ page }) => {
        await page.goto('/admin/tenants');

        // Click first tenant
        await page.locator('[data-testid="tenant-row"]').first().click();

        // Navigate to entitlements tab
        await page.click('[data-testid="tab-entitlements"]');

        // Verify current entitlements
        await expect(page.locator('[data-testid="entitlement-max-users"]')).toBeVisible();
        await expect(page.locator('[data-testid="entitlement-max-campaigns"]')).toBeVisible();

        // Edit entitlements
        await page.click('[data-testid="edit-entitlements-btn"]');

        // Change max users
        await page.fill('[data-testid="input-max-users"]', '50');

        // Toggle feature
        await page.click('[data-testid="toggle-ai-agents"]');

        // Save
        await page.click('[data-testid="save-entitlements"]');

        // Verify success
        await expect(page.locator('text=Entitlements updated')).toBeVisible();
    });

    test('E2E-AD-003: Tenant suspension/reactivation', async ({ page }) => {
        await page.goto('/admin/tenants');

        // Find active tenant
        const activeTenant = page.locator('[data-testid="tenant-row"][data-status="active"]').first();
        await activeTenant.click();

        // Suspend tenant
        await page.click('[data-testid="suspend-tenant-btn"]');

        // Confirm suspension with reason
        await page.fill('[data-testid="suspension-reason"]', 'E2E test suspension');
        await page.click('[data-testid="confirm-suspend"]');

        // Verify status changed
        await expect(page.locator('[data-testid="tenant-status"]')).toContainText(/suspended/i);

        // Reactivate
        await page.click('[data-testid="reactivate-tenant-btn"]');
        await page.click('[data-testid="confirm-reactivate"]');

        // Verify status changed back
        await expect(page.locator('[data-testid="tenant-status"]')).toContainText(/active/i);
    });

    test('E2E-AD-004: Tenant data export', async ({ page }) => {
        await page.goto('/admin/tenants');

        // Select tenant
        await page.locator('[data-testid="tenant-row"]').first().click();

        // Navigate to data export
        await page.click('[data-testid="tab-data-export"]');

        // Select export options
        await page.check('[data-testid="export-users"]');
        await page.check('[data-testid="export-campaigns"]');
        await page.check('[data-testid="export-assets"]');

        // Select format
        await page.selectOption('[data-testid="export-format"]', 'json');

        // Initiate export
        const [download] = await Promise.all([
            page.waitForEvent('download'),
            page.click('[data-testid="start-export"]'),
        ]);

        // Verify download
        expect(download.suggestedFilename()).toMatch(/tenant.*export.*\.json/i);

        // Verify export appears in history
        await expect(page.locator('[data-testid="export-history-item"]').first()).toBeVisible();
    });
});

test.describe('User Management', () => {

    test('E2E-AD-005: User invite flow', async ({ page }) => {
        await page.goto('/admin/users');

        // Click invite user
        await page.click('[data-testid="invite-user-btn"]');

        // Fill invite form
        const inviteEmail = `invited-${Date.now()}@test.com`;
        await page.fill('[data-testid="invite-email"]', inviteEmail);
        await page.fill('[data-testid="invite-first-name"]', 'Invited');
        await page.fill('[data-testid="invite-last-name"]', 'User');

        // Select role
        await page.selectOption('[data-testid="invite-role"]', 'client');

        // Select tenant
        await page.selectOption('[data-testid="invite-tenant"]', { index: 1 });

        // Send invite
        await page.click('[data-testid="send-invite"]');

        // Verify success
        await expect(page.locator('text=Invitation sent')).toBeVisible();

        // Verify pending invite appears
        await page.click('[data-testid="tab-pending-invites"]');
        await expect(page.locator(`text=${inviteEmail}`)).toBeVisible();
    });

    test('E2E-AD-006: User role change', async ({ page }) => {
        await page.goto('/admin/users');

        // Find a user
        await page.locator('[data-testid="user-row"]').first().click();

        // Get current role
        const currentRole = await page.locator('[data-testid="user-current-role"]').textContent();

        // Change role
        await page.click('[data-testid="change-role-btn"]');

        // Select new role (different from current)
        const newRole = currentRole?.includes('client') ? 'manager' : 'client';
        await page.selectOption('[data-testid="new-role-select"]', newRole);

        // Confirm change
        await page.fill('[data-testid="role-change-reason"]', 'E2E test role change');
        await page.click('[data-testid="confirm-role-change"]');

        // Verify success
        await expect(page.locator('text=Role updated')).toBeVisible();

        // Verify audit log entry
        await page.click('[data-testid="tab-audit-log"]');
        await expect(page.locator('[data-testid="audit-entry"]').first()).toContainText(/role.*change/i);
    });

    test('E2E-AD-007: User deactivation', async ({ page }) => {
        await page.goto('/admin/users');

        // Find active user
        const activeUser = page.locator('[data-testid="user-row"][data-status="active"]').first();
        await activeUser.click();

        // Deactivate
        await page.click('[data-testid="deactivate-user-btn"]');

        // Confirm with reason
        await page.fill('[data-testid="deactivation-reason"]', 'E2E test deactivation');
        await page.click('[data-testid="confirm-deactivate"]');

        // Verify status changed
        await expect(page.locator('[data-testid="user-status"]')).toContainText(/inactive|deactivated/i);

        // Verify user cannot login (would need separate test with that user's credentials)
        // This is logged in audit trail
        await page.click('[data-testid="tab-audit-log"]');
        await expect(page.locator('[data-testid="audit-entry"]').first()).toContainText(/deactivate/i);
    });

    test('E2E-AD-008: Audit trail verification', async ({ page }) => {
        await page.goto('/admin/audit-logs');

        // Verify audit log table loads
        await expect(page.locator('[data-testid="audit-log-table"]')).toBeVisible();

        // Verify columns
        await expect(page.locator('th:has-text("Timestamp")')).toBeVisible();
        await expect(page.locator('th:has-text("User")')).toBeVisible();
        await expect(page.locator('th:has-text("Action")')).toBeVisible();
        await expect(page.locator('th:has-text("Resource")')).toBeVisible();

        // Filter by action type
        await page.click('[data-testid="filter-action-type"]');
        await page.click('[data-testid="action-type-user-created"]');

        // Verify filtered results
        const rows = page.locator('[data-testid="audit-log-row"]');
        const count = await rows.count();
        expect(count).toBeGreaterThan(0);

        // Verify all rows match filter
        for (let i = 0; i < Math.min(count, 5); i++) {
            await expect(rows.nth(i)).toContainText(/user.*created/i);
        }

        // Search by user
        await page.fill('[data-testid="search-audit-logs"]', 'admin@');
        await page.keyboard.press('Enter');

        // Verify search results
        await expect(page.locator('[data-testid="audit-log-row"]').first()).toBeVisible();
    });
});

test.describe('Agent Orchestration', () => {

    test('E2E-AD-009: Agent job trigger', async ({ page }) => {
        await page.goto('/admin/agents');

        // Select an agent
        await page.locator('[data-testid="agent-card"]').first().click();

        // Trigger manual job
        await page.click('[data-testid="trigger-agent-btn"]');

        // Fill job parameters
        await page.fill('[data-testid="job-param-tenant-id"]', 'tenant-test-001');
        await page.fill('[data-testid="job-param-task"]', 'content-optimization');

        // Submit
        await page.click('[data-testid="submit-job"]');

        // Verify job created
        await expect(page.locator('text=Job queued successfully')).toBeVisible();

        // Verify job appears in queue
        await page.click('[data-testid="view-queue-btn"]');
        await expect(page.locator('[data-testid="job-row"]').first()).toBeVisible();
    });

    test('E2E-AD-010: Agent queue monitoring', async ({ page }) => {
        await page.goto('/admin/agents/queue');

        // Verify queue dashboard loads
        await expect(page.locator('[data-testid="queue-stats"]')).toBeVisible();

        // Verify metrics
        await expect(page.locator('[data-testid="stat-pending-jobs"]')).toBeVisible();
        await expect(page.locator('[data-testid="stat-running-jobs"]')).toBeVisible();
        await expect(page.locator('[data-testid="stat-completed-jobs"]')).toBeVisible();
        await expect(page.locator('[data-testid="stat-failed-jobs"]')).toBeVisible();

        // Verify queue lag metric
        const queueLag = await page.locator('[data-testid="queue-lag-seconds"]').textContent();
        expect(queueLag).toBeTruthy();

        // Filter by status
        await page.click('[data-testid="filter-status-running"]');

        // Verify running jobs shown
        await expect(page.locator('[data-testid="job-row"][data-status="running"]').first()).toBeVisible();
    });

    test('E2E-AD-011: Agent retry policy verification', async ({ page }) => {
        await page.goto('/admin/agents/queue');

        // Find a failed job
        await page.click('[data-testid="filter-status-failed"]');

        const failedJob = page.locator('[data-testid="job-row"][data-status="failed"]').first();

        if (await failedJob.isVisible()) {
            await failedJob.click();

            // Verify retry information
            await expect(page.locator('[data-testid="retry-count"]')).toBeVisible();
            await expect(page.locator('[data-testid="max-retries"]')).toBeVisible();

            // Retry manually
            await page.click('[data-testid="retry-job-btn"]');
            await page.click('[data-testid="confirm-retry"]');

            // Verify job re-queued
            await expect(page.locator('text=Job retried')).toBeVisible();
        }
    });

    test('E2E-AD-012: HIL checkpoint escalation', async ({ page }) => {
        await page.goto('/admin/agents/hil-checkpoints');

        // Verify HIL dashboard loads
        await expect(page.locator('[data-testid="hil-pending-count"]')).toBeVisible();

        // Find pending checkpoint
        const checkpoint = page.locator('[data-testid="checkpoint-row"][data-status="pending"]').first();

        if (await checkpoint.isVisible()) {
            await checkpoint.click();

            // Verify checkpoint details
            await expect(page.locator('[data-testid="checkpoint-context"]')).toBeVisible();
            await expect(page.locator('[data-testid="checkpoint-question"]')).toBeVisible();

            // Provide human input
            await page.fill('[data-testid="human-response"]', 'Approved for E2E test');

            // Approve
            await page.click('[data-testid="approve-checkpoint"]');

            // Verify checkpoint resolved
            await expect(page.locator('text=Checkpoint approved')).toBeVisible();
        }
    });
});

test.describe('Compliance & Data Management', () => {

    test('E2E-AD-013: RTBF data export/delete', async ({ page }) => {
        await page.goto('/admin/compliance/rtbf');

        // Create RTBF request
        await page.click('[data-testid="create-rtbf-request"]');

        // Select user
        await page.fill('[data-testid="search-user"]', 'test@example.com');
        await page.keyboard.press('Enter');
        await page.locator('[data-testid="user-result"]').first().click();

        // Select request type
        await page.click('[data-testid="request-type-export"]');

        // Submit
        await page.click('[data-testid="submit-rtbf-request"]');

        // Verify request created
        await expect(page.locator('text=RTBF request created')).toBeVisible();

        // Process request
        await page.locator('[data-testid="rtbf-request-row"]').first().click();
        await page.click('[data-testid="process-request"]');

        // Download export
        const [download] = await Promise.all([
            page.waitForEvent('download'),
            page.click('[data-testid="download-export"]'),
        ]);

        expect(download.suggestedFilename()).toMatch(/user.*data.*export/i);
    });

    test('E2E-AD-014: Data retention policy enforcement', async ({ page }) => {
        await page.goto('/admin/compliance/retention');

        // Verify retention policies listed
        await expect(page.locator('[data-testid="retention-policy-row"]').first()).toBeVisible();

        // Edit policy
        await page.locator('[data-testid="retention-policy-row"]').first().click();
        await page.click('[data-testid="edit-policy-btn"]');

        // Change retention period
        await page.fill('[data-testid="retention-days"]', '365');

        // Save
        await page.click('[data-testid="save-policy"]');

        // Verify success
        await expect(page.locator('text=Policy updated')).toBeVisible();

        // Trigger manual cleanup
        await page.click('[data-testid="run-cleanup-btn"]');
        await page.click('[data-testid="confirm-cleanup"]');

        // Verify cleanup job started
        await expect(page.locator('text=Cleanup job started')).toBeVisible();
    });

    test('E2E-AD-015: Audit log search and filters', async ({ page }) => {
        await page.goto('/admin/audit-logs');

        // Advanced search
        await page.click('[data-testid="advanced-search-toggle"]');

        // Date range filter
        await page.fill('[data-testid="filter-date-from"]', '2025-01-01');
        await page.fill('[data-testid="filter-date-to"]', '2025-12-31');

        // Action type filter
        await page.selectOption('[data-testid="filter-action-type"]', 'user.login');

        // Resource type filter
        await page.selectOption('[data-testid="filter-resource-type"]', 'user');

        // Apply filters
        await page.click('[data-testid="apply-filters"]');

        // Verify filtered results
        await expect(page.locator('[data-testid="audit-log-row"]').first()).toBeVisible();

        // Export audit logs
        const [download] = await Promise.all([
            page.waitForEvent('download'),
            page.click('[data-testid="export-audit-logs"]'),
        ]);

        expect(download.suggestedFilename()).toMatch(/audit.*log.*\.csv/i);
    });
});
