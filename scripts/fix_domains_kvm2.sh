#!/bin/bash
# fix_domains_kvm2.sh

# Fix Bizoholic Labels & Networks
cat << 'EOF' > bizoholic_compose.yml
services:
  wordpress:
    image: wordpress:latest
    volumes:
      - wp_app:/var/www/html
      - ../files/uploads.ini:/usr/local/etc/php/conf.d/uploads.ini
    environment:
      WORDPRESS_DB_HOST: wp_db
      WORDPRESS_DB_NAME: $DB_NAME
      WORDPRESS_DB_USER: root
      WORDPRESS_DB_PASSWORD: $DB_PASSWORD
      WORDPRESS_DEBUG: ${WORDPRESS_DEBUG:-0}
      WORDPRESS_CONFIG_EXTRA: |
        define('WP_MEMORY_LIMIT', '256M');
        define('DISALLOW_FILE_EDIT', true);
    depends_on:
      wp_db:
        condition: service_started
    restart: unless-stopped
    networks:
      - bizoholicwebsite-wordpress-rbtyli
      - dokploy-network
    labels:
      - traefik.enable=true
      - traefik.docker.network=dokploy-network
      - traefik.http.routers.bizoholic-wp.rule=Host(`bizoholic.com`, `www.bizoholic.com`)
      - traefik.http.routers.bizoholic-wp.entrypoints=web
      - traefik.http.routers.bizoholic-wp.middlewares=redirect-to-https@file
      - traefik.http.routers.bizoholic-wp-secure.rule=Host(`bizoholic.com`, `www.bizoholic.com`)
      - traefik.http.routers.bizoholic-wp-secure.entrypoints=websecure
      - traefik.http.routers.bizoholic-wp-secure.tls.certresolver=letsencrypt
      - traefik.http.services.bizoholic-wp.loadbalancer.server.port=80
  wp_db:
    image: mysql:8.4
    restart: unless-stopped
    volumes:
      - wp_data:/var/lib/mysql
    environment:
      MYSQL_ROOT_PASSWORD: $DB_PASSWORD
      MYSQL_DATABASE: $DB_NAME
    networks:
      - bizoholicwebsite-wordpress-rbtyli
volumes:
  wp_app: null
  wp_data: null
networks:
  bizoholicwebsite-wordpress-rbtyli:
    name: bizoholicwebsite-wordpress-rbtyli
    external: true
  dokploy-network:
    name: dokploy-network
    external: true
EOF

# Fix CorelDove Labels & Networks
cat << 'EOF' > coreldove_compose.yml
services:
  wordpress:
    image: wordpress:latest
    volumes:
      - wp_app:/var/www/html
      - ../files/uploads.ini:/usr/local/etc/php/conf.d/uploads.ini
    environment:
      WORDPRESS_DB_HOST: wp_db
      WORDPRESS_DB_NAME: $DB_NAME
      WORDPRESS_DB_USER: root
      WORDPRESS_DB_PASSWORD: $DB_PASSWORD
      WORDPRESS_DEBUG: ${WORDPRESS_DEBUG:-0}
      WORDPRESS_CONFIG_EXTRA: |
        define('WP_MEMORY_LIMIT', '256M');
        define('DISALLOW_FILE_EDIT', true);
    depends_on:
      wp_db:
        condition: service_started
    restart: unless-stopped
    labels:
      - traefik.enable=true
      - traefik.docker.network=dokploy-network
      - traefik.http.routers.coreldove-wp.rule=Host(`coreldove.com`, `www.coreldove.com`)
      - traefik.http.routers.coreldove-wp.entrypoints=web
      - traefik.http.routers.coreldove-wp.middlewares=redirect-to-https@file
      - traefik.http.routers.coreldove-wp-secure.rule=Host(`coreldove.com`, `www.coreldove.com`)
      - traefik.http.routers.coreldove-wp-secure.entrypoints=websecure
      - traefik.http.routers.coreldove-wp-secure.tls.certresolver=letsencrypt
      - traefik.http.services.coreldove-wp.loadbalancer.server.port=80
      - traefik.http.routers.coreldove-stg1.rule=Host(`stg1.coreldove.com`)
      - traefik.http.routers.coreldove-stg1.entrypoints=websecure
      - traefik.http.routers.coreldove-stg1.tls.certresolver=letsencrypt
    networks:
      - coreldovewebsite-wordpress-fnoyyo
      - dokploy-network
  wp_db:
    image: mysql:8.4
    restart: unless-stopped
    volumes:
      - wp_data:/var/lib/mysql
    environment:
      MYSQL_ROOT_PASSWORD: $DB_PASSWORD
      MYSQL_DATABASE: $DB_NAME
    networks:
      - coreldovewebsite-wordpress-fnoyyo
volumes:
  wp_app: null
  wp_data: null
networks:
  coreldovewebsite-wordpress-fnoyyo:
    name: coreldovewebsite-wordpress-fnoyyo
    external: true
  dokploy-network:
    name: dokploy-network
    external: true
EOF

# Update n8n Labels & Networks
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
      - traefik.http.services.n8n-c8d.loadbalancer.server.port=5678
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

echo "Transferring configurations..."
scp -o StrictHostKeyChecking=no bizoholic_compose.yml root@194.238.16.237:/etc/dokploy/compose/bizoholicwebsite-wordpress-rbtyli/code/docker-compose.yml
scp -o StrictHostKeyChecking=no coreldove_compose.yml root@194.238.16.237:/etc/dokploy/compose/coreldovewebsite-wordpress-fnoyyo/code/docker-compose.yml
scp -o StrictHostKeyChecking=no n8n_compose.yml root@194.238.16.237:/etc/dokploy/compose/automationhub-n8nwithpostgres-nzgisq/code/docker-compose.yml

echo "Restarting services..."
ssh -o StrictHostKeyChecking=no root@194.238.16.237 "cd /etc/dokploy/compose/bizoholicwebsite-wordpress-rbtyli/code && docker compose -p bizoholicwebsite-wordpress-rbtyli up -d"
ssh -o StrictHostKeyChecking=no root@194.238.16.237 "cd /etc/dokploy/compose/coreldovewebsite-wordpress-fnoyyo/code && docker compose -p coreldovewebsite-wordpress-fnoyyo up -d"
ssh -o StrictHostKeyChecking=no root@194.238.16.237 "cd /etc/dokploy/compose/automationhub-n8nwithpostgres-nzgisq/code && docker compose -p automationhub-n8nwithpostgres-nzgisq up -d"

# Clean up local
rm bizoholic_compose.yml coreldove_compose.yml n8n_compose.yml
