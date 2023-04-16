#!/bin/bash -x

echo 'si no esta logeado ejecutar: docker login ghcr.io -u <username>'

cd ~
docker compose -f docker-compose.prod.yml down -v --rmi all
docker compose -f docker-compose.prod.yml up -d --build