# QuantTrade Deployment Guide

## 🚀 Complete Deployment Instructions

This guide covers deploying QuantTrade to production using HashiCorp Vault for secrets management.

---

## Prerequisites

- Docker & Docker Compose installed
- HashiCorp Vault server running
- PostgreSQL with pgvector extension
- Redis server
- Temporal server
- BizOSaaS Brain API Gateway

---

## 1. Vault Setup

### Initialize Vault Secrets

```bash
# Login to Vault
export VAULT_ADDR='http://your-vault-server:8200'
export VAULT_TOKEN='your-vault-token'
export VAULT_NAMESPACE='admin'

# Create secrets for Deribit
vault kv put secret/quanttrade/exchanges/deribit \
  api_key="your_deribit_api_key" \
  api_secret="your_deribit_api_secret" \
  testnet=true

# Create secrets for Binance
vault kv put secret/quanttrade/exchanges/binance \
  api_key="your_binance_api_key" \
  api_secret="your_binance_api_secret" \
  testnet=true

# Create database credentials
vault kv put secret/quanttrade/database \
  host="postgres" \
  port=5432 \
  database="bizosaas" \
  username="postgres" \
  password="your_db_password"

# Create Brain API credentials
vault kv put secret/quanttrade/brain-api \
  url="http://brain-gateway:8002" \
  api_key="your_brain_api_key"

# Create JWT secret
vault kv put secret/quanttrade/auth \
  secret_key="your_jwt_secret_key_min_32_characters"
```

### Verify Secrets

```bash
# Verify Deribit credentials
vault kv get secret/quanttrade/exchanges/deribit

# Verify Binance credentials
vault kv get secret/quanttrade/exchanges/binance

# Verify database credentials
vault kv get secret/quanttrade/database

# Verify Brain API credentials
vault kv get secret/quanttrade/brain-api
```

---

## 2. Environment Configuration

Create `.env` file with only Vault connection details:

```bash
# Vault Configuration (ONLY these are needed)
VAULT_ADDR=http://vault:8200
VAULT_TOKEN=your_vault_token
VAULT_NAMESPACE=admin

# Optional: Temporal Configuration
TEMPORAL_HOST=temporal:7233
TEMPORAL_NAMESPACE=default
```

---

## 3. Database Setup

### Create Database and Extensions

```sql
-- Connect to PostgreSQL
psql -U postgres

-- Create database (if not exists)
CREATE DATABASE bizosaas;

-- Connect to database
\c bizosaas

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Verify extension
SELECT * FROM pg_extension WHERE extname = 'vector';
```

### Run Migrations

```bash
cd /home/alagiri/projects/bizosaas-platform/quanttrade/backend

# Run Alembic migrations
alembic upgrade head
```

---

## 4. Docker Deployment

### Build and Start Services

```bash
cd /home/alagiri/projects/bizosaas-platform/quanttrade

# Build images
docker-compose build

# Start services
docker-compose up -d

# Check logs
docker-compose logs -f quanttrade-backend
docker-compose logs -f quanttrade-frontend
```

### Verify Services

```bash
# Check backend health
curl http://localhost:8012/health

# Check frontend
curl http://localhost:3010

# Check Temporal
curl http://localhost:8202
```

---

## 5. Initialize AI Agents

### Register Agents with Brain API

```bash
# Access backend container
docker exec -it quanttrade-backend bash

# Run agent initialization
python -c "
from app.agents.trading_agents import initialize_agents
import asyncio
asyncio.run(initialize_agents())
"
```

---

## 6. Production Deployment

### Using Traefik (Recommended)

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  quanttrade-backend:
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.quanttrade-api.rule=Host(`api.quanttrade.yourdomain.com`)"
      - "traefik.http.routers.quanttrade-api.entrypoints=websecure"
      - "traefik.http.routers.quanttrade-api.tls.certresolver=letsencrypt"
      - "traefik.http.services.quanttrade-api.loadbalancer.server.port=8012"

  quanttrade-frontend:
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.quanttrade-web.rule=Host(`quanttrade.yourdomain.com`)"
      - "traefik.http.routers.quanttrade-web.entrypoints=websecure"
      - "traefik.http.routers.quanttrade-web.tls.certresolver=letsencrypt"
      - "traefik.http.services.quanttrade-web.loadbalancer.server.port=3010"
```

Deploy:

```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

---

## 7. Monitoring & Logging

### View Logs

```bash
# Backend logs
docker-compose logs -f quanttrade-backend

# Frontend logs
docker-compose logs -f quanttrade-frontend

# Temporal logs
docker-compose logs -f temporal
```

### Health Checks

```bash
# Backend health
curl http://localhost:8012/health

# Check Vault connection
curl http://localhost:8012/api/health/vault

# Check database connection
curl http://localhost:8012/api/health/database

# Check Temporal connection
curl http://localhost:8012/api/health/temporal
```

---

## 8. Testing

### Paper Trading Mode

```bash
# Ensure paper trading is enabled
vault kv patch secret/quanttrade/config \
  enable_paper_trading=true

# Restart backend
docker-compose restart quanttrade-backend
```

### Run Backtest

