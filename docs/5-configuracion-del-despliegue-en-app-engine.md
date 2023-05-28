# Memorias de la configuración del despliegue PaaS en GCloud (Quinta entrega)

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

service: api # This service name is used in the URL for the service. {'api', 'jobs'}

instance_class: B2 # (default instance class) Number of workers=4, Memory Limit=768MB, CPU Limit=1.2GHz 

basic_scaling:
  max_instances: 5
  idle_timeout: 10m

#env_variables: # Este bloque se usa para definir variables de entorno.
#  BUCKET_NAME: "example-gcs-bucket"

handlers:
  - url: /.*
    secure: always
    redirect_http_response_code: 301
    script: auto
    http_headers:
      Access-Control-Allow-Origin: "*"

entrypoint: gunicorn -b :$PORT -w 4 wsgi:app
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
@app.route("/")
def hello():
    return "<h1 style='color:blue'>¡Hola API!</h1>"

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=config.PORT, debug=True)
```

Se siguio el siguiente turorial para desplegar un app en Gunicorn

[How To Serve Flask Applications with Gunicorn and Nginx on Ubuntu 18.04](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04#step-4-configuring-gunicorn)

## Desplegar la aplicación en App Engine

Si se preparo el entorno y se cuenta con la utilidad de gcloud instalada, se puede desplegar la aplicación con el siguiente comando:

```bash
# Testear la aplicación en local, en la carpeta ./api y ./jobs
dev_appserver.py app.yaml

# Desplegar, en la carpeta ./api y ./jobs
gcloud app deploy

# Ver el servicio desplegado
gcloud app browse
```