# Vault Setup and Configuration

## Current Status
✅ **Vault Container Running**
- Container: `brain-vault` (ID: fb0d48492e4c)
- Network: `brain-network`
- Port: `8200:8200`
- Token: `staging-root-token-bizosaas-2025`
- Status: Initialized and unsealed

## Configuration

### Environment Variables
```bash
USE_VAULT=true
VAULT_ADDR=http://vault:8200
VAULT_TOKEN=staging-root-token-bizosaas-2025
```

### Docker Run Command
```bash
docker run -d \
  --name brain-vault \
  --network brain-network \
  --network-alias vault \
  -p 8200:8200 \
  -e VAULT_DEV_ROOT_TOKEN_ID=staging-root-token-bizosaas-2025 \
  -e VAULT_DEV_LISTEN_ADDRESS=0.0.0.0:8200 \
  --cap-add IPC_LOCK \
  --restart unless-stopped \
  hashicorp/vault:latest
```

## Portal Integration

### Admin Dashboard & Client Portal
Both portals now have **optional** Vault integration:
- If `VAULT_TOKEN` and `VAULT_SECRET_PATH` are set, secrets will be injected
- If not set, portals will start normally without Vault
- This prevents the "VAULT_TOKEN and VAULT_SECRET_PATH must be set" error

### Updated Dockerfile CMD
```dockerfile
CMD ["sh", "-c", "if [ -n \"$VAULT_TOKEN\" ] && [ -n \"$VAULT_SECRET_PATH\" ]; then eval $(node scripts/vault-injector.js 2>/dev/null || echo ''); fi && node server.js"]
```

## Verification

### Check Vault Health
```bash
curl http://localhost:8200/v1/sys/health | jq .
```

Expected response:
```json
{
  "initialized": true,
  "sealed": false,
  "standby": false,
  "version": "1.21.1"
}
```

### Test Authentication
```bash
export VAULT_ADDR=http://localhost:8200
export VAULT_TOKEN=staging-root-token-bizosaas-2025
vault status
```

## Next Steps

1. **For Production**: Replace dev mode with proper Vault setup
   - Use sealed Vault with proper unseal keys
   - Configure TLS/SSL
   - Set up proper authentication methods (AppRole, Kubernetes, etc.)

2. **Secret Management**:
   ```bash
   # Store secrets
   vault kv put secret/bizosaas/portals/admin-dashboard \
     NEXT_PUBLIC_API_URL=https://api.bizoholic.net \
     CLERK_SECRET_KEY=sk_...
   
   # Read secrets
   vault kv get secret/bizosaas/portals/admin-dashboard
   ```

3. **Environment Setup**:
   - Set `VAULT_SECRET_PATH` for each portal (e.g., `secret/data/bizosaas/portals/admin-dashboard`)
   - Ensure `VAULT_TOKEN` is available in deployment environment

## Troubleshooting

### Error: "permission denied * invalid token"
**Solution**: Recreate Vault container with correct token as shown above

### Error: "VAULT_TOKEN and VAULT_SECRET_PATH must be set"
**Solution**: Either:
- Set the required environment variables, OR
- Use the updated Dockerfiles that make Vault optional

### Container Not Starting
```bash
# Check logs
docker logs brain-vault

# Restart container
docker restart brain-vault
```

## Security Notes

⚠️ **Development Mode Warning**
- Current setup uses Vault in DEV mode (not production-ready)
- Root token is stored in plain text
- No TLS encryption
- Data is not persisted (stored in memory)

For production, follow HashiCorp's [Production Hardening](https://developer.hashicorp.com/vault/tutorials/operations/production-hardening) guide.
