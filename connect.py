import os
from contextlib import contextmanager
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "aldb.lmmsys.cl"),
    "port": int(os.getenv("DB_PORT", "5434")),
    "user": os.getenv("DB_USER", "aaron.cancino"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "aaron_cancino_test"),
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

@contextmanager
def db_cursor(dictionary=False):
    conn = get_connection()
    cur = conn.cursor(dictionary=dictionary)
    try:
        yield conn, cur
    finally:
        cur.close(); conn.close()
