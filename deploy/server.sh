#!/bin/bash

# Calcula el directorio donde está el script.
FASTAPI_DIR=$(dirname $(cd `dirname $0` && pwd))

# Cambia al directorio del proyecto FastAPI.
cd $FASTAPI_DIR

# Activa el entorno virtual.
source env/bin/activate

exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload