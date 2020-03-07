#!/bin/sh
# Starting in app container
# Don't edit this file!


# var
SUPERVISOR_CONF="/etc/supervisor/conf.d/flask.conf"


# create log files
touch "${SUPERVISOR_LOG_FILE}"
touch "${GUNICORN_LOG_FILE}"


# run gunicorn command
RUN_COMMAND="gunicorn \
--workers ${GUNICORN_WORKERS_COUNT} \
--bind 0.0.0.0:${FLASK_PORT} \
--timeout ${GUNIKORN_TIMEOUT} \
--log-level=${GUNIKORN_LOG_LEVEL} \
--log-file=${GUNICORN_LOG_FILE} \
${RUN_APP}"


echo "=> Creating supervisor config"
rm -f ${SUPERVISOR_CONF}
cat <<EOF >> ${SUPERVISOR_CONF}
[supervisord]
nodaemon = true
logfile = ${SUPERVISOR_LOG_FILE}
logfile_maxbytes=50MB               ; maximum size of logfile before rotation
logfile_backups=10                  ; number of backed up logfiles
pidfile = /var/run/supervisord.pid
minprocs=200                        ; number of process descriptors
childlogdir = /log
username = supervisor
password = qT3CIh2HFWa7ItoF

[supervisorctl]
serverurl = unix:///var/run/supervisor.sock
username = supervisor
password = qT3CIh2HFWa7ItoF

[program:gunicorn]
command = ${RUN_COMMAND}
directory = /app
username = supervisor
stopsignal = KILL
autostart = true
autorestart = true
stdout_logfile = ${GUNICORN_LOG_FILE}
stderr_logfile = ${GUNICORN_LOG_FILE}
environment = ENV=prod,FLASK_APP=${FLASK_APP}
EOF


 # restart supervisor
echo "=> Starting supervisor"
supervisorctl -c ${SUPERVISOR_CONF} reread
service supervisor restart
supervisord -c ${SUPERVISOR_CONF}



# check supervisor status
supervisorctl status gunicorn >> "${SUPERVISOR_LOG_FILE}"

