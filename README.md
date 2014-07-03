## Pulp Dockerfiles

This repository contains dockerfiles for [Pulp](http://pulpproject.org/), a repository management system. Pulp may be used as a docker registry.

## Orchestration
Options
* shell script
* [GearD](http://openshift.github.io/geard/)
* [Kubernetes](https://developers.google.com/compute/docs/containers#kubernetes)

## Component Images
Start the containers in this order.

### pulp data
Shared configuration container. Provides volumes `/etc/pulp`, `/var/www`, `/opt/pulp_docker` and `/var/lib/pulp`

    docker run -d -e MONGO=$(hostname -i) --name pulp-data pulp/data

### Qpid
Messaging queue

    docker run -d -p 5672:5672 --name pulp-qpid pulp/qpid

### Mongo DB
MongoDB is the datastore for pulp content

    docker run -d -p 27017:27017 --name pulp-mongo pulp/mongodb

### web server
The is the pulp web server for the REST API and serving static content from pulp. This container also sets up the mongo database. It requires syslog so for now we mount /dev/log and run as `--privileged`.

    docker run -d -p 443:443 --privileged -v /dev/log:/dev/log --volumes-from pulp-data pulp/apache

### Server
This is the core pulp server image that may be invoked several ways. It requires syslog so for now we mount /dev/log and run as `--privileged`.

* pulp worker

        docker run -d --privileged -v /dev/log:/dev/log --name pulp-worker1 pulp/server worker 1
        docker run -d --privileged -v /dev/log:/dev/log --name pulp-worker2 pulp/server worker 2

* celery beat

        docker run -d --privileged -v /dev/log:/dev/log --name pulp-celerybeat pulp/server beat

* resource manager

        docker run -d --privileged -v /dev/log:/dev/log --name pulp-resource-mgr pulp/server resource_manager

### Crane
Crane is an API implementation of the docker protocol. It responds to docker client requests. This is the only end-user facing element to respond to docker client requests. See https://github.com/pulp/crane

    docker run -d -v /root/crane_data:/var/lib/crane/metadata -p 5000:80 --name pulp-crane-registry pulp/crane

