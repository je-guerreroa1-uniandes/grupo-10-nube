#!/bin/bash -x

# Antes de ejecutar la primera vez este script, ejecutar desde consola la instrucción:
# gcloud compute addresses create reverse-proxy --project=<id_proyecto> --description=Direccion\ fija\ para\ el\ reverse\ proxy\ nginx --network-tier=STANDARD --region=us-central1

terraform init
terraform destroy
terraform apply