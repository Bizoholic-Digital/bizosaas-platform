# vault policy for brain-gateway
# File: infrastructure/vault/policies/gateway-policy.hcl

# Read-only access to platform-wide secrets
path "secret/data/platform/*" {
  capabilities = ["read"]
}

# Read-only access to integration-specific secrets
path "secret/data/integrations/*" {
  capabilities = ["read"]
}

# Read/Write/Delete access to tenant-specific secrets (required for provisioning)
path "secret/data/tenants/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

# Allow listing of secrets
path "secret/metadata/*" {
  capabilities = ["list"]
}