```bash
# Access backend container
docker exec -it quanttrade-backend bash

# Run sample backtest
python -c "
from services.backtesting_service import BacktestingEngine, BacktestConfig
from services.strategy_engine import RSIMomentumStrategy
import asyncio

async def run_backtest():
    config = BacktestConfig(initial_capital=100000)
    engine = BacktestingEngine(config)
    strategy = RSIMomentumStrategy('BTCUSDT')
    # Add your market data here
    result = await engine.run_backtest(strategy, market_data)
    print(result)

asyncio.run(run_backtest())
"
```

---

## 9. Backup & Recovery

### Backup Vault Secrets

```bash
# Export all QuantTrade secrets
vault kv get -format=json secret/quanttrade > quanttrade-secrets-backup.json

# Store securely (encrypted)
gpg -c quanttrade-secrets-backup.json
```

### Backup Database

```bash
# Backup PostgreSQL
docker exec postgres pg_dump -U postgres bizosaas > bizosaas-backup.sql

# Restore
docker exec -i postgres psql -U postgres bizosaas < bizosaas-backup.sql
```

---

## 10. Security Checklist

- [ ] Vault secrets properly configured
- [ ] Database credentials stored in Vault
- [ ] Exchange API keys stored in Vault
- [ ] JWT secret key is strong (32+ characters)
- [ ] Paper trading enabled for testing
- [ ] SSL/TLS enabled for production
- [ ] Firewall rules configured
- [ ] Regular backups scheduled
- [ ] Monitoring and alerts configured
- [ ] Rate limiting enabled

---

## 11. Troubleshooting

### Vault Connection Issues

```bash
# Check Vault status
vault status

# Test authentication
vault token lookup

# Check secret access
vault kv get secret/quanttrade/exchanges/deribit
```

### Database Connection Issues

```bash
# Check PostgreSQL
docker exec postgres psql -U postgres -c "SELECT version();"

# Check pgvector extension
docker exec postgres psql -U postgres bizosaas -c "SELECT * FROM pg_extension WHERE extname = 'vector';"
```

### Backend Issues

```bash
# Check logs
docker-compose logs quanttrade-backend

# Access container
docker exec -it quanttrade-backend bash

# Test imports
python -c "from services.vault_client import get_vault_client; print(get_vault_client())"
```

---

## 12. Scaling

### Horizontal Scaling

```yaml
# docker-compose.scale.yml
services:
  quanttrade-backend:
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '2'
          memory: 4G
```

Deploy:

```bash
docker-compose -f docker-compose.yml -f docker-compose.scale.yml up -d --scale quanttrade-backend=3
```

---

## 13. Maintenance

### Update Secrets

```bash
# Update Deribit API key
vault kv patch secret/quanttrade/exchanges/deribit \
  api_key="new_api_key"

# Restart backend to pick up changes
docker-compose restart quanttrade-backend
```

### Update Application

```bash
# Pull latest code
git pull origin main

# Rebuild images
docker-compose build

# Rolling update
docker-compose up -d --no-deps --build quanttrade-backend
docker-compose up -d --no-deps --build quanttrade-frontend
```

---

## 14. Production Checklist

**Before Going Live:**

- [ ] All secrets in Vault (no .env files)
- [ ] Database backups configured
- [ ] Monitoring and alerts set up
- [ ] SSL/TLS certificates installed
- [ ] Rate limiting configured
- [ ] Paper trading tested thoroughly
- [ ] All AI agents registered
- [ ] Temporal workflows tested
- [ ] WebSocket connections tested
- [ ] Exchange API limits understood
- [ ] Risk limits configured
- [ ] Emergency stop procedures documented

---

## 15. Support

**Documentation:**
- [Implementation Plan](file:///home/alagiri/.gemini/antigravity/brain/c832c9d9-f704-4616-8c9e-8d375fdce23e/implementation_plan.md)
- [Architecture](file:///home/alagiri/.gemini/antigravity/brain/c832c9d9-f704-4616-8c9e-8d375fdce23e/quanttrade_architecture.md)
- [Final Summary](file:///home/alagiri/.gemini/antigravity/brain/c832c9d9-f704-4616-8c9e-8d375fdce23e/final_summary.md)

**Code:**
- Backend: `/home/alagiri/projects/bizosaas-platform/quanttrade/backend`
- Frontend: `/home/alagiri/projects/bizosaas-platform/quanttrade/frontend`

---

## Quick Start (Development)

```bash
# 1. Setup Vault secrets (see section 1)

# 2. Create .env with Vault credentials only
cat > .env << EOF
VAULT_ADDR=http://localhost:8200
VAULT_TOKEN=your_vault_token
VAULT_NAMESPACE=admin
EOF

# 3. Start services
docker-compose up -d

# 4. Initialize agents
docker exec -it quanttrade-backend python -c "from app.agents.trading_agents import initialize_agents; import asyncio; asyncio.run(initialize_agents())"

# 5. Access application
# Frontend: http://localhost:3010
# Backend API: http://localhost:8012
# Temporal UI: http://localhost:8203
```

---

**🎉 QuantTrade is now deployed with Vault-based secrets management!**
