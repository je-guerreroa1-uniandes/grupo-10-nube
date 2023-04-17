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
# Ejecuta la aplicación
flask run

# Desactivar el entorno (requiere: Activar el entorno)
deactivate
```

# Activar docker
Ingresar a la carpeta de docker
Bash start.sh usando una consola de Bash 