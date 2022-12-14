from settings import NO_SUCH_ENDPOINT, SUCCESS, SLACK_UNREACHABLE, PORT
from webhooks.webhooks import openIssueWebhook, closeIssueWebhook, reopenIssueWebhook

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
    'closed': lambda req: closeIssueWebhook(issue=dict(issue=req.json['issue'])).post(),
    'reopen': lambda req: reopenIssueWebhook(issue=dict(issue=req.json['issue'])).post()
}


@app.route('/github', methods=['POST'])
def github_case_switch():
    result = NO_SUCH_ENDPOINT
    status_code = endpoint_case_switch.get(request.json['action'], lambda r: 400)(request)

    if status_code == 200:
        result = SUCCESS
    elif result != NO_SUCH_ENDPOINT:
        result = SLACK_UNREACHABLE
        status_code = 500

    response = make_response(jsonify(result), status_code)

    response.headers["Content-Type"] = "application/json"
    return response


if __name__ == '__main__':
    app.run(port=PORT)




