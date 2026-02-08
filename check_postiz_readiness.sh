#!/bin/bash
# Postiz Readiness Check Script

set -e

echo "Checking Postiz services on KVM2..."

# 1. Check PostgreSQL
echo "Waiting for Postiz PostgreSQL to be healthy..."
until [ "$(sshpass -p "&k3civYG5Q6YPb" ssh -o StrictHostKeyChecking=no root@194.238.16.237 "docker inspect -f '{{.State.Health.Status}}' postiz-postgres 2>/dev/null")" == "healthy" ]; do
  printf "."
  sleep 5
done
echo "PostgreSQL is healthy!"

# 2. Check Redis
echo "Waiting for Postiz Redis to be healthy..."
until [ "$(sshpass -p "&k3civYG5Q6YPb" ssh -o StrictHostKeyChecking=no root@194.238.16.237 "docker inspect -f '{{.State.Health.Status}}' postiz-redis 2>/dev/null")" == "healthy" ]; do
  printf "."
  sleep 5
done
echo "Redis is healthy!"

# 3. Check App
echo "Waiting for Postiz App to be up..."
until [ "$(sshpass -p "&k3civYG5Q6YPb" ssh -o StrictHostKeyChecking=no root@194.238.16.237 "docker ps -q -f name=postiz-app")" ]; do
  printf "."
  sleep 5
done
echo "Postiz App container is running!"

# 4. Check HTTP Access
echo "Verifying HTTP access at https://postiz.bizoholic.net..."
STATUS_CODE=$(curl -o /dev/null -s -w "%{http_code}" https://postiz.bizoholic.net)
if [ "$STATUS_CODE" -eq 200 ]; then
  echo "SUCCESS: Postiz is accessible at https://postiz.bizoholic.net"
else
  echo "WARNING: Postiz returned status code $STATUS_CODE"
fi
