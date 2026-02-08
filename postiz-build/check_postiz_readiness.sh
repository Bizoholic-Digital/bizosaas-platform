#!/bin/bash
echo "Checking Postiz stack health..."
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep postiz
