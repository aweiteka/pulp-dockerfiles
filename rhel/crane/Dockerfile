FROM pulp/crane

RUN /bin/rm /var/lib/crane/metadata -r && \
    /bin/ln -s /var/www/pub/docker/app/ /var/lib/crane/metadata

ENTRYPOINT ["/usr/sbin/httpd"]
CMD ["-D", "FOREGROUND"]
