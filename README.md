Generate some users for a load testing session. Run this from the Olympia repo:

    ./manage.py gen_loadtest_users

Move the `loadtest-users.txt` file to the `data` directory of the load test
source code repository.

Run master and workers against your local Olympia docker container (by IP
address). Change this to a real host, such as `http://addons-dev.allizom.org`.

    SITE_UNDER_TEST=http://192.168.59.103 docker-compose up -d

Open the dashboard at http://olympia.dev:8089/
