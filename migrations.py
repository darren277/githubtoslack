""""""
import asyncio
from llm.rag.lib import RAG, DBConfig
from settings import SURREALDB_NS, SURREALDB_DB, SURREALDB_USER, SURREALDB_PASS, SURREALDB_HOST, SURREALDB_POR
from settings import OPENPROJECT_API_KEY, OP_PORT


rag = RAG("wiki", DBConfig(SURREALDB_NS, SURREALDB_DB, SURREALDB_USER, SURREALDB_PASS, SURREALDB_HOST, SURREALDB_PORT))

async def migrate_test_data():
    await rag.insert("This is a test about cats.", {"file": "test1.txt", "tags": ["test", "cats"]})
    await rag.insert("This is a test about dogs", {"file": "test2.txt", "tags": ["test", "dogs"]})
    await rag.insert("This is a test about birds.", {"file": "test3.txt", "tags": ["test", "birds"]})
    await rag.insert("This is a test about fish.", {"file": "test4.txt", "tags": ["test", "fish"]})

    await rag.insert("This is a test about cats and dogs.", {"file": "test5.txt", "tags": ["test", "cats", "dogs"]})
    await rag.insert("This is a test about dogs and birds.", {"file": "test6.txt", "tags": ["test", "dogs", "birds"]})
    await rag.insert("This is a test about birds and fish.", {"file": "test7.txt", "tags": ["test", "birds", "fish"]})
    await rag.insert("This is a test about fish and cats.", {"file": "test8.txt", "tags": ["test", "fish", "cats"]})


class WikiPage:
    def __init__(self, id: int, title: str):
        self.id = id
        self.title = title


async def migrate_wiki_data(project_id: int):
    from pyopenproject.openproject import OpenProject
    from pyopenproject.model.project import Project

    op = OpenProject(url=f"http://localhost:{OP_PORT}", api_key=OPENPROJECT_API_KEY)

    wiki_pages_service = op.get_wiki_page_service()

    print(wiki_pages_service.__dir__())

    found = wiki_pages_service.find(
        WikiPage(project_id, 'TOC')
    )

    print(found)


async def test_search(query: str):
    results = await rag.search(query)
    try:
        result = results[1].get('result')
        for r in result:
            print(r)
    except:
        print("Something went wrong", results)


async def main():
    await rag.connect()

    # await rag.migrate_table_schema()

    await migrate_test_data()

    q = "cats"
    print(f'results for search of: "{q}"')
    await test_search(q)

    q = "dogs"
    print(f'results for search of: "{q}"')
    await test_search(q)

#asyncio.run(main())

async def migrate_wiki():
    await rag.connect()

    await migrate_wiki_data(2)

asyncio.run(migrate_wiki())
