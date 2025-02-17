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

LLM_API_KEY = os.environ.get("LLM_API_KEY")

SURREALDB_NS = "gptstuff"
SURREALDB_DB = "op"

SURREALDB_USER = "root"
SURREALDB_PASS = "root"

SURREALDB_HOST = "localhost"
SURREALDB_PORT = 8011

OP_PORT = 8130

PROJECT_IDS_DICT = {
    'Scrum project': 2
}

USERS_LOOKUP_TABLE = {
    'Darren MacKenzie': 5
}

PRIORITIES = {
    'Normal': 8,
    'High': 9,
    # etc...
}
