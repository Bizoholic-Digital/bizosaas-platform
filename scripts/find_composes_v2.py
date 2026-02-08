import requests
import json

API_KEY = "mKgAkCySnrCaAupZYGLiHNNugPRzbsGQZHbcJFMoQSSfdhKUGUPksUuGrWQGWBug"
BASE_URL = "https://dk.bizoholic.com/api/trpc"

def find_all_composes():
    url = f"{BASE_URL}/project.all?batch=1&input=%7B%220%22%3A%7B%22json%22%3A%7B%7D%7D%7D"
    resp = requests.get(url, headers={"x-api-key": API_KEY})
    projects = resp.json()[0]['result']['data']['json']
    for p in projects:
        url_one = f"{BASE_URL}/project.one?batch=1&input=%7B%220%22%3A%7B%22json%22%3A%7B%22projectId%22%3A%22{p['projectId']}%22%7D%7D%7D"
        resp_one = requests.get(url_one, headers={"x-api-key": API_KEY})
        details = resp_one.json()[0]['result']['data']['json']
        print(f"Project: {p['name']} | Environments: {len(details.get('environments', []))}")
        for env in details.get('environments', []):
            print(f"  Env: {env.get('name')} | Composes: {len(env.get('compose', []))}")
            composes = env.get('compose', [])
            for c in composes:
                print(f"Project: {p['name']} | Env: {env['name']} | Compose: {c.get('name')} | ID: {c.get('composeId')}")

find_all_composes()
