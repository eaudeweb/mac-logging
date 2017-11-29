# MAC Logging

MAC Logging application is developed in order to provide a tool to detect when
people come and go from work, depending on MAC addresses of their personal
devices.

[![Travis](https://travis-ci.org/eaudeweb/mac-logging.svg?branch=master)](https://travis-ci.org/eaudeweb/mac-logging.svg)
[![Coverage Status](https://coveralls.io/repos/github/eaudeweb/mac-logging/badge.svg?branch=master)](https://coveralls.io/github/eaudeweb/mac-logging?branch=master)
[![Docker](https://dockerbuildbadges.quelltext.eu/status.svg?organization=eaudeweb&repository=mac-logging)](https://hub.docker.com/r/eaudeweb/mac-logging/builds)

## Prerequisites

1. Install [Docker](https://docs.docker.com/engine/installation/)
1. Install [Docker Compose](https://docs.docker.com/compose/install/)

## Installing the application

1. Get the source code:

        git clone https://github.com/eaudeweb/mac-logging.git
        cd mac-logging

1. Customize env files:

        cp docker/app.env.example docker/app.env
        vim docker/app.env

1. Customize docker orchestration:

        cp docker-compose.override.yml.example docker-compose.override.yml

1. Start stack, all services should be "Up" :

        docker-compose up -d
        docker-compose ps

1. See it in action: <http://localhost:5000>

## Upgrading the application

1. Get the latest version of source code:

        cd mac-logging
        git pull origin master

1. Update the application stack, all services should be "Up" :

        docker-compose up -d
        docker-compose ps

1. See it in action: <http://localhost:5000>

## Development instructions

In the _docker-compose.dev.yml_, the project directory is mapped inside the _app_ service container. Make sure you set DEBUG=True in app.env to reload the changes.

* Start stack, all services should be "Up" :

        docker-compose up -d
        docker-compose ps

* Check application logs:

        docker-compose app

* When the image is modified you should update the stack:

        docker-compose up -d --build

* Delete the containers and the volumes with:

        docker-compose down -v

## Debugging

* Please make sure that `DEBUG=True` in `app.env` file.

* Update docker-compose.override.yml file `app` section with the following so that `docker-entrypoint.sh` is not executed:

        entrypoint: ["/usr/bin/tail", "-f", "/dev/null"]

* Attach to docker container and start the server in debug mode:

        docker exec -it pontaj.app sh
        python ./manage.py runserver -h 0.0.0.0 -p 5000

* See it in action: <http://localhost:5000>
