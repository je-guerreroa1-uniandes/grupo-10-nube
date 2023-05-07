#!/bin/bash -x

sudo apt update
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
sudo mkdir -p /gcfuse/general

sudo gcsfuse --foreground --only-dir general uniandes-grupo-10.appspot.com /gcsfuse/general

# create and start gcsfuse service
sudo tee /etc/systemd/system/gcsfuse.service > /dev/null <<EOF
[Unit]
Description=GCSFuse Mount

[Service]
Type=simple
ExecStart=/usr/bin/gcsfuse --foreground --only-dir general uniandes-grupo-10.appspot.com /gcsfuse/general
ExecStop=/bin/fusermount -u /gcsfuse/general
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable gcsfuse.service
sudo systemctl start gcsfuse.service
sudo systemctl status gcsfuse.service