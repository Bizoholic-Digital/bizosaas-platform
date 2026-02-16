from langchain.tools import tool
import requests
import os
import json
from typing import Dict, Any, Optional

# Default to internal docker network URL
BRAIN_GATEWAY_URL = os.getenv("BRAIN_GATEWAY_URL", "http://brain-gateway:8000")

@tool("fetch_data")
def fetch_data(connector_id: str, resource: str, tenant_id: str = "default_tenant") -> Any:
    """
    Fetch data from a connected platform via the Brain Gateway.
    
    Args:
        connector_id (str): The ID of the connector (e.g., 'wordpress', 'zoho-crm').
        resource (str): The resource to fetch (e.g., 'posts', 'pages', 'leads', 'contacts').
        tenant_id (str): The tenant ID of the user (default: 'default_tenant').
        
    Returns:
        Dict: The fetched data and metadata.
    """
    url = f"{BRAIN_GATEWAY_URL}/api/connectors/{connector_id}/sync/{resource}"
    try:
        # In a real scenario, we'd pass auth tokens here
        response = requests.get(url, params={"tenant_id": tenant_id}, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return f"Error fetching data from {connector_id}: {str(e)}"

@tool("perform_action")
def perform_action(connector_id: str, action: str, payload: str, tenant_id: str = "default_tenant") -> Any:
    """
    Perform a write action on a connected platform via the Brain Gateway.
    
    Args:
        connector_id (str): The ID of the connector (e.g., 'wordpress').
        action (str): The action to perform (e.g., 'create_post', 'update_lead').
        payload (str): JSON string containing the data for the action.
        tenant_id (str): The tenant ID of the user.
        
    Returns:
        Dict: The result of the action.
    """
    url = f"{BRAIN_GATEWAY_URL}/api/connectors/{connector_id}/action/{action}"
    try:
        data = json.loads(payload)
        response = requests.post(url, json=data, params={"tenant_id": tenant_id}, timeout=30)
        response.raise_for_status()
        return response.json()
    except json.JSONDecodeError:
        return "Error: Payload must be a valid JSON string."
    except requests.exceptions.RequestException as e:
        return f"Error performing action on {connector_id}: {str(e)}"

def get_all_tools() -> list:
    """Return a list of all available connector tools."""
    return [fetch_data, perform_action]

class ConnectorTools:
    """Legacy wrapper for backward compatibility"""
    def __init__(self):
        self.fetch_data = fetch_data
        self.perform_action = perform_action
