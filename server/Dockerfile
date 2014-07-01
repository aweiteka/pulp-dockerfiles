FROM centos:latest
MAINTAINER Aaron Weitekamp <aweiteka@redhat.com>

RUN curl -o /etc/yum.repos.d/rhel-pulp.repo \
            http://repos.fedorapeople.org/repos/pulp/pulp/rhel-pulp.repo

RUN rpm -Uvh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm

ADD ../mrg.repo /etc/yum.repos.d/mrg.repo

# may not need python-pulp-rpm-common
RUN  yum update -y && \
     yum groupinstall -y --disablerepo=pulp-v2-stable --enablerepo=pulp-v2-beta \
         pulp-server && \
     yum install -y --disablerepo=pulp-v2-stable --enablerepo=pulp-v2-beta \
          qpid-cpp-server qpid-cpp-server-store python-qpid-qmf python-qpid \
          python-pulp-rpm-common git && \
     yum clean all

# install pulp_docker plugin to manage docker image repositories
RUN git clone https://github.com/pulp/pulp_docker.git /opt/pulp_docker

RUN /opt/pulp_docker/manage_setup_pys.sh develop

ADD run.sh /run.sh
RUN chmod -v +x /run.sh

# Usage: /run.sh worker|beat|resource_manager|apache <unique_worker_number>
ENTRYPOINT ["/run.sh"]
