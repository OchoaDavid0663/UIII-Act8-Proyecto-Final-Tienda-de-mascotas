#!/bin/sh
source .venv/bin/activate
python backend_TiendaMascotas/manage.py runserver $PORT
