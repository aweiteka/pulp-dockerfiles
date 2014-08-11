FROM aweiteka/pulp-admin:latest
MAINTAINER Aaron Weitekamp <aweiteka@redhat.com>

ADD pulp-publish-docker.py /root/pulp_utils/pulp-publish-docker.py

# -u read unbuffered input from STDIN
ENTRYPOINT ["python", "-u", "/root/pulp_utils/pulp-publish-docker.py"]
