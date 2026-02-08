import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Connect to 'postgres' db to create new db
conn = psycopg2.connect("postgresql://neondb_owner:npg_puEbTnkSO9F8@ep-gentle-flower-a15rdh2r-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require")
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()

try:
    cur.execute("CREATE DATABASE wagtail_db;")
    print("Database wagtail_db created successfully")
except psycopg2.errors.DuplicateDatabase:
    print("Database wagtail_db already exists")
except Exception as e:
    print(f"Error: {e}")
finally:
    cur.close()
    conn.close()
