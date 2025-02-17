""""""

attachments = {
    "_type":"Collection",
    "total":0,
    "count":0,
    "_embedded":{"elements":[]},
    "_links":{"self":{"href":"/api/v3/work_packages/43/attachments"}}
}

relations = {
    "_type":"Collection",
    "total":0,
    "count":0,
    "_embedded":{"elements":[]},
    "_links":{"self":{"href":"/api/v3/work_packages/43/relations"}}
}

_type = {
    "_type":"Type",
    "id":1,
    "name":"Task",
    "color":"#1A67A3",
    "position":1,
    "isDefault":true,
    "isMilestone":false,
    "createdAt":"2025-01-27T17:26:54.426Z",
    "updatedAt":"2025-01-27T17:26:54.426Z",
    "_links":{"self":{"href":"/api/v3/types/1", "title":"Task"}}
}

priority = {
    "_type":"Priority",
    "id":8,
    "name":"Normal",
    "position":2,
    "color":"#74C0FC",
    "isDefault":true,
    "isActive":true,
    "_links":{"self":{"href":"/api/v3/priorities/8", "title":"Normal"}}
}

project = {
    "_type":"Project",
    "id":2,
    "identifier":"your-scrum-project",
    "name":"Scrum project",
    "active":true,
    "public":true,
    "description":{
        "format":"markdown",
        "raw":"This is a short summary of the goals of this demo Scrum project.",
        "html":"<p class=\"op-uc-p\">This is a short summary of the goals of this demo Scrum project.</p>"
    },
    "createdAt":"2025-01-27T17:26:57.746Z",
    "updatedAt":"2025-01-28T10:14:42.974Z",
    "statusExplanation":{
        "format":"markdown",
        "raw":"All tasks are on schedule. The people involved know their tasks. The system is completely set up.",
        "html":"<p class=\"op-uc-p\">All tasks are on schedule. The people involved know their tasks. The system is completely set up.</p>"
    },
    "_links":{
        "self":{"href":"/api/v3/projects/2", "title":"Scrum project"},
        "createWorkPackage":{"href":"/api/v3/projects/2/work_packages/form", "method":"post"},
        "createWorkPackageImmediately":{"href":"/api/v3/projects/2/work_packages", "method":"post"},
        "workPackages":{"href":"/api/v3/projects/2/work_packages"},
        "storages":[],
        "categories":{"href":"/api/v3/projects/2/categories"},
        "versions":{"href":"/api/v3/projects/2/versions"},
        "memberships":{"href":"/api/v3/memberships?filters=%5B%7B%22project%22%3A%7B%22operator%22%3A%22%3D%22%2C%22values%22%3A%5B%222%22%5D%7D%7D%5D"},
        "types":{"href":"/api/v3/projects/2/types"},
        "update":{"href":"/api/v3/projects/2/form", "method":"post"},
        "updateImmediately":{"href":"/api/v3/projects/2", "method":"patch"},
        "delete":{"href":"/api/v3/projects/2", "method":"delete"},
        "schema":{"href":"/api/v3/projects/schema"},
        "ancestors":[],
        "projectStorages":{"href":"/api/v3/project_storages?filters=%5B%7B%22projectId%22%3A%7B%22operator%22%3A%22%3D%22%2C%22values%22%3A%5B%222%22%5D%7D%7D%5D"},
        "parent":{"href":"None"},
        "status":{"href":"/api/v3/project_statuses/at_risk", "title":"At risk"}
    }
}

status = {
    "_type":"Status",
    "id":1,
    "name":"New",
    "isClosed":false,
    "color":"#1098AD",
    "isDefault":true,
    "isReadonly":false,
    "excludedFromTotals":false,
    "defaultDoneRatio":0,
    "position":1,
    "_links":{"self":{"href":"/api/v3/statuses/1", "title":"New"}}
}

author = {
    "_type":"User",
    "id":4,
    "name":"Darren MacKenzie",
    "createdAt":"2025-01-27T17:26:55.872Z",
    "updatedAt":"2025-01-28T10:20:37.937Z",
    "login":"me@darrenmackenzie.com",
    "admin":true,
    "firstName":"Darren",
    "lastName":"MacKenzie",
    "email":"me@darrenmackenzie.com",
    "avatar":"https://secure.gravatar.com/avatar/aa72f19e3ad65a46ac6ebbde1072884d?default=404&secure=true",
    "status":"active",
    "identityUrl":"None",
    "language":"en",
    "_links":{
        "self":{"href":"/api/v3/users/4", "title":"Darren MacKenzie"},
        "memberships":{"href":"/api/v3/memberships?filters=%5B%7B%22principal%22%3A%7B%22operator%22%3A%22%3D%22%2C%22values%22%3A%5B%224%22%5D%7D%7D%5D", "title":"Memberships"},
        "showUser":{"href":"/users/4", "type":"text/html"},
        "updateImmediately":{"href":"/api/v3/users/4", "title":"Update me@darrenmackenzie.com", "method":"patch"},
        "lock":{"href":"/api/v3/users/4/lock", "title":"Set lock on me@darrenmackenzie.com", "method":"post"},
        "delete":{"href":"/api/v3/users/4", "title":"Delete me@darrenmackenzie.com", "method":"delete"}
    }
}

_embedded = {
    "attachments": attachments,
    "relations": relations,
    "type": _type,
    "priority": priority,
    "project": project,
    "status": status,
    "author": author,
    "customActions":[]
}

