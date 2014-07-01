#!/bin/bash

case $1 in
  worker)
    if [ -n "$2" ]; then
      exec sudo -u apache /usr/bin/celery worker --events --app=pulp.server.async.app --loglevel=INFO -c 1 -n reserved_resource_worker-$2@localhost --logfile=/var/log/pulp/reserved_resource_worker-$2.log --pidfile=/var/run/pulp/reserved_resource_worker-$2.pid
    else
      echo "The 'worker' role must be assigned a unique number as the second positional argument."
      echo "For example 'worker 1'."
      echo "Exiting"
      exit 1
    fi
    ;;
  beat)
    exec sudo -u apache /usr/bin/celery beat --scheduler=pulp.server.async.scheduler.Scheduler --workdir=/var/lib/pulp/celery/ -f /var/log/pulp/celerybeat.log -l INFO --detach --pidfile=/var/run/pulp/celerybeat.pid
    ;;
  resource_manager)
    exec sudo -u apache /usr/bin/celery worker -c 1 -n resource_manager@localhost --events --app=pulp.server.async.app --loglevel=INFO -Q resource_manager --logfile=/var/log/pulp/resource_manager.log --pidfile=/var/run/pulp/resource_manager.pid
    ;;
  apache)
    rm -rf /run/httpd/*
    exec /usr/sbin/apachectl -D FOREGROUND
    ;;
  *)
    echo "'$1' is not a supported celery command."
    echo "Use one of the following: worker, beat, resource_manager, apache."
    echo "Exiting"
    exit 1
    ;;
esac
