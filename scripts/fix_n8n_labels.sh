#!/bin/bash
# fix_n8n_labels.sh

cat << 'EOF' > n8n_compose.yml
services:
  postgres:
    image: postgres:17-alpine
    restart: unless-stopped
    environment:
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=${POSTGRES_DB}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test:
        - CMD-SHELL
        - pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}
      start_period: 30s
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - automationhub-n8nwithpostgres-nzgisq
  n8n:
    image: n8nio/n8n:1.122.4
    restart: unless-stopped
    environment:
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_PORT=5432
      - DB_POSTGRESDB_DATABASE=${POSTGRES_DB}
      - DB_POSTGRESDB_USER=${POSTGRES_USER}
      - DB_POSTGRESDB_PASSWORD=${POSTGRES_PASSWORD}
      - N8N_ENCRYPTION_KEY=${N8N_ENCRYPTION_KEY}
      - N8N_HOST=${N8N_HOST}
      - N8N_PORT=${N8N_PORT}
      - N8N_PROTOCOL=http
      - NODE_ENV=production
      - WEBHOOK_URL=https://${N8N_HOST}/
      - GENERIC_TIMEZONE=${GENERIC_TIMEZONE}
      - N8N_SECURE_COOKIE=false
    volumes:
      - n8n_data:/home/node/.n8n
    depends_on:
      postgres:
        condition: service_healthy
    networks:
      - automationhub-n8nwithpostgres-nzgisq
      - dokploy-network
    labels:
      - traefik.enable=true
      - traefik.docker.network=dokploy-network
      - traefik.http.routers.n8n-c8d.rule=Host(`c8d.coreldove.com`)
      - traefik.http.routers.n8n-c8d.entrypoints=web
      - traefik.http.routers.n8n-c8d.middlewares=redirect-to-https@file
      - traefik.http.routers.n8n-c8d-secure.rule=Host(`c8d.coreldove.com`)
      - traefik.http.routers.n8n-c8d-secure.entrypoints=websecure
      - traefik.http.routers.n8n-c8d-secure.tls.certresolver=letsencrypt
      - traefik.http.routers.n8n-c8d-secure.service=n8n-service
      - traefik.http.services.n8n-service.loadbalancer.server.port=5678
volumes:
  n8n_data: null
  postgres_data: null
networks:
  automationhub-n8nwithpostgres-nzgisq:
    name: automationhub-n8nwithpostgres-nzgisq
    external: true
  dokploy-network:
    name: dokploy-network
    external: true
EOF

scp -o StrictHostKeyChecking=no n8n_compose.yml root@194.238.16.237:/etc/dokploy/compose/automationhub-n8nwithpostgres-nzgisq/code/docker-compose.yml
ssh -o StrictHostKeyChecking=no root@194.238.16.237 "cd /etc/dokploy/compose/automationhub-n8nwithpostgres-nzgisq/code && docker compose -p automationhub-n8nwithpostgres-nzgisq up -d"

rm n8n_compose.yml
