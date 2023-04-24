#!/bin/bash -x

CYAN=$(tput setaf 6)
RESET=$(tput sgr0)
BOLD=$(tput bold)

echo 'si no esta logeado ejecutar: docker login ghcr.io -u <username>'

cd ~

echo "${BOLD}${CYAN}¿Eliminar los contenedores, imagenes y volumenes? (No usar en la primera ejecución) [Yy/Nn]${RESET}"
read -u 1 -n 1 key
{ [[ $key = "y" ]] || [[ $key = "Y" ]]; } && docker compose -f docker-compose.prod.yml down -v --rmi all

docker compose -f docker-compose.prod.yml up -d --build --remove-orphans api custom-nginx