""""""
from settings import OPENPROJECT_URL, OPENPROJECT_API_KEY
from pyopenproject.openproject import OpenProject
import pyopenproject

import json

JSON_OUTPUT_PATH = "output/op/"

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


def export_custom_fields_and_custom_options():
    raise NotImplementedError

    data = build_query(url)

    with open(f"{JSON_OUTPUT_PATH}custom_fields.json", "w") as f:
        json.dump(data, f, indent=2)


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
    try:
        queries = op.get_query_service().find_all()
    except Exception as e:
        print(f"Failed to export queries. {e}")
        breakpoint()
        return

    data = [serialize_query(query) for query in queries]

    with open(f"{JSON_OUTPUT_PATH}queries.json", "w") as f:
        json.dump(data, f, indent=2)


def export_work_packages():
    try:
        work_packages = op.get_work_package_service().find_all()
    except Exception as e:
        print(f"Failed to export work packages. {e}")
        breakpoint()
        return

    #for wp in work_packages: print(wp)

    data = work_packages

    try:
        with open(f"{JSON_OUTPUT_PATH}work_packages.json", "w") as f: json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Failed to write work packages to file. {e}")
        breakpoint()
        return


def export_attachments():
    raise NotImplementedError

    data = build_query(url)

    try:
        with open(f"{JSON_OUTPUT_PATH}attachments.json", "w") as f: json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Failed to write attachments to file. {e}")
        breakpoint()
        return


def export_comments_in_journal():
    raise NotImplementedError

    data = build_query(url)

    with open(f"{JSON_OUTPUT_PATH}comments_in_journal.json", "w") as f:
        json.dump(data, f, indent=2)


def export_work_package_configurations_and_project_configurations():
    raise NotImplementedError

    data = build_query(url)

    with open(f"{JSON_OUTPUT_PATH}work_package_configurations.json", "w") as f:
        json.dump(data, f, indent=2)


def export_journals():
    raise NotImplementedError

    data = build_query(url)

    with open(f"{JSON_OUTPUT_PATH}journals.json", "w") as f:
        json.dump(data, f, indent=2)


def export_relations():
    try:
        s = op.get_relation_service()
        relations = s.find_all()
    except Exception as e:
        print(f"Failed to export relations. {e}")
        breakpoint()
        return
    #for relation in relations: print(relation)

    #data = [relation.__dict__ for relation in relations]
    data = relations

    try:
        with open(f"{JSON_OUTPUT_PATH}relations.json", "w") as f: json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Failed to write relations to file. {e}")
        breakpoint()
        return


def export_types():
    try:
        data = op.get_type_service().find_all()
    except Exception as e:
        print(f"Failed to export types. {e}")
        breakpoint()
        return

    #for t in data: print(t)

    try:
        with open(f"{JSON_OUTPUT_PATH}types.json", "w") as f: json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Failed to write types to file. {e}")
        breakpoint()
        return


def export_project_roles():
    raise NotImplementedError

    data = build_query(url)

    with open(f"{JSON_OUTPUT_PATH}project_roles.json", "w") as f:
        json.dump(data, f, indent=2)


def export_versions():
    # Work Packages can be assigned to a version.
    # As such, versions serve to group Work Packages into logical units where each group comprises all the work packages that needs to be finished in order for the version to be finished.

    try:
        versions = op.get_version_service().find_all()
    except Exception as e:
        print(f"Failed to export versions. {e}")
        breakpoint()
        return

    #for version in versions: print(version)

    data = versions

    try:
        with open(f"{JSON_OUTPUT_PATH}versions.json", "w") as f: json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Failed to write versions to file. {e}")
        breakpoint()
        return


def export_users():
    try:
        users = op.get_user_service().find_all()
    except Exception as e:
        print(f"Failed to export users. {e}")
        breakpoint()
        return

    #for user in users: print(user)

    #data = [user.__dict__ for user in users]
    data = users

    try:
        with open(f"{JSON_OUTPUT_PATH}users.json", "w") as f: json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Failed to write users to file. {e}")
        breakpoint()
        return


def export_projects():
    try:
        project = op.get_project_service().find_all()
    except Exception as e:
        print(f"Failed to export projects. {e}")
        breakpoint()
        return

    #for p in project: print(p)

    data = project

    try:
        with open(f"{JSON_OUTPUT_PATH}projects.json", "w") as f: json.dump(data, f, indent=2)
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

