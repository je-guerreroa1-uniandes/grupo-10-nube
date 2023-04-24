#!/bin/bash -x

sudo apt update
sudo apt -y install nfs-common
sudo mkdir -p /nfs/general
sudo mount 10.120.0.3:/var/nfs/general /nfs/general

# Verificar que se haya montado correctamente
sudo du -h

sudo grep '10.120.0.3' /etc/fstab 2>&1 >/dev/null && sudo sed -i '/10.120.0.3/d' /etc/fstab
sudo echo '10.120.0.3:/var/nfs/general /nfs/general nfs auto,nofail,noatime,nolock,intr,tcp,actimeo=1800 0 0' | sudo tee -a /etc/fstab