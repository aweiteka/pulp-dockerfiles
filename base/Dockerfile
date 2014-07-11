FROM rhel7:latest
MAINTAINER Aaron Weitekamp <aweiteka@redhat.com>

ADD http://repos.fedorapeople.org/repos/pulp/pulp/rhel-pulp.repo \
	/etc/yum.repos.d/rhel-pulp.repo

RUN yum -y install http://dl.fedoraproject.org/pub/epel/beta/7/x86_64/epel-release-7-0.2.noarch.rpm

RUN yum update -y && \
    yum groupinstall -y --disablerepo=pulp-v2-stable --enablerepo=pulp-v2-beta \
        pulp-server && \
    yum clean all

COMMENT { "description": "base image for pulp images", \ 
          "usage": "Dockerfile FROM pulp/base" }
