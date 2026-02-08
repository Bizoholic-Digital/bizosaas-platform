import sys
import os

# Add the gateway root to sys.path
GATEWAY_ROOT = "/home/alagiri/projects/bizosaas-platform/bizosaas-brain-core/brain-gateway"
if GATEWAY_ROOT not in sys.path:
    sys.path.insert(0, GATEWAY_ROOT)

# Ensure 'app' is not being shadowed by individual folder additions
# We want 'import app' to resolve to GATEWAY_ROOT/app
# and 'import adapters' to resolve to GATEWAY_ROOT/adapters
