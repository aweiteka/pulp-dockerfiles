#!/bin/bash

declare -A IMAGES

# ["build_directory"]=image/name
IMAGES+=( ["base"]=aweiteka/pulp-centosbase \
         ["config-data"]=aweiteka/pulp-data \
         ["crane-allinone"]=aweiteka/pulp-crane-allinone \
         ["worker"]=aweiteka/pulp-worker \
         ["qpid"]=aweiteka/pulp-qpid \
         ["mondodb"]=aweiteka/pulp-mongodb \
         ["apache"]=aweiteka/pulp-apache \
         ["admin-client"]=aweiteka/pulp-admin \
         ["publish-client"]=aweiteka/pulp-publish-docker )

for dir in ${!IMAGES[@]}; do
  echo "Building ${IMAGES[${dir}]} ..."
  sudo docker build --no-cache -t ${IMAGES[${dir}]}:$(date +%F) ${dir}
done
