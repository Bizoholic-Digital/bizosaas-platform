from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("NEO4J_URI")
user = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")

def test_connection():
    print(f"Testing connection to: {uri}")
    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        driver.verify_connectivity()
        print("✅ Successfully connected to Neo4j Aura Cloud!")
        driver.close()
    except Exception as e:
        print(f"❌ Failed to connect: {e}")

if __name__ == "__main__":
    test_connection()
