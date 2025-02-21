""""""
import json
from sentence_transformers import SentenceTransformer

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

        self.llm_client = None

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

    def build_vector_query(self, text: str, use_remote: bool = False):
        if use_remote:
            response = self.llm_client.embeddings.create(input=text, model="text-embedding-3-small")
            embedding = response.data[0].embedding
            embedding_string = json.dumps(embedding)
        else:
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

    async def search(self, text: str, use_remote: bool = False):
        v_q = self.build_vector_query(text, use_remote=use_remote)
        return await self.query(v_q)

