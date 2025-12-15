from typing import Dict, Any

# Simple in-memory store for MVP
# In production, this would be Redis or Database
active_connectors: Dict[str, Dict[str, Any]] = {}
