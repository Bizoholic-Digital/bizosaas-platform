# BizOSaaS Testing Implementation - Quick Start Guide

This guide will help you get started with the comprehensive testing suite for production readiness.

## 📋 Prerequisites

### Required Software
- **Node.js** >= 18.0.0
- **Python** >= 3.11
- **Docker** & **Docker Compose**
- **PostgreSQL** 16 (or use Docker)
- **Redis** 7 (or use Docker)

### Optional Tools
- **k6** - For performance testing
- **Playwright** - For E2E testing (auto-installed)
- **OWASP ZAP** - For security testing

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Navigate to testing directory
cd testing

# Install Node.js dependencies
npm install

# Install Playwright browsers
npm run setup:playwright

# Install Python dependencies (for backend tests)
cd ../bizosaas-brain-core/brain-gateway
pip install -r requirements.txt
pip install pytest pytest-cov pytest-asyncio
```

### 2. Set Up Test Environment

```bash
# Set up staging environment
cd testing/scripts
chmod +x setup-staging-env.sh
./setup-staging-env.sh --start

# This will:
# - Start PostgreSQL, Redis, Vault, Temporal
# - Initialize databases
# - Configure secrets in Vault
# - Set up feature flags
```

### 3. Configure Environment Variables

```bash
# Copy environment template
cp testing/.env.example testing/.env.test

# Edit with your values
nano testing/.env.test
```

Required variables:
```env
BASE_URL=http://localhost:3003
ADMIN_URL=http://localhost:3004
API_URL=http://localhost:8001

TEST_CLIENT_EMAIL=client@test.com
TEST_CLIENT_PASSWORD=TestPassword123!
TEST_ADMIN_EMAIL=admin@test.com
TEST_ADMIN_PASSWORD=AdminPassword123!

DATABASE_URL=postgresql://admin:password@localhost:5433/bizosaas_staging
REDIS_URL=redis://localhost:6380/0
```

### 4. Seed Test Data

```bash
cd testing
npm run setup:test-data
```

## 🧪 Running Tests

### Run All Tests
```bash
cd testing
npm test
```

### Run Specific Test Suites

#### Unit Tests
```bash
# Backend unit tests
cd testing/backend
pytest test_brain_gateway.py -v

# Frontend unit tests (if configured)
cd portals/client-portal
npm test
```

#### Integration Tests
```bash
cd testing/backend
pytest test_integration.py -v
```

#### E2E Tests
```bash
cd testing/playwright

# Run all E2E tests
npm run test:e2e

# Run with UI mode (interactive)
npm run test:e2e:ui

# Run in headed mode (see browser)
npm run test:e2e:headed

# Debug mode
npm run test:e2e:debug

