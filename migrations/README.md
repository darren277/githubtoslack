From the feature description:

```
Migration of all Jira Projects, including:
- Project details (name, key, URL, project type, project category, Project avatar)
- Ticket data (description, comments -> including author and date/time) 
- Issue Types (Task, Sub-Task, Bug, Epic, Story, etc.)
- Default Fields (Type, Priority, Components, Label, Status, Resolution, 
Assignee, Reporter, Watchers, Created Date, Updated Date, Issue Links, Epic)
- Custom Fields
- Workflows
- Components
- Priorities
- Versions
- Labels (are global in Jira, not project-related)
- Assignment of ticket users (creator, assignee) based on username
- Specification of a fallback user for migration if Jira 
ticket user is not found in OpenProject
```

```
What we explicitly do NOT see as part of this migration:

- User and roles, Permissions, Issue Security
- Notifications
- E-Mail interfaces (inbound/outbound)
- individual user settings, Dashboards and saved views
- Kanban Boards (nice to have though)
```

https://community.openproject.org/projects/openproject/work_packages/35007/activity
