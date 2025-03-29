""""""
from settings import OPENPROJECT_URL, OPENPROJECT_API_KEY, OP_JSON_OUTPUT_PATH, ALREADY_TESTED
from pyopenproject.openproject import OpenProject
import pyopenproject

import json

op = OpenProject(url=OPENPROJECT_URL, api_key=OPENPROJECT_API_KEY)


def custom_request(api_user: str, api_key: str, url_path: str):
    '''
    A utility function for those hard to reach places...

    :param api_user:
    :param api_key:
    :param url_path:
    :return:
    '''

    import requests

    headers = {
        "Accept": "application/json"
    }

    from requests.auth import HTTPBasicAuth
    auth = HTTPBasicAuth(api_user, api_key)

    response = requests.request(
        "GET",
        f"{OPENPROJECT_URL}{url_path}",
        headers=headers,
        auth=auth
    )

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None

    return response.json()



'''
PAGINATION
----------

API: Collections

Whenever a client calls a resource that can return more than one element, it will receive a collection of elements. However as collections can become quite large, the API will not simply return a JSON array, but a special collection object that will contain the actual elements in its embedded property elements.

Collections may be paginated, this means that a single response from the server will not contain all elements of the collection, but only a subset. In this case the client can issue further requests to retrieve the remaining elements. There are two ways to access the result pages of a paginated collection:

    offset based pagination

    cursor based pagination

The available ways of pagination depend on the collection queried. Some collections feature no pagination at all, meaning they will always return all elements. Others might only offer one of the two pagination methods or both of them.

A collection also carries meta information like the total count of elements in the collection or - in case of a paginated collection - the amount of elements returned in this response and action links to retrieve the remaining elements.
Local Properties
Property 	Description 	Type 	Availability
total 	The total amount of elements available in the collection 	Integer 	always
pageSize 	Amount of elements that a response will hold 	Integer 	when paginated
count 	Actual amount of elements in this response 	Integer 	always
offset 	The page number that is requested from paginated collection 	Integer 	when offset based available
groups 	Summarized information about aggregation groups 	Object 	when grouping
totalSums 	Aggregations of supported values for elements of the collection 	Object 	when showing sums
'''

custom_project_fields = dict()
already_seen_schema_href = set()



def serialize_query(query: pyopenproject.model.query.Query):
    return dict(
        _type=query._type,
        starred=query.starred,
        id=query.id,
        name=query.name,
        createdAt=query.createdAt,
        updatedAt=query.updatedAt,
        filters=query.filters,
        includeSubprojects=query.includeSubprojects,
        sums=query.sums,
        public=query.public,
        hidden=query.hidden,
        timelineVisible=query.timelineVisible,
        showHierarchies=query.showHierarchies,
        timelineZoomLevel=query.timelineZoomLevel,
        timelineLabels=query.timelineLabels,
        timestamps=query.timestamps,
        highlightingMode=query.highlightingMode,
        _links=query._links
    )

def export_queries():
    if 'queries' in ALREADY_TESTED:
        raise Exception("ALREADY TESTED QUERIES SO SKIPPING...")
    try:
        queries = op.get_query_service().find_all()
    except Exception as e:
        print(f"Failed to export queries. {e}")
        breakpoint()
        return

    data = [serialize_query(query) for query in queries]

    with open(f"{OP_JSON_OUTPUT_PATH}queries.json", "w") as f:
        json.dump(data, f, indent=2)


def export_project_schema():
    if 'project_schema' in ALREADY_TESTED:
        raise Exception("ALREADY TESTED PROJECT SCHEMA SO SKIPPING...")

    try:
        project_schema = op.get_project_service().find_schema().__dict__
    except Exception as e:
        print(f"Failed to export project schema. {e}")
        breakpoint()
        return

    with open(f"{OP_JSON_OUTPUT_PATH}project_schema.json", "w") as f:
        json.dump(project_schema, f, indent=2)

    for key, val in project_schema.items():
        if key.startswith('customField'):
            custom_project_fields.update({key: val})



""" WORK PACKAGES """

