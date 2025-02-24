""""""
from settings import GITHUB_REPO
from webhooks.factories import issueWebhookFactory, sgWebhookFactory
from webhooks.utils import SlackCommentTemplate

openIssueWebhook = issueWebhookFactory.createWebhook('open',
    slack_comment_template = SlackCommentTemplate(*[
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"A new issue has been *created*: <{GITHUB_REPO}issues/" + '{{issue.number}}' + "|#" + '{{issue.number}}' + "> | Labels: " + '{% for label in issue.labels %}{{ label.name }}{{ ", " if not loop.last else "" }}{% endfor %}'
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": '{{ issue.title }}'
            }
        }
    ])
)

closeIssueWebhook = issueWebhookFactory.createWebhook('close',
    slack_comment_template = SlackCommentTemplate(*[
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"An issue has been *closed*: <{GITHUB_REPO}issues/" + '{{issue.number}}' + "|#" + '{{issue.number}}' + "> | Labels: " + '{% for label in issue.labels %}{{ label.name }}{{ ", " if not loop.last else "" }}{% endfor %}'
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn", "text": '{{ issue.title }}'
            }
        }
    ])
)

reopenIssueWebhook = issueWebhookFactory.createWebhook('reopen',
    slack_comment_template = SlackCommentTemplate(*[
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"An issue has been *reopened*: <{GITHUB_REPO}issues/" + '{{issue.number}}' + "|#" + '{{issue.number}}' + "> | Labels: " + '{% for label in issue.labels %}{{ label.name }}{{ ", " if not loop.last else "" }}{% endfor %}'
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": '{{ issue.title }}'
            }
        }
    ])
)


universal_sg_slack_template = SlackCommentTemplate(*[
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "[{{ event_type }}: {{unique_tag}}]({{ email }}) has occured with reason: {{ reason }}."
        }
    }
])

def create_sendgrid_issue_webhook(event_type, email, reason, unique_id):
    webhook_cls = sgWebhookFactory.createWebhook(
        event_type,
        slack_comment_template=universal_sg_slack_template,
        email=email,
        reason=reason,
        unique_tag=unique_id
    )
    return webhook_cls()
