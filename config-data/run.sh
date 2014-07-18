#!/bin/bash

# Modify /etc/pulp/server.conf with variables from 'docker run'
cp /etc/pulp/server.conf{,.orig}
sed -i "s/# seeds: localhost:27017/seeds: $MONGO_HOST:27017/" /etc/pulp/server.conf
sed -i "s/# server_name: server_hostname/server_name: $PULP_HOST/" /etc/pulp/server.conf
