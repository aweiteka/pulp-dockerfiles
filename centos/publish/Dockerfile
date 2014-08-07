FROM aweiteka/pulp-admin:latest
MAINTAINER Aaron Weitekamp <aweiteka@redhat.com>

RUN git clone https://gist.github.com/2c46f99d3f5cb393ff3b.git /root/pulp_utils
#ADD pulp-publish-docker.py /root/pulp_utils/pulp-publish-docker.py

# -u read unbuffered input from STDIN
ENTRYPOINT ["python", "-u", "/root/pulp_utils/pulp-publish-docker.py"]
#ENTRYPOINT ["/usr/bin/pulp-admin", "docker", "repo", "list"]
