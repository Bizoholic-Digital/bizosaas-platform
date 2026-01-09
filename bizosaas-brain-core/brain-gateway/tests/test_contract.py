import schemathesis
from main import app
import pytest

# Create a Schemathesis schema from the FastAPI app
schema = schemathesis.from_asgi("/openapi.json", app)

@schema.parametrize()
@pytest.mark.parametrize("role", ["Super Admin", "Admin", "Client"])
def test_api_contract(case, role):
    """
    Contract tests that use property-based testing to verify the API 
    conforms to its OpenAPI specification.
    """
    # We can inject headers for authentication if needed
    # For property-based testing, we might want to check both auth and unauth cases
    headers = {"Authorization": f"Bearer {role.lower()}-token"}
    
    response = case.call_asgi(app, headers=headers)
    
    # Schemathesis checks:
    # 1. Not a 5xx error
    # 2. Matches the schema definitions
    # 3. Response time is reasonable (optional)
    case.validate_response(response)
