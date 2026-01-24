import requests
import json

API_KEY = "mKgAkCySnrCaAupZYGLiHNNugPRzbsGQZHbcJFMoQSSfdhKUGUPksUuGrWQGWBug"
BASE_URL = "https://dk.bizoholic.com/api/trpc"

def get_managed_services():
    # Try postgresql.all
    url_pg = f"{BASE_URL}/postgres.all?batch=1&input=%7B%220%22%3A%7B%22json%22%3A%7B%7D%7D%7D"
    resp_pg = requests.get(url_pg, headers={"x-api-key": API_KEY})
    if resp_pg.status_code == 200:
        print("PostgreSQL Services:")
        try:
            pgs = resp_pg.json()[0]['result']['data']['json']
            for pg in pgs:
                print(f"  ID: {pg.get('databaseId')} | Name: {pg.get('name')} | AppName: {pg.get('appName')}")
        except: pass
        
    url_rd = f"{BASE_URL}/redis.all?batch=1&input=%7B%220%22%3A%7B%22json%22%3A%7B%7D%7D%7D"
    resp_rd = requests.get(url_rd, headers={"x-api-key": API_KEY})
    if resp_rd.status_code == 200:
        print("Redis Services:")
        try:
            rds = resp_rd.json()[0]['result']['data']['json']
            for rd in rds:
                print(f"  ID: {rd.get('redisId')} | Name: {rd.get('name')} | AppName: {rd.get('appName')}")
        except: pass

get_managed_services()
