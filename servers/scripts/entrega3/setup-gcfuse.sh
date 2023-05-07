#!/bin/bash

# Add the GCSFuse repository to package sources
export GCSFUSE_REPO=gcsfuse-$(lsb_release -c -s)
echo "deb http://packages.cloud.google.com/apt $GCSFUSE_REPO main" | sudo tee /etc/apt/sources.list.d/gcsfuse.list

# Download and add the GCSFuse GPG key
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -

# Update package lists
sudo apt-get update

# Install GCSFuse
sudo apt-get install gcsfuse
sudo mkdir -p /gcsfuse/general

# create and start gcsfuse service
sudo tee /etc/systemd/system/gcsfuse.service > /dev/null <<EOF
[Unit]
Description=GCSFuse Mount
After=network-online.target

[Service]
Type=simple
ExecStart=/usr/bin/sudo /usr/bin/gcsfuse --only-dir general uniandes-grupo-10.appspot.com /gcsfuse/general
ExecStop=/usr/bin/sudo /bin/fusermount -u /gcsfuse/general
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable gcsfuse.service
sudo systemctl start gcsfuse.service
sudo systemctl status gcsfuse.service