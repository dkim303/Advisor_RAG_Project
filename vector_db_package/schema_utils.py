import sqlalchemy as sa
import json
import pandas as pd
import numpy as np
import pyodbc
import yaml
import requests
import psycopg
import io
from psycopg import sql
import logging
from sentence_transformers import SentenceTransformer

def check_table_exists(cur: psycopg.Cursor, schema: str, table: str) -> bool:
    query = """
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = %s
              AND table_name = %s
        );
    """

    cur.execute(query, (schema, table))
    return cur.fetchone()[0]


def get_table_columns(cur: psycopg.Cursor, schema: str, table: str) -> list[str]:
    query = """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = %s
          AND table_name = %s
        ORDER BY ordinal_position;
    """

    cur.execute(query, (schema, table))
    rows = cur.fetchall()

    return [row[0] for row in rows]


def get_missing_columns(df: pd.DataFrame, table_coluns: list[str]) -> list[str]:
    df_columns = set(df.columns)
    table_columns_set = set(table_coluns)

    missing_columns = table_columns_set - df_columns

    return list(missing_columns)


def get_advisors(cur: psycopg.Cursor) -> list[str]:
    query = """
        SELECT name
        FROM Project.advisors
        ORDER BY name;
    """

    cur.execute(query)
    rows = cur.fetchall()

    return [row[0] for row in rows]


def advisor_exists(cur: psycopg.Cursor, names_list: list[str], name: str) -> bool:
    if name is None or name.strip() == "":
        raise ValueError("Advisor Name List is Empty")

    if name in names_list:
        return True
    else:
        return False


def create_new_advisor(cur: psycopg.Cursor, name: str, description: str = None, config: str = None) -> None:
    try:
        if name is None or name.strip() == "":
            raise ValueError("Empty Name")
        
        if isinstance(config, dict):
            config = json.dumps(config)
        
        query = """
            INSERT INTO project.advisors (name, description, config)
            VALUES (%s, %s, %s)
            RETURNING advisor_id;
        """
        cur.execute(query, (name, description, config))
        cur.commit()
        logging.info(f"Created new advisor: {name}")
        
    except Exception as e:
        logging.error(f"Failed to create new advisor: {e}")
        raise