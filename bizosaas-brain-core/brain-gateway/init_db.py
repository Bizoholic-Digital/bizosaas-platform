import os
import sys

# Add current directory to path so imports work
sys.path.append(os.getcwd())

from app.dependencies import engine
from app.models import Base

# Import all models to ensure they are registered with Base
from app.models import user, mcp, agent, support

def init_db():
    print(f"Creating database tables using engine: {engine.url}...")
    try:
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully!")
    except Exception as e:
        print(f"Error creating tables: {e}")

if __name__ == "__main__":
    init_db()
