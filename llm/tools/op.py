""""""

""" WIKI SEARCH TOOL """

async def search(rag, query: str):
    await rag.connect()

    results = await rag.search(query)

    return results

async def search_wiki(project_name: str, query: str):
    # Placeholder implementation
    ###logger.debug(f"Searching {project_name} Wiki for {query}...")
    print((f"Searching {project_name} Wiki for {query}..."))

    from llm.rag.lib import RAG, DBConfig
    from settings import SURREALDB_NS, SURREALDB_DB, SURREALDB_USER, SURREALDB_PASS, SURREALDB_HOST, SURREALDB_PORT
    from settings import OPENPROJECT_API_KEY, OP_PORT

    rag = RAG("wiki", DBConfig(SURREALDB_NS, SURREALDB_DB, SURREALDB_USER, SURREALDB_PASS, SURREALDB_HOST, SURREALDB_PORT))

    results = await search(rag, query)

    try:
        result = results[1].get('result')
        print('results from search_wiki()')
        for r in result:
            print(r)
        top_result = result[0].get('chunk_text', 'Something went wrong or maybe no results.')
    except:
        print("Something went wrong", results)
        top_result = "Something went wrong."

    return top_result



search_wiki_tool = {
    "type": "function",
    "function": {
        "name": "search_wiki",
        "description": "Searches the project's wiki for a given query",
        "parameters": {
            "type": "object",
            "properties": {
                "project_name": {
                    "type": "string",
                    "description": "The name of the project to search"
                },
                "query": {
                    "type": "string",
                    "description": "The search query"
                }
            },
            "required": ["project_name", "query"]
        }
    }
}


""" WORK PACKAGE CREATION TOOL """
from settings import USERS_LOOKUP_TABLE, PRIORITIES
from llm.outputs.op import create_new_task

def create_work_package(title: str, description: str = None, start_date: str = None, due_date: str = None, estimated_time: str = None,
                        assignee: str = None, responsible: str = None, priority: str = None):
    kwargs = dict()

    description = dict(format='markdown', raw=description, html=f'<p class="op-uc-p">{description}</p>') if description else dict(format='markdown', raw='Description TBD.', html='<p class="op-uc-p">Description TBD.</p>')
    kwargs['description'] = description

    if start_date: kwargs['startDate'] = start_date # '2025-01-22',
    if due_date: kwargs['dueDate'] = due_date # '2025-01-24',
    if estimated_time: kwargs['estimatedTime'] = estimated_time # 'PT1H' (1 hour),
    if assignee: kwargs['assignee'] = USERS_LOOKUP_TABLE.get(assignee)
    if responsible: kwargs['responsible'] = USERS_LOOKUP_TABLE.get(responsible)

    # TODO: Get this working properly. Defaults to High or Normal while ther are other options available.
    if priority: kwargs['priority'] = High if PRIORITIES.get(priority) == 9 else Normal

    try:
        create_new_task(
            title,
            'Scrum project',
            **kwargs,
            #type=Task
            # TODO: category=...,
        )
    except Exception as e:
        return f"Error creating work package: {e}"

    return f"Work package created successfully: {title}"


create_work_package_tool = {
    "type": "function",
    "function": {
        "name": "create_work_package",
        "description": "Creates a new work package in the project",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "The title of the work package"
                },
                "description": {
                    "type": "string",
                    "description": "The description of the work package"
                },
                "start_date": {
                    "type": "string",
                    "description": "The start date of the work package"
                },
                "due_date": {
                    "type": "string",
                    "description": "The due date of the work package"
                },
                "estimated_time": {
                    "type": "string",
                    "description": "The estimated time to complete the work package"
                },
                "assignee": {
                    "type": "string",
                    "description": "The assignee of the work package"
                },
                "responsible": {
                    "type": "string",
                    "description": "The responsible person for the work package"
                },
                "priority": {
                    "type": "string",
                    "description": "The priority of the work package"
                }
            },
            "required": ["title"]
        }
    }
}


""" WORK PACKAGE OUTPUT TOOL """
provide_work_package_output_tool = {
    "type": "function",
    "function": {
        "name": "provide_work_package_output",
        "description": "Returns structured work package output in JSON format according to the Pydantic schema.",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "The final title of the work package"},
                "description": {"type": "string", "description": "The final description"},
                "priority": {"type": "integer", "description": "The final numeric priority"},
                "start_date": {"type": "string", "description": "The final start date"},
                "due_date": {"type": "string", "description": "The final due date"},
                "estimate_time": {"type": "string", "description": "The final estimated time in ISO8601 duration format or hours"},
            },
            "required": [
                "title",
                "description",
                "priority",
                "start_date",
                "due_date",
                "estimate_time"
            ]
        }
    }
}
