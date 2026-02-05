import os
import json
import psycopg2
from psycopg2.extras import execute_values

def get_conn(): # conecta c postgres
    conn_str = os.getenv("PG_CONN")
    if not conn_str:
        raise RuntimeError("Missing env var PG_CONN")
    return psycopg2.connect(conn_str) 

def insert_json_rows(table: str, ingestion_date, rows: list[dict]):
    """
    Insert rows into staging table with schema: (ingestion_date date, payload jsonb, ingested_at default now()).
    """
    if not rows:
        return 0

    values = [(ingestion_date, json.dumps(r, ensure_ascii=False)) for r in rows]

    sql = f"INSERT INTO {table} (ingestion_date, payload) VALUES %s"
    with get_conn() as conn:
        with conn.cursor() as cur:
            execute_values(cur, sql, values, page_size=1000)
        conn.commit()
    return len(rows)
