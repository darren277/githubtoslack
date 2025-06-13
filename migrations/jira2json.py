""""""
import requests
from requests.auth import HTTPBasicAuth
import json
from settings import JIRA_JSON_OUTPUT_PATH



url = "https://{JIRA_DOMAIN}.atlassian.net/rest/api/3/field/{fieldId}/context/{contextId}/option"

auth = HTTPBasicAuth(JIRA_EMAIL_ADDRESS, JIRA_API_TOKEN)


def build_query(url: str, data: dict = None):
    headers = {
      "Accept": "application/json"
    }

    if not data:
        response = requests.request(
           "GET",
           url,
           headers=headers,
           auth=auth
        )
    else:
        response = requests.request(
           "POST",
           url,
           headers=headers,
           auth=auth,
           json=data
        )

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None
    else:
        return response.json()


def get_fields_paginated(page: int = 0):
    url = f"https://{JIRA_DOMAIN}.atlassian.net/rest/api/3/field/search?startAt={page}&maxResults=1000"

    data = build_query(url)

    if data is None:
        return None
    else:
        return data



def export_custom_fields_and_custom_field_options():
    data = build_query(url)

    page = 0

    while data is not None:
        with open(f"{JSON_OUTPUT_PATH}custom_fields_{page}.json", "w") as f:
            json.dump(data, f, indent=2)

        page += 1
        data = get_fields_paginated(page)


def get_paginated_filters(page: int = 0):
    url = f"https://{JIRA_DOMAIN}.atlassian.net/rest/api/3/filter/search?startAt={page}&maxResults=1000"

    data = build_query(url)

    if data is None:
        return None
    else:
        return data



def export_filters():
    data = build_query(url)

    page = 0

    while data is not None:
        with open(f"{JIRA_JSON_OUTPUT_PATH}filters_{page}.json", "w") as f:
            json.dump(data, f, indent=2)

        page += 1
        data = get_paginated_filters(page)


# POST /rest/api/3/issue/bulkfetch

# Returns the details for a set of requested issues. You can request up to 100 issues.
# Each issue is identified by its ID or key, however, if the identifier doesn't match an issue, a case-insensitive search and check for moved issues is performed. If a matching issue is found its details are returned, a 302 or other redirect is not returned.
# Issues will be returned in ascending id order. If there are errors, Jira will return a list of issues which couldn't be fetched along with error messages.

def get_issues(page: int = 0):
    # issueIdsOrKeys: An array of issue IDs or issue keys to fetch. You can mix issue IDs and keys in the same query.

    issue_ids_or_keys = [f"issue-{i}" for i in range(page * 100, (page + 1) * 100)]

    url = f"https://{JIRA_DOMAIN}.atlassian.net/rest/api/3/issue/bulkfetch"

    data = build_query(url, data=issue_ids_or_keys)

    if data is None:
        return None
    else:
        return data


def export_issue_attachments(issue_id: str):
    url = f"https://{JIRA_DOMAIN}.atlassian.net/rest/api/3/issue/{issue_id}/attachments"

    data = build_query(url)

    with open(f"{JIRA_JSON_OUTPUT_PATH}issue_attachments.json", "w") as f:
        json.dump(data, f, indent=2)

    # /rest/api/3/attachment/content/{id}
    url = f"https://{JIRA_DOMAIN}.atlassian.net/rest/api/3/attachment/content/{attachment_id}"

    data = build_query(url)

    file_name = data.get("filename") # ???

    with open(f"{JIRA_JSON_OUTPUT_PATH}issue_attachments/{file_name}", "wb") as f:
        f.write(data.get("content"))


def export_issue_comments():
    data = build_query(url)

    with open(f"{JIRA_JSON_OUTPUT_PATH}issue_comments.json", "w") as f:
        json.dump(data, f, indent=2)


def export_issue_histories():
    # /rest/api/3/issue/{issueIdOrKey}/changelog

    data = build_query(url)

    with open(f"{JIRA_JSON_OUTPUT_PATH}issue_histories.json", "w") as f:
        json.dump(data, f, indent=2)


def export_issues():
    data = get_issues()

    page = 0

    while data is not None:
        # check for attachments...
        # export_issue_attachments(data.get("id"))

        # check for comments...
        # export_issue_comments()

        # check for histories...
        # export_issue_histories()

        with open(f"{JIRA_JSON_OUTPUT_PATH}issues_{page}.json", "w") as f:
            json.dump(data, f, indent=2)

        page += 1
        data = get_issues(page)





def export_issue_field_configurations_and_issue_custom_field_contexts():
    data = build_query(url)

    with open(f"{JIRA_JSON_OUTPUT_PATH}issue_field_configurations.json", "w") as f:
        json.dump(data, f, indent=2)

    with open(f"{JIRA_JSON_OUTPUT_PATH}issue_custom_field_contexts.json", "w") as f:
        json.dump(data, f, indent=2)


def export_issue_links():
    data = build_query(url)

    with open(f"{JIRA_JSON_OUTPUT_PATH}issue_links.json", "w") as f:
        json.dump(data, f, indent=2)


def export_issue_types():
    data = build_query(url)

    with open(f"{JIRA_JSON_OUTPUT_PATH}issue_types.json", "w") as f:
        json.dump(data, f, indent=2)


def export_project_roles():
    data = build_query(url)

    with open(f"{JIRA_JSON_OUTPUT_PATH}project_roles.json", "w") as f:
        json.dump(data, f, indent=2)


def export_project_versions_and_sprints():
    data = build_query(url)

    with open(f"{JIRA_JSON_OUTPUT_PATH}project_versions.json", "w") as f:
        json.dump(data, f, indent=2)

    with open(f"{JIRA_JSON_OUTPUT_PATH}project_sprints.json", "w") as f:
        json.dump(data, f, indent=2)


def export_users_and_groups():
    data = build_query(url)

    with open(f"{JIRA_JSON_OUTPUT_PATH}users.json", "w") as f:
        json.dump(data, f, indent=2)

    with open(f"{JIRA_JSON_OUTPUT_PATH}groups.json", "w") as f:
        json.dump(data, f, indent=2)
