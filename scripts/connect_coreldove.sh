#!/bin/bash

echo "Connecting CorelDove WordPress..."
curl -v -X POST https://api.bizoholic.net/api/connectors/wordpress/connect \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.coreldove.com/",
    "username": "coreldove.admin",
    "application_password": "xNeZ DGuP Of7x pfPM 4QDa PkkO"
  }'

echo -e "\n\nConnecting CorelDove FluentCRM..."
curl -v -X POST https://api.bizoholic.net/api/connectors/fluentcrm/connect \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.coreldove.com/",
    "username": "coreldove.admin",
    "application_password": "xNeZ DGuP Of7x pfPM 4QDa PkkO"
  }'

echo -e "\n\nConnecting CorelDove WooCommerce..."
curl -v -X POST https://api.bizoholic.net/api/connectors/woocommerce/connect \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.coreldove.com/",
    "consumer_key": "coreldove.admin",
    "consumer_secret": "xNeZ DGuP Of7x pfPM 4QDa PkkO"
  }'