def extract_work_package_schema(schema_href: str):
    conn = op.conn
    api_key, api_user = conn.api_key, conn.api_user

    if schema_href in already_seen_schema_href:
        print(f"Already seen schema href: {schema_href}")
        return

    schema = custom_request(api_user, api_key, schema_href)

    # for key, val in schema.items():
    #     if key.startswith('customField'):
    #         cf = schema[key]
    #         for key, val in cf.items():
    #             print(key, val)

    already_seen_schema_href.add(schema_href)

    schema_identifier = schema_href.split('/')[-1]

    # mkdir if does not exist...
    import os
    if not os.path.exists(f"{OP_JSON_OUTPUT_PATH}/wp_schema"):
        os.makedirs(f"{OP_JSON_OUTPUT_PATH}/wp_schema")

    with open(f"{OP_JSON_OUTPUT_PATH}/wp_schema/{schema_identifier}.json", "w") as f:
        json.dump(schema, f, indent=2)

def extract_work_package_activities(work_package: pyopenproject.model.work_package.WorkPackage):
    try:
        activities = op.get_work_package_service().find_activities(work_package)
    except Exception as e:
        print(f"Failed to extract work package activities. {e}")
        breakpoint()
        return

    # Serializing directly as is for now...
    data = [activity.__dict__ for activity in activities]

    return data


def extract_work_package_attachments(work_package: pyopenproject.model.work_package.WorkPackage):
    try:
        attachments = op.get_work_package_service().find_attachments(work_package)
    except Exception as e:
        print(f"Failed to extract work package attachments. {e}")
        breakpoint()
        return

    # Serializing directly as is for now...
    data = [attachment.__dict__ for attachment in attachments]

    return data


def extract_work_package_revisions(work_package: pyopenproject.model.work_package.WorkPackage):
    try:
        revisions = op.get_work_package_service().find_revisions(work_package)
    except Exception as e:
        print(f"Failed to extract work package revisions. {e}")
        breakpoint()
        return

    # Serializing directly as is for now...
    data = [revision.__dict__ for revision in revisions]

    return data


def serialize_derived(d):
    new_d = dict()
    if getattr(d, 'derivedStartDate', None): new_d['derivedStartDate'] = d.derivedStartDate
    if getattr(d, 'derivedDueDate', None): new_d['derivedDueDate'] = d.derivedDueDate
    if getattr(d, 'derivedEstimatedTime', None): new_d['derivedEstimatedTime'] = d.derivedEstimatedTime
    if getattr(d, 'derivedRemainingTime', None): new_d['derivedRemainingTime'] = d.derivedRemainingTime
    if getattr(d, 'derivedPercentageDone', None): new_d['derivedPercentageDone'] = d.derivedPercentageDone
    return new_d

def serialize_work_package(wp: pyopenproject.model.work_package.WorkPackage):
    d = dict()
    try:
        if getattr(wp, 'startDate', None): d.update(startDate = wp.startDate)
        if getattr(wp, 'dueDate', None): d.update(dueDate = wp.dueDate)
        if getattr(wp, 'duration', None): d.update(duration = wp.duration)
        d.update(
            **serialize_derived(wp),
            _type=wp._type,
            id=wp.id,
            lockVersion=wp.lockVersion,
            subject=wp.subject,
            description=wp.description,
            scheduleManually=wp.scheduleManually,
            estimatedTime=wp.estimatedTime,
            ignoreNonWorkingDays=wp.ignoreNonWorkingDays,
            percentageDone=wp.percentageDone,
            createdAt=wp.createdAt,
            updatedAt=wp.updatedAt,
            _links=wp._links
        )

        try:
            custom_fields = dict()
            for key, val in wp.__dict__.items():
                if key.startswith('customField'):
                    custom_fields.update({key: val})
            d.update(custom_fields=custom_fields)
        except Exception as e:
            print(f"Failed to serialize work package custom fields. {e}")
            breakpoint()

        try:
            d.update(activities=extract_work_package_activities(wp))
        except Exception as e:
            print(f"Failed to serialize work package activities. {e}")
            breakpoint()

        try:
            d.update(attachments=extract_work_package_attachments(wp))
        except Exception as e:
            print(f"Failed to serialize work package attachments. {e}")
            breakpoint()

        try:
            d.update(revisions=extract_work_package_revisions(wp))
        except Exception as e:
            print(f"Failed to serialize work package revisions. {e}")
            breakpoint()

        try:
            schema_href = wp._links['schema']['href']
            extract_work_package_schema(schema_href)
        except Exception as e:
            print(f"Failed to extract work package schema. {e}")
            breakpoint()

    except Exception as e:
        print(f"Failed to serialize work package. {e}")
        breakpoint()
    return d

