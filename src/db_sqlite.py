import os
import sqlite3

DB_PATH = os.getenv("SQLITE_PATH", "data/local.db")

# Caminho absoluto para a pasta migrations na raiz do projeto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MIGRATIONS_PATH = os.path.join(BASE_DIR, "migrations")

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    return conn

def init_db():
    """
    Executa todos os scripts SQL dentro da pasta migrations/
    para criar tabelas caso não existam.
    """
    if not os.path.exists(MIGRATIONS_PATH):
        raise FileNotFoundError(f"Pasta migrations não encontrada: {MIGRATIONS_PATH}")

    conn = get_connection()
    cursor = conn.cursor()

    sql_files = sorted(f for f in os.listdir(MIGRATIONS_PATH) if f.endswith(".sql"))

    for sql_file in sql_files:
        script_path = os.path.join(MIGRATIONS_PATH, sql_file)
        with open(script_path, "r", encoding="utf-8") as f:
            sql = f.read()
            cursor.executescript(sql)
    
    conn.commit()
    conn.close()

def get_cities():
    """Retorna todas as cidades como lista de dicionários"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, state, country_id, latitude, longitude FROM City")
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "id": r[0],
            "name": r[1],
            "state": r[2],
            "country_id": r[3],
            "latitude": r[4],
            "longitude": r[5]
        } for r in rows
    ]