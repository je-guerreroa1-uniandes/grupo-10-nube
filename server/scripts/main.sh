#!/bin/bash

# Ejecutar script desde esta carpeta

# TODO: Escribir la ip correcta (Cambia en cada reinicio / cada 4 horas)
MACHINE_IP='54.84.119.128'

function asksure() {
    echo "[$(date +'%F %T')]: $1 (Yy/Nn)"
    while read -r answer; do
        if [[ $answer = [YyNn] ]]; then
            [[ $answer = [Yy] ]] && retval=0
            [[ $answer = [Nn] ]] && retval=1
            break
        fi
        echo "[$(date +'%F %T')]: $1 (Yy/Nn)"
    done

    return ${retval}
}

function main() {
    if asksure "¿Desea configurar la máquina?"; then
        ssh -i ../secure/llavemaquina.pem ubuntu@${MACHINE_IP} 'bash -s' < ./setup-machine.sh
    fi

    if asksure "¿Desea Desplegar los componentes?"; then
        scp -i ../secure/llavemaquina.pem ../../docker/docker-compose.prod.yml ubuntu@${MACHINE_IP}:~/docker-compose.prod.yml
        scp -i ../secure/llavemaquina.pem ./run.sh ubuntu@${MACHINE_IP}:~/run.sh
    fi

    if asksure "¿Desea entrar a la máquina para ejecutar ~/run.sh?"; then
        ssh -i ../secure/llavemaquina.pem ubuntu@${MACHINE_IP}
    fi
}

main