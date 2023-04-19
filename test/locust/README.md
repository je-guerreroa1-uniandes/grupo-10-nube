# python3 en linux; py en windows

# Crear el entorno la primera vez
# Puede que toque Correr esto la primera vez 
# sudo apt install python3.11-venv
python3 -m venv .venv

# Activar el entorno
source .venv/bin/activate
# Activar el entorno virtual windows
.venv/Scripts/activate

# Trabajar (requiere: Activar el entorno)
# pip3 install locust
# pip3 freeze > requirements.txt
# Instala las dependencias en el entorno
pip3 install -r requirements.txt
# Ejecuta la prueba de carga
locust
# locust --users 1000 --spawn-rate 25 -H https://api.arquitecturaccp.com --locustfile locustfile.py
# locust --users 350 --spawn-rate 25 -H https://api.arquitecturaccp.com --locustfile locustfile.py
# locust --users 100 --spawn-rate 5 -H https://api.arquitecturaccp.com --locustfile locustfile.py

# Desactivar el entorno (requiere: Activar el entorno)
deactivate