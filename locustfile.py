import logging
import os
import random

import lxml.html
from lxml.html import submit_form
from locust import HttpLocust, TaskSet, task

data_dir = os.path.join(os.path.dirname(__file__), 'data')
log = logging.getLogger(__name__)


class UserBehavior(TaskSet):

    def on_start(self):
        user_file = os.path.join(data_dir, 'loadtest-users.txt')
        if not os.path.exists(user_file):
            raise ValueError(
                'User file does not exist: {}; did you generate one?'
                .format(user_file))
        users = []
        with open(user_file, 'r') as f:
            for line in f:
                email, password = line.strip().split(':')
                users.append({'email': email, 'password': password})

        credentials = random.choice(users)

        log.info('Running test with {}'.format(credentials))
        self.login(credentials['email'], credentials['password'])

    def submit_form(self, form=None, url=None, extra_values=None):
        if form is None:
            raise ValueError('form cannot be None; url={}'.format(url))

        def submit(method, form_action_url, values):
            values = dict(values)
            if 'csrfmiddlewaretoken' not in values:
                raise ValueError(
                    'Possibly the wrong form. Could not find '
                    'csrfmiddlewaretoken: {}'.format(repr(values)))
            with self.client.post(
                    url or form_action_url, values,
                    allow_redirects=False, catch_response=True) as response:
                if response.status_code not in (301, 302):
                    # This probably means the form failed and is displaying
                    # errors.
                    # TODO: scrape out the errors.
                    response.failure(
                        'Form submission did not redirect; status={}'
                        .format(response.status_code))

        submit_form(form, open_http=submit, extra_values=extra_values)

    def get_the_only_form_without_id(self, response_content):
        """
        Gets the only form on the page that doesn't have an ID.

        A lot of pages (login, registration) have a single form with an ID.
        This is the one we want. The other forms on the page have IDs so we
        can ignore them. I'm sure this will break one day.
        """
        html = lxml.html.fromstring(response_content)
        target_form = None
        for form in html.forms:
            if not form.attrib.get('id'):
                target_form = form
        if target_form is None:
            raise valueerror(
                'Could not find only one form without an ID; found: {}'
                .format(html.forms))
        return target_form

    def login(self, email, password):
        login_url = "/en-US/firefox/users/login"
        resp = self.client.get(login_url)
        login_form = self.get_the_only_form_without_id(resp.content)

        self.submit_form(
            form=login_form, url=login_url, extra_values={
                "username": email,
                "password": password})

    @task(1)
    def index(self):
        with self.client.get(
                "/en-US/developers/addons",
                allow_redirects=False, catch_response=True) as response:
            if response.status_code != 200:
                more_info = ''
                if response.status_code in (301, 302):
                    more_info = ('Location: {}'
                                 .format(response.headers['Location']))
                response.failure('Unexpected status: {}; {}'
                                 .format(response.status_code, more_info))


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait=5000
    max_wait=9000
