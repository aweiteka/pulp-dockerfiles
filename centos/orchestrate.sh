#!/bin/bash

# optional URL of registry to pull from
# my.registry.example.com
REGISTRY=$1

# data
docker run -e PULP_HOST=$(hostname) -e MONGO_HOST=$(hostname -i) -e QPID_HOST=$(hostname -i) --name pulp-data $REGISTRY/pulp-data

# mongo
docker run -d -p 27017:27017 --name pulp-mongodb $REGISTRY/pulp-mongodb

# qpid
docker run -d -p 5672:5672 --name pulp-qpid $REGISTRY/pulp-qpid

# apache -- creates/migrates pulp_database 
docker run -d --privileged -v /dev/log:/dev/log --volumes-from pulp-data -p 443:443 -p 8080:80 -e APACHE_HOSTNAME=$(hostname) --name pulp-apache $REGISTRY/pulp-apache

# pulp workers
docker run -d -e WORKER_HOST=$(hostname -i) --privileged -v /dev/log:/dev/log --volumes-from pulp-data --name pulp-worker1 $REGISTRY/pulp-worker worker 1
docker run -d -e WORKER_HOST=$(hostname -i) --privileged -v /dev/log:/dev/log --volumes-from pulp-data --name pulp-worker2 $REGISTRY/pulp-worker worker 2
docker run -d --privileged -v /dev/log:/dev/log --volumes-from pulp-data --name pulp-beat $REGISTRY/pulp-worker beat
docker run -d -e WORKER_HOST=$(hostname -i) --privileged -v /dev/log:/dev/log --volumes-from pulp-data --name pulp-resource_manager $REGISTRY/pulp-worker resource_manager

# crane
docker run -d -p 80:80 --volumes-from pulp-data --name pulp-crane $REGISTRY/pulp-crane-allinone
