""""""
import uuid

import json

import requests

from settings import SLACK_RELAY_ENDPOINT


class Webhook:
    slack_relay_endpoint: str = SLACK_RELAY_ENDPOINT
    slack_comment_template: list or dict
    issue: dict

    def __init__(self, **attributes):
        print(f"Initializing Webhook with the following attributes: {attributes}")
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
        print(f"Posting to {self.slack_relay_endpoint} with the following data: Event type ({self.event_type}), Email ({self.email}), Reason ({self.reason})")
        unique_tag = uuid.uuid4()
        print(f"Posting with unique ID: {unique_tag}")
        formatted_blocks = self.slack_comment_template.format(
            event_type=self.event_type,
            email=self.email,
            reason=self.reason,
            unique_tag=unique_tag
        )

        data = json.dumps({"blocks": formatted_blocks})

        print("DEBUG LOG:", data)

        req = requests.post(self.slack_relay_endpoint, headers={'Content-Type': 'application/json'}, data=data)
        return req.status_code

