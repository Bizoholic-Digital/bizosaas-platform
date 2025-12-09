# Oracle Cloud Deployment Steps

This guide outlines the specific steps to deploy the BizOSaaS platform on an Oracle Cloud Infrastructure (OCI) Always Free tier instance.

## 1. Instance Provisioning

1.  **Sign up/Login to Oracle Cloud Console**.
2.  **Create a VM Instance**:
    *   **Name**: `bizosaas-brain`
    *   **Image**: Canonical Ubuntu 22.04
    *   **Shape**: Ampere (Arm based processor) -> `VM.Standard.A1.Flex`
    *   **OCPU**: 4
    *   **Memory**: 24 GB
    *   **Networking**: Create a new VCN (e.g., `bizosaas-vcn`) and a public subnet.
    *   **SSH Keys**: Generate and save your SSH key pair. Upload the public key.
    *   **Boot Volume**: Default (or up to 200GB free).
3.  **Create**: Click create and wait for the instance to provision. Note the **Public IP**.

## 2. Network Configuration (Security Lists)

1.  Navigate to **Networking** -> **Virtual Cloud Networks**.
2.  Click on your VCN (`bizosaas-vcn`).
3.  Click on **Security Lists** -> **Default Security List**.
4.  **Add Inbound Rules** to allow traffic to your services:
    *   **Source CIDR**: `0.0.0.0/0` (Allow all)
    *   **Protocols**: TCP
    *   **Destination Ports**:
        *   `80` (HTTP)
        *   `443` (HTTPS)
        *   `3003` (Client Portal)
        *   `8000` (Brain Gateway)
        *   `9000` (Authentik SSO)
        *   `9001` (Portainer HTTP)
        *   `9443` (Authentik HTTPS)
        *   `9444` (Portainer HTTPS)

## 3. Server Setup

SSH into your new instance:
```bash
ssh -i /path/to/your/private.key ubuntu@<YOUR_PUBLIC_IP>
```

Run the following commands to set up the environment:

```bash
# Update System
sudo apt update && sudo apt upgrade -y

# Install Docker
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io

# Enable Docker for non-root user
sudo usermod -aG docker ${USER}
# (You may need to logout and login again for this to take effect)

# Install Docker Compose (V2 is included in newer docker-ce, check with 'docker compose version')

# Allow ports in OS firewall (iptables/netfilter usually managed by Oracle security lists, but UFW might be active)
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 3003/tcp
sudo ufw allow 8000/tcp
sudo ufw allow 9000/tcp
sudo ufw allow 9001/tcp
sudo ufw allow 9443/tcp
sudo ufw allow 9444/tcp
# sudo ufw enable # Use with caution, ensure SSH (22) is allowed first!
```

## 4. Deploy BizOSaaS

```bash
# Clone the repository
git clone https://github.com/Bizoholic-Digital/bizosaas-platform.git
cd bizosaas-platform

# Setup Environment Variables
cp .env.example .env
nano .env
# PASTE your production values into .env (Database passwords, API keys, etc.)

# Start the Platform
./scripts/start-bizosaas-core-full.sh --wait
```

## 5. Post-Deployment Verification

1.  Access Portainer: `https://<YOUR_PUBLIC_IP>:9444`
2.  Access Client Portal: `http://<YOUR_PUBLIC_IP>:3003`
3.  Access Authentik: `http://<YOUR_PUBLIC_IP>:9000`

## 6. Domain & SSL (Optional but Recommended)

For a production setup, you should point a domain name to your Oracle Cloud IP and use a reverse proxy (like Traefik, Nginx, or Caddy) to handle SSL termination.

*   A simple way is to use **coolify.io** (self-hostable PaaS) which can be installed on this same server to manage deployments and automatic SSL.
*   Alternatively, configure the existing **Traefik** service in the docker-compose to handle Let's Encrypt certificates.
