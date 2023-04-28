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

function maquina_nfs() {
    if asksure "¿Desea hacer la configuración inicial de la máquina nfs?"; then
        ssh-keygen -f "${HOME}/.ssh/known_hosts" -R "${G10_NFS_IP}"
        ssh -i ../../secure/key_prod_rsa ubuntu@${G10_NFS_IP} 'bash -s' < ./setup-docker.sh
        ssh -i ../../secure/key_prod_rsa ubuntu@${G10_NFS_IP} 'bash -s' < ./setup-nfs-server.sh
    fi

    if asksure "¿Desea tranferir el docker-compose y las .env a la máquina nfs?"; then
        scp -i ../../secure/key_prod_rsa ../../../docker/docker-compose.prod.yml ubuntu@${G10_NFS_IP}:~/docker-compose.prod.yml
        scp -i ../../secure/key_prod_rsa ./run-nfs.sh ubuntu@${G10_NFS_IP}:~/run-nfs.sh
        scp -i ../../secure/key_prod_rsa ../../../docker/*.env ubuntu@${G10_NFS_IP}:~/
    fi

    if asksure "¿Desea entrar a la máquina para ejecutar ~/run-nfs.sh?"; then
        ssh -i ../../secure/key_prod_rsa ubuntu@${G10_NFS_IP}
    fi
}

function maquina_jobs() {
    if asksure "¿Desea hacer la configuración inicial de la máquina jobs?"; then
        ssh-keygen -f "${HOME}/.ssh/known_hosts" -R "${G10_JOBS_IP}"
        ssh -i ../../secure/key_prod_rsa ubuntu@${G10_JOBS_IP} 'bash -s' < ./setup-docker.sh
        ssh -i ../../secure/key_prod_rsa ubuntu@${G10_JOBS_IP} 'bash -s' < ./setup-nfs-client.sh
    fi

    if asksure "¿Desea tranferir el docker-compose y las .env a la máquina jobs?"; then
        scp -i ../../secure/key_prod_rsa ../../../docker/docker-compose.prod.yml ubuntu@${G10_JOBS_IP}:~/docker-compose.prod.yml
        scp -i ../../secure/key_prod_rsa ./run-jobs.sh ubuntu@${G10_JOBS_IP}:~/run-jobs.sh
        scp -i ../../secure/key_prod_rsa ../../../docker/*.env ubuntu@${G10_JOBS_IP}:~/
    fi

    if asksure "¿Desea entrar a la máquina para ejecutar ~/run-jobs.sh?"; then
        ssh -i ../../secure/key_prod_rsa ubuntu@${G10_JOBS_IP}
    fi
}

function maquina_reverse_proxy() {
    if asksure "¿Desea hacer la configuración inicial de la máquina reverse_proxy?"; then
        ssh-keygen -f "${HOME}/.ssh/known_hosts" -R "${G10_REVERSE_PROXY_IP}"
        ssh -i ../../secure/key_prod_rsa ubuntu@${G10_REVERSE_PROXY_IP} 'bash -s' < ./setup-docker.sh
        ssh -i ../../secure/key_prod_rsa ubuntu@${G10_REVERSE_PROXY_IP} 'bash -s' < ./setup-nfs-client.sh
        ssh -i ../../secure/key_prod_rsa ubuntu@${G10_REVERSE_PROXY_IP} 'bash -s' < ./setup-port-bending-reverse-proxy.sh
    fi

    if asksure "¿Desea tranferir el docker-compose y las .env a la máquina reverse_proxy?"; then
        scp -i ../../secure/key_prod_rsa ../../../docker/docker-compose.prod.yml ubuntu@${G10_REVERSE_PROXY_IP}:~/docker-compose.prod.yml
        scp -i ../../secure/key_prod_rsa ./run-reverse-proxy.sh ubuntu@${G10_REVERSE_PROXY_IP}:~/run-reverse-proxy.sh
        scp -i ../../secure/key_prod_rsa ../../../docker/*.env ubuntu@${G10_REVERSE_PROXY_IP}:~/
    fi

    if asksure "¿Desea entrar a la máquina para ejecutar ~/run-reverse-proxy.sh?"; then
        ssh -i ../../secure/key_prod_rsa ubuntu@${G10_REVERSE_PROXY_IP}
    fi
}

function maquina_locust() {
    if asksure "¿Desea hacer la configuración inicial de la máquina locust?"; then
        ssh-keygen -f "${HOME}/.ssh/known_hosts" -R "${G10_LOCUST_IP}"
        ssh -i ../../secure/key_prod_rsa ubuntu@${G10_LOCUST_IP} 'bash -s' < ./setup-docker.sh
    fi

    if asksure "¿Desea tranferir el docker-compose y las .env a la máquina locust?"; then
        scp -i ../../secure/key_prod_rsa ../../../docker/docker-compose.prod.yml ubuntu@${G10_LOCUST_IP}:~/docker-compose.prod.yml
        scp -i ../../secure/key_prod_rsa ./run-locust.sh ubuntu@${G10_LOCUST_IP}:~/run-locust.sh
        scp -i ../../secure/key_prod_rsa ../../../docker/*.env ubuntu@${G10_LOCUST_IP}:~/
    fi

    if asksure "¿Desea entrar a la máquina para ejecutar ~/run-locust.sh?"; then
        ssh -i ../../secure/key_prod_rsa ubuntu@${G10_LOCUST_IP}
    fi
}

function main() {
    if [ -z "${G10_REVERSE_PROXY_IP}" ] || [ -z "${G10_NFS_IP}" ] || [ -z "${G10_JOBS_IP}" ] || [ -z "${G10_LOCUST_IP}" ]; then
        echo "[$(date +'%F %T')]: No se ha encontrado una de las variable de entorno: G10_REVERSE_PROXY_IP, G10_NFS_IP, G10_JOBS_IP ó G10_LOCUST_IP" 1>&2
        exit 1
    fi

    maquina_nfs
    maquina_jobs
    maquina_reverse_proxy
    maquina_locust
}

main