""""""
import json

import requests

from settings import SLACK_RELAY_ENDPOINT


class Webhook:
    slack_relay_endpoint: str = SLACK_RELAY_ENDPOINT
    slack_comment_template: list or dict
    issue: dict

    def __init__(self, **attributes):
        for key, val in attributes.items():
            setattr(self, key, val)

    @classmethod
    def make(self, **attributes):
        self.__init__(**attributes)

    def post(self):
        d = self.slack_comment_template.format(**self.issue)
        req = requests.post(self.slack_relay_endpoint, headers={'Content-Type': 'application/json'}, data=json.dumps(dict(blocks=d)))
        return req.status_code


class IssueWebhook(Webhook):
    status: str
    labels: [dict]
    number: int
    title: str
    body: str

    # slack_relay_endpoint: str = '/issue'


class SGWebhook(Webhook):
    event_type: str
    email: str
    reason: str

    # slack_relay_endpoint: str = '/sg'

    def post(self):
        d = self.slack_comment_template.format(dict(
            event_type=self.event_type,
            email=self.email,
            reason=self.reason
        ))
        req = requests.post(self.slack_relay_endpoint, headers={'Content-Type': 'application/json'}, data=json.dumps(dict(blocks=d)))
        return req.status_code

