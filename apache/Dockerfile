FROM rhel7:latest
MAINTAINER Scott Collier <scollier@redhat.com>

ENV container docker

VOLUME [ "/sys/fs/cgroup" ]

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


RUN yum swap -y -- remove fakesystemd -- install systemd systemd-libs && yum clean all; \
(cd /lib/systemd/system/sysinit.target.wants/; for i in *; do [ $i == systemd-tmpfiles-setup.service ] || rm -f $i; done); \
rm -f /lib/systemd/system/multi-user.target.wants/*;\
rm -f /etc/systemd/system/*.wants/*;\
rm -f /lib/systemd/system/local-fs.target.wants/*; \
rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
rm -f /lib/systemd/system/basic.target.wants/*;\
rm -f /lib/systemd/system/anaconda.target.wants/*; \
systemctl enable httpd.service; \
yum -y erase iprutils

EXPOSE 443

# install pulp_docker plugin to manage docker image repositories
RUN git clone https://github.com/pulp/pulp_docker.git /opt/pulp_docker

RUN /opt/pulp_docker/manage_setup_pys.sh develop

ADD run.sh /run.sh

CMD [ "/run.sh" ]
