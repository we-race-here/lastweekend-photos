#!/bin/bash

NAME="lastweekend_photos"                                  # Name of the application
ROOTDIR=/opt/webapps
PROJECTDIR=${ROOTDIR}/${NAME}
DJANGODIR=${PROJECTDIR}/${NAME}
ENVDIR=${PROJECTDIR}/env
SOCKFILE=${PROJECTDIR}/run/${NAME}.sock
USER=appuser                                        # the user to run as
GROUP=appuser                                     # the group to run as
NUM_WORKERS=3                                    # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=lastweekend_photos.settings.main             # which settings file should Django use
DJANGO_WSGI_MODULE=lastweekend_photos.wsgi                     # WSGI module name

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
source ${ENVDIR}/bin/activate
export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}
export PYTHONPATH=${DJANGODIR}/lastweekend_photos:${PYTHONPATH}

# Create the run directory if it doesn't exist
RUNDIR=$(dirname ${SOCKFILE})
test -d ${RUNDIR} || mkdir -p ${RUNDIR}

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec ${ENVDIR}/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name ${NAME} \
  --workers ${NUM_WORKERS} \
  --user=${USER} --group=${GROUP} \
  --bind=unix:${SOCKFILE} \
  --log-level=debug \
  --timeout=100 \
  --log-file=${PROJECTDIR}/logs/gunicorn.log
