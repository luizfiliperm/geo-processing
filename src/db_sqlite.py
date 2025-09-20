# db_sqlite.py
import os
import sqlite3

def get_connection():
    """
    Retorna uma conexão SQLite para o arquivo definido em SQLITE_PATH
    """
    DB_PATH = os.getenv("SQLITE_PATH", "data/local.db")
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    return conn
