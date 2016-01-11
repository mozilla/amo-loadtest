This is an attempt to run some load tests on
[addons.mozilla.org](https://addons.mozilla.org/) ([Olympia](https://github.com/mozilla/olympia)).
The short term goal is to use this to fix write performance issues.
We'll see what happens after that.

The tests run using [Locust](http://locust.io/) but everything is managed with
[docker-compose](https://docs.docker.com/compose/).


## Run load tests

Generate some users for a load testing session.
Run this from the [Olympia](https://github.com/mozilla/olympia) repo
on the site that you want to load test. For example, to test things out locally,
generate this from your local Olympia repo::

    ./manage.py gen_loadtest_users

Move the `loadtest-users.txt` file to the `data` directory of the load test
source code repository.

## Run a local test

Run master and workers against your local Olympia docker container (by IP
address, which may be different for you).

    SITE_UNDER_TEST=http://192.168.59.103 docker-compose up -d

Open the Locust dashboard at http://192.168.59.103:8089/

## Run load tests from AWS

Generate a `loadtest-users.txt` file on the server for the website under test
similar to how it's documented above.

### Start a master

First, boot up a master EC2 instance and do the following things:

- Clone the source from https://github.com/mozilla/amo-loadtest
- Push your `loadtest-users.txt` file up to the `data` directory
- Install docker and docker-compose
- Run this to start a master container::

    cd src/amo-loadtest
    SITE_UNDER_TEST=https://addons.allizom.org \
        docker-compose -f docker-compose-master.yml up -d

Find the IP of your master and check the dashboard. It will be
at something like http://ec2-N-N-N-N.us-west-2.compute.amazonaws.com:8089/

### Start a worker

You can start as many workers as you want. For each EC2 instance you start, you
need to begin by cloning the code, pushing your `loadtest-users.txt` file,
and installing docker just like you would for a master instance.
Run this command to start a worker container::

    cd src/amo-loadtest
    SITE_UNDER_TEST=https://addons.allizom.org \
        MASTER_HOST=ec2-N-N-N-N.us-west-2.compute.amazonaws.com \
        docker-compose -f docker-compose-worker.yml up -d

You'll notice that the `$MASTER_HOST` var is set to the publicly accessible DNS
host that your master is running on.
