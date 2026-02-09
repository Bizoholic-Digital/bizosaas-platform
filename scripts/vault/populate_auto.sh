#!/bin/bash
set -e
VN=$1
if [ -z "$VN" ]; then echo "Usage: ./populate_auto.sh <TOKEN>"; exit 1; fi
export VAULT_TOKEN=$VN
export VAULT_ADDR="http://127.0.0.1:8200"

run_vault() {
  echo "Setting $1..."
  docker exec -e VAULT_TOKEN=$VAULT_TOKEN -e VAULT_ADDR=$VAULT_ADDR bizosaas-vault vault kv put -mount=secret $1 $2=$3 > /dev/null
}

run_vault "production/core/django" "secret_key" "PLACEHOLDER_DJANGO_KEY"
run_vault "production/core/database" "password" "PLACEHOLDER_POSTGRES_PASS"
run_vault "production/core/redis" "password" "PLACEHOLDER_REDIS_PASS"
run_vault "production/integrations/shopify" "client_id" "PLACEHOLDER_SHOPIFY_ID"
run_vault "production/integrations/shopify" "client_secret" "PLACEHOLDER_SHOPIFY_SECRET"
run_vault "production/payment/stripe" "secret_key" "PLACEHOLDER_STRIPE_KEY"
run_vault "production/payment/paypal" "client_id" "PLACEHOLDER_PAYPAL_ID"
run_vault "production/payment/paypal" "client_secret" "PLACEHOLDER_PAYPAL_SECRET"

echo "DONE - Secrets Populated"
