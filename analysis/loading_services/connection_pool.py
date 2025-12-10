import psycopg2
import psycopg2.pool
from contextlib import contextmanager
import os

dbpool = psycopg2.pool.ThreadedConnectionPool(
    host = os.environ['DB_HOST_IP'],
    port = os.environ['DB_PORT'],
    dbname = 'program_data',
    user = os.environ['DB_USERNAME'],
    password = os.environ['DB_PASSWORD'],
    minconn = 1,
    maxconn = 100
)

@contextmanager
def db_cursor():
    conn = dbpool.getconn()
    try:
        with conn.cursor() as cur:
            yield cur
            conn.commit()
    except:
        conn.rollback()
        raise
    finally:
        dbpool.putconn(conn)