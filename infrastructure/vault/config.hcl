# HashiCorp Vault Configuration for BizOSaaS
# File: infrastructure/vault/config.hcl

storage "file" {
  path = "/vault/file"
}

listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_disable = 1 # We will use Traefik for SSL termination
}

api_addr = "http://vault.bizoholic.net:8200"
cluster_addr = "https://127.0.0.1:8201"
ui = true

# Enable KV secrets engine version 2 by default is handled via CLI after init
