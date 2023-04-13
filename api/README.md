## workflow en Linux
```bash
# python3 en linux; py en windows.

# Crear el entorno la primera vez
python3 -m venv .venv

# Activar el entorno
source .venv/bin/activate

# Trabajar (requiere: Activar el entorno)
# Instala las dependencias en el entorno
pip3 install -r requirements.txt
# Ejecuta la aplicación
flask run

# Desactivar el entorno (requiere: Activar el entorno)
deactivate
```