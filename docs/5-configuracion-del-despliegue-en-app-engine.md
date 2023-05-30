# Memorias de la configuración del despliegue PaaS en GCloud (Quinta entrega)

## Para ejecutar este laboratorio:

Para ejecutar este laboratorio se debe haber preparado el entorno según las instrucciones del numeral **I** del archivo [CONTRIBUTING.md](../CONTRIBUTING.md), especificamente los puntos **1 y 2.b**.

> Otra consideracion fue que se necesito en la configuración **2.b**: Un nivel de permisos de propietario para poder desplegar la aplicación en app engine. Para editar los permisos de un usuario, se debe ir a la consola de IAM y administración > IAM y agregar el rol de propietario al usuario. [IAM Admin](https://console.cloud.google.com/iam-admin)

Adicionalmente se deben dejar establecidas en la máquina que esta realizando el despliegue las variables de entorno asociadas a la conexion a la base de datos. se deben crear los archivos api/env_variables.yaml y jobs/env_variables.yaml con el siguiente contenido:

```yaml
env_variables:
  G10_DB_PREFIX: "postgresql"
  G10_DB_USERNAME: "converter_db"
  G10_DB_PASSWORD: "... dar el valor ..."
  G10_DB_HOST: "... dar el valor ..."
  G10_DB_PORT: "5432"
  G10_DB_DBNAME: "conversion"
```

## Selecionar el entorno de app engine a utilizar

Nuestra aplicacion fue desarrollada para ejecutarse usando python 3.9.6. Esto nos permite usar app engine standar. Ese entorno nos resulta mas atractivo porque nos ofrece las siguientes ventajas:

- Tiempo de inicio de las instancias en segundos.
- Escalado automático de instancias.
- Puede escalar a cero instancias (Perfecto para gestionar costos).
- Tiempo de despliegue de la aplicación en segundos.
- Parches de seguridad automáticos.
- Acceso a cloud storage y memorystore.
- Ideal para cargas de trabajo espontaneas que requieran escalar inmediatamente.

## Diseñar el entorno de ejecución con el archivo app.yaml

El archivo app.yaml se especifican las dependencias de nuestra aplicación, el runtime, el lenguaje, el servicio, el handler, etc. En nuestro caso, el archivo app.yaml quedo de la siguiente manera:

```yaml
# Python 3.7, 3.8, and 3.9 run on Ubuntu 18.04
# Python 3.10 and 3.11 run on Ubuntu 22.04
runtime: python39

# The first service (module) you upload to a new application must be the 'default' service (module).
# Please upload a version of the 'default' service (module) before uploading a version for the 'api' service
service: default # This service name is used in the URL for the service. {'default', 'jobs'}. default es el api

instance_class: B2 # (default instance class) Number of workers=4, Memory Limit=768MB, CPU Limit=1.2GHz

basic_scaling:
  max_instances: 5
  idle_timeout: 10m

#env_variables: # Este bloque se usa para definir variables de entorno. Pero no lo vamos a dejar en el mismo archivo app.yaml
#  BUCKET_NAME: "example-gcs-bucket"

# Con este include podemos declarar variables de entorno en un archivo aparte
# y dejarlo por fuera del repositorio con el .gitignore
includes:
  - env_variables.yaml

handlers:
  - url: /.*
    secure: always
    redirect_http_response_code: 301
    script: auto

# NOTA: Los primeros 2 entrypoints son para ejecutar la aplicación api
# Algunos estan comentados porque solo se espera que se ejecute uno de ellos, los otros se escriben por ser utiles de diferentes formas.

# ========================= ENTRYPOINTS PARA API =========================

entrypoint: gunicorn -b :$PORT -w 4 wsgi:app

# entrypoint: flask run --port=$PORT # Usar este entrypoint para ver mas informacion de los errores

# ========================= ENTRYPOINTS PARA JOBS =========================

# entrypoint: python -m worker # El entrypoint del Jobs

```

## Ajustar las aplicaciones para que corran un webserver sobre el puerto $PORT (default 5000)

En nuestro caso, el archivo wsgi.py quedo de la siguiente manera:

```python
from app import app

if __name__ == "__main__":
    app.run()
```

Al final del archivo app.py se agrego el siguiente bloque de codigo:

```python
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=config.PORT, debug=True)
```

Se siguio el siguiente turorial para desplegar un app en Gunicorn

[How To Serve Flask Applications with Gunicorn and Nginx on Ubuntu 18.04](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04#step-4-configuring-gunicorn)

## Ajustar loc componentes api y jobs para que realizen operaciones de escritura unicamente en el directorio /tmp

[Reading and writing temporary files](https://cloud.google.com/appengine/docs/standard/using-temp-files?tab=python)

## Desplegar la aplicación en App Engine

Si se preparo el entorno y se cuenta con la utilidad de gcloud instalada, se puede desplegar la aplicación con el siguiente comando:

```bash
# Testear la aplicación en local, en la carpeta ./api y ./jobs
dev_appserver.py app.yaml # Este comando no funciona muy bien, se recomienda usar el siguiente

# Desplegar, en la carpeta ./api y ./jobs
gcloud app deploy

# Desplegar mostrando mas informacion
gcloud app deploy --verbosity=debug

# Ver el servicio desplegado
gcloud app browse

# Mas especificamente ...
gcloud app browse -s default # este es el api
gcloud app browse -s jobs

# Ver los logs del servicio desplegado
gcloud app logs tail -s default # este es el api
gcloud app logs tail -s jobs
```

Todo junto:

```bash
echo Y | gcloud app deploy --verbosity=debug && gcloud app browse -s default && gcloud app logs tail -s default
```