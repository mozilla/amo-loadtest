import os

import lxml.html
from lxml.html import submit_form
from locust import HttpLocust, TaskSet, task


class UserBehavior(TaskSet):

    def on_start(self):
        username, password = self.create_account()
        self.login(username, password)

    def submit_form(self, form=None, url=None, extra_values=None):
        if form is None:
            raise ValueError('form cannot be None; url={}'.format(url))

        def submit(method, form_action_url, values):
            values = dict(values)
            if 'csrfmiddlewaretoken' not in values:
                raise ValueError(
                    'Possibly the wrong form. Could not find '
                    'csrfmiddlewaretoken: {}'.format(repr(values)))
            self.client.post(url or form_action_url, values)

        submit_form(form, open_http=submit, extra_values=extra_values)

    def create_account(self):
        resp = self.client.get("/en-US/firefox/users/register")
        register_form = self.get_the_only_form_without_id(resp.content)
        if 'recaptcha_response_field' in register_form.fields:
            raise ValueError(
                'Aww snap, cannot register a new user because reCaptcha is on')
        id = os.urandom(4).encode('hex')
        username = 'kumars-loadtest-{}'.format(id)
        password = os.urandom(32).encode('hex')

        self.submit_form(
            form=register_form, extra_values={
                "username": username,
                "password": password,
                "password2": password,
                "email": "kumars-loadtest-{}@nowhere.org".format(id),
                "display_name": "Kumar's Loadtest {}".format(id)})

        return username, password

    def get_the_only_form_without_id(self, response_content):
        """
        Gets the only form on the page that doesn't have an ID.
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
    def devhub_test(self):
        with self.client.get(
                "/en-US/developers/addon/",
                allow_redirects=False, catch_response=True) as response:
            if response.status_code != 200:
                response.failure('Unexpected status: {}'
                                 .format(response.status_code))


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait=5000
    max_wait=9000
