This is an attempt to run some load tests on
[addons.mozilla.org](https://addons.mozilla.org/) ([Olympia](https://github.com/mozilla/olympia)).
The short term goal is to use this to fix write performance issues.
We'll see what happens after that.

The tests run using [Locust](http://locust.io/) but everything is managed with
[docker-compose](https://docs.docker.com/compose/).


## Run load tests

Generate some users for a load testing session.
Run this from the [Olympia](https://github.com/mozilla/olympia) repo:

    ./manage.py gen_loadtest_users

Move the `loadtest-users.txt` file to the `data` directory of the load test
source code repository.

Run master and workers against your local Olympia docker container (by IP
address). You could change this to a real host, such as
`http://addons-dev.allizom.org`.

    SITE_UNDER_TEST=http://192.168.59.103 docker-compose up -d

Open the Locust dashboard at http://192.168.59.103:8089/

## Run load tests from AWS

TODO: deploy master/worker docker containers to AWS.