def export_work_packages():
    '''
    This function is for exporting ALL work packages.
    For exporting work packages specific to a particular project, use extract_project_work_packages() [called by serialize_project()].
    :return:
    '''
    if 'work_packages' in ALREADY_TESTED:
        raise Exception("ALREADY TESTED WORK PACKAGES SO SKIPPING...")
    try:
        work_packages = op.get_work_package_service().find_all()
    except Exception as e:
        print(f"Failed to export work packages. {e}")
        breakpoint()
        return

    #for wp in work_packages: print(wp)

    data = [serialize_work_package(wp) for wp in work_packages]

    try:
        with open(f"{OP_JSON_OUTPUT_PATH}work_packages.json", "w") as f: json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Failed to write work packages to file. {e}")
        breakpoint()
        return


def export_attachments():
    raise NotImplementedError

    data = build_query(url)

    try:
        with open(f"{OP_JSON_OUTPUT_PATH}attachments.json", "w") as f: json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Failed to write attachments to file. {e}")
        breakpoint()
        return


def export_comments_in_journal():
    raise NotImplementedError

    data = build_query(url)

    with open(f"{OP_JSON_OUTPUT_PATH}comments_in_journal.json", "w") as f:
        json.dump(data, f, indent=2)


def export_work_package_configurations_and_project_configurations():
    raise NotImplementedError

    data = build_query(url)

    with open(f"{OP_JSON_OUTPUT_PATH}work_package_configurations.json", "w") as f:
        json.dump(data, f, indent=2)


def export_journals():
    raise NotImplementedError

    data = build_query(url)

    with open(f"{OP_JSON_OUTPUT_PATH}journals.json", "w") as f:
        json.dump(data, f, indent=2)


def serialize_relation(relation: pyopenproject.model.relation.Relation):
    return dict(
        _type=relation._type,
        id=relation.id,
        name=relation.name,
        type=relation.type,
        reverseType=relation.reverseType,
        lag=relation.lag,
        description=relation.description,
        _links=relation._links
    )


def export_relations():
    if 'relations' in ALREADY_TESTED:
        raise Exception("ALREADY TESTED RELATIONS SO SKIPPING...")
    try:
        s = op.get_relation_service()
        relations = s.find_all()
    except Exception as e:
        print(f"Failed to export relations. {e}")
        breakpoint()
        return
    #for relation in relations: print(relation)

    #data = [relation.__dict__ for relation in relations]
    data = [serialize_relation(relation) for relation in relations]

    try:
        with open(f"{OP_JSON_OUTPUT_PATH}relations.json", "w") as f: json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Failed to write relations to file. {e}")
        breakpoint()
        return


def serialize_type(t: pyopenproject.model.type.Type):
    return dict(
        _type=t._type,
        id=t.id,
        name=t.name,
        color=t.color,
        position=t.position,
        isDefault=t.isDefault,
        isMilestone=t.isMilestone,
        createdAt=t.createdAt,
        updatedAt=t.updatedAt,
        _links=t._links
    )

def export_types():
    if 'types' in ALREADY_TESTED:
        raise Exception("ALREADY TESTED TYPES SO SKIPPING...")
    try:
        data = op.get_type_service().find_all()
    except Exception as e:
        print(f"Failed to export types. {e}")
        breakpoint()
        return

    #for t in data: print(t)
    data = [serialize_type(t) for t in data]

    try:
        with open(f"{OP_JSON_OUTPUT_PATH}types.json", "w") as f: json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Failed to write types to file. {e}")
        breakpoint()
        return



def serialize_role(role: pyopenproject.model.role.Role):
    d = dict()
    try:
        d.update(
            _type=role._type,
            id=role.id,
            name=role.name,
            _links=role._links
        )
    except Exception as e:
        print(f"Failed to serialize role. {e}")
        breakpoint()
    return dict()

