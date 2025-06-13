""""""
from settings import OPENPROJECT_URL, OPENPROJECT_API_KEY
from pyopenproject.openproject import OpenProject

JSON_OUTPUT_PATH = "output/op/"

op = OpenProject(url=OPENPROJECT_URL, api_key=OPENPROJECT_API_KEY)


def import_work_packages():
    with open(f"{JSON_OUTPUT_PATH}work_packages.json", "r") as f:
        data = json.load(f)

    for wp in data:
        print(wp)

        op.get_work_package_service().create(wp)


def import_projects():
    with open(f"{JSON_OUTPUT_PATH}projects.json", "r") as f:
        data = json.load(f)

    for p in data:
        print(p)

        op.get_project_service().create(p)


def import_users():
    with open(f"{JSON_OUTPUT_PATH}users.json", "r") as f:
        data = json.load(f)

    for user in data:
        print(user)

        op.get_user_service().create(user)


def import_versions():
    with open(f"{JSON_OUTPUT_PATH}versions.json", "r") as f:
        data = json.load(f)

    for version in data:
        print(version)

        op.get_version_service().create(version)


def import_types():
    with open(f"{JSON_OUTPUT_PATH}types.json", "r") as f:
        data = json.load(f)

    for t in data:
        print(t)

        op.get_type_service().create(t)


def import_relations():
    with open(f"{JSON_OUTPUT_PATH}relations.json", "r") as f:
        data = json.load(f)

    for relation in data:
        print(relation)

        op.get_relation_service().create(relation)


def import_journals():
    ...


def import_work_package_configurations_and_project_configurations():
    ...


def import_comments_in_journal():
    ...


def import_attachments():
    ...


def import_queries():
    with open(f"{JSON_OUTPUT_PATH}queries.json", "r") as f:
        data = json.load(f)

    for query in data:
        print(query)

        op.get_query_service().create(query)



def import_all():
    try:
        import_custom_fields_and_custom_options()
    except Exception as e:
        print(f"Failed to import custom fields and custom options. {e}")

    try:
        import_queries()
    except Exception as e:
        print(f"Failed to import queries. {e}")

    try:
        import_work_packages()
    except Exception as e:
        print(f"Failed to import work packages. {e}")

    try:
        import_attachments()
    except Exception as e:
        print(f"Failed to import attachments. {e}")

    try:
        import_comments_in_journal()
    except Exception as e:
        print(f"Failed to import comments in journal. {e}")

    try:
        import_work_package_configurations_and_project_configurations()
    except Exception as e:
        print(f"Failed to import work package configurations and project configurations. {e}")

    try:
        import_journals()
    except Exception as e:
        print(f"Failed to import journals. {e}")

    try:
        import_relations()
    except Exception as e:
        print(f"Failed to import relations. {e}")

    try:
        import_types()
    except Exception as e:
        print(f"Failed to import types. {e}")

    try:
        import_project_roles()
    except Exception as e:
        print(f"Failed to import project roles. {e}")

    try:
        import_versions()
    except Exception as e:
        print(f"Failed to import versions. {e}")

    try:
        import_users()
    except Exception as e:
        print(f"Failed to import users. {e}")

    try:
        import_projects()
    except Exception as e:
        print(f"Failed to import projects. {e}")

    print("Import complete.")
