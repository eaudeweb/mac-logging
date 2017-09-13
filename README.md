# MAC Logging

MAC Logging application is developed in order to provide a tool to detect when
people come and go from work, depending on MAC addresses of their personal
devices.

### Prerequisites

1. Install [Docker](https://docs.docker.com/engine/installation/)
2. Install [Docker Compose](https://docs.docker.com/compose/install/)

### Installing the application

1. Get the source code:

        $ git clone https://github.com/eaudeweb/mac-logging.git
        $ cd mac-logging

2. Customize env files:

        $ cp docker/app.env.example docker/app.env
        $ vim docker/app.env

2. Start stack, all services should be "Up" :

        $ docker-compose up -d
        $ docker-compose ps

3. See it in action: [http://0.0.0.0:5000](http://0.0.0.0:5000)


### Upgrading the application

1. Get the latest version of source code:

        $ cd mac-logging
        $ git pull origin master

2. Update the application stack, all services should be "Up" :

        $ docker-compose up -d
        $ docker-compose ps

3. See it in action: [http://0.0.0.0:5000](http://0.0.0.0:5000)
