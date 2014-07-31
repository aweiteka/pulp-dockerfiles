# Running pulp-admin as a Docker container

The pulp-admin client may be run as a container. It works best to create an alias for the `docker run` command. The `ENTRYPOINT` for the container is the pulp-admin executable, so commands may simply be passed as arguments to the alias. For example, `pulp-client <pulp admin arguments>`.

## Setup

1. The `~/.pulp` directory will be mounted when the container is run. Add the pulp server hostname and any other configuration values to `~/.pulp/admin.conf`

        [server]
        host = pulp-server.example.com

1. Pull the pulp-admin image

        docker pull aweiteka/pulp-admin

1. Create a directory for uploads for the output of `docker save`, for example, `/tmp/pulp_uploads/`. This will be mapped to the container so local files may be uploaded from the container. Use this in the next step.

1. Create an alias for `pulp-client`. For example, update your `$HOME/.bashrc` file with the line below and run `source $HOME/.bashrc`.

        alias pulp-client="sudo docker run --rm -t -v $HOME/.pulp:/.pulp -v /tmp/pulp_uploads/:/tmp/pulp_uploads/ aweiteka/pulp-admin"

## About

* based on centos image
* includes pulp beta repository
* adds pulp_docker plugin
* The `--rm` flag adds about 4 seconds to runtime but will remove the container when complete.
