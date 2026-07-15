import os
import psycopg2

POSTGRES_HOST = os.environ["DB_HOST"]
POSTGRES_DB = os.environ["DB_NAME"]
POSTGRES_USER = os.environ["DB_USER"]
POSTGRES_PASSWORD = os.environ["DB_PASSWORD"]
POSTGRES_PORT = int(os.environ["DB_PORT"])


def get_connection():
    return psycopg2.connect(
        host=POSTGRES_HOST,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        port=POSTGRES_PORT,
    )