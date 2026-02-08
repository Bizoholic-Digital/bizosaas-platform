import requests
import json

API_KEY = "mKgAkCySnrCaAupZYGLiHNNugPRzbsGQZHbcJFMoQSSfdhKUGUPksUuGrWQGWBug"
BASE_URL = "https://dk.bizoholic.com/api/trpc"

def get_all_projects():
    url = f"{BASE_URL}/project.all?batch=1&input=%7B%220%22%3A%7B%22json%22%3A%7B%7D%7D%7D"
    resp = requests.get(url, headers={"x-api-key": API_KEY})
    if resp.status_code == 200:
        return resp.json()[0]['result']['data']['json']
    return []

def get_project_details(project_id):
    url = f"{BASE_URL}/project.one?batch=1&input=%7B%220%22%3A%7B%22json%22%3A%7B%22projectId%22%3A%22{project_id}%22%7D%7D%7D"
    resp = requests.get(url, headers={"x-api-key": API_KEY})
    if resp.status_code == 200:
        return resp.json()[0]['result']['data']['json']
    return None

projects = get_all_projects()
for p in projects:
    details = get_project_details(p['projectId'])
    if details:
        envs = details.get('environments', [])
        for env in envs:
            composes = env.get('composes', [])
            for c in composes:
                print(f"Project: {p['name']} | Env: {env['name']} | Compose: {c['name']} | ID: {c['composeId']} | Status: {c['status']}")
