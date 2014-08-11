#!/bin/bash

sudo docker build --no-cache -t aweiteka/pulp-centosbase base
sudo docker build --no-cache -t aweiteka/pulp-admin admin-client
sudo docker build --no-cache -t aweiteka/pulp-apache apache
sudo docker build --no-cache -t aweiteka/pulp-crane-allinone crane-allinone
sudo docker build --no-cache -t aweiteka/pulp-mongodb mongodb
sudo docker build --no-cache -t aweiteka/pulp-data config-data
sudo docker build --no-cache -t aweiteka/pulp-qpid qpid
sudo docker build --no-cache -t aweiteka/pulp-worker worker

