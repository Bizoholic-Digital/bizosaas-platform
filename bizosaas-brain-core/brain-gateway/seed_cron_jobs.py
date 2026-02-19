"""
Seed default system cron jobs into the database.
Run once during initial platform setup or via init_db.py
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.cron_job import CronJob
from app.temporal_workflows.cron_workflow import DEFAULT_CRON_JOBS


def seed_default_cron_jobs():
    db = SessionLocal()
    try:
        created = 0
        for job_def in DEFAULT_CRON_JOBS:
            existing = db.query(CronJob).filter(CronJob.name == job_def["name"]).first()
            if existing:
                print(f"  ⏭️  Skipping '{job_def['name']}' (already exists)")
                continue
            job = CronJob(**job_def)
            db.add(job)
            created += 1
            print(f"  ✅ Created cron job: {job_def['name']} [{job_def['schedule']}]")

        db.commit()
        print(f"\nSeeded {created} default system cron jobs.")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_default_cron_jobs()
