from settings import MALFORMED_REQUEST, NO_SUCH_ENDPOINT, SUCCESS, SLACK_UNREACHABLE, PORT
from settings import GITHUB_REPO_OWNER, GITHUB_REPO_NAME, GITHUB_TOKEN
from webhooks.webhooks import openIssueWebhook, closeIssueWebhook, reopenIssueWebhook

import requests

from flask import Flask, request, make_response, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return "<html>This is meant to just be a purely backend webhook API. For a list of endpoints, <a href='/endpoints'>click here</a>.</html>"

@app.route('/endpoints')
def endpoints():
    return "TODO: Programmatically list endpoints."



endpoint_case_switch = {
    'open': lambda req: openIssueWebhook(issue=dict(issue=req.json['issue'])).post(),
    'opened': lambda req: openIssueWebhook(issue=dict(issue=req.json['issue'])).post(),
    'closed': lambda req: closeIssueWebhook(issue=dict(issue=req.json['issue'])).post(),
    'reopen': lambda req: reopenIssueWebhook(issue=dict(issue=req.json['issue'])).post()
}


@app.route('/github', methods=['POST'])
def github_case_switch():
    result = NO_SUCH_ENDPOINT
    action = request.json.get('action')
    if action:
        status_code = endpoint_case_switch.get(action, lambda r: 400)(request)
    else:
        zen = request.json.get('zen')
        if zen == 'Practicality beats purity.':
            result = 'Testing Webhook'
            status_code = 200
        else:
            print('action missing from payload')
            print(request.json)
            result = MALFORMED_REQUEST
            status_code = 400

    if status_code == 200:
        result = SUCCESS
    elif result != NO_SUCH_ENDPOINT:
        result = SLACK_UNREACHABLE
        status_code = 500
    elif status_code == 400:
        print("Something else wrong with request:")
        print(action)

    response = make_response(jsonify(result), status_code)

    response.headers["Content-Type"] = "application/json"
    return response

def create_issue_on_github(title, body):
    url = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/issues"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    data = {
        "title": title,
        "body": body,
        # Optionally labels, assignees, etc.
        # "labels": ["slack-created", ...],
        # "assignees": ["your-github-username"],
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code not in [200, 201]:
        print("Error creating GitHub issue:", response.text)
        return False
    else:
        return True

@app.route("/slack/githubissue", methods=["POST"])
def slack_github_issue():
    user_text = request.form.get("text", "")
    user_id = request.form.get("user_id", "")

    issue_title = user_text if user_text else "New Issue from Slack"
    issue_body = f"Created by Slack user <@{user_id}>"
    result = create_issue_on_github(issue_title, issue_body)
    if not result:
        return jsonify({"response_type": "ephemeral", "text": "Error creating issue on GitHub"}), 500

    return jsonify({"response_type": "ephemeral", "text": f"Your issue was created on GitHub: {issue_title}"}), 200


if __name__ == '__main__':
    app.run(port=PORT)




