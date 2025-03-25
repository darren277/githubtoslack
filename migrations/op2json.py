""""""
from settings import OPENPROJECT_URL, OPENPROJECT_API_KEY, OP_JSON_OUTPUT_PATH
from pyopenproject.openproject import OpenProject
import pyopenproject

import json

op = OpenProject(url=OPENPROJECT_URL, api_key=OPENPROJECT_API_KEY)


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

def extract_schema():
    all_projects = op.get_project_service().find_all()

    schemas = []
    for project in all_projects:
        project_id = project.id

        types_url = project._links.types.href
        project_types = op.conn.get(types_url)._embedded.elements

        for t in project_types:
            type_id = t.id
            schema_url = f"/api/v3/projects/{project_id}/types/{type_id}/schema"
            schema = op.conn.get(schema_url)
            schemas.append({
                "project_id": project_id,
                "type_id": type_id,
                "schema": schema
            })
    with open(f"{OP_JSON_OUTPUT_PATH}schemas.json", "w") as f:
        json.dump(schemas, f, indent=2)

extract_schema()
quit(54)



def serialize_custom_option(custom_option: pyopenproject.model.custom_object.CustomObject):
    d = dict()
    try:
        d.update(
            _type=custom_option._type,
            id=custom_option.id,
            name=custom_option.name,
            position=custom_option.position,
            color=custom_option.color,
            _links=custom_option._links
        )
    except Exception as e:
        print(f"Failed to serialize custom option. {e}")
        breakpoint()
    return d


def serialize_custom_field(custom_field: pyopenproject.model.custom_field.CustomField):
    d = dict()
    try:
        d.update(
            _type=custom_field._type,
            id=custom_field.id,
            name=custom_field.name,
            position=custom_field.position,
            fieldType=custom_field.fieldType,
            possibleValues=custom_field.possibleValues,
            _links=custom_field._links
        )
    except Exception as e:
        print(f"Failed to serialize custom field. {e}")
        breakpoint()
    return d

def export_custom_fields_and_custom_options():
    print("WARNING: WHAT IS CUSTOM FIELD?")
    try:
        custom_fields = op.get_custom_field_service().find_all()
    except Exception as e:
        print(f"Failed to export custom fields. {e}")
        breakpoint()
        return

    custom_field_data = [serialize_custom_field(custom_field) for custom_field in custom_fields]

    data = []

    for field in custom_field_data:
        field_id = field['id']
        try:
            custom_options = op.get_custom_object_service().find(field_id)
        except Exception as e:
            print(f"Failed to export custom options. {e}")
            breakpoint()
            return
        data.append(dict(custom_field=field, custom_options=[serialize_custom_option(custom_option) for custom_option in custom_options]))

    try:
        with open(f"{OP_JSON_OUTPUT_PATH}custom_fields_and_options.json", "w") as f: json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Failed to write custom options to file. {e}")
        breakpoint()
        return


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
    except Exception as e:
        print(f"Failed to serialize work package. {e}")
        breakpoint()
    return d

def export_work_packages():
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


def serialize_project(project: pyopenproject.model.project.Project):
    # ['_type', 'id', 'identifier', 'name', 'active', 'public', 'description', 'createdAt', 'updatedAt', 'statusExplanation', '_links',
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
        _links=project._links
    )


def export_projects():
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


def export_all():
    try:
        export_custom_fields_and_custom_options()
    except Exception as e:
        print(f"Failed to export custom fields and custom options. {e}")

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

    print("Export complete.")

