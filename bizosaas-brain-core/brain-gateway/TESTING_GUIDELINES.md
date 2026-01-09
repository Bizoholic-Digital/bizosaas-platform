# Brain Gateway Testing Guidelines

This document outlines the testing strategy and standards for the Brain Gateway microservice.

## 🧪 Testing Pyramid

We follow a balanced testing pyramid to ensure reliability while maintaining speed:

1.  **Unit Tests (70%)**: Focus on individual functions, services, and domain logic.
2.  **Integration Tests (20%)**: Verify interactions between the Gateway and external dependencies (DB, Redis, Vault, Temporal).
3.  **E2E API Tests (10%)**: Validate full user journeys through API endpoints.

## 🛠 Tools

- **Framework**: `pytest`
- **Async Support**: `pytest-asyncio`
- **API Client**: `httpx` (via FastAPI `TestClient`)
- **Isolation**: `unittest.mock` and `app.dependency_overrides`
- **Load Testing**: `Locust`

## 📁 Directory Structure

```text
tests/
├── conftest.py          # Shared fixtures
├── test_agents.py       # Unit tests for AI Agent logic
├── test_connectors/     # Connector-specific unit tests
├── test_db_integration.py # DB connectivity and schema tests
├── test_e2e_campaigns.py  # End-to-end campaign lifecycle
└── test_auth_rbac.py    # Auth and Role-Based Access tests
```

## 🚀 Running Tests

### Local Execution

```bash
cd bizosaas-brain-core/brain-gateway
# Set environment variables for testing
export DATABASE_URL=sqlite:///./test.db
export ENVIRONMENT=testing

# Run all tests
pytest tests/

# Run with coverage
pytest --cov=app tests/
```

### CI/CD
Tests are automatically executed on every push and pull request via `.github/workflows/ci-brain-gateway.yml`.

## 📝 Standards

- **Isolation**: Use `app.dependency_overrides` to mock external auth (Clerk) or third-party APIs.
- **Naming**: Test files must start with `test_`. Test functions must start with `test_`.
- **Database**: Use a separate SQLite database for testing. Fixtures should handle setup/teardown.
- **Async**: Use `@pytest.mark.asyncio` for tests involving `await`.
- **RBAC**: Always verify that restricted endpoints return `403 Forbidden` for unauthorized roles.

## 📊 Performance Testing
Run Locust from the `tests/` directory:
```bash
locust -f tests/locustfile.py --host=http://localhost:8000
```
Visit http://localhost:8089 to configure the load test.
