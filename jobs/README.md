## workflow en Linux
```bash
# python3 en linux; py en windows.

# Crear el entorno la primera vez
python3 -m venv .venv

# Activar el entorno linux
source .venv/bin/activate
# Activar el entorno virtual windows
.venv/Scripts/activate


# Trabajar (requiere: Activar el entorno)
# Instala las dependencias en el entorno
pip3 install -r requirements.txt
# pip3 install gunicorn
# pip3 freeze > requirements.txt

# Ejecuta la aplicación
flask run

# Ejectuar la aplicación con gunicorn
gunicorn -b :5555 -w 4 wsgi:app

# Desactivar el entorno (requiere: Activar el entorno)
deactivate
```
