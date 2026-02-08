import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.billing import SubscriptionPlan
from app.models import Base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/bizosaas")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_plans():
    db = SessionLocal()
    try:
        # Check if plans exist
        if db.query(SubscriptionPlan).count() > 0:
            print("Plans already exist, skipping seed.")
            return

        plans = [
            SubscriptionPlan(
                name="Starter",
                slug="starter",
                description="Perfect for small businesses starting their digital journey.",
                price=29.00,
                currency="USD",
                interval="monthly",
                features={"leads": 1000, "storage": "5GB", "agents": 1}
            ),
            SubscriptionPlan(
                name="Professional",
                slug="professional",
                description="Advanced tools for growing businesses.",
                price=99.00,
                currency="USD",
                interval="monthly",
                features={"leads": 10000, "storage": "50GB", "agents": 5}
            ),
            SubscriptionPlan(
                name="Enterprise",
                slug="enterprise",
                description="Custom solutions for large scale operations.",
                price=499.00,
                currency="USD",
                interval="monthly",
                features={"leads": "Unlimited", "storage": "500GB", "agents": "Unlimited"}
            )
        ]
        
        db.add_all(plans)
        db.commit()
        print("Billing plans seeded successfully!")
    except Exception as e:
        print(f"Error seeding plans: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # Ensure tables are created (in case migrations haven't run)
    Base.metadata.create_all(bind=engine)
    seed_plans()
