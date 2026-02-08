import requests
import json

API_KEY = "mKgAkCySnrCaAupZYGLiHNNugPRzbsGQZHbcJFMoQSSfdhKUGUPksUuGrWQGWBug"
BASE_URL = "https://dk.bizoholic.com/api/trpc"

def get_server_stats():
    url = f"{BASE_URL}/server.all?batch=1&input=%7B%220%22%3A%7B%22json%22%3A%7B%7D%7D%7D"
    resp = requests.get(url, headers={"x-api-key": API_KEY})
    if resp.status_code == 200:
        data = resp.json()
        print("Server Stats:")
        try:
            servers = data[0]['result']['data']['json']
            for server in servers:
                print(f"  ID: {server.get('serverId')} | Name: {server.get('name')} | IP: {server.get('ipAddress')}")
        except Exception as e:
            print(f"  Error: {e}")
            print(data)
    else:
        print(f"Failed: {resp.status_code} {resp.text}")

get_server_stats()
