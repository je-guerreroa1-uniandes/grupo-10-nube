#!/bin/bash

# clone repository
cd /home/ubuntu
git clone https://github.com/je-guerreroa1-uniandes/grupo-10-nube.git

# run setup machine script
chmod +x ./grupo-10-nube/servers/scripts/entrega1/setup-machine.sh
./grupo-10-nube/servers/scripts/entrega1/setup-machine.sh

# run setup nfs
chmod +x ./grupo-10-nube/servers/scripts/entrega2/setup-nfs-client.sh
./grupo-10-nube/servers/scripts/entrega2/setup-nfs-client.sh

# start API
chmod +x ./grupo-10-nube/docker/start-api.sh
cd ./grupo-10-nube/docker
./start-api.sh

# create and start docker-compose-api service
sudo tee /etc/systemd/system/docker-compose-api.service > /dev/null <<EOF
[Unit]
Description=Docker Compose for API
Requires=docker.service
After=docker.service

[Service]
Restart=always
User=ubuntu
WorkingDirectory=/home/ubuntu/grupo-10-nube/docker
ExecStart=/usr/bin/sudo /usr/bin/docker compose --file /home/ubuntu/grupo-10-nube/docker/docker-compose.api.dev.yml up -d --build --remove-orphans
ExecStop=/usr/bin/sudo /usr/bin/docker compose --file /home/ubuntu/grupo-10-nube/docker/docker-compose.api.dev.yml down


[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable docker-compose-api.service
sudo systemctl start docker-compose-api.service
sudo systemctl status docker-compose-api.service