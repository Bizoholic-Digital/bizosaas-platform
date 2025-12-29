import httpx
import json

def assign_role():
    clerk_secret = "sk_test_hsYzctm4bTgGxWB5Z6f7GT2OgnJ1biw7t21Q8NJvjv"
    user_id = "user_37SpjCv6JUvLxu5cl8IHzQ2DzCG"
    url = f"https://api.clerk.com/v1/users/{user_id}/metadata"
    headers = {
        "Authorization": f"Bearer {clerk_secret}",
        "Content-Type": "application/json"
    }
    payload = {
        "public_metadata": {
            "role": "Super Admin",
            "roles": ["Super Admin"],
            "tenant_id": "platform_admin"
        }
    }
    
    print(f"Assigning role via direct HTTP call to Clerk API for user: {user_id}")
    try:
        with httpx.Client() as client:
            response = client.patch(url, json=payload, headers=headers)
            print(f"Status Code: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            
            if response.status_code == 200:
                print("Successfully updated user metadata!")
            else:
                print("Failed to update user metadata.")
    except Exception as e:
        print(f"Error calling Clerk API: {e}")

if __name__ == "__main__":
    assign_role()
