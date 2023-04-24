#!/bin/bash -x

sudo apt update
sudo apt -y install nfs-kernel-server
sudo mkdir /var/nfs/general -p
sudo chown nobody:nogroup /var/nfs/general
sudo grep '/var/nfs/general' /etc/exports 2>&1 >/dev/null && sudo sed -i '/\/var\/nfs\/general/d' /etc/exports
sudo echo '/var/nfs/general *(rw,sync,no_subtree_check)' | sudo tee -a /etc/exports
sudo systemctl restart nfs-kernel-server

# Verificar que se haya montado correctamente
sudo exportfs