def export_project_roles():
    if 'project_roles' in ALREADY_TESTED:
        raise Exception("ALREADY TESTED PROJECT ROLES SO SKIPPING...")
    try:
        data = op.get_role_service().find_all()
    except Exception as e:
        print(f"Failed to export project roles. {e}")
        breakpoint()
        return

    data = [serialize_role(role) for role in data]

    try:
        with open(f"{OP_JSON_OUTPUT_PATH}project_roles.json", "w") as f: json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Failed to write project roles to file. {e}")
        breakpoint()
        return


def serialize_version(version: pyopenproject.model.version.Version):
    return dict(
        _type=version._type,
        id=version.id,
        name=version.name,
        description=version.description,
        startDate=version.startDate,
        endDate=version.endDate,
        status=version.status,
        sharing=version.sharing,
        createdAt=version.createdAt,
        updatedAt=version.updatedAt,
        _links=version._links
    )

def export_versions():
    if 'versions' in ALREADY_TESTED:
        raise Exception("ALREADY TESTED VERSIONS SO SKIPPING...")
    # Work Packages can be assigned to a version.
    # As such, versions serve to group Work Packages into logical units where each group comprises all the work packages that needs to be finished in order for the version to be finished.

    try:
        versions = op.get_version_service().find_all()
    except Exception as e:
        print(f"Failed to export versions. {e}")
        breakpoint()
        return

    #for version in versions: print(version)

    data = [serialize_version(version) for version in versions]

    try:
        with open(f"{OP_JSON_OUTPUT_PATH}versions.json", "w") as f: json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Failed to write versions to file. {e}")
        breakpoint()
        return


def serialize_user(user: pyopenproject.model.user.User):
    return dict(
        _type=user._type,
        id=user.id,
        name=user.name,
        createdAt=user.createdAt,
        updatedAt=user.updatedAt,
        login=user.login,
        admin=user.admin,
        firstName=user.firstName,
        lastName=user.lastName,
        email=user.email,
        avatar=user.avatar,
        status=user.status,
        identityUrl=user.identityUrl,
        language=user.language,
        _links=user._links
    )

def export_users():
    if 'users' in ALREADY_TESTED:
        raise Exception("ALREADY TESTED USERS SO SKIPPING...")
    try:
        users = op.get_user_service().find_all()
    except Exception as e:
        print(f"Failed to export users. {e}")
        breakpoint()
        return

    #for user in users: print(user)

    #data = [user.__dict__ for user in users]
    data = [serialize_user(user) for user in users]

    try:
        with open(f"{OP_JSON_OUTPUT_PATH}users.json", "w") as f: json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Failed to write users to file. {e}")
        breakpoint()
        return


def extract_project_work_package_types(project: pyopenproject.model.project.Project):
    try:
        types = op.get_project_service().find_types(project)
    except Exception as e:
        print(f"Failed to extract project work package types. {e}")
        breakpoint()
        return

    data = [serialize_type(t) for t in types]

    return data


def extract_project_work_packages(project: pyopenproject.model.project.Project):
    try:
        work_packages = op.get_project_service().find_work_packages(project)
    except Exception as e:
        print(f"Failed to extract project work packages. {e}")
        breakpoint()
        return

    data = [serialize_work_package(wp) for wp in work_packages]

    try:
        with open(f"{OP_JSON_OUTPUT_PATH}{project.identifier}_work_packages.json", "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Failed to write work packages to file. {e}")
        breakpoint()
        return

    return work_packages

def serialize_project(project: pyopenproject.model.project.Project):
    # ['_type', 'id', 'identifier', 'name', 'active', 'public', 'description', 'createdAt', 'updatedAt', 'statusExplanation', '_links',

    try:
        project_custom_fields = dict()
        for key, val in project.__dict__.items():
            if key.startswith('customField'):
                project_custom_fields.update({key: val})
    except Exception as e:
        print(f"Failed to serialize project custom fields. {e}")
        breakpoint()
        return

    try:
        project_work_package_types = extract_project_work_package_types(project)
    except Exception as e:
        print(f"Failed to extract project work package types. {e}")
        breakpoint()
        return


    return dict(
        _type=project._type,
        id=project.id,
        identifier=project.identifier,
        name=project.name,
        active=project.active,
        public=project.public,
        description=project.description,
        createdAt=project.createdAt,
        updatedAt=project.updatedAt,
        statusExplanation=project.statusExplanation,
        _links=project._links,
        custom_fields=project_custom_fields,
        work_package_types=project_work_package_types
    )


