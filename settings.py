""""""

import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

SLACK_RELAY_ENDPOINT = os.environ.get("SLACK_RELAY_ENDPOINT")
GITHUB_REPO = os.environ.get("GITHUB_REPO")
PORT = int(os.environ.get("PORT"))

NO_SUCH_ENDPOINT = {"error": 'No such endpoint'}
SUCCESS = {"success": 'Slack message sent!'}
SLACK_UNREACHABLE = {"error": 'Slack unreachable.'}
MALFORMED_REQUEST = {"error": 'Malformed request.'}

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_REPO_OWNER = os.environ.get("GITHUB_REPO_OWNER")
GITHUB_REPO_NAME = os.environ.get("GITHUB_REPO_NAME")

OPENPROJECT_API_KEY = os.environ.get("OPENPROJECT_API_KEY")
OPENPROJECT_URL = os.environ.get("OPENPROJECT_URL")
