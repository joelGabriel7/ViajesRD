#!/bin/bash

FASTAPI_DIR=$(dirname $(cd `dirname $0` && pwd))
cd $FASTAPI_DIR
source env/bin/activate

exec uvicorn main:app --host 0.0.0.0 --port 8000 
