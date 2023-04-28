#!/bin/bash

# Ejecutar script desde esta carpeta 

rm -i key_prod_rsa
rm -i key_prod_rsa.pub

# 1) File
# 2,3) password & password confirmation. Vacias para poder hacers despliegues desatendidos.
( echo "${PWD}/key_prod_rsa"; echo ''; echo '') | ssh-keygen -t rsa -b 4096
chmod 400 key_prod_rsa*