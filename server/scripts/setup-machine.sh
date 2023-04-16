#!/bin/bash -x

# Instalar Docker
sudo apt update
sudo apt -y install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
apt-cache policy docker-ce
sudo apt -y install docker-ce docker-compose-plugin
sudo systemctl status docker
sudo usermod -aG docker ${USER}

# Logearse en ghcr.io (mejor manualmente, para hacerlo solo una vez)
# docker login ghcr.io -u <username>

# Crear la redirección de puertos (mejor manualmente, para hacerlo solo una vez)
# https://youtu.be/d6qtr-rYxXw?t=241
# sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8888
# sudo iptables -t nat -A OUTPUT -o lo -p tcp --dport 80 -j REDIRECT --to-port 8888
