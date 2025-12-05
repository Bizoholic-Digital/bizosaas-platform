storage "file" {
  path = "/vault/data"
}

listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_disable = 1
}

api_addr = "http://0.0.0.0:8200"
cluster_addr = "http://0.0.0.0:8201"
ui = true

# Development mode - for production use proper storage backend
disable_mlock = true
default_lease_ttl = "168h"
max_lease_ttl = "720h"

# Plugin directory for custom auth methods
plugin_directory = "/vault/plugins"

# Log level
log_level = "INFO"

# Enable raw endpoint for health checks
raw_storage_endpoint = true

# Seal configuration for auto-unseal in production
# seal "awskms" {
#   region     = "us-west-2"
#   kms_key_id = "REPLACE-ME"
# }