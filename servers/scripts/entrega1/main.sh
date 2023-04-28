#!/bin/bash

# Ejecutar script desde esta carpeta

CYAN=$(tput setaf 6)
RESET=$(tput sgr0)
BOLD=$(tput bold)

function asksure() {
    echo "${BOLD}${CYAN}[$(date +'%F %T')]: $1 (Yy/Nn)${RESET}"
    while read -r answer; do
        if [[ $answer = [YyNn] ]]; then
            [[ $answer = [Yy] ]] && retval=0
            [[ $answer = [Nn] ]] && retval=1
            break
        fi
        echo "${BOLD}${CYAN}[$(date +'%F %T')]: $1 (Yy/Nn)${RESET}"
    done

    return ${retval}
}

function main() {
    if [ -z "${MACHINE_IP}" ]; then
        echo "[$(date +'%F %T')]: No se ha encontrado la variable de entorno MACHINE_IP" 1>&2
        exit 1
    fi

    if asksure "¿Desea configurar la máquina?"; then
        ssh-keygen -f "${HOME}/.ssh/known_hosts" -R "${MACHINE_IP}"
        ssh -i ../../secure/key_prod_rsa ubuntu@${MACHINE_IP} 'bash -s' < ./setup-machine.sh
    fi

    if asksure "¿Desea Desplegar los componentes?"; then
        scp -i ../../secure/key_prod_rsa ../../../docker/docker-compose.prod.yml ubuntu@${MACHINE_IP}:~/docker-compose.prod.yml
        scp -i ../../secure/key_prod_rsa ./run.sh ubuntu@${MACHINE_IP}:~/run.sh
    fi

    if asksure "¿Desea entrar a la máquina para ejecutar ~/run.sh?"; then
        ssh -i ../../secure/key_prod_rsa ubuntu@${MACHINE_IP}
    fi
}

main