def export_projects():
    if 'projects' in ALREADY_TESTED:
        raise Exception("ALREADY TESTED PROJECTS SO SKIPPING...")
    try:
        project = op.get_project_service().find_all()
    except Exception as e:
        print(f"Failed to export projects. {e}")
        breakpoint()
        return

    #for p in project: print(p)

    data = [serialize_project(p) for p in project]

    try:
        with open(f"{OP_JSON_OUTPUT_PATH}projects.json", "w") as f: json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Failed to write projects to file. {e}")
        breakpoint()
        return


def serialize_grid_widget(grid_widget):
    # ['_type', 'id', 'identifier', 'startRow', 'endRow', 'startColumn', 'endColumn', 'options']
    return dict(
        _type=grid_widget._type,
        id=grid_widget.id,
        identifier=grid_widget.identifier,
        startRow=grid_widget.startRow,
        endRow=grid_widget.endRow,
        startColumn=grid_widget.startColumn,
        endColumn=grid_widget.endColumn,
        options=grid_widget.options
    )

def serialize_grid(grid: pyopenproject.model.grid.Grid):
    # ['_type', 'id', 'name', 'rowCount', 'columnCount', 'options', 'widgets', 'createdAt', 'updatedAt', '_links']
    return dict(
        _type=grid._type,
        id=grid.id,
        name=grid.name,
        rowCount=grid.rowCount,
        columnCount=grid.columnCount,
        options=grid.options,
        widgets=[serialize_grid_widget(widget) for widget in grid.widgets],
        createdAt=grid.createdAt,
        updatedAt=grid.updatedAt,
        _links=grid._links
    )


def export_grids():
    if 'grids' in ALREADY_TESTED:
        raise Exception("ALREADY TESTED GRIDS SO SKIPPING...")
    try:
        grids = op.get_grid_service().find_all()
    except Exception as e:
        print(f"Failed to export grids. {e}")
        breakpoint()
        return

    data = [grid.__dict__ for grid in grids]

    try:
        with open(f"{OP_JSON_OUTPUT_PATH}grids.json", "w") as f: json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Failed to write grids to file. {e}")
        breakpoint()
        return


# get_priority_service()
# get_status_service()
# get_category_service()
# get_role_service()
# get_memberships_service()
# get_group_service()
# get_news_service()
# get_time_entry_service()
# get_activity_service()
# get_revision_service()

# wiki?


def export_all():
    try:
        export_project_schema()
    except Exception as e:
        print(f"Failed to export project schema. {e}")

    try:
        export_queries()
    except Exception as e:
        print(f"Failed to export queries. {e}")

    try:
        export_work_packages()
    except Exception as e:
        print(f"Failed to export work packages. {e}")

    try:
        export_attachments()
    except Exception as e:
        print(f"Failed to export attachments. {e}")

    try:
        export_comments_in_journal()
    except Exception as e:
        print(f"Failed to export comments in journal. {e}")

    try:
        export_work_package_configurations_and_project_configurations()
    except Exception as e:
        print(f"Failed to export work package configurations and project configurations. {e}")

    try:
        export_journals()
    except Exception as e:
        print(f"Failed to export journals. {e}")

    try:
        export_relations()
    except Exception as e:
        print(f"Failed to export relations. {e}")

    try:
        export_types()
    except Exception as e:
        print(f"Failed to export types. {e}")

    try:
        export_project_roles()
    except Exception as e:
        print(f"Failed to export project roles. {e}")

    try:
        export_versions()
    except Exception as e:
        print(f"Failed to export versions. {e}")

    try:
        export_users()
    except Exception as e:
        print(f"Failed to export users. {e}")

    try:
        export_projects()
    except Exception as e:
        print(f"Failed to export projects. {e}")

    try:
        export_grids()
    except Exception as e:
        print(f"Failed to export grids. {e}")

    print("Export complete.")

