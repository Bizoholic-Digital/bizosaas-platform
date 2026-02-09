
import secrets
import string

def generate_key(length=64):
    """Generate a secure random key."""
    chars = string.ascii_letters + string.digits + "!@#%^&*"
    return ''.join(secrets.choice(chars) for _ in range(length))

def generate_password(length=24):
    """Generate a secure password."""
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))

keys = [
    "CMS_AUTH_KEY",
    "CMS_SECURE_AUTH_KEY",
    "CMS_LOGGED_IN_KEY",
    "CMS_NONCE_KEY",
    "CMS_AUTH_SALT",
    "CMS_SECURE_AUTH_SALT",
    "CMS_LOGGED_IN_SALT",
    "CMS_NONCE_SALT"
]

db_vars = {
    "DB_NAME": "bizoholic_cms",
    "DB_PASSWORD": generate_password()
}

env_path = ".env"

try:
    with open(env_path, "a") as f:
        f.write("\n\n# Bizoholic CMS Configuration\n")
        
        # Write DB config
        for key, value in db_vars.items():
            f.write(f"{key}={value}\n")
            print(f"Generated {key}")

        # Write Keys/Salts
        for key in keys:
            val = generate_key()
            f.write(f"{key}='{val}'\n")
            print(f"Generated {key}")
    
    print(f"\nSuccessfully appended CMS configuration to {env_path}")
    print("IMPORTANT: You must copy these new values to your deployment environment (Dokploy) for them to take effect.")

except Exception as e:
    print(f"Error updating .env: {e}")
