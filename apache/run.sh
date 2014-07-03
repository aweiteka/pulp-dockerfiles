#!/bin/bash

runuser apache -s /bin/bash /bin/bash -c "/usr/bin/pulp-manage-db"

exec /usr/sbin/init
