FROM pulp/base
MAINTAINER Aaron Weitekamp <aweiteka@redhat.com>

COMMENT { "description": "Pulp configuration data shared volume", \ 
          "usage": "docker run -d -e MONGO=$(hostname -i) --name pulp-data pulp/data" }

RUN yum install -y git findutils && \
    yum clean all

# install pulp_docker plugin to manage docker image repositories
RUN git clone https://github.com/pulp/pulp_docker.git /opt/pulp_docker

RUN /opt/pulp_docker/manage_setup_pys.sh develop

RUN python /opt/pulp_docker/pulp-dev.py -I

RUN touch /etc/pulp/vhosts80/blank.conf

VOLUME [ "/etc/pulp", "/var/www", "/opt/pulp_docker", "/var/lib/pulp" ]

ADD ./run.sh /run.sh

CMD [ "/run.sh" ]
