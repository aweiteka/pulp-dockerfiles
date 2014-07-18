FROM aweiteka/pulp-admin:latest
MAINTAINER Aaron Weitekamp <aweiteka@redhat.com>

RUN git clone https://gist.github.com/2c46f99d3f5cb393ff3b.git /root/pulp_utils

ENTRYPOINT ["python", "/root/pulp_utils/pulp_docker_util.py"]
