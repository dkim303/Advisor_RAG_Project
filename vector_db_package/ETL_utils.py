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

logger = logging.getLogger(__name__)

def get_config(config_file: str):
    # Read YAML file for information:
    with open(config_file, "r") as config:
        config_info = yaml.safe_load(config)

        sql_host = config_info.get("host_name")
        sql_port = config_info.get("port")
        sql_database = config_info.get("database_name")
        sql_uid = config_info.get("username")
        sql_pwd = config_info.get("password")

        # Ensure all information is valid
        if any(x is None for x in (sql_host, sql_port, sql_database, sql_uid, sql_pwd)):
            raise("Critical Error: invalid config file information")

    return config_info


def get_connection(config_info: dict) -> tuple:
    host = config_info.get("host_name")
    port = config_info.get("port")
    dbname = config_info.get("database_name")
    user = config_info.get("username")
    password = config_info.get("password")

    conn = psycopg.connect(
            host = host,
            port = port,
            dbname = dbname,
            user = user,
            password = password)
    
    cur = conn.cursor()
    return conn, cur


def check_table_exists(cur: psycopg.cursor, schema: str, table: str) -> bool:
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


def df_insert(cur: psycopg.cursor, df: pd.DataFrame, schema: str, table: str) -> None:
    try:
        if df is None:
            raise ValueError("Error: Attempted to Insert None as DataFrame")

        if df.empty:
            raise ValueError("Error: Attempted to Insert Empty DataFrame")
        
        if not check_table_exists(cur, schema, table):
            raise ValueError("Error: Attempted to Insert DataFrame to Nonexistant Table")

        columns = list(df.columns)
        
        buffer = io.StringIO()

        df[columns].to_csv(
            buffer,
            index=False,
            header=False,
            na_rep="\\N"   # PostgreSQL NULL marker
        )

        buffer.seek(0)

        copy_query = sql.SQL("""
            COPY {} ({})
            FROM STDIN
            WITH (
                FORMAT CSV,
                NULL '\\N'
            )
            """).format(
                sql.Identifier(schema, table),
                sql.SQL(", ").join(sql.Identifier(col) for col in columns)
        )

        with cur.copy(copy_query) as copy:
            copy.write(buffer.getvalue())
        
    except Exception as e:
        logging.error(f"Dataframe Insertion Failure")
        logging.error(f"{e}")


def get_advisors(cur: psycopg.cursor) -> list[str]:
    query = """
        SELECT name
        FROM Project.advisors
        ORDER BY name;
    """

    cur.execute(query)
    rows = cur.fetchall()

    return [row[0] for row in rows]


def create_new_advisor(cur, name: str, description: str = None, config: str = None) -> None:
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
        logger.info(f"Created new advisor: {name}")
        
    except Exception as e:
        logging.error(f"Failed to create new advisor: {e}")
        raise