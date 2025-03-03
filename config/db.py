from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool
from dotenv import load_dotenv
import os
from os import environ

class PGDB:
    def __init__(self):
        load_dotenv()

        host = environ.get('POSTGRES_HOST')
        port = environ.get('POSTGRES_PORT')
        user = environ.get('POSTGRES_USER')
        passw = environ.get('POSTGRES_PASS')
        db = environ.get('POSTGRES_DATABASE')

        if not all([host, port, user, passw, db]):
            raise ValueError("Missing required environment variables for PostgreSQL connection")

        connect_str = f"postgresql+psycopg2://{user}:{passw}@{host}:{port}/{db}"
        self.engine = create_engine(connect_str, pool_size=5, max_overflow=10, poolclass=QueuePool)

        if not self.engine:
            raise ValueError("Failed to connect to Postgres database")

    def execute(self, statement: str):
        with self.engine.connect() as connection:
            cursor = connection.execute(text(statement))
            result = cursor.fetchall()
            cursor.close()
            return result

class SQLiteDB:
    def __init__(self):
        self.dir_path = os.path.abspath("py_tool_data")
        self.db_path = os.path.join(self.dir_path, "sqlite.db")

        if not os.path.exists(self.dir_path):
            os.makedirs(self.dir_path)

        if not os.path.exists(self.db_path):
            open(self.db_path, 'w').close()

        connect_str = f"sqlite:///sqlite.db"
        self.engine = create_engine(connect_str, pool_size=5, max_overflow=10, poolclass=QueuePool)

        if not self.engine:
            raise ValueError("Failed to connect to Postgres database")

    def execute(self, statement: str):
        with self.engine.connect() as connection:
            cursor = connection.execute(text(statement))
            result = cursor.fetchall()
            cursor.close()
            return result

