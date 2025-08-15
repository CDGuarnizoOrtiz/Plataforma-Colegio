#!/bin/sh

# Salir si algo falla
set -e

# Aplicar migraciones
python manage.py migrate

# Recoger archivos estáticos
python manage.py collectstatic --noinput

exec "$@"
