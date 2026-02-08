import requests
import json

API_KEY = "mKgAkCySnrCaAupZYGLiHNNugPRzbsGQZHbcJFMoQSSfdhKUGUPksUuGrWQGWBug"
BASE_URL = "https://dk.bizoholic.com/api/trpc"

def get_all_projects():
    url = f"{BASE_URL}/project.all?batch=1&input=%7B%220%22%3A%7B%22json%22%3A%7B%7D%7D%7D"
    resp = requests.get(url, headers={"x-api-key": API_KEY})
    if resp.status_code == 200:
        data = resp.json()
        print("All Projects:")
        try:
            projects = data[0]['result']['data']['json']
            for p in projects:
                print(f"  ID: {p.get('projectId')} | Name: {p.get('name')} | ServerID: {p.get('serverId')}")
        except Exception as e:
            print(f"  Error: {e}")
            print(data)
    else:
        print(f"Failed: {resp.status_code} {resp.text}")

get_all_projects()
