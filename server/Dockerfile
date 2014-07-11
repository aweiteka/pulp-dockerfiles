FROM pulp/base
MAINTAINER Aaron Weitekamp <aweiteka@redhat.com>

COMMENT { "description": "Pulp worker image", \ 
          "usage": "docker run -d --privileged -v /dev/log:/dev/log --volumes-from pulp-data aweiteka/pulp-server worker|beat|resource_manager [<worker_number>]" }

# may not need python-pulp-rpm-common
RUN  yum install -y --disablerepo=pulp-v2-stable --enablerepo=pulp-v2-beta \
         qpid-cpp-server qpid-cpp-server-store python-qpid-qmf python-qpid \
         python-pulp-rpm-common && \
     yum clean all

ADD run.sh /run.sh

# Usage: /run.sh worker|beat|resource_manager [<unique_worker_number>]
ENTRYPOINT ["/run.sh"]
