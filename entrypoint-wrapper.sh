#!/bin/bash
set -e
export LAGO_RSA_PRIVATE_KEY="$(base64 -d /app/keys/lago_private.b64)"
export LAGO_RSA_PUBLIC_KEY="$(base64 -d /app/keys/lago_public.b64)"
echo "Testing keys with ruby inside container..."
# Using a temp file to avoid env var length issues in the test command if any
echo "$LAGO_RSA_PRIVATE_KEY" > /tmp/test_priv.pem
echo "$LAGO_RSA_PUBLIC_KEY" > /tmp/test_pub.pem
ruby -e "require 'openssl'; OpenSSL::PKey::RSA.new(File.read('/tmp/test_priv.pem')); puts 'Private Key OK'; OpenSSL::PKey::RSA.new(File.read('/tmp/test_pub.pem')); puts 'Public Key OK'"
echo "Internal key test passed. Starting application..."
exec "$@"
