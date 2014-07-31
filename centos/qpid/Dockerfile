FROM centos7:latest
MAINTAINER Aaron Weitekamp <aweiteka@redhat.com>

COMMENT { "description": "Pulp qpid server image", \ 
          "usage": "docker run -d -p 5672:5672 --name pulp-qpid pulp/qpid" }

RUN yum -y install http://dl.fedoraproject.org/pub/epel/beta/7/x86_64/epel-release-7-0.2.noarch.rpm

RUN  yum update -y && \
     yum install -y qpid-cpp-server qpid-cpp-server-store python-qpid-qmf python-qpid \
     yum clean all

ADD . /.qpidd

WORKDIR /.qpidd

EXPOSE 5672

ENTRYPOINT ["qpidd", "-t", "--auth=no"]
