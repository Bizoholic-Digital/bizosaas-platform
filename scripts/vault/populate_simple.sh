#!/bin/bash
set -e
VN=$1
if [ -z "$VN" ]; then echo "Usage: ./populate_simple.sh <TOKEN>"; exit 1; fi
export VAULT_TOKEN=$VN
export VAULT_ADDR="http://127.0.0.1:8200"

run_vault() {
  echo "Setting $1..."
  docker exec -e VAULT_TOKEN=$VAULT_TOKEN -e VAULT_ADDR=$VAULT_ADDR bizosaas-vault vault kv put -mount=secret $1 $2=$3 > /dev/null
}

run_vault "production/core/django" "secret_key" "REPLACE_WITH_SECRET_KEY"
run_vault "production/core/database" "password" "REPLACE_WITH_DB_PASSWORD"
run_vault "production/core/redis" "password" "REPLACE_WITH_REDIS_PASSWORD"
run_vault "production/integrations/shopify" "client_id" "REPLACE_WITH_SHOPIFY_CLIENT_ID"
run_vault "production/integrations/shopify" "client_secret" "REPLACE_WITH_SHOPIFY_CLIENT_SECRET"
run_vault "production/payment/stripe" "secret_key" "sk_test_key"
run_vault "production/payment/paypal" "client_id" "sandbox_id"
run_vault "production/payment/paypal" "client_secret" "sandbox_secret"

echo "DONE - Secrets Populated"
