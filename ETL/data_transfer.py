import sqlalchemy as sa
import json
import pandas as pd
import numpy as np
import yaml
import requests
import logging
import psycopg

logger = logging.getLogger(__name__)

def main(config_file: str) -> int:
    run_status = "Failure"
    num_migrated = 0

    try:

        logger.info("Begginign data migration process")

        # Read YAML file for information:
        with open(config_file, "r") as config:
            config_info = yaml.safe_load(config)

            sql_database = config_info.get("database_name")
            sql_embeddings_table = config_info.get("e_table")
            sql_paragraphs_table = config_info.get()
            sql_uid = config_info.get("username")
            sql_pwd = config_info.get("password")

            # Ensure all information is valid
            if any(x is None for x in (sql_database, sql_embeddings_table, sql_paragraphs_table, sql_uid, sql_pwd)):
                raise("Critical Error: invalid config file information")

            conn = psycopg.connect(
                    host="localhost",
                    port=5432,
                    dbname="rag_db",
                    user="postgres",
                    password="your_password")
            
            cur = conn.cursor()

    except Exception as e:
        logger.error(e)

    finally:
        logger.info(f"Migration End Status: {run_status}")
        logger.info(f"Total data points migrated: {num_migrated}")

        # Close SQL Server API connections
        cur.close()
        conn.close()

if __name__ == "__main__":
    main()