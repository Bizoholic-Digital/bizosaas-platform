import os
import sys
import time
from neo4j import GraphDatabase
from dotenv import load_dotenv

# Path setup
os.chdir("/home/alagiri/projects/bizosaas-platform/bizosaas-brain-core/brain-gateway")
sys.path.append(".")

# Load secrets
from main import load_vault_secrets_sync
print("Loading Vault secrets...")
load_vault_secrets_sync()

uri = os.getenv("NEO4J_URI")
user = os.getenv("NEO4J_USERNAME")
pwd = os.getenv("NEO4J_PASSWORD")

print(f"DEBUG: Attempting to connect to Neo4j Aura at: {uri}")
print(f"DEBUG: Username: {user}")

if not uri or not user or not pwd:
    print("ERROR: Neo4j credentials missing in environment!")
    sys.exit(1)

try:
    print("Initializing driver...")
    # Use neo4j+s for Aura (encrypted)
    # The driver should handle the routing automatically
    driver = GraphDatabase.driver(uri, auth=(user, pwd))
    
    print("Verifying connectivity (timeout in 15s)...")
    start_time = time.time()
    driver.verify_connectivity()
    end_time = time.time()
    
    print(f"SUCCESS: Connected to Neo4j Aura in {end_time - start_time:.2f}s!")
    
    # Try a simple query
    with driver.session() as session:
        result = session.run("RETURN 'Connection Verified' as msg")
        row = result.single()
        print(f"Query Result: {row['msg']}")
        
    driver.close()
    
except Exception as e:
    print(f"FAILURE: Failed to connect to Neo4j Aura: {e}")
    if "Routing information" in str(e):
        print("TIP: This often means the URI is incorrect or the DB is in a transition state.")
    sys.exit(1)
