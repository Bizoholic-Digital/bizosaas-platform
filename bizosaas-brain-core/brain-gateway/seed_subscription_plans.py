import os
import sys
import uuid

# Add current directory to path so imports work
sys.path.append(os.getcwd())

from app.dependencies import SessionLocal
from app.models.billing import SubscriptionPlan

from dotenv import load_dotenv
load_dotenv()

def seed_subscription_plans():
    db = SessionLocal()
    try:
        print("Seeding Subscription Plans...")
        
        plans_data = [
            {
                "name": "Starter",
                "slug": "starter",
                "description": "Perfect for individuals and small teams getting started",
                "price": 29.00,
                "currency": "USD",
                "interval": "monthly",
                "features": {
                    "max_users": 3,
                    "max_tools": 5,
                    "ai_credits": 1000,
                    "storage_gb": 10,
                    "support": "email",
                    "features": [
                        "5 Tool Integrations",
                        "1,000 AI Credits/month",
                        "10GB Storage",
                        "Email Support",
                        "Basic Analytics"
                    ]
                },
                "is_active": True
            },
            {
                "name": "Professional",
                "slug": "professional",
                "description": "For growing businesses that need more power",
                "price": 79.00,
                "currency": "USD",
                "interval": "monthly",
                "features": {
                    "max_users": 10,
                    "max_tools": 15,
                    "ai_credits": 5000,
                    "storage_gb": 50,
                    "support": "priority",
                    "features": [
                        "15 Tool Integrations",
                        "5,000 AI Credits/month",
                        "50GB Storage",
                        "Priority Support",
                        "Advanced Analytics",
                        "Custom Workflows",
                        "API Access"
                    ]
                },
                "is_active": True
            },
            {
                "name": "Business",
                "slug": "business",
                "description": "For established businesses with advanced needs",
                "price": 199.00,
                "currency": "USD",
                "interval": "monthly",
                "features": {
                    "max_users": 50,
                    "max_tools": -1,  # unlimited
                    "ai_credits": 20000,
                    "storage_gb": 200,
                    "support": "dedicated",
                    "features": [
                        "Unlimited Tool Integrations",
                        "20,000 AI Credits/month",
                        "200GB Storage",
                        "Dedicated Support",
                        "Advanced Analytics",
                        "Custom Workflows",
                        "API Access",
                        "White-label Options",
                        "SSO/SAML"
                    ]
                },
                "is_active": True
            },
            {
                "name": "Enterprise",
                "slug": "enterprise",
                "description": "Custom solutions for large organizations",
                "price": 499.00,
                "currency": "USD",
                "interval": "monthly",
                "features": {
                    "max_users": -1,  # unlimited
                    "max_tools": -1,  # unlimited
                    "ai_credits": -1,  # unlimited
                    "storage_gb": -1,  # unlimited
                    "support": "dedicated",
                    "features": [
                        "Unlimited Everything",
                        "Dedicated Account Manager",
                        "Custom Integrations",
                        "On-premise Deployment Option",
                        "SLA Guarantees",
                        "Advanced Security",
                        "Compliance Support",
                        "Training & Onboarding"
                    ]
                },
                "is_active": True
            },
            {
                "name": "Free Trial",
                "slug": "trial",
                "description": "14-day free trial with full access",
                "price": 0.00,
                "currency": "USD",
                "interval": "monthly",
                "features": {
                    "max_users": 2,
                    "max_tools": 3,
                    "ai_credits": 500,
                    "storage_gb": 5,
                    "support": "community",
                    "trial_days": 14,
                    "features": [
                        "3 Tool Integrations",
                        "500 AI Credits",
                        "5GB Storage",
                        "Community Support",
                        "14-day Trial"
                    ]
                },
                "is_active": True
            }
        ]
        
        for plan_data in plans_data:
            plan = db.query(SubscriptionPlan).filter_by(slug=plan_data["slug"]).first()
            if not plan:
                plan = SubscriptionPlan(**plan_data)
                db.add(plan)
                print(f"Created plan: {plan.name}")
            else:
                # Update existing plan
                for key, value in plan_data.items():
                    setattr(plan, key, value)
                print(f"Updated plan: {plan.name}")
        
        db.commit()
        print("Subscription plans seeding completed successfully!")
        
    except Exception as e:
        print(f"Error seeding subscription plans: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_subscription_plans()
