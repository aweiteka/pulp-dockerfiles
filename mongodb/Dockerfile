FROM rhel:latest
MAINTAINER Aaron Weitekamp <aweiteka@redhat.com>

ADD http://repos.fedorapeople.org/repos/pulp/pulp/rhel-pulp.repo /etc/yum.repos.d/rhel-pulp.repo

RUN yum -y install http://dl.fedoraproject.org/pub/epel/beta/7/x86_64/epel-release-7-0.2.noarch.rpm

RUN  yum update -y && \
     yum install -y --disablerepo=pulp-v2-stable --enablerepo=pulp-v2-beta \
         mongodb-server && \
     yum clean all

RUN  mkdir -p /var/lib/mongodb && \
     touch /var/lib/mongodb/.keep && \
     chown -R mongodb:mongodb /var/lib/mongodb

VOLUME ["/var/lib/mongodb"]
USER mongodb

ADD mongodb.conf /etc/mongodb.conf

EXPOSE 27017
CMD ["/usr/bin/mongod", "--quiet", "--config", "/etc/mongodb.conf", "run"]
