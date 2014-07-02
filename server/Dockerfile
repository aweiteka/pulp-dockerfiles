FROM rhel7:latest
MAINTAINER Aaron Weitekamp <aweiteka@redhat.com>

ADD http://repos.fedorapeople.org/repos/pulp/pulp/rhel-pulp.repo /etc/yum.repos.d/rhel-pulp.repo

RUN yum -y install http://dl.fedoraproject.org/pub/epel/beta/7/x86_64/epel-release-7-0.2.noarch.rpm

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
