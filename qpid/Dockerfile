FROM rhel7:latest
MAINTAINER Aaron Weitekamp <aweiteka@redhat.com>

RUN curl -o /etc/yum.repos.d/rhel-pulp.repo \
            http://repos.fedorapeople.org/repos/pulp/pulp/rhel-pulp.repo

RUN rpm -Uvh http://dl.fedoraproject.org/pub/epel/beta/7/x86_64/epel-release-7-0.2.noarch.rpm

ADD mrg.repo /etc/yum.repos.d/mrg.repo

RUN  yum update -y && \
     yum install -y --disablerepo=pulp-v2-stable --enablerepo=pulp-v2-beta \
          qpid-cpp-server qpid-cpp-server-store python-qpid-qmf python-qpid \
     yum clean all

ADD . /.qpidd

WORKDIR /.qpidd

EXPOSE 5672

ENTRYPOINT ["qpidd", "-t", "--auth=no"]
