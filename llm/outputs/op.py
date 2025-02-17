""""""
from settings import PROJECT_IDS_DICT
from pydantic import BaseModel
from pyopenproject.model import WorkPackage, Project

class WorkPackageOutput(BaseModel):
    title: str
    description: str
    priority: int
    start_date: str
    due_date: str
    estimate_time: str

    def _fmt(self):
        return dict(
            title=self.title,
            description=self.description,
            start_date=self.start_date,
            due_date=self.due_date,
            estimated_time=self.estimate_time,
            priority=self.priority
        )

class Task(WorkPackageOutput):
    ...



def parse_task(project, title, attrs):
    kwargs = dict()
    _links = dict()

    description = attrs.get('description', dict(format='markdown', raw='Description TBD.', html='<p class="op-uc-p">Description TBD.</p>'))

    _type = attrs.get('type', Task)
    if _type: _links['type'] = dict(href=f"/api/v3/types/{_type.id}")

    priority = attrs.get('priority', Normal)
    if priority: _links['priority'] = dict(href=f"/api/v3/priorities/{priority.id}")

    status = attrs.get('status', Status(1, 'New', False, '#1098AD', True))
    if status: _links['status'] = dict(href=f"/api/v3/statuses/{status.id}")

    author: int = attrs.get('author', None)
    if author: _links['author'] = dict(href=f"/api/v3/users/{author}")

    assignee: int = attrs.get('assignee', None)
    if assignee: _links['assignee'] = dict(href=f"/api/v3/users/{assignee}")

    responsible: int = attrs.get('responsible', None)
    if responsible: _links['responsible'] = dict(href=f"/api/v3/users/{responsible}")

    due_date = attrs.get('dueDate', None)
    if due_date: kwargs['dueDate'] = due_date

    start_date = attrs.get('startDate', None)
    if start_date: kwargs['startDate'] = start_date

    estimated_time = attrs.get('estimatedTime', None)
    if estimated_time: kwargs['estimatedTime'] = estimated_time

    p = dict(href=f"/api/v3/projects/{project.id}", title=project.name)

    d = dict(subject=title, project=p, description=description, _links=_links, **kwargs)

    return d


def create_new_task(title: str, project_name: str, **attrs):
    task = None

    '''
    :param title:
    :param project_name:
    :param attrs:
        :description: dict(format='markdown', raw='Description TBD.', html='<p class="op-uc-p">Description TBD.</p>')
        :startDate: str
        :dueDate: str
        :estimatedTime: str
        :assignee: int
        :responsible: int
        :priority: Priority
        :type: WorkPackageType
        :status: Status
    :return:
    '''
    project_id = PROJECT_IDS_DICT[project_name]
    project = Project(dict(id=project_id))
    try:
        project = op.get_project_service().find(project)
        if project is None:
            raise Exception(f"Project not found: {project_name}")
    except Exception as e:
        raise Exception(f"Failed to fetch project. {e}")
    try:
        d = parse_task(project, title, attrs)

        print(f"About to create task ({title}) with data: {d}")

        wp = WorkPackage(d)

        task = op.get_work_package_service().create(wp)

        if task is None:
            raise Exception(f"Failed to create task: {title}")
    except BusinessError as e:
        direct_cause = e.__cause__
        if isinstance(direct_cause, RequestError):
            try:
                error_json = direct_cause.args[0]

                print("Caught direct cause (MultipleErrors) with JSON:", error_json)

                line2 = error_json.split('\n')[1].lstrip().rstrip()

                j = json.loads(line2)

                errorIdentifier = j['errorIdentifier']

                print(f"Error Identifier: {errorIdentifier}")

                message = j['message']

                print(f"Error: {message}")

                errors = j['_embedded']['errors']

                for error in errors:
                    print(f"--- Error: {error['message']}")

            except Exception:
                pass
    except Exception as e:
        raise Exception(f"Failed to create task. {e}")
    return task
