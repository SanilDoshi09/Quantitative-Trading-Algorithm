import os
import logging
import psycopg2

from dotenv import load_dotenv
from contextlib import contextmanager
from ..logger import set_logger



logger = set_logger("database")

class Database:

    def __init__(self):
        load_dotenv()
        self.db_params = {
            'dbname': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASS'),
            'host': os.getenv('DB_HOST'),
            'port': os.getenv('DB_PORT')
        }
        logger.info("Database object initialized")

    @contextmanager
    def get_connection(self):
        # '**': unpacks the dictionary into keyword arguments
        logger.debug("Connecting to database")
        conn = psycopg2.connect(**self.db_params)
        try:
            yield conn # yield is like return, but for generators 
            # (excution is paused and resumed witin a 'with' block)
        except psycopg2.DatabaseError as e:
            logger.warning(f"Database connection failed: {e}")
            raise
        finally:
            conn.close()
            logger.debug("Database connection closed")

    def execute_query(self, query, params=None):
        # excutes single query
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
                logger.info("Executed query successfully")

    def execute_queries(self, queries):
        # executes multiple queries (good for batch operations)
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                for query in queries:
                    if query.strip():
                        cursor.execute(query)
                        print(cursor.statusmessage)
                conn.commit()
                logger.info("Executed queries successfully")
    
    def read_sql(self, filepath):
        # read multiple queries from sql files
        try:
            with open(filepath, 'r') as file:
                file_content = file.read()
                queries = file_content.split(';')
            logger.info(f"SQL file {filepath} read successfully") 
            return [query.strip() for query in queries if query.strip()]
        except IOError as e:
            logger.error(f"Error reading SQL file: {e}")  
            raise
