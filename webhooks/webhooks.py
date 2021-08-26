""""""
from settings import GITHUB_REPO
from webhooks.factories import issueWebhookFactory
from webhooks.utils import SlackCommentTemplate

openIssueWebhook = issueWebhookFactory.createWebhook('open',
    slack_comment_template = SlackCommentTemplate(*[{"type": "section", "text": {"type": "mrkdwn", "text": "A new issue has been *created*: <"+GITHUB_REPO+"issues/" + '{{issue.number}}' + "|#" + '{{issue.number}}' + "> | Labels: " + '{% for label in issue.labels %}{{ label.name }}{{ ", " if not loop.last else "" }}{% endfor %}'}}, {"type": "section", "text": {"type": "mrkdwn", "text": '{{ issue.title }}'}}])
)

closeIssueWebhook = issueWebhookFactory.createWebhook('close',
    slack_comment_template = SlackCommentTemplate(*[{"type": "section", "text": {"type": "mrkdwn", "text": "An issue has been *closed*: <"+GITHUB_REPO+"issues/" + '{{issue.number}}' + "|#" + '{{issue.number}}' + "> | Labels: " + '{% for label in issue.labels %}{{ label.name }}{{ ", " if not loop.last else "" }}{% endfor %}'}}, {"type": "section", "text": {"type": "mrkdwn", "text": '{{ issue.title }}'}}])
)

reopenIssueWebhook = issueWebhookFactory.createWebhook('reopen',
slack_comment_template = SlackCommentTemplate(*[{"type": "section", "text": {"type": "mrkdwn", "text": "An issue has been *reopened*: <"+GITHUB_REPO+"issues/" + '{{issue.number}}' + "|#" + '{{issue.number}}' + "> | Labels: " + '{% for label in issue.labels %}{{ label.name }}{{ ", " if not loop.last else "" }}{% endfor %}'}}, {"type": "section", "text": {"type": "mrkdwn", "text": '{{ issue.title }}'}}])
)
