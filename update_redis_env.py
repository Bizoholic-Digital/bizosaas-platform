import os

env_path = "/home/alagiri/projects/bizosaas-platform/.env"
creds_path = "/home/alagiri/projects/bizosaas-platform/credentials.md"

# Redis Cloud URL from credentials.md
# REDIS_URL=redis://default:Gt7QxXA4ybMzYzD9e6KIBULfnv1IU6f9@redis-10690.c264.ap-south-1-1.ec2.cloud.redislabs.com:10690/0
NEW_REDIS_URL = "redis://default:Gt7QxXA4ybMzYzD9e6KIBULfnv1IU6f9@redis-10690.c264.ap-south-1-1.ec2.cloud.redislabs.com:10690/0"

def update_env_file():
    if not os.path.exists(env_path):
        print(f"Error: {env_path} not found.")
        return

    with open(env_path, "r") as f:
        lines = f.readlines()

    new_lines = []
    redis_updated = False

    for line in lines:
        if line.startswith("REDIS_URL="):
            new_lines.append(f"REDIS_URL={NEW_REDIS_URL}\n")
            redis_updated = True
            print("Updated existing REDIS_URL")
        else:
            new_lines.append(line)

    if not redis_updated:
        new_lines.append(f"\nREDIS_URL={NEW_REDIS_URL}\n")
        print("Added new REDIS_URL")

    with open(env_path, "w") as f:
        f.writelines(new_lines)
    
    print(f"Successfully updated {env_path}")

if __name__ == "__main__":
    update_env_file()
