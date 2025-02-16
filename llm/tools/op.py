""""""

async def search(rag, query: str):
    await rag.connect()

    results = await rag.search(query)

    return results

def search_wiki(project_name: str, query: str):
    # Placeholder implementation
    ###logger.debug(f"Searching {project_name} Wiki for {query}...")
    print((f"Searching {project_name} Wiki for {query}..."))

    import asyncio
    from llm.rag.lib import RAG, DBConfig
    from settings import SURREALDB_NS, SURREALDB_DB, SURREALDB_USER, SURREALDB_PASS, SURREALDB_HOST, SURREALDB_PORT
    from settings import OPENPROJECT_API_KEY, OP_PORT

    rag = RAG("wiki", DBConfig(SURREALDB_NS, SURREALDB_DB, SURREALDB_USER, SURREALDB_PASS, SURREALDB_HOST, SURREALDB_PORT))

    results = asyncio.run(search(rag, query))

    try:
        result = results[1].get('result')
        print('results from search_wiki()')
        for r in result:
            print(r)
    except:
        print("Something went wrong", results)

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
