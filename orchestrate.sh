#!/bin/bash

# data
docker run -e PULP_HOST=$(hostname) -e MONGO_HOST=$(hostname -i) -e QPID_HOST=$(hostname -i) --name pulp-data pulp/data

# mongo
docker run -d -p 27017:27017 --name pulp-mongodb pulp/mongodb

# qpid
docker run -d -p 5672:5672 --name pulp-qpid pulp/qpid

# apache -- creates/migrates pulp_database 
docker run -d -t --privileged -v /dev/log:/dev/log --volumes-from pulp-data -p 443:443 -e APACHE_HOSTNAME=$(hostname) --name pulp-apache pulp/apache

# pulp workers
docker run -d -e WORKER_HOST=$(hostname -i) --privileged -v /dev/log:/dev/log --volumes-from pulp-data --name pulp-worker1 aweiteka/pulp-server worker 1
docker run -d -e WORKER_HOST=$(hostname -i) --privileged -v /dev/log:/dev/log --volumes-from pulp-data --name pulp-worker2 aweiteka/pulp-server worker 2
docker run -d --privileged -v /dev/log:/dev/log --volumes-from pulp-data --name pulp-beat aweiteka/pulp-server beat
docker run -d -e WORKER_HOST=$(hostname -i) --privileged -v /dev/log:/dev/log --volumes-from pulp-data --name pulp-resource_manager aweiteka/pulp-server resource_manager

# crane
docker run -d -p 80:5000 --volumes-from pulp-data pulp/crane-all-in-one
