#!/bin/bash

# Modify /etc/pulp/server.conf with variables from 'docker run'
cp /etc/pulp/server.conf{,.orig}
sed -i "s/# seeds: localhost:27017/seeds: $MONGO:27017/" /etc/pulp/server.conf
