""""""
import json
from sentence_transformers import SentenceTransformer

SURREALDB_NS = "gptstuff"
SURREALDB_DB = "op"

SURREALDB_USER = "root"
SURREALDB_PASS = "root"

SURREALDB_HOST = "localhost"
SURREALDB_PORT = 8011

import surrealdb


## SURREALDB VECTOR STORE ##

class DBConfig:
    def __init__(self, namespace: str, database: str, user: str, password: str, host: str, port: int):
        self.namespace = namespace
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port

class RAG:
    def __init__(self, table_name: str, db_config: DBConfig, transformer: str = 'sentence-transformers/all-mpnet-base-v2'):
        self.table_name = table_name
        self.db_config = db_config
        self.client = None
        self.transformer = SentenceTransformer(transformer)

    async def connect(self):
        self.client = surrealdb.Surreal(f"ws://{self.db_config.host}:{self.db_config.port}/rpc")
        await self.client.connect()
        await self.client.use(self.db_config.namespace, self.db_config.database)
        await self.client.signin({"user": self.db_config.user, "pass": self.db_config.password})

    def migrate_table_schema(self):
        table_schema = f'''
DEFINE TABLE {self.table_name} SCHEMAFULL;

DEFINE FIELD {self.table_name}.embedding TYPE array<float>;    -- The embedding vector
DEFINE FIELD {self.table_name}.chunk_text TYPE string;         -- Raw text for this chunk
DEFINE FIELD {self.table_name}.metadata TYPE object;           -- Extra metadata (file name, headings, tags, etc.)
        '''

        self.client.query(table_schema)

    async def insert(self, chunk_text: str, metadata: dict):
        embedding = self.transformer.encode(chunk_text)

        embedding_string = json.dumps(embedding.tolist())

        await self.client.query(f"INSERT INTO {self.table_name} (embedding, chunk_text, metadata) VALUES ({embedding_string}, '{chunk_text}', {metadata})")

    async def query(self, vector_query: str):
        return await self.client.query(vector_query)

    def build_vector_query(self, text: str):
        embedding = self.transformer.encode(text)

        embedding_string = json.dumps(embedding.tolist())

        v_q = f'''
        LET $query_vector = {embedding_string};

        SELECT id,
               chunk_text,
               vector::similarity::cosine(embedding, $query_vector) AS sim
        FROM {self.table_name}
        ORDER BY sim DESC
        LIMIT 5;
        '''

        return v_q

    async def search(self, text: str):
        v_q = self.build_vector_query(text)
        return await self.query(v_q)


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

async def test_search():
    results = await rag.search("cats")
    print(results)


import asyncio

async def main():
    await rag.connect()

    # await rag.migrate_table_schema()

    await migrate_test_data()

    await test_search()

asyncio.run(main())



