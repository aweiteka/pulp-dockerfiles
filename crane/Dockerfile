FROM pulp/crane

ADD crane.conf /etc/crane.conf

ENTRYPOINT ["/usr/sbin/httpd"]
CMD ["-D", "FOREGROUND"]
