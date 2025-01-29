""""""


def search_wiki(project_name: str, query: str):
    # Placeholder implementation
    logger.debug(f"Searching {project_name} Wiki for {query}...")
    return f"Search results for {query} in {project_name} Wiki"



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