# Run specific test file
npx playwright test tests/client-portal/auth.spec.ts
```

#### Security Tests
```bash
cd testing
npm run test:security
```

#### Performance Tests
```bash
cd testing
npm run test:performance
```

#### Accessibility Tests
```bash
cd testing
npm run test:accessibility
```

## 📊 Viewing Test Reports

### Playwright E2E Reports
```bash
cd testing/playwright
npm run report:e2e
# Opens HTML report in browser
```

### Coverage Reports
```bash
cd testing
npm run report:coverage
# Opens coverage report in browser
```

### Performance Reports
```bash
# Reports are in testing/reports/performance/
open testing/reports/performance/latest/summary.html
```

### Accessibility Reports
```bash
# Reports are in testing/reports/accessibility/
open testing/reports/accessibility/latest/summary.html
```

## 🔍 Test Organization

```
testing/
├── playwright/                 # E2E tests
│   ├── tests/
│   │   ├── client-portal/     # Client portal E2E tests
│   │   ├── admin-dashboard/   # Admin dashboard E2E tests
│   │   ├── security/          # Security vulnerability tests
│   │   └── accessibility/     # Accessibility tests
│   └── playwright.config.ts   # Playwright configuration
├── backend/                   # Backend tests
│   ├── test_brain_gateway.py # Unit tests
│   └── test_integration.py   # Integration tests
├── fixtures/                  # Test data fixtures
│   ├── tenants/              # Tenant fixtures
│   └── users/                # User fixtures
├── scripts/                   # Test automation scripts
│   ├── setup-staging-env.sh  # Environment setup
│   ├── run-performance-tests.sh
│   └── run-accessibility-tests.sh
└── reports/                   # Test reports (generated)
```

## 🎯 Test Coverage Goals

| Area | Target Coverage |
|------|----------------|
| Backend Unit Tests | ≥ 80% |
| Frontend Unit Tests | ≥ 70% |
| Integration Tests | Critical paths covered |
| E2E Tests | All user workflows |
| Security Tests | OWASP Top 10 |
| Performance Tests | All SLO targets met |
| Accessibility | WCAG 2.1 AA compliant |

## 🐛 Debugging Failed Tests

### E2E Test Failures

1. **Check test videos** (if enabled):
   ```bash
   open testing/playwright/test-results/[test-name]/video.webm
   ```

2. **Check screenshots**:
   ```bash
   open testing/playwright/test-results/[test-name]/screenshot.png
   ```

3. **Run in debug mode**:
   ```bash
   cd testing/playwright
   npx playwright test --debug tests/path/to/test.spec.ts
   ```

### Backend Test Failures

1. **Run with verbose output**:
   ```bash
   pytest test_brain_gateway.py -v -s
   ```

2. **Run specific test**:
   ```bash
   pytest test_brain_gateway.py::TestAuthentication::test_jwt_token_generation -v
   ```

3. **Check logs**:
   ```bash
   docker logs bizosaas-postgres-staging
   docker logs bizosaas-redis-staging
   ```

## 📝 Writing New Tests

### E2E Test Template
```typescript
import { test, expect } from '@playwright/test';

test.describe('Feature Name', () => {
  test('should do something', async ({ page }) => {
    await page.goto('/path');
    
    // Your test steps
    await page.click('[data-testid="button"]');
    
    // Assertions
    await expect(page.locator('[data-testid="result"]')).toBeVisible();
  });
});
```

### Backend Test Template
```python
import pytest

class TestFeature:
    """Test feature description"""
    
    def test_something(self):
        """Test specific behavior"""
        # Arrange
        input_data = {"key": "value"}
        
        # Act
        result = function_to_test(input_data)
        
        # Assert
        assert result == expected_value
```

## 🔄 CI/CD Integration

Tests run automatically on:
- **Push to staging/main branches**
- **Pull requests to main**
- **Daily at 2 AM** (scheduled)
- **Manual trigger** (workflow_dispatch)

View results in GitHub Actions:
```
https://github.com/Bizoholic-Digital/bizosaas-platform/actions
```

## 📚 Additional Resources

- [Full Testing Plan](./PRODUCTION_READINESS_TESTING_PLAN.md)
- [Playwright Documentation](https://playwright.dev)
- [pytest Documentation](https://docs.pytest.org)
- [k6 Documentation](https://k6.io/docs)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)

## 🆘 Getting Help

If you encounter issues:

1. Check the [Testing Plan](./PRODUCTION_READINESS_TESTING_PLAN.md) for detailed task descriptions
2. Review test logs and reports
3. Check GitHub Actions for CI/CD failures
4. Contact the QA team

## ✅ Pre-Production Checklist

Before deploying to production, ensure:

- [ ] All unit tests passing (≥80% coverage)
- [ ] All integration tests passing
- [ ] All E2E tests passing
- [ ] No critical security vulnerabilities
- [ ] Performance SLOs met
- [ ] Accessibility WCAG 2.1 AA compliant
- [ ] All test reports reviewed
- [ ] UAT sign-off received
- [ ] Runbooks updated
- [ ] Rollback plan documented

---

**Last Updated**: January 8, 2026  
**Maintained by**: QA Team
