#!/bin/bash -x

# Crear la redirección de puertos (mejor manualmente, para hacerlo solo una vez)
# https://youtu.be/d6qtr-rYxXw?t=241
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8888
sudo iptables -t nat -A OUTPUT -o lo -p tcp --dport 80 -j REDIRECT --to-port 8888
sudo iptables-save