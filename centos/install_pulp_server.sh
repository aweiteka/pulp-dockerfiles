#!/usr/bin/env bash

arg=$1

IMAGES=( "aweiteka/pulp-crane-allinone" \
         "aweiteka/pulp-worker" \
         "aweiteka/pulp-qpid" \
         "aweiteka/pulp-mongodb" \
         "aweiteka/pulp-apache" \
         "aweiteka/pulp-data" \
         "aweiteka/pulp-centosbase" )

CONTAINERS=( "pulp-crane" \
             "pulp-worker1" \
             "pulp-worker2" \
             "pulp-beat" \
             "pulp-resource_manager" \
             "pulp-qpid" \
             "pulp-mongodb" \
             "pulp-apache" \
             "pulp-data" \
             "pulp-data" )

usage() {
  echo "USAGE: `basename $0` <pulp_ip_address>|uninstall"
  exit 1
}

function private_ip() {
  local priv_ip=$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' $(docker ps -l -q))
  echo $priv_ip
}

install() {

  PULP_IP=$1

  echo "Using hostname '$(hostname)'"
  echo "Pulling docker images. This may take several minutes."

  for i in "${IMAGES[@]}"; do sudo docker pull $i; done

  echo "Running docker images"

  # data
  sudo docker run \
         -e PULP_HOST=$(hostname) \
         -e MONGO_HOST=$PULP_IP \
         -e QPID_HOST=$PULP_IP \
         --name pulp-data \
         aweiteka/pulp-data

  # mongo
  # mount host  -v /var/lib/mongo:/run/pulp/mongo
  sudo docker run -d \
         -p 27017:27017 \
         --name pulp-mongodb \
         aweiteka/pulp-mongodb

  echo $(private_ip)

  # qpid
  sudo docker run -d \
         -p 5672:5672 \
         --name pulp-qpid \
         aweiteka/pulp-qpid

  echo private_ip

  # apache -- creates/migrates pulp_database
  sudo docker run -d --privileged \
         -v /dev/log:/dev/log \
         --volumes-from pulp-data \
         -p 443:443 -p 8080:80 \
         -e APACHE_HOSTNAME=$(hostname) \
         --name pulp-apache \
         aweiteka/pulp-apache

  echo private_ip

  # pulp workers
  sudo docker run -d --privileged \
         -e WORKER_HOST=$PULP_IP \
         -v /dev/log:/dev/log \
         --volumes-from pulp-data \
         --name pulp-worker1 \
         aweiteka/pulp-worker worker 1
  sudo docker run -d --privileged \
         -e WORKER_HOST=$PULP_IP \
         -v /dev/log:/dev/log \
         --volumes-from pulp-data \
         --name pulp-worker2 \
         aweiteka/pulp-worker worker 2
  sudo docker run -d --privileged \
         -v /dev/log:/dev/log \
         --volumes-from pulp-data \
         --name pulp-beat \
         aweiteka/pulp-worker beat
  sudo docker run -d --privileged \
         -e WORKER_HOST=$PULP_IP \
         -v /dev/log:/dev/log \
         --volumes-from pulp-data \
         --name pulp-resource_manager \
         aweiteka/pulp-worker resource_manager

  # crane
  sudo docker run -d \
         -p 80:80 \
         --volumes-from pulp-data \
         --name pulp-crane \
         aweiteka/pulp-crane-allinone

}

usage() {
  echo "USAGE: `basename $0` <pulp_ip_address>|uninstall"
  exit 1
}

uninstall() {

  echo "Uninstalling Pulp server"
  for c in "${CONTAINERS[@]}"; do
    PID=$(docker ps | awk "/$c/ {print \$1}")
    echo "Stopping container ${c}"
    docker stop $PID
  done
  for c in "${CONTAINERS[@]}"; do
    PID=$(docker ps -a | awk "/$c/ {print \$1}")
    echo "Removing container ${c}"
    docker rm $PID
  done

}

if [ -z "$1" ]; then
  echo "USAGE: `basename $0` <pulp_ip_address>|uninstall"
  exit 1
else
  case $1 in
    uninstall)
      uninstall
    ;;
    *) install
    ;;
  esac
fi

