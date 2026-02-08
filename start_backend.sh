#!/bin/bash
docker-compose --env-file staging.env -f docker-compose.core.yml up -d brain-gateway
docker-compose -f docker-compose.core.yml ps brain-gateway
