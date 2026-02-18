from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("NEO4J_URI", "neo4j+s://42c5bda2.databases.neo4j.io")
user = os.getenv("NEO4J_USERNAME", "neo4j")
password = os.getenv("NEO4J_PASSWORD")

print(f"Testing connection to {uri} with user {user}...")

try:
    driver = GraphDatabase.driver(uri, auth=(user, password))
    driver.verify_connectivity()
    print("SUCCESS: Connected to Neo4j!")
    driver.close()
except Exception as e:
    print(f"FAILED: {e}")
