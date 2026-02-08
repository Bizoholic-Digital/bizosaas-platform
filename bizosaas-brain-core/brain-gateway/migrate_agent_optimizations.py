import os
import sys
from sqlalchemy import text
sys.path.append(os.getcwd())
from app.dependencies import engine

def migrate():
    with engine.connect() as conn:
        print("Migrating agent_optimizations table...")
        
        try:
            conn.execute(text("ALTER TABLE agent_optimizations ADD COLUMN potential_savings JSON"))
            conn.commit()
            print("Added potential_savings column")
        except Exception as e:
            conn.rollback()
            if "DuplicateColumn" in str(e) or "already exists" in str(e):
                print("Column potential_savings already exists.")
            else:
                print(f"Error adding potential_savings: {e}")
            
        conn.commit()
        print("Migration complete.")

if __name__ == "__main__":
    migrate()
