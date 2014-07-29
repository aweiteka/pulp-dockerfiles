#!/bin/bash

# optional URL of registry to pull from with trailing slash
# my.registry.example.com/
REGISTRY=$1

# data
docker run -e PULP_HOST=$(hostname) -e MONGO_HOST=$(hostname -i) -e QPID_HOST=$(hostname -i) --name pulp-data $REGISTRYpulp/data

# mongo
docker run -d -p 27017:27017 --name pulp-mongodb $REGISTRYpulp/mongodb

# qpid
docker run -d -p 5672:5672 --name pulp-qpid $REGISTRYpulp/qpid

# apache -- creates/migrates pulp_database 
docker run -d --privileged -v /dev/log:/dev/log --volumes-from pulp-data -p 443:443 -p 8080:80 -e APACHE_HOSTNAME=$(hostname) --name pulp-apache $REGISTRYpulp/apache

# pulp workers
docker run -d -e WORKER_HOST=$(hostname -i) --privileged -v /dev/log:/dev/log --volumes-from pulp-data --name pulp-worker1 $REGISTRYpulp/worker worker 1
docker run -d -e WORKER_HOST=$(hostname -i) --privileged -v /dev/log:/dev/log --volumes-from pulp-data --name pulp-worker2 $REGISTRYpulp/worker worker 2
docker run -d --privileged -v /dev/log:/dev/log --volumes-from pulp-data --name pulp-beat $REGISTRYpulp/worker beat
docker run -d -e WORKER_HOST=$(hostname -i) --privileged -v /dev/log:/dev/log --volumes-from pulp-data --name pulp-resource_manager $REGISTRYpulp/worker resource_manager

# crane
docker run -d -p 80:80 --volumes-from pulp-data --name pulp-crane $REGISTRYpulp/crane-allinone
