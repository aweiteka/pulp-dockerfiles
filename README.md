## Pulp Dockerfiles

This repository contains dockerfiles for [Pulp](http://pulpproject.org/), a repository management system. Pulp may be used as a docker registry.

## Orchestration
[GearD](http://openshift.github.io/geard/)

## Component Images

### Server
This is the core pulp server image that may be invoked several ways.

* pulp worker

        docker run -d --name pulp-worker1  aweiteka/pulp-server worker 1
        docker run -d --name pulp-worker2 aweiteka/pulp-server worker 2

* celery beat

        docker run -d --name pulp-celerybeat aweiteka/pulp-server beat

* resource manager

        docker run -d --name pulp-resource-mgr aweiteka/pulp-server resource_manager

* web server

        docker run -d --name pulp-apache aweiteka/pulp-server apache

### pulp data
Shared configuration container. Provides volumes `/etc/pulp/` and `/var/www`

        docker run -d --name pulp-data aweiteka/pulp-data

### Crane
Crane is an API implementation of the docker protocol. It responds to docker client requests. See https://github.com/pulp/crane

        docker run -d --name crane_server -p 5000:80 -v /root/crane_data:/var/lib/crane/metadata pulp/crane

### Mongo DB
MongoDB is the datastore for the solutoin.

	docker run -d -t -p 27017:27017 scollier/mongodb

### Qpid
Messaging queue
