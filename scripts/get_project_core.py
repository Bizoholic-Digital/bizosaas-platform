import requests
import json

API_KEY = "mKgAkCySnrCaAupZYGLiHNNugPRzbsGQZHbcJFMoQSSfdhKUGUPksUuGrWQGWBug"
BASE_URL = "https://dk.bizoholic.com/api/trpc"

def get_project_one(project_id):
    url = f"{BASE_URL}/project.one?batch=1&input=%7B%220%22%3A%7B%22json%22%3A%7B%22projectId%22%3A%22{project_id}%22%7D%7D%7D"
    resp = requests.get(url, headers={"x-api-key": API_KEY})
    if resp.status_code == 200:
        data = resp.json()
        print(f"Project One ({project_id}):")
        try:
            project_data = data[0]['result']['data']['json']
            for env in project_data.get('environments', []):
                print(f"  Environment: {env.get('name')}")
                for c in env.get('composes', []):
                    print(f"    - Compose: {c.get('name')} | ID: {c.get('composeId')} | Path: {c.get('composePath')}")
        except Exception as e:
            print(f"  Error: {e}")
            print(data)
    else:
        print(f"Failed: {resp.status_code} {resp.text}")

get_project_one("p4fmYaVZ_iDFDH4XSDnOU")
