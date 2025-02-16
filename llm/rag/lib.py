""""""
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

    def connect(self):
        self.client = surrealdb.Surreal(f"http://{self.db_config.host}:{self.db_config.port}/rpc")
        self.client.signin({"user": self.db_config.user, "password": self.db_config.password})
        self.client.use(self.db_config.namespace, self.db_config.database)

    def migrate_table_schema(self):
        table_schema = f'''
DEFINE TABLE {self.table_name} SCHEMAFULL;

DEFINE FIELD {self.table_name}.embedding TYPE array<float>;    -- The embedding vector
DEFINE FIELD {self.table_name}.chunk_text TYPE string;         -- Raw text for this chunk
DEFINE FIELD {self.table_name}.metadata TYPE object;           -- Extra metadata (file name, headings, tags, etc.)
        '''

        self.client.query(table_schema)

    def insert(self, chunk_text: str, metadata: dict):
        embedding = self.transformer.encode(chunk_text)
        self.client.query(f"INSERT INTO {self.table_name} (embedding, chunk_text, metadata) VALUES ({embedding}, '{chunk_text}', {metadata})")

    def query(self, vector_query: str):
        return self.client.query(vector_query)

    def build_vector_query(self, text: str):
        embedding = self.transformer.encode(text)

        v_q = f'''
        LET $query_vector = {embedding};

        SELECT id,
               chunk_text,
               vector::similarity::cosine(embedding, $query_vector) AS sim
        FROM {self.table_name}
        ORDER BY sim DESC
        LIMIT 5;
        '''

        return v_q

    def search(self, text: str):
        v_q = self.build_vector_query(text)
        return self.query(v_q)


rag = RAG("wiki", DBConfig(SURREALDB_NS, SURREALDB_DB, SURREALDB_USER, SURREALDB_PASS, SURREALDB_HOST, SURREALDB_PORT))
rag.connect()

# rag.migrate_table_schema()

def migrate_test_data():
    rag.insert("This is a test about cats.", {"file": "test1.txt", "tags": ["test", "cats"]})
    rag.insert("This is a test about dogs", {"file": "test2.txt", "tags": ["test", "dogs"]})
    rag.insert("This is a test about birds.", {"file": "test3.txt", "tags": ["test", "birds"]})
    rag.insert("This is a test about fish.", {"file": "test4.txt", "tags": ["test", "fish"]})

    rag.insert("This is a test about cats and dogs.", {"file": "test5.txt", "tags": ["test", "cats", "dogs"]})
    rag.insert("This is a test about dogs and birds.", {"file": "test6.txt", "tags": ["test", "dogs", "birds"]})
    rag.insert("This is a test about birds and fish.", {"file": "test7.txt", "tags": ["test", "birds", "fish"]})
    rag.insert("This is a test about fish and cats.", {"file": "test8.txt", "tags": ["test", "fish", "cats"]})

def test_search():
    results = rag.search("cats")
    print(results)


migrate_test_data()
test_search()


