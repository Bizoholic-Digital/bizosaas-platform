#!/bin/bash
set -e

# Directory where script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$SCRIPT_DIR/.."
ENV_FILE="$PROJECT_ROOT/.env.lago"

echo "Setting up Lago Billing locally..."

# Check if openssl is installed
if ! command -v openssl &> /dev/null; then
    echo "Error: openssl is required but not installed."
    exit 1
fi

# Generate .env.lago if it doesn't exist
if [ ! -f "$ENV_FILE" ]; then
    echo "Generating new Lago configuration in .env.lago..."
    
    # Generate RSA Private Key (PKCS#1)
    RSA_PRIVATE_KEY=$(openssl genrsa 2048 | awk 'NF {sub(/\r/, ""); printf "%s\\n",$0;}')
    
    # Create the file
    cat > "$ENV_FILE" <<EOL
# Lago Local Environment Variables
LAGO_RSA_PRIVATE_KEY="$RSA_PRIVATE_KEY"
LAGO_API_URL=http://localhost:3000
LAGO_FRONT_URL=http://localhost:8088
EOL
    echo "Generated .env.lago with new RSA key."
else
    echo "Using existing .env.lago configuration."
fi

# Start Lago using Docker Compose
echo "Starting Lago services..."
cd "$PROJECT_ROOT"
docker compose -f docker-compose.lago.yml --env-file .env.lago up -d

echo "------------------------------------------------"
echo "✅ Lago Billing is starting up!"
echo "   Dashboard: http://localhost:8088"
echo "   API:       http://localhost:3000"
echo "   Login:     Create your admin account on first visit."
echo ""
echo "   To stop:   docker compose -f docker-compose.lago.yml down"
echo "------------------------------------------------"
