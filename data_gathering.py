from bs4 import BeautifulSoup
import numpy as np
from sentence_transformers import SentenceTransformer
from vector_db_package import utils
import requests
import json
import sys
from pathlib import Path
import os
import logging
import time
import pandas as pd
import numpy as np
import psycopg

from vector_db_package.ETL_utils import (
    get_config,
    get_connection
    get_advisors,
    create_new_advisor,
    check_table_exists,
)

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def main(config_file: str):
    # initialize paths and files for logging
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    LOG_DIR = os.path.join(BASE_DIR, "logs")
    #makes logs directory if it DNE, exists_ok=True prevents error if it already exis
    os.makedirs(LOG_DIR, exist_ok=True)
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")

    LOG_FILE = os.path.join(LOG_DIR, f"Database_{timestamp}.log")
    logging.basicConfig(
        filename=LOG_FILE,
        level = logging.INFO,
        format = "%(asctime)s - %(levelname)s - %(name)s - %(filename)s:%(lineno)d - %(message)s"
    )
    logging.info("Program Started")
    run_status = "Failure"
    is_ended = False

    try:
        sql_information = get_config(config_file)
        conn, cur = get_connection(sql_information)

        while not is_ended:
            print("Enter URL: ")

            
        run_status = "Success"

    except Exception as e:
        run_status = "Failure"
    finally:
        logging.info("Terminating Program")
        conn.close()
        cur.close()

if __name__ == "__main__":
    main()