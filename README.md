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

Launch a new Ubuntu EC2 instance and provision it like this:

    sudo apt-get update
    sudo apt-get install -y git-core
    git clone https://github.com/mozilla/amo-loadtest.git
    cd amo-loadtest
    sudo ./scripts/provision-ec2.sh

Finally, push your `loadtest-users.txt` file up to the
`amo-loadtest/data` directory.

### Start a master

Boot up a master EC2 instance, provision it as described above,
and run this to start a master container:

    cd src/amo-loadtest
    sudo SITE_UNDER_TEST=https://addons.allizom.org \
        docker-compose -f docker-compose-master.yml up -d

Be sure this EC2 instance can accept inbound TCP connections from 8089 (the
dashboard) and 5557-5558 (worker connections).

Find the IP of your master and check the dashboard. It will be
at something like http://ec2-N-N-N-N.us-west-2.compute.amazonaws.com:8089/

### Start a worker

You can start as many workers as you want. For each EC2 instance you start, you
need to begin by provisioning it as described above.
Run this command to start a worker container:

    cd src/amo-loadtest
    sudo SITE_UNDER_TEST=https://addons.allizom.org \
        MASTER_HOST=ec2-N-N-N-N.us-west-2.compute.amazonaws.com \
        docker-compose -f docker-compose-worker.yml up -d

You'll notice that the `$MASTER_HOST` var is set to the publicly accessible DNS
host that your master is running on.

## Results!

- AMO tests on stage
  - [2016-01-11](https://docs.google.com/spreadsheets/d/17y8MqnLgf5LG6wlQ6SVEljcQl3FuNaDt3Wr8zo4ERP8/edit#gid=331334299)
  - [2016-01-12](https://docs.google.com/spreadsheets/d/1l-8AXxhjEV1QT9Kl1raB6B76u3MU5ira927OY7mcy5Y/edit#gid=2013401068)
  - [2016-01-13](https://docs.google.com/spreadsheets/d/1sSjGnjJMNxgOTBROyDrRd93MFgMxx0hNk9dMZXsp_is/edit#gid=0)
