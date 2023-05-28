# Contribuir al desarrollo del proyecto

> El paso I es fundamental para la contribución al proyecto. En este se prepara la cuenta de Google Cloud Platform con la que se trabajara todos los laboratorios.

## I. Preparamos el entorno para ejecutar la automatización de la infraestructura

    Nota: Para ejecutar la automatización de la infraestructura se requiere tener instalado Terraform, bash y docker.

### 1. Crear un proyecto en Google Cloud Platform y crear una cuenta de servicio con permisos de editor

- 1. Ingresar a la consola de Google Cloud Platform
- 2. Crear un proyecto con el nombre: `grupo-10-nube` (El nombre es irrelevante, el proyecto se referenciará por su ID en la configuración de Terraform)
- 3. Ir a IAM & Admin > Service Accounts
- 4. Crear una cuenta de servicio con permisos de editor
- 5. Crear una llave privada en formato JSON y descargarla en la ruta: `./servers/secure/service-account-key.json`

### 2. Reservar 4 IP estáticas (Con los nombres: api, nfs, jobs, locust)

#### 2.a. A través de la consola de Google Cloud Platform

- 1. Ingresar a la consola de Google Cloud Platform
- 2. Ir a VPC Network > External IP addresses
- 3. Reservar 4 IP estáticas con los nombres: api, nfs, jobs & locust

#### 2.b. A través de la línea de comandos

- 1. Instalar el SDK de Google Cloud Platform o usar el Cloud Shell
- 2. Ejecutar el siguiente comando:

```bash
# Si instalo el SDK de Google Cloud Platform
# Autenticarse con la llave de la cuenta de servicio
gcloud auth activate-service-account --key-file=<ruta-llave-privada>

# Reservar las IP estáticas
gcloud compute addresses create api --project=<id-proyecto> --description=la\ descripción --network-tier=STANDARD --region=us-central1

gcloud compute addresses create nfs --project=<id-proyecto> --description=la\ descripción --network-tier=STANDARD --region=us-central1

gcloud compute addresses create jobs --project=<id-proyecto> --description=la\ descripción --network-tier=STANDARD --region=us-central1

gcloud compute addresses create locust --project=<id-proyecto> --description=la\ descripción --network-tier=STANDARD --region=us-central1
```

### 3. Obtener el ID del proyecto y dejarlo en la configuración de Terraform

- 1. Ingresar a la consola de Google Cloud Platform
- 2. Ir a IAM & Admin > Settings
- 3. Copiar el ID del proyecto
- 4. Dejar el ID del proyecto en el archivo `./servers/terraform/terraform.tfvars` con el siguiente formato:

```tfvars
project = "<id-proyecto>"
```

### 4. ~~Preparar un token de autenticación para leer del registro de los contenedores ghcr.io~~

> Este paso no es necesario, ya que se cambio la visibilidad del repositorio a publico.

- 1. ~~Ingresar a la configuración de la cuenta de GitHub (settings/profile/developer settings)~~
- 2. ~~Ir a Personal access tokens~~
- 3. ~~Crear un nuevo token con permisos de `read:packages`~~
- 4. ~~Copiar el token~~
- 5. ~~Dejar el token en un archivo llamado `github-token.txt` en la ruta: `./servers/secure/github-token.txt`, que tenga este formato:~~

```bash
# ¡¡¡ YA NO ES NECESARIO !!!
# Estas lineas se correran a mano al momento de ejecutar el script de bash
# y entara a una maquina para configurarla.
export CR_PAT=<token>
echo $CR_PAT | docker login ghcr.io -u <user> --password-stdin
```

### 5. Crear una llave ssh para conectarse a las instancias que creara Terraform

- 1. En la carpeta `./servers/secure` leer y ejecutar el script `./servers/secure/create-key.sh`

### 6. Declara las variables de entorno para el bash

- 1. En ~/.bashrc o ~/.zshrc agregar las siguientes variables de entorno:

```bash
# Usar las ips reservadas en el paso 2
export G10_API_IP='xxx.xxx.xxx.xxx'
export G10_NFS_IP='xxx.xxx.xxx.xxx'
export G10_JOBS_IP='xxx.xxx.xxx.xxx'
export G10_LOCUST_IP='xxx.xxx.xxx.xxx'
```

## II. Ejecutamos la automatización de la infraestructura

### 1. Ejecutar la automatización de la infraestructura con Terraform

- 1. En la carpeta `./servers/terraform/gcloud/entrega2` ejecutar el script `./main.sh`. **Ignorar** la instrucción `terraform destroy`.

### 2. Configurar las instancias creadas, con ayuda de bash

En la carpeta `./servers/scripts/entrega2` ejecutar el script `./main.sh`.

- 1. Permitir que el script se conecte a las instancias con la llave ssh creada en el paso 5. del apartado I.
- 2. Aceptar la instalación de los paquetes necesarios para la configuración de las instancias(docker-ce, docker-compose-plugin, nfs-kernel-server y nfs-common).
- 3. Aceptar el envio por scp de los archivos necesarios para la configuración de las instancias (docker-compose.prod.yml, run*.sh, *.env).
- 4. Ingresar a cada instancia y ejecutar el script `./run*.sh` para levantar los contenedores.

## III. Destruimos la infraestructura (Para no generar costos innecesarios)

- 1. En la carpeta `./servers/terraform/gcloud/entrega2` ejecutar el script `./main.sh`. En este caso cuando pase por la instrucción `terraform destroy` se debe ingresar `yes` para confirmar la destrucción de la infraestructura.
- 2. Manualmente eliminar las IP estáticas reservadas en el paso 2. del apartado I.
- 3. Manualmente eliminar el proyecto creado en el paso 1. del apartado I. (Opcional)
- 4. Manualmente eliminar la cuenta de servicio creada en el paso 4. del apartado I. (Opcional)
