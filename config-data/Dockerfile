FROM rhel7:latest
MAINTAINER Aaron Weitekamp <aweiteka@redhat.com>

RUN curl -o /etc/yum.repos.d/rhel-pulp.repo \
            http://repos.fedorapeople.org/repos/pulp/pulp/rhel-pulp.repo

RUN rpm -Uvh http://dl.fedoraproject.org/pub/epel/beta/7/x86_64/epel-release-7-0.2.noarch.rpm

RUN yum update -y && \
    yum groupinstall -y --disablerepo=pulp-v2-stable --enablerepo=pulp-v2-beta \
        pulp-server && \
    yum install -y git && \
    yum clean all

# install pulp_docker plugin to manage docker image repositories
RUN git clone https://github.com/pulp/pulp_docker.git /opt/pulp_docker

RUN /opt/pulp_docker/manage_setup_pys.sh develop
RUN python /opt/pulp_docker/pulp-dev.py -I