_links = {
    "attachments":{"href":"/api/v3/work_packages/43/attachments"},
    "prepareAttachment":{"href":"/api/v3/work_packages/43/attachments/prepare", "method":"post"},
    "addAttachment":{"href":"/api/v3/work_packages/43/attachments", "method":"post"},
    "fileLinks":{"href":"/api/v3/work_packages/43/file_links"},
    "addFileLink":{"href":"/api/v3/work_packages/43/file_links", "method":"post"},
    "self":{"href":"/api/v3/work_packages/43", "title":"Test task"},
    "update":{"href":"/api/v3/work_packages/43/form", "method":"post"},
    "schema":{"href":"/api/v3/work_packages/schemas/2-1"},
    "updateImmediately":{"href":"/api/v3/work_packages/43", "method":"patch"},
    "delete":{"href":"/api/v3/work_packages/43", "method":"delete"},
    "logTime":{"href":"/api/v3/time_entries", "title":"Log time on work package 'Test task'"},
    "move":{"href":"/work_packages/43/move/new", "type":"text/html", "title":"Move work package 'Test task'"},
    "copy":{"href":"/work_packages/43/copy", "type":"text/html", "title":"Copy work package 'Test task'"},
    "pdf":{"href":"/work_packages/43.pdf", "type":"application/pdf", "title":"Export as PDF"},
    "atom":{"href":"/work_packages/43.atom", "type":"application/rss+xml", "title":"Atom feed"},
    "availableRelationCandidates":{"href":"/api/v3/work_packages/43/available_relation_candidates", "title":"Potential work packages to relate to"},
    "customFields":{"href":"/projects/your-scrum-project/settings/custom_fields", "type":"text/html", "title":"Custom fields"},
    "configureForm":{"href":"/types/1/edit?tab=form_configuration", "type":"text/html", "title":"Configure form"},
    "activities":{"href":"/api/v3/work_packages/43/activities"},
    "availableWatchers":{"href":"/api/v3/work_packages/43/available_watchers"},
    "relations":{"href":"/api/v3/work_packages/43/relations"},
    "revisions":{"href":"/api/v3/work_packages/43/revisions"},
    "watchers":{"href":"/api/v3/work_packages/43/watchers"},
    "addWatcher":{"href":"/api/v3/work_packages/43/watchers", "method":"post", "payload":{"user":{"href":"/api/v3/users/{user_id}"}}, "templated":true},
    "removeWatcher":{"href":"/api/v3/work_packages/43/watchers/{user_id}", "method":"delete", "templated":true},
    "addRelation":{"href":"/api/v3/work_packages/43/relations", "method":"post", "title":"Add relation"},
    "addChild":{"href":"/api/v3/projects/your-scrum-project/work_packages", "method":"post", "title":"Add child of Test task"},
    "changeParent":{"href":"/api/v3/work_packages/43", "method":"patch", "title":"Change parent of Test task"},
    "addComment":{"href":"/api/v3/work_packages/43/activities", "method":"post", "title":"Add comment"},
    "previewMarkup":{"href":"/api/v3/render/markdown?context=/api/v3/work_packages/43", "method":"post"},
    "timeEntries":{"href":"/api/v3/time_entries?filters=%5B%7B%22work_package_id%22%3A%7B%22operator%22%3A%22%3D%22%2C%22values%22%3A%5B%2243%22%5D%7D%7D%5D", "title":"Time entries"},
    "ancestors":[],
    "category":{"href":"None"},
    "type":{"href":"/api/v3/types/1", "title":"Task"},
    "priority":{"href":"/api/v3/priorities/8", "title":"Normal"},
    "project":{"href":"/api/v3/projects/2", "title":"Scrum project"},
    "status":{"href":"/api/v3/statuses/1", "title":"New"},
    "author":{"href":"/api/v3/users/4", "title":"Darren MacKenzie"},
    "responsible":{"href":"None"},
    "assignee":{"href":"None"},
    "version":{"href":"None"},
    "parent":{"href":"None", "title":"None"},
    "customActions":[],
    "meetings":{"href":"/work_packages/43/tabs/meetings", "title":"meetings"},
    "github":{"href":"/work_packages/43/tabs/github", "title":"github"},
    "github_pull_requests":{"href":"/api/v3/work_packages/43/github_pull_requests", "title":"GitHub pull requests"},
    "gitlab":{"href":"/work_packages/43/tabs/gitlab", "title":"gitlab"},
    "gitlab_merge_requests":{"href":"/api/v3/work_packages/43/gitlab_merge_requests", "title":"Gitlab merge requests"},
    "gitlab_issues":{"href":"/api/v3/work_packages/43/gitlab_issues", "title":"Gitlab Issues"},
    "convertBCF":{"href":"/api/bcf/2.1/projects/your-scrum-project/topics", "title":"Convert to BCF", "payload":{"reference_links":["/api/v3/work_packages/43"]}, "method":"post"}
}

work_package = {
    "_type":"WorkPackage",
    "id":43,
    "lockVersion":1,
    "subject":"Test task",
    "description":{"format":"markdown", "raw":"Updating description.", "html":"<p class=\"op-uc-p\">Updating description.</p>"},
    "scheduleManually":false,
    "startDate":"None",
    "dueDate":"None",
    "derivedStartDate":"None",
    "derivedDueDate":"None",
    "estimatedTime":"None",
    "derivedEstimatedTime":"None",
    "derivedRemainingTime":"None",
    "duration":"None",
    "ignoreNonWorkingDays":false,
    "percentageDone":"None",
    "derivedPercentageDone":"None",
    "createdAt":"2025-01-28T12:24:17.520Z",
    "updatedAt":"2025-01-28T12:26:33.351Z",
    "readonly":false,
    "_embedded": _embedded,
    "_links": _links
}

work_package_created = {
    "action":"work_package:created",
    "work_package": work_package